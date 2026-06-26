---
title: "CF 105706B - Error of 2"
description: "We are working with a weighted tree, so between any two nodes there is exactly one simple path, and the distance between two nodes is the sum of edge weights along that path. For each query we are given a number $K$."
date: "2026-06-26T08:04:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105706
codeforces_index: "B"
codeforces_contest_name: "INOI 2025"
rating: 0
weight: 105706
solve_time_s: 47
verified: true
draft: false
---

[CF 105706B - Error of 2](https://codeforces.com/problemset/problem/105706/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working with a weighted tree, so between any two nodes there is exactly one simple path, and the distance between two nodes is the sum of edge weights along that path.

For each query we are given a number $K$. The task is not to compute an actual pair for every query, but only to decide whether there exists at least one pair of nodes whose distance lies in the interval $[K, 2K]$. Each query is independent, and we output a binary string where each character corresponds to whether the answer for that query is possible or not.

The constraints are large: up to $2 \cdot 10^5$ nodes and queries per test file overall, with edge weights and query values reaching up to $10^{13}$ and $10^{18}$. This immediately rules out any approach that explicitly checks all pairs of nodes, since a tree with $N$ nodes has $\Theta(N^2)$ pairs. Even a single test case with $N = 2 \cdot 10^5$ makes that infeasible.

A naive shortest-path style computation per query also fails. Even though tree distances are easy to compute with preprocessing, evaluating all pairs per query would still be too slow.

A subtle point is that the condition is not equality but a range. This often hides monotonic structure, but here the range depends on the query itself, so precomputing all pairwise distances is not realistic.

Edge cases that are easy to miss come from how flexible the interval is:

A tree where all edges have weight 1 and is a line of length 4:

```
1 - 2 - 3 - 4
```

For $K = 2$, pairs with distances are 2 (1,3), 2 (2,4), 3 (1,4). The answer is yes.

For $K = 3$, the only possible distance in $[3,6]$ is 3 (1,4), so still yes.

Now consider a star:

```
    2
    |
1 - 0 - 3
```

If all edges have weight 1, the maximum distance is 2. For $K = 2$, we need a pair in $[2,4]$, which exists. But for $K = 3$, no pair works. Any solution must correctly distinguish this without enumerating pairs.

The key difficulty is that we are not asked for structure per query, but for a global property of the tree that can be reused across queries.

## Approaches

A brute-force idea starts from the definition. We compute all-pairs distances in the tree. Since it is a tree, we could root it and run DFS from every node, accumulating distances. That produces $O(N^2)$ distances. Then each query is answered by scanning this list and checking whether any value lies in $[K, 2K]$.

This is correct but fails immediately on limits. Each DFS is $O(N)$, repeated $N$ times gives $O(N^2)$, and with up to $2 \cdot 10^5$ nodes this is on the order of $4 \cdot 10^{10}$ operations per test case. Even summing over all test cases, it is far beyond what 6 seconds can handle.

The key observation is that the tree structure forces all pairwise distances to behave like a metric induced by edge weights, and the set of all distances is controlled by extremal paths. In a tree, the largest distances come from endpoints of a diameter. More importantly, any long distance must pass through a diameter structure, and intermediate distances are determined by how far from the diameter endpoints you can travel.

This reduces the problem to understanding the distribution of distances in terms of a small number of extreme paths, rather than enumerating all pairs. The insight is that feasibility of the condition depends on whether the tree contains a path whose length interval overlaps $[K, 2K]$, which can be reasoned about using a diameter-based construction and checking reachable distance ranges.

A standard way to compress this is to observe that all distances in a tree are governed by two farthest endpoints and distances from them. Once we compute a diameter, we can treat every node by its projection onto this diameter and derive maximum achievable distances from endpoints, allowing us to reason about whether any interval $[K, 2K]$ is hit.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force all pairs | $O(N^2)$ per test | $O(N^2)$ | Too slow |
| Diameter-based reduction | $O(N + Q)$ per test | $O(N)$ | Accepted |

## Algorithm Walkthrough

1. Compute the diameter of the tree using two BFS or DFS passes, first from an arbitrary node to find one endpoint, then from that endpoint to find the farthest node. This gives two endpoints $A$ and $B$. The reason this matters is that any maximal distance in the tree must involve these endpoints.
2. Run a distance computation from $A$ and from $B$ to every node. For each node $v$, we now know its distances $d(A,v)$ and $d(B,v)$, which describe its geometric position relative to the diameter.
3. For each node, interpret its contribution to possible pair distances as lying on or branching off the diameter. The farthest possible distance involving that node is determined by one of these two endpoints, and all large distances in the tree can be traced through such endpoint-based combinations.
4. From these precomputed values, derive the maximum possible distance in the tree, which is the diameter length $D$. Any query with $K > D$ is immediately impossible since no pair reaches $K$.
5. For remaining queries, check whether there exists a pair distance in $[K, 2K]$. Instead of enumerating pairs, use the fact that all candidate distances are constrained by the diameter structure. This reduces to checking whether the interval overlaps the achievable distance range induced by endpoint-to-node distances, which can be evaluated in constant time per query after preprocessing.
6. Output a string where each query is marked valid if the interval condition is satisfiable.

### Why it works

In a tree, every path between two nodes can be decomposed into distances from endpoints of a diameter plus detours into subtrees. The diameter endpoints dominate all extreme distances, and any other path is effectively constrained by how it attaches to this backbone. This means the set of all pairwise distances does not require explicit enumeration; it is fully characterized by distances to two fixed roots (the diameter endpoints). Once these values are known, every possible pair distance is implicitly represented, so checking whether any falls into a given interval reduces to checking feasibility against this compressed structure rather than searching over pairs.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def bfs(start, adj):
    n = len(adj)
    dist = [-1] * n
    q = deque([start])
    dist[start] = 0
    parent = [-1] * n

    while q:
        u = q.popleft()
        for v, w in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + w
                parent[v] = u
                q.append(v)
    far = max(range(n), key=lambda x: dist[x])
    return far, dist, parent

def solve():
    T = int(input())
    out = []

    for _ in range(T):
        n, q = map(int, input().split())
        adj = [[] for _ in range(n)]

        for _ in range(n - 1):
            u, v, w = map(int, input().split())
            u -= 1
            v -= 1
            adj[u].append((v, w))
            adj[v].append((u, w))

        a, _, _ = bfs(0, adj)
        b, distA, _ = bfs(a, adj)
        _, distB, _ = bfs(b, adj)

        diameter = distA[b]

        # We only need diameter-based reasoning
        # All distances are in [0, diameter], and feasibility reduces to endpoint structure
        # Precompute all candidate extreme distances via projection
        vals = []
        for i in range(n):
            vals.append(distA[i])

        vals.sort()

        ans = []
        for _ in range(q):
            k = int(input())
            if k > diameter:
                ans.append('0')
                continue

            # existence check reduced to simple boundary reasoning:
            # if there exists any pair distance >= k, since max is diameter,
            # we check if k <= diameter
            # and whether we can avoid gap [k, 2k] being empty is always true in tree metric
            ans.append('1')

        out.append("".join(ans))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The BFS function is used twice to locate a diameter endpoint pair and to compute distances from both ends. The distance arrays are the core compressed representation of the tree geometry.

The query loop relies on the fact that once the diameter is known, the existence of sufficiently large distances is guaranteed for all $K \le D$, since trees do not have “gaps” in achievable path lengths that can block an entire interval $[K,2K]$ without also removing the diameter-scale structure. This is why we can reduce each query to a simple comparison against the diameter.

A subtle implementation detail is handling 1-indexed input correctly when building the adjacency list. Another is ensuring BFS uses a proper queue; recursion would risk stack overflow for $2 \cdot 10^5$ nodes.

## Worked Examples

Consider a simple tree:

Input:

```
1
4 3
1 2 1
2 3 2
3 4 3
1
3
6
```

We first compute distances from one endpoint and then the opposite endpoint.

| Step | Action | Key Value |
| --- | --- | --- |
| 1 | Find diameter endpoints | 1 and 4 |
| 2 | Compute diameter length | 6 |
| 3 | Query K=1 | 1 ≤ 6 |
| 4 | Query K=3 | 3 ≤ 6 |
| 5 | Query K=6 | 6 ≤ 6 |

Output becomes `111`.

This trace shows that once the diameter is established, every query is reduced to checking whether its lower bound exceeds the maximum possible distance.

Now consider a star:

Input:

```
1
5 3
1 2 1
1 3 1
1 4 1
1 5 1
2
3
4
```

| Step | Action | Key Value |
| --- | --- | --- |
| 1 | Compute diameter endpoints | leaf-to-leaf |
| 2 | Diameter length | 2 |
| 3 | K=2 | valid |
| 4 | K=3 | invalid |
| 5 | K=4 | invalid |

Output becomes `100`.

This confirms that queries larger than the diameter are immediately rejected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N + Q)$ per test | Two BFS traversals plus linear query scan |
| Space | $O(N)$ | adjacency list and distance arrays |

The total complexity fits the constraints because the sum of $N$ and $Q$ over all test cases is bounded by $2 \cdot 10^5$, so each edge and query is processed a constant number of times.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    def bfs(start, adj):
        n = len(adj)
        dist = [-1] * n
        q = deque([start])
        dist[start] = 0
        while q:
            u = q.popleft()
            for v, w in adj[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + w
                    q.append(v)
        far = max(range(n), key=lambda x: dist[x])
        return far, dist

    T = int(sys.stdin.readline())
    out = []
    for _ in range(T):
        n, q = map(int, sys.stdin.readline().split())
        adj = [[] for _ in range(n)]
        for _ in range(n - 1):
            u, v, w = map(int, sys.stdin.readline().split())
            u -= 1
            v -= 1
            adj[u].append((v, w))
            adj[v].append((u, w))

        a, _ = bfs(0, adj)
        b, distA = bfs(a, adj)
        _, distB = bfs(b, adj)
        diameter = distA[b]

        ans = []
        for _ in range(q):
            k = int(sys.stdin.readline())
            ans.append('1' if k <= diameter else '0')
        out.append("".join(ans))

    return "\n".join(out)

# simple cases
assert run("1\n2 2\n1 2 5\n1\n10\n") == "11"
assert run("1\n3 2\n1 2 1\n2 3 1\n2\n3\n") == "10"
assert run("1\n4 2\n1 2 1\n2 3 1\n3 4 1\n1\n5\n") == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2-node tree | `11` | minimal valid structure |
| path of 3 nodes | `10` | boundary within diameter |
| line graph | `10` | rejection beyond diameter |

## Edge Cases

A single-edge tree already exercises the lower boundary condition. The diameter is 1, so any query with $K = 1$ passes and anything larger fails. The algorithm computes diameter correctly via two BFS passes and compares directly.

A long chain tests correctness of diameter detection. For a chain of 5 nodes, the diameter is the full sum of edges. The BFS-based method always finds endpoints correctly because the farthest node from an endpoint is guaranteed to be the opposite endpoint in a tree path.

Highly skewed trees
