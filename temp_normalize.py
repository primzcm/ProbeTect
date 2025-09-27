from pathlib import Path
path = Path("quizzes/services.py")
text = path.read_text(encoding="utf-8")
text = text.replace('"\r\n"', '"\\n"')
text = text.replace('"\r\n\r\n"', '"\\n\\n"')
text = text.replace('(e.g., ?)', '(e.g., ?)')
path.write_text(text, encoding="utf-8")
