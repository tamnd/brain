---
title: "CF 104969F - Pizza Stack"
description: "We are given a set of pizzas labeled from 1 to n, where each label is also its radius. We must arrange all pizzas in a single vertical stack, which is equivalent to choosing a permutation of numbers from 1 to n."
date: "2026-06-28T18:26:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104969
codeforces_index: "F"
codeforces_contest_name: "UTPC Contest 02-09-24 Div. 1 (Advanced)"
rating: 0
weight: 104969
solve_time_s: 61
verified: true
draft: false
---

[CF 104969F - Pizza Stack](https://codeforces.com/problemset/problem/104969/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of pizzas labeled from 1 to n, where each label is also its radius. We must arrange all pizzas in a single vertical stack, which is equivalent to choosing a permutation of numbers from 1 to n.

For any two pizzas in the stack, consider the one that is physically lower and the one above it. If the lower pizza has a larger radius than the one above it, that pair contributes to what the problem calls a “proper pair”. In permutation language, this is exactly an inversion: a pair of indices i < j such that the value at i is greater than the value at j.

So the task becomes counting how many permutations of size n contain exactly k inversions.

The constraint n ≤ 1000 and k ≤ 1000 immediately suggests that we are not working in factorial or exponential space directly. A naive enumeration over all permutations would involve n! possibilities, which becomes impossible already around n = 12 or 13. Even n = 100 would be far beyond reach. This pushes us toward a dynamic programming approach where we count permutations by gradually inserting elements and tracking how many inversions are formed.

Edge cases are mostly structural rather than implementation bugs. When k = 0, only the increasing permutation works. When k is maximal, k = n(n − 1)/2, only the decreasing permutation works. Any solution must correctly handle these extremes without relying on assumptions like k < n or k being small relative to n, even though k ≤ 1000 caps the DP state space.

A subtle case is when n is large but k is small. For example, n = 1000 and k = 1 still requires reasoning about how a single inversion can be created by placing exactly one element out of order among many already fixed relative positions. This is where naive combinatorics tends to fail unless the DP structure is carefully defined.

## Approaches

A brute-force approach would generate all permutations of 1 to n and count inversions for each. Computing inversions per permutation takes O(n^2), and there are n! permutations, so the total work is O(n! · n^2), which becomes infeasible almost immediately.

We need a structure that builds permutations incrementally. The key observation is to think about inserting numbers one by one in increasing order of labels. Suppose we have already built a valid arrangement of numbers 1 to i − 1. When we insert number i, we can place it in any position among the existing i − 1 elements. If we insert it at position t from the left, it creates exactly i − 1 − t new inversions, because it will be placed before that many smaller elements.

This gives a clean recurrence: each insertion contributes a controllable number of new inversions depending only on its position. That independence is what enables dynamic programming.

We define dp[i][j] as the number of permutations of the first i numbers that have exactly j inversions. For each i, we try all possible insertion positions of i into a permutation of size i − 1, and accumulate inversion contributions.

A direct transition would try O(i) positions for each state, leading to O(n^3) total time. However, we can optimize using prefix sums over the previous dp row. This turns the inner transition into O(1), reducing the full solution to O(nk).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n^2) | O(n) | Too slow |
| DP with prefix sums | O(nk) | O(nk) | Accepted |

## Algorithm Walkthrough

We build a table dp where dp[i][j] counts permutations of {1..i} with exactly j inversions.

1. Initialize dp[1][0] = 1. A single element has exactly one permutation and zero inversions. This anchors the construction.
2. For each i from 2 to n, we compute dp[i] from dp[i − 1]. At this stage, we assume all counts for smaller sets are already correct.
3. For a fixed i, consider inserting element i into every possible position of a permutation of size i − 1. If we insert it at position p (0-indexed), it contributes (i − 1 − p) inversions.
4. Translate this into a recurrence: dp[i][j] equals the sum of dp[i − 1][j − t] over all t from 0 to i − 1, where t is the number of inversions introduced by inserting i. This is a sliding window sum over dp[i − 1].
5. Compute dp[i][j] efficiently using prefix sums of dp[i − 1]. For each j, we maintain a running window sum over the last i values of dp[i − 1].
6. Ensure we only consider j up to k, since larger values are irrelevant for the answer.

The key reason this works is that inserting the largest element i does not disturb relative order among 1..i − 1, so all inversion structure comes only from its placement. Every permutation of size i is uniquely formed by inserting i into exactly one position in a permutation of size i − 1, so the DP covers all states without overlap.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

n, k = map(int, input().split())

dp = [[0] * (k + 1) for _ in range(n + 1)]
dp[1][0] = 1

for i in range(2, n + 1):
    window_sum = 0
    for j in range(0, k + 1):
        window_sum += dp[i - 1][j]
        if j - i >= 0:
            window_sum -= dp[i - 1][j - i]
        dp[i][j] = window_sum % MOD

print(dp[n][k] % MOD)
```

The code builds the DP row by row. The `window_sum` maintains a sliding window of size i over the previous row, corresponding exactly to the i possible insertion positions of the current number i. Each dp[i][j] accumulates contributions from dp[i − 1][j], dp[i − 1][j − 1], ..., dp[i − 1][j − (i − 1)].

A common pitfall is forgetting that the window size grows with i. Another subtle issue is boundary handling when j − i becomes negative, which must not index into the array. The modulo is applied after each state update to prevent overflow.

## Worked Examples

### Example 1: n = 3, k = 0

We compute dp row by row.

| i | j | window_sum source | dp[i][j] |
| --- | --- | --- | --- |
| 1 | 0 | base | 1 |
| 2 | 0 | dp[1][0] | 1 |
| 2 | 1 | dp[1][0] (shift) | 1 |
| 3 | 0 | dp[2][0] | 1 |

For n = 3, only the increasing permutation 1 2 3 has zero inversions. Any swap introduces at least one inversion, so the answer is 1.

### Example 2: n = 3, k = 1

| i | j | contributions | dp[i][j] |
| --- | --- | --- | --- |
| 1 | 0 | base | 1 |
| 2 | 1 | insert 2 before 1 | 1 |
| 3 | 1 | from dp[2][1] + dp[2][0] | 2 |

For n = 3 and k = 1, the valid permutations are 1 3 2 and 2 1 3. Each corresponds to exactly one inversion formed by a single local swap.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nk) | Each dp row is computed with a single sliding window over k states |
| Space | O(nk) | Full DP table of size n × k |

With n, k ≤ 1000, the solution performs about 10^6 transitions, which is comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import comb

    MOD = 10**9 + 7

    n, k = map(int, inp.split())
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    dp[1][0] = 1

    for i in range(2, n + 1):
        window_sum = 0
        for j in range(k + 1):
            window_sum += dp[i - 1][j]
            if j - i >= 0:
                window_sum -= dp[i - 1][j - i]
            dp[i][j] = window_sum % MOD

    return str(dp[n][k] % MOD)

# provided samples
assert run("3 0") == "1"
assert run("3 1") == "2"

# custom cases
assert run("1 0") == "1"
assert run("4 0") == "1"
assert run("4 6") == "1"
assert run("5 1") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 | 1 | base case single element |
| 4 0 | 1 | only sorted permutation |
| 4 6 | 1 | fully reversed permutation |
| 5 1 | 4 | single inversion placements |

## Edge Cases

For n = 1 and k = 0, the DP initializes dp[1][0] = 1 and immediately returns it. There is no transition step, so no risk of accessing dp[0] or invalid indices.

For n = 4 and k = 0, the sliding window never accumulates any positive contribution beyond dp[i][0], since all higher inversion counts are irrelevant. The algorithm preserves dp[i][0] = 1 at every level because inserting the largest element at the end introduces zero inversions, and all other insertions are filtered out by the k bound.

For n = 4 and k = 6, which is the maximum inversion count for 4 elements, the DP correctly counts only the completely reversed permutation. The sliding window naturally accumulates exactly one valid construction path through successive forced placements at the beginning of each permutation.
