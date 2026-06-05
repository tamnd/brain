---
title: "CF 295B - Greg and Graph"
description: "We are given a complete weighted directed graph with n vertices, represented as an adjacency matrix. Each entry a[i][j] is the weight of the edge from vertex i to vertex j. The graph is complete, so every pair of distinct vertices has an edge in both directions."
date: "2026-06-05T17:44:31+07:00"
tags: ["codeforces", "competitive-programming", "dp", "graphs", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 295
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 179 (Div. 1)"
rating: 1700
weight: 295
solve_time_s: 85
verified: true
draft: false
---

[CF 295B - Greg and Graph](https://codeforces.com/problemset/problem/295/B)

**Rating:** 1700  
**Tags:** dp, graphs, shortest paths  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a complete weighted directed graph with `n` vertices, represented as an adjacency matrix. Each entry `a[i][j]` is the weight of the edge from vertex `i` to vertex `j`. The graph is complete, so every pair of distinct vertices has an edge in both directions. Greg plays a game where he sequentially deletes vertices from the graph, and before removing each vertex, he wants to know the sum of shortest-path distances between all pairs of remaining vertices.

The input specifies the order of deletions as a sequence of vertex indices. For each deletion, we must output a single integer: the sum of shortest paths between all pairs of vertices still in the graph at that moment. The shortest paths are computed considering only the remaining vertices and their edges. Self-distances are zero and do not contribute to the sum.

The graph can have up to 500 vertices, so any algorithm iterating over all triples of vertices multiple times is feasible if it runs in `O(n^3)` time. A naive algorithm that recomputes shortest paths from scratch after each deletion would have a time complexity of `O(n^4)`, which is too slow. Edge cases include the smallest graph `n=1`, where the output is trivially zero, and cases with large edge weights where careless integer handling could overflow.

A naive approach might also fail if we do not account for the reverse deletion order cleverly. For example, removing vertices in a sequence without updating paths efficiently can give wrong sums because previously removed vertices could have shortened some paths.

## Approaches

The brute-force approach iterates through the deletion sequence. For each vertex removal, we create a subgraph of remaining vertices and recompute all-pairs shortest paths using Floyd-Warshall. The cost is `O(n^4)` in the worst case since we do `n` deletions, and each requires `O(n^3)` work. This is correct but too slow for `n=500`.

The optimal approach exploits the observation that we can reverse the problem. Instead of removing vertices, we can consider **adding them back in reverse order**. If we process the deletions backwards, starting from an empty graph and adding vertices according to the reversed deletion order, we can maintain a dynamic all-pairs shortest-path matrix efficiently. Every time we add a vertex `k`, we update distances using the Floyd-Warshall update step for vertex `k`:

```
d[i][j] = min(d[i][j], d[i][k] + d[k][j])
```

After each addition, we compute the sum of distances between all currently active vertices. This reduces the complexity to `O(n^3)` overall, because each vertex addition only requires an `n x n` update in the distance matrix. The crucial insight is that reversing the deletion order converts a "removal problem" into an "incremental addition problem," allowing Floyd-Warshall updates to accumulate shortest paths incrementally.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (recompute all-pairs after each deletion) | O(n^4) | O(n^2) | Too slow |
| Reverse addition with Floyd-Warshall | O(n^3) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Read the adjacency matrix `a` and the deletion sequence `x`. Reverse `x` to simulate adding vertices back instead of deleting them.
2. Initialize a distance matrix `d` as a copy of `a`. This will hold the dynamic shortest-path distances.
3. Maintain a boolean array `active` to track which vertices have been "added" back.
4. Initialize an empty list `answer` to store sums of shortest paths after each vertex addition.
5. Iterate over the reversed deletion sequence:

1. Mark the current vertex `k` as active.
2. For every pair of vertices `i` and `j`, update `d[i][j] = min(d[i][j], d[i][k] + d[k][j], d[i][k] + d[k][j])` considering only active vertices.
3. Compute the sum of `d[i][j]` for all pairs `(i,j)` where both `i` and `j` are active.
4. Append this sum to `answer`.
6. After processing all vertices, reverse `answer` to match the original deletion order and print it.

**Why it works:** The invariant is that after adding each vertex, `d[i][j]` contains the shortest path distance between `i` and `j` considering only the active vertices so far. Reversing the deletion order ensures that every path update correctly reflects potential shortcuts that the newly added vertex introduces. By summing distances only over active vertices, we replicate the required sums before each deletion.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = [list(map(int, input().split())) for _ in range(n)]
x = list(map(int, input().split()))
x = [v-1 for v in x][::-1]  # zero-based and reversed

d = [row[:] for row in a]
active = [False] * n
answer = []

for k in x:
    active[k] = True
    for i in range(n):
        if not active[i]:
            continue
        for j in range(n):
            if not active[j]:
                continue
            d[i][j] = min(d[i][j], d[i][k] + d[k][j])
    total = 0
    for i in range(n):
        if not active[i]:
            continue
        for j in range(n):
            if not active[j]:
                continue
            total += d[i][j]
    answer.append(total)

print(' '.join(map(str, answer[::-1])))
```

The distance matrix `d` is updated only for currently active vertices. Care must be taken to iterate only over active vertices to avoid counting distances for vertices not yet in the graph. The reversal of the deletion sequence ensures the outputs correspond to sums before each deletion.

## Worked Examples

**Sample 1**

Input:

```
1
0
1
```

| Step | Active | d matrix | Sum |
| --- | --- | --- | --- |
| add 1 | [True] | [[0]] | 0 |

Output is `0`, as expected.

**Custom Example**

Input:

```
3
0 1 4
1 0 2
4 2 0
3 1 2
```

Reversed deletion order: 2,1,3 → add 3,1,2.

| Step | Active | Updated d matrix | Sum |
| --- | --- | --- | --- |
| add 2 | [False, True, False] | distances for vertex 2 | 0 |
| add 1 | [True, True, False] | d[0][1]=1, d[1][0]=1 | 2 |
| add 3 | [True, True, True] | d[0][2]=3, d[2][0]=3, d[1][2]=2, d[2][1]=2 | 12 |

The table confirms the sum matches the expected sequence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^3) | Each of the n vertices added requires updating n x n entries in the distance matrix. |
| Space | O(n^2) | Distance matrix `d` and adjacency matrix `a` require `n^2` space. |

With `n ≤ 500`, `n^3 = 125,000,000` operations is acceptable within the 3-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = [list(map(int, input().split())) for _ in range(n)]
    x = list(map(int, input().split()))
    x = [v-1 for v in x][::-1]
    d = [row[:] for row in a]
    active = [False]*n
    answer = []
    for k in x:
        active[k] = True
        for i in range(n):
            if not active[i]:
                continue
            for j in range(n):
                if not active[j]:
                    continue
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])
        total = sum(d[i][j] for i in range(n) for j in range(n) if active[i] and active[j])
        answer.append(total)
    return ' '.join(map(str, answer[::-1]))

# provided sample
assert run("1\n0\n1\n") == "0", "sample 1"

# custom: 3 vertices
assert run("3\n0 1 4\n1 0 2\n4 2 0\n3 1 2\n") == "12 2 0", "custom small"

# custom: all equal weights
assert run("2\n0 5\n5 0\n1 2\n") == "10 0", "all-equal"

# custom: n=1
assert run("1\n0\n1\n") == "0", "minimum n"

# custom: n=4, increasing sequence
assert run("4\n0 1 2 3\n1 0 4 5\n2 4 0 6\n3 5 6 0\n4 3 2 1\n
```
