# 15113-HW8-AGENTIC-BUILD

Command-line quiz application for CMU 36-401 / 36-402 related topics (regression and modern data analysis).

## Features

- Local account system: register, log in, and recover account via privacy questions (birthday + last name).
- Credentials are stored with salted hash, not plain text.
- Quiz engine supports `multiple_choice`, `true_false`, and `short_answer`.
- Supports category and difficulty selection (`N/A` means default mode).
- Weighted question sampling uses user history (correctness + like/dislike feedback).
- Stores score history: total question count, correct count, correct rate, per-question performance, and total score.
- Difficulty-based scoring:
- Easy (1): correct `+1`, wrong `-1`.
- Medium (2): correct `+1`, wrong `0`.
- Hard (3): correct `+2`, wrong `0`.

## Run

From project root:

```bash
py quiz.py
```

or (if `python` is configured in your environment):

```bash
python quiz.py
```

## Project Structure

```text
15113-HW8-AGENTIC-BUILD
|-- quiz.py
|-- app/
|   |-- quiz.py
|   |-- auth.py
|   |-- quiz_logic.py
|   |-- data_manage.py
|-- data/
|   |-- question.json
|   |-- question.py
|   |-- users.dat
|   |-- scores.dat
|   |-- feedback.dat
|-- SPEC.md
|-- REVIEW.md
|-- REFLECTION.md
```

## Error Handling

- Missing `question.json`: outputs `Error, question.json not opend/found`.
- Broken `question.json` format: outputs `Error, JSON file is broken` and exits.
- Missing or broken `.dat` files: outputs `Error, dat files are broken` and resets data files.
- Illegal user answer input: outputs `illegal answers` and asks for re-input.
- If illegal input occurs 3 times continuously for one question, the question is skipped.
- Wrong login credentials: hints user to use `Forget user name/password` function.

## Notes

- `data/question.json` includes sample questions from `SPEC.md` plus additional professional questions.
- The app is fully local (no HTML/CSS/API usage).
