from pathlib import Path
import re

path = Path("quizzes/views.py")
text = path.read_text(encoding="utf-8")
pattern = re.compile(
    r"            payload = generate_quiz\(material, question_count=question_count\)\n"
    r"        except GeminiError as exc:\n"
    r"            quiz.status = Quiz.Status.ERROR\n"
    r"            quiz.error_message = str\(exc\)\n"
    r"            quiz.save\(update_fields=\[\"status\", \"error_message\", \"updated_at\"\]\)\n"
    r"            messages.error\(request, f\"Quiz generation failed: {exc}\"\)\n"
    r"        else:\n",
    re.MULTILINE,
)
replacement = (
    "            try:\n"
    "                payload = generate_quiz(material, question_count=question_count)\n"
    "            except GeminiError as exc:\n"
    "                quiz.status = Quiz.Status.ERROR\n"
    "                quiz.error_message = str(exc)\n"
    "                quiz.save(update_fields=[\"status\", \"error_message\", \"updated_at\"])\n"
    "                messages.error(request, f\"Quiz generation failed: {exc}\")\n"
    "            else:\n"
)
if not pattern.search(text):
    raise SystemExit('expected block not found')
text = pattern.sub(replacement, text)
path.write_text(text, encoding='utf-8')
