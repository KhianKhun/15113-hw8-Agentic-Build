class ExitRequested(Exception):
    """Raised when user requests immediate exit by typing 'exit'."""


def read_input_or_exit(prompt: str) -> str:
    value = input(prompt).strip()
    if value.lower() == "exit":
        raise ExitRequested
    return value
