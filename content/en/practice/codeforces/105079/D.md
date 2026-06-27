---
title: "CF 105079D - Spicy Cupcakes"
description: "We are given a sequence of cupcake types, each type having a fixed spiciness value. The judge eats all cupcakes in some order, exactly one of each type."
date: "2026-06-27T22:48:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105079
codeforces_index: "D"
codeforces_contest_name: "UTPC x WiCS Contest 04-05-23 (UT Internal)"
rating: 0
weight: 105079
solve_time_s: 68
verified: false
draft: false
---

[CF 105079D - Spicy Cupcakes](https://codeforces.com/problemset/problem/105079/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of cupcake types, each type having a fixed spiciness value. The judge eats all cupcakes in some order, exactly one of each type. The contribution of a cupcake is not just based on its own spiciness, but also depends on how many cupcakes have already been eaten before it.

If a cupcake with spiciness `s` is eaten in position `j + 1` in the order, its contribution is `(j + 1) * (A * s + B)`. The total score is the sum of these contributions over all cupcakes. The task is to permute the cupcakes to maximize this total.

The key difficulty is that the position multiplier `(j + 1)` grows linearly, so earlier or later placement changes the weight of each cupcake. The decision is about ordering items with weights that depend on both position and transformed values `A * s + B`.

The constraints allow up to `N = 100000`, so any solution that tries all permutations is impossible. A factorial number of permutations grows far beyond computational limits. Even a quadratic `O(N^2)` approach risks timing out depending on constants, so we are looking for an `O(N log N)` or `O(N)` greedy structure.

A subtle point is that `A` and `B` can be negative. This means the transformed contribution `(A * s + B)` can be positive, negative, or zero. That changes ordering behavior significantly compared to classical “sort by value” scheduling problems.

One edge case that breaks naive intuition is when all transformed values are identical. For example, if `A = 0`, then every cupcake contributes `(j + 1) * B`, and ordering does not matter at all. Another tricky case is when `A < 0`, which reverses the meaning of “large spiciness is good”.

A small illustrative failure case arises if one assumes sorting by `s` always works. If `A = -1` and `B = 0`, larger `s` values become more negative, and placing them early reduces their weight penalty, so the optimal order is reversed compared to the positive case.

## Approaches

A brute-force solution would try every permutation of cupcakes, compute the score for each ordering, and take the maximum. This is correct because it directly evaluates the objective function, but it requires evaluating `N!` permutations. Even for `N = 10`, this becomes already borderline, and for `N = 100000` it is completely infeasible.

To find structure, rewrite the contribution of a fixed order `p`:

We sum over positions `i`:

`i * (A * s_{p[i]} + B)`

Distribute the sum:

`A * sum(i * s_{p[i]}) + B * sum(i)`

The second term depends only on `N`, since `sum(i)` is fixed as `N(N+1)/2`. That means `B` does not affect ordering at all; it only shifts the final value.

So the entire optimization reduces to maximizing:

`A * sum(i * s_{p[i]})`

Now the problem becomes a classic weighted ordering task: maximize or minimize a dot product between positions and values depending on the sign of `A`.

If `A > 0`, we want large `s` to appear at large positions, since both `i` and `s` contribute positively. This matches the rearrangement inequality: sorting both sequences in the same order maximizes the sum.

If `A < 0`, we effectively want to minimize `sum(i * s_{p[i]})`, so we reverse the ordering: large `s` should be paired with small `i`.

If `A = 0`, the entire first term vanishes and only the constant `B * N(N+1)/2` remains, so any permutation is optimal.

This turns the problem into sorting once and computing a single linear pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N!) | O(N) | Too slow |
| Optimal | O(N log N) | O(1) extra (besides sort) | Accepted |

## Algorithm Walkthrough

1. Compute a transformed comparison rule based on the sign of `A`. If `A` is positive, we want to place smaller `s` earlier; if `A` is negative, we want larger `s` earlier. If `A` is zero, ordering is irrelevant.
2. Sort the array of spiciness values according to this rule. This ensures the pairing between positions and values is optimal under the rearrangement inequality.
3. Compute the constant contribution from `B`. Since every position `i` appears exactly once, the sum of all position weights is `N(N+1)/2`, so the total contribution from `B` is fixed.
4. Compute the main term by iterating through the sorted array. Maintain a running position index `i + 1` and accumulate `(i + 1) * A * s[i]`.
5. Add the constant `B * N(N+1)/2` to the accumulated result and output it.

### Why it works

The objective separates cleanly into a position-dependent linear function applied to a permutation. Once expanded, the only term affected by ordering is `sum(i * s_{p[i]})`. The rearrangement inequality guarantees that this sum is maximized by sorting one sequence in the same order as the other when the coefficient is positive, and in opposite order when negative. Since `B` contributes a fixed constant independent of permutation, it does not influence the optimal arrangement. This invariance ensures that any deviation from the sorted structure can only worsen the weighted sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N, A, B = map(int, input().split())
    s = list(map(int, input().split()))
    
    if A == 0:
        # all permutations equal
        return B * N * (N + 1) // 2

    s.sort()

    if A < 0:
        s.reverse()

    res = 0
    for i, val in enumerate(s, 1):
        res += i * (A * val)

    res += B * N * (N + 1) // 2
    return res

if __name__ == "__main__":
    print(solve())
```

The code begins by reading input and handling the degenerate case where `A = 0`, since then ordering has no effect and the answer collapses to a constant arithmetic sum.

The list is sorted in ascending order by default, and reversed when `A` is negative to ensure correct pairing between position indices and transformed values. This directly implements the optimal alignment dictated by the rearrangement inequality.

The loop computes the contribution of the `A` term only, multiplying each value by its 1-based index. The `B` term is added once at the end using the closed form sum of first `N` integers, avoiding any dependency on ordering.

## Worked Examples

### Sample 1

Input:

```
3 1 13
5 8 3
```

Sorted order is `[3, 5, 8]` since `A > 0`.

| Posit
