---
title: "CF 106452L - MST"
description: "We have a connected weighted undirected graph. An MST is a spanning tree with the smallest possible total edge weight, but several different trees can have the same minimum cost."
date: "2026-06-25T09:18:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106452
codeforces_index: "L"
codeforces_contest_name: "UTPC April Fools Contest 2026"
rating: 0
weight: 106452
solve_time_s: 32
verified: true
draft: false
---

[CF 106452L - MST](https://codeforces.com/problemset/problem/106452/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 32s  
**Verified:** yes  

## Solution
# Problem Understanding

We have a connected weighted undirected graph. An MST is a spanning tree with the smallest possible total edge weight, but several different trees can have the same minimum cost.

The operation allowed by the problem is unusual: we may only increase edge weights, and each increase costs one operation. The goal is not to find an MST, but to remove all ambiguity from the existing MST structure. We need to increase the weights of the minimum number of edges so that the minimum spanning tree cost stays exactly the same and there is only one possible MST.

The input describes vertices and edges. Each edge connects two vertices and has a positive weight. The output is the minimum number of individual `+1` weight increases needed.

The constraints are large: both the number of vertices and edges can reach `2 * 10^5`. An algorithm that checks every possible spanning tree is impossible because the number of spanning trees can be exponential. Even approaches with repeated graph searches over all edges are too slow. We need a near-linear or `O(m log m)` solution, which points toward using the structure of Kruskal's algorithm.

The tricky part is handling groups of equal-weight edges. Equal weights are the only reason multiple MSTs exist. For example, consider:

```
3 3
1 2 1
2 3 1
1 3 1
```

The answer is `1`. A careless solution may think all three edges are necessary because they all have the smallest weight, but only two edges are needed to connect three vertices. Raising any one edge to weight `2` leaves exactly one MST.

Another edge case is when equal weights do not create any choice:

```
3 3
1 2 1
2 3 2
1 3 3
```

The answer is `0`. The MST is already unique because the smallest edge choices force the tree. A solution that counts every non-MST edge would incorrectly return `1` or more.

A final boundary case is a graph with one vertex:

```
1 0
```

The answer is `0`. There are no edges to modify, and the single vertex already forms a spanning tree. Code that assumes at least one edge or tries to build an MST with `n-1` edges can fail here.

# Approaches

A direct approach would be to build an MST and then inspect every alternative tree. If several MSTs exist, we could try increasing edges one by one and checking whether the MST becomes unique. The idea is correct because uniqueness can be tested by MST properties, but the number of possible modifications is too large. In the worst case, a dense graph with many equal-weight edges would require repeatedly examining many MST candidates, which is far beyond the limits.

The key observation comes from Kruskal's algorithm. Kruskal processes edges in increasing weight order. When all edges with weight smaller than `w` have been processed, the current DSU components represent everything that is already forced before considering edges of weight `w`.

Now look only at edges with the same weight `w`. Inside each DSU component from smaller weights, those edges cannot affect the MST. The remaining equal-weight edges connect the current components together. If these edges contain a cycle, there are multiple ways to choose MST edges of weight `w`.

For every connected component formed by these equal-weight edges, we only need a spanning tree among them. Any extra edge beyond that tree creates an alternative MST and must be increased. If a temporary component contains `E` edges and `V` DSU components, exactly `E - (V - 1)` edges need to be raised.

This can be calculated while processing each weight group. We count the equal-weight edges that connect different current DSU components, then count how many of them actually merge components. The difference is the number of unnecessary edges.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in `n` | O(n + m) | Too slow |
| Optimal | O(m log m) | O(n + m) | Accepted |

# Algorithm Walkthrough

1. Sort all edges by their weight. Kruskal's algorithm depends on processing smaller weights first, because edges with lower weights are already fixed before a heavier group is considered.
2. Maintain a DSU containing all edges with weight strictly smaller than the current group. For a group of edges with the same weight, temporarily ignore edges that already connect two vertices inside the same DSU component. Those edges can never change an MST because a cheaper path already connects their endpoints.
3. For the remaining edges of this weight group, count how many can connect different DSU components. These are the edges that can participate in some MST.
4. Merge these remaining edges in the DSU. Each successful merge reduces the number of independent connections needed. If a merge fails, the edge creates a cycle among equal-weight choices, meaning it is an edge that causes non-uniqueness.
5. Add the number of failed merges from this weight group to the answer. These are exactly the edges whose weights need to be increased.
6. Continue with the next weight group until every edge has been processed.

Why it works:

Kruskal's algorithm tells us that every MST can be constructed by choosing edges inside each weight group so that they connect as many currently separate components as possible. After all smaller weights are fixed, a connected group of equal-weight edges with a cycle gives multiple valid choices. Removing enough edges to leave a tree removes all choices while preserving the ability to build an MST with the same total cost. The failed DSU merges are exactly the surplus cycle edges, so counting them gives the minimum number of required increases.

# Python Solution

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

    def unite(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        return True

def solve():
    n, m = map(int, input().split())
    edges = []

    for _ in range(m):
        u, v, w = map(int, input().split())
        edges.append((w, u - 1, v - 1))

    edges.sort()

    dsu = DSU(n)
    ans = 0
    i = 0

    while i < m:
        j = i
        while j < m and edges[j][0] == edges[i][0]:
            j += 1

        before = 0
        for k in range(i, j):
            _, u, v = edges[k]
            if dsu.find(u) != dsu.find(v):
                before += 1

        merged = 0
        for k in range(i, j):
            _, u, v = edges[k]
            if dsu.unite(u, v):
                merged += 1

        ans += before - merged
        i = j

    print(ans)

if __name__ == "__main__":
    solve()
```

The DSU stores the components formed by all already processed lighter edges. The sorting step gives the same ordering used by Kruskal.

For each weight group, `before` counts the number of equal-weight edges that still have a chance to appear in an MST. Edges already inside one component are ignored because they are already replaceable by lighter paths.

The `merged` count records how many of those edges are actually needed to connect the components. Every successful merge contributes one edge to the possible spanning forest. The difference `before - merged` is the number of cycle edges in that weight group.

The code uses iterative path compression in `find` and union by size in `unite`, keeping DSU operations almost constant time. All weights are handled as integers, and the answer fits in a normal Python integer without overflow concerns.

# Worked Examples

Consider:

```
4 3
1 2 3
2 4 1
4 3 4
```

The sorted edges are processed in increasing order.

| Weight | Edge processing | Components before group | `before` | `merged` | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | Add 2-4 | {1},{2},{3},{4} | 1 | 1 | 0 |
| 3 | Add 1-2 | {1},{2,4},{3} | 1 | 1 | 0 |
| 4 | Add 4-3 | {1,2,4},{3} | 1 | 1 | 0 |

The graph already has a unique MST, so no edges need to be increased.

Now consider:

```
3 3
1 2 1
2 3 1
1 3 1
```

| Weight | Edge processing | Components before group | `before` | `merged` | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | Process all three edges | {1},{2},{3} | 3 | 2 | 1 |

Three equal edges connect three separate vertices. Only two are needed for a tree, so one edge must be raised.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log m) | Sorting dominates the DSU processing |
| Space | O(n + m) | The graph edges and DSU arrays are stored |

The constraints allow `2 * 10^5` edges, so an `O(m log m)` solution comfortably fits. The DSU operations are effectively linear because of path compression and union by size.

# Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out

assert run("""3 3
1 2 1
2 3 1
1 3 1
""") == "1\n", "all equal triangle"

assert run("""3 3
1 2 1
2 3 2
1 3 3
""") == "0\n", "already unique"

assert run("""1 0
""") == "0\n", "single vertex"

assert run("""5 6
1 2 2
2 3 1
4 5 3
2 4 2
1 4 2
1 5 3
""") == "2\n", "multiple equal weight cycles"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Triangle with three equal edges | `1` | Detects a simple equal-weight cycle |
| Strictly increasing MST choices | `0` | Confirms no unnecessary modifications |
| One vertex | `0` | Handles the smallest graph |
| Several equal-weight groups | `2` | Checks processing of multiple weight layers |

# Edge Cases

For the equal-weight triangle:

```
3 3
1 2 1
2 3 1
1 3 1
```

Initially every edge can appear in an MST. The DSU starts with three separate components. The first two merges create a spanning tree. The third edge connects vertices already connected by weight-one edges, so it forms a cycle. The algorithm counts one failed merge and returns `1`.

For an already unique MST:

```
3 3
1 2 1
2 3 2
1 3 3
```

The first edge connects two components. The second edge connects the remaining vertex. The last edge is heavier and never creates a choice among minimum edges. No failed merge happens, so the answer remains `0`.

For the single-vertex graph:

```
1 0
```

The edge loop is never entered. The DSU already represents the complete spanning tree of one vertex, so the answer stays `0`.

For multiple equal-weight groups:

```
5 6
1 2 2
2 3 1
4 5 3
2 4 2
1 4 2
1 5 3
```

The weight-one edge is forced. Among weight-two edges, one edge is redundant after the cheaper component is considered, and among weight-three edges another redundancy appears. The algorithm counts both surplus choices and returns `2`.
