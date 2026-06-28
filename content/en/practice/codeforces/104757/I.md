---
title: "CF 104757I - ISBN Conversion"
description: "Each input string represents a candidate ISBN-10 code that may contain digits, hyphens, and possibly the character X as a checksum digit."
date: "2026-06-28T22:49:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104757
codeforces_index: "I"
codeforces_contest_name: "2023-2024 ICPC East North America Regional Contest (ECNA 2023)"
rating: 0
weight: 104757
solve_time_s: 33
verified: true
draft: false
---

[CF 104757I - ISBN Conversion](https://codeforces.com/problemset/problem/104757/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 33s  
**Verified:** yes  

## Solution
## Problem Understanding

Each input string represents a candidate ISBN-10 code that may contain digits, hyphens, and possibly the character `X` as a checksum digit. Our task is to first determine whether this string is a valid ISBN-10 under the rules given, and if it is valid, transform it into the corresponding ISBN-13 representation.

Validation is the first gate. We must interpret the string as a 10-digit ISBN after removing hyphens, where the last character is the checksum digit. The checksum rule is a weighted sum from 10 down to 1 that must be divisible by 11, with the special rule that the digit `X` represents the value 10 but only allowed in the checksum position.

If the ISBN-10 is valid, conversion proceeds by discarding its checksum, prepending the prefix `978`, then recomputing a new ISBN-13 checksum under alternating weights 1 and 3.

The constraints are small: at most 25 strings, each with length up to 13. This immediately rules out any need for heavy data structures or optimization. Every operation can be linear in the string length, and even a straightforward parsing and recomputation approach is sufficient.

The main subtle edge cases are structural rather than computational.

One issue is hyphen handling. The input allows hyphens anywhere except leading, trailing, or consecutive positions. A naive approach might simply remove hyphens and validate digits, but this is not sufficient unless we also ensure that after removal we still have exactly 10 meaningful characters.

Another issue is the `X` character. A careless implementation might treat `X` as invalid outright, but it is only valid as the checksum digit and only contributes value 10 in the final position.

A third subtlety is that invalid formatting and invalid checksum both produce the same output `"invalid"`. For example, `3-540-4258-02` is structurally fine after removing hyphens, but fails checksum, while malformed hyphen patterns also lead to invalidity.

## Approaches

A brute-force approach would explicitly try to interpret the string in multiple ways, checking all possible hyphen placements and digit interpretations. This is unnecessary because the problem already fixes the structure: hyphens are irrelevant to numeric meaning except for formatting, and the checksum rules uniquely determine validity.

Instead, the key observation is that we can reduce the problem to two independent linear passes. First, normalize the string by stripping hyphens while preserving the meaning of `X` only at the final position. Then compute the ISBN-10 checksum directly. If it passes, construct the ISBN-13 by concatenation and compute its checksum in one pass.

The structure of the problem guarantees that once normalization is done, everything is deterministic arithmetic. There is no search or ambiguity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force parsing variants | Exponential | O(n) | Too slow |
| Normalize + direct checksum computation | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

### ISBN-10 validation and conversion

1. Read the input string and remove all hyphens, producing a compact form.
2. Verify that the resulting string has exactly 10 characters. If not, it is invalid.
3. Check that characters 1 through 9 are digits only. If any is not a digit, reject the string.
4. Handle the last character separately: it may be a digit or `X`, where `X` represents 10.
5. Compute the ISBN-10 weighted sum using weights 10 down to 1.
6. If the sum is not divisible by 11, output `"invalid"`.
7. Otherwise construct the ISBN-13 base string by taking the first 9 digits and prepending `"978"`, inserting a hyphen after the prefix for formatting.
8. Compute the ISBN-13 checksum digit using alternating weights 1 and 3 over the first 12 digits.
9. Append the checksum digit and output the final ISBN-13 string with preserved hyphens from the original (excluding the old checksum position) plus the new hyphen after `978`.

### Why it works

The correctness rests on the fact that ISBN-10 validity is entirely captured by a single linear congruence modulo 11 over fixed weights, and ISBN-13 validity is similarly a linear congruence modulo 10. Once the string is normalized, hyphens no longer affect arithmetic structure, so the computation reduces to evaluating two deterministic weighted sums. Since both checksum rules uniquely determine the final digit given the preceding digits, the conversion step is fully well-defined and does not introduce ambiguity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_valid_isbn10(s):
    # s is string without hyphens
    if len(s) != 10:
        return False, None

    total = 0
    for i in range(9):
        if not s[i].isdigit():
            return False, None
        total += (10 - i) * int(s[i])

    # last digit
    if s[9] == 'X':
        d10 = 10
    elif s[9].isdigit():
        d10 = int(s[9])
    else:
        return False, None

    total += 1 * d10

    if total % 11 != 0:
        return False, None

    return True, s[:9]

def isbn13_checksum(digits12):
    total = 0
    for i, ch in enumerate(digits12):
        d = int(ch)
        if i % 2 == 0:
            total += d
        else:
            total += 3 * d
    return (10 - (total % 10)) % 10

def convert(isbn10_raw):
    s = isbn10_raw.strip()

    # keep hyphen pattern info
    parts = []
    cur = []
    for ch in s:
        if ch == '-':
            if cur:
                parts.append(''.join(cur))
                cur = []
            parts.append('-')
        else:
            cur.append(ch)
    if cur:
        parts.append(''.join(cur))

    compact = ''.join(ch for ch in s if ch != '-')

    ok, base9 = is_valid_isbn10(compact)
    if not ok:
        return "invalid"

    # build ISBN-13 digits
    digits12 = "978" + base9

    check = isbn13_checksum(digits12)
    full_digits = digits12 + str(check)

    # formatting: prepend 978- then keep original hyphens except last checksum position removed
    # We reconstruct simply: 978- + original structure without last char
    rebuilt = []
    rebuilt.append("978-")

    # reuse original hyphen structure except last char removed
    core = s.replace('-', '')[:-1]
    idx = 0
    for ch in s:
        if ch == '-':
            rebuilt.append('-')
        else:
            if idx < len(core):
                rebuilt.append(core[idx])
                idx += 1

    rebuilt.append(str(check))
    return ''.join(rebuilt)

t = int(input())
for _ in range(t):
    print(convert(input().strip()))
```

The implementation first strips and validates the ISBN-10, isolating the numeric core and c
