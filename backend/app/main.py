import os
import uuid
import pathlib
import time
import traceback
from typing import List, Optional, Tuple

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import requests
import math
import hashlib
import fnmatch
import chromadb
import base64
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import asyncio
import re
from html import unescape
from urllib.parse import quote
import subprocess
import tempfile
import shutil

load_dotenv()

# ---------------------------------------------------------------------
# Env & constants
# ---------------------------------------------------------------------

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama_ollama:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")

# Optional OpenAI embeddings config. If `OPENAI_API_KEY` is set, we use
# OpenAI embeddings (defaults to `text-embedding-3-large`). This lets you
# use a dedicated embedding model while keeping Ollama for chat/LLM.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_URL = os.getenv("OPENAI_URL", "https://api.openai.com/v1").rstrip("/")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")
OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
LOG_FULL_EMBEDDINGS = os.getenv("LOG_FULL_EMBEDDINGS", "false").lower() in ("1", "true", "yes")
EMBED_PREVIEW_COUNT = int(os.getenv("EMBED_PREVIEW_COUNT", "8"))

# SINGLE ROOT DIRECTORY: all .md files are under /app/wiki_files
WIKI_ROOT = os.getenv("WIKI_DIR", "/app/wiki_files")

CHROMA_DIR = os.getenv("CHROMA_DIR", "/app/chroma_db")

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
COLLECTION_NAME = "wiki_rag"
MEMORY_COLLECTION_NAME = "wiki_memories"

# Special “image criteria” doc we know exists
IMAGE_CRITERIA_DOC_REL = "TA9-WIKI/IT/Add-an-image-to-criteria-in-4.x.md"

app = FastAPI(title="Wiki RAG API")


# ---------------------------------------------------------------------
# Embedding + LLM
# ---------------------------------------------------------------------

def embed_text(text: str) -> List[float]:
    snippet = text[:120].replace("\n", " ")
    # If OPENAI_API_KEY is present, call OpenAI embeddings API
    if OPENAI_API_KEY:
        print(f"[EMBED] Calling OpenAI embeddings model={OPENAI_EMBEDDING_MODEL} len={len(text)} snippet='{snippet}...'")
        start = time.time()
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
        body = {"model": OPENAI_EMBEDDING_MODEL, "input": text}
        try:
            resp = requests.post(f"{OPENAI_URL}/embeddings", json=body, headers=headers, timeout=120)
        except Exception as e:
            print(f"[EMBED][ERROR] Exception while calling OpenAI embeddings: {e}")
            traceback.print_exc()
            raise RuntimeError(f"Failed to call OpenAI embeddings: {e}")
        duration = time.time() - start
        print(f"[EMBED] OpenAI embeddings status={resp.status_code} took={duration:.2f}s")

        if resp.status_code != 200:
            print(f"[EMBED][ERROR] Non-200 from OpenAI embeddings: {resp.text[:400]}")
            raise RuntimeError(f"OpenAI embeddings error: {resp.text}")

        data = resp.json()
        # OpenAI embeddings are in data['data'][0]['embedding']
        try:
            emb = data["data"][0]["embedding"]
        except Exception as e:
            print(f"[EMBED][ERROR] Unexpected OpenAI response shape: {data}")
            raise RuntimeError(f"OpenAI embeddings response missing embedding: {e}")

        # Compute metadata for easier tracing: preview, length, norm, and hash
        preview = ",".join([f"{x:.6f}" for x in emb[:EMBED_PREVIEW_COUNT]])
        norm = math.sqrt(sum([x * x for x in emb]))
        h = hashlib.sha256(
            ",".join([f"{x:.6f}" for x in emb[:16]]).encode("utf-8")
        ).hexdigest()[:12]
        print(f"[EMBED] Got OpenAI embedding length={len(emb)} preview=[{preview}] norm={norm:.6f} hash={h}")
        if LOG_FULL_EMBEDDINGS:
            print(f"[EMBED][FULL] {emb}")
        return emb

    # Fallback: Ollama embeddings (original behavior)
    print(f"[EMBED] Calling Ollama embeddings len={len(text)} snippet='{snippet}...'")
    start = time.time()
    try:
        resp = requests.post(
            f"{OLLAMA_URL}/api/embeddings",
            json={"model": OLLAMA_MODEL, "prompt": text},
            timeout=120,
        )
    except Exception as e:
        print(f"[EMBED][ERROR] Exception while calling Ollama embeddings: {e}")
        traceback.print_exc()
        raise RuntimeError(f"Failed to call Ollama embeddings: {e}")
    duration = time.time() - start
    print(f"[EMBED] Ollama embeddings status={resp.status_code} took={duration:.2f}s")

    if resp.status_code != 200:
        print(f"[EMBED][ERROR] Non-200 from Ollama embeddings: {resp.text[:400]}")
        raise RuntimeError(f"Ollama embeddings error: {resp.text}")

    data = resp.json()
    if "embedding" not in data:
        print(f"[EMBED][ERROR] Missing 'embedding' key in response: {data}")
        raise RuntimeError(f"Ollama embeddings response missing 'embedding': {data}")

    emb = data["embedding"]
    # Compute metadata for easier tracing: preview, length, norm, and hash
    preview = ",".join([f"{x:.6f}" for x in emb[:EMBED_PREVIEW_COUNT]])
    norm = math.sqrt(sum([x * x for x in emb]))
    h = hashlib.sha256(
        ",".join([f"{x:.6f}" for x in emb[:16]]).encode("utf-8")
    ).hexdigest()[:12]
    print(f"[EMBED] Got embedding of length {len(emb)} preview=[{preview}] norm={norm:.6f} hash={h}")
    if LOG_FULL_EMBEDDINGS:
        print(f"[EMBED][FULL] {emb}")
    return emb


def call_llm(prompt: str) -> str:
    """Call LLM for final answer. Prefer OpenAI chat if key is set, otherwise use Ollama."""
    if OPENAI_API_KEY:
        print(f"[LLM] Calling OpenAI chat model={OPENAI_CHAT_MODEL} prompt_len={len(prompt)}")
        start = time.time()
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
        body = {
            "model": OPENAI_CHAT_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        }
        try:
            resp = requests.post(f"{OPENAI_URL}/chat/completions", json=body, headers=headers, timeout=600)
        except Exception as e:
            print(f"[LLM][ERROR] Exception while calling OpenAI chat: {e}")
            traceback.print_exc()
            raise RuntimeError(f"Failed to call OpenAI chat: {e}")
        duration = time.time() - start
        print(f"[LLM] OpenAI chat status={resp.status_code} took={duration:.2f}s")

        if resp.status_code != 200:
            print(f"[LLM][ERROR] Non-200 from OpenAI chat: {resp.text[:400]}")
            raise RuntimeError(f"OpenAI chat error: {resp.text}")

        try:
            data = resp.json()
            msg = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        except Exception as e:
            print(f"[LLM][ERROR] Unexpected OpenAI chat response: {resp.text[:400]}")
            traceback.print_exc()
            raise RuntimeError(f"OpenAI chat parse error: {e}")

        print(f"[LLM] Got OpenAI answer length={len(msg)}")
        return msg

    print(f"[LLM] Calling Ollama chat with prompt length={len(prompt)}")
    start = time.time()
    try:
        resp = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
            },
            timeout=600,
        )
    except Exception as e:
        print(f"[LLM][ERROR] Exception while calling Ollama chat: {e}")
        traceback.print_exc()
        raise RuntimeError(f"Failed to call Ollama chat: {e}")
    duration = time.time() - start
    print(f"[LLM] Ollama chat status={resp.status_code} took={duration:.2f}s")

    if resp.status_code != 200:
        print(f"[LLM][ERROR] Non-200 from Ollama chat: {resp.text[:400]}")
        raise RuntimeError(f"Ollama chat error: {resp.text}")

    data = resp.json()
    msg = data.get("message", {}).get("content", "").strip()
    print(f"[LLM] Got answer length={len(msg)}")
    return msg


# ---------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------

def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    print(f"[CHUNK] Splitting text len={len(text)} size={size} overlap={overlap}")
    chunks: List[str] = []
    start_idx = 0
    while start_idx < len(text):
        end = min(start_idx + size, len(text))
        chunk = text[start_idx:end].strip()
        if chunk:
            chunks.append(chunk)
        start_idx += size - overlap
    print(f"[CHUNK] Produced {len(chunks)} chunks")
    return chunks


# ---------------------------------------------------------------------
# Iterate ALL markdown files under WIKI_ROOT
# ---------------------------------------------------------------------

def iter_markdown_files():
    root = pathlib.Path(WIKI_ROOT)
    print(f"[FILES] Scanning for .md files under: {WIKI_ROOT}")
    if not root.exists():
        print(f"[FILES][WARN] WIKI_ROOT path does not exist: {WIKI_ROOT}")
        return
    for path in root.rglob("*.md"):
        if path.is_file():
            yield path


# ---------------------------------------------------------------------
# ChromaDB Setup
# ---------------------------------------------------------------------

print(f"[CHROMA] Initializing PersistentClient path={CHROMA_DIR}")
client = chromadb.PersistentClient(path=CHROMA_DIR)
print(f"[CHROMA] Getting/creating collection '{COLLECTION_NAME}'")
collection = client.get_or_create_collection(name=COLLECTION_NAME)
print(f"[CHROMA] Getting/creating memory collection '{MEMORY_COLLECTION_NAME}'")
memory_collection = client.get_or_create_collection(name=MEMORY_COLLECTION_NAME)

# ---------------------------------------------------------------------
# Azure DevOps config & helpers
# ---------------------------------------------------------------------

ADO_ORG = os.getenv("ADO_ORG")
ADO_PROJECT = os.getenv("ADO_PROJECT")
ADO_PAT = os.getenv("ADO_PAT")

def _ado_headers() -> dict:
    if not (ADO_ORG and ADO_PROJECT and ADO_PAT):
        raise RuntimeError("Azure DevOps is not configured. Set ADO_ORG, ADO_PROJECT, ADO_PAT env vars.")
    token = f":{ADO_PAT}"  # PAT used as password with empty username
    b64 = base64.b64encode(token.encode("utf-8")).decode("utf-8")
    return {
        "Authorization": f"Basic {b64}",
        "Content-Type": "application/json",
    }

def _ado_base() -> str:
    return f"https://dev.azure.com/{ADO_ORG}/{ADO_PROJECT}"

def ado_list_tickets(tag_contains: str = "CC") -> List[dict]:
    """Run WIQL and return a list of work items with details (id,title,state,tags,url)."""
    url = f"{_ado_base()}/_apis/wit/wiql?api-version=7.1-preview.2"
    # WIQL: State <> Closed and Tags contains tag_contains
    wiql = (
        "SELECT [System.Id] FROM WorkItems "
        "WHERE [System.TeamProject] = @project "
        "AND [System.State] <> 'Closed' "
        f"AND [System.Tags] CONTAINS '{tag_contains}' "
        "ORDER BY [System.ChangedDate] DESC"
    )
    try:
        resp = requests.post(url, json={"query": wiql}, headers=_ado_headers(), timeout=60)
    except Exception as e:
        print(f"[ADO][ERROR] WIQL call failed: {e}")
        traceback.print_exc()
        raise RuntimeError(f"ADO WIQL failed: {e}")
    if resp.status_code != 200:
        print(f"[ADO][ERROR] WIQL non-200: {resp.status_code} {resp.text[:300]}")
        raise RuntimeError(f"ADO WIQL error: {resp.text}")
    items = resp.json().get("workItems", [])
    ids = [str(it.get("id")) for it in items if it.get("id")]
    if not ids:
        return []

    # Fetch work item details
    det_url = f"{_ado_base()}/_apis/wit/workitems?ids={','.join(ids)}&$expand=all&api-version=7.1"
    det = requests.get(det_url, headers=_ado_headers(), timeout=60)
    if det.status_code != 200:
        print(f"[ADO][ERROR] workitems details non-200: {det.status_code} {det.text[:300]}")
        raise RuntimeError(f"ADO workitems details error: {det.text}")
    results = []
    for wi in det.json().get("value", []):
        fid = wi.get("id")
        flds = wi.get("fields", {})
        title = flds.get("System.Title", "")
        state = flds.get("System.State", "")
        tags = flds.get("System.Tags", "")
        web_url = f"https://dev.azure.com/{ADO_ORG}/{ADO_PROJECT}/_workitems/edit/{fid}"
        results.append({"id": fid, "title": title, "state": state, "tags": tags, "url": web_url})
    return results

def ado_check_access_by_id(work_item_id: int) -> bool:
    try:
        u = f"{_ado_base()}/_apis/wit/workitems/{work_item_id}?api-version=7.1"
        r = requests.get(u, headers=_ado_headers(), timeout=30)
        return r.status_code == 200
    except Exception:
        return False

def ado_parse_id_from_url(url: str) -> Optional[int]:
    try:
        # expected e.g. https://dev.azure.com/{org}/{project}/_workitems/edit/{id}
        parts = url.rstrip("/").split("/")
        return int(parts[-1])
    except Exception:
        return None

def ado_fetch_ticket_text(work_item_id: int) -> str:
    """Fetch main fields and comments to a single plain-text blob."""
    base = _ado_base()
    hdrs = _ado_headers()
    main = requests.get(f"{base}/_apis/wit/workitems/{work_item_id}?$expand=all&api-version=7.1", headers=hdrs, timeout=60)
    if main.status_code != 200:
        raise RuntimeError(f"ADO workitem fetch error: {main.text}")
    data = main.json()
    f = data.get("fields", {})
    title = f.get("System.Title", "")
    state = f.get("System.State", "")
    tags = f.get("System.Tags", "")
    desc = f.get("System.Description", "") or f.get("Microsoft.VSTS.TCM.ReproSteps", "") or ""

    # Convert possible HTML description to plain text for cleaner context
    def _strip_html(text: str) -> str:
        try:
            # Remove HTML tags and collapse whitespace
            txt = re.sub(r"<[^>]+>", " ", text or "")
            txt = unescape(txt)
            return " ".join(txt.split())
        except Exception:
            return text or ""

    desc = _strip_html(desc)

    comments_text = []
    try:
        c = requests.get(f"{base}/_apis/wit/workItems/{work_item_id}/comments?api-version=7.1-preview.3", headers=hdrs, timeout=60)
        if c.status_code == 200:
            for it in c.json().get("comments", []):
                txt = it.get("text", "")
                if txt:
                    comments_text.append(_strip_html(txt))
    except Exception as e:
        print(f"[ADO][WARN] comments fetch failed: {e}")

    blob = (
        f"Title: {title}\nState: {state}\nTags: {tags}\n\nDescription:\n{desc}\n\n"
        + ("Comments:\n" + "\n---\n".join(comments_text) if comments_text else "")
    ).strip()
    if not blob:
        blob = f"(Empty work item {work_item_id})"
    return blob


def collection_empty() -> bool:
    try:
        c = collection.count()
        print(f"[CHROMA] collection.count() = {c}")
        return c == 0
    except Exception as e:
        print(f"[CHROMA][ERROR] Failed to get collection count: {e}")
        traceback.print_exc()
        return True


def get_ingested_sources() -> List[str]:
    """
    Return the list of all 'source' values from collection metadatas.
    Used for 'only_missing' ingest mode.
    """
    try:
        print("[CHROMA] Fetching existing metadatas for ingested sources list")
        data = collection.get(include=["metadatas"])
        ingested = sorted({m["source"] for m in data["metadatas"] if m})
        print(f"[CHROMA] Found {len(ingested)} distinct sources already ingested")
        return ingested
    except Exception as e:
        print(f"[CHROMA][ERROR] Failed to get ingested sources: {e}")
        traceback.print_exc()
        return []


# ---------------------------------------------------------------------
# Azure DevOps Wiki API helpers
# ---------------------------------------------------------------------

def ado_list_wikis() -> List[dict]:
    """Return available wikis (id, name)."""
    url = f"{_ado_base()}/_apis/wiki/wikis?api-version=7.1"
    print(f"[ADO][WIKI] Fetching wikis from: {url}")
    try:
        hdrs = _ado_headers()
        print(f"[ADO][WIKI] Auth header set with PAT")
        r = requests.get(url, headers=hdrs, timeout=60)
    except Exception as e:
        print(f"[ADO][WIKI][ERROR] list wikis failed: {e}")
        traceback.print_exc()
        raise
    if r.status_code != 200:
        print(f"[ADO][WIKI][ERROR] list wikis non-200: {r.status_code}")
        print(f"[ADO][WIKI][ERROR] Response body: {r.text[:500]}")
        print(f"[ADO][WIKI][ERROR] Response headers: {r.headers}")
        raise RuntimeError(f"ADO list wikis error (status {r.status_code}): {r.text}")
    val = r.json().get("value", [])
    return [{"id": w.get("id"), "name": w.get("name")} for w in val]


def ado_get_wiki_id_by_name(name: Optional[str] = None) -> str:
    """Find a wiki id by name. If name is None, try project default '<PROJECT>.wiki'."""
    wikis = ado_list_wikis()
    if not wikis:
        raise RuntimeError("No wikis found in Azure DevOps")
    if name:
        for w in wikis:
            if str(w.get("name", "")) == name:
                return str(w.get("id"))
        raise RuntimeError(f"Wiki '{name}' not found. Available: {[w['name'] for w in wikis]}")
    # Fallback: exact project wiki name
    default_name = f"{ADO_PROJECT}.wiki"
    for w in wikis:
        if str(w.get("name", "")) == default_name:
            return str(w.get("id"))
    # If not found, just use the first wiki
    return str(wikis[0].get("id"))


def ado_wiki_get_pages_recursive(wiki_id: str, path: str = "/") -> List[dict]:
    """Fetch all pages under a path and return list of {path, content}.

    NOTE: The recursive list endpoint does NOT include content even with includeContent=true
    in many orgs. So we first fetch the tree to collect all paths, then fetch content per path.
    """
    norm_path = path if path.startswith("/") else f"/{path}"
    enc_path = quote(norm_path, safe="/")
    tree_url = f"{_ado_base()}/_apis/wiki/wikis/{wiki_id}/pages?path={enc_path}&recursionLevel=full&api-version=7.1"
    try:
        r = requests.get(tree_url, headers=_ado_headers(), timeout=120)
    except Exception as e:
        print(f"[ADO][WIKI][ERROR] get pages tree failed: {e}")
        traceback.print_exc()
        raise
    if r.status_code != 200:
        print(f"[ADO][WIKI][ERROR] get pages tree non-200: {r.status_code} {r.text[:300]}")
        raise RuntimeError(f"ADO wiki pages tree fetch error: {r.text}")

    data = r.json()
    all_paths: List[str] = []

    def _collect_paths(node: dict):
        p = node.get("path")
        if p and p != "/":
            all_paths.append(p)
        for sub in node.get("subPages", []):
            _collect_paths(sub)

    _collect_paths(data)
    print(f"[ADO][WIKI] Collected {len(all_paths)} page paths from tree")

    pages: List[dict] = []

    def _fetch_content(p: str) -> Optional[str]:
        enc = quote(p if p.startswith("/") else f"/{p}", safe="/")
        url = f"{_ado_base()}/_apis/wiki/wikis/{wiki_id}/pages?path={enc}&includeContent=true&api-version=7.1"
        try:
            rr = requests.get(url, headers=_ado_headers(), timeout=60)
        except Exception as e:
            print(f"[ADO][WIKI][WARN] fetch content failed for path='{p}': {e}")
            return None
        if rr.status_code != 200:
            # Some nodes are containers only; ignore non-200 for them
            print(f"[ADO][WIKI][WARN] content non-200 for path='{p}': {rr.status_code}")
            return None
        try:
            return rr.json().get("content", "")
        except Exception:
            return None

    for p in all_paths:
        content = _fetch_content(p)
        if content and content.strip():
            pages.append({"path": p, "content": content})

    return pages


# ---------------------------------------------------------------------
# Ingest wiki files
# ---------------------------------------------------------------------

def ingest_wiki_files(
    force: bool = False,
    only_missing: bool = False,
    include_empty: bool = False,
    selected_paths: Optional[List[str]] = None,
    ignore_patterns: Optional[List[str]] = None,
) -> int:
    """
    Ingest .md files under WIKI_ROOT into the Chroma collection.

    Args:
        force:
            - If True:
                * Delete the existing collection and recreate it.
                * Ingest from scratch (ignores only_missing).
        only_missing:
            - If True and force is False:
                * Do NOT skip when collection is non-empty.
                * Only ingest files whose 'source' is NOT already in Chroma.
        include_empty:
            - If True, 0-byte / empty .md files are still ingested
              as a single placeholder chunk.
        selected_paths:
            - Optional list of specific relative paths (from WIKI_ROOT)
              to ingest. If provided, only those files will be processed.
    """
    print(
        f"[INGEST] ingest_wiki_files(force={force}, only_missing={only_missing}, "
        f"include_empty={include_empty}, selected_paths_count={0 if not selected_paths else len(selected_paths)})"
    )
    print(f"[INGEST] WIKI_ROOT={WIKI_ROOT} CHROMA_DIR={CHROMA_DIR} COLLECTION_NAME={COLLECTION_NAME}")

    if not os.path.isdir(WIKI_ROOT):
        print(f"[INGEST][ERROR] WIKI_ROOT not found: {WIKI_ROOT}")
        raise RuntimeError(f"WIKI_ROOT not found: {WIKI_ROOT}")

    global collection

    # ----- FORCE mode: drop and recreate collection -----
    if force:
        print(f"[INGEST] FORCE mode: deleting collection '{COLLECTION_NAME}'")
        start_del = time.time()
        client.delete_collection(COLLECTION_NAME)
        print(f"[INGEST] Collection '{COLLECTION_NAME}' deleted in {time.time() - start_del:.2f}s")
        collection = client.get_or_create_collection(name=COLLECTION_NAME)
        print(f"[INGEST] Collection '{COLLECTION_NAME}' recreated")

    # ----- Build base file list -----
    if selected_paths:
        # Use only the explicitly specified relative paths
        all_files: List[pathlib.Path] = []
        for rel in selected_paths:
            abs_path = os.path.join(WIKI_ROOT, rel)
            if os.path.isfile(abs_path):
                all_files.append(pathlib.Path(abs_path))
                print(f"[INGEST] Selected file found: {rel}")
            else:
                print(f"[INGEST][WARN] Selected file not found on disk: {rel}")
    else:
        # Use all markdown files under WIKI_ROOT
        all_files = list(iter_markdown_files())

    # ----- Apply .ragignore or provided ignore_patterns -----
    ignore_file = os.path.join(WIKI_ROOT, ".ragignore")
    # Also allow a repo-level .ragignore (one level up from WIKI_ROOT)
    repo_ignore = os.path.join(os.path.dirname(WIKI_ROOT), ".ragignore")
    compiled_ignores: List[str] = []
    if os.path.exists(ignore_file):
        try:
            with open(ignore_file, "r", encoding="utf-8") as f:
                for ln in f:
                    ln = ln.strip()
                    if not ln or ln.startswith("#"):
                        continue
                    compiled_ignores.append(ln)
            print(f"[INGEST] Loaded {len(compiled_ignores)} ignore patterns from .ragignore")
        except Exception as e:
            print(f"[INGEST][WARN] Failed to read .ragignore: {e}")

    if ignore_patterns:
        compiled_ignores.extend(ignore_patterns)

    # load repo-level .ragignore if present
    if os.path.exists(repo_ignore):
        try:
            with open(repo_ignore, "r", encoding="utf-8") as f:
                for ln in f:
                    ln = ln.strip()
                    if not ln or ln.startswith("#"):
                        continue
                    compiled_ignores.append(ln)
            print(f"[INGEST] Loaded {len(compiled_ignores)} ignore patterns (including repo .ragignore)")
        except Exception as e:
            print(f"[INGEST][WARN] Failed to read repo .ragignore: {e}")

    if compiled_ignores:
        filtered_files = []
        for p in all_files:
            rel = os.path.relpath(str(p), WIKI_ROOT)
            skip = False
            for pat in compiled_ignores:
                # treat patterns as globs relative to WIKI_ROOT
                if fnmatch.fnmatch(rel, pat):
                    print(f"[INGEST] Skipping file due to ignore pattern: {rel} (pattern: {pat})")
                    skip = True
                    break
            if not skip:
                filtered_files.append(p)
        all_files = filtered_files

    total_files = len(all_files)
    print(f"[INGEST] Base file set size (before only_missing filter) = {total_files}")

    # ----- only_missing mode (skip already ingested sources) -----
    if only_missing and not force:
        existing_sources = set(get_ingested_sources())
        print(f"[INGEST] Filtering files by only_missing=True (existing_sources={len(existing_sources)})")
        filtered_files: List[pathlib.Path] = []
        for p in all_files:
            rel_path = os.path.relpath(str(p), WIKI_ROOT)
            if rel_path in existing_sources:
                print(f"[INGEST] Skipping already ingested file: {rel_path}")
                continue
            filtered_files.append(p)
        all_files = filtered_files
        total_files = len(all_files)
        print(f"[INGEST] After only_missing filter, files to ingest={total_files}")
    else:
        if not force and not selected_paths and not only_missing:
            # Original behavior: if collection not empty and no special mode → skip
            empty = collection_empty()
            print(f"[INGEST] collection_empty()={empty}")
            if not empty:
                print("[INGEST] Collection not empty and force=False, only_missing=False → skipping ingest entirely")
                return 0

    print(f"[INGEST] FINAL file count to process = {total_files}")

    added_chunks = 0
    started_at = time.time()

    for file_idx, md_path in enumerate(all_files, start=1):
        rel_path = os.path.relpath(str(md_path), WIKI_ROOT)
        print(f"[INGEST] [{file_idx}/{total_files}] Processing file: {rel_path}")

        try:
            with open(md_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        except Exception as e:
            print(f"[INGEST][ERROR] Failed to read file {rel_path}: {e}")
            traceback.print_exc()
            continue

        if not text.strip():
            if include_empty:
                print(f"[INGEST] File {rel_path} is empty → ingesting placeholder chunk")
                text = f"(Empty TA9 wiki page: {rel_path})"
            else:
                print(f"[INGEST] File {rel_path} is empty → skipping (include_empty=False)")
                continue

        chunks = chunk_text(text)
        if not chunks:
            print(f"[INGEST] File {rel_path} produced 0 chunks → skipping")
            continue

        print(f"[INGEST] File {rel_path} produced {len(chunks)} chunks")

        ids: List[str] = []
        docs: List[str] = []
        metas: List[dict] = []
        embeds: List[List[float]] = []

        for i, chunk in enumerate(chunks):
            try:
                print(f"[INGEST] Embedding chunk {i+1}/{len(chunks)} of file {rel_path}")
                emb = embed_text(chunk)
            except Exception as e:
                print(f"[INGEST][ERROR] Embedding failed for file={rel_path} chunk={i}: {e}")
                traceback.print_exc()
                # Skip this chunk but continue with others
                continue

            ids.append(str(uuid.uuid4()))
            docs.append(chunk)
            metas.append({"source": rel_path, "chunk": i})
            embeds.append(emb)

        if not ids:
            print(f"[INGEST][WARN] No successful chunks for file {rel_path} → skipping add()")
            continue

        try:
            print(f"[INGEST] Adding {len(ids)} chunks for file {rel_path} to Chroma")
            collection.add(
                ids=ids,
                documents=docs,
                metadatas=metas,
                embeddings=embeds,
            )
            added_chunks += len(ids)
            print(f"[INGEST] Successfully added {len(ids)} chunks. Total so far={added_chunks}")
        except Exception as e:
            print(f"[INGEST][ERROR] Failed to add chunks for file {rel_path}: {e}")
            traceback.print_exc()

    total_time = time.time() - started_at
    print(f"[INGEST] Completed ingest. Total chunks added={added_chunks} in {total_time:.2f}s")
    try:
        new_count = collection.count()
        print(f"[INGEST] collection.count() after ingest = {new_count}")
    except Exception as e:
        print(f"[INGEST][WARN] Could not get collection count after ingest: {e}")
    return added_chunks


# ---------------------------------------------------------------------
# Compare-and-ingest helper (git clone wiki and ingest missing)
# ---------------------------------------------------------------------

def _git_clone_wiki(tmp_root: Optional[str] = None) -> str:
    if not (ADO_ORG and ADO_PROJECT and ADO_PAT):
        raise RuntimeError("ADO env not configured (ADO_ORG, ADO_PROJECT, ADO_PAT)")
    wiki_name = os.getenv("ADO_WIKI_NAME", f"{ADO_PROJECT}.wiki")
    remote = f"https://dev.azure.com/{ADO_ORG}/{ADO_PROJECT}/_git/{wiki_name}"
    b64 = base64.b64encode(f":{ADO_PAT}".encode("utf-8")).decode("utf-8")

    base_dir = tempfile.mkdtemp(prefix="wiki_rag_git_", dir=tmp_root)
    dest = os.path.join(base_dir, "repo")
    print(f"[GIT] Cloning wiki '{wiki_name}' into {dest}")
    cmd = [
        "git",
        "-c",
        f"http.extraHeader=Authorization: Basic {b64}",
        "clone",
        "--depth",
        "1",
        remote,
        dest,
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"[GIT][ERROR] clone failed: {e.stderr.decode('utf-8', errors='ignore')[:400]}")
        shutil.rmtree(base_dir, ignore_errors=True)
        raise RuntimeError("git clone failed")
    return dest


def compare_and_ingest_internal() -> Tuple[int, int]:
    """Clone the Azure DevOps wiki repo and ingest only missing .md files."""
    print("[COMPARE_INGEST] Starting compare-and-ingest via git clone")

    # If ADO not configured, fallback to local filesystem ingest
    if not (ADO_ORG and ADO_PROJECT and ADO_PAT):
        print("[COMPARE_INGEST][WARN] ADO not configured, falling back to local files")
        added = ingest_wiki_files(only_missing=True)
        return added, collection.count()

    repo_dir = None
    try:
        repo_dir = _git_clone_wiki()
        print(f"[GIT] Clone completed: {repo_dir}")
        # Collect all .md files from repo
        md_files: List[str] = []
        for p in pathlib.Path(repo_dir).rglob("*.md"):
            if p.is_file():
                rel = os.path.relpath(str(p), repo_dir)
                md_files.append(rel)
        print(f"[GIT] Found {len(md_files)} markdown files in wiki repo")

        if not md_files:
            return 0, collection.count()

        existing_sources = set(get_ingested_sources())
        to_ingest = [f for f in md_files if f not in existing_sources]
        print(f"[COMPARE_INGEST] Files to ingest (missing) = {len(to_ingest)}")

        if not to_ingest:
            return 0, collection.count()

        added_chunks = 0
        for idx, rel in enumerate(to_ingest, start=1):
            abs_path = os.path.join(repo_dir, rel)
            print(f"[COMPARE_INGEST] [{idx}/{len(to_ingest)}] Ingesting file: {rel}")
            try:
                with open(abs_path, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
            except Exception as e:
                print(f"[COMPARE_INGEST][ERROR] Failed to read {rel}: {e}")
                continue

            if not text.strip():
                print(f"[COMPARE_INGEST] Empty file {rel} → skipping")
                continue

            chunks = chunk_text(text)
            if not chunks:
                print(f"[COMPARE_INGEST] 0 chunks for {rel} → skipping")
                continue

            ids: List[str] = []
            docs: List[str] = []
            metas: List[dict] = []
            embeds: List[List[float]] = []
            for i, ch in enumerate(chunks):
                try:
                    emb = embed_text(ch)
                except Exception as e:
                    print(f"[COMPARE_INGEST][ERROR] Embedding failed for {rel} chunk={i}: {e}")
                    continue
                ids.append(str(uuid.uuid4()))
                docs.append(ch)
                metas.append({"source": rel, "chunk": i})
                embeds.append(emb)

            if not ids:
                print(f"[COMPARE_INGEST][WARN] No successful chunks for {rel} → skipping add()")
                continue

            try:
                collection.add(ids=ids, documents=docs, metadatas=metas, embeddings=embeds)
                added_chunks += len(ids)
            except Exception as e:
                print(f"[COMPARE_INGEST][ERROR] Failed to add chunks for {rel}: {e}")

        total = collection.count()
        print(f"[COMPARE_INGEST] Finished git-based ingest: added_chunks={added_chunks}, total_chunks={total}")
        return added_chunks, total
    finally:
        if repo_dir and os.path.isdir(repo_dir):
            try:
                shutil.rmtree(os.path.dirname(repo_dir), ignore_errors=True)
                print("[GIT] Cleaned up temp clone directory")
            except Exception:
                pass


# ---------------------------------------------------------------------
# RAG “brain” – augmentation + reranking
# ---------------------------------------------------------------------

def augment_question(question: str) -> str:
    """
    Add synonyms / hints so embeddings are more likely to match
    the right wiki pages, especially for internal jargon.
    """
    q_low = question.lower()
    extras: List[str] = []

    # --- Ops / DevOps / Infra (NEW) ---
    if any(k in q_low for k in ["wildfly", "jboss", "standalone.xml", "domain.xml", "deployment", "redeploy", "undeploy"]):
        extras.append(
            "WildFly, JBoss, redeploy, deployment, undeploy, "
            "jboss-cli, management console, standalone.xml, domain mode"
        )

    if any(k in q_low for k in ["nginx", "reverse proxy", "proxy_pass", "ingress", "load balancer"]):
        extras.append(
            "nginx, reverse proxy, proxy_pass, ingress, load balancer"
        )

    if any(k in q_low for k in ["docker", "swarm", "stack", "service", "container", "compose"]):
        extras.append(
            "docker, docker swarm, stack deploy, docker service, container logs"
        )

    if any(k in q_low for k in ["systemctl", "service", "restart", "reload", "daemon", "linux", "bash"]):
        extras.append(
            "systemctl, restart service, reload, linux administration, bash scripts"
        )

    # --- Your existing Image / Criteria domain ---
    if "image" in q_low or "picture" in q_low or "photo" in q_low:
        extras.append(
            "image upload, image field, upload image, screenshot, picture, "
            "configure image field in data model, admin studio image configuration"
        )

    if "criteria" in q_low or "field" in q_low:
        extras.append(
            "criteria = data model field, detection field, condition field, "
            "configure detection image field in data model"
        )

    if "dm" in q_low or "data model" in q_low:
        extras.append(
            "DM = data model, data model configuration, model fields, "
            "admin studio data model editor"
        )

    if "intsight" in q_low or "ta9" in q_low:
        extras.append(
            "IntSight platform overview, TA9 company overview, flagship system, "
            "big data intelligence system"
        )

    # --- Helpful business keywords (NEW) ---
    if "deloitte" in q_low:
        extras.append(
            "Deloitte dashboard, Deloitte project overview, Deloitte data collection process, Deloitte PRD"
        )

    if not extras:
        print("[AUGMENT] No extra synonyms added")
        return question

    print(f"[AUGMENT] Extras added: {extras}")
    augmented = question + "\n\nExpanded synonyms & internal context:\n" + " ".join(extras)
    print(f"[AUGMENT] Augmented question from len={len(question)} to len={len(augmented)}")
    return augmented


def lexical_boost_score(question: str, doc: str, meta: dict) -> float:
    """
    Heuristic lexical + domain score.
    Higher score = more relevant.
    """
    q = question.lower()
    d = doc.lower()
    source = str(meta.get("source", "")).lower()

    score = 0.0

    concepts = [
        (["image", "picture", "photo", "screenshot"], ["image", "picture", "photo", "screenshot"], 5.0),
        (["criteria", "criterion", "field"], ["criteria", "criterion", "field", "condition"], 4.0),
        (["4.x", "4x"], ["4.x", "4x"], 3.0),
        (["detection"], ["detection"], 3.0),
        (["dm", "data model"], ["data model", "dm", "model"], 2.5),
        (["admin studio", "admin"], ["admin studio", "developer environment", "configuration"], 2.0),

        # NEW: ops/devops boosts
        (["wildfly", "jboss", "redeploy", "deployment"], ["wildfly", "jboss", "redeploy", "deploy", "deployment"], 3.5),
        (["nginx", "proxy", "reverse"], ["nginx", "proxy", "reverse"], 2.5),
        (["docker", "swarm", "stack", "service"], ["docker", "swarm", "stack", "service"], 2.5),
        (["deloitte"], ["deloitte"], 4.0),
    ]

    for q_terms, d_terms, w in concepts:
        if any(t in q for t in q_terms) and any(t in d for t in d_terms):
            score += w

    if "image" in q and "criteria" in q and "add-an-image-to-criteria" in source:
        score += 10.0

    # No root-doc boost to keep all files treated equally

    # Small source-name boost if query tokens appear in filename
    for tok in set([t for t in q.replace("\n", " ").split() if len(t) > 3]):
        if tok in source:
            score += 0.7

    # Light lexical overlap
    q_tokens = [t for t in q.replace("\n", " ").split() if len(t) > 3]
    for tok in set(q_tokens):
        if tok in d:
            score += 0.5

    return score


def inject_special_doc_for_image(question: str, docs: List[str], metas: List[dict]) -> None:
    q = question.lower()
    needs_image_help = (
        "image" in q
        and ("criteria" in q or "field" in q or "upload" in q or "detection" in q)
    )

    print(f"[SPECIAL] inject_special_doc_for_image needs_image_help={needs_image_help}")
    if not needs_image_help:
        return

    abs_path = os.path.join(WIKI_ROOT, IMAGE_CRITERIA_DOC_REL)
    print(f"[SPECIAL] Checking special doc: {abs_path}")
    if not os.path.exists(abs_path):
        print("[SPECIAL][WARN] Special image criteria doc not found on disk")
        return

    try:
        with open(abs_path, "r", encoding="utf-8") as f:
            text = f.read().strip()
    except Exception as e:
        print(f"[SPECIAL][ERROR] Failed to read special doc: {e}")
        traceback.print_exc()
        return

    if not text:
        print("[SPECIAL][WARN] Special doc is empty")
        return

    docs.insert(0, text)
    metas.insert(0, {"source": IMAGE_CRITERIA_DOC_REL, "chunk": 0})
    print("[SPECIAL] Injected special 'Add image to criteria' doc as first context chunk")


def rerank_results(
    question: str,
    docs: List[str],
    metas: List[dict],
    distances: Optional[List[float]] = None,
    ids: Optional[List[str]] = None,
) -> Tuple[List[str], List[dict], List[float], List[str]]:
    if not docs:
        print("[RERANK] No docs to rerank")
        return docs, metas, distances or [], ids or []

    print(f"[RERANK] Reranking {len(docs)} docs for question='{question[:120]}...'")
    items = []
    for idx, (d, m) in enumerate(zip(docs, metas)):
        s = lexical_boost_score(question, d, m)
        dist = None if distances is None or idx >= len(distances) else distances[idx]
        idv = None if ids is None or idx >= len(ids) else ids[idx]
        items.append({"doc": d, "meta": m, "score": s, "idx": idx, "dist": dist, "id": idv})

    if all(it["score"] == 0 for it in items):
        print("[RERANK] All scores=0 → keeping original vector order")
        # Still print a summary of results
        for it in items[:10]:
            print(f"[RERANK] src={it['meta'].get('source')} chunk={it['meta'].get('chunk')} id={it['id']} dist={it['dist']}")
        return docs, metas, distances or [], ids or []

    items.sort(key=lambda x: (-x["score"], x["idx"]))

    print("[RERANK] Top 10 after rerank (score, dist, id, source, chunk):")
    for it in items[:10]:
        print(f"         score={it['score']:.2f} dist={it['dist']} id={it['id']} source={it['meta'].get('source')} chunk={it['meta'].get('chunk')}")

    reranked_docs = [it["doc"] for it in items]
    reranked_metas = [it["meta"] for it in items]
    reranked_distances = [it["dist"] for it in items]
    reranked_ids = [it["id"] for it in items]
    return reranked_docs, reranked_metas, reranked_distances, reranked_ids


# ---------------------------------------------------------------------
# API Models
# ---------------------------------------------------------------------

class ChatRequest(BaseModel):
    question: str
    top_k: int = 5
    force_reingest: Optional[bool] = False
    ticket_url: Optional[str] = None
    teach: Optional[bool] = False


class ChatResponse(BaseModel):
    answer: str
    sources: List[str]


class IngestRequest(BaseModel):
    force: bool = False
    only_missing: bool = False
    include_empty: bool = False
    paths: Optional[List[str]] = None  # relative to WIKI_ROOT, e.g. "TA9-WIKI/QA/Export-Event-Viewer-Logs.md"
    validate_only: bool = False  # when True, just compute the planned file count without ingesting


class IngestResponse(BaseModel):
    added_chunks: int
    total_chunks: int
    message: Optional[str] = None


# ---------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------

@app.get("/health")
def health():
    print("[API][HEALTH] /health called")
    info = {
        "status": "ok",
        "chroma_empty": collection_empty(),
        "wiki_root": WIKI_ROOT,
        "collection_name": COLLECTION_NAME,
        "embedding_backend": "openai" if OPENAI_API_KEY else "ollama",
        "embedding_model": OPENAI_EMBEDDING_MODEL if OPENAI_API_KEY else OLLAMA_MODEL,
    }
    print(f"[API][HEALTH] {info}")
    return info


@app.get("/azure/tickets")
def azure_tickets(tag: str = "CC"):
    print(f"[API][ADO] /azure/tickets tag={tag}")
    try:
        items = ado_list_tickets(tag_contains=tag)
        return {"items": items}
    except Exception as exc:
        print(f"[API][ADO][ERROR] {exc}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/azure/ticket/access")
def azure_ticket_access(url: Optional[str] = None, id: Optional[int] = None):
    print(f"[API][ADO] /azure/ticket/access url={url} id={id}")
    if url:
        id = ado_parse_id_from_url(url)
    if not id:
        raise HTTPException(status_code=400, detail="ticket id or url is required")
    ok = ado_check_access_by_id(int(id))
    return {"accessible": bool(ok)}


@app.post("/ingest", response_model=IngestResponse)
def ingest(req: IngestRequest):
    print(
        f"[API][INGEST] /ingest called with "
        f"force={req.force}, only_missing={req.only_missing}, "
        f"include_empty={req.include_empty}, paths_count={0 if not req.paths else len(req.paths)}, validate_only={req.validate_only}"
    )
    try:
        # Validation-only mode: compute planned file set size without ingesting
        if req.validate_only:
            print("[API][INGEST] validate_only=True → computing planned file set without ingesting")
            # Build base file list
            if req.paths:
                all_files: List[pathlib.Path] = []
                for rel in req.paths:
                    abs_path = os.path.join(WIKI_ROOT, rel)
                    if os.path.isfile(abs_path):
                        all_files.append(pathlib.Path(abs_path))
                        print(f"[INGEST][PLAN] Selected file found: {rel}")
                    else:
                        print(f"[INGEST][PLAN][WARN] Selected file not found on disk: {rel}")
            else:
                all_files = list(iter_markdown_files())

            # Apply ignore patterns from .ragignore (wiki and repo root)
            ignore_file = os.path.join(WIKI_ROOT, ".ragignore")
            repo_ignore = os.path.join(os.path.dirname(WIKI_ROOT), ".ragignore")
            compiled_ignores: List[str] = []
            for ig in (ignore_file, repo_ignore):
                if os.path.exists(ig):
                    try:
                        with open(ig, "r", encoding="utf-8") as f:
                            for ln in f:
                                ln = ln.strip()
                                if not ln or ln.startswith("#"):
                                    continue
                                compiled_ignores.append(ln)
                    except Exception as e:
                        print(f"[INGEST][PLAN][WARN] Failed to read {ig}: {e}")
            if compiled_ignores:
                filtered = []
                for p in all_files:
                    rel = os.path.relpath(str(p), WIKI_ROOT)
                    if any(fnmatch.fnmatch(rel, pat) for pat in compiled_ignores):
                        print(f"[INGEST][PLAN] Skipping due to ignore: {rel}")
                        continue
                    filtered.append(p)
                all_files = filtered

            total_files = len(all_files)
            print(f"[INGEST][PLAN] Base file set size (before only_missing/empty filters) = {total_files}")

            # If only_missing requested, filter out already ingested sources
            if req.only_missing and not req.force:
                existing_sources = set(get_ingested_sources())
                print(f"[INGEST][PLAN] only_missing=True existing_sources={len(existing_sources)}")
                all_files = [p for p in all_files if os.path.relpath(str(p), WIKI_ROOT) not in existing_sources]
                total_files = len(all_files)
                print(f"[INGEST][PLAN] After only_missing filter, files={total_files}")

            # Exclude empty files unless include_empty=True
            if not req.include_empty:
                filtered = []
                for p in all_files:
                    try:
                        sz = os.path.getsize(str(p))
                    except Exception:
                        sz = 0
                    if sz == 0:
                        print(f"[INGEST][PLAN] Skipping empty file: {os.path.relpath(str(p), WIKI_ROOT)}")
                        continue
                    filtered.append(p)
                all_files = filtered
                total_files = len(all_files)
                print(f"[INGEST][PLAN] After empty-file filter, files={total_files}")

            # Do NOT ingest; just return a summary. total_chunks is a proxy (unknown until chunking), so we return file count.
            print(f"[API][INGEST][PLAN] Completed. planned_files={total_files}")
            return IngestResponse(added_chunks=0, total_chunks=total_files)

        added = ingest_wiki_files(
            force=req.force,
            only_missing=req.only_missing,
            include_empty=req.include_empty,
            selected_paths=req.paths,
        )
        total = collection.count()
        print(f"[API][INGEST] Completed. added_chunks={added}, total_chunks={total}")
        return IngestResponse(added_chunks=added, total_chunks=total)
    except Exception as exc:
        print(f"[API][INGEST][ERROR] {exc}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(exc))


# ---------------------------------------------------------------------
# Compare and Ingest Endpoint
# ---------------------------------------------------------------------

@app.post("/compare_and_ingest", response_model=IngestResponse)
def compare_and_ingest():
    """
    Compare wiki files to the vector DB and ingest only missing ones.
    Safe to call manually (curl) or via the scheduler.
    """
    try:
        added, total = compare_and_ingest_internal()
        if added == 0:
            msg = "No new files to ingest. All wiki files are already in the vector database."
        else:
            msg = f"Successfully ingested {added} new chunks from wiki files."
        return IngestResponse(added_chunks=added, total_chunks=total, message=msg)
    except Exception as exc:
        print(f"[API][COMPARE_INGEST][ERROR] {exc}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(exc))


# ---------------------------------------------------------------------
# Chat Endpoint
# ---------------------------------------------------------------------

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    print(f"[API][CHAT] /chat called question='{req.question[:200]}' top_k={req.top_k} force_reingest={req.force_reingest}")
    question = req.question.strip()
    if not question:
        print("[API][CHAT][ERROR] Empty question")
        raise HTTPException(status_code=400, detail="question is empty")

    if req.force_reingest:
        print("[API][CHAT] force_reingest=True → calling ingest_wiki_files(force=True)")
        ingest_wiki_files(force=True)

    augmented_question = augment_question(question)

    try:
        q_emb = embed_text(augmented_question)
        # Log a short preview of the query embedding used for vector search
        q_preview = ",".join([f"{x:.6f}" for x in q_emb[:EMBED_PREVIEW_COUNT]])
        q_norm = math.sqrt(sum([x * x for x in q_emb]))
        q_hash = hashlib.sha256(
            ",".join([f"{x:.6f}" for x in q_emb[:16]]).encode("utf-8")
        ).hexdigest()[:12]
        print(f"[API][CHAT] Query embedding preview=[{q_preview}] len={len(q_emb)} norm={q_norm:.6f} hash={q_hash}")
        if LOG_FULL_EMBEDDINGS:
            print(f"[API][CHAT][EMBED_FULL] {q_emb}")
    except Exception as exc:
        print(f"[API][CHAT][ERROR] Embedding failed: {exc}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Embedding failed: {exc}")

    # More candidates improves recall a lot
    effective_top_k = max(req.top_k, 50)
    print(f"[API][CHAT] effective_top_k={effective_top_k}")

    try:
        # Request ids, distances and (if available) embeddings for richer logging
        results = collection.query(
            query_embeddings=[q_emb],
            n_results=effective_top_k,
            include=["distances", "documents", "metadatas", "embeddings"],
        )
    except Exception as exc:
        print(f"[API][CHAT][ERROR] Vector search failed: {exc}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Vector search failed: {exc}")

    ids = results.get("ids", [[]])[0]
    distances = results.get("distances", [[]])[0]
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    emb_results = results.get("embeddings", [[]])[0]

    print(f"[API][CHAT] Vector search returned {len(docs)} docs")
    # Log top matches briefly (id, dist, source, chunk, snippet)
    for i, (d, m) in enumerate(zip(docs, metas)):
        if i >= 10:
            break
        did = ids[i] if i < len(ids) else None
        dist = distances[i] if i < len(distances) else None
        snippet = (d[:200].replace("\n", " ") + "...") if d else ""
        emb_preview = None
        emb_norm = None
        emb_hash = None
        try:
            if i < len(emb_results):  # avoid truthiness checks on numpy arrays
                emb = emb_results[i]
                if emb is not None and len(emb) > 0:
                    emb_preview = ",".join([f"{x:.6f}" for x in emb[:EMBED_PREVIEW_COUNT]])
                    emb_norm = math.sqrt(sum([x * x for x in emb]))
                    emb_hash = hashlib.sha256(
                        ",".join([f"{x:.6f}" for x in emb[:16]]).encode("utf-8")
                    ).hexdigest()[:12]
        except Exception:
            pass
        print(
            f"[API][CHAT] Match[{i+1}] id={did} dist={dist} source={m.get('source')} chunk={m.get('chunk')} snippet='{snippet}' emb_preview={emb_preview} norm={emb_norm} hash={emb_hash}"
        )

    # --------- NEW: fallback when embeddings miss ----------
    # Sometimes embeddings don't pull the right file. If we got nothing,
    # do a lightweight keyword search on documents content.
    if not docs:
        print("[API][CHAT][FALLBACK] No docs from vector search → trying keyword fallback")
        keywords = [t for t in question.lower().replace("\n", " ").split() if len(t) >= 5]
        keywords = list(dict.fromkeys(keywords))[:6]  # unique, limit
        print(f"[API][CHAT][FALLBACK] keywords={keywords}")

        fallback_docs: List[str] = []
        fallback_metas: List[dict] = []
        fallback_ids: List[str] = []
        fallback_distances: List[float] = []

        for kw in keywords:
            try:
                fb = collection.query(
                    query_texts=[kw],
                    n_results=10,
                    include=["distances", "documents", "metadatas"],
                )
                fb_docs = fb.get("documents", [[]])[0]
                fb_metas = fb.get("metadatas", [[]])[0]
                fb_ids = fb.get("ids", [[]])[0]
                fb_dists = fb.get("distances", [[]])[0]
                for idx, (d, m) in enumerate(zip(fb_docs, fb_metas)):
                    if d and m:
                        fallback_docs.append(d)
                        fallback_metas.append(m)
                        if idx < len(fb_ids):
                            fallback_ids.append(fb_ids[idx])
                        if idx < len(fb_dists):
                            fallback_distances.append(fb_dists[idx])
            except Exception as e:
                print(f"[API][CHAT][FALLBACK][WARN] failed query_texts for kw='{kw}': {e}")

        if fallback_docs:
            print(f"[API][CHAT][FALLBACK] Got {len(fallback_docs)} fallback docs")
            docs = fallback_docs
            metas = fallback_metas
            ids = fallback_ids
            distances = fallback_distances
        else:
            print("[API][CHAT][FALLBACK] Still no docs after fallback")

    # No forced root-file injection: all files treated equally

    # If a ticket is selected, fetch it now and pin it later as the first context
    selected_ticket_id: Optional[int] = None
    selected_ticket_text: Optional[str] = None
    if req.ticket_url:
        selected_ticket_id = ado_parse_id_from_url(req.ticket_url)
        if selected_ticket_id:
            print(f"[API][CHAT] Fetching Azure DevOps ticket id={selected_ticket_id}")
            try:
                selected_ticket_text = ado_fetch_ticket_text(int(selected_ticket_id))
            except Exception as e:
                print(f"[API][CHAT][WARN] failed to fetch ticket: {e}")
                selected_ticket_id = None
                selected_ticket_text = None

    # Also include memory snippets related to the question
    # Gather memory docs (generic + ticket-specific) but do not pin them; they will be reranked
    try:
        mem = memory_collection.query(
            query_embeddings=[q_emb],
            n_results=6,
            include=["documents", "metadatas", "ids", "distances"],
        )
        mem_docs = mem.get("documents", [[]])[0]
        mem_metas = mem.get("metadatas", [[]])[0]
        if mem_docs:
            print(f"[API][CHAT] Collected {len(mem_docs)} memory docs for context candidates")
            for d, m in zip(mem_docs, mem_metas):
                docs.insert(0, d)
                metas.insert(0, m or {"source": "memory", "chunk": 0})
    except Exception as e:
        print(f"[API][CHAT][WARN] memory query failed: {e}")

    inject_special_doc_for_image(question, docs, metas)

    if not docs:
        print("[API][CHAT] No docs after injection → calling LLM with 'no context' message")
        answer = call_llm(
            "No wiki context available. Answer briefly but mention that you "
            "do not have access to the internal knowledge base.\n\n"
            f"Question: {question}"
        )
        return ChatResponse(answer=answer, sources=[])

    docs, metas, distances, ids = rerank_results(question, docs, metas, distances=distances, ids=ids)

    context_blocks: List[str] = []
    source_strings: List[str] = []

    # More context improves answer success rate
    MAX_CONTEXT_DOCS = 12
    print(f"[API][CHAT] Building context with MAX_CONTEXT_DOCS={MAX_CONTEXT_DOCS}")

    # Build context blocks, pinning the selected ticket first if present
    if selected_ticket_text:
        src = f"azure-devops:{selected_ticket_id} (selected ticket)"
        source_strings.append(src)
        snippet = selected_ticket_text[:200].replace("\n", " ")
        print(f"[API][CHAT] Context source: {src} | snippet='{snippet}...'")
        context_blocks.append(f"Source: {src}\n{selected_ticket_text}")

    remaining_slots = MAX_CONTEXT_DOCS - (1 if selected_ticket_text else 0)
    for i, (doc, meta) in enumerate(list(zip(docs, metas))[:remaining_slots]):
        id_val = ids[i] if i < len(ids) else None
        dist_val = distances[i] if i < len(distances) else None
        src = f"{meta.get('source')} (chunk {meta.get('chunk', 0)}) id={id_val} dist={dist_val}"
        source_strings.append(src)
        snippet = doc[:200].replace("\n", " ")
        print(f"[API][CHAT] Context source: {src} | snippet='{snippet}...'")
        context_blocks.append(f"Source: {src}\n{doc}")

    context_text = "\n\n---\n\n".join(context_blocks)

    # ChatGPT-style prompt for natural, high-quality responses
    prompt_intro = (
        "You are an internal TA9 / IntSight assistant. Your goal is to respond in the same style and quality as ChatGPT: "
        "clear, structured, ordered, and professional.\n\n"
        "RULES FOR EVERY RESPONSE:\n\n"
        "1. STRUCTURE\n"
        "- Always organize answers into clear sections.\n"
        "- Use headings, numbered steps, and bullet points where appropriate.\n"
        "- Present information in a logical top-down order (overview → details → examples).\n\n"
        "2. CLARITY\n"
        "- Be concise but complete.\n"
        "- Avoid unnecessary repetition.\n"
        "- Explain technical concepts clearly and precisely.\n\n"
        "3. ORDER & FLOW\n"
        "- Start with a short direct answer or summary.\n"
        "- Then expand with details.\n"
        "- End with practical tips, examples, or next steps when relevant.\n\n"
        "4. TONE\n"
        "- Professional, calm, confident.\n"
        "- Helpful and instructional.\n"
        "- No emojis unless explicitly requested.\n\n"
        "5. TECHNICAL ANSWERS\n"
        "- Use code blocks for commands or code.\n"
        "- Explain what the code does.\n"
        "- Prefer best practices and production-grade solutions.\n\n"
        "6. UNCERTAINTY\n"
        "- If information is missing, state what is known first.\n"
        "- Clearly say what is unknown and why.\n"
        "- Never hallucinate facts.\n\n"
        "7. FORMAT EXAMPLES\n"
        "- Use tables when comparing things.\n"
        "- Use step-by-step lists for procedures.\n"
        "- Use short paragraphs for explanations.\n\n"
        "8. DEFAULT STYLE\n"
        "- Assume the user prefers ChatGPT-level answers: well-structured, readable, and actionable.\n\n"
        "If context is provided, base your answer strictly on that context.\n"
        "If context is partial, answer with what is available and state limitations.\n\n"
        "Formatting guidelines:\n"
        "- Use minimal headings; avoid over-structuring when not needed.\n"
        "- Only use fenced code blocks for commands or code. Do NOT put normal text in code blocks.\n"
        "- Avoid emojis unless they add clear value; if used, keep them rare.\n\n"
    )

    ticket_focus_rules = ""
    if selected_ticket_id:
        ticket_focus_rules = (
            f"A SELECTED AZURE DEVOPS TICKET IS PROVIDED (ID {selected_ticket_id}). Follow these rules:\n"
            "- Focus primarily on the selected ticket's content.\n"
            "- Do not reference any other ticket numbers; if a number appears, ensure it matches the selected ticket ID.\n"
            "- If information is missing in the ticket, state the gaps clearly and avoid guessing.\n\n"
        )

    prompt = (
        prompt_intro + ticket_focus_rules +
        f"Context:\n{context_text}\n\n" +
        f"Question: {question}\n\n" +
        "Answer:"
    )

    try:
        answer = call_llm(prompt)
    except Exception as exc:
        print(f"[API][CHAT][ERROR] LLM call failed: {exc}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"LLM call failed: {exc}")

    # Optional teach: persist summarized lesson to memory collection
    if req.teach:
        try:
            lesson_prompt = (
                "Summarize the key knowledge learned from the following Q&A. "
                "Return a concise explanation (<= 180 words) followed by 6-10 bullet points of exact steps or commands. "
                "Avoid sensitive secrets. Keep it generally reusable.\n\n"
                f"Question:\n{question}\n\nAnswer:\n{answer}\n\nSummary + Steps:"
            )
            lesson = call_llm(lesson_prompt)
            emb = embed_text(lesson)
            src = "memory:generic"
            if req.ticket_url:
                tid = ado_parse_id_from_url(req.ticket_url)
                if tid:
                    src = f"memory:ticket:{tid}"
            memory_collection.add(
                ids=[str(uuid.uuid4())],
                documents=[lesson],
                embeddings=[emb],
                metadatas=[{"source": src, "created_at": datetime.utcnow().isoformat()}],
            )
            print(f"[API][CHAT] Stored lesson to memory collection source={src} len={len(lesson)}")
        except Exception as e:
            print(f"[API][CHAT][WARN] Failed to store memory: {e}")

    print(f"[API][CHAT] Returning answer len={len(answer)} with {len(source_strings)} sources")
    return ChatResponse(answer=answer, sources=source_strings)


# ---------------------------------------------------------------------
# Scheduler: run compare-and-ingest daily at 20:00 Asia/Jerusalem
# ---------------------------------------------------------------------

async def _wait_until(hour: int, minute: int, tz: ZoneInfo) -> float:
    now = datetime.now(tz)
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if now >= target:
        target += timedelta(days=1)
    return (target - now).total_seconds()


async def _daily_compare_and_ingest_task():
    tz = ZoneInfo("Asia/Jerusalem")
    while True:
        try:
            wait_s = await _wait_until(20, 0, tz)
            print(f"[SCHEDULE] Next compare_and_ingest at 20:00 Asia/Jerusalem in {wait_s:.0f}s")
            await asyncio.sleep(wait_s)
            print("[SCHEDULE] Triggering scheduled compare_and_ingest")
            compare_and_ingest_internal()
        except Exception as e:
            print(f"[SCHEDULE][ERROR] {e}")
            traceback.print_exc()
            # small backoff before retrying scheduling loop
            await asyncio.sleep(60)


@app.on_event("startup")
async def _start_scheduler():
    asyncio.create_task(_daily_compare_and_ingest_task())
