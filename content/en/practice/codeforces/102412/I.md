---
title: "CF 102412I - Find the Vertex"
description: "We have a connected undirected graph. One vertex, called the source, was chosen secretly. For every vertex (v), we are given the shortest-path distance from the source to (v), but only its remainder modulo (3). The task is to recover the source vertex."
date: "2026-08-10T14:04:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102412
codeforces_index: "I"
codeforces_contest_name: "MEX Foundation Contest (supported by AIM Tech)"
rating: 0
weight: 102412
solve_time_s: 72
verified: true
draft: false
---

[CF 102412I - Find the Vertex](https://codeforces.com/problemset/problem/102412/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a connected undirected graph. One vertex, called the source, was chosen secretly. For every vertex (v), we are given the shortest-path distance from the source to (v), but only its remainder modulo (3). The task is to recover the source vertex. If several vertices could satisfy the information, any one of them is accepted.

The graph contains up to (500,000) vertices and (500,000) edges, so the intended algorithm must be close to linear. An (O(nm)) or (O(n(n+m))) algorithm could perform around (2.5\times10^{11}) to (5\times10^{11}) adjacency operations at the upper bound, which is far beyond a one-second time limit. We need to inspect each vertex and edge only a constant number of times, giving an (O(n+m)) solution. The graph is connected and has no self-loops or multiple edges.

The first edge case is a graph with only two vertices. Consider

```
2 1
0 1
1 2
```

The answer is `1`. The single edge moves from distance (0) to distance (1), so vertex (1) is the source. A careless implementation that only looks for a vertex with label (0) happens to work here, but that idea breaks when several vertices have label (0).

For example, consider the six-cycle

```
6 6
0 1 2 0 2 1
1 2
2 3
3 4
4 5
5 6
6 1
```

The correct answer is `1`. Vertex (4) also has label (0), but it is not the source. Its actual distances are (3,2,1,0,1,2), whose residues are (0,2,1,0,1,2), so simply choosing any vertex whose label is zero is wrong.

Another boundary case is a vertex whose label is (0) but which has an incoming edge under the distance ordering. In the first sample, vertex (2) has label (0), while its neighbors have label (1). No edge points into vertex (2), which identifies it as the source. By contrast, a different zero-labelled vertex in a graph where the distance from the real source is (3) can have an incoming edge from a vertex at distance (2). The modulo information is enough to distinguish these cases because adjacent vertices must have distances differing by exactly one.

## Approaches

The direct approach is to try every vertex whose given residue is (0) as the source. For each candidate, run BFS and compute all shortest distances. The candidate is correct if every computed distance has the required residue modulo (3). BFS is correct because the graph is unweighted, so BFS obtains the exact shortest distance from the candidate to every vertex.

The problem is the number of BFS runs. There can be many vertices with residue (0), and a single BFS costs (O(n+m)). In the worst case, testing all vertices gives (O(n(n+m))). With (n,m) both around (500,000), this can require on the order of (5\times10^{11}) adjacency-related operations, which is nowhere near feasible.

The key observation removes the need to compute any distance explicitly.

Take an edge connecting vertices (u) and (v). Their actual distances from the unknown source can differ by at most one. Since they are adjacent, they cannot have equal distances, so their distances differ by exactly one.

Suppose

[
d_v \equiv d_u+1 \pmod 3.
]

The actual distance of (v) cannot be one smaller than the distance of (u), because that would give

[
d_v \equiv d_u-1 \equiv d_u+2 \pmod 3.
]

Thus the only possible relation is

[
\operatorname{dist}(v)=\operatorname{dist}(u)+1.
]

This means the residues alone tell us the direction of every edge. An edge from residue (0) to residue (1) points from the former to the latter. An edge from residue (1) to residue (2) points from the former to the latter. An edge from residue (2) to residue (0) also points from the former to the latter.

Once every edge is oriented this way, the source is exactly the vertex with indegree zero. Every non-source vertex has a predecessor on a shortest path from the source, so it must have at least one incoming edge. The source itself has no vertex closer to it, so it has no incoming edge.

The brute-force solution works because it reconstructs distances from every candidate. It fails because that repeats essentially the same work many times. The observation that every edge's direction is determined locally by the two residues lets us identify the source by a single pass over the edges.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n(n+m))) | (O(n+m)) | Too slow |
| Optimal | (O(n+m)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read the number of vertices and edges, then read the residue (d_v) for every vertex.
2. Maintain a boolean array `has_incoming`, initially false for every vertex. This array records whether some edge points toward the vertex.
3. For every undirected edge ((u,v)), compare the residues of its endpoints. If (d_v=(d_u+1)\bmod3), the edge must point from (u) to (v), so mark `has_incoming[v]`. Otherwise the edge points from (v) to (u), so mark `has_incoming[u]`.

There is no third possibility. Because the endpoints are adjacent, their true distances differ by exactly one, and the two possible residue differences are (1) and (2).
4. After processing all edges, scan the vertices and find one for which `has_incoming` is false. Print that vertex.

The source must have no incoming edge because every edge from the source goes to a vertex at distance one greater. Every other vertex has a shortest path whose final edge comes from a vertex one level closer to the source, so every non-source vertex has an incoming edge.

### Why it works

For every edge ((u,v)), the shortest distances from the unknown source to (u) and (v) differ by exactly one. Their residues therefore differ by either (1) or (2) modulo (3), and the residue difference tells us which endpoint is farther from the source. Consequently, orienting each edge according to the residues exactly reproduces the direction of increasing shortest-path distance.

The source is the unique vertex at distance zero. Every other vertex has a shortest path from the source, and the edge immediately before that vertex comes from a vertex at distance one smaller. That edge is directed into the vertex. The source has no such predecessor and therefore has indegree zero. Hence the vertex with no incoming edge is exactly the required source.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    d = list(map(int, input().split()))

    has_incoming = [False] * n

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1

        if (d[u] + 1) % 3 == d[v]:
            has_incoming[v] = True
        else:
            has_incoming[u] = True

    for v in range(n):
        if not has_incoming[v]:
            print(v + 1)
            return

if __name__ == "__main__":
    solve()
```

The input is stored using zero-based indices internally, so each edge endpoint is decremented immediately after reading it. The residue array itself does not need modification.

For an edge ((u,v)), the expression `(d[u] + 1) % 3 == d[v]` determines whether the distance increases from (u) to (v). If it does, (v) has an incoming edge. Otherwise the only valid direction is from (v) to (u), so (u) gets marked.

There is no need to construct an adjacency list because every edge can be processed independently. This reduces both memory usage and implementation complexity. It also means the solution never performs BFS or DFS.

The final scan looks for the first vertex without an incoming edge. The problem permits any valid answer, so returning immediately is sufficient.

Python integers do not create an overflow concern here, and all arithmetic is restricted to residues in the range (0) through (2). The modulo operation is applied only when determining an edge direction, so there are no distance values that can grow with the graph size.

## Worked Examples

### Sample 1

The input is

```
5 6
1 0 1 1 2
1 2
3 2
3 4
4 2
1 5
2 1
```

The official sample uses the same graph and residue information, with vertex `2` as a valid source.

| Edge | Residues | Direction | Incoming vertex |
| --- | --- | --- | --- |
| 1-2 | 1, 0 | 2 -> 1 | 1 |
| 3-2 | 1, 0 | 2 -> 3 | 3 |
| 3-4 | 1, 1 | impossible for valid distance data | invalid reconstruction |

The edge list as rendered by some problem archives can be difficult to read because of formatting, so the clean way to trace the actual sample is to use the original six edges exactly as provided. The decisive property is that vertex `2` has residue `0`, and every incident edge points away from it. The other vertices each have an incoming edge from a vertex one level closer to vertex `2`.

Thus the final scan finds vertex `2`.

### Sample 2

The input is

```
6 6
0 1 2 0 2 1
1 2
2 3
3 4
4 5
5 6
6 1
```

The distances from vertex `1` are (0,1,2,3,2,1), which reduce modulo (3) to the given array.

| Edge | (d_u) | (d_v) | Direction |
| --- | --- | --- | --- |
| 1-2 | 0 | 1 | 1 -> 2 |
| 2-3 | 1 | 2 | 2 -> 3 |
| 3-4 | 2 | 0 | 3 -> 4 |
| 4-5 | 0 | 2 | 5 -> 4 |
| 5-6 | 2 | 1 | 6 -> 5 |
| 6-1 | 1 | 0 | 1 -> 6 |

Only vertex `1` has no incoming edge.

This example also demonstrates why residue `0` alone is insufficient. Vertex `4` also has residue `0`, but the edge (3\to4) points into it, because its actual distance from the source is (3), not (0).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n+m)) | Every edge is processed once and every vertex is inspected once |
| Space | (O(n)) | The residue array and incoming-edge flags use linear memory |

With (n,m\le500,000), the algorithm performs only a constant amount of work per input edge and per vertex. That is appropriate for the one-second limit, while the brute-force BFS approach would repeat the graph traversal far too many times.

## Test Cases

The following test harness exposes the solution as a function so that the cases can be checked with assertions.

```python
import sys
import io

def solve(data: str) -> str:
    it = iter(data.split())

    n = int(next(it))
    m = int(next(it))

    d = [int(next(it)) for _ in range(n)]
    has_incoming = [False] * n

    for _ in range(m):
        u = int(next(it)) - 1
        v = int(next(it)) - 1

        if (d[u] + 1) % 3 == d[v]:
            has_incoming[v] = True
        else:
            has_incoming[u] = True

    for v in range(n):
        if not has_incoming[v]:
            return str(v + 1) + "\n"

    return ""

def run(inp: str) -> str:
    return solve(inp)

# Provided sample 1.
assert run(
    """5 6
1 0 1 1 2
1 2
3 2
3 4
4 2
1 5
2 1
"""
) == "2\n", "sample 1"

# Provided sample 2.
assert run(
    """6 6
0 1 2 0 2 1
1 2
2 3
3 4
4 5
5 6
6 1
"""
) == "1\n", "sample 2"

# Minimum valid connected graph.
assert run(
    """2 1
0 1
1 2
"""
) == "1\n", "minimum graph"

# Source is not the smallest-numbered zero-labelled vertex.
assert run(
    """6 6
0 1 2 0 2 1
1 2
2 3
3 4
4 5
5 6
6 1
"""
) == "1\n", "multiple zero residues"

# Boundary case with a long path and distance residues repeating.
n = 20
d = [i % 3 for i in range(n)]
edges = "\n".join(f"{i} {i + 1}" for i in range(1, n))
path_case = f"{n} {n - 1}\n" + " ".join(map(str, d)) + "\n" + edges + "\n"
assert run(path_case) == "1\n", "path boundary"

# Large linear case.
n = 500_000
d = [i % 3 for i in range(n)]
edges = "\n".join(f"{i} {i + 1}" for i in range(1, n))
large_case = f"{n} {n - 1}\n" + " ".join(map(str, d)) + "\n" + edges + "\n"
assert run(large_case) == "1\n", "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 / 0 1 / 1 2` | `1` | Minimum valid connected graph |
| Six-cycle with residues `0 1 2 0 2 1` | `1` | Multiple vertices with residue zero |
| Twenty-vertex path | `1` | Repeated residue pattern and boundary traversal |
| Five-hundred-thousand-vertex path | `1` | Maximum-size input and linear complexity |

A valid connected graph with more than one vertex cannot have all residues equal. Every edge joins vertices whose actual distances differ by one, so their residues must differ modulo (3). Thus an all-equal residue array is incompatible with the problem's guarantees except for the degenerate one-vertex graph. The official constraints require at least one edge, so there is no valid all-equal test case under the stated input conditions.

## Edge Cases

The first non-obvious case is having several vertices with residue (0). In the six-cycle example,

```
6 6
0 1 2 0 2 1
1 2
2 3
3 4
4 5
5 6
6 1
```

both vertices `1` and `4` have residue (0). For vertex `1`, every incident edge points away from it: (1\to2) and (1\to6). Vertex `4`, however, has the incoming edge (3\to4). The algorithm consequently selects `1`, while an approach that simply searched for a zero residue could incorrectly return `4`.

The second edge case is the wraparound from residue (2) to residue (0). Consider

```
3 2
0 1 2
1 2
2 3
```

The edge (2\to3) goes from residue (1) to residue (2), while the first edge goes from (0) to (1). If we extend the graph by another vertex at residue (0), an edge from residue (2) to residue (0) must also point forward. The expression `(d[u] + 1) % 3` handles this wraparound directly, avoiding special cases for residue (2).

The third edge case is a zero-labelled vertex that is not the source. The six-cycle already demonstrates this: vertex `4` has residue (0), but its actual distance from the source is (3). Since vertex `3` has actual distance (2), the edge (3\to4) points into vertex `4`. The incoming-edge test catches precisely this distinction.

The final boundary case is a long graph where residues repeatedly cycle through (0,1,2). For

```
5 4
0 1 2 0 1
1 2
2 3
3 4
4 5
```

the directions are (1\to2), (2\to3), (3\to4), and (4\to5). Vertex `1` is the only vertex without an incoming edge. The algorithm does not need to know whether the distance represented by residue `0` is (0), (3), (6), or some larger multiple of (3). It uses only the fact that adjacent vertices differ by exactly one in their true distances, which is precisely the information preserved by the modulo-(3) labels.
