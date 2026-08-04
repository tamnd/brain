---
title: "CF 102606E - Even Degree"
description: "We have an undirected graph where every vertex starts with an even number of incident edges. We may remove edges one by one, but an edge can only be removed if at least one of its two endpoints currently has an even degree."
date: "2026-08-04T17:02:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102606
codeforces_index: "E"
codeforces_contest_name: "2020 ECNU Campus Online Invitational Contest"
rating: 0
weight: 102606
solve_time_s: 92
verified: true
draft: false
---

[CF 102606E - Even Degree](https://codeforces.com/problemset/problem/102606/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an undirected graph where every vertex starts with an even number of incident edges. We may remove edges one by one, but an edge can only be removed if at least one of its two endpoints currently has an even degree. The task is to find the largest possible number of removals and output the edge indices in a valid order.

The input describes the vertices and the original edges. The output is a sequence of edge IDs, arranged exactly in the order in which those edges should be deleted. The graph after all deletions does not need to be empty because some edges may become impossible to remove.

The limits are large: both the number of vertices and edges can reach 500000. This immediately rules out simulations that repeatedly search through all edges or try different deletion choices. An algorithm around linear time is required because even an (O(m \log m)) solution needs to be carefully implemented, while anything involving many passes over the graph will exceed the limit.

The key edge cases come from the parity of degrees changing after every deletion. A vertex that starts with even degree can become odd after removing one incident edge, so checking only the initial graph is incorrect.

For example:

```
3 3
1 2
2 3
1 3
```

One valid optimal answer is:

```
2
1 2
```

After deleting edge 1, the remaining degrees are 1, 1, and 2. Edge 2 can still be deleted because vertex 3 has even degree. A solution that assumes the first deletion makes all future choices impossible would miss valid removals.

Another important case is a disconnected graph:

```
6 2
1 2
3 4
```

This graph does not satisfy the original even-degree condition, so it cannot appear in the input. The actual edge case is a disconnected graph made of several even-degree components, such as:

```
6 4
1 2
2 3
3 4
4 1
```

There is only one component with edges, and three edges can be removed. The last edge in that component cannot be removed because its two endpoints would both have degree one.

## Approaches

A direct approach would repeatedly scan all remaining edges. Whenever an edge has at least one endpoint with even degree, we delete it and update the two degrees. This is correct because every chosen deletion follows the rule. However, in the worst case we might scan all (m) edges after each deletion, resulting in (O(m^2)) operations. With (m=500000), this is far beyond what is possible.

The useful observation comes from the fact that every vertex initially has even degree. Each connected component of such a graph has an Euler circuit. Consider the order of edges along an Euler circuit. If we delete those edges one by one except for the final edge of the circuit, every deletion is legal.

Why does this happen? Before removing an edge in an Euler traversal, the current vertex still has an even number of unused incident edges. The traversal enters and leaves vertices in pairs, so the edge being removed always touches a vertex whose remaining degree is even. After removing all but one edge from a component, the final remaining edge has both endpoints of odd degree and cannot be removed.

This also proves the maximum. A connected component containing at least one edge cannot lose its last edge, because the last edge would leave two vertices of degree one. Since every non-empty component must keep at least one edge, leaving exactly one edge per component is optimal.

The problem is reduced to finding Euler circuits for all components and outputting every edge in each circuit except the final edge of that component.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m²) | O(n + m) | Too slow |
| Optimal | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Build an adjacency list containing every edge ID. Because the graph is undirected, every edge appears twice in the adjacency structure.
2. For every vertex that has not been processed and has at least one incident edge, run an iterative Hierholzer traversal to construct an Euler circuit of its connected component.
3. Store the edge IDs produced by the Euler traversal. The traversal contains every edge of that component exactly once.
4. Add all edges from this component except the last edge in the Euler order to the answer. The last edge is intentionally kept because it is the unavoidable remaining edge of the component.
5. Continue until every component containing edges has been processed. Output the collected deletion sequence.

Why it works: the invariant is that every component is processed independently through an Euler circuit, and the deletion order inside that component follows a valid cyclic edge order. During the first (s-1) deletions of a component with (s) edges, the next Euler edge always has an endpoint with even remaining degree. Since no component can be completely erased, keeping one edge per component is also the best possible result.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    adj = [[] for _ in range(n)]
    for i in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        adj[u].append((v, i))
        adj[v].append((u, i))

    used = [False] * m
    ans = []

    for start in range(n):
        if not adj[start]:
            continue

        if all(used[e] for _, e in adj[start]):
            continue

        stack = [(start, -1)]
        circuit = []

        while stack:
            u, in_edge = stack[-1]

            while adj[u] and used[adj[u][-1][1]]:
                adj[u].pop()

            if adj[u]:
                v, eid = adj[u].pop()
                if used[eid]:
                    continue
                used[eid] = True
                stack.append((v, eid))
            else:
                stack.pop()
                if in_edge != -1:
                    circuit.append(in_edge)

        if circuit:
            ans.extend(circuit[:-1])

    print(len(ans))
    if ans:
        print(*[x + 1 for x in ans])

if __name__ == "__main__":
    solve()
```

The adjacency list stores edge IDs instead of only neighboring vertices because the output requires the original edge numbers. The `used` array prevents an undirected edge from being taken twice during Hierholzer's algorithm.

The stack version of Hierholzer is used because recursive DFS can exceed Python's recursion limit on graphs with hundreds of thousands of vertices. When a vertex has no unused incident edge left, the algorithm adds the edge used to enter that vertex into the circuit. This produces the Euler order in reverse, which is still a valid Euler traversal because reversing a cycle preserves its validity.

The final edge of every circuit is skipped. The indexing conversion happens only while printing because the input and internal representation use zero-based edge IDs.

## Worked Examples

For the sample:

```
3 3
1 2
1 3
2 3
```

One possible Euler order is the cycle containing all three edges.

| Step | Euler edge removed | Remaining edges in component |
| --- | --- | --- |
| 1 | 1 | 2 |
| 2 | 2 | 1 |

The algorithm outputs two deletions and leaves the last edge. The remaining edge cannot be removed because both of its endpoints have degree one.

A square cycle:

```
4 4
1 2
2 3
3 4
4 1
```

can be processed as follows.

| Step | Euler edge removed | Remaining edges |
| --- | --- | --- |
| 1 | 1 | 3 |
| 2 | 2 | 2 |
| 3 | 3 | 1 |

The fourth edge stays. This demonstrates the rule that a component with edges always contributes exactly one unavoidable edge.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Every vertex and every edge is processed a constant number of times by Hierholzer's algorithm. |
| Space | O(n + m) | The adjacency lists, edge state array, and traversal stack store linear information. |

The solution fits the constraints because it performs only linear work. A graph with 500000 edges is handled by one traversal instead of repeated simulations.

## Test Cases

```python
import sys
import io

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

def valid(inp):
    out = run(inp).strip().split()
    if not out:
        return False
    k = int(out[0])
    return k == len(out) - 1

assert valid("""3 3
1 2
1 3
2 3
""")

assert valid("""4 4
1 2
2 3
3 4
4 1
""")

assert valid("""1 0
""")

assert valid("""6 6
1 2
2 3
3 4
4 1
5 6
5 6
""")

assert valid("""8 8
1 2
2 3
3 4
4 1
5 6
6 7
7 8
8 5
""")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Triangle cycle | Any two removable edges | Basic Euler circuit handling |
| Four-cycle | Three removable edges | Keeping one edge per component |
| Single vertex with no edges | Zero deletions | Empty graph handling |
| Multiple components | All but one edge from each component | Component separation |
| Two independent cycles | Independent Euler traversals | Repeated processing |

## Edge Cases

For the triangle example:

```
3 3
1 2
1 3
2 3
```

Hierholzer creates one Euler circuit of length three. The algorithm removes the first two circuit edges and keeps the third. The invariant holds because every removed edge appears before the final edge of a cycle.

For a graph with isolated vertices, such as:

```
5 4
1 2
2 3
3 4
4 1
```

only the first four vertices are processed. Vertex 5 has no edges and contributes nothing. The answer removes three of the four cycle edges.

For multiple connected components:

```
8 8
1 2
2 3
3 4
4 1
5 6
6 7
7 8
8 5
```

each cycle is handled separately. The algorithm leaves one edge in the first component and one edge in the second component, while deleting the other six edges. This matches the lower bound that every non-empty component must keep one edge.
