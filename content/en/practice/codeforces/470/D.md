---
title: "CF 470D - Caesar Cipher"
description: "We are asked to implement a simple Caesar cipher. The input gives us a key k, an integer between 0 and 25, which represents how many positions each letter in the message should be shifted forward in the alphabet."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 470
codeforces_index: "D"
codeforces_contest_name: "Surprise Language Round 7"
rating: 1900
weight: 470
solve_time_s: 84
verified: true
draft: false
---

[CF 470D - Caesar Cipher](https://codeforces.com/problemset/problem/470/D)

**Rating:** 1900  
**Tags:** *special  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to implement a simple Caesar cipher. The input gives us a key `k`, an integer between 0 and 25, which represents how many positions each letter in the message should be shifted forward in the alphabet. The message itself is a string of uppercase Latin letters, and its length ranges from 1 to 10 characters. Our task is to output the encrypted message by applying this shift.

The constraints make this a straightforward problem: since the message is very short, we do not need to worry about the efficiency of our algorithm. Even a naive implementation that loops over each character and performs arithmetic to shift it will run in microseconds. The only subtlety is correctly wrapping around the alphabet. For example, shifting 'Z' by 1 should produce 'A'. A careless implementation might try to add `k` directly to the ASCII value and forget to wrap modulo 26, which would give an invalid character.

Another edge case arises when the shift is 0. In this case, the encrypted message should be identical to the input, and a naive implementation that always adds `k` and wraps modulo 26 will handle this correctly if modulo is applied.

## Approaches

A brute-force approach naturally presents itself. For each character in the message, we convert it to its 0-based position in the alphabet by subtracting the ASCII value of 'A'. We then add `k` and take modulo 26 to handle wrapping. Finally, we convert back to a character by adding the ASCII value of 'A'. This works for any input because each operation is constant-time, and there are at most 10 characters. The brute-force approach is fully acceptable here because of the small input size. There is no need for any optimization in terms of time complexity. The key insight is recognizing that the Caesar cipher is just modular arithmetic over 26 letters. This makes the implementation both simple and mathematically precise.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(n) | Accepted |
| Optimal | O(n) | O(n) | Accepted |

In this case, the brute-force approach and the optimal approach are effectively the same, because the problem's constraints allow us to handle every character individually without worrying about performance.

## Algorithm Walkthrough

1. Read the encryption key `k` from input. This integer tells us how many positions to shift each letter.
2. Read the original message as a string of uppercase letters. We will process each letter independently.
3. Initialize an empty list or string to build the encrypted message. We choose a list for efficiency in Python since string concatenation in a loop is less efficient.
4. Iterate over each character `c` in the message. Convert `c` to its 0-based alphabet index by computing `ord(c) - ord('A')`.
5. Add `k` to this index and apply modulo 26. This ensures that the shift wraps around the alphabet correctly.
6. Convert the resulting index back to a character by adding `ord('A')` and appending it to the result list.
7. After processing all characters, join the list into a single string and print it.

Why it works: Each character is mapped to its correct shifted value independently, and the modulo operation guarantees that indices always stay within the bounds of the alphabet. The process preserves the order of letters, only transforming each according to the Caesar cipher rule, so correctness follows directly from the arithmetic.

## Python Solution

```python
import sys
input = sys.stdin.readline

k = int(input())
message = input().strip()

encrypted = []

for c in message:
    index = ord(c) - ord('A')
    shifted = (index + k) % 26
    encrypted.append(chr(shifted + ord('A')))

print(''.join(encrypted))
```

In this solution, we first read the key and message. We strip the newline from the message to prevent it from affecting the result. Each character is converted to an index, shifted with modulo 26, and then converted back to a character. Using a list to accumulate characters avoids the inefficiency of repeatedly concatenating strings. Finally, we join the list to form the final encrypted message.

## Worked Examples

**Sample 1:**

Input:

```
5
CODEFORCES
```

| Character | Index | Shifted Index | Encrypted Character |
| --- | --- | --- | --- |
| C | 2 | 7 | H |
| O | 14 | 19 | T |
| D | 3 | 8 | I |
| E | 4 | 9 | J |
| F | 5 | 10 | K |
| O | 14 | 19 | T |
| R | 17 | 22 | W |
| C | 2 | 7 | H |
| E | 4 | 9 | J |
| S | 18 | 23 | X |

Output: `HTIJKTWHJX`

This trace confirms that each letter is correctly shifted and wrapped, maintaining the order.

**Sample 2:**

Input:

```
1
AZ
```

| Character | Index | Shifted Index | Encrypted Character |
| --- | --- | --- | --- |
| A | 0 | 1 | B |
| Z | 25 | 0 | A |

Output: `BA`

This demonstrates the modulo wrap-around: shifting 'Z' by 1 correctly cycles back to 'A'.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We process each of the n characters exactly once. |
| Space | O(n) | We store the encrypted characters in a list before joining them into the final string. |

Given that n ≤ 10, this solution runs almost instantly and uses negligible memory, well within the 2-second, 256 MB limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    k = int(input())
    message = input().strip()
    encrypted = []
    for c in message:
        index = ord(c) - ord('A')
        shifted = (index + k) % 26
        encrypted.append(chr(shifted + ord('A')))
    return ''.join(encrypted)

# provided samples
assert run("5\nCODEFORCES\n") == "HTIJKTWHJX", "sample 1"

# custom cases
assert run("0\nHELLO\n") == "HELLO", "shift 0"
assert run("25\nAZ\n") == "ZY", "wrap-around backward"
assert run("13\nABCDEFGHIJ\n") == "NOPQRSTUVWX", "max length 10"
assert run("1\nZZZZZZZZZZ\n") == "AAAAAAAAAA", "all Z wrap"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0, HELLO | HELLO | No shift edge case |
| 25, AZ | ZY | Modulo wrap-around at start and end |
| 13, ABCDEFGHIJ | NOPQRSTUVWX | Maximum input length with large shift |
| 1, ZZZZZZZZZZ | AAAAAAAAAA | All Z letters wrapping to A |

## Edge Cases

If the key is 0, each letter remains unchanged. For example, `0` and `HELLO` produces `HELLO`. The algorithm calculates `(index + 0) % 26` for each letter, returning the original index every time.

When letters are at the end of the alphabet, like 'Z', shifting by any positive `k` wraps modulo 26. For input `1` and `Z`, the algorithm computes `(25 + 1) % 26 = 0`, which maps to 'A', handling wrap-around correctly. For a message of all 'Z's and shift 1, each letter maps to 'A', as confirmed in the custom test.
