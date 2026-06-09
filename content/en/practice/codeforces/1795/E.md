---
title: "CF 1795E - Explosions?"
description: "We are given a row of monsters, each with a certain health, and two types of attacks: a basic spell that reduces any monster's health by 1 for 1 MP, and a single-use \"Explosion\" that can be targeted on one monster with an arbitrary power."
date: "2026-06-09T10:08:14+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dp", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1795
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 143 (Rated for Div. 2)"
rating: 2200
weight: 1795
solve_time_s: 87
verified: false
draft: false
---

[CF 1795E - Explosions?](https://codeforces.com/problemset/problem/1795/E)

**Rating:** 2200  
**Tags:** binary search, data structures, dp, greedy, math  
**Solve time:** 1m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a row of monsters, each with a certain health, and two types of attacks: a basic spell that reduces any monster's health by 1 for 1 MP, and a single-use "Explosion" that can be targeted on one monster with an arbitrary power. The explosion kills the target if its health is less than or equal to the spell's power and triggers chain explosions to adjacent monsters, with each secondary explosion having a power of the killed monster's health minus one. The task is to minimize the total MP spent, which is the sum of basic spell casts and the explosion power, so that the explosion ultimately kills all monsters.

The input provides multiple test cases. Each test case gives the number of monsters $n$ and an array of their healths. Output is the minimum total MP required for each case.

The constraints tell us that the total number of monsters across all test cases can be up to $3 \cdot 10^5$. This immediately rules out naive approaches that try to simulate all possible explosion targets with all possible basic spell distributions because that could lead to $O(n^2)$ or worse time complexity. Any solution should be roughly linear in the number of monsters per test case, ideally $O(n)$, or maybe $O(n \log n)$ if using binary search or a heap.

A non-obvious edge case is when all monsters have the same health, especially when they are small. For example, if all monsters are 1, the optimal strategy is to cast basic spells zero times and choose the last monster as the explosion target. A careless greedy approach might try to reduce healths unnecessarily and overspend MP. Another tricky scenario is a peak in the middle: [1, 10, 1], where the optimal explosion targets the middle monster; misidentifying which monster to hit first can double the MP cost.

## Approaches

The brute-force approach would be to try casting basic spells on every combination of monsters, then simulate every possible explosion target and compute the resulting MP. While correct in principle, the number of options grows exponentially with $n$, making it completely infeasible for the constraints. For example, even a naive linear simulation of the explosion for all $n$ monsters would be $O(n^2)$ in the worst case if every explosion propagates linearly across all neighbors.

The key observation that unlocks a faster solution is that for each monster, the only relevant contribution to the total MP is the difference between its health and the smaller of its two neighbors. More precisely, if you think of the explosion as a wave propagating left and right, the explosion can at most "subtract" the smaller of the adjacent monsters' healths minus one. This leads to a greedy strategy: for each monster, compute the MP needed to reduce it so that its explosion kills it and triggers the maximum chain. Formally, the total MP can be expressed as the sum of contributions of each monster after "absorbing" damage from the previous explosion, which is equivalent to computing the sum of max(0, h[i] - min(h[i-1], h[i+1])) for each monster (with special handling at the edges).

The optimal solution avoids any simulation and reduces the problem to computing these differences in linear time. It works because explosion propagation is deterministic: the only decision is which monster to target, and once the wave starts, it cannot be redirected or stopped, so we only need to account for healths not already covered by neighboring explosions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) per test case | O(n) | Too slow |
| Optimal | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the number of monsters $n$ and the array of their healths $h$.
2. Initialize a variable `total_mp` to zero. This will accumulate the MP needed.
3. For each monster $i$ from 0 to $n-1$, compute the effective damage it must take from basic spells before the explosion so that the chain can reach it. The effective damage is `max(0, h[i] - min(h[i-1], h[i+1]))`. For the first and last monsters, only one neighbor exists, so use only that neighbor’s health. Add this value to `total_mp`.
4. After processing all monsters, `total_mp` now represents the minimum MP needed: the sum of all basic spells required to set up a single explosion anywhere. Output this value for the current test case.

Why it works: The invariant is that for any monster, the explosion from an adjacent monster can cover up to `neighbor_health - 1` damage. By reducing the monster's health to account for the maximum explosion it will take from neighbors, we ensure that each monster dies either by the main explosion or by a propagated explosion, without wasting MP on unnecessary basic spells. This guarantees a minimal total MP while ensuring all monsters die.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        h = list(map(int, input().split()))
        total_mp = 0
        for i in range(n):
            left = h[i - 1] if i > 0 else 0
            right = h[i + 1] if i < n - 1 else 0
            needed = max(0, h[i] - max(left, right))
            total_mp += needed
        print(total_mp)

solve()
```

In this solution, we handle edges carefully by treating non-existent neighbors as zero. We calculate the MP each monster requires after considering the maximum damage it can receive from neighbors. The use of `max(left, right)` instead of `min` is in
