import base64
import hashlib
import hmac
import json
import secrets
import uuid
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class QuestionFileMissingError(Exception):
    pass


class QuestionFileBrokenError(Exception):
    pass


class DataManager:
    _CIPHER_KEY = hashlib.sha256(b"15113-hw8-agentic-build").digest()

    def __init__(self, root_dir: Optional[Path] = None) -> None:
        self.root_dir = Path(root_dir) if root_dir else Path(__file__).resolve().parents[1]
        self.data_dir = self.root_dir / "data"
        self.questions_path = self.data_dir / "question.json"
        self.users_path = self.data_dir / "users.dat"
        self.scores_path = self.data_dir / "scores.dat"
        self.feedback_path = self.data_dir / "feedback.dat"
        self._defaults = {
            "users": {"users": []},
            "scores": {"users": {}},
            "feedback": {"users": {}},
        }
        self._prepare_data_files()
        self.users_data = self._read_users()
        self.scores_data = self._read_scores()
        self.feedback_data = self._read_feedback()

    def load_questions(self) -> List[Dict[str, Any]]:
        if not self.questions_path.exists():
            raise QuestionFileMissingError

        try:
            raw = self.questions_path.read_text(encoding="utf-8")
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise QuestionFileBrokenError from exc
        except OSError as exc:
            raise QuestionFileMissingError from exc

        if not isinstance(data, dict) or not isinstance(data.get("questions"), list):
            raise QuestionFileBrokenError

        questions = data["questions"]
        if not questions:
            raise QuestionFileBrokenError

        for question in questions:
            if not self._is_valid_question(question):
                raise QuestionFileBrokenError
        return questions

    def login_user(self, username: str, password: str) -> Optional[Dict[str, str]]:
        username = self._normalize_username(username)
        password = self._normalize_password(password)
        record = self._find_user_by_username(username)
        if record is None:
            return None
        if not self._verify_value(password, record["password_salt"], record["password_hash"]):
            return None
        self._ensure_user_stats(record["user_id"])
        self._ensure_user_feedback(record["user_id"])
        return {"user_id": record["user_id"], "username": username}

    def is_username_taken(self, username: str, exclude_user_id: Optional[str] = None) -> bool:
        username = self._normalize_username(username)
        for user in self.users_data["users"]:
            if exclude_user_id and user["user_id"] == exclude_user_id:
                continue
            if self._verify_value(username, user["username_salt"], user["username_hash"]):
                return True
        return False

    def register_user(
        self, username: str, password: str, birthday: str, last_name: str
    ) -> Tuple[bool, str]:
        username = self._normalize_username(username)
        password = self._normalize_password(password)
        birthday = self._normalize_birthday(birthday)
        last_name = self._normalize_last_name(last_name)

        if self.is_username_taken(username):
            return False, "User name already exists. Please use other names."

        user_record = {
            "user_id": uuid.uuid4().hex,
            "username_salt": self._new_salt(),
            "password_salt": self._new_salt(),
            "birthday_salt": self._new_salt(),
            "last_name_salt": self._new_salt(),
        }
        user_record["username_hash"] = self._hash_value(username, user_record["username_salt"])
        user_record["password_hash"] = self._hash_value(password, user_record["password_salt"])
        user_record["birthday_hash"] = self._hash_value(birthday, user_record["birthday_salt"])
        user_record["last_name_hash"] = self._hash_value(last_name, user_record["last_name_salt"])

        self.users_data["users"].append(user_record)
        self._write_users(self.users_data)
        self._ensure_user_stats(user_record["user_id"])
        self._ensure_user_feedback(user_record["user_id"])
        return True, "Register successful."

    def recover_account(
        self, birthday: str, last_name: str, new_username: str, new_password: str
    ) -> Tuple[bool, str]:
        birthday = self._normalize_birthday(birthday)
        last_name = self._normalize_last_name(last_name)
        new_username = self._normalize_username(new_username)
        new_password = self._normalize_password(new_password)

        matches: List[Dict[str, Any]] = []
        for user in self.users_data["users"]:
            birthday_ok = self._verify_value(birthday, user["birthday_salt"], user["birthday_hash"])
            last_name_ok = self._verify_value(
                last_name, user["last_name_salt"], user["last_name_hash"]
            )
            if birthday_ok and last_name_ok:
                matches.append(user)

        if not matches:
            return False, "Privacy information is wrong."

        target = matches[0]
        if self.is_username_taken(new_username, exclude_user_id=target["user_id"]):
            return False, "User name already exists. Please use other names."

        target["username_salt"] = self._new_salt()
        target["password_salt"] = self._new_salt()
        target["username_hash"] = self._hash_value(new_username, target["username_salt"])
        target["password_hash"] = self._hash_value(new_password, target["password_salt"])

        self._write_users(self.users_data)
        return True, "Account information updated."

    def get_user_weights(self, user_id: str) -> Dict[int, float]:
        entry = self._ensure_user_feedback(user_id)
        raw_weights = entry["question_weights"]
        result: Dict[int, float] = {}
        for key, value in raw_weights.items():
            try:
                result[int(key)] = float(value)
            except (ValueError, TypeError):
                continue
        return result

    def update_weight_by_answer(self, user_id: str, question_id: int, correct: bool) -> float:
        entry = self._ensure_user_feedback(user_id)
        qid = str(question_id)
        current = float(entry["question_weights"].get(qid, 1.0))
        if not correct:
            current += 0.35
        elif current > 1.0:
            current = max(1.0, current - 0.25)
        entry["question_weights"][qid] = round(current, 4)
        self._write_feedback(self.feedback_data)
        return current

    def update_question_feedback(self, user_id: str, question_id: int, like_value: int) -> None:
        entry = self._ensure_user_feedback(user_id)
        qid = str(question_id)
        current = float(entry["question_weights"].get(qid, 1.0))

        if like_value == 0:
            current = max(0.2, current - 0.4)
            entry["question_feedback"][qid] = -1
        elif like_value == 1:
            if current < 1.0:
                current = min(1.0, current + 0.4)
            entry["question_feedback"][qid] = 1

        entry["question_weights"][qid] = round(current, 4)
        self._write_feedback(self.feedback_data)

    def record_question_result(
        self, user_id: str, question_id: int, correct: bool, score_delta: int
    ) -> None:
        stats = self._ensure_user_stats(user_id)
        stats["total_questions"] += 1
        stats["total_score"] += score_delta
        if correct:
            stats["correct_questions"] += 1

        total_questions = stats["total_questions"]
        stats["correct_rate"] = (
            round(stats["correct_questions"] / total_questions, 4) if total_questions else 0.0
        )

        qid = str(question_id)
        per_question = stats["per_question"].setdefault(qid, {"asked": 0, "correct": 0})
        per_question["asked"] += 1
        if correct:
            per_question["correct"] += 1

        self._write_scores(self.scores_data)

    def record_session_summary(
        self,
        user_id: str,
        requested_questions: int,
        asked_questions: int,
        correct_questions: int,
        session_score: int,
    ) -> None:
        stats = self._ensure_user_stats(user_id)
        stats["sessions"].append(
            {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "requested_questions": requested_questions,
                "asked_questions": asked_questions,
                "correct_questions": correct_questions,
                "session_score": session_score,
            }
        )
        self._write_scores(self.scores_data)

    def get_user_statistics(self, user_id: str) -> Dict[str, Any]:
        stats = self._ensure_user_stats(user_id)
        return deepcopy(stats)

    def _prepare_data_files(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        missing_file = not (self.users_path.exists() and self.scores_path.exists() and self.feedback_path.exists())
        broken_file = False

        if not missing_file:
            try:
                users = self._read_dat_file(self.users_path)
                scores = self._read_dat_file(self.scores_path)
                feedback = self._read_dat_file(self.feedback_path)
                if not self._is_valid_users_dat(users):
                    broken_file = True
                if not self._is_valid_scores_dat(scores):
                    broken_file = True
                if not self._is_valid_feedback_dat(feedback):
                    broken_file = True
            except (ValueError, OSError, json.JSONDecodeError):
                broken_file = True

        if missing_file or broken_file:
            print("Error, dat files are broken")
            self._write_dat_file(self.users_path, self._defaults["users"])
            self._write_dat_file(self.scores_path, self._defaults["scores"])
            self._write_dat_file(self.feedback_path, self._defaults["feedback"])

    def _read_users(self) -> Dict[str, Any]:
        data = self._read_dat_file(self.users_path)
        if not self._is_valid_users_dat(data):
            raise ValueError("users.dat invalid")
        return data

    def _read_scores(self) -> Dict[str, Any]:
        data = self._read_dat_file(self.scores_path)
        if not self._is_valid_scores_dat(data):
            raise ValueError("scores.dat invalid")
        return data

    def _read_feedback(self) -> Dict[str, Any]:
        data = self._read_dat_file(self.feedback_path)
        if not self._is_valid_feedback_dat(data):
            raise ValueError("feedback.dat invalid")
        return data

    def _write_users(self, data: Dict[str, Any]) -> None:
        self._write_dat_file(self.users_path, data)

    def _write_scores(self, data: Dict[str, Any]) -> None:
        self._write_dat_file(self.scores_path, data)

    def _write_feedback(self, data: Dict[str, Any]) -> None:
        self._write_dat_file(self.feedback_path, data)

    def _read_dat_file(self, path: Path) -> Dict[str, Any]:
        payload = path.read_text(encoding="utf-8").strip()
        if not payload:
            raise ValueError("empty dat file")
        decoded = self._decode_payload(payload)
        data = json.loads(decoded)
        if not isinstance(data, dict):
            raise ValueError("dat data must be an object")
        return data

    def _write_dat_file(self, path: Path, data: Dict[str, Any]) -> None:
        serialized = json.dumps(data, ensure_ascii=True, separators=(",", ":"))
        encoded = self._encode_payload(serialized)
        path.write_text(encoded, encoding="utf-8")

    def _encode_payload(self, payload: str) -> str:
        data_bytes = payload.encode("utf-8")
        obfuscated = bytes(
            byte ^ self._CIPHER_KEY[index % len(self._CIPHER_KEY)] for index, byte in enumerate(data_bytes)
        )
        return base64.urlsafe_b64encode(obfuscated).decode("ascii")

    def _decode_payload(self, payload: str) -> str:
        raw = base64.urlsafe_b64decode(payload.encode("ascii"))
        recovered = bytes(
            byte ^ self._CIPHER_KEY[index % len(self._CIPHER_KEY)] for index, byte in enumerate(raw)
        )
        return recovered.decode("utf-8")

    @staticmethod
    def _new_salt() -> str:
        return secrets.token_hex(16)

    @staticmethod
    def _hash_value(value: str, salt_hex: str) -> str:
        digest = hashlib.pbkdf2_hmac("sha256", value.encode("utf-8"), bytes.fromhex(salt_hex), 180000)
        return digest.hex()

    def _verify_value(self, plain_text: str, salt_hex: str, hash_hex: str) -> bool:
        candidate = self._hash_value(plain_text, salt_hex)
        return hmac.compare_digest(candidate, hash_hex)

    def _find_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        for user in self.users_data["users"]:
            if self._verify_value(username, user["username_salt"], user["username_hash"]):
                return user
        return None

    def _ensure_user_stats(self, user_id: str) -> Dict[str, Any]:
        users = self.scores_data.setdefault("users", {})
        if user_id not in users:
            users[user_id] = {
                "total_questions": 0,
                "correct_questions": 0,
                "correct_rate": 0.0,
                "total_score": 0,
                "per_question": {},
                "sessions": [],
            }
            self._write_scores(self.scores_data)
        return users[user_id]

    def _ensure_user_feedback(self, user_id: str) -> Dict[str, Any]:
        users = self.feedback_data.setdefault("users", {})
        if user_id not in users:
            users[user_id] = {"question_feedback": {}, "question_weights": {}}
            self._write_feedback(self.feedback_data)
        return users[user_id]

    @staticmethod
    def _normalize_username(username: str) -> str:
        return username.strip()

    @staticmethod
    def _normalize_password(password: str) -> str:
        return password.strip()

    @staticmethod
    def _normalize_birthday(birthday: str) -> str:
        return birthday.strip()

    @staticmethod
    def _normalize_last_name(last_name: str) -> str:
        return last_name.strip().lower()

    @staticmethod
    def _is_valid_users_dat(data: Dict[str, Any]) -> bool:
        if not isinstance(data, dict) or not isinstance(data.get("users"), list):
            return False
        required = {
            "user_id",
            "username_salt",
            "username_hash",
            "password_salt",
            "password_hash",
            "birthday_salt",
            "birthday_hash",
            "last_name_salt",
            "last_name_hash",
        }
        for item in data["users"]:
            if not isinstance(item, dict):
                return False
            if not required.issubset(item.keys()):
                return False
        return True

    @staticmethod
    def _is_valid_scores_dat(data: Dict[str, Any]) -> bool:
        return isinstance(data, dict) and isinstance(data.get("users"), dict)

    @staticmethod
    def _is_valid_feedback_dat(data: Dict[str, Any]) -> bool:
        return isinstance(data, dict) and isinstance(data.get("users"), dict)

    @staticmethod
    def _is_valid_question(question: Dict[str, Any]) -> bool:
        if not isinstance(question, dict):
            return False
        required = {"id", "question", "type", "answer", "category", "difficulty", "like"}
        if not required.issubset(question.keys()):
            return False
        if not isinstance(question["id"], int):
            return False
        if not isinstance(question["question"], str) or not question["question"].strip():
            return False
        if question["type"] not in {"multiple_choice", "true_false", "short_answer"}:
            return False
        if question["difficulty"] not in {1, 2, 3}:
            return False
        if question["like"] != [0, 1]:
            return False
        if not isinstance(question["category"], str) or not question["category"].strip():
            return False

        if question["type"] == "multiple_choice":
            options = question.get("options")
            if not isinstance(options, list) or len(options) < 2:
                return False
            if not all(isinstance(item, str) and item.strip() for item in options):
                return False
            if not isinstance(question["answer"], str):
                return False
            if question["answer"] not in options:
                return False
        elif question["type"] == "true_false":
            if question["answer"] not in {"True", "False"}:
                return False
        elif question["type"] == "short_answer":
            answer = question["answer"]
            if isinstance(answer, str):
                return bool(answer.strip())
            if isinstance(answer, list):
                return bool(answer) and all(isinstance(item, str) and item.strip() for item in answer)
            return False
        return True
