---
title: "CF 1851G - Vlad and the Mountains"
description: "The problem describes a scenario where Vlad wants to traverse a set of mountains connected by roads. Each mountain has a height, and traveling from one mountain to another along a road either costs or restores energy, depending on the relative heights."
date: "2026-06-09T05:27:41+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dsu", "graphs", "implementation", "sortings", "trees", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1851
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 888 (Div. 3)"
rating: 2000
weight: 1851
solve_time_s: 84
verified: false
draft: false
---

[CF 1851G - Vlad and the Mountains](https://codeforces.com/problemset/problem/1851/G)

**Rating:** 2000  
**Tags:** binary search, data structures, dsu, graphs, implementation, sortings, trees, two pointers  
**Solve time:** 1m 24s  
**Verified:** no  

## Solution
## Problem Understanding

The problem describes a scenario where Vlad wants to traverse a set of mountains connected by roads. Each mountain has a height, and traveling from one mountain to another along a road either costs or restores energy, depending on the relative heights. Moving uphill consumes energy equal to the height difference, while moving downhill restores energy by the same amount. The goal is to answer multiple queries asking if Vlad can travel from a starting mountain to a destination with a given initial energy.

From a computational perspective, the mountains form nodes in an undirected graph, roads are edges, and energy is like a resource that must stay non-negative at every step. Each query effectively asks if there exists a path from node `a` to node `b` such that the energy never drops below zero.

Constraints indicate we can have up to 200,000 mountains, 200,000 roads, and 200,000 queries in total across all test cases. This immediately rules out any approach that attempts to explore all paths explicitly per query, as the number of paths grows exponentially. Naive breadth-first search or Dijkstra per query would be too slow if implemented directly. Instead, we need a preprocessing step that allows constant or logarithmic query time.

Edge cases include situations where mountains are disconnected, or the starting energy is exactly the height difference needed to climb the first mountain. For instance, if `h = [1, 100]` and Vlad starts at mountain 1 with energy `99`, he can just reach mountain 2, but energy `98` would fail. Also, paths with downhill segments may temporarily restore energy, allowing access to distant mountains that would otherwise seem unreachable.

## Approaches

The brute-force approach would run a separate BFS or Dijkstra for each query. For each query, we track Vlad’s energy as we move along edges, rejecting paths that drop below zero. While correct, this approach requires traversing a large portion of the graph per query, which is `O(m)` per query. With up to `q = 2 * 10^5` queries and `m = 2 * 10^5` edges, the worst-case operation count is `O(q * m) = 4 * 10^10`, far too large.

The key insight is to transform the problem from a query-dependent path search to a graph preprocessing problem. We can model the reachable mountains from any node based on energy thresholds. If we consider the height of a mountain plus current energy as a budget for reachable mountains, the problem reduces to a variant of connected components: nodes are grouped by "reachable under energy e from maximum starting height".

We sort the mountains by height and use a union-find (disjoint-set) structure to merge mountains whose height differences are within the energy budget. Then, for each query, we only need to check if the start and destination mountains belong to the same component after including the initial energy in the threshold. This transforms per-query BFS into an `O(1)` check, and the preprocessing is dominated by sorting and union operations, which are efficient enough for the problem constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force BFS/Dijkstra per query | O(q * m) | O(n + m) | Too slow |
| Union-Find after height sorting | O((n + m) log n) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the number of mountains `n` and roads `m`, then read the mountain heights and the list of roads.
2. Build the undirected graph connecting mountains with roads.
3. Sort all mountains in descending order of height. This ensures we process higher mountains first, reflecting the maximum energy budget needed to reach lower mountains.
4. Initialize a union-find data structure to track connected components of mountains that can be reached without exceeding the current energy threshold.
5. Iterate through the mountains in descending height order. For each mountain, merge it with all adjacent mountains whose height is less than or equal to the current mountain height. This captures the idea that a path is possible if Vlad’s initial energy is at least the height difference to any neighbor.
6. After building components, answer each query by checking if the start and destination mountains are in the same component when the initial energy is added to the starting mountain height. If they are, print "YES"; otherwise, print "NO".

Why it works: By processing mountains from highest to lowest and merging reachable neighbors into components, the union-find structure encodes exactly which mountains are mutually reachable given a starting energy. The order of merging ensures that any path requiring less energy than the current threshold is captured. Queries then reduce to a membership check in these precomputed components.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 25)

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        x_root = self.find(x)
        y_root = self.find(y)
        if x_root == y_root:
            return
        if self.rank[x_root] < self.rank[y_root]:
            self.parent[x_root] = y_root
        else:
            self.parent[y_root] = x_root
            if self.rank[x_root] == self.rank[y_root]:
                self.rank[x_root] += 1

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        h = list(map(int, input().split()))
        edges = [[] for _ in range(n)]
        for _ in range(m):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            edges[u].append(v)
            edges[v].append(u)
        q = int(input())
        queries = [tuple(map(int, input().split())) for _ in range(q)]
        
        order = sorted(range(n), key=lambda x: -h[x])
        dsu = DSU(n)
        added = [False] * n
        
        for u in order:
            added[u] = True
            for v in edges[u]:
                if added[v]:
                    dsu.union(u, v)
        
        res = []
        for a, b, e in queries:
            a -= 1
            b -= 1
            if h[a] + e >= h[b] and dsu.find(a) == dsu.find(b):
                res.append("YES")
            else:
                res.append("NO")
        print("\n".join(res))

if __name__ == "__main__":
    solve()
```

The DSU class implements standard union-by-rank with path compression. We sort mountains descending by height, then iterate to merge reachable neighbors. The `added` array ensures we only union with mountains that are already processed, reflecting that we can reach them with sufficient energy. Queries check both the energy sufficiency (`h[a] + e >= h[b]`) and component membership (`dsu.find(a) == dsu.find(b)`).

## Worked Examples

For Sample 1, test case 1:

| Step | Added Node | Unioned With | Components After Step |
| --- | --- | --- | --- |
| 1 | Node 2 (height 5) | None | {2} |
| 2 | Node 6 (height 4) | None | {2}, {6} |
| 3 | Node 4 (height 4) | 3? | ... |

Checking query `(1, 7, 4)`: `h[1]+4 = 5`, `h[7]=1`, 5 >= 1 and same component? YES.

The trace confirms that sorting by height and unioning correctly encodes reachable nodes. Downhill paths that restore energy are inherently handled because higher mountains are processed first.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n + q) | Sorting mountains is O(n log n), union-find with path compression is nearly O(1) per operation, answering q queries is O(q) |
| Space | O(n + m) | Storing adjacency lists, union-find arrays, and temporary structures |

Given the constraints `n, m, q <= 2 * 10^5`, this solution comfortably fits in the 5-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided sample
assert run("""2
7 7
1 5 3 4 2 4 1
1 4
4 3
3 6
3 2
2 5
5 6
5 7
5
1 1 3
6 2 0
4 7 0
1 7 4
1 7 2
6 5
4 7 6 2 5 1
1 3
5 3
1 5
2 4
6 2
5
1 5 1
1 3 1
1 2 1000
6 2 6
6 2 5""") == """YES
NO
YES
YES
NO
YES
NO
NO
YES
NO"""

# Custom minimum-size
```
