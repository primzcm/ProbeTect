from pathlib import Path

path = Path("quizzes/views.py")
lines = path.read_text(encoding="utf-8").splitlines()
insert_idx = None
for idx, line in enumerate(lines):
    if line.strip() == "else:" and idx > 0 and "try:" in lines[idx-1]:
        if lines[idx+1].strip().startswith("questions = payload"):
            insert_idx = idx + 1
            break
if insert_idx is None:
    raise SystemExit('insertion point not found')
lines.insert(insert_idx, "            reduced_from = payload.pop('reduced_from', None) if isinstance(payload, dict) else None")
lines.insert(insert_idx+1, "            if reduced_from:")
lines.insert(insert_idx+2, "                messages.warning(request, f'Gemini could only generate {payload.get(\"question_count\", len(payload.get(\"questions\", [])))} questions instead of {reduced_from}.')")
path.write_text("\n".join(lines) + "\n", encoding='utf-8')
