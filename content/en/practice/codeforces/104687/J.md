---
title: "CF 104687J - \u0412\u044b\u0431\u043e\u0440 \u0447\u0438\u0441\u0435\u043b 3"
description: "We are given a sequence of integers indexed from left to right. The task is to select exactly k elements from this sequence so that any two chosen positions are at least d apart. In other words, if we pick indices i1 < i2 < ..."
date: "2026-06-29T08:47:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104687
codeforces_index: "J"
codeforces_contest_name: "\u041e\u0442\u0431\u043e\u0440 \u0432 \u0426\u0420\u041e\u0414 2022"
rating: 0
weight: 104687
solve_time_s: 25
verified: false
draft: false
---

[CF 104687J - \u0412\u044b\u0431\u043e\u0440 \u0447\u0438\u0441\u0435\u043b 3](https://codeforces.com/problemset/problem/104687/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 25s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of integers indexed from left to right. The task is to select exactly `k` elements from this sequence so that any two chosen positions are at least `d` apart. In other words, if we pick indices `i1 < i2 < ... < ik`, then each consecutive gap must satisfy `i(t+1) - i(t) ≥ d`. Among all valid selections, we want the one that maximizes the sum of the chosen values.

The constraint on `k` being at most 50 is the central structural hint. It means we are not searching over arbitrary subsets of size up to 150000, but over very short increasing sequences, which allows dynamic programming over the number of picks.

The bound `(k - 1) * d + 1 ≤ n` guarantees feasibility, so we never face an impossible configuration. It also implies that spacing constraints are not degenerate; there is always enough room to place `k` elements.

A naive approach would try all ways to pick `k` indices with spacing constraints. Even if we only consider combinations, the number of valid subsets is still exponential in `n`, since for each position we either pick or skip with constraints. For `n = 150000`, brute force is infeasible.

A more subtle issue appears if one tries greedy selection. Picking locally large elements fails because a high value early in the array may block multiple later positions due to spacing, and a slightly smaller early pick can enable several large future picks.

A simple counterexample:

Input:

```
6 2 3
10 1 1 1 100 1
```

Greedy picking 10 first blocks index 2 and 3, forcing the second pick to be at 5 or 6, yielding 110. However skipping 10 allows choosing 100, giving 100 + 10 = 110 here equal, but slight variations easily break greedy behavior when multiple candidates interact. The real issue is that local decisions have long-range constraints.

We therefore need a method that evaluates combinations systematically with reuse of subproblems.

## Approaches

The brute-force formulation is straightforward: choose a subset of size `k`, ensure spacing constraints hold, compute sum, take maximum. This requires enumerating all combinations with pruning for distance violations. Even with pruning, the branching factor remains high because each position may or may not be chosen, and checking validity repeatedly still leads to exponential growth.

The key observation is that the structure depends only on two parameters: the current index and how many elements we still need to pick. Once we decide to take an element at position `i`, the next decision is forced to start from at least `i + d`.

This creates a clean overlapping subproblem structure. Define a state that represents the best possible sum starting from a position while needing to pick a fixed number of elements. From each state, we either skip the current position or take it and jump forward by `d`.

Since `k ≤ 50`, the number of states in the “how many picked so far” dimension is small. This suggests dynamic programming where transitions scan forward efficiently. The main challenge is making transitions fast enough, since naive scanning from every position would still be too slow.

We fix this by reversing the perspective: instead of starting decisions from every position, we precompute best transitions for each `(i, t)` where `t` is how many elements we still need. We process positions from right to left so future states are already known.

The problem then becomes a layered DP over `k` layers, each layer computing best sums for picking `t` elements starting at each index.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | exponential in n | O(k) recursion stack | Too slow |
| Optimal DP | O(nk) | O(nk) or O(nk) optimized | Accepted |

## Algorithm Walkthrough

We define `dp[t][i]` as the maximum sum we can obtain by selecting `t` elements starting from index `i` or later, assuming the next chosen index is at least `i`.

1. Initialize base case: for `t = 0`, set `dp[0][i] = 0` for all `i`. This represents that selecting zero elements yields zero sum regardless of position.
2. Process number of picks from `t = 1` up to `k`. Each layer depends only on the previous one.
3. For a fixed `t`, we compute `dp[t][i]` from right to left over `i`. This ensures that when we consider taking position `i`, the state `dp[t-1][i + d]` is already known.
4. At position `i`, we consider two choices. We skip `i`, so the value becomes `dp[t][i+1]`. This represents ignoring the current element.
5. Alternatively, we take `a[i]` and then we must pick `t-1` more elements starting from `i + d`. This contributes `a[i] + dp[t-1][i + d]`.
6. We assign `dp[t][i]` as the maximum of skipping and taking. This encodes all valid decisions at position `i` for `t` picks.
7. Answer is `dp[k][1]`, meaning we start from the first position and must pick `k` elements.

### Why it works

The correctness rests on the fact that every valid selection ha
