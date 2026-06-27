---
title: "CF 105172J - Divide the Sequence (easy version)"
description: "We are given a sequence of integers and we must cut it into exactly $k$ consecutive pieces. Once the sequence is split, we look inside each piece and count how many subarrays inside that piece have sum exactly equal to a fixed value $x$."
date: "2026-06-27T08:25:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105172
codeforces_index: "J"
codeforces_contest_name: "The 20th Southeast University Programming Contest (Summer)"
rating: 0
weight: 105172
solve_time_s: 27
verified: false
draft: false
---

[CF 105172J - Divide the Sequence (easy version)](https://codeforces.com/problemset/problem/105172/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of integers and we must cut it into exactly $k$ consecutive pieces. Once the sequence is split, we look inside each piece and count how many subarrays inside that piece have sum exactly equal to a fixed value $x$. The final cost of a partition is the sum of these counts over all $k$ segments, and we want to minimize that cost over all valid ways to split the sequence.

A key point is that every segment contributes independently to the cost once it is fixed, but the choice of where to cut affects how subarrays are grouped and therefore how many “sum equals $x$” intervals are counted inside each segment.

The constraints $n \le 3000$ and $k \le 20$ immediately suggest that anything cubic in $n$ is acceptable, but anything involving exponential splitting or recomputing segment costs from scratch for all partitions is too slow. A typical threshold here is around $n^2 k$, which is about $1.8 \cdot 10^8$, borderline but acceptable in optimized DP.

A naive attempt would try to enumerate all ways to split into $k$ segments, but that is combinatorially impossible since there are $\binom{n-1}{k-1}$ choices, already astronomical for $n=3000, k=20$.

A second naive mistake is recomputing the number of valid subarrays for every segment repeatedly. Even if we fix segments, computing the number of subarrays summing to $x$ inside each segment in $O(n^2)$ and embedding that inside a partition search leads to at least $O(n^3)$ or worse.

A subtle edge case is when $k = n$. Then every segment has length 1, so no subarray longer than 1 exists. The answer is simply the number of elements equal to $x$. Any DP that assumes segments must have length at least 2 would fail here.

Another edge case is when $k = 1$. Then we do not split at all, and we just count all subarrays in the full array whose sum is $x$. This serves as a correctness baseline for the subarray counting method.

## Approaches

We first consider the brute-force perspective. If we fix a partition of the array into $k$ segments, we can compute the cost of each segment independently. For a segment $[l, r]$, the number of subarrays with sum $x$ can be computed using prefix sums and a hash map in $O(r-l+1)$. This already gives $O(n)$ per segment, hence $O(nk)$ for a fixed partition.

The difficulty is that there are exponentially many partitions. Trying all ways to place $k-1$ cuts is infeasible.

The key observation is that the cost inside a segment depends only on its endpoints, not on global structure. This makes the problem a classic interval partition dynamic programming problem. We define a DP where we incrementally decide where each segment ends.

To make transitions efficient, we precompute the cost of every interval $[l, r]$, which is the number of subarrays inside it whose sum is $x$. This preprocessing can be done in $O(n^2)$ using prefix sums and a frequency map per starting point.

Once this cost table is available, the problem becomes: partition the prefix $1..i$ into $j$ segments minimizing sum of costs. The transition tries all previous cut positions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over partitions | exponential | O(1) | Too slow |
| Precompute interval costs + DP | $O(n^2 + n^2 k)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

We define prefix sums $p[i]$, where $p[i]$ is the sum of the first $i$ elements. This lets us compute any subarray sum in constant time.

We precompute a table $cost[l][r]$, which counts how many subarrays inside $[l, r]$ have sum exactly $x$. For each fixed $l$, we extend $r$ and maintain a hashmap of prefix sums seen inside that segment.

We then define DP:

Let $dp[j][i]$ be the minimum cost to split the prefix $1..i$ into exactly $j$ segments.

Transitions consider the last segment starting at position $t+1$ and ending at $i$, so:

$$dp[j][i] = \min_{t < i} dp[j-1][t] + cost[t+1][i]$$

The answer is $dp[k][n]$.

### Steps

1. Compute prefix sums $p[i]$. This allows constant-time subarray sum queries.
2. Precompute $cost[l][r]$ for all $1 \le l \le r \le n$. For each $l$, maintain a frequency map of prefix sums while extending $r$, and count how often $p[r] - p[i] = x$.
3. Initialize DP array with infinity, and set $dp[0][0] = 0$. This represents an empty prefix split into zero segments.
4. For each number of segments $j$ from 1 to $k$, compute all $dp[j][i]$ for $i \ge j$.
5. For each $i$, try all previous cut positions $t$ from $j-1$ to $i-1$, updating $dp[j][i]$ using the precomputed interval cost.
6. Return $dp[k][n]$.

### Why it works

The DP maintains the invariant that $dp[j][i]$ stores the optimal cost over all ways to partition the prefix $1..i$ into exactly $j$ contiguous segments. Every valid partition of $1..i$ into $j$ segments must end with some last segment $[t+1, i]$, and the previous part must be an optimal partition of $1..t$ into $j-1$ segments. Since segment costs are independent and fully captured by $cost[l][r]$, the recurrence explores all vali
