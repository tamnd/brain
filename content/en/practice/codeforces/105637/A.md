---
title: "CF 105637A - Final Price"
description: "We are given a simple model of how a price evolves over time. There is an initial value representing the price on the first day, and then for each subsequent day we are given how much the price changes compared to the previous day."
date: "2026-06-26T13:50:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105637
codeforces_index: "A"
codeforces_contest_name: "The 2022 ICPC Asia Tehran Regional Contest"
rating: 0
weight: 105637
solve_time_s: 34
verified: true
draft: false
---

[CF 105637A - Final Price](https://codeforces.com/problemset/problem/105637/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a simple model of how a price evolves over time. There is an initial value representing the price on the first day, and then for each subsequent day we are given how much the price changes compared to the previous day. Each change is applied cumulatively, so the value on day i is the value on day i−1 plus the i−1-th change.

The task is to compute the final value after all daily changes have been applied, i.e. the value on the last day.

Although the statement sounds like a “time process”, the structure is purely linear accumulation. Every update is additive and independent, so we are really just reconstructing a prefix sum over the change array.

The input size is small, with at most 1000 days. That immediately tells us that even a straightforward O(n) scan is more than sufficient, since 10^3 operations is negligible under typical limits. Any solution beyond linear time would be unnecessary overhead.

A few edge cases are worth keeping in mind.

If there is only one day, there are no changes to apply, so the answer is just the initial value. A naive implementation that always tries to read at least one change would fail here.

If all changes are negative, the final price can still remain positive according to the problem guarantee, but intermediate implementations that accidentally clamp values to zero (a common mistake in simulation-style thinking) would produce incorrect results.

If changes include zeros, nothing special happens mathematically, but implementations that skip zero entries under the assumption they are irrelevant would break correctness.

## Approaches

A brute-force interpretation would simulate the process day by day. We start from the initial price and iterate through each change, updating the current value each time. This is already O(n) time, since each day contributes a constant-time update. There is no hidden state, no branching, and no combinatorial explosion.

Trying to “optimize” further would miss the point of the structure. The key observation is that the final value depends only on the sum of all changes, not on their order or intermediate states. The repeated updates collapse into a single arithmetic expression: initial value plus total sum of all daily differences.

So the optimal approach is not a different algorithmic technique, but a recognition that simulation and direct summation are identical here.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Step-by-step simulation | O(n) | O(1) | Accepted |
| Sum of changes directly | O(n) | O(1) | Accepted |

Both are effectively the same implementation in practice.

## Algorithm Walkthrough

1. Read the number of days n. This determines how many updates will be applied.
2. Read the initial price. This is the starting state before any changes.
3. Initialize a variable current with this initial price.
4. For each of the next n−1 lines, read the daily change and add it to current. Each addition corresponds exactly to moving one day forward in time.
5. After processing all changes, output current as the final price.

The key decision is that we never need to store the full sequence of values. Each intermediate price exists only as a temporary state, and since every transition is additive, keeping only the current value preserves all necessary information.

### Why it works

The process defines a recurrence of the form value[i] = value[i−1] + delta[i]. Expanding this recurrence repeatedly shows that value[n] equals the initial value plus the sum of all deltas. Since addition is associative, the grouping of operations does not matter, and no intermediate step affects the final result beyond contributing its value once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    cur = int(input())
    
    for _ in range(n - 1):
        cur += int(input())
    
    print(cur)

if __name__ == "__main__":
    solve()
```

The code directly implements the recurrence described in the walkthrough. The variable `cur` represents the evolving price. Each input line is immediately applied, avoiding unnecessary storage of the full array.

A common implementation mistake is trying to store all values in a list and recompute later. That is unnecessary but still safe here. A more serious mistake is initializing the accumulator incorrectly, for example starting from zero instead of the given initial price, which shifts the entire result.

## Worked Examples

### Example 1

Input:

```
2
11
68
```

| Step | Current Price | Operation |
| --- | --- | --- |
| Start | 11 | initial value |
| Day 2 | 79 | 11 + 68 |

Output is 79.

This confirms the simplest case where a single update is applied.

### Example 2

Input:

```
4
110
-5
0
27
```

| Step | Current Price | Operation |
| --- | --- | --- |
| Start | 110 | initial value |
| Day 2 | 105 | 110 - 5 |
| Day 3 | 105 | 105 + 0 |
| Day 4 | 132 | 105 + 27 |

Output is 132.

This trace shows that negative and zero changes behave uniformly under the same additive rule, with no special handling required.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | each daily change is processed once |
| Space | O(1) | only one accumulator variable is maintained |

The constraints allow up to 1000 days, so a single linear pass is well within limits. Even if the bound were much larger, the same approach would still scale efficiently since it avoids any nested computation.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    n = int(input())
    cur = int(input())
    for _ in range(n - 1):
        cur += int(input())
    return str(cur)

# provided samples
assert run("2\n11\n68\n") == "79"
assert run("4\n110\n-5\n0\n27\n") == "132"

# custom cases
assert run("1\n5\n") == "5", "single day no changes"
assert run("3\n10\n-3\n-7\n") == "0", "all negative changes"
assert run("5\n1\n1\n1\n1\n1\n") == "5", "uniform increments"
assert run("2\n1000000\n-1\n") == "999999", "boundary decrement"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 day only | initial value | no change handling |
| all negative | 0 | correctness under decreases |
| repeated +1 | linear accumulation | repeated additions |
| large values | 999999 | boundary arithmetic correctness |

## Edge Cases

For a single-day input, the algorithm reads the initial value and never enters the loop, so the output is exactly that value. There is no risk of uninitialized updates because the accumulator is set immediately from input.

For negative-only sequences, each subtraction is applied directly to the running total. The algorithm does not assume positivity at any point, so it naturally tracks decreases without clamping or overflow issues.

For zero changes, each iteration performs `cur += 0`, leaving the state unchanged. Since no condition filters out zero values, they are correctly included in the uniform accumulation process.
