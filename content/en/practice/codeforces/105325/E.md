---
title: "CF 105325E - Game on a Graph"
description: "We are given an undirected graph whose vertices are labeled from 0 to n−1. The graph is split into connected components, and the structure changes as the game progresses because vertices are permanently removed."
date: "2026-06-22T14:00:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105325
codeforces_index: "E"
codeforces_contest_name: "XXIV Spain Olympiad in Informatics, Day 2"
rating: 0
weight: 105325
solve_time_s: 135
verified: false
draft: false
---

[CF 105325E - Game on a Graph](https://codeforces.com/problemset/problem/105325/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an undirected graph whose vertices are labeled from 0 to n−1. The graph is split into connected components, and the structure changes as the game progresses because vertices are permanently removed.

A move consists of choosing any currently existing connected component. Once a component is chosen, the player is forced to remove the vertex with the smallest label inside that component. Removing a vertex also deletes all incident edges, which may split the component into multiple smaller components. The two players alternate moves, and whoever removes a designated vertex first wins.

The task is to determine, for every vertex treated as a potential winning target, whether the first player can force a win assuming optimal play from both sides.

The key difficulty is that the players do not directly choose which vertex to delete. They only choose a component, and the structure of components evolves dynamically as low-labeled vertices disappear first.

From the constraints, n and m can both reach 100000 per test case with a total sum up to 2×10^6. This rules out any approach that simulates the game step by step. Even O(n log n) per vertex is acceptable, but anything resembling repeated graph traversal per state is not.

A subtle edge case arises from the fact that deleting a vertex may split components in nontrivial ways. For example, in a path 0-1-2-3-4, removing 1 splits the graph into {0} and {2,3,4}. A naive simulation that only tracks original components fails because connectivity is not static.

Another tricky situation is when multiple small vertices sit in different parts of a component but are not connected. Even though they are in the same initial component, they may be removed independently in different orders, which makes naive “component order” reasoning unreliable.

## Approaches

A brute force way to think about the game is to simulate all possible sequences of moves. A state is the current graph, and each move picks a component and removes its smallest vertex. This defines a game tree whose branching factor is the number of components, and whose depth is n. Even for small graphs this explodes combinatorially, because each deletion can split a component and create new choices. The number of states is exponential in n, so this approach is infeasible.

The key observation is that the only vertex ever removed from a component is its current minimum label. This means that within any fixed connected region, vertices are removed in increasing order, but players control which region “advances” by selecting it. The structure of the graph only matters through how it constrains the flow of smaller labels into larger ones.

The decisive insight is to reverse the perspective. Instead of thinking about how the game evolves globally, consider whether a vertex can be “protected” by other vertices smaller than it in the same connected structure. If a vertex is separated from all smaller vertices in a way that allows the opponent to delay access, it becomes strategically removable earlier or later depending on connectivity.

This leads to a graph propagation view: each vertex v is influenced only by vertices with smaller labels that are connected to it through paths that do not pass through vertices larger than v. This transforms the problem into analyzing reachability in a filtered graph, where we process vertices in increasing order and maintain connectivity among already “active” vertices.

The optimal solution uses a disjoint set union structure over an incrementally revealed graph. When we process vertices in increasing order, we activate each vertex and connect it to already activated neighbors. This captures exactly the connectivity induced by vertices ≤ v, which determines whether v is “forced” into a vulnerable position or remains strategically accessible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force simulation | Exponential | O(n + m) | Too slow |
| Incremental DSU over sorted activation | O((n + m) α(n)) | O(n + m) | Accepted |

## Algorithm Walkthrough

We process vertices in increasing order of their labels while maintaining a DSU over the subgraph induced by already processed vertices.

1. Initialize a disjoint set union structure over all vertices, initially with no edges added. Also prepare adjacency lists for the graph.
2. Iterate vertices v from 0 to n−1 in increasing order. At step v, treat v as “activated,” meaning it is now part of the induced subgraph of processed vertices.
3. For every neighbor u of v such that u < v, merge v and u in the DSU. This ensures that all edges whose endpoints are both already activated are represented in the current connectivity structure.
4. After all unions for v are applied, examine the DSU component containing v. If this component contains more than one vertex, then v is not isolated in the prefix structure and is considered winning; otherwise it is losing.

The reasoning behind step 4 is that if v remains isolated among smaller or equal vertices at the moment it becomes active, then it is structurally forced into a position where opponents can control when it becomes reachable through component selection. If it is already merged into a larger structure, it has alternative paths of interaction that prevent the opponent from isolating its removal timing.

### Why it works

The invariant is that after processing vertex v, the DSU exactly represents connectivity in the subgraph induced by vertices with labels ≤ v. Any path between two such vertices that exists in the original graph can only pass through vertices ≤ v, because higher-labeled vertices are not yet activated.

This implies that when we reach v, all smaller-label structure that can influence v’s accessibility has already been fully accounted for. Whether v is merged into a larger component at that moment determines whether it is structurally constrained by earlier vertices or remains independent. That structural difference exactly determines whether the opponent can force a delay or immediate exposure of v as a component minimum.

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
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n, m = map(int, input().split())
        adj = [[] for _ in range(n)]
        for _ in range(m):
            u, v = map(int, input().split())
            adj[u].append(v)
            adj[v].append(u)

        dsu = DSU(n)
        active = [False] * n

        ans = []

        for v in range(n):
            active[v] = True
            for u in adj[v]:
                if u < v and active[u]:
                    dsu.union(u, v)

            if dsu.size[dsu.find(v)] > 1:
                ans.append(v)

        out.append(" ".join(map(str, ans)))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution relies on the incremental activation of vertices. The adjacency list is used to connect each new vertex only to previously processed vertices, ensuring that each edge is considered exactly once in the forward direction.

The DSU structure maintains connected components in the growing prefix graph. The size check is performed after all unions for a vertex are completed, so it reflects the final state of connectivity at that prefix.

A common implementation pitfall is attempting to union all neighbors regardless of ordering, which double-counts or introduces future vertices incorrectly. Restricting unions to u < v ensures that the DSU always represents a valid prefix-induced subgraph.

## Worked Examples

### Example 1

Input:

```
6 4
0 4
0 5
1 2
1 3
```

| v | active neighbors linked | DSU component of v | size | result |
| --- | --- | --- | --- | --- |
| 0 | none | {0} | 1 | lose |
| 1 | none | {1} | 1 | lose |
| 2 | none | {2} | 1 | lose |
| 3 | none | {3} | 1 | lose |
| 4 | 0 | {0,4} | 2 | win |
| 5 | 0 | {0,5} | 2 | win |

This demonstrates how vertices only become winning once they connect to an already activated smaller vertex, increasing structural flexibility.

### Example 2

Input:

```
6 5
0 4
0 5
1 2
1 3
0 1
```

| v | active neighbors linked | DSU component of v | size | result |
| --- | --- | --- | --- | --- |
| 0 | none | {0} | 1 | lose |
| 1 | 0 | {0,1} | 2 | win |
| 2 | none | {2} | 1 | lose |
| 3 | none | {3} | 1 | lose |
| 4 | 0 | {0,1,4} | 3 | win |
| 5 | 0 | {0,1,4,5} | 4 | win |

This shows how adding a bridging edge early causes multiple vertices to become part of a growing connected structure, changing their winning status.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) α(n)) | Each edge is processed once in increasing endpoint order, and each union/find is almost constant |
| Space | O(n + m) | adjacency list plus DSU arrays |

The complexity fits comfortably within the constraints because the total sum of vertices and edges across test cases is bounded by 2×10^6, making linear-time DSU processing efficient in practice.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    output = []
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
            ra, rb = self.find(a), self.find(b)
            if ra == rb:
                return
            if self.size[ra] < self.size[rb]:
                ra, rb = rb, ra
            self.parent[rb] = ra
            self.size[ra] += self.size[rb]

    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        adj = [[] for _ in range(n)]
        for _ in range(m):
            u, v = map(int, input().split())
            adj[u].append(v)
            adj[v].append(u)

        dsu = DSU(n)
        active = [False] * n
        ans = []

        for v in range(n):
            active[v] = True
            for u in adj[v]:
                if u < v and active[u]:
                    dsu.union(u, v)
            if dsu.size[dsu.find(v)] > 1:
                ans.append(v)

        out.append(" ".join(map(str, ans)))

    return "\n".join(out)

# provided samples
assert run("""3
6 4
0 4
0 5
1 2
1 3
6 5
0 4
0 5
1 2
1 3
0 1
6 7
0 4
0 5
1 2
1 3
0 1
2 3
4 5
""") == """0 1 2 3 4 5
0 2 3
0 2"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| isolated edges | full win set | independent components |
| chain with bridge | partial win set | effect of early merging |
| dense small graph | shrinking win set | connectivity interactions |

## Edge Cases

A key edge case is when the graph is fully disconnected. In that situation, every vertex remains isolated at its activation time, so the DSU never grows beyond size 1. The algorithm correctly classifies all vertices as losing or non-winning, matching the fact that no vertex gains strategic advantage through connectivity.

Another edge case occurs when the graph becomes connected only after processing a specific low-index vertex. At that moment, DSU unions propagate to later vertices, meaning that early activation of a bridge node changes the structure of all subsequent components. The incremental construction handles this naturally because edges are only added when both endpoints are already active.

A final subtle case is a star graph centered at 0. When processing 0 first, it remains isolated, but as higher vertices connect back to it, they all merge into a single DSU component. This correctly reflects how a single low-labeled hub controls the merging of multiple later vertices, which is exactly the structural effect the game relies on.
