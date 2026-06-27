---
title: "CF 104968F - Pizza Stack"
description: "We are arranging a permutation of pizzas labeled from 1 to $n$, where each label is the radius of that pizza. Once we choose an order, we look at all pairs of positions in the stack: if a larger pizza appears below a smaller one, we call that pair “proper”."
date: "2026-06-28T06:47:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104968
codeforces_index: "F"
codeforces_contest_name: "UTPC Contest 02-09-24 Div. 2 (Beginner)"
rating: 0
weight: 104968
solve_time_s: 24
verified: true
draft: false
---

[CF 104968F - Pizza Stack](https://codeforces.com/problemset/problem/104968/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are arranging a permutation of pizzas labeled from 1 to $n$, where each label is the radius of that pizza. Once we choose an order, we look at all pairs of positions in the stack: if a larger pizza appears below a smaller one, we call that pair “proper”.

This is exactly the same as counting inversions in a permutation, except the definition is phrased in terms of “below” and “above” in a stack. If we write the stack from top to bottom as a permutation $p$, then a proper pair is any pair $i < j$ such that $p_i > p_j$.

So the task is: count how many permutations of $\{1,2,\dots,n\}$ have exactly $k$ inversions.

The constraints $n \le 1000$, $k \le 1000$ immediately suggest that we are counting permutations with a bounded inversion count, not enumerating permutations. A full enumeration is impossible since $n!$ grows extremely quickly, even for $n = 20$. The bound on $k$ is the key signal: although permutations are large, the inversion count we care about is small, so dynamic programming over $k$ is plausible.

A subtle edge case is when $k = 0$ or $k = \frac{n(n-1)}{2}$. For $k = 0$, only the increasing permutation works, so the answer is 1. For large $k$, we must remember that even though $k \le 1000$, the maximum possible inversions for $n = 1000$ is much larger, so many states correspond to zero valid permutations and must be handled naturally by DP bounds rather than assumptions.

Another common failure is treating this as a simple combinatorial insertion problem without controlling overcounting. Each insertion step affects inversion count in a range-dependent way, so naive greedy placement does not preserve correctness.

## Approaches

A brute-force approach would generate all permutations of size $n$ and count inversions for each, incrementing a counter when it equals $k$. This is correct but infeasible. Even $n = 12$ already produces $479001600$ permutations, and computing inversions per permutation would multiply that cost, leading to an explosion far beyond any time limit.

The key observation is to build permutations incrementally. Suppose we already know how many ways there are to arrange $i-1$ elements with a certain inversion count. When we insert element $i$, we choose a position in the current sequence. Placing $i$ at position $j$ contributes exactly $i - 1 - j$ new inversions, because all elements after position $j$ that are smaller than $i$ create inversions. Since $i$ is the largest element among the first $i$, every element to its right is smaller, so each right-side element contributes one inversion.

This reduces the problem to a standard dynamic programming formulation over prefix size and inversion count. The structure is identical to counting permutations by inversion number, also known as the Mahonian numbers.

We maintain a DP where $dp[i][j]$ is the number of permutations of $\{1..i\}$ with exactly $j$ inversions. Transitions come from inserting element $i$ into all possible positions in a permutation of size $i-1$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n! \cdot n)$ | $O(n)$ | Too slow |
| Optimal DP | $O(nk)$ | $O(nk)$ | Accepted |

## Algorithm Walkthrough

We define a DP table where each state records how many permutations of a prefix length achieve a given inversion count.

### Steps

1. Initialize a DP table of size $(n+1) \times (k+1)$ with zeros. Set $dp[0][0] = 1$.

This represents that there is exactly one way to arrange zero elements with zero inversions: the empty permutation.
2. Iterate over prefix size $i$ from 1 to $n$.

At each step, we incorporate element $i$ as the largest value in the current prefix.
3. For each $i$, compute transitions to $dp[i]$ from $dp[i-1]$.

We consider inserting $i$ into every possible position in a permutation of length $i-1$. If we insert it $pos$ positions from the right, it creates exactly $pos$ new inversions.
4. For each inversion count $j$ from 0 to $k$, accumulate contributions from valid insertions:

$$dp[i][j] = \sum_{x=0}^{\min(j, i-1)} dp[i-1][j-x]$$

Here $x$ represents the number of inversions contributed by placing $i$, and it ranges from 0 (placing at the end) to $i-1$ (placing at the front).
5. To compute this efficiently, use a prefix sum over $dp[i-1]$.

This avoids recomputing the sum for every $j$, reducing complexity from $O(n^2k)$ to $O(nk)$.
6. Return $dp[n][k]$ modulo $10^9 + 7$.

### Why it works

At step $i$, every valid permutation of size $i$ is formed uniquely by taking a permutation of size $i-1$ and inserting $i$ at exactly one position. That insertion contributes a deterministic number of new inversions equal to how many elements are shifted to the left of $i$. This gives a bijection between states of size $i-1$ and transitions into states of size $i$. The DP counts each construction exactly once, so no overcounting or omission occurs.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

n, k = map(int, input().split())

# dp[j] = number of permutations for current i with j inversions
dp = [0] * (k + 1)
dp[0] = 1

for i in range(1, n + 1):
    new = [0] * (k + 1)
    window_sum = 0

    for j in range(0, k + 1):
        window_sum += dp[j]
        if window_sum >= MOD:
            window_su_ -= MOD

        if j >= i:
            window_sum -= dp[j - i]
            if window_sum < 0:
                window_sum += MOD

        new[j] = window_sum

    dp = new

print(dp[k] % MOD)
```

The DP is com
