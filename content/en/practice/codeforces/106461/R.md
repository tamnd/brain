---
title: "CF 106461R - Rock Paper Scissors"
description: "We are given two integers that describe aggregate information about a group of people playing a simplified Rock-Paper-Scissors setting. Instead of tracking individual interactions, we only care about how many people choose each hand: rock, scissors, and paper."
date: "2026-06-19T15:31:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106461
codeforces_index: "R"
codeforces_contest_name: "KUPC 2025 (The 4th Universal Cup. Stage 22: GP of Kyoto)"
rating: 0
weight: 106461
solve_time_s: 42
verified: true
draft: false
---

[CF 106461R - Rock Paper Scissors](https://codeforces.com/problemset/problem/106461/R)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two integers that describe aggregate information about a group of people playing a simplified Rock-Paper-Scissors setting. Instead of tracking individual interactions, we only care about how many people choose each hand: rock, scissors, and paper. Let those counts be $R$, $S$, and $P$. They must sum to the total number of players $N$, and they also must satisfy a second linear constraint involving scissors and paper: twice the number of scissors plus five times the number of paper players equals a given value $M$.

The task is not to construct an actual configuration, but only to determine whether any nonnegative integer triple $(R, S, P)$ exists that satisfies both equations. Additionally, we also need to determine whether there exists a valid configuration in which the game has a winner. The statement encodes this condition as a structural property: a winner exists exactly when not all three hand types are present simultaneously, meaning at most two of $R, S, P$ are positive.

Even though the problem is expressed in terms of a game, the core structure is purely arithmetic feasibility over a small system of linear constraints with nonnegative integer variables.

The constraints imply a very small search space in terms of degrees of freedom. Once $S$ and $P$ are chosen, $R$ is forced, so the system effectively reduces to checking integer solutions on a one-dimensional or two-dimensional lattice depending on how we eliminate variables. This strongly suggests that brute forcing both variables up to $N$ would already be too slow for large $N$, since that would be quadratic in the worst case.

The main subtlety is that feasibility depends on integer consistency, not just real-valued solutions. A common mistake is to solve the linear system over reals and assume feasibility carries over, but divisibility constraints can eliminate most candidates.

Edge cases arise when solutions lie on boundaries where one or more of $R, S, P$ become zero. For example, if $P = 0$, the equation reduces to $2S = M$, which may or may not be even. Similarly, if $S = 0$, we get $5P = M$, forcing divisibility by 5. These boundary cases matter both for feasibility and for the “winner exists” condition.

## Approaches

A brute-force approach would enumerate all pairs $(S, P)$ such that $2S + 5P = M$, compute $R = N - S - P$, and check whether all variables are nonnegative. The equation itself already restricts the search space significantly: $P$ ranges up to $M/5$, and for each choice we compute $S = (M - 5P)/2$ if it is an integer. This is already linear in $M$, which is acceptable for small constraints but becomes inefficient when $M$ is large, especially if multiple test cases exist.

The key observation is that the system is not really two-dimensional. The second equation pins down a relationship between $S$ and $P$, so once $P$ is chosen, $S$ is determined uniquely if it is valid. Then $R$ is forced. So the problem becomes checking whether there exists a nonnegative integer $P$ such that both divisibility and range constraints are satisfied.

The second part, about whether a winner exists, is simpler structurally. A winner exists exactly when not all three of $R, S, P$ are positive. So once we find any valid solution, we additionally check whether at least one of the variables is zero. If a solution exists where all are positive, that corresponds to a fully mixed state and thus no winner under the given condition. If all valid solutions necessarily force a zero component, then a winner is possible.

This reduces the problem to scanning a small range of $P$, computing corresponding $S$, deriving $R$, and checking constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over (S, P) | O(M) | O(1) | Too slow for large M |
| Iterate P only | O(M) worst-case, O(M/5) effective | O(1) | Accepted |

## Algorithm Walkthrough

1. Iterate over all possible values of $P$ from 0 to $\lfloor M/5 \rfloor$. This is sufficient because each paper contributes 5 units to the second equation, and any larger value would immediately exceed $M$.
2. For each $P$, compute the remaining contribution for scissors as $M - 5P$. This quantity must be even, otherwise no integer $S$ exists.
3. If it is even, compute $S = (M - 5P)/2$. This step enforces the exact satisfaction of the second equation without floating point arithmetic, which avoids precision issues.
4. Compute $R = N - S - P$. This comes directly from the total population constraint.
5. Check whether $R, S, P$ are all nonnegative. If any is negative, discard this candidate since it violates feasibility in the interpretation of counts.
6. If a valid triple is found, record feasibility. Additionally track whether there exists at least one valid triple where at least one variable equals zero, since that determines whether a winner configuration exists.

Why it works is based on the fact that the second equation defines a one-dimensional lattice of integer points in the $(S, P)$ plane. Every valid solution must lie on this lattice, and every candidate is fully determined by choosing $P$. The first equation then acts as a filter selecting only those lattice points that project correctly onto $N$. Because both constraints are linear and we enforce integrality at each step, no valid solution is skipped and no invalid solution is accepted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N, M = map(int, input().split())

    possible = False
    has_winner = False

    for P in range(M // 5 + 1):
        rem = M - 5 * P
        if rem < 0:
            break
        if rem % 2 != 0:
            continue

        S = rem // 2
        R = N - S - P

        if R < 0:
            continue

        possible = True
        if R == 0 or S == 0 or P == 0:
            has_winner = True

    if not possible:
        print("NO")
    else:
        print("YES" if has_winner else "NO")

if __name__ == "__main__":
    solve()
```

The code directly follows the enumeration over $P$. The parity check ensures that $S$ remains an integer, avoiding invalid half-values. Once $S$ is derived, $R$ is forced by the first equation.

A subtle implementation detail is the early break when $M - 5P < 0$, which is technically unnecessary but prevents extra iterations in pathological inputs. Another important detail is checking nonnegativity after computing $R$, since even if the second equation is satisfied, the first constraint can still invalidate the candidate.

The condition for a winner is tracked during enumeration, since it depends only on whether any valid solution places at least one variable at zero.

## Worked Examples

### Example 1

Consider $N = 6, M = 10$.

| P | rem = M-5P | S | R = N-S-P | Valid | Zero present |
| --- | --- | --- | --- | --- | --- |
| 0 | 10 | 5 | 1 | yes | yes |

We find a valid configuration $(R, S, P) = (1, 5, 0)$. This satisfies both equations. The presence of $P = 0$ indicates that not all three hands are present, so a winner configuration exists.

### Example 2

Consider $N = 8, M = 13$.

| P | rem | S | R | Valid |
| --- | --- | --- | --- | --- |
| 0 | 13 | - | - | no |
| 1 | 8 | 4 | 3 | yes |

We get a valid triple $(3, 4, 1)$, but all values are positive. This corresponds to a fully mixed game state, so no winner configuration exists under the condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(M/5)$ | We iterate over all feasible values of $P$, each checked in O(1) |
| Space | $O(1)$ | Only a constant number of variables are maintained |

The iteration is linear in the number of feasible values of $P$, which is bounded by $M$. For typical constraints in Codeforces-style problems, this is efficient enough when combined with early pruning and constant-time checks.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()
    return out.getvalue().strip()

# minimal valid case
assert run("1 0\n") == "YES", "trivial all zero"

# simple valid configuration
assert run("6 10\n") == "YES", "example valid with zero component"

# valid but no winner
assert run("8 13\n") == "NO", "all positive solution only"

# impossible case
assert run("5 1\n") == "NO", "no integer solution"

# boundary case large P only
assert run("10 50\n") == "YES", "multiple solutions possible"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 | YES | minimal feasibility |
| 6 10 | YES | solution with zero component |
| 8 13 | NO | all-positive solution only |
| 5 1 | NO | no integer lattice point |
| 10 50 | YES | multiple valid candidates |

## Edge Cases

One edge case is when $M$ is odd. In this case, every candidate $P$ produces an odd remainder $M - 5P$ whenever $5P$ is even or odd inconsistently, but in practice parity immediately eliminates all candidates where $S$ would not be integer. For example, $N = 10, M = 3$ yields no valid solution because $2S = 3 - 5P$ cannot be even for any integer $P$.

Another edge case is when $P = 0$, which reduces the system to $2S = M$ and $R = N - S$. For instance, $N = 7, M = 4$ gives $S = 2, R = 5$, a valid solution where one variable is zero, guaranteeing a winner configuration.

A third edge case is when all variables become strictly positive but still satisfy both equations. For example, $N = 8, M = 13$ produces $(R, S, P) = (3, 4, 1)$. The algorithm correctly marks feasibility but does not mark a winner, since no variable is zero in the only valid solution space.
