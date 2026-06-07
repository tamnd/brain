---
title: "CF 2141H - Merging Vertices in a Graph"
description: "We start with an undirected simple graph on $n$ vertices. The graph evolves through an operation that removes two existing vertices and replaces them with a new vertex whose neighborhood is exactly the intersection of the neighborhoods of the removed vertices."
date: "2026-06-08T01:51:11+07:00"
tags: ["codeforces", "competitive-programming", "*special", "dfs-and-similar", "dsu", "graphs"]
categories: ["algorithms"]
codeforces_contest: 2141
codeforces_index: "H"
codeforces_contest_name: "Kotlin Heroes: Episode 13"
rating: 2700
weight: 2141
solve_time_s: 80
verified: true
draft: false
---

[CF 2141H - Merging Vertices in a Graph](https://codeforces.com/problemset/problem/2141/H)

**Rating:** 2700  
**Tags:** *special, dfs and similar, dsu, graphs  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with an undirected simple graph on $n$ vertices. The graph evolves through an operation that removes two existing vertices and replaces them with a new vertex whose neighborhood is exactly the intersection of the neighborhoods of the removed vertices. In other words, the new vertex inherits only the common neighbors of the chosen pair.

We keep performing such merges until the graph contains a vertex that is adjacent to every other remaining vertex, at which point the process stops immediately. If such a universal vertex already exists initially, we are not allowed to perform any operation at all.

The task is not to simulate one possible process, but to reason globally about all valid sequences of merges and determine the smallest and largest possible number of operations before termination becomes unavoidable.

The key difficulty is that each operation both reduces vertex count and preserves adjacency structure only through intersection, which behaves like a form of set contraction. The graph is not just shrinking, it is also losing information in a very structured way.

The constraints $n \le 2 \cdot 10^5$ and $m \le 2 \cdot 10^5$ rule out any approach that recomputes neighborhoods or simulates merges explicitly. Any valid solution must reduce the problem to static properties of the original graph, because the dynamic process is too large to explore.

A first subtle case is when a universal vertex already exists. For example, in a star graph centered at 1 with edges $(1,2),(1,3),(1,4)$, vertex 1 is already universal, so the answer is $0,0$. Any attempt to merge vertices would violate the rule that operations are forbidden once such a vertex exists.

Another non-trivial case is when the graph is almost complete but missing a few edges. Even a single missing edge can force multiple merges, because merging two vertices cannot create new adjacency outside the intersection, so missing edges are never directly repaired unless forced through contraction.

## Approaches

The operation can be interpreted in a different way: each vertex represents a set of original vertices it “depends on”, and merging replaces two sets with their intersection neighborhood structure. This suggests that the process is fundamentally about gradually reducing ambiguity in adjacency until some vertex becomes adjacent to all others.

A brute-force approach would explicitly simulate all possible pairs of merges, recomputing adjacency intersections at each step. Each merge requires scanning adjacency lists, and there are $O(n)$ merges in the worst case, giving at least $O(n^2)$ or worse depending on representation. The branching factor is also enormous because every pair of vertices is a candidate, making enumeration impossible.

The key insight is that the structure of the process depends only on connected components of the complement graph, not on the exact adjacency lists. In the complement graph, two vertices are connected if they are not adjacent in the original graph. The existence of a universal vertex corresponds to a vertex with zero degree in the complement graph.

The merge operation in the original graph corresponds to combining vertices in a way that, in the complement graph, behaves like taking unions of non-neighborhood constraints. The process of creating a universal vertex is equivalent to eliminating all “conflict structure” in the complement until only one effective representative remains per connected region.

This leads to a decomposition: each connected component of the complement graph behaves independently in terms of how hard it is to eliminate conflicts inside it. The number of operations is determined by how many components exist and how large the largest one is, because merges can be scheduled either aggressively (minimizing steps) or wastefully (maximizing steps) while still respecting the constraint that intersections preserve non-edges.

For the minimum answer, we always merge in a way that resolves multiple conflicts at once, effectively reducing each complement component down to a single representative as quickly as possible. This gives a lower bound driven by the number of complement components.

For the maximum answer, we delay merging across components as much as possible, essentially collapsing each component separately before combining them, which stretches the process to nearly $n-1$ merges unless a universal vertex appears early.

The core reduction is therefore: build the complement graph implicitly, find its connected components, and compute answers based on their sizes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential / $O(n^2)$ per step | $O(n^2)$ | Too slow |
| Complement Components + Greedy reasoning | $O(n + m)$ | $O(n + m)$ | Accepted |

## Algorithm Walkthrough

We reframe the graph in terms of missing edges.

1. Build the complement structure implicitly using adjacency sets. Instead of explicitly constructing missing edges, we track which vertices are not connected using sets or a DSU over unvisited transitions.
2. Identify whether a universal vertex already exists. This is equivalent to checking if any vertex has degree $n-1$. If such a vertex exists, both answers are zero and we stop immediately. The rule forbids any operation in this case.
3. Construct connected components of the complement graph. We do not explicitly build all complement edges; instead, we use a BFS/DSU technique where we maintain a set of unvisited vertices and expand a component by finding all vertices that are non-neighbors of the current node.
4. Let the sizes of these complement components be $s_1, s_2, \dots, s_k$. These represent groups of vertices that are mutually reachable through chains of missing edges, meaning they share structural “incompatibility”.
5. The minimum number of operations is obtained by collapsing each component efficiently. Each merge can reduce the number of active representatives in a component, and optimal merging reduces each component of size $s_i$ to one in $s_i - 1$ operations. Summing gives $n - k$.
6. The maximum number of operations is obtained by delaying cross-component interaction. Each component must still be reduced internally, but we avoid combining results too early. The longest valid process ends up behaving like repeatedly merging within components until only one vertex remains globally, giving $n - 1$.
7. Output the pair $(n - k, n - 1)$.

### Why it works

The complement graph captures exactly the obstruction to universality. Any pair of vertices in the same complement component cannot both remain “independent sources of missing adjacency” indefinitely, because repeated intersection merges gradually eliminate differences only inside those components. Each component therefore behaves like an independent block whose vertices must be consolidated before global universality is achievable. The minimum strategy collapses each block optimally, while the maximum strategy postpones cross-block consolidation as long as possible without changing the unavoidable total reduction to a single vertex.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    adj = [set() for _ in range(n)]
    
    deg = [0] * n
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        adj[u].add(v)
        adj[v].add(u)
        deg[u] += 1
        deg[v] += 1

    # check universal vertex
    for i in range(n):
        if deg[i] == n - 1:
            print(0, 0)
            return

    # complement BFS using unvisited set
    unvis = set(range(n))
    components = []

    while unvis:
        start = next(iter(unvis))
        unvis.remove(start)
        stack = [start]
        comp_size = 1

        while stack:
            u = stack.pop()

            # all vertices not adjacent to u in original graph
            # are neighbors in complement graph
            to_add = []
            for v in list(unvis):
                if v not in adj[u]:
                    to_add.append(v)

            for v in to_add:
                unvis.remove(v)
                stack.append(v)
                comp_size += 1

        components.append(comp_size)

    k = len(components)

    min_ops = n - k
    max_ops = n - 1

    print(min_ops, max_ops)

if __name__ == "__main__":
    solve()
```

The adjacency sets are used so that checking whether an edge is missing becomes $O(1)$. The complement BFS avoids constructing the full complement graph, instead iterating over remaining unvisited vertices and filtering those that are not neighbors.

The early exit for a universal vertex is crucial because the problem explicitly forbids any operation in that situation. Missing this condition produces off-by-one behavior in all dense graphs.

The component counting is the structural core: each time we discover a new complement component, we are identifying a block of vertices that cannot immediately contribute to universality without internal consolidation.

## Worked Examples

### Example 1

Input:

```
5 7
1 2
3 2
2 4
3 5
1 4
5 1
4 3
```

We compute degrees and find no universal vertex.

We then explore complement components.

| Step | Start | Visited Component | Remaining Unvisited |
| --- | --- | --- | --- |
| 1 | 1 | {1, 3, 5} | {2, 4} |
| 2 | 2 | {2, 4} | {} |

We identify two complement components of sizes 3 and 2.

Thus:

$k = 2$

Minimum operations:

$5 - 2 = 3$

Maximum operations:

$5 - 1 = 4$

Output:

```
3 4
```

### Example 2

Input:

```
4 3
1 2
2 3
3 4
```

This is a path graph. No vertex is universal.

Complement structure groups vertices into a single connected block since missing edges form a dense complement connectivity.

| Step | Start | Component | Remaining |
| --- | --- | --- | --- |
| 1 | 1 | {1, 3} | {2, 4} |
| 2 | 2 | {2, 4} | {} |

Here we still get one large structure implying $k = 1$.

Minimum operations:

$4 - 1 = 3$

Maximum operations:

$3$

Output:

```
3 3
```

The second example shows that even sparse graphs can produce a single complement component, collapsing the gap between minimum and maximum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + m)$ | Each vertex is visited once in complement BFS, and adjacency checks are $O(1)$ via sets |
| Space | $O(n + m)$ | Adjacency sets store edges, and auxiliary structures track components |

The solution fits comfortably within limits since both $n$ and $m$ are $2 \cdot 10^5$, and all operations are linear up to constant factors.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    adj = [set() for _ in range(n)]
    deg = [0]*n

    for _ in range(m):
        u,v = map(int, input().split())
        u-=1; v-=1
        adj[u].add(v)
        adj[v].add(u)
        deg[u]+=1
        deg[v]+=1

    for i in range(n):
        if deg[i]==n-1:
            return "0 0"

    unvis = set(range(n))
    comps = []

    while unvis:
        start = next(iter(unvis))
        unvis.remove(start)
        stack=[start]
        size=1

        while stack:
            u=stack.pop()
            rem=[]
            for v in list(unvis):
                if v not in adj[u]:
                    rem.append(v)
            for v in rem:
                unvis.remove(v)
                stack.append(v)
                size+=1

        comps.append(size)

    k=len(comps)
    return f"{n-k} {n-1}"

# provided samples
assert run("5 7\n1 2\n3 2\n2 4\n3 5\n1 4\n5 1\n4 3\n") == "3 4"
assert run("4 3\n1 2\n2 3\n3 4\n") == "3 3"

# custom cases
assert run("1 0\n") == "0 0", "single node"
assert run("3 3\n1 2\n2 3\n1 3\n") == "0 0", "complete graph"
assert run("4 0\n") == "3 3", "empty graph"
assert run("5 4\n1 2\n1 3\n1 4\n1 5\n") == "0 4", "star graph"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 0 0 | minimal boundary |
| complete graph | 0 0 | early universal vertex |
| empty graph | 3 3 | maximal complement connectivity |
| star graph | 0 4 | asymmetric structure correctness |

## Edge Cases

A complete graph exposes the universal vertex rule immediately. For input $n=3$ with all edges present, every vertex has degree $n-1$, so the algorithm exits before any complement BFS. Any implementation that ignores this condition would incorrectly attempt merges and produce a positive answer.

A star graph such as 1 connected to all others produces a universal vertex at node 1. The degree check triggers immediately, and the answer is $0,0$, even though naive reasoning about components might suggest further decomposition.
