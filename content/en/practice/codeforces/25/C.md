---
title: "CF 25C - Roads in Berland"
description: "We are given a fully connected network of cities in Berland. The input is a matrix that already encodes the shortest dis"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "graphs", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 25
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 25 (Div. 2 Only)"
rating: 1900
weight: 25
solve_time_s: 96
verified: false
draft: false
---

[CF 25C - Roads in Berland](https://codeforces.com/problemset/problem/25/C)

**Rating:** 1900  
**Tags:** graphs, shortest paths  
**Solve time:** 1m 36s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a fully connected network of cities in Berland. The input is a matrix that already encodes the shortest distances between each pair of cities, so we do not need to reconstruct the original roads. In addition, we have a list of proposed new roads, each with a specified length and endpoints. The task is to simulate adding these roads one by one and, after each addition, compute the sum of the shortest distances between all unordered pairs of cities.

The matrix size, `n`, can be up to 300, which is small enough that algorithms with time complexity `O(n^3)` are feasible, but anything quadratic in both `n` and the number of roads `k` could become tight. Each road addition potentially reduces distances, so the naive approach of recomputing all-pairs shortest paths from scratch for every new road would be wasteful. Instead, we need to incrementally update distances using the new road and propagate improvements efficiently.

A non-obvious edge case occurs when a new road connects two cities whose existing shortest path is already shorter than the road length. For instance, suppose the shortest distance between city 1 and city 2 is 3, and we plan to add a road of length 5. The sum of all shortest distances should remain unchanged after this addition. A careless implementation that blindly adds the road length to the sum would overcount.

Another subtle scenario arises when the new road creates indirect improvements. Suppose a new road connects city 1 and city 2 with a shorter distance than the current shortest path. This not only affects the direct pair but may also improve the distance between city 1 and every other city via city 2, or vice versa. This propagation must be applied to all city pairs, or the sum will be incorrect.

## Approaches

The brute-force solution would be to take the initial shortest distance matrix and, for each new road, reconstruct the graph by adding the road, then recompute all-pairs shortest paths using Floyd-Warshall. Each update is `O(n^3)`, and with `k` roads, the total time complexity is `O(k n^3)`. With `n` and `k` up to 300, this could reach 8.1 billion operations, which is far too slow for a 2-second time limit.

The key observation is that adding a single road affects shortest distances only if it provides a strictly shorter path between two cities, either directly or through one of its endpoints. We can iterate over all city pairs `(i, j)` and see if the path going through the new road `a-b` reduces the distance: `d[i][a] + c + d[b][j]` or `d[i][b] + c + d[a][j]`. If it does, we update `d[i][j]` and adjust the sum accordingly. Since the matrix is symmetric, we only need to update each unordered pair once, which ensures correctness. This approach is `O(k n^2)` and works within the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (recompute all-pairs each road) | O(k n^3) | O(n^2) | Too slow |
| Incremental Floyd-Warshall update | O(k n^2) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n` and the initial shortest distance matrix `d`. Initialize a variable `total_sum` to the sum of all unordered pairs of distances. Iterate only over `i < j` to avoid double-counting.
2. Read the number of new roads `k` and store each road as a tuple `(a, b, c)` in a list.
3. For each road `(a, b, c)`, subtract 1 from `a` and `b` to convert to zero-based indexing. Check if the direct distance `d[a][b]` is greater than `c`. If so, update `d[a][b] = d[b][a] = c` and propagate potential improvements.
4. Propagation: iterate over all cities `i` and `j`. Compute potential new distances using the new road: `d[i][j]` can be reduced to `min(d[i][j], d[i][a] + c + d[b][j], d[i][b] + c + d[a][j])`. If `d[i][j]` decreases, subtract the difference from `total_sum` to keep the sum consistent.
5. After processing all pairs for the current road, append `total_sum` to the output list.
6. Print the output as a space-separated string.

Why it works: the invariant maintained is that `d[i][j]` always stores the true shortest distance between cities `i` and `j` after adding each road. By considering paths through the new road endpoints, we guarantee that any possible improvement in distance is captured. Since updates are symmetric and only applied if they improve the distance, the sum remains correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
d = [list(map(int, input().split())) for _ in range(n)]

total_sum = 0
for i in range(n):
    for j in range(i + 1, n):
        total_sum += d[i][j]

k = int(input())
roads = [tuple(map(int, input().split())) for _ in range(k)]

res = []

for a, b, c in roads:
    a -= 1
    b -= 1
    if c < d[a][b]:
        d[a][b] = d[b][a] = c

    for i in range(n):
        for j in range(n):
            new_dist = min(d[i][j], d[i][a] + c + d[b][j], d[i][b] + c + d[a][j])
            if new_dist < d[i][j]:
                if i < j:
                    total_sum -= d[i][j] - new_dist
                d[i][j] = new_dist
                d[j][i] = new_dist

    res.append(str(total_sum))

print(" ".join(res))
```

Each section corresponds to a step in the algorithm. The initial sum computation handles unordered pairs only. The update loop carefully computes possible improvements through the new road. Symmetry is enforced by setting `d[j][i] = d[i][j]`. The `total_sum` is adjusted incrementally rather than recomputed from scratch.

## Worked Examples

**Sample 1:**

Input:

```
2
0 5
5 0
1
1 2 3
```

| Step | d matrix | total_sum |
| --- | --- | --- |
| Initial | [[0,5],[5,0]] | 5 |
| Add road 1-2 with c=3 | [[0,3],[3,0]] | 3 |

The new road directly improves the only pair, reducing the sum from 5 to 3.

**Custom Example 2:**

Input:

```
3
0 2 4
2 0 3
4 3 0
1
1 3 1
```

| Step | d matrix | total_sum |
| --- | --- | --- |
| Initial | [[0,2,4],[2,0,3],[4,3,0]] | 9 |
| Add road 1-3 with c=1 | [[0,2,1],[2,0,3],[1,3,0]] | 6 |

Adding the road reduces `1-3` from 4 to 1. Also, `2-3` via 1 reduces distance from 3 to 3 (no change), so total sum decreases to 6.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k n^2) | Each new road requires updating all n^2 distances through its endpoints. |
| Space | O(n^2) | Store the shortest distance matrix. |

With `n, k ≤ 300`, `k n^2` is about 27 million operations, which fits comfortably in 2 seconds. Memory usage is well below the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    # Paste the solution here
    n = int(input())
    d = [list(map(int, input().split())) for _ in range(n)]

    total_sum = 0
    for i in range(n):
        for j in range(i + 1, n):
            total_sum += d[i][j]

    k = int(input())
    roads = [tuple(map(int, input().split())) for _ in range(k)]

    res = []

    for a, b, c in roads:
        a -= 1
        b -= 1
        if c < d[a][b]:
            d[a][b] = d[b][a] = c

        for i in range(n):
            for j in range(n):
                new_dist = min(d[i][j], d[i][a] + c + d[b][j], d[i][b] + c + d[a][j])
                if new_dist < d[i][j]:
                    if i < j:
                        total_sum -= d[i][j] - new_dist
                    d[i][j] = new_dist
                    d[j][i] = new_dist

        res.append(str(total_sum))

    return " ".join(res)

# provided sample
assert run("2\n0 5\n5
```
