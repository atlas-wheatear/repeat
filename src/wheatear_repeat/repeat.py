from __future__ import annotations

import threading, random

from dataclasses import dataclass
from typing import Callable, List, Optional


repeater_callable = Callable[[str], bool]


class MaxLengthReachedException(Exception):
    def __init__(self, max_length: int, last_candiate_string: str):
        self.max_length = max_length
        self.last_candiate_string = last_candiate_string
        super().__init__(
            f'The specified max length ({max_length}) was reached. '
            f'The final candiate string was:\n\t{last_candiate_string}'
        )


class _Repeater:
    def __init__(self, repeatable: Repeatable):
        self.initial = repeatable.initial
        self.legal_chars = repeatable.legal_chars
        self.max_length = repeatable.max_length
        self.function = repeatable.function

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

    def repeat(self) -> str:
        self.so_far = self.initial if self.initial is not None else ""
        max_suffix_chars = self.max_length - len(self.so_far)
        return self.find_match(max_suffix_chars)


class _ParallelRepeater(_Repeater):
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

    def __init__(self, repeatable: Repeatable):
        self.parallelism = repeatable.parallelism
        self.match = None
        super().__init__(repeatable)

    def __shuffle_legal_chars(self) -> str:
        list_legal_chars = list(self.legal_chars)
        random.shuffle(list_legal_chars)
        return ''.join(list_legal_chars)

    def __partition_legal_chars(self):
        shuffled_legal_chars = self.__shuffle_legal_chars()
        return [
            shuffled_legal_chars[i::self.parallelism]
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


@dataclass
class Repeatable:
    function: repeater_callable
    parallelism: Optional[int] = None
    initial: Optional[str] = ''
    legal_chars: Optional[str] = ''
    max_length: Optional[int] = 20

    def __call__(self) -> str:
        repeater = self.__get_repeater_class()
        return repeater.repeat()

    def __get_repeater_class(self) -> _Repeater:
        if self.parallelism is None:
            return _Repeater(self)
        else:
            return _ParallelRepeater(self)


def repeat(function: repeater_callable) -> Repeatable:
    """
    The decorator that manages the calls to the given function.
    """
    return Repeatable(function=function)
