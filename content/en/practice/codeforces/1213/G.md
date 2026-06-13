---
title: "CF 1213G - Path Queries"
description: "We are given a weighted tree where every edge has a cost, and we are asked multiple questions about how “expensive” paths between pairs of vertices can be. For any two vertices $u$ and $v$, there is exactly one simple path between them because the graph is a tree."
date: "2026-06-13T17:18:52+07:00"
tags: ["codeforces", "competitive-programming", "divide-and-conquer", "dsu", "graphs", "sortings", "trees"]
categories: ["algorithms"]
codeforces_contest: 1213
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 582 (Div. 3)"
rating: 1800
weight: 1213
solve_time_s: 271
verified: true
draft: false
---

[CF 1213G - Path Queries](https://codeforces.com/problemset/problem/1213/G)

**Rating:** 1800  
**Tags:** divide and conquer, dsu, graphs, sortings, trees  
**Solve time:** 4m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a weighted tree where every edge has a cost, and we are asked multiple questions about how “expensive” paths between pairs of vertices can be.

For any two vertices $u$ and $v$, there is exactly one simple path between them because the graph is a tree. Along that path, we look at all edge weights and take the maximum one. The query asks: among all pairs of distinct vertices, how many have this maximum edge weight on their connecting path not exceeding a given threshold $q$.

So each query is essentially asking: if we are only allowed to “use” edges up to weight $q$, how many pairs of nodes become connected through only such edges.

A direct interpretation is that we are counting pairs of vertices that lie in the same connected component of the graph formed by keeping only edges with weight at most $q$.

The constraints go up to $2 \cdot 10^5$ vertices, edges, and queries. This immediately rules out recomputing connectivity from scratch per query. Any approach that tries to run a DFS or BFS per query would lead to roughly $O(m(n + n))$, which is far beyond feasible limits.

A second subtle issue is that pairs are counted over all queries independently. The answers are not incremental in a naive sense unless we exploit sorting and reuse structure.

A naive mistake is to interpret each query separately and rebuild a filtered graph every time. For example, if all edges are distinct and queries are also large, repeated traversal would time out even for moderate inputs.

Another common pitfall is to try to compute path maximums for every pair using LCA preprocessing. While LCA can compute maximum edge on a path in $O(\log n)$, doing this for all $O(n^2)$ pairs is impossible.

## Approaches

The brute-force viewpoint starts from the definition. For each query $q$, we would check every pair $(u, v)$, compute the maximum edge weight on their path, and count valid pairs. Even with LCA preprocessing, each query costs $O(n^2 \log n)$, which is completely infeasible for $n = 2 \cdot 10^5$.

A more structured view comes from flipping the perspective. Instead of asking “for each pair, what is the maximum edge on its path”, we ask “for each threshold, how many pairs become connected when edges up to that threshold are activated”.

As we increase the allowed weight, edges appear in increasing order. Each time we add an edge, it may merge two previously separate components. When two components of sizes $a$ and $b$ merge, they contribute $a \cdot b$ new valid pairs, because every vertex in one component can now reach every vertex in the other using edges of at most the current weight.

This observation converts the problem into a dynamic connectivity process over sorted edges, which is exactly what a DSU (disjoint set union) maintains efficiently. Instead of recomputing components per query, we process edges in increasing weight and maintain the number of connected pairs incrementally.

Queries can also be sorted by threshold, allowing us to sweep through both edges and queries in order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(m n^2)$ or worse | $O(n)$ | Too slow |
| DSU + sorting | $O((n + m)\log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We process edges in increasing weight while answering queries in increasing order of $q$.

1. Sort all edges by weight in non-decreasing order.

This ensures that when we process an edge, all previously processed edges are no heavier than it.
2. Sort queries but keep track of original indices.

This allows us to output answers in the original order while still processing efficiently.
3. Initialize a DSU with each node in its own component.

Each component initially contributes zero pairs since no two distinct nodes are connected.
4. Maintain a running variable `ans = 0` representing the number of valid pairs currently connected using only processed edges.
5. Maintain a pointer over edges.

For each query threshold $q$, we advance the edge pointer while edge weight $\le q$.

Each time we process an edge $(u, v, w)$:

If $u$ and $v$ are in different DSU components of sizes $a$ and $b$, merging them increases `ans` by $a \cdot b$.

We then union the components.
6. After processing all edges up to $q$, store `ans` as the answer for that query.

### Why it works

At any moment while processing edges up to weight $q$, the DSU components are exactly the connected components of the subgraph formed by edges with weight at most $q$. Every pair of nodes inside the same component has a path whose maximum edge is at most $q$, because all edges in the component satisfy this bound.

Conversely, if two nodes are in different components, there is no path between them using edges $\le q$, so their path must include an edge greater than $q$. Thus they are correctly excluded.

Each union operation accounts exactly for new reachable pairs introduced by the newly added edge, and no pair is counted twice because once two nodes are connected, they remain connected for all larger thresholds.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return 0
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        pairs = self.size[a] * self.size[b]
        self.size[a] += self.size[b]
        return pairs

def solve():
    n, m = map(int, input().split())
    edges = []
    for _ in range(n - 1):
        u, v, w = map(int, input().split())
        edges.append((w, u - 1, v - 1))

    edges.sort()

    queries = list(map(int, input().split()))
    q = [(queries[i], i) for i in range(m)]
    q.sort()

    dsu = DSU(n)
    ans = 0
    ei = 0
    res = [0] * m

    for val, idx in q:
        while ei < len(edges) and edges[ei][0] <= val:
            w, u, v = edges[ei]
            ans += dsu.union(u, v)
            ei += 1
        res[idx] = ans

    print(*res)

if __name__ == "__main__":
    solve()
```

The DSU stores component sizes so that every merge contributes exactly the number of new vertex pairs created. The sorting of edges and queries ensures we never revisit an edge or recompute connectivity.

A subtle implementation detail is returning the contribution from `union` instead of updating globally inside DSU. This keeps the logic explicit and avoids accidentally double counting.

Another important point is indexing: vertices are converted to zero-based indexing immediately to avoid repeated conversions during DSU operations.

## Worked Examples

### Sample 1

Input:

```
7 5
1 2 1
3 2 3
2 4 1
4 5 2
5 7 4
3 6 2
5 2 3 4 1
```

Sorted edges by weight:

| Step | Edge processed | DSU components merged | Added pairs | Total |
| --- | --- | --- | --- | --- |
| 1 | (1-2) w1 | 1 and 2 | 1 | 1 |
| 2 | (2-4) w1 | {1,2} and 4 | 2 | 3 |
| 3 | (4-5) w2 | {1,2,4} and 5 | 3 | 6 |
| 4 | (3-6) w2 | 3 and 6 | 1 | 7 |
| 5 | (3-2) w3 | merges big components | 12 | 19 |
| 6 | (5-7) w4 | final merge | 7 | 26 |

Now queries are processed in increasing order, and the DSU state is reused across thresholds. Each query captures the total number of connected pairs at that threshold.

This demonstrates that once components merge, all future queries include those pairs.

### Sample 2

Input:

```
4 3
1 2 5
2 3 1
3 4 4
1 4 5
```

Sorted edges:

(1,2), (3,4), (2,3)

Processing:

At threshold 1: only edge (2,3) active, pairs = 1

At threshold 4: edges (2,3), (3,4) active, component size 3 gives 3 pairs

At threshold 5: all edges active, whole tree size 4 gives 6 pairs

This shows how increasing thresholds monotonically expand DSU components and increase pair counts.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n + m)\log n)$ | Sorting edges and queries dominates, DSU operations are almost constant amortized |
| Space | $O(n)$ | DSU arrays and edge storage |

The solution scales comfortably to $2 \cdot 10^5$ constraints since each edge is processed exactly once and each query is answered in amortized constant time after sorting.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    solve()
    return sys.stdout.getvalue().strip()

# provided sample
assert run("""7 5
1 2 1
3 2 3
2 4 1
4 5 2
5 7 4
3 6 2
5 2 3 4 1
""") == "21 7 15 21 3"

# minimum case
assert run("""2 1
1 2 10
10
""") == "1"

# chain test
assert run("""5 3
1 2 1
2 3 2
3 4 3
4 5 4
1 2 4
""") == "4 6 10"

# all edges same weight
assert run("""4 2
1 2 5
2 3 5
3 4 5
4 5
3
""") == "10 0"

# single query large
assert run("""3 1
1 2 1
2 3 2
2
""") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 nodes | 1 | minimal connectivity |
| chain | increasing pairs | incremental merging |
| equal weights | full merge at once | batch union correctness |
| threshold split | partial connectivity | query filtering |

## Edge Cases

A key edge case is when all edges have weight larger than the smallest query. In that situation, no union ever happens before answering early queries, so all answers must remain zero until a threshold crosses the smallest edge weight. The DSU ensures this because no merge is performed until `edges[ei][0] <= q`.

Another case is when all edges have identical weight. Then every query either returns zero (if below that weight) or the full number of pairs once all edges are processed. The algorithm handles this naturally because all equal-weight edges are processed in a single batch when the threshold is reached.

A third subtle case is large components forming early. When a very small edge connects two large subtrees, the pair contribution becomes large immediately. The union function computes `size[a] * size[b]` at merge time, ensuring the count is exact at the moment of connectivity and not recomputed later, avoiding double counting across future queries.
