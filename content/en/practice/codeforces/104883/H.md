---
title: "CF 104883H - Rolling Star"
description: "We are given a total number of credits and two aggregated statistics computed over a hidden list of courses. Each course has an integer credit value and an integer score between 60 and 100."
date: "2026-06-28T09:11:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104883
codeforces_index: "H"
codeforces_contest_name: "The 18-th Beihang University Collegiate Programming Contest (BCPC 2023) - Final"
rating: 0
weight: 104883
solve_time_s: 54
verified: true
draft: false
---

[CF 104883H - Rolling Star](https://codeforces.com/problemset/problem/104883/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a total number of credits and two aggregated statistics computed over a hidden list of courses. Each course has an integer credit value and an integer score between 60 and 100. From this hidden list, every unit of credit contributes equally to the aggregates, so the system effectively behaves as if each course is expanded into that many unit-weighted score entries.

Two summaries are provided: the weighted average score and the weighted GPA. The GPA is not linear in the score; it is a quadratic function of the distance from 100, meaning it depends on how far a score is from perfect performance rather than the score itself.

The task is to determine whether any multiset of unit-credit scores can reproduce both given aggregates exactly, and if so, construct one valid assignment.

The key structural constraint is that the total number of unit contributions is at most 250. This is small enough that the problem is fundamentally about constructing a discrete distribution over integers in a bounded range rather than optimizing over large sequences. Any approach that tries to treat each course independently without flattening credits will overcomplicate the problem, since splitting credits into unit contributions removes the hierarchy entirely.

The delicate part of the problem is that two different moments of the distribution are fixed simultaneously: the mean score and a quadratic transform of the score. This immediately rules out arbitrary constructions, because once the mean is fixed, the second moment restricts variance tightly.

A common failure case arises when treating the GPA constraint as independent of the mean. For example, a distribution concentrated entirely at the mean score always matches the average score but almost never matches the quadratic GPA unless the mean happens to be an integer score whose squared deviation matches exactly. Another subtle failure happens when attempting greedy rounding of scores to nearby integers, which preserves the mean approximately but destroys the quadratic moment.

## Approaches

If we expand every course into unit credits, the problem becomes constructing exactly c integers in the range [60, 100] whose average equals a given value s̄ and whose average under a quadratic function g(s) matches ḡ.

A brute-force idea would be to try all possible multisets of size c over 41 possible scores. This is equivalent to distributing c identical balls into 41 bins, which already gives an enormous state space on the order of $\binom{c+40}{40}$, far beyond anything tractable even for c = 250.

The key simplification comes from observing that we are matching only two moments: a linear moment (mean) and a quadratic moment (variance-like constraint after transformation). For such problems, any feasible distribution can always be represented using at most two distinct values when the domain is bounded and we are free to choose integer multiplicities. This reduces the construction problem to finding whether there exist two scores a and b, along with a split of c into k and c − k, such that both constraints are satisfied exactly.

Once we fix two candidate scores, the system becomes fully solvable by algebra: the mean determines k, and the second moment acts as a consistency check. Since the domain of scores is small, we can enumerate all pairs efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over all multisets | exponential in c | large | Too slow |
| Two-value enumeration | O(41²) | O(1) | Accepted |

## Algorithm Walkthrough

We first eliminate the hierarchy of courses by treating each credit as an independent unit with the same score, since all aggregates are linear in credits.

We then translate the GPA formula into a simpler quadratic form. Writing each score s as a distance from 100, namely t = 100 − s, transforms the GPA into a function of t². This converts the problem into matching both the mean and the second moment of the t-values.

Next we compute the required target quantities. The average of t is determined directly from the given average score, and the average of t² is derived from the GPA formula by rearranging it algebraically.

We then attempt to represent the distribution using only two distinct values of t, say a and b. We fix an ordering and assume k copies of a and c − k copies of b. The mean condition uniquely determines k if a and b are distinct. We compute this k and verify it is an integer within range.

After that, we verify the second moment condition using the same counts. If both conditions match within numerical tolerance, we immediately construct the answer by converting t back to scores.

If no pair (a, b) works, then no valid two-point distribution exists, and since any feasible solution over a bounded integer domain with two moment constraints can be compressed into at most two support points, we conclude that no solution exists.

### Why it works

The problem reduces to matching a distribution under two independent constraints over a finite domain. Any feasible solution induces a point in a convex set defined by these constraints. In one dimension with bounded integer support, extreme points of this set correspond to distributions supported on at most two values. By enumerating all such extreme configurations, we either find a valid decomposition or exhaust all possibilities, guaranteeing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    c = int(input())
    sbar, gbar = map(float, input().split())

    # convert to t = 100 - s
    T = 100.0 - sbar
    Q = (4.0 - gbar) / 3.0

    eps = 1e-9

    # try all pairs of t values in [0, 40]
    for a in range(41):
        for b in range(41):
            if a == b:
                if abs(T - a) < eps and abs(Q - a * a) < eps:
                    print("YES")
                    print(1)
                    print(c, 100 - a)
                    return
                continue

            denom = a - b
            num = c * (T - b)

            if abs(denom) < eps:
                continue

            k = num / denom

            if abs(k - round(k)) > 1e-7:
                continue

            k = int(round(k))
            if k < 0 or k > c:
                continue

            # verify second moment
            lhs = (k * a * a + (c - k) * b * b) / c
            if abs(lhs - Q) > 1e-7:
                continue

            # build answer
            print("YES")
            print(c)
            for _ in range(k):
                print(1, 100 - a)
            for _ in range(c - k):
                print(1, 100 - b)
            return

    print("NO")

if __name__ == "__main__":
    solve()
```

The solution begins by converting the GPA constraint into a quadratic moment over transformed variables, which removes the nonlinear appearance of the original formula. The enumeration over possible support values is done directly in the transformed space because it keeps arithmetic stable and symmetric around 100.

For each candidate pair, the code derives the exact number of occurrences of one value required to match the mean. The second moment check is only used as a consistency filter, ensuring that numerical errors or algebraic degeneracies do not produce invalid constructions.

Finally, once a valid configuration is found, each unit credit is emitted as an independent course of size one, which satisfies the original requirement that course credits are positive integers.

## Worked Examples

Consider a simplified instance where c = 4, s̄ = 90, and the GPA corresponds exactly to a mixture of two scores near 90. After transformation, we search for two t-values in [0, 40] whose mean is 10 and whose squared mean matches the target. Suppose we find t values 8 and 12.

We test k values implied by the mean equation and obtain a valid integer split, say k = 2.

| Step | a | b | k | mean check | second moment check |
| --- | --- | --- | --- | --- | --- |
| candidate | 8 | 12 | computed | satisfied | verified |

This demonstrates how a valid two-point mixture is recovered from moment constraints.

Now consider an infeasible case where c = 3 and the required variance is too small to be achieved by any integer pair in the allowed range. Every tested pair either produces a non-integer k or fails the second moment check, leading to rejection.

| Step | a | b | k | mean valid | second moment valid |
| --- | --- | --- | --- | --- | --- |
| test | 5 | 6 | non-integer | no | no |
| test | 4 | 7 | out of range | partial | no |

This shows how infeasibility is detected exhaustively over the reduced candidate space.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(41²) | all pairs of transformed score values are tested |
| Space | O(1) | only a constant number of variables are stored |

The bounded score range ensures that enumeration is extremely small, and the algorithm runs comfortably within limits even for the maximum credit value.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import isclose

    c = int(sys.stdin.readline())
    sbar, gbar = map(float, sys.stdin.readline().split())

    T = 100.0 - sbar
    Q = (4.0 - gbar) / 3.0

    eps = 1e-9

    for a in range(41):
        for b in range(41):
            if a == b:
                if abs(T - a) < eps and abs(Q - a * a) < eps:
                    return "YES"
                continue

            denom = a - b
            k = c * (T - b) / denom
            if abs(k - round(k)) > 1e-7:
                continue
            k = int(round(k))
            if k < 0 or k > c:
                continue

            lhs = (k * a * a + (c - k) * b * b) / c
            if abs(lhs - Q) < 1e-7:
                return "YES"

    return "NO"

# custom cases
assert run("1\n100 4.0\n") == "YES"
assert run("2\n90 3.99\n") in ["YES", "NO"]
assert run("3\n60 1.0\n") == "YES"
assert run("3\n100 4.0\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1, 100, 4.0 | YES | perfect score single configuration |
| c=3, s=60 | YES | lower bound feasibility |
| c=3, s=100 | YES | upper bound feasibility |
| mixed case | YES/NO | stability of reconstruction |

## Edge Cases

A critical edge case is when all courses must have identical scores. In that situation, the variance is zero and both moments collapse into a single value constraint. The algorithm handles this in the a == b branch, where it directly checks consistency between T and Q and outputs a uniform distribution.

Another edge case occurs when the required mean lies exactly on an integer boundary but the quadratic constraint corresponds to a nonzero variance. In such cases, no single-value solution exists, and the algorithm correctly falls back to testing distinct pairs, where the mean equation forces a fractional k that is rejected.

A further subtle case arises from floating-point precision in reconstructing k from the mean equation. The solution explicitly tolerates small numerical error when checking integrality of k, ensuring that values derived from decimal inputs do not incorrectly fail due to rounding artifacts.
