from pathlib import Path
path = Path("quizzes/services.py")
text = path.read_text(encoding="utf-8")
old_start = text.index('def build_prompt(')
old_end = text.index('\n\n\ndef _extract_json_payload')
new_block = '''

def build_prompt(chunks: list[str], question_count: int) -> str:
    joined = "\n\n".join(chunks[:3])
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
        - Use plain Unicode characters (e.g., ?) and do not emit literal \\u escapes.
        """).strip()
    instructions = template.format(question_count=question_count)
    return f"{instructions}\n\nMaterial:\n{joined}"

'''
new_text = text[:old_start] + new_block + text[old_end:]
path.write_text(new_text, encoding="utf-8")
