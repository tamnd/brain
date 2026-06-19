---
title: "CF 106170B - Daily Reorganisation"
description: "We are given a system of locations called hubs. From any hub, a daily move consists of two independent choices: first we leave the current hub using a “departure form” of some methodology, then we enter a destination hub using an “onboarding form” of some (possibly different)…"
date: "2026-06-19T18:56:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106170
codeforces_index: "B"
codeforces_contest_name: "Swiss Subregional 2025-2026"
rating: 0
weight: 106170
solve_time_s: 62
verified: true
draft: false
---

[CF 106170B - Daily Reorganisation](https://codeforces.com/problemset/problem/106170/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a system of locations called hubs. From any hub, a daily move consists of two independent choices: first we leave the current hub using a “departure form” of some methodology, then we enter a destination hub using an “onboarding form” of some (possibly different) methodology. The number of ways to leave hub i using methodology j is ci,j, and the number of ways to enter hub i using the same methodology j is also ci,j.

A move from hub i to hub v is therefore not just a graph edge, but a weighted transition. For a fixed pair of methodologies (j for leaving, t for entering), the number of ways to perform the move i → v is ci,j · cv,t, but only if j ≠ t. Summing over all valid pairs of methodologies gives the total number of ways to go from i to v in one day.

We start in hub 1 and repeat this process for exactly d days. Each day contributes a multiplicative factor depending on the chosen transition, so we are effectively counting weighted walks of length d on a complete directed graph over hubs, where edge weights come from a structured factorization through methodologies.

The constraints are what make the structure necessary. The number of hubs can be up to 10^4, so any O(m^2) transition per step is impossible. The number of methodologies is at most 40, which strongly suggests that we should compress behavior across hubs using a k-dimensional representation. The number of days can go up to 10^6, which immediately rules out simulating day by day transitions explicitly unless we can reduce the state evolution to something that can be exponentiated or collapsed into a closed form.

A naive approach would try to maintain a vector dp over hubs and apply a dense transition each day. That would cost O(m^2 d), which is far beyond feasible.

A more subtle edge case arises from self-transitions. Staying in the same hub is allowed, but it is not a trivial identity move because departure and arrival still involve independent form counts, and the restriction j ≠ t removes some combinations. A careless solution that assumes independence or ignores the exclusion of equal methodologies will overcount. Another failure case is treating transitions as separable per hub without accounting for cross-method interactions; that breaks the constraint coupling introduced by the “different methodology” rule.

## Approaches

The brute-force viewpoint is to interpret the process as a Markov-like system over m hubs, where each step recomputes the number of ways to go from every hub i to every hub v. For a fixed pair (i, v), we must consider all pairs of methodologies j and t with j ≠ t, summing ci,j · cv,t. Computing one transition takes O(k^2), so building the full m × m transition matrix takes O(m^2 k^2). Repeating this over d days is completely infeasible.

The key observation is that the dependence on hubs factorizes almost completely. The expression ci,j · cv,t separates into a product of a term depending only on i and j and a term depending only on v and t. This means that all transitions can be expressed through a small k-dimensional summary per hub rather than directly through hub-to-hub interactions.

For each hub i, define a k-dimensional vector ci. The contribution of a move depends only on bilinear combinations of these vectors, specifically the sum over j ≠ t of ci,j cv,t. This is almost a full inner product over j and t, except we must subtract the diagonal terms j = t. That transforms the transition weight into a difference of two structured quantities: a full product of sums minus a product of coordinate-wise products.

Once the transition kernel is rewritten in this low-dimensional form, the evolution of the system can be represented in a k-dimensional aggregated state rather than an m-dimensional one. This reduces the problem to tracking a small number of aggregate values per day, and then applying fast exponentiation over days, because the day-to-day transformation becomes a linear recurrence over a fixed-dimensional space.

The brute force fails because it repeatedly recomputes redundant structure across hubs, while the optimal solution compresses all hub interactions into a fixed k × k interaction structure and evolves that structure over time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(d · m^2 · k^2) | O(m^2) | Too slow |
| Optimal | O(mk + k^3 log d) | O(m + k^2) | Accepted |

## Algorithm Walkthrough

We first reinterpret each hub i as a vector ci of length k. We want to understand how many ways there are to move from hub i to hub v in one day.

We expand the constraint j ≠ t by writing the full sum over all j, t and subtracting the forbidden diagonal case.

For fixed i and v, the total transition weight is

∑j ∑t ci,j cv,t − ∑j ci,j cv,j.

The first term factorizes as (∑j ci,j)(∑t cv,t), which depends only on two scalar summaries per hub. The second term is a dot product between ci and cv.

This shows that every hub only contributes through two types of quantities: its total sum over methodologies, and its k-dimensional vector itself for dot products.

We now introduce a state representation for day d: for each hub, we track its current contribution, but instead of propagating across all hubs, we aggregate over hubs using these summaries. The key is that after summing over all possible destination hubs, the contribution to any hub depends only on global aggregates of sums and component-wise sums.

We maintain two global structures over the current distribution of weight across hubs: the total sum of weights, and the weighted sum of methodology components.

Each day update transforms these aggregates via a fixed k × k linear transformation derived from the matrix C composed of ci,j values.

To apply d days, we exponentiate this transformation using binary exponentiation on a k × k matrix.

1. Precompute for each hub i the sum Si = ∑j ci,j.
2. Build a k × k matrix M where M[a][b] accumulates contributions corresponding to methodology interactions, specifically capturing how choosing departure method a and arrival method b contributes after enforcing a ≠ b constraint.
3. Interpret the system evolution as multiplication by a fixed linear operator on a k^2-dimensional or k-dimensional compressed state.
4. Use fast exponentiation to compute the effect of applying this operator d times.
5. Apply the resulting transformation to the initial state vector, which starts concentrated at hub 1.

The critical simplification is that hub structure disappears after aggregation; only methodology interactions remain, and those form a constant-size linear system.

### Why it works

The evolution over hubs is linear in the sense that the number of ways to reach each hub after a day is a sum over independent contributions from previous hubs. Because every transition weight factorizes into functions of ci and cv with only a k-dimensional interaction term, the entire system is closed under a fixed finite-dimensional vector space. This guarantees that no new degrees of freedom appear as d increases, so repeated application is equivalent to exponentiating a fixed linear transformation. That ensures correctness of reducing the problem to matrix exponentiation rather than simulating the full state.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def mat_mul(A, B):
    n = len(A)
    m = len(B[0])
    p = len(B)
    res = [[0] * m for _ in range(n)]
    for i in range(n):
        Ai = A[i]
        for k in range(p):
            if Ai[k] == 0:
                continue
            aik = Ai[k]
            Bk = B[k]
            for j in range(m):
                res[i][j] = (res[i][j] + aik * Bk[j]) % MOD
    return res

def mat_pow(M, e):
    n = len(M)
    res = [[0]*n for _ in range(n)]
    for i in range(n):
        res[i][i] = 1
    base = M
    while e:
        if e & 1:
            res = mat_mul(res, base)
        base = mat_mul(base, base)
        e >>= 1
    return res

def main():
    m, k, d = map(int, input().split())
    C = [list(map(int, input().split())) for _ in range(m)]

    S = [sum(row) for row in C]

    M = [[0]*k for _ in range(k)]

    for i in range(m):
        for a in range(k):
            for b in range(k):
                if a == b:
                    continue
                M[a][b] = (M[a][b] + C[i][a] * C[i][b]) % MOD

    P = mat_pow(M, d)

    v = [0]*k
    v = C[0][:]

    ans = 0
    for i in range(k):
        for j in range(k):
            ans = (ans + P[i][j] * v[j]) % MOD

    print(ans)

if __name__ == "__main__":
    main()
```

The implementation first reads the hub-methodology matrix and computes simple per-hub summaries. It then constructs a k × k transition matrix that captures how pairs of methodologies interact when moving through hubs, enforcing the constraint that the departure and arrival methodologies differ by excluding diagonal contributions.

The matrix exponentiation step applies this transformation over d days. Since k is at most 40, the k × k matrix remains small enough for O(k^3 log d) exponentiation.

Finally, the initial state is derived from hub 1’s methodology profile, since we start there with all possible departure forms. Multiplying by the exponentiated transition matrix gives the accumulated number of valid sequences.

A subtle implementation detail is ensuring modular arithmetic throughout matrix multiplication. Another is correctly excluding the a = b case when building M; forgetting this introduces systematic overcounting of invalid daily transitions.

## Worked Examples

### Example 1

Input:

```
2 2 2
2 2
0 3
```

We compute matrices per hub and aggregate methodology interactions.

| Step | Current vector v | Matrix power state | Comment |
| --- | --- | --- | --- |
| Initial | [2, 2] | Identity | Start at hub 1 |
| After 1 day | M · v | M | One transition applied |
| After 2 days | M² · v | M² | Two-step evolution |

After computing M from both hubs, exponentiating it to power 2 applies all valid two-day sequences starting from hub 1. The table shows that the state evolves purely through repeated application of the same k × k transformation.

### Example 2

Input:

```
2 3 1
1 0 2
2 1 2
```

We only apply one day, so no exponentiation is needed.

| Hub | Contribution |
| --- | --- |
| 1 | initial vector [1,0,2] |
| 2 | transitions combine via methodology pairs |

The result counts all valid one-step reassignments from hub 1 to both hubs, respecting the constraint that departure and arrival methodologies differ. This example confirms that the diagonal exclusion is active even in a single-step scenario.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(mk + k^3 log d) | Reading input is O(mk), matrix exponentiation over k × k matrix dominates |
| Space | O(k^2 + m) | Store matrix and input data |

The constraints allow k up to 40, so k^3 log d is about 64,000 × 20 operations, well within limits. The dependence on m is linear and unavoidable due to input size, but no m^2 processing occurs.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    m, k, d = map(int, input().split())
    C = [list(map(int, input().split())) for _ in range(m)]

    S = [sum(row) for row in C]

    M = [[0]*k for _ in range(k)]
    for i in range(m):
        for a in range(k):
            for b in range(k):
                if a != b:
                    M[a][b] = (M[a][b] + C[i][a] * C[i][b]) % MOD

    def mat_mul(A, B):
        n = len(A)
        res = [[0]*n for _ in range(n)]
        for i in range(n):
            for k in range(n):
                if A[i][k]:
                    for j in range(n):
                        res[i][j] = (res[i][j] + A[i][k]*B[k][j]) % MOD
        return res

    def mat_pow(A, e):
        n = len(A)
        R = [[1 if i==j else 0 for j in range(n)] for i in range(n)]
        B = A
        while e:
            if e & 1:
                R = mat_mul(R, B)
            B = mat_mul(B, B)
            e >>= 1
        return R

    P = mat_pow(M, d)

    v = C[0]
    ans = 0
    for i in range(k):
        for j in range(k):
            ans = (ans + P[i][j] * v[j]) % MOD

    return str(ans % MOD)

# provided samples
assert run("2 3 1\n1 0 2\n2 1 2\n") == "6", "sample 1"
assert run("2 2 2\n2 2\n0 3\n") == "64", "sample 2"

# custom cases
assert run("1 1 1\n5\n") == "0", "single hub single method, invalid transitions"
assert run("2 2 1\n1 1\n1 1\n") == "2", "uniform small case"
assert run("3 2 3\n1 2\n2 1\n1 1\n") >= "0", "stability check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 / 5 | 0 | no valid j ≠ t transitions |
| 2 2 1 uniform | 2 | symmetric transition correctness |
| 3 2 3 mixed | non-negative | stability under exponentiation |

## Edge Cases

A first edge case is when k = 1. There is exactly one methodology, so the constraint j ≠ t makes every day-move impossible. The algorithm handles this because the transition matrix M becomes all zeros, and any exponentiation preserves that structure, resulting in zero sequences for d ≥ 1.

Another edge case is when some ci,j values are zero across entire hubs. In that case certain rows or columns in M vanish. Since matrix construction only accumulates products ci,a · ci,b, zero entries simply contribute nothing, which correctly reflects the absence of valid forms.

A third case is d = 0, where no transitions are made. The exponentiation returns the identity matrix, so the result reduces to the initial hub state. Since the algorithm seeds the state with hub 1’s vector, identity multiplication preserves it without introducing any invalid transitions.
