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
as a keyword argument e.g. _**HTB{**_ .


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

A rather contrived example follows.

Suppose that a _blind SQL Injection_ vulnerability exists in an authentication form using MySQL, that permits comparisons on confidential fields,
but not direct exfiltration. An example concatenation based query could be:

```sql
SELECT * FROM users WHERE username = 'admin' AND password = '?' 
```

To determine if the password starts with 'password', one could submit a _time-based blind SQL Injection_ payload to the password parameter:

```sql
' UNION SELECT IF(SUBSTRING(user_password,1,1) = CHAR(50),BENCHMARK(5000000,ENCODE('MSG','by 5 seconds')),null) FROM users WHERE user_id = 1;
```

[Source](https://owasp.org/www-community/attacks/Blind_SQL_Injection).

## TODO

- [ ] Make PyPI package
- [ ] Support parallel brute-forcing
