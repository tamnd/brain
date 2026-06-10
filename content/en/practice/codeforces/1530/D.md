---
title: "CF 1530D - Secret Santa"
description: "We are asked to construct a permutation-like assignment for a group of people. Each person must give a gift to exactly one other person, and no one is allowed to give a gift to themselves."
date: "2026-06-10T16:54:46+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "flows", "graphs", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1530
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 733 (Div. 1 + Div. 2, based on VK Cup 2021 - Elimination (Engine))"
rating: 1600
weight: 1530
solve_time_s: 158
verified: false
draft: false
---

[CF 1530D - Secret Santa](https://codeforces.com/problemset/problem/1530/D)

**Rating:** 1600  
**Tags:** constructive algorithms, flows, graphs, greedy, math  
**Solve time:** 2m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct a permutation-like assignment for a group of people. Each person must give a gift to exactly one other person, and no one is allowed to give a gift to themselves. This already means we are building a permutation of size `n` with the restriction that no position maps to itself.

In addition, each person has a preferred recipient. If person `i` gives a gift to `a_i`, that wish is considered satisfied. The goal is to build any valid derangement-like permutation that maximizes how many positions match their preferred target.

So the task is not just constructing any valid permutation, but one that aligns with the given array `a` as much as possible while still ensuring every value is used exactly once and no fixed points exist.

The constraint `n ≤ 2⋅10^5` over all test cases immediately forces a linear or near-linear solution. Any approach that considers many permutations, tries matching subsets exhaustively, or performs repeated matching with backtracking will fail because even `O(n log n)` per test case can be borderline if implemented with heavy constants, while `O(n^2)` is completely impossible.

The key structural constraint is that the output must be a permutation. This means every value is used exactly once, so even if many people want the same target, only one of them can get it. This global coupling is what makes greedy local assignment unsafe.

A subtle failure case appears when many indices point to the same `a_i`. For example, if all `a_i = 1`, then only one person can be assigned to 1, and the rest must be rearranged in a cycle. A naive greedy approach that assigns `b_i = a_i` whenever possible will break injectivity.

Another problematic situation is when following wishes produces a fixed point. If we assign `b_i = a_i` greedily, it is possible that some last remaining assignment forces `b_j = j`, which is forbidden. A small example is `a = [2, 1]`. If we greedily assign both, we get a valid cycle, but in larger mixed cases greedily fixing early choices can trap the last positions into self-loops.

The core difficulty is that we want to maximize matches to a given array under a permutation constraint with forbidden fixed points.

## Approaches

A brute-force approach would try all permutations of `b` that satisfy `b_i ≠ i` and then count how many positions match `a_i`. This is a standard assignment problem with constraints. The number of valid permutations is on the order of derangements, roughly `n! / e`, which is far beyond any computational limit even for `n = 10^5`. Even for `n = 10`, this becomes infeasible.

A more structured brute-force would be to treat it as an assignment problem and use maximum bipartite matching between left nodes `i` and right nodes `j`, forbidding edges `i -> i`, and maximizing matches where `j = a_i` has priority. This becomes a weighted matching problem with `n` vertices on each side and `O(n^2)` edges. A flow or Hungarian-style solution is theoretically correct but too slow for `n = 2⋅10^5`.

The key observation is that the structure is not arbitrary matching. Each node only has one “preferred” edge that gives value 1, and all other edges are equivalent (value 0). So we are maximizing how many times we can use preferred edges while still producing a permutation.

This reduces the problem to resolving conflicts inside groups of identical preferences and fixing only the cases where taking all preferred edges would break injectivity or create a fixed point.

The crucial structural fact is that conflicts happen only inside groups of equal `a_i`. Across groups, assignments are independent except for global availability of targets. This suggests we can first assign all “safe” preferred edges and then repair remaining structure using leftover positions, typically by cycling them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Permutations | O(n!) | O(n) | Too slow |
| Maximum Matching / Flow | O(n^2 √n) or worse | O(n^2) | Too slow |
| Greedy with cycle repair | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We separate indices by their preferred target. For each value `x`, we maintain the list of indices that want `x`. We then try to assign `x` to one of these indices.

1. Group all indices by their desired value `a_i`. This identifies all competitors for each target.
2. For each value `x`, consider all indices that want `x`. If `x` itself is among them, we are careful because assigning `b_x = x` is forbidden.
3. For each group of indices wanting `x`, we can assign `x` to one of them, but not necessarily all.
4. We maintain a set of unused targets. Initially, all numbers `1..n` are available.
5. We iterate through indices and try to assign `b_i = a_i` only if `a_i` is still unused and `a_i ≠ i`. If both hold, we tentatively assign it and mark `a_i` as used.
6. After this greedy phase, some positions remain unassigned, and some values remain unused. We collect both lists.
7. We now match remaining positions with remaining values arbitrarily, but we must avoid fixed points. If at any point position `i` would get value `i`, we swap it with another value.
8. A simple linear fix is to rotate the leftover values by one position, which guarantees no fixed points as long as there are at least two elements.

The reason this works is that the greedy phase only commits to safe matches where the target has not yet been taken. This ensures injectivity. Any remaining unmatched indices form a subproblem where no preferred assignment is possible without conflicts, so all remaining structure can be rearranged freely.

## Why it works

At any point, each value is assigned at most once because we only use a target when it is still unused. Thus `b` remains a permutation invariant throughout construction.

Every time we assign `b_i = a_i`, we maximize the number of satisfied wishes locally without blocking future assignments that would have been impossible anyway, since any later attempt to use the same value would be invalid.

The leftover positions form a set where no safe preferred assignments remain, meaning every remaining assignment must be a permutation of the remaining values. A cyclic shift on this residual set avoids fixed points by construction, because shifting ensures every index maps to a different index.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        used = [False] * (n + 1)
        b = [-1] * n

        free_pos = []

        for i in range(n):
            x = a[i]
```
