# Wheatear Repeat

## Use-Case

This library automates a specific category of "simplified" brute-force searches, exploiting
a vulnerability by which a string can be determined to start with an initial substring, without
providing the entire string.

## Example Vulnerability

A rather contrived example follows.

Suppose that an _SQL Injection_ vulnerability exists in an authentication form, due to using a **LIKE**
comparison on the username and password fields and not strict equality.

One can simply bypass authentication entirely by entering a wildcard character (such as **%** or **\***).

However to determine the password for a given known username, an attack could proceed thusly:

1. Try a password attempt consisting of each character in the valid alphabet/set of characters, suffixed with the wildcard, until
successful authentication occurs, e.g.
    - **a\***
    - **b\***
    - **c\***
    - ...
    - **z\***
2. That character becomes the known initial substring
3. Using the initial substring, create a password attempt consisting of
`(initial substring) + (the next guess character) + (the wildcard character)`
for each character in the valid alphabet
4. If a password attempt succesfully authenticates, add the guess character to the initial substring
5. Repeat steps 3. and 4. until no guess character succesfully authenticates - the initial substring is now complete!

## TODO

- [ ] Support parallel brute-forcing
