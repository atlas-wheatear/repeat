import pytest, string


from wheatear_repeat import repeat
from wheatear_repeat.repeat import MaxLengthReachedException


def test_basic_max_length():
    @repeat
    def test_function(candidate_string: str) -> bool:
        return "lol".startswith(candidate_string)

    test_function.characters = string.ascii_lowercase
    test_function.max_length = 3
    match = test_function()
    assert match == 'lol'


def test_basic_max_length_parallel():
    @repeat
    def test_function(candidate_string: str) -> bool:
        return "lol".startswith(candidate_string)

    test_function.characters = string.ascii_lowercase
    test_function.max_length = 3
    test_function.parallelism = 5
    match = test_function()
    assert match == 'lol'


def test_max_length_exceeded():
    @repeat
    def test_function(candidate_string: str) -> bool:
        return False

    test_function.characters = string.ascii_lowercase
    test_function.max_length = 3
    test_function.parallelism = 5

    with pytest.raises(MaxLengthReachedException):
        test_function()
