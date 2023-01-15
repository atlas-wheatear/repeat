# Wheatear Repeat

## Use-Case

This library automates a specific category of "simplified" brute-force searches, exploiting
a vulnerability by which a string can be determined to start with an initial substring, without
providing the entire string.

## Explanation

A secret string can be exfiltrated by repeated tests of whether it starts with an arbitrary substring, given knowledge
of the character set from which it may have been built.

1. Simply try each character in the legal character set until one tests positive for being the first.
2. Then try that character repeatedly suffixed with 1 different character from the legal subset until a 2-length string
tests positive
3. Repeat  by adding 1 different character to an n-length string from the legal subset, while positive tests still occur.
4. If an iteration does not produce a positive test, this is the reversed secret string

## Usage

Create a python function that takes a _candidate string_, performs a test (e.g. a blind SQL injection), and returns:

- `True` if the _secret string_ **starts** with the _candiate string_
- `False` otherwise

Then decorate it with the `repeat` method from the repeat package, giving the following arguments:

- the _legal characters_ that the secret string may be formed from (as a string)
- the maximum length of the secret string attempts, before an iteration is halted

This produces a function, that when called, performs this attack. An optional initial string may be provided
as the keyword argument `initial`, e.g. _**HTB{**_ . If parallelism is desired, it is supported by specifying the number of
parallel threads (as an integer) as the keyword argument `parallelism`.


```python
import string
from repeat import repeat

@repeat(
    string.ascii_letters + string.digits + '-_}',
    30
)
def get_flag(candidate_string: str) -> bool:
    FLAG = 'HTB{fl4gs-4r3_fun}'
    # this is a silly example
    return FLAG.startswith(candidate_string)

print(
    get_flag(initial='HTB{')
)
```

A better example will follow.

## Example Vulnerability

See the example folder in this repository, containing a totally unrealistic blind-SQL injection vulnerability.

## TODO

- [ ] Make PyPI package
- [x] Support parallel brute-forcing
