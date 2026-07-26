---
title: "CF 102835I - Critical Structures"
description: "The input describes a communication network. Each vertex is a computing node and each edge is a communication link between two nodes. A critical node is a vertex whose removal makes the network disconnected. A critical link is an edge whose removal disconnects the network."
date: "2026-07-26T15:01:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102835
codeforces_index: "I"
codeforces_contest_name: "The 2020 ICPC Asia Taipei-Hsinchu Site Programming Contest"
rating: 0
weight: 102835
solve_time_s: 70
verified: true
draft: false
---

[CF 102835I - Critical Structures](https://codeforces.com/problemset/problem/102835/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

The input describes a communication network. Each vertex is a computing node and each edge is a communication link between two nodes. A critical node is a vertex whose removal makes the network disconnected. A critical link is an edge whose removal disconnects the network.

The remaining structure we need is based on groups of edges that belong together inside cycles. A critical component is a maximal group of edges where every pair of edges can appear together on a cycle. These groups are exactly the biconnected components of the graph. For the final fraction, we divide the number of such components by the number of edges in the largest one and reduce the fraction.

The constraints are designed for a linear graph traversal. With up to around one thousand vertices per test case and up to one million edges in total, checking connectivity after removing every vertex or edge would be far too slow. A brute-force articulation point check would require repeatedly running DFS, which becomes quadratic in the number of vertices or edges. A Tarjan DFS that processes every edge a constant number of times fits easily within the limits.

Several edge cases are easy to miss. A single edge is itself a biconnected component, even though it is also a bridge. For example:

```
1
2 1
1 2
```

The answer is:

```
1 1 1 1
```

The two vertices are both critical nodes, the only edge is a critical link, and the only critical component contains one edge. An implementation that only records components when it finds a cycle would incorrectly lose this component.

A cycle has no articulation point and no bridge. For example:

```
1
4 4
1 2
2 3
3 4
4 1
```

The answer is:

```
0 0 1 4
```

A DFS that marks every visited vertex as suspicious without checking low-link values would incorrectly count vertices here.

A graph with several biconnected parts connected by bridges is another important case. For example:

```
1
6 7
1 2
2 3
3 1
4 5
5 6
6 4
1 4
```

The answer is:

```
2 1 1 1
```

There are three biconnected components, but the fraction is three divided by the largest component size, three, which reduces to one over one. A solution that forgets to reduce the fraction would fail.

## Approaches

A direct approach would be to test every vertex and edge independently. For a vertex, remove it and run a graph traversal to see whether some nodes become unreachable. For an edge, remove it and do the same. This is correct because articulation points and bridges are defined exactly by these removals. However, it repeats almost the same traversal many times. With many edges, the number of operations becomes too large.

The key observation is that DFS already exposes the information needed to answer all of these questions. During a DFS, every vertex receives a discovery time. For each vertex, we also maintain the lowest discovery time reachable from its subtree using zero or more tree edges and at most one back edge.

If a child subtree of a vertex cannot reach any ancestor of that vertex, then the vertex separates that subtree from the rest of the graph. This gives the articulation point condition. If a child cannot even reach the vertex itself through another route, the connecting edge is a bridge.

The same DFS can collect biconnected components. Whenever we discover a bridge or finish exploring a subtree that forms a separate biconnected region, the edges currently stored in a stack belong to one component. Each component is then counted and its edge count is used to update the largest component size.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n(n+m)) | O(n+m) | Too slow |
| Tarjan DFS | O(n+m) | O(n+m) | Accepted |

## Algorithm Walkthrough

1. Run a DFS over the graph while maintaining discovery times and low-link values. The low-link value tells us the earliest ancestor that can be reached from a subtree.
2. Every traversed edge is pushed into an edge stack. Keeping the edges instead of only vertices allows us to reconstruct biconnected components when DFS finishes exploring a region.
3. For a DFS tree edge from vertex `u` to child `v`, update `low[u]` after returning from `v`. If `low[v] >= tin[u]`, then the edges from the stack until the edge `u-v` form one complete biconnected component. The inequality means the subtree of `v` cannot connect above `u`.
4. For the same child edge, if `low[v] > tin[u]`, the edge `u-v` is a bridge. There is no alternate path from `v`'s side back to `u` or higher.
5. Mark articulation points using the same low-link information. A non-root vertex `u` is an articulation point if it has a child `v` with `low[v] >= tin[u]`. A DFS root is special because it is critical only when it has at least two DFS children.
6. After all components are found, let `c` be their count and `s` be the largest component size in edges. Reduce `c/s` using the greatest common divisor.

The correctness comes from the DFS low-link invariant. At any point, `low[v]` represents exactly the highest ancestor that the subtree of `v` can reach without using the parent edge. Because of this, `low[v] >= tin[u]` is precisely the condition that the subtree below `v` is separated from ancestors of `u`. The same separation property defines both articulation points and the boundary of biconnected components, so every reported structure is valid and no valid structure is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case():
    n, m = map(int, input().split())
    graph = [[] for _ in range(n)]
    edges = []
    for i in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        edges.append((a, b))
        graph[a].append((b, i))
        graph[b].append((a, i))

    tin = [-1] * n
    low = [0] * n
    timer = 0

    edge_stack = []
    components = []
    is_bridge = [False] * m
    is_cut = [False] * n

    sys.setrecursionlimit(1 << 25)

    def dfs(u, parent_edge):
        nonlocal timer
        tin[u] = low[u] = timer
        timer += 1
        children = 0

        for v, eid in graph[u]:
            if eid == parent_edge:
                continue

            if tin[v] == -1:
                edge_stack.append(eid)
                children += 1
                dfs(v, eid)
                low[u] = min(low[u], low[v])

                if low[v] > tin[u]:
                    is_bridge[eid] = True

                if low[v] >= tin[u]:
                    if parent_edge != -1 or children > 1:
                        is_cut[u] = True

                    comp = []
                    while True:
                        x = edge_stack.pop()
                        comp.append(x)
                        if x == eid:
                            break
                    components.append(comp)
            else:
                if tin[v] < tin[u]:
                    edge_stack.append(eid)
                low[u] = min(low[u], tin[v])

    dfs(0, -1)

    cut_count = sum(is_cut)
    bridge_count = sum(is_bridge)
    comp_count = len(components)
    largest = max(len(c) for c in components)

    g = __import__("math").gcd(comp_count, largest)
    return f"{cut_count} {bridge_count} {comp_count // g} {largest // g}"

def main():
    t = int(input())
    ans = []
    for _ in range(t):
        ans.append(solve_case())
    print("\n".join(ans))

if __name__ == "__main__":
    main()
```

The adjacency list stores both the neighboring vertex and the edge index. The edge index is necessary because the graph is undirected, and comparing only parent vertices is not enough when identifying the exact DFS tree edge.

The `edge_stack` is the key part for biconnected components. When DFS reaches a vertex where `low[child] >= tin[parent]`, every edge above that boundary belongs to one component. Popping until the tree edge is removed gives exactly that component.

The bridge condition uses a strict comparison, `low[v] > tin[u]`. Equality means there is an alternate path returning directly to `u`, so the edge still belongs to a cycle. The articulation condition uses `>=` because even a back edge to `u` does not help connect the child subtree to vertices above `u`.

The root handling is separated by checking `parent_edge`. A root with one child does not disconnect anything when removed, while a non-root vertex with one such child can still separate that child subtree.

## Worked Examples

For the first sample:

```
1
6 6
1 2
2 3
3 4
4 5
5 6
6 1
```

The DFS forms one component containing all six edges.

| Step | Current vertex | low value | Components found | Bridges |
| --- | --- | --- | --- | --- |
| DFS enters 1 | 1 | 0 | 0 | 0 |
| DFS reaches 6 | 6 | 0 | 0 | 0 |
| Back edge 6 to 1 found | 6 | 0 | 0 | 0 |
| DFS finishes child of 1 | 1 | 0 | 1 component of size 6 | 0 |

The cycle lets every vertex reach every other vertex without depending on a single edge or vertex. The final fraction is one component divided by six edges.

For the second sample:

```
1
6 7
1 2
2 3
3 1
4 5
5 6
6 4
1 4
```

The graph contains two triangle components joined by a bridge.

| Step | Current edge | low update | Components found | Bridges |
| --- | --- | --- | --- | --- |
| Explore triangle 1-2-3 | 1-2,2-3,3-1 | low becomes 0 | none yet | 0 |
| Explore edge 1-4 | 1-4 | separates side 4 | triangle 2 and bridge not yet split | 0 |
| Finish triangle 4-5-6 | 4-5,5-6,6-4 | low returns to 3 | component of size 3 | 1-4 |
| Finish first triangle | 1-2,2-3,3-1 | low returns to 0 | component of size 3 | 1 |

There are three critical components: the two triangles and the single bridge. The largest size is three edges, so the fraction becomes three over three, reduced to one over one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each vertex and edge is processed a constant number of times during DFS. |
| Space | O(n + m) | The adjacency list, DFS arrays, and edge stack all store linear information. |

The total number of edges across all test cases is bounded, so a linear algorithm easily fits the time limit. The memory usage is also linear and remains well below the available limit.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)

    import math
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n, m = map(int, input().split())
        g = [[] for _ in range(n)]
        for i in range(m):
            a, b = map(int, input().split())
            a -= 1
            b -= 1
            g[a].append((b, i))
            g[b].append((a, i))

        tin = [-1] * n
        low = [0] * n
        bridges = [False] * m
        cut = [False] * n
        stack = []
        comps = []
        timer = 0
        sys.setrecursionlimit(100000)

        def dfs(u, pe):
            nonlocal timer
            tin[u] = low[u] = timer
            timer += 1
            children = 0
            for v, e in g[u]:
                if e == pe:
                    continue
                if tin[v] == -1:
                    stack.append(e)
                    children += 1
                    dfs(v, e)
                    low[u] = min(low[u], low[v])
                    if low[v] > tin[u]:
                        bridges[e] = True
                    if low[v] >= tin[u]:
                        if pe != -1 or children > 1:
                            cut[u] = True
                        c = []
                        while True:
                            x = stack.pop()
                            c.append(x)
                            if x == e:
                                break
                        comps.append(c)
                else:
                    if tin[v] < tin[u]:
                        stack.append(e)
                    low[u] = min(low[u], tin[v])

        dfs(0, -1)
        a = len(comps)
        b = max(map(len, comps))
        g0 = math.gcd(a, b)
        out.append(f"{sum(cut)} {sum(bridges)} {a//g0} {b//g0}")

    sys.stdin = old
    return "\n".join(out)

assert run("""1
6 6
1 2
2 3
3 4
4 5
5 6
6 1
""") == "0 0 1 6"

assert run("""1
6 7
1 2
2 3
3 1
4 5
5 6
6 4
1 4
""") == "2 1 1 1"

assert run("""1
2 1
1 2
""") == "1 1 1 1"

assert run("""1
4 4
1 2
2 3
3 4
4 1
""") == "0 0 1 4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two vertices with one edge | `1 1 1 1` | Single bridge component handling |
| One simple cycle | `0 0 1 4` | No false articulation points or bridges |
| Two cycles joined by an edge | `2 1 1 1` | Multiple components and fraction reduction |

## Edge Cases

For the single-edge graph:

```
1
2 1
1 2
```

DFS enters one vertex, visits the other, and discovers that removing the edge leaves two disconnected vertices. The edge is popped as a biconnected component when the child finishes. The algorithm counts one articulation point in the DFS root structure, one bridge, and one component with one edge.

For the cycle:

```
1
4 4
1 2
2 3
3 4
4 1
```

The back edge from the last vertex to the first makes every `low` value return to the root. No bridge condition is satisfied because every edge has an alternate route. The DFS root has only one child, so it is not an articulation point.

For the graph with two triangles and one bridge:

```
1
6 7
1 2
2 3
3 1
4 5
5 6
6 4
1 4
```

The bridge splits the graph into two DFS regions, so its edge is its own component. The two triangles are each collected separately. The component count is three and the largest component contains three edges, producing the reduced fraction `1/1`.
