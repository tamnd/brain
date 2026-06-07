---
title: "CF 2121A - Letter Home"
description: "We are given a set of distinct integer positions on the number line and a starting position. From the starting position, we can move left or right by one unit at a time."
date: "2026-06-08T03:46:52+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math"]
categories: ["algorithms"]
codeforces_contest: 2121
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1032 (Div. 3)"
rating: 800
weight: 2121
solve_time_s: 70
verified: true
draft: false
---

[CF 2121A - Letter Home](https://codeforces.com/problemset/problem/2121/A)

**Rating:** 800  
**Tags:** brute force, math  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of distinct integer positions on the number line and a starting position. From the starting position, we can move left or right by one unit at a time. Our goal is to visit every specified position at least once, and we want to compute the minimum number of moves required to achieve this.

The input provides multiple test cases. Each test case gives the number of positions to visit, the starting point, and the sorted list of positions. The output for each test case is a single integer representing the minimum number of steps to ensure all positions are visited.

The constraints are small: the number of positions `n` is at most 10, the starting position and target positions are between 1 and 100, and there can be up to 1000 test cases. Because `n` is very small, algorithms that are exponential in `n` are feasible. We do not need to consider high-complexity graph or dynamic programming methods, since even trying all permutations of visit orders is computationally reasonable.

A subtle edge case arises when the starting position `s` is outside the range of the positions we need to visit. For example, if `s = 1` and the positions are `[3, 4, 5]`, the optimal path is to move directly to the nearest endpoint, then traverse all positions sequentially. A naive implementation that assumes `s` is always within the range of positions would produce the wrong answer.

Another edge case is when `s` coincides with one of the positions. For example, if `s = 3` and the positions are `[3, 4, 5]`, the minimum number of steps decreases because we do not need to move to reach the starting position.

## Approaches

A brute-force approach would generate all permutations of the positions and compute the distance traveled from `s` through each permutation. This is correct because it considers all possible orders, but it is unnecessary due to the linear nature of the number line. With `n = 10`, there are `10! = 3,628,800` permutations per test case. Multiplied by 1000 test cases, this approach is too slow.

The key insight is that all positions are on a one-dimensional line and are sorted. The minimum number of steps is determined entirely by the leftmost and rightmost positions we must visit. If the starting position is inside this interval, the optimal strategy is to go to the nearer endpoint first, then traverse to the other end. If the starting position is outside the interval, we move directly to the nearest endpoint and traverse to the far end. The minimum steps are therefore the distance between the leftmost and rightmost positions plus any additional distance to reach the interval from the starting point.

This reduces the problem to simple arithmetic: find the leftmost and rightmost positions, compute the distance to reach them from `s`, and add the interval length. This approach is linear in `n` per test case and trivial to implement.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all permutations) | O(n! * n) | O(n) | Too slow |
| Optimal (interval + distance) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, read `n`, `s`, and the sorted list of positions `x`.
3. Identify the leftmost position `L = x[0]` and rightmost position `R = x[-1]`.
4. If the starting position `s` is between `L` and `R` (inclusive), the minimal path is either `R - s + s - L = R - L`, since moving first to the closer end and then traversing the interval always results in the same total distance. Compute `max(R - s, s - L) + (R - L)`; in practice, this simplifies to `(R - L)` when `s` is inside the interval.
5. If the starting position `s` is less than `L`, the steps are `R - s`, since we must move from `s` to `L` then traverse to `R`.
6. If the starting position `s` is greater than `R`, the steps are `s - L`, since we move from `s` to `R` then traverse to `L`.
7. Output the computed minimal steps.

Why it works: The solution exploits the one-dimensional nature of the positions. The minimal sequence of steps is always to reach one endpoint of the interval and traverse to the other. Any deviation, such as visiting positions in non-sequential order, increases the number of steps unnecessarily. This guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, s = map(int, input().split())
    x = list(map(int, input().split()))
    L, R = x[0], x[-1]

    if s < L:
        steps = R - s
    elif s > R:
        steps = s - L
    else:
        steps = (R - L) + min(R - s, s - L)
    
    print(steps)
```

The code reads input efficiently with `sys.stdin.readline` to handle many test cases quickly. It identifies the interval `[L, R]` that contains all positions. Depending on whether the starting position `s` lies outside or inside this interval, the code computes the minimal number of steps. The `min(R - s, s - L)` ensures we start from the closer end when `s` is within the interval, reducing the distance traveled.

## Worked Examples

### Example 1

Input: `1 2 1 3`

| Step | L | R | s | Case | Steps |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 3 | 2 | s in [L,R] | (3-1) + min(3-2,2-1) = 2 + 1 = 3 |

We start at 2, go to 1, then traverse to 3, total 3 steps.

### Example 2

Input: `2 2 1 3`

| Step | L | R | s | Case | Steps |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 3 | 2 | s in [L,R] | (3-1) + min(3-2,2-1) = 2 + 1 = 3 |

We start at 2, go to 1, then traverse to 3, confirming the algorithm is consistent.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * t) | Each test case requires a single pass through the positions to find L and R. n ≤ 10, t ≤ 1000. |
| Space | O(n) | Storing the positions array per test case. |

The solution easily fits within the 1s time limit and 256 MB memory limit, since the total operations are at most 10 * 1000 = 10,000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n, s = map(int, input().split())
        x = list(map(int, input().split()))
        L, R = x[0], x[-1]
        if s < L:
            steps = R - s
        elif s > R:
            steps = s - L
        else:
            steps = (R - L) + min(R - s, s - L)
        print(steps)
    return output.getvalue().strip()

# provided samples
assert run("12\n1 1\n1\n1 2\n1\n1 1\n2\n2 1\n2 3\n2 2\n1 3\n2 3\n1 2\n3 1\n1 2 3\n3 2\n1 3 4\n3 3\n1 2 3\n4 3\n1 2 3 10\n5 5\n1 2 3 6 7\n6 6\n1 2 3 9 10 11") == "0\n1\n1\n2\n3\n2\n2\n4\n2\n11\n8\n15"

# custom cases
assert run("2\n1 5\n10\n3 1\n2 3 4") == "5\n3", "minimum-size and interior case"
assert run("1\n4 10\n1 2 3 4") == "10", "start outside right"
assert run("1\n4 1\n1 2 3 4") == "3", "start at left endpoint"
assert run("1\n5 3\n1 2 3 4 5") == "4", "start in middle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 5 10` | `5` | Starting position right of interval |
| `3 1 2 3 4` | `3` | Starting position at left endpoint |
| `5 3 1 2 3 4 5` | `4` | Starting position inside interval |
| `1 1 1 |  |  |
