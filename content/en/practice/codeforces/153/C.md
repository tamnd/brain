---
title: "CF 153C - Caesar Cipher"
description: "We are asked to implement a Caesar cipher on an input string of uppercase Latin letters. Conceptually, this means each letter is shifted forward in the alphabet by a fixed number of positions, denoted by k. If the shift goes past 'Z', it wraps around to 'A'."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 153
codeforces_index: "C"
codeforces_contest_name: "Surprise Language Round 5"
rating: 2200
weight: 153
solve_time_s: 62
verified: true
draft: false
---

[CF 153C - Caesar Cipher](https://codeforces.com/problemset/problem/153/C)

**Rating:** 2200  
**Tags:** *special  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to implement a Caesar cipher on an input string of uppercase Latin letters. Conceptually, this means each letter is shifted forward in the alphabet by a fixed number of positions, denoted by _k_. If the shift goes past 'Z', it wraps around to 'A'. For example, with a shift of 3, 'X' becomes 'A', 'Y' becomes 'B', and 'Z' becomes 'C'.

The input consists of a string of length between 1 and 10 characters, so we are guaranteed a very small dataset. The second line is an integer _k_ between 0 and 25, which means the shift will never need multiple cycles of the alphabet. The output should be the transformed string after applying the Caesar cipher to every character.

One subtle edge case occurs when the letter is near the end of the alphabet and _k_ pushes it past 'Z'. For instance, with input `"XYZ"` and `k = 5`, the expected output is `"CDE"`. A naive approach that simply adds _k_ to the ASCII value of each character without wrapping would give invalid letters beyond 'Z'. Another edge case is `k = 0`, where the string should remain unchanged.

## Approaches

The brute-force approach is straightforward: iterate over each character, convert it to a number from 0 to 25 corresponding to its position in the alphabet, add _k_, and then wrap around using modulo 26. This works because the alphabet has a fixed size, and we can map the letters to integers easily using ASCII arithmetic. For a string of length _n_, this approach takes exactly _n_ operations, which in our case is at most 10. There is no performance problem; the "brute-force" is essentially optimal given the constraints.

The observation that simplifies everything is that the modulo operation inherently handles the wrap-around. Specifically, if we map 'A' to 0, 'B' to 1, ..., 'Z' to 25, then `(index + k) % 26` produces the correct shifted index. This modulo operation is the only key insight necessary. Once you think in terms of numerical indices rather than letters, the problem reduces to a simple array transformation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force / Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the input string and the integer shift _k_. The string will be treated as a sequence of characters, and _k_ is guaranteed to be within 0 to 25.
2. Initialize an empty list to hold the resulting characters. Using a list instead of building a string incrementally avoids quadratic time complexity in languages where strings are immutable.
3. Iterate over each character in the input string. Convert the character to an index from 0 to 25 by subtracting the ASCII value of 'A'. This gives a numeric representation suitable for arithmetic.
4. Compute the new index after shifting by adding _k_ and taking modulo 26. The modulo ensures that the shift wraps correctly from 'Z' back to 'A'.
5. Convert the new index back to a character by adding the ASCII value of 'A' and append it to the result list.
6. Join the list of characters into a single string and print it.

Why it works: The algorithm maintains a consistent mapping from characters to numeric indices, applies the shift in a closed numeric system modulo 26, and maps back to characters. The invariant is that every character's index is always between 0 and 25, so the modulo operation guarantees correctness for both small and boundary shifts.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
k = int(input())

result = []

for char in s:
    index = ord(char) - ord('A')
    new_index = (index + k) % 26
    result.append(chr(new_index + ord('A')))

print(''.join(result))
```

The code first reads the string and the shift, stripping any extra newline characters. We then iterate over each character, converting it to a zero-based index. Adding _k_ and taking modulo 26 ensures the wrap-around is handled correctly. Finally, we convert each shifted index back to a character and assemble the output string. Using `ord` and `chr` for character-index mapping is standard, and the order of operations is carefully arranged to avoid off-by-one errors.

## Worked Examples

Input `"CODEFORCES"` with `k = 5`:

| char | index | new_index | result char |
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

This demonstrates that every character is shifted independently and the modulo operation handles wrapping automatically.

Input `"XYZ"` with `k = 5`:

| char | index | new_index | result char |
| --- | --- | --- | --- |
| X | 23 | 2 | C |
| Y | 24 | 3 | D |
| Z | 25 | 4 | E |

This shows the wrap-around behavior at the end of the alphabet.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once in a fixed sequence of arithmetic operations. |
| Space | O(n) | A list of length n is used to store the resulting characters. |

With n ≤ 10, this runs in negligible time and uses trivial memory, well within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = sys.stdin.readline().strip()
    k = int(sys.stdin.readline())
    result = [chr((ord(c) - ord('A') + k) % 26 + ord('A')) for c in s]
    return ''.join(result)

# Provided samples
assert run("CODEFORCES\n5\n") == "HTIJKTWHJX", "sample 1"

# Minimum-size input
assert run("A\n0\n") == "A", "min size, no shift"

# Maximum-size input
assert run("ABCDEFGHIJ\n25\n") == "ZABCDEFGHI", "max size, wrap-around"

# All-equal letters
assert run("ZZZZZ\n1\n") == "AAAAA", "all Zs wrap to A"

# Boundary shift
assert run("XYZ\n5\n") == "CDE", "wrap-around near end"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| A\n0 | A | minimal length, zero shift |
| ABCDEFGHIJ\n25 | ZABCDEFGHI | maximal length, near-full shift |
| ZZZZZ\n1 | AAAAA | all letters wrap from Z to A |
| XYZ\n5 | CDE | boundary wrap-around |

## Edge Cases

For the input `"XYZ"` with `k = 5`, the numeric indices are 23, 24, 25. Adding 5 gives 28, 29, 30, which modulo 26 results in 2, 3, 4. Mapping these back to characters produces `"CDE"`. The algorithm correctly handles letters near the end of the alphabet without special branching or conditionals, confirming that the modulo operation fully manages edge wrapping.
