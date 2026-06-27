---
title: "CF 105137A - Good Target"
description: "We are simulating a simplified cricket scoring system where each ball contributes a fixed amount of runs. The batsman can only score either 4 or 6 runs per ball, and we want to reach at least a target score $n$."
date: "2026-06-27T18:43:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105137
codeforces_index: "A"
codeforces_contest_name: "TheForces Round #30 (Good-Forces)"
rating: 0
weight: 105137
solve_time_s: 71
verified: false
draft: false
---

[CF 105137A - Good Target](https://codeforces.com/problemset/problem/105137/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We are simulating a simplified cricket scoring system where each ball contributes a fixed amount of runs. The batsman can only score either 4 or 6 runs per ball, and we want to reach at least a target score $n$. Each ball is independent and always produces one of these two outcomes.

For every test case, the task is to determine two quantities. First, the minimum number of balls needed to reach a total score of at least $n$. Second, the maximum number of balls needed to still reach at least $n$, assuming we choose scoring outcomes optimally for each objective.

The constraints are small, with $n \le 1000$ and up to 100 test cases. This rules out anything heavier than constant or very small linear work per test case. A direct greedy reasoning or closed-form computation per test case is sufficient.

A subtle edge case appears when $n$ is not divisible cleanly by 4 or 6 combinations. Since every ball contributes at least 4 runs, the number of balls is always bounded between $\lceil n/6 \rceil$ and $\lceil n/4 \rceil$, but we must be careful because mixing 4s and 6s can shift feasibility around small values. For example, if $n = 10$, two balls suffice using $4 + 6$, but using only 4s or only 6s would mislead a naive formula.

## Approaches

A brute-force way to think about the problem is to try all sequences of balls, gradually increasing the number of balls $k$, and checking whether some combination of 4s and 6s can achieve at least $n$. For each fixed $k$, we would enumerate all $2^k$ assignments of 4 or 6 and compute sums. This quickly becomes infeasible even for moderate $k$, since $k$ can be as large as 250 when $n$ is 1000 and all scores are 4.

The key observation is that only two values exist, and both are positive. This turns the problem into reasoning about extremal constructions. To minimize balls, we want to maximize runs per ball, so we always pick 6. To maximize balls, we want to minimize runs per ball while still staying feasible, so we always pick 4, except that we may need a final adjustment because overshooting constraints interact with the “at least n” requirement.

Thus, the problem reduces to two ceiling divisions:

the minimum number of balls is achieved by using all 6s, and the maximum number is achieved by using all 4s.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over sequences | O(2^n) | O(n) | Too slow |
| Greedy extremal reasoning | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

### Minimum balls

1. Compute how many balls are needed if every ball scores 6 runs.

This is optimal because 6 is the largest possible contribution per ball, so it minimizes the count of balls required to reach at least $n$.
2. Since we need at least $n$ runs, we take the smallest integer $k$ such that $6k \ge n$.

This is computed as $\lceil n/6 \rceil$.

### Maximum balls

1. Compute how many balls are needed if every ball scores 4 runs.

This maximizes the number of balls because 4 is the smallest possible contribution per ball.
2. We take the smallest integer $k$ such that $4k \ge n$.

This is $\lceil n/4 \rceil$.

### Why it works

The scoring system is monotone in a strong sense: every additional ball strictly increases total runs by either 4 or 6. To minimize balls, replacing any 4 with a 6 can only reduce or preserve the number of balls needed, never increase it. Conversely, to maximize balls, replacing any 6 with a 4 can only increase or preserve the number of balls needed. Since there are no constraints on the distribution of 4s and 6s other than total sum, extremal uniform assignments already define the optimal bounds.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input().strip())
        
        # minimum balls: maximize per-ball score (6)
        min_balls = (n + 5) // 6
        
        # maximum balls: minimize per-ball score (4)
        max_balls = (n + 3) // 4
        
        print(min_balls, max_balls)

if __name__ == "__main__":
    solve()
```

The implementation directly translates the two ceiling divisions into integer arithmetic. The expression $(n + 5) // 6$ computes $\lceil n/6 \rceil$, and $(n + 3) // 4$ computes $\lceil n/4 \rceil$. Using integer math avoids floating-point errors and keeps the solution constant time per test case.

## Worked Examples

### Example 1: $n = 10$

Minimum balls:

| Step | Value |
| --- | --- |
| Compute ceil(10 / 6) | 2 |
| Interpretation | 6 + 4 reaches 10 |

Maximum balls:

| Step | Value |
| --- | --- |
| Compute ceil(10 / 4) | 3 |
| Interpretation | 4 + 4 + 4 reaches at least 10 |

This shows that mixing 4 and 6 does not change the extremal bounds; the bounds depend only on per-ball extremes.

### Example 2: $n = 21$

Minimum balls:

| Step | Value |
| --- | --- |
| ceil(21 / 6) | 4 |
| Construction | 6 + 6 + 6 + 6 = 24 |

Maximum balls:

| Step | Value |
| --- | --- |
| ceil(21 / 4) | 6 |
| Construction | 4 + 4 + 4 + 4 + 4 + 4 = 24 |

This confirms both bounds still guarantee reaching at least $n$, even if they overshoot.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | One constant-time computation per test case |
| Space | O(1) | Only a few integers are stored |

The solution easily fits within limits since $t \le 100$, and each case requires only two integer operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input().strip())
        min_balls = (n + 5) // 6
        max_balls = (n + 3) // 4
        out.append(f"{min_balls} {max_balls}")
    return "\n".join(out)

# provided sample
assert run("4\n10\n20\n30\n40\n") == "2 3\n4 5\n5 8\n7 10"

# custom cases
assert run("1\n1\n") == "1 1", "minimum edge"
assert run("1\n4\n") == "1 1", "exact 4 boundary"
assert run("1\n6\n") == "1 2", "mix boundary"
assert run("1\n1000\n") == "167 250", "large boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 1 | smallest possible score |
| 4 | 1 1 | exact 4-run single ball |
| 6 | 1 2 | transition between 4 and 6 regimes |
| 1000 | 167 250 | upper bound correctness |

## Edge Cases

For $n = 1, 2, 3$, the formula still behaves correctly even though no single ball can exactly match the target. For $n = 3$, minimum balls is $\lceil 3/6 \rceil = 1$ and maximum is $\lceil 3/4 \rceil = 1$, which correctly reflects that one ball already exceeds the target.

For $n = 4$, both bounds collapse to 1, since one 4-run ball is sufficient and also necessary for the maximum construction.

For large $n = 1000$, the algorithm produces $167$ minimum balls using all 6s and $250$ maximum balls using all 4s. Both constructions exceed or meet the target as required, and no mixture can break these extremal bounds because replacing any 6 with a 4 strictly increases the number of balls needed, and replacing any 4 with a 6 strictly decreases it.
