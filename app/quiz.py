from .auth import authenticate_user
from .data_manage import DataManager, QuestionFileBrokenError, QuestionFileMissingError
from .exit_signal import ExitRequested, read_input_or_exit
from .illegal_iput import print_illegal_answers
from .quiz_logic import run_quiz_for_user


def main() -> None:
    print("Welcome to use test")
    try:
        manager = DataManager()
        questions = manager.load_questions()
    except QuestionFileMissingError:
        print("Error, question.json not opend/found")
        return
    except QuestionFileBrokenError:
        print("Error, JSON file is broken")
        return
    except MemoryError:
        print("Error, out of memory. Program exits.")
        return

    try:
        while True:
            user = authenticate_user(manager)
            if user is None:
                print("Bye.")
                return

            while True:
                run_quiz_for_user(manager, questions, user)
                while True:
                    action = read_input_or_exit('Type "restart" to restart or "exit" to exit: ').lower()
                    if action == "restart":
                        break
                    if action == "exit":
                        print("Bye.")
                        return
                    print_illegal_answers()
                if action == "restart":
                    continue
    except ExitRequested:
        print("Bye.")
    except MemoryError:
        print("Error, out of memory. Program exits.")
