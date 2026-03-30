import os
import uuid
import pathlib
import time
import traceback
from typing import List, Optional, Tuple, Dict, Any, Deque
from collections import Counter, defaultdict, deque

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from dotenv import load_dotenv
import requests
import math
import hashlib
import fnmatch
import chromadb
import base64
from datetime import datetime
import asyncio
import re
from html import unescape
import subprocess
import tempfile
import shutil
import json
import mimetypes
from io import BytesIO
from urllib.parse import unquote, quote, urlsplit, urlunsplit, parse_qsl, urlencode
import threading

# Try to import optional dependencies
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import openpyxl
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False

import csv

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

try:
    import fitz
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False

try:
    import tiktoken
    HAS_TIKTOKEN = True
except ImportError:
    HAS_TIKTOKEN = False

load_dotenv()

# ---------------------------------------------------------------------
# Env & constants
# ---------------------------------------------------------------------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_URL = os.getenv("OPENAI_URL", "https://api.openai.com/v1").rstrip("/")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")
OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
OPENAI_RERANK_MODEL = os.getenv("OPENAI_RERANK_MODEL", OPENAI_CHAT_MODEL)
OPENAI_VISION_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4o")
LOG_FULL_EMBEDDINGS = os.getenv("LOG_FULL_EMBEDDINGS", "false").lower() in ("1", "true", "yes")
EMBED_PREVIEW_COUNT = int(os.getenv("EMBED_PREVIEW_COUNT", "8"))

# SINGLE ROOT DIRECTORY: all .md files are under /app/wiki_files
WIKI_ROOT = os.getenv("WIKI_DIR", "/app/wiki_files")

# Directory exposed for "Add Knowledge" server file listing
KNOWLEDGE_DIR = os.getenv("KNOWLEDGE_DIR", WIKI_ROOT)

CHROMA_DIR = os.getenv("CHROMA_DIR", "/app/chroma_db")
SYSTEM_PROMPT_FILE = os.getenv("SYSTEM_PROMPT_FILE", "/app/system_prompt_template.txt")
SYSTEM_PROMPT_DISPLAY_PATH = os.getenv("SYSTEM_PROMPT_DISPLAY_PATH", "backend/system_prompt_template.txt")

# Chunk configuration optimized for large files (2M+ tokens)
# Larger chunks = fewer embeddings = faster processing of massive files
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "2000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "300"))

COLLECTION_NAME = "Intsight"
MEMORY_COLLECTION_NAME = "New_Knowledge"
VECTOR_DB_PREVIEW_CHARS = 280
VECTOR_DB_DEFAULT_CHUNK_LIMIT = 25
VECTOR_DB_MAX_CHUNK_LIMIT = 100

# PDF processing: optimized for large files
# PDF_MAX_PAGES=0 means unlimited (process entire file)
PDF_MAX_PAGES = int(os.getenv("PDF_MAX_PAGES", "0"))
PDF_OCR_ENABLED = os.getenv("PDF_OCR_ENABLED", "true").lower() in ("1", "true", "yes")
# For image-heavy PDFs, analyze ALL pages with vision model (not just first 50)
PDF_OCR_MAX_PAGES = int(os.getenv("PDF_OCR_MAX_PAGES", "0"))  # 0 = unlimited = analyze all pages
PDF_TABLE_EXTRACTION_ENABLED = os.getenv("PDF_TABLE_EXTRACTION_ENABLED", "true").lower() in ("1", "true", "yes")
# Aggressive image extraction from ALL PDF pages (not just fallback)
PDF_IMAGE_EXTRACTION_ENABLED = os.getenv("PDF_IMAGE_EXTRACTION_ENABLED", "true").lower() in ("1", "true", "yes")
PDF_MAX_IMAGES_PER_PAGE = int(os.getenv("PDF_MAX_IMAGES_PER_PAGE", "4"))
PDF_MIN_IMAGE_AREA_RATIO = float(os.getenv("PDF_MIN_IMAGE_AREA_RATIO", "0.015"))

# Vision model configuration
VISION_MAX_TOKENS = int(os.getenv("VISION_MAX_TOKENS", "2500"))
VISION_TIMEOUT_SECONDS = int(os.getenv("VISION_TIMEOUT_SECONDS", "120"))
VISION_RETRY_COUNT = int(os.getenv("VISION_RETRY_COUNT", "2"))

# Large file processing support (up to 2M tokens per uploaded or fetched file)
MAX_FILE_SIZE_TOKENS = int(os.getenv("MAX_FILE_SIZE_TOKENS", "2000000"))
BLOCK_PROCESSING_ENABLED = os.getenv("BLOCK_PROCESSING_ENABLED", "true").lower() in ("1", "true", "yes")
DETAILED_INGEST_LOGS = os.getenv("DETAILED_INGEST_LOGS", "true").lower() in ("1", "true", "yes")
LLM_MAX_INPUT_TOKENS = 120000

TABLE_ROW_START_TAG = "[TABLE_ROW]"
TABLE_ROW_END_TAG = "[/TABLE_ROW]"

DEFAULT_SYSTEM_PROMPT_TEMPLATE = (
    "You are a TA9 / IntSight customer support assistant with deep technical knowledge. "
    "Your role is to provide clear, accurate, and helpful answers in a natural, conversational way.\n\n"
    "INSTRUCTIONS:\n"
    "1. When the user attaches files (images, documents), those files are your PRIMARY source - answer directly from them.\n"
    "2. When you see [Image Content from ...] sections, that means the image has been analyzed - describe what you see in the analysis naturally.\n"
    "3. For images: Provide a comprehensive explanation of what is shown in the provided analysis. Highlight key details, technical context, and likely causes when relevant.\n"
    "4. When a ticket is selected, use it to understand the user's issue and provide relevant solutions.\n"
    "4.1 For ticket responses, begin with a short explanation of the ticket before listing the solution steps.\n"
    "5. Use knowledge base context to supplement your answer or provide additional related information.\n"
    "6. Use fenced code blocks (```bash, ```python, ```sql, etc.) only for real commands, code, SQL queries, JSON, config files, or other text the user may copy and run exactly as-is.\n"
    "6.1 Do NOT use fenced code blocks for numbered steps, UI navigation sequences, button names, field labels, prose instructions, or short key-value notes such as 'Source: ...' or 'Type: ...'. Render those as normal Markdown text, numbered lists, or bullet points.\n"
    "6.2 A summary of steps (e.g., '1. Open Admin Studio and log in. 2. Locate the data model...') is NOT code — always render it as a plain numbered list, never inside a code fence.\n"
    "7. If the context contains redundant or overlapping information, synthesize it into a single coherent answer.\n"
    "8. Do NOT repeat information from different sources - intelligently merge related points.\n"
    "8.1 Use a balanced approach across both collections (Intsight and New_Knowledge) and do not assume one is always better.\n"
    "8.2 If relevant details are split across both collections, combine them into one integrated, consistent answer.\n"
    "9. Grounding is mandatory: only state facts supported by the provided context sections.\n"
    "9.1 If a requested detail is not in context, explicitly say it is not available in the current knowledge context.\n"
    "9.2 Never invent commands, configuration keys, UI paths, API names, or procedural steps.\n"
    "9.3 If the response is about a BUG ticket and the issue is not fully resolved, frame the ending as an INTERNAL escalation from support to engineering or R&D. Never tell the support engineer to 'contact support', 'reach out to support', or use wording that treats support as the customer.\n"
    "10. Keep a professional, helpful tone that encourages follow-up questions.\n"
    "11. Answer naturally and conversationally - avoid rigid structured formats unless specifically requested.\n"
    "12. For Intsight or system configuration guidance, ALWAYS provide instructions using Admin Studio (UI-based configuration) by default. Do NOT include SQL queries, INSERT/UPDATE statements, or direct database table manipulation unless the user explicitly asks.\n"
    "13. Provide database-level (DB) configuration instructions ONLY when the user explicitly mentions 'database', 'SQL', 'DB', 'table', 'query', or specifically requests backend/database-level steps. If the context contains both Admin Studio steps and DB-level steps for the same task, present ONLY the Admin Studio steps unless DB steps are explicitly requested.\n"
    "13.1 When DB steps are explicitly requested, you may include SQL queries and table-level instructions alongside the Admin Studio approach.\n"
    "14. Never hard-refuse when at least partial context exists; provide the best grounded answer possible, explicitly flag uncertainty, and ask one focused clarifying question if needed.\n"
    "14.1 For BUG tickets that remain unresolved, end with a brief internal handoff note to engineering or R&D and the information support should gather before escalation. Do NOT say 'contact support'.\n\n"
    "SOURCE SEPARATION AND ACCURACY:\n"
    "15. Each context block (labeled PRIMARY MATCH, SUPPLEMENTAL MATCH, or PRIORITY REFERENCE) comes from a DIFFERENT document. Treat each document as a separate, self-contained source.\n"
    "15.1 NEVER combine or merge procedural steps from different source documents into a single procedure. Each document describes its own workflow — mixing steps from Document A with steps from Document B creates incorrect instructions.\n"
    "15.2 If two source documents describe different procedures for related but distinct tasks, present them separately with clear labels. Do NOT interleave their steps.\n"
    "15.3 When multiple sources cover the same topic, use the one that best matches the user's specific question. Use supplemental sources only for additional context that the primary source does not cover.\n\n"
    "QUESTION ANALYSIS:\n"
    "16. Before answering, carefully analyze the user's question to understand what they ALREADY HAVE vs what they NEED:\n"
    "16.1 If the user says 'in a data model' or 'in my data model', the data model already exists — do NOT provide steps to create it. Focus on the specific operation they are asking about.\n"
    "16.2 If the user says 'configure X' or 'define X', they want to set up that specific feature — do NOT provide steps for creating the parent object that already exists.\n"
    "16.3 Pay attention to prepositions: 'in', 'on', 'for', 'within' usually indicate an existing context. 'Create', 'new', 'set up from scratch' indicate they need to build something new.\n"
    "16.4 Match the scope of your answer to the scope of the question. If the user asks about one specific feature within a larger system, focus your answer on that feature — do not explain the entire system setup.\n"
)

app = FastAPI(title="Wiki RAG API")

# Track if a structured "first ticket response" was already sent per ticket key (id or URL fallback)
ticket_first_reply_done: Dict[str, bool] = {}

# Lightweight in-memory conversation memory (per conversation key)
MAX_CONVERSATION_MESSAGES = 12
conversation_store: Dict[str, Deque[Dict[str, str]]] = defaultdict(
    lambda: deque(maxlen=MAX_CONVERSATION_MESSAGES)
)
conversation_state_store: Dict[str, Dict[str, Any]] = {}

# In-memory cancellation flags for long-running knowledge ingestion requests.
knowledge_cancel_lock = threading.Lock()
knowledge_cancel_flags: Dict[str, bool] = {}

# In-memory job store so knowledge_add returns immediately and the UI polls for the result.
knowledge_job_store: Dict[str, dict] = {}
knowledge_job_store_lock = threading.Lock()

# In-memory cache of merged vector document content for large document viewing.
VECTOR_DOCUMENT_CACHE_MAX_ITEMS = int(os.getenv("VECTOR_DOCUMENT_CACHE_MAX_ITEMS", "24"))
vector_document_cache: Dict[str, dict] = {}
vector_document_cache_lock = threading.Lock()


def _request_log_prefix(request_id: Optional[str]) -> str:
    return f"[rid={request_id}]" if request_id else "[rid=-]"


def _ingest_log(message: str, request_id: Optional[str] = None, force: bool = False) -> None:
    if DETAILED_INGEST_LOGS or force:
        print(f"[INGEST]{_request_log_prefix(request_id)} {message}")


def _rag_log_step(step_number: int, total_steps: int, title: str, detail: Optional[str] = None) -> None:
    prefix = f"[RAG][Step {step_number}/{total_steps}] {title}"
    if detail:
        print(f"{prefix}: {detail}")
    else:
        print(prefix)


def _mark_knowledge_request_started(request_id: Optional[str]) -> None:
    if not request_id:
        return
    with knowledge_cancel_lock:
        # If cancel arrived first, do not overwrite it.
        if knowledge_cancel_flags.get(request_id) is True:
            _ingest_log("request start observed after cancel signal; keeping canceled=true", request_id, force=True)
            return
        knowledge_cancel_flags[request_id] = False
    _ingest_log("request marked active", request_id)


def _cancel_knowledge_request(request_id: Optional[str]) -> bool:
    if not request_id:
        return False
    with knowledge_cancel_lock:
        existed = request_id in knowledge_cancel_flags
        knowledge_cancel_flags[request_id] = True
    _ingest_log(f"cancel signal stored (was_active={existed})", request_id, force=True)
    return existed


def _is_knowledge_request_cancelled(request_id: Optional[str]) -> bool:
    if not request_id:
        return False
    with knowledge_cancel_lock:
        return bool(knowledge_cancel_flags.get(request_id, False))


def _clear_knowledge_request(request_id: Optional[str]) -> None:
    if not request_id:
        return
    with knowledge_cancel_lock:
        knowledge_cancel_flags.pop(request_id, None)
    _ingest_log("request state cleared", request_id)


def _store_job_result(request_id: Optional[str], result: dict) -> None:
    if not request_id:
        return
    with knowledge_job_store_lock:
        # Evict very old completed jobs (older than 24 h) to keep memory bounded.
        cutoff = datetime.utcnow().isoformat()
        keys_to_remove = [
            k for k, v in knowledge_job_store.items()
            if v.get("status") == "done" and v.get("stored_at", cutoff) < cutoff
        ]
        # Keep at most 100 completed jobs regardless of age.
        done_jobs = [k for k, v in knowledge_job_store.items() if v.get("status") == "done"]
        if len(done_jobs) > 100:
            keys_to_remove += done_jobs[:-100]
        for k in keys_to_remove:
            knowledge_job_store.pop(k, None)
        result["stored_at"] = datetime.utcnow().isoformat() + "Z"
        knowledge_job_store[request_id] = result


def _get_job_result(request_id: Optional[str]) -> Optional[dict]:
    if not request_id:
        return None
    with knowledge_job_store_lock:
        return knowledge_job_store.get(request_id)


def _vector_document_cache_key(collection_name: str, source: str) -> str:
    return f"{collection_name}::{source}"


def _get_cached_vector_document_payload(collection_name: str, source: str) -> Optional[dict]:
    key = _vector_document_cache_key(collection_name, source)
    with vector_document_cache_lock:
        payload = vector_document_cache.get(key)
        if payload is None:
            return None
        # Refresh insertion order for simple LRU behavior.
        vector_document_cache.pop(key, None)
        vector_document_cache[key] = payload
        return dict(payload)


def _store_cached_vector_document_payload(
    collection_name: str,
    source: str,
    full_content: str,
    token_count: int,
) -> None:
    key = _vector_document_cache_key(collection_name, source)
    payload = {
        "full_content": full_content,
        "token_count": int(token_count or 0),
        "cached_at": datetime.utcnow().isoformat() + "Z",
    }
    with vector_document_cache_lock:
        vector_document_cache.pop(key, None)
        vector_document_cache[key] = payload
        while len(vector_document_cache) > VECTOR_DOCUMENT_CACHE_MAX_ITEMS:
            oldest_key = next(iter(vector_document_cache))
            vector_document_cache.pop(oldest_key, None)


def _invalidate_cached_vector_document_payload(collection_name: str, source: str) -> None:
    key = _vector_document_cache_key(collection_name, source)
    with vector_document_cache_lock:
        vector_document_cache.pop(key, None)


def _validate_system_prompt_template(template: str) -> str:
    candidate = str(template or "")
    if not candidate.strip():
        raise ValueError("System prompt template cannot be empty.")

    return candidate


def _read_system_prompt_template() -> str:
    try:
        with open(SYSTEM_PROMPT_FILE, "r", encoding="utf-8") as handle:
            template = handle.read()
        return _validate_system_prompt_template(template)
    except FileNotFoundError:
        return DEFAULT_SYSTEM_PROMPT_TEMPLATE
    except Exception as exc:
        print(f"[PROMPT][WARN] Failed to read system prompt template from {SYSTEM_PROMPT_FILE}: {exc}")
        return DEFAULT_SYSTEM_PROMPT_TEMPLATE


def _write_system_prompt_template(template: str) -> str:
    validated = _validate_system_prompt_template(template)
    parent = os.path.dirname(SYSTEM_PROMPT_FILE)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(SYSTEM_PROMPT_FILE, "w", encoding="utf-8") as handle:
        handle.write(validated)
    return validated


def _build_system_prompt(
    question: str,
    combined_context: str,
    foundational_instruction: str = "",
    ta9_instruction: str = "",
) -> str:
    template = _read_system_prompt_template().strip()
    sections: List[str] = [template]

    if foundational_instruction and foundational_instruction.strip():
        sections.append(foundational_instruction.strip())

    if ta9_instruction and ta9_instruction.strip():
        sections.append(ta9_instruction.strip())

    if combined_context and combined_context.strip():
        sections.append(combined_context.strip())

    sections.append(f"Question: {question}")
    sections.append("Answer:")
    return "\n\n".join(section for section in sections if section)


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


def call_llm(prompt: str, temperature: float = 0.2, model: Optional[str] = None) -> str:
    """Call OpenAI chat for final answer."""
    selected_model = (model or OPENAI_CHAT_MODEL).strip() or OPENAI_CHAT_MODEL
    print(f"[LLM] Calling OpenAI chat model={selected_model} prompt_len={len(prompt)} temp={temperature}")
    start = time.time()
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    body = {
        "model": selected_model,
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
    tokens_estimate = len(text) // 4
    print(f"[CHUNK] Splitting text len={len(text)} chars (~{tokens_estimate} tokens) size={size} overlap={overlap}")
    chunks: List[str] = []
    start_idx = 0
    while start_idx < len(text):
        end = min(start_idx + size, len(text))
        chunk = text[start_idx:end].strip()
        if chunk:
            chunks.append(chunk)
        start_idx += size - overlap
    total_tokens = sum(len(c) // 4 for c in chunks)
    print(f"[CHUNK] Produced {len(chunks)} chunks (~{total_tokens} tokens total)")
    return chunks


def chunk_text_preserve_table_rows(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    if not text:
        return []

    pattern = re.compile(r"\[TABLE_ROW\][\s\S]*?\[/TABLE_ROW\]")
    chunks: List[str] = []
    cursor = 0

    for match in pattern.finditer(text):
        regular_part = text[cursor:match.start()].strip()
        if regular_part:
            chunks.extend(chunk_text(regular_part, size=size, overlap=overlap))

        table_row_block = match.group(0).strip()
        if table_row_block:
            if len(table_row_block) <= size:
                chunks.append(table_row_block)
            else:
                chunks.extend(chunk_text(table_row_block, size=size, overlap=0))

        cursor = match.end()

    tail = text[cursor:].strip()
    if tail:
        chunks.extend(chunk_text(tail, size=size, overlap=overlap))

    print(f"[CHUNK] Produced {len(chunks)} chunks with TABLE_ROW preservation")
    return chunks


def extract_table_row_metadata(chunk: str) -> Dict[str, int]:
    if not chunk:
        return {}
    match = re.search(r"\[TABLE_ROW\]\s*page=(\d+)\s+table=(\d+)\s+row=(\d+)", chunk)
    if not match:
        return {}
    return {
        "table_page": int(match.group(1)),
        "table_index": int(match.group(2)),
        "table_row_index": int(match.group(3)),
    }


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
ADO_SUPPORT_TICKET_QUERY_TARGETS = os.getenv(
    "ADO_SUPPORT_TICKET_QUERY_TARGETS",
    "TA9 Support::My Queries/external tickets|STE Support Board::My Queries/external tickets",
)
ADO_SUPPORT_TICKET_ASSIGNED_TO = os.getenv(
    "ADO_SUPPORT_TICKET_ASSIGNED_TO",
    "Support <support@ta-9.com>",
)

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
    if ADO_PROJECT:
        return f"https://dev.azure.com/{ADO_ORG}/{ADO_PROJECT}"
    return f"https://dev.azure.com/{ADO_ORG}"


def _ado_project_base(project: Optional[str] = None) -> str:
    project_name = (project or ADO_PROJECT or "").strip()
    if project_name:
        return f"https://dev.azure.com/{ADO_ORG}/{project_name}"
    return f"https://dev.azure.com/{ADO_ORG}"


def _ado_query_api_path(query_path: str) -> str:
    parts = [quote(part.strip(), safe="") for part in str(query_path or "").split("/") if part.strip()]
    if not parts:
        raise RuntimeError("Azure DevOps query path is empty.")
    return "/".join(parts)


def _ado_support_ticket_query_definitions() -> List[Tuple[str, str]]:
    targets: List[Tuple[str, str]] = []
    for raw_target in str(ADO_SUPPORT_TICKET_QUERY_TARGETS or "").split("|"):
        target = raw_target.strip()
        if not target:
            continue
        if "::" not in target:
            print(f"[ADO][TICKETS][WARN] Ignoring malformed query target '{target}'. Expected Project::Query Path.")
            continue
        project, query_path = target.split("::", 1)
        project = project.strip()
        query_path = query_path.strip()
        if project and query_path:
            targets.append((project, query_path))
    if not targets:
        default_project = (ADO_PROJECT_TICKET_SUMMARY or ADO_PROJECT or "").strip()
        if default_project:
            targets.append((default_project, "My Queries/external tickets"))
    return targets


def _ado_support_ticket_fallback_wiql(project: str) -> str:
    project_name = str(project or "").replace("'", "''")
    assigned_to = str(ADO_SUPPORT_TICKET_ASSIGNED_TO or "").replace("'", "''")
    query = (
        "SELECT [System.Id] FROM WorkItems "
        f"WHERE [System.TeamProject] = '{project_name}' "
        "AND [System.State] <> 'Closed' "
    )
    if assigned_to:
        query += f"AND [System.AssignedTo] = '{assigned_to}' "
    query += "ORDER BY [System.ChangedDate] DESC"
    return query


def _ado_fetch_saved_query_wiql(project: str, query_path: str) -> str:
    url = (
        f"{_ado_project_base(project)}/_apis/wit/queries/{_ado_query_api_path(query_path)}"
        "?$expand=wiql&api-version=7.1"
    )
    resp = requests.get(url, headers=_ado_headers(), timeout=60)
    if resp.status_code != 200:
        raise RuntimeError(f"saved query fetch failed: {resp.status_code} {resp.text[:300]}")
    payload = resp.json()
    wiql = str(payload.get("wiql") or "").strip()
    if not wiql:
        raise RuntimeError(f"saved query '{query_path}' in project '{project}' did not return WIQL text")
    return wiql


def _ado_execute_wiql(project: str, wiql: str, label: str) -> List[int]:
    url = f"{_ado_project_base(project)}/_apis/wit/wiql?api-version=7.1-preview.2"
    try:
        resp = requests.post(url, json={"query": wiql}, headers=_ado_headers(), timeout=60)
    except Exception as e:
        print(f"[ADO][TICKETS][ERROR] Query '{label}' failed during execution: {e}")
        traceback.print_exc()
        raise RuntimeError(f"ADO WIQL failed: {e}")
    if resp.status_code != 200:
        print(f"[ADO][TICKETS][ERROR] Query '{label}' returned {resp.status_code}: {resp.text[:300]}")
        raise RuntimeError(f"ADO WIQL error: {resp.text}")
    items = resp.json().get("workItems", [])
    ids = [int(it.get("id")) for it in items if it.get("id")]
    print(f"[ADO][TICKETS] Query '{label}' returned {len(ids)} work items")
    return ids


def _ado_fetch_work_items_by_ids(ids: List[int]) -> List[dict]:
    if not ids:
        return []

    results: List[dict] = []
    org_base = _ado_project_base(None)
    for start in range(0, len(ids), 200):
        batch_ids = ids[start:start + 200]
        det_url = (
            f"{org_base}/_apis/wit/workitems?ids={','.join(str(item_id) for item_id in batch_ids)}"
            "&$expand=all&api-version=7.1"
        )
        det = requests.get(det_url, headers=_ado_headers(), timeout=60)
        if det.status_code != 200:
            print(f"[ADO][TICKETS][ERROR] Work item detail fetch returned {det.status_code}: {det.text[:300]}")
            raise RuntimeError(f"ADO workitems details error: {det.text}")
        results.extend(det.json().get("value", []))
    return results


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


def _normalize_ado_resource_url(resource_url: str, project: Optional[str] = None) -> str:
    raw_url = str(resource_url or "").strip()
    if not raw_url:
        return ""
    if raw_url.startswith("data:"):
        return raw_url
    if raw_url.startswith("//"):
        return "https:" + raw_url
    if raw_url.startswith("http://") or raw_url.startswith("https://"):
        return raw_url
    if raw_url.startswith("/_apis/") or raw_url.startswith("/_attachments/"):
        return f"{_ado_project_base(project)}{raw_url}"
    if raw_url.startswith("_apis/") or raw_url.startswith("_attachments/"):
        return f"{_ado_project_base(project)}/{raw_url}"
    if raw_url.startswith("/"):
        return f"{_ado_project_base(project)}{raw_url}"
    return raw_url


def _ado_guess_filename(resource_url: str, fallback_name: str = "attachment") -> str:
    try:
        parsed = urlsplit(resource_url)
        query = dict(parse_qsl(parsed.query, keep_blank_values=True))
        for key in ("fileName", "filename", "name"):
            value = (query.get(key) or "").strip()
            if value:
                return unquote(value)
        tail = pathlib.Path(unquote(parsed.path)).name
        if tail:
            return tail
    except Exception:
        pass
    return fallback_name


def _ado_with_download_flag(resource_url: str) -> str:
    parsed = urlsplit(resource_url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    if "download" not in query:
        query["download"] = "true"
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urlencode(query), parsed.fragment))


def _download_ado_binary_resource(
    resource_url: str,
    project: Optional[str] = None,
    file_name: Optional[str] = None,
) -> Optional[dict]:
    normalized_url = _normalize_ado_resource_url(resource_url, project=project)
    if not normalized_url:
        return None

    if normalized_url.startswith("data:"):
        normalized_b64, payload_mime = _normalize_image_base64_payload(normalized_url)
        if not normalized_b64:
            return None
        try:
            decoded_bytes = base64.b64decode(normalized_b64)
        except Exception:
            return None
        resolved_name = file_name or "embedded-image"
        return {
            "file_name": resolved_name,
            "content_type": payload_mime or mimetypes.guess_type(resolved_name)[0] or "application/octet-stream",
            "data": decoded_bytes,
            "url": normalized_url,
        }

    urls_to_try = [normalized_url]
    download_url = _ado_with_download_flag(normalized_url)
    if download_url != normalized_url:
        urls_to_try.append(download_url)

    last_error: Optional[str] = None
    while urls_to_try:
        candidate_url = urls_to_try.pop(0)
        try:
            response = requests.get(candidate_url, headers=_ado_headers(), timeout=120, allow_redirects=True)
        except Exception as exc:
            last_error = str(exc)
            continue

        if response.status_code != 200:
            last_error = f"{response.status_code} {response.text[:200]}"
            continue

        content_type = (response.headers.get("content-type") or "").split(";")[0].strip().lower()
        if content_type == "application/json":
            try:
                payload = response.json()
            except Exception:
                payload = {}
            follow_url = str(payload.get("downloadUrl") or payload.get("url") or "").strip()
            if follow_url and follow_url not in urls_to_try:
                urls_to_try.append(follow_url)
                continue

        resolved_name = file_name or _ado_guess_filename(response.url or candidate_url)
        return {
            "file_name": resolved_name,
            "content_type": content_type or mimetypes.guess_type(resolved_name)[0] or "application/octet-stream",
            "data": response.content,
            "url": response.url or candidate_url,
        }

    print(f"[ADO][TICKET][WARN] Failed to download Azure DevOps resource '{normalized_url}': {last_error}")
    return None


def _describe_ticket_image_reference(image_ref: str, source_label: str, project: Optional[str] = None) -> str:
    normalized_ref = _normalize_ado_resource_url(image_ref, project=project)
    if not normalized_ref:
        return f"[Image Content from {source_label}]\n[Image source was empty]"

    downloaded = _download_ado_binary_resource(normalized_ref, project=project, file_name=source_label)
    if downloaded:
        resolved_name = downloaded.get("file_name") or source_label
        content_type = str(downloaded.get("content_type") or "")
        if content_type.startswith("image/") or resolved_name.split(".")[-1].lower() in POPULAR_IMAGE_EXTS:
            file_b64 = base64.b64encode(downloaded["data"]).decode("utf-8")
            return _process_image_file(
                resolved_name,
                file_b64,
                content_type,
                describe_func=_describe_image_via_vision,
            )

    try:
        description = _describe_image_via_vision(normalized_ref)
    except Exception as exc:
        description = f"[Image analysis failed: {exc}]"
    return f"[Image Content from {source_label}]\n{description}"


def _render_ado_html_with_inline_images(html: str, section_label: str, project: Optional[str] = None) -> str:
    raw_html = str(html or "")
    if not raw_html.strip():
        return ""

    parts: List[str] = []
    cursor = 0
    image_index = 0
    for match in re.finditer(r'<img[^>]+src=["\']?([^"\'>\s]+)["\']?[^>]*>', raw_html, flags=re.IGNORECASE):
        text_segment = _strip_html(raw_html[cursor:match.start()]).strip()
        if text_segment:
            parts.append(text_segment)

        image_index += 1
        parts.append(
            _describe_ticket_image_reference(
                match.group(1),
                source_label=f"{section_label} image {image_index}",
                project=project,
            )
        )
        cursor = match.end()

    tail_text = _strip_html(raw_html[cursor:]).strip()
    if tail_text:
        parts.append(tail_text)

    if not parts:
        return _strip_html(raw_html).strip()
    return "\n\n".join(part for part in parts if part)


def _build_ticket_attachment_context(
    work_item_id: int,
    attachments: List[dict],
    project: Optional[str] = None,
) -> str:
    if not attachments:
        return ""

    ordered_attachments = sorted(
        attachments,
        key=lambda item: (item.get("createdDate") or "", item.get("name") or ""),
    )
    blocks: List[str] = []
    total = len(ordered_attachments)

    for index, attachment in enumerate(ordered_attachments, start=1):
        attachment_name = str(attachment.get("name") or f"attachment-{index}")
        print(f"[ADO][TICKET] Downloading attachment {index}/{total} for work item {work_item_id}: {attachment_name}")
        downloaded = _download_ado_binary_resource(
            str(attachment.get("url") or ""),
            project=project,
            file_name=attachment_name,
        )

        header_lines = [f"Attachment {index}: {attachment_name}"]
        created_date = str(attachment.get("createdDate") or "").strip()
        comment = str(attachment.get("comment") or "").strip()
        if created_date:
            header_lines.append(f"Added: {created_date}")
        if comment:
            header_lines.append(f"Note: {comment}")

        if not downloaded:
            header_lines.append("[Unable to download attachment content from Azure DevOps]")
            blocks.append("\n".join(header_lines))
            continue

        upload_payload = {
            "name": str(downloaded.get("file_name") or attachment_name),
            "type": str(downloaded.get("content_type") or "application/octet-stream"),
            "data": base64.b64encode(downloaded["data"]).decode("utf-8"),
        }
        extracted_text = process_uploaded_file(
            upload_payload,
            describe_image_func=_describe_image_via_vision,
        ).strip()
        if extracted_text:
            header_lines.append(extracted_text)
        else:
            header_lines.append("[Attachment was downloaded but produced no extractable content]")
        blocks.append("\n".join(header_lines))

    return "\n\n---\n\n".join(blocks)


def _describe_image_via_vision(image_url: str) -> str:
    """
    Use OpenAI vision (gpt-4o) to describe an image in detail.
    Returns a comprehensive text description focusing on technical content, UI, data, and context.
    Supports both HTTP(S) URLs and data URIs (base64 encoded images).
    """
    try:
        # Accept both URLs and data URIs
        if not (image_url.startswith("http://") or image_url.startswith("https://") or image_url.startswith("data:image/")):
            print(f"[VISION][WARN] Invalid image URL format: {image_url[:60]}...")
            return f"[Local image: {image_url}]"
        
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
        body = {
            "model": OPENAI_VISION_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "You are a detailed technical image analyzer. Provide a comprehensive description of this image. Include:\n"
                                "1. What type of document/UI/diagram is this (screenshot, chart, diagram, form, etc.)\n"
                                "2. Main content and purpose\n"
                                "3. Any visible text, labels, headers, field names, buttons, or menu items\n"
                                "4. Technical details: configuration settings, error messages, status indicators\n"
                                "5. Any tables, data, metrics, or numerical values shown\n"
                                "6. UI elements: panels, sections, checkboxes, dropdowns, input fields\n"
                                "7. Anything that would help someone understand what's happening in this image.\n\n"
                                "Be thorough and specific. Do not refuse to analyze. Focus on technical relevance."
                            ),
                        },
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                }
            ],
            "max_tokens": 1000,
        }
        resp = requests.post(f"{OPENAI_URL}/chat/completions", json=body, headers=headers, timeout=60)
        if resp.status_code == 200:
            data = resp.json()
            description = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            print(f"[VISION] Detailed image analysis ({len(description)} chars) for {image_url[:60]}...")
            return description
        else:
            print(f"[VISION][WARN] Vision call failed for {image_url}: {resp.status_code} {resp.text[:200]}")
            return f"[Image analysis unavailable]"
    except Exception as e:
        print(f"[VISION][WARN] Failed to describe image {image_url[:60]}...: {e}")
        return f"[Image analysis unavailable]"


def _extract_structured_text_from_image(
    image_ref: str,
    source_label: str = "image",
    cancel_check=None,
) -> str:
    """
    Extract OCR-style text from an image using gpt-4o vision and preserve table content as markdown.
    Uses best OpenAI vision model for superior accuracy.
    """
    if not OPENAI_API_KEY:
        return ""

    if cancel_check and cancel_check():
        print(f"[VISION] Skipping OCR extraction for {source_label}: canceled")
        return ""

    try:
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
        body = {
            "model": OPENAI_VISION_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "You are an advanced OCR and visual content extractor. Extract all useful information from this image comprehensively. "
                                "Follow this exact output structure:\n"
                                "[IMAGE_SUMMARY]\n"
                                "2-4 detailed sentences describing what this screenshot/image shows, its purpose, and context.\n\n"
                                "[VISIBLE_TEXT]\n"
                                "Extract ALL readable text: labels, values, menu names, buttons, error text, headings, configuration keys, field names, etc. "
                                "Preserve the exact text and format. Use one item per line. If none, write: <none>.\n\n"
                                "[TABLES]\n"
                                "If a table/grid/matrix exists, output it in markdown format preserving all row/column values and structure exactly. If none, write: <none>.\n\n"
                                "[DATA_VALUES]\n"
                                "Extract any numbers, metrics, timestamps, thresholds, or measurable data shown. Include context (e.g., 'CPU: 85%').\n\n"
                                "[UI_ELEMENTS]\n"
                                "List all important UI components: buttons, panels, tabs, sections, checkboxes, dropdowns, input fields, dialogs, and their states.\n\n"
                                "[TECHNICAL_SIGNALS]\n"
                                "Identify technical details: screen/page type, selected items, active filters, visible warnings, error codes, status indicators, configuration mode.\n\n"
                                "Rules: Extract everything visible. Do not refuse. Do not invent unseen details. Mark unclear or illegible content as [unclear]. "
                                "This is for technical documentation and troubleshooting support."
                            ),
                        },
                        {"type": "image_url", "image_url": {"url": image_ref}},
                    ],
                }
            ],
            "max_tokens": min(VISION_MAX_TOKENS, 2500),
            "temperature": 0,
        }
        for attempt in range(VISION_RETRY_COUNT + 1):
            if cancel_check and cancel_check():
                print(f"[VISION] Stopping OCR extraction for {source_label}: canceled")
                return ""
            try:
                resp = requests.post(
                    f"{OPENAI_URL}/chat/completions",
                    json=body,
                    headers=headers,
                    timeout=VISION_TIMEOUT_SECONDS,
                )
            except requests.exceptions.ReadTimeout as e:
                if attempt >= VISION_RETRY_COUNT:
                    print(f"[VISION][WARN] OCR extraction timeout for {source_label} after retries: {e}")
                    return ""
                wait_sec = (attempt + 1) * 2
                print(f"[VISION][WARN] OCR timeout for {source_label}, retry {attempt + 1}/{VISION_RETRY_COUNT} in {wait_sec}s")
                time.sleep(wait_sec)
                continue
            except Exception as e:
                print(f"[VISION][WARN] OCR extraction error for {source_label}: {e}")
                return ""

            if resp.status_code != 200:
                print(f"[VISION][WARN] OCR extraction failed for {source_label}: {resp.status_code} {resp.text[:200]}")
                return ""

            data = resp.json()
            text = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            if text:
                print(f"[VISION] OCR extraction success for {source_label} using {OPENAI_VISION_MODEL}, len={len(text)}")
            return text
        return ""
    except Exception as e:
        print(f"[VISION][WARN] OCR extraction error for {source_label}: {e}")
        return ""


def _normalize_image_base64_payload(payload: str) -> Tuple[Optional[str], Optional[str]]:
    """Return (normalized_b64, mime_type_if_present) from either raw base64 or data URI."""
    raw = (payload or "").strip()
    if not raw:
        return None, None

    mime_type = None
    if raw.startswith("data:") and "," in raw:
        header, raw = raw.split(",", 1)
        match = re.match(r"^data:([^;]+);base64$", header, re.IGNORECASE)
        if match:
            mime_type = (match.group(1) or "").lower()

    # Remove whitespace/newlines and normalize padding.
    raw = re.sub(r"\s+", "", raw)
    if not raw:
        return None, mime_type
    padding = len(raw) % 4
    if padding:
        raw += "=" * (4 - padding)

    return raw, mime_type


def _is_low_signal_image_context(text: str) -> bool:
    candidate = (text or "").strip().lower()
    if not candidate:
        return True

    low_signal_markers = [
        "unable to extract text",
        "cannot extract text",
        "can't extract text",
        "no readable text",
        "image analysis unavailable",
        "i cannot",
        "i can't",
        "<none>",
    ]
    if any(marker in candidate for marker in low_signal_markers):
        return True

    # Very short outputs are typically not enough for troubleshooting context.
    return len(candidate) < 80


def _normalize_table_rows(rows: List[List[Any]]) -> List[List[str]]:
    normalized: List[List[str]] = []
    for row in rows:
        row_values: List[str] = []
        for cell in (row or []):
            cell_text = "" if cell is None else str(cell)
            cell_text = " ".join(cell_text.replace("\r", " ").split())
            cell_text = cell_text.replace("|", "\\|")
            row_values.append(cell_text)
        normalized.append(row_values)
    return normalized


def _format_table_rows_as_markdown(rows: List[List[Any]]) -> str:
    if not rows:
        return ""

    normalized = _normalize_table_rows(rows)

    if not normalized:
        return ""

    width = max(len(r) for r in normalized)
    if width == 0:
        return ""

    padded = [r + [""] * (width - len(r)) for r in normalized]
    header = padded[0]
    separator = ["---"] * width

    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(separator) + " |",
    ]

    for row in padded[1:]:
        lines.append("| " + " | ".join(row) + " |")

    return "\n".join(lines)


def _format_table_rows_as_blocks(rows: List[List[Any]], page_number: int, table_number: int) -> List[str]:
    normalized = _normalize_table_rows(rows)
    if len(normalized) <= 1:
        return []

    width = max(len(r) for r in normalized)
    if width == 0:
        return []

    padded = [r + [""] * (width - len(r)) for r in normalized]
    header = padded[0]
    row_blocks: List[str] = []

    for row_idx, row_values in enumerate(padded[1:], start=1):
        row_dict = {}
        for col_idx, cell_val in enumerate(row_values, start=1):
            key = header[col_idx - 1].strip() or f"col_{col_idx}"
            row_dict[key] = cell_val

        row_payload = {
            "page": page_number,
            "table": table_number,
            "row": row_idx,
            "cells": row_values,
            "by_header": row_dict,
        }
        row_blocks.append(
            f"{TABLE_ROW_START_TAG} page={page_number} table={table_number} row={row_idx}\n"
            + json.dumps(row_payload, ensure_ascii=False)
            + f"\n{TABLE_ROW_END_TAG}"
        )

    return row_blocks


def _extract_text_from_pypdf2_page(page: Any) -> str:
    try:
        text = page.extract_text(extraction_mode="layout")
        if text:
            return text
    except TypeError:
        pass
    except Exception:
        pass

    try:
        return page.extract_text() or ""
    except Exception:
        return ""


def _looks_like_command_or_code_line(line: str) -> bool:
    candidate = str(line or "").strip()
    if not candidate:
        return False

    upper_candidate = candidate.upper()
    if upper_candidate in {"SQL", "BASH", "SHELL", "CMD", "POWERSHELL", "PYTHON"}:
        return True

    sql_markers = (
        "CREATE TABLE", "ALTER TABLE", "DROP TABLE", "INSERT INTO", "UPDATE ", "DELETE FROM",
        "SELECT ", "FROM ", "WHERE ", "LEFT JOIN", "RIGHT JOIN", "INNER JOIN", "PRIMARY KEY",
        "FOREIGN KEY", "UNIQUE KEY", "ENGINE=", "COLLATE=", "DEFAULT CHARSET=", "NOT NULL",
    )
    if any(marker in upper_candidate for marker in sql_markers):
        return True

    shell_markers = ("sudo ", "docker ", "kubectl ", "python ", "pip ", "npm ", "yarn ", "git ", "curl ", "wget ")
    if any(candidate.startswith(marker) for marker in shell_markers):
        return True

    if re.search(r'[`{}();=<>"]', candidate):
        return True
    # Lines starting with # that contain UI/navigation language are NOT code
    if re.match(r"^\s*#", candidate):
        _comment_body = re.sub(r"^\s*#\s*", "", candidate)
        if re.search(
            r"\b(click|select|open|navigate|button|tab|screen|ui|portainer|admin studio|"
            r"field|dropdown|checkbox|page|section|restart|restarting|service|clearing|"
            r"browser|cache|setting|menu|dialog|typically|usually|involves|done through|via)"
            r"\b", _comment_body, re.IGNORECASE
        ):
            return False
        return True
    if re.match(r"^\s*(--|/\*|\*)", candidate):
        return True
    if re.match(r"^[A-Za-z0-9_.-]+\s*=\s*.+$", candidate):
        return True
    return False


def _normalize_pdf_extracted_text(text: str) -> str:
    raw_lines = [line.rstrip() for line in str(text or "").replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    normalized_lines: List[str] = []
    paragraph_parts: List[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph_parts
        if paragraph_parts:
            paragraph = " ".join(part for part in paragraph_parts if part).strip()
            if paragraph:
                normalized_lines.append(paragraph)
            paragraph_parts = []

    for raw_line in raw_lines:
        line = raw_line.strip()
        if not line:
            flush_paragraph()
            if normalized_lines and normalized_lines[-1] != "":
                normalized_lines.append("")
            continue

        heading_like = bool(re.match(r"^(?:---\s*Page\s+\d+\s*---|\[Table\s+\d+\]|Table:\s|\d+\.\s+|#+\s+)", line))
        code_like = _looks_like_command_or_code_line(line)

        if heading_like or code_like:
            flush_paragraph()
            normalized_lines.append(line)
            continue

        if paragraph_parts and paragraph_parts[-1].endswith("-"):
            paragraph_parts[-1] = paragraph_parts[-1][:-1] + line
        else:
            paragraph_parts.append(line)

    flush_paragraph()

    collapsed: List[str] = []
    previous_blank = False
    for line in normalized_lines:
        if line == "":
            if not previous_blank:
                collapsed.append(line)
            previous_blank = True
        else:
            collapsed.append(line)
            previous_blank = False

    return "\n".join(collapsed).strip()


def _extract_text_from_pymupdf_page(page: Any) -> str:
    try:
        blocks = page.get_text("blocks", sort=True) or []
    except Exception:
        try:
            return _normalize_pdf_extracted_text(page.get_text("text", sort=True) or "")
        except Exception:
            return ""

    block_texts: List[str] = []
    for block in blocks:
        text = str(block[4] or "").strip() if len(block) > 4 else ""
        if not text:
            continue
        normalized = _normalize_pdf_extracted_text(text)
        if normalized:
            block_texts.append(normalized)

    return "\n\n".join(block_texts).strip()


def _extract_layout_ordered_segments_from_pymupdf_page(
    page: Any,
    file_name: str,
    page_number: int,
    allow_image_analysis: bool,
    cancel_check=None,
    request_id: Optional[str] = None,
) -> List[str]:
    """Extract page content in visual reading order (text and images interleaved)."""
    try:
        data = page.get_text("dict", sort=True) or {}
        blocks = data.get("blocks", []) or []
    except Exception as e:
        print(f"[FILE][PDF][WARN] Layout extraction failed page={page_number}: {e}")
        return []

    segments: List[str] = []
    image_count = 0
    page_rect = getattr(page, "rect", None)
    page_area = 0.0
    if page_rect is not None:
        page_area = max(1.0, float(page_rect.width) * float(page_rect.height))

    for block_idx, block in enumerate(blocks):
        if cancel_check and cancel_check():
            _ingest_log(f"pdf page={page_number}: layout extraction canceled", request_id, force=True)
            break
        block_type = int(block.get("type", 0))
        bbox = block.get("bbox") or []
        if DETAILED_INGEST_LOGS:
            kind = "text" if block_type == 0 else ("image" if block_type == 1 else f"type-{block_type}")
            _ingest_log(
                f"pdf page={page_number}: scanning block={block_idx + 1}/{len(blocks)} kind={kind} bbox={bbox if len(bbox) == 4 else 'n/a'}",
                request_id,
            )

        if block_type == 0:
            text_parts: List[str] = []
            for line in block.get("lines", []) or []:
                spans = line.get("spans", []) or []
                line_text = "".join(str(span.get("text", "")) for span in spans).strip()
                if line_text:
                    text_parts.append(line_text)
            text = "\n".join(text_parts).strip()
            if text:
                normalized = _normalize_pdf_extracted_text(text)
                if normalized:
                    segments.append(normalized)
                    _ingest_log(
                        f"pdf page={page_number}: text block accepted len={len(normalized)} -> queued for embedding",
                        request_id,
                    )
            continue

        if block_type != 1 or not allow_image_analysis:
            continue

        if PDF_MAX_IMAGES_PER_PAGE > 0 and image_count >= PDF_MAX_IMAGES_PER_PAGE:
            continue

        bbox = block.get("bbox") or []
        if len(bbox) != 4:
            continue

        x0, y0, x1, y1 = [float(v) for v in bbox]
        width = max(0.0, x1 - x0)
        height = max(0.0, y1 - y0)
        block_area = width * height
        area_ratio = block_area / page_area if page_area else 0.0

        if area_ratio < PDF_MIN_IMAGE_AREA_RATIO:
            _ingest_log(
                f"pdf page={page_number}: image block skipped ratio={area_ratio:.4f} (< {PDF_MIN_IMAGE_AREA_RATIO:.4f})",
                request_id,
            )
            continue

        try:
            clip = fitz.Rect(x0, y0, x1, y1)
            pix = page.get_pixmap(clip=clip, dpi=200, alpha=False)
            image_b64 = base64.b64encode(pix.tobytes("png")).decode("utf-8")
            data_uri = f"data:image/png;base64,{image_b64}"
            image_text = _extract_structured_text_from_image(
                data_uri,
                source_label=f"{file_name}:page-{page_number}:image-{block_idx + 1}",
                cancel_check=cancel_check,
            )
            if image_text:
                image_count += 1
                segments.append("[IMAGE_BLOCK_ANALYSIS]\n" + image_text)
                _ingest_log(
                    f"pdf page={page_number}: image block analyzed with vision block={block_idx + 1} ratio={area_ratio:.3f} desc_len={len(image_text)} -> queued for embedding",
                    request_id,
                )
        except Exception as e:
            print(
                f"[FILE][PDF][WARN] Inline image block extraction failed page={page_number} block={block_idx + 1}: {e}"
            )

    return segments


def _strip_html(text: str) -> str:
    try:
        txt = re.sub(r"<[^>]+>", " ", text or "")
        txt = unescape(txt)
        return " ".join(txt.split())
    except Exception:
        return text or ""


# ---------------------------------------------------------------------
# File Processing Functions (for uploaded files in chat)
# ---------------------------------------------------------------------

POPULAR_IMAGE_EXTS = {
    "png", "jpg", "jpeg", "gif", "webp", "bmp", "tif", "tiff", "svg", "ico", "heic", "heif", "avif", "jfif"
}
POPULAR_EXCEL_EXTS = {"xlsx", "xls", "xlsm", "xltx", "xltm", "xlsb", "ods"}
POPULAR_TEXT_EXTS = {
    "txt", "md", "markdown", "rst", "csv", "tsv", "log", "ini", "cfg", "conf", "properties", "env",
    "json", "jsonl", "xml", "yaml", "yml", "toml", "sql",
    "sh", "bash", "zsh", "ps1", "bat", "cmd",
    "py", "js", "ts", "jsx", "tsx", "java", "cs", "go", "rb", "php", "c", "cpp", "h", "hpp",
    "html", "htm", "css", "scss", "less",
}
POPULAR_OTHER_EXTS = {
    "ppt", "pptx", "odp", "odt", "rtf", "eml", "msg",
    "zip", "rar", "7z", "tar", "gz",
    "mp3", "wav", "m4a", "aac", "ogg", "flac",
    "mp4", "mkv", "mov", "avi", "wmv", "webm",
}


def _process_unstructured_popular_file(file_name: str, file_ext: str) -> str:
    """Graceful fallback for popular file types that are uploadable but not text-extractable yet."""
    return (
        f"**File: {file_name}**\n\n"
        f"[NOTICE] .{file_ext} is accepted for upload, but automatic text extraction is not available yet for this type."
    )

def process_uploaded_file(
    file_data: Dict[str, str],
    describe_image_func=None,
    cancel_check=None,
    request_id: Optional[str] = None,
) -> str:
    """
    Process an uploaded file (base64 encoded) and extract its content.
    Supports: images (via OCR/vision), Excel, CSV, PDF, text, Word docs.
    
    Args:
        file_data: Dict with keys 'name', 'type', 'data' (base64 encoded)
        describe_image_func: Optional function to describe images via Vision API
    
    Returns:
        Extracted text content
    """
    try:
        if cancel_check and cancel_check():
            _ingest_log("file processing skipped due to cancel before start", request_id, force=True)
            return "[CANCELED] Upload processing stopped by user."

        file_name = file_data.get("name", "unknown")
        file_type = file_data.get("type", "")
        file_b64 = file_data.get("data", "")
        
        if not file_b64:
            return f"[ERROR] Empty file: {file_name}"
        
        file_ext = file_name.split(".")[-1].lower()
        
        # Decode base64
        try:
            file_bytes = base64.b64decode(file_b64)
        except Exception as e:
            print(f"[FILE] Failed to decode base64 for {file_name}: {e}")
            return f"[ERROR] Failed to decode file: {file_name}"
        
        print(f"[FILE] Processing {file_name} (ext={file_ext}, size={len(file_bytes)} bytes)")
        _ingest_log(f"file begin name='{file_name}' ext={file_ext} size_bytes={len(file_bytes)}", request_id, force=True)
        
        # Route to appropriate handler
        if file_ext in POPULAR_IMAGE_EXTS or (file_type and file_type.startswith("image/")):
            return _process_image_file(file_name, file_b64, file_type, describe_image_func)
        elif file_ext in POPULAR_EXCEL_EXTS:
            return _process_excel_file(file_name, file_bytes)
        elif file_ext == "csv":
            return _process_csv_file(file_name, file_bytes)
        elif file_ext == "pdf":
            return _process_pdf_file(file_name, file_bytes, cancel_check=cancel_check, request_id=request_id)
        elif file_ext in POPULAR_TEXT_EXTS:
            return _process_text_file(file_name, file_bytes)
        elif file_ext in ["doc", "docx"]:
            return _process_word_file(file_name, file_bytes)
        elif file_ext in POPULAR_OTHER_EXTS:
            return _process_unstructured_popular_file(file_name, file_ext)
        else:
            return f"[WARNING] Unsupported file type: {file_name} (.{file_ext})"
    
    except Exception as e:
        print(f"[FILE] Error processing file: {e}")
        return f"[ERROR] Failed to process file: {str(e)}"


def _process_image_file(file_name: str, file_b64: str, file_type: Optional[str] = None, describe_func=None) -> str:
    """Process image file using OpenAI Vision API or fallback."""
    try:
        if not OPENAI_API_KEY:
            return f"[Image file {file_name} - OPENAI_API_KEY is not configured]"

        normalized_b64, payload_mime = _normalize_image_base64_payload(file_b64)
        if not normalized_b64:
            return f"[Image file {file_name} - invalid base64 data]"

        # Decode base64 to bytes for potential conversion
        try:
            file_bytes = base64.b64decode(normalized_b64)
        except Exception as e:
            print(f"[FILE] Failed to decode base64 for image {file_name}: {e}")
            return f"[Image file {file_name} - invalid base64 data]"

        # Determine mime type
        mime_type = None
        if file_type and file_type.startswith("image/"):
            mime_type = file_type
        if not mime_type and payload_mime and payload_mime.startswith("image/"):
            mime_type = payload_mime
        if not mime_type:
            mime_type = mimetypes.guess_type(file_name)[0]
        if not mime_type:
            mime_type = "image/jpeg"

        # If unsupported by vision, try convert to JPEG via PIL
        vision_supported = {"image/jpeg", "image/png", "image/gif", "image/webp"}
        if mime_type not in vision_supported:
            if HAS_PIL:
                try:
                    img = Image.open(BytesIO(file_bytes))
                    if img.mode not in ("RGB", "L"):
                        img = img.convert("RGB")
                    buf = BytesIO()
                    img.save(buf, format="JPEG")
                    jpeg_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
                    data_uri = f"data:image/jpeg;base64,{jpeg_b64}"
                except Exception as e:
                    print(f"[FILE] Failed to convert image {file_name} to JPEG: {e}")
                    return f"[Image file {file_name} - unsupported format for analysis]"
            else:
                return f"[Image file {file_name} - unsupported format for analysis]"
        else:
            data_uri = f"data:{mime_type};base64,{normalized_b64}"

        extracted = _extract_structured_text_from_image(data_uri, source_label=file_name)
        fallback_desc = ""
        if describe_func and _is_low_signal_image_context(extracted):
            fallback_desc = (describe_func(data_uri) or "").strip()

        merged_parts: List[str] = []
        if extracted:
            merged_parts.append(extracted.strip())
        if fallback_desc:
            extracted_lc = (extracted or "").strip().lower()
            fallback_lc = fallback_desc.lower()
            if fallback_lc and fallback_lc not in extracted_lc:
                merged_parts.append("[VISUAL_FALLBACK]\n" + fallback_desc)

        image_context = "\n\n".join(part for part in merged_parts if part).strip()
        if not image_context:
            image_context = "[Image analysis unavailable]"

        return f"[Image Content from {file_name}]\n{image_context}"
    except Exception as e:
        print(f"[FILE] Vision API failed for {file_name}: {e}")
        return f"[Image file {file_name} - analysis failed: {e}]"


def _process_text_file(file_name: str, file_bytes: bytes) -> str:
    """Extract text from text file."""
    try:
        content = file_bytes.decode("utf-8", errors="ignore")
        return f"**File: {file_name}**\n\n{content}"
    except Exception as e:
        print(f"[FILE] Failed to read text file {file_name}: {e}")
        return f"[ERROR] Failed to read text file: {file_name}"


def _process_excel_file(file_name: str, file_bytes: bytes) -> str:
    """Extract text from Excel file."""
    try:
        if not HAS_OPENPYXL:
            return f"**File: {file_name}** [Excel support not installed - openpyxl required]"
        
        excel_file = BytesIO(file_bytes)
        wb = openpyxl.load_workbook(excel_file)
        
        content_lines = [f"**File: {file_name}**\n"]
        
        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            content_lines.append(f"\n**Sheet: {sheet_name}**\n")
            
            row_count = 0
            for row in ws.iter_rows(max_row=1000):
                row_data = []
                for cell in row:
                    val = cell.value
                    row_data.append(str(val) if val is not None else "")
                
                if any(row_data):
                    content_lines.append(" | ".join(row_data))
                    row_count += 1
            
            if row_count == 1000:
                content_lines.append("\n... (file too large, showing first 1000 rows)")
        
        return "\n".join(content_lines)
    
    except Exception as e:
        print(f"[FILE] Failed to process Excel file {file_name}: {e}")
        return f"**File: {file_name}** [Error reading Excel: {str(e)}]"


def _process_csv_file(file_name: str, file_bytes: bytes) -> str:
    """Extract text from CSV file."""
    try:
        csv_text = file_bytes.decode("utf-8", errors="ignore")
        reader = csv.reader(csv_text.splitlines())
        
        content_lines = [f"**File: {file_name}**\n"]
        
        row_count = 0
        for row in reader:
            if row_count >= 500:
                content_lines.append("\n... (file too large, showing first 500 rows)")
                break
            
            if any(row):
                content_lines.append(" | ".join(row))
                row_count += 1
        
        return "\n".join(content_lines)
    
    except Exception as e:
        print(f"[FILE] Failed to process CSV file {file_name}: {e}")
        return f"**File: {file_name}** [Error reading CSV: {str(e)}]"


def _process_pdf_file(file_name: str, file_bytes: bytes, cancel_check=None, request_id: Optional[str] = None) -> str:
    """Extract text from PDF file."""
    try:
        import PyPDF2
        pdf_file = BytesIO(file_bytes)
        reader = PyPDF2.PdfReader(pdf_file)

        total_pages = len(reader.pages)
        pages_to_process = total_pages
        if PDF_MAX_PAGES > 0:
            pages_to_process = min(total_pages, PDF_MAX_PAGES)

        _ingest_log(
            f"pdf begin file='{file_name}' pages_total={total_pages} pages_to_process={pages_to_process}",
            request_id,
            force=True,
        )

        content_lines = [f"**File: {file_name}** ({total_pages} pages)\n"]

        plumber_doc = None
        if HAS_PDFPLUMBER and PDF_TABLE_EXTRACTION_ENABLED:
            try:
                plumber_doc = pdfplumber.open(BytesIO(file_bytes))
            except Exception as e:
                print(f"[FILE][PDF][WARN] pdfplumber open failed for {file_name}: {e}")

        pymupdf_doc = None
        if HAS_PYMUPDF:
            try:
                pymupdf_doc = fitz.open(stream=file_bytes, filetype="pdf")
            except Exception as e:
                print(f"[FILE][PDF][WARN] PyMuPDF open failed for {file_name}: {e}")

        for page_idx in range(pages_to_process):
            if cancel_check and cancel_check():
                _ingest_log(
                    f"cancel acknowledged during PDF parse at page={page_idx + 1}; stopping parse",
                    request_id,
                    force=True,
                )
                content_lines.append("\n[CANCELED] PDF processing stopped by user.")
                break
            page = reader.pages[page_idx]
            page_lines: List[str] = [f"\n--- Page {page_idx + 1} ---"]
            _ingest_log(f"pdf page={page_idx + 1}: start top-to-bottom scan", request_id)
            allow_image_analysis = (
                PDF_IMAGE_EXTRACTION_ENABLED
                and PDF_OCR_ENABLED
                and OPENAI_API_KEY
                and (PDF_OCR_MAX_PAGES == 0 or page_idx < PDF_OCR_MAX_PAGES)
            )

            text = ""
            used_layout_segments = False
            if pymupdf_doc and page_idx < len(pymupdf_doc):
                try:
                    pymupdf_page = pymupdf_doc.load_page(page_idx)
                    ordered_segments = _extract_layout_ordered_segments_from_pymupdf_page(
                        pymupdf_page,
                        file_name=file_name,
                        page_number=page_idx + 1,
                        allow_image_analysis=allow_image_analysis,
                        cancel_check=cancel_check,
                        request_id=request_id,
                    )
                    if ordered_segments:
                        used_layout_segments = True
                        page_lines.append("\n\n".join(ordered_segments))
                        _ingest_log(
                            f"pdf page={page_idx + 1}: ordered segments ready count={len(ordered_segments)}",
                            request_id,
                        )
                    else:
                        text = _extract_text_from_pymupdf_page(pymupdf_page)
                except Exception as e:
                    print(f"[FILE][PDF][WARN] PyMuPDF text extraction failed page={page_idx + 1}: {e}")

            if not used_layout_segments and not text.strip():
                text = _normalize_pdf_extracted_text(_extract_text_from_pypdf2_page(page))

            if text and text.strip():
                page_lines.append(text)
                _ingest_log(
                    f"pdf page={page_idx + 1}: fallback text extracted len={len(text)} -> queued for embedding",
                    request_id,
                )

            table_count = 0
            if plumber_doc and page_idx < len(plumber_doc.pages):
                try:
                    tables = plumber_doc.pages[page_idx].extract_tables() or []
                    for table_idx, table_rows in enumerate(tables, start=1):
                        table_md = _format_table_rows_as_markdown(table_rows)
                        if table_md:
                            table_count += 1
                            page_lines.append(f"\n[Table {table_idx}]\n{table_md}")
                            _ingest_log(
                                f"pdf page={page_idx + 1}: table extracted idx={table_idx} len={len(table_md)} -> queued for embedding",
                                request_id,
                            )
                            row_blocks = _format_table_rows_as_blocks(
                                table_rows,
                                page_number=page_idx + 1,
                                table_number=table_idx,
                            )
                            if row_blocks:
                                page_lines.append("\n" + "\n".join(row_blocks))
                except Exception as e:
                    print(f"[FILE][PDF][WARN] Table extraction failed page={page_idx + 1}: {e}")

            should_try_ocr = (
                pymupdf_doc is not None
                and allow_image_analysis
                and len(page_lines) == 1
            )

            if should_try_ocr:
                try:
                    p = pymupdf_doc.load_page(page_idx)
                    pix = p.get_pixmap(dpi=200, alpha=False)
                    image_bytes = pix.tobytes("png")
                    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
                    data_uri = f"data:image/png;base64,{image_b64}"
                    ocr_text = _extract_structured_text_from_image(
                        data_uri,
                        source_label=f"{file_name}:page-{page_idx + 1}",
                        cancel_check=cancel_check,
                    )
                    if ocr_text:
                        page_lines.append("\n[PAGE_IMAGE_ANALYSIS_FALLBACK]\n" + ocr_text)
                        print(f"[FILE][PDF] Fallback page image analysis extracted from page {page_idx + 1}")
                        _ingest_log(
                            f"pdf page={page_idx + 1}: fallback full-page vision len={len(ocr_text)} -> queued for embedding",
                            request_id,
                        )
                except Exception as e:
                    print(f"[FILE][PDF][WARN] Image extraction failed page={page_idx + 1}: {e}")

            if len(page_lines) == 1:
                page_lines.append("[No extractable text found on this page]")

            content_lines.append("\n".join(page_lines))
            _ingest_log(f"pdf page={page_idx + 1}: complete sections={max(0, len(page_lines)-1)}", request_id)

        if pages_to_process < total_pages:
            content_lines.append(
                f"\n... (showing first {pages_to_process} pages of {total_pages} total; set PDF_MAX_PAGES=0 for all pages)"
            )

        if plumber_doc:
            try:
                plumber_doc.close()
            except Exception:
                pass
        if pymupdf_doc:
            try:
                pymupdf_doc.close()
            except Exception:
                pass
        
        return "\n".join(content_lines)
    
    except ImportError:
        print(f"[FILE] PyPDF2 not installed, cannot process PDF: {file_name}")
        return f"**File: {file_name}** [PDF support not installed - PyPDF2 required]"
    except Exception as e:
        print(f"[FILE] Failed to process PDF file {file_name}: {e}")
        return f"**File: {file_name}** [Error reading PDF: {str(e)}]"


def _process_word_file(file_name: str, file_bytes: bytes) -> str:
    """Extract text from Word document."""
    try:
        from docx import Document
        docx_file = BytesIO(file_bytes)
        doc = Document(docx_file)
        
        content_lines = [f"**File: {file_name}**\n"]
        
        for para in doc.paragraphs:
            if para.text.strip():
                content_lines.append(para.text)
        
        for table_idx, table in enumerate(doc.tables):
            content_lines.append(f"\n**Table {table_idx + 1}:**")
            for row in table.rows:
                row_data = [cell.text for cell in row.cells]
                content_lines.append(" | ".join(row_data))
        
        return "\n".join(content_lines)
    
    except ImportError:
        print(f"[FILE] python-docx not installed, cannot process Word doc: {file_name}")
        return f"**File: {file_name}** [Word support not installed - python-docx required]"
    except Exception as e:
        print(f"[FILE] Failed to process Word file {file_name}: {e}")
        return f"**File: {file_name}** [Error reading Word doc: {str(e)}]"


def build_file_context(
    files: Optional[List[Dict[str, str]]],
    describe_image_func=None,
    cancel_check=None,
    request_id: Optional[str] = None,
) -> str:
    """
    Process all uploaded files and build a context string to include in LLM prompt.
    
    Args:
        files: List of file dicts with 'name', 'type', 'data' keys
        describe_image_func: Optional function to describe images
    
    Returns:
        Combined text from all files, or empty string if no files.
    """
    if not files:
        return ""
    
    print(f"[FILE] Processing {len(files)} uploaded files")
    _ingest_log(f"file batch start count={len(files)}", request_id, force=True)
    
    file_contents = []
    for idx, file_data in enumerate(files, start=1):
        if cancel_check and cancel_check():
            _ingest_log(f"cancel acknowledged before file index={idx}; stopping batch", request_id, force=True)
            file_contents.append("[CANCELED] File processing stopped by user.")
            break
        file_name = str((file_data or {}).get("name", "unknown"))
        _ingest_log(f"file batch item {idx}/{len(files)} begin name='{file_name}'", request_id)
        content = process_uploaded_file(
            file_data,
            describe_image_func,
            cancel_check=cancel_check,
            request_id=request_id,
        )
        file_contents.append(content)
        _ingest_log(f"file batch item {idx}/{len(files)} done name='{file_name}' extracted_len={len(content)}", request_id)
    
    combined = "\n\n---FILE SEPARATOR---\n\n".join(file_contents)
    print(f"[FILE] Extracted content from {len(files)} files, total length={len(combined)}")
    _ingest_log(f"file batch complete total_combined_len={len(combined)}", request_id, force=True)
    return combined


# ---------------------------------------------------------------------
# ADO Helpers (continued)
# ---------------------------------------------------------------------



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
    base = _ado_project_base(None)
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
    relations = data.get("relations", [])
    project_name = fields.get("System.TeamProject") or ADO_PROJECT

    comments: List[dict] = []
    try:
        c = requests.get(
            f"{_ado_project_base(project_name)}/_apis/wit/workItems/{work_item_id}/comments?api-version=7.1-preview.3",
            headers=hdrs,
            timeout=60,
        )
        if c.status_code == 200:
            for it in c.json().get("comments", []):
                raw_html = it.get("text", "") or ""
                comments.append(
                    {
                        "text": _strip_html(raw_html),
                        "raw_html": raw_html,
                        "createdBy": (it.get("createdBy") or {}).get("displayName")
                        or (it.get("createdBy") or {}).get("uniqueName")
                        or "",
                        "createdDate": it.get("createdDate") or "",
                    }
                )
    except Exception as e:
        print(f"[ADO][WARN] comments fetch failed: {e}")

    attachments: List[dict] = []
    for relation in relations or []:
        if str(relation.get("rel") or "") != "AttachedFile":
            continue
        attributes = relation.get("attributes") or {}
        relation_url = relation.get("url") or ""
        attachment_name = attributes.get("name") or _ado_guess_filename(relation_url)
        attachments.append(
            {
                "name": attachment_name,
                "url": relation_url,
                "comment": attributes.get("comment") or "",
                "createdDate": attributes.get("resourceCreatedDate") or attributes.get("authorizedDate") or "",
            }
        )

    return {
        "id": work_item_id,
        "project": project_name,
        "fields": fields,
        "comments": comments,
        "attachments": attachments,
    }


def ado_list_tickets(tag_contains: str = "CC") -> List[dict]:
    """Load open support tickets from the configured Azure DevOps saved queries."""
    del tag_contains

    query_targets = _ado_support_ticket_query_definitions()
    if not query_targets:
        return []

    merged_ids: List[int] = []
    seen_ids = set()
    for project, query_path in query_targets:
        label = f"{project}::{query_path}"
        try:
            wiql = _ado_fetch_saved_query_wiql(project, query_path)
            ids = _ado_execute_wiql(project, wiql, label)
        except Exception as exc:
            print(
                f"[ADO][TICKETS][WARN] Saved query '{label}' could not be used ({exc}). "
                "Falling back to the same filter shown in the screenshot."
            )
            ids = _ado_execute_wiql(project, _ado_support_ticket_fallback_wiql(project), f"{label} [fallback]")
        for item_id in ids:
            if item_id in seen_ids:
                continue
            seen_ids.add(item_id)
            merged_ids.append(item_id)

    if not merged_ids:
        return []

    results = []
    for wi in _ado_fetch_work_items_by_ids(merged_ids):
        fid = wi.get("id")
        flds = wi.get("fields", {})
        title = flds.get("System.Title", "")
        state = flds.get("System.State", "")
        tags = flds.get("System.Tags", "")
        project_name = flds.get("System.TeamProject", "")
        changed_date = flds.get("System.ChangedDate", "")
        web_url = f"https://dev.azure.com/{ADO_ORG}/{project_name}/_workitems/edit/{fid}"
        results.append(
            {
                "id": fid,
                "title": title,
                "state": state,
                "tags": tags,
                "project": project_name,
                "changedDate": changed_date,
                "url": web_url,
            }
        )

    results.sort(key=lambda item: (item.get("changedDate") or "", item.get("id") or 0), reverse=True)
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
    """Fetch full ticket context as chronological plain text, including attachments."""
    ticket = ado_fetch_ticket_full(work_item_id)
    fields = ticket.get("fields", {})
    comments = sorted(ticket.get("comments", []), key=lambda item: item.get("createdDate") or "")
    attachments = ticket.get("attachments", [])
    project_name = ticket.get("project") or fields.get("System.TeamProject") or ADO_PROJECT

    title = fields.get("System.Title", "")
    state = fields.get("System.State", "")
    tags = fields.get("System.Tags", "")
    work_item_type = fields.get("System.WorkItemType", "")
    assigned_to = _first_field(fields, ["System.AssignedTo"])
    raw_desc = fields.get("System.Description", "") or fields.get("Microsoft.VSTS.TCM.ReproSteps", "") or ""
    description_text = _render_ado_html_with_inline_images(
        raw_desc,
        section_label=f"ticket {work_item_id} description",
        project=project_name,
    ).strip() or "Not provided."

    discussion_blocks: List[str] = []
    total_comments = len(comments)
    for index, comment in enumerate(comments, start=1):
        author = comment.get("createdBy") or "Unknown"
        created_date = comment.get("createdDate") or ""
        body = _render_ado_html_with_inline_images(
            comment.get("raw_html") or comment.get("text") or "",
            section_label=f"ticket {work_item_id} discussion comment {index}",
            project=project_name,
        ).strip() or "[Empty discussion entry]"
        header = f"[{created_date}] {author}"
        discussion_blocks.append(f"{header}\n{body}")
        print(f"[ADO][TICKET] Processed discussion entry {index}/{total_comments} for work item {work_item_id}")

    attachment_text = _build_ticket_attachment_context(
        work_item_id,
        attachments,
        project=project_name,
    ).strip()

    sections = [
        f"Ticket ID: {work_item_id}",
        f"Project: {project_name}",
        f"Type: {work_item_type}",
        f"Title: {title}",
        f"State: {state}",
        f"Assigned To: {assigned_to}",
        f"Tags: {tags}",
        "",
        "Description (full, chronological):",
        description_text,
        "",
        "Discussion (full, chronological):",
        "\n\n---\n\n".join(discussion_blocks) if discussion_blocks else "Not provided.",
    ]

    if attachment_text:
        sections.extend(
            [
                "",
                "Attachments (full content, chronological when Azure DevOps provides dates):",
                attachment_text,
            ]
        )

    blob = "\n".join(section for section in sections if section is not None).strip()
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
    
    # Clone the source repository (not wiki) to access "AI Knowledge Files"
    repo_name = os.getenv("ADO_REPO_NAME", "Support")
    remote = f"https://dev.azure.com/{ADO_ORG}/{ADO_PROJECT}/_git/{repo_name}"
    b64 = base64.b64encode(f":{ADO_PAT}".encode("utf-8")).decode("utf-8")

    base_dir = tempfile.mkdtemp(prefix="wiki_rag_git_", dir=tmp_root)
    dest = os.path.join(base_dir, "repo")
    print(f"[GIT] Cloning repository '{repo_name}' into {dest}")
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


def _describe_local_image_via_vision(file_path: str) -> Optional[str]:
    """
    Use OpenAI vision to describe a local image file (supports .png, .jpg, .jpeg, .gif, .webp).
    Converts file to base64 data URI and sends to vision API.
    Returns a text description of the image, or None if processing fails.
    """
    if not HAS_PIL:
        print(f"[VISION] PIL not installed; skipping image analysis for {file_path}")
        return None
    
    try:
        # Determine mime type
        ext = os.path.splitext(file_path)[1].lower()
        mime_map = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp",
        }
        mime_type = mime_map.get(ext)
        if not mime_type:
            print(f"[VISION] Unsupported image format: {ext}")
            return None
        
        # Read and encode to base64
        with open(file_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
        
        data_uri = f"data:{mime_type};base64,{image_data}"
        
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
        body = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Briefly describe what you see in this image. Focus on any technical content, errors, UI elements, code, diagrams, or relevant details."},
                        {"type": "image_url", "image_url": {"url": data_uri}},
                    ],
                }
            ],
            "max_tokens": 200,
        }
        print(f"[VISION] Processing image file: {file_path}")
        resp = requests.post(f"{OPENAI_URL}/chat/completions", json=body, headers=headers, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            description = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            print(f"[VISION] Image description ({os.path.basename(file_path)}): {description[:150]}...")
            structured = _extract_structured_text_from_image(data_uri, source_label=os.path.basename(file_path))
            return structured or description
        else:
            print(f"[VISION][WARN] Vision call failed for {file_path}: {resp.status_code}")
            return None
    except Exception as e:
        print(f"[VISION][WARN] Failed to describe image {file_path}: {e}")
        return None


def compare_and_ingest_internal() -> Tuple[int, int]:
    """Clone the Azure DevOps repo and ingest files from AI Knowledge Files directory."""
    print("[COMPARE_INGEST] Starting compare-and-ingest from Azure DevOps repo")

    # If ADO not configured, fallback to local filesystem ingest
    if not (ADO_ORG and ADO_PROJECT and ADO_PAT):
        print("[COMPARE_INGEST][WARN] ADO not configured, falling back to local files")
        added = ingest_wiki_files(only_missing=True)
        return added, collection.count()

    repo_dir = None
    try:
        repo_dir = _git_clone_wiki()
        print(f"[GIT] Clone completed: {repo_dir}")
        
        # Navigate to AI Knowledge Files directory
        ai_knowledge_path = os.path.join(repo_dir, "AI Knowledge Files")
        
        if not os.path.exists(ai_knowledge_path):
            print(f"[COMPARE_INGEST][ERROR] AI Knowledge Files directory not found at {ai_knowledge_path}")
            return 0, collection.count()
        
        print(f"[COMPARE_INGEST] Found AI Knowledge Files at {ai_knowledge_path}")
        
        # Get files from the two target directories (both markdown and images)
        target_dirs = ["new_files_for_ai_knowledge", "TA9-WIKI"]
        md_files: List[str] = []
        image_files: List[str] = []
        image_extensions = (".png", ".jpg", ".jpeg", ".gif", ".webp")
        
        for target_dir in target_dirs:
            dir_path = os.path.join(ai_knowledge_path, target_dir)
            if os.path.exists(dir_path):
                print(f"[COMPARE_INGEST] Scanning {target_dir} directory...")
                for p in pathlib.Path(dir_path).rglob("*"):
                    if p.is_file():
                        rel = os.path.relpath(str(p), ai_knowledge_path)
                        if p.suffix.lower() == ".md":
                            md_files.append(rel)
                        elif p.suffix.lower() in image_extensions:
                            image_files.append(rel)
            else:
                print(f"[COMPARE_INGEST][WARN] Directory {target_dir} not found")
        
        print(f"[GIT] Found {len(md_files)} markdown files and {len(image_files)} image files in AI Knowledge Files")

        all_files = md_files + image_files
        if not all_files:
            return 0, collection.count()

        existing_sources = set(get_ingested_sources())
        to_ingest = [f for f in all_files if f not in existing_sources]
        print(f"[COMPARE_INGEST] Files to ingest (missing) = {len(to_ingest)}")

        if not to_ingest:
            return 0, collection.count()

        added_chunks = 0
        skipped_empty: List[str] = []
        skipped_no_chunks: List[str] = []
        skipped_errors: List[str] = []
        
        for idx, rel in enumerate(to_ingest, start=1):
            abs_path = os.path.join(ai_knowledge_path, rel)
            is_image = rel.lower().endswith(image_extensions)
            print(f"[COMPARE_INGEST] [{idx}/{len(to_ingest)}] Ingesting {'image' if is_image else 'markdown'} file: {rel}")
            
            text = None
            if is_image:
                # Process image file using vision API
                text = _describe_local_image_via_vision(abs_path)
                if not text:
                    print(f"[COMPARE_INGEST] Failed to extract content from image {rel}")
                    skipped_errors.append(rel)
                    continue
                # Prepend file name to image description for context
                text = f"[Image: {os.path.basename(rel)}]\n\n{text}"
            else:
                # Process markdown file
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
                metas.append({"source": rel, "chunk": i, "file_type": "image" if is_image else "markdown"})
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
        print(f"[COMPARE_INGEST] Markdown files in AI Knowledge Files: {len(md_files)}")
        print(f"[COMPARE_INGEST] Image files in AI Knowledge Files: {len(image_files)}")
        print(f"[COMPARE_INGEST] Total files in AI Knowledge Files: {len(all_files)}")
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
        "dashboard", "admin studio", "data model", "dm",
        "situational awareness", "incident", "incidents", "map", "layer", "layers",
        "camera", "cameras", "protocol", "federated search", "ontology","kyc"
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


def _has_ta9_context(text: str) -> bool:
    """Domain gate: detects clear TA9/IntSight product context."""
    if not text:
        return False
    t = text.lower()
    term_groups = {
        "brand": [
            "ta9", "t-a9", "t a9", "intsight", "int-sight", "int sight",
        ],
        "core_modules": [
            "admin studio", "kyc", "federated search", "data model", "data models", "entities",
            "relations", "ontology manager", "main graph", "link analysis", "cases",
            "tasks", "situational awareness", "dashboard", "insight", "annotations", "autoloader",
        ],
        "platform_terms": [
            "identifier", "taxonomy", "query builder", "cluster query", "field role",
            "is free text", "is id", "sequence", "permission mode", "case profile",
            "indexing service", "index to federated", "admin tools", "lookup manager",
        ],
    }

    group_hits = 0
    for _, terms in term_groups.items():
        if any(term in t for term in terms):
            group_hits += 1

    return group_hits >= 1


def _has_ta9_support_signal(text: str) -> bool:
    """
    Detects meaningful technical/procedural support content aligned with TA9 guide material.
    Accepts operational documentation, configuration steps, integration guidance, and troubleshooting.
    """
    if not text:
        return False

    t = text.lower()

    workflow_terms = [
        "step", "click", "open", "select", "save", "configure", "set", "define", "navigate",
        "upload", "download", "reset", "create", "edit", "delete", "assign", "grant",
        "permission", "role", "profile", "workflow", "prerequisite", "note:",
    ]
    technical_terms = [
        "api", "rest", "endpoint", "json", "regex", "query", "sql", "mysql", "mariadb",
        "solr", "orient", "indexing", "schema", "field", "mapping", "lookup", "parser",
        "config", "dll", "path", "service", "cache", "cron", "batch", "token", "2fa",
        "sso", "active directory", "ldap", "authentication", "authorization", "audit",
    ]
    product_artifacts = [
        "admin", "analyst", "developer", "entity", "relation", "case", "incident", "protocol",
        "map", "graph", "gantt", "timeline", "facet", "widget", "dashboard", "federated",
        "data loader", "load file manager", "autoloader", "document viewer", "speech to text",
        "translation", "system config", "localization", "situational awareness", "situational picture", "sit pit",
    ]
    integration_terms = [
        "kerberos", "krb5", "krb5.conf", "krb5.keytab", "keytab", "spn", "realm", "kdc",
        "mssql", "sql server", "odbc", "odbc.ini", "trusted_connection", "integratedsecurity",
        "authmech", "krbservicename", "krbhostfqdn", "krbauthrealm", "active directory",
        "domain controller", "dc", "ad user",
    ]
    application_reference_terms = [
        "integration", "integrations", "integrate", "integrated with", "connector", "connectors",
        "application", "applications", "module", "modules", "plugin", "plugins", "supported app",
        "supported apps", "external system", "external systems", "third-party", "third party",
        "known as", "also known as", "alias", "aliases", "alternative name", "alternative names",
        "naming", "mapped to", "referred to as",
    ]

    workflow_hits = sum(1 for term in workflow_terms if term in t)
    technical_hits = sum(1 for term in technical_terms if term in t)
    artifact_hits = sum(1 for term in product_artifacts if term in t)
    integration_hits = sum(1 for term in integration_terms if term in t)
    application_reference_hits = sum(1 for term in application_reference_terms if term in t)

    has_structured_config_pattern = bool(
        re.search(r"\b[a-z0-9_.-]+\s*=\s*[^\s].+", t)
        or re.search(r"<add\s+key=", t)
        or re.search(r"\{\s*\"[a-z0-9_\-]+\"\s*:", t)
    )
    has_stepwise_pattern = bool(re.search(r"\bstep\s*\d+\b", t))
    has_version_or_section_pattern = bool(re.search(r"\b(v|version)\s*\d+(\.\d+)*\b", t))

    # Broad but meaningful acceptance for guide-like knowledge
    if workflow_hits >= 3 and artifact_hits >= 1:
        return True
    if technical_hits >= 3 and artifact_hits >= 1:
        return True
    if artifact_hits >= 2 and (has_structured_config_pattern or has_stepwise_pattern):
        return True
    if artifact_hits >= 2 and technical_hits >= 2:
        return True
    if has_version_or_section_pattern and artifact_hits >= 2 and (workflow_hits >= 2 or technical_hits >= 2):
        return True
    # Explicit acceptance for enterprise integration/config guides (e.g., Kerberos + MSSQL setup)
    if integration_hits >= 3 and has_structured_config_pattern:
        return True
    if integration_hits >= 4 and (workflow_hits >= 2 or technical_hits >= 2):
        return True
    if "prerequisite" in t and integration_hits >= 3:
        return True
    # Accept IntSight application/integration reference knowledge even when it is descriptive rather than procedural.
    if application_reference_hits >= 2 and artifact_hits >= 1:
        return True
    if application_reference_hits >= 1 and artifact_hits >= 2:
        return True

    return False


def _looks_clearly_out_of_scope_knowledge(text: str) -> bool:
    """Reject only obvious junk or clearly unrelated content."""
    if not text:
        return True

    if _has_ta9_context(text) or _has_ta9_support_signal(text):
        return False

    candidate = str(text or "").strip()
    lower_candidate = candidate.lower()
    word_count = len(re.findall(r"\b\w+\b", candidate))

    if word_count < 4:
        return True

    if re.fullmatch(r"[\W_]+", candidate):
        return True

    repeated_tokens = re.findall(r"\b([a-z0-9]{2,})\b", lower_candidate)
    if repeated_tokens and len(set(repeated_tokens)) == 1 and len(repeated_tokens) >= 4:
        return True

    off_topic_terms = {
        "food": ["banana", "recipe", "cook", "cooking", "bake", "oven", "ingredient", "meal", "diet", "nutrition"],
        "travel": ["flight", "hotel", "vacation", "beach", "tourism", "itinerary", "passport", "resort"],
        "entertainment": ["movie", "series", "celebrity", "song", "lyrics", "album", "netflix"],
        "lifestyle": ["dating", "horoscope", "astrology", "workout", "gym", "fashion", "makeup"],
        "creative": ["joke", "poem", "haiku", "story prompt", "fan fiction"],
    }
    off_topic_hits = 0
    for terms in off_topic_terms.values():
        if any(term in lower_candidate for term in terms):
            off_topic_hits += 1

    conversational_irrelevance = any(
        phrase in lower_candidate
        for phrase in [
            "tell me a joke",
            "write a poem",
            "how to cook",
            "how do i eat",
            "what should i eat",
            "travel plan",
            "write me a joke",
            "write me a poem",
        ]
    )

    return off_topic_hits >= 1 or conversational_irrelevance


def _strip_non_knowledge_markers(text: str) -> str:
    candidate = str(text or "")
    candidate = re.sub(r"\*\*File:\s*.+?\*\*", " ", candidate)
    candidate = candidate.replace("---FILE SEPARATOR---", " ")
    candidate = re.sub(r"(?mi)^\[(error|warning|notice|canceled)[^\n]*\]", " ", candidate)
    candidate = re.sub(r"(?mi)^\[image content from [^\n]+\]", " ", candidate)
    candidate = re.sub(r"(?mi)^\[visual_fallback\]", " ", candidate)
    candidate = re.sub(r"(?mi)^\[image analysis unavailable\]", " ", candidate)
    candidate = re.sub(r"\s+", " ", candidate)
    return candidate.strip()


def _looks_like_failed_or_empty_extraction(text: str) -> bool:
    candidate = str(text or "").strip()
    if not candidate:
        return True

    has_failure_marker = bool(re.search(r"(?mi)^\[(error|warning|notice|canceled)[^\n]*\]", candidate))
    normalized = _strip_non_knowledge_markers(candidate)
    meaningful_word_count = len(re.findall(r"\b\w+\b", normalized))

    if has_failure_marker and meaningful_word_count < 8:
        return True

    if meaningful_word_count < 4:
        return True

    return False


def _validate_ta9_knowledge_content(content_text: str) -> Tuple[bool, str]:
    """Approve by default and reject only obvious junk or irrelevant content."""
    text = (content_text or "").strip()
    if not text:
        return False, "The content is empty. Please provide TA9-related details before adding knowledge."

    if _looks_like_failed_or_empty_extraction(text):
        return False, (
            "The new knowledge could not be extracted into usable content. "
            "Please provide meaningful text or upload a file that contains readable, relevant information."
        )

    if _has_ta9_context(text) or _has_ta9_support_signal(text):
        return True, "Approved"

    text_word_count = len(re.findall(r"\b\w+\b", text))
    if text_word_count < 4:
        return False, (
            "The content is too short to classify. "
            "Please add a few more words so it can be stored as useful knowledge."
        )

    if not _looks_clearly_out_of_scope_knowledge(text):
        return True, "Approved"

    return False, (
        "The content looks clearly out of scope for this knowledge base. "
        "Only obvious junk or unrelated topics are blocked."
    )


def _build_query_variants(question: str, ta9_mode: bool) -> List[str]:
    """Generate a small set of semantically-equivalent queries for multi-retrieval."""
    variants = []
    base = question.strip()
    if base:
        variants.append(base)
    normalized = _normalize_question(question)
    if normalized and normalized not in variants:
        variants.append(normalized)

    q_low = (question or "").lower()
    procedural_intent = _question_has_procedural_intent(question)
    entity_fact_intent = _question_has_entity_fact_intent(question)
    broad_coverage_intent = _question_requests_broad_coverage(question)
    if any(term in q_low for term in ["camera", "cameras", "layer", "layers", "situational awareness", "incident", "map"]):
        map_ops_boost = (
            "situational awareness map layers camera request surrounding cameras "
            "view actions map toolbar layers panel"
        )
        variants.append(f"{base}\n\n{map_ops_boost}" if base else map_ops_boost)

    if procedural_intent:
        procedural_boost = "step by step instructions procedure configure setup admin tools system configuration"
        variants.append(f"{base}\n\n{procedural_boost}" if base else procedural_boost)

        procedural_subtasks = _extract_procedural_subtasks(question, max_subtasks=3)
        for action, object_phrase in procedural_subtasks[:2]:
            subtask_variant = f"how to {action} {object_phrase} step by step"
            if subtask_variant not in variants:
                variants.append(subtask_variant)

    if entity_fact_intent:
        entity_boost = (
            "company name product names naming policy naming convention "
            "referred to as alias aliases main platform known as"
        )
        variants.append(f"{base}\n\n{entity_boost}" if base else entity_boost)

    if broad_coverage_intent:
        breadth_boost = (
            "alternative ways other methods different approaches additional options "
            "another way supported methods available options compare distinct procedures"
        )
        variants.append(f"{base}\n\n{breadth_boost}" if base else breadth_boost)

    # Avoid broad TA9 expansion for already-specific procedural questions because it dilutes retrieval.
    if ta9_mode and not procedural_intent and not entity_fact_intent and not broad_coverage_intent and len(_tokenize_normalized(question)) <= 6:
        ta9_boost = (
            "TA9 / IntSight platform features, capabilities, modules, "
            "system overview, dashboards, admin studio, data model"
        )
        variants.append(f"{base}\n\n{ta9_boost}" if base else ta9_boost)
    deduped_variants: List[str] = []
    seen = set()
    for variant in variants:
        key = re.sub(r"\s+", " ", str(variant or "").strip().lower())
        if not key or key in seen:
            continue
        seen.add(key)
        deduped_variants.append(variant)
    return deduped_variants[:5]

def augment_question(question: str) -> str:
    """
    Minimal augmentation: only expand very short questions with common synonyms.
    Keep general-purpose for any domain.
    """
    if not question or len(question.split()) > 15:
        # Only augment genuinely short queries
        return question

    if _question_has_entity_fact_intent(question):
        return question
    
    q_low = question.lower()
    synonyms: List[str] = []
    
    # Minimal, general augmentation for short queries
    if (("how" in q_low and "how many" not in q_low and "how much" not in q_low) or "add" in q_low or "create" in q_low):
        synonyms.extend(["how to", "instructions", "steps", "procedure", "create", "add", "setup", "configure"])
    
    if "what" in q_low:
        synonyms.extend(["definition", "explanation", "description", "overview"])
    
    if "help" in q_low or "issue" in q_low or "problem" in q_low:
        synonyms.extend(["troubleshooting", "solution", "fix", "resolve", "error"])
    
    if not synonyms:
        return question
    
    augmented = question + "\n" + " ".join(set(synonyms))
    return augmented


def _question_has_procedural_intent(question: str) -> bool:
    q = (question or "").lower()
    if not q:
        return False
    procedural_terms = [
        "how to", "step by step", "step-by-step", "steps", "procedure", "configure",
        "configuration", "setup", "set up", "create", "add", "edit", "change",
        "update", "install", "enable", "disable", "fix", "resolve",
    ]
    return any(term in q for term in procedural_terms)


def _question_requests_broad_coverage(question: str) -> bool:
    q = (question or "").lower().strip()
    if not q:
        return False

    explicit_patterns = [
        r"\bis there (any )?more (ways|options|methods|approaches)\b",
        r"\bmore (ways|options|methods|approaches)\b",
        r"\bother (ways|options|methods|approaches)\b",
        r"\banother (way|option|method|approach)\b",
        r"\bdifferent (ways|options|methods|approaches)\b",
        r"\balternative(s)?\b",
        r"\bwhat else\b",
        r"\bany other\b",
        r"\blist (all )?(ways|options|methods|approaches|types|variants)\b",
        r"\bwhat are the (ways|options|methods|approaches|types)\b",
        r"\bwhich (ways|options|methods|approaches|types)\b",
        r"\bsupported (ways|options|methods|approaches)\b",
        r"\bavailable (ways|options|methods|approaches)\b",
    ]
    if any(re.search(pattern, q) for pattern in explicit_patterns):
        return True

    breadth_terms = ["way", "ways", "option", "options", "method", "methods", "approach", "approaches"]
    breadth_modifiers = ["more", "other", "another", "different", "alternative", "alternatives", "available", "supported", "all"]
    return any(term in q for term in breadth_terms) and any(modifier in q for modifier in breadth_modifiers)


def _question_has_entity_fact_intent(question: str) -> bool:
    q = (question or "").lower()
    if not q:
        return False

    explicit_patterns = [
        r"\bhow many\s+(product|products|module|modules|service|services|platform|platforms)\b",
        r"\bwhich\s+(product|products|module|modules|service|services|platform|platforms)\b",
        r"\bwhat\s+(product|products|module|modules|service|services|platform|platforms)\b",
        r"\b(company|vendor|organization|brand)\s+name\b",
        r"\bproduct\s+name(s)?\b",
        r"\bnaming\s+(policy|convention|rule|rules)\b",
        r"\breferred\s+to\s+as\b",
        r"\bcalled\b",
        r"\balias(es)?\b",
        r"\bmain\s+platform\b",
    ]
    if any(re.search(pattern, q) for pattern in explicit_patterns):
        return True

    fact_terms = [
        "company", "companies", "product", "products", "platform", "platforms",
        "module", "modules", "vendor", "brand", "name", "names", "named",
        "naming", "called", "alias", "aliases", "provide", "provides", "offered",
        "offer", "offers", "created", "create",
    ]
    term_hits = sum(1 for term in fact_terms if term in q)
    return term_hits >= 2


def _question_explicitly_requests_database_solution(question: str) -> bool:
    q = (question or "").lower().strip()
    if not q:
        return False

    explicit_patterns = [
        r"\b(database|db)\b",
        r"\b(sql|sql server|mssql|mysql|mariadb|postgres(?:ql)?|sqlite)\b",
        r"\bbackend table(?:-level)?\b",
        r"\btable[- ]level\b",
        r"\bdirect(?:ly)? in (?:the )?database\b",
        r"\bthrough (?:the )?database\b",
        r"\bvia sql\b",
        r"\bdataschema1\b",
        r"\bdataschemafields1\b",
        r"\bdataconnectionsmanager\b",
        r"\bindexing_audit\b",
    ]
    if any(re.search(pattern, q) for pattern in explicit_patterns):
        return True

    table_terms = bool(re.search(r"\b(table|tables|column|columns|schema)\b", q))
    db_terms = bool(re.search(r"\b(database|db|sql|backend)\b", q))
    return table_terms and db_terms


def _question_explicitly_requests_admin_studio_solution(question: str) -> bool:
    q = (question or "").lower().strip()
    if not q:
        return False

    explicit_patterns = [
        r"\badmin studio\b",
        r"\bui\b",
        r"\buser interface\b",
        r"\bthrough (?:the )?ui\b",
        r"\bfrom (?:the )?ui\b",
        r"\bthrough admin studio\b",
        r"\bfrom admin studio\b",
        r"\busing admin studio\b",
    ]
    return any(re.search(pattern, q) for pattern in explicit_patterns)


def _preferred_solution_channel(question: str) -> Optional[str]:
    if _question_explicitly_requests_database_solution(question):
        return "database"
    if _question_explicitly_requests_admin_studio_solution(question):
        return "admin_studio"
    if _question_has_procedural_intent(question) and (_is_ta9_question(question) or _has_ta9_context(question)):
        return "admin_studio"
    return None


def _source_solution_channel_scores(title: str = "", source: str = "", text: str = "") -> Tuple[float, float]:
    combined = "\n".join(part for part in [title, source, text] if part).lower()
    if not combined.strip():
        return 0.0, 0.0

    admin_score = 0.0
    database_score = 0.0

    admin_markers = [
        ("admin studio", 4.0),
        ("ui-based", 2.8),
        ("user interface", 2.5),
        ("navigate", 1.1),
        ("click", 1.1),
        ("open", 0.6),
        ("select", 0.6),
        ("button", 1.0),
        ("tab", 0.9),
        ("page", 0.8),
        ("screen", 0.9),
        ("dropdown", 1.0),
        ("checkbox", 1.0),
        ("save", 0.4),
    ]
    database_markers = [
        ("dataschema1", 4.0),
        ("dataschemafields1", 4.0),
        ("dataconnectionsmanager", 3.5),
        ("indexing_audit", 3.5),
        ("database", 3.0),
        (" sql ", 2.2),
        ("sql server", 3.0),
        ("mssql", 3.0),
        ("mysql", 3.0),
        ("mariadb", 3.0),
        ("postgres", 3.0),
        ("sqlite", 3.0),
        ("dbtablename", 1.8),
        ("connectionid", 1.8),
        ("isindextofederatedsearch", 1.9),
        ("fieldrole", 1.4),
        ("isid", 1.2),
        ("isqueryable", 1.2),
        ("isvalid", 1.2),
        ("backend table", 2.2),
    ]

    for marker, weight in admin_markers:
        if marker in combined:
            admin_score += weight
    for marker, weight in database_markers:
        if marker in combined:
            database_score += weight

    ui_like_hits = len(re.findall(r"\b(click|select|open|navigate|button|tab|screen|ui|admin studio|dropdown|checkbox|page|section)\b", combined))
    if ui_like_hits >= 2:
        admin_score += min(3.0, ui_like_hits * 0.45)

    if re.search(r"(?mi)^\s*(select|update|insert\s+into|delete\s+from)\b", combined):
        database_score += 3.0
    if re.search(r"\bfrom\s+[a-z0-9_.]+\b", combined):
        database_score += 1.2

    return admin_score, database_score


def _classify_source_solution_channel(title: str = "", source: str = "", text: str = "") -> str:
    admin_score, database_score = _source_solution_channel_scores(title=title, source=source, text=text)
    if admin_score >= 3.0 and admin_score >= database_score + 1.0:
        return "admin_studio"
    if database_score >= 3.0 and database_score >= admin_score + 1.0:
        return "database"
    if admin_score >= 3.0 and database_score >= 3.0:
        return "mixed"
    return "unknown"


def _source_solution_preference_adjustment(question: str, title: str = "", source: str = "", text: str = "") -> float:
    preferred_channel = _preferred_solution_channel(question)
    if not preferred_channel:
        return 0.0

    admin_score, database_score = _source_solution_channel_scores(title=title, source=source, text=text)
    channel = _classify_source_solution_channel(title=title, source=source, text=text)
    if preferred_channel == "admin_studio":
        if channel == "admin_studio":
            return 5.5
        if channel == "database":
            return -6.5
        if admin_score > database_score and admin_score >= 2.0:
            return 2.0
        if database_score > admin_score and database_score >= 2.0:
            return -2.5
        return 0.0

    if channel == "database":
        return 5.5
    if channel == "admin_studio":
        return -6.5
    if database_score > admin_score and database_score >= 2.0:
        return 2.0
    if admin_score > database_score and admin_score >= 2.0:
        return -2.5
    return 0.0


def _broad_coverage_signal_score(question: str, text: str) -> float:
    if not _question_requests_broad_coverage(question) or not text:
        return 0.0

    t = (text or "").lower()
    score = 0.0
    weighted_phrases = [
        ("alternative", 1.8),
        ("alternatively", 1.8),
        ("another way", 2.0),
        ("other way", 2.0),
        ("different way", 2.0),
        ("another method", 2.0),
        ("other method", 2.0),
        ("different method", 2.0),
        ("another option", 1.7),
        ("other option", 1.7),
        ("additional option", 1.7),
        ("additional way", 1.7),
        ("additional method", 1.7),
        ("supported method", 1.4),
        ("supported option", 1.4),
        ("available method", 1.4),
        ("available option", 1.4),
        ("can also be", 1.3),
        ("can be created from", 1.5),
        ("can be created via", 1.5),
        ("can be configured from", 1.5),
        ("can be done via", 1.5),
    ]
    for phrase, weight in weighted_phrases:
        if phrase in t:
            score += weight

    if re.search(r"(?m)^\s*(?:[-*]|\d+\.)\s+.+", t):
        score += 0.9

    method_terms = sum(1 for term in ["way", "ways", "option", "options", "method", "methods", "approach", "approaches"] if term in t)
    if method_terms >= 2:
        score += min(1.6, method_terms * 0.35)

    return min(score, 6.0)


def _entity_fact_signal_score(question: str, text: str) -> float:
    if not _question_has_entity_fact_intent(question) or not text:
        return 0.0

    q = (question or "").lower()
    t = (text or "").lower()
    score = 0.0

    shared_pairs = [
        ("company", 1.2),
        ("product", 1.2),
        ("products", 1.2),
        ("name", 0.8),
        ("names", 0.8),
        ("naming", 1.0),
        ("called", 0.9),
        ("referred to as", 1.0),
        ("alias", 0.9),
        ("main platform", 1.1),
    ]
    for token, weight in shared_pairs:
        if token in q and token in t:
            score += weight

    if ("company" in t or "company name" in t) and ("product" in t or "product name" in t or "product names" in t):
        score += 1.8

    high_signal_phrases = [
        "company name",
        "product name",
        "product names",
        "naming policy",
        "naming convention",
        "should be referred to as",
        "should not be used as part of the product name",
        "main platform name",
    ]
    for phrase in high_signal_phrases:
        if phrase in t:
            score += 1.4

    if re.search(r"(?m)^\s*[-*]\s+.+", t) and ("product" in q or "how many" in q or "which" in q):
        score += 0.8

    if re.search(r"\b(known as|also known as|referred to as|called)\b", t):
        score += 1.0

    return min(score, 8.0)


_LEXICAL_STOPWORDS = {
    "the", "is", "are", "a", "an", "and", "or", "to", "of", "in", "on", "for", "with", "by",
    "from", "as", "at", "be", "this", "that", "these", "those", "it", "its", "if", "then",
    "how", "what", "when", "where", "why", "who", "can", "could", "should", "would", "do",
    "does", "did", "i", "we", "you", "they", "he", "she", "my", "our", "your", "their",
    "about", "into", "through", "using", "use", "want", "need", "like", "please",
}


def _normalize_term(term: str) -> str:
    t = (term or "").strip().lower()
    t = re.sub(r"[^a-z0-9_\-]", "", t)
    if not t:
        return ""
    # Light stemming to match camera/cameras, layer/layers, etc.
    if len(t) > 5 and t.endswith("ies"):
        t = t[:-3] + "y"
    elif len(t) > 4 and t.endswith("es"):
        t = t[:-2]
    elif len(t) > 3 and t.endswith("s"):
        t = t[:-1]
    return t


def _tokenize_normalized(text: str) -> List[str]:
    raw_tokens = re.findall(r"[a-zA-Z0-9_\-]+", (text or "").lower())
    out: List[str] = []
    for token in raw_tokens:
        norm = _normalize_term(token)
        if len(norm) <= 2 or norm in _LEXICAL_STOPWORDS:
            continue
        out.append(norm)
    return out


def _extract_key_phrases(question: str, max_phrases: int = 6) -> List[str]:
    q = (question or "").strip().lower()
    if not q:
        return []

    phrases: List[str] = []
    # Quoted phrases should be treated as high-signal hints.
    for quoted in re.findall(r'"([^"]{3,80})"', q):
        cleaned = " ".join(quoted.split()).strip()
        if cleaned:
            phrases.append(cleaned)

    tokens = _tokenize_normalized(q)
    # Add bigrams/trigrams for intent like "situational awareness", "camera request".
    for n in (3, 2):
        for i in range(0, max(0, len(tokens) - n + 1)):
            candidate = " ".join(tokens[i:i + n])
            if len(candidate) >= 8:
                phrases.append(candidate)
            if len(phrases) >= max_phrases:
                break
        if len(phrases) >= max_phrases:
            break

    deduped: List[str] = []
    seen = set()
    for item in phrases:
        if item in seen:
            continue
        seen.add(item)
        deduped.append(item)
        if len(deduped) >= max_phrases:
            break
    return deduped


def _normalize_compact_text(text: str) -> str:
    normalized = _normalize_question(text or "")
    return re.sub(r"\s+", " ", normalized).strip()


def _extract_action_object_targets(question: str, max_targets: int = 3) -> List[Tuple[str, str]]:
    if not question:
        return []

    normalized_question = re.sub(r"\s+", " ", re.sub(r"[^a-z0-9_\-\s]", " ", str(question or "").lower())).strip()
    if not normalized_question:
        return []

    action_patterns = [
        ("set up", "set up"),
        ("setup", "setup"),
        ("configure", "configure"),
        ("create", "create"),
        ("add", "add"),
        ("edit", "edit"),
        ("update", "update"),
        ("delete", "delete"),
        ("remove", "remove"),
        ("install", "install"),
        ("enable", "enable"),
        ("disable", "disable"),
        ("fix", "fix"),
        ("resolve", "resolve"),
    ]
    filler_terms = {
        "a", "an", "the", "new", "another", "other", "more", "additional", "existing",
        "selected", "target", "current", "available", "supported", "different",
    }
    clause_boundary_pattern = re.compile(
        r"\b(?:when|if|after|before|because|while|unless|except|where|which|that)\b"
    )
    trailing_procedural_noise_pattern = re.compile(
        r"\b(?:step(?:\s+by\s+step)?|step-by-step|instructions?|procedure|procedures|guide|guidance)\b.*$"
    )
    preserved_joiners = {"and", "or", "from", "using", "with", "by", "via", "through", "into", "in", "on", "for", "to"}

    targets: List[Tuple[str, str]] = []
    seen = set()
    for raw_action, canonical_action in action_patterns:
        for match in re.finditer(rf"\b{re.escape(raw_action)}\b", normalized_question):
            tail = normalized_question[match.end():].strip()
            if not tail:
                continue
            tail = clause_boundary_pattern.split(tail, maxsplit=1)[0].strip()
            tail = trailing_procedural_noise_pattern.sub("", tail).strip(" ,-_")
            raw_tokens = re.findall(r"[a-z0-9_\-]+", tail)
            object_tokens: List[str] = []
            for raw_token in raw_tokens:
                if raw_token in filler_terms:
                    continue
                if raw_token in preserved_joiners:
                    if object_tokens and object_tokens[-1] not in preserved_joiners:
                        object_tokens.append(raw_token)
                    continue

                token = _normalize_term(raw_token)
                if len(token) <= 2 or token in _LEXICAL_STOPWORDS:
                    continue
                object_tokens.append(token)
                if len([item for item in object_tokens if item not in preserved_joiners]) >= 10:
                    break
            if not object_tokens:
                continue
            while object_tokens and object_tokens[-1] in preserved_joiners:
                object_tokens.pop()
            while object_tokens and object_tokens[0] in preserved_joiners:
                object_tokens.pop(0)
            object_phrase = " ".join(object_tokens)
            key = (canonical_action, object_phrase)
            if key in seen:
                continue
            seen.add(key)
            targets.append(key)
            if len(targets) >= max_targets:
                return targets
    return targets


def _split_coordinated_object_phrase(object_phrase: str) -> List[str]:
    candidate = re.sub(r"\s+", " ", str(object_phrase or "").strip().lower())
    if not candidate:
        return []

    qualifier_match = re.search(r"\b(from|using|with|via|through|in|on|for|into)\b.+$", candidate)
    qualifier = ""
    base_phrase = candidate
    if qualifier_match:
        qualifier = qualifier_match.group(0).strip()
        base_phrase = candidate[:qualifier_match.start()].strip()

    if not re.search(r"\b(and|or)\b", base_phrase):
        return [candidate]

    parts = [part.strip(" ,-_") for part in re.split(r"\b(?:and|or)\b", base_phrase) if part.strip(" ,-_")]
    expanded: List[str] = []
    seen = set()
    for part in parts:
        normalized_part = re.sub(r"\s+", " ", part).strip()
        if not normalized_part:
            continue
        combined = f"{normalized_part} {qualifier}".strip() if qualifier else normalized_part
        combined = re.sub(r"\s+", " ", combined).strip()
        if combined and combined not in seen:
            seen.add(combined)
            expanded.append(combined)

    return expanded or [candidate]


def _extract_procedural_subtasks(question: str, max_subtasks: int = 6) -> List[Tuple[str, str]]:
    subtasks: List[Tuple[str, str]] = []
    seen = set()
    for action, object_phrase in _extract_action_object_targets(question, max_targets=max_subtasks):
        split_objects = _split_coordinated_object_phrase(object_phrase)
        for object_part in split_objects:
            key = (action, object_part)
            if key in seen:
                continue
            seen.add(key)
            subtasks.append(key)
            if len(subtasks) >= max_subtasks:
                return subtasks
    return subtasks


def _split_text_into_relevance_segments(text: str, max_segments: int = 120) -> List[str]:
    if not text:
        return []
    segments = [
        segment.strip()
        for segment in re.split(r"[\n\r]+|(?<=[\.;:!?])\s+", str(text or ""))
        if segment and segment.strip()
    ]
    return segments[:max_segments]


def _is_generic_procedural_scaffolding_segment(segment: str) -> bool:
    normalized = re.sub(r"\s+", " ", str(segment or "").strip().lower())
    if not normalized:
        return False

    generic_patterns = [
        r"\bfollow these step by step instructions\b",
        r"\bby following these steps\b",
        r"\byou can successfully\b",
        r"\bthe following steps\b",
        r"\bhere are the steps\b",
        r"\bthese steps\b",
    ]
    return any(re.search(pattern, normalized) for pattern in generic_patterns)


def _subtask_distinguishing_terms(subtasks: List[Tuple[str, str]]) -> Dict[Tuple[str, str], set]:
    generic_tokens = {
        "data",
        "model",
        "models",
        "source",
        "sources",
        "table",
        "tables",
        "field",
        "fields",
        "step",
        "steps",
    }
    token_counts: Counter = Counter()
    token_sets: Dict[Tuple[str, str], set] = {}

    for subtask in subtasks:
        _, object_phrase = subtask
        tokens = {token for token in _tokenize_normalized(object_phrase) if token not in generic_tokens}
        token_sets[subtask] = tokens
        token_counts.update(tokens)

    distinguishing: Dict[Tuple[str, str], set] = {}
    for subtask, tokens in token_sets.items():
        unique_tokens = {token for token in tokens if token_counts[token] == 1}
        distinguishing[subtask] = unique_tokens or tokens

    return distinguishing


def _segment_mentions_multiple_procedural_subtasks(
    segment: str,
    distinguishing_terms: Dict[Tuple[str, str], set],
) -> bool:
    normalized_tokens = set(_tokenize_normalized(segment))
    if not normalized_tokens:
        return False

    matched_subtasks = 0
    for terms in distinguishing_terms.values():
        if terms and (terms & normalized_tokens):
            matched_subtasks += 1
            if matched_subtasks >= 2:
                return True
    return False


def _segment_supports_subtask(
    action: str,
    object_phrase: str,
    segment: str,
    strict: bool = False,
    distinguishing_terms: Optional[Dict[Tuple[str, str], set]] = None,
) -> bool:
    normalized_segment = re.sub(r"\s+", " ", str(segment or "").strip())
    if not normalized_segment:
        return False

    subtask_text = f"{action} {object_phrase}".strip()
    specificity = _procedural_task_specificity_score(subtask_text, normalized_segment)
    alignment = _procedural_alignment_score(subtask_text, normalized_segment)
    overlap = _lexical_overlap_ratio(object_phrase, normalized_segment)
    local_overlap = _best_local_overlap_ratio(object_phrase, normalized_segment)
    exact_object = re.search(
        r"\b" + r"\s+".join(re.escape(part) for part in object_phrase.split()) + r"\b",
        normalized_segment.lower(),
    ) is not None

    strong_signal = (
        specificity >= 3.2
        or (alignment >= 2.2 and max(overlap, local_overlap) >= 0.48)
        or (exact_object and specificity >= 1.8)
    )
    if not strict:
        return strong_signal or local_overlap >= 0.62

    if _is_generic_procedural_scaffolding_segment(normalized_segment):
        return False
    if distinguishing_terms and _segment_mentions_multiple_procedural_subtasks(normalized_segment, distinguishing_terms):
        return specificity >= 4.2 or (alignment >= 3.0 and exact_object)
    return strong_signal


def _subtask_coverage_details(question: str, text: str, strict: bool = False) -> Dict[str, Any]:
    subtasks = _extract_procedural_subtasks(question, max_subtasks=6)
    if not subtasks or not text:
        return {
            "subtask_total": len(subtasks),
            "covered_subtasks": [],
            "coverage_count": 0,
            "coverage_ratio": 0.0,
        }

    combined_text = str(text or "")
    segments = _split_text_into_relevance_segments(combined_text)
    distinguishing_terms = _subtask_distinguishing_terms(subtasks) if strict else None
    covered: List[Tuple[str, str]] = []
    for action, object_phrase in subtasks:
        if any(
            _segment_supports_subtask(
                action,
                object_phrase,
                segment,
                strict=strict,
                distinguishing_terms=distinguishing_terms,
            )
            for segment in segments
        ):
            covered.append((action, object_phrase))
            continue

        if strict:
            continue

        score = _procedural_task_specificity_score(f"{action} {object_phrase}", combined_text)
        overlap = _lexical_overlap_ratio(object_phrase, combined_text)
        local_overlap = _best_local_overlap_ratio(object_phrase, combined_text)
        exact_object = re.search(
            r"\b" + r"\s+".join(re.escape(part) for part in object_phrase.split()) + r"\b",
            combined_text.lower(),
        ) is not None
        if score >= 2.0 or (exact_object and max(overlap, local_overlap) >= 0.28) or local_overlap >= 0.46:
            covered.append((action, object_phrase))

    coverage_ratio = (len(covered) / max(1, len(subtasks))) if subtasks else 0.0
    return {
        "subtask_total": len(subtasks),
        "covered_subtasks": covered,
        "coverage_count": len(covered),
        "coverage_ratio": round(coverage_ratio, 4),
    }


def _subtask_coverage_score(question: str, text: str) -> float:
    details = _subtask_coverage_details(question, text)
    subtask_total = int(details.get("subtask_total") or 0)
    coverage_count = int(details.get("coverage_count") or 0)
    coverage_ratio = float(details.get("coverage_ratio") or 0.0)
    if subtask_total <= 1:
        return 0.0
    return min(6.0, (coverage_count * 1.8) + (coverage_ratio * 2.6))


def _object_phrase_overlap_ratio(left: str, right: str) -> float:
    left_tokens = set(_tokenize_normalized(left))
    right_tokens = set(_tokenize_normalized(right))
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / max(1, len(left_tokens))


def _best_local_overlap_ratio(question: str, text: str, max_segments: int = 80) -> float:
    if not question or not text:
        return 0.0

    segments = [
        segment.strip()
        for segment in re.split(r"[\n\r]+|(?<=[\.;:!?])\s+", str(text or ""))
        if segment and segment.strip()
    ]
    best = 0.0
    for segment in segments[:max_segments]:
        overlap = _lexical_overlap_ratio(question, segment)
        if overlap > best:
            best = overlap
            if best >= 0.95:
                break
    return best


def _procedural_alignment_score(question: str, text: str) -> float:
    if not _question_has_procedural_intent(question) or not text:
        return 0.0

    targets = _extract_action_object_targets(question)
    if not targets:
        return 0.0

    compact_text = re.sub(r"\s+", " ", re.sub(r"[^a-z0-9_\-\s]", " ", str(text or "").lower())).strip()
    if not compact_text:
        return 0.0

    filler_group = r"(?:a|an|the|new|another|other|more|additional|existing|selected|target|current)"
    nominal_forms = {
        "create": ["create", "creates", "created", "creating", "creation"],
        "add": ["add", "adds", "added", "adding", "addition"],
        "configure": ["configure", "configures", "configured", "configuring", "configuration"],
        "setup": ["setup", "set up", "setting up"],
        "set up": ["setup", "set up", "setting up"],
        "edit": ["edit", "edits", "edited", "editing"],
        "update": ["update", "updates", "updated", "updating"],
        "delete": ["delete", "deletes", "deleted", "deleting", "deletion"],
        "remove": ["remove", "removes", "removed", "removing", "removal"],
        "install": ["install", "installs", "installed", "installing", "installation"],
        "enable": ["enable", "enables", "enabled", "enabling", "enablement"],
        "disable": ["disable", "disables", "disabled", "disabling"],
        "fix": ["fix", "fixes", "fixed", "fixing", "resolution"],
        "resolve": ["resolve", "resolves", "resolved", "resolving", "resolution"],
    }

    score = 0.0
    for action, object_phrase in targets:
        object_pattern = r"\b" + r"\s+".join(re.escape(part) for part in object_phrase.split()) + r"\b"
        action_forms = nominal_forms.get(action, [action])

        direct_patterns = [
            rf"\b{re.escape(action_form)}\b(?:\s+{filler_group}){{0,3}}\s+{object_pattern}"
            for action_form in action_forms
        ]
        nominal_patterns = [
            rf"{object_pattern}(?:\s+{filler_group}){{0,2}}\s+\b{re.escape(action_form)}\b"
            for action_form in action_forms
        ]

        has_direct_alignment = any(re.search(pattern, compact_text) for pattern in direct_patterns)
        has_nominal_alignment = any(re.search(pattern, compact_text) for pattern in nominal_patterns)
        object_present = re.search(object_pattern, compact_text) is not None

        if has_direct_alignment:
            score += 3.2
            continue
        if has_nominal_alignment:
            score += 1.6
            continue
        if object_present:
            score -= 1.4

    return max(-4.0, min(score, 6.0))


def _procedural_task_specificity_score(question: str, text: str) -> float:
    if not _question_has_procedural_intent(question) or not text:
        return 0.0

    question_targets = _extract_action_object_targets(question, max_targets=5)
    if not question_targets:
        return 0.0

    candidate_text = str(text or "")
    compact_text = re.sub(r"\s+", " ", re.sub(r"[^a-z0-9_\-\s]", " ", candidate_text.lower())).strip()
    if not compact_text:
        return 0.0

    candidate_targets = _extract_action_object_targets(candidate_text, max_targets=8)
    text_tokens = set(_tokenize_normalized(compact_text))
    score = 0.0

    for action, object_phrase in question_targets:
        object_tokens = set(_tokenize_normalized(object_phrase))
        if not object_tokens:
            continue

        same_action_targets = [candidate_object for candidate_action, candidate_object in candidate_targets if candidate_action == action]
        best_overlap = 0.0
        for candidate_object in same_action_targets:
            best_overlap = max(best_overlap, _object_phrase_overlap_ratio(object_phrase, candidate_object))

        object_coverage = len(object_tokens & text_tokens) / max(1, len(object_tokens))
        exact_object_pattern = r"\b" + r"\s+".join(re.escape(part) for part in object_phrase.split()) + r"\b"
        exact_object_match = re.search(exact_object_pattern, compact_text) is not None

        if exact_object_match and best_overlap >= 0.6:
            score += 4.5
            continue
        if best_overlap >= 0.8:
            score += 3.8
            continue
        if best_overlap >= 0.5:
            score += 1.8
            continue
        if object_coverage >= 0.8:
            score += 1.2
            continue

        if same_action_targets:
            score -= 4.2
            continue

        if len(object_tokens) >= 2 and object_coverage < 0.4:
            score -= 1.8

    return max(-8.0, min(score, 8.0))


def _filter_low_context_source_candidates(question: str, candidates: List[dict], max_sources: int = 6) -> List[dict]:
    if not candidates:
        return []

    question_is_procedural = _question_has_procedural_intent(question)
    has_action_targets = bool(_extract_action_object_targets(question))
    top_score = max(0.01, float(candidates[0].get("score") or 0.01))
    top_task_specificity = max(float(candidate.get("task_specificity") or 0.0) for candidate in candidates)
    filtered: List[dict] = []

    for idx, candidate in enumerate(candidates):
        if idx == 0:
            filtered.append(candidate)
            continue

        score = float(candidate.get("score") or 0.0)
        overlap_ratio = float(candidate.get("overlap_ratio") or 0.0)
        title_overlap = float(candidate.get("title_overlap") or 0.0)
        local_overlap_ratio = float(candidate.get("local_overlap_ratio") or 0.0)
        phrase_hits = int(candidate.get("phrase_hits") or 0)
        procedural_alignment = float(candidate.get("procedural_alignment") or 0.0)
        task_specificity = float(candidate.get("task_specificity") or 0.0)

        should_keep = True
        if question_is_procedural and has_action_targets:
            if procedural_alignment <= -0.5 and phrase_hits == 0 and local_overlap_ratio < 0.34 and task_specificity < 0.6:
                should_keep = False
            if should_keep and top_task_specificity >= 2.5:
                if task_specificity < 0.6 and phrase_hits == 0 and title_overlap < 0.18 and local_overlap_ratio < 0.3:
                    should_keep = False
            if should_keep:
                if phrase_hits == 0 and task_specificity < 0.2 and title_overlap < 0.08 and overlap_ratio < 0.12 and local_overlap_ratio < 0.18:
                    should_keep = False
        if should_keep and question_is_procedural:
            if score < (top_score * 0.45) and max(overlap_ratio, title_overlap, local_overlap_ratio) < 0.26 and phrase_hits == 0:
                should_keep = False
        elif should_keep:
            if score < (top_score * 0.35) and max(overlap_ratio, title_overlap, local_overlap_ratio) < 0.16 and phrase_hits == 0:
                should_keep = False

        if should_keep:
            filtered.append(candidate)
        if len(filtered) >= max_sources:
            break

    return filtered[:max_sources]


def lexical_boost_score(question: str, doc: str, meta: dict) -> float:
    """
    Simple, general-purpose lexical score.
    Avoid domain-specific or collection-specific biases; reward token overlap only.
    """
    if doc is None:
        doc = ""
    
    q = (question or "").lower()
    d = (doc or "").lower()
    source = str(meta.get("source", "")).lower()
    score = 0.0

    # Normalized overlap reward with light stemming for singular/plural variants.
    q_tokens = set(_tokenize_normalized(q))
    d_tokens = set(_tokenize_normalized(d))
    matched = len(q_tokens & d_tokens)
    if matched > 0:
        score += min(4.0, matched * 0.65)

    # Exact key phrase match is a strong relevance signal for long manuals.
    key_phrases = _extract_key_phrases(q)
    phrase_hits = 0
    for phrase in key_phrases:
        if phrase in d:
            phrase_hits += 1
    if phrase_hits > 0:
        score += min(3.0, phrase_hits * 1.2)

    normalized_question = _normalize_compact_text(q)
    normalized_doc = _normalize_compact_text(d)
    if normalized_question and normalized_doc:
        if normalized_question in normalized_doc:
            score += 6.0
        elif len(normalized_question) >= 24:
            question_terms = normalized_question.split()
            for size in range(min(6, len(question_terms)), 2, -1):
                spans = [" ".join(question_terms[i:i + size]) for i in range(0, len(question_terms) - size + 1)]
                if any(span and span in normalized_doc for span in spans):
                    score += min(4.0, size * 0.7)
                    break

    # Prioritize chunks where heading lines contain query terms.
    heading_hits = 0
    heading_lines = re.findall(r"(?m)^\s*(?:\d+(?:\.\d+)*\.?\s+)?[^\n]{3,120}$", d)
    if heading_lines and q_tokens:
        for line in heading_lines[:10]:
            line_tokens = set(_tokenize_normalized(line))
            if line_tokens and len(q_tokens & line_tokens) >= 2:
                heading_hits += 1
    if heading_hits > 0:
        score += min(2.0, heading_hits * 0.8)

    score += _entity_fact_signal_score(question, f"{source}\n{d}")
    score += _procedural_task_specificity_score(question, f"{source}\n{d}") * 0.45
    score += _source_solution_preference_adjustment(question, source=source, text=d) * 0.4
    
    # Source name match
    for tok in q_tokens:
        if tok in source:
            score += 1.0
    
    return score


def _content_similarity(text1: str, text2: str) -> float:
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
    max_chunks_per_source: int = 5,
) -> Tuple[List[str], List[dict], List[float], List[str]]:
    """
    Intelligent deduplication:
    1. Removes near-duplicate documents (content similarity > threshold)
    2. Limits chunks per source while allowing more for comprehensive topics
    3. Prefers diverse sources for better context
    4. Adaptive thresholds based on document characteristics
    
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
        source_key = source  # Use full source as key
        max_allowed = max_chunks_per_source
        if _is_priority_document(source, meta):
            max_allowed = max_chunks_per_source * 3
        
        # Check if we've already included max chunks from this source
        if source_key in source_chunk_count and source_chunk_count[source_key] >= max_allowed:
            print(f"[DEDUP] Skipping doc {idx} (source={source_key} reached max={max_allowed})")
            continue
        
        # Check for content similarity with already selected docs
        is_duplicate = False
        doc_len = len(doc.split())
        
        for seen_doc in seen_contents:
            seen_len = len(seen_doc.split())
            # For very short docs (<50 words), use stricter threshold; for long docs, more lenient
            adaptive_threshold = similarity_threshold
            if doc_len < 50 or seen_len < 50:
                adaptive_threshold = 0.75  # Stricter for short snippets
            elif doc_len > 500 or seen_len > 500:
                adaptive_threshold = 0.60  # More lenient for comprehensive docs
            
            sim = _content_similarity(doc, seen_doc)
            if sim > adaptive_threshold:
                print(f"[DEDUP] Skipping doc {idx} (similarity={sim:.3f} > {adaptive_threshold:.3f})")
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
        meta = m or {}
        s = lexical_boost_score(question, d, m)
        dist = None if distances is None or idx >= len(distances) else distances[idx]
        idv = None if ids is None or idx >= len(ids) else ids[idx]
        items.append({
            "doc": d,
            "meta": meta,
            "score": s,
            "idx": idx,
            "dist": dist,
            "id": idv,
        })

    if all(it["score"] == 0 for it in items):
        print("[RERANK] All scores=0 → sorting by vector distance (balanced across collections)")
        # Still print a summary of results
        for it in items[:10]:
            print(f"[RERANK] src={it['meta'].get('source')} chunk={it['meta'].get('chunk')} id={it['id']} dist={it['dist']}")

        items.sort(key=lambda x: ((x["dist"] if x["dist"] is not None else 999.0), x["idx"]))
        
        # Even with 0 score, apply deduplication
        reranked_docs = [it["doc"] for it in items]
        reranked_metas = [it["meta"] for it in items]
        reranked_distances = [it["dist"] for it in items]
        reranked_ids = [it["id"] for it in items]
        return _smart_deduplicate_and_diversify(reranked_docs, reranked_metas, reranked_distances, reranked_ids)

    items.sort(
        key=lambda x: (
            -x["score"],
            (x["dist"] if x["dist"] is not None else 999.0),
            x["idx"],
        )
    )

    # Safeguard for very specific questions: keep the strongest lexical-overlap chunks first.
    overlap_ranked = sorted(
        items,
        key=lambda x: _lexical_overlap_ratio(question, x["doc"]),
        reverse=True,
    )
    pinned = [it for it in overlap_ranked[:4] if _lexical_overlap_ratio(question, it["doc"]) >= 0.18]
    if pinned:
        pinned_ids = {it["id"] for it in pinned}
        items = pinned + [it for it in items if it["id"] not in pinned_ids]

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
    q_tokens = set(_tokenize_normalized(str(question)))
    d_tokens = set(_tokenize_normalized(str(doc)))
    if not q_tokens or not d_tokens:
        return 0.0
    inter = len(q_tokens & d_tokens)
    return inter / max(1, len(q_tokens))


def _is_short_query(question: str) -> bool:
    """Detect if query is short (likely needs lenient matching)."""
    word_count = len(question.strip().split())
    return word_count <= 8


def _extract_query_keywords(question: str, max_terms: int = 8) -> List[str]:
    """Extract compact keyword terms from a user question for fallback retrieval."""
    if not question:
        return []
    stopwords = {
        "the", "is", "are", "a", "an", "and", "or", "to", "of", "in", "on", "for", "with", "by",
        "from", "as", "at", "be", "this", "that", "these", "those", "it", "its", "if", "then",
        "how", "what", "when", "where", "why", "who", "can", "could", "should", "would", "do",
        "does", "did", "i", "we", "you", "they", "he", "she", "my", "our", "your", "their",
        "about", "into", "through", "using", "use", "want", "need", "like", "please",
    }
    tokens = re.findall(r"[a-zA-Z0-9_\-]+", question.lower())
    ranked = [t for t in tokens if len(t) > 2 and t not in stopwords]
    seen = set()
    deduped = []
    for term in ranked:
        if term in seen:
            continue
        seen.add(term)
        deduped.append(term)
        if len(deduped) >= max_terms:
            break
    return deduped


def _build_fallback_query_variants(question: str) -> List[str]:
    """Build generic fallback variants for broader recall across any topic."""
    if not question:
        return []
    variants: List[str] = []
    base = question.strip()
    if base:
        variants.append(base)

    normalized = _normalize_question(base)
    if normalized and normalized not in variants:
        variants.append(normalized)

    # Split compound questions into smaller clauses for better retrieval hit rate
    clauses = re.split(r"\?|\.|,|\band\b|\bthen\b|\balso\b", base, flags=re.IGNORECASE)
    for clause in clauses:
        c = clause.strip()
        if len(c.split()) >= 2 and c not in variants:
            variants.append(c)

    keywords = _extract_query_keywords(base)
    if keywords:
        keyword_query = " ".join(keywords)
        if keyword_query and keyword_query not in variants:
            variants.append(keyword_query)

    return variants[:6]


def _context_confidence_profile(
    question: str,
    docs: List[str],
    distances: Optional[List[float]],
) -> dict:
    """Compute topic-agnostic retrieval confidence from semantic and lexical signals."""
    if not docs:
        return {
            "confidence": 0.0,
            "best_distance": None,
            "max_overlap": 0.0,
            "is_short": _is_short_query(question),
        }

    best_distance = min(distances) if distances else None
    top_docs = [d for d in docs[:5] if d]
    max_overlap = max((_lexical_overlap_ratio(question, d) for d in top_docs), default=0.0)

    # Distance score: lower distance => higher confidence
    if best_distance is None:
        distance_score = 0.35
    else:
        distance_score = 1.0 - min(max(best_distance, 0.0), 0.95) / 0.95

    # Overlap score saturates once overlap is reasonably meaningful
    overlap_score = min(max_overlap / 0.22, 1.0)

    # Blend scores with slight leniency for short follow-up style questions
    is_short = _is_short_query(question)
    confidence = (0.7 * distance_score) + (0.3 * overlap_score)
    if is_short:
        confidence = max(confidence, 0.45 * distance_score + 0.55 * overlap_score)

    return {
        "confidence": round(max(0.0, min(1.0, confidence)), 4),
        "best_distance": best_distance,
        "max_overlap": round(max_overlap, 4),
        "is_short": is_short,
    }


def _ground_answer_against_context(question: str, context_text: str, draft_answer: str) -> str:
    """
    Universal anti-hallucination guard.
    Rewrites the draft so final output only contains claims supported by provided context.
    """
    if not draft_answer:
        return ""
    if not OPENAI_API_KEY:
        return draft_answer

    if not context_text or not context_text.strip():
        return (
            "I couldn’t find enough verified information in the current knowledge base context to answer this reliably. "
            "Please share more specific details or add the relevant documentation so I can answer precisely."
        )

    grounding_prompt = (
        "You are a strict grounding and factuality verifier for a RAG assistant.\n\n"
        "TASK:\n"
        "Rewrite the draft answer so EVERY factual claim is directly supported by the provided context.\n"
        "If a claim is not supported, remove it.\n"
        "If critical details are missing, explicitly say they are not present in the available knowledge context.\n"
        "If the available context is about adjacent or different topics, do not summarize those topics as if they answer the question.\n"
        "When no directly relevant procedure or detail is present, say that no directly relevant document was found in the current knowledge context.\n"
        "Do not invent commands, paths, settings, UI labels, API names, or product behavior.\n"
        "Do not use outside knowledge.\n"
        "Keep the response helpful and concise.\n"
        "Ask at most one focused follow-up question if needed.\n\n"
        f"QUESTION:\n{question}\n\n"
        f"CONTEXT:\n{context_text}\n\n"
        f"DRAFT ANSWER:\n{draft_answer}\n\n"
        "RETURN ONLY THE FINAL REWRITTEN ANSWER."
    )

    try:
        grounded = call_llm(grounding_prompt, temperature=0.0)
        grounded = (grounded or "").strip()
        return grounded if grounded else draft_answer
    except Exception as e:
        print(f"[API][CHAT][WARN] Grounding verification failed: {e}")
        return draft_answer


def _normalize_history_messages(raw_messages: Optional[List[Dict[str, Any]]]) -> List[Dict[str, str]]:
    """Normalize user-provided history messages to role/content pairs."""
    if not raw_messages:
        return []
    normalized: List[Dict[str, str]] = []
    for msg in raw_messages:
        role = str((msg or {}).get("role") or "").strip().lower()
        content = str((msg or {}).get("content") or "").strip()
        if role not in {"user", "assistant"} or not content:
            continue
        normalized.append({"role": role, "content": content})
    return normalized


def _format_history_for_prompt(messages: List[Dict[str, str]], max_messages: int = 8) -> str:
    """Format recent conversation history for retrieval and prompt context."""
    if not messages:
        return ""
    tail = messages[-max_messages:]
    lines: List[str] = []
    for msg in tail:
        role = "User" if msg.get("role") == "user" else "Assistant"
        lines.append(f"{role}: {msg.get('content', '')}")
    return "\n".join(lines)


def _question_looks_like_followup(question: str) -> bool:
    candidate = str(question or "").strip().lower()
    if not candidate:
        return False

    followup_starters = (
        "and ", "also ", "what about", "how about", "why ", "then ", "so ",
        "can you elaborate", "can you explain more", "tell me more", "continue",
        "based on that", "for that", "for this", "regarding that", "regarding this",
    )
    if candidate.startswith(followup_starters):
        return True

    referential_patterns = [
        r"\bthat\b",
        r"\bthis\b",
        r"\bthese\b",
        r"\bthose\b",
        r"\bit\b",
        r"\bthey\b",
        r"\bthem\b",
        r"\bthe previous\b",
        r"\bthe last\b",
        r"\bearlier\b",
        r"\babove\b",
        r"\bbefore\b",
    ]
    short_question = len(candidate) <= 120
    if short_question and any(re.search(pattern, candidate) for pattern in referential_patterns):
        return True

    # Standalone questions with explicit nouns/topics should not inherit prior context.
    return False


def _should_use_history_for_question(
    question: str,
    stored_history: List[Dict[str, str]],
    explicit_is_followup: bool = False,
) -> bool:
    if not stored_history:
        return False

    if _question_looks_like_followup(question):
        return True

    if not explicit_is_followup:
        return False

    if _question_has_entity_fact_intent(question) or _question_requests_broad_coverage(question):
        return False

    explicit_topic_tokens = [
        token for token in _tokenize_normalized(question)
        if token not in _LEXICAL_STOPWORDS and token not in {"how", "step", "steps", "way", "ways", "method", "methods"}
    ]
    return len(explicit_topic_tokens) < 3


_GENERIC_ANCHOR_TERMS = {
    "ticket", "issue", "problem", "error", "bug", "case", "item", "thing", "things", "one", "ones",
    "service", "system", "module", "component", "file", "document", "doc", "guide", "article",
    "log", "attachment", "image", "screenshot", "request", "record", "row", "column", "field",
    "setting", "settings", "configuration", "config", "workflow", "task", "job", "result", "answer",
}

_REFERENTIAL_ANCHOR_PATTERNS = [
    r"\bthis\b",
    r"\bthat\b",
    r"\bthese\b",
    r"\bthose\b",
    r"\bit\b",
    r"\bthey\b",
    r"\bthem\b",
    r"\bcurrent\b",
    r"\bselected\b",
    r"\bprevious\b",
    r"\blast\b",
    r"\bearlier\b",
    r"\bsame\b",
    r"\babove\b",
    r"\bbefore\b",
    r"\bwhich one\b",
    r"\bwhat about\b",
    r"\bhow about\b",
]


def _topic_bearing_tokens(question: str) -> List[str]:
    generic_fillers = _GENERIC_ANCHOR_TERMS | {
        "how", "what", "why", "which", "where", "when", "who", "tell", "show", "explain", "help",
        "solve", "fix", "use", "used", "using", "refer", "refers", "referred", "talk", "talking",
        "mean", "means", "meant", "about", "last", "previous", "current", "selected", "exact",
    }
    tokens: List[str] = []
    for token in _tokenize_normalized(question):
        if not token or token in _LEXICAL_STOPWORDS or token in generic_fillers or token.isdigit():
            continue
        tokens.append(token)
    return tokens


def _question_needs_anchor(question: str) -> bool:
    candidate = str(question or "").strip().lower()
    if not candidate:
        return False

    has_referential_language = any(re.search(pattern, candidate) for pattern in _REFERENTIAL_ANCHOR_PATTERNS)
    if not has_referential_language:
        return False

    topic_tokens = _topic_bearing_tokens(candidate)
    return len(topic_tokens) < 2


def _question_requests_previous_answer_source(question: str) -> bool:
    candidate = str(question or "").strip().lower()
    if not candidate:
        return False

    patterns = [
        r"\bwhich\s+(ticket|source|document|doc|guide|file|case|issue|item)\b.*\b(referring to|refer to|talking about|used|meant)",
        r"\bwhat\s+(ticket|source|document|doc|guide|file|case|issue|item)\b.*\b(referring to|refer to|talking about|used|meant)",
        r"\bwhat are you referring to\b",
        r"\bwhat do you mean\b",
        r"\bwhich one are you talking about\b",
        r"\bwhat was your source\b",
        r"\bwhich source did you use\b",
        r"\bwhere did that come from\b",
    ]
    return any(re.search(pattern, candidate) for pattern in patterns)


def _generate_llm_meta_response(question: str, scenario: str, facts: List[str]) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not configured; cannot generate chat response.")

    fact_block = "\n".join(f"- {fact}" for fact in facts if str(fact or "").strip()) or "- No additional facts provided."
    prompt = (
        "You are a grounded support assistant replying directly to the user.\n"
        "Generate the user-facing answer using ONLY the facts below.\n"
        "Do not invent details, hidden reasoning, sources, or context.\n"
        "Do not mention prompts, policies, internal state, retrieval, or chain-of-thought.\n"
        "Keep the answer concise, natural, and actionable.\n"
        "If the facts indicate missing context, clearly say what is missing and ask for the exact item needed.\n"
        "If the facts identify prior grounding sources, explain them plainly and specifically.\n\n"
        f"Scenario: {scenario}\n"
        f"User question: {question}\n\n"
        f"Facts:\n{fact_block}\n\n"
        "Return only the final answer to the user."
    )
    return (call_llm(prompt, temperature=0.1) or "").strip()


def _build_anchor_clarification_answer(question: str) -> str:
    candidate = str(question or "").lower()
    target_label = "subject"
    for token in (
        "ticket", "issue", "problem", "service", "file", "document", "guide", "log", "attachment",
        "image", "screenshot", "request", "record", "row", "column", "field", "configuration",
    ):
        if re.search(rf"\b{re.escape(token)}s?\b", candidate):
            target_label = token
            break

    facts = [
        "The current user question is referential or ambiguous.",
        "There is no active grounding anchor from a selected ticket, uploaded file, or grounded prior answer.",
    ]
    if target_label == "subject":
        facts.append("The missing anchor is a specific subject, item, document, component, or context.")
    else:
        facts.append(f"The missing anchor is the exact {target_label} the user means.")
        facts.append(f"The user can clarify by naming the exact {target_label}, selecting it in the UI, or restating the question with that subject.")
    return _generate_llm_meta_response(question, "missing-anchor", facts)


def _humanize_conversation_source(source: str) -> str:
    raw_source = str(source or "").strip()
    if not raw_source:
        return ""

    if raw_source.startswith("azure-devops:"):
        match = re.search(r"azure-devops:(\d+)", raw_source)
        if match:
            return f"selected Azure DevOps ticket {match.group(1)}"
        return "selected Azure DevOps ticket"

    learn_match = re.search(r"(?:^|::)ado:learn:(\d+)", raw_source)
    if learn_match:
        return f"knowledge-base ticket {learn_match.group(1)}"

    compact = raw_source.split(" (", 1)[0]
    if "::" in compact:
        compact = compact.split("::", 1)[1]
    return _display_source_name(compact)


def _build_previous_answer_source_answer(question: str, conversation_state: Optional[dict]) -> str:
    state = dict(conversation_state or {})
    sources = [str(item).strip() for item in list(state.get("sources") or []) if str(item).strip()]
    selected_ticket_id = state.get("selected_ticket_id")
    used_selected_ticket = bool(state.get("used_selected_ticket"))
    facts: List[str] = ["The user is asking what grounded my previous answer."]

    if used_selected_ticket and selected_ticket_id:
        facts.append(f"The selected Azure DevOps ticket {selected_ticket_id} was used as grounding context.")
        supplemental = [source for source in sources if not str(source).startswith("azure-devops:")]
        if supplemental:
            formatted = [_humanize_conversation_source(source) for source in supplemental[:3]]
            facts.append("Supplemental grounding sources were: " + ", ".join(formatted) + ".")
        return _generate_llm_meta_response(question, "previous-answer-source", facts)

    if sources:
        formatted_sources = [_humanize_conversation_source(source) for source in sources[:4]]
        if len(formatted_sources) == 1:
            facts.append(f"There was one recorded grounding source: {formatted_sources[0]}.")
        else:
            facts.append("Recorded grounding sources were: " + ", ".join(formatted_sources) + ".")
        return _generate_llm_meta_response(question, "previous-answer-source", facts)

    facts.append("There is no specific grounded source recorded for the previous answer.")
    facts.append("Ask the user to provide the exact subject, select the relevant item, or restate the question with explicit context.")
    return _generate_llm_meta_response(question, "previous-answer-source", facts)


def _store_conversation_turn(
    conversation_key: str,
    question: str,
    answer: str,
    *,
    sources: Optional[List[str]] = None,
    selected_ticket_id: Optional[int] = None,
    selected_ticket_url: Optional[str] = None,
    used_selected_ticket: bool = False,
    used_file_context: bool = False,
) -> None:
    try:
        conversation_store[conversation_key].append({"role": "user", "content": question})
        conversation_store[conversation_key].append({"role": "assistant", "content": answer})
        conversation_state_store[conversation_key] = {
            "sources": list(sources or []),
            "selected_ticket_id": selected_ticket_id,
            "selected_ticket_url": selected_ticket_url,
            "used_selected_ticket": bool(used_selected_ticket),
            "used_file_context": bool(used_file_context),
            "has_grounded_sources": bool(sources),
            "updated_at": datetime.utcnow().isoformat() + "Z",
        }
    except Exception as exc:
        print(f"[API][CHAT][WARN] Failed to persist conversation context/state: {exc}")


def _question_requires_specifics(question: str) -> bool:
    """Detect questions that require explicit, concrete details instead of generic guidance."""
    if not question:
        return False
    q = question.lower()
    patterns = [
        r"\bwhich\b",
        r"\bwhat exact\b",
        r"\bexactly\b",
        r"\blist\b",
        r"\bshow\b",
        r"\bcolumn(s)?\b",
        r"\bfield(s)?\b",
        r"\bheader(s)?\b",
        r"\bparameter(s)?\b",
        r"\bproperty|properties\b",
        r"\bstep(s)?\b",
        r"\bcommand(s)?\b",
        r"\bpath(s)?\b",
        r"\bname(s)?\b",
        r"\bhow many\b",
        r"\bcount\b",
    ]
    return any(re.search(p, q) for p in patterns)


def _enforce_specific_grounded_answer(question: str, context_text: str, answer: str) -> str:
    """
    If the question asks for concrete details, force the answer to be explicit and context-grounded.
    """
    if not answer or not OPENAI_API_KEY:
        return answer
    if not _question_requires_specifics(question):
        return answer

    prompt = (
        "You are a strict response quality checker for a RAG assistant.\n\n"
        "Goal: ensure the final answer is concrete, specific, and grounded in context.\n"
        "Rules:\n"
        "1) Keep only details supported by CONTEXT.\n"
        "2) If user asks for explicit lists (columns/fields/steps/commands/etc), provide explicit bullet list.\n"
        "2.1) If the context explicitly lists items and the user asks how many, count only those explicit items and state the count plus the item names.\n"
        "2.2) If the question asks for multiple requested actions, objects, or subtasks, address every requested part that is supported by CONTEXT.\n"
        "2.3) Never answer only one requested part while ignoring the others. If CONTEXT covers only some parts, explicitly state which parts are covered and which are missing.\n"
        "3) If exact details are missing in CONTEXT, explicitly say which exact details are missing.\n"
        "4) Do not output vague placeholders like 'necessary columns' when specifics are available.\n"
        "5) Never invent values, names, paths, or commands.\n\n"
        f"QUESTION:\n{question}\n\n"
        f"CONTEXT:\n{context_text}\n\n"
        f"CURRENT ANSWER:\n{answer}\n\n"
        "Return ONLY the improved final answer."
    )
    try:
        improved = call_llm(prompt, temperature=0.0)
        improved = (improved or "").strip()
        return improved if improved else answer
    except Exception as e:
        print(f"[API][CHAT][WARN] Specificity enforcement failed: {e}")
        return answer


def _format_subtask_label(action: str, object_phrase: str) -> str:
    return re.sub(r"\s+", " ", f"{action} {object_phrase}").strip()


def _llm_ensure_answer_completeness(question: str, context_text: str, answer: str) -> str:
    """
    Single LLM pass that checks whether the answer covers ALL parts of the question
    that are supported by the retrieved context. If not, it rewrites the answer to
    include the missing parts. This replaces complex heuristic subtask parsing with
    natural language understanding.
    """
    if not answer or not OPENAI_API_KEY or not context_text:
        return answer

    prompt = (
        "You are a completeness checker for a grounded RAG assistant.\n\n"
        "TASK: Check whether the CURRENT ANSWER fully covers every part of the QUESTION "
        "that is supported by the CONTEXT. If it does, return the answer unchanged. "
        "If any part of the question is answered by the CONTEXT but missing from the CURRENT ANSWER, "
        "rewrite the answer to include ALL covered parts with their full details.\n\n"
        "RULES:\n"
        "1) If the question asks about multiple actions or objects (e.g., 'create entities AND relations'), "
        "each one must have its own dedicated section with full step-by-step details from CONTEXT.\n"
        "2) A passing mention or a single sentence about a topic does NOT count as coverage. "
        "If CONTEXT has a full procedure section (with steps, fields, SQL, config), include it fully.\n"
        "3) Keep ONLY details supported by CONTEXT. Do not invent.\n"
        "4) If CONTEXT does not support some requested part, explicitly say that part is missing.\n"
        "5) Preserve all correct details already in the CURRENT ANSWER.\n"
        "6) Return ONLY the final complete answer.\n\n"
        f"QUESTION:\n{question}\n\n"
        f"CONTEXT:\n{context_text}\n\n"
        f"CURRENT ANSWER:\n{answer}\n"
    )
    try:
        improved = call_llm(prompt, temperature=0.0)
        improved = (improved or "").strip()
        if improved and len(improved) >= len(answer) * 0.5:
            return improved
        return answer
    except Exception as e:
        print(f"[API][CHAT][WARN] Completeness check failed: {e}")
        return answer


def _llm_verify_answer_relevance(question: str, context_text: str, answer: str) -> str:
    """
    Final LLM gate: verify the answer actually addresses the specific question.
    If the retrieved documents are about adjacent/related topics but do NOT contain
    information that directly answers the question, replace the answer with an honest
    'not found' message instead of fabricating steps from loosely related content.
    """
    if not answer or not OPENAI_API_KEY or not context_text:
        return answer

    prompt = (
        "You are a strict relevance judge for a RAG assistant.\n\n"
        "TASK: Decide whether the ANSWER below genuinely answers the specific QUESTION asked, "
        "using information that is directly present in CONTEXT.\n\n"
        "CRITERIA FOR REJECTION:\n"
        "- The answer describes a DIFFERENT procedure or topic than what was asked, even if it is related.\n"
        "- The answer assembles vaguely related fragments into fabricated steps that are not explicitly described in CONTEXT.\n"
        "- The CONTEXT contains information about a related but different concept, and the answer pretends it answers the question.\n"
        "- Key terms from the question do not appear in substantive procedural detail in CONTEXT.\n\n"
        "CRITERIA FOR ACCEPTANCE:\n"
        "- The CONTEXT contains a direct explanation, procedure, or factual answer to the specific question.\n"
        "- The answer accurately reflects what CONTEXT says about the specific topic asked.\n\n"
        "OUTPUT:\n"
        "- If the answer is RELEVANT and accurate: return it UNCHANGED.\n"
        "- If the answer is NOT genuinely answering the question: return a helpful message that says:\n"
        "  1) The current knowledge base does not contain a direct answer to this specific question.\n"
        "  2) Briefly mention what related topics WERE found (1-2 sentences max).\n"
        "  3) Suggest the user add the relevant documentation or rephrase their question.\n\n"
        f"QUESTION:\n{question}\n\n"
        f"CONTEXT:\n{context_text[:6000]}\n\n"
        f"ANSWER:\n{answer}\n\n"
        "Return ONLY the final answer text."
    )
    try:
        result = call_llm(prompt, temperature=0.0)
        result = (result or "").strip()
        if result:
            return result
        return answer
    except Exception as e:
        print(f"[API][CHAT][WARN] Relevance verification failed: {e}")
        return answer


def _looks_like_noncode_fenced_block(language: str, content: str) -> bool:
    lang = str(language or "").strip().lower()

    lines = [line.rstrip() for line in str(content or "").strip().splitlines() if line.strip()]
    if not lines:
        return False

    # Even for "code" languages like bash/shell, detect blocks that are purely
    # UI/navigation instructions disguised as code comments (no real commands).
    if lang in {"bash", "sh", "shell", "zsh", "powershell", "ps1"}:
        _real_cmd_count = 0
        _ui_comment_count = 0
        for _ln in lines:
            _stripped = _ln.strip()
            # Lines that are actual commands (not comments)
            if _stripped and not re.match(r"^\s*#", _stripped):
                _real_cmd_count += 1
            elif re.match(r"^\s*#", _stripped):
                _body = re.sub(r"^\s*#\s*", "", _stripped)
                if re.search(
                    r"\b(click|select|open|navigate|button|tab|screen|ui|portainer|"
                    r"admin studio|field|dropdown|checkbox|page|section|restart|restarting|"
                    r"service|clearing|browser|cache|setting|menu|dialog|typically|usually|"
                    r"involves|done through|via the|this can|you can|access)\b",
                    _body, re.IGNORECASE,
                ):
                    _ui_comment_count += 1
        # If there are NO real commands and at least some UI comments, it's not code
        if _real_cmd_count == 0 and _ui_comment_count > 0:
            return True
        # If it has real commands, keep it as code
        return False

    if lang in {"python", "py", "sql", "json", "yaml", "yml", "xml", "javascript", "js", "typescript", "ts", "html", "css", "ini", "toml", "diff", "dockerfile"}:
        return False
    if not lines:
        return False

    code_like_count = sum(1 for line in lines if _looks_like_command_or_code_line(line))
    ui_like_count = sum(
        1
        for line in lines
        if re.search(r"\b(click|select|open|navigate|button|tab|screen|ui|portainer|admin studio|field|dropdown|checkbox|page|section)\b", line, re.IGNORECASE)
    )
    key_value_count = sum(1 for line in lines if re.match(r"^[A-Za-z][A-Za-z0-9_ /()-]{1,40}:\s+.+$", line))

    if code_like_count == 0 and (ui_like_count > 0 or key_value_count > 0):
        return True
    if code_like_count <= max(1, len(lines) // 4) and lang in {"", "text", "plaintext", "plain", "md", "markdown"}:
        return True
    return False


def _normalize_noncode_fenced_blocks(answer: str) -> str:
    if not answer or "```" not in answer:
        return answer

    pattern = re.compile(r"```([A-Za-z0-9_+-]*)\n([\s\S]*?)```", re.MULTILINE)

    def _replace(match: re.Match) -> str:
        language = match.group(1) or ""
        content = (match.group(2) or "").strip("\n")
        if not _looks_like_noncode_fenced_block(language, content):
            return match.group(0)

        lines = [line.strip() for line in content.splitlines() if line.strip()]
        if not lines:
            return ""
        # Strip leading # from comment-only lines (UI instructions that were in bash blocks)
        cleaned = []
        for line in lines:
            stripped = re.sub(r"^\s*#\s*", "", line).strip()
            cleaned.append(stripped if stripped else line)
        if all(re.match(r"^[A-Za-z][A-Za-z0-9_ /()-]{1,40}:\s+.+$", cl) for cl in cleaned):
            return "\n".join(f"- {cl}" for cl in cleaned)
        return "  \n".join(cleaned)

    return pattern.sub(_replace, answer)


def _get_vector_collection(collection_name: str):
    normalized_name = (collection_name or "").strip()
    if normalized_name == COLLECTION_NAME:
        return collection
    if normalized_name == MEMORY_COLLECTION_NAME:
        return memory_collection
    raise HTTPException(status_code=400, detail=f"Unknown collection: {collection_name}")


def _vector_collection_description(collection_name: str) -> str:
    if collection_name == COLLECTION_NAME:
        return "Wiki + User Guide + Old Tickets Summeries"
    if collection_name == MEMORY_COLLECTION_NAME:
        return "New User Knowledge"
    return "Vector collection"


def _safe_embedding_to_list(embedding: Any) -> List[float]:
    if embedding is None:
        return []
    if hasattr(embedding, "tolist"):
        embedding = embedding.tolist()
    return [float(value) for value in embedding]


def _display_source_name(source: str) -> str:
    source_text = str(source or "").strip()
    if not source_text:
        return "Untitled document"
    return os.path.basename(unquote(source_text)) or source_text


def _normalize_vector_input_type(value: Any) -> Optional[str]:
    normalized = str(value or "").strip().lower()
    if normalized in {"file", "upload", "uploaded_file", "uploaded-file"}:
        return "file"
    if normalized in {"free_text", "free-text", "text", "content", "manual"}:
        return "free_text"
    return None


def _looks_like_uploaded_file_content(text: str) -> bool:
    normalized_text = str(text or "").strip()
    if not normalized_text:
        return False
    if "---FILE SEPARATOR---" in normalized_text:
        return True
    if re.search(r"(?m)^\*\*File:\s*.+?\*\*(?:\s*\(.+?\))?$", normalized_text):
        return True
    if re.search(r"(?mi)^\[Image Content from .+\]$", normalized_text):
        return True
    return bool(re.search(r"(?i)\.(pdf|docx?|xlsx?|csv|png|jpe?g|gif|webp|txt|md)\b", normalized_text[:240]))


def _get_tokenizer_encoding():
    if not HAS_TIKTOKEN:
        return None

    for model_name in (OPENAI_EMBEDDING_MODEL, OPENAI_CHAT_MODEL):
        try:
            return tiktoken.encoding_for_model(model_name)
        except KeyError:
            continue

    return tiktoken.get_encoding("cl100k_base")


def _infer_vector_document_input_type(collection_name: str, source: str, items: List[dict], merged_content: str) -> Optional[str]:
    if collection_name != MEMORY_COLLECTION_NAME:
        return None

    seed_meta = dict((items[0].get("metadata") if items else {}) or {})
    is_user_knowledge = str(seed_meta.get("collection") or "").strip().lower() == "user_knowledge" or str(source or "").startswith("user:content:")
    if not is_user_knowledge:
        return None

    for item in items:
        safe_meta = item.get("metadata") or {}
        explicit_type = _normalize_vector_input_type(safe_meta.get("input_type") or safe_meta.get("source_type"))
        if explicit_type == "file":
            return explicit_type
        if explicit_type == "free_text" and not _looks_like_uploaded_file_content(merged_content):
            return explicit_type

    return "file" if _looks_like_uploaded_file_content(merged_content) else "free_text"


def _extract_document_heading(text: str) -> str:
    if not text:
        return ""
    for raw_line in text.splitlines()[:10]:
        line = raw_line.strip()
        if not line:
            continue
        file_match = re.match(r"^\*\*File:\s*(.+?)\*\*$", line)
        if file_match:
            return file_match.group(1).strip()
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return ""


def _build_document_title(source: str, first_chunk_text: str) -> str:
    heading = _extract_document_heading(first_chunk_text)
    return heading or _display_source_name(source)


def _find_chunk_overlap(existing_text: str, next_chunk: str, max_overlap: int = CHUNK_OVERLAP) -> int:
    if not existing_text or not next_chunk:
        return 0
    max_len = min(max_overlap, len(existing_text), len(next_chunk))
    for overlap_size in range(max_len, 0, -1):
        if existing_text.endswith(next_chunk[:overlap_size]):
            return overlap_size
    return 0


def _merge_chunk_texts(chunks: List[str], max_chars: Optional[int] = None) -> str:
    if not chunks:
        return ""
    merged_parts: List[str] = []
    merged_length = 0
    merged_tail = ""

    for chunk in chunks:
        if not chunk:
            continue

        if not merged_parts:
            piece = chunk
        else:
            overlap_size = _find_chunk_overlap(merged_tail, chunk)
            piece = chunk[overlap_size:]

        if not piece:
            continue

        if max_chars is not None:
            remaining = max_chars - merged_length
            if remaining <= 0:
                break
            if len(piece) > remaining:
                piece = piece[:remaining]

        merged_parts.append(piece)
        merged_length += len(piece)
        merged_tail = (merged_tail + piece)[-CHUNK_OVERLAP:]

        if max_chars is not None and merged_length >= max_chars:
            break

    return "".join(merged_parts)


def _build_chunk_boundaries(rows: List[dict], preview_chars: int = 72) -> List[dict]:
    boundaries: List[dict] = []
    merged_length = 0
    merged_tail = ""

    for row in rows:
        chunk_text = row.get("content") or ""
        chunk_number = int(row.get("chunk", 0) or 0)
        if not chunk_text:
            boundaries.append(
                {
                    "chunk": chunk_number,
                    "start_position": merged_length,
                    "end_position": merged_length,
                    "visible_length": 0,
                    "original_length": 0,
                    "start_preview": "",
                    "end_preview": "",
                }
            )
            continue

        if not boundaries:
            overlap_size = 0
            visible_text = chunk_text
        else:
            overlap_size = _find_chunk_overlap(merged_tail, chunk_text)
            visible_text = chunk_text[overlap_size:]

        visible_length = len(visible_text)
        start_position = merged_length + 1 if visible_length > 0 else merged_length
        end_position = merged_length + visible_length

        start_preview = visible_text[:preview_chars].strip()
        end_preview = visible_text[-preview_chars:].strip() if visible_text else ""

        boundaries.append(
            {
                "chunk": chunk_number,
                "start_position": start_position,
                "end_position": end_position,
                "visible_length": visible_length,
                "original_length": len(chunk_text),
                "overlap_trimmed": overlap_size,
                "start_preview": start_preview,
                "end_preview": end_preview,
            }
        )

        if not visible_text:
            continue

        merged_length += visible_length
        merged_tail = (merged_tail + visible_text)[-CHUNK_OVERLAP:]

    return boundaries


def _vector_chunk_page_bounds(limit: int, offset: int) -> Tuple[int, int]:
    safe_limit = max(1, min(int(limit), VECTOR_DB_MAX_CHUNK_LIMIT))
    safe_offset = max(0, int(offset))
    return safe_limit, safe_offset


def _get_sorted_document_rows(
    collection_name: str,
    source: str,
    include_embeddings: bool = False,
) -> List[dict]:
    target_collection = _get_vector_collection(collection_name)
    include_fields = ["documents", "metadatas"]
    if include_embeddings:
        include_fields.append("embeddings")

    raw = target_collection.get(where={"source": source}, include=include_fields)
    ids = list(raw.get("ids", []) or [])
    docs = list(raw.get("documents", []) or [])
    metas = list(raw.get("metadatas", []) or [])
    embeddings = list(raw.get("embeddings", []) or []) if include_embeddings else []

    rows: List[dict] = []
    for idx, (doc_id, doc_text, meta) in enumerate(zip(ids, docs, metas)):
        safe_meta = meta or {}
        rows.append(
            {
                "id": doc_id,
                "chunk": int(safe_meta.get("chunk", 0) or 0),
                "content": doc_text or "",
                "metadata": safe_meta,
                "embedding": embeddings[idx] if include_embeddings and idx < len(embeddings) else None,
            }
        )

    rows.sort(key=lambda item: item["chunk"])
    return rows


def _build_chunk_page(rows: List[dict], limit: int, offset: int, include_embeddings: bool = False) -> Tuple[List[dict], int, int]:
    safe_limit, safe_offset = _vector_chunk_page_bounds(limit, offset)
    page_rows = rows[safe_offset:safe_offset + safe_limit]
    chunk_items: List[dict] = []
    for row in page_rows:
        chunk_items.append(
            {
                "id": row["id"],
                "chunk": row["chunk"],
                "content": row["content"],
                "metadata": row["metadata"],
                "embedding": _safe_embedding_to_list(row.get("embedding")) if include_embeddings else None,
                "embedding_loaded": bool(include_embeddings),
            }
        )
    return chunk_items, safe_limit, safe_offset


def _count_collection_documents(collection_name: str) -> int:
    target_collection = _get_vector_collection(collection_name)
    raw = target_collection.get(include=["metadatas"])
    sources = {
        str((meta or {}).get("source") or "").strip()
        for meta in list(raw.get("metadatas", []) or [])
        if str((meta or {}).get("source") or "").strip()
    }
    return len(sources)


def _count_text_tokens(text: str) -> int:
    raw_text = str(text or "")
    if not raw_text:
        return 0

    encoding = _get_tokenizer_encoding()
    if encoding is None:
        raise RuntimeError("tiktoken is required for exact token counting")

    return len(encoding.encode(raw_text, disallowed_special=()))


def _estimate_text_tokens(text: str) -> int:
    raw_text = str(text or "")
    if not raw_text:
        return 0
    try:
        return _count_text_tokens(raw_text)
    except Exception:
        return max(1, len(raw_text) // 4)


def _truncate_text_to_token_budget(text: str, max_tokens: int, label: str) -> str:
    raw_text = str(text or "")
    if not raw_text or max_tokens <= 0:
        return ""

    current_tokens = _estimate_text_tokens(raw_text)
    if current_tokens <= max_tokens:
        return raw_text

    notice = (
        f"\n\n[TRUNCATED {label}: original_tokens={current_tokens}, kept_tokens={max_tokens}]\n\n"
    )
    encoding = _get_tokenizer_encoding()
    if encoding is not None:
        encoded = encoding.encode(raw_text, disallowed_special=())
        head_count = max_tokens // 2
        tail_count = max_tokens - head_count
        if len(encoded) <= max_tokens:
            return raw_text
        head_text = encoding.decode(encoded[:head_count]).strip()
        tail_text = encoding.decode(encoded[-tail_count:]).strip() if tail_count > 0 else ""
        merged = head_text
        if tail_text:
            merged = f"{head_text}{notice}{tail_text}"
        return merged.strip()

    approx_chars = max_tokens * 4
    head_chars = approx_chars // 2
    tail_chars = approx_chars - head_chars
    head_text = raw_text[:head_chars].strip()
    tail_text = raw_text[-tail_chars:].strip() if tail_chars > 0 else ""
    merged = head_text
    if tail_text:
        merged = f"{head_text}{notice}{tail_text}"
    return merged.strip()


def _fit_prompt_to_model_budget(
    question: str,
    combined_context: str,
    foundational_instruction: str = "",
    ta9_instruction: str = "",
) -> Tuple[str, str]:
    prompt = _build_system_prompt(
        question=question,
        combined_context=combined_context,
        foundational_instruction=foundational_instruction,
        ta9_instruction=ta9_instruction,
    )
    prompt_tokens = _estimate_text_tokens(prompt)
    if prompt_tokens <= LLM_MAX_INPUT_TOKENS:
        return prompt, combined_context

    context_tokens = _estimate_text_tokens(combined_context)
    overflow_tokens = prompt_tokens - LLM_MAX_INPUT_TOKENS
    target_context_tokens = max(4000, context_tokens - overflow_tokens - 1024)
    trimmed_context = _truncate_text_to_token_budget(
        combined_context,
        target_context_tokens,
        "combined context for final LLM input",
    )
    prompt = _build_system_prompt(
        question=question,
        combined_context=trimmed_context,
        foundational_instruction=foundational_instruction,
        ta9_instruction=ta9_instruction,
    )

    second_pass_tokens = _estimate_text_tokens(prompt)
    if second_pass_tokens > LLM_MAX_INPUT_TOKENS:
        second_overflow = second_pass_tokens - LLM_MAX_INPUT_TOKENS
        second_budget = max(2000, target_context_tokens - second_overflow - 1024)
        trimmed_context = _truncate_text_to_token_budget(
            trimmed_context,
            second_budget,
            "combined context for final LLM input",
        )
        prompt = _build_system_prompt(
            question=question,
            combined_context=trimmed_context,
            foundational_instruction=foundational_instruction,
            ta9_instruction=ta9_instruction,
        )

    final_prompt_tokens = _estimate_text_tokens(prompt)
    if final_prompt_tokens > LLM_MAX_INPUT_TOKENS:
        print(
            f"[API][CHAT][WARN] Prompt is still larger than the model budget after trimming: "
            f"tokens={final_prompt_tokens} budget={LLM_MAX_INPUT_TOKENS}"
        )
    else:
        print(
            f"[API][CHAT] Prompt fitted to model budget: tokens={final_prompt_tokens} budget={LLM_MAX_INPUT_TOKENS}"
        )
    return prompt, trimmed_context


def _estimate_rows_token_count(rows: List[dict]) -> int:
    # Fast approximation for huge documents: avoids expensive tokenizer passes.
    return sum(len(str((row or {}).get("content") or "")) // 4 for row in rows)


def _count_collection_tokens(collection_name: str) -> int:
    summaries = _group_collection_documents(collection_name)
    return sum(int(item.get("token_count", 0) or 0) for item in summaries)


def _group_collection_documents(collection_name: str) -> List[dict]:
    target_collection = _get_vector_collection(collection_name)
    raw = target_collection.get(include=["metadatas", "documents"])
    ids = list(raw.get("ids", []) or [])
    docs = list(raw.get("documents", []) or [])
    metas = list(raw.get("metadatas", []) or [])

    grouped: Dict[str, dict] = {}
    for doc_id, doc_text, meta in zip(ids, docs, metas):
        safe_meta = meta or {}
        source = str(safe_meta.get("source") or doc_id or "")
        chunk_index = int(safe_meta.get("chunk", 0) or 0)
        entry = grouped.setdefault(
            source,
            {
                "source": source,
                "items": [],
                "updated_at": "",
            },
        )
        entry["items"].append(
            {
                "id": doc_id,
                "chunk": chunk_index,
                "document": doc_text or "",
                "metadata": safe_meta,
            }
        )

        candidate_timestamp = str(
            safe_meta.get("edited_at")
            or safe_meta.get("uploaded_at")
            or safe_meta.get("created_at")
            or ""
        )
        if candidate_timestamp and candidate_timestamp > entry["updated_at"]:
            entry["updated_at"] = candidate_timestamp

    summaries: List[dict] = []
    for source, payload in grouped.items():
        items = sorted(payload["items"], key=lambda item: item["chunk"])
        merged_content = _merge_chunk_texts([item["document"] for item in items])
        preview = re.sub(r"\s+", " ", merged_content).strip()
        if len(preview) > VECTOR_DB_PREVIEW_CHARS:
            preview = preview[:VECTOR_DB_PREVIEW_CHARS].rstrip() + "..."
        title = _build_document_title(source, items[0]["document"] if items else "")
        input_type = _infer_vector_document_input_type(collection_name, source, items, merged_content)
        summaries.append(
            {
                "source": source,
                "title": title,
                "display_source": _display_source_name(source),
                "preview": preview,
                "chunk_count": len(items),
                "token_count": _count_text_tokens(merged_content),
                "input_type": input_type,
                "updated_at": payload["updated_at"] or None,
                "_search_content": merged_content,
            }
        )

    summaries.sort(key=lambda item: ((item["updated_at"] or ""), item["title"].lower()), reverse=True)
    return summaries


def _normalize_vector_search_value(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "").lower()).strip()


def _build_vector_search_preview(content: str, query: str, fallback_preview: str) -> str:
    text = re.sub(r"\s+", " ", str(content or "")).strip()
    if not text:
        return fallback_preview

    raw_query = str(query or "").strip().lower()
    normalized_terms = [term for term in _tokenize_normalized(query) if term]
    lower_text = text.lower()

    hit_index = -1
    if raw_query:
        hit_index = lower_text.find(raw_query)
    if hit_index < 0:
        for term in normalized_terms:
            hit_index = lower_text.find(term.lower())
            if hit_index >= 0:
                break

    if hit_index < 0:
        return fallback_preview or (text[:VECTOR_DB_PREVIEW_CHARS].rstrip() + "..." if len(text) > VECTOR_DB_PREVIEW_CHARS else text)

    window = max(80, VECTOR_DB_PREVIEW_CHARS // 2)
    start = max(0, hit_index - window)
    end = min(len(text), hit_index + window)
    snippet = text[start:end].strip()

    if start > 0:
        snippet = "..." + snippet
    if end < len(text):
        snippet = snippet + "..."
    return snippet


def _score_vector_document_summary(item: dict, query: str) -> Optional[dict]:
    query_text = str(query or "").strip()
    normalized_query = _normalize_vector_search_value(query_text)
    query_terms = [term for term in _tokenize_normalized(query_text) if term]
    if not normalized_query and not query_terms:
        return None

    title = str(item.get("title") or "")
    source = str(item.get("source") or "")
    display_source = str(item.get("display_source") or "")
    search_content = str(item.get("_search_content") or "")

    title_normalized = _normalize_vector_search_value(title)
    source_normalized = _normalize_vector_search_value(f"{display_source} {source}")
    content_normalized = _normalize_vector_search_value(search_content)

    title_terms = set(_tokenize_normalized(title))
    source_terms = set(_tokenize_normalized(f"{display_source} {source}"))
    content_terms = set(_tokenize_normalized(search_content))
    combined_terms = title_terms | source_terms | content_terms

    matched_terms = [term for term in query_terms if term in combined_terms]
    if normalized_query:
        exact_in_title = normalized_query in title_normalized
        exact_in_source = normalized_query in source_normalized
        exact_in_content = normalized_query in content_normalized
    else:
        exact_in_title = False
        exact_in_source = False
        exact_in_content = False

    has_any_match = exact_in_title or exact_in_source or exact_in_content or bool(matched_terms)
    if not has_any_match:
        return None

    all_terms_matched = bool(query_terms) and len(matched_terms) == len(query_terms)
    score = 0.0

    if exact_in_title:
        score += 220.0
    if exact_in_source:
        score += 170.0
    if exact_in_content:
        score += 120.0

    title_term_hits = sum(1 for term in query_terms if term in title_terms)
    source_term_hits = sum(1 for term in query_terms if term in source_terms)
    content_term_hits = sum(1 for term in query_terms if term in content_terms)

    score += title_term_hits * 40.0
    score += source_term_hits * 24.0
    score += content_term_hits * 12.0

    if all_terms_matched:
        score += 90.0
    elif query_terms:
        score += (len(matched_terms) / len(query_terms)) * 25.0

    preview = _build_vector_search_preview(search_content, query_text, str(item.get("preview") or ""))
    return {
        "score": score,
        "all_terms_matched": all_terms_matched,
        "preview": preview,
    }


def _build_vector_document_detail(
    collection_name: str,
    source: str,
    chunk_limit: int = VECTOR_DB_DEFAULT_CHUNK_LIMIT,
    chunk_offset: int = 0,
    include_embeddings: bool = False,
    include_full_content: bool = True,
) -> dict:
    rows = _get_sorted_document_rows(
        collection_name,
        source,
        include_embeddings=include_embeddings,
    )
    if not rows:
        raise HTTPException(status_code=404, detail="Document not found")

    chunk_items, safe_limit, safe_offset = _build_chunk_page(
        rows,
        limit=chunk_limit,
        offset=chunk_offset,
        include_embeddings=include_embeddings,
    )
    chunk_boundaries = _build_chunk_boundaries(rows)
    merged_content: Optional[str] = None
    cached_payload: Optional[dict] = None
    if include_full_content:
        cached_payload = _get_cached_vector_document_payload(collection_name, source)
        if cached_payload is not None:
            merged_content = str(cached_payload.get("full_content") or "")
        else:
            merged_content = _merge_chunk_texts([row["content"] for row in rows])
    full_content = merged_content if include_full_content else None
    if merged_content is not None:
        if cached_payload is not None:
            token_count = int(cached_payload.get("token_count") or 0)
        else:
            token_count = _count_text_tokens(merged_content)
            _store_cached_vector_document_payload(collection_name, source, merged_content, token_count)
    else:
        token_count = _estimate_rows_token_count(rows)
    title = _build_document_title(source, rows[0]["content"] if rows else "")
    input_type = _infer_vector_document_input_type(
        collection_name,
        source,
        [{"metadata": row["metadata"]} for row in rows],
        merged_content or "",
    )
    updated_at = None
    for row in rows:
        safe_meta = row["metadata"] or {}
        candidate_timestamp = safe_meta.get("edited_at") or safe_meta.get("uploaded_at") or safe_meta.get("created_at")
        if candidate_timestamp and (updated_at is None or str(candidate_timestamp) > str(updated_at)):
            updated_at = str(candidate_timestamp)

    return {
        "collection_name": collection_name,
        "collection_description": _vector_collection_description(collection_name),
        "source": source,
        "title": title,
        "display_source": _display_source_name(source),
        "chunk_count": len(rows),
        "token_count": token_count,
        "input_type": input_type,
        "updated_at": updated_at,
        "full_content": full_content,
        "chunk_boundaries": chunk_boundaries,
        "chunk_limit": safe_limit,
        "chunk_offset": safe_offset,
        "chunk_has_more": safe_offset + safe_limit < len(rows),
        "chunks": chunk_items,
    }


def _build_updated_chunk_records(source: str, content: str, existing_metas: List[dict]) -> Tuple[List[str], List[str], List[dict], List[List[float]]]:
    clean_content = (content or "").strip()
    if not clean_content:
        raise HTTPException(status_code=400, detail="content is empty")

    seed_meta = dict((existing_metas or [{}])[0] or {})
    base_meta = {
        key: value
        for key, value in seed_meta.items()
        if key not in {"chunk", "chunk_type", "table_page", "table_index", "table_row_index"}
    }
    base_meta["source"] = source
    base_meta["edited_at"] = datetime.utcnow().isoformat() + "Z"

    if str(base_meta.get("collection") or "").strip().lower() == "user_knowledge" or str(source or "").startswith("user:content:"):
        current_input_type = _normalize_vector_input_type(base_meta.get("input_type"))
        if current_input_type != "file" and _looks_like_uploaded_file_content(clean_content):
            base_meta["input_type"] = "file"
        elif current_input_type is None:
            base_meta["input_type"] = "free_text"

    chunks = (
        chunk_text_preserve_table_rows(clean_content)
        if TABLE_ROW_START_TAG in clean_content or base_meta.get("input_type") == "file"
        else chunk_text(clean_content)
    )
    if not chunks:
        raise HTTPException(status_code=400, detail="No chunks generated from content")

    ids_to_add: List[str] = []
    docs_to_add: List[str] = []
    metas_to_add: List[dict] = []
    embeddings_to_add: List[List[float]] = []

    for chunk_index, chunk_text_value in enumerate(chunks):
        embedding = embed_text(chunk_text_value)
        chunk_meta = dict(base_meta)
        chunk_meta["chunk"] = chunk_index
        if chunk_text_value.startswith(TABLE_ROW_START_TAG):
            chunk_meta["chunk_type"] = "table_row"
            chunk_meta.update(extract_table_row_metadata(chunk_text_value))
        else:
            chunk_meta["chunk_type"] = "text"
        ids_to_add.append(str(uuid.uuid4()))
        docs_to_add.append(chunk_text_value)
        metas_to_add.append(chunk_meta)
        embeddings_to_add.append(embedding)

    return ids_to_add, docs_to_add, metas_to_add, embeddings_to_add


def _resolve_collection_name_from_meta(meta: Optional[dict]) -> str:
    label = str((meta or {}).get("collection") or "").strip().lower()
    if label == "user_knowledge":
        return MEMORY_COLLECTION_NAME
    return COLLECTION_NAME


def _count_procedural_markers(text: str) -> int:
    candidate = str(text or "")
    if not candidate:
        return 0

    markers = 0
    if re.search(r"(?mi)^\s*step\s*\d+", candidate):
        markers += 3
    if re.search(r"(?mi)^\s*\d+\.\s+", candidate):
        markers += 2
    if re.search(r"(?i)\b(step-by-step|procedure|instructions?|configure|configuration|setup|set up)\b", candidate):
        markers += 1
    return markers


def _count_exact_phrase_hits(question: str, text: str) -> int:
    if not question or not text:
        return 0
    lowered_text = str(text or "").lower()
    hits = 0
    for phrase in _extract_key_phrases(question, max_phrases=8):
        if phrase and phrase in lowered_text:
            hits += 1
    normalized_question = _normalize_compact_text(question)
    normalized_text = _normalize_compact_text(text)
    if normalized_question and normalized_text and normalized_question in normalized_text:
        hits += 3
    return hits


def _is_priority_document(source: str, meta: Optional[dict] = None) -> bool:
    """Check if a document is a priority document that should be boosted in search."""
    if meta and str(meta.get("priority", "")).strip().lower() == "user_upload":
        return True
    return str(source or "").lower().startswith("user:content:")


def _is_generic_source_title(title: str, source: str = "") -> bool:
    candidate = f"{title} {source}".lower()
    generic_markers = [
        "user guide", "user-guide", "manual", "overview", "general", "introduction",
        "getting started", "guide", "documentation",
    ]
    return any(marker in candidate for marker in generic_markers)


def _build_source_context_candidates(
    question: str,
    docs: List[str],
    metas: List[dict],
    distances: Optional[List[float]] = None,
    ids: Optional[List[str]] = None,
    max_sources: int = 6,
) -> List[dict]:
    if not docs:
        return []

    grouped: Dict[Tuple[str, str], dict] = {}
    for idx, (doc, meta) in enumerate(zip(docs, metas)):
        safe_meta = meta or {}
        source = str(safe_meta.get("source") or "").strip()
        if not source or not doc:
            continue

        collection_name = _resolve_collection_name_from_meta(safe_meta)
        key = (collection_name, source)
        distance = None if distances is None or idx >= len(distances) else distances[idx]
        chunk_score = lexical_boost_score(question, doc, safe_meta)
        overlap_score = _lexical_overlap_ratio(question, doc) * 5.0
        position_bonus = max(0.0, 3.0 - (idx * 0.12))
        distance_bonus = 0.0 if distance is None else max(0.0, 1.5 - (float(distance) * 3.0))

        entry = grouped.setdefault(
            key,
            {
                "collection_name": collection_name,
                "source": source,
                "best_distance": distance,
                "chunk_signal_scores": [],
                "seed_meta": safe_meta,
                "matched_chunk_ids": [],
            },
        )
        entry["chunk_signal_scores"].append(chunk_score + overlap_score + position_bonus + distance_bonus)
        if distance is not None and (entry["best_distance"] is None or float(distance) < float(entry["best_distance"])):
            entry["best_distance"] = distance
        if ids is not None and idx < len(ids) and ids[idx] is not None:
            entry["matched_chunk_ids"].append(ids[idx])

    if not grouped:
        return []

    question_is_procedural = _question_has_procedural_intent(question)
    entity_fact_intent = _question_has_entity_fact_intent(question)
    broad_coverage_intent = _question_requests_broad_coverage(question)
    prelim_ranked = sorted(
        grouped.values(),
        key=lambda item: (
            -sum(sorted(item["chunk_signal_scores"], reverse=True)[:3]),
            (item["best_distance"] if item["best_distance"] is not None else 999.0),
        ),
    )[: max(max_sources * 2, 8)]

    source_candidates: List[dict] = []
    for entry in prelim_ranked:
        try:
            rows = _get_sorted_document_rows(entry["collection_name"], entry["source"], include_embeddings=False)
        except Exception as exc:
            print(
                f"[SOURCE_RERANK][WARN] Failed to load source={entry['source']} "
                f"collection={entry['collection_name']}: {exc}"
            )
            continue

        if not rows:
            continue

        full_content = _merge_chunk_texts([row["content"] for row in rows])
        excerpt_limit = 3200 if broad_coverage_intent else (2600 if question_is_procedural else 1800)
        if _is_priority_document(entry["source"], entry.get("seed_meta")):
            excerpt_limit = max(excerpt_limit, 4000)
        excerpt = _merge_chunk_texts([row["content"] for row in rows], max_chars=excerpt_limit)
        seed_meta = rows[0]["metadata"] or entry["seed_meta"]
        top_chunk_signals = sorted(entry.get("chunk_signal_scores") or [0.0], reverse=True)[:3]
        chunk_signal_strength = sum(top_chunk_signals)
        if entity_fact_intent:
            chunk_signal_strength = min(chunk_signal_strength, 7.5)
        overlap_ratio = _lexical_overlap_ratio(question, full_content)
        local_overlap_ratio = _best_local_overlap_ratio(question, full_content)
        lexical_score = lexical_boost_score(question, full_content, seed_meta)
        title = _build_document_title(entry["source"], rows[0]["content"] if rows else "")
        entity_fact_bonus = _entity_fact_signal_score(question, f"{title}\n{full_content}")
        broad_coverage_bonus = _broad_coverage_signal_score(question, f"{title}\n{full_content}")
        procedural_alignment = _procedural_alignment_score(question, f"{title}\n{full_content}")
        procedural_markers = _count_procedural_markers(full_content)
        procedural_bonus = min(4.0, procedural_markers * 0.8) if question_is_procedural else 0.0
        title_overlap = _lexical_overlap_ratio(question, title)
        source_overlap = _lexical_overlap_ratio(question, entry["source"])
        phrase_hits = _count_exact_phrase_hits(question, f"{title}\n{full_content}")
        coverage_details = _subtask_coverage_details(question, f"{title}\n{full_content}")
        subtask_coverage_bonus = _subtask_coverage_score(question, f"{title}\n{full_content}")
        is_priority = _is_priority_document(entry["source"], entry.get("seed_meta"))
        chunk_count_penalty = min(6.0, math.log(max(1, len(rows)), 2) * 0.9) if len(rows) > 8 else 0.0
        if is_priority:
            chunk_count_penalty = min(chunk_count_penalty, 1.0)
        if entity_fact_intent and len(rows) > 4:
            chunk_count_penalty += min(3.5, math.log(max(1, len(rows)), 2) * 0.9)
            if is_priority:
                chunk_count_penalty = min(chunk_count_penalty, 1.5)
        generic_penalty = 4.5 if question_is_procedural and _is_generic_source_title(title, entry["source"]) and not is_priority else 0.0
        priority_boost = 6.0 if is_priority else 0.0
        compact_fact_bonus = 1.5 if entity_fact_intent and len(rows) <= 3 and entity_fact_bonus > 0 else 0.0
        task_specificity = _procedural_task_specificity_score(question, f"{title}\n{full_content}")
        solution_channel = _classify_source_solution_channel(title=title, source=entry["source"], text=full_content)
        solution_channel_bias = _source_solution_preference_adjustment(
            question,
            title=title,
            source=entry["source"],
            text=full_content,
        )
        source_score = (
            chunk_signal_strength
            + lexical_score
            + entity_fact_bonus
            + broad_coverage_bonus
            + compact_fact_bonus
            + (overlap_ratio * 8.0)
            + (local_overlap_ratio * 6.5)
            + (title_overlap * 5.0)
            + (source_overlap * 4.0)
            + procedural_bonus
            + procedural_alignment
            + task_specificity
            + (phrase_hits * 1.5)
            + subtask_coverage_bonus
            + solution_channel_bias
            + priority_boost
            - chunk_count_penalty
            - generic_penalty
        )

        source_candidates.append(
            {
                "collection_name": entry["collection_name"],
                "source": entry["source"],
                "title": title,
                "full_content": full_content,
                "excerpt": excerpt,
                "chunk_count": len(rows),
                "best_distance": entry["best_distance"],
                "score": round(source_score, 4),
                "source_overlap": round(source_overlap, 4),
                "overlap_ratio": round(overlap_ratio, 4),
                "local_overlap_ratio": round(local_overlap_ratio, 4),
                "title_overlap": round(title_overlap, 4),
                "phrase_hits": phrase_hits,
                "covered_subtasks": list(coverage_details.get("covered_subtasks") or []),
                "subtask_total": int(coverage_details.get("subtask_total") or 0),
                "subtask_coverage_count": int(coverage_details.get("coverage_count") or 0),
                "subtask_coverage_ratio": float(coverage_details.get("coverage_ratio") or 0.0),
                "subtask_coverage_bonus": round(subtask_coverage_bonus, 4),
                "procedural_markers": procedural_markers,
                "procedural_alignment": round(procedural_alignment, 4),
                "task_specificity": round(task_specificity, 4),
                "lexical_score": round(lexical_score, 4),
                "entity_fact_bonus": round(entity_fact_bonus, 4),
                "broad_coverage_bonus": round(broad_coverage_bonus, 4),
                "chunk_signal_strength": round(chunk_signal_strength, 4),
                "chunk_count_penalty": round(chunk_count_penalty, 4),
                "generic_penalty": generic_penalty,
                "priority_boost": priority_boost,
                "is_priority": is_priority,
                "solution_channel": solution_channel,
                "solution_channel_bias": round(solution_channel_bias, 4),
                "matched_chunk_ids": entry["matched_chunk_ids"],
            }
        )

    source_candidates.sort(
        key=lambda item: (
            -item["score"],
            (item["best_distance"] if item["best_distance"] is not None else 999.0),
            item["title"].lower(),
        )
    )

    print("[SOURCE_RERANK] Top source candidates:")
    for candidate in source_candidates[:10]:
        print(
            f"[SOURCE_RERANK] score={candidate['score']:.2f} dist={candidate['best_distance']} "
            f"collection={candidate['collection_name']} source={candidate['source']} chunks={candidate['chunk_count']}"
        )

    return _filter_low_context_source_candidates(question, source_candidates, max_sources=max_sources)


def _build_global_lexical_source_candidates(question: str, max_sources: int = 6) -> List[dict]:
    if not question:
        return []

    question_is_procedural = _question_has_procedural_intent(question)
    entity_fact_intent = _question_has_entity_fact_intent(question)
    broad_coverage_intent = _question_requests_broad_coverage(question)
    collected: List[dict] = []
    for collection_name in sorted((COLLECTION_NAME, MEMORY_COLLECTION_NAME)):
        try:
            target_collection = _get_vector_collection(collection_name)
            raw = target_collection.get(include=["documents", "metadatas"])
        except Exception as exc:
            print(f"[LEXICAL_RESCUE][WARN] Failed to load collection={collection_name}: {exc}")
            continue

        docs = list(raw.get("documents", []) or [])
        metas = list(raw.get("metadatas", []) or [])
        grouped: Dict[str, List[dict]] = {}
        for doc_text, meta in zip(docs, metas):
            safe_meta = meta or {}
            source = str(safe_meta.get("source") or "").strip()
            if not source or not doc_text:
                continue
            grouped.setdefault(source, []).append(
                {
                    "content": doc_text,
                    "chunk": int(safe_meta.get("chunk", 0) or 0),
                    "metadata": safe_meta,
                }
            )

        for source, rows in grouped.items():
            sorted_rows = sorted(rows, key=lambda item: item["chunk"])
            excerpt = _merge_chunk_texts([row["content"] for row in sorted_rows], max_chars=3200)
            if not excerpt:
                continue
            title = _build_document_title(source, sorted_rows[0]["content"] if sorted_rows else "")
            title_overlap = _lexical_overlap_ratio(question, title)
            excerpt_overlap = _lexical_overlap_ratio(question, excerpt)
            local_overlap_ratio = _best_local_overlap_ratio(question, excerpt)
            source_overlap = _lexical_overlap_ratio(question, source)
            lexical_score = lexical_boost_score(question, f"{title}\n{excerpt}", sorted_rows[0]["metadata"])
            entity_fact_bonus = _entity_fact_signal_score(question, f"{title}\n{excerpt}")
            broad_coverage_bonus = _broad_coverage_signal_score(question, f"{title}\n{excerpt}")
            procedural_alignment = _procedural_alignment_score(question, f"{title}\n{excerpt}")
            phrase_hits = _count_exact_phrase_hits(question, f"{title}\n{excerpt}")
            procedural_markers = _count_procedural_markers(excerpt)
            procedural_bonus = min(4.0, procedural_markers * 0.8) if question_is_procedural else 0.0
            coverage_details = _subtask_coverage_details(question, f"{title}\n{excerpt}")
            subtask_coverage_bonus = _subtask_coverage_score(question, f"{title}\n{excerpt}")
            chunk_count_penalty = min(6.0, math.log(max(1, len(sorted_rows)), 2) * 0.9) if len(sorted_rows) > 8 else 0.0
            if entity_fact_intent and len(sorted_rows) > 4:
                chunk_count_penalty += min(3.5, math.log(max(1, len(sorted_rows)), 2) * 0.9)
            generic_penalty = 4.5 if question_is_procedural and _is_generic_source_title(title, source) else 0.0
            compact_fact_bonus = 1.5 if entity_fact_intent and len(sorted_rows) <= 3 and entity_fact_bonus > 0 else 0.0
            task_specificity = _procedural_task_specificity_score(question, f"{title}\n{excerpt}")
            solution_channel = _classify_source_solution_channel(title=title, source=source, text=excerpt)
            solution_channel_bias = _source_solution_preference_adjustment(
                question,
                title=title,
                source=source,
                text=excerpt,
            )
            score = (
                lexical_score
                + entity_fact_bonus
                + broad_coverage_bonus
                + compact_fact_bonus
                + (title_overlap * 7.0)
                + (excerpt_overlap * 8.5)
                + (local_overlap_ratio * 6.0)
                + (source_overlap * 4.0)
                + (phrase_hits * 1.3)
                + procedural_bonus
                + procedural_alignment
                + task_specificity
                + subtask_coverage_bonus
                + solution_channel_bias
                - chunk_count_penalty
                - generic_penalty
            )
            if score <= 0:
                continue

            collected.append(
                {
                    "collection_name": collection_name,
                    "source": source,
                    "title": title,
                    "excerpt": excerpt,
                    "full_content": excerpt,
                    "chunk_count": len(sorted_rows),
                    "best_distance": None,
                    "score": round(score, 4),
                    "source_overlap": round(source_overlap, 4),
                    "overlap_ratio": round(excerpt_overlap, 4),
                    "local_overlap_ratio": round(local_overlap_ratio, 4),
                    "title_overlap": round(title_overlap, 4),
                    "phrase_hits": phrase_hits,
                    "covered_subtasks": list(coverage_details.get("covered_subtasks") or []),
                    "subtask_total": int(coverage_details.get("subtask_total") or 0),
                    "subtask_coverage_count": int(coverage_details.get("coverage_count") or 0),
                    "subtask_coverage_ratio": float(coverage_details.get("coverage_ratio") or 0.0),
                    "subtask_coverage_bonus": round(subtask_coverage_bonus, 4),
                    "procedural_markers": procedural_markers,
                    "procedural_alignment": round(procedural_alignment, 4),
                    "task_specificity": round(task_specificity, 4),
                    "lexical_score": round(lexical_score, 4),
                    "entity_fact_bonus": round(entity_fact_bonus, 4),
                    "broad_coverage_bonus": round(broad_coverage_bonus, 4),
                    "chunk_count_penalty": round(chunk_count_penalty, 4),
                    "generic_penalty": generic_penalty,
                    "solution_channel": solution_channel,
                    "solution_channel_bias": round(solution_channel_bias, 4),
                    "matched_chunk_ids": [],
                    "origin": "lexical_rescue",
                }
            )

    collected.sort(key=lambda item: (-item["score"], item["title"].lower()))
    print("[LEXICAL_RESCUE] Top source candidates:")
    for candidate in collected[:10]:
        print(
            f"[LEXICAL_RESCUE] score={candidate['score']:.2f} collection={candidate['collection_name']} "
            f"source={candidate['source']} chunks={candidate['chunk_count']}"
        )
    return _filter_low_context_source_candidates(question, collected, max_sources=max_sources)


def _merge_source_candidate_lists(*candidate_lists: List[dict], max_sources: int = 6) -> List[dict]:
    merged: Dict[Tuple[str, str], dict] = {}
    for candidate_list in candidate_lists:
        for candidate in candidate_list or []:
            key = (candidate.get("collection_name"), candidate.get("source"))
            if not key[0] or not key[1]:
                continue
            existing = merged.get(key)
            if existing is None:
                merged[key] = dict(candidate)
                continue

            existing["score"] = round(float(existing.get("score") or 0.0) + float(candidate.get("score") or 0.0), 4)
            if existing.get("best_distance") is None and candidate.get("best_distance") is not None:
                existing["best_distance"] = candidate.get("best_distance")
            elif existing.get("best_distance") is not None and candidate.get("best_distance") is not None:
                existing["best_distance"] = min(float(existing.get("best_distance")), float(candidate.get("best_distance")))

            if len(str(candidate.get("full_content") or "")) > len(str(existing.get("full_content") or "")):
                existing["full_content"] = candidate.get("full_content")
            if len(str(candidate.get("excerpt") or "")) > len(str(existing.get("excerpt") or "")):
                existing["excerpt"] = candidate.get("excerpt")

            for field_name in ("overlap_ratio", "local_overlap_ratio", "title_overlap", "source_overlap", "procedural_alignment"):
                existing[field_name] = max(float(existing.get(field_name) or 0.0), float(candidate.get(field_name) or 0.0))
            existing["phrase_hits"] = max(int(existing.get("phrase_hits") or 0), int(candidate.get("phrase_hits") or 0))
            existing["procedural_markers"] = max(int(existing.get("procedural_markers") or 0), int(candidate.get("procedural_markers") or 0))
            existing["task_specificity"] = max(float(existing.get("task_specificity") or 0.0), float(candidate.get("task_specificity") or 0.0))
            existing["subtask_total"] = max(int(existing.get("subtask_total") or 0), int(candidate.get("subtask_total") or 0))
            existing["subtask_coverage_count"] = max(
                int(existing.get("subtask_coverage_count") or 0),
                int(candidate.get("subtask_coverage_count") or 0),
            )
            existing["subtask_coverage_ratio"] = max(
                float(existing.get("subtask_coverage_ratio") or 0.0),
                float(candidate.get("subtask_coverage_ratio") or 0.0),
            )
            existing["subtask_coverage_bonus"] = max(
                float(existing.get("subtask_coverage_bonus") or 0.0),
                float(candidate.get("subtask_coverage_bonus") or 0.0),
            )
            merged_subtasks = list(existing.get("covered_subtasks") or [])
            for subtask in list(candidate.get("covered_subtasks") or []):
                if subtask not in merged_subtasks:
                    merged_subtasks.append(subtask)
            existing["covered_subtasks"] = merged_subtasks

            existing_ids = list(existing.get("matched_chunk_ids") or [])
            for chunk_id in list(candidate.get("matched_chunk_ids") or []):
                if chunk_id not in existing_ids:
                    existing_ids.append(chunk_id)
            existing["matched_chunk_ids"] = existing_ids

            origins = set(filter(None, [existing.get("origin"), candidate.get("origin")]))
            existing["origin"] = ",".join(sorted(origins)) if origins else existing.get("origin")

    ranked = sorted(
        merged.values(),
        key=lambda item: (
            -float(item.get("score") or 0.0),
            (item.get("best_distance") if item.get("best_distance") is not None else 999.0),
            str(item.get("title") or "").lower(),
        ),
    )
    return ranked[:max_sources]


def _llm_select_source_candidates(question: str, candidates: List[dict], max_sources: int = 4) -> List[dict]:
    if not OPENAI_API_KEY or len(candidates) <= 1:
        return candidates[:max_sources]

    shortlist = candidates[: min(6, len(candidates))]
    broad_coverage_intent = _question_requests_broad_coverage(question)
    preferred_channel = _preferred_solution_channel(question)
    requested_subtasks = _extract_procedural_subtasks(question, max_subtasks=6)
    candidate_lines: List[str] = []
    for idx, candidate in enumerate(shortlist, start=1):
        covered_subtask_labels = [
            _format_subtask_label(action, object_phrase)
            for action, object_phrase in list(candidate.get("covered_subtasks") or [])
        ]
        candidate_lines.append(
            f"Candidate {idx}:\n"
            f"Collection: {candidate.get('collection_name')}\n"
            f"Title: {candidate.get('title')}\n"
            f"Source: {candidate.get('source')}\n"
            f"Inferred channel: {candidate.get('solution_channel') or _classify_source_solution_channel(title=str(candidate.get('title') or ''), source=str(candidate.get('source') or ''), text=str(candidate.get('excerpt') or ''))}\n"
            f"Task specificity: {candidate.get('task_specificity')}\n"
            f"Covered subtasks: {', '.join(covered_subtask_labels) if covered_subtask_labels else 'none detected'}\n"
            f"Chunks: {candidate.get('chunk_count')}\n"
            f"Heuristic score: {candidate.get('score')}\n"
            f"Excerpt:\n{str(candidate.get('excerpt') or '')[:2200]}"
        )

    candidates_block = "\n\n".join(candidate_lines)

    selector_prompt = (
        "You are a retrieval ranking specialist for a RAG system.\n"
        "Pick the document candidates that best answer the user question.\n"
        "Prefer candidates that directly contain the exact procedure, exact configuration steps, exact field names, or exact command/config examples asked for.\n"
        "Exact task match is more important than source style preference. Never replace the asked task with an adjacent task that shares some words.\n"
        "For naming, company/product identity, alias, or count/list questions, prefer candidates that explicitly define or enumerate those facts, even if they are shorter than broad manuals.\n"
        "Reject adjacent-task candidates that share vocabulary with the question but answer a different action, object, target, or scope.\n"
        "If two candidates are about related topics, prefer the one whose concrete task intent most closely matches the user question.\n"
        "De-prioritize broad overview or generic admin guides when a narrower exact guide exists.\n"
    )
    if preferred_channel == "admin_studio":
        selector_prompt += (
            "For TA9/IntSight procedural guidance, prefer Admin Studio or UI-based candidates by default. "
            "Choose database/SQL/table-level candidates only if the user explicitly requested database guidance.\n"
        )
    elif preferred_channel == "database":
        selector_prompt += (
            "The user explicitly requested database or SQL guidance. Prefer database/table-level candidates over Admin Studio/UI candidates.\n"
        )
    if broad_coverage_intent:
        selector_prompt += (
            "When the user asks for more ways, alternatives, other options, supported methods, or broader coverage, "
            "keep multiple distinct candidates that cover different valid approaches. Do not collapse to a single "
            "candidate unless the rest are duplicates.\n"
        )
    if len(requested_subtasks) > 1:
        selector_prompt += (
            "This is a compound procedural question with multiple requested subtasks. "
            "Keep the combination of candidates that jointly covers all requested subtasks whenever the candidates support them. "
            "Do not prefer a single broad or aggregated document if it only clearly covers one subtask while another candidate covers a missing subtask directly.\n"
            "De-prioritize huge aggregated user-knowledge dumps when narrower task-specific procedure documents exist.\n"
        )
    selector_prompt += (
        "Return strict JSON with this shape only: {\"ordered_candidates\":[1,2],\"reason\":\"short reason\"}.\n\n"
        f"Question:\n{question}\n\n"
        + (
            "Requested subtasks:\n- "
            + "\n- ".join(_format_subtask_label(action, object_phrase) for action, object_phrase in requested_subtasks)
            + "\n\n"
            if requested_subtasks
            else ""
        )
        +
        f"Candidates:\n\n{candidates_block}\n"
    )

    try:
        verdict_text = call_llm(selector_prompt, temperature=0.0, model=OPENAI_RERANK_MODEL)
        try:
            parsed = json.loads(verdict_text)
        except json.JSONDecodeError:
            json_match = re.search(r"\{[\s\S]*\}", verdict_text)
            if not json_match:
                raise
            parsed = json.loads(json_match.group(0))
        ordered = parsed.get("ordered_candidates") or []
        ranked: List[dict] = []
        seen = set()
        for raw_idx in ordered:
            try:
                candidate_index = int(raw_idx) - 1
            except Exception:
                continue
            if 0 <= candidate_index < len(shortlist) and candidate_index not in seen:
                ranked.append(shortlist[candidate_index])
                seen.add(candidate_index)
            if len(ranked) >= max_sources:
                break
        if ranked:
            ranked.extend([item for idx, item in enumerate(shortlist) if idx not in seen])
            print(f"[LLM_RERANK] Applied LLM source ordering reason={parsed.get('reason', '')}")
            return ranked[:max_sources]
    except Exception as exc:
        print(f"[LLM_RERANK][WARN] Failed to rerank source candidates: {exc}")

    return shortlist[:max_sources]


# ---------------------------------------------------------------------
# API Models
# ---------------------------------------------------------------------

class ChatRequest(BaseModel):
    question: str
    top_k: int = 5
    force_reingest: Optional[bool] = False
    ticket_url: Optional[str] = None
    conversation_id: Optional[str] = None
    history: Optional[List[Dict[str, str]]] = None
    teach: Optional[bool] = False
    # If a ticket is selected, set to True for follow-up messages after the first structured reply
    is_followup: Optional[bool] = False
    # File uploads with content
    files: Optional[List[Dict[str, str]]] = None  # List of {name, type, data} where data is base64


class KnowledgeAddRequest(BaseModel):
    mode: str  # "content"
    text: Optional[str] = None
    files: Optional[List[Dict[str, str]]] = None
    request_id: Optional[str] = None


class KnowledgeCancelRequest(BaseModel):
    request_id: str


class ChatResponse(BaseModel):
    answer: str
    sources: List[str]


class IngestResponse(BaseModel):
    added_chunks: int
    total_chunks: int
    message: Optional[str] = None


class VectorDbDocumentUpdateRequest(BaseModel):
    collection_name: str
    source: str
    content: str


class VectorDbDocumentDeleteRequest(BaseModel):
    collection_name: str
    source: str


class SystemPromptUpdateRequest(BaseModel):
    template: str


# ---------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------


@app.get("/vector-db/collections")
def vector_db_collections():
    items: List[dict] = []
    for collection_name in (COLLECTION_NAME, MEMORY_COLLECTION_NAME):
        target_collection = _get_vector_collection(collection_name)
        items.append(
            {
                "name": collection_name,
                "description": _vector_collection_description(collection_name),
                "document_count": _count_collection_documents(collection_name),
                "token_count": _count_collection_tokens(collection_name),
                "chunk_count": target_collection.count(),
            }
        )
    return {"items": items}


@app.get("/vector-db/documents")
def vector_db_documents(
    collection_name: str,
    search: str = "",
    limit: int = 24,
    offset: int = 0,
    sort_by: str = "updated_at",
    sort_direction: str = "desc",
):
    safe_limit = max(1, min(limit, 100))
    safe_offset = max(0, offset)
    normalized_sort_by = (sort_by or "updated_at").strip().lower()
    normalized_sort_direction = (sort_direction or "desc").strip().lower()

    if normalized_sort_by not in {"updated_at", "token_count"}:
        raise HTTPException(status_code=400, detail=f"Unsupported sort_by: {sort_by}")
    if normalized_sort_direction not in {"asc", "desc"}:
        raise HTTPException(status_code=400, detail=f"Unsupported sort_direction: {sort_direction}")

    summaries = _group_collection_documents(collection_name)
    search_value = (search or "").strip()
    if search_value:
        full_term_matches: List[dict] = []
        partial_matches: List[dict] = []
        for item in summaries:
            match_meta = _score_vector_document_summary(item, search_value)
            if not match_meta:
                continue

            matched_item = dict(item)
            matched_item["preview"] = match_meta["preview"]
            matched_item["_search_score"] = match_meta["score"]

            if match_meta["all_terms_matched"] or not _tokenize_normalized(search_value):
                full_term_matches.append(matched_item)
            else:
                partial_matches.append(matched_item)

        active_matches = full_term_matches if full_term_matches else partial_matches
        active_matches.sort(
            key=lambda item: (
                -float(item.get("_search_score") or 0.0),
                str(item.get("updated_at") or ""),
                str(item.get("title") or "").lower(),
            )
        )
        summaries = active_matches

    if normalized_sort_by == "token_count":
        summaries.sort(
            key=lambda item: (
                int(item.get("token_count") or 0),
                str(item.get("title") or "").lower(),
            ),
            reverse=(normalized_sort_direction == "desc"),
        )
    else:
        summaries.sort(
            key=lambda item: (
                str(item.get("updated_at") or ""),
                str(item.get("title") or "").lower(),
            ),
            reverse=(normalized_sort_direction == "desc"),
        )

    page_items = [
        {key: value for key, value in item.items() if not key.startswith("_")}
        for item in summaries[safe_offset:safe_offset + safe_limit]
    ]
    return {
        "collection_name": collection_name,
        "total": len(summaries),
        "limit": safe_limit,
        "offset": safe_offset,
        "sort_by": normalized_sort_by,
        "sort_direction": normalized_sort_direction,
        "items": page_items,
    }


@app.get("/vector-db/document")
def vector_db_document(
    collection_name: str,
    source: str,
    chunk_limit: int = VECTOR_DB_DEFAULT_CHUNK_LIMIT,
    chunk_offset: int = 0,
    include_embeddings: bool = False,
    include_full_content: bool = True,
):
    return _build_vector_document_detail(
        collection_name,
        source,
        chunk_limit=chunk_limit,
        chunk_offset=chunk_offset,
        include_embeddings=include_embeddings,
        include_full_content=include_full_content,
    )


@app.get("/vector-db/chunk-embedding")
def vector_db_chunk_embedding(collection_name: str, chunk_id: str):
    target_collection = _get_vector_collection(collection_name)
    raw = target_collection.get(ids=[chunk_id], include=["embeddings", "metadatas"])
    ids = list(raw.get("ids", []) or [])
    if not ids:
        raise HTTPException(status_code=404, detail="Chunk not found")

    metas = list(raw.get("metadatas", []) or [])
    embeddings = list(raw.get("embeddings", []) or [])
    safe_meta = (metas[0] if metas else {}) or {}
    embedding = _safe_embedding_to_list(embeddings[0]) if embeddings else []

    return {
        "id": ids[0],
        "chunk": int(safe_meta.get("chunk", 0) or 0),
        "metadata": safe_meta,
        "embedding": embedding,
        "vector_dimensions": len(embedding),
    }


@app.put("/vector-db/document")
def vector_db_update_document(req: VectorDbDocumentUpdateRequest):
    target_collection = _get_vector_collection(req.collection_name)
    existing = target_collection.get(where={"source": req.source}, include=["metadatas"])
    existing_ids = list(existing.get("ids", []) or [])
    existing_metas = list(existing.get("metadatas", []) or [])
    if not existing_ids:
        raise HTTPException(status_code=404, detail="Document not found")

    new_ids, new_docs, new_metas, new_embeddings = _build_updated_chunk_records(
        req.source,
        req.content,
        existing_metas,
    )

    try:
        target_collection.add(
            ids=new_ids,
            documents=new_docs,
            metadatas=new_metas,
            embeddings=new_embeddings,
        )
        target_collection.delete(ids=existing_ids)
    except Exception as exc:
        try:
            target_collection.delete(ids=new_ids)
        except Exception:
            pass
        print(f"[API][VECTOR_DB][ERROR] update failed: {exc}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to update document: {exc}")

    _invalidate_cached_vector_document_payload(req.collection_name, req.source)

    return {
        "message": "Document updated successfully.",
        "source": req.source,
        "chunks_added": len(new_ids),
        "detail": _build_vector_document_detail(
            req.collection_name,
            req.source,
            chunk_limit=VECTOR_DB_DEFAULT_CHUNK_LIMIT,
            chunk_offset=0,
            include_embeddings=False,
            include_full_content=False,
        ),
    }


@app.delete("/vector-db/document")
def vector_db_delete_document(req: VectorDbDocumentDeleteRequest):
    target_collection = _get_vector_collection(req.collection_name)
    existing = target_collection.get(where={"source": req.source}, include=["metadatas"])
    existing_ids = list(existing.get("ids", []) or [])
    if not existing_ids:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        target_collection.delete(ids=existing_ids)
    except Exception as exc:
        print(f"[API][VECTOR_DB][ERROR] delete failed: {exc}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {exc}")

    _invalidate_cached_vector_document_payload(req.collection_name, req.source)

    return {
        "message": "Document deleted successfully.",
        "source": req.source,
        "deleted_chunks": len(existing_ids),
    }


@app.post("/internal/reinsert-backup")
def reinsert_backup():
    """Temporary endpoint: re-insert User Guide chunks from backup JSON using the app's own DB connection."""
    import json as _json
    backup_path = "/app/chroma_db/user_guide_backup.json"
    if not os.path.exists(backup_path):
        raise HTTPException(status_code=404, detail="Backup file not found")

    with open(backup_path) as f:
        data = _json.load(f)
    ids = data["ids"]
    docs = data["documents"]
    metas = data["metadatas"]
    total = len(ids)
    print(f"[REINSERT] Loaded {total} chunks from backup")

    # Check which chunks already exist
    existing = set()
    for i in range(0, total, 500):
        batch_ids = ids[i:i+500]
        try:
            got = collection.get(ids=batch_ids)
            existing.update(got["ids"])
        except Exception:
            pass
    print(f"[REINSERT] {len(existing)} chunks already exist, skipping those")

    # Filter remaining
    todo_ids, todo_docs, todo_metas = [], [], []
    for i in range(total):
        if ids[i] not in existing:
            todo_ids.append(ids[i])
            todo_docs.append(docs[i])
            todo_metas.append(metas[i])
    remaining = len(todo_ids)
    print(f"[REINSERT] Need to insert {remaining} chunks")
    if remaining == 0:
        return {"message": "All chunks already present", "total": total, "inserted": 0, "collection_count": collection.count()}

    BATCH = 50
    inserted = 0
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    for i in range(0, remaining, BATCH):
        b_ids = todo_ids[i:i+BATCH]
        b_docs = todo_docs[i:i+BATCH]
        b_metas = todo_metas[i:i+BATCH]

        # Batch embed via OpenAI API
        body = {"model": OPENAI_EMBEDDING_MODEL, "input": b_docs}
        resp = requests.post(f"{OPENAI_URL}/embeddings", json=body, headers=headers, timeout=120)
        if resp.status_code != 200:
            return {"error": f"OpenAI embeddings failed at batch {i}: {resp.text[:300]}", "inserted_so_far": inserted}
        embeddings = [item["embedding"] for item in sorted(resp.json()["data"], key=lambda x: x["index"])]

        collection.add(ids=b_ids, documents=b_docs, metadatas=b_metas, embeddings=embeddings)
        inserted += len(b_ids)
        print(f"[REINSERT] Inserted {inserted}/{remaining} (collection count: {collection.count()})")

    result = {"message": "Re-insertion complete", "total": total, "inserted": inserted, "collection_count": collection.count()}
    print(f"[REINSERT] Done: {result}")
    return result


@app.get("/health")
def health():
    print("[API][HEALTH] /health called")
    info = {
        "status": "ok",
        "chroma_empty": collection_empty(),
        "wiki_root": WIKI_ROOT,
        "collection_name": COLLECTION_NAME,
        "memory_collection_name": MEMORY_COLLECTION_NAME,
        "embedding_backend": "openai",
        "embedding_model": OPENAI_EMBEDDING_MODEL,
    }
    print(f"[API][HEALTH] {info}")
    return info


@app.get("/azure/tickets")
def azure_tickets(tag: str = "CC"):
    print(f"[API][ADO] /azure/tickets loading merged support-query results tag_param_ignored={tag}")
    try:
        items = ado_list_tickets(tag_contains=tag)
        return {"items": items}
    except Exception as exc:
        print(f"[API][ADO][ERROR] {exc}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/system-prompt")
def get_system_prompt():
    template = _read_system_prompt_template()
    return {
        "template": template,
        "path": SYSTEM_PROMPT_FILE,
        "display_path": SYSTEM_PROMPT_DISPLAY_PATH,
    }


@app.put("/system-prompt")
def update_system_prompt(req: SystemPromptUpdateRequest):
    try:
        template = _write_system_prompt_template(req.template)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        print(f"[API][PROMPT][ERROR] Failed to save system prompt: {exc}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to save system prompt: {exc}") from exc

    return {
        "message": "System prompt saved successfully.",
        "template": template,
        "path": SYSTEM_PROMPT_FILE,
        "display_path": SYSTEM_PROMPT_DISPLAY_PATH,
    }


def _knowledge_add_process(req: KnowledgeAddRequest, request_id: Optional[str]) -> dict:
    """Core knowledge ingestion logic — runs in a background thread.
    Returns a result dict with at least {approved: bool}; may include {canceled: bool}.
    """
    _ingest_log("knowledge_add start", request_id, force=True)
    content_text = ""
    source_name = ""
    collection_label = "user_knowledge"
    mode = (req.mode or "").strip().lower()

    if mode == "content":
        text_part = (req.text or "").strip()
        file_part = ""
        if req.files:
            file_part = build_file_context(
                req.files,
                describe_image_func=_describe_image_via_vision,
                cancel_check=lambda: _is_knowledge_request_cancelled(request_id),
                request_id=request_id,
            )
        content_text = "\n\n".join([p for p in [text_part, file_part] if p])
        source_name = f"user:content:{uuid.uuid4()}"
    else:
        return {"approved": False, "message": "mode must be content"}

    if not content_text.strip():
        return {"approved": False, "message": "No content to ingest"}

    if _is_knowledge_request_cancelled(request_id):
        _ingest_log("knowledge_add canceled before embedding started", request_id, force=True)
        return {"approved": False, "message": "Upload stopped by user.", "canceled": True}

    _ingest_log(f"knowledge_add content_ready len={len(content_text)}", request_id, force=True)

    # Validation policy: reject unusable or clearly irrelevant knowledge for both free text and files.
    is_valid_ta9_content, rejection_reason = _validate_ta9_knowledge_content(content_text)
    if not is_valid_ta9_content:
        return {"approved": False, "message": rejection_reason}

    # Chunk, embed, and add with the same retrieval weight as every other document.
    input_type = "file" if req.files or _looks_like_uploaded_file_content(content_text) else "free_text"
    chunks = chunk_text_preserve_table_rows(content_text) if input_type == "file" else chunk_text(content_text)
    if not chunks:
        return {"approved": False, "message": "No chunks generated from content"}

    _ingest_log(f"embedding phase start chunks_total={len(chunks)} input_type={input_type}", request_id, force=True)

    ids: List[str] = []
    docs: List[str] = []
    metas: List[dict] = []
    embeds: List[List[float]] = []
    uploaded_at = datetime.utcnow().isoformat() + "Z"

    for i, ch in enumerate(chunks):
        if _is_knowledge_request_cancelled(request_id):
            _ingest_log(
                f"cancel acknowledged during embedding at chunk={i + 1}/{len(chunks)} partial_chunks_added={len(ids)}",
                request_id,
                force=True,
            )
            return {
                "approved": False,
                "message": "Embedding stopped by user.",
                "chunks_added": len(ids),
                "source": source_name,
                "canceled": True,
            }
        try:
            chunk_kind = "text"
            if ch.startswith(TABLE_ROW_START_TAG):
                chunk_kind = "table_row"
            elif "[IMAGE_BLOCK_ANALYSIS]" in ch or "[PAGE_IMAGE_ANALYSIS_FALLBACK]" in ch:
                chunk_kind = "image_description"
            _ingest_log(
                f"embedding chunk={i + 1}/{len(chunks)} kind={chunk_kind} chars={len(ch)}",
                request_id,
            )
            emb = embed_text(ch)
        except Exception as e:
            print(f"[KNOWLEDGE][ERROR] Embedding failed chunk={i}: {e}")
            traceback.print_exc()
            return {
                "approved": False,
                "message": "Knowledge upload failed during embedding. Nothing was saved to the database.",
                "failed_chunk": i,
                "source": source_name,
            }
        metadata = {
            "source": source_name,
            "chunk": i,
            "uploaded_at": uploaded_at,
            "mode": mode,
            "input_type": input_type,
            "path": "",
            "collection": collection_label,
        }
        if ch.startswith(TABLE_ROW_START_TAG):
            metadata["chunk_type"] = "table_row"
            metadata.update(extract_table_row_metadata(ch))
        else:
            metadata["chunk_type"] = "text"
        ids.append(str(uuid.uuid4()))
        docs.append(ch)
        metas.append(metadata)
        embeds.append(emb)

    if not ids:
        return {"approved": False, "message": "Failed to embed any chunks"}

    memory_collection.add(ids=ids, documents=docs, metadatas=metas, embeddings=embeds)
    _ingest_log(f"knowledge_add complete chunks_added={len(ids)}", request_id, force=True)
    return {
        "approved": True,
        "message": "Knowledge added successfully.",
        "chunks_added": len(ids),
        "source": source_name,
    }


@app.post("/knowledge/add")
def knowledge_add(req: KnowledgeAddRequest):
    """Start knowledge ingestion in a background thread and return immediately.
    Poll GET /knowledge/status/{request_id} for progress and the final result.
    """
    mode = (req.mode or "").strip().lower()
    if mode != "content":
        raise HTTPException(status_code=400, detail="mode must be content")

    request_id = (req.request_id or "").strip() or str(uuid.uuid4())
    try:
        _mark_knowledge_request_started(request_id)
        _store_job_result(request_id, {"status": "processing", "started_at": datetime.utcnow().isoformat() + "Z"})
        _ingest_log("knowledge_add queued as background job", request_id, force=True)

        def _run() -> None:
            try:
                result = _knowledge_add_process(req, request_id)
                _store_job_result(request_id, {"status": "done", **result})
            except Exception as exc:
                print(f"[API][KNOWLEDGE][ERROR] background job exception: {exc}")
                traceback.print_exc()
                _store_job_result(request_id, {"status": "done", "approved": False, "message": f"Processing error: {exc}"})
            finally:
                _clear_knowledge_request(request_id)

        threading.Thread(target=_run, daemon=True).start()
        return {"status": "processing", "request_id": request_id}
    except HTTPException:
        raise
    except Exception as exc:
        print(f"[API][KNOWLEDGE][ERROR] knowledge_add setup failed: {exc}")
        traceback.print_exc()
        _clear_knowledge_request(request_id)
        raise HTTPException(status_code=500, detail=str(exc))


# Maximum characters to send to LLM for content prep (stays within 128k token context)
# ~400k chars ≈ 100k tokens, safe for any OpenAI model
_LLM_PREP_MAX_CHARS = int(os.getenv("LLM_PREP_MAX_CHARS", "400000"))


def _prepare_rag_content(raw_text: str) -> str:
    """Normalize and structure knowledge content for better RAG ingestion.
    
    For large files (>400k chars), LLM prep is skipped — the raw extracted text is already
    high quality from PyMuPDF + vision analysis and does not need LLM restructuring.
    Chunking handles large content; LLM prep is only useful for short user-typed content.
    """
    if not raw_text.strip():
        return ""
    if not OPENAI_API_KEY:
        return raw_text

    # Skip LLM prep for large files — sending 1M+ tokens to LLM would crash.
    # Large files (PDFs etc.) are already well-structured from extraction pipeline.
    if len(raw_text) > _LLM_PREP_MAX_CHARS:
        print(f"[KNOWLEDGE] Content too large for LLM prep ({len(raw_text)} chars > {_LLM_PREP_MAX_CHARS}), skipping — using raw extracted text directly.")
        return raw_text

    prep_prompt = (
        "You are a strict TA9 knowledge normalizer."
        "then rewrite it into clean, structured text for retrieval. "
        "Use ONLY information explicitly present in the input. "
        "Do NOT infer, assume, enrich, generalize, or add domain details that are not written in the source. "
        "Do NOT invent product names, categories, industries, procedures, tags, or entities.\n\n"
        "Output English plain text with these sections in order, each on its own line header:\n"
        "Title:\n"
        "Summary:\n"
        "Key Details:\n"
        "Steps or Procedures (if any):\n"
        "Entities/Fields:\n"
        "Tags:\n\n"
        "Guidelines:\n"
        "- Title: short, specific, based only on source text.\n"
        "- Summary: 2-4 sentences, source-faithful only.\n"
        "- Key Details: bullet list of facts explicitly present in source.\n"
        "- Steps or Procedures: numbered steps only if applicable.\n"
        "- Entities/Fields: list only entities/fields explicitly named in source.\n"
        "- Tags: only source-grounded terms; no invented tags.\n"
        "- If a section has no explicit source data, write: Not provided in source.\n\n"
        "Input:\n" + raw_text
    )
    try:
        prepared = call_llm(prep_prompt, temperature=0.1)
        prepared = (prepared or "").strip()
        return prepared if prepared else raw_text
    except Exception as e:
        print(f"[KNOWLEDGE][WARN] RAG prep failed: {e}")
        return raw_text


def _find_similar_knowledge_sources(text: str, limit: int = 5, max_distance: float = 0.28) -> List[str]:
    """Find existing knowledge sources that are highly similar to the provided text.
    
    The OpenAI embedding API has an 8,191 token limit per request (~32,000 chars).
    For large files, we sample the first representative chunk only.
    """
    if not text.strip():
        return []
    if not OPENAI_API_KEY:
        return []
    try:
        # Truncate to embedding API limit: 8191 tokens ≈ 32,000 characters
        _EMBED_MAX_CHARS = 32000
        sample_text = text[:_EMBED_MAX_CHARS]
        if len(text) > _EMBED_MAX_CHARS:
            print(f"[KNOWLEDGE] Truncating text for similarity check: {len(text)} -> {_EMBED_MAX_CHARS} chars")
        emb = embed_text(sample_text)
        similar_sources: List[str] = []
        for col in (memory_collection, collection):
            results = col.query(query_embeddings=[emb], n_results=limit, include=["metadatas", "distances"])
            metas = results.get("metadatas", [[]])[0] if results else []
            distances = results.get("distances", [[]])[0] if results else []
            for meta, dist in zip(metas or [], distances or []):
                if dist is not None and dist <= max_distance:
                    source = meta.get("source") if meta else None
                    if source:
                        similar_sources.append(str(source))
        seen = set()
        deduped = []
        for src in similar_sources:
            if src in seen:
                continue
            seen.add(src)
            deduped.append(src)
        return deduped
    except Exception as e:
        print(f"[KNOWLEDGE][WARN] Similarity check failed: {e}")
        return []


@app.post("/knowledge/prepare")
def knowledge_prepare(req: KnowledgeAddRequest):
    """Prepare user content for RAG and return the normalized text without validating it."""
    try:
        request_id = (req.request_id or "").strip() or None
        _mark_knowledge_request_started(request_id)
        _ingest_log("knowledge_prepare start", request_id, force=True)
        text_part = (req.text or "").strip()
        file_part = ""
        if req.files:
            file_part = build_file_context(
                req.files,
                describe_image_func=_describe_image_via_vision,
                cancel_check=lambda: _is_knowledge_request_cancelled(request_id),
                request_id=request_id,
            )

        raw_content = "\n\n".join([p for p in [text_part, file_part] if p])
        if not raw_content.strip():
            raise HTTPException(status_code=400, detail="No content to prepare")

        if _is_knowledge_request_cancelled(request_id):
            _ingest_log("knowledge_prepare canceled", request_id, force=True)
            return {
                "approved": False,
                "message": "Preparation stopped by user.",
                "canceled": True,
            }

        prepared_content = _prepare_rag_content(raw_content)
        final_content = prepared_content if prepared_content.strip() else raw_content
        return {
            "approved": True,
            "message": "Knowledge prepared for RAG.",
            "prepared_text": final_content,
        }
    except HTTPException:
        raise
    except Exception as exc:
        print(f"[API][KNOWLEDGE][ERROR] prepare failed: {exc}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        _clear_knowledge_request((req.request_id or "").strip() or None)


@app.post("/knowledge/cancel")
def knowledge_cancel(req: KnowledgeCancelRequest):
    request_id = (req.request_id or "").strip()
    if not request_id:
        raise HTTPException(status_code=400, detail="request_id is required")
    existed = _cancel_knowledge_request(request_id)
    _ingest_log(f"/knowledge/cancel accepted (was_active={existed})", request_id, force=True)
    return {
        "ok": True,
        "message": "Cancellation requested.",
        "request_id": request_id,
        "was_active": existed,
    }


@app.get("/knowledge/status/{request_id}")
def knowledge_job_status(request_id: str):
    """Poll the status of a background knowledge ingestion job started by POST /knowledge/add.
    Returns {status: 'processing'} while running, or {status: 'done', approved: bool, ...} when finished.
    """
    if not request_id:
        raise HTTPException(status_code=400, detail="request_id is required")
    job = _get_job_result(request_id)
    if not job:
        return {"status": "not_found", "request_id": request_id}
    return {"request_id": request_id, **job}


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
# Chat Endpoint
# ---------------------------------------------------------------------

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    print(f"[API][CHAT] /chat called question='{req.question[:200]}' top_k={req.top_k} force_reingest={req.force_reingest} files={len(req.files) if req.files else 0}")
    question = (req.question or "").strip()
    total_rag_steps = 8
    _rag_log_step(1, total_rag_steps, "Request received", f"question_len={len(question)} files={len(req.files) if req.files else 0}")

    conversation_key = (req.conversation_id or req.ticket_url or "default").strip() or "default"
    incoming_history = _normalize_history_messages(req.history)
    if incoming_history:
        dq = deque(incoming_history[-MAX_CONVERSATION_MESSAGES:], maxlen=MAX_CONVERSATION_MESSAGES)
        conversation_store[conversation_key] = dq
    stored_history = list(conversation_store.get(conversation_key, deque()))
    conversation_state = dict(conversation_state_store.get(conversation_key) or {})
    use_history_context = _should_use_history_for_question(
        question,
        stored_history,
        explicit_is_followup=bool(req.is_followup),
    )
    history_context = _format_history_for_prompt(stored_history, max_messages=8) if use_history_context else ""
    if history_context:
        print(f"[API][CHAT] Using conversation history context key={conversation_key} messages={len(stored_history)}")
    else:
        print(f"[API][CHAT] Treating question as standalone key={conversation_key}")

    # Process uploaded files early to include their content in context
    file_context = ""
    if req.files:
        _rag_log_step(2, total_rag_steps, "Processing user-uploaded files", f"count={len(req.files)}")
        try:
            file_context = build_file_context(req.files, describe_image_func=_describe_image_via_vision)
            if file_context:
                print(f"[API][CHAT] Extracted file context: {len(file_context)} characters")
        except Exception as e:
            print(f"[API][CHAT][WARN] File processing failed: {e}")
            file_context = ""
    else:
        _rag_log_step(2, total_rag_steps, "Processing user-uploaded files", "no files were attached")

    # Parse ticket selection early so we can allow an empty initial message to trigger the first structured reply
    selected_ticket_id: Optional[int] = None
    selected_ticket_text: Optional[str] = None
    ticket_key: Optional[str] = None
    if req.ticket_url:
        _rag_log_step(3, total_rag_steps, "Loading selected ticket context", req.ticket_url)
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
    else:
        _rag_log_step(3, total_rag_steps, "Loading selected ticket context", "no ticket selected")

    has_ticket = bool(ticket_key)

    # Enforce non-empty question
    if not question:
        print("[API][CHAT][ERROR] Empty question")
        raise HTTPException(status_code=400, detail="question is empty")

    if _question_requests_previous_answer_source(question):
        answer = _build_previous_answer_source_answer(question, conversation_state)
        _store_conversation_turn(
            conversation_key,
            question,
            answer,
            sources=list(conversation_state.get("sources") or []),
            selected_ticket_id=conversation_state.get("selected_ticket_id"),
            selected_ticket_url=conversation_state.get("selected_ticket_url"),
            used_selected_ticket=bool(conversation_state.get("used_selected_ticket")),
            used_file_context=bool(conversation_state.get("used_file_context")),
        )
        print("[API][CHAT] Answered previous-source clarification from conversation state")
        return ChatResponse(answer=answer, sources=list(conversation_state.get("sources") or []))

    has_active_anchor = bool(
        selected_ticket_text
        or file_context
        or (use_history_context and bool(conversation_state.get("has_grounded_sources")))
    )
    if _question_needs_anchor(question) and not has_active_anchor:
        answer = _build_anchor_clarification_answer(question)
        _store_conversation_turn(
            conversation_key,
            question,
            answer,
            sources=[],
            selected_ticket_id=selected_ticket_id,
            selected_ticket_url=req.ticket_url,
            used_selected_ticket=bool(selected_ticket_text),
            used_file_context=bool(file_context),
        )
        print("[API][CHAT] Blocked ambiguous referential question without an anchor")
        return ChatResponse(answer=answer, sources=[])

    if req.force_reingest:
        print("[API][CHAT] force_reingest=True → calling ingest_wiki_files(force=True)")
        ingest_wiki_files(force=True)

    ta9_mode = _is_ta9_question(question)
    is_foundational = _is_foundational_question(question)
    query_variants = _build_query_variants(question, ta9_mode)
    _rag_log_step(4, total_rag_steps, "Preparing retrieval queries", f"variants={len(query_variants)} history_used={bool(history_context)}")
    if history_context:
        history_seed = f"Conversation context:\n{history_context}\n\nCurrent question:\n{question}"
        query_variants = [history_seed] + query_variants
        query_variants = query_variants[:4]
    ticket_context_hint = None
    if selected_ticket_text:
        # Keep a short hint to enrich similarity search without overwhelming the question
        ticket_context_hint = (selected_ticket_text[:800] or "").strip()

    primary_emb = None
    agg_ids: List[str] = []
    agg_distances: List[float] = []
    agg_docs: List[str] = []
    agg_metas: List[dict] = []

    try:
        _rag_log_step(5, total_rag_steps, "Running vector retrieval", f"query_variants={len(query_variants)}")
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

            # Primary search: question-focused (user knowledge first, then wiki)
            for col, col_label in ((memory_collection, "user_knowledge"), (collection, "wiki")):
                results = col.query(
                    query_embeddings=[q_emb],
                    n_results=per_query_k,
                    include=["distances", "documents", "metadatas", "embeddings"],
                )

                ids = results.get("ids", [[]])[0]
                distances = results.get("distances", [[]])[0]
                docs = results.get("documents", [[]])[0]
                metas = results.get("metadatas", [[]])[0]

                normalized_metas = []
                for meta in metas or []:
                    meta = meta or {}
                    if "collection" not in meta:
                        meta = {**meta, "collection": col_label}
                    normalized_metas.append(meta)

                agg_ids.extend(ids or [])
                agg_distances.extend(distances or [])
                agg_docs.extend(docs or [])
                agg_metas.extend(normalized_metas)
    except Exception as exc:
        print(f"[API][CHAT][ERROR] Embedding or vector search failed: {exc}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Embedding/vector search failed: {exc}")

    ids = agg_ids
    distances = agg_distances
    docs = agg_docs
    metas = agg_metas

    # Dedicated priority-document search: ensure the best-matching chunks from
    # priority documents (e.g. User Guide) are always in the candidate pool.
    if primary_emb:
        try:
            _priority_sources = set()
            for _m in metas:
                if _m and _is_priority_document(str(_m.get("source", "")), _m):
                    _priority_sources.add(str(_m.get("source", "")))
            # Also scan a small sample to discover priority sources not yet in results
            _sample = collection.get(limit=200, include=["metadatas"])
            for _m in (_sample.get("metadatas") or []):
                if _m and _is_priority_document(str(_m.get("source", "")), _m):
                    _priority_sources.add(str(_m.get("source", "")))

            existing_ids = set(ids)
            for _ps in _priority_sources:
                if not _ps:
                    continue
                for _col, _cl in ((collection, "wiki"), (memory_collection, "user_knowledge")):
                    try:
                        pr = _col.query(
                            query_embeddings=[primary_emb],
                            n_results=30,
                            where={"source": _ps},
                            include=["distances", "documents", "metadatas"],
                        )
                        pr_ids = pr.get("ids", [[]])[0]
                        pr_dists = pr.get("distances", [[]])[0]
                        pr_docs = pr.get("documents", [[]])[0]
                        pr_metas = pr.get("metadatas", [[]])[0]
                        added = 0
                        for _i, _id in enumerate(pr_ids or []):
                            if _id not in existing_ids:
                                ids.append(_id)
                                distances.append(pr_dists[_i])
                                docs.append(pr_docs[_i])
                                _pm = pr_metas[_i] or {}
                                if "collection" not in _pm:
                                    _pm = {**_pm, "collection": _cl}
                                metas.append(_pm)
                                existing_ids.add(_id)
                                added += 1
                        if added:
                            print(f"[API][CHAT] Priority search: added {added} chunks from {_ps} via {_cl}")
                    except Exception:
                        pass
        except Exception as e:
            print(f"[API][CHAT][WARN] Priority document search failed: {e}")

    # Secondary search: ticket-aware similarity without overriding the question
    if ticket_context_hint:
        try:
            similar_query = question + "\n\nRelated ticket context:\n" + ticket_context_hint
            if history_context:
                similar_query += "\n\nRecent conversation:\n" + history_context
            sim_emb = embed_text(similar_query)
            for col, col_label in ((memory_collection, "user_knowledge"), (collection, "wiki")):
                sim_results = col.query(
                    query_embeddings=[sim_emb],
                    n_results=max(20, req.top_k * 4),
                    include=["distances", "documents", "metadatas"],
                )
                sim_ids = sim_results.get("ids", [[]])[0]
                sim_distances = sim_results.get("distances", [[]])[0]
                sim_docs = sim_results.get("documents", [[]])[0]
                sim_metas = sim_results.get("metadatas", [[]])[0]

                normalized_metas = []
                for meta in sim_metas or []:
                    meta = meta or {}
                    if "collection" not in meta:
                        meta = {**meta, "collection": col_label}
                    normalized_metas.append(meta)

                if sim_docs:
                    docs = docs + sim_docs
                    metas = metas + normalized_metas
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
            include=["documents", "metadatas", "distances"],
        )
        mem_docs = mem.get("documents", [[]])[0]
        mem_metas = mem.get("metadatas", [[]])[0]
        if mem_docs:
            print(f"[API][CHAT] Collected {len(mem_docs)} memory docs for context candidates")
            for d, m in zip(mem_docs, mem_metas):
                meta = m or {"source": "memory", "chunk": 0}
                if "collection" not in meta:
                    meta = {**meta, "collection": "user_knowledge"}
                docs.append(d)
                metas.append(meta)
    except Exception as e:
        print(f"[API][CHAT][WARN] memory query failed: {e}")

    # Topic-agnostic fallback retrieval when initial context is weak or empty
    initial_profile = _context_confidence_profile(question, docs, distances)
    if not file_context and not selected_ticket_text and (not docs or initial_profile["confidence"] < 0.42):
        fallback_variants = _build_fallback_query_variants(question)
        print(
            f"[API][CHAT] Triggering fallback retrieval: docs={len(docs)} "
            f"confidence={initial_profile['confidence']} variants={len(fallback_variants)}"
        )
        try:
            for variant in fallback_variants:
                if not variant.strip():
                    continue
                fv_emb = embed_text(variant)
                for col, col_label in ((memory_collection, "user_knowledge"), (collection, "wiki")):
                    fv_results = col.query(
                        query_embeddings=[fv_emb],
                        n_results=max(12, req.top_k * 3),
                        include=["distances", "documents", "metadatas"],
                    )
                    fv_ids = fv_results.get("ids", [[]])[0]
                    fv_distances = fv_results.get("distances", [[]])[0]
                    fv_docs = fv_results.get("documents", [[]])[0]
                    fv_metas = fv_results.get("metadatas", [[]])[0]

                    normalized_metas = []
                    for meta in fv_metas or []:
                        meta = meta or {}
                        if "collection" not in meta:
                            meta = {**meta, "collection": col_label}
                        normalized_metas.append(meta)

                    if fv_docs:
                        docs.extend(fv_docs)
                        metas.extend(normalized_metas)
                        ids.extend(fv_ids)
                        distances.extend(fv_distances)
            print(f"[API][CHAT] Fallback retrieval completed: total docs now={len(docs)}")
        except Exception as e:
            print(f"[API][CHAT][WARN] fallback retrieval failed: {e}")

    if not docs:
        print("[API][CHAT] No docs after all retrieval attempts → returning strict no-context response")
        answer = call_llm(
            "You are a strict RAG assistant. There is no retrievable knowledge-base context for this question. "
            "Do NOT provide speculative or generic product guidance. "
            "Return a short response that clearly states the missing context and asks for the exact document/topic needed.\n\n"
            f"Question: {question}\n\n"
            "Response:"
        )
        _store_conversation_turn(
            conversation_key,
            question,
            answer,
            sources=[],
            selected_ticket_id=selected_ticket_id,
            selected_ticket_url=req.ticket_url,
            used_selected_ticket=bool(selected_ticket_text),
            used_file_context=bool(file_context),
        )
        return ChatResponse(answer=answer, sources=[])

    docs, metas, distances, ids = rerank_results(question, docs, metas, distances=distances, ids=ids)
    _rag_log_step(6, total_rag_steps, "Ranking and consolidating sources", f"candidate_docs={len(docs)}")
    question_is_procedural = _question_has_procedural_intent(question)
    entity_fact_intent = _question_has_entity_fact_intent(question)
    broad_coverage_intent = _question_requests_broad_coverage(question)

    # Confidence-based behavior: avoid hard refusals and answer in best-effort mode when confidence is low
    final_profile = _context_confidence_profile(question, docs, distances)
    low_confidence_mode = (
        not file_context
        and not selected_ticket_text
        and final_profile["confidence"] < 0.35
    )
    print(
        "[API][CHAT] Retrieval confidence "
        f"confidence={final_profile['confidence']} best_distance={final_profile['best_distance']} "
        f"max_overlap={final_profile['max_overlap']} low_confidence_mode={low_confidence_mode}"
    )

    context_blocks: List[str] = []
    source_strings: List[str] = []
    source_candidates = _build_source_context_candidates(
        question,
        docs,
        metas,
        distances=distances,
        ids=ids,
        max_sources=6 if broad_coverage_intent else 5,
    )

    # Source-level lexical rescue helps when the exact guide is present in the collection
    # but was not ranked high enough by embeddings alone.
    should_run_lexical_rescue = (
        question_is_procedural
        or final_profile["confidence"] < 0.68
        or final_profile["max_overlap"] < 0.32
    )
    if should_run_lexical_rescue:
        lexical_candidates = _build_global_lexical_source_candidates(
            question,
            max_sources=7 if broad_coverage_intent else (6 if question_is_procedural else 4),
        )
        source_candidates = _merge_source_candidate_lists(
            source_candidates,
            lexical_candidates,
            max_sources=7 if broad_coverage_intent else (6 if question_is_procedural else 5),
        )
        source_candidates = _filter_low_context_source_candidates(
            question,
            source_candidates,
            max_sources=7 if broad_coverage_intent else (6 if question_is_procedural else 5),
        )

    should_run_llm_rerank = (
        len(source_candidates) > 1
        and (question_is_procedural or final_profile["confidence"] < 0.8)
    )
    if should_run_llm_rerank:
        source_candidates = _llm_select_source_candidates(
            question,
            source_candidates,
            max_sources=6 if broad_coverage_intent else 5,
        )
        source_candidates = _filter_low_context_source_candidates(
            question,
            source_candidates,
            max_sources=6 if broad_coverage_intent else 5,
        )

    # Let the LLM reranking decide source order; give every selected source full content
    MAX_CONTEXT_SOURCES = 6 if broad_coverage_intent else 5
    print(f"[API][CHAT] Building context with MAX_CONTEXT_SOURCES={MAX_CONTEXT_SOURCES}")

    # Guaranteed priority-document context: always query the largest priority document
    # (User Guide) and inject the most relevant chunks as a mandatory context block.
    _priority_context_block = None
    _priority_source_str = None
    _priority_already_in_candidates = False
    if primary_emb:
        try:
            # Find the largest priority document source in the Intsight collection
            _pri_source_counts: Dict[str, int] = {}
            _all_metas = collection.get(include=["metadatas"]).get("metadatas", [])
            for _pm in _all_metas:
                if _pm and _is_priority_document(str(_pm.get("source", "")), _pm):
                    _src = str(_pm.get("source", ""))
                    _pri_source_counts[_src] = _pri_source_counts.get(_src, 0) + 1

            # Pick the largest priority doc (User Guide = 1655 chunks)
            _target_source = max(_pri_source_counts, key=_pri_source_counts.get) if _pri_source_counts else None

            if _target_source:
                _priority_already_in_candidates = any(
                    c.get("source") == _target_source for c in source_candidates
                )
                # Query best-matching chunks from the User Guide
                pr = collection.query(
                    query_embeddings=[primary_emb],
                    n_results=50,
                    where={"source": _target_source},
                    include=["distances", "documents", "metadatas"],
                )
                pr_docs = pr.get("documents", [[]])[0]
                pr_dists = pr.get("distances", [[]])[0]
                if pr_docs:
                    paired = sorted(zip(pr_dists, pr_docs), key=lambda x: x[0])
                    best_chunks = [doc for _, doc in paired[:25]]
                    best_dist = paired[0][0] if paired else None
                    priority_content = _merge_chunk_texts(best_chunks, max_chars=16000)
                    if priority_content.strip():
                        chunk_count = _pri_source_counts[_target_source]
                        _priority_source_str = (
                            f"Intsight::{_target_source} "
                            f"({chunk_count} chunks, best_dist={best_dist})"
                        )
                        _priority_context_block = (
                            f"PRIORITY REFERENCE: {_priority_source_str}\n"
                            f"Title: User Guide (Priority Document)\n"
                            f"{priority_content}"
                        )
                        print(
                            f"[API][CHAT] Priority doc injection: source={_target_source} "
                            f"chunks_queried=50 used=25 chars={len(priority_content)} "
                            f"best_dist={best_dist} already_in_candidates={_priority_already_in_candidates}"
                        )
        except Exception as e:
            print(f"[API][CHAT][WARN] Priority context injection failed: {e}")

    if source_candidates:
        remaining_slots = MAX_CONTEXT_SOURCES - (1 if selected_ticket_text else 0)
        for idx, candidate in enumerate(source_candidates[:remaining_slots]):
            doc_number = idx + 1
            match_label = f"DOCUMENT {doc_number} — PRIMARY MATCH" if idx == 0 else f"DOCUMENT {doc_number} — SUPPLEMENTAL MATCH"
            src = (
                f"{candidate['collection_name']}::{candidate['source']} "
                f"({candidate['chunk_count']} chunks, best_dist={candidate['best_distance']})"
            )
            source_strings.append(src)
            snippet = candidate["excerpt"][:200].replace("\n", " ")
            # Give EVERY source its full content so the LLM can extract all relevant parts
            # Priority documents get a larger context window
            max_content_chars = 12000 if candidate.get("is_priority") else 8000
            candidate_content = _merge_chunk_texts(
                [str(candidate.get("full_content") or candidate.get("excerpt") or "")],
                max_chars=max_content_chars,
            )
            print(f"[API][CHAT] Context source: {src} | snippet='{snippet}...'")
            context_blocks.append(
                f"=== {match_label}: {src} ===\n"
                f"Title: {candidate['title']}\n"
                f"(This is a separate document. Do NOT mix its steps with other documents.)\n"
                f"{candidate_content}\n"
                f"=== END DOCUMENT {doc_number} ==="
            )
    else:
        # Fallback to chunk-level context if source consolidation could not be built.
        remaining_slots = 10 - (1 if selected_ticket_text else 0)
        for i, (doc, meta) in enumerate(list(zip(docs, metas))[:remaining_slots]):
            id_val = ids[i] if i < len(ids) else None
            dist_val = distances[i] if i < len(distances) else None
            src = f"{meta.get('source')} (chunk {meta.get('chunk', 0)}) id={id_val} dist={dist_val}"
            source_strings.append(src)
            snippet = doc[:200].replace("\n", " ")
            print(f"[API][CHAT] Context source: {src} | snippet='{snippet}...'")
            context_blocks.append(f"Source: {src}\n{doc}")

    # Inject priority document context block — always first, always present
    if _priority_context_block:
        # If the priority doc was already selected as a regular source, remove it
        # to avoid duplication — the priority block has richer content
        if _priority_already_in_candidates and _priority_source_str:
            _pri_src_key = _priority_source_str.split("::")[1].split(" (")[0] if "::" in _priority_source_str else ""
            context_blocks = [
                b for b in context_blocks
                if _pri_src_key not in b[:200]
            ]
            source_strings = [s for s in source_strings if _pri_src_key not in s]
        context_blocks.insert(0, _priority_context_block)
        if _priority_source_str:
            source_strings.insert(0, _priority_source_str)

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
        "provide a clear explanation using only the available context. If context is incomplete, clearly state what is missing. "
        "Do not add unsupported product details.\n\n"
        if is_foundational or ta9_mode
        else ""
    )
    
    ta9_instruction = (
        "11. If the question is about TA9/IntSight features or platform capabilities, "
        "provide a detailed answer grounded in retrieved context, and avoid examples that are not present in context. "
        "Use bullet points when helpful.\n\n"
        if ta9_mode
        else ""
    )

    # Build context sections with proper priority
    # When files are attached, they should be PRIMARY source of truth
    context_sections = []
    
    if file_context:
        # Files come FIRST and are marked as primary
        context_sections.append(
            f"=== USER-PROVIDED FILES (PRIMARY SOURCE) ===\n"
            f"The user has attached files. Answer their question using this content as the main source.\n\n"
            f"{file_context}\n"
        )
    
    if selected_ticket_text:
        # Ticket context is secondary if files exist, primary otherwise
        priority_label = "REFERENCE" if file_context else "PRIMARY"
        context_sections.append(
            f"=== SELECTED TICKET ({priority_label}) ===\n"
            f"{selected_ticket_text}\n"
        )
    
    # Include KB context as reference even with files for how-to/procedural questions.
    # Screenshot-only context is often insufficient for actionable guidance.
    should_include_rag_context = True
    if file_context:
        question_lc = (question or "").lower()
        procedural_intent = any(term in question_lc for term in [
            "how", "step", "steps", "add", "create", "configure", "setup", "set up"
        ])
        best_distance = distances[0] if distances else 1.0
        top_overlap = _lexical_overlap_ratio(question, docs[0]) if docs else 0.0
        # More permissive threshold so attached screenshots still benefit from the manual/KB.
        should_include_rag_context = procedural_intent or ta9_mode or best_distance < 0.75 or top_overlap >= 0.10
        if not should_include_rag_context:
            print(
                "[API][CHAT] Skipping RAG context with file attachment: "
                f"best_distance={best_distance} top_overlap={top_overlap}."
            )
    
    if context_text and should_include_rag_context:
        # Wiki context is always supplemental
        priority_label = "REFERENCE" if (file_context or selected_ticket_text) else "PRIMARY"
        context_sections.append(
            f"=== KNOWLEDGE BASE ({priority_label}) ===\n"
            f"{context_text}\n"
        )

    if source_candidates and question_is_procedural:
        context_sections.append(
            "=== RETRIEVAL & COMPLETENESS PRIORITY ===\n"
            "For how-to or configuration questions, identify which retrieved document BEST answers the specific question asked.\n"
            "Use that document's procedure as your primary answer. Do NOT merge procedural steps from different documents.\n"
            "If the user's question asks about MULTIPLE distinct operations (e.g. 'entities AND relations'), "
            "provide the procedure for each from its own source document, clearly separated.\n"
            "CRITICAL: Each retrieved document describes a SPECIFIC procedure. Before using content from a document, "
            "verify that the document's procedure matches what the user is asking. A document about 'creating a relation data model' "
            "is NOT the same as 'defining link analysis in an existing data model'. Use only the document whose topic matches the question.\n"
            "If only one document matches the user's actual question, use only that document and ignore unrelated ones.\n"
        )

    if source_candidates and broad_coverage_intent:
        context_sections.append(
            "=== BREADTH COVERAGE PRIORITY ===\n"
            "The user is asking for alternatives, additional options, different methods, or broader coverage. "
            "Synthesize distinct valid approaches from all relevant matches. Do not say there is only one way unless the retrieved context clearly supports that conclusion after considering the supplemental matches too.\n"
        )

    if source_candidates and entity_fact_intent:
        context_sections.append(
            "=== ENTITY FACT PRIORITY ===\n"
            "When the question asks about company names, product names, aliases, naming rules, or how many products are listed, "
            "prefer the documents that explicitly define or enumerate those facts. "
            "If the context lists the relevant items, answer directly from that list and state the count.\n"
        )

    if file_context and should_include_rag_context:
        context_sections.append(
            "=== ANSWERING STRATEGY ===\n"
            "Use the screenshot to identify the current UI state, and use knowledge-base chunks to provide concrete step-by-step instructions.\n"
            "If the exact button/path is not visible in screenshot but appears in KB, state that clearly as KB-based guidance.\n"
        )

    if low_confidence_mode:
        context_sections.append(
            "=== RETRIEVAL CONFIDENCE NOTICE ===\n"
            "The retrieved context may only partially match the question. "
            "Provide a best-effort answer grounded in available context, state assumptions clearly, "
            "and ask one concise follow-up question to close the gap.\n"
        )

    if history_context:
        context_sections.append(
            "=== RECENT CONVERSATION CONTEXT ===\n"
            "Use this to resolve references like 'that', 'those', or follow-up clarifications.\n"
            f"{history_context}\n"
        )
    else:
        context_sections.append(
            "=== QUESTION ISOLATION RULE ===\n"
            "Treat the current user question as standalone. Do not use previous conversation topics to infer missing nouns, products, areas, or procedures unless the current question explicitly refers back to them.\n"
        )
    
    combined_context = "\n\n".join(context_sections)
    combined_context_tokens = _estimate_text_tokens(combined_context)
    _rag_log_step(
        7,
        total_rag_steps,
        "Building final prompt context",
        f"context_chars={len(combined_context)} context_tokens={combined_context_tokens}",
    )

    prompt, combined_context = _fit_prompt_to_model_budget(
        question=question,
        combined_context=combined_context,
        foundational_instruction=foundational_instruction,
        ta9_instruction=ta9_instruction,
    )

    try:
        _rag_log_step(
            8,
            total_rag_steps,
            "Generating grounded answer",
            f"prompt_chars={len(prompt)} prompt_tokens={_estimate_text_tokens(prompt)}",
        )
        draft_answer = call_llm(prompt, temperature=0.2)
        # NOTE: Removed 4 post-processing LLM calls that were degrading answers:
        # _ground_answer_against_context — was stripping valid content and saying "not found"
        # _enforce_specific_grounded_answer — redundant with system prompt rules
        # _llm_ensure_answer_completeness — redundant with system prompt rules
        # _llm_verify_answer_relevance — was nuking entire answers with "does not contain a direct answer"
        # The system prompt already handles grounding, specificity, and completeness.
        answer = _normalize_noncode_fenced_blocks(draft_answer)
    except Exception as exc:
        print(f"[API][CHAT][ERROR] LLM call failed: {exc}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"LLM call failed: {exc}")

    _store_conversation_turn(
        conversation_key,
        question,
        answer,
        sources=source_strings,
        selected_ticket_id=selected_ticket_id,
        selected_ticket_url=req.ticket_url,
        used_selected_ticket=bool(selected_ticket_text),
        used_file_context=bool(file_context),
    )

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
# TEMPORARY: Re-insert User Guide chunks from backup
# ---------------------------------------------------------------------
@app.post("/admin/reinsert-all")
def admin_reinsert_all():
    """Re-insert all documents from backup JSONs into both collections."""
    import json as _json

    results = {}
    backups = [
        ("Intsight", os.path.join(CHROMA_DIR, "Intsight_full_backup.json"), collection),
        ("New_Knowledge", os.path.join(CHROMA_DIR, "New_Knowledge_full_backup.json"), memory_collection),
    ]

    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    BATCH = 50

    for col_name, backup_path, col_obj in backups:
        if not os.path.exists(backup_path):
            print(f"[REINSERT][{col_name}] Backup file not found: {backup_path}")
            results[col_name] = {"status": "skipped", "reason": "backup_not_found"}
            continue

        print(f"[REINSERT][{col_name}] Loading backup...")
        with open(backup_path) as f:
            data = _json.load(f)
        ids = data["ids"]
        docs = data["documents"]
        metas = data["metadatas"]
        total = len(ids)
        print(f"[REINSERT][{col_name}] Loaded {total} chunks")

        # Check which already exist
        existing = set()
        for i in range(0, total, 500):
            try:
                got = col_obj.get(ids=ids[i:i+500])
                existing.update(got["ids"])
            except Exception:
                pass
        print(f"[REINSERT][{col_name}] {len(existing)} already exist")

        todo_ids, todo_docs, todo_metas = [], [], []
        for i in range(total):
            if ids[i] not in existing:
                todo_ids.append(ids[i])
                todo_docs.append(docs[i])
                todo_metas.append(metas[i])

        remaining = len(todo_ids)
        if remaining == 0:
            results[col_name] = {"status": "nothing_to_do", "already_exist": len(existing), "count": col_obj.count()}
            print(f"[REINSERT][{col_name}] Nothing to insert")
            continue

        print(f"[REINSERT][{col_name}] Need to insert {remaining} chunks")
        inserted = 0
        for i in range(0, remaining, BATCH):
            b_ids = todo_ids[i:i+BATCH]
            b_docs = todo_docs[i:i+BATCH]
            b_metas = todo_metas[i:i+BATCH]

            body = {"model": OPENAI_EMBEDDING_MODEL, "input": b_docs}
            resp = requests.post(f"{OPENAI_URL}/embeddings", json=body, headers=headers, timeout=120)
            if resp.status_code != 200:
                print(f"[REINSERT][{col_name}][ERROR] Embedding API error: {resp.text[:400]}")
                results[col_name] = {"status": "error", "detail": resp.text[:400], "inserted_so_far": inserted}
                break
            emb_data = resp.json()
            embeddings = [item["embedding"] for item in sorted(emb_data["data"], key=lambda x: x["index"])]

            col_obj.add(ids=b_ids, documents=b_docs, metadatas=b_metas, embeddings=embeddings)
            inserted += len(b_ids)
            print(f"[REINSERT][{col_name}] {inserted}/{remaining} done")
        else:
            final_count = col_obj.count()
            print(f"[REINSERT][{col_name}] Complete! Inserted {inserted}, final count: {final_count}")
            results[col_name] = {"status": "done", "inserted": inserted, "skipped": len(existing), "count": final_count}

    return results