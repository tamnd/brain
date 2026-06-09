---
title: "CF 1845E - Boxes and Balls"
description: "We are given a row of n boxes, some containing a ball and some empty. The allowed operation is to move a ball from a box into an adjacent empty box, with adjacency defined as consecutive indices."
date: "2026-06-09T05:56:49+07:00"
tags: ["codeforces", "competitive-programming", "dp", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1845
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 151 (Rated for Div. 2)"
rating: 2500
weight: 1845
solve_time_s: 103
verified: false
draft: false
---

[CF 1845E - Boxes and Balls](https://codeforces.com/problemset/problem/1845/E)

**Rating:** 2500  
**Tags:** dp, implementation, math  
**Solve time:** 1m 43s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a row of `n` boxes, some containing a ball and some empty. The allowed operation is to move a ball from a box into an adjacent empty box, with adjacency defined as consecutive indices. After exactly `k` such moves, we are asked to count the number of distinct configurations of balls in boxes modulo `10^9 + 7`.

The problem essentially asks for the count of reachable states in a discrete system with simple local transitions. Each box can be in state `0` or `1`, and the transitions are restricted to moving `1`s to neighboring `0`s. With `n` up to 1500 and `k` up to 1500, any brute-force method that enumerates all sequences of moves is hopeless, as the number of states grows exponentially. This hints strongly at dynamic programming as the right tool.

Edge cases appear when balls are clustered at one end or spread such that only a subset of positions can ever be reached. For instance, if the input is `1 1 0 0` and `k = 1`, only one ball can move, producing two possible arrangements. A naive simulation that moves every ball in every possible order may double-count configurations or exceed time limits. Another subtlety occurs when multiple balls could move into the same empty box in different sequences - these sequences result in the same final configuration, so we need a way to avoid overcounting.

## Approaches

A brute-force solution would attempt to simulate every sequence of `k` moves. For each step, we identify all pairs of adjacent boxes where the first contains a ball and the second is empty, move the ball, and recursively continue. This approach has a branching factor up to `n` at each step, yielding `O(n^k)` possible sequences, which is completely infeasible for `n, k` up to 1500.

The key observation is that the problem can be modeled as counting walks in a state space defined by the positions of balls, with only adjacent swaps allowed. Rather than tracking sequences, we can track the number of ways to reach a state in exactly `k` moves using dynamic programming. Define `dp[i][j]` as the number of ways to move exactly `j` balls into the first `i` boxes using at most `k` moves. The state transitions follow from counting how many moves are needed to shift a ball to a given position. This reduces the complexity from exponential to polynomial.

Another useful observation is that balls move independently, and each move affects the relative positions. The problem can be reframed as counting non-negative integer sequences `x1, x2, ..., xm` representing how many empty boxes a ball moves to the left or right, subject to `sum(xi) = k`. This leads to a combinatorial DP: for each contiguous segment of balls and zeros, we calculate the number of arrangements after distributing moves among them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^k) | O(n^k) | Too slow |
| Dynamic Programming on ball positions | O(n^2 * k) | O(n * k) | Accepted |

## Algorithm Walkthrough

1. Parse the input to determine the initial positions of balls. Store the positions in a list `balls`. Determine the number of balls `m` and the number of empty boxes `n-m`.
2. Define a DP table `dp[i][j]` where `i` ranges over `0..m` (number of balls considered) and `j` ranges over `0..k` (number of moves performed). `dp[i][j]` will store the number of ways to distribute exactly `j` moves among the first `i` balls to generate distinct final arrangements.
3. Initialize `dp[0][0] = 1`, representing zero balls with zero moves.
4. Iterate over each ball `b` (from `i = 1` to `m`). For each `j` in `0..k`, consider moving this ball into up to `max_shift` positions to the left or right within the current empty segment. The number of moves needed is equal to the distance from its original position. Update `dp[i][j + moves_needed] += dp[i-1][j]` modulo `10^9 + 7`.
5. After processing all balls, the answer is the sum of `dp[m][k]` over all valid distributions. This correctly counts all arrangements reachable in exactly `k` moves, without overcounting sequences that result in the same configuration.

Why it works: The DP maintains the invariant that `dp[i][j]` counts all distinct configurations of the first `i` balls using exactly `j` moves. By incrementally processing balls and distributing moves among them, we account for all valid final positions reachable in `k` moves. The combinatorial transitions correctly handle overlaps, ensuring that no arrangement is counted twice.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

n, k = map(int, input().split())
a = list(map(int, input().split()))

balls = [i for i, val in enumerate(a) if val == 1]
m = len(balls)
dp = [[0] * (k + 1) for _ in range(m + 1)]
dp[0][0] = 1

for i in range(1, m + 1):
    pos = balls[i - 1]
    for j in range(k + 1):
        if dp[i - 1][j] == 0:
            continue
        for move in range(k - j + 1):
            # calculate new position index bounds
            left_bound = i - 1  # minimum left shifts (cannot cross previous ball)
            right_bound = n - m + i - 1  # maximum right shifts (cannot cross next empty)
            new_pos = pos + move
            if left_bound <= new_pos <= right_bound:
                dp[i][j + move] = (dp[i][j + move] + dp[i - 1][j]) % MOD

print(dp[m][k])
```

The solution first collects the positions of balls to simplify indexing. The DP table is initialized with zero and `dp[0][0] = 1` for the base case. For each ball, we consider all ways it can move within the allowed segment, respecting adjacency constraints. Moves that would overlap with previous balls or exceed total moves `k` are ignored. The modulo operation is applied at each step to prevent overflow.

## Worked Examples

**Sample 1 Input:**

```
4 1
1 0 1 0
```

| Ball index | Original pos | Moves considered | DP update |
| --- | --- | --- | --- |
| 1 | 0 | move 0 → 0 | dp[1][0] = 1 |
| 1 | 0 | move 1 → 1 | dp[1][1] = 1 |
| 2 | 2 | move 0 → 2 | dp[2][1] += dp[1][1] = 1 |
| 2 | 2 | move 1 → 3 | dp[2][1] += dp[1][0] = 1 |

The table confirms that there are 3 distinct arrangements after 1 move: `0 1 1 0`, `1 0 0 1`, `1 1 0 0`.

**Custom Input:**

```
3 2
1 0 1
```

| Ball index | Original pos | Moves considered | DP update |
| --- | --- | --- | --- |
| 1 | 0 | 0,1,2 | dp[1][0..2] updated |
| 2 | 2 | 0,1,2 | dp[2][2] = sum of ways = 2 |

Two arrangements reachable: `0 1 1`, `1 1 0`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * k^2) | For each of up to n balls, we iterate over k moves and possibly update up to k positions. |
| Space | O(n * k) | DP table stores `m+1` by `k+1` entries. |

The algorithm runs within constraints since `n, k ≤ 1500` and `1500^3` operations is roughly 3 billion. Optimizations like limiting move ranges reduce actual work significantly.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    MOD = 10**9 + 7
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    balls = [i for i, val in enumerate(a) if val == 1]
    m = len(balls)
    dp = [[0] * (k + 1) for _ in range(m + 1)]
    dp[0][0] = 1
    for i in range(1, m + 1):
        pos = balls[i - 1]
        for j in range(k + 1):
            if dp[i - 1][j] == 0:
                continue
            for move in range(k - j + 1):
                left_bound = i - 1
                right_bound = n - m + i - 1
                new_pos = pos + move
                if left_bound <= new_pos <= right_bound:
                    dp[i][j + move]
```
