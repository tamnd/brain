---
title: "CF 102163B - Let me sleep"
description: "The dorm can be modeled as an undirected graph. Each room is a vertex and each portal is an edge. A portal is useful to the supervisor exactly when removing that edge disconnects its connected component, which is the standard definition of a bridge."
date: "2026-08-19T14:38:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102163
codeforces_index: "B"
codeforces_contest_name: "NCD 2019"
rating: 0
weight: 102163
solve_time_s: 461
verified: true
draft: false
---

[CF 102163B - Let me sleep](https://codeforces.com/problemset/problem/102163/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

The dorm can be modeled as an undirected graph. Each room is a vertex and each portal is an edge. A portal is useful to the supervisor exactly when removing that edge disconnects its connected component, which is the standard definition of a bridge.

Hasan may add exactly one new portal between two rooms. Adding an edge can destroy some existing bridges because the new edge may create a cycle containing them. The goal is to choose the new portal so that as few bridges as possible remain.

The input contains several independent graphs. For each graph, the required output is the minimum possible number of bridges after adding one edge.

The bounds allow up to (10^5) vertices and (10^5) edges in one test case. The official problem page gives a 3 second time limit and 256 MB memory limit. With this size, an algorithm should process the graph in roughly linear or near-linear time. Enumerating all vertex pairs already costs (O(N^2)), which is around (5\cdot10^9) pairs at the maximum size, so any solution that examines every possible new portal individually is far too slow.

There are several graph details that can make a careless implementation fail. First, the graph may be disconnected. For example,

```
1
4 2
1 2
3 4
```

has two bridges, but adding an edge between vertices from different connected components does not create a cycle, so the answer is `2`. A solution that treats the entire bridge structure as one tree can incorrectly connect the two components and claim that both bridges disappear.

Second, a graph can contain cycles. For

```
1
3 3
1 2
2 3
3 1
```

there are no bridges already, so the answer is `0`. A solution that simply counts edges or assumes every edge in a connected graph is a bridge gets this wrong.

Third, repeated edges need to be handled correctly if they occur. For

```
1
2 2
1 2
1 2
```

neither edge is a bridge, because removing either one still leaves the other connection. The answer is `0`. Tarjan's algorithm must distinguish the two physical edges rather than treating the second occurrence as the same edge.

A self-loop is another harmless case if the input contains one. For

```
1
1 1
1 1
```

the edge cannot disconnect anything, so the answer is `0`. The implementation below naturally handles it.

## Approaches

A direct solution would try every possible pair of rooms as the endpoints of the new portal. For each pair, add the edge conceptually, run a bridge-finding algorithm, count the remaining bridges, and keep the minimum. This is correct because every legal choice of the new portal is explicitly evaluated.

The problem is the number of choices. There are (O(N^2)) pairs, and finding all bridges costs (O(N+M)), so the total complexity is (O(N^2(N+M))). With (N=M=10^5), that is on the order of (10^{15}) graph operations, which is nowhere near feasible.

The useful observation is that adding one edge can only make edges on one particular path stop being bridges. Suppose two rooms are already connected. There is a unique path between their edge-biconnected components after all existing bridges are contracted. Adding the new edge creates a cycle consisting of the new edge and that path. Every bridge on the path is now part of a cycle and ceases to be a bridge. Bridges outside the path remain bridges.

This suggests compressing every maximal region that contains no bridges into one component. After this compression, every remaining edge is a bridge, and the resulting structure is a forest. In each tree of this forest, adding an edge between two components removes exactly the bridge edges on their unique path.

So the problem becomes much simpler. Let the total number of bridges be (B). If the longest path in the bridge forest has length (D), we can add a portal between rooms belonging to the two endpoints of that path and remove exactly (D) bridges. The answer is consequently

[
B-D.
]

If the original graph is disconnected, the compressed structure is a forest rather than one tree. An edge between two different trees cannot remove any old bridge, so we take the maximum diameter over all trees.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N^2(N+M))) | (O(N+M)) | Too slow |
| Optimal | (O(N+M)) | (O(N+M)) | Accepted |

## Algorithm Walkthrough

1. Store the undirected graph with an explicit edge ID for every portal. Using edge IDs is necessary because two different portals may connect the same pair of rooms.
2. Run Tarjan's bridge algorithm. For every vertex, maintain its discovery time `tin` and its lowest reachable discovery time `low`. For a DFS tree edge from (u) to (v), the edge is a bridge exactly when `low[v] > tin[u]`.

The implementation uses an explicit stack instead of recursive DFS. With (10^5) vertices, a recursive Python DFS can hit the recursion limit or incur unnecessary overhead, while the iterative version keeps the same Tarjan logic.
3. Ignore every bridge and find the connected components of the remaining graph. Every such component is an edge-biconnected component, meaning that no single edge inside it can disconnect the component.
4. Give each edge-biconnected component a compressed vertex ID. Every original bridge connects two different compressed components.
5. Build a new graph containing only those bridges. Since all internal non-bridge edges were contracted, this graph is a forest. Each edge in it represents exactly one original bridge.
6. Count all bridge edges. Call this value (B).
7. For every tree in the bridge forest, compute its diameter. Because all compressed edges have unit length, the diameter is simply the maximum number of bridge edges on a path.
8. The standard two-traversal method finds each tree's diameter. Start from an arbitrary vertex and find a farthest vertex (a). Starting from (a), find the farthest vertex (b). The distance from (a) to (b) is the tree's diameter.
9. Keep the largest diameter (D) among all trees. Connecting rooms from the two endpoint components of this path creates a cycle containing exactly those (D) bridges, so those bridges disappear.
10. Return `total_bridges - maximum_diameter`.

**Why it works.** After all non-bridge edges are contracted, every remaining edge is a bridge and the compressed graph is a forest. Adding one edge inside a connected component creates exactly one cycle, consisting of the new edge and the unique path between its endpoints in the compressed tree. Exactly the bridge edges on that path stop being bridges, while every other bridge remains a bridge. Thus the number of removed bridges is exactly the path length. The best possible path is the diameter, so subtracting the maximum forest diameter from the original bridge count gives the minimum possible number of remaining bridges.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    answers = []

    for _ in range(t):
        n, m = map(int, input().split())

        adj = [[] for _ in range(n)]
        edges = []

        for eid in range(m):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            edges.append((u, v))
            adj[u].append((v, eid))
            adj[v].append((u, eid))

        tin = [-1] * n
        low = [0] * n
        parent = [-1] * n
        parent_edge = [-1] * n
        it = [0] * n
        is_bridge = [False] * m

        timer = 0

        for root in range(n):
            if tin[root] != -1:
                continue

            tin[root] = low[root] = timer
            timer += 1

            stack = [root]

            while stack:
                v = stack[-1]

                if it[v] < len(adj[v]):
                    to, eid = adj[v][it[v]]
                    it[v] += 1

                    if eid == parent_edge[v]:
                        continue

                    if tin[to] == -1:
                        parent[to] = v
                        parent_edge[to] = eid
                        tin[to] = low[to] = timer
                        timer += 1
                        stack.append(to)
                    else:
                        if tin[to] < low[v]:
                            low[v] = tin[to]
                else:
                    stack.pop()
                    p = parent[v]

                    if p != -1:
                        pe = parent_edge[v]

                        if low[v] > tin[p]:
                            is_bridge[pe] = True

                        if low[v] < low[p]:
                            low[p] = low[v]

        comp = [-1] * n
        component_count = 0

        for start in range(n):
            if comp[start] != -1:
                continue

            comp[start] = component_count
            stack = [start]

            while stack:
                v = stack.pop()

                for to, eid in adj[v]:
                    if is_bridge[eid]:
                        continue
                    if comp[to] != -1:
                        continue

                    comp[to] = component_count
                    stack.append(to)

            component_count += 1

        forest = [[] for _ in range(component_count)]
        total_bridges = 0

        for eid, (u, v) in enumerate(edges):
            if not is_bridge[eid]:
                continue

            a = comp[u]
            b = comp[v]

            forest[a].append(b)
            forest[b].append(a)
            total_bridges += 1

        seen = [False] * component_count

        def farthest(start, mark):
            stack = [(start, -1, 0)]
            far_vertex = start
            far_distance = 0

            while stack:
                v, parent_vertex, distance = stack.pop()

                if mark:
                    seen[v] = True

                if distance > far_distance:
                    far_distance = distance
                    far_vertex = v

                for to in forest[v]:
                    if to == parent_vertex:
                        continue
                    stack.append((to, v, distance + 1))

            return far_vertex, far_distance

        maximum_diameter = 0

        for start in range(component_count):
            if seen[start]:
                continue

            endpoint, _ = farthest(start, True)
            _, diameter = farthest(endpoint, False)

            if diameter > maximum_diameter:
                maximum_diameter = diameter

        answers.append(str(total_bridges - maximum_diameter))

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()
```

The graph is first stored as adjacency lists. Every adjacency entry contains both the neighboring vertex and the physical edge ID, which lets Tarjan distinguish parallel edges correctly.

The first traversal computes `tin` and `low`. When a DFS child `v` finishes, the condition `low[v] > tin[parent[v]]` identifies the parent edge as a bridge. The parent edge itself is skipped using its ID, rather than by skipping the parent vertex, which is the subtle detail needed for multigraphs.

After the bridges are known, a second traversal assigns component IDs while refusing to cross bridges. These components are exactly the vertices of the compressed forest. We then inspect every original edge once and add only bridge edges to `forest`.

The diameter calculation uses a stack containing `(vertex, parent, distance)`. Because `forest` is a forest, remembering the parent is enough to prevent walking backward, so no additional per-traversal visited array is necessary. The first traversal for a tree marks its vertices in `seen`, which prevents processing the same tree again.

There is no integer overflow concern in Python. The largest possible answer is at most (10^5), while Python integers handle arbitrary sizes anyway. The distance starts at zero, so a compressed component with no bridge edges has diameter zero and contributes nothing to the number of removed bridges.

## Worked Examples

### Sample case 1

The graph is

```
1 -- 2 -- 3
```

Both edges are bridges. After contracting non-bridge regions, nothing is contracted, so the bridge forest is still a path of three components.

| Phase | Components | Bridge edges | Total bridges | Maximum diameter | Answer |
| --- | --- | --- | --- | --- | --- |
| Original graph | 3 | 2 | 2 | 2 | 0 |
| After choosing endpoints 1 and 3 | 3 | 2 | 2 | 2 | 0 |

Adding a portal between rooms 1 and 3 creates the cycle `1-2-3-1`. Both original bridges now lie on a cycle, so neither remains a bridge. The answer is `2 - 2 = 0`.

### Sample case 2

The graph contains a triangle on rooms 2, 3, and 8. The rooms 1, 4, 5, and 7 are also joined through multiple paths, so all of those edges belong to one edge-biconnected component. The remaining bridge structure is a three-leaf tree.

| Phase | Compressed components | Bridge edges | Total bridges | Maximum diameter | Answer |
| --- | --- | --- | --- | --- | --- |
| After bridge detection | 4 | `(triangle)-(core)`, `(core)-6`, `(core)-9` | 3 | 2 | 1 |
| Choose leaves 2 and 6 | 4 | 3 original bridges | 3 | 2 removed | 1 |

The three bridges are the portal from room 1 to room 2, the portal from room 4 to room 6, and the portal from room 5 to room 9. The compressed forest is a star whose center is the large cyclic component and whose leaves are the triangle component, room 6, and room 9.

The longest path contains two bridges. Connecting two leaves creates a cycle containing those two bridges, leaving exactly one bridge. Hence the sample output is `1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N+M)) | Tarjan, component construction, forest construction, and diameter traversals each process every vertex and edge only a constant number of times |
| Space | (O(N+M)) | The original adjacency list, bridge data, component IDs, and compressed forest are all linear in the graph size |

With (N,M\le10^5), the algorithm performs only a small constant number of linear graph traversals. This is the right scale for the official 3 second and 256 MB limits.

## Test Cases

The following test harness assumes the submitted solution is saved as `solution.py` and exposes the `solve()` function shown above.

```python
import sys
import io
from solution import solve

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

sample = """\
2
3 2
1 2
2 3
9 11
3 2
3 8
2 8
1 2
1 5
1 4
5 9
7 5
4 5
6 4
4 7
"""

assert run(sample) == "0\n1", "provided sample"

assert run("""\
1
1 1
1 1
""") == "0", "single vertex and self-loop"

assert run("""\
1
4 3
1 2
2 3
3 4
""") == "0", "a path can be closed into one cycle"

assert run("""\
1
2 2
1 2
1 2
""") == "0", "parallel edges are not bridges"

assert run("""\
1
4 2
1 2
3 4
""") == "1", "two disconnected components"

n = 100000
m = 100000
maximum_case = "1\n" + f"{n} {m}\n" + ("1 1\n" * m)
assert run(maximum_case) == "0", "maximum size with repeated self-loops"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Official sample | `0\n1` | Main cases, cycles, bridges, and a disconnected graph |
| `1 1` with edge `1 1` | `0` | Minimum size and self-loop handling |
| Path `1-2-3-4` | `0` | Diameter can remove every bridge |
| Two parallel edges | `0` | Correct edge-ID handling for repeated edges |
| Two disconnected single-edge components | `1` | Maximum diameter must be taken over a forest |
| (N=M=10^5), all edges `1 1` | `0` | Maximum input size and repeated identical endpoints |

## Edge Cases

For a disconnected graph such as

```
1
4 2
1 2
3 4
```

Tarjan finds both edges as bridges. Since there are no non-bridge edges, every room becomes its own compressed component, and the bridge forest consists of two separate trees, each containing one edge. Each tree has diameter one, so the maximum diameter is one. The total bridge count is two, giving `2 - 1 = 1`. The algorithm never incorrectly connects the two disconnected trees because it only uses a path inside one forest component.

For a graph that already contains a cycle,

```
1
3 3
1 2
2 3
3 1
```

Tarjan finds no bridges. All three vertices are placed in the same compressed component, so the bridge forest has one isolated vertex and the maximum diameter is zero. The total bridge count is also zero, giving the correct answer `0`.

For parallel edges,

```
1
2 2
1 2
1 2
```

the two portals have different edge IDs. During DFS, when the second physical edge is encountered, it is treated as a back edge rather than being confused with the DFS parent edge. Consequently the low-link value drops enough that neither portal satisfies the bridge condition. The compressed graph contains one component, the bridge count is zero, and the answer is `0`.

For a self-loop,

```
1
1 1
1 1
```

the edge starts and ends at the same vertex. It cannot disconnect the graph, so Tarjan does not mark it as a bridge. The only room becomes one compressed component, the bridge forest has diameter zero, and the answer is `0`.

The most revealing case is a simple path,

```
1
4 3
1 2
2 3
3 4
```

All three edges are bridges, so the compressed forest is the path of length three. The first diameter traversal reaches one endpoint, and the second reaches the other endpoint at distance three. The algorithm computes `total_bridges = 3`, `maximum_diameter = 3`, and returns `0`. Adding a portal between rooms 1 and 4 creates a cycle containing every original edge, which is exactly the optimal operation.
