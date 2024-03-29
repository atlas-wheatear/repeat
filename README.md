# Wheatear Repeat

## Summary

This library automates a specific category of "simplified" brute-force searches, exploiting
a vulnerability by which a string can be determined to start with an initial substring, without
providing the entire string.

## Requirements

_Three_ conditions are necessary for this library to be applicable to deducing a secret string (faster
than a regular brute-force search):

1. No rate limiting is in place
2. The permitted character set, from which the secret string was formed, is known (e.g. ASCII-printable)
3. A vulnerability exists that permits an attacker to determine if the secret string _starts_ with an arbitrary guess
    - this must also be scriptable as a boolean _"test-function"_ in python

## Explanation

A secret string can be exfiltrated by repeated tests of whether it starts with an arbitrary guess, given knowledge
of the character set from which it was built.

1. Simply try each character in the legal character set until one tests positive for being the first.
2. Then try that character repeatedly suffixed with 1 different character from the legal subset until a 2-length string
tests positive
3. Repeat  by adding 1 different character to an n-length string from the legal subset, while positive tests still occur.
4. If an iteration does not produce a positive test, this is the reversed secret string

## Installing

From the root directory (ideally in a virtual environment), install locally with the following command:

```bash
python3 -m pip install -e .
```

## Usage

Create a python function that takes a _candidate string_, performs a test (e.g. a blind SQL injection), and returns:

- `True` if the _secret string_ **starts** with the _candiate string_
- `False` otherwise

Then decorate it with the `repeat` method from the repeat package, giving the following arguments:

- the _legal characters_ that the secret string may be formed from (as a string)
- the maximum length of the secret string attempts, before an iteration is halted

This produces a function, that when called, performs this attack. An optional initial string may be provided
as the keyword argument `initial`, e.g. _**HTB{**_ . If parallelism is desired, it is supported by specifying the number of
parallel threads (as an integer) as the keyword argument `parallelism` (though see the health warning below!)


```python
import string
from wheatear_repeat import repeat

@repeat
def get_flag(candidate_string: str) -> bool:
    FLAG = 'HTB{fl4gs-4r3_fun}'
    # this is a silly example
    return FLAG.startswith(candidate_string)

get_flag.characters = string.ascii_letters + string.digits + '-_}', # the permitted character set
get_flag.max_length = 30 # the maximum length of guess before giving up
get_flag.initial = 'HTB{' # the flag must start like all other HTB flags
get_flag.parallelism = 5 # use 5 parallel threads

flag = get_flag()
print(flag)
```

A better example will follow.

## A Note on Parallelism

Parallelism can give wrong results on certain servers, especially for higher numbers of parallel threads against
servers with low resources.

Obviously incorrect behaviour includes:
- giving different results each time it is run.
- giving a very short string (just 1 or 2 characters)
- giving a long string very fast, usually containing the same character over and over

## Example Vulnerability

See the example folder in this repository, containing a totally unrealistic blind-SQL injection vulnerability.

## Running the tests

First install the testing requirements:

```bash
python3 -m pip install -r test/requirements.txt
```

Then run the tests:

```bash
python3 -m pytest test
```

## TODO

- [x] Make PyPI package
- [x] Support parallel brute-forcing
