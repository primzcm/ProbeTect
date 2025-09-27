from pathlib import Path

path = Path("quizzes/views.py")
text = path.read_text(encoding="utf-8")
old = "            else:\n            questions = payload.get(\"questions\", [])\n"
if old not in text:
    raise SystemExit('expected else block not found')
new = "            else:\n                reduced_from = payload.pop('reduced_from', None) if isinstance(payload, dict) else None\n                questions = payload.get('questions', [])\n                if reduced_from:\n                    actual = payload.get('question_count', len(questions))\n                    messages.warning(request, f'Gemini could only generate {actual} questions instead of {reduced_from}.')\n"
text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')
