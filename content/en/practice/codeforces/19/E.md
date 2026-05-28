---
title: "CF 19E - Fairy"
description: "We are given an undirected graph. Each edge represents a segment drawn between two points. We may erase exactly one edge, and after removing it we want the remaining graph to become bipartite."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "divide-and-conquer", "dsu"]
categories: ["algorithms"]
codeforces_contest: 19
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 19"
rating: 2900
weight: 19
solve_time_s: 110
verified: true
draft: false
---
[CF 19E - Fairy](https://codeforces.com/problemset/problem/19/E)

**Rating:** 2900  
**Tags:** dfs and similar, divide and conquer, dsu  
**Solve time:** 1m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected graph. Each edge represents a segment drawn between two points. We may erase exactly one edge, and after removing it we want the remaining graph to become bipartite.

A graph is bipartite if we can color every vertex using two colors such that every edge connects vertices of different colors. Another way to say the same thing is that the graph must contain no odd cycle.

The task is to output every edge whose removal makes the whole graph bipartite.

The graph can contain up to $10^4$ vertices and $10^4$ edges. That size immediately rules out anything quadratic in both vertices and edges if the constant factor is large. A naive solution that removes every edge and checks bipartiteness from scratch would perform a full DFS or BFS $m$ times. Each check costs $O(n+m)$, so the total complexity becomes $O(m(n+m))$. With both values near $10^4$, that reaches roughly $2 \cdot 10^8$ operations, which is too risky in Python.

The tricky part is that the graph may be disconnected. A careless implementation that only DFSes from vertex 1 misses odd cycles in other components.

Another subtle case happens when the graph already is bipartite. Then removing any edge still leaves a bipartite graph, so every edge must be printed.

For example:

```
3 2
1 2
2 3
```

The graph is already bipartite. Correct output:

```
2
1 2
```

A wrong approach that only searches for “bad” edges participating in odd cycles could incorrectly print nothing.

There is also the opposite extreme, where multiple odd cycles exist independently. If removing one edge cannot destroy all odd cycles, then the answer is empty.

Example:

```
6 6
1 2
2 3
3 1
4 5
5 6
6 4
```

There are two disconnected triangles. Removing one edge destroys only one triangle, while the other odd cycle remains. Correct output:

```
0
```

A naive “edge belongs to some odd cycle” criterion fails here, because every edge lies on an odd cycle, but no single edge fixes the entire graph.

The hardest edge case is overlapping odd cycles. Sometimes several odd cycles share edges, and only the shared edges work.

Example:

```
5 6
1 2
2 3
3 1
3 4
4 5
5 3
```

Two triangles share vertex 3 but not edges. No single edge removal destroys both odd cycles, so the answer is still empty.

## Approaches

The brute-force idea is straightforward. For every edge, temporarily remove it and test whether the remaining graph is bipartite using BFS or DFS coloring.

The bipartite check itself is standard. We assign alternating colors during traversal. If we ever encounter an edge connecting vertices with the same color, the graph contains an odd cycle and is not bipartite.

This works because removing an edge is independent from the coloring process. Every candidate edge can be tested directly.

The problem is the total cost. We repeat an $O(n+m)$ graph traversal for every edge, producing $O(m(n+m))$ time overall. With $m = 10^4$, this becomes too large.

The key observation is that odd cycles are the only obstruction to bipartiteness. Removing one edge can only help if that edge belongs to every odd cycle in the graph.

That changes the problem completely. Instead of recomputing bipartiteness after each removal, we study the structure of odd cycles inside a single DFS tree.

Suppose we DFS the graph and color vertices by depth parity. Tree edges always connect opposite colors. A non-tree edge behaves differently:

If it connects vertices of different parity, it forms an even cycle.

If it connects vertices of the same parity, it forms an odd cycle.

These “bad” back edges completely characterize odd cycles in the graph.

Now consider how removing one edge can eliminate all odd cycles. Every odd cycle corresponds to one bad back edge together with the tree path between its endpoints. An edge is valid exactly when it belongs to all such odd cycles.

This becomes a counting problem on the DFS tree.

We assign each bad back edge a contribution along the path between its endpoints. After accumulating contributions bottom-up, each tree edge knows how many odd cycles pass through it.

If the graph contains exactly $k$ odd cycles induced by bad back edges, then:

If $k = 0$, every edge works.

If $k > 0$, an edge works iff it belongs to all $k$ odd cycles.

Non-tree bad edges themselves also work if they are the only edge responsible for one odd cycle contribution.

This reduces the entire problem to one DFS plus one accumulation pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(m(n+m))$ | $O(n+m)$ | Too slow |
| Optimal | $O(n+m)$ | $O(n+m)$ | Accepted |

## Algorithm Walkthrough

1. Build the undirected graph and store the index of every edge.
2. Run DFS over every connected component.

During DFS, store:

- depth of each vertex
- parent edge in the DFS tree
- parity color using depth modulo 2
3. Classify edges during DFS.

If an already visited neighbor is not the parent, we found a back edge.

If the two endpoints have the same parity, this back edge creates an odd cycle.
4. Count all odd back edges globally.

Let this value be `odd_cnt`.

If `odd_cnt == 0`, the graph already is bipartite, so every edge is valid.
5. For every odd back edge $(u,v)$, add path contributions.

Assume `depth[u] > depth[v]`.

Increment `mark[u] += 1`

Decrement `mark[v] -= 1`

Later, when we aggregate values upward through the DFS tree, every tree edge on the path from `u` to `v` receives one contribution.
6. DFS again to accumulate subtree sums.

For each vertex, sum contributions from children into the parent.

Let `sub[x]` denote the final accumulated value.

If a tree edge from parent to child has `sub[child] == odd_cnt`, then every odd cycle passes through this edge, so removing it fixes the graph.
7. Handle non-tree odd edges separately.

Every odd back edge individually belongs to exactly one odd cycle descriptor. Such an edge works iff `odd_cnt == 1`.
8. Collect all valid edge indices and print them sorted.

### Why it works

Every odd cycle in an undirected DFS can be represented by one odd back edge plus the tree path connecting its endpoints.

The contribution propagation marks exactly the tree edges belonging to each odd cycle. After accumulation, `sub[x]` equals the number of odd cycles passing through the tree edge connecting `x` to its parent.

If an edge belongs to all odd cycles, removing it destroys every odd cycle simultaneously, making the graph bipartite.

If an edge misses even one odd cycle, that cycle survives after removal, so the graph remains non-bipartite.

The algorithm checks precisely this condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1 << 25)

n, m = map(int, input().split())

g = [[] for _ in range(n + 1)]
edges = [None]

for i in range(1, m + 1):
    u, v = map(int, input().split())
    edges.append((u, v))
    g[u].append((v, i))
    g[v].append((u, i))

depth = [0] * (n + 1)
visited = [False] * (n + 1)
parent = [0] * (n + 1)
parent_edge = [0] * (n + 1)

mark = [0] * (n + 1)

odd_edges = []
odd_cnt = 0

def dfs(u, pe):
    global odd_cnt

    visited[u] = True

    for v, idx in g[u]:
        if idx == pe:
            continue

        if not visited[v]:
            depth[v] = depth[u] + 1
            parent[v] = u
            parent_edge[v] = idx
            dfs(v, idx)
        elif depth[v] < depth[u]:
            if (depth[u] - depth[v]) % 2 == 0:
                odd_cnt += 1
                odd_edges.append(idx)

                mark[u] += 1
                mark[v] -= 1

for i in range(1, n + 1):
    if not visited[i]:
        dfs(i, -1)

if odd_cnt == 0:
    print(m)
    print(*range(1, m + 1))
    sys.exit()

ans = []

def collect(u, pe):
    subtotal = mark[u]

    for v, idx in g[u]:
        if idx == pe:
            continue

        if parent[v] == u:
            child_sum = collect(v, idx)

            if child_sum == odd_cnt:
                ans.append(idx)

            subtotal += child_sum

    return subtotal

for i in range(1, n + 1):
    if parent[i] == 0:
        collect(i, -1)

if odd_cnt == 1:
    ans.extend(odd_edges)

ans.sort()

print(len(ans))
print(*ans)
```

The first DFS builds the DFS tree and detects odd back edges. The parity test comes from DFS depths. If the depth difference between two endpoints is even, then the cycle length becomes odd.

The `mark` array implements path accumulation. For an odd back edge $(u,v)$, incrementing at the deeper endpoint and decrementing at the ancestor causes every tree edge on that path to receive one contribution during subtree aggregation.

The second DFS computes subtree sums bottom-up. If a tree edge carries exactly `odd_cnt` contributions, then all odd cycles pass through it.

The condition `depth[v] < depth[u]` avoids processing the same back edge twice. Without it, undirected edges would be counted from both directions.

The separate handling of non-tree odd edges is subtle. Such an edge itself closes one odd cycle. Removing it fixes the graph only when that is the only odd cycle descriptor in the entire graph.

The recursion limit must be increased because the DFS tree can become a long chain of length $10^4$.

## Worked Examples

### Example 1

Input:

```
4 4
1 2
1 3
2 4
3 4
```

DFS traversal:

| Step | Edge | Depths | Odd back edge? | odd_cnt |
| --- | --- | --- | --- | --- |
| 1 | 1-2 | 0,1 | No | 0 |
| 2 | 2-4 | 1,2 | No | 0 |
| 3 | 4-3 | 2,3 | No | 0 |
| 4 | 3-1 | 3,0 | No | 0 |

No odd cycle exists. The graph is already bipartite.

Output:

```
4
1 2 3 4
```

This example demonstrates the special case `odd_cnt == 0`. Every edge is valid because removing edges cannot destroy bipartiteness.

### Example 2

Input:

```
3 3
1 2
2 3
3 1
```

DFS traversal:

| Step | Edge | Depths | Odd back edge? | odd_cnt |
| --- | --- | --- | --- | --- |
| 1 | 1-2 | 0,1 | No | 0 |
| 2 | 2-3 | 1,2 | No | 0 |
| 3 | 3-1 | 2,0 | Yes | 1 |

Contribution propagation:

| Vertex | mark before collect | Final subtree sum |
| --- | --- | --- |
| 3 | +1 | 1 |
| 2 | 0 | 1 |
| 1 | -1 | 0 |

Both tree edges receive value 1, equal to `odd_cnt`.

The back edge itself also works because `odd_cnt == 1`.

Output:

```
3
1 2 3
```

This trace shows that every edge of a single odd cycle is removable.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n+m)$ | Each edge and vertex is processed a constant number of times |
| Space | $O(n+m)$ | Graph storage plus DFS arrays |

With at most $10^4$ vertices and edges, linear complexity easily fits within the limits. The algorithm performs only two DFS traversals and a few constant-time operations per edge.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    sys.setrecursionlimit(1 << 25)

    n, m = map(int, input().split())

    g = [[] for _ in range(n + 1)]
    edges = [None]

    for i in range(1, m + 1):
        u, v = map(int, input().split())
        edges.append((u, v))
        g[u].append((v, i))
        g[v].append((u, i))

    depth = [0] * (n + 1)
    visited = [False] * (n + 1)
    parent = [0] * (n + 1)

    mark = [0] * (n + 1)

    odd_edges = []
    odd_cnt = 0

    def dfs(u, pe):
        nonlocal odd_cnt

        visited[u] = True

        for v, idx in g[u]:
            if idx == pe:
                continue

            if not visited[v]:
                depth[v] = depth[u] + 1
                parent[v] = u
                dfs(v, idx)
            elif depth[v] < depth[u]:
                if (depth[u] - depth[v]) % 2 == 0:
                    odd_cnt += 1
                    odd_edges.append(idx)

                    mark[u] += 1
                    mark[v] -= 1

    for i in range(1, n + 1):
        if not visited[i]:
            dfs(i, -1)

    if odd_cnt == 0:
        print(m)
        print(*range(1, m + 1))
        return

    ans = []

    def collect(u, pe):
        subtotal = mark[u]

        for v, idx in g[u]:
            if idx == pe:
                continue

            if parent[v] == u:
                child = collect(v, idx)

                if child == odd_cnt:
                    ans.append(idx)

                subtotal += child

        return subtotal

    for i in range(1, n + 1):
        if parent[i] == 0:
            collect(i, -1)

    if odd_cnt == 1:
        ans.extend(odd_edges)

    ans.sort()

    print(len(ans))
    if ans:
        print(*ans)
    else:
        print()

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run(
"""4 4
1 2
1 3
2 4
3 4
"""
) == "4\n1 2 3 4\n"

# single triangle
assert run(
"""3 3
1 2
2 3
3 1
"""
) == "3\n1 2 3\n"

# two disconnected odd cycles
assert run(
"""6 6
1 2
2 3
3 1
4 5
5 6
6 4
"""
) == "0\n\n"

# no edges
assert run(
"""1 0
"""
) == "0\n\n"

# already bipartite chain
assert run(
"""5 4
1 2
2 3
3 4
4 5
"""
) == "4\n1 2 3 4\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single triangle | All edges valid | One odd cycle |
| Two disconnected triangles | Empty answer | One edge cannot destroy multiple odd cycles |
| No edges | Empty answer | Minimum graph |
| Simple chain | All edges valid | Already bipartite graph |

## Edge Cases

Consider the graph with no odd cycles:

```
4 3
1 2
2 3
3 4
```

DFS never finds an odd back edge, so `odd_cnt = 0`. The algorithm immediately outputs all edges. This is correct because deleting any edge from a bipartite graph preserves bipartiteness.

Now consider two disconnected odd cycles:

```
6 6
1 2
2 3
3 1
4 5
5 6
6 4
```

The DFS detects two odd back edges, so `odd_cnt = 2`.

Every tree edge receives contribution 1 from only one triangle, never 2. No edge belongs to both odd cycles simultaneously, so the answer remains empty.

Finally, consider overlapping structure:

```
5 6
1 2
2 3
3 1
3 4
4 5
5 3
```

DFS finds two odd cycles. Edges inside the first triangle only receive one contribution. Edges inside the second triangle also receive one contribution. No edge reaches `odd_cnt = 2`.

The algorithm correctly prints:

```
0
```

because removing one edge still leaves another odd cycle alive.
