---
title: "CF 1615A - Closing The Gap"
description: "We have a row of towers, each with a certain number of blocks stacked vertically. The goal is to make the heights of all towers as close as possible. On any day, we can take a block from one tower and place it on another tower."
date: "2026-06-10T06:38:08+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1615
codeforces_index: "A"
codeforces_contest_name: "Codeforces Global Round 18"
rating: 800
weight: 1615
solve_time_s: 71
verified: true
draft: false
---

[CF 1615A - Closing The Gap](https://codeforces.com/problemset/problem/1615/A)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a row of towers, each with a certain number of blocks stacked vertically. The goal is to make the heights of all towers as close as possible. On any day, we can take a block from one tower and place it on another tower. The ugliness of the arrangement is the difference between the tallest and shortest towers. We want to determine the smallest possible ugliness we can achieve after any number of block moves.

The input consists of multiple test cases. For each test case, we get the number of towers `n` and the heights of those towers. The output should be a single integer per test case representing the minimum achievable ugliness.

The constraints are moderate: up to 100 towers and 1000 test cases. Individual tower heights can be up to $10^7$. Since `n` is small, an algorithm that is quadratic in `n` is feasible, but a linear solution is preferable. Edge cases include towers that are already equal, towers with only one very tall or very short building, and cases where the sum of blocks does not divide evenly by `n`. A naive approach that repeatedly moves one block at a time would be correct but unnecessarily slow. For example, if the towers are `[1, 2, 3, 1, 5]`, we cannot always reach equal heights, and the minimum ugliness ends up being `1`.

## Approaches

The brute-force approach would attempt to repeatedly move blocks from the tallest tower to the shortest until no improvement is possible. While this would eventually converge, it could require up to $O(n \cdot \text{max}(a_i))$ operations, which is infeasible when `a_i` can reach $10^7$. We need a smarter approach.

The key observation is that moving blocks only redistributes the total sum of blocks across towers. Let `total = sum(a)`. If `total` divides evenly by `n`, we can make all towers equal, achieving an ugliness of 0. If `total` does not divide evenly, then some towers must have `floor(total/n)` blocks and some must have `ceil(total/n)` blocks. The difference between these two quantities is always `1`, which is the minimum achievable ugliness.

This observation allows us to compute the result in constant time per test case: check the divisibility of the sum by the number of towers and output either `0` or `1`. No actual block-moving simulation is needed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * max(a_i)) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n` and the array of tower heights `a`.
3. Compute the sum of all tower heights.
4. Compute the integer division `avg = total // n`.
5. Compute the remainder `r = total % n`. If `r == 0`, the sum divides evenly, so the minimum ugliness is `0`. Otherwise, some towers will inevitably be one block taller than others, giving a minimum ugliness of `1`.
6. Output the computed ugliness for each test case.

The algorithm works because the block-moving operation preserves the total sum of blocks. The tallest and shortest towers can only differ by at most one if the total sum cannot be divided evenly. This invariant guarantees that our computation of `0` or `1` is always correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    total = sum(a)
    if total % n == 0:
        print(0)
    else:
        print(1)
```

The solution first reads all input efficiently using `sys.stdin.readline`. Summing the array `a` gives the total number of blocks. Checking divisibility by `n` directly gives the minimum possible ugliness. The check `total % n == 0` handles both small and large sums correctly, and no additional storage beyond the input array is needed.

## Worked Examples

Trace for input `[3, 10, 10, 10]`:

| Step | a | total | total % n | ugliness |
| --- | --- | --- | --- | --- |
| compute sum | [10, 10, 10] | 30 | 0 | 0 |

All towers are already equal; output is `0`.

Trace for input `[5, 1, 2, 3, 1, 5]`:

| Step | a | total | total % n | ugliness |
| --- | --- | --- | --- | --- |
| compute sum | [1, 2, 3, 1, 5] | 12 | 12 % 5 = 2 | 1 |

The sum `12` divided by `5` leaves remainder `2`. Some towers must be `2` blocks taller than others, so minimum ugliness is `1`.

These traces demonstrate the invariant that the sum determines the minimal achievable difference.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Need to sum the array once for each test case |
| Space | O(n) per test case | Storing the tower heights |

Given `n <= 100` and `t <= 1000`, the worst-case time is roughly 100,000 operations, well within a 2-second time limit. Memory use is negligible at this scale.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        print(0 if sum(a) % n == 0 else 1)
    return out.getvalue().strip()

# provided samples
assert run("3\n3\n10 10 10\n4\n3 2 1 2\n5\n1 2 3 1 5\n") == "0\n0\n1", "sample 1"

# custom cases
assert run("2\n2\n1 2\n3\n2 2 2\n") == "1\n0", "minimum size inputs"
assert run("1\n4\n10000000 10000000 10000000 10000001\n") == "1", "large numbers"
assert run("1\n5\n5 5 5 5 5\n") == "0", "all equal values"
assert run("1\n3\n1 1 2\n") == "1", "boundary conditions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2\n2\n1 2\n3\n2 2 2\n` | `1\n0` | smallest arrays, uneven/even sums |
| `1\n4\n10000000 10000000 10000000 10000001\n` | `1` | large numbers near limit |
| `1\n5\n5 5 5 5 5\n` | `0` | all towers equal |
| `1\n3\n1 1 2\n` | `1` | sum not divisible, minimal difference |

## Edge Cases

For a single operation needed case, `[1, 2]`, the sum is `3`. Dividing by `2` leaves remainder `1`. The algorithm outputs `1`, correctly identifying that one tower must be one taller than the other. For the already balanced case `[2, 2, 2]`, the sum is `6`, divisible by `3`, so output is `0`. Both edge cases demonstrate that the algorithm handles both divisible and non-divisible sums correctly without explicit block movement.
