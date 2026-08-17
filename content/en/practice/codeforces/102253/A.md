---
title: "CF 102253A - Add More Zero"
description: "The supercomputer can represent every integer from 0 through 2^m - 1. The youngster, however, only wants to work with the range from 1 through 10^k. We need the largest k for which every number in that decimal range is representable."
date: "2026-08-17T21:22:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102253
codeforces_index: "A"
codeforces_contest_name: "2017 Chinese Multi-University Training, BeihangU Contest"
rating: 0
weight: 102253
solve_time_s: 72
verified: true
draft: false
---

[CF 102253A - Add More Zero](https://codeforces.com/problemset/problem/102253/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

The supercomputer can represent every integer from `0` through `2^m - 1`. The youngster, however, only wants to work with the range from `1` through `10^k`. We need the largest `k` for which every number in that decimal range is representable.

Since the largest number the youngster uses is `10^k`, the entire range fits exactly when

`10^k <= 2^m - 1`.

So each test case gives `m`, and the output is the largest integer `k` satisfying this inequality. The case number must also be printed, starting from `1`. The official statement confirms the constraints of up to about `10^5` test cases with `1 <= m <= 10^5`.

The number of test cases is large enough that a solution doing work proportional to `m` for every case is already too expensive. With `10^5` cases and `m` as large as `10^5`, that could reach around `10^10` iterations. We need to reduce each test case to constant time.

There are two boundary details that commonly cause mistakes. First, when `m = 1`, the machine represents only `0` and `1`, so `10^0 = 1` fits but `10^1 = 10` does not. The answer is `0`, not `1`.

```
Input:
1

Output:
Case #1: 0
```

A careless implementation that computes the number of decimal digits of `2^m` might return `1`, but the machine's maximum value is `2^m - 1`, not `2^m`.

The second boundary is the strict difference between `2^m` and `2^m - 1`. For `m = 10`, the machine supports values through `1023`. Since `1000 <= 1023`, `k = 3` is valid.

```
Input:
10

Output:
Case #1: 3
```

A solution that mistakenly requires `10^k < 2^m - 1` would happen to reject some exact boundary cases. The clean way around this is to use the fact that both sides are integers and transform the condition into a strict inequality involving `2^m`.

## Approaches

A direct solution could try values of `k` starting from zero and test whether `10^k <= 2^m - 1`. This is correct because the valid values of `k` form a consecutive range starting at zero, so the first failed value is one larger than the answer. For `m = 100000`, however, the answer is around `30102`, so one test case requires about `30103` candidate checks. With `10^5` such cases, that is about `3,010,300,000` checks before even considering the cost of manipulating the increasingly large integers. That is far beyond what the one-second limit can support.

The useful observation is that the inequality contains powers of two and ten, so logarithms remove both exponentials immediately. Starting from

`10^k <= 2^m - 1`,

we have, because both sides are integers,

`10^k < 2^m`.

Taking base-10 logarithms gives

`k < m * log10(2)`.

The maximum integer strictly smaller than `m * log10(2)` is its floor, provided that this value is not itself an integer. It cannot be an integer for positive `m`. If `m * log10(2) = r`, then `2^m = 10^r`, but `10^r` contains a factor of `5` while `2^m` does not, which is impossible.

Thus the answer has the remarkably simple form

`answer = floor(m * log10(2))`.

This changes the problem from potentially tens of thousands of iterations per test case to one floating-point multiplication and one floor operation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m) per case | O(1) | Too slow |
| Optimal | O(1) per case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number `m` for the current test case. We only need this one value because the maximum usable decimal power depends directly on the machine's bit width.
2. Compute `m * log10(2)`. This is the real-valued boundary obtained by taking the base-10 logarithm of `2^m`.
3. Take the floor of that value. Since `m * log10(2)` cannot be an integer for positive `m`, this is exactly the largest integer `k` satisfying `k < m * log10(2)`.
4. Print the result using the required `Case #x: y` format.

Why it works can be expressed as a chain of equivalent conditions. A value of `k` is valid exactly when `10^k <= 2^m - 1`. Since both quantities are integers, this is equivalent to `10^k < 2^m`. Taking logarithms gives `k < m log10(2)`. The largest integer satisfying that inequality is `floor(m log10(2))`. The code computes precisely that quantity, so every printed answer is maximal and valid.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

LOG10_2 = math.log10(2.0)

def solve():
    t = int(input())
    out = []

    for case in range(1, t + 1):
        m = int(input())
        ans = int(m * LOG10_2)
        out.append(f"Case #{case}: {ans}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

`LOG10_2` is computed once rather than once per test case. Every test case then performs only one multiplication and an integer conversion, which is the constant-time formula from the algorithm.

The conversion `int(m * LOG10_2)` performs the required floor here because the value is positive. Python's `int` truncates toward zero, which is the same as taking the floor for positive numbers.

The `2^m - 1` boundary does not require explicitly constructing either `2^m` or `10^k`. The logarithmic derivation has already handled that boundary. Python integers also have arbitrary precision, but avoiding huge integer construction makes the implementation both simpler and faster.

For the given constraint `m <= 100000`, the largest result is only about `30102`. Double precision has far more precision than needed for this range, and `m * log10(2)` is not an integer for any positive integer `m`, so there is no exact-integer logarithmic boundary to confuse the floor operation.

The official sample has `m = 1` producing `0` and `m = 64` producing `19`, matching the formula.

## Worked Examples

For the first sample, `m = 1`.

| m | `m * log10(2)` | floor | answer |
| --- | --- | --- | --- |
| 1 | approximately `0.3010` | 0 | 0 |

The machine's largest representable value is `2^1 - 1 = 1`. The youngster can use `1 = 10^0`, but cannot use `10 = 10^1`, so `k = 0` is correct.

For the second sample, `m = 64`.

| m | `m * log10(2)` | floor | answer |
| --- | --- | --- | --- |
| 64 | approximately `19.2659` | 19 | 19 |

Here the machine supports values through `2^64 - 1`, which is greater than `10^19` but less than `10^20`. Thus the entire range from `1` through `10^19` fits, while the range through `10^20` does not. The result is `19`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case uses a constant number of arithmetic operations. |
| Space | O(t) | The output strings are stored before one final write. |

With about `10^5` test cases, the algorithm performs only about `10^5` constant-time computations. This is comfortably within the stated one-second and 128 MB limits.

## Test Cases

```python
import sys
import io
import math

LOG10_2 = math.log10(2.0)

def solve():
    input = sys.stdin.readline
    t = int(input())
    out = []

    for case in range(1, t + 1):
        m = int(input())
        ans = int(m * LOG10_2)
        out.append(f"Case #{case}: {ans}")

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
assert run("2\n1\n64\n") == (
    "Case #1: 0\n"
    "Case #2: 19"
), "provided sample"

# Minimum input
assert run("1\n1\n") == "Case #1: 0", "m = 1"

# Boundary where 10^3 first becomes possible
assert run("2\n9\n10\n") == (
    "Case #1: 2\n"
    "Case #2: 3"
), "boundary around k = 3"

# Several equal values, checking case numbering as well
assert run("4\n10\n10\n10\n10\n") == (
    "Case #1: 3\n"
    "Case #2: 3\n"
    "Case #3: 3\n"
    "Case #4: 3"
), "repeated values"

# Maximum allowed m
assert run("1\n100000\n") == "Case #1: 30102", "maximum m"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n` | `Case #1: 0` | Minimum `m` and the `2^m - 1` boundary |
| `2\n9\n10\n` | `Case #1: 2`, `Case #2: 3` | Off-by-one transition where `1000` becomes representable |
| `4\n10\n10\n10\n` | Four cases with answer `3` | Repeated inputs and correct case numbering |
| `1\n100000\n` | `Case #1: 30102` | Maximum constraint and large logarithmic result |

## Edge Cases

For `m = 1`, the formula gives `floor(log10(2)) = 0`. The algorithm never tries to construct `10^1`, so it naturally handles the smallest possible machine. The exact input is `1`, and the output is `Case #1: 0`.

The transition around `m = 10` catches the most likely off-by-one error. For `m = 9`, the maximum machine value is `511`, so `100` fits but `1000` does not, giving `2`. For `m = 10`, the maximum is `1023`, so `1000` fits and the answer becomes `3`. The logarithmic values are approximately `2.7093` and `3.0103`, producing exactly those floors.

For repeated values, such as four test cases all containing `10`, every answer must be `3`, but the case numbers must still increase from `1` through `4`. Since each input line is processed independently and the case counter is incremented on every iteration, the implementation preserves both properties.

For the maximum input `m = 100000`, the formula gives `floor(100000 * log10(2)) = 30102`. The algorithm does not construct `2^100000`, which would be a large integer, and does not iterate through thirty thousand candidate powers of ten. It performs the same constant-time calculation as it does for `m = 1`, which is the key reason the solution scales to the full input range.
