import pytest, string


from wheatear_repeat import repeat


def test_basic_max_length():
    @repeat
    def test_function(candiate_string: str) -> bool:
        return "lol".startswith(candiate_string)

    test_function.characters = string.ascii_lowercase
    test_function.max_length = 3
    match = test_function()
    assert match == 'lol'


def test_basic_max_length_parallel():
    @repeat
    def test_function(candiate_string: str) -> bool:
        return "lol".startswith(candiate_string)

    test_function.characters = string.ascii_lowercase
    test_function.max_length = 3
    test_function.parallelism = 5
    match = test_function()
    assert match == 'lol'
