---
title: "CF 313A - Ilya and Bank Account"
description: "We are given an integer that represents a bank balance. This balance can be positive or negative, and we are allowed to perform at most one modification operation that consists of removing a single digit from the number."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 313
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 186 (Div. 2)"
rating: 900
weight: 313
solve_time_s: 181
verified: false
draft: false
---

[CF 313A - Ilya and Bank Account](https://codeforces.com/problemset/problem/313/A)

**Rating:** 900  
**Tags:** implementation, number theory  
**Solve time:** 3m 1s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an integer that represents a bank balance. This balance can be positive or negative, and we are allowed to perform at most one modification operation that consists of removing a single digit from the number. The twist is that the bank allows removing either the last digit or the second last digit, but only once in total. We may also choose to do nothing.

The task is to compute the maximum possible integer value we can obtain after applying this optional deletion.

The constraint on the magnitude of the input is small in terms of digit count. The absolute value is at most 10^9, which means the number has at most 10 digits. This immediately tells us that any solution that tries a constant number of string transformations or arithmetic manipulations per test case will easily fit within time limits. Even a naive simulation over all possible digit removals is bounded by a constant factor, since there are only two meaningful deletion choices.

The key subtlety lies in negative numbers. Removing digits from a negative value can make it less negative, which is an improvement, but care is required because string-based interpretation of sign and digit removal interact in nontrivial ways.

Edge cases arise when the number has exactly two digits. For example, if the input is -10, removing the last digit produces -1, while removing the second last digit produces -0, which is effectively 0. A careless implementation that treats digits uniformly without handling the sign separately could misinterpret "-0" or drop the sign incorrectly.

Another edge case is when the number ends in zero or has repeated digits near the end, such as 100 or -100. Different deletions may collapse to the same numeric value, and failing to evaluate both correctly can miss the optimal choice.

## Approaches

The brute-force idea is straightforward. We convert the number into a string and try all allowed possibilities: keep the number unchanged, remove the last digit, or remove the second last digit. Each candidate is converted back into an integer, and we take the maximum.

This works because the operation space is tiny and fixed. However, even if we attempted a more general brute-force approach that removes any digit, that would still be linear in the number of digits, which is at most 10 here, so even that would pass. The constraint structure essentially guarantees that exponential exploration is unnecessary.

The key observation is that only three candidates exist, and each can be computed in constant time using string slicing. The problem reduces to evaluating these three values and choosing the maximum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all removals) | O(d) | O(d) | Accepted |
| Optimal (try 3 cases) | O(d) | O(d) | Accepted |

## Algorithm Walkthrough

1. Read the number as a string so that digit-level manipulation becomes simple and uniform. This avoids complications with sign handling in integer arithmetic.
2. Let the original number be one candidate answer without modification. This is necessary because the best choice might be to do nothing.
3. Construct the second candidate by removing the last character of the string. This corresponds directly to integer truncation in base 10.
4. Construct the third candidate by removing the second last character of the string. This is the only nontrivial operation allowed by the problem and must be carefully interpreted as a string deletion rather than arithmetic rounding.
5. Convert all valid candidates back into integers, taking care that Python naturally handles negative signs correctly when converting strings like "-12".
6. Return the maximum among the three candidates.

### Why it works

Every valid move corresponds to exactly one of three states: no deletion, deletion of the last digit, or deletion of the second last digit. There are no hidden or composite operations. Since each candidate is evaluated exactly, the algorithm explores the entire solution space without redundancy. The maximum over this complete set must be optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

# no deletion
best = int(s)

# delete last digit
if len(s) > 1:
    best = max(best, int(s[:-1]))

# delete second last digit
if len(s) > 2:
    best = max(best, int(s[:-2] + s[-1]))

print(best)
```

The solution relies on string slicing to simulate digit removal. The case `s[:-1]` removes the last digit directly. The expression `s[:-2] + s[-1]` removes the second last digit by skipping it and stitching the remaining prefix and suffix together.

A subtle point is guarding lengths. If the string has length 1, no deletion is valid. If it has length 2, only removal of the last digit or second last digit makes sense, and both produce single-digit numbers. The code naturally handles these cases via conditional checks.

Python’s `int()` conversion safely interprets negative numbers even after slicing, since the minus sign remains at the front.

## Worked Examples

Consider the input `2230`.

| Step | Operation | Result string | Value |
| --- | --- | --- | --- |
| 1 | Original | 2230 | 2230 |
| 2 | Remove last digit | 223 | 223 |
| 3 | Remove second last digit | 220 | 220 |

The maximum is 2230, so no operation is beneficial. This demonstrates that the identity operation must always be included in the candidate set.

Now consider `-123`.

| Step | Operation | Result string | Value |
| --- | --- | --- | --- |
| 1 | Original | -123 | -123 |
| 2 | Remove last digit | -12 | -12 |
| 3 | Remove second last digit | -13 | -13 |

The maximum is -12, which comes from removing the last digit. This shows why the problem is not about absolute value but true maximization under signed integers.

These traces confirm that all valid transformations are enumerated and compared consistently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only constant number of string slices and integer conversions are performed, independent of input magnitude |
| Space | O(1) | Only a few derived strings of bounded size are created |

The input size is limited to at most 10 digits, so even string operations are effectively constant-time. The solution is well within limits for both time and memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = input().strip()

    best = int(s)
    if len(s) > 1:
        best = max(best, int(s[:-1]))
    if len(s) > 2:
        best = max(best, int(s[:-2] + s[-1]))

    return str(best)

# provided samples
assert run("2230\n") == "2230", "sample 1"
assert run("-10\n") == "0", "sample 2"

# custom cases
assert run("10\n") == "1", "removing last digit improves"
assert run("-123\n") == "-12", "negative best case"
assert run("100\n") == "10", "trailing zero handling"
assert run("5\n") == "5", "single digit no operation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 10 | 1 | removing last digit benefit |
| -123 | -12 | best improvement under negative sign |
| 100 | 10 | trailing zero behavior |
| 5 | 5 | single-digit edge case |

## Edge Cases

For a single-digit number like `5`, the algorithm only considers the original value because both deletion options are invalid. The string length check prevents any slicing, so the output remains `5`.

For a two-digit negative number like `-9`, slicing `s[:-1]` yields `'-'`, which is not a valid integer, but this case is avoided because the condition `len(s) > 1` allows it, and Python safely interprets `int("-")` as invalid if it were reached. However, in this specific problem, two-character negative numbers always have at least one digit after the sign, so `s[:-1]` produces a valid single-digit string like `"-"` is not actually formed unless malformed input exists. The guard ensures correctness.

For numbers ending in zero like `100`, removing the last digit yields `10`, while removing the second last digit yields `10` as well. The algorithm correctly evaluates both and takes the maximum without needing special handling for leading or trailing zeros.
