---
title: "CF 9E - Interestring graph and Apples"
description: "We start with an undirected multigraph. Multiple edges are allowed, and loops are also allowed. We may add new edges, and the goal is to transform the graph into a very specific structure."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dsu", "graphs"]
categories: ["algorithms"]
codeforces_contest: 9
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 9 (Div. 2 Only)"
rating: 2300
weight: 9
solve_time_s: 108
verified: true
draft: false
---
[CF 9E - Interestring graph and Apples](https://codeforces.com/problemset/problem/9/E)

**Rating:** 2300  
**Tags:** dfs and similar, dsu, graphs  
**Solve time:** 1m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with an undirected multigraph. Multiple edges are allowed, and loops are also allowed. We may add new edges, and the goal is to transform the graph into a very specific structure.

A graph is called interesting when every vertex belongs to exactly one cycle. Since connected components are allowed, each connected component must look like a single simple cycle, possibly of length one if it is a loop.

Another way to say the same thing is that every connected component must be unicyclic. A tree is not allowed because some vertices would belong to no cycle, and a component with two different cycles is not allowed because vertices on the overlap would belong to more than one cycle.

We are asked to add as few edges as possible. Among all optimal answers, we must output the lexicographically smallest set of added edges.

The graph has at most 50 vertices, but up to 2500 edges because multiple edges and loops are allowed. The small value of `n` means even `O(n^3)` or `O(n^4)` solutions are completely safe. The harder part is not performance, but reasoning about the structure and lexicographic minimality.

The tricky part is understanding what configurations are already impossible.

Suppose a connected component already contains two different cycles. Then no amount of adding edges can fix it, because we are only allowed to add edges, never remove them. For example:

```
4 4
1 2
2 3
3 1
3 4
```

Vertices `1,2,3` already form a cycle. Vertex `4` is attached as a tree node. This component is still valid, because we can add edge `(4,4)` and then every vertex belongs to exactly one cycle.

Now compare with:

```
4 5
1 2
2 3
3 1
2 4
4 3
```

This component already contains two cycles:

`1-2-3-1` and `2-4-3-2`.

No added edges can remove this overlap, so the correct answer is `NO`.

Loops also require care. A loop already counts as a cycle involving that vertex alone. If a vertex with a loop participates in any other cycle, the graph becomes invalid immediately. For example:

```
2 2
1 1
1 2
```

This graph is still repairable. We can add `(2,2)`.

But:

```
2 3
1 1
1 2
2 1
```

contains both the loop at `1` and the cycle `1-2-1`, so vertex `1` belongs to two cycles. The answer is `NO`.

Another subtle case is parallel edges. Two parallel edges between `u` and `v` form a cycle of length two. For example:

```
2 2
1 2
1 2
```

is already an interesting graph. Each vertex belongs to exactly one cycle.

A careless DFS that assumes simple graphs would miss this.

Finally, lexicographic order matters globally, not edge-by-edge independently. If two different optimal constructions exist, we must prefer the one whose flattened sequence of endpoints is lexicographically smaller.

## Approaches

A brute-force approach would try all possible sets of added edges and check whether the resulting graph becomes interesting. Since there are `n(n+1)/2` possible edges including loops, even for `n = 50` the search space is astronomical. Exhaustive search is completely infeasible.

The first useful observation is structural. In a connected component with `v` vertices and `e` edges, the number of independent cycles equals:

```
e - v + 1
```

For an interesting component, every vertex must belong to exactly one cycle. That means the component must contain exactly one cycle, because two different cycles would force some vertex to belong to multiple cycles or create disconnected cyclic regions.

So every connected component must satisfy:

```
e = v
```

A connected component with `e = v - 1` is a tree. It contains no cycle yet, but we can create exactly one by adding one edge.

A connected component with `e > v` already has at least two cycles, so it is impossible forever because edges cannot be removed.

This transforms the problem into something much simpler.

Every component falls into one of three categories:

First, components with `e > v` are immediately impossible.

Second, components with `e = v` are already good. We should not touch them.

Third, components with `e = v - 1` are trees. We need exactly one added edge inside each such component to create a single cycle.

Now the task becomes:

For every tree component, add one edge between two vertices that are not already connected by an edge.

Why must the endpoints be non-adjacent already? Because adding another edge between adjacent vertices would create a cycle that reuses the existing path of length one, producing a multi-edge cycle. That is actually valid. The real restriction is different.

The issue is that adding any edge inside a tree creates exactly one cycle, which is always acceptable. Even parallel edges and loops are allowed. So every tree component can always be fixed with one edge.

The remaining challenge is lexicographic minimality.

Suppose we have a tree component. Among all possible added edges inside it, we want the lexicographically smallest pair `(u,v)` with `u <= v`.

Since components are independent, choosing the smallest valid edge inside each component independently also minimizes the global sequence after sorting.

We can simply try all pairs `(u,v)` in lexicographic order and pick the first one whose addition creates exactly one cycle without violating the condition.

For a tree, every added edge works. So the lexicographically smallest valid edge is simply the smallest pair inside the component.

A loop is always allowed in a tree component because the vertex previously belonged to no cycle. Adding `(u,u)` creates a cycle only for `u`, while all other vertices remain outside cycles, which is not enough. So loops are not valid unless the component has size one.

This is the key subtlety.

To make every vertex belong to the same cycle, the added edge must connect two distinct vertices. The created cycle then includes the whole path between them.

In a tree, adding edge `(u,v)` creates a cycle consisting exactly of the path from `u` to `v`.

For every vertex in the component to belong to that cycle, the path between `u` and `v` must contain every vertex of the component. That means the tree must itself be a simple path, and `u,v` must be its endpoints.

This is the real characterization.

So a component is repairable iff:

```
e = v
```

or

```
e = v - 1
```

and in the second case the component must be a path.

A branching tree can never become interesting with one added edge because some branch vertex would stay outside the cycle.

For example:

```
4 3
1 2
2 3
2 4
```

No added edge can make all four vertices belong to exactly one cycle.

The decisive observation is that every valid connected component must already be either:

```
a cycle
```

or

```
a path
```

because degrees in the final graph must all become exactly two inside non-loop cycles.

Thus:

If a component already has a vertex of degree greater than two, impossible.

If a component has more than two vertices of degree one, impossible.

If a component is a path, connect its two endpoints.

If a component is an isolated vertex, add a loop.

Among all optimal answers, this greedy construction is automatically lexicographically smallest because each component has only one valid completion.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n²) | O(n²) | Accepted |

## Algorithm Walkthrough

1. Build the multigraph exactly as given, including loops and parallel edges.
2. Compute the degree of every vertex carefully.

A loop contributes `2` to the degree in undirected graphs.
3. Find connected components using DFS or DSU.
4. For each component, count:

the number of vertices,

the number of edges,

and the degree of every vertex inside it.
5. If any vertex has degree greater than `2`, output `NO`.

In an interesting graph every vertex belongs to exactly one cycle, so every vertex must have degree exactly `2`.
6. If the component already satisfies `edges = vertices`, then it is already a cycle.

No edge should be added.
7. Otherwise the component must satisfy `edges = vertices - 1`.

If not, output `NO`.
8. In such a component, count vertices of degree `1`.

A valid path component must have exactly two endpoints.
9. If the component has exactly one vertex and no edges, add a loop `(v,v)`.
10. Otherwise connect the two degree-1 vertices.

This closes the path into a cycle containing every vertex exactly once.
11. Store all added edges and sort them lexicographically.
12. Output the resulting list.

### Why it works

Inside an interesting connected component, every vertex must lie on one simple cycle. That forces every vertex to have degree exactly two.

A connected graph where every vertex has degree two is exactly a cycle component, including loops and 2-cycles from parallel edges.

If a component already satisfies this, we leave it unchanged.

If a component has one fewer edge than vertices, it is a tree. The only trees that can become cycles after adding one edge are paths, because every vertex must end with degree two. Connecting the two endpoints transforms the path into a cycle containing all vertices.

Any component violating these structural properties can never be repaired by adding edges alone.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**6)

def solve():
    n, m = map(int, input().split())

    adj = [[] for _ in range(n)]
    deg = [0] * n
    edges = []

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1

        adj[u].append(v)
        if u != v:
            adj[v].append(u)

        deg[u] += 1
        deg[v] += 1

        edges.append((u, v))

    visited = [False] * n
    answer = []

    def dfs(start, comp):
        stack = [start]
        visited[start] = True

        while stack:
            u = stack.pop()
            comp.append(u)

            for v in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    stack.append(v)

    for i in range(n):
        if visited[i]:
            continue

        comp = []
        dfs(i, comp)

        comp_set = set(comp)

        edge_count = 0
        for u, v in edges:
            if u in comp_set and v in comp_set:
                edge_count += 1

        size = len(comp)

        bad = False
        leaves = []

        for v in comp:
            if deg[v] > 2:
                bad = True
                break

            if deg[v] == 1:
                leaves.append(v)

        if bad:
            print("NO")
            return

        if edge_count == size:
            for v in comp:
                if deg[v] != 2:
                    print("NO")
                    return

        elif edge_count == size - 1:
            if size == 1:
                if deg[comp[0]] != 0:
                    print("NO")
                    return

                answer.append((comp[0] + 1, comp[0] + 1))

            else:
                if len(leaves) != 2:
                    print("NO")
                    return

                u, v = sorted([leaves[0] + 1, leaves[1] + 1])
                answer.append((u, v))

        else:
            print("NO")
            return

    answer.sort()

    print("YES")
    print(len(answer))

    for u, v in answer:
        print(u, v)

solve()
```

The solution begins by constructing the graph exactly as given. Parallel edges and loops are preserved because they affect cycle structure.

Degree handling is subtle. A loop contributes twice to the degree of its vertex in an undirected graph. The implementation achieves this automatically because both endpoints are incremented even when `u == v`.

Connected components are discovered with DFS. Since `n <= 50`, efficiency is not a concern, but iterative DFS avoids recursion depth issues entirely.

For each component we recompute the number of edges by scanning the original edge list. This works cleanly even with loops and parallel edges.

The central validation is the degree condition. Any vertex with degree larger than two makes the answer impossible immediately.

A component with `edges == vertices` must already be a cycle. Every vertex must already have degree exactly two.

A component with `edges == vertices - 1` is a tree. The only valid trees are paths. For a path, the two degree-1 vertices are connected to close the cycle.

The isolated-vertex case requires special treatment. Connecting the vertex to itself creates a loop cycle of length one.

Finally, all added edges are sorted lexicographically before output.

## Worked Examples

### Example 1

Input:

```
3 2
1 2
2 3
```

The graph is a single path.

| Step | Component | Degrees | Edge Count | Action |
| --- | --- | --- | --- | --- |
| 1 | {1,2,3} | [1,2,1] | 2 | Path detected |
| 2 | endpoints = (1,3) | - | - | Add (1,3) |

Final added edges:

```
1 3
```

The new graph becomes the cycle `1-2-3-1`, and every vertex belongs to exactly one cycle.

### Example 2

Input:

```
4 3
1 2
2 3
2 4
```

This graph is a branching tree.

| Step | Component | Degrees | Edge Count | Action |
| --- | --- | --- | --- | --- |
| 1 | {1,2,3,4} | [1,3,1,1] | 3 | Degree 3 found |

Since vertex `2` already has degree greater than two, no final interesting graph is possible.

Output:

```
NO
```

This trace demonstrates the key invariant: every vertex in the final graph must have degree exactly two.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | DFS plus repeated edge scans over tiny constraints |
| Space | O(n²) | Adjacency storage in worst case multigraph |

With only 50 vertices and at most 2500 edges, this solution easily fits within the limits. Even a cubic solution would pass comfortably.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m = map(int, input().split())

    adj = [[] for _ in range(n)]
    deg = [0] * n
    edges = []

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1

        adj[u].append(v)
        if u != v:
            adj[v].append(u)

        deg[u] += 1
        deg[v] += 1

        edges.append((u, v))

    visited = [False] * n
    answer = []

    def dfs(start, comp):
        stack = [start]
        visited[start] = True

        while stack:
            u = stack.pop()
            comp.append(u)

            for v in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    stack.append(v)

    out = []

    for i in range(n):
        if visited[i]:
            continue

        comp = []
        dfs(i, comp)

        comp_set = set(comp)

        edge_count = 0
        for u, v in edges:
            if u in comp_set and v in comp_set:
                edge_count += 1

        size = len(comp)

        leaves = []

        for v in comp:
            if deg[v] > 2:
                return "NO\n"

            if deg[v] == 1:
                leaves.append(v)

        if edge_count == size:
            for v in comp:
                if deg[v] != 2:
                    return "NO\n"

        elif edge_count == size - 1:
            if size == 1:
                answer.append((comp[0] + 1, comp[0] + 1))
            else:
                if len(leaves) != 2:
                    return "NO\n"

                u, v = sorted([leaves[0] + 1, leaves[1] + 1])
                answer.append((u, v))

        else:
            return "NO\n"

    answer.sort()

    out.append("YES")
    out.append(str(len(answer)))

    for u, v in answer:
        out.append(f"{u} {v}")

    return "\n".join(out) + "\n"

# provided sample
assert run(
"""3 2
1 2
2 3
"""
) == (
"""YES
1
1 3
"""
), "sample 1"

# isolated vertex
assert run(
"""1 0
"""
) == (
"""YES
1
1 1
"""
), "single vertex loop"

# already valid cycle
assert run(
"""3 3
1 2
2 3
3 1
"""
) == (
"""YES
0
"""
), "already interesting"

# branching tree impossible
assert run(
"""4 3
1 2
2 3
2 4
"""
) == (
"""NO
"""
), "degree > 2 impossible"

# parallel edges form cycle
assert run(
"""2 2
1 2
1 2
"""
) == (
"""YES
0
"""
), "2-cycle with parallel edges"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0` | add loop | isolated vertex handling |
| triangle graph | `YES 0` | already valid cycle |
| branching tree | `NO` | degree greater than two |
| parallel edges | `YES 0` | multigraph cycle handling |

## Edge Cases

Consider the isolated vertex case:

```
1 0
```

The component has one vertex and zero edges. It is technically a tree, but connecting endpoints is impossible because there is only one vertex.

The algorithm detects `size == 1` and adds loop `(1,1)`.

The final graph has one cycle containing the only vertex, so the answer is valid.

Now consider parallel edges:

```
2 2
1 2
1 2
```

Degrees become `[2,2]`. The component has `2` vertices and `2` edges, so it is already a cycle component.

A simple-graph implementation might incorrectly reject this, but the algorithm correctly accepts it.

Finally, consider a component with overlapping cycles:

```
4 5
1 2
2 3
3 1
2 4
4 3
```

Vertex degrees are `[2,3,3,2]`.

The algorithm immediately rejects the graph because vertices `2` and `3` already have degree greater than two.

No added edge could repair this structure, since removing cycles is impossible.
