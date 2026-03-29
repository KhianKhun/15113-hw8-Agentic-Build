import json
from pathlib import Path
from typing import Any, Dict, List


QUESTION_JSON_PATH = Path(__file__).resolve().with_name("question.json")


def load_question_bank() -> List[Dict[str, Any]]:
    data = json.loads(QUESTION_JSON_PATH.read_text(encoding="utf-8"))
    return data["questions"]


if __name__ == "__main__":
    questions = load_question_bank()
    print(f"Question count: {len(questions)}")
