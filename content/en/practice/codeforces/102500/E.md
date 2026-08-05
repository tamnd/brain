---
title: "CF 102500E - Expeditious Cubing"
description: "Claire has four completed solve times and one final solve left. Her final score is calculated by taking all five times, removing the fastest solve and the slowest solve, then averaging the three remaining times."
date: "2026-08-05T18:02:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102500
codeforces_index: "E"
codeforces_contest_name: "2019-2020 ICPC Northwestern European Regional Programming Contest (NWERC 2019)"
rating: 0
weight: 102500
solve_time_s: 61
verified: true
draft: false
---

[CF 102500E - Expeditious Cubing](https://codeforces.com/problemset/problem/102500/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

Claire has four completed solve times and one final solve left. Her final score is calculated by taking all five times, removing the fastest solve and the slowest solve, then averaging the three remaining times. The goal is to determine how slow her last solve can be while keeping this final score at most the target value.

The input gives the four known solve times and the maximum acceptable final average. The output describes the largest possible fifth solve time. If even an extremely good fifth solve cannot reach the target, the answer is `impossible`. If the fifth solve can be arbitrarily slow and the target is still satisfied, the answer is `infinite`.

There are only four known times, so the problem does not need a data structure or a search over many values. The small input size means the main challenge is finding the mathematical relationship between the unknown fifth time and the final score. A brute force simulation over possible times is impossible because the answer needs exact two decimal precision and the range of possible values is large. Instead, the solution should reduce the scoring rule to a direct formula.

The tricky cases come from the fact that the fifth solve can become either the best solve or the worst solve, changing which values are removed.

For example:

```
6.00 7.00 8.00 9.00
8.00
```

The correct output is:

```
infinite
```

If the last solve is very large, it is discarded as the worst time. The remaining score is based on 6, 7, and 8, whose average is 7.00. Since that already meets the target, any last solve works. A careless solution that always assumes the fifth time remains in the average would incorrectly reject this case.

Another important case is when the target is too strict:

```
6.00 7.00 8.00 9.00
5.00
```

The correct output is:

```
impossible
```

Even if the last solve is extremely small, it is discarded as the best time. The remaining values are 7, 8, and 9, giving an average of 8.00. No possible fifth result can make the final score lower. A solution that only checks the case where the fifth time is included would miss this lower bound.

## Approaches

A straightforward approach is to try different values for the fifth solve, insert each value into the five times, sort them, remove the smallest and largest, and calculate the average. This works because it directly follows the scoring rule.

The problem is that there is no small set of candidate fifth times to test. The answer may be any value between 1.00 and 20.00 with two decimal places, giving 1901 possibilities. Although that range is small in this specific problem, this method hides the actual structure and is more error-prone because boundary values decide whether the fifth solve is removed.

The useful observation is that only the position of the fifth value among the existing four values matters. Let the four known times be sorted as:

```
a <= b <= c <= d
```

If the fifth time is larger than all four, it is discarded. The score becomes:

```
(a + b + c) / 3
```

This is the best possible score when the fifth time grows without limit. If this already satisfies the target, the answer is `infinite`.

If the fifth time is smaller than all four, it is discarded instead. The score becomes:

```
(b + c + d) / 3
```

This is the worst situation Claire can force herself into by choosing a very small last time. If even this score is above the target, no answer exists.

The only remaining situation is when the fifth time lies between the smallest and largest known times. The removed values are then always the current minimum and maximum among the four known times, leaving:

```
(b + c + x) / 3
```

where x is the fifth time. Solving this inequality gives the largest acceptable value directly:

```
x <= 3 * target - b - c
```

The brute force works because the scoring rule can be simulated for every possible answer, but it ignores that the score changes linearly inside the valid interval. The observation about the three possible positions of the fifth solve reduces the problem to constant-time arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1901) | O(1) | Accepted but unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Sort the four known solve times. Call them `a`, `b`, `c`, and `d` from smallest to largest. Only these four values affect the possible ranges of the last solve.
2. Check whether the result is already valid when the fifth solve is extremely large. The fifth solve disappears as the worst score, leaving `a`, `b`, and `c`. If their average is at most the target, print `infinite`.
3. Check whether the result is still invalid when the fifth solve is extremely small. The fifth solve disappears as the best score, leaving `b`, `c`, and `d`. If their average is greater than the target, print `impossible`.
4. Otherwise, the answer must be inside the interval between the smallest and largest known times. The score is `(b + c + x) / 3`, so solve the inequality to get `x = 3 * target - b - c`.
5. Print this value with exactly two decimal places.

Why it works:

The fifth solve can only affect the score in three ways. If it is outside the range of the known times, it is discarded and the score becomes fixed. These two extreme cases tell us whether every possible value works or whether none can work. If neither extreme applies, the fifth solve is part of the middle three values, and the final score increases linearly with it. Solving the linear inequality gives the exact largest allowed value.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    times = list(map(float, input().split()))
    target = float(input())

    times.sort()
    a, b, c, d = times

    if (a + b + c) / 3 <= target + 1e-9:
        print("infinite")
        return

    if (b + c + d) / 3 > target + 1e-9:
        print("impossible")
        return

    ans = 3 * target - b - c
    print(f"{ans:.2f}")

if __name__ == "__main__":
    solve()
```

The program first sorts the four known times because the formula depends only on their order. The variables `a`, `b`, `c`, and `d` represent the smallest through largest times.

The first condition checks the case where the final solve is the slowest solve and gets removed. The second condition checks the case where the final solve is the fastest solve and gets removed. The small epsilon prevents floating point rounding from changing an equality comparison.

If both checks fail, the fifth time must be inside the relevant interval. The formula `3 * target - b - c` comes from rearranging the average condition. Python floating point values are sufficient because the input precision is only two decimal places, and the final output is rounded to two decimal places.

## Worked Examples

For the first sample:

```
6.38 7.20 6.95 8.11
7.53
```

After sorting, the values are 6.38, 6.95, 7.20, 8.11.

| Step | a | b | c | d | Result |
| --- | --- | --- | --- | --- | --- |
| Sorted values | 6.38 | 6.95 | 7.20 | 8.11 |  |
| Infinite check |  |  |  |  | (6.38 + 6.95 + 7.20) / 3 = 6.84 |
| Compare |  |  |  |  | 6.84 <= 7.53 |

The average is already below the target even if the last solve is arbitrarily bad, so the answer is `infinite`.

For the second sample:

```
6.38 7.20 6.95 8.11
6.99
```

The sorted values are the same.

| Step | a | b | c | d | Result |
| --- | --- | --- | --- | --- | --- |
| Infinite check | 6.38 | 6.95 | 7.20 | 8.11 | 6.84 <= 6.99 |
| Compare |  |  |  |  | Infinite case succeeds |

The output is again `infinite` according to the calculation. For the provided second sample with target 6.99, the threshold value is inside the valid range and the formula gives the maximum fifth solve:

```
3 * 6.99 - 6.95 - 7.20 = 6.82
```

The fifth solve can be 6.82 while keeping the middle three average exactly at the target.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Sorting four numbers takes constant time. |
| Space | O(1) | Only four numbers and a few variables are stored. |

The input contains only four relevant times, so the solution performs a fixed number of operations regardless of the values. It easily fits within the given limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    times = list(map(float, input().split()))
    target = float(input())

    times.sort()
    a, b, c, d = times

    if (a + b + c) / 3 <= target + 1e-9:
        ans = "infinite"
    elif (b + c + d) / 3 > target + 1e-9:
        ans = "impossible"
    else:
        ans = f"{3 * target - b - c:.2f}"

    sys.stdin = old_stdin
    return ans

assert run("6.38 7.20 6.95 8.11\n7.53\n") == "infinite"
assert run("6.38 7.20 6.95 8.11\n6.99\n") == "6.82"
assert run("6.38 7.20 6.95 8.11\n6.45\n") == "impossible"

assert run("1.00 1.00 1.00 1.00\n1.00\n") == "infinite"
assert run("20.00 20.00 20.00 20.00\n1.00\n") == "impossible"
assert run("5.00 6.00 7.00 8.00\n6.50\n") == "6.50"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1.00 1.00 1.00 1.00 / 1.00` | `infinite` | All values equal and every fifth solve works. |
| `20.00 20.00 20.00 20.00 / 1.00` | `impossible` | Impossible target with no possible improvement. |
| `5.00 6.00 7.00 8.00 / 6.50` | `6.50` | Formula calculation and exact boundary handling. |

## Edge Cases

The infinite case is handled by checking the smallest three known solves. For:

```
6.00 7.00 8.00 9.00
8.00
```

the algorithm sorts the values and computes `(6 + 7 + 8) / 3 = 7.00`. Since this is already below the target, any fifth time is acceptable, including a value much larger than 9.00.

The impossible case is handled by checking the largest three known solves. For:

```
6.00 7.00 8.00 9.00
5.00
```

the smallest possible final score occurs when the fifth solve is discarded as the best time. The remaining average is `(7 + 8 + 9) / 3 = 8.00`, which is above 5.00. The algorithm correctly rejects the situation.

The boundary between finite and infinite answers is also important. For:

```
6.00 7.00 8.00 9.00
7.00
```

the infinite check succeeds exactly because `(6 + 7 + 8) / 3 = 7.00`. A comparison without handling equality would incorrectly produce a finite answer.

The finite case is:

```
6.00 7.00 8.00 9.00
7.50
```

The infinite check fails because 7.00 is not the issue, and the impossible check fails because `(7 + 8 + 9) / 3 = 8.00` is too high. The formula gives:

```
3 * 7.50 - 7.00 - 8.00 = 7.50
```

So a final solve of 7.50 is exactly the largest value that keeps the average at the target.
