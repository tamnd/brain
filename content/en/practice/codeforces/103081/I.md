---
title: "CF 103081I - Emails"
description: "We are given a set of people represented as nodes in an undirected graph. An edge between two nodes means those two people initially know each other’s email addresses. The system evolves in synchronous rounds."
date: "2026-07-04T00:24:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103081
codeforces_index: "I"
codeforces_contest_name: "2020-2021 ICPC Southwestern European Regional Contest (SWERC 2020)"
rating: 0
weight: 103081
solve_time_s: 57
verified: true
draft: false
---

[CF 103081I - Emails](https://codeforces.com/problemset/problem/103081/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of people represented as nodes in an undirected graph. An edge between two nodes means those two people initially know each other’s email addresses. The system evolves in synchronous rounds. Every morning, each person broadcasts their entire current address book to all their neighbors. Every evening, each person merges everything they received during the day into their own address book. Once a person receives nothing new in an evening update, they stop participating.

The question is not to simulate the process directly, but to determine whether eventually every person learns every other person’s email address. If yes, we must also compute how long it takes until the last meaningful propagation completes, measured in days with a specific convention about whether we count the last update or the stabilization step.

The communication rule is essentially transitive closure of information over time, but the key detail is that information spreads one hop per day in a layered fashion, because updates are only incorporated in the evening and only sent the next morning.

The input graph has up to 100,000 nodes and 100,000 edges. Any solution that tries to explicitly simulate propagation of full address books is impossible, because each node could accumulate O(N) information and each day could cost O(N + M) per node in the worst case, which is far beyond feasible limits. This immediately forces us to reason at the level of graph structure and distances rather than simulating sets.

A critical observation is that the process only makes sense if the graph is connected. If it is not connected, there is no path of email transmission between components, so no amount of repeated unioning will ever bridge different connected components.

A subtle edge case appears when the graph is already complete or nearly complete. For example, if every node is connected to every other node, the process finishes in essentially one round. A naive BFS-style “multi-source flood” might incorrectly assume zero time or off-by-one differences depending on whether the final stabilization day is counted. Another edge case is a disconnected graph where only two components exist: even though within each component everything converges, globally it is impossible to reach a full global address book.

## Approaches

A brute-force interpretation of the process is to simulate each day explicitly. Each node maintains a set of known emails. On each day, every node sends its full set to neighbors, unions all received sets, and we repeat until no set changes. Each union operation can cost O(N) in the worst case if sets are large, and it happens across O(M) edges per day. In the worst case, this leads to O(D · N · M) behavior where D can be O(N), which is completely infeasible for 100,000 nodes.

The key structural insight is that the process is equivalent to computing shortest-path distances in an unweighted graph, but with a twist in how rounds are defined. If we think carefully, a piece of information travels one edge per day. That means that if we fix a starting node, the time it takes for its email to reach another node is exactly the shortest path distance between them in edges. Since eventually everyone must know everyone else’s email, what matters is how long it takes for information to propagate across the diameter of each connected component.

More precisely, once we consider a single connected component, information spreads like a wave from every node simultaneously. The last moment when any new information appears corresponds to the eccentricity structure of the graph. The process completes when every node has reached every other node, so the time is governed by the maximum shortest path distance between any two nodes in the same connected component, i.e. the diameter.

Thus, the problem reduces to finding whether the graph is connected, and if so computing the diameter of the connected graph. The final answer is derived from this diameter with a small adjustment depending on whether we measure last update day or stabilization day.

To compute diameter in a general unweighted graph, we use two BFS passes per component: pick any node, BFS to find the farthest node, then BFS again from that node to get the farthest distance. The maximum such value across components is the diameter. If there are multiple components, the process never fully connects everyone, so answer is -1.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(D · N · M) | O(N²) worst-case sets | Too slow |
| BFS Diameter per component | O(N + M) | O(N + M) | Accepted |

## Algorithm Walkthrough

We convert the input into an adjacency list representation of an undirected graph.

We first determine connectivity and prepare to measure distances.

1. Build the adjacency list of the graph from the M edges. This is required because BFS needs fast neighbor access, and edge list traversal would be too slow for repeated searches.
2. Check whether all nodes belong to a single connected component using BFS or DFS. If we find more than one component, we immediately return -1 because no sequence of local exchanges can bridge disconnected parts.
3. For each connected component, we compute its diameter using two BFS passes. We start from an arbitrary node in the component and run BFS to find the farthest node u from it. This step identifies one endpoint of a longest path in that component.
4. We run BFS again starting from u to compute the maximum distance to any node in the same component. The largest distance encountered is the diameter of that component.
5. Track the maximum diameter across all components. If the graph is connected, this is simply the global diameter.
6. Convert the diameter into the required number of days according to the process timing rules. Since each day corresponds to a full propagation of one edge layer and the process starts with initial knowledge already present on day 0 morning, the number of days until the last update is the diameter.

### Why it works

The key invariant is that after k full days, every node knows exactly the information that originates within k edges of distance in the graph. This follows because each day expands knowledge exactly one hop outward along all edges simultaneously. Therefore, the set of known emails at node v after k days corresponds exactly to all nodes within distance k of v.

Once k reaches the eccentricity of a node, that node stops changing. The last global change happens when k reaches the maximum eccentricity over all nodes, which is exactly the graph diameter. Thus, no node can receive new information after diameter steps, and some node must still be receiving information until that point, ensuring correctness.

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
    far = start

    while q:
        v = q.popleft()
        for to in adj[v]:
            if dist[to] == -1:
                dist[to] = dist[v] + 1
                q.append(to)
                if dist[to] > dist[far]:
                    far = to
    return far, dist

def bfs_dist(start, adj):
    n = len(adj) - 1
    dist = [-1] * (n + 1)
    q = deque([start])
    dist[start] = 0
    far = 0

    while q:
        v = q.popleft()
        for to in adj[v]:
            if dist[to] == -1:
                dist[to] = dist[v] + 1
                q.append(to)
                if dist[to] > dist[far]:
                    far = to
    return dist

def solve():
    n, m = map(int, input().split())
    adj = [[] for _ in range(n + 1)]

    for _ in range(m):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)

    visited = [False] * (n + 1)
    components = 0
    diameter = 0

    for i in range(1, n + 1):
        if not visited[i]:
            components += 1
            q = deque([i])
            visited[i] = True
            comp_nodes = [i]

            while q:
                v = q.popleft()
                for to in adj[v]:
                    if not visited[to]:
                        visited[to] = True
                        q.append(to)
                        comp_nodes.append(to)

            if components > 1:
                print(-1)
                return

            start = i
            far, _ = bfs(start, adj)
            dist = bfs_dist(far, adj)
            diameter = max(diameter, max(dist))

    print(diameter)

if __name__ == "__main__":
    solve()
```

The solution begins by constructing adjacency lists, which supports linear-time traversal of neighbors. A BFS-based component check ensures we detect disconnection early, which is required because no communication path can exist between components.

For each connected component, we compute its diameter using the standard two-BFS technique. The first BFS identifies a farthest node from an arbitrary start, which serves as an endpoint of a longest path in that component. The second BFS from that endpoint computes the true eccentricity structure, giving the maximum distance in that component.

The final answer is the diameter because each unit of distance corresponds to one full day of propagation.

## Worked Examples

### Example 1

Input:

```
4 3
1 2
2 3
3 4
```

This is a single chain.

We first BFS from node 1:

| Step | Node | Distance |
| --- | --- | --- |
| 1 | 1 | 0 |
| 2 | 2 | 1 |
| 3 | 3 | 2 |
| 4 | 4 | 3 |

The farthest node is 4.

Now BFS from 4:

| Step | Node | Distance |
| --- | --- | --- |
| 1 | 4 | 0 |
| 2 | 3 | 1 |
| 3 | 2 | 2 |
| 4 | 1 | 3 |

The diameter is 3, so after 3 days no new information can propagate.

This corresponds to the longest chain distance in the graph.

### Example 2

Input:

```
6 3
1 2
3 4
5 6
```

This graph has three disconnected components.

During the component scan, we encounter a second component after finishing the first. Since more than one component exists, the process can never unify all email sets.

Output is:

```
-1
```

This confirms that connectivity is a strict requirement for full convergence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + M) | Each BFS visits nodes and edges once, and we perform a constant number of BFS runs per component |
| Space | O(N + M) | Adjacency list plus BFS queues and distance arrays |

The constraints allow linear-time graph traversal, so this approach comfortably fits within limits even for 100,000 nodes and edges.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    def bfs(start, adj):
        n = len(adj) - 1
        dist = [-1] * (n + 1)
        q = deque([start])
        dist[start] = 0
        far = start
        while q:
            v = q.popleft()
            for to in adj[v]:
                if dist[to] == -1:
                    dist[to] = dist[v] + 1
                    q.append(to)
                    if dist[to] > dist[far]:
                        far = to
        return far

    def bfs_dist(start, adj):
        n = len(adj) - 1
        dist = [-1] * (n + 1)
        q = deque([start])
        dist[start] = 0
        while q:
            v = q.popleft()
            for to in adj[v]:
                if dist[to] == -1:
                    dist[to] = dist[v] + 1
                    q.append(to)
        return dist

    def solve():
        n, m = map(int, input().split())
        adj = [[] for _ in range(n + 1)]
        for _ in range(m):
            u, v = map(int, input().split())
            adj[u].append(v)
            adj[v].append(u)

        visited = [False] * (n + 1)
        components = 0
        diameter = 0

        for i in range(1, n + 1):
            if not visited[i]:
                components += 1
                q = deque([i])
                visited[i] = True
                while q:
                    v = q.popleft()
                    for to in adj[v]:
                        if not visited[to]:
                            visited[to] = True
                            q.append(to)

                if components > 1:
                    return "-1"

                far = bfs(i, adj)
                dist = bfs_dist(far, adj)
                diameter = max(diameter, max(dist))

        return str(diameter)

    return solve()

# provided samples
assert run("4 3\n1 2\n2 3\n3 4\n") == "3"
assert run("6 3\n1 2\n3 4\n5 6\n") == "-1"

# custom cases
assert run("2 1\n1 2\n") == "1", "minimum chain"
assert run("5 4\n1 2\n2 3\n3 4\n4 5\n") == "4", "line graph"
assert run("3 3\n1 2\n2 3\n1 3\n") == "1", "complete graph"
assert run("4 2\n1 2\n3 4\n") == "-1", "two components"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2-node chain | 1 | smallest connected case |
| 5-node line | 4 | long path propagation |
| triangle | 1 | dense graph early convergence |
| two pairs | -1 | disconnection handling |

## Edge Cases

A disconnected graph is handled at the component detection stage. When scanning nodes, the algorithm increments a component counter each time it finds an unvisited node. If this counter exceeds one, it immediately returns -1. For example, input `1-2` and `3-4` forms two components. BFS marks only nodes within each component, and the second discovery triggers termination before any diameter computation is attempted.

A fully connected graph has diameter 1. The first BFS from any node reaches all others in one step, and the second BFS confirms maximum distance 1. The algorithm correctly returns 1, matching the intuition that one round is sufficient for full exchange.

A linear chain is the worst case for propagation. Each BFS step extends reach by exactly one node, so the diameter equals N-1. The algorithm correctly captures this because the farthest endpoints are the ends of the chain, and the second BFS measures full length.
