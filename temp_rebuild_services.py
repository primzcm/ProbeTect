from pathlib import Path
import textwrap

content = textwrap.dedent('''
from __future__ import annotations

import json
import re
import textwrap
import urllib.error
import urllib.request
from io import BytesIO

from django.conf import settings

from materials.supabase import download_file

try:  # pragma: no cover - optional dependency
    from pypdf import PdfReader
except ImportError:  # pragma: no cover - handled at runtime
    PdfReader = None  # type: ignore[misc]


class GeminiError(RuntimeError):
    """Raised when Gemini quiz generation fails."""


def _pdf_bytes(material) -> bytes:
    if not material.storage_path:
        raise GeminiError("Material is missing a Supabase storage path.")
    try:
        return download_file(material.storage_path)
    except Exception as exc:  # pragma: no cover
        raise GeminiError(f"Unable to download PDF: {exc}") from exc


def extract_text(material) -> str:
    if PdfReader is None:
        raise GeminiError("pypdf is not installed. Run 'pip install pypdf'.")
    reader = PdfReader(BytesIO(_pdf_bytes(material)))
    parts: list[str] = []
    for page in reader.pages:
        try:
            parts.append(page.extract_text() or "")
        except Exception:  # pragma: no cover
            continue
    text = "\\n".join(filter(None, parts))
    if not text.strip():
        raise GeminiError("Could not extract text from PDF.")
    return text


def chunk_text(text: str, max_chars: int = 8000) -> list[str]:
    text = textwrap.dedent(text).strip()
    if len(text) <= max_chars:
        return [text]
    words = text.split()
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0
    for word in words:
        if current_len + len(word) + 1 > max_chars:
            chunks.append(" ".join(current))
            current = [word]
            current_len = len(word)
        else:
            current.append(word)
            current_len += len(word) + 1
    if current:
        chunks.append(" ".join(current))
    return chunks


def build_prompt(chunks: list[str], question_count: int) -> str:
    joined = "\\n\\n".join(chunks[:3])
    template = textwrap.dedent("""
        You are an AI tutor. Read the provided study material and create {question_count} high-quality multiple-choice questions.
        Each question must have exactly four answer choices, indicate the correct answer, and include a short explanation referencing the source material.
        Return STRICT JSON that matches this structure:
        {{
          "quiz_title": "string",
          "questions": [
            {{
              "prompt": "string",
              "choices": ["choice A", "choice B", "choice C", "choice D"],
              "correct_index": 0,
              "explanation": "string"
            }}
          ]
        }}
        Requirements:
        - Output must be valid JSON (RFC 8259) with no markdown, comments, or trailing commas.
        - The "choices" array must contain exactly four strings; separate each element with a comma.
        - Each question object except the last must end with a comma; do not add additional keys or sections.
        - Use plain Unicode characters (e.g., ?) and do not emit literal \\\\\\\\u escapes.
        """).strip()
    instructions = template.format(question_count=question_count)
    return f"{instructions}\\n\\nMaterial:\n{joined}"


def _extract_json_payload(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = [line for line in cleaned.splitlines() if not line.strip().startswith("```")]
        cleaned = "\\n".join(lines).strip()
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and start < end:
        return cleaned[start : end + 1]
    return cleaned


def call_gemini(prompt: str) -> dict:
    api_key = settings.GEMINI_API_KEY
    model = getattr(settings, "GEMINI_MODEL", "gemini-2.5-flash")
    if not api_key:
        raise GeminiError("GEMINI_API_KEY is not configured.")
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.4, "maxOutputTokens": 2048},
    }
    data = json.dumps(body).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:  # pragma: no cover
        detail = exc.read().decode(errors="ignore")
        raise GeminiError(f"Gemini API error {exc.code}: {detail[:200]}") from exc
    except urllib.error.URLError as exc:  # pragma: no cover
        raise GeminiError(f"Gemini network error: {exc.reason}") from exc

    payload = json.loads(raw)
    try:
        text = payload["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise GeminiError(f"Unexpected response from Gemini API: {payload}")
    cleaned = _extract_json_payload(text)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        cleaned = re.sub(r"\\u(?![0-9a-fA-F]{4})", "", cleaned)
        cleaned = cleaned.replace("\\\\", "\\")
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as exc:
            snippet = cleaned[:200]
            raise GeminiError(f"Gemini returned invalid JSON: {exc}. Payload snippet: {snippet}") from exc


def generate_quiz(material, *, question_count: int = 5) -> dict:
    question_count = max(1, min(question_count, 10))
    text = extract_text(material)
    chunks = chunk_text(text)
    prompt = build_prompt(chunks, question_count)
    return call_gemini(prompt)
''')

path = Path('quizzes/services.py')
path.write_text(content, encoding='utf-8')

