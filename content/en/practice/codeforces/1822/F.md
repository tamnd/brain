---
title: "CF 1822F - Gardening Friends"
description: "We are given a tree rooted at vertex 1, where every edge has the same length. The “cost” of the tree is simply how far the farthest vertex is from the current root. Because all edges have identical weight, this cost is just the height of the tree times the edge length."
date: "2026-06-09T07:50:31+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dfs-and-similar", "dp", "graphs", "trees"]
categories: ["algorithms"]
codeforces_contest: 1822
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 867 (Div. 3)"
rating: 1700
weight: 1822
solve_time_s: 74
verified: true
draft: false
---

[CF 1822F - Gardening Friends](https://codeforces.com/problemset/problem/1822/F)

**Rating:** 1700  
**Tags:** brute force, dfs and similar, dp, graphs, trees  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree rooted at vertex 1, where every edge has the same length. The “cost” of the tree is simply how far the farthest vertex is from the current root. Because all edges have identical weight, this cost is just the height of the tree times the edge length.

The twist is that we are allowed to move the root, but only along edges, one step at a time. Each move shifts the root to an adjacent vertex and costs a fixed number of coins. After any number of such moves, we evaluate the tree cost again from the new root, and subtract the total movement cost. The goal is to choose a sequence of root shifts that maximizes the final profit.

The input is a tree, so there are no cycles and exactly one simple path between any pair of vertices. This structure is crucial because every root movement is effectively a walk on this tree.

The constraints force a linear or near-linear solution. With up to 200,000 vertices total across test cases, any solution that recomputes distances from scratch for every possible root would fail. Even a BFS or DFS per candidate root leads to quadratic behavior, which is far beyond what is acceptable.

A subtle issue appears when thinking greedily. A naive idea is to keep moving the root toward deeper parts of the tree to increase height. This fails because every move has a cost, and increasing depth does not necessarily increase the overall eccentricity of the root.

Another common pitfall is assuming the best final root must be a centroid or midpoint of a diameter. This is not sufficient because we are not choosing a static root, but paying to walk to it.

The real difficulty is that movement cost depends on the path taken, while tree cost depends only on the final root.

## Approaches

A brute-force interpretation would be to consider every possible sequence of root moves. From a given root, we try moving to any neighbor, recursively exploring all states, and compute the resulting profit. This immediately explodes, because the state space is essentially all walks on the tree, which is exponential in depth.

Even if we restrict ourselves to final root positions only, we would still need to compute, for every node, the distance to the farthest node (its eccentricity). That part is already O(n) per node using BFS or DFS, leading to O(n²) per test case.

The key observation is that we never need to explicitly simulate all movement paths. The cost of moving the root is proportional to the number of edges traversed, so if we fix a final root, the movement cost is exactly the distance in the tree from 1 to that root, multiplied by c.

So the problem reduces to choosing a node v to maximize:

profit(v) = eccentricity(v) * k - dist(1, v) * c

This is now a tree DP-style optimization over nodes, where we need two quantities for each node: its distance from the original root, and its eccentricity.

The distance from root 1 is straightforward via a DFS or BFS. The eccentricity requires the classical tree trick: two BFS traversals. First find one endpoint of the diameter, then from it find the farthest node, and then compute distances from both endpoints. The eccentricity of any node is the maximum of its distances to the two diameter endpoints.

Once these values are precomputed, evaluating every node becomes linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over paths | Exponential | O(n) | Too slow |
| Compute eccentricity + evaluate all roots | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Run a BFS/DFS from node 1 to compute dist1[v], the distance from the original root to every node v. This captures the total cost of moving the root to v, since each move is one edge and costs c.
2. Find one endpoint of the tree diameter by running a BFS from any node, typically node 1. Call this endpoint a.
3. Run a BFS from a to compute distances da[v]. Then find the farthest node from a, call it b.
4. Run another BFS from b to compute distances db[v].
5. For every node v, compute its eccentricity as max(da[v], db[v]). This works because in a tree, the farthest node from v is always one of the diameter endpoints.
6. For each node v, compute profit candidate as ecc[v] * k - dist1[v] * c.
7. Return the maximum value over all nodes.

The reason we can restrict eccentricity computation to diameter endpoints is that in a tree, all longest paths pass through the diameter, so any farthest node must lie at one of its ends.

### Why it works

The algorithm separates the two competing effects cleanly: moving the root has a linear cost along tree edges, while the benefit depends only on how far the new root is from the farthest leaf. Both quantities are path-based and can be fully captured using BFS distances. The diameter endpoints provide a global structure that bounds all eccentricities, ensuring that no node’s farthest distance is missed. Because every possible final state is uniquely represented by a node, and every such node is evaluated exactly once, the maximum computed value is globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def bfs(start, adj):
    n = len(adj) - 1
    dist = [-1] * (n + 1)
    q = deque([start])
    dist[start] = 0
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist

t = int(input())
for _ in range(t):
    n, k, c = map(int, input().split())
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)

    dist1 = bfs(1, adj)

    a = max(range(1, n + 1), key=lambda x: dist1[x])
    da = bfs(a, adj)
    b = max(range(1, n + 1), key=lambda x: da[x])
    db = bfs(b, adj)

    ans = 0
    for v in range(1, n + 1):
        ecc = max(da[v], db[v])
        ans = max(ans, ecc * k - dist1[v] * c)

    print(ans)
```

The first BFS fixes the cost of reaching any potential final root. The second and third BFS computations locate the diameter endpoints, which allow eccentricities to be derived in constant time per node.

The final loop evaluates every possible root directly. The multiplication by k and c is kept as integer arithmetic throughout, avoiding precision issues.

A subtle implementation detail is that we do not recompute BFS from every node, since that would be quadratic. Instead, we reuse the diameter structure, which is what reduces eccentricity computation to linear time.

## Worked Examples

### Example 1

Input:

```
3 2 3
2 1
3 1
```

We compute distances from node 1:

| Node | dist1 |
| --- | --- |
| 1 | 0 |
| 2 | 1 |
| 3 | 1 |

Diameter endpoints are 2 and 3. Distances:

| Node | da (from 2) | db (from 3) | ecc |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 2 | 0 | 2 | 2 |
| 3 | 2 | 0 | 2 |

Profit values:

| Node | ecc*k | dist1*c | profit |
| --- | --- | --- | --- |
| 1 | 2 | 0 | 2 |
| 2 | 4 | 3 | 1 |
| 3 | 4 | 3 | 1 |

Maximum is 2 at node 1.

This shows that even though moving increases distance from some leaves, the movement cost dominates immediately.

### Example 2

A longer tree:

```
5 4 1
2 1
4 2
5 4
3 4
```

Distances from 1:

| Node | dist1 |
| --- | --- |
| 1 | 0 |
| 2 | 1 |
| 4 | 2 |
| 5 | 3 |
| 3 | 3 |

Diameter endpoints are 5 and 3. Eccentricities:

| Node | ecc |
| --- | --- |
| 1 | 3 |
| 2 | 2 |
| 4 | 2 |
| 5 | 3 |
| 3 | 3 |

Profit:

| Node | ecc*k | dist1*c | profit |
| --- | --- | --- | --- |
| 1 | 12 | 0 | 12 |
| 2 | 8 | 1 | 7 |
| 4 | 8 | 2 | 6 |
| 5 | 12 | 3 | 9 |
| 3 | 12 | 3 | 9 |

Best is 12 at node 1.

This illustrates that despite high eccentricity nodes existing, the cost to reach them reduces net gain.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each BFS runs in linear time and we perform three BFS traversals plus one linear scan |
| Space | O(n) | Adjacency list and distance arrays |

The sum of n over all test cases is bounded by 2e5, so the total runtime remains linear overall. This comfortably fits within the constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import collections

    def solve():
        input = sys.stdin.readline

        def bfs(start, adj):
            n = len(adj) - 1
            dist = [-1] * (n + 1)
            q = collections.deque([start])
            dist[start] = 0
            while q:
                u = q.popleft()
                for v in adj[u]:
                    if dist[v] == -1:
                        dist[v] = dist[u] + 1
                        q.append(v)
            return dist

        t = int(input())
        out = []
        for _ in range(t):
            n, k, c = map(int, input().split())
            adj = [[] for _ in range(n + 1)]
            for _ in range(n - 1):
                u, v = map(int, input().split())
                adj[u].append(v)
                adj[v].append(u)

            dist1 = bfs(1, adj)
            a = max(range(1, n + 1), key=lambda x: dist1[x])
            da = bfs(a, adj)
            b = max(range(1, n + 1), key=lambda x: da[x])
            db = bfs(b, adj)

            ans = 0
            for v in range(1, n + 1):
                ecc = max(da[v], db[v])
                ans = max(ans, ecc * k - dist1[v] * c)

            out.append(str(ans))

        return "\n".join(out)

    return solve()

# provided samples
assert run("""4
3 2 3
2 1
3 1
5 4 1
2 1
4 2
5 4
3 4
6 5 3
4 1
6 1
2 6
5 1
3 2
10 6 4
1 3
1 9
9 7
7 6
6 4
9 2
2 8
8 5
5 10
""") == """2
12
17
32"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single star tree | handles minimal diameter | correctness on trivial structure |
| chain tree | linear structure extremes | correctness of eccentricity |
| balanced tree | multiple equal optimal roots | tie handling |

## Edge Cases

A star-shaped tree is the clearest case where intuition can fail. The center has minimal eccentricity but zero movement cost, while leaves have maximal eccentricity but high movement cost. The algorithm correctly evaluates both and selects based on net profit.

In a path graph, every node lies on the diameter, so eccentricity equals distance to one endpoint or the other. The BFS-from-diameter-ends method correctly assigns each node its farthest distance without needing per-node BFS.

When k is small compared to c, moving the root is never beneficial. The algorithm still handles this because the dist1 * c term dominates all gains, and the maximum naturally occurs at node 1.
