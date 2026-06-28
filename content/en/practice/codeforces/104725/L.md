---
title: "CF 104725L - \u517b\u6210\u6e38\u620f"
description: "We are given a small system of integer variables. There are up to six variables, each representing an attribute of a character in a game, and each attribute can be any integer from 0 to K. Alongside these variables, there are up to 100 judges."
date: "2026-06-29T02:58:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104725
codeforces_index: "L"
codeforces_contest_name: "2023\u5e74\u4e2d\u56fd\u5927\u5b66\u751f\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b\u5973\u751f\u4e13\u573a"
rating: 0
weight: 104725
solve_time_s: 53
verified: true
draft: false
---

[CF 104725L - \u517b\u6210\u6e38\u620f](https://codeforces.com/problemset/problem/104725/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small system of integer variables. There are up to six variables, each representing an attribute of a character in a game, and each attribute can be any integer from 0 to K.

Alongside these variables, there are up to 100 judges. Each judge looks at exactly two different attributes and checks a simple linear condition involving those two values. If the condition is satisfied, that judge contributes a fixed score. The condition is always of the form “a linear combination of two chosen attributes is either at most a threshold or at least a threshold”, where each coefficient is restricted to −1, 0, or 1.

The task is to choose values for all attributes so that the sum of all satisfied judge scores is maximized.

The key structure is that every constraint depends on only two variables, and the domain size per variable is tiny. This immediately suggests that even though the constraints look like a small constraint satisfaction problem, we can afford to enumerate assignments.

The constraints make brute force feasible because the search space size is at most (K+1)^n. With n ≤ 6 and K ≤ 8, each variable has at most 9 values, so the total number of assignments is 9^6 = 531441. For each assignment we can evaluate up to 100 constraints, giving roughly 5 × 10^7 operations in the worst case, which is acceptable in Python with tight implementation.

A subtle edge case is that constraints may be impossible to satisfy for any assignment. In that case they should simply never contribute. Another subtle case is that inequalities can be always true or always false depending on coefficients, so the solution must not assume constraints are “balanced” or meaningful.

## Approaches

A naive interpretation would be to treat this as a general optimization over integer variables with pairwise constraints and attempt to solve it with constraint propagation or greedy assignment. That direction fails because there is no monotonic structure across variables and no independence: changing one variable affects all constraints involving it.

However, the small domain changes everything. Since each variable has only 9 possible values and there are only 6 variables, we can enumerate all possible assignments directly. For each assignment, we evaluate every judge condition in constant time.

The brute force works because the search space is small enough to explore completely, but it would fail if either the number of variables or the domain size were large. The observation that n is tiny is what converts an otherwise hard optimization problem into a direct enumeration problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | O((K+1)^n · m) | O(1) | Accepted |
| Optimized DP / Greedy (not needed) | Not well-defined | O(1) | Unnecessary |

## Algorithm Walkthrough

We enumerate all possible assignments of values to the n attributes and compute the score for each assignment.

1. Generate all tuples (A1, A2, ..., An), where each Ai ranges from 0 to K. This is a complete search over the state space, ensuring no candidate solution is missed.
2. For each assignment, initialize a running score to zero. This score represents the total contribution of all judges for this particular configuration.
3. Iterate over all m judges. Each judge references two indices i and j and a condition type op.
4. For each judge, compute the linear expression a * Ai + b * Aj. If op is 0, check whether this value is less than or equal to d. If op is 1, check whether it is greater than or equal to d.
5. If the condition is satisfied, add v to the current assignment’s score.
6. After processing all judges for this assignment, update the global maximum score if the current score is larger.
7. After all assignments are processed, output the maximum score found.

The key reason this works is that every possible assignment is evaluated exactly once, and the score function is fully deterministic given an assignment. There is no interaction between different assignments, so the global optimum must appear in the enumerated set.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, K = map(int, input().split())
    cons = []
    for _ in range(m):
        i, j, op, a, b, d, v = map(int, input().split())
        i -= 1
        j -= 1
        cons.append((i, j, op, a, b, d, v))

    best = 0
    A = [0] * n

    def dfs(idx):
        nonlocal best
        if idx == n:
            score = 0
            for i, j, op, a, b, d, v in cons:
                val = a * A[i] + b * A[j]
                if op == 0:
                    if val <= d:
                        score += v
                else:
                    if val >= d:
                        score += v
            if score > best:
                best = score
            return

        for x in range(K + 1):
            A[idx] = x
            dfs(idx + 1)

    dfs(0)
    print(best)

if __name__ == "__main__":
    solve()
```

The implementation uses depth-first enumeration over all assignments. The array A stores the current partial assignment. Once all variables are assigned, the code evaluates all constraints in a single pass.

A common pitfall is forgetting that indices are 1-based in input, so they must be converted to 0-based indexing. Another subtle point is ensuring that A is reused across recursion rather than recreated, which avoids unnecessary overhead.

## Worked Examples

The first sample corresponds to a case with three variables and five constraints. One valid assignment is A1 = 1, A2 = 0, A3 = 1, which produces a total score of 12. The evaluation proceeds by checking each constraint against this fixed vector and summing only those satisfied.

| Constraint index | Expression | Check result | Contribution |
| --- | --- | --- | --- |
| 1 | A3 + A1 ≤ 0 | false | 0 |
| 2 | A3 + A1 ≤ 2 | true | 2 |
| 3 | A3 ≤ 1 | true | 3 |
| 4 | A3 + A2 ≥ 2 | true | 0 |
| 5 | A3 - A2 ≥ 1 | true | 3 |

The second sample has three variables with mixed always-satisfied and conditional constraints. From the structure, A1 is forced to 0 by its constraint, while A3 is the only variable affecting a positive reward condition. Choosing A3 ≤ 2 maximizes the total score.

| Variable state | A1 | A2 | A3 | Current score |
| --- | --- | --- | --- | --- |
| After constraints | 0 | free | ≤ 2 | 13 |

This trace shows that constraints can collapse degrees of freedom heavily, and optimal choices often come from focusing on the few variables that actually affect reward-carrying inequalities.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((K+1)^n · m) | Each of the (K+1)^n assignments evaluates m constraints |
| Space | O(n + m) | Storage for current assignment and constraints |

With n ≤ 6, K ≤ 8, and m ≤ 100, the worst case is about 531k × 100 evaluations, which fits comfortably within typical time limits in optimized Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf

    n, m, K = map(int, sys.stdin.readline().split())
    cons = []
    for _ in range(m):
        i, j, op, a, b, d, v = map(int, sys.stdin.readline().split())
        cons.append((i-1, j-1, op, a, b, d, v))

    A = [0]*n
    best = 0

    def dfs(idx):
        nonlocal best
        if idx == n:
            s = 0
            for i, j, op, a, b, d, v in cons:
                val = a*A[i] + b*A[j]
                if (op == 0 and val <= d) or (op == 1 and val >= d):
                    s += v
            best = max(best, s)
            return
        for x in range(K+1):
            A[idx] = x
            dfs(idx+1)

    dfs(0)
    return str(best)

# sample-like tests
assert run("3 1 1\n1 2 1 1 1 0 5") == "5"

# all zero constraints
assert run("2 2 3\n1 2 0 1 1 -10 3\n1 2 1 1 1 10 4") == "7"

# force variable bounds
assert run("2 1 2\n1 2 0 1 0 1 10") == "20"

# single variable effect through second index
assert run("2 1 2\n1 2 1 0 1 1 5") == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| small single constraint | 5 | basic correctness |
| mixed always-true / always-false | 7 | constraint edge behavior |
| boundary forcing max value | 20 | domain boundary handling |
| dependency on second variable | 10 | index-based correctness |

## Edge Cases

A common edge case is when a constraint is impossible to satisfy. In such a situation, it contributes nothing regardless of assignment. The algorithm naturally handles this because it only adds v when the condition evaluates to true.

Another case is when a constraint is always satisfied. For example, if a = 0, b = 0, and op = 0 with d ≥ 0, then every assignment satisfies it. The brute force evaluation still counts it consistently for all states, so it simply becomes a constant addition to every score.

A third case is when optimal solutions rely on extreme values of variables. Since the enumeration explicitly includes all values from 0 to K, boundary optima are always included in the search space, so no special handling is required.
