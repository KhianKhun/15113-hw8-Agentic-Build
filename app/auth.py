from typing import Dict, Optional

from .data_manage import DataManager
from .exit_signal import read_input_or_exit
from .illegal_iput import print_illegal_answers


def authenticate_user(manager: DataManager) -> Optional[Dict[str, str]]:
    while True:
        print("\nMain Menu")
        print("1. log in account")
        print("2. register a new account")
        print("3. Forget user name/password")
        print("0. exit")

        choice = read_input_or_exit("Select an option: ")
        if choice == "1":
            user = _login_flow(manager)
            if user is not None:
                return user
        elif choice == "2":
            _register_flow(manager)
        elif choice == "3":
            _forget_flow(manager)
        elif choice == "0":
            return None
        else:
            print_illegal_answers()


def _login_flow(manager: DataManager) -> Optional[Dict[str, str]]:
    username = read_input_or_exit("User name: ")
    password = read_input_or_exit("Password: ")
    if not username or not password:
        print_illegal_answers()
        return None

    user = manager.login_user(username, password)
    if user is None:
        print('Wrong user name + password. Please use "Forget user name/password" function.')
        return None

    print("Log in successful.")
    return user


def _register_flow(manager: DataManager) -> None:
    username = read_input_or_exit("New user name: ")
    if not username:
        print_illegal_answers()
        return

    if manager.is_username_taken(username):
        print("User name already exists. Please use other names.")
        return

    password = read_input_or_exit("New password: ")
    confirm_password = read_input_or_exit("Re-input password: ")
    if not password or password != confirm_password:
        print_illegal_answers()
        return

    birthday = read_input_or_exit("Birthday (privacy question): ")
    last_name = read_input_or_exit("Last name (privacy question): ")
    if not birthday or not last_name:
        print_illegal_answers()
        return

    success, message = manager.register_user(username, password, birthday, last_name)
    print(message)
    if success:
        print("Back to step 3.")


def _forget_flow(manager: DataManager) -> None:
    birthday = read_input_or_exit("Input your birthday: ")
    last_name = read_input_or_exit("Input your last name: ")
    if not birthday or not last_name:
        print_illegal_answers()
        return

    new_username = read_input_or_exit("New user name: ")
    new_password = read_input_or_exit("New password: ")
    confirm_password = read_input_or_exit("Re-input password: ")
    if not new_username or not new_password or new_password != confirm_password:
        print_illegal_answers()
        return

    success, message = manager.recover_account(birthday, last_name, new_username, new_password)
    print(message)
    if success:
        print("Back to step 3.")
