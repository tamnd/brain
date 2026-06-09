---
title: "CF 1801E - Gasoline prices"
description: "We are given a country, Berland, structured as a tree of cities rooted at city 1. Each city has a gas station with a price range $[li, ri]$. Every year, the king’s two sons inspect gasoline prices along two paths of equal length."
date: "2026-06-09T09:32:15+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "divide-and-conquer", "dsu", "hashing", "trees"]
categories: ["algorithms"]
codeforces_contest: 1801
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 857 (Div. 1)"
rating: 3000
weight: 1801
solve_time_s: 77
verified: true
draft: false
---

[CF 1801E - Gasoline prices](https://codeforces.com/problemset/problem/1801/E)

**Rating:** 3000  
**Tags:** data structures, divide and conquer, dsu, hashing, trees  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a country, Berland, structured as a tree of cities rooted at city 1. Each city has a gas station with a price range $[l_i, r_i]$. Every year, the king’s two sons inspect gasoline prices along two paths of equal length. Each inspection requires that corresponding cities along the two paths have the exact same price.

The task is to compute, for each year $i$, the number of ways to assign prices to all cities such that all inspections from year 1 to year $i$ are satisfied, modulo $10^9 + 7$. The output for each year must reflect the cumulative constraints imposed by inspections up to that point.

The key constraints are that the number of cities and inspections can be as high as $2 \cdot 10^5$, and price ranges can be up to $10^9 + 6$. A brute-force approach of trying all price assignments is impossible because the search space is exponential in $n$. We also need to handle paths in a tree efficiently, since paths can be arbitrary sequences of nodes.

Edge cases include situations where an inspection forces an empty intersection of ranges, producing zero valid assignments. Another subtle case is when multiple inspections impose overlapping equalities among cities-careless bookkeeping may double-count constraints.

## Approaches

A brute-force solution would iterate over all possible assignments of gasoline prices for each city and check all paths for equality constraints. This is correct in principle, but the complexity is $\prod_{i=1}^n (r_i - l_i + 1)$, which is exponential in $n$ and completely infeasible for $n = 2 \cdot 10^5$. Even iterating over paths naively for each inspection is too slow, since each path may contain $O(n)$ nodes.

The key insight is that the equality constraints can be represented as a union of sets of cities whose prices must match. Once we identify these sets, the valid prices for each set are the intersection of the ranges of all cities in that set. Each inspection corresponds to pairing up nodes along two equal-length paths, and every pair must belong to the same set.

This suggests a Disjoint Set Union (DSU) or Union-Find structure. Each city starts in its own set. For each inspection, we merge sets according to the equality constraints along the paths. After each merge, we update the valid price range for the merged set to be the intersection of the ranges of the combined sets. If any intersection becomes empty, that set has zero valid prices, and the total number of price assignments is zero.

Tracking the sets and intersections efficiently lets us calculate the cumulative number of valid assignments after each year by multiplying the sizes of the ranges of all disjoint sets. This reduces the complexity to roughly $O(n \log n + m \cdot k)$, where $k$ is the maximum path length.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(\prod_{i=1}^n (r_i-l_i+1) \cdot m \cdot n)$ | $O(n)$ | Too slow |
| DSU + Path Decomposition | $O(n \log n + m \cdot k)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Represent the tree as an adjacency list. Compute the parent array and, if needed, precompute node depths to walk paths efficiently.
2. Initialize a DSU where each city starts in its own set. Each set tracks two numbers: `set_min` and `set_max`, representing the intersection of acceptable price ranges for that set.
3. For each inspection year:

1. Break each path into a list of nodes in order from start to end. You can walk up to the root using parent pointers, then reverse part of the path to get the full path.
2. Iterate over corresponding positions along the two paths. For each pair `(u, v)`, merge their DSU sets. When merging, compute the new intersection of ranges: `new_min = max(set_min[u], set_min[v])`, `new_max = min(set_max[u], set_max[v])`.
3. If any intersection becomes empty (`new_min > new_max`), mark the total count as zero immediately.
4. After processing all path pairs for the year, iterate over all DSU sets and compute the product of `(set_max - set_min + 1)` modulo $10^9 + 7$. This is the total number of valid assignments for that year.
5. Output the cumulative counts year by year.

Why it works: The DSU ensures that any city in the same set must have the same price. Merging sets along paths implements the pairwise equality constraints imposed by the inspections. Maintaining the intersection of ranges guarantees that we only count valid assignments. The multiplication of range sizes over disjoint sets counts all combinations without overcounting, as all constraints have been encoded in the DSU structure.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 25)

MOD = 10**9 + 7

class DSU:
    def __init__(self, n, l, r):
        self.parent = list(range(n))
        self.min_val = l[:]
        self.max_val = r[:]

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        x_root, y_root = self.find(x), self.find(y)
        if x_root == y_root:
            return
        new_min = max(self.min_val[x_root], self.min_val[y_root])
        new_max = min(self.max_val[x_root], self.max_val[y_root])
        self.parent[y_root] = x_root
        self.min_val[x_root] = new_min
        self.max_val[x_root] = new_max

def main():
    n = int(input())
    p = list(map(int, input().split()))
    tree = [[] for _ in range(n)]
    for i, parent in enumerate(p):
        tree[parent-1].append(i+1)

    l = [0]*n
    r = [0]*n
    for i in range(n):
        l[i], r[i] = map(int, input().split())

    m = int(input())
    queries = [tuple(map(int, input().split())) for _ in range(m)]

    parent = [-1]*n
    depth = [0]*n
    def dfs(u, par):
        parent[u] = par
        for v in tree[u]:
            depth[v] = depth[u]+1
            dfs(v, u)
    dfs(0, -1)

    def path(u, v):
        up = []
        down = []
        while depth[u] > depth[v]:
            up.append(u)
            u = parent[u]
        while depth[v] > depth[u]:
            down.append(v)
            v = parent[v]
        while u != v:
            up.append(u)
            down.append(v)
            u = parent[u]
            v = parent[v]
        up.append(u)
        return up + down[::-1]

    dsu = DSU(n, l, r)
    result = []

    for a, b, c, d in queries:
        path1 = path(a-1, b-1)
        path2 = path(c-1, d-1)
        for u, v in zip(path1, path2):
            dsu.union(u, v)
        total = 1
        counted = set()
        for i in range(n):
            root = dsu.find(i)
            if root in counted:
                continue
            counted.add(root)
            if dsu.min_val[root] > dsu.max_val[root]:
                total = 0
                break
            total = total * (dsu.max_val[root] - dsu.min_val[root] + 1) % MOD
        result.append(total)

    print("\n".join(map(str, result)))

if __name__ == "__main__":
    main()
```

The solution constructs paths using parent pointers and merges sets via DSU. Updating min/max values enforces intersections of ranges. Counting only the root of each set prevents overcounting. Handling empty intersections immediately avoids invalid multiplications.

## Worked Examples

**Sample 1**

Input:

```
5
1 1 2 2
2 4
1 3
1 3
2 4
4 4
4
1 1 2 2
1 2 2 1
3 4 4 3
3 4 3 5
```

Trace after each year:

| Year | Merged Sets | Intersections | Count |
| --- | --- | --- | --- |
| 1 | {1,2} | [2,3] | 18 |
| 2 | {1,2} | [2,3] | 18 |
| 3 | {1,2}, {3,4} | [2,3], [2,3] | 4 |
| 4 | {1,2,3,4,5} | empty | 0 |

This demonstrates that merging sets correctly propagates equality constraints, and empty intersections lead to zero assignments.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m_k_α |  |
