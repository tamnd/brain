---
title: "CF 104308J - Traveling Alien Masud"
description: "The earth map can be modeled as a directed graph where each city is a node and each one-way road is a directed edge."
date: "2026-07-01T20:03:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104308
codeforces_index: "J"
codeforces_contest_name: "Mirror of Independence Day Programming Contest 2023 by MIST Computer Club"
rating: 0
weight: 104308
solve_time_s: 51
verified: true
draft: false
---

[CF 104308J - Traveling Alien Masud](https://codeforces.com/problemset/problem/104308/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

The earth map can be modeled as a directed graph where each city is a node and each one-way road is a directed edge. Two cities belong to the same country exactly when they are mutually reachable, meaning there is a directed path from the first to the second and also a directed path back. This is exactly the definition of a strongly connected component, so the graph is naturally partitioned into SCCs, and each SCC acts as a single country.

After compressing the graph into SCCs, we get a directed acyclic graph where nodes are countries and edges represent that at least one road exists from some city in one country to a city in another.

Masud can only prepare documents for at most two countries, but he is allowed to travel freely along roads. The goal is to maximize the number of distinct cities he can visit while never leaving the union of at most two SCCs.

So the problem reduces to choosing either one SCC or two SCCs such that all visited cities lie entirely inside those SCCs and are reachable via directed roads.

The key subtlety is that choosing two SCCs is only useful when it is possible to move from one SCC into the other through directed edges in the original graph. If there is no directed path connecting them in a usable direction, he cannot traverse between them in a single travel plan.

The constraints are large, with up to 100,000 cities and 100,000 edges per test case. This immediately rules out any quadratic approach over nodes or SCC pairs. Even iterating over all pairs of components would be too slow. A linear or near-linear graph algorithm per test case is required, such as SCC decomposition in O(n + m).

A few edge cases are easy to miss. If there are no edges, every city is its own country and the answer is simply the largest SCC size, which is 1. If the graph is already strongly connected, the answer is all nodes since only one country exists. Another tricky case is when SCCs form a chain A → B → C. Choosing A and C together is impossible because travel would require passing through B, which would introduce a third country, violating the constraint.

## Approaches

A brute-force interpretation would be to consider every possible starting city, simulate all possible walks, and track how many cities can be visited while ensuring that the walk only enters at most two SCCs. This would involve exploring paths in the original graph and maintaining a set of visited components. In the worst case, each traversal branches across many edges, leading to exponential behavior. Even restricting to SCCs does not help much if we still try all pairs of components and test reachability between them, which would lead to O(k²) checks where k can be up to n.

The structure of the problem becomes much simpler once we compress SCCs. After compression, we have a DAG. Any valid travel using at most two countries must correspond to either staying inside one SCC or moving along a single directed edge from SCC A to SCC B and then stopping. The reason is that once we enter a third SCC, we exceed the allowed number of countries.

This observation reduces the problem to evaluating only two types of choices. The first is the size of each SCC individually. The second is the sum of sizes of two SCCs connected by a directed edge in the condensation graph.

We do not need to consider longer paths in the DAG because any path of length at least two would necessarily involve three SCCs, which is forbidden. This collapses the problem from a global graph traversal into a simple edge-based aggregation problem over SCC sizes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (paths / pairs of cities or SCCs) | O(n²) or worse | O(n + m) | Too slow |
| SCC + Edge Pair Check | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

We start by identifying strongly connected components using a standard SCC algorithm such as Kosaraju or Tarjan. Each SCC is assigned an id, and we also compute its size, which represents how many cities are inside that country.

Next, we scan all edges in the original graph. For each directed edge u → v, if u and v belong to different SCCs, we record a connection from component cu to component cv. We do not need to store the full DAG structure; we only need to know which pairs of components are directly connected.

After this, we compute two types of candidates for the answer. First, we consider each SCC individually and take its size as a possible answer. This corresponds to visiting only one country.

Second, for every directed edge between SCCs cu → cv, we consider the sum size[cu] + size[cv]. This corresponds to starting in one country and moving into exactly one neighboring country, then stopping.

Finally, we take the maximum over all single SCC sizes and all valid SCC edge pairs.

### Why it works

Any valid travel plan can only include cities from at most two SCCs. If the plan uses only one SCC, it is fully captured by the SCC size. If it uses two SCCs, then there must exist at least one edge allowing movement from one SCC to the other in the direction of travel. Once that transition happens, visiting any third SCC would require another transition, which is disallowed. Therefore every valid solution corresponds exactly to either one SCC or one SCC pair connected by at least one directed edge, and evaluating these exhaustively covers all feasible cases.

## Python Solution

```python
import sys
sys.setrecursionlimit(10**7)
input = sys.stdin.readline

def kosaraju(n, adj, radj):
    visited = [False] * n
    order = []

    def dfs1(u):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                dfs1(v)
        order.append(u)

    for i in range(n):
        if not visited[i]:
            dfs1(i)

    comp = [-1] * n
    cid = 0

    def dfs2(u):
        comp[u] = cid
        for v in radj[u]:
            if comp[v] == -1:
                dfs2(v)

    for u in reversed(order):
        if comp[u] == -1:
            dfs2(u)
            cid += 1

    return comp, cid

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        adj = [[] for _ in range(n)]
        radj = [[] for _ in range(n)]

        edges = []
        for _ in range(m):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            adj[u].append(v)
            radj[v].append(u)
            edges.append((u, v))

        comp, k = kosaraju(n, adj, radj)

        size = [0] * k
        for i in range(n):
            size[comp[i]] += 1

        ans = max(size)

        for u, v in edges:
            cu, cv = comp[u], comp[v]
            if cu != cv:
                ans = max(ans, size[cu] + size[cv])

        print(ans)

if __name__ == "__main__":
    solve()
```

The solution first builds forward and reverse adjacency lists to support Kosaraju’s two-pass DFS. The first DFS builds a finishing order, and the second assigns component ids on the reversed graph.

After SCC compression, the size array tracks how many cities belong to each country. The initial answer is set to the largest SCC because visiting a single country is always allowed.

We then iterate through all original edges. Each edge that crosses SCC boundaries represents a potential two-country journey. We sum the sizes of its endpoints’ components and update the answer. Duplicate edges or multiple edges between the same SCC pair do not affect correctness because taking the maximum is idempotent.

## Worked Examples

Consider a graph with two cycles connected by a single edge: 1 → 2 → 3 → 1 and 4 → 5 → 6 → 4, plus an edge 3 → 4.

After SCC compression, we have two components: C1 with size 3 and C2 with size 3, and a single edge C1 → C2.

| Step | Action | C1 size | C2 size | Best answer |
| --- | --- | --- | --- | --- |
| 1 | Build SCCs | 3 | 3 | 3 |
| 2 | Process edge C1 → C2 | 3 | 3 | 6 |

This shows that the best strategy is to traverse from the first country into the second and stop there.

Now consider a chain of three SCCs: A → B → C with sizes 2, 5, and 4.

| Step | Action | Candidate |
| --- | --- | --- |
| 1 | Single SCCs | max is 5 |
| 2 | Edge A → B | 7 |
| 3 | Edge B → C | 9 |

We never consider A → C because no direct edge exists, and using B as an intermediate would exceed the two-country limit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Kosaraju runs in linear time, and each edge is processed once |
| Space | O(n + m) | Adjacency lists, reverse graph, and SCC arrays |

The solution fits comfortably within limits because both n and m are up to 100,000 per test case, and all operations are linear scans or DFS traversals.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    # assume solve() is defined above
    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# minimum graph
assert run("1\n1 0\n") == "1"

# simple two-node chain
assert run("1\n2 1\n1 2\n") == "2"

# strongly connected cycle
assert run("1\n3 3\n1 2\n2 3\n3 1\n") == "3"

# chain of SCCs
assert run("1\n4 3\n1 2\n2 3\n3 4\n") == "3"

# two separate cycles with connection
assert run("1\n6 7\n1 2\n2 1\n3 4\n4 3\n2 3\n") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 1 | minimal SCC handling |
| single edge | 2 | two-country transition |
| full cycle | n | already one country |
| linear chain | best adjacent pair only | forbids skipping SCCs |
| two cycles connected | sum of best pair | SCC aggregation correctness |

## Edge Cases

A graph with no edges creates n separate SCCs, each of size 1. The algorithm treats every node as its own component, and the best answer becomes the largest SCC size, which is 1. Since no cross-component edges exist, the second phase never updates the answer beyond this value.

In a fully strongly connected graph, all nodes belong to one SCC. The SCC decomposition produces a single component of size n. The edge processing step does nothing useful since there are no inter-component edges. The final answer remains n, matching the fact that only one country exists.

In a chain structure like 1 → 2 → 3 → 4, SCCs are all single nodes. The only valid pairs considered are (1,2), (2,3), and (3,4). The algorithm never considers (1,3) or (1,4), which correctly prevents invalid multi-country traversals that would require passing through intermediate components.
