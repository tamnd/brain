---
title: "CF 313A - Ilya and Bank Account"
description: "The problem centers on Ilya’s bank account balance, which is a signed integer. Positive values indicate savings, and negative values indicate debt."
date: "2026-06-06T01:03:21+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 313
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 186 (Div. 2)"
rating: 900
weight: 313
solve_time_s: 56
verified: true
draft: false
---

[CF 313A - Ilya and Bank Account](https://codeforces.com/problemset/problem/313/A)

**Rating:** 900  
**Tags:** implementation, number theory  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem centers on Ilya’s bank account balance, which is a signed integer. Positive values indicate savings, and negative values indicate debt. The bank allows Ilya a one-time operation: he can remove either the last digit or the second-to-last digit from his balance to potentially improve it. The goal is to determine the maximum balance achievable using this operation, or to leave the number unchanged if that produces the best outcome.

The input is a single integer `n` where `10 ≤ |n| ≤ 10^9`. The lower bound ensures the number has at least two digits, which makes the operation of removing digits meaningful. The upper bound is comfortably within 32-bit integer range, so arithmetic operations are safe without needing arbitrary-precision handling.

Non-obvious edge cases include negative numbers with small absolute value, such as `-10` or `-11`. Simply dropping the last digit could create `-1` or `-1` respectively, and dropping the second-to-last digit could produce `0` or `-1`. A careless implementation could ignore the second-to-last digit option or miscompute the new value, yielding suboptimal results.

## Approaches

A brute-force approach would attempt every combination of removing one digit or leaving the number as is. For positive numbers, removing digits will almost never increase the value, so the brute force reduces to checking two operations for negative numbers. The maximum number of checks is three: keep `n` as-is, remove the last digit, remove the second-to-last digit. Since this is constant work per input, the brute force is actually acceptable in practice.

The key observation that leads to a simple optimal solution is that for positive numbers, doing nothing is always optimal. For negative numbers, the only potential improvements come from removing either the last or second-to-last digit. Converting these modified numbers into integers and taking the maximum among the three options guarantees correctness. This observation reduces the problem to O(1) operations without any loops or recursion.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n` from input. This represents the current bank account state.
2. If `n` is non-negative, print `n` immediately because removing digits cannot improve a positive balance.
3. If `n` is negative, convert `n` to a string to manipulate its digits. Let `s` be the string representation of `n`.
4. Construct two candidate balances: remove the last digit to form `candidate1` and remove the second-to-last digit to form `candidate2`. This is done by slicing the string: `s[:-1]` for the last digit and `s[:-2] + s[-1]` for the second-to-last digit. Convert these strings back to integers.
5. Compute the maximum among the three values: `n`, `candidate1`, and `candidate2`. This maximum is the best possible account balance.
6. Print the result.

The correctness relies on the invariant that, for negative numbers, removing digits either makes the number less negative or keeps it unchanged. There are no other operations to consider, so comparing the three possibilities is exhaustive and guarantees the maximum result.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

if n >= 0:
    print(n)
else:
    s = str(n)
    candidate1 = int(s[:-1])  # remove last digit
    candidate2 = int(s[:-2] + s[-1])  # remove second-to-last digit
    print(max(n, candidate1, candidate2))
```

The solution begins by handling positive numbers separately to avoid unnecessary string operations. For negative numbers, string slicing ensures we correctly remove the target digits. A common mistake is misindexing when removing the second-to-last digit; `s[:-2] + s[-1]` correctly preserves the digits before the last two and appends the final digit.

## Worked Examples

Sample Input 1:

```
2230
```

| Step | n | s | candidate1 | candidate2 | max(n, c1, c2) |
| --- | --- | --- | --- | --- | --- |
| 1 | 2230 | N/A | N/A | N/A | 2230 |

The input is positive, so no digit removal is beneficial. The algorithm returns 2230.

Sample Input 2:

```
-123
```

| Step | n | s | candidate1 | candidate2 | max(n, c1, c2) |
| --- | --- | --- | --- | --- | --- |
| 1 | -123 | "-123" | -12 | -13 | -12 |

Removing the last digit gives -12, which is better than -13 or -123. The maximum balance is -12.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only constant-time arithmetic and string slicing operations. |
| Space | O(1) | Only a few integer variables and a short string are stored. |

The algorithm comfortably fits within the 2-second time limit and 256 MB memory limit for any valid input.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    if n >= 0:
        return str(n)
    else:
        s = str(n)
        candidate1 = int(s[:-1])
        candidate2 = int(s[:-2] + s[-1])
        return str(max(n, candidate1, candidate2))

# provided samples
assert run("2230\n") == "2230", "sample 1"
assert run("-123\n") == "-12", "sample 2"

# custom cases
assert run("-10\n") == "0", "negative two-digit boundary"
assert run("-11\n") == "-1", "negative two-digit equal digits"
assert run("10\n") == "10", "positive two-digit minimum"
assert run("-1000000000\n") == "-100000000", "large negative number"
assert run("999999999\n") == "999999999", "large positive number"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| -10 | 0 | Removing the second-to-last digit produces 0 |
| -11 | -1 | Removing either digit yields the best result of -1 |
| 10 | 10 | Positive number should remain unchanged |
| -1000000000 | -100000000 | Handles large negative number correctly |
| 999999999 | 999999999 | Handles large positive number |

## Edge Cases

For `n = -10`, removing the last digit produces `-1` but removing the second-to-last digit yields `0`, which is the maximum. The algorithm computes `candidate1 = -1` and `candidate2 = 0`, then returns `max(-10, -1, 0) = 0`, demonstrating correct handling of small negative numbers.

For `n = -11`, both candidates produce `-1`. The algorithm computes `candidate1 = -1` and `candidate2 = -1`, then returns `max(-11, -1, -1) = -1`, confirming it handles repeated digits correctly.
