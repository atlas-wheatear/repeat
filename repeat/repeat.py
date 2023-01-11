from functools import wraps
from typing import Callable


repeater_callable = Callable[[str], bool]


class MaxLengthReachedException(Exception):
    def __init__(self, max_length: int, last_candiate_string: str):
        self.max_length = max_length
        self.last_candiate_string = last_candiate_string
        super().__init__(
            f'The specified max length ({max_length}) was reached. '
            f'The final candiate string was:\n\t{last_candiate_string}'
        )


def __candiate_string_generator(initial: str, legal_chars: str):
    for char in legal_chars:
        yield initial + char


def __test_all_candidate_strings(initial: str, legal_chars: str, function: repeater_callable):
    for candiate_string in __candiate_string_generator(initial, legal_chars):
        if function(candiate_string):
            return candiate_string


def __find_match(initial: str, legal_chars: str, function: repeater_callable, max_length: int):
    so_far = initial if initial is not None else ""
    max_suffix_chars = max_length - len(so_far)
    for _ in range(max_suffix_chars):
        match = __test_all_candidate_strings(initial, legal_chars, function)
        if match is None:
            return match
        else:
            so_far = match
    raise MaxLengthReachedException(max_length, so_far)


def repeat(legal_chars: str, max_length: int):
    def decorator(function: repeater_callable):
        @wraps(function)
        def wrapper(initial: str = None):
            return __find_match(
                initial,
                legal_chars,
                function,
                max_length
            ) 
        return wrapper
    return decorator
