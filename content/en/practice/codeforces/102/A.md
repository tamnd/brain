---
title: "CF 102A - Clothes"
description: "We are asked to find the cheapest way for Gerald to buy three pieces of clothing that all match each other. Each clothing item has a price, and some pairs of items are marked as matching. The input gives us the total number of items, the prices, and a list of matching pairs."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 102
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 79 (Div. 2 Only)"
rating: 1200
weight: 102
solve_time_s: 102
verified: true
draft: false
---

[CF 102A - Clothes](https://codeforces.com/problemset/problem/102/A)

**Rating:** 1200  
**Tags:** brute force  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to find the cheapest way for Gerald to buy three pieces of clothing that all match each other. Each clothing item has a price, and some pairs of items are marked as matching. The input gives us the total number of items, the prices, and a list of matching pairs. Our output should be the minimal sum of three items that form a fully connected matching triple, or -1 if no such triple exists.

The problem can be naturally interpreted as a graph problem. Each clothing item is a node, and each matching pair is an undirected edge. Gerald wants to find a triangle in this graph, and among all triangles, he wants the one with the smallest sum of node weights (prices).

Given the constraints, `n` can go up to 100, and `m` up to n(n-1)/2, meaning the graph could be dense. With `n` this small, a solution that checks all triples of nodes is feasible. However, we must be careful to efficiently check whether a triple forms a triangle without redundant computation.

A subtle edge case is when there are exactly three items but not all of them match. For example, `n=3` and only two edges exist: we cannot form a valid triple, and the answer must be -1. Another edge case occurs when multiple triples exist, but one includes a very expensive item; we must find the triple with the minimal sum, not just any triangle.

## Approaches

The naive approach is brute force: consider every combination of three items and check if all three pairs exist in the matching list. This is correct, but it involves checking `O(n^3)` triples, and for each triple, verifying existence of three edges. With `n=100`, `n^3` is 1,000,000, which is acceptable given the 2-second limit.

A slightly more efficient approach is to store adjacency information in a set for each node. Then, for a candidate triple `(i, j, k)`, we can verify in constant time whether edges `(i, j)`, `(i, k)`, and `(j, k)` exist. This reduces the overhead from repeated searching in the original list of edges.

The key observation is that this problem is small enough to tolerate O(n^3) iteration, so no complex graph algorithms are needed. Using adjacency sets simplifies edge checking, and iterating i<j<k ensures we do not consider the same triple multiple times.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force triple check with adjacency list | O(n^3) | O(n^2) | Accepted |
| Brute Force triple check with adjacency sets | O(n^3) | O(n^2) | Accepted and simpler |

## Algorithm Walkthrough

1. Read the number of items `n` and the number of matching pairs `m`. Read the list of prices for each item.
2. Construct an adjacency set for each node, storing which items it matches with. This allows O(1) edge checks.
3. Initialize a variable `min_sum` to a very large number, which will track the minimal sum of a valid triple.
4. Iterate over all triples `(i, j, k)` such that `0 <= i < j < k < n`. This ensures no triple is repeated and all combinations are considered.
5. For each triple, check if all three edges exist in the adjacency sets: `i-j`, `i-k`, `j-k`. If they do, compute the sum of their prices.
6. If this sum is less than `min_sum`, update `min_sum`.
7. After checking all triples, if `min_sum` was updated, print it. Otherwise, print -1 to indicate no valid triple exists.

Why it works: The algorithm systematically considers every possible triple and only accepts triples that form a triangle in the matching graph. By keeping the minimal sum, we ensure the result is the cheapest combination. The adjacency sets guarantee fast edge lookups, so every valid triple is correctly identified without redundant computation.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
prices = list(map(int, input().split()))

# adjacency sets for fast edge lookup
adj = [set() for _ in range(n)]
for _ in range(m):
    u, v = map(int, input().split())
    u -= 1
    v -= 1
    adj[u].add(v)
    adj[v].add(u)

min_sum = float('inf')
for i in range(n):
    for j in range(i+1, n):
        if j not in adj[i]:
            continue
        for k in range(j+1, n):
            if k in adj[i] and k in adj[j]:
                total = prices[i] + prices[j] + prices[k]
                if total < min_sum:
                    min_sum = total

print(min_sum if min_sum != float('inf') else -1)
```

The solution first reads the prices and edges, storing adjacency information in sets. The triple iteration ensures no duplicate combinations and checks existence of all three edges in constant time. Using `float('inf')` as initial `min_sum` ensures we can detect the absence of any valid triple cleanly.

## Worked Examples

Sample 1:

| i | j | k | Edges exist? | Prices sum | min_sum |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 2 | yes | 1+2+3=6 | 6 |

Here all three edges exist, so the only valid triple is used, resulting in output 6.

Sample 2 (no triple):

Input:

```
3 2
10 20 30
1 2
2 3
```

| i | j | k | Edges exist? | Prices sum | min_sum |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 2 | missing edge 0-2 | - | inf |

No valid triple exists, so output is -1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^3) | Iterate over all triples and check edges in O(1) using adjacency sets |
| Space | O(n^2) | Adjacency sets store up to n(n-1)/2 edges |

Given `n <= 100`, `n^3` is around 1,000,000 iterations, which runs comfortably within 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    prices = list(map(int, input().split()))
    adj = [set() for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        adj[u].add(v)
        adj[v].add(u)
    min_sum = float('inf')
    for i in range(n):
        for j in range(i+1, n):
            if j not in adj[i]:
                continue
            for k in range(j+1, n):
                if k in adj[i] and k in adj[j]:
                    total = prices[i] + prices[j] + prices[k]
                    if total < min_sum:
                        min_sum = total
    return str(min_sum if min_sum != float('inf') else -1)

# provided samples
assert run("3 3\n1 2 3\n1 2\n2 3\n3 1\n") == "6"
assert run("3 2\n10 20 30\n1 2\n2 3\n") == "-1"

# custom cases
assert run("4 6\n1 2 3 4\n1 2\n1 3\n1 4\n2 3\n2 4\n3 4\n") == "6" # all items form multiple triangles
assert run("3 0\n1 2 3\n") == "-1" # no edges
assert run("5 3\n5 4 3 2 1\n1 2\n2 3\n3 4\n") == "-1" # not enough connected triple
assert run("3 3\n1000000 1000000 1000000\n1 2\n2 3\n1 3\n") == "3000000" # max prices
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 6 with all edges | 6 | Finds minimal triangle in fully connected graph |
| 3 0 | -1 | Handles no edges at all |
| 5 3 | -1 | Handles graph with no valid triple despite some edges |
| 3 3 max prices | 3000000 | Correctly sums large prices |

## Edge Cases

If there are exactly three items but one pair does not match, like input `3 2\n10 20 30\n1 2\n2 3\n`, the algorithm checks the triple `(0,1,2)`, sees that edge `0-2` is missing, and `min_sum` remains `inf`. It correctly prints -1.

If all items are fully connected, the triple `(i,j,k)` iteration finds multiple candidates but always updates `min_sum` to the smallest sum. For input `4 6\n1 2 3 4\n1 2\n1 3\n1 4\n2
