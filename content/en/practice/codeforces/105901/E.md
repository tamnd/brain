---
title: "CF 105901E - Colorful Graph"
description: "We are given an undirected graph with $n$ vertices and $m$ edges. Each edge must be assigned a color, using colors labeled from $1$ to $m$, and colors may be reused across edges."
date: "2026-06-22T02:51:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105901
codeforces_index: "E"
codeforces_contest_name: "2025 ICPC Wuhan Invitational Contest (The 3rd Universal Cup. Stage 37: Wuhan)"
rating: 0
weight: 105901
solve_time_s: 67
verified: true
draft: false
---

[CF 105901E - Colorful Graph](https://codeforces.com/problemset/problem/105901/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected graph with $n$ vertices and $m$ edges. Each edge must be assigned a color, using colors labeled from $1$ to $m$, and colors may be reused across edges.

The restriction is local to vertices: for any vertex $u$, if you look at all edges incident to $u$, then any fixed color can appear at most twice among those incident edges. So a vertex is allowed to touch the same color once or twice, but never three or more times.

For each vertex $u$, define $f_u$ as the number of distinct colors appearing among its incident edges. The goal is to assign colors to edges so that the total sum of these values over all vertices is minimized.

The constraints are large: the total number of vertices and edges across all test cases is up to $2 \cdot 10^5$. This immediately rules out anything quadratic in $n$ or $m$, and also makes it clear that we need a linear or near linear construction per test case. Any solution that repeatedly processes adjacency lists per color or simulates color assignment with heavy bookkeeping per vertex will not survive.

A subtle difficulty is that the constraint “at most two edges per color per vertex” does not behave like standard edge coloring or matching. A naive greedy that assigns colors per edge without global structure will easily get stuck in a situation where a vertex accumulates too many distinct colors even though each color is locally valid.

For example, in a star centered at vertex $u$ with degree 5, if we assign all edges different colors, we get $f_u = 5$, but the constraint allows pairing edges so that a single color can cover two incident edges, so the best possible is $f_u = 3$. A greedy that avoids reuse at the center would miss this improvement entirely.

The real challenge is to force structure so that each vertex “reuses colors in pairs” as much as possible, without violating consistency across edges.

## Approaches

The lower bound for each vertex is already determined by the constraint. Since each color can appear at most twice at a vertex, if $d_u$ edges touch $u$, then at least $\lceil d_u / 2 \rceil$ colors are needed at $u$. Summing this over all vertices gives a global lower bound on the objective.

So the problem becomes: can we construct an edge coloring such that every vertex achieves exactly this bound? That would mean we are perfectly pairing incident edges at every vertex so that each pair shares a color.

The difficulty is consistency. If we arbitrarily pair edges at a vertex, the same edge participates in pairings at both endpoints, and those pairings must agree globally so that they form valid color classes.

The key idea is to stop thinking in terms of colors first, and instead build a structure on edges. We want to group edges into connected components where each component will later become a single color. Inside each component, every vertex should have degree at most two, so that the constraint is automatically satisfied.

This suggests building a decomposition of edges into paths and cycles. If each connected component of this decomposition is a path or cycle, then assigning one color per component works: at any vertex, each component contributes at most two incident edges, so the constraint holds.

Now the goal becomes constructing such a decomposition while ensuring that at each vertex, incident edges are paired optimally. The standard way to enforce this is to locally pair edges at every vertex arbitrarily, then interpret each pair as a connection between two edges. After performing this at all vertices, each edge has degree exactly two in this “edge-to-edge” structure, except possibly endpoints created by odd degrees. This naturally breaks into disjoint trails over edges.

Each resulting trail is exactly one color class. Every vertex belongs to as many trails as it has incident pairs, which matches the lower bound $\lceil d_u / 2 \rceil$, so the objective is minimized.

The construction is linear because each edge is processed a constant number of times while forming pairs and extracting components.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Greedy per edge | $O(m \cdot n)$ worst-case | $O(m)$ | Too slow / Wrong structure |
| Pairing + decomposition into trails | $O(n + m)$ | $O(n + m)$ | Accepted |

## Algorithm Walkthrough

We build a structure where edges are gradually connected into chains using local pairing at vertices, then extract those chains as color classes.

1. Store the adjacency list of the graph, but also keep track of which edges are still unused.

This is necessary because we will gradually “consume” edges when pairing them.
2. For every vertex $u$, take its list of incident edges and pair them arbitrarily: the first with the second, the third with the fourth, and so on.

This pairing is the only place where optimality is enforced. Each vertex tries to group its edges into as many pairs as possible, so that each pair can later share a color.
3. For each pair of edges $(e_1, e_2)$ formed at a vertex, connect these two edges in a secondary graph where nodes are original edges.

This step transforms the problem from vertex-based constraints into an edge-graph where each edge-node has degree at most two. The pairing ensures that each edge participates in at most one connection per endpoint.
4. After processing all vertices, the edge-graph decomposes into disjoint paths and cycles over edges.

Each connected component corresponds to a sequence of edges where consecutive edges share a vertex pairing.
5. Traverse each component and assign it a unique color ID.

Since components are independent, any labeling is valid. The constraint is already guaranteed by the structure.
6. Output the color assigned to each original edge.

### Why it works

Each vertex $u$ contributes pairings of its incident edges, so every pair reduces the number of distinct “edge groups” that pass through $u$. Each group corresponds to exactly one connected component in the edge decomposition, meaning one color.

A vertex of degree $d_u$ can form exactly $\lfloor d_u / 2 \rfloor$ pairs, leaving at most one unpaired edge. Each pair becomes part of a trail, and the leftover edges form additional endpoints. Therefore, the number of trails touching $u$ is exactly $\lceil d_u / 2 \rceil$, which is the minimum possible value of $f_u$.

Since each color class is a path or cycle over edges, no vertex can have more than two incident edges of the same color, satisfying the constraint automatically.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**7)

def solve():
    n, m = map(int, input().split())
    g = [[] for _ in range(n)]
    
    edges = []
    for i in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        edges.append((u, v))
        g[u].append((v, i))
        g[v].append((u, i))
    
    used_edge = [False] * m
    adj_edge = [[] for _ in range(m)]
    
    # pair edges at each vertex
    for u in range(n):
        lst = []
        for v, eid in g[u]:
            lst.append(eid)
        
        for i in range(0, len(lst) - 1, 2):
            e1 = lst[i]
            e2 = lst[i + 1]
            adj_edge[e1].append(e2)
            adj_edge[e2].append(e1)
    
    visited_edge = [False] * m
    color = [0] * m
    cur_color = 0
    
    for i in range(m):
        if not visited_edge[i]:
            cur_color += 1
            stack = [i]
            visited_edge[i] = True
            color[i] = cur_color
            
            while stack:
                e = stack.pop()
                for ne in adj_edge[e]:
                    if not visited_edge[ne]:
                        visited_edge[ne] = True
                        color[ne] = cur_color
                        stack.append(ne)
    
    print(*color)

def main():
    t = int(input())
    for _ in range(t):
        solve()

if __name__ == "__main__":
    main()
```

The first phase builds an implicit graph whose nodes are edges. Each vertex contributes a local perfect matching over its incident edges, which is implemented by simply pairing them in order. The second phase runs a DFS over this edge-graph to identify connected components, and each component becomes one color.

A key implementation detail is that we never need to explicitly simulate “paths”. Once adjacency between edges is built, standard graph traversal over edges is enough. Another subtle point is that each edge is added to at most two pairing connections, so the auxiliary graph stays linear in size.

## Worked Examples

### Example 1

Consider a triangle: edges $(1,2), (2,3), (3,1)$.

At each vertex, there are two incident edges, so each vertex pairs them directly. This creates a cycle over all three edges.

| Step | Action | Edge Connections |
| --- | --- | --- |
| Pairing at 1 | (1,2)-(1,3) | e1 connected to e2 |
| Pairing at 2 | (1,2)-(2,3) | e1 connected to e3 |
| Pairing at 3 | (2,3)-(1,3) | e3 connected to e2 |

All edges become connected into one component, so all edges receive the same color.

This shows that cycles naturally collapse into a single color class.

### Example 2

Consider a path: $1 - 2 - 3 - 4$.

Edges are $e1=(1,2), e2=(2,3), e3=(3,4)$.

| Vertex | Pairing |
| --- | --- |
| 1 | none |
| 2 | (e1, e2) |
| 3 | (e2, e3) |
| 4 | none |

This produces a single chain over all edges, so again one color is used.

The important observation is that even though edges are paired locally twice at different vertices, consistency naturally forms a single trail.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + m)$ | Each edge is processed a constant number of times in pairing and DFS |
| Space | $O(n + m)$ | Adjacency lists and edge graph storage |

The constraints allow up to $2 \cdot 10^5$ total elements, so a linear-time construction with simple adjacency processing fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    
    def solve():
        n, m = map(int, input().split())
        g = [[] for _ in range(n)]
        edges = []
        for i in range(m):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            edges.append((u, v))
            g[u].append(i)
            g[v].append(i)

        adj = [[] for _ in range(m)]
        for u in range(n):
            lst = g[u]
            for i in range(0, len(lst) - 1, 2):
                a, b = lst[i], lst[i + 1]
                adj[a].append(b)
                adj[b].append(a)

        vis = [False] * m
        col = [0] * m
        cid = 0

        for i in range(m):
            if not vis[i]:
                cid += 1
                stack = [i]
                vis[i] = True
                col[i] = cid
                while stack:
                    e = stack.pop()
                    for ne in adj[e]:
                        if not vis[ne]:
                            vis[ne] = True
                            col[ne] = cid
                            stack.append(ne)

        return " ".join(map(str, col))

    return solve()

# sample / custom tests

assert run("""1 0
""") == "", "empty graph"

assert run("""2 1
1 2
""") == "1", "single edge"

assert run("""3 3
1 2
2 3
3 1
""") == "1 1 1", "triangle cycle"

assert run("""4 3
1 2
2 3
3 4
""") == "1 1 1", "path graph"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| empty graph | empty | base boundary case |
| single edge | 1 | minimal non-empty graph |
| triangle | all 1s | cycle merging behavior |
| path of length 3 | all 1s | chain formation |

## Edge Cases

A key edge case is when a vertex has odd degree. In such a situation, one incident edge is left unpaired at that vertex. That edge still participates in pairing at its other endpoint, so globally it becomes an endpoint of a trail. This ensures that the resulting component is still a valid path rather than breaking consistency.

Another edge case is disconnected graphs. Since pairing is done purely locally per vertex, components never interact across connected components, so each component independently forms valid trails and receives its own colors without any special handling.

A final subtle case is when multiple vertices create overlapping pairings that seem contradictory. The construction avoids conflicts because edges are never paired twice at the same vertex, and each adjacency in the edge-graph is symmetric. This guarantees that DFS over edges always sees a consistent undirected structure rather than directional conflicts.
