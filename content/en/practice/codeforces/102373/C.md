---
title: "CF 102373C - Diamonds"
description: "We have a simple undirected graph with up to 300,000 vertices and 300,000 edges. A diamond consists of two different triangles that use the same edge. If an edge has several vertices connected to both of its endpoints, every pair of those common neighbors forms one diamond."
date: "2026-08-12T22:52:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102373
codeforces_index: "C"
codeforces_contest_name: "\u0426\u0438\u043a\u043b \u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434 \u0434\u043b\u044f \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u041f\u0435\u0440\u0432\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102373
solve_time_s: 519
verified: true
draft: false
---

[CF 102373C - Diamonds](https://codeforces.com/problemset/problem/102373/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 8m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a simple undirected graph with up to 300,000 vertices and 300,000 edges. A diamond consists of two different triangles that use the same edge. If an edge has several vertices connected to both of its endpoints, every pair of those common neighbors forms one diamond.

Suppose the edge is (u-v), and exactly (c) vertices are adjacent to both (u) and (v). Each common neighbor gives one triangle containing (u-v), so choosing any two common neighbors gives a pair of triangles sharing that edge. The contribution of this edge is consequently

[
\binom{c}{2}=\frac{c(c-1)}2.
]

The task is to sum this value over every edge.

The graph can contain 300,000 edges, so an algorithm that examines every pair of vertices is already too large. An (O(n^2)) algorithm would have roughly (9\cdot10^{10}) vertex pairs in the largest case, while an (O(n^3)) or (O(n^4)) approach is completely out of range. The official limits are 2 seconds and 512 MB, so the solution needs near-linear or roughly (m\sqrt m) graph processing rather than exhaustive enumeration.

There are several edge cases that are easy to mishandle. A graph can contain triangles without containing any diamond. For example,

```
4 4
1 2
2 3
3 4
4 1
```

has no triangles at all, so the answer is `0`. A triangle-counting implementation that treats every triangle as a diamond would incorrectly return `1`.

A complete graph on four vertices is another useful case:

```
4 6
1 2
1 3
1 4
2 3
2 4
3 4
```

The answer is `6`, not `1`. Every edge belongs to two triangles, and each of the six edges gives one pair of triangles. A careless implementation that counts each set of four vertices only once would miss five diamonds.

There can also be several triangles around one edge. Consider

```
5 7
1 2
1 3
2 3
1 4
2 4
1 5
2 5
```

The edge (1-2) belongs to three triangles, using vertices (3,4,5). Any two of those triangles form a diamond, giving (\binom32=3). Counting triangles and simply dividing by two would not work because each triangle participates in several diamonds.

## Approaches

The most direct brute-force solution considers every four-vertex set. A diamond always uses exactly four distinct vertices. Among those four vertices there are six possible edges. If exactly five are present, the four vertices form one diamond. If all six are present, they form a (K_4), which contains six different diamonds, one for each choice of the shared edge.

Thus, for every quadruple we could inspect its six possible edges and add either zero, one, or six to the answer. This is correct, but there are

[
\binom n4=O(n^4)
]

quadruples. At (n=300000), this is on the order of (3.4\cdot10^{20}) quadruples, before even accounting for the six edge checks per quadruple. The approach is useful only as a conceptual baseline.

The key observation is to stop looking at four vertices directly. For every edge (u-v), the only information needed is its number of common neighbors. Instead of explicitly constructing every pair of triangles, we can first enumerate every triangle and record which three edges belong to it.

If an edge has already appeared in (k) triangles and another triangle containing that edge is found, that new triangle forms exactly (k) new diamonds with the previously found triangles. So when a triangle is discovered, for each of its three edges we add the current triangle count of that edge to the answer, then increase that edge's triangle count.

The remaining problem is efficient triangle enumeration. Checking every pair of neighbors of every vertex can be quadratic on a star or another graph with a high-degree vertex. The standard way around this is to orient every edge according to vertex degree. An edge goes from the endpoint with smaller degree to the endpoint with larger degree, breaking equal-degree ties by vertex number. Then we only search for triangles through these forward edges.

This degree ordering bounds the total amount of forward wedge exploration by (O(m\sqrt m)), the standard degree-oriented triangle-counting bound. The same idea is commonly used for efficient triangle and four-cycle enumeration in sparse graphs.

The brute force works because every diamond is a four-vertex structure, but fails because there are far too many four-vertex sets. The observation that a diamond is simply a pair of triangles sharing an edge lets us reduce the problem to triangle enumeration plus a small counter for every edge.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^4)) | (O(m)) | Too slow |
| Optimal | (O(m\sqrt m)) | (O(n+m)) | Accepted |

## Algorithm Walkthrough

1. Read the graph and compute the degree of every vertex. We need the degrees before orienting the edges because the orientation is what keeps the later triangle search small.
2. Give every vertex an ordering based on `(degree, vertex_id)`. An edge is directed from the smaller vertex in this ordering to the larger one. Equal degrees are resolved by the vertex number, so every edge receives exactly one direction.
3. Store only the outgoing edges of each vertex. Along with the destination, store the original edge ID, because later we need to update the triangle count belonging to that edge.
4. Maintain an array `mark`. While processing a vertex (v), mark every outgoing neighbor (w) with the edge ID of (v-w). This gives constant-time access to the edge between (v) and a marked vertex.
5. For every outgoing edge (v\rightarrow u), scan all outgoing edges (u\rightarrow w). If (w) is currently marked by (v), then (v,u,w) form a triangle. The three edge IDs are immediately known: the edge (v-u), the edge (u-w), and the marked edge (v-w).
6. When a triangle is found, suppose its three edges currently belong to (a), (b), and (c) previously found triangles. The new triangle forms (a+b+c) new diamonds, because it can be paired with every earlier triangle sharing any of those edges. Add that value to the answer, then increment all three edge counters.
7. Clear the marks belonging to (v)'s outgoing neighbors before moving to the next vertex. The clearing step prevents a vertex marked for one center from being mistaken for a neighbor of another center.

### Why it works

Every triangle has a unique smallest vertex under the chosen total ordering. Its other two vertices are both larger than that vertex, and the edge between those two larger vertices is directed from the smaller one to the larger one. Consequently, the triangle is discovered exactly once, when its smallest vertex is processed.

For every edge, its counter is exactly the number of triangles discovered so far that contain that edge. When a new triangle containing the edge is found, it forms one new diamond with each previously counted triangle on that edge. Adding the old counter before incrementing it therefore counts every pair of triangles exactly once. Since every diamond is precisely one pair of triangles sharing one edge, the accumulated answer is exactly the required number of diamonds.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    degree = [0] * n
    edges = [None] * m

    for eid in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        edges[eid] = (u, v)
        degree[u] += 1
        degree[v] += 1

    order = sorted(range(n), key=lambda v: (degree[v], v))
    pos = [0] * n
    for i, v in enumerate(order):
        pos[v] = i

    out = [[] for _ in range(n)]

    for eid, (u, v) in enumerate(edges):
        if pos[u] < pos[v]:
            out[u].append((v, eid))
        else:
            out[v].append((u, eid))

    triangle_count = [0] * m
    mark = [-1] * n
    answer = 0

    for v in range(n):
        ov = out[v]

        for w, eid in ov:
            mark[w] = eid

        for u, eid_vu in ov:
            for w, eid_uw in out[u]:
                eid_vw = mark[w]

                if eid_vw != -1:
                    answer += (
                        triangle_count[eid_vu]
                        + triangle_count[eid_uw]
                        + triangle_count[eid_vw]
                    )

                    triangle_count[eid_vu] += 1
                    triangle_count[eid_uw] += 1
                    triangle_count[eid_vw] += 1

        for w, _ in ov:
            mark[w] = -1

    print(answer)

if __name__ == "__main__":
    solve()
```

The first pass builds `degree` and stores every edge with a stable ID. The IDs are necessary because the final answer depends on how many triangles use each particular edge, not merely on how many triangles exist in total.

The `order` array implements the degree orientation. `pos[v]` gives the position of a vertex in that ordering, so every undirected edge can be directed with one comparison. The outgoing adjacency lists contain `(neighbor, edge_id)` pairs, which lets the triangle search identify all three edge counters without another dictionary lookup.

The `mark` array is reused for every vertex. When processing `v`, `mark[w]` contains the edge ID of (v-w) for every forward neighbor (w). Thus, when the inner loop reaches a vertex `w` from `u`, `mark[w] != -1` is exactly the condition that (v-w) also exists.

The answer is updated before the three counters are incremented. If an edge has appeared in (k) earlier triangles, the new triangle creates (k) new pairs with that edge. Updating first would count the new triangle paired with itself, which is invalid.

Python integers have arbitrary precision, so even the largest possible answer does not overflow. For example, a complete graph with 775 vertices already has 89,491,021,650 diamonds.

## Worked Examples

For Sample 1, the graph is a four-cycle. Every vertex has degree two, so the vertex IDs break the ties. No forward search finds a triangle.

| Processed vertex | Forward neighbors | Triangle found | Answer |
| --- | --- | --- | --- |
| 1 | 2, 4 | none | 0 |
| 2 | 3, 4 | none | 0 |
| 3 | 4 | none | 0 |
| 4 | none | none | 0 |

The important property here is that an edge can be present without participating in a triangle. The algorithm never creates a diamond merely because two edges meet at a vertex.

For Sample 2, there are two triangles, (1-2-3) and (1-3-4), sharing edge (1-3). The degree ordering is (2,4,1,3). The first triangle increments the counters of edges (1-2), (2-3), and (1-3). The second triangle increments the counters of (1-4), (3-4), and (1-3), and the previous counter of (1-3) contributes one new diamond.

| Processed vertex | Triangle | Edge counters before | Added to answer | Answer |
| --- | --- | --- | --- | --- |
| 2 | (1,2,3) | (0,0,0) | 0 | 0 |
| 4 | (1,3,4) | edge (1-3) has 1 | 1 | 1 |
| 1 | none | unchanged | 0 | 1 |
| 3 | none | unchanged | 0 | 1 |

The trace demonstrates why counting triangles alone is insufficient. The first triangle creates no diamond because there is nothing to pair it with. The second triangle creates exactly one pair with the first triangle, giving the required answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(m\sqrt m+n\log n)) | Sorting the vertices takes (O(n\log n)); degree-oriented triangle enumeration takes (O(m\sqrt m)) |
| Space | (O(n+m)) | Degrees, ordering arrays, marks, edge IDs, counters, and oriented adjacency lists are all linear |

With (m\le300000), the degree-oriented bound is roughly (m\sqrt m), rather than a quadratic or cubic function of the number of vertices. The graph itself also has only (O(m)) stored adjacency entries, so the memory usage remains linear and fits the 512 MB limit.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    data = inp.split()
    it = iter(data)

    n = int(next(it))
    m = int(next(it))

    degree = [0] * n
    edges = [None] * m

    for eid in range(m):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        edges[eid] = (u, v)
        degree[u] += 1
        degree[v] += 1

    order = sorted(range(n), key=lambda v: (degree[v], v))
    pos = [0] * n

    for i, v in enumerate(order):
        pos[v] = i

    out = [[] for _ in range(n)]

    for eid, (u, v) in enumerate(edges):
        if pos[u] < pos[v]:
            out[u].append((v, eid))
        else:
            out[v].append((u, eid))

    cnt = [0] * m
    mark = [-1] * n
    ans = 0

    for v in range(n):
        for w, eid in out[v]:
            mark[w] = eid

        for u, e1 in out[v]:
            for w, e2 in out[u]:
                e3 = mark[w]
                if e3 != -1:
                    ans += cnt[e1] + cnt[e2] + cnt[e3]
                    cnt[e1] += 1
                    cnt[e2] += 1
                    cnt[e3] += 1

        for w, _ in out[v]:
            mark[w] = -1

    return str(ans)

# Provided sample 1
assert solve_data("""\
4 4
1 2
2 3
3 4
4 1
""") == "0", "sample 1"

# Provided sample 2
assert solve_data("""\
4 5
1 2
2 3
3 4
4 1
1 3
""") == "1", "sample 2"

# Provided sample 3
assert solve_data("""\
4 6
1 2
2 3
3 4
4 1
1 3
2 4
""") == "6", "sample 3"

# Minimum-size graph with exactly two triangles sharing one edge
assert solve_data("""\
4 5
1 2
2 3
3 1
1 4
2 4
""") == "1", "minimum diamond"

# Three triangles sharing the same edge: C(3, 2) = 3
assert solve_data("""\
5 7
1 2
1 3
2 3
1 4
2 4
1 5
2 5
""") == "3", "three triangles around one edge"

# Complete graph K4: every one of the six edges is a shared edge
assert solve_data("""\
4 6
1 2
1 3
1 4
2 3
2 4
3 4
""") == "6", "complete K4"

# Maximum-size sparse graph: 300000 vertices and 300000 edges.
# A star plus one extra edge still contains no triangle.
n = 300000
parts = [f"{n} 300000"]
parts.extend(f"1 {v}" for v in range(2, n + 1))
parts.append("2 3")
max_case = "\n".join(parts) + "\n"

assert solve_data(max_case) == "0", "maximum-size sparse graph"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Four-cycle with 4 edges | 0 | Graphs with edges but no triangles |
| Two triangles sharing one edge | 1 | Minimum possible diamond |
| Three triangles around one edge | 3 | The (\binom c2) counting rule |
| Complete (K_4) | 6 | Multiple diamonds on the same four vertices |
| 300,000-vertex sparse graph | 0 | Maximum input size and high-degree vertex handling |

## Edge Cases

The four-cycle

```
4 4
1 2
2 3
3 4
4 1
```

contains no triangle. During orientation, the algorithm may explore several two-edge paths, but none closes into a forward edge. No edge counter is incremented, so the final answer remains `0`.

The minimum diamond

```
4 5
1 2
2 3
3 1
1 4
2 4
```

contains triangles (1-2-3) and (1-2-4). When the first triangle is found, the counter of edge (1-2) becomes one. When the second triangle is found, the old counter of (1-2) contributes one to the answer. The final output is `1`.

The graph

```
5 7
1 2
1 3
2 3
1 4
2 4
1 5
2 5
```

has three triangles sharing (1-2). The counter of (1-2) changes from zero to one after the first triangle, from one to two after the second, and from two to three after the third. The answer receives (0+1+2=3), which is exactly (\binom32).

Finally, in

```
4 6
1 2
1 3
1 4
2 3
2 4
3 4
```

every edge belongs to two triangles. Each edge contributes (\binom22=1), and there are six edges, so the answer is `6`. This is the case that catches implementations which count each four-vertex diamond-shaped subgraph only once and accidentally treat (K_4) as a single diamond.
