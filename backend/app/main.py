import os
import uuid
import pathlib
import time
import traceback
from typing import List, Optional, Tuple, Dict
import random

from fastapi import FastAPI, HTTPException, BackgroundTasks
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
import subprocess
import tempfile
import shutil

load_dotenv()

# ---------------------------------------------------------------------
# Env & constants
# ---------------------------------------------------------------------

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

app = FastAPI(title="Wiki RAG API")

# Track if a structured "first ticket response" was already sent per ticket key (id or URL fallback)
ticket_first_reply_done: Dict[str, bool] = {}


# ---------------------------------------------------------------------
# Embedding + LLM
# ---------------------------------------------------------------------

def embed_text(text: str) -> List[float]:
    snippet = text[:120].replace("\n", " ")
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
    try:
        emb = data["data"][0]["embedding"]
    except Exception as e:
        print(f"[EMBED][ERROR] Unexpected OpenAI response shape: {data}")
        raise RuntimeError(f"OpenAI embeddings response missing embedding: {e}")

    preview = ",".join([f"{x:.6f}" for x in emb[:EMBED_PREVIEW_COUNT]])
    norm = math.sqrt(sum([x * x for x in emb]))
    h = hashlib.sha256(
        ",".join([f"{x:.6f}" for x in emb[:16]]).encode("utf-8")
    ).hexdigest()[:12]
    print(f"[EMBED] Got OpenAI embedding length={len(emb)} preview=[{preview}] norm={norm:.6f} hash={h}")
    if LOG_FULL_EMBEDDINGS:
        print(f"[EMBED][FULL] {emb}")
    return emb


def call_llm(prompt: str, temperature: float = 0.2) -> str:
    """Call OpenAI chat for final answer."""
    print(f"[LLM] Calling OpenAI chat model={OPENAI_CHAT_MODEL} prompt_len={len(prompt)} temp={temperature}")
    start = time.time()
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    body = {
        "model": OPENAI_CHAT_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
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
ADO_PROJECT_TICKET_SUMMARY = os.getenv("ADO_PROJECT_TICKET_SUMMARY", "").strip('"')
ADO_PAT = os.getenv("ADO_PAT")

LEARN_QUERY_NAME = os.getenv("ADO_LEARN_QUERY_NAME", "ai_learn_tickets_query")

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


def _ado_wiql_learning_query(project: Optional[str] = None) -> str:
    """
    WIQL based on the query shown in the screenshot:
      - Changed Date > @Today - 720
      - Work Item Type = [Any] (no filter)
      - State In closed,completed,fixed,ready,resolved
    """
    if project:
        return (
            "SELECT [System.Id] FROM WorkItems "
            f"WHERE [System.TeamProject] = '{project}' "
            "AND [System.ChangedDate] > @Today - 720 "
            "AND [System.State] IN ('Closed','Completed','Fixed','Ready','Resolved') "
            "ORDER BY [System.ChangedDate] DESC"
        )
    return (
        "SELECT [System.Id] FROM WorkItems "
        "WHERE [System.TeamProject] = @project "
        "AND [System.ChangedDate] > @Today - 720 "
        "AND [System.State] IN ('Closed','Completed','Fixed','Ready','Resolved') "
        "ORDER BY [System.ChangedDate] DESC"
    )


def ado_list_learning_tickets(limit: Optional[int] = None) -> List[int]:
    """Run WIQL and return a list of work item IDs matching the learning query."""
    project = ADO_PROJECT_TICKET_SUMMARY or ADO_PROJECT
    url = f"https://dev.azure.com/{ADO_ORG}/{project}/_apis/wit/wiql?api-version=7.1-preview.2"
    wiql = _ado_wiql_learning_query(project)
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
    ids = [int(it.get("id")) for it in items if it.get("id")]
    if limit is not None:
        ids = ids[: max(0, int(limit))]
    return ids


def _extract_images_from_html(html: str) -> List[str]:
    """
    Extract image URLs/references from HTML.
    Returns list of image src attributes.
    """
    if not html:
        return []
    try:
        img_pattern = r'<img[^>]+src=["\']?([^"\'>\s]+)["\']?'
        matches = re.findall(img_pattern, html or "")
        return [m for m in matches if m.strip()]
    except Exception:
        return []


def _describe_image_via_vision(image_url: str) -> str:
    """
    Use OpenAI vision to describe an image.
    Returns a text description of the image.
    """
    try:
        # Only attempt if it's a valid URL
        if not (image_url.startswith("http://") or image_url.startswith("https://")):
            return f"[Local image: {image_url}]"
        
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
        body = {
            "model": "gpt-4o-mini",  # Vision capable model
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Briefly describe what you see in this image. Focus on any technical content, errors, UI elements, or relevant details."},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                }
            ],
            "max_tokens": 150,
        }
        resp = requests.post(f"{OPENAI_URL}/chat/completions", json=body, headers=headers, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            description = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            print(f"[VISION] Described image {image_url[:60]}... -> {description[:100]}...")
            return description
        else:
            print(f"[VISION][WARN] Vision call failed for {image_url}: {resp.status_code}")
            return f"[Image: {image_url}]"
    except Exception as e:
        print(f"[VISION][WARN] Failed to describe image {image_url}: {e}")
        return f"[Image: {image_url}]"


def _strip_html(text: str) -> str:
    try:
        txt = re.sub(r"<[^>]+>", " ", text or "")
        txt = unescape(txt)
        return " ".join(txt.split())
    except Exception:
        return text or ""


def _first_field(fields: dict, keys: List[str]) -> str:
    for k in keys:
        if k in fields and fields.get(k) not in (None, ""):
            v = fields.get(k)
            if isinstance(v, dict):
                return v.get("displayName") or v.get("uniqueName") or str(v)
            return str(v)
    return ""


def ado_fetch_ticket_full(work_item_id: int) -> dict:
    """Fetch main fields + comments for a work item."""
    base = _ado_base()
    hdrs = _ado_headers()
    main = requests.get(
        f"{base}/_apis/wit/workitems/{work_item_id}?$expand=all&api-version=7.1",
        headers=hdrs,
        timeout=60,
    )
    if main.status_code != 200:
        raise RuntimeError(f"ADO workitem fetch error: {main.text}")
    data = main.json()
    fields = data.get("fields", {})

    comments: List[dict] = []
    try:
        c = requests.get(
            f"{base}/_apis/wit/workItems/{work_item_id}/comments?api-version=7.1-preview.3",
            headers=hdrs,
            timeout=60,
        )
        if c.status_code == 200:
            for it in c.json().get("comments", []):
                comments.append(
                    {
                        "text": _strip_html(it.get("text", "")),
                        "createdBy": (it.get("createdBy") or {}).get("displayName")
                        or (it.get("createdBy") or {}).get("uniqueName")
                        or "",
                        "createdDate": it.get("createdDate") or "",
                    }
                )
    except Exception as e:
        print(f"[ADO][WARN] comments fetch failed: {e}")

    return {"id": work_item_id, "fields": fields, "comments": comments}


def build_conversation_block(comments: List[dict]) -> str:
    if not comments:
        return "Not provided."
    lines: List[str] = []
    for c in comments:
        who = c.get("createdBy") or "Unknown"
        when = c.get("createdDate") or ""
        txt = c.get("text") or ""
        lines.append(f"[{when}] {who}: {txt}")
    return "\n".join(lines)


def generate_professional_ticket_report(ticket: dict) -> str:
    fields = ticket.get("fields", {})
    comments = ticket.get("comments", [])

    work_item_type = _first_field(fields, ["System.WorkItemType"]) or "Not provided"
    title = _first_field(fields, ["System.Title"]) or "Not provided"
    product = _first_field(
        fields,
        [
            "Custom.Product",
            "Microsoft.VSTS.Common.Product",
            "Product",
            "Custom.ProductName",
        ],
    ) or "Not provided"
    service = _first_field(
        fields,
        [
            "Custom.Service",
            "Microsoft.VSTS.Common.Service",
            "Service",
            "Custom.ServiceName",
        ],
    ) or "Not provided"
    
    # Get raw HTML description to extract images
    raw_description = _first_field(
        fields,
        ["System.Description", "Microsoft.VSTS.TCM.ReproSteps", "System.History"],
    ) or ""
    
    # Extract and describe images
    image_descriptions = ""
    if raw_description:
        images = _extract_images_from_html(raw_description)
        if images:
            print(f"[TICKET] Found {len(images)} images in description, describing via vision...")
            image_texts = []
            for img_url in images[:3]:  # Limit to first 3 images to avoid too many API calls
                desc = _describe_image_via_vision(img_url)
                image_texts.append(desc)
            if image_texts:
                image_descriptions = "\n\nImages in description:\n" + "\n".join(image_texts)
    
    description = _strip_html(raw_description) + image_descriptions

    conversation = build_conversation_block(comments)

    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not configured; cannot format ticket report.")

    llm_prompt = (
        "You are a technical support documentation assistant. "
        "Using ONLY the provided ticket data, create a professional report with EXACT sections below. "
        "If data is missing, write 'Not provided.' Do not invent facts. "
        "Return plain text with these headings exactly and in this order:\n\n"
        "Ticket type:\n"
        "Title:\n"
        "Product:\n"
        "Service:\n\n"
        "User description:\n\n"
        "Observed error:\n\n"
        "Expected behavior:\n\n"
        "Resolution steps (step-by-step):\n\n"
        "-----\n"
        "Ticket data:\n"
        f"Type: {work_item_type}\n"
        f"Title: {title}\n"
        f"Product: {product}\n"
        f"Service: {service}\n\n"
        f"Description: {description}\n\n"
        f"Conversation: {conversation}\n"
    )

    report = call_llm(llm_prompt)
    full_report = (
        report.strip()
        + "\n\nConversation with client (chronological):\n"
        + conversation
    )
    return full_report

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

def ado_parse_id_from_url(url: str) -> Optional[int]:
    try:
        # expected e.g. https://dev.azure.com/{org}/{project}/_workitems/edit/{id}
        # Be resilient to trailing params or alternative shapes; grab the last digit run.
        digits = re.findall(r"(\d+)", url or "")
        if not digits:
            return None
        return int(digits[-1])
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
    raw_desc = f.get("System.Description", "") or f.get("Microsoft.VSTS.TCM.ReproSteps", "") or ""

    # Extract and describe images
    image_descriptions = ""
    if raw_desc:
        images = _extract_images_from_html(raw_desc)
        if images:
            print(f"[ADO_FETCH] Found {len(images)} images in ticket {work_item_id}, describing via vision...")
            image_texts = []
            for img_url in images[:3]:  # Limit to first 3 images
                desc = _describe_image_via_vision(img_url)
                image_texts.append(desc)
            if image_texts:
                image_descriptions = "\n\nImages in description:\n" + "\n".join(image_texts)

    desc = _strip_html(raw_desc) + image_descriptions

    comments_text = []
    try:
        c = requests.get(f"{base}/_apis/wit/workItems/{work_item_id}/comments?api-version=7.1-preview.3", headers=hdrs, timeout=60)
        if c.status_code == 200:
            for it in c.json().get("comments", []):
                txt = it.get("text", "")
                if txt:
                    # Also check for images in comments
                    comment_images = _extract_images_from_html(txt)
                    comment_text = _strip_html(txt)
                    if comment_images:
                        for img_url in comment_images[:2]:
                            img_desc = _describe_image_via_vision(img_url)
                            comment_text += f"\n[Image: {img_desc}]"
                    comments_text.append(comment_text)
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
        skipped_empty: List[str] = []
        skipped_no_chunks: List[str] = []
        skipped_errors: List[str] = []
        
        for idx, rel in enumerate(to_ingest, start=1):
            abs_path = os.path.join(repo_dir, rel)
            print(f"[COMPARE_INGEST] [{idx}/{len(to_ingest)}] Ingesting file: {rel}")
            try:
                with open(abs_path, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
            except Exception as e:
                print(f"[COMPARE_INGEST][ERROR] Failed to read {rel}: {e}")
                skipped_errors.append(rel)
                continue

            if not text.strip():
                print(f"[COMPARE_INGEST] Empty file {rel} → skipping")
                skipped_empty.append(rel)
                continue

            chunks = chunk_text(text)
            if not chunks:
                print(f"[COMPARE_INGEST] 0 chunks for {rel} → skipping")
                skipped_no_chunks.append(rel)
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
                skipped_errors.append(rel)

        total = collection.count()
        
        # Print summary
        print(f"[COMPARE_INGEST] ===== SUMMARY =====")
        print(f"[COMPARE_INGEST] Total files in wiki repo: {len(md_files)}")
        print(f"[COMPARE_INGEST] Already ingested: {len(existing_sources)}")
        print(f"[COMPARE_INGEST] Missing files found: {len(to_ingest)}")
        print(f"[COMPARE_INGEST] Successfully ingested: {added_chunks} chunks")
        print(f"[COMPARE_INGEST] Skipped (empty files): {len(skipped_empty)}")
        print(f"[COMPARE_INGEST] Skipped (no chunks): {len(skipped_no_chunks)}")
        print(f"[COMPARE_INGEST] Skipped (errors): {len(skipped_errors)}")
        print(f"[COMPARE_INGEST] Total chunks in DB: {total}")
        
        if skipped_empty:
            print(f"[COMPARE_INGEST] Empty files list ({len(skipped_empty)} files):")
            for f in skipped_empty[:10]:  # Show first 10
                print(f"[COMPARE_INGEST]   - {f}")
            if len(skipped_empty) > 10:
                print(f"[COMPARE_INGEST]   ... and {len(skipped_empty) - 10} more")
        
        print(f"[COMPARE_INGEST] ==================")
        print(f"[COMPARE_INGEST] DONE: api worked properly (added_chunks={added_chunks}, total_chunks={total})")
        
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

def _normalize_question(question: str) -> str:
    """Normalize question to a canonical form to improve recall."""
    if not question:
        return ""
    q = question.lower()
    q = re.sub(r"[^a-z0-9\s\-]", " ", q)
    q = re.sub(r"\s+", " ", q).strip()
    return q


def _is_ta9_question(question: str) -> bool:
    if not question:
        return False
    q = question.lower()
    ta9_terms = [
        "ta9", "intsight", "int-sight", "intsight", "platform", "system",
        "features", "capabilities", "modules", "use cases", "overview",
        "dashboard", "admin studio", "data model", "dm"
    ]
    return any(t in q for t in ta9_terms)


def _is_foundational_question(question: str) -> bool:
    """Detect if question is about foundational product concepts that should always be answered."""
    if not question:
        return False
    q = question.lower()
    foundational_terms = [
        "what is", "what are", "explain", "define", "how does", "how do",
        "data model", "entity", "detection", "dashboard", "admin studio",
        "module", "feature", "capability", "system", "platform",
        "link analysis", "timeline", "geospatial", "visualization",
        "criteria", "field", "dm", "configuration"
    ]
    return any(t in q for t in foundational_terms)


def _build_query_variants(question: str, ta9_mode: bool) -> List[str]:
    """Generate a small set of semantically-equivalent queries for multi-retrieval."""
    variants = []
    base = question.strip()
    if base:
        variants.append(base)
    normalized = _normalize_question(question)
    if normalized and normalized not in variants:
        variants.append(normalized)
    if ta9_mode:
        ta9_boost = (
            "TA9 / IntSight platform features, capabilities, modules, "
            "system overview, dashboards, admin studio, data model"
        )
        variants.append(f"{base}\n\n{ta9_boost}" if base else ta9_boost)
    return variants[:3]

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
    # Safety: handle None doc from ChromaDB
    if doc is None:
        doc = ""
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


def _content_similarity(text1: str, text2: str, threshold: float = 0.7) -> float:
    """
    Calculate similarity between two texts based on overlapping tokens.
    Returns a value between 0 and 1.
    """
    if not text1 or not text2:
        return 0.0
    
    tokens1 = set([t.lower() for t in text1.split() if len(t) > 3])
    tokens2 = set([t.lower() for t in text2.split() if len(t) > 3])
    
    if not tokens1 or not tokens2:
        return 0.0
    
    intersection = len(tokens1 & tokens2)
    union = len(tokens1 | tokens2)
    
    return intersection / union if union > 0 else 0.0


def _smart_deduplicate_and_diversify(
    docs: List[str],
    metas: List[dict],
    distances: Optional[List[float]] = None,
    ids: Optional[List[str]] = None,
    similarity_threshold: float = 0.65,
    max_chunks_per_source: int = 2,
) -> Tuple[List[str], List[dict], List[float], List[str]]:
    """
    Deduplicate results by:
    1. Removing near-duplicate documents (content similarity > threshold)
    2. Limiting consecutive chunks from same source
    3. Preferring diverse sources for better context
    
    Returns deduplicated and diversified lists.
    """
    if not docs:
        return docs, metas, distances or [], ids or []
    
    print(f"[DEDUP] Starting deduplication: {len(docs)} docs, similarity_threshold={similarity_threshold}")
    
    selected_items = []
    seen_contents = []  # Track content we've already selected
    source_chunk_count = {}  # Track how many chunks from each source
    
    for idx, (doc, meta, dist, id_val) in enumerate(zip(
        docs, metas, distances or [None]*len(docs), ids or [None]*len(docs)
    )):
        if not doc:
            continue
        
        source = meta.get("source", "unknown") if meta else "unknown"
        chunk_num = meta.get("chunk", 0) if meta else 0
        source_key = source.split()[0]  # Get base source name (e.g., "ado:learn:123" → "ado:learn:123")
        
        # Check if we've already included max chunks from this source
        if source_key in source_chunk_count and source_chunk_count[source_key] >= max_chunks_per_source:
            print(f"[DEDUP] Skipping doc idx={idx} source={source} (already have {max_chunks_per_source} chunks from this source)")
            continue
        
        # Check for content similarity with already selected docs
        is_duplicate = False
        for seen_doc in seen_contents:
            similarity = _content_similarity(doc, seen_doc, threshold=similarity_threshold)
            if similarity > similarity_threshold:
                print(f"[DEDUP] Skipping doc idx={idx} source={source} (similarity={similarity:.2f} > threshold={similarity_threshold})")
                is_duplicate = True
                break
        
        if is_duplicate:
            continue
        
        # This doc is acceptable
        selected_items.append({
            "doc": doc,
            "meta": meta or {},
            "dist": dist,
            "id": id_val,
            "source": source,
        })
        seen_contents.append(doc)
        source_chunk_count[source_key] = source_chunk_count.get(source_key, 0) + 1
    
    dedup_docs = [item["doc"] for item in selected_items]
    dedup_metas = [item["meta"] for item in selected_items]
    dedup_distances = [item["dist"] for item in selected_items if item["dist"] is not None]
    dedup_ids = [item["id"] for item in selected_items if item["id"] is not None]
    
    print(f"[DEDUP] After deduplication: {len(dedup_docs)} docs (removed {len(docs) - len(dedup_docs)} duplicates/chunks)")
    return dedup_docs, dedup_metas, dedup_distances, dedup_ids


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
        # Safety: skip None documents
        if d is None:
            print(f"[RERANK] Skipping None doc at idx={idx}")
            continue
        s = lexical_boost_score(question, d, m)
        dist = None if distances is None or idx >= len(distances) else distances[idx]
        idv = None if ids is None or idx >= len(ids) else ids[idx]
        items.append({"doc": d, "meta": m, "score": s, "idx": idx, "dist": dist, "id": idv})

    if all(it["score"] == 0 for it in items):
        print("[RERANK] All scores=0 → keeping original vector order")
        # Still print a summary of results
        for it in items[:10]:
            print(f"[RERANK] src={it['meta'].get('source')} chunk={it['meta'].get('chunk')} id={it['id']} dist={it['dist']}")
        
        # Even with 0 score, apply deduplication
        reranked_docs = [it["doc"] for it in items]
        reranked_metas = [it["meta"] for it in items]
        reranked_distances = [it["dist"] for it in items]
        reranked_ids = [it["id"] for it in items]
        return _smart_deduplicate_and_diversify(reranked_docs, reranked_metas, reranked_distances, reranked_ids)

    items.sort(key=lambda x: (-x["score"], x["idx"]))

    print("[RERANK] Top 10 after rerank (score, dist, id, source, chunk):")
    for it in items[:10]:
        print(f"         score={it['score']:.2f} dist={it['dist']} id={it['id']} source={it['meta'].get('source')} chunk={it['meta'].get('chunk')}")

    reranked_docs = [it["doc"] for it in items]
    reranked_metas = [it["meta"] for it in items]
    reranked_distances = [it["dist"] for it in items]
    reranked_ids = [it["id"] for it in items]
    
    # Apply comprehensive deduplication and diversification
    return _smart_deduplicate_and_diversify(reranked_docs, reranked_metas, reranked_distances, reranked_ids)


def _lexical_overlap_ratio(question: str, doc: str) -> float:
    if not question or not doc:
        return 0.0
    # Extra safety: handle None explicitly
    if doc is None or question is None:
        return 0.0
    q_tokens = {t.lower() for t in str(question).split() if len(t) > 3}
    d_tokens = {t.lower() for t in str(doc).split() if len(t) > 3}
    if not q_tokens or not d_tokens:
        return 0.0
    inter = len(q_tokens & d_tokens)
    return inter / max(1, len(q_tokens))


def _is_context_relevant(
    question: str,
    docs: List[str],
    distances: Optional[List[float]],
    max_distance: float = 0.45,
    min_overlap: float = 0.08,
) -> bool:
    """
    Lightweight answerability gate:
    - Require at least one doc with acceptable semantic distance
    - Require minimal lexical overlap to avoid unrelated KB answers
    """
    if not docs:
        return False
    best_dist = None
    if distances:
        best_dist = min(distances)
    if best_dist is not None and best_dist > max_distance:
        return False
    # Filter out None docs before checking overlap
    top_docs = [d for d in docs[:3] if d is not None]
    if not top_docs:
        return False
    max_overlap = max((_lexical_overlap_ratio(question, d) for d in top_docs), default=0.0)
    return max_overlap >= min_overlap


def _generate_contextual_rejection(question: str, docs: List[str] = None) -> str:
    """
    Generate an intelligent, question-aware rejection response using the LLM.
    Instead of returning a canned message, ask the LLM to:
    1. Acknowledge what the user asked
    2. Explain why it doesn't relate to available resources
    3. Ask for clarification in a way that mirrors their intent
    
    This ensures each rejection feels unique and personalized.
    """
    if not OPENAI_API_KEY:
        # Fallback to simple rejection if no LLM available
        return (
            "I don't see a clear connection between that question and the knowledge base. "
            "Could you clarify how it relates to the ticket, or ask a more specific support question?"
        )
    
    try:
        # Extract key phrases from the question to acknowledge what they asked
        question_phrases = []
        if "how" in question.lower():
            question_phrases.append("understand how something works")
        elif "why" in question.lower():
            question_phrases.append("understand why something happened")
        elif "what" in question.lower():
            question_phrases.append("learn what something is")
        elif "can" in question.lower() or "does" in question.lower():
            question_phrases.append("know if something is possible")
        else:
            question_phrases.append("solve a problem")
        
        # Build a prompt that generates a contextual rejection
        rejection_prompt = (
            "You are a helpful technical support assistant. A user asked a question, but it doesn't "
            "relate to the technical knowledge base or selected ticket.\n\n"
            f"User's question: {question}\n\n"
            "Your task: Generate a SHORT, natural response (1-2 sentences) that:\n"
            "1. Shows you understood what they're asking about (acknowledge their intent)\n"
            "2. Explains why the knowledge base can't help with this specific question\n"
            "3. Ask them to clarify how it relates to the selected ticket or ask a more specific technical question\n\n"
            "Keep it conversational and helpful, not robotic. Be brief.\n"
            "Response:"
        )
        
        rejection = call_llm(rejection_prompt)
        return rejection.strip() if rejection else (
            "I don't see a clear connection between your question and the knowledge base. "
            "Could you clarify what technical issue you're trying to solve?"
        )
    except Exception as e:
        print(f"[REJECTION][WARN] Failed to generate contextual rejection: {e}")
        # Fallback to a simple rejection
        return (
            "I don't see a clear connection between your question and the knowledge base. "
            "Could you provide more context about what you're trying to accomplish?"
        )


# ---------------------------------------------------------------------
# API Models
# ---------------------------------------------------------------------

class ChatRequest(BaseModel):
    question: str
    top_k: int = 5
    force_reingest: Optional[bool] = False
    ticket_url: Optional[str] = None
    teach: Optional[bool] = False
    # If a ticket is selected, set to True for follow-up messages after the first structured reply
    is_followup: Optional[bool] = False


class ChatResponse(BaseModel):
    answer: str
    sources: List[str]


class IngestResponse(BaseModel):
    added_chunks: int
    total_chunks: int
    message: Optional[str] = None


class AdoLearnIngestRequest(BaseModel):
    async_run: Optional[bool] = False
    limit: Optional[int] = None
    force: Optional[bool] = False


class AdoLearnIngestResponse(BaseModel):
    added_chunks: int
    total_chunks: int
    tickets_processed: int
    tickets_skipped: int
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
        "embedding_backend": "openai",
        "embedding_model": OPENAI_EMBEDDING_MODEL,
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


# ---------------------------------------------------------------------
# Debug/Inspect Endpoint
# ---------------------------------------------------------------------

@app.get("/debug/inspect_vectors")
def inspect_vectors(source_pattern: str = "ado:learn:", limit: int = 10):
    """
    Inspect stored vectors and their documents.
    Use source_pattern to filter (e.g., 'ado:learn:' for tickets, or a specific file name).
    """
    print(f"[API][DEBUG] /debug/inspect_vectors source_pattern={source_pattern} limit={limit}")
    try:
        # Get all items (up to limit) matching the pattern
        results = collection.get(
            include=["documents", "metadatas"],
            limit=min(limit * 100, 10000),  # Fetch more to filter
        )
        
        docs = results.get("documents", [])
        metas = results.get("metadatas", [])
        ids = results.get("ids", [])
        
        # Filter by source pattern
        filtered = []
        for i, (doc, meta) in enumerate(zip(docs, metas)):
            source = meta.get("source", "") if meta else ""
            if source_pattern in source:
                filtered.append({
                    "id": ids[i] if i < len(ids) else None,
                    "source": source,
                    "chunk": meta.get("chunk", 0) if meta else 0,
                    "ticket_id": meta.get("ticket_id") if meta else None,
                    "title": meta.get("title") if meta else None,
                    "type": meta.get("type") if meta else None,
                    "state": meta.get("state") if meta else None,
                    "document_preview": doc[:500] if doc else "",
                    "document_length": len(doc) if doc else 0,
                    "full_document": doc,
                })
                if len(filtered) >= limit:
                    break
        
        return {
            "total_matching": len(filtered),
            "items": filtered,
        }
    except Exception as exc:
        print(f"[API][DEBUG][ERROR] {exc}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(exc))


# ---------------------------------------------------------------------
# Compare and Ingest Endpoint
# ---------------------------------------------------------------------

@app.post("/compare_and_ingest", response_model=IngestResponse)
def compare_and_ingest(async_run: bool = False, background_tasks: BackgroundTasks = None):
    """
    Compare wiki files to the vector DB and ingest only missing ones.
    Safe to call manually (curl) or via the scheduler.
    """
    # Optional background mode to avoid long-running request timeouts
    if async_run:
        print("[API][COMPARE_INGEST] async_run=True → scheduling background task")

        def _bg_job():
            try:
                a, t = compare_and_ingest_internal()
                print(f"[API][COMPARE_INGEST][ASYNC] DONE: api worked properly (added_chunks={a}, total_chunks={t})")
            except Exception as e:
                print(f"[API][COMPARE_INGEST][ASYNC][ERROR] {e}")
                traceback.print_exc()

        if background_tasks is not None:
            background_tasks.add_task(_bg_job)
        else:
            # Fallback if BackgroundTasks not provided
            asyncio.create_task(asyncio.to_thread(_bg_job))
        # We can't know counts yet; return immediate acknowledgement
        try:
            current_total = collection.count()
        except Exception:
            current_total = 0
        print("[API][COMPARE_INGEST] async ok: api worked! background task scheduled; responding immediately")
        return IngestResponse(
            added_chunks=0,
            total_chunks=current_total,
            message="api worked! compare_and_ingest started in background; check logs for progress",
        )

    try:
        added, total = compare_and_ingest_internal()
        if added == 0:
            msg = "No new files to ingest. All wiki files are already in the vector database."
        else:
            msg = f"Successfully ingested {added} new chunks from wiki files."
        print(f"[API][COMPARE_INGEST] success: api worked properly (added_chunks={added}, total_chunks={total})")
        return IngestResponse(added_chunks=added, total_chunks=total, message=msg)
    except Exception as exc:
        print(f"[API][COMPARE_INGEST][ERROR] {exc}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(exc))


# ---------------------------------------------------------------------
# Azure DevOps Learning Tickets Ingest Endpoint
# ---------------------------------------------------------------------

def ingest_learning_tickets_internal(limit: Optional[int] = None, force: bool = False) -> Tuple[int, int, int, int]:
    if not (ADO_ORG and ADO_PROJECT and ADO_PAT):
        raise RuntimeError("Azure DevOps is not configured. Set ADO_ORG, ADO_PROJECT, ADO_PAT env vars.")
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not configured; cannot generate ticket reports.")

    ids = ado_list_learning_tickets(limit=limit)
    if not ids:
        return 0, collection.count(), 0, 0

    existing_sources = set(get_ingested_sources()) if not force else set()
    added_chunks = 0
    tickets_processed = 0
    tickets_skipped = 0

    for idx, ticket_id in enumerate(ids, start=1):
        source = f"ado:learn:{ticket_id}"
        if source in existing_sources:
            print(f"[ADO][LEARN] Skipping already ingested ticket {ticket_id}")
            tickets_skipped += 1
            continue

        print(f"[ADO][LEARN] [{idx}/{len(ids)}] Processing ticket {ticket_id}")
        try:
            ticket = ado_fetch_ticket_full(ticket_id)
            report = generate_professional_ticket_report(ticket)
        except Exception as e:
            print(f"[ADO][LEARN][ERROR] Failed to build report for ticket {ticket_id}: {e}")
            traceback.print_exc()
            tickets_skipped += 1
            continue

        chunks = chunk_text(report)
        if not chunks:
            print(f"[ADO][LEARN][WARN] No chunks for ticket {ticket_id} → skipping")
            tickets_skipped += 1
            continue

        fields = ticket.get("fields", {})
        meta_title = _first_field(fields, ["System.Title"]) or ""
        meta_type = _first_field(fields, ["System.WorkItemType"]) or ""
        meta_state = _first_field(fields, ["System.State"]) or ""

        ids_to_add: List[str] = []
        docs: List[str] = []
        metas: List[dict] = []
        embeds: List[List[float]] = []

        for i, ch in enumerate(chunks):
            try:
                emb = embed_text(ch)
            except Exception as e:
                print(f"[ADO][LEARN][ERROR] Embedding failed ticket={ticket_id} chunk={i}: {e}")
                traceback.print_exc()
                continue
            ids_to_add.append(str(uuid.uuid4()))
            docs.append(ch)
            metas.append(
                {
                    "source": source,
                    "chunk": i,
                    "ticket_id": ticket_id,
                    "title": meta_title,
                    "type": meta_type,
                    "state": meta_state,
                    "query": LEARN_QUERY_NAME,
                }
            )
            embeds.append(emb)

        if not ids_to_add:
            print(f"[ADO][LEARN][WARN] No successful chunks for ticket {ticket_id} → skipping add()")
            tickets_skipped += 1
            continue

        try:
            collection.add(ids=ids_to_add, documents=docs, metadatas=metas, embeddings=embeds)
            added_chunks += len(ids_to_add)
            tickets_processed += 1
            print(f"[ADO][LEARN] Added {len(ids_to_add)} chunks for ticket {ticket_id}")
        except Exception as e:
            print(f"[ADO][LEARN][ERROR] Failed to add chunks for ticket {ticket_id}: {e}")
            traceback.print_exc()
            tickets_skipped += 1

    total_chunks = collection.count()
    return added_chunks, total_chunks, tickets_processed, tickets_skipped


@app.post("/azure/learn_tickets/ingest", response_model=AdoLearnIngestResponse)
def ingest_learning_tickets(req: AdoLearnIngestRequest, background_tasks: BackgroundTasks = None):
    """
    Run the Azure DevOps 'ai_learn_tickets_query' style WIQL, generate
    professional ticket reports, and store them in the Chroma collection.
    """
    if req.async_run:
        print("[API][ADO][LEARN] async_run=True → scheduling background task")

        def _bg_job():
            try:
                a, t, p, s = ingest_learning_tickets_internal(limit=req.limit, force=bool(req.force))
                print(
                    f"[API][ADO][LEARN][ASYNC] DONE: added_chunks={a}, total_chunks={t}, processed={p}, skipped={s}"
                )
            except Exception as e:
                print(f"[API][ADO][LEARN][ASYNC][ERROR] {e}")
                traceback.print_exc()

        if background_tasks is not None:
            background_tasks.add_task(_bg_job)
        else:
            asyncio.create_task(asyncio.to_thread(_bg_job))

        try:
            current_total = collection.count()
        except Exception:
            current_total = 0
        return AdoLearnIngestResponse(
            added_chunks=0,
            total_chunks=current_total,
            tickets_processed=0,
            tickets_skipped=0,
            message="api worked! learning tickets ingest started in background; check logs for progress",
        )

    try:
        added, total, processed, skipped = ingest_learning_tickets_internal(
            limit=req.limit, force=bool(req.force)
        )
        msg = (
            f"Processed {processed} tickets, skipped {skipped}, added {added} chunks."
            if processed or skipped
            else "No tickets matched the query."
        )
        return AdoLearnIngestResponse(
            added_chunks=added,
            total_chunks=total,
            tickets_processed=processed,
            tickets_skipped=skipped,
            message=msg,
        )
    except Exception as exc:
        print(f"[API][ADO][LEARN][ERROR] {exc}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(exc))


# ---------------------------------------------------------------------
# Chat Endpoint
# ---------------------------------------------------------------------

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    print(f"[API][CHAT] /chat called question='{req.question[:200]}' top_k={req.top_k} force_reingest={req.force_reingest}")
    question = (req.question or "").strip()

    # Parse ticket selection early so we can allow an empty initial message to trigger the first structured reply
    selected_ticket_id: Optional[int] = None
    selected_ticket_text: Optional[str] = None
    ticket_key: Optional[str] = None
    if req.ticket_url:
        ticket_key = (req.ticket_url or "").strip() or None
        selected_ticket_id = ado_parse_id_from_url(req.ticket_url)
        if selected_ticket_id is not None:
            ticket_key = str(selected_ticket_id)
            print(f"[API][CHAT] Fetching Azure DevOps ticket id={selected_ticket_id}")
            try:
                selected_ticket_text = ado_fetch_ticket_text(int(selected_ticket_id))
            except Exception as e:
                print(f"[API][CHAT][WARN] failed to fetch ticket: {e}")
                selected_ticket_text = None

    has_ticket = bool(ticket_key)

    # Enforce non-empty question
    if not question:
        print("[API][CHAT][ERROR] Empty question")
        raise HTTPException(status_code=400, detail="question is empty")

    if req.force_reingest:
        print("[API][CHAT] force_reingest=True → calling ingest_wiki_files(force=True)")
        ingest_wiki_files(force=True)

    ta9_mode = _is_ta9_question(question)
    is_foundational = _is_foundational_question(question)
    query_variants = _build_query_variants(question, ta9_mode)
    ticket_context_hint = None
    if selected_ticket_text:
        # Keep a short hint to enrich similarity search without overwhelming the question
        ticket_context_hint = (selected_ticket_text[:800] or "").strip()

    emb_results = []

    primary_emb = None
    agg_ids: List[str] = []
    agg_distances: List[float] = []
    agg_docs: List[str] = []
    agg_metas: List[dict] = []

    try:
        for idx, qv in enumerate(query_variants):
            augmented_qv = augment_question(qv)
            q_emb = embed_text(augmented_qv)
            if idx == 0:
                primary_emb = q_emb
                # Log a short preview of the query embedding used for vector search
                q_preview = ",".join([f"{x:.6f}" for x in q_emb[:EMBED_PREVIEW_COUNT]])
                q_norm = math.sqrt(sum([x * x for x in q_emb]))
                q_hash = hashlib.sha256(
                    ",".join([f"{x:.6f}" for x in q_emb[:16]]).encode("utf-8")
                ).hexdigest()[:12]
                print(f"[API][CHAT] Query embedding preview=[{q_preview}] len={len(q_emb)} norm={q_norm:.6f} hash={q_hash}")
                if LOG_FULL_EMBEDDINGS:
                    print(f"[API][CHAT] Query embeddings FULL={q_emb}")

            # More candidates improves recall a lot
            effective_top_k = max(req.top_k, 50)
            per_query_k = max(20, min(50, effective_top_k // max(1, len(query_variants))))
            print(f"[API][CHAT] effective_top_k={effective_top_k} per_query_k={per_query_k} variant_idx={idx}")

            # Primary search: question-focused
            results = collection.query(
                query_embeddings=[q_emb],
                n_results=per_query_k,
                include=["distances", "documents", "metadatas", "embeddings"],
            )

            ids = results.get("ids", [[]])[0]
            distances = results.get("distances", [[]])[0]
            docs = results.get("documents", [[]])[0]
            metas = results.get("metadatas", [[]])[0]

            agg_ids.extend(ids or [])
            agg_distances.extend(distances or [])
            agg_docs.extend(docs or [])
            agg_metas.extend(metas or [])
    except Exception as exc:
        print(f"[API][CHAT][ERROR] Embedding or vector search failed: {exc}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Embedding/vector search failed: {exc}")

    ids = agg_ids
    distances = agg_distances
    docs = agg_docs
    metas = agg_metas

    # Secondary search: ticket-aware similarity without overriding the question
    if ticket_context_hint:
        try:
            similar_query = question + "\n\nRelated ticket context:\n" + ticket_context_hint
            sim_emb = embed_text(similar_query)
            sim_results = collection.query(
                query_embeddings=[sim_emb],
                n_results=max(20, req.top_k * 4),
                include=["distances", "documents", "metadatas", "ids"],
            )
            sim_ids = sim_results.get("ids", [[]])[0]
            sim_distances = sim_results.get("distances", [[]])[0]
            sim_docs = sim_results.get("documents", [[]])[0]
            sim_metas = sim_results.get("metadatas", [[]])[0]

            if sim_docs:
                docs = docs + sim_docs
                metas = metas + sim_metas
                ids = ids + sim_ids
                distances = distances + sim_distances
                print(f"[API][CHAT] Added {len(sim_docs)} ticket-similar docs to candidates")
        except Exception as e:
            print(f"[API][CHAT][WARN] Similar-ticket search failed: {e}")

    print(f"[API][CHAT] Vector search returned {len(docs)} docs")
    # Log top matches briefly (id, dist, source, chunk, snippet)
    for i, (d, m) in enumerate(zip(docs, metas)):
        if i >= 10:
            break
        did = ids[i] if i < len(ids) else None
        dist = distances[i] if i < len(distances) else None
        snippet = (d[:200].replace("\n", " ") + "...") if d else ""
        m_safe = m or {}
        dist_str = f"{dist:.4f}" if dist is not None else "N/A"
        print(f"[API][CHAT] Result {i}: id={did} dist={dist_str} source={m_safe.get('source', 'N/A')} chunk={m_safe.get('chunk', 'N/A')} snippet='{snippet[:100]}'")

    # No forced root-file injection: all files treated equally

    # Also include memory snippets related to the question
    # Gather memory docs (generic + ticket-specific) but do not pin them; they will be reranked
    try:
        mem_query_emb = primary_emb or embed_text(question)
        mem = memory_collection.query(
            query_embeddings=[mem_query_emb],
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

    if not docs:
        print("[API][CHAT] No docs after injection → calling LLM with 'no context' message")
        answer = call_llm(
            "No wiki context available. Answer briefly but mention that you "
            "do not have access to the internal knowledge base.\n\n"
            f"Question: {question}"
        )
        return ChatResponse(answer=answer, sources=[])

    docs, metas, distances, ids = rerank_results(question, docs, metas, distances=distances, ids=ids)

    # Answerability gate: refuse to answer if context does not match the question
    # BUT: be much more permissive when ticket is selected OR for foundational/TA9 questions
    # Most relaxed: ticket selected + any question = answer from ticket context
    if selected_ticket_text:
        max_dist = 0.85  # VERY permissive when ticket is primary context
        min_overlap = 0.0  # Don't require lexical overlap - ticket context is king
    elif ta9_mode or is_foundational:
        max_dist = 0.70  # Very permissive for product questions
        min_overlap = 0.01  # Minimal lexical overlap required
    else:
        max_dist = 0.45
        min_overlap = 0.08
    
    if not _is_context_relevant(question, docs, distances, max_distance=max_dist, min_overlap=min_overlap):
        # For ticket-based, foundational/TA9 questions, even with weak context, answer from context
        if selected_ticket_text or ta9_mode or is_foundational:
            print(f"[API][CHAT] Weak context but permissive mode enabled (ticket={bool(selected_ticket_text)}, ta9={ta9_mode}, foundational={is_foundational})")
            # Don't reject - fall through to answer with weak context
        else:
            rejection_msg = _generate_contextual_rejection(question, docs)
            return ChatResponse(answer=rejection_msg, sources=[])

    context_blocks: List[str] = []
    source_strings: List[str] = []

    # More context improves answer success rate
    MAX_CONTEXT_DOCS = 12
    print(f"[API][CHAT] Building context with MAX_CONTEXT_DOCS={MAX_CONTEXT_DOCS}")

    # Build context blocks: prioritize retrieved knowledge, then add selected ticket as supplemental context
    remaining_slots = MAX_CONTEXT_DOCS - (1 if selected_ticket_text else 0)
    for i, (doc, meta) in enumerate(list(zip(docs, metas))[:remaining_slots]):
        id_val = ids[i] if i < len(ids) else None
        dist_val = distances[i] if i < len(distances) else None
        src = f"{meta.get('source')} (chunk {meta.get('chunk', 0)}) id={id_val} dist={dist_val}"
        source_strings.append(src)
        snippet = doc[:200].replace("\n", " ")
        print(f"[API][CHAT] Context source: {src} | snippet='{snippet}...'")
        context_blocks.append(f"Source: {src}\n{doc}")

    if selected_ticket_text:
        src = f"azure-devops:{selected_ticket_id} (selected ticket)"
        source_strings.append(src)
        snippet = selected_ticket_text[:200].replace("\n", " ")
        print(f"[API][CHAT] Context source: {src} | snippet='{snippet}...'")
        context_blocks.append(f"Source: {src}\n{selected_ticket_text}")

    context_text = "\n\n---\n\n".join(context_blocks)

    # Enhanced prompt that handles potentially redundant context intelligently
    foundational_instruction = (
        "10. FOUNDATIONAL QUESTIONS: If asked about core product concepts (data models, entities, features, Federated Search, Cases, Link Analysis etc.), "
        "provide a clear explanation even if the context is weak. Explain the concept, then connect it to the product. "
        "Never refuse to answer foundational product questions - help the user understand.\n\n"
        if is_foundational or ta9_mode
        else ""
    )
    
    ta9_instruction = (
        "11. If the question is about TA9/IntSight features or platform capabilities, "
        "provide a comprehensive, structured answer with key features, modules, and examples. "
        "Use bullet points and be more explanatory.\n\n"
        if ta9_mode
        else ""
    )

    prompt = (
        "You are a TA9 / IntSight customer support assistant with deep technical knowledge. "
        "Your role is to provide clear, accurate, and helpful answers that keep users engaged.\n\n"
        "IMPORTANT INSTRUCTIONS:\n"
        "1. Prioritize user understanding over document perfection. If asked about foundational concepts, explain them clearly.\n"
        + (
            "2. TICKET CONTEXT: A ticket has been selected. Use the ticket information as PRIMARY context to understand the user's issue and provide relevant solutions.\n"
            if selected_ticket_text
            else "2. Use context from the knowledge base to answer the question accurately.\n"
        )
        + "3. If the user asks for similar tickets, identify and compare the most similar cases from context.\n"
        "4. Use fenced code blocks (```bash, ```python, ```sql, etc.) for any commands or code snippets.\n"
        "5. If the context contains redundant or overlapping information, synthesize it into a single coherent answer.\n"
        "6. Do NOT simply repeat information from different sources - intelligently merge related points.\n"
        "7. For product-related questions, you can use general product knowledge even if context is weak, "
        "but always try to reference the context when available.\n"
        "8. Keep a professional, helpful tone that encourages follow-up questions.\n"
        "9. If multiple sources provide similar information, cite the most authoritative or recent source.\n"
        f"{foundational_instruction}"
        f"{ta9_instruction}"
        f"Context from knowledge base and ticket:\n{context_text}\n\n"
        f"Question: {question}\n\n"
        "Answer:"
    )

    try:
        answer = call_llm(prompt, temperature=0.35 if ta9_mode else 0.2)
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
