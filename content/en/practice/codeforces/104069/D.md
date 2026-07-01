---
title: "CF 104069D - Diary of Hapiness"
description: "We are given a sequence of integers representing how a person felt over a series of days. Each value is between -10 and 10 inclusive, so the sequence encodes short daily mood scores."
date: "2026-07-02T02:59:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104069
codeforces_index: "D"
codeforces_contest_name: "VII MaratonUSP Freshman Contest"
rating: 0
weight: 104069
solve_time_s: 42
verified: true
draft: false
---

[CF 104069D - Diary of Hapiness](https://codeforces.com/problemset/problem/104069/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers representing how a person felt over a series of days. Each value is between -10 and 10 inclusive, so the sequence encodes short daily mood scores. The task is to compute the arithmetic mean of all these values and classify the result into one of three emotional labels: positive mean, zero mean, or negative mean.

The output is not the numeric average itself, but only its sign. If the sum of all values divided by n is greater than zero, we print a happy face. If it is exactly zero, we print a neutral face. Otherwise, we print a sad face.

The key observation is that computing the average explicitly as a floating point number is unnecessary. Since division by a positive integer does not change the sign of a number, we can instead work directly with the sum of the array.

The constraint n ≤ 100000 means a linear scan is sufficient. Any solution that attempts recomputation over subranges or repeated aggregation would still pass, but anything worse than O(n) is unnecessary. A quadratic approach would do up to 10^10 operations in the worst case, which is clearly too slow for a 1 second limit.

Edge cases are mostly about sign handling.

One edge case is when all numbers are zero. The sum is zero and the output must be ":|". A careless floating-point average implementation might introduce rounding issues if implemented with floats, but integer sum avoids that entirely.

Another edge case is when the sum is very small but nonzero, such as [-1, 1]. The average is exactly zero, and integer arithmetic preserves that exactly. This is important because floating-point division could produce a tiny epsilon instead of exact zero depending on implementation details.

## Approaches

The brute-force interpretation of the problem is to compute the sum of all values and divide by n, then check the result. This is already linear time, since it requires a single pass to compute the sum and a constant-time division afterward. There is no meaningful subproblem structure or need for prefix computation, sorting, or data structures.

A slightly more naive version might compute the average in a loop by repeatedly adding and dividing, or recomputing partial sums multiple times. For example, recomputing the sum from scratch for each element would lead to O(n^2) time, which becomes infeasible when n reaches 100000.

The key simplification is recognizing that the sign of the average depends only on the sign of the total sum because n is strictly positive. This removes the need for division entirely in most implementations and avoids floating-point issues.

We reduce the problem to a single accumulation pass over the array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Recompute sum repeatedly | O(n^2) | O(1) | Too slow |
| Single pass sum | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer n, which represents the number of recorded days. This determines how many values we will aggregate.
2. Initialize a variable `total_sum = 0`. This variable will accumulate all daily scores as we process the input.
3. Iterate through each of the n integers in the sequence and add each value to `total_sum`. This builds the exact sum of all daily moods in one pass.
4. After processing all values, compare `total_sum` with zero. Since n is positive, dividing by n would not change the sign, so this comparison fully determines the answer.
5. If `total_sum > 0`, output ":)". If `total_sum == 0`, output ":|". Otherwise output ":(".

Why it works: the average is defined as `total_sum / n`. Since n > 0, the sign of the fraction is entirely determined by `total_sum`. The division cannot flip the sign, so checking the sum directly is equivalent to checking the average.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    arr = list(map(int, input().split()))
    
    total = 0
    for x in arr:
        total += x
    
    if total > 0:
        print(":)")
    elif total == 0:
        print(":|")
    else:
        print(":(")

if __name__ == "__main__":
    solve()
```

The solution begins by reading the input size and the list of integers. It then performs a single accumulation loop, which is the core computation. No intermediate structures are needed beyond an integer accumulator.

The final decision step compares the accumulated sum against zero. This avoids computing the actual average and avoids floating-point arithmetic entirely, which keeps the solution exact and safe.

## Worked Examples

### Example 1: `10 10 10 10 10`

We interpret this as five positive values.

| Step | Current Value | Running Sum |
| --- | --- | --- |
| 1 | 10 | 10 |
| 2 | 10 | 20 |
| 3 | 10 | 30 |
| 4 | 10 | 40 |
| 5 | 10 | 50 |

Final sum is 50, which is positive, so the output is ":)".

This confirms that consistently positive inputs produce a positive classification regardless of magnitude scaling.

### Example 2: `-1 1`

| Step | Current Value | Running Sum |
| --- | --- | --- |
| 1 | -1 | -1 |
| 2 | 1 | 0 |

Final sum is 0, so the output is ":|".

This demonstrates the cancellation case where positive and negative values balance exactly, and shows why integer accumulation correctly preserves exact neutrality.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed exactly once in a single pass |
| Space | O(1) | Only a single integer accumulator is used aside from input storage |

The input size up to 100000 fits comfortably within a linear scan. The operations performed are simple integer additions and comparisons, which are easily fast enough under typical Codeforces constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("5\n10 10 10 10 10\n") == ":)", "sample 1"
assert run("2\n-1 1\n") == ":|", "sample 2"

# custom cases
assert run("1\n5\n") == ":)", "single positive"
assert run("1\n-7\n") == ":(", "single negative"
assert run("3\n0 0 0\n") == ":|", "all zeros"
assert run("4\n1 2 -4 1\n") == ":|", "balanced mix"
assert run("6\n10 10 10 -10 -10 -10\n") == ":|", "symmetric cancellation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single positive | :) | minimal positive case |
| single negative | :( | minimal negative case |
| all zeros | : |  |
| balanced mix | : |  |
| symmetric cancellation | : |  |

## Edge Cases

A key edge case is when all values are zero. For example:

Input:

```
3
0 0 0
```

The algorithm initializes `total = 0` and never changes it. The final comparison `total == 0` triggers and outputs ":|", which is correct.

Another edge case is perfect cancellation:

Input:

```
2
-1 1
```

The running sum becomes 0 after processing both elements. Even though intermediate values are negative, the final state is what matters. The algorithm correctly outputs ":|".

A final subtle case is large positive or negative skew, such as all 10s or all -10s. Since the accumulator uses integer arithmetic and the maximum sum magnitude is bounded by 100000 × 10 = 10^6, there is no overflow risk in standard 32-bit or 64-bit integer types. The sign comparison remains stable and deterministic.
