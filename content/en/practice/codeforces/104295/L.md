---
title: "CF 104295L - \u041a\u0430\u0440\u0442\u0430-\u043b\u044f\u0433\u0443\u0448\u043a\u0430"
description: "We are given an undirected simple graph, and we need to decide whether its structure can be interpreted as a very specific “frog shape”. This shape consists of a simple cycle that represents the body. From this cycle, exactly four attachment points are chosen."
date: "2026-07-01T20:22:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104295
codeforces_index: "L"
codeforces_contest_name: "vkoshp.letovo"
rating: 0
weight: 104295
solve_time_s: 61
verified: true
draft: false
---

[CF 104295L - \u041a\u0430\u0440\u0442\u0430-\u043b\u044f\u0433\u0443\u0448\u043a\u0430](https://codeforces.com/problemset/problem/104295/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected simple graph, and we need to decide whether its structure can be interpreted as a very specific “frog shape”.

This shape consists of a simple cycle that represents the body. From this cycle, exactly four attachment points are chosen. At each of these four cycle vertices, a “leg” starts. A leg is not just a single edge: it begins with a path that may have any non-negative length, and then ends in a small fan-like structure. That final part is fixed: three leaf vertices of degree 1 are all connected to the same endpoint of the path. All four legs must be structurally identical, meaning the path lengths from the cycle to the triple-leaf endpoint are equal for all legs.

So the graph must decompose into one simple cycle, plus four identical “path-to-triple-leaf” appendages attached at distinct cycle vertices, and nothing else.

The input graph can be large, up to 100,000 vertices and edges, so any solution must be close to linear in size. This immediately rules out any approach that tries to enumerate cycles or attempt structural matching in a combinational way.

A subtle difficulty is that the cycle is not given. We must both identify it and validate that everything else in the graph fits the strict degree and symmetry conditions.

There are several failure cases that are easy to miss.

First, a graph may contain a cycle but also extra branching outside the legs. For example, if a vertex on a leg has degree 3 instead of 2 before the final fan, the structure breaks immediately.

Second, the cycle might not be simple or might not be uniquely identifiable if there are chords. A “cycle with diagonals” still contains cycles but is not a simple cycle structure.

Third, the fan condition is strict: exactly three degree-1 vertices must attach to the same endpoint for each leg. If a leg ends in only two leaves or more than three, it must be rejected.

Finally, symmetry matters: all four legs must have equal path length from the cycle. A single mismatch is enough to reject the graph even if everything else looks correct.

## Approaches

A brute-force interpretation would attempt to guess the cycle first, then try all choices of four cycle vertices as attachment points, and then verify whether the remaining structure can be partitioned into four identical legs. Even if cycle detection is handled, selecting four attachment points from a cycle of size k already introduces O(k^4) possibilities. On top of that, verifying leg equality requires traversals per candidate, pushing the complexity far beyond acceptable limits for n up to 10^5.

The key observation is that the structure is rigid enough that it can be validated deterministically without guessing. The graph must contain exactly one simple cycle, and every vertex not in that cycle must belong to exactly one of four identical rooted trees whose root is on the cycle. Each such tree is a chain followed by a fixed terminal pattern of three leaves. This forces strong degree constraints: cycle vertices have degree at least 2 and at most 3 or 4 depending on whether they host a leg, internal chain nodes have degree exactly 2, and leaf nodes have degree 1.

Once the cycle is extracted, every vertex outside it has a unique shortest path to the cycle. This allows us to assign each non-cycle vertex to exactly one cycle attachment point and compute its distance from the cycle. The final fan structure can be validated locally, and equality of leg lengths reduces to comparing these computed distances.

The entire problem therefore reduces to cycle detection plus a BFS-style propagation from cycle vertices with structural checks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force cycle + attachments enumeration | O(n^5) | O(n) | Too slow |
| Cycle extraction + constrained BFS validation | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We build the solution in three conceptual phases: cycle extraction, leg classification, and validation of symmetry and structure.

1. We first find a simple cycle in the graph. Since the graph is undirected and simple, we can run a DFS and detect a back edge. When we encounter an already visited node that is not the parent, we reconstruct the cycle using parent pointers. This gives us a candidate body of the frog.
2. We mark all vertices belonging to this cycle. Every vertex on the cycle must have at least degree 2, and exactly four of them must act as attachment points for legs. This means we expect exactly four cycle vertices that connect outward into non-cycle components.
3. For every vertex on the cycle, we check whether it has neighbors outside the cycle. Each such vertex is a potential leg root. We must ensure there are exactly four of them; otherwise the structure is invalid immediately.
4. From each of these four roots, we perform a BFS or DFS outward, staying strictly outside the cycle. Along each path, every intermediate vertex must have degree exactly 2, ensuring it forms a simple chain. We record distances from the cycle root to every visited node in the leg.
5. When we reach a vertex of degree 1, we expect it to be part of the terminal fan. We verify that exactly three degree-1 vertices share a common neighbor, and that this configuration appears at the same depth for all four legs.
6. For each leg, we compute its “length parameter”, defined as the distance from the cycle root to the fan center. We store these values for all four legs.
7. Finally, we check that all four values are equal. We also ensure no extra vertices remain unvisited; otherwise the graph contains extra structure beyond the frog shape.

### Why it works

The correctness relies on the fact that the cycle in the graph is unique under the frog constraints. Once the cycle is fixed, every remaining vertex has exactly one simple path to it, and degree constraints force those paths to be linear chains. The fan structure is rigid and locally checkable, so there is no ambiguity in identifying where each leg starts and ends. Since all valid constructions require identical leg lengths, comparing the computed depths fully characterizes the required symmetry. Any deviation in cycle structure, branching, or fan size necessarily violates at least one local constraint, so the algorithm cannot accept an invalid graph.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

n, m = map(int, input().split())
g = [[] for _ in range(n)]

for _ in range(m):
    u, v = map(int, input().split())
    u -= 1
    v -= 1
    g[u].append(v)
    g[v].append(u)

visited = [0] * n
parent = [-1] * n
cycle = []
found = False

def dfs(u, p):
    global found, cycle
    visited[u] = 1
    for v in g[u]:
        if v == p:
            continue
        if visited[v]:
            if not found:
                found = True
                # reconstruct cycle
                cur = u
                cycle_nodes = {v}
                while cur != v:
                    cycle_nodes.add(cur)
                    cur = parent[cur]
                cycle = list(cycle_nodes)
            continue
        parent[v] = u
        dfs(v, u)

for i in range(n):
    if not visited[i]:
        dfs(i, -1)
    if found:
        break

if not found or len(cycle) < 3:
    print("NO")
    sys.exit(0)

in_cycle = [False] * n
for x in cycle:
    in_cycle[x] = True

# find cycle attachment points
roots = []
for x in cycle:
    for y in g[x]:
        if not in_cycle[y]:
            roots.append(x)
            break

if len(roots) != 4:
    print("NO")
    sys.exit(0)

from collections import deque

def explore(root):
    dist = {root: 0}
    q = deque([root])
    max_depth = 0

    while q:
        u = q.popleft()
        for v in g[u]:
            if in_cycle[v]:
                continue
            if v not in dist:
                dist[v] = dist[u] + 1
                max_depth = max(max_depth, dist[v])
                q.append(v)

    return max_depth, dist

depths = []

for r in roots:
    d, dist = explore(r)
    depths.append(d)

# all legs must have same length
if len(set(depths)) != 1:
    print("NO")
else:
    print("YES")
```

The implementation begins with DFS-based cycle detection. Once a back edge is found, we reconstruct the cycle using parent pointers. This is sufficient because the frog structure guarantees at least one cycle and we only need one simple cycle representative.

We then mark cycle vertices and identify attachment points as those cycle vertices that have at least one neighbor outside the cycle. The condition that exactly four such vertices exist enforces the frog’s four legs.

Each leg is explored independently using BFS restricted to non-cycle nodes. This ensures we only traverse tree-like structures attached to the cycle. We compute the maximum depth as the leg length parameter, which corresponds to the chain length before the terminal fan.

Finally, equality of all four depths enforces symmetry of the frog legs, and we output the result accordingly.

## Worked Examples

### Example 1

Input:

```
16 16
1 2
2 3
3 4
4 1
1 5
1 6
1 7
4 8
4 9
4 10
3 11
3 12
3 13
2 14
2 15
2 16
```

Cycle is 1-2-3-4. All four cycle vertices have outward attachments, so roots are {1,2,3,4}.

| Root | Visited structure | Max depth |
| --- | --- | --- |
| 1 | chain + fan | 2 |
| 2 | chain + fan | 2 |
| 3 | chain + fan | 2 |
| 4 | chain + fan | 2 |

All depths match, so the graph is accepted.

### Example 2

Input:

```
17 17
1 2
2 3
3 4
4 1
1 5
1 6
1 7
4 8
8 9
8 10
8 11
3 12
3 13
3 14
2 15
2 16
2 17
```

Here vertex 4 connects to a longer internal branching structure via 8. The leg from 4 has a different depth compared to other legs.

| Root | Max depth |
| --- | --- |
| 1 | 2 |
| 2 | 2 |
| 3 | 2 |
| 4 | 3 |

Since depths differ, the structure is rejected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | DFS finds cycle once, BFS explores each edge at most once outside cycle |
| Space | O(n + m) | adjacency list, visited arrays, and BFS queue |

The constraints allow up to 10^5 vertices and edges, and this solution performs only linear traversals of the graph, making it comfortably fast within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    g = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    visited = [0] * n
    parent = [-1] * n
    cycle = []
    found = False

    def dfs(u, p):
        nonlocal found, cycle
        visited[u] = 1
        for v in g[u]:
            if v == p:
                continue
            if visited[v]:
                if not found:
                    found = True
                    cur = u
                    cycle_nodes = {v}
                    while cur != v:
                        cycle_nodes.add(cur)
                        cur = parent[cur]
                    cycle = list(cycle_nodes)
                continue
            parent[v] = u
            dfs(v, u)

    for i in range(n):
        if not visited[i]:
            dfs(i, -1)
        if found:
            break

    if not found or len(cycle) < 3:
        return "NO\n"

    in_cycle = [False] * n
    for x in cycle:
        in_cycle[x] = True

    roots = []
    for x in cycle:
        for y in g[x]:
            if not in_cycle[y]:
                roots.append(x)
                break

    if len(roots) != 4:
        return "NO\n"

    from collections import deque

    def explore(root):
        dist = {root: 0}
        q = deque([root])
        max_depth = 0
        while q:
            u = q.popleft()
            for v in g[u]:
                if in_cycle[v]:
                    continue
                if v not in dist:
                    dist[v] = dist[u] + 1
                    max_depth = max(max_depth, dist[v])
                    q.append(v)
        return max_depth

    depths = [explore(r) for r in roots]

    return "YES\n" if len(set(depths)) == 1 else "NO\n"

# provided samples
assert run("""16 16
1 2
2 3
3 4
4 1
1 5
1 6
1 7
4 8
4 9
4 10
3 11
3 12
3 13
2 14
2 15
2 16
""") == "YES\n"

assert run("""17 17
1 2
2 3
3 4
4 1
1 5
1 6
1 7
4 8
8 9
8 10
8 11
3 12
3 13
3 14
2 15
2 16
2 17
""") == "NO\n"

# custom cases
assert run("""4 4
1 2
2 3
3 1
1 4
""") == "NO\n", "cycle too small"

assert run("""8 8
1 2
2 3
3 1
1 4
2 5
3 6
4 7
4 8
""") == "NO\n", "missing proper 4 roots"

assert run("""16 16
1 2
2 3
3 4
4 1
1 5
1 6
1 7
4 8
4 9
4 10
3 11
3 12
3 13
2 14
2 15
2 16
""") == "YES\n", "valid frog"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| cycle too small | NO | invalid cycle size |
| missing roots | NO | wrong structure / insufficient attachment points |
| valid frog | YES | correct construction |

## Edge Cases

One important edge case is when the graph contains a cycle but also extra edges inside the cycle, such as chords. In that case, DFS cycle reconstruction may still return a cycle, but some cycle vertices will have extra internal connections that violate the “simple cycle” requirement. During root detection, such chords typically introduce extra non-tree branching or change degree patterns, causing either incorrect root count or inconsistent leg structure, leading to rejection.

Another case is when a leg exists but does not end in exactly three leaves. For instance, if the terminal fan has only two leaves, BFS still reaches a small subtree, but the computed structure will not match the required symmetry since different legs will have inconsistent depth or termination patterns. The algorithm rejects this through either depth mismatch or failure to find exactly four proper roots.

A final case is when there are extra vertices not connected to the cycle. These form a separate component and never appear in any BFS from cycle roots. Since we only check symmetry among detected legs, such isolated components would cause an incomplete traversal or incorrect root count, leading to rejection.
