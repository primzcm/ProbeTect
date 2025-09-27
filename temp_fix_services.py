from pathlib import Path

path = Path("quizzes/services.py")
text = path.read_text(encoding="utf-8")
text = text.replace("(e.g., \\u2192) instead of literal \\u escapes", "(e.g., ?) instead of literal \\u escapes")
text = text.replace("literal \\u escapes", "literal \\u escapes")  # ensure double backslash
text = text.replace("literal \\u escapes", "literal \\\\u escapes")
text = text.replace("r\"\\u(?![0-9a-fA-F]{4})\"", "r\\"\\\\u(?![0-9a-fA-F]{4})\\"")
path.write_text(text, encoding="utf-8")
