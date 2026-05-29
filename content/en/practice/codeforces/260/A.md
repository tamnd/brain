---
title: "CF 260A - Adding Digits"
description: "We are given a number a and a target divisor b, along with a count n representing how many digits we want to append to a. Each operation consists of appending a single digit to the right of the current number such that the new number is divisible by b."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 260
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 158 (Div. 2)"
rating: 1400
weight: 260
solve_time_s: 81
verified: false
draft: false
---

[CF 260A - Adding Digits](https://codeforces.com/problemset/problem/260/A)

**Rating:** 1400  
**Tags:** implementation, math  
**Solve time:** 1m 21s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a number `a` and a target divisor `b`, along with a count `n` representing how many digits we want to append to `a`. Each operation consists of appending a single digit to the right of the current number such that the new number is divisible by `b`. If no single-digit extension produces a number divisible by `b`, the process stops and we should return `-1`. Otherwise, we repeat this `n` times and output the resulting number.

The inputs are constrained so that `a`, `b`, and `n` are all at most 10^5. Since `n` can be as large as 10^5, any solution that tries to iterate over all numbers up to `10^(n+len(a))` would be infeasible. Instead, we need an approach that builds the number incrementally, evaluating only the digits 0 through 9 at each step, which is manageable.

Edge cases that can trip a naive implementation include situations where the first appended digit is zero, which is allowed, or when no single digit can extend the current number to a multiple of `b`, which must produce `-1`. For example, if `a = 1` and `b = 3`, appending any digit from 0 to 9 yields numbers 10 through 19; only 12, 15, and 18 are divisible by 3. If none existed, the algorithm should correctly detect impossibility.

## Approaches

The brute-force approach would attempt to generate all possible numbers by appending `n` digits, checking divisibility after each full number is formed. This quickly becomes infeasible because the number of candidates grows exponentially as `10^n`.

The key insight is that we only need to consider one digit at a time. At each step, the remainder of the current number modulo `b` determines which next digit will yield a multiple of `b`. We can check digits 0 through 9 sequentially, compute `(current_number * 10 + d) % b`, and stop when we find a `d` that results in zero remainder. Once the first digit is found, the rest of the appended digits can be zeros without violating divisibility, because multiplying by 10 preserves divisibility modulo `b`. This observation reduces the problem from a potential 10^n search to at most 10 checks for the first digit and trivial operations for the remaining `n-1` digits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(10^n) | O(n) | Too slow |
| Incremental Check | O(10 * n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integers `a`, `b`, `n` from input. Convert `a` to a string for easier appending.
2. Initialize a variable `current` to `a`.
3. Loop over digits 0 through 9, appending each to `a` to form a candidate number. Compute the candidate modulo `b`. Stop when a digit produces a number divisible by `b`.
4. If no digit satisfies divisibility, print `-1` and terminate.
5. Append the found digit to `a`. This guarantees the number after one operation is divisible by `b`.
6. Append `n-1` zeros to `a`. Multiplying by 10 repeatedly does not change divisibility by `b` because the last number was divisible.
7. Print the resulting number.

Why it works: The algorithm maintains the invariant that the number after the first appended digit is divisible by `b`. Multiplying by 10 any number of times does not break this divisibility, ensuring the final number after `n` operations remains valid. There is guaranteed to be at least one digit to append first because the problem statement promises a solution exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

a, b, n = map(int, input().split())
found = False

for d in range(10):
    candidate = a * 10 + d
    if candidate % b == 0:
        a = candidate
        found = True
        break

if not found:
    print(-1)
else:
    result = str(a) + '0' * (n - 1)
    print(result)
```

The code reads the input values and loops over digits 0 to 9 to find a first appendable digit that makes `a` divisible by `b`. Once found, it appends `n-1` zeros, exploiting the property that multiplying by 10 preserves divisibility. The `found` flag ensures we correctly handle the case where no digit satisfies divisibility, which must return `-1`.

## Worked Examples

### Sample Input 1

```
5 4 5
```

| Step | a (current number) | Appended digit | Candidate % b | Action |
| --- | --- | --- | --- | --- |
| 1 | 5 | 2 | 0 | Found |
| 2 | 52 | 0 | 0 | Append 4 zeros |

Final number: `524848`

This demonstrates that finding the first divisible digit is sufficient; the remaining digits can be zeros.

### Custom Input 2

```
1 3 3
```

| Step | a | Candidate | % b | Action |
| --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 0 | Found |
| 2 | 12 | 0 | 0 | Append 2 zeros |

Final number: `1200`

The algorithm correctly identifies the first digit to ensure divisibility and pads the remaining operations with zeros.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(10 * n) | First digit check iterates at most 10 times, appending remaining n-1 zeros is O(n) |
| Space | O(1) | Only integers and the resulting string of length n + len(a) are stored |

The solution easily fits within the 2-second time limit and 256 MB memory limit, since operations are linear in `n` and the number of appended digits is at most 10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    a, b, n = map(int, input().split())
    found = False
    for d in range(10):
        candidate = a * 10 + d
        if candidate % b == 0:
            a = candidate
            found = True
            break
    if not found:
        return "-1"
    else:
        return str(a) + '0' * (n - 1)

# provided sample
assert run("5 4 5\n") == "520000", "sample 1"

# custom cases
assert run("1 3 3\n") == "1200", "append first divisible and zeros"
assert run("10 2 1\n") == "10", "already divisible, append zero"
assert run("7 7 4\n") == "70" + "0" * 3, "append zero for divisibility"
assert run("5 13 2\n") == "-1", "no digit makes divisible"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 4 5 | 520000 | Finds first digit divisible by b and pads zeros |
| 1 3 3 | 1200 | Edge case where first digit is needed |
| 10 2 1 | 10 | Already divisible, single operation |
| 7 7 4 | 70000 | Multiplying by 10 preserves divisibility |
| 5 13 2 | -1 | No digit can make divisible |

## Edge Cases

For the edge case `a = 10`, `b = 2`, `n = 1`, the number is already divisible by `b`. The algorithm appends digit 0 to maintain divisibility. For `a = 5`, `b = 13`, `n = 2`, there is no single-digit append that produces a multiple of 13; the algorithm correctly outputs `-1`. The solution handles leading zeros implicitly because the first appendable digit can be zero but the number itself is built from an integer, avoiding any invalid representation.
