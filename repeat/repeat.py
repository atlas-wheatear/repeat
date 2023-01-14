import threading

from functools import wraps
from typing import Callable, List


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

    def find_match(self, max_suffix_chars: int) -> str:
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
        return self.find_match(max_suffix_chars)


class __ParallelRepeater(__Repeater):
    class __RepeatThread(threading.Thread):
        def __init__(self, manager, so_far: str, given_chars: List[str], *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.manager = manager
            self.function = self.manager.function
            self.so_far = so_far
            self.given_chars = given_chars
            self.should_stop = threading.Event()

        def stop(self):
            self.should_stop.set()

        def stopped(self):
            return self.should_stop.is_set()

        def __candiate_string_generator(self):
            for char in self.given_chars:
                yield self.so_far + char

        def run(self):
            for candiate_string in self.__candiate_string_generator():
                if self.function(candiate_string):
                    self.manager.match_found(candiate_string)

    def __init__(
        self,
        legal_chars: str,
        function: repeater_callable,
        max_length: int,
        parallelism: int
    ):
        self.parallelism = parallelism
        super().__init__(
            legal_chars,
            function,
            max_length
        )

    def __partition_legal_chars(self):
        return [
            self.legal_chars[i::self.parallelism]
            for i in range(self.parallelism)
        ]

    def __start_repeat_threads(self):
        self.threads = [
            self.__RepeatThread(
                self,
                self.so_far,
                partition
            )
            for partition
            in self.__partition_legal_chars()
        ]
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()

    def match_found(self, match: str):
        self.match = match
        for thread in self.threads:
            thread.stop()

    def find_match(self, max_suffix_chars: int) -> str:
        for _ in range(max_suffix_chars + 1):
            self.__start_repeat_threads()
            if self.match is None:
                return self.so_far
            else:
                self.so_far = self.match
                self.match = None
        raise MaxLengthReachedException(
            self.max_length,
            self.so_far
        )


def __get_repeater_class(
    legal_chars: str,
    max_length: int,
    function: repeater_callable,
    parallelism: int
) -> __Repeater:
    if parallelism is None:
        return __Repeater(
            legal_chars,
            function,
            max_length
        )
    else:
        return __ParallelRepeater(
            legal_chars,
            function,
            max_length,
            parallelism
        )


def repeat(legal_chars: str, max_length: int):
    def decorator(function: repeater_callable):
        @wraps(function)
        def wrapper(initial: str = None, parallelism: int = None) -> str:
            repeater_class = __get_repeater_class(
                legal_chars,
                max_length,
                function,
                parallelism
            )
            return repeater_class.repeat(initial)
        return wrapper
    return decorator
