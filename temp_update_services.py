from pathlib import Path
import textwrap

path = Path("quizzes/services.py")
text = path.read_text(encoding="utf-8")

text = text.replace("- Use plain Unicode characters (e.g., ?) and do not emit literal \\\\u escapes.", "- Use plain Unicode characters (e.g., ?) and do not emit literal \\u escapes.")
text = text.replace("- Do not introduce extra sections or keys beyond the schema above.\n- Use plain Unicode characters (e.g., ?) and do not emit literal \\u escapes.", "- Do not introduce extra sections or keys beyond the schema above.\n- Use plain Unicode characters (e.g., ?) and do not emit literal \\u escapes.")
text = text.replace("- Do not introduce extra sections or keys beyond the schema above.\n- Use plain Unicode characters (e.g., ?) and do not emit literal \\u escapes.\n- Do not introduce extra sections or keys beyond the schema above.", "- Do not introduce extra sections or keys beyond the schema above.\n- Use plain Unicode characters (e.g., ?) and do not emit literal \\u escapes.")

path.write_text(text, encoding="utf-8")
