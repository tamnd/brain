---
title: "CF 1217D - Coloring Edges"
description: "We are given a directed graph where each edge is fixed in advance, and we must assign a color (an integer label) to every edge. The constraint is not about vertices but about directed cycles: if you look at all edges of a single color, they must not contain any directed cycle."
date: "2026-06-15T18:50:02+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dfs-and-similar", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1217
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 72 (Rated for Div. 2)"
rating: 2100
weight: 1217
solve_time_s: 161
verified: true
draft: false
---

[CF 1217D - Coloring Edges](https://codeforces.com/problemset/problem/1217/D)

**Rating:** 2100  
**Tags:** constructive algorithms, dfs and similar, graphs  
**Solve time:** 2m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed graph where each edge is fixed in advance, and we must assign a color (an integer label) to every edge. The constraint is not about vertices but about directed cycles: if you look at all edges of a single color, they must not contain any directed cycle.

The task is to minimize how many colors are used while still ensuring that every monochromatic subgraph is acyclic.

A useful way to reinterpret the requirement is that each color class must form a Directed Acyclic Graph. We are effectively decomposing the edge set into the minimum number of acyclic directed subgraphs.

The constraints are small enough that an O(nm) or O(m log m) construction is fine, since both n and m are at most 5000. This suggests that we can afford graph traversals, repeated DFS, or greedy constructions over edges without worrying about asymptotic tightness beyond quadratic.

A naive idea would be to assign colors arbitrarily or by grouping edges, but cycles immediately break such attempts. For example, in a directed triangle 1 → 2 → 3 → 1, if all edges share the same color, we already violate the condition. This shows that even small strongly connected components force multiple colors.

A subtle failure case appears when edges are processed without respecting dependencies. For instance, in a graph where edges are given in arbitrary order, assigning colors greedily without tracking reachability can produce a situation where a back edge in DFS shares a color with forward edges, creating a monochromatic cycle. A correct approach must ensure that any edge participating in a DFS back-edge structure is separated in color from the DFS tree edges that precede it.

The key structural insight is that the answer is tightly connected to the depth of back edges in a DFS tree.

## Approaches

The brute-force direction would be to attempt all possible assignments of colors to edges, increasing k from 1 upward, and checking whether each coloring is valid. Validity checking requires verifying that each color class is acyclic, which itself requires a cycle detection per color, typically O(n + m). Even if we restrict k to m, this becomes combinatorial and grows as k^m in the worst interpretation, which is infeasible.

We can simplify the search space by noticing that we do not actually need to try assignments. Instead, we can construct a coloring directly.

The central observation is that cycles in a directed graph are exposed by DFS back edges. During a DFS, when we traverse an edge to a currently active node, that edge closes a cycle. If we ensure that such edges receive a strictly larger color than the DFS tree depth at which they occur, we prevent them from sharing a color with all edges that participate in the same DFS stack structure.

This leads to a constructive idea: maintain a DFS visitation state and assign colors based on whether an edge goes forward in the DFS tree or goes backward to an active node. Forward edges can safely share color 1 because they cannot form a directed cycle among themselves if they respect DFS ordering. Back edges must be assigned a different color, since each back edge indicates a dependency violation relative to DFS order.

A careful refinement shows that we only ever need two colors. If the graph has no cycles, one color is sufficient. If there is at least one back edge, two colors are enough to separate tree/forward edges from back edges in a way that prevents monochromatic cycles.

The problem reduces to detecting whether the graph contains a directed cycle reachable in DFS and labeling edges accordingly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n + m) | Too slow |
| DFS-based constructive coloring | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

We perform a DFS over the directed graph while tracking node states.

1. Build adjacency lists for the graph, storing also the index of each edge so we can assign colors in input order. This is necessary because output is tied to original edge ordering.
2. Maintain a visitation state array for nodes with three states: unvisited, active in recursion stack, and fully processed. This allows us to detect back edges precisely.
3. Start DFS from every unvisited node. The graph may be disconnected, so we must cover all components.
4. When exploring an edge u → v, we classify it based on the state of v. If v is unvisited, we treat it as a DFS tree edge and continue DFS.
5. If v is currently active, the edge u → v is a back edge, meaning it closes a directed cycle. We assign this edge color 2.
6. If v is already fully processed, the edge is a forward or cross edge. It cannot create a cycle in the DFS stack context, so it is assigned color 1.
7. DFS completion marks a node as fully processed.

The final answer uses k = 2 if any back edge was encountered, otherwise k = 1.

### Why it works

The DFS ordering induces a partial order over edges that are not back edges. Any edge that is not a back edge respects this order and cannot participate in a directed cycle within the same color class. Back edges are precisely those that violate this order by pointing into the active recursion stack, which guarantees they are responsible for closing cycles. By isolating them into a separate color, we break every potential monochromatic cycle, since every directed cycle must contain at least one back edge in any DFS traversal.

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
    edges.append((u, v))

color = [1] * m
state = [0] * n  # 0 = unvisited, 1 = active, 2 = done

has_cycle = False

def dfs(u):
    global has_cycle
    state[u] = 1
    for v, idx in g[u]:
        if state[v] == 0:
            dfs(v)
        elif state[v] == 1:
            color[idx] = 2
            has_cycle = True
        else:
            color[idx] = 1
    state[u] = 2

for i in range(n):
    if state[i] == 0:
        dfs(i)

k = 2 if has_cycle else 1
print(k)
print(*color)
```

The implementation directly encodes the DFS classification. The key detail is that edge coloring is decided at the moment we inspect an edge, based on whether its destination is in the recursion stack or already processed. The recursion stack detection is handled by the state array, where value 1 means active.

The final k depends on whether we ever encountered a back edge. If none exist, the graph is already a DAG and all edges can safely share color 1.

## Worked Examples

### Example 1

Input:

```
4 5
1 2
1 3
3 4
2 4
1 4
```

All edges form a DAG, so no back edges appear.

| Step | Edge | State of v | Type | Color |
| --- | --- | --- | --- | --- |
| 1 | 1→2 | unvisited | tree | 1 |
| 2 | 1→3 | unvisited | tree | 1 |
| 3 | 3→4 | unvisited | tree | 1 |
| 4 | 2→4 | done | forward | 1 |
| 5 | 1→4 | done | forward | 1 |

No cycle is detected, so k = 1.

This trace confirms that in a DAG all edges remain safe in a single color class.

### Example 2

Consider a graph:

```
3 3
1 2
2 3
3 1
```

This is a directed cycle.

| Step | Edge | State of v | Type | Color |
| --- | --- | --- | --- | --- |
| 1 | 1→2 | unvisited | tree | 1 |
| 2 | 2→3 | unvisited | tree | 1 |
| 3 | 3→1 | active | back | 2 |

Here the last edge closes the cycle and must be separated.

This confirms that every directed cycle forces at least one edge into a second color.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each node and edge is processed once during DFS traversal |
| Space | O(n + m) | Adjacency list plus recursion stack and state arrays |

The graph size is small enough that linear traversal is easily within limits. Even in worst-case dense edge patterns up to 5000 edges, DFS runs comfortably in time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    g = [[] for _ in range(n)]
    color = [1] * m
    state = [0] * n

    edges = []
    for i in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append((v, i))
        edges.append((u, v))

    sys.setrecursionlimit(10**7)
    has_cycle = False

    def dfs(u):
        nonlocal has_cycle
        state[u] = 1
        for v, idx in g[u]:
            if state[v] == 0:
                dfs(v)
            elif state[v] == 1:
                color[idx] = 2
                has_cycle = True
            else:
                color[idx] = 1
        state[u] = 2

    for i in range(n):
        if state[i] == 0:
            dfs(i)

    k = 2 if has_cycle else 1
    return str(k) + "\n" + " ".join(map(str, color))

# provided sample
assert run("""4 5
1 2
1 3
3 4
2 4
1 4
""") == "1\n1 1 1 1 1"

# simple cycle
assert run("""3 3
1 2
2 3
3 1
""") == "2\n1 1 2"

# chain (DAG)
assert run("""5 4
1 2
2 3
3 4
4 5
""") == "1\n1 1 1 1"

# mixed graph
assert run("""4 4
1 2
2 3
3 1
3 4
""") in ["2\n1 1 2 1", "2\n1 1 2 1"]

# single cycle edge case structure
assert run("""3 3
1 3
3 2
2 1
""")[0] == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| DAG chain | 1 color | single-color feasibility |
| 3-cycle | 2 colors | cycle detection |
| mixed graph | 2 colors | partial cyclic structure |
| reverse cycle | 2 colors | arbitrary cycle orientation |

## Edge Cases

A key edge case is a graph that is already a DAG. In such cases, no recursion stack back edges appear, so the algorithm assigns all edges color 1. This matches the optimal answer since a DAG has no cycles by definition.

Another edge case is a graph where cycles exist but are separated by structure, such as two disjoint cycles. The DFS will detect back edges in both components, but still only requires color 2 globally. The separation works because every back edge is isolated into the second class regardless of where it appears.

A final subtle case is when cycles are formed through cross edges rather than immediate back edges in some DFS ordering. Even then, any directed cycle must contain at least one back edge in DFS classification, so the algorithm still identifies at least one edge requiring the second color, ensuring correctness.
