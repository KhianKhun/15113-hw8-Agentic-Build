import random
import re
from typing import Any, Dict, List, Optional, Tuple

from .data_manage import DataManager


def run_quiz_for_user(
    manager: DataManager, questions: List[Dict[str, Any]], user: Dict[str, str]
) -> None:
    requested_count, category, difficulty = _prompt_quiz_settings(questions)

    remaining = requested_count
    asked_questions = 0
    correct_questions = 0
    session_score = 0
    asked_ids: List[int] = []

    while remaining > 0:
        batch_size = min(10, remaining)
        batch = _build_batch(questions, manager, user["user_id"], batch_size, category, difficulty, asked_ids)
        if not batch:
            print("No matching questions. Fallback to mixed/default mode.")
            batch = _build_batch(questions, manager, user["user_id"], batch_size, None, None, asked_ids)
            if not batch:
                print("Question bank is empty.")
                break

        print(f"\nNew question list generated: {len(batch)} question(s).")
        for question in batch:
            asked_questions += 1
            asked_ids.append(question["id"])

            result = _ask_question(question)
            correct = result["correct"]
            delta = _score_delta(question["difficulty"], correct)
            session_score += delta
            if correct:
                correct_questions += 1

            manager.record_question_result(user["user_id"], question["id"], correct, delta)
            manager.update_weight_by_answer(user["user_id"], question["id"], correct)

            feedback = _prompt_feedback()
            if feedback is not None:
                manager.update_question_feedback(user["user_id"], question["id"], feedback)

            remaining -= 1
            if remaining == 0:
                break

    manager.record_session_summary(
        user["user_id"], requested_count, asked_questions, correct_questions, session_score
    )
    _show_session_summary(manager, user["user_id"], asked_questions, correct_questions, session_score)


def _prompt_quiz_settings(questions: List[Dict[str, Any]]) -> Tuple[int, Optional[str], Optional[int]]:
    categories = sorted({q["category"] for q in questions})

    while True:
        raw_count = input("How many questions do you want? ").strip()
        if raw_count.isdigit() and int(raw_count) > 0:
            question_count = int(raw_count)
            break
        print("illegal answers")

    category_map = {item.lower(): item for item in categories}
    print("\nCategories:")
    print(", ".join(categories))
    print("Use N/A for default category mode.")
    while True:
        raw_category = input("Category: ").strip()
        if not raw_category or raw_category.lower() in {"n/a", "na"}:
            category = None
            break
        chosen = category_map.get(raw_category.lower())
        if chosen:
            category = chosen
            break
        print("illegal answers")

    while True:
        raw_difficulty = input("Difficulty (1/2/3, N/A for default): ").strip().lower()
        if raw_difficulty in {"", "n/a", "na"}:
            difficulty = None
            break
        if raw_difficulty in {"1", "2", "3"}:
            difficulty = int(raw_difficulty)
            break
        print("illegal answers")

    return question_count, category, difficulty


def _build_batch(
    questions: List[Dict[str, Any]],
    manager: DataManager,
    user_id: str,
    batch_size: int,
    category: Optional[str],
    difficulty: Optional[int],
    asked_ids: List[int],
) -> List[Dict[str, Any]]:
    filtered = [
        question
        for question in questions
        if (category is None or question["category"] == category)
        and (difficulty is None or question["difficulty"] == difficulty)
    ]
    if not filtered:
        return []

    unasked = [question for question in filtered if question["id"] not in asked_ids]
    candidate_pool = unasked if len(unasked) >= batch_size else filtered
    weights = manager.get_user_weights(user_id)

    return _weighted_pick(candidate_pool, weights, batch_size)


def _weighted_pick(
    questions: List[Dict[str, Any]], user_weights: Dict[int, float], count: int
) -> List[Dict[str, Any]]:
    if not questions:
        return []

    if len(questions) >= count:
        return _weighted_without_replacement(questions, user_weights, count)

    selected: List[Dict[str, Any]] = []
    for _ in range(count):
        selected.append(_weighted_single_pick(questions, user_weights))
    return selected


def _weighted_without_replacement(
    questions: List[Dict[str, Any]], user_weights: Dict[int, float], count: int
) -> List[Dict[str, Any]]:
    selected: List[Dict[str, Any]] = []
    pool = list(questions)
    for _ in range(count):
        if not pool:
            break
        picked = _weighted_single_pick(pool, user_weights)
        selected.append(picked)
        pool.remove(picked)
    return selected


def _weighted_single_pick(
    questions: List[Dict[str, Any]], user_weights: Dict[int, float]
) -> Dict[str, Any]:
    effective_weights: List[float] = []
    for question in questions:
        weight = float(user_weights.get(question["id"], 1.0))
        effective_weights.append(max(0.05, weight))
    return random.choices(questions, weights=effective_weights, k=1)[0]


def _ask_question(question: Dict[str, Any]) -> Dict[str, Any]:
    print("\n----------------------------------------")
    print(f"Question ID: {question['id']}")
    print(f"Category: {question['category']} | Difficulty: {question['difficulty']}")
    print(question["question"])

    if question["type"] == "multiple_choice":
        for index, option in enumerate(question["options"], start=1):
            print(f"{index}. {option}")

    illegal_count = 0
    while illegal_count < 3:
        raw_answer = input("Your answer: ").strip()
        parsed_answer, illegal = _parse_answer(question, raw_answer)
        if illegal:
            illegal_count += 1
            print("illegal answers")
            continue

        correct = _is_correct(question, parsed_answer)
        _print_result(question, correct)
        return {"correct": correct}

    print("Maximum illegal answers reached. Skip this question.")
    print(f"Correct answer: {_format_correct_answer(question)}")
    return {"correct": False}


def _parse_answer(question: Dict[str, Any], raw_answer: str) -> Tuple[str, bool]:
    q_type = question["type"]
    if q_type == "multiple_choice":
        if not raw_answer:
            return "", True
        if raw_answer.isdigit():
            choice_index = int(raw_answer) - 1
            options = question["options"]
            if 0 <= choice_index < len(options):
                return options[choice_index], False
            return "", True

        lowered_input = raw_answer.lower()
        for option in question["options"]:
            if lowered_input == option.lower():
                return option, False
        return "", True

    if q_type == "true_false":
        mapping = {"true": "True", "t": "True", "false": "False", "f": "False"}
        canonical = mapping.get(raw_answer.lower())
        if canonical is None:
            return "", True
        return canonical, False

    if q_type == "short_answer":
        if not raw_answer:
            return "", True
        return raw_answer, False

    return "", True


def _is_correct(question: Dict[str, Any], user_answer: str) -> bool:
    q_type = question["type"]
    correct_answer = question["answer"]

    if q_type in {"multiple_choice", "true_false"}:
        return _normalize_text(user_answer) == _normalize_text(str(correct_answer))

    if q_type == "short_answer":
        user_normalized = _normalize_text(user_answer)
        if isinstance(correct_answer, str):
            return user_normalized == _normalize_text(correct_answer)
        if isinstance(correct_answer, list):
            return all(_normalize_text(token) in user_normalized for token in correct_answer)
    return False


def _normalize_text(text: str) -> str:
    lowered = text.strip().lower()
    return re.sub(r"[^a-z0-9^().+\-_/ ]+", "", lowered)


def _print_result(question: Dict[str, Any], correct: bool) -> None:
    print("Result: Correct." if correct else "Result: Wrong.")
    print(f"Correct answer: {_format_correct_answer(question)}")


def _format_correct_answer(question: Dict[str, Any]) -> str:
    answer = question["answer"]
    if isinstance(answer, list):
        return ", ".join(answer)
    return str(answer)


def _prompt_feedback() -> Optional[int]:
    print("Feedback: 0 is dislike, 1 is like. Press Enter to skip.")
    illegal_count = 0
    while illegal_count < 3:
        raw_feedback = input("Your feedback: ").strip()
        if raw_feedback == "":
            return None
        if raw_feedback in {"0", "1"}:
            return int(raw_feedback)
        illegal_count += 1
        print("illegal answers")
    print("Skip feedback for this question.")
    return None


def _score_delta(difficulty: int, correct: bool) -> int:
    if correct:
        return 2 if difficulty == 3 else 1
    if difficulty == 1:
        return -1
    return 0


def _show_session_summary(
    manager: DataManager, user_id: str, asked_questions: int, correct_questions: int, session_score: int
) -> None:
    print("\n===== Ending Page =====")
    print(f"Questions asked: {asked_questions}")
    print(f"Correct answers: {correct_questions}")
    rate = (correct_questions / asked_questions * 100.0) if asked_questions else 0.0
    print(f"Session correct rate: {rate:.2f}%")
    print(f"Session score: {session_score}")

    total_stats = manager.get_user_statistics(user_id)
    print("\nHistorical statistics")
    print(f"Total questions: {total_stats['total_questions']}")
    print(f"Total correct: {total_stats['correct_questions']}")
    print(f"Total correct rate: {total_stats['correct_rate'] * 100:.2f}%")
    print(f"Total score: {total_stats['total_score']}")
