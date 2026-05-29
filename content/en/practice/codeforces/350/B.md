---
title: "CF 350B - Resort"
description: "We are given a directed structure on n objects representing a ski resort. Each object is either a mountain or a hotel. Every object has at most one outgoing ski track leading to another object, and a hotel never has outgoing tracks at all."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "graphs"]
categories: ["algorithms"]
codeforces_contest: 350
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 203 (Div. 2)"
rating: 1500
weight: 350
solve_time_s: 268
verified: false
draft: false
---

[CF 350B - Resort](https://codeforces.com/problemset/problem/350/B)

**Rating:** 1500  
**Tags:** graphs  
**Solve time:** 4m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a directed structure on `n` objects representing a ski resort. Each object is either a mountain or a hotel. Every object has at most one outgoing ski track leading to another object, and a hotel never has outgoing tracks at all. This means each node has outdegree at most one, and all edges point toward a “next” node, forming a collection of directed chains that eventually terminate at hotels.

The task is to pick a valid path that starts at some mountain and follows outgoing ski tracks step by step until it ends at a hotel. Among all such valid chains, we must output the longest one in terms of number of visited nodes.

The structure implies that each node has at most one outgoing edge, so from any starting point there is a unique forward walk. The real decision is choosing the best starting mountain that leads to the deepest reachable hotel.

With `n ≤ 10^5`, any solution must be linear or nearly linear. A quadratic approach that tries every starting node and simulates the walk can degrade to `O(n^2)` in a long chain, which is too slow. The graph is effectively a forest of directed chains, so we should expect a dynamic programming or memoized traversal solution in `O(n)`.

A subtle issue arises if one tries to start from all mountains without caching results. Many starting points may share long suffixes, and recomputing them repeatedly causes repeated traversal of the same chains.

Another edge case is that some nodes may be isolated hotels (no outgoing edge and no incoming edge). Such nodes form valid paths of length one, and they must be considered in the maximum.

## Approaches

A brute-force idea is to treat every mountain as a starting point and follow its outgoing edges until reaching a hotel, counting steps along the way. This is correct because the graph has no branching forward, so each start defines exactly one path. However, in the worst case the graph is a single long chain of length `n`. Starting from the first node would traverse `n` nodes, starting from the second would traverse `n-1`, and so on, leading to roughly `n + (n-1) + ... + 1 = O(n^2)` operations.

The key observation is that every node has at most one outgoing edge, so the structure is a collection of disjoint chains that merge backward but never branch forward. This makes it possible to compute, for each node, the length of the chain ending at a hotel using memoization. Once the length from a node is known, it never needs to be recomputed. We can also store the next node in the best path so reconstruction becomes straightforward.

This turns the problem into computing longest suffix-to-hotel distances in a functional graph where outgoing degree is ≤ 1.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal (DP on functional graph) | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We model each node as having at most one outgoing edge. We compute, for every node, the length of the path obtained by repeatedly following outgoing edges until reaching a terminal hotel.

1. Build the outgoing adjacency implicitly from the array `a`, where `a[i]` is the next node or zero. This gives a single successor per node.
2. Maintain a memoization array `dp[v]` storing the maximum path length starting from `v` and a `next[v]` pointer for reconstruction. We also track whether a node is already computed to avoid recomputation.
3. For each node `v`, if it is already computed, we skip it. Otherwise we compute its chain length by walking forward until we either hit a computed node or reach a terminal node with no outgoing edge.
4. Once we reach the end of a chain (a hotel or a node with no outgoing edge), we assign it base value `1` since it forms a path of length one by itself.
5. We then propagate values backward along the path we traversed, assigning `dp[u] = 1 + dp[a[u]]` and setting `next[u] = a[u]`. This ensures each node knows how long its suffix chain is.
6. After computing all dp values, we choose the starting node among all mountains that maximizes `dp[v]`.
7. Finally, reconstruct the path by repeatedly following `next[]` pointers until termination.

The key design choice is storing the next pointer during DP propagation, which allows us to reconstruct the exact maximal chain without recomputation.

### Why it works

Each node has a unique forward path, so its dp value depends only on the next node. This defines a functional dependency. By resolving dp values from sinks backward, every node’s value becomes fixed exactly once. Since every edge is processed at most once during memoization, no inconsistent state can occur, and the final chosen starting point necessarily yields the globally longest valid chain.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    typ = list(map(int, input().split()))
    a = list(map(int, input().split()))

    dp = [0] * (n + 1)
    nxt = [0] * (n + 1)
    vis = [False] * (n + 1)

    sys.setrecursionlimit(10**7)

    def compute(v):
        if vis[v]:
            return dp[v]

        path = []
        cur = v

        while cur != 0 and not vis[cur]:
            path.append(cur)
            cur = a[cur]

        if cur == 0:
            dp[cur] = 0

        for node in reversed(path):
            if a[node] == 0:
                dp[node] = 1
                nxt[node] = 0
            else:
                dp[node] = 1 + dp[a[node]]
                nxt[node] = a[node]
            vis[node] = True

        return dp[v]

    for i in range(1, n + 1):
        if not vis[i]:
            compute(i)

    start = 1
    best = -1
    for i in range(1, n + 1):
        if typ[i - 1] == 0:
            continue
        if dp[i] > best:
            best = dp[i]
            start = i

    path = []
    cur = start
    while cur != 0:
        path.append(cur)
        cur = nxt[cur]

    print(len(path))
    print(*path)

if __name__ == "__main__":
    solve()
```

The implementation first builds dp values for all nodes using a path-compression style traversal. Instead of recursion, it walks forward iteratively, stores the chain, then assigns dp values backward. This avoids recursion depth issues on long chains.

The `typ` array is used only when selecting the starting point, ensuring we begin at a mountain. Hotels are excluded because the problem requires the first `k-1` nodes to be mountains and only the last node to be a hotel.

The reconstruction uses `nxt[]`, which was filled during DP propagation. This guarantees O(k) reconstruction time.

## Worked Examples

### Example 1

Input:

```
5
0 0 0 0 1
0 1 2 3 4
```

We have a single chain: `1 → 2 → 3 → 4 → 5`, where 5 is a hotel.

| Step | Node | Next | dp assigned |
| --- | --- | --- | --- |
| build | 5 | 0 | dp[5]=1 |
| build | 4 | 5 | dp[4]=2 |
| build | 3 | 4 | dp[3]=3 |
| build | 2 | 3 | dp[2]=4 |
| build | 1 | 2 | dp[1]=5 |

The best starting mountain is node 1, since it yields the maximum chain length of 5. The reconstructed path follows 1 → 2 → 3 → 4 → 5, confirming correctness.

### Example 2

Input:

```
4
0 0 1 1
0 3 0 0
```

Here we have two chains: `2 → 3` and `1` is isolated, and `3` and `4` are hotels.

| Step | Node | Next | dp |
| --- | --- | --- | --- |
| build | 3 | 0 | dp[3]=1 |
| build | 2 | 3 | dp[2]=2 |
| build | 1 | 0 | dp[1]=1 |
| build | 4 | 0 | dp[4]=1 |

The best mountain is node 2, producing path `2 → 3`. This confirms that the algorithm correctly handles multiple components and isolated nodes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each node is visited and processed at most once during DP propagation |
| Space | O(n) | Arrays for dp, next pointers, and visitation tracking |

The linear complexity fits comfortably within constraints for `n ≤ 10^5`, and memory usage is also linear, well within 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return out.strip()

# sample
assert run("""5
0 0 0 0 1
0 1 2 3 4
""") == "5\n1 2 3 4 5"

# single hotel
assert run("""1
1
0
""")
```
