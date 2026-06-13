---
title: "CF 1204E - Natasha, Sasha and the Prefix Sums"
description: "We are looking at all possible sequences of length $n+m$ made of exactly $n$ ones and $m$ minus ones. Every arrangement is considered once, so this is a multiset permutation problem."
date: "2026-06-13T15:48:54+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1204
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 581 (Div. 2)"
rating: 2300
weight: 1204
solve_time_s: 467
verified: false
draft: false
---

[CF 1204E - Natasha, Sasha and the Prefix Sums](https://codeforces.com/problemset/problem/1204/E)

**Rating:** 2300  
**Tags:** combinatorics, dp, math, number theory  
**Solve time:** 7m 47s  
**Verified:** no  

## Solution
## Problem Understanding

We are looking at all possible sequences of length $n+m$ made of exactly $n$ ones and $m$ minus ones. Every arrangement is considered once, so this is a multiset permutation problem. For each sequence, we scan prefixes from left to right, compute their running sums, and record the largest prefix sum achieved, but we clamp it below by zero so that sequences which never go above zero contribute zero.

The task is not to evaluate one sequence, but to sum this “best prefix height” over every valid permutation of the multiset.

A direct reading suggests that what matters is how often positive excursions happen in all prefix-sum walks formed by permutations of $+1$ and $-1$. Since $n,m \le 2000$, the number of permutations is $\binom{n+m}{n}$, which is enormous even at moderate values. Any approach that explicitly enumerates permutations is immediately impossible.

The deeper structure is that each sequence is a lattice path starting at zero, moving up for $+1$ and down for $-1$. The maximal prefix sum is the maximum height reached by that path, but never below zero.

Edge cases that break naive thinking appear when negative steps dominate early. For example, when $n=0$, every prefix sum is non-positive, so all contributions are zero. Another corner is when $m=0$, where every permutation is all ones and the answer is simply $n$ per sequence, multiplied by a single configuration.

A more subtle issue is that the maximum prefix sum is not tied to the final sum $n-m$. Even sequences that end high may never have a large prefix peak if the ones are delayed, so counting based only on final displacement fails.

## Approaches

A brute-force solution would generate every permutation of the multiset and compute prefix maxima in $O(n+m)$ per sequence. Since there are $\binom{n+m}{n}$ sequences, this leads to roughly $O((n+m)\binom{n+m}{n})$, which explodes beyond any limit for $n,m\le 2000$.

The key structural shift is to stop thinking in terms of permutations and instead think in terms of when the maximum prefix sum becomes at least a given value. If we fix a height $h$, we can ask how many sequences ever reach prefix sum $\ge h$. Every sequence contributes its maximum height, so it contributes $1$ for each level it manages to reach. This turns the problem into summing over levels rather than sequences.

So instead of summing maxima directly, we count contributions level by level. For each $h \ge 1$, we count how many sequences have a prefix that reaches at least $h$. This is equivalent to counting paths that never stay strictly below $h$ before their first hitting time of $h$. This is a classic reflection principle setup: we count all sequences and subtract those that never reach level $h$.

For a fixed $h$, we shift the coordinate system so that reaching $h$ corresponds to reaching zero in a transformed walk, and we reduce the problem to counting paths that stay below a boundary. This becomes a combinatorial prefix restriction problem, solvable using binomial coefficients and standard “ballot-type” counts.

Summing these contributions over all possible $h$ yields the final answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O((n+m)\binom{n+m}{n})$ | $O(n+m)$ | Too slow |
| Optimal | $O(nm)$ | $O(nm)$ | Accepted |

## Algorithm Walkthrough

We reinterpret the answer using the identity

$$f(a) = \sum_{h \ge 1} [\text{prefix sum reaches } h].$$

So the total answer becomes a sum over heights of the number of valid permutations that reach that height.

1. Define $C = \binom{n+m}{n}$, the total number of sequences. This is the baseline from which all restricted counts are derived.
2. For a fixed height $h$, define a function $g(h)$ as the number of sequences whose prefix sums never reach $h$. These are exactly sequences where the maximum prefix sum is at most $h-1$.
3. We compute $g(h)$ using a ballot-style transformation. If a path never reaches $h$, then shifting all prefix sums down by $h$ transforms the problem into counting paths that stay strictly below zero after a shift. This becomes equivalent to a constrained walk from $(0,0)$ that never crosses a boundary line.
4. Using reflection principle, the number of sequences that ever reach $h$ is

$$C - \binom{n+m}{n-h}$$

whenever $n \ge h$, otherwise all sequences fail to reach $h$.

This comes from reflecting the first hitting point at level $h$, which maps invalid paths to unconstrained paths with reduced counts of up steps.
5. Each height $h$ contributes exactly the number of sequences that reach it, so we add:

$$\sum_{h=1}^{n} \left(C - \binom{n+m}{n-h}\right)$$
6. Split the sum:

$$n \cdot C - \sum_{h=1}^{n} \binom{n+m}{n-h}$$

Reindexing simplifies the second term into a standard prefix of binomial coefficients.
7. Precompute factorials and inverse factorials to evaluate all binomial coefficients in $O(1)$ each, then evaluate the sum in $O(n)$.

### Why it works

Every sequence contributes exactly one unit for each integer level it manages to reach. Counting “reach level $h$” converts the maximum operation into a sum of indicator events. The reflection principle ensures that the number of paths that fail to reach a threshold can be expressed as a single shifted binomial coefficient. Since each path is uniquely mapped under reflection at its first violation, no overcounting or omission occurs, and the decomposition over heights remains exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244853

def solve():
    n, m = map(int, input().split())
    N = n + m

    if n == 0:
        print(0)
        return

    # factorials up to N
    fact = [1] * (N + 1)
    invfact = [1] * (N + 1)

    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    def C(a, b):
        if b < 0 or b > a:
            return 0
        return fact[a] * invfact[b] % MOD * invfact[a - b] % MOD

    total
```
