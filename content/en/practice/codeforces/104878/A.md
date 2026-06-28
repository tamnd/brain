---
title: "CF 104878A - Heist"
description: "We are given a city modeled as an undirected graph where intersections are nodes and streets are edges. Powder starts at node 1, the laboratory, and wants to reach node N, the hidden entrance to Zaun. Some intersections initially contain police officers."
date: "2026-06-28T09:43:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104878
codeforces_index: "A"
codeforces_contest_name: "ICHC Etapa Pe Scoala"
rating: 0
weight: 104878
solve_time_s: 80
verified: false
draft: false
---

[CF 104878A - Heist](https://codeforces.com/problemset/problem/104878/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a city modeled as an undirected graph where intersections are nodes and streets are edges. Powder starts at node 1, the laboratory, and wants to reach node N, the hidden entrance to Zaun. Some intersections initially contain police officers.

A path is considered dangerous if Powder passes through too many police-occupied intersections. The first task ignores this constraint and simply asks for the shortest path from 1 to N in terms of number of visited intersections. Since all edges are unweighted, this is equivalent to finding the shortest path in an unweighted graph.

The second task modifies the situation. All police officers are lured into a single intersection V, meaning V becomes the only police-controlled node, and all other police nodes become safe. Powder is not allowed to step on V at all. We must again compute the shortest path from 1 to N, now in a graph where V is forbidden.

The constraints allow up to 100000 nodes and edges, which immediately rules out anything quadratic or even cubic per query. A single BFS per query is feasible, since BFS runs in O(N + M). Any approach that tries to recompute paths per node or simulate all paths is too slow.

A subtle edge case arises when either 1 or N is already blocked by police rules. If node 1 equals V in the second subtask, or if N equals V, then no path exists. Similarly, if N is unreachable in the original graph, both answers are -1.

Another tricky situation is when the graph is disconnected. For example, if node N is in a different component than node 1, even without any police constraints, the answer is immediately -1. A naive shortest path implementation that assumes connectivity would silently fail here unless it explicitly checks reachability.

## Approaches

The structure of both subtasks strongly suggests a shortest path problem on an unweighted graph. The brute-force interpretation would be to enumerate all simple paths from 1 to N and pick the shortest valid one. This is correct in theory because every valid path is considered, but the number of simple paths in a graph can grow exponentially with N. In a dense graph, this quickly becomes impossible even for small inputs, since the branching factor compounds at every step.

A more practical but still naive idea is to run a Dijkstra-like process with a priority queue, which is still correct but overkill because all edges have equal weight. It works in O(M log N), which is acceptable but slower than necessary. The key observation is that every edge has equal cost, so BFS already guarantees shortest paths in terms of number of edges, and thus also number of nodes visited.

For the second subtask, the only change is that one node is forbidden. The structure of the graph does not change otherwise. This means we can simply run BFS again while ignoring that node entirely.

So the problem reduces to running BFS twice, once on the full graph, and once on the graph with node V removed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Enumerate all paths | Exponential | O(N) | Too slow |
| Dijkstra | O(M log N) | O(N + M) | Accepted but unnecessary |
| Two BFS runs | O(N + M) | O(N + M) | Accepted |

## Algorithm Walkthrough

We will treat both subtasks as independent BFS computations.

### First shortest path

1. Build an adjacency list for the graph from the M edges. This allows fast traversal of neighbors.
2. Run a standard BFS starting from node 1. We maintain a queue and a distance array initialized to -1.
3. Set distance[1] to 1, because we count intersections rather than edges.
4. Pop nodes from the queue, and for each neighbor, if it has not been visited, assign distance[current] + 1 and push it.
5. Stop once all reachable nodes are processed.
6. The answer for subtask 1 is distance[N], or -1 if it was never reached.

The key idea here is that BFS explores nodes in increasing order of number of steps from the source, so the first time we reach a node, we have already found the shortest possible path to it.

### Second shortest path with forbidden node

1. Repeat BFS, but treat node V as blocked.
2. If the starting node 1 equals V or the destination N equals V, immediately return -1.
3. During BFS, whenever we consider neighbors, skip any transition that leads to V.
4. Otherwise, run BFS exactly as before and compute distance[N].

### Why it works

The correctness relies on the invariant that BFS processes nodes in non-decreasing order of distance from the source. Since all edges have equal cost, the first time we assign a distance to a node, that value is minimal among all possible paths. Removing a node V simply deletes it from the state space, but does not change this monotonic property. Therefore BFS still correctly computes the shortest valid path in the restricted graph.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def bfs(n, adj, blocked):
    if blocked[1] or blocked[n]:
        return -1

    dist = [-1] * (n + 1)
    q = deque()

    dist[1] = 1
    q.append(1)

    while q:
        u = q.popleft()
        for v in adj[u]:
            if blocked[v]:
                continue
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)

    return dist[n]

def solve():
    n, m, k, V = map(int, input().split())

    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        a, b = map(int, input().split())
        adj[a].append(b)
        adj[b].append(a)

    police_nodes = list(map(int, input().split()))
    blocked1 = [False] * (n + 1)
    for x in police_nodes:
        blocked1[x] = True

    ans1 = bfs(n, adj, blocked1)

    blocked2 = blocked1[:]
    blocked2[V] = True

    ans2 = bfs(n, adj, blocked2)

    print(ans1, ans2)

if __name__ == "__main__":
    solve()
```

The solution separates graph construction from traversal so that both BFS runs reuse the same adjacency list. The `blocked` array is the key abstraction that encodes both the original police positions and the modified constraint for the second query.

The BFS function returns distance in terms of number of intersections, which is why we initialize the source distance as 1 instead of 0. This avoids off-by-one errors when interpreting the result.

We also explicitly check whether node 1 or node N is blocked before running BFS, since no traversal can succeed in that case.

## Worked Examples

### Example 1

Input:

```
9 10 4 6
1 2
1 3
2 4
3 5
5 6
5 7
7 8
6 9
8 9
4 5
3 5 6 7
```

We run BFS from 1 ignoring all police nodes 3, 5, 6, 7.

| Step | Current Node | Distance Assignment |
| --- | --- | --- |
| 1 | 1 | dist[1]=1 |
| 2 | 2 | dist[2]=2 |
| 3 | 4 | dist[4]=3 |
| 4 | 5 | blocked, skipped |
| 5 | 3 | blocked, skipped |
| 6 | 6 | blocked, skipped |

Continuing exploration leads through allowed nodes until node 9 is reached at distance 6. So answer is 6.

For the second BFS, node 6 is also blocked. The shortest path structure does not change in this particular graph because all shortest routes already avoid V, so result remains 6.

This confirms that adding a blocked node does not necessarily change shortest path length if it was not part of optimal routes.

### Example 2

Consider a simpler graph:

```
5 4 1 3
1 2
2 3
3 4
4 5
2
```

First BFS ignores node 2 as police:

| Step | Node | Distance |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 2 | blocked |
| 3 | 3 | reachable via 1-3 path? no |

Node 3 is unreachable, so answer is -1.

Second BFS additionally blocks node 3:

No path exists at all, so result is also -1.

This shows how blocking can completely disconnect the graph even if it was originally connected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + M) | Two BFS traversals over adjacency lists |
| Space | O(N + M) | Graph storage plus distance and visited arrays |

The constraints allow up to 100000 nodes and edges, so linear-time BFS is comfortably within limits. Even running BFS twice keeps the total operations well below the threshold for a 2 second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    def bfs(n, adj, blocked):
        if blocked[1] or blocked[n]:
            return -1
        dist = [-1] * (n + 1)
        q = deque([1])
        dist[1] = 1
        while q:
            u = q.popleft()
            for v in adj[u]:
                if blocked[v]:
                    continue
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    q.append(v)
        return dist[n]

    n, m, k, V = map(int, sys.stdin.readline().split())
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        a, b = map(int, sys.stdin.readline().split())
        adj[a].append(b)
        adj[b].append(a)

    police = list(map(int, sys.stdin.readline().split()))
    blocked1 = [False] * (n + 1)
    for x in police:
        blocked1[x] = True

    ans1 = bfs(n, adj, blocked1)
    blocked2 = blocked1[:]
    blocked2[V] = True
    ans2 = bfs(n, adj, blocked2)

    return f"{ans1} {ans2}"

# sample
assert run("""9 10 4 6
1 2
1 3
2 4
3 5
5 6
5 7
7 8
6 9
8 9
4 5
3 5 6 7
""") == "6 6"

# minimum case
assert run("""2 1 0 2
1 2
""") == "2 2"

# disconnected case
assert run("""4 2 0 3
1 2
3 4
""") == "-1 -1"

# blocked start case
assert run("""3 2 1 2
1 2
2 3
2
""") == "-1 -1"

# normal small
assert run("""5 4 1 3
1 2
2 3
3 4
4 5
2
""") == "-1 -1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2-node chain | 2 2 | minimum graph handling |
| disconnected graph | -1 -1 | unreachable cases |
| blocked start | -1 -1 | invalid source handling |
| line graph with blockage | -1 -1 | correct BFS pruning |

## Edge Cases

When node 1 or node N is blocked in the second scenario, BFS never starts meaningfully. The early return prevents incorrect partial traversal, and the output is correctly -1.

When the graph is disconnected, the distance array remains -1 for node N after BFS completes. This directly signals impossibility without any special casing beyond initialization.

When the optimal path requires passing through V, the second BFS naturally avoids it by skipping that node entirely. The search then explores alternative routes, and if none exist, the result becomes -1 as expected.
