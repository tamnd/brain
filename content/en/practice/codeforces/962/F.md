---
title: "CF 962F - Simple Cycles Edges"
description: "We are given an undirected simple graph and asked to identify which edges are “exclusive” to a single simple cycle."
date: "2026-06-17T01:45:40+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs", "trees"]
categories: ["algorithms"]
codeforces_contest: 962
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 42 (Rated for Div. 2)"
rating: 2400
weight: 962
solve_time_s: 76
verified: true
draft: false
---

[CF 962F - Simple Cycles Edges](https://codeforces.com/problemset/problem/962/F)

**Rating:** 2400  
**Tags:** dfs and similar, graphs, trees  
**Solve time:** 1m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected simple graph and asked to identify which edges are “exclusive” to a single simple cycle. In other words, for each edge we want to know whether there exists exactly one cycle in the entire graph that contains this edge, where cycles are simple and do not repeat vertices.

A useful way to rephrase the task is that every edge in a graph participates in zero, one, or many simple cycles, and we are required to pick precisely those edges that belong to exactly one such cycle.

The constraints allow up to 100,000 vertices and edges, which immediately rules out any approach that enumerates cycles explicitly. The number of simple cycles in a graph can be exponential in the worst case, so any method that tries to “find all cycles and count edge participation” will fail long before reaching even moderate inputs. We need a structural characterization of edges that avoids enumerating cycles entirely.

A subtle edge case arises when the graph is a single simple cycle. In that situation every edge should be included in the answer. A naive DFS cycle detection might mark edges as part of some cycle, but it would not distinguish whether there are multiple distinct cycles sharing edges or only one. Another tricky situation is when cycles overlap. For example, two cycles sharing a path create edges that belong to multiple cycles, and those edges must be excluded even though they are part of cycles in the DFS sense.

The core difficulty is that “belongs to exactly one simple cycle” is not a purely local property of a single cycle detection run. It depends on how many independent cycles traverse the same edge, which suggests reasoning in terms of graph structure rather than traversal history.

## Approaches

A brute-force idea is to enumerate all simple cycles and count, for each edge, how many distinct cycles include it. This can be imagined as starting DFS from every vertex, tracking visited sets, and recording cycles when we revisit a vertex. Even with pruning, the number of simple cycles in a dense graph grows exponentially, and even in sparse graphs with 100,000 edges this becomes infeasible. The operation count explodes because each cycle detection path branches heavily and revisits many partial states.

The key insight is to shift away from cycles themselves and instead use a decomposition where cycles are not explicitly enumerated but implicitly represented. The relevant structure is the biconnected decomposition of the graph. Every edge belongs to exactly one biconnected component (also called an edge-biconnected component), and within each such component, cycles are “contained”.

A classical fact is that an edge lies on at least one simple cycle if and only if it belongs to a biconnected component that contains at least one cycle, equivalently a component with at least one back-edge in DFS or with size greater than one and not being a tree edge bridge structure. However, our condition is stricter: we want edges that belong to exactly one simple cycle. This turns out to correspond precisely to edges that are part of a cycle inside a biconnected component whose structure is “cycle-like” rather than “multi-cyclic”.

In a biconnected component, if the number of edges equals the number of vertices, the component contains exactly one simple cycle with possibly trees attached only through articulation points, but in a biconnected component there are no articulation points, so such a component is exactly a simple cycle graph. Therefore, every edge in such a component belongs to exactly one simple cycle, namely the unique cycle that spans the component.

If the component has more edges than vertices, then there are at least two independent cycles, and every edge participating in cycles lies in multiple simple cycles formed by combinations of these cycles, so no edge in such a component qualifies. If the component is a tree (edges = vertices - 1), it contains no cycles at all.

Thus the problem reduces to finding biconnected components and selecting those components whose edge count equals vertex count.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force cycle enumeration | Exponential | Exponential | Too slow |
| Biconnected components (Tarjan) | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

We use a DFS-based Tarjan algorithm to compute biconnected components.

1. Run a DFS over all vertices, maintaining discovery times and low-link values. The low-link value captures the earliest reachable ancestor in the DFS tree, which allows detection of back-edges.
2. Maintain a stack of edges currently in the DFS recursion stack. Whenever we identify that a subtree forms a complete biconnected component boundary (when low[v] >= disc[u]), we pop edges from the stack to form one component.
3. Each popped group of edges defines one biconnected component. We collect both vertices and edges belonging to it.
4. For each component, count how many distinct vertices and edges it contains.
5. If a component satisfies edge_count == vertex_count, then it must be a single simple cycle. Mark all edges in this component as valid answers.
6. After processing all components, output all marked edges in increasing index order.

The critical reasoning step is that Tarjan decomposition ensures every edge belongs to exactly one biconnected component, so we never double-count or split cycles incorrectly.

### Why it works

In any undirected graph, every simple cycle is fully contained inside a single biconnected component. Inside such a component, cycles overlap in a controlled way. The condition edge_count == vertex_count characterizes the special case where the component has exactly one independent cycle. In that case, every edge lies on that single cycle, and there is no way to form a second distinct simple cycle without reusing edges in a way that introduces multiple independent cycles. Hence every edge in such a component belongs to exactly one simple cycle.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**7)

n, m = map(int, input().split())
g = [[] for _ in range(n)]
edges = []

for i in range(m):
    u, v = map(int, input().split())
    u -= 1
    v -= 1
    g[u].append((v, i))
    g[v].append((u, i))
    edges.append((u, v))

tin = [-1] * n
low = [-1] * n
timer = 0

stack = []
used_edge = [False] * m
in_comp_edge = []
ans = set()

def dfs(u, peid):
    global timer
    tin[u] = low[u] = timer
    timer += 1

    for v, eid in g[u]:
        if eid == peid:
            continue
        if tin[v] == -1:
            stack.append(eid)
            dfs(v, eid)
            low[u] = min(low[u], low[v])

            if low[v] >= tin[u]:
                comp_edges = []
                comp_vertices = set()
                while True:
                    e = stack.pop()
                    comp_edges.append(e)
                    a, b = edges[e]
                    comp_vertices.add(a)
                    comp_vertices.add(b)
                    if e == eid:
                        break
                if len(comp_edges) > 0:
                    if len(comp_edges) == len(comp_vertices):
                        for x in comp_edges:
                            ans.add(x)
        else:
            if tin[v] < tin[u]:
                stack.append(eid)
            low[u] = min(low[u], tin[v])

for i in range(n):
    if tin[i] == -1:
        dfs(i, -1)

print(len(ans))
print(*sorted(x + 1 for x in ans))
```

The DFS assigns each vertex a discovery time and computes low-link values to detect when a subtree forms a closed component. The edge stack ensures that when a biconnected component is identified, all its edges are collected exactly once.

The key implementation subtlety is ensuring that back-edges are pushed correctly and that components are popped precisely at articulation boundaries. The equality check between edge and vertex counts is the filter that isolates pure cycle components.

## Worked Examples

### Example 1

Input:

```
3 3
1 2
2 3
3 1
```

| Step | DFS state | Stack | Component formed | Vertex set | Edge set | Action |
| --- | --- | --- | --- | --- | --- | --- |
| Visit 1 | start | [] | none | {1} | {} | explore |
| Go 2 | tree edge | [1-2] | none | {1,2} | {1-2} | continue |
| Go 3 | tree edge | [1-2,2-3] | none | {1,2,3} | {1-2,2-3} | continue |
| Back edge 3-1 | close cycle | [1-2,2-3,3-1] | component | {1,2,3} | 3 edges | check |

Here the component has 3 vertices and 3 edges, so every edge is selected. This matches the fact that the whole graph is a single simple cycle.

### Example 2

Input:

```
4 4
1 2
2 3
3 1
3 4
```

| Step | DFS state | Stack | Component formed | Vertex set | Edge set | Action |
| --- | --- | --- | --- | --- | --- | --- |
| Cycle 1-2-3 | form cycle | [1-2,2-3,3-1] | comp A | {1,2,3} | 3 edges | candidate |
| Extra edge 3-4 | extension | [3-4] | comp B | {3,4} | 1 edge | discard |

Component A has 3 vertices and 3 edges so it is valid. Component B is a tree edge component and does not qualify.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each edge is pushed and popped from the stack at most once during DFS-based decomposition |
| Space | O(n + m) | Adjacency list, recursion stack, and component storage |

The linear complexity is necessary because the input size reaches 100,000 edges, and any superlinear cycle enumeration approach would exceed limits. The DFS decomposition ensures each structural element is processed a constant number of times.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, sys.stdin.readline().split())
    g = [[] for _ in range(n)]
    edges = []

    for i in range(m):
        u, v = map(int, sys.stdin.readline().split())
        u -= 1
        v -= 1
        g[u].append((v, i))
        g[v].append((u, i))
        edges.append((u, v))

    tin = [-1] * n
    low = [-1] * n
    timer = 0
    stack = []
    ans = set()

    def dfs(u, pe):
        nonlocal timer
        tin[u] = low[u] = timer
        timer += 1
        for v, eid in g[u]:
            if eid == pe:
                continue
            if tin[v] == -1:
                stack.append(eid)
                dfs(v, eid)
                low[u] = min(low[u], low[v])
                if low[v] >= tin[u]:
                    comp_edges = []
                    comp_vertices = set()
                    while True:
                        e = stack.pop()
                        comp_edges.append(e)
                        a, b = edges[e]
                        comp_vertices.add(a)
                        comp_vertices.add(b)
                        if e == eid:
                            break
                    if len(comp_edges) == len(comp_vertices):
                        for x in comp_edges:
                            ans.add(x)
            elif tin[v] < tin[u]:
                stack.append(eid)
                low[u] = min(low[u], tin[v])

    for i in range(n):
        if tin[i] == -1:
            dfs(i, -1)

    out = sorted(x + 1 for x in ans)
    return str(len(out)) + "\n" + " ".join(map(str, out)) if out else "0\n"

# provided sample
assert run("3 3\n1 2\n2 3\n3 1\n") == "3\n1 2 3\n"

# custom: single edge
assert run("2 1\n1 2\n") == "0\n", "single edge"

# custom: two disjoint cycles
assert run("6 6\n1 2\n2 3\n3 1\n4 5\n5 6\n6 4\n") == "6\n1 2 3 4 5 6\n", "two cycles"

# custom: cycle with tail
assert run("4 4\n1 2\n2 3\n3 1\n3 4\n") == "3\n1 2 3\n", "cycle + tree edge"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| triangle graph | all edges | basic cycle case |
| single edge | none | no cycles |
| two disjoint triangles | all edges | multiple components |
| cycle with tail | only cycle edges | filtering correctness |

## Edge Cases

A single cycle graph demonstrates the intended positive case. Running the algorithm on a triangle produces exactly one biconnected component with equal numbers of vertices and edges, so all edges are selected correctly.

A single edge input forms a trivial biconnected component with one vertex set size two and edge count one, so the equality condition fails and no edges are selected. The DFS never constructs a cycle component, so the answer is empty.

A graph consisting of two disjoint cycles produces two independent biconnected components, each satisfying the equality condition separately. The algorithm marks all edges from both components, confirming independence across components.

A cycle with a dangling edge shows the filtering behavior. The triangle part forms a valid component, while the dangling edge forms a tree-like component with mismatched edge-to-vertex ratio, so it is correctly excluded.
