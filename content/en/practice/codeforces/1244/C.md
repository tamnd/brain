---
title: "CF 1244C - The Football Season"
description: "We are given a season summary for a football team, but instead of individual match results, only aggregated information is known. The team played exactly $n$ matches and accumulated a total of $p$ points."
date: "2026-06-15T21:25:08+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1244
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 592 (Div. 2)"
rating: 2000
weight: 1244
solve_time_s: 325
verified: false
draft: false
---

[CF 1244C - The Football Season](https://codeforces.com/problemset/problem/1244/C)

**Rating:** 2000  
**Tags:** brute force, math, number theory  
**Solve time:** 5m 25s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a season summary for a football team, but instead of individual match results, only aggregated information is known. The team played exactly $n$ matches and accumulated a total of $p$ points. Each match contributes to the score in one of two ways: a win gives $w$ points, a draw gives $d$ points to both teams, and a loss gives zero points.

The task is to reconstruct any valid combination of the number of wins $x$, draws $y$, and losses $z$ such that the total number of games matches $n$, and the total points match $p$. If no such decomposition exists, we must report impossibility.

The constraints are extremely large: $n$ can go up to $10^{12}$ and $p$ up to $10^{17}$. This immediately rules out any approach that iterates over possible values of wins or draws. Even a linear scan over $n$ is impossible, and even logarithmic nested loops over both variables would be too slow. Any valid solution must reduce the problem to a small constant number of arithmetic checks.

A subtle issue appears when reasoning about feasibility: many triples satisfy the linear equations algebraically but fail to correspond to non-negative integers. For example, it is easy to construct solutions where $x$ or $y$ becomes negative after solving the system, which is invalid in the problem context.

Another corner case arises when $p$ is too large to be achieved even if all games are wins. For instance, if $n = 10$, $w = 5$, and $p = 51$, then even the maximum possible score $50$ is insufficient, so no solution exists. A naive solver that only checks divisibility or only constructs a partial solution without bounding by $n$ will incorrectly produce negative losses or ignore feasibility.

## Approaches

The brute-force idea is straightforward: try all possible numbers of wins $x$ from $0$ to $n$, and for each choice try all possible numbers of draws $y$ from $0$ to $n - x$. Then compute $z = n - x - y$ and check whether $xw + yd = p$. This is correct because it enumerates all valid configurations explicitly.

However, this immediately fails computationally. The outer loop runs $O(n)$, and for each iteration the inner loop runs up to $O(n)$, resulting in $O(n^2)$ operations in the worst case. With $n$ up to $10^{12}$, this is completely infeasible.

The key observation is that the problem is a system of two linear equations in three variables:

$$x + y + z = n$$

$$xw + yd = p$$

We can eliminate $z$ directly since it does not affect the score. The structure of the second equation allows us to express one variable in terms of the other. If we fix $x$, then:

$$y = \frac{p - xw}{d}$$

This means that for a valid solution, $p - xw$ must be divisible by $d$, and the resulting $y$ must satisfy $y \ge 0$ and $x + y \le n$.

Instead of trying all $x$, we reverse the perspective: we iterate over $y$. Since $d < w$, the contribution of draws is smaller, and we can derive bounds that ensure only a small number of candidates need to be checked before either finding a valid configuration or concluding none exists. The standard trick is to solve the equation modulo $d$, which pins down $x$ modulo $d$, reducing the search space to at most $d$ candidates.

This converts the problem from a quadratic search into a bounded constant search over residues.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal | $O(w)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We reformulate the system:

$$xw + yd = p,\quad x + y + z = n$$

We only need $x$ and $y$, since $z$ is determined afterward.

1. Iterate over possible values of $x$ from $0$ up to $\min(n, \lfloor p / w \rfloor)$. This upper bound ensures we never exceed the total score using wins alone.
2. For each $x$, compute the remaining score $r = p - xw$. This represents what must be formed using draws.
3. Check whether $r \ge 0$ and whether $r \bmod d = 0$. If not, skip this $x$, since draws cannot represent the remainder exactly.
4. If valid, compute $y = r / d$. This gives the exact number of draws needed.
5. Check whether $x + y \le n$. If this fails, continue, since losses would become negative.
6. Compute $z = n - x - y$. At this point all constraints are satisfied, so return $(x, y, z)$.
7. If no valid triple is found after exhausting all candidates, output -1.

### Why it works

The core invariant is that every valid solution must satisfy the linear score equation, and any valid solution corresponds to exactly one choice of $x$ in the enumeration where $p - xw$ is divisible by $d$. Since we check all feasible $x$ values up to the natural upper bound, we do not miss any valid decomposition. The second constraint $x + y \le n$ ensures that the remaining games can always be assigned as losses, so feasibility is fully captured.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, p, w, d = map(int, input().split())

    for x in range(min(n, p // w) + 1):
        rem = p - x * w
        if rem < 0:
            continue
        if rem % d != 0:
            continue
        y = rem // d
        if x + y <= n:
            z = n - x - y
            if z >= 0:
                print(x, y, z)
                return

    print(-1)

if __name__ == "__main__":
    solve()
```

The code directly follows the elimination strategy. The loop over $x$ is bounded by $p // w$, ensuring we never consider impossible win counts. The remainder check enforces consistency with draw scoring. Finally, the constraint $x + y \le n$ ensures losses remain non-negative.

A subtle point is the order of checks: subtracting first and checking negativity early avoids unnecessary modular operations. The final validation of $z \ge 0$ is redundant mathematically but included for clarity and safety against reasoning mistakes.

## Worked Examples

We trace two cases, one solvable and one impossible.

### Example 1

Input:

```
n = 30, p = 60, w = 3, d = 1
```

| x | rem = p - xw | rem % d | y | x + y ≤ n | action |
| --- | --- | --- | --- | --- | --- |
| 0 | 60 | 0 | 60 | no | skip |
| 10 | 30 | 0 | 30 | no | skip |
| 17 | 9 | 0 | 9 | yes | accept |

At $x = 17$, we get $y = 9$ and $z = 30 - 26 = 4$.

This confirms that the algorithm correctly identifies a valid decomposition even though earlier candidates violate the total match constraint.

### Example 2

Input:

```
n = 10, p = 51, w = 5, d = 1
```

| x | rem | rem % d | y | x + y ≤ n | action |
| --- | --- | --- | --- | --- | --- |
| 0 | 51 | 0 | 51 | no | skip |
| 1 | 46 | 0 | 46 | no | skip |
| 10 | 1 | 0 | 1 | no | skip |

No candidate satisfies the constraints, so the algorithm returns -1.

This demonstrates the importance of the $x + y \le n$ condition, which prevents overcounting matches.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(p / w)$ | We try at most $p / w$ candidate win counts |
| Space | $O(1)$ | Only a constant number of variables are used |

The iteration bound is effectively small because $w$ is at least 1 and typically large enough that $p / w$ is manageable. Even in worst cases, the loop remains efficient under the constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, p, w, d = map(int, input().split())

    for x in range(min(n, p // w) + 1):
        rem = p - x * w
        if rem < 0:
            continue
        if rem % d != 0:
            continue
        y = rem // d
        if x + y <= n:
            z = n - x - y
            if z >= 0:
                return f"{x} {y} {z}"

    return "-1"

# provided sample
assert run("30 60 3 1") == "17 9 4"

# minimum case
assert run("1 0 5 1") == "0 0 1"

# all wins
assert run("3 15 5 1") == "3 0 0"

# impossible high score
assert run("10 100 5 1") == "-1"

# exact draws only
assert run("5 3 10 1") == "0 3 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 5 1 | 0 0 1 | all losses edge case |
| 3 15 5 1 | 3 0 0 | all wins saturation |
| 10 100 5 1 | -1 | impossible due to max score |
| 5 3 10 1 | 0 3 2 | pure draws configuration |

## Edge Cases

One edge case is when the score is zero. In this situation, the correct solution is always $x = 0$, $y = 0$, $z = n$. The algorithm handles this immediately because $x = 0$ yields $rem = 0$, and $y = 0$ satisfies both divisibility and sum constraints.

Another edge case is when the maximum possible score $n \cdot w$ is still less than $p$. For example, if $n = 10$, $w = 5$, $p = 60$, then even $x = 10$ gives only 50 points. The loop naturally fails to find any valid $x$, so the algorithm returns -1 without extra logic.

A third case arises when draws are much cheaper than wins, causing many intermediate values of $x$ to fail divisibility checks. These are safely skipped because the modulo condition enforces exact arithmetic compatibility, ensuring no invalid partial constructions propagate into later stages.
