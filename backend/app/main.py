import os
import uuid
import pathlib
import time
import traceback
from typing import List, Optional, Tuple, Dict, Any, Deque
import random
from collections import defaultdict, deque

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
import json
import mimetypes
from io import BytesIO
from urllib.parse import unquote

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

try:
    import csv
    HAS_CSV = True
except ImportError:
    HAS_CSV = False

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

# Directory exposed for "Add Knowledge" server file listing
KNOWLEDGE_DIR = os.getenv("KNOWLEDGE_DIR", WIKI_ROOT)

CHROMA_DIR = os.getenv("CHROMA_DIR", "/app/chroma_db")

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
COLLECTION_NAME = "Intsight"
MEMORY_COLLECTION_NAME = "New_Knowledge"
PDF_MAX_PAGES = int(os.getenv("PDF_MAX_PAGES", "0"))
PDF_OCR_ENABLED = os.getenv("PDF_OCR_ENABLED", "true").lower() in ("1", "true", "yes")
PDF_OCR_MAX_PAGES = int(os.getenv("PDF_OCR_MAX_PAGES", "25"))
PDF_TABLE_EXTRACTION_ENABLED = os.getenv("PDF_TABLE_EXTRACTION_ENABLED", "true").lower() in ("1", "true", "yes")
VISION_MAX_TOKENS = int(os.getenv("VISION_MAX_TOKENS", "1200"))
TABLE_ROW_START_TAG = "[TABLE_ROW]"
TABLE_ROW_END_TAG = "[/TABLE_ROW]"

app = FastAPI(title="Wiki RAG API")

# Track if a structured "first ticket response" was already sent per ticket key (id or URL fallback)
ticket_first_reply_done: Dict[str, bool] = {}

# Lightweight in-memory conversation memory (per conversation key)
MAX_CONVERSATION_MESSAGES = 12
conversation_store: Dict[str, Deque[Dict[str, str]]] = defaultdict(
    lambda: deque(maxlen=MAX_CONVERSATION_MESSAGES)
)


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
    Supports both HTTP(S) URLs and data URIs (base64 encoded images).
    """
    try:
        # Accept both URLs and data URIs
        if not (image_url.startswith("http://") or image_url.startswith("https://") or image_url.startswith("data:image/")):
            print(f"[VISION][WARN] Invalid image URL format: {image_url[:60]}...")
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
            "max_tokens": 300,
        }
        resp = requests.post(f"{OPENAI_URL}/chat/completions", json=body, headers=headers, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            description = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            print(f"[VISION] Described image {image_url[:60]}... -> {description[:100]}...")
            return description
        else:
            print(f"[VISION][WARN] Vision call failed for {image_url}: {resp.status_code} {resp.text[:200]}")
            return f"[Image analysis unavailable]"
    except Exception as e:
        print(f"[VISION][WARN] Failed to describe image {image_url[:60]}...: {e}")
        return f"[Image analysis unavailable]"


def _extract_structured_text_from_image(image_ref: str, source_label: str = "image") -> str:
    """
    Extract OCR-style text from an image and preserve table content as markdown.
    """
    if not OPENAI_API_KEY:
        return ""

    try:
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
        body = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Extract all readable text from this image exactly as it appears. "
                                "If there are tables, output each table in markdown table format and preserve row/column values. "
                                "Do not summarize. Do not omit rows. If text is unclear, mark it as [unclear]."
                            ),
                        },
                        {"type": "image_url", "image_url": {"url": image_ref}},
                    ],
                }
            ],
            "max_tokens": VISION_MAX_TOKENS,
            "temperature": 0,
        }
        resp = requests.post(f"{OPENAI_URL}/chat/completions", json=body, headers=headers, timeout=120)
        if resp.status_code != 200:
            print(f"[VISION][WARN] OCR extraction failed for {source_label}: {resp.status_code} {resp.text[:200]}")
            return ""
        data = resp.json()
        text = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        if text:
            print(f"[VISION] OCR extraction success for {source_label}, len={len(text)}")
        return text
    except Exception as e:
        print(f"[VISION][WARN] OCR extraction error for {source_label}: {e}")
        return ""


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

def process_uploaded_file(file_data: Dict[str, str], describe_image_func=None) -> str:
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
        
        # Route to appropriate handler
        if file_ext in POPULAR_IMAGE_EXTS or (file_type and file_type.startswith("image/")):
            return _process_image_file(file_name, file_b64, file_type, describe_image_func)
        elif file_ext in POPULAR_EXCEL_EXTS:
            return _process_excel_file(file_name, file_bytes)
        elif file_ext == "csv":
            return _process_csv_file(file_name, file_bytes)
        elif file_ext == "pdf":
            return _process_pdf_file(file_name, file_bytes)
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
        if not describe_func:
            return f"[Image file {file_name} - processing not available]"

        # Decode base64 to bytes for potential conversion
        try:
            file_bytes = base64.b64decode(file_b64)
        except Exception as e:
            print(f"[FILE] Failed to decode base64 for image {file_name}: {e}")
            return f"[Image file {file_name} - invalid base64 data]"

        # Determine mime type
        mime_type = None
        if file_type and file_type.startswith("image/"):
            mime_type = file_type
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
            data_uri = f"data:{mime_type};base64,{file_b64}"

        image_description = _extract_structured_text_from_image(data_uri, source_label=file_name)
        if not image_description and describe_func:
            image_description = describe_func(data_uri)
        if not image_description:
            image_description = "[Image analysis unavailable]"
        return f"[Image Content from {file_name}]\n{image_description}"
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


def _process_pdf_file(file_name: str, file_bytes: bytes) -> str:
    """Extract text from PDF file."""
    try:
        import PyPDF2
        pdf_file = BytesIO(file_bytes)
        reader = PyPDF2.PdfReader(pdf_file)

        total_pages = len(reader.pages)
        pages_to_process = total_pages
        if PDF_MAX_PAGES > 0:
            pages_to_process = min(total_pages, PDF_MAX_PAGES)

        content_lines = [f"**File: {file_name}** ({total_pages} pages)\n"]

        plumber_doc = None
        if HAS_PDFPLUMBER and PDF_TABLE_EXTRACTION_ENABLED:
            try:
                plumber_doc = pdfplumber.open(BytesIO(file_bytes))
            except Exception as e:
                print(f"[FILE][PDF][WARN] pdfplumber open failed for {file_name}: {e}")

        pymupdf_doc = None
        if HAS_PYMUPDF and PDF_OCR_ENABLED and OPENAI_API_KEY:
            try:
                pymupdf_doc = fitz.open(stream=file_bytes, filetype="pdf")
            except Exception as e:
                print(f"[FILE][PDF][WARN] PyMuPDF open failed for {file_name}: {e}")

        for page_idx in range(pages_to_process):
            page = reader.pages[page_idx]
            page_lines: List[str] = [f"\n--- Page {page_idx + 1} ---"]

            text = _extract_text_from_pypdf2_page(page)
            if text and text.strip():
                page_lines.append(text)

            table_count = 0
            if plumber_doc and page_idx < len(plumber_doc.pages):
                try:
                    tables = plumber_doc.pages[page_idx].extract_tables() or []
                    for table_idx, table_rows in enumerate(tables, start=1):
                        table_md = _format_table_rows_as_markdown(table_rows)
                        if table_md:
                            table_count += 1
                            page_lines.append(f"\n[Table {table_idx}]\n{table_md}")
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
                and page_idx < max(0, PDF_OCR_MAX_PAGES)
                and (not text.strip() or table_count == 0)
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
                    )
                    if ocr_text:
                        page_lines.append("\n[OCR Content]\n" + ocr_text)
                except Exception as e:
                    print(f"[FILE][PDF][WARN] OCR fallback failed page={page_idx + 1}: {e}")

            if len(page_lines) == 1:
                page_lines.append("[No extractable text found on this page]")

            content_lines.append("\n".join(page_lines))

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


def build_file_context(files: Optional[List[Dict[str, str]]], describe_image_func=None) -> str:
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
    
    file_contents = []
    for file_data in files:
        content = process_uploaded_file(file_data, describe_image_func)
        file_contents.append(content)
    
    combined = "\n\n---FILE SEPARATOR---\n\n".join(file_contents)
    print(f"[FILE] Extracted content from {len(files)} files, total length={len(combined)}")
    return combined


def _safe_resolve_path(root_dir: str, rel_path: str) -> str:
    """Resolve a relative path safely within root_dir."""
    root_abs = os.path.abspath(root_dir)
    candidate = os.path.abspath(os.path.join(root_abs, rel_path))
    if not candidate.startswith(root_abs + os.sep) and candidate != root_abs:
        raise RuntimeError("Invalid path outside knowledge directory")
    return candidate


def _list_server_files(root_dir: str) -> List[dict]:
    """List files under the knowledge directory for server-file selection."""
    allowed_exts = {
        ".md", ".markdown", ".txt", ".rst", ".csv", ".tsv", ".log", ".ini", ".cfg", ".conf", ".properties",
        ".json", ".jsonl", ".xml", ".yaml", ".yml", ".toml", ".sql",
        ".pdf", ".doc", ".docx", ".rtf", ".odt", ".eml", ".msg",
        ".xlsx", ".xls", ".xlsm", ".xltx", ".xltm", ".xlsb", ".ods",
        ".ppt", ".pptx", ".odp",
        ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tif", ".tiff", ".svg", ".ico", ".heic", ".heif", ".avif", ".jfif",
        ".zip", ".rar", ".7z", ".tar", ".gz",
        ".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac",
        ".mp4", ".mkv", ".mov", ".avi", ".wmv", ".webm",
    }
    files = []
    root_abs = os.path.abspath(root_dir)
    for base, _, names in os.walk(root_abs):
        for name in names:
            ext = os.path.splitext(name)[1].lower()
            if allowed_exts and ext not in allowed_exts:
                continue
            abs_path = os.path.join(base, name)
            rel_path = os.path.relpath(abs_path, root_abs)
            try:
                stat = os.stat(abs_path)
                files.append({
                    "path": rel_path.replace("\\", "/"),
                    "size": stat.st_size,
                    "modified": int(stat.st_mtime),
                })
            except Exception:
                continue
    files.sort(key=lambda x: x["path"].lower())
    return files


def _process_local_file(file_path: str) -> str:
    """Process a local file path into text for ingestion."""
    file_name = os.path.basename(file_path)
    ext = os.path.splitext(file_name)[1].lower().lstrip(".")
    try:
        with open(file_path, "rb") as f:
            file_bytes = f.read()
    except Exception as e:
        return f"[ERROR] Failed to read file {file_name}: {e}"

    if ext in POPULAR_IMAGE_EXTS:
        desc = _describe_local_image_via_vision(file_path)
        if not desc:
            return f"[Image file {file_name} - analysis unavailable]"
        return f"[Image Content from {file_name}]\n{desc}"
    if ext in POPULAR_EXCEL_EXTS:
        return _process_excel_file(file_name, file_bytes)
    if ext == "csv":
        return _process_csv_file(file_name, file_bytes)
    if ext == "pdf":
        return _process_pdf_file(file_name, file_bytes)
    if ext in {"doc", "docx"}:
        return _process_word_file(file_name, file_bytes)
    if ext in POPULAR_OTHER_EXTS:
        return _process_unstructured_popular_file(file_name, ext)
    return _process_text_file(file_name, file_bytes)


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
        "translation", "system config", "localization",
    ]
    integration_terms = [
        "kerberos", "krb5", "krb5.conf", "krb5.keytab", "keytab", "spn", "realm", "kdc",
        "mssql", "sql server", "odbc", "odbc.ini", "trusted_connection", "integratedsecurity",
        "authmech", "krbservicename", "krbhostfqdn", "krbauthrealm", "active directory",
        "domain controller", "dc", "ad user",
    ]

    workflow_hits = sum(1 for term in workflow_terms if term in t)
    technical_hits = sum(1 for term in technical_terms if term in t)
    artifact_hits = sum(1 for term in product_artifacts if term in t)
    integration_hits = sum(1 for term in integration_terms if term in t)

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

    return False


def _validate_ta9_knowledge_content(content_text: str) -> Tuple[bool, str]:
    """Comprehensive validation for TA9/IntSight knowledge ingestion with explicit rejection reason."""
    text = (content_text or "").strip()
    if not text:
        return False, "The content is empty. Please provide TA9-related details before adding knowledge."

    fallback_reason = (
        "The content was rejected because it is not specific to TA9/IntSight. "
        "Please include concrete IntSight/TA9 details such as module names, admin/configuration steps, "
        "permissions, data model/entity behavior, integration settings, troubleshooting context, or procedures."
    )

    # Heuristic domain and substance gates (comprehensive)
    has_strong_ta9_signal = _has_ta9_context(text)
    has_support_signal = _has_ta9_support_signal(text)

    # If both domain and support signals are strong, approve early to avoid LLM false negatives.
    # This is especially important for technical integration/configuration runbooks.
    if has_strong_ta9_signal and has_support_signal:
        return True, "Approved"

    # Reject very short, low-information text unless it has very strong product context.
    text_word_count = len(re.findall(r"\b\w+\b", text))
    if text_word_count < 12 and not (has_strong_ta9_signal and has_support_signal):
        return False, (
            "The content is too short to be useful for support retrieval. "
            "Please add specific TA9/IntSight details, steps, or technical context."
        )

    if not has_strong_ta9_signal and not OPENAI_API_KEY:
        return False, fallback_reason

    # LLM gate for meaningfulness and domain relevance (authoritative verdict)
    if OPENAI_API_KEY:
        prompt = (
            "You are a strict-but-practical validator for TA9/IntSight RAG ingestion. "
            "Decide whether the submitted content is meaningful and domain-relevant for TA9.\n\n"
            "Approval criteria (ALL required):\n"
            "1) Clearly tied to TA9/IntSight product usage, administration, configuration, integration, troubleshooting, or operations.\n"
            "2) Contains concrete support-relevant details such as modules, roles/permissions, fields, entities/relations, workflows, settings, queries, endpoints, errors, or procedures.\n"
            "3) Useful for retrieval by support/admin/analyst teams (can be user-guide, runbook, config guide, FAQ, or troubleshooting instructions).\n"
            "4) Not purely irrelevant/general text unrelated to TA9/IntSight.\n\n"
            "If not approved, explain briefly what is missing.\n"
            "Return ONLY valid JSON with this exact schema:\n"
            "{\"approved\": true|false, \"reason\": \"short reason\"}\n\n"
            f"Content to validate:\n{text}"
        )
        try:
            verdict_raw = (call_llm(prompt, temperature=0.0) or "").strip()
            verdict_text = verdict_raw
            if verdict_text.startswith("```"):
                verdict_text = re.sub(r"^```(?:json)?\s*", "", verdict_text)
                verdict_text = re.sub(r"\s*```$", "", verdict_text).strip()
            parsed = json.loads(verdict_text)
            approved = bool(parsed.get("approved", False))
            reason = str(parsed.get("reason") or "").strip()
            if approved:
                # Keep domain integrity: require explicit TA9 context OR strong support signal.
                if not has_strong_ta9_signal and not has_support_signal:
                    return False, (
                        "The content appears structured but lacks clear TA9/IntSight context. "
                        "Please mention relevant modules, workflows, admin/configuration concepts, or product terms."
                    )
                return True, "Approved"
            return False, reason or fallback_reason
        except Exception as e:
            print(f"[KNOWLEDGE][WARN] LLM validation parse/exec failed: {e}")
            return (False, fallback_reason) if not (has_strong_ta9_signal and has_support_signal) else (True, "Approved")

    return (True, "Approved") if (has_strong_ta9_signal and has_support_signal) else (False, fallback_reason)


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
    Minimal augmentation: only expand very short questions with common synonyms.
    Keep general-purpose for any domain.
    """
    if not question or len(question.split()) > 15:
        # Only augment genuinely short queries
        return question
    
    q_low = question.lower()
    synonyms: List[str] = []
    
    # Minimal, general augmentation for short queries
    if "how" in q_low or "add" in q_low or "create" in q_low:
        synonyms.extend(["how to", "instructions", "steps", "procedure", "create", "add", "setup", "configure"])
    
    if "what" in q_low:
        synonyms.extend(["definition", "explanation", "description", "overview"])
    
    if "help" in q_low or "issue" in q_low or "problem" in q_low:
        synonyms.extend(["troubleshooting", "solution", "fix", "resolve", "error"])
    
    if not synonyms:
        return question
    
    augmented = question + "\n" + " ".join(set(synonyms))
    return augmented


def lexical_boost_score(question: str, doc: str, meta: dict) -> float:
    """
    Simple, general-purpose lexical score.
    Avoid domain-specific biases; reward token overlap and user-added content.
    """
    if doc is None:
        doc = ""
    
    q = question.lower()
    d = doc.lower()
    source = str(meta.get("source", "")).lower()
    score = 0.0
    
    # Basic lexical overlap reward
    q_tokens = set([t for t in q.replace("\n", " ").split() if len(t) > 3])
    matched = sum(1 for t in q_tokens if t in d)
    if matched > 0:
        score += min(3.0, matched * 0.5)
    
    # Source name match
    for tok in q_tokens:
        if tok in source:
            score += 1.0
    
    # User-added content priority
    if meta and meta.get("priority") in ["user_upload", "user_upload_high"]:
        score += 2.0
    if meta and meta.get("supersedes"):
        score += 1.0
    
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
        col = meta.get("collection", "unknown") if meta else "unknown"
        source_key = source  # Use full source as key
        
        # Memory collection gets priority: allow more chunks from memory sources
        max_allowed = 5 if col == "user_knowledge" else max_chunks_per_source
        
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
            
            sim = _content_similarity(doc, seen_doc, threshold=adaptive_threshold)
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


def _is_context_relevant(
    question: str,
    docs: List[str],
    distances: Optional[List[float]],
    max_distance: float = 0.50,
    min_overlap: float = 0.05,
) -> bool:
    """
    Intelligent answerability gate with adaptive thresholds.
    Pure query-length based: short queries get lenient thresholds universally.
    """
    if not docs:
        return False
    
    # Only query length matters - no domain-specific checks
    is_short = _is_short_query(question)
    
    # For short queries, be much more lenient (this fixes "add new department" issue)
    if is_short:
        effective_max_distance = 0.60  # Very lenient for short queries
        effective_min_overlap = 0.01   # Accept 1% word overlap
    else:
        effective_max_distance = max_distance
        effective_min_overlap = min_overlap
    
    # Check semantic distance
    best_dist = None
    if distances:
        best_dist = min(distances)
    if best_dist is not None and best_dist > effective_max_distance:
        return False
    
    # Check lexical overlap
    top_docs = [d for d in docs[:5] if d is not None]
    if not top_docs:
        return False
    
    max_overlap = max((_lexical_overlap_ratio(question, d) for d in top_docs), default=0.0)
    return max_overlap >= effective_min_overlap


def _generate_contextual_rejection(question: str, docs: List[str] = None) -> str:
    """
    Generate an intelligent, question-aware rejection response using the LLM.
    Makes the rejection feel natural and contextual rather than robotic.
    """
    if not OPENAI_API_KEY:
        return (
            "I don't have enough information in the knowledge base to answer that. "
            "Could you provide more context or ask about a specific technical issue?"
        )
    
    try:
        # Build a prompt that generates a flexible, natural rejection
        rejection_prompt = (
            "You are a helpful technical support assistant. The user asked a question, but there isn't "
            "relevant information in the knowledge base to answer it properly.\n\n"
            f"User's question: {question}\n\n"
            "Generate a SHORT (1-2 sentences), friendly response that:\n"
            "- Acknowledges what they're asking about\n"
            "- Explains you don't have specific information on this topic\n"
            "- Suggests they provide more context or ask about technical documentation/issues\n\n"
            "Be conversational and helpful. Don't mention \"viewing images\" or \"can't view\" - just focus on not having information.\n"
            "Response:"
        )
        
        rejection = call_llm(rejection_prompt, temperature=0.3)
        return rejection.strip() if rejection else (
            "I don't have specific information about that in the knowledge base. "
            "Could you provide more details or ask about a technical issue I can help with?"
        )
    except Exception as e:
        print(f"[REJECTION][WARN] Failed to generate contextual rejection: {e}")
        return (
            "I don't have information about that in the knowledge base. "
            "Could you provide more context about the technical issue you're facing?"
        )


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


def _get_vector_collection(collection_name: str):
    normalized_name = (collection_name or "").strip()
    if normalized_name == COLLECTION_NAME:
        return collection
    if normalized_name == MEMORY_COLLECTION_NAME:
        return memory_collection
    raise HTTPException(status_code=400, detail=f"Unknown collection: {collection_name}")


def _vector_collection_description(collection_name: str) -> str:
    if collection_name == COLLECTION_NAME:
        return "Primary operational knowledge base"
    if collection_name == MEMORY_COLLECTION_NAME:
        return "User-added and curated knowledge"
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


def _merge_chunk_texts(chunks: List[str]) -> str:
    if not chunks:
        return ""
    merged = chunks[0]
    for chunk in chunks[1:]:
        overlap_size = _find_chunk_overlap(merged, chunk)
        merged += chunk[overlap_size:]
    return merged


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
        merged_text = _merge_chunk_texts([item["document"] for item in items])
        preview = re.sub(r"\s+", " ", merged_text).strip()[:280]
        title = _build_document_title(source, items[0]["document"] if items else "")
        summaries.append(
            {
                "source": source,
                "title": title,
                "display_source": _display_source_name(source),
                "preview": preview,
                "chunk_count": len(items),
                "updated_at": payload["updated_at"] or None,
            }
        )

    summaries.sort(key=lambda item: ((item["updated_at"] or ""), item["title"].lower()), reverse=True)
    return summaries


def _build_vector_document_detail(collection_name: str, source: str) -> dict:
    target_collection = _get_vector_collection(collection_name)
    raw = target_collection.get(
        where={"source": source},
        include=["documents", "metadatas", "embeddings"],
    )

    ids = list(raw.get("ids", []) or [])
    if not ids:
        raise HTTPException(status_code=404, detail="Document not found")

    docs = list(raw.get("documents", []) or [])
    metas = list(raw.get("metadatas", []) or [])
    embeddings = raw.get("embeddings")
    if embeddings is None:
        embeddings = [None] * len(ids)

    chunk_items: List[dict] = []
    for doc_id, doc_text, meta, embedding in zip(ids, docs, metas, embeddings):
        safe_meta = meta or {}
        chunk_index = int(safe_meta.get("chunk", 0) or 0)
        chunk_items.append(
            {
                "id": doc_id,
                "chunk": chunk_index,
                "content": doc_text or "",
                "metadata": safe_meta,
                "embedding": _safe_embedding_to_list(embedding),
            }
        )

    chunk_items.sort(key=lambda item: item["chunk"])
    full_content = _merge_chunk_texts([item["content"] for item in chunk_items])
    title = _build_document_title(source, chunk_items[0]["content"] if chunk_items else "")
    vector_dimensions = len(chunk_items[0]["embedding"]) if chunk_items and chunk_items[0]["embedding"] else 0
    updated_at = None
    for item in chunk_items:
        safe_meta = item["metadata"] or {}
        candidate_timestamp = safe_meta.get("edited_at") or safe_meta.get("uploaded_at") or safe_meta.get("created_at")
        if candidate_timestamp and (updated_at is None or str(candidate_timestamp) > str(updated_at)):
            updated_at = str(candidate_timestamp)

    return {
        "collection_name": collection_name,
        "collection_description": _vector_collection_description(collection_name),
        "source": source,
        "title": title,
        "display_source": _display_source_name(source),
        "chunk_count": len(chunk_items),
        "vector_dimensions": vector_dimensions,
        "updated_at": updated_at,
        "full_content": full_content,
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

    chunks = (
        chunk_text_preserve_table_rows(clean_content)
        if TABLE_ROW_START_TAG in clean_content
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


class VectorDbDocumentUpdateRequest(BaseModel):
    collection_name: str
    source: str
    content: str


class VectorDbDocumentDeleteRequest(BaseModel):
    collection_name: str
    source: str


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
        "memory_collection_name": MEMORY_COLLECTION_NAME,
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


@app.post("/knowledge/add")
def knowledge_add(req: KnowledgeAddRequest):
    """Add a knowledge item from user-provided content."""
    try:
        mode = (req.mode or "").strip().lower()
        content_text = ""
        source_name = ""
        target_collection = memory_collection
        collection_label = "user_knowledge"

        if mode == "content":
            text_part = (req.text or "").strip()
            file_part = ""
            if req.files:
                file_part = build_file_context(req.files, describe_image_func=_describe_image_via_vision)
            content_text = "\n\n".join([p for p in [text_part, file_part] if p])
            source_name = f"user:content:{uuid.uuid4()}"
        else:
            raise HTTPException(status_code=400, detail="mode must be content")

        if not content_text.strip():
            raise HTTPException(status_code=400, detail="No content to ingest")

        similar_sources = _find_similar_knowledge_sources(content_text)
        priority = "user_upload_high" if similar_sources else "user_upload"

        # Strict TA9 meaningfulness validation
        is_valid_ta9_content, rejection_reason = _validate_ta9_knowledge_content(content_text)
        if not is_valid_ta9_content:
            return {
                "approved": False,
                "message": rejection_reason,
            }

        # Chunk + embed + add to collection with priority metadata
        chunks = chunk_text_preserve_table_rows(content_text) if req.files else chunk_text(content_text)
        if not chunks:
            raise HTTPException(status_code=400, detail="No chunks generated from content")

        ids: List[str] = []
        docs: List[str] = []
        metas: List[dict] = []
        embeds: List[List[float]] = []
        uploaded_at = datetime.utcnow().isoformat() + "Z"

        for i, ch in enumerate(chunks):
            try:
                emb = embed_text(ch)
            except Exception as e:
                print(f"[KNOWLEDGE][ERROR] Embedding failed chunk={i}: {e}")
                traceback.print_exc()
                continue
            metadata = {
                "source": source_name,
                "chunk": i,
                "priority": priority,
                "uploaded_at": uploaded_at,
                "mode": mode,
                "path": "",
                "collection": collection_label,
            }
            if ch.startswith(TABLE_ROW_START_TAG):
                metadata["chunk_type"] = "table_row"
                metadata.update(extract_table_row_metadata(ch))
            else:
                metadata["chunk_type"] = "text"
            if similar_sources:
                metadata["supersedes"] = similar_sources
            ids.append(str(uuid.uuid4()))
            docs.append(ch)
            metas.append(metadata)
            embeds.append(emb)

        if not ids:
            raise HTTPException(status_code=500, detail="Failed to embed any chunks")

        target_collection.add(ids=ids, documents=docs, metadatas=metas, embeddings=embeds)
        return {
            "approved": True,
            "message": "Knowledge added successfully and prioritized.",
            "chunks_added": len(ids),
            "source": source_name,
            "priority": priority,
            "supersedes": similar_sources,
        }
    except HTTPException:
        raise
    except Exception as exc:
        print(f"[API][KNOWLEDGE][ERROR] add failed: {exc}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(exc))


def _prepare_rag_content(raw_text: str) -> str:
    """Normalize and structure knowledge content for better RAG ingestion."""
    if not raw_text.strip():
        return ""
    if not OPENAI_API_KEY:
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
    """Find existing knowledge sources that are highly similar to the provided text."""
    if not text.strip():
        return []
    if not OPENAI_API_KEY:
        return []
    try:
        emb = embed_text(text)
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
    """Prepare user content for RAG and return the normalized text."""
    try:
        text_part = (req.text or "").strip()
        file_part = ""
        if req.files:
            file_part = build_file_context(req.files, describe_image_func=_describe_image_via_vision)

        raw_content = "\n\n".join([p for p in [text_part, file_part] if p])
        if not raw_content.strip():
            raise HTTPException(status_code=400, detail="No content to prepare")

        is_valid_ta9_content, rejection_reason = _validate_ta9_knowledge_content(raw_content)
        if not is_valid_ta9_content:
            return {
                "approved": False,
                "message": rejection_reason,
                "prepared_text": raw_content,
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
    print(f"[API][CHAT] /chat called question='{req.question[:200]}' top_k={req.top_k} force_reingest={req.force_reingest} files={len(req.files) if req.files else 0}")
    question = (req.question or "").strip()

    conversation_key = (req.conversation_id or req.ticket_url or "default").strip() or "default"
    incoming_history = _normalize_history_messages(req.history)
    if incoming_history:
        dq = deque(incoming_history[-MAX_CONVERSATION_MESSAGES:], maxlen=MAX_CONVERSATION_MESSAGES)
        conversation_store[conversation_key] = dq
    stored_history = list(conversation_store.get(conversation_key, deque()))
    history_context = _format_history_for_prompt(stored_history, max_messages=8)
    if history_context:
        print(f"[API][CHAT] Using conversation history context key={conversation_key} messages={len(stored_history)}")

    # Process uploaded files early to include their content in context
    file_context = ""
    if req.files:
        try:
            file_context = build_file_context(req.files, describe_image_func=_describe_image_via_vision)
            if file_context:
                print(f"[API][CHAT] Extracted file context: {len(file_context)} characters")
        except Exception as e:
            print(f"[API][CHAT][WARN] File processing failed: {e}")
            file_context = ""

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
    if history_context:
        history_seed = f"Conversation context:\n{history_context}\n\nCurrent question:\n{question}"
        query_variants = [history_seed] + query_variants
        query_variants = query_variants[:4]
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
        try:
            conversation_store[conversation_key].append({"role": "user", "content": question})
            conversation_store[conversation_key].append({"role": "assistant", "content": answer})
        except Exception as e:
            print(f"[API][CHAT][WARN] Failed to persist conversation context: {e}")
        return ChatResponse(answer=answer, sources=[])

    docs, metas, distances, ids = rerank_results(question, docs, metas, distances=distances, ids=ids)

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
    
    # Only include RAG context if files are NOT attached or if context is highly relevant
    # When user attaches files, they want analysis of those files, not wiki docs
    should_include_rag_context = True
    if file_context:
        # Files attached: only include RAG context if it's highly relevant (very short distance)
        # Check if best doc has good relevance
        best_distance = distances[0] if distances else 1.0
        should_include_rag_context = best_distance < 0.5  # Very strict: only highly relevant docs
        if not should_include_rag_context:
            print(f"[API][CHAT] Skipping RAG context: best_distance={best_distance} (>= 0.5 threshold). User has file context, prioritizing that.")
    
    if context_text and should_include_rag_context:
        # Wiki context is always supplemental
        priority_label = "REFERENCE" if (file_context or selected_ticket_text) else "PRIMARY"
        context_sections.append(
            f"=== KNOWLEDGE BASE ({priority_label}) ===\n"
            f"{context_text}\n"
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
    
    combined_context = "\n\n".join(context_sections)

    prompt = (
        "You are a TA9 / IntSight customer support assistant with deep technical knowledge. "
        "Your role is to provide clear, accurate, and helpful answers in a natural, conversational way.\n\n"
        "INSTRUCTIONS:\n"
        "1. When the user attaches files (images, documents), those files are your PRIMARY source - answer directly from them.\n"
        "2. When you see [Image Content from ...] sections, that means the image has been analyzed - describe what you see in the analysis naturally.\n"
        "3. For images: Provide a comprehensive explanation of what is shown in the provided analysis. Highlight key details, technical context, and likely causes when relevant.\n"
        "4. When a ticket is selected, use it to understand the user's issue and provide relevant solutions.\n"
        "5. Use knowledge base context to supplement your answer or provide additional related information.\n"
        "6. Use fenced code blocks (```bash, ```python, ```sql, etc.) for any commands or code snippets.\n"
        "7. If the context contains redundant or overlapping information, synthesize it into a single coherent answer.\n"
        "8. Do NOT repeat information from different sources - intelligently merge related points.\n"
        "8.1 Use a balanced approach across both collections (Intsight and New_Knowledge) and do not assume one is always better.\n"
        "8.2 If relevant details are split across both collections, combine them into one integrated, consistent answer.\n"
        "9. Grounding is mandatory: only state facts supported by the provided context sections.\n"
        "9.1 If a requested detail is not in context, explicitly say it is not available in the current knowledge context.\n"
        "9.2 Never invent commands, configuration keys, UI paths, API names, or procedural steps.\n"
        "10. Keep a professional, helpful tone that encourages follow-up questions.\n"
        "11. Answer naturally and conversationally - avoid rigid structured formats unless specifically requested.\n"
        "12. For Intsight or system configuration guidance, prioritize instructions that use Admin Studio (UI-based configuration) by default.\n"
        "13. Provide database-level (DB) configuration instructions only when the user explicitly asks for DB configuration, SQL/database changes, or backend table-level steps.\n"
        "14. Never hard-refuse when at least partial context exists; provide the best grounded answer possible, explicitly flag uncertainty, and ask one focused clarifying question if needed.\n"
        f"{foundational_instruction}"
        f"{ta9_instruction}\n"
        f"{combined_context}\n\n"
        f"Question: {question}\n\n"
        "Answer:"
    )

    try:
        draft_answer = call_llm(prompt, temperature=0.2)
        answer = _ground_answer_against_context(question, combined_context, draft_answer)
        answer = _enforce_specific_grounded_answer(question, combined_context, answer)
    except Exception as exc:
        print(f"[API][CHAT][ERROR] LLM call failed: {exc}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"LLM call failed: {exc}")

    try:
        conversation_store[conversation_key].append({"role": "user", "content": question})
        conversation_store[conversation_key].append({"role": "assistant", "content": answer})
    except Exception as e:
        print(f"[API][CHAT][WARN] Failed to persist conversation context: {e}")

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
