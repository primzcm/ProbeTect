from __future__ import annotations

from pathlib import Path
import re

path = Path("quizzes/services.py")
text = path.read_text(encoding="utf-8")

pattern = re.compile(r"def generate_quiz\(material, \*, question_count: int = 5\) -> dict:\n\s+question_count = max\(1, min\(question_count, 10\)\)\n\s+text = extract_text\(material\)\n\s+chunks = chunk_text\(text\)\n\s+prompt = build_prompt\(chunks, question_count\)\n\s+return call_gemini\(prompt\)")
replacement = """def generate_quiz(material, *, question_count: int = 5) -> dict:\n    question_count = max(1, min(question_count, 10))\n    text = extract_text(material)\n    chunks = chunk_text(text)\n    prompt = build_prompt(chunks, question_count)\n    try:\n        return call_gemini(prompt)\n    except GeminiError as exc:\n        message = str(exc)\n        if 'MAX_TOKENS' in message and question_count > 5:\n            reduced_count = max(5, question_count - 2)\n            if reduced_count < question_count:\n                prompt = build_prompt(chunks, reduced_count)\n                quiz = call_gemini(prompt)\n                quiz['question_count'] = reduced_count\n                quiz['reduced_from'] = question_count\n                return quiz\n        raise"""
if not pattern.search(text):
    raise SystemExit("generate_quiz structure unexpected")
text = pattern.sub(replacement, text)
path.write_text(text, encoding="utf-8")
