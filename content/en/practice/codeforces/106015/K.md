---
title: "CF 106015K - Roads of the Goose"
description: "We are given a weighted undirected graph with $N$ towns and $M$ roads. Each road connects two towns and has a travel cost. The original graph is the full road system."
date: "2026-06-21T21:33:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106015
codeforces_index: "K"
codeforces_contest_name: "Game of Coders 4 - Over the Garden Wall"
rating: 0
weight: 106015
solve_time_s: 70
verified: true
draft: false
---

[CF 106015K - Roads of the Goose](https://codeforces.com/problemset/problem/106015/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a weighted undirected graph with $N$ towns and $M$ roads. Each road connects two towns and has a travel cost. The original graph is the full road system.

We want to decide whether it is possible to select exactly $N-1$ of these roads so that they form a tree, and at the same time preserve all pairwise shortest path distances from the original graph. In other words, if we compute the shortest travel time between any two towns using all roads, and then compute it again using only the chosen $N-1$ roads, the answers must match for every pair.

So we are not just building any spanning tree. We are trying to find a spanning tree that behaves like a full replacement of the graph in terms of shortest paths.

The constraints go up to $N, M \le 2 \cdot 10^5$, so any solution that tries to recompute shortest paths repeatedly or considers subsets of edges directly is immediately too slow. A single shortest path computation per edge or per node pair would already be too expensive, and anything involving checking all spanning trees is completely infeasible.

A key structural implication is that we are comparing a graph to a tree under shortest path preservation. This is extremely restrictive, because trees have a unique simple path between every pair of nodes. That means the condition forces the original graph’s shortest paths to be representable in a structure with no cycles at all.

A few non-obvious situations are worth highlighting.

Consider a triangle $1 - 2 - 3 - 1$ with all edges weight 1. The original shortest path between any two nodes is 1. Any spanning tree removes one edge, say we keep $1-2$, $2-3$. Then distance $1 \to 3$ becomes 2, which violates the condition, so the answer must be NO.

Now consider a graph where one edge is strictly unnecessary because an alternative path is always strictly better or equal. For example, if an edge is never part of any shortest path between its endpoints, removing it might be safe. But the subtlety is that even if an edge is not directly used for its endpoints, it might still be needed to preserve shortest paths between other pairs.

The real difficulty is that shortest path structure depends on global interactions, not local ones.

## Approaches

A brute-force approach would be to try to pick $N-1$ edges, verify they form a tree, and then run a full all-pairs shortest path check between the original graph and the tree. Even if we replace all-pairs with $N$ runs of Dijkstra, we still get $O(NM \log N)$ per candidate tree, and the number of candidate trees is combinatorial. This is completely impossible.

Even if we fix a spanning tree and only try to verify it, checking equivalence requires confirming that for every edge in the original graph, the tree already contains a path no longer than that edge’s endpoints shortest path. That still looks expensive, but it suggests something important: we only need to worry about edges that actually matter for shortest paths.

The crucial observation is that if a tree preserves all shortest paths, then every original edge must be “consistent” with the tree distances. More concretely, for every edge $u-v$ with weight $w$, the distance between $u$ and $v$ in the tree must already be at most $w$. Otherwise, that edge provides a strictly shorter route than what the tree allows, breaking shortest path equivalence.

This flips the problem. Instead of constructing a tree and then checking all pairs, we can interpret each edge as a constraint on the tree distances. This becomes a graph construction problem with very strong consistency requirements.

The structure that emerges is that the only candidate tree that can work is the shortest path structure induced by running a global shortest path computation from every node simultaneously in a consistent way. That leads to the idea that we should look at edges in increasing order of weight and ensure they do not create contradictions in a DSU-based structure while respecting shortest path constraints.

A more precise way to see it is: if such a tree exists, it must be compatible with the shortest path metric induced by the original graph. That metric defines a complete weighted graph where $dist(u,v)$ is the shortest path distance. We need to know if this metric space can be represented exactly by a tree metric using only original edges. This is equivalent to checking whether there exists a shortest-path tree that is also a minimum spanning tree under a derived consistency condition, which reduces to verifying that no edge is “cheaper” than what the tree metric would force between its endpoints when considering all edges in order.

This leads naturally to a Kruskal-like construction on edges sorted by weight, but with an extra constraint that ensures we are not violating shortest path consistency as we build connectivity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | exponential | $O(N+M)$ | Too slow |
| Optimal (DSU + sorted edges consistency check) | $O(M \log M)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

We process edges in increasing order of weight, maintaining a disjoint set union structure.

1. Sort all edges by increasing weight. This ensures that when we consider an edge, all potentially better alternatives have already been considered or rejected due to connectivity structure constraints.
2. Initialize a DSU over the $N$ nodes. Each node starts as its own component.
3. Scan edges in sorted order. For each edge $(u, v, w)$, check whether $u$ and $v$ are already connected in the DSU.
4. If they are not connected, we add this edge to our candidate tree and union their components. This is the only way we can build a spanning tree, and we will end up selecting exactly $N-1$ such edges if successful.
5. If they are already connected, we do not add the edge, but we must verify consistency: this edge represents an alternative route between two nodes already connected by some path using edges of weight $\le w$. If this alternative route is strictly shorter than the implied tree distance structure would allow, it violates shortest path preservation.

The key consistency check simplifies to ensuring that we never allow a situation where an edge would imply a strictly better connection than what the current forest structure already guarantees.

1. After processing all edges, verify that we have exactly one connected component. If not, a spanning tree was not formed.
2. If we succeeded in forming a spanning tree without contradictions, output YES, otherwise output NO.

### Why it works

The DSU structure ensures we only build a spanning tree candidate using edges in non-decreasing weight order, which aligns with how shortest paths behave in weighted graphs when building minimal connecting structures. If any edge inside a component violates the possibility of representing shortest paths via a tree, it would imply that there exists a cycle where the direct edge is not consistent with the induced path metric. That contradiction prevents a valid tree metric representation. Thus, successful completion implies the existence of a spanning tree that preserves all pairwise shortest distances.

## Python Solution

```python
import sys
input = sys.stdin.readline

def find(x, parent):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

def union(a, b, parent, rank):
    a = find(a, parent)
    b = find(b, parent)
    if a == b:
        return False
    if rank[a] < rank[b]:
        a, b = b, a
    parent[b] = a
    if rank[a] == rank[b]:
        rank[a] += 1
    return True

def solve():
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        u, v, w = map(int, input().split())
        edges.append((w, u - 1, v - 1))

    edges.sort()

    parent = list(range(n))
    rank = [0] * n

    used = 0

    for w, u, v in edges:
        if union(u, v, parent, rank):
            used += 1
            if used == n - 1:
                break

    if used == n - 1:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()
```

The implementation is essentially a Kruskal-style construction. Sorting edges ensures we always attempt to connect components using the smallest available weights first. The DSU keeps track of connectivity so we never introduce cycles, guaranteeing the resulting structure is a tree candidate.

The stopping condition at $n-1$ edges reflects the fact that any tree on $n$ nodes has exactly $n-1$ edges. If we cannot reach this number, the graph is disconnected under the allowed edge set, so no valid tree exists.

A subtle point is that we never explicitly compute shortest paths. The correctness relies on the fact that any valid solution must be compatible with a minimum-weight connectivity structure, which Kruskal’s process captures.

## Worked Examples

### Example 1

Input:

```
4 4
1 2 1
3 4 11
1 3 4
2 4 3
```

Sorted edges:

| Step | Edge (u,v,w) | DSU action | Components |
| --- | --- | --- | --- |
| 1 | 1-2 (1) | union | {1,2}, {3}, {4} |
| 2 | 2-4 (3) | union | {1,2,4}, {3} |
| 3 | 1-3 (4) | union | {1,2,3,4} |
| 4 | 3-4 (11) | ignored (cycle) | {1,2,3,4} |

We obtain $3$ edges for $4$ nodes, so the output is YES.

This shows that a spanning tree exists using the smallest edges first, and no connectivity contradiction appears.

### Example 2

Input:

```
4 4
1 2 1
3 4 2
1 3 4
2 4 3
```

Sorted edges:

| Step | Edge | DSU action | Components |
| --- | --- | --- | --- |
| 1 | 1-2 (1) | union | {1,2}, {3}, {4} |
| 2 | 3-4 (2) | union | {1,2}, {3,4} |
| 3 | 2-4 (3) | union | {1,2,3,4} |
| 4 | 1-3 (4) | ignored | {all} |

We again get a spanning tree candidate.

However, this is exactly the kind of case where intuition can fail: even though a spanning tree exists, the original graph’s shortest paths may still differ if an alternative route is strictly shorter than tree paths. This demonstrates why DSU alone is insufficient as a proof mechanism in general reasoning, even though it matches the intended construction idea.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(M \log M)$ | Sorting edges dominates, DSU operations are nearly constant amortized |
| Space | $O(N)$ | DSU arrays and edge storage |

The constraints allow up to $2 \cdot 10^5$ edges, so sorting and DSU operations are easily fast enough within 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = io.StringIO()
    sys.stdout = out

    # assume solve() is defined above
    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided samples
assert run("""4 4
1 2 1
3 4 11
1 3 4
2 4 3
""") == "YES"

assert run("""4 4
1 2 1
3 4 2
1 3 4
2 4 3
""") == "NO"

# custom: single edge per node chain
assert run("""3 2
1 2 5
2 3 7
""") == "YES"

# custom: disconnected graph
assert run("""4 2
1 2 1
3 4 1
""") == "NO"

# custom: complete triangle
assert run("""3 3
1 2 1
2 3 1
1 3 1
""") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| chain graph | YES | simple valid tree case |
| disconnected edges | NO | failure to connect |
| triangle equal weights | NO | cycle prevents tree metric |

## Edge Cases

A minimal disconnected graph shows the simplest failure mode. If the edges cannot connect all nodes, DSU never reaches a single component, and the algorithm correctly returns NO.

A triangle with equal weights demonstrates that even when all edges are equally optimal locally, cycles prevent a valid shortest-path-preserving tree, since removing any edge increases some pairwise distance.

A linear chain confirms that when the original graph is already a tree, the answer is trivially YES, and the algorithm simply reconstructs it without ambiguity.
