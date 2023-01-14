import pytest, string


from ..repeat import repeat


def test_basic_max_length():
    @repeat(string.ascii_lowercase, 3)
    def test_function(candiate_string: str) -> bool:
        return "lol".startswith(candiate_string)

    match = test_function()
    assert match == 'lol'


def test_basic_max_length_parallel():
    @repeat(string.ascii_lowercase, 3)
    def test_function(candiate_string: str) -> bool:
        return "lol".startswith(candiate_string)

    match = test_function(parallelism=5)
    assert match == 'lol'
