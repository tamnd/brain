---
title: "CF 1543A - Exciting Bets"
description: "We are given two non-negative integers, and we can move them in lockstep: every operation changes both values by exactly the same amount, either increasing both by one or decreasing both by one (as long as we do not go below zero)."
date: "2026-06-16T15:25:08+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1543
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 730 (Div. 2)"
rating: 900
weight: 1543
solve_time_s: 486
verified: true
draft: false
---

[CF 1543A - Exciting Bets](https://codeforces.com/problemset/problem/1543/A)

**Rating:** 900  
**Tags:** greedy, math, number theory  
**Solve time:** 8m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two non-negative integers, and we can move them in lockstep: every operation changes both values by exactly the same amount, either increasing both by one or decreasing both by one (as long as we do not go below zero).

The score we care about is the greatest common divisor of the two numbers after any sequence of moves. We want to maximize this score, and among all ways that achieve the maximum possible GCD, we want the smallest number of moves needed.

A key observation is that every move preserves the difference between the two numbers. If we define $d = a - b$, then both operations keep $a - b$ unchanged. This means the entire process is constrained to points of the form $(x, x - d)$ or $(x + d, x)$ depending on ordering.

The constraints go up to $10^{18}$, so any solution that tries all reachable states is impossible. Even scanning a range of values around $a$ and $b$ is not feasible, since the reachable values span an infinite line in both directions.

A subtle edge case appears when $a = b$. In that case, increasing both numbers preserves equality and keeps the GCD equal to the value itself, and it can grow without bound. This leads to infinite excitement, which must be detected.

Another corner case arises when one value is zero. Since $gcd(x, 0) = x$, decreasing both values may not be possible, but increasing both allows reaching arbitrarily large equal values as long as we do not block ourselves with negativity constraints. However, the optimal reasoning still depends on the invariant difference.

A naive mistake is to assume we can independently adjust values toward a multiple relationship. We cannot change the difference, so any target pair must satisfy a fixed linear relation.

## Approaches

A brute-force idea is to simulate all possible states reachable from $(a, b)$ by BFS or DFS, updating both values by ±1 together. This quickly becomes infinite because the state graph is an infinite line in both directions. Even if we restrict bounds heuristically, the optimal GCD might occur far away, since GCD depends on divisibility, not proximity.

The key structural insight is that the difference $d = |a - b|$ never changes. Any reachable pair can be written as:

$$(a', b') = (x, x - d)$$

for some integer $x$ (assuming ordering).

We want to choose $x$ such that:

$$\gcd(x, x - d)$$

is maximized.

Using the identity:

$$\gcd(x, x - d) = \gcd(x, d)$$

the problem reduces to choosing $x$ on a line so that it shares the largest possible divisor with a fixed number $d$, while minimizing the distance from the starting point.

The maximum possible GCD is simply $d$ itself when possible, but we must ensure feasibility with the constraint that we can only reach values consistent with integer steps from $a$ and $b$.

The important structural result is that the best achievable GCD is $g = |a - b|$ if we can align one number to a multiple structure via shifting; otherwise, when $a = b$, the answer is infinite.

This reduces the task to a simple number-theoretic computation based on difference alignment and distance to nearest valid configuration.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Infinite (state explosion) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. If $a = b$, immediately return infinite excitement.

The reason is that both numbers always stay equal after any number of operations, and repeated increment operations make the GCD grow without bound.
2. Compute $d = |a - b|$.

This difference is invariant under all allowed operations, so every reachable state lies on a fixed arithmetic line.
3. If $d = 0$, we already handled it, so proceed assuming $d > 0$.
4. Compute the best achievable GCD as $g = d$.

This comes from the identity $\gcd(x, x - d) = \gcd(x, d)$, meaning the GCD is always a divisor of $d$, and we can align $x$ to maximize this divisor, achieving $d$ itself.
5. Determine the minimum number of moves needed to reach a configuration where one of the numbers becomes divisible by $d$.

Since each move shifts both numbers by 1, we are effectively shifting the pair along the integer line. We choose the nearest multiple alignment to minimize distance.
6. Compute how far $a$ is from the nearest multiple of $d$, and use that shift as the number of moves.

### Why it works

The invariant is that the difference $a - b$ never changes. This restricts all reachable states to a single one-dimensional lattice. On this lattice, the GCD simplifies to a function of one variable and a fixed constant $d$. Since every GCD achievable is a divisor of $d$, the maximum is achieved by aligning the state so that one coordinate is a multiple of $d$. The minimal move count follows because each operation shifts the entire lattice point by exactly one unit, so reaching the closest valid alignment is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        a, b = map(int, input().split())

        if a == b:
            print(0, 0)
            continue

        d = abs(a - b)

        # shift to nearest multiple alignment
        r = a % d
        move = min(r, d - r)

        print(d, move)

if __name__ == "__main__":
    solve()
```

The solution first checks the equal case, which is the only scenario leading to unbounded growth. After that, everything depends on the invariant difference $d$. The remainder of $a$ modulo $d$ tells how far we are from aligning $a$ to a multiple of $d$, and shifting both numbers preserves feasibility while moving along the reachable line.

The choice of using only $a \% d$ is valid because shifting both numbers affects both symmetrically, and the alignment condition depends only on divisibility relative to the fixed difference.

## Worked Examples

### Example 1

Input:

```
8 5
```

Here $d = 3$.

| Step | a | b | d | a % d | Move |
| --- | --- | --- | --- | --- | --- |
| Start | 8 | 5 | 3 | 2 | - |
| Compute d | 8 | 5 | 3 | 2 | - |
| Remainder | 8 | 5 | 3 | 2 | 1 |
| Result | - | - | 3 | - | 1 |

The optimal GCD is 3, achieved by shifting once. This demonstrates that the best alignment is found by moving toward a multiple structure of the difference.

### Example 2

Input:

```
3 9
```

Here $d = 6$.

| Step | a | b | d | a % d | Move |
| --- | --- | --- | --- | --- | --- |
| Start | 3 | 9 | 6 | 3 | - |
| Compute d | 3 | 9 | 6 | 3 | - |
| Remainder | 3 | 9 | 6 | 3 | 3 |
| Result | - | - | 6 | - | 3 |

This case shows that sometimes the best move is not zero, because we need to shift to reach a configuration where divisibility by the difference becomes optimal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case requires constant arithmetic operations |
| Space | O(1) | Only a few variables are used |

The constraints allow up to 5000 test cases with values up to $10^{18}$, so an $O(1)$ per test solution is necessary. The algorithm satisfies this comfortably.

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
        a, b = map(int, input().split())
        if a == b:
            out.append("0 0")
        else:
            d = abs(a - b)
            r = a % d
            out.append(f"{d} {min(r, d - r)}")
    return "\n".join(out)

# provided samples
assert run("""4
8 5
1 2
4 4
3 9
""") == """3 1
1 0
0 0
6 3"""

# custom cases
assert run("1\n0 5\n") == "5 0"
assert run("1\n10 10\n") == "0 0"
assert run("1\n7 3\n") == "4 1"
assert run("1\n1000000000000000000 999999999999999999\n") == "1 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 5 | 5 0 | zero boundary behavior |
| 10 10 | 0 0 | infinite case correctness |
| 7 3 | 4 1 | non-trivial remainder shift |
| large adjacent values | 1 0 | performance and edge scaling |

## Edge Cases

When $a = b$, the algorithm immediately returns $0, 0$. For example, input $4, 4$ produces equality, and repeated increments allow unbounded growth of the GCD, so the early exit correctly captures this.

When one value is zero, such as $0, 5$, the difference is 5 and the remainder logic still applies. The computation yields a valid shift distance of zero, meaning no movement is needed to maximize GCD.

When the values are already close, such as $7, 3$, the difference is 4 and the remainder of 7 modulo 4 is 3. The algorithm correctly picks the minimal shift to reach a configuration aligned with divisibility by 4.

When values are extremely large but differ by 1, the difference is 1 and every configuration has GCD 1. The remainder logic produces zero moves, since no improvement is possible.
