---
title: "CF 30C - Shooting Gallery"
description: "We are asked to help King Copa maximize his expected number of hits in a shooting gallery. The gallery is represented as"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 30
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 30 (Codeforces format)"
rating: 1800
weight: 30
solve_time_s: 60
verified: true
draft: false
---

[CF 30C - Shooting Gallery](https://codeforces.com/problemset/problem/30/C)

**Rating:** 1800  
**Tags:** dp, probabilities  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to help King Copa maximize his expected number of hits in a shooting gallery. The gallery is represented as a 2D plane, and each target appears at a specific point $(x_i, y_i)$ exactly at a specific time $t_i$ and disappears immediately afterward. If the king’s gun sight is aimed at the target when it appears, he hits it with probability $p_i$. The gun sight can move at unit speed, so to aim from one point $(x_1, y_1)$ to another $(x_2, y_2)$, it takes Euclidean distance $\sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}$ units of time. The king knows all targets and their timings in advance, and he wants to plan a sequence of moves to maximize the sum of probabilities of hitting the targets.

Input consists of $n$ targets ($1 \le n \le 1000$), each with coordinates, a time, and a probability. The output is the maximum expected number of hits.

The constraints give us some guidance. With $n$ up to 1000 and time up to $10^9$, a naive O($n^2$) solution is acceptable, but anything approaching O($2^n$) is far too slow. Distances can be negative, but we only care about Euclidean movement cost. Probabilities are real numbers between 0 and 1.

Non-obvious edge cases include: a single target at time 0 with probability less than 1, multiple targets clustered so close in time that moving between them is impossible, or targets with probability 0 which should be ignored. For example, with input:

```
1
0 0 0 0.5
```

The output is 0.5. A naive algorithm that assumes the king can only score whole hits (0 or 1) would fail here.

Another tricky scenario is when two targets are too far apart to reach in time:

```
2
0 0 1 1
1000 1000 2 1
```

Even though $t_2 > t_1$, the distance is so large that the king cannot reach the second target in time. A careless solution might attempt both and overcount.

## Approaches

The brute-force solution is to consider every permutation of targets, compute whether the king can move from one to the next in time, and sum the probabilities. This works for correctness, because it explores all sequences, but the number of permutations is $n!$, which is completely infeasible for $n=1000$.

The key insight is that hitting targets is independent in expectation, so we can model this as a form of dynamic programming. If we sort targets by increasing time, we only need to consider the best expected value we can achieve if we finish at each target. For target $i$, we can look at all previous targets $j$ that can reach $i$ in time $t_i - t_j \ge \text{distance}(i, j)$, and compute:

$$dp[i] = p_i + \max(dp[j] \text{ for all valid } j)$$

If no previous target can reach $i$, we can start from time 0 at any location, which simplifies to $dp[i] = p_i$. This reduces the problem from $O(n!)$ to $O(n^2)$, which is acceptable given $n \le 1000$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all permutations) | O(n!) | O(n) | Too slow |
| Dynamic Programming with time sorting | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all targets and store them as tuples $(x_i, y_i, t_i, p_i)$.
2. Sort the targets by appearance time $t_i$. This guarantees that any previous target we consider in DP is guaranteed to appear before the current one, so we only look backward.
3. Initialize a DP array `dp[i]` to store the maximum expected number of hits ending at target $i$.
4. Iterate over targets in order of increasing time. For each target $i$, assume initially `dp[i] = p_i`, representing starting directly at this target from the initial position at time 0.
5. For every earlier target $j < i$, check if the king can move from $j$ to $i$ in the available time. Compute the Euclidean distance $\text{dist} = \sqrt{(x_i - x_j)^2 + (y_i - y_j)^2}$. If $t_i - t_j \ge \text{dist}$, update `dp[i] = max(dp[i], dp[j] + p_i)`.
6. After processing all targets, the answer is the maximum value in the DP array, since the sequence can end at any target.

Why it works: The DP invariant is that `dp[i]` is the optimal expected number of hits achievable if the last target hit is $i$. Because expectation is additive, and we always consider feasible transitions from earlier targets, we guarantee that every sequence considered is valid, and we never miss a better sequence.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

n = int(input())
targets = []
for _ in range(n):
    x, y, t, p = input().split()
    x = int(x)
    y = int(y)
    t = int(t)
    p = float(p)
    targets.append((t, x, y, p))

targets.sort()  # sort by time

dp = [0.0] * n

for i in range(n):
    t_i, x_i, y_i, p_i = targets[i]
    dp[i] = p_i  # start directly at this target
    for j in range(i):
        t_j, x_j, y_j, _ = targets[j]
        dist = math.hypot(x_i - x_j, y_i - y_j)
        if t_i - t_j >= dist:
            dp[i] = max(dp[i], dp[j] + p_i)

print(f"{max(dp):.10f}")
```

The code reads and stores targets as tuples `(t, x, y, p)` so sorting by time is trivial. `math.hypot` is used for Euclidean distance to avoid manual squaring and square roots. DP initialization with `p_i` handles starting at the target from the origin or any initial position. Checking all `j < i` ensures we consider every valid previous position.

## Worked Examples

**Example 1:**

Input:

```
1
0 0 0 0.5
```

| i | t_i | x_i | y_i | p_i | dp[i] |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0.5 | 0.5 |

Output: `0.5`. Confirms that a single target produces `dp[i] = p_i`.

**Example 2:**

Input:

```
3
0 0 1 0.5
1 0 2 0.5
0 1 2 0.5
```

| i | t_i | x_i | y_i | p_i | dp[i] | transitions considered |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | 0.5 | 0.5 | start at 0 |
| 1 | 2 | 1 | 0 | 0.5 | 1.0 | from 0: dist=1 <=1 |
| 2 | 2 | 0 | 1 | 0.5 | 1.0 | from 0: dist=1 <=1 |

Output: `1.0`. Demonstrates multiple feasible transitions and DP correctly selects the optimal path.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | For each of n targets, we consider all previous targets, so n*(n-1)/2 comparisons |
| Space | O(n) | DP array stores a single float per target |

With n ≤ 1000, O(n^2) = 10^6 operations, which comfortably fits in the 2-second limit.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    targets = []
    for _ in range(n):
        x, y, t, p = input().split()
        x = int(x)
        y = int(y)
        t = int(t)
        p = float(p)
        targets.append((t, x, y, p))
    targets.sort()
    dp = [0.0] * n
    for i in range(n):
        t_i, x_i, y_i, p_i = targets[i]
        dp[i] = p_i
        for j in range(i):
            t_j, x_j, y_j, _ = targets[j]
            if
```
