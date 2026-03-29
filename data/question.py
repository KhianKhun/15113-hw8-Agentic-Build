import json
from pathlib import Path
from typing import Any, Dict, List


QUESTION_JSON_PATH = Path(__file__).resolve().with_name("question.json")


def load_question_bank() -> List[Dict[str, Any]]:
    if not QUESTION_JSON_PATH.exists():
        print("Error, question.json not opend/found")
        return []

    try:
        raw = QUESTION_JSON_PATH.read_text(encoding="utf-8")
        data = json.loads(raw)
    except MemoryError:
        print("Error, out of memory. Program exits.")
        return []
    except OSError:
        print("Error, question.json not opend/found")
        return []
    except json.JSONDecodeError:
        print("Error, JSON file is broken")
        return []

    questions = data.get("questions")
    if not isinstance(questions, list):
        print("Error, JSON file is broken")
        return []
    return questions


if __name__ == "__main__":
    questions = load_question_bank()
    print(f"Question count: {len(questions)}")
