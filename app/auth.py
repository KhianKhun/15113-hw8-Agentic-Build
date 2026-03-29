from typing import Dict, Optional

from .data_manage import DataManager


def authenticate_user(manager: DataManager) -> Optional[Dict[str, str]]:
    while True:
        print("\nMain Menu")
        print("1. log in account")
        print("2. register a new account")
        print("3. Forget user name/password")
        print("0. exit")

        choice = input("Select an option: ").strip()
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
            print("illegal answers")


def _login_flow(manager: DataManager) -> Optional[Dict[str, str]]:
    username = input("User name: ").strip()
    password = input("Password: ").strip()
    if not username or not password:
        print("illegal answers")
        return None

    user = manager.login_user(username, password)
    if user is None:
        print('Wrong user name + password. Please use "Forget user name/password" function.')
        return None

    print("Log in successful.")
    return user


def _register_flow(manager: DataManager) -> None:
    username = input("New user name: ").strip()
    if not username:
        print("illegal answers")
        return

    if manager.is_username_taken(username):
        print("User name already exists. Please use other names.")
        return

    password = input("New password: ").strip()
    confirm_password = input("Re-input password: ").strip()
    if not password or password != confirm_password:
        print("illegal answers")
        return

    birthday = input("Birthday (privacy question): ").strip()
    last_name = input("Last name (privacy question): ").strip()
    if not birthday or not last_name:
        print("illegal answers")
        return

    success, message = manager.register_user(username, password, birthday, last_name)
    print(message)
    if success:
        print("Back to step 3.")


def _forget_flow(manager: DataManager) -> None:
    birthday = input("Input your birthday: ").strip()
    last_name = input("Input your last name: ").strip()
    if not birthday or not last_name:
        print("illegal answers")
        return

    new_username = input("New user name: ").strip()
    new_password = input("New password: ").strip()
    confirm_password = input("Re-input password: ").strip()
    if not new_username or not new_password or new_password != confirm_password:
        print("illegal answers")
        return

    success, message = manager.recover_account(birthday, last_name, new_username, new_password)
    print(message)
    if success:
        print("Back to step 3.")
