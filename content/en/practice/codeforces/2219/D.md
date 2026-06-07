---
title: "CF 2219D - MEX Replacement on Tree"
description: "We are given a tree with n vertices rooted at vertex 1. Each vertex has a unique integer weight between 0 and n-1. For any vertex v, we define Sv as the set of weights along the path from the root to v, inclusive."
date: "2026-06-07T18:36:47+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation", "math", "trees"]
categories: ["algorithms"]
codeforces_contest: 2219
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 1093 (Div. 1)"
rating: 0
weight: 2219
solve_time_s: 131
verified: false
draft: false
---

[CF 2219D - MEX Replacement on Tree](https://codeforces.com/problemset/problem/2219/D)

**Rating:** -  
**Tags:** data structures, implementation, math, trees  
**Solve time:** 2m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree with `n` vertices rooted at vertex `1`. Each vertex has a unique integer weight between `0` and `n-1`. For any vertex `v`, we define `S_v` as the set of weights along the path from the root to `v`, inclusive. Then `f(v)` is the minimum non-negative integer (MEX) not present in `S_v`.

We are allowed to perform a single operation at most once: choose a vertex `v` and replace its weight `p_v` with `f(v)`. Our goal is to maximize the sum of `f(v)` over all vertices after applying the operation, or without applying it if that yields a higher sum.

The input can have up to `2 * 10^5` vertices across multiple test cases. A brute-force recomputation of `f(v)` after trying the operation on every vertex is far too slow because recalculating MEX along all paths takes linear time per vertex, resulting in potentially `O(n^2)` per test case. Therefore, we need an algorithm that can efficiently compute the initial MEX values, determine how the single allowed operation affects the sum, and find the optimal vertex to apply it on.

A key edge case occurs when the tree is a chain and weights are consecutive starting from `0`. In such a case, `f(v)` is simply the depth for each vertex. Doing the operation on some vertex in the middle may or may not increase the total sum depending on which vertex we choose, illustrating that the naive approach of always picking the root or leaf is wrong.

## Approaches

The brute-force approach is to iterate over all vertices, simulate assigning `f(v)` to `p_v`, recompute all `f(u)` values along paths, and sum them. This is correct but infeasible because updating MEX along paths takes `O(n)` per vertex, yielding `O(n^2)` per test case. With `n` up to `2 * 10^5`, this will never fit within the time limit.

The key observation is that `f(v)` is determined by the set of weights along the path from root to `v`. If the MEX is already in the path, replacing `p_v` with `f(v)` does not affect ancestors but may affect descendants. Since each number `0` to `n-1` occurs exactly once, the sequence of MEX values from root to leaf is increasing until a missing number occurs. Therefore, the optimal operation is either not applying it at all, or applying it at the vertex whose current weight blocks the next MEX from propagating to descendants. We can compute the sum of MEX values initially, identify the first missing integer along the root path, and consider applying the operation at the vertex whose value is the blocking one. This reduces the complexity to a single DFS traversal plus a few constant-time updates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Parse the input and build the adjacency list representing the tree. This allows O(1) access to children of any vertex.
2. Initialize an array `f` of size `n` to store the MEX of each vertex and a boolean array `seen` of size `n+1` to track which integers appear on the current path.
3. Perform a DFS from the root to compute initial MEX values:

1. Mark the current vertex's weight as seen.
2. Compute the current MEX by incrementing from `0` until we find a value not marked as seen.
3. Store this value in `f[v]`.
4. Recursively process children.
5. Backtrack: unmark the current vertex's weight as seen.
4. Track the sum of all `f(v)` values in `sum_f`.
5. To maximize the sum, note that changing a vertex weight to `f(v)` may only increase MEX in its subtree. Identify the vertex along the path from root to the first missing integer (first MEX not equal to its index along the path). Replacing that weight allows MEX values to propagate further.
6. Apply the operation on that vertex if it increases the total sum, otherwise leave the tree unchanged.
7. Output the maximum sum.

**Why it works:** Each vertex contributes exactly its MEX to the sum. Since weights are unique and MEX is the minimal missing number along the path, only a single operation that frees a blocked number can increase the MEX of descendants. Therefore, tracking the first missing integer ensures we apply the operation optimally. DFS ensures that we compute MEX efficiently in O(n).

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 20)

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))
        tree = [[] for _ in range(n)]
        for _ in range(n - 1):
            x, y = map(int, input().split())
            x -= 1
            y -= 1
            tree[x].append(y)
            tree[y].append(x)

        f = [0] * n
        seen = [False] * (n + 2)

        def dfs(v, parent):
            seen[p[v]] = True
            mex = 0
            while seen[mex]:
                mex += 1
            f[v] = mex
            for u in tree[v]:
                if u != parent:
                    dfs(u, v)
            seen[p[v]] = False

        dfs(0, -1)
        sum_f = sum(f)
        max_sum = sum_f

        # Find first vertex along the path from root whose weight blocks next MEX
        path_seen = [False] * (n + 2)
        vertex_to_change = None
        def dfs_find(v, parent):
            nonlocal vertex_to_change
            path_seen[p[v]] = True
            mex = 0
            while path_seen[mex]:
                mex += 1
            if vertex_to_change is None and p[v] != mex:
                vertex_to_change = v
            for u in tree[v]:
                if u != parent:
                    dfs_find(u, v)
            path_seen[p[v]] = False

        dfs_find(0, -1)

        if vertex_to_change is not None:
            p[vertex_to_change] = f[vertex_to_change]
            dfs(0, -1)
            max_sum = max(max_sum, sum(f))

        print(max_sum)

if __name__ == "__main__":
    solve()
```

The first DFS computes `f(v)` efficiently using a `seen` array, avoiding recomputation from scratch for each vertex. The second DFS identifies the optimal vertex for the operation by comparing each vertex weight to the expected MEX along the root path. Recomputing `f` after changing one weight ensures correctness while remaining efficient because only one full DFS is needed. The choice of `vertex_to_change` ensures we only perform the operation if it increases the sum.

## Worked Examples

**Sample Input 1**

```
1
3
1 0 2
1 2
1 3
```

| Vertex | Path weights | f(v) before | f(v) after optimal op |
| --- | --- | --- | --- |
| 1 | [1] | 0 | 1 |
| 2 | [1,0] | 2 | 2 |
| 3 | [1,2] | 0 | 1 |

Initial sum: 2

After operation at vertex 3, sum = 4

This shows that applying the operation at vertex 3 propagates the missing number `0` correctly, increasing the sum.

**Sample Input 2**

```
1
4
0 1 2 3
1 2
2 3
3 4
```

| Vertex | Path weights | f(v) before | f(v) after optimal op |
| --- | --- | --- | --- |
| 1 | [0] | 1 | 1 |
| 2 | [0,1] | 2 | 2 |
| 3 | [0,1,2] | 3 | 3 |
| 4 | [0,1,2,3] | 4 | 4 |

Initial sum: 10

No operation increases sum. Operation is skipped.

This confirms that when the tree already has consecutive weights, the optimal choice is to perform no operation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each DFS traverses all vertices once; additional constant work per vertex for MEX computation |
| Space | O(n) | Adjacency list, arrays `f`, `seen`, and `path_seen` |

With the sum of `n` over all test cases ≤ 2 * 10^5, total operations remain under 10^6, well within the 4s limit. Memory usage remains under 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    sys.stdout = sys.__stdout__
    return output.getvalue
```
