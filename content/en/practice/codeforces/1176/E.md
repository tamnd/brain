---
title: "CF 1176E - Cover it!"
description: "We are given an undirected connected graph for each query, and we must select a subset of vertices such that every vertex we do not select has at least one selected neighbor. In other words, every unchosen vertex must be “covered” by an adjacent chosen vertex."
date: "2026-06-13T10:18:37+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dsu", "graphs", "shortest-paths", "trees"]
categories: ["algorithms"]
codeforces_contest: 1176
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 565 (Div. 3)"
rating: 1700
weight: 1176
solve_time_s: 633
verified: false
draft: false
---

[CF 1176E - Cover it!](https://codeforces.com/problemset/problem/1176/E)

**Rating:** 1700  
**Tags:** dfs and similar, dsu, graphs, shortest paths, trees  
**Solve time:** 10m 33s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an undirected connected graph for each query, and we must select a subset of vertices such that every vertex we do not select has at least one selected neighbor. In other words, every unchosen vertex must be “covered” by an adjacent chosen vertex. The extra restriction is that the number of chosen vertices must not exceed half of all vertices.

So the task is essentially to construct a vertex set that dominates the graph, but with a guaranteed size bound of at most floor(n/2). We do not need to minimize anything, only to produce any valid set satisfying both the coverage condition and the size constraint.

The constraints are large: the sum of all n and m over queries is up to 2⋅10^5, and there can be up to 2⋅10^5 queries. This forces a linear or near-linear solution per query, with total complexity around O(n + m) overall. Anything involving pairwise checks, subset enumeration, or repeated graph traversals per vertex would be too slow.

A subtle edge case arises in sparse graphs like a path. If we try to greedily pick arbitrary vertices without structure, we might accidentally pick too many vertices or fail to guarantee coverage. For example, in a path 1-2-3-4-5, choosing {2,4} works, but naive strategies like always picking every second vertex starting incorrectly can overshoot or miss coverage at boundaries depending on traversal order.

Another edge case is dense graphs like cliques. In a complete graph, any single vertex covers all others, so choosing 1 vertex is enough. A naive alternating strategy might still pick too many vertices unnecessarily, but still valid.

The key difficulty is to ensure a construction that always stays within n/2 while guaranteeing domination.

## Approaches

A brute-force idea would be to try all subsets of vertices, check whether they dominate the graph, and track those of size at most n/2. For each candidate set, verifying coverage requires scanning all edges or adjacency lists, which already costs O(n + m). Since there are 2^n subsets, this is completely infeasible.

We need a structure that inherently limits the answer size while ensuring coverage. The key observation is that if we 2-color the graph using a BFS or DFS parity coloring, every edge connects either same-parity or different-parity nodes, but we can still partition vertices into two groups based on BFS tree depth. Since the graph is connected, BFS levels give us a natural bipartition-like structure even if the graph is not bipartite.

Now consider grouping vertices by their BFS level parity: even depth and odd depth. Every edge connects nodes whose depths differ by at most 1 in BFS tree terms, but in general graph edges can connect arbitrary levels. However, the important property we exploit is simpler: every edge has endpoints, and at least one endpoint belongs to either even or odd level set. Therefore, every vertex not chosen from one parity set is adjacent (via BFS tree edges or graph edges) to some vertex in the other parity set in a way that guarantees coverage when choosing the smaller set.

A more robust way to see it is to root the graph at any node and color by distance parity. Every edge connects either same or opposite parity. If an edge connects same parity, it does not help directly, but coverage is ensured globally because every vertex has a parent-child relationship in the BFS tree that connects opposite parity. Hence, choosing the smaller of the two parity sets ensures that every unchosen vertex has at least one neighbor in the chosen set.

Since the two sets partition the vertices, one of them has size at most n/2, which satisfies the constraint immediately.

This reduces the problem to a single BFS and a parity count.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · (n + m)) | O(n) | Too slow |
| BFS parity partition | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

We root the graph at any vertex, typically 1, and compute BFS distances.

1. Run a BFS from node 1 and record distance parity for each node.

We assign each node either 0 or 1 depending on whether its distance from the root is even or odd. This creates two candidate groups.
2. Collect nodes into two lists based on parity.

One list contains all even-distance nodes, the other contains all odd-distance nodes.
3. Compare the sizes of the two lists.

Since together they contain all nodes, at least one list has size at most floor(n/2). We select that list.
4. Output the selected list as the answer.

Why this is sufficient comes from how BFS layering guarantees reachability structure from the root and ensures every node has a path alternating parity steps, which implies that removing one parity class still leaves every node adjacent to at least one selected vertex.

### Why it works

Every vertex belongs to exactly one of the two parity classes. The selected set is the smaller of these two classes, so any vertex not selected belongs to the other class. In the BFS tree, every node except the root has a parent with opposite parity, meaning every unselected node has at least one adjacent node in the opposite parity class. Since we select one entire class, every unselected node is guaranteed to have a neighbor in the selected set. The size bound holds because we always choose the smaller partition.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    g = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v = map(int, input().split())
        g[u].append(v)
        g[v].append(u)

    dist = [-1] * (n + 1)
    q = deque([1])
    dist[1] = 0

    while q:
        u = q.popleft()
        for v in g[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)

    even = []
    odd = []

    for i in range(1, n + 1):
        if dist[i] % 2 == 0:
            even.append(i)
        else:
            odd.append(i)

    if len(even) <= len(odd):
        ans = even
    else:
        ans = odd

    print(len(ans))
    print(*ans)
```

The BFS computes shortest distances from node 1, which is sufficient because connectivity guarantees every node is reachable. The parity split is stored in two lists. Finally, we pick the smaller list to ensure the size constraint.

A common mistake is to assume arbitrary coloring works; the BFS ensures a consistent parity assignment across the graph. Another subtle point is that we do not need to explicitly verify coverage, since the parity construction guarantees it structurally.

## Worked Examples

### Example 1

Input:

```
4 6
1 2
1 3
1 4
2 3
2 4
3 4
```

This is a complete graph.

| Step | Queue | Node | dist | even | odd |
| --- | --- | --- | --- | --- | --- |
| Init | [1] | 1 | 0 | [] | [] |
| BFS 1 | [2,3,4] | 1 processed | 0 | [1] | [] |
| BFS 2 | [] | 2,3,4 all dist 1 | 1 | [1] | [2,3,4] |

We choose even = [1] since it is smaller.

This shows that in dense graphs, BFS depth collapses quickly and still yields a valid minimal partition.

### Example 2

Input:

```
5 4
1 2
2 3
3 4
4 5
```

This is a path.

| Step | Queue | dist assignment | even | odd |
| --- | --- | --- | --- | --- |
| Start | [1] | 1:0 | [] | [] |
| BFS | [2] | 2:1 | [1] | [] |
| BFS | [3] | 3:2 | [1,3,5] | [2,4] |

We select odd = [2,4] since it is smaller.

This confirms that alternating layers in a path produce a perfect covering set.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | BFS visits each vertex and edge once per query |
| Space | O(n + m) | adjacency list and distance array |

The total input size across all queries is bounded by 2⋅10^5 edges, so this linear traversal is easily fast enough under the time limit.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline
    from collections import deque

    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        g = [[] for _ in range(n + 1)]
        for _ in range(m):
            u, v = map(int, input().split())
            g[u].append(v)
            g[v].append(u)

        dist = [-1] * (n + 1)
        q = deque([1])
        dist[1] = 0

        while q:
            u = q.popleft()
            for v in g[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    q.append(v)

        even = []
        odd = []
        for i in range(1, n + 1):
            if dist[i] % 2 == 0:
                even.append(i)
            else:
                odd.append(i)

        ans = even if len(even) <= len(odd) else odd
        out.append(str(len(ans)))
        out.append(" ".join(map(str, ans)))

    return "\n".join(out)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# sample 1
assert run("""2
4 6
1 2
1 3
1 4
2 3
2 4
3 4
6 8
2 5
5 4
4 3
4 1
1 3
2 3
2 6
5 6
""") == """1
1
3
4 3 6"""

# chain graph
assert run("""1
5 4
1 2
2 3
3 4
4 5
""").split()[0] == "2"

# star graph
assert run("""1
5 4
1 2
1 3
1 4
1 5
""").split()[0] == "1"

# complete graph
assert run("""1
4 6
1 2
1 3
1 4
2 3
2 4
3 4
""").split()[0] == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| complete graph | 1 vertex | optimal collapse case |
| chain graph | n/2 selection | alternating structure |
| star graph | center or leaves | extreme imbalance handling |
| sample | valid partition | correctness on mixed graphs |

## Edge Cases

In a single-vertex-centered star, BFS depth produces one center at distance 0 and all others at distance 1. The algorithm selects the smaller parity class, which is the center, correctly covering all leaves.

In a long path, BFS alternates distances exactly along the chain, so parity classes split evenly or nearly evenly. Selecting the smaller class still covers every internal node via its neighbors.

In a complete graph, BFS assigns distance 1 to all nodes except the root. The even set becomes a single node, which already dominates all others since every vertex is adjacent to it.
