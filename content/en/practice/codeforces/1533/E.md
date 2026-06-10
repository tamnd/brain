---
title: "CF 1533E - Chess Team Forming"
description: "We are tasked with forming a chess team by adding one final player to Polycarp's existing roster of $n$ members. Each player's strength is an integer, and the opposing team already has $n+1$ members."
date: "2026-06-10T16:22:14+07:00"
tags: ["codeforces", "competitive-programming", "*special", "binary-search", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1533
codeforces_index: "E"
codeforces_contest_name: "Kotlin Heroes: Episode 7"
rating: 0
weight: 1533
solve_time_s: 192
verified: true
draft: false
---

[CF 1533E - Chess Team Forming](https://codeforces.com/problemset/problem/1533/E)

**Rating:** -  
**Tags:** *special, binary search, data structures, greedy  
**Solve time:** 3m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are tasked with forming a chess team by adding one final player to Polycarp's existing roster of $n$ members. Each player's strength is an integer, and the opposing team already has $n+1$ members. The goal is to select one candidate from $m$ options so that, after pairing our team against the opposing team, the maximum difference between a player's opponent and themselves-the game difficulty-is minimized.

The input gives us the skills of our current team $a_1 \dots a_n$, the opposing team $b_1 \dots b_{n+1}$, and the candidate options $c_1 \dots c_m$. For each candidate, we need to compute the minimum possible difficulty we can achieve by optimally pairing players.

The constraints are substantial: $n$ and $m$ can reach $2 \cdot 10^5$, meaning any $O(n \cdot m)$ or $O(n^2)$ approach will be too slow. With 2 seconds of execution, we need a solution that is close to $O(n \log n + m \log n)$ or better.

Edge cases that a naive implementation might miss include situations where the candidate's skill is either much smaller or much larger than all existing team members. For example, if all $a_i = 1$ and the candidate is $c_k = 10^9$, pairing poorly could produce a huge difficulty. A careless algorithm that does not consider sorting and optimal pairing order would produce wrong results in these extremes.

## Approaches

A brute-force approach would consider adding each candidate to the team, generating all $n+1$ factorial possible pairings with the opposing team, and computing the maximum difficulty for each. This approach is correct in principle but utterly infeasible. For $n = 2 \cdot 10^5$, the number of permutations is astronomical.

The key observation is that minimizing the maximum difference is equivalent to matching the smallest skills with the smallest opposing skills and the largest with the largest, after sorting. This is because the function $f(x) = b_j - a_i$ is monotonic with respect to ordering: matching strong players with strong opponents reduces the worst-case gap. Therefore, sorting both the existing team and the opponent allows us to precompute the differences between consecutive members. We can compute two arrays of differences, one representing skipping the first opponent and the other skipping the last, effectively covering all insertion points for the new candidate. Then, for each candidate, a binary search finds the correct position in the sorted team, and the precomputed arrays quickly give the minimal difficulty.

The observation that we only need to consider adjacent pairs after sorting reduces the problem from $O((n+1)!)$ to $O(n \log n + m \log n)$, which is acceptable for the input size.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n+1)!) | O(n) | Too slow |
| Sorting + Greedy + Binary Search | O(n log n + m log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort Polycarp's current team $a$ and the opposing team $b$. This ensures that pairing by order will minimize individual difficulties.
2. Compute two prefix arrays: `left_diffs` for pairing $a_i$ with $b_{i-1}$ (skipping the first opponent) and `right_diffs` for pairing $a_i$ with $b_i$ (skipping the last opponent). Each stores the maximal difference for that scenario. These arrays represent the two natural "gaps" that the new candidate can fill.
3. For each candidate $c_k$, use binary search to determine where $c_k$ would fit in the sorted team $a$. This identifies which opponent gap it will occupy.
4. Compute the difficulty by combining the maximum difficulty of the prefix to the left, the difference introduced by the candidate, and the maximum difficulty of the suffix to the right. This step uses the precomputed arrays for $O(1)$ access.
5. Output the minimum difficulty for each candidate.

Why it works: Sorting ensures that pairing in order minimizes the maximum difference. Precomputing prefix maximums allows us to efficiently calculate the new maximum difficulty for any insertion of the candidate. The binary search guarantees the candidate is placed in the optimal spot relative to the existing team. By construction, the algorithm always evaluates the minimal achievable maximum difference for each candidate.

## Python Solution

```python
import sys
input = sys.stdin.readline
import bisect

n = int(input())
a = list(map(int, input().split()))
b = list(map(int, input().split()))
m = int(input())
c = list(map(int, input().split()))

a.sort()
b.sort()

left = [0] * n
right = [0] * n

for i in range(n):
    left[i] = b[i] - a[i]
for i in range(n):
    right[i] = b[i+1] - a[i]

pref_left = [0] * (n+1)
pref_right = [0] * (n+1)

for i in range(n):
    pref_left[i+1] = max(pref_left[i], left[i])
for i in range(n-1, -1, -1):
    pref_right[i] = max(pref_right[i+1], right[i])

res = []
for val in c:
    idx = bisect.bisect_left(a, val)
    max_left = pref_left[idx]
    max_right = pref_right[idx]
    max_diff = max(max_left, max_right, b[idx] - val)
    res.append(str(max_diff))

print(' '.join(res))
```

This solution first sorts the teams, then precomputes the differences when skipping either end of the opponent array. Binary search identifies the candidate's optimal insertion point, and the maximum difficulty is calculated in constant time per candidate. The careful handling of prefix arrays prevents off-by-o
