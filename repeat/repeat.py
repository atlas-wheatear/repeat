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


class __Repeater:
    def __init__(self, legal_chars: str, function: repeater_callable, max_length: int):
        self.legal_chars = legal_chars
        self.max_length = max_length
        self.function = function

    @property
    def so_far(self):
        return self.__so_far

    @so_far.setter
    def so_far(self, value):
        self.__so_far = value
        print(self.__so_far)

    def __candiate_string_generator(self):
        for char in self.legal_chars:
            yield self.so_far + char

    def __test_all_candidate_strings(self):
        for candiate_string in self.__candiate_string_generator():
            if self.function(candiate_string):
                return candiate_string

    def __find_match(self, max_suffix_chars: int) -> str:
        for _ in range(max_suffix_chars + 1):
            match = self.__test_all_candidate_strings()
            if match is None:
                return self.so_far
            else:
                self.so_far = match
        raise MaxLengthReachedException(
            self.max_length,
            self.so_far
        )

    def repeat(self, initial: str) -> str:
        self.so_far = initial if initial is not None else ""
        max_suffix_chars = self.max_length - len(self.so_far)
        return self.__find_match(max_suffix_chars)


def __get_repeater_class(parallelism: int) -> __Repeater:
    if parallelism is None:
        return __Repeater


def repeat(legal_chars: str, max_length: int):
    def decorator(function: repeater_callable):
        @wraps(function)
        def wrapper(initial: str = None, parallelism: int = None) -> str:
            repeater_class = __get_repeater_class(parallelism)
            return repeater_class(
                legal_chars,
                function,
                max_length
            ).repeat(initial)
        return wrapper
    return decorator
