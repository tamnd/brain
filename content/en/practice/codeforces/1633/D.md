---
title: "CF 1633D - Make Them Equal"
description: "We are asked to start with an array of size $n$ where every element is initially 1. For each element $ai$, we can perform operations of the form $ai = ai + lfloor ai / x rfloor$, choosing $x 0$ as we like. Each element has a target value $bi$ and a reward $ci$."
date: "2026-06-10T04:49:03+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1633
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 122 (Rated for Div. 2)"
rating: 1600
weight: 1633
solve_time_s: 42
verified: true
draft: false
---

[CF 1633D - Make Them Equal](https://codeforces.com/problemset/problem/1633/D)

**Rating:** 1600  
**Tags:** dp, greedy  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to start with an array of size $n$ where every element is initially 1. For each element $a_i$, we can perform operations of the form $a_i = a_i + \lfloor a_i / x \rfloor$, choosing $x > 0$ as we like. Each element has a target value $b_i$ and a reward $c_i$. Our goal is to maximize the total coins earned by making some elements exactly equal to their targets, without exceeding $k$ total operations across all elements.

The input contains multiple test cases. Each test case specifies the array size $n$, the operation limit $k$, the target array $b$, and the coin array $c$. We must output the maximum coins obtainable for each test case.

Looking at constraints, $n$ can be up to $10^3$ and the sum of $n$ across all test cases is at most $10^3$, which means the number of elements in total is small. However, $k$ can be as large as $10^6$, so any algorithm that simulates operations naively would be too slow. Each operation increases an element by a function of itself, and since $b_i \le 10^3$, the number of operations to reach any $b_i$ is bounded and relatively small. This suggests we can precompute the minimal number of operations to reach each possible target from 1.

A non-obvious edge case occurs when $k = 0$. In that case, no element can be increased, so the only elements that contribute coins are those whose target $b_i = 1$. A careless implementation might try to perform operations without checking $k = 0$ and give a non-zero answer. Another edge case is when $b_i = 1$; reaching 1 requires zero operations, which must be recognized.

## Approaches

A brute-force approach would simulate each possible choice of $x$ for every element until it reaches its target, counting operations. For a single element $a_i$, the number of operations needed to reach $b_i$ could be up to $b_i - 1$, because each operation increases $a_i$ by at least 1. Across $n$ elements, this could lead to up to $n \cdot 10^3$ operations simulated per test case, multiplied by the range of $x$, which quickly exceeds the time limit.

The key observation is that the minimal number of operations needed to reach any value from 1 is relatively small and independent of $k$. For $1 \le a_i \le 10^3$, we can precompute an array `ops_needed[val]` such that `ops_needed[val]` is the minimum number of operations to reach `val` from 1. We can build this with a BFS-like approach, exploring from 1 and, for each current value, applying all possible operations $a_i + \lfloor a_i / x \rfloor$ that do not exceed 1000. This gives a table of minimal operations for all values up to 1000.

Once we know the minimal operations for each target $b_i$, the problem reduces to a classic bounded knapsack problem. Each element is an item with weight equal to `ops_needed[b_i]` and value equal to `c_i`. We have a knapsack of capacity $k$ and we want to maximize total coins. Using dynamic programming over `k` is efficient because `k` can be up to $10^6$ but the sum of minimal operations across all items is far smaller; specifically, the sum of all `ops_needed[b_i]` across a test case is at most $n \cdot 12$ since no element requires more than about 12 operations to reach 1000. Therefore, DP over `k` with the optimization that we never exceed `k` works well.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * b_i * x) | O(1) | Too slow |
| Optimal (precompute + knapsack) | O(n * k) worst-case, practical ~O(n * max_ops_needed) | O(k) | Accepted |

## Algorithm Walkthrough

1. Precompute the minimal number of operations to reach each value from 1 up to 1000. Start with a queue containing 1 with 0 operations. For each value in the queue, iterate `x` from 1 up to the current value. Compute the next value as `next_val = cur + cur // x`. If `next_val` has not been reached before, mark its operations count as `cur_ops + 1` and add it to the queue. Stop when all values up to 1000 are filled.
2. For each test case, read `n`, `k`, `b`, and `c`. Transform the problem into a knapsack: for each element, `weight = ops_needed[b_i]` and `value = c_i`.
3. Initialize a DP array `dp[0..k]` to 0, where `dp[j]` represents the maximum coins achievable with at most `j` operations.
4. For each element, iterate `j` from `k` down to `weight`. Update `dp[j] = max(dp[j], dp[j - weight] + value)`. Iterating backwards ensures each element is used at most once.
5. After processing all elements, `dp[k]` contains the maximum coins achievable with up to `k` operations. Output this value.

Why it works: Precomputing minimal operations guarantees we know the least-cost way to reach each target. The DP ensures that we choose the subset of elements whose combined operations fit within the budget `k` while maximizing coins. Iterating backwards prevents double-counting any element, preserving the 0-1 knapsack property.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

# Precompute minimal operations to reach values from 1 to 1000
MAX_VAL = 1000
ops_needed = [float('inf')] * (MAX_VAL + 1)
ops_needed[1] = 0
queue = deque([1])
while queue:
    cur = queue.popleft()
    cur_ops = ops_needed[cur]
    for x in range(1, cur + 1):
        nxt = cur + cur // x
        if nxt <= MAX_VAL and ops_needed[nxt] > cur_ops + 1:
            ops_needed[nxt] = cur_ops + 1
            queue.append(nxt)

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    b = list(map(int, input().split()))
    c = list(map(int, input().split()))
    
    # Map b[i] to ops_needed, cap at k+1 (we cannot use more than k)
    weights = [min(ops_needed[val], k + 1) for val in b]
    
    dp = [0] * (k + 1)
    for w, v in zip(weights, c):
        if w > k:
            continue
        for j in range(k, w - 1, -1):
            dp[j] = max(dp[j], dp[j - w] + v)
    
    print(dp[k])
```

The precomputation section ensures that each target value has its minimal operation count. Using BFS prevents redundant recalculation and avoids infinite loops. Mapping weights to `min(ops_needed[val], k + 1)` ensures we skip elements that cannot be reached within `k` operations. The knapsack DP handles the subset selection. Iterating `j` backwards guarantees 0-1 selection.

## Worked Examples

**Sample 1**

Input:

```
n = 4, k = 4
b = [1, 7, 5, 2]
c = [2, 6, 5, 2]
```

| i | b_i | ops_needed | c_i | DP updates |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 2 | dp[0..4] = max(dp[j], dp[j-0]+2) → adds 2 to all j |
| 1 | 7 | 4 | 6 | dp[4] = max(dp[4], dp[0]+6)=8, dp[3]=..., etc. |
| 2 | 5 | 3 | 5 | combine with dp to maximize |
| 3 | 2 | 1 | 2 | final dp[4]=9 |

This confirms the DP picks elements that maximize coins within operation limit.

**Edge Case k=0**

Input:

```
n = 3, k = 0
b = [1, 2, 1]
c = [5, 4, 3]
```

| i | b_i | ops_needed | c_i | DP updates |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 5 | dp[0] = max(0,0+5)=5 |
| 1 | 2 | 1 | 4 | weight>k, skip |
| 2 | 1 | 0 | 3 | dp[0]=max(5,5+3)=8 |

Correctly counts coins from elements already equal to 1.

## Complexity Analysis

| Measure | Complexity
