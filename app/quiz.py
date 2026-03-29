from .auth import authenticate_user
from .data_manage import DataManager, QuestionFileBrokenError, QuestionFileMissingError
from .quiz_logic import run_quiz_for_user


def main() -> None:
    print("Welcome to use test")
    manager = DataManager()
    try:
        questions = manager.load_questions()
    except QuestionFileMissingError:
        print("Error, question.json not opend/found")
        return
    except QuestionFileBrokenError:
        print("Error, JSON file is broken")
        return

    while True:
        user = authenticate_user(manager)
        if user is None:
            print("Bye.")
            return

        while True:
            run_quiz_for_user(manager, questions, user)
            while True:
                action = input('Type "restart" to restart or "exit" to exit: ').strip().lower()
                if action == "restart":
                    break
                if action == "exit":
                    print("Bye.")
                    return
                print("illegal answers")
            if action == "restart":
                continue
