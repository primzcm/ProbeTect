from pathlib import Path
path = Path("quizzes/services.py")
text = path.read_text(encoding="utf-8")
target = "    except json.JSONDecodeError:\r\n        cleaned = re.sub(r'\\u(?![0-9a-fA-F]{4})', '', cleaned)\r\n        try:\r\n"
replacement = "    except json.JSONDecodeError:\r\n        cleaned = re.sub(r'\\u(?![0-9a-fA-F]{4})', '', cleaned)\r\n        cleaned = cleaned.replace('\\\\', '\\')\r\n        try:\r\n"
if target not in text:
    raise SystemExit('target not found')
text = text.replace(target, replacement)
path.write_text(text, encoding="utf-8")
