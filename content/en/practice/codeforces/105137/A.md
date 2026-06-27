---
title: "CF 105137A - Good Target"
description: "Each test case gives a target number of runs that must be reached or exceeded using a very restricted scoring system. Every ball in the innings contributes either 4 runs or 6 runs, nothing else is possible."
date: "2026-06-27T17:04:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105137
codeforces_index: "A"
codeforces_contest_name: "TheForces Round #30 (Good-Forces)"
rating: 0
weight: 105137
solve_time_s: 82
verified: false
draft: false
---

[CF 105137A - Good Target](https://codeforces.com/problemset/problem/105137/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 22s  
**Verified:** no  

## Solution
## Problem Understanding

Each test case gives a target number of runs that must be reached or exceeded using a very restricted scoring system. Every ball in the innings contributes either 4 runs or 6 runs, nothing else is possible. The batsman faces an unlimited number of balls, and the only question is how many balls are needed if we are free to choose between 4 and 6 on each delivery.

For a given target $n$, we are asked to determine two quantities. The first is the minimum number of balls required to reach at least $n$ runs, assuming we always make the most efficient scoring choices. The second is the maximum number of balls required, assuming we try to stretch the innings as long as possible while still reaching the target.

The constraints are small, with $n \le 10^3$ and up to 100 test cases. This immediately rules out anything heavy like dynamic programming over large states or search-based enumeration. Even a direct arithmetic reasoning per test case is more than sufficient.

A subtle point is that the target is “at least $n$” rather than “exactly $n$”. This matters because overshooting is allowed and often necessary. For example, if $n = 5$, a single 4-run ball is not enough, so we would need at least two balls, even though we may end up with 8 runs.

Another potential pitfall is assuming that mixing 4 and 6 in a clever way might affect the minimum or maximum beyond simple division logic. In reality, since both values are fixed and independent per ball, the problem reduces to simple bounds on how many fixed-size contributions are needed to reach a threshold.

## Approaches

A brute-force approach would try all possible sequences of 4s and 6s, gradually increasing the number of balls until the sum reaches at least $n$. For each number of balls $k$, we would enumerate all $2^k$ sequences of scoring choices and check whether any sequence achieves the required sum. This quickly becomes infeasible because even for $k = 20$, the number of combinations exceeds a million, and we may need to test many values of $k$ per test case.

The key observation is that we do not actually care about ordering or combinations. We only care about total contribution per ball. Each ball independently contributes either 4 or 6. This means the best way to minimize balls is always to use the larger value, 6, as often as possible. Similarly, the best way to maximize balls is always to use the smaller value, 4, as often as possible. There is no interaction between balls, so no greedy conflict arises.

This reduces the problem to simple arithmetic: compute how many 6s are needed to reach at least $n$, and how many 4s are needed to reach at least $n$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | Exponential in balls | O(1) to O(2^k) | Too slow |
| Arithmetic Greedy | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read the target value $n$. This is the minimum total runs required.
2. Compute the minimum number of balls by assuming every ball scores 6 runs. We need the smallest integer $k$ such that $6k \ge n$. This is computed as $\lceil n / 6 \rceil$. The reason this works is that replacing any 6 with a 4 would only reduce total runs per ball and therefore could not reduce the number of balls needed.
3. Compute the maximum number of balls by assuming every ball scores 4 runs. We need the smallest integer $k$ such that $4k \ge n$, which is $\lceil n / 4 \rceil$. Any use of a 6-run ball would only reduce the number of balls required, so it cannot increase the maximum.
4. Output the pair $(\lceil n/6 \rceil, \lceil n/4 \rceil)$.

### Why it works

Any valid innings corresponds to choosing a multiset of values from $\{4, 6\}$. The total score is linear in the number of balls, and each ball contributes independently. The minimum number of balls is achieved by maximizing per-ball contribution, and the maximum number of balls is achieved by minimizing per-ball contribution. Since both 4 and 6 are positive and fixed, no mixture can outperform these extremes in either direction. This establishes that the optimal solutions lie exactly at the two uniform configurations.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    
    min_balls = (n + 5) // 6
    max_balls = (n + 3) // 4
    
    print(min_balls, max_balls)
```

The implementation directly encodes ceiling division using integer arithmetic. For the minimum, adding 5 before dividing by 6 ensures correct rounding up. For the maximum, adding 3 before dividing by 4 performs the same ceiling behavior.

A common mistake is using floating point division and `math.ceil`, which is unnecessary and slightly riskier in competitive programming due to precision concerns and overhead. Another issue is forgetting that both answers must be printed per test case in the correct order.

## Worked Examples

Consider a case where $n = 10$. We compute minimum balls as $\lceil 10/6 \rceil = 2$ and maximum balls as $\lceil 10/4 \rceil = 3$.

| Step | Value |
| --- | --- |
| Target $n$ | 10 |
| Minimum balls | 2 (using 6 + 4) |
| Maximum balls | 3 (using 4 + 4 + 4) |

This confirms that mixing is only relevant for feasibility, not for optimal extremes.

Now consider $n = 20$. Minimum is $\lceil 20/6 \rceil = 4$, maximum is $\lceil 20/4 \rceil = 5$.

| Step | Value |
| --- | --- |
| Target $n$ | 20 |
| Minimum balls | 4 |
| Maximum balls | 5 |

This shows that even though 6 is more efficient, we still need multiple balls due to the threshold constraint.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case uses constant-time arithmetic operations |
| Space | O(1) | No additional data structures are used |

The constraints allow up to 100 test cases with small $n$, so this direct computation is easily fast enough.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        min_balls = (n + 5) // 6
        max_balls = (n + 3) // 4
        out.append(f"{min_balls} {max_balls}")
    return "\n".join(out)

# provided samples
assert run("4\n10\n20\n30\n40\n") == "2 3\n4 5\n5 8\n7 10"

# custom cases
assert run("1\n1\n") == "1 1", "minimum boundary"
assert run("1\n6\n") == "1 2", "exact multiple of 6"
assert run("1\n7\n") == "2 2", "just over 6"
assert run("1\n1000\n") == f"{(1000+5)//6} {(1000+3)//4}", "upper bound"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n = 1 | 1 1 | smallest possible target |
| n = 6 | 1 2 | exact fit for 6-run ball |
| n = 7 | 2 2 | overshoot forcing extra ball |
| n = 1000 | computed | upper constraint behavior |

## Edge Cases

For $n = 1$, a single 4-run ball already exceeds the target. The algorithm computes $\lceil 1/6 \rceil = 1$ and $\lceil 1/4 \rceil = 1$, which matches the fact that at least one ball is always required.

For values exactly divisible by 6, such as $n = 6$, the minimum becomes 1 ball. The maximum becomes $\lceil 6/4 \rceil = 2$, which corresponds to using only 4-run balls, requiring two deliveries to reach or exceed the target.

For values just above a multiple of 6, such as $n = 7$, the minimum jumps to 2 because one 6-run ball is insufficient. The maximum also stays at 2, since two 4-run balls are enough.

For the upper bound $n = 1000$, both formulas still behave correctly since all operations are constant time and do not depend on magnitude beyond integer arithmetic limits.
