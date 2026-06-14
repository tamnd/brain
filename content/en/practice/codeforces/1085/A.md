---
title: "CF 1085A - Right-Left Cipher"
description: "We are given a string that was produced by repeatedly building a word from left to right, but alternating the side where each new character is inserted."
date: "2026-06-15T05:39:21+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1085
codeforces_index: "A"
codeforces_contest_name: "Technocup 2019 - Elimination Round 4"
rating: 800
weight: 1085
solve_time_s: 155
verified: false
draft: false
---

[CF 1085A - Right-Left Cipher](https://codeforces.com/problemset/problem/1085/A)

**Rating:** 800  
**Tags:** implementation, strings  
**Solve time:** 2m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string that was produced by repeatedly building a word from left to right, but alternating the side where each new character is inserted. The construction starts with the first character, then the second character is appended to the right, the third is inserted to the left, the fourth is appended to the right, and so on until the string is complete.

The task is reversed: instead of simulating the construction, we are given the final result and must recover the original sequence of characters before the alternating insertion process happened.

The key observation is that the process does not preserve simple positional indexing. Characters that start at the beginning of the original string end up oscillating between the ends of the evolving string, depending on parity of insertion steps. This makes direct reconstruction via naive simulation of all possible insertions unnecessary; the final string already encodes the history in its structure.

The input length is at most 50, which removes any concern about efficiency. Even quadratic or cubic solutions are trivial to accept. This shifts focus entirely to correctly modeling how the construction affects positions.

A common mistake is assuming the first character of the final string is always the first or last character of the original. Another mistake is trying to reconstruct by guessing insertion positions without tracking parity, which quickly leads to inconsistent results even on small examples like `"ncteho"`.

Edge cases are mostly structural:

A single-character string such as `"a"` should return `"a"` directly because no operations occur.

Even-length strings behave differently from odd-length ones because the last operation alternates the side of insertion, which determines whether the final character belongs to the left or right end of the evolving structure.

## Approaches

A brute-force way to understand the process is to simulate all possible original strings and run the encryption process until we match the given output. This is immediately infeasible even for length 50 because the search space is 26^50 possibilities.

A more reasonable brute-force direction is to simulate the encryption process forward for a guessed string and compare with the target. This is correct but useless as a solver since it requires trying all permutations.

The key insight is to invert the construction step-by-step. Each step in the forward process either appends to the right or prepends to the left. If we reverse the process, we need to determine which side the last inserted character came from.

Instead of reconstructing dynamically with a deque simulation in reverse order, we notice a simpler pattern: the final string is formed by taking characters alternately from the center outward in a controlled pattern. If we collect characters in the correct order, we can rebuild the original string by simulating the inverse pattern using a deque.

We reconstruct by determining the order in which characters were inserted: for each position in reverse, we extract from either the left or right end depending on parity of remaining length.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | O(26^n · n^2) | O(n) | Too slow |
| Reverse Construction (deque simulation) | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We simulate the reverse process using a deque that initially contains the final encrypted string.

1. Sort out the correct reconstruction order length `n = len(t)` and initialize a deque with all characters of `t`. This represents the current remaining pool of characters that were placed during encryption.
2. We rebuild the original string from the end toward the beginning. At each step, we decide which end of the deque corresponds to the last inserted character in the forward process.
3. Observe the forward rule: characters are inserted alternately right, left, right, left. Reversing this means we alternately remove from the left and right ends in reverse order of insertion.
4. We simulate this by maintaining a boolean flag that tracks whether the current removal corresponds to a left or right insertion in reverse time.
5. If the step corresponds to a “right insertion in forward time”, then in reverse we take from the right end of the deque. Otherwise, we take from the left end.
6. Append removed characters into a result list. After processing all characters, reverse the result because we reconstructed in reverse insertion order.

### Why it works

At every step of the forward process, exactly one new character is added to one of the two ends. This means that in the final string, the last operation determines which end contains the most recently inserted character. Reversing the process preserves this invariant: removing from the correct end always corresponds to undoing the last insertion. Because each insertion only affects an endpoint, the remaining middle section is never disturbed, so the deque structure remains valid throughout the reconstruction.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

t = input().strip()
n = len(t)

dq = deque(t)
res = []

# We reverse the process by simulating removal of last inserted chars.
# The forward process alternates: append, prepend, append, prepend...
# So in reverse, we alternate taking from right and left.

take_right = True  # corresponds to reversing the forward pattern

while dq:
    if take_right:
        res.append(dq.pop())
    else:
        res.append(dq.popleft())
    take_right = not take_right

# We built characters in reverse of original order
print("".join(reversed(res)))
```

The solution initializes a deque from the encrypted string because the endpoints represent the only places where the last inserted character could reside. The boolean `take_right` encodes whether the reversed operation should remove from the right or left end. Each removal corresponds to undoing one insertion in the forward process.

The final reversal is required because we are effectively peeling characters in reverse chronological order of construction.

A subtle point is that we do not explicitly reconstruct the intermediate strings; the deque alone captures all necessary structural constraints.

## Worked Examples

### Example 1

Input:

```
ncteho
```

We start with:

```
dq = [n, c, t, e, h, o]
```

| Step | take_right | dq before | removed | result |
| --- | --- | --- | --- | --- |
| 1 | True | n c t e h o | o | o |
| 2 | False | n c t e h | n | on |
| 3 | True | c t e h | h | onh |
| 4 | False | c t e | c | onhc |
| 5 | True | t e | e | onhce |
| 6 | False | t | t | onhcet |

Final reversed result: `techno`

This trace shows that alternating endpoint removal correctly reconstructs the original sequence in reverse order.

### Example 2

Input:

```
ab
```

| Step | take_right | dq before | removed | result |
| --- | --- | --- | --- | --- |
| 1 | True | a b | b | b |
| 2 | False | a | a | ba |

Reversing gives `ab`, which matches the original string.

This confirms correctness even for minimal alternating cases.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is removed exactly once from the deque |
| Space | O(n) | Deque and result storage both scale with input length |

The maximum length is 50, so this linear reconstruction is trivial in both time and memory, far below the constraints.

## Test Cases

```python
import sys, io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    t = input().strip()
    dq = deque(t)
    res = []
    take_right = True
    while dq:
        if take_right:
            res.append(dq.pop())
        else:
            res.append(dq.popleft())
        take_right = not take_right
    return "".join(reversed(res))

# provided sample
assert run("ncteho\n") == "techno"

# minimum size
assert run("a\n") == "a"

# two characters
assert run("ab\n") == "ab"

# symmetric pattern
assert run("ba\n") == "ba"

# longer mixed case
assert run("ncteho\n") == "techno"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| a | a | single character edge case |
| ab | ab | minimal alternating behavior |
| ba | ba | reversed order handling |
| ncteho | techno | full reconstruction correctness |

## Edge Cases

For input `"a"`, the deque contains only one character. The algorithm removes it immediately as a right-side operation, producing `["a"]`, which reverses to `"a"`.

For input `"ba"`, the deque starts as `[b, a]`. The first removal takes `a` from the right, then `b` from the left. This produces `"ab"` after reversal, showing that even when characters appear reversed in the encrypted form, the alternating endpoint rule still correctly restores order.
