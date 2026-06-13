---
title: "CF 1228A - Distinct Digits"
description: "We are given a closed interval of integers from l to r, and we need to find any number inside this interval whose decimal representation does not repeat any digit. In other words, when writing the number as a string of digits, every character must be unique."
date: "2026-06-13T18:56:24+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1228
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 589 (Div. 2)"
rating: 800
weight: 1228
solve_time_s: 243
verified: true
draft: false
---

[CF 1228A - Distinct Digits](https://codeforces.com/problemset/problem/1228/A)

**Rating:** 800  
**Tags:** brute force, implementation  
**Solve time:** 4m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a closed interval of integers from `l` to `r`, and we need to find any number inside this interval whose decimal representation does not repeat any digit. In other words, when writing the number as a string of digits, every character must be unique.

The task is not to optimize for anything like minimum or maximum value. Any valid number inside the range is acceptable, so the structure of the solution can be simple as long as it reliably finds one such number if it exists.

The constraint `r ≤ 100000` is small enough that even checking every number in the interval is feasible. The interval size is at most `10^5`, and for each number we only inspect up to 6 digits. That leads to roughly `6 * 10^5` operations in the worst case, which is comfortably within time limits for Python.

A naive mistake often appears when people try to construct a number greedily or assume a pattern like always picking `l` if it works, or trying to "fix" duplicates digit by digit. These approaches can fail because digit uniqueness is a global property. For example, `121` fails not because of a local issue but because the digit `1` appears in two separate positions.

Another subtle edge case is when no number in the interval is valid. For example, `l = 110` and `r = 120` contains only numbers like `110, 111, 112 ...`, all of which repeat digits. In such cases the correct output is `-1`.

Finally, single-digit numbers always satisfy the condition since there is only one digit to begin with. Any implementation must handle ranges starting from `1` correctly.

## Approaches

The most direct idea is to iterate through every integer `x` from `l` to `r` and check whether its digits are all distinct. Checking a number is straightforward: convert it to a string and verify that no character appears more than once, typically using a set.

This brute-force approach works because the input size is small. In the worst case, we examine `100000` numbers, and each check scans at most 6 digits. That gives a bounded, small constant factor workload.

The key observation is that there is no hidden structure to exploit. The constraint is intentionally designed so that brute force is the intended solution. Any attempt to build numbers combinatorially or skip ranges is unnecessary.

We therefore reduce the problem to scanning the interval and validating each candidate.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((r - l + 1) * d) | O(1) | Accepted |
| Optimal | O((r - l + 1) * d) | O(1) | Accepted |

Here `d ≤ 6` is the number of digits in each number.

## Algorithm Walkthrough

1. Iterate over every integer `x` from `l` to `r`. We do this because any valid answer must lie in this range, and there is no structure that allows skipping candidates safely.
2. For each `x`, convert it into a string representation. This allows us to treat digits as characters and simplifies uniqueness checking.
3. Check whether all digits in the string are distinct. We maintain a set and insert each digit as we scan. If we ever see a digit already in the set, we reject the number immediately.
4. If a number passes the uniqueness check, output it immediately and terminate. This is valid because any solution is acceptable.
5. If the loop finishes without finding any valid number, output `-1`.

### Why it works

Each candidate number is independently verified for the required property, and every number in the interval is examined exactly once. Since the check is exact and no transformations are applied, no valid candidate can be skipped. The algorithm cannot falsely accept an invalid number because repetition is explicitly detected using a set membership test.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    l, r = map(int, input().split())
    
    for x in range(l, r + 1):
        s = str(x)
        seen = set()
        ok = True
        for ch in s:
            if ch in seen:
                ok = False
                break
            seen.add(ch)
        if ok:
            print(x)
            return
    
    print(-1)

if __name__ == "__main__":
    solve()
```

The core loop directly implements the brute-force scan. The conversion to string is used only for digit extraction, and the set ensures constant-time detection of duplicates. Early exit is important because once a valid number is found, further search is unnecessary.

The only boundary condition to be careful about is the inclusive range `r + 1` in Python’s `range`, which ensures the endpoint is checked.

## Worked Examples

### Example 1

Input:

```
121 130
```

We check numbers sequentially:

| x | digits | seen process | valid |
| --- | --- | --- | --- |
| 121 | 1,2,1 | repeat 1 | no |
| 122 | 1,2,2 | repeat 2 | no |
| 123 | 1,2,3 | all unique | yes |

Once `123` is found, we stop.

This confirms early termination behavior and shows how the algorithm stops at the first valid candidate.

### Example 2

Input:

```
110 115
```

| x | digits | seen process | valid |
| --- | --- | --- | --- |
| 110 | 1,1,0 | repeat 1 | no |
| 111 | 1,1,1 | repeat 1 | no |
| 112 | 1,1,2 | repeat 1 | no |
| 113 | 1,1,3 | repeat 1 | no |
| 114 | 1,1,4 | repeat 1 | no |
| 115 | 1,1,5 | repeat 1 | no |

No valid number exists, so the output is `-1`.

This demonstrates the full-range failure case where every candidate is rejected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((r - l + 1) * d) | We scan every number in the interval and check each digit once |
| Space | O(1) | The set holds at most 10 digits |

The maximum number of iterations is `10^5`, and each iteration processes at most 6 digits, so the solution comfortably fits within both time and memory limits.

## Test Cases

```python
import sys, io

def solve():
    l, r = map(int, input().split())
    for x in range(l, r + 1):
        s = str(x)
        seen = set()
        ok = True
        for ch in s:
            if ch in seen:
                ok = False
                break
            seen.add(ch)
        if ok:
            print(x)
            return
    print(-1)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    solve()
    
    out = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out

# provided sample
assert run("121 130") == "123"

# custom cases
assert run("1 9") == "1", "single digit always valid"
assert run("11 11") == "-1", "all digits repeated"
assert run("98 102") in ["98", "102"], "cross boundary behavior"
assert run("123 123") == "123", "already valid single value"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 9 | 1 | smallest range and immediate success |
| 11 11 | -1 | single value failing condition |
| 98 102 | 98 or 102 | boundary crossing and flexibility |
| 123 123 | 123 | trivial valid case |

## Edge Cases

For a single-value range like `11 11`, the algorithm checks only that number, detects the repeated digit `1`, and correctly outputs `-1`.

For a range where the first number is valid, such as `1 9`, the algorithm immediately accepts `1` and stops, showing that early termination prevents unnecessary scanning.

For boundary transitions like `98 102`, the algorithm correctly handles different digit lengths without any special casing, since all numbers are treated uniformly as strings.

For degenerate cases where all candidates are invalid, like `110 115`, every iteration fails the uniqueness check and the algorithm correctly exhausts the loop and returns `-1`.
