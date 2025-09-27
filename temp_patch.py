from pathlib import Path

path = Path("quizzes/services.py")
text = path.read_text(encoding="utf-8")

if "def _repair_json" not in text:
    insert = """

def _repair_json(cleaned: str) -> str | None:
    patched, replacements = re.subn(r'}(\s*)(?=\{\"prompt\")', r'},\\1', cleaned)
    return patched if replacements else None
"""
    idx = text.index("def _extract_json_payload")
    text = text[:idx] + insert + text[idx:]
else:
    text = re.sub(
        r"def _repair_json\(cleaned: str\) -> str \| None:[\s\S]*?return f\"\{cleaned\[:match.start\(\)\]}\{prefix\}\{patched_body\}\{suffix\}\{cleaned\[match.end\(\)\]:\}\"",
        "def _repair_json(cleaned: str) -> str | None:\n    patched, replacements = re.subn(r'}(\\s*)(?=\\{\\\"prompt\\\")', r'},\\1', cleaned)\n    return patched if replacements else None",
        text,
        flags=re.MULTILINE,
    )

requirements_pattern = re.compile(
    r"(Return STRICT JSON.*?Requirements:[\s\S]*?)- Use plain Unicode characters \(e\.g\., ?\) and do not emit literal \\\\u escapes\."
)
text = requirements_pattern.sub(
    r"\1- Use plain Unicode characters (e.g., ?) and do not emit literal \\u escapes.\n        - Do not introduce extra sections or keys.",
    text,
)

text = text.replace(
    "except json.JSONDecodeError:\n        cleaned = re.sub(r\"\\u(?![0-9a-fA-F]{4})\", \"\", cleaned)\n        cleaned = cleaned.replace(\"\\\\", \"\\\")\n        try:\n            return json.loads(cleaned)\n        except json.JSONDecodeError as exc:\n            snippet = cleaned[:200]\n            raise GeminiError(f\"Gemini returned invalid JSON: {exc}. Payload snippet: {snippet}\") from exc\n",
    "except json.JSONDecodeError:\n        cleaned = re.sub(r\"\\u(?![0-9a-fA-F]{4})\", \"\", cleaned)\n        cleaned = cleaned.replace(\"\\\\", \"\\\")\n        try:\n            return json.loads(cleaned)\n        except json.JSONDecodeError:\n            repaired = _repair_json(cleaned)\n            if repaired:\n                try:\n                    return json.loads(repaired)\n                except json.JSONDecodeError:\n                    cleaned = repaired\n            try:\n                return json.loads(cleaned)\n            except json.JSONDecodeError as exc:\n                snippet = cleaned[:200]\n                raise GeminiError(f\"Gemini returned invalid JSON: {exc}. Payload snippet: {snippet}\") from exc\n",
)

path.write_text(text, encoding="utf-8")
