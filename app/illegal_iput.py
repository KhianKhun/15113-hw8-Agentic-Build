from typing import Callable, Optional, Tuple, TypeVar


T = TypeVar("T")
Validator = Callable[[str], Tuple[bool, T]]
Reader = Callable[[str], str]


def print_illegal_answers() -> None:
    print("illegal answers")


def prompt_validated(
    prompt: str,
    validator: Validator[T],
    reader: Reader,
    max_illegal: Optional[int] = None,
) -> Tuple[bool, T]:
    illegal_count = 0
    while True:
        raw_value = reader(prompt)
        is_valid, value = validator(raw_value)
        if is_valid:
            return True, value

        illegal_count += 1
        print_illegal_answers()
        if max_illegal is not None and illegal_count >= max_illegal:
            return False, value
