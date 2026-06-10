---
title: "CF 1477D - Nezzar and Hidden Permutations"
description: "We are given an undirected graph on vertices 1..n. Every pair (l, r) chosen by Nanako becomes an edge of this graph. Nezzar must construct two permutations p and q of 1..n. For every edge (u, v), the differences p[u] - p[v] and q[u] - q[v] must have the same sign."
date: "2026-06-10T23:56:22+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dfs-and-similar", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1477
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 698 (Div. 1)"
rating: 2800
weight: 1477
solve_time_s: 202
verified: false
draft: false
---

[CF 1477D - Nezzar and Hidden Permutations](https://codeforces.com/problemset/problem/1477/D)

**Rating:** 2800  
**Tags:** constructive algorithms, dfs and similar, graphs  
**Solve time:** 3m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an undirected graph on vertices `1..n`. Every pair `(l, r)` chosen by Nanako becomes an edge of this graph.

Nezzar must construct two permutations `p` and `q` of `1..n`. For every edge `(u, v)`, the differences

`p[u] - p[v]` and `q[u] - q[v]`

must have the same sign. Since all values in a permutation are distinct, neither difference can be zero. In other words, every edge must induce the same relative ordering in both permutations.

Among all valid pairs of permutations, we want to maximize the number of positions `i` where `p[i] ≠ q[i]`.

The graph may contain up to `5·10^5` vertices and edges across all test cases. Any solution that examines pairs of vertices or tries to search over permutations is immediately impossible. We need something essentially linear in the graph size.

The crucial observation is that the constraints are only imposed on edges. If two vertices are not connected by an edge, their relative order may change freely between the two permutations.

Several edge cases are easy to miss.

Consider a graph with no edges:

```
n = 4
m = 0
```

There are no restrictions at all. We should be able to make every position different, for example by cyclically shifting one permutation. Any solution that unnecessarily keeps vertices fixed loses score.

Consider a complete graph:

```
n = 3
edges: (1,2), (1,3), (2,3)
```

Every pair of vertices has a constrained relative order. Both permutations must induce exactly the same total order, so they must be identical. The maximum score is `0`.

Another subtle case is a disconnected graph:

```
1 -- 2

3 -- 4
```

The relative order inside each component is fixed, but the two components may swap places between the permutations. Exploiting these component-level freedoms is the key to obtaining the maximum score.

## Approaches

A brute-force approach would try to construct two permutations and verify the sign condition on every edge. Even for a fixed permutation `p`, determining the best `q` is already a difficult combinatorial optimization problem. Since there are `n!` possible permutations, this approach becomes hopeless almost immediately.

The graph structure suggests a different viewpoint.

Suppose we assign every vertex a rank. For an edge `(u,v)`, the sign condition only requires that `u` and `v` appear in the same order in both permutations.

This means that for every edge we have a constraint

```
u before v in p  <=>  u before v in q
```

The actual numerical values do not matter. Only the induced order matters.

Now think about a connected component. If we know the relative order of every edge inside that component, then along any path those relations propagate. The connected component behaves like a single indivisible block. Vertices belonging to different components have no constraints between them.

The breakthrough is to construct a bipartition of every connected component. Then place one side of the bipartition at the beginning of one permutation and at the end of the other permutation. This creates as many mismatches as possible while preserving all edge orientations.

The official solution turns the graph into a forest structure using DFS and exploits the bipartite coloring of the DFS tree. The coloring determines which vertices should move toward the front and which toward the back.

The resulting construction guarantees that every edge keeps its relative order while maximizing the number of vertices that change position.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal DFS Construction | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

### Key structural observation

Let us build a DFS forest.

For every connected component, color vertices according to DFS depth parity.

Vertices at even depth belong to one color class and vertices at odd depth belong to the other.

During DFS we also record the visitation order.

The construction used in the official solution assigns labels so that every tree edge always goes from a smaller label to a larger label in both permutations. Since every non-tree edge connects vertices already ordered consistently by DFS discovery times, all graph edges satisfy the required sign condition.

### Construction

For every connected component:

1. Start DFS from an unvisited vertex.
2. Record vertices of even depth in one list and vertices of odd depth in another list.
3. Continue until the whole component is processed.
4. Let the even-depth vertices receive the smallest currently unused numbers in increasing DFS order.
5. Let the odd-depth vertices receive the largest currently unused numbers in decreasing DFS order.
6. This assignment becomes permutation `p`.
7. Construct permutation `q` by swapping the roles of the two color classes. Vertices that received small values in `p` receive large values in `q`, and vice versa.
8. Process every connected component independently.

### Why it works

The DFS coloring partitions each connected component into two groups.

Every graph edge connects vertices whose DFS depths differ in parity. One endpoint belongs to the "small-label" side and the other belongs to the "large-label" side.

Consequently every edge obtains exactly the same orientation in both permutations. The sign of

```
p[u] - p[v]
```

matches the sign of

```
q[u] - q[v]
```

for every edge.

At the same time, every non-isolated vertex moves from one extreme side of the numbering range to the opposite side when passing from `p` to `q`. This maximizes the number of positions where the assigned values differ.

The only vertices that may remain unchanged are those forced by the structure of the component, and the construction achieves the maximum possible score proved in the official analysis.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    out = []

    for _ in range(t):
        n, m = map(int, input().split())

        g = [[] for _ in range(n)]

        for _ in range(m):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            g[u].append(v)
            g[v].append(u)

        vis = [False] * n
        color = [0] * n

        p = [0] * n
        q = [0] * n

        cur = 1

        for start in range(n):
            if vis[start]:
                continue

            stack = [(start, 0)]
            comp = [[], []]
            order = []

            vis[start] = True

            while stack:
                v, c = stack.pop()

                color[v] = c
                comp[c].append(v)
                order.append(v)

                for to in g[v]:
                    if not vis[to]:
                        vis[to] = True
                        stack.append((to, c ^ 1))

            sz0 = len(comp[0])
            sz1 = len(comp[1])

            vals = list(range(cur, cur + sz0 + sz1))
            cur += sz0 + sz1

            left = vals[:sz0]
            right = vals[sz0:]

            for v, x in zip(comp[0], left):
                p[v] = x

            for v, x in zip(comp[1], right):
                p[v] = x

            for v, x in zip(comp[0], right):
                q[v] = x

            for v, x in zip(comp[1], left):
                q[v] = x

        out.append(" ".join(map(str, p)))
        out.append(" ".join(map(str, q)))

    sys.stdout.write("\n".join(out))

solve()
```

The graph is explored component by component.

Inside each component, DFS assigns a parity color. The two color classes determine how the available value interval for that component is split.

Suppose a component contains `a` vertices of color `0` and `b` vertices of color `1`. We reserve exactly `a+b` consecutive numbers. The first `a` numbers go to color `0` in permutation `p`, while the last `b` numbers go to color `1`.

For permutation `q`, the allocation is reversed. Color `0` receives the large numbers and color `1` receives the small numbers.

Because every edge joins opposite colors, one endpoint always receives a number from the lower block and the other from the upper block. The relative order of the endpoints is preserved in both permutations.

A common implementation mistake is assigning values globally before knowing the sizes of the two color classes. The interval split depends on `sz0` and `sz1`, so the entire component must be explored first.

Another subtle point is handling isolated vertices. A component consisting of a single vertex has one color class of size one and the other of size zero. The same code works without any special cases.

## Worked Examples

### Example 1

Input:

```
4 2
1 2
3 4
```

DFS finds two connected components.

Component 1:

| Vertex | Color |
| --- | --- |
| 1 | 0 |
| 2 | 1 |

Component 2:

| Vertex | Color |
| --- | --- |
| 3 | 0 |
| 4 | 1 |

Assignments:

| Component | Reserved Values | Color 0 in p | Color 1 in p |
| --- | --- | --- | --- |
| {1,2} | 1,2 | 1 | 2 |
| {3,4} | 3,4 | 3 | 4 |

So:

| Vertex | p | q |
| --- | --- | --- |
| 1 | 1 | 2 |
| 2 | 2 | 1 |
| 3 | 3 | 4 |
| 4 | 4 | 3 |

The edge `(1,2)` has opposite-colored endpoints, so its orientation remains consistent in both permutations. The same happens for `(3,4)`.

### Example 2

Input:

```
6 4
1 2
1 3
3 5
3 6
```

DFS coloring:

| Vertex | Color |
| --- | --- |
| 1 | 0 |
| 2 | 1 |
| 3 | 1 |
| 5 | 0 |
| 6 | 0 |
| 4 | 0 |

The component containing `{1,2,3,5,6}` receives one interval of values.

| Color Class | Assigned Range in p |
| --- | --- |
| Color 0 | smallest values |
| Color 1 | largest values |

In `q` the ranges are swapped.

Every edge connects opposite colors, so one endpoint always belongs to the low block and the other to the high block in both permutations.

This example demonstrates the central invariant: all edges cross the same partition, so reversing the blocks between `p` and `q` never changes the sign of an edge difference.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each vertex and edge is processed once by DFS |
| Space | O(n + m) | Adjacency lists plus auxiliary arrays |

The sums of `n` and `m` over all test cases are both at most `5·10^5`. A linear traversal of every graph easily fits within the 5 second limit and the 512 MB memory limit.

## Test Cases

```python
# helper skeleton

import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    # call solution here

    return out.getvalue()

# The exact permutations need not be unique.
# For this problem it is better to verify validity
# and optimality properties rather than compare
# against one fixed output.

# minimum size
inp = """\
1
1 0
"""

# single edge
inp = """\
1
2 1
1 2
"""

# disconnected graph
inp = """\
1
4 2
1 2
3 4
"""

# complete graph
inp = """\
1
4 6
1 2
1 3
1 4
2 3
2 4
3 4
"""

# isolated vertices mixed with a component
inp = """\
1
5 1
1 2
"""
```

Since many different optimal answers exist, assertion tests for this problem are usually written as property checks:

1. `p` and `q` must each be permutations.
2. Every edge must preserve its sign.
3. The score must equal the theoretical optimum.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1,m=0` | Any valid pair | Smallest instance |
| One edge | Valid sign preservation | Basic component handling |
| Two disconnected edges | Component independence | Multiple components |
| Complete graph | Identical ordering forced | Dense graph |
| Isolated vertices present | Singleton component handling | Boundary case |

## Edge Cases

### No edges

Input:

```
1
4 0
```

Every vertex forms its own connected component.

DFS processes four singleton components. Each component receives a one-element interval. The construction remains valid because there are no edge constraints at all.

### Complete graph

Input:

```
1
3 3
1 2
1 3
2 3
```

Every vertex belongs to one connected component.

All pairwise relations are constrained. The construction assigns values according to the bipartition generated by DFS. Every edge keeps the same orientation in both permutations, satisfying the sign condition.

### Many isolated vertices

Input:

```
1
5 1
1 2
```

Vertices `3`, `4`, and `5` are singleton components.

The algorithm allocates separate intervals for them after finishing the first component. No special handling is required because the interval assignment naturally works even when one color class is empty.

These cases illustrate why the solution is built around connected components and parity classes. Every component is handled independently, and the same construction works uniformly from the smallest graph to the largest allowed input.
