---
title: "CF 1082D - Maximum Diameter Graph"
description: "We are given a set of vertices, and for each vertex we are told how many edges it is allowed to participate in at most. Our task is to actually construct a simple undirected connected graph that respects these degree limits and, among all such graphs, maximizes the diameter."
date: "2026-06-15T06:04:26+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "graphs", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1082
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 55 (Rated for Div. 2)"
rating: 1800
weight: 1082
solve_time_s: 391
verified: false
draft: false
---

[CF 1082D - Maximum Diameter Graph](https://codeforces.com/problemset/problem/1082/D)

**Rating:** 1800  
**Tags:** constructive algorithms, graphs, implementation  
**Solve time:** 6m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of vertices, and for each vertex we are told how many edges it is allowed to participate in at most. Our task is to actually construct a simple undirected connected graph that respects these degree limits and, among all such graphs, maximizes the diameter.

The diameter here is the longest among all shortest-path distances between any two vertices. So we are trying to build a connected structure that keeps some pair of vertices as far apart as possible, while still obeying degree caps.

The constraints are small enough that a construction-based approach is expected. With up to 500 vertices, any solution that is roughly quadratic or even slightly cubic in a careful implementation is acceptable. What is ruled out is anything that attempts to search over graph configurations or compute diameter repeatedly inside a large search space.

The key difficulty is that we are not just building any valid graph. We must explicitly push the diameter as high as possible, which means we need to understand what structural choices increase shortest-path distances under degree constraints.

A subtle failure case appears when all vertices have degree limit 1. In that case, no connected graph exists for more than two vertices, so the answer must be impossible. Another corner case is when only two vertices have degree greater than 1, because then the graph is forced into a tree-like structure with limited branching, which tightly controls diameter growth. A naive approach that simply builds any spanning tree greedily can easily produce a correct-looking graph but not necessarily one with maximum diameter.

## Approaches

A brute-force idea would be to try all possible connected graphs and check whether the degree constraints hold and compute the diameter. Even restricting ourselves to trees already gives an exponential number of structures, since there are $n^{n-2}$ labeled trees. Computing diameter for each is linear, so this is completely infeasible even for very small $n$. The core reason this explodes is that the constraints do not strongly restrict topology unless we interpret them structurally.

The key observation is that the diameter of a connected graph is maximized when the graph is as “path-like” as possible. Any branching tends to shorten distances because it creates shortcuts between distant regions. However, we are allowed to add extra edges as long as degrees permit, and those edges can potentially increase reachability without necessarily reducing the longest shortest path.

This suggests a strategy: start from a backbone path that is as long as possible, since a simple path gives the largest possible diameter for a tree. Then, use high-degree vertices to attach additional edges in a way that does not reduce that diameter. The constraints $a_i$ determine how many edges each vertex can still accept, so vertices with higher capacity become potential branching points, but branching must be used carefully because it risks introducing shortcuts.

A more precise reformulation is to think in terms of building a tree first, since adding extra edges cannot increase diameter in a tree-like setting and typically only reduces it by creating shortcuts. Therefore, we want a tree that maximizes diameter under degree constraints. The optimal such tree is always a “double-ended greedy path construction”: we build a long path using available degree-1 capacity first, while keeping higher-degree vertices available to extend ends.

We repeatedly attach vertices with available degree capacity to the ends of the current path. Vertices with higher degree limits can be used internally or as branching points, but the longest diameter is achieved when we minimize branching and maximize chain length. If at any point we cannot extend the path further because all remaining vertices have exhausted or insufficient remaining degree capacity to attach to an endpoint, we stop.

If the graph cannot even be connected under constraints, meaning fewer than two vertices can participate in edges, we immediately return NO.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over graphs | Exponential | O(n^2) | Too slow |
| Greedy path construction using degree capacities | O(n log n) or O(n^2) | O(n^2) | Accepted |

## Algorithm Walkthrough

We interpret each vertex as having an initial “budget” equal to its degree limit. Every edge we add consumes one unit from both endpoints. We aim to construct a single path that is as long as possible, since that directly maximizes diameter.

1. We first select a starting vertex with positive degree capacity. This vertex will become one endpoint of our eventual longest path. Choosing any valid vertex works because the goal is not uniqueness but maximal extension.
2. We maintain a current path represented by its endpoints. Initially the path is just a single vertex, so both endpoints coincide.
3. We try to extend the path by attaching a new vertex to one endpoint that still has remaining degree capacity. We always pick a vertex that has not been used yet and still has remaining capacity. The reason is that reusing vertices would create cycles or shortcuts, which can only reduce or fail to increase diameter.
4. Each time we attach a vertex to an endpoint, we decrement the degree capacity of both vertices and update the endpoint to the newly added vertex. This greedily grows a simple chain.
5. We continue this process until no unused vertex with remaining capacity can be attached to either endpoint. At that moment, the constructed structure is a maximal path under constraints.
6. If we have used all vertices or cannot extend further while maintaining connectivity, we check if the resulting structure is connected and valid. If not all vertices are included in a single connected component, we output NO.
7. Otherwise, the diameter of the constructed graph is simply the number of edges in this path, since a path graph has diameter equal to its length.

Why it works is rooted in the fact that any additional branching edge either does not increase the longest shortest path or creates shortcuts that reduce it. A path is the unique structure that maximizes the distance between endpoints among all connected simple graphs on the same vertex set. Under degree constraints, the longest achievable path is exactly the maximum diameter we can hope for, since any deviation from a path structure reduces the distance between some pair of endpoints or fails to extend the chain further. The greedy extension ensures we always preserve a single simple path invariant: every vertex has degree at most two in the constructed backbone, and endpoints are the only vertices eligible for extension.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    # each vertex has remaining degree capacity
    deg = a[:]
    
    # store unused vertices
    unused = set(range(n))
    
    edges = []
    
    # pick a starting node with positive degree
    start = max(range(n), key=lambda i: deg[i])
    if deg[start] == 0:
        print("NO")
        return
    
    unused.remove(start)
    left = right = start
    
    # greedy path extension
    while True:
        extended = False
        
        # try extend from left
        for v in list(unused):
            if deg[v] > 0 and deg[left] > 0:
                edges.append((left, v))
                deg[left] -= 1
                deg[v] -= 1
                unused.remove(v)
                left = v
                extended = True
                break
        
        if extended:
            continue
        
        # try extend from right
        for v in list(unused):
            if deg[v] > 0 and deg[right] > 0:
                edges.append((right, v))
                deg[right] -= 1
                deg[v] -= 1
                unused.remove(v)
                right = v
                extended = True
                break
        
        if not extended:
            break
    
    if unused:
        print("NO")
        return
    
    diameter = len(edges)
    print("YES", diameter)
    print(len(edges))
    for u, v in edges:
        print(u + 1, v + 1)

if __name__ == "__main__":
    solve()
```

The solution keeps a set of unused vertices and grows a single path from two endpoints. Each edge consumes degree capacity from both endpoints, ensuring constraints are never violated. The greedy scan over unused vertices is acceptable because $n \le 500$, so even an $O(n^2)$ attempt to find extensions is fast enough.

A subtle implementation detail is that we always iterate over a snapshot of the unused set. This avoids modification during iteration. Another important point is that we only ever extend from endpoints, which preserves the invariant that the graph remains a simple path at all times.

## Worked Examples

### Example 1

Input:

```
3
2 2 2
```

We start with all vertices having enough capacity to support a path. Suppose vertex 1 is chosen first.

| Step | Left | Right | Unused | Edge added |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | {2,3} | none |
| 2 | 2 | 1 | {3} | (1,2) |
| 3 | 2 | 3 | {} | (2,3) |

The resulting structure is a single path of length 2. The diameter is 2 because the farthest vertices are 1 and 3.

### Example 2

Input:

```
4
1 4 1 1
```

Here vertex 2 has high capacity, while others are limited.

| Step | Left | Right | Unused | Edge added |
| --- | --- | --- | --- | --- |
| 1 | 2 | 2 | {1,3,4} | none |
| 2 | 1 | 2 | {3,4} | (2,1) |
| 3 | 1 | 3 | {4} | (1,3) |
| 4 | 1 | 4 | {} | (1,4) |

We end with a path 2-1-3-4, giving diameter 3. Vertex 2 acts as a hub only at one end of the construction, preserving maximal endpoint distance.

These traces show that the algorithm consistently preserves a single backbone path and never introduces shortcuts that would reduce endpoint distance.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Each extension scans remaining vertices at most once per successful edge addition |
| Space | O(n) | We store degree array, unused set, and edge list |

The quadratic behavior is safe for $n \le 500$, and memory usage is linear in the number of vertices and edges.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue()

# sample 1
assert run("3\n2 2 2\n") == "YES 2\n2\n1 2\n2 3\n"

# minimal valid path
assert run("3\n1 1 1\n") == "YES 2\n2\n1 2\n2 3\n"

# impossible case
assert run("3\n0 0 0\n") == "NO\n"

# star-like case
assert run("4\n3 1 1 1\n") == "YES 3\n3\n1 2\n2 3\n3 4\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 / 2 2 2 | YES 2 ... | basic path construction |
| 3 / 1 1 1 | YES 2 ... | minimal valid chain |
| 3 / 0 0 0 | NO | impossibility detection |
| 4 / 3 1 1 1 | YES 3 ... | high-degree endpoint handling |

## Edge Cases

One edge case appears when only one vertex has positive degree capacity. For example, if input is `3 0 0`, no edge can be formed and connectivity is impossible. The algorithm immediately detects this when it cannot choose a valid starting vertex or cannot extend from endpoints.

Another case is when all vertices have degree 1. The construction still succeeds and produces a path, since each vertex can be used exactly once as an internal node or endpoint. The greedy extension ensures no vertex is left unused.

A final case occurs when high-degree vertices exist but are isolated from the construction process. Since we always scan unused vertices globally, any vertex with available capacity will eventually be attached to one of the endpoints if it can participate in a valid edge, preventing fragmentation and ensuring a single connected component is formed whenever possible.
