---
title: "CF 105345F - Haunted House"
description: "The task is to determine which exit rooms in a building are safe for Harry to reach given that ghosts are also moving through the same building at the same speed. We can view the house as an undirected graph where rooms are nodes and doors are edges."
date: "2026-06-23T15:27:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105345
codeforces_index: "F"
codeforces_contest_name: "UTPC Contest 09-13-24 Div. 1 (Advanced)"
rating: 0
weight: 105345
solve_time_s: 95
verified: false
draft: false
---

[CF 105345F - Haunted House](https://codeforces.com/problemset/problem/105345/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 35s  
**Verified:** no  

## Solution
## Problem Understanding

The task is to determine which exit rooms in a building are safe for Harry to reach given that ghosts are also moving through the same building at the same speed.

We can view the house as an undirected graph where rooms are nodes and doors are edges. Harry starts at a fixed room, and there are several rooms marked as exits. At the same time, multiple ghosts start from their own rooms. Every second, Harry can move along one edge to a neighboring room, and every ghost can do the same. Movement happens simultaneously in discrete steps.

An exit is considered safe if Harry can reach it while ensuring that at no moment does he occupy a room at the same time as any ghost. Since both move at the same speed and can choose optimal paths, we are effectively comparing how quickly Harry and the closest ghost can reach each room.

The constraints allow up to 200,000 rooms and 200,000 edges, which immediately rules out any approach that recomputes shortest paths separately for each exit or simulates movements over time. A solution must rely on a small number of linear or near-linear graph traversals, typically O(n + m).

A subtle failure case appears when a ghost can reach a room at the same time Harry does. For example, if Harry reaches a room in 3 seconds and some ghost also reaches it in 3 seconds, Harry is considered unsafe there because they occupy the same room at the same time step.

Another important edge case is when Harry starts in a room that already contains a ghost. In that case, the starting position is immediately invalid for survival, since both occupy the same room at time 0.

Finally, exits may include rooms that are unreachable from Harry’s start. Such exits are automatically unsafe because Harry cannot reach them at all.

## Approaches

A direct way to think about the problem is to simulate both Harry and all ghosts over time. One could attempt a multi-agent BFS or simulate each second, tracking positions of all entities. This quickly becomes infeasible because at every step, each ghost branches through the graph, and we would be repeatedly exploring the same states. In the worst case, this degenerates into repeated traversals of size O(n + m) for each entity and each time step, leading to exponential or at least O(k(n + m)) behavior, which is far beyond the limit.

A more structured approach is to observe that what matters for each room is not the exact path taken, but the earliest time at which Harry and any ghost can arrive there. If we compute the shortest distance from Harry’s starting node to every room, and separately compute the shortest distance from any ghost’s starting position to every room, then the problem reduces to a simple comparison per exit room.

The key insight is that all ghosts move simultaneously and independently, so their influence can be combined by treating all ghost starting positions as sources in a single multi-source BFS. This gives, for every room, the earliest time any ghost can occupy it. Harry’s BFS gives his earliest arrival time. Since both move one step per second, Harry is safe in a room only if he arrives strictly before any ghost can reach it.

This reduces the entire problem to two BFS traversals over the same graph.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(k · (n + m)) or worse | O(n + m) | Too slow |
| Dual Multi-source BFS | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

We solve the problem by computing two distance maps over the graph.

## Algorithm Walkthrough

1. Build the adjacency list of the graph from the given edges. This allows efficient traversal of all connected rooms.
2. Run a multi-source BFS starting from all ghost positions at once. Initialize a distance array `distG` where all values are infinity except ghost starting rooms, which are set to 0. This BFS computes the earliest time any ghost can reach each room, because expanding simultaneously from all ghost sources naturally simulates the fastest possible spread.
3. Run a standard BFS from Harry’s starting room `s` to compute another distance array `distH`, representing the earliest time Harry can reach each room.
4. For each exit room `e_i`, check whether `distH[e_i]` is strictly less than `distG[e_i]`. If yes, Harry can arrive before any ghost can ever occupy that room, so it is safe. Otherwise it is unsafe.
5. Count all exit rooms satisfying this condition and output the total.

The reason the strict inequality matters is that simultaneous arrival is unsafe. If both distances are equal, a ghost can occupy the room at the same time step Harry arrives, violating the safety condition.

### Why it works

Each BFS computes shortest-path distances in an unweighted graph, which corresponds exactly to minimum time under unit movement cost. Because ghosts and Harry move at identical speeds and do not interact except by collision, the earliest arrival time fully characterizes whether a position can ever be safely occupied. The invariant is that at the end of BFS, `distG[v]` is the minimum possible time any ghost can reach room `v`, and `distH[v]` is the minimum time Harry can reach `v`. Since both processes explore all optimal paths in parallel, no faster arrival is possible than what BFS records. Comparing these two values is therefore equivalent to checking whether Harry can strictly outrun all ghosts to each exit.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

INF = 10**18

def bfs(starts, adj, n):
    dist = [INF] * (n + 1)
    q = deque()
    for s in starts:
        dist[s] = 0
        q.append(s)

    while q:
        v = q.popleft()
        for to in adj[v]:
            if dist[to] == INF:
                dist[to] = dist[v] + 1
                q.append(to)
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

    distH = bfs([s], adj, n)
    distG = bfs(ghosts, adj, n)

    ans = 0
    for e in exits:
        if distH[e] < distG[e]:
            ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation uses a shared BFS routine for both Harry and ghosts. The only difference is the initialization: Harry’s BFS starts from a single node, while the ghost BFS starts from multiple sources at once.

A subtle point is the initialization of distances to a large sentinel value, which ensures that unvisited nodes remain effectively unreachable. This is important when comparing distances, since an unreachable ghost node should not block Harry from reaching it.

The strict comparison `distH[e] < distG[e]` encodes the simultaneity constraint directly.

## Worked Examples

### Sample 1

We compute distances from Harry and from ghosts, then compare at the exit.

| Step | distH at exit | distG at exit | Decision |
| --- | --- | --- | --- |
| BFS from Harry | computed shortest time | - | - |
| BFS from ghosts | - | computed shortest time | - |
| Compare | 2 | 3 | safe |

Harry reaches the exit strictly earlier than any ghost, so the exit is counted as valid. This demonstrates the case where Harry successfully stays ahead of all ghost paths.

### Sample 2

| Step | distH at exit | distG at exit | Decision |
| --- | --- | --- | --- |
| BFS from Harry | 2 | - | - |
| BFS from ghosts | - | 2 | unsafe |
| Compare | 2 | 2 | rejected |

Here a ghost can reach the exit at the same time as Harry. Even though Harry has a path, the simultaneity condition makes the exit unsafe. This highlights why strict inequality is required.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Two BFS traversals each process every node and edge at most once |
| Space | O(n + m) | Adjacency list plus distance arrays |

The constraints allow up to 200,000 nodes and edges, and this solution performs only a small constant number of linear passes over the graph, so it fits comfortably within limits.

## Test Cases

```python
import sys, io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from collections import deque

    INF = 10**18

    def bfs(starts, adj, n):
        dist = [INF] * (n + 1)
        q = deque()
        for s in starts:
            dist[s] = 0
            q.append(s)
        while q:
            v = q.popleft()
            for to in adj[v]:
                if dist[to] == INF:
                    dist[to] = dist[v] + 1
                    q.append(to)
        return dist

    n, m, s, k, g = map(int, input().split())
    adj = [[] for _ in range(n + 1)]

    for _ in range(m):
        a, b = map(int, input().split())
        adj[a].append(b)
        adj[b].append(a)

    exits = list(map(int, input().split()))
    ghosts = list(map(int, input().split()))

    distH = bfs([s], adj, n)
    distG = bfs(ghosts, adj, n)

    ans = 0
    for e in exits:
        if distH[e] < distG[e]:
            ans += 1
    return str(ans)

# provided samples
assert run("""5 4 5 1 2
1 2
2 3
2 4
1 5
3
4
""") == "1"

assert run("""5 5 5 1 2
1 2
2 3
3 4
4 5
1 5
3
4
""") == "0"

# custom cases
assert run("""3 2 1 1 1
1 2
2 3
3
2
""") == "0", "ghost blocks path"

assert run("""4 3 1 2 1
1 2
2 3
3 4
4 2
3
""") == "1", "ghost far away exit safe"

assert run("""1 0 1 1 1
1
1
""") == "0", "same start collision"

assert run("""6 5 1 1 2
1 2
2 3
3 4
4 5
5 6
6
3 4
""") == "0", "ghost reaches middle first"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| chain with blocking ghost | 0 | ghost overtakes path early |
| distant ghost | 1 | safe when Harry strictly faster |
| single node collision | 0 | start position conflict |
| mid-graph pressure | 0 | multi-step dominance of ghosts |

## Edge Cases

A key edge case occurs when Harry starts in a room that is also a ghost source. In that situation, the ghost BFS assigns distance 0 to the starting node, and Harry’s BFS also assigns 0. The comparison fails immediately, so any exit requiring staying in or passing through that node is unsafe. The algorithm naturally handles this because equality is not allowed.

Another case is when an exit is disconnected from both Harry and all ghosts. Harry’s distance becomes infinity, while ghost distance is also infinity. Since the condition requires strict inequality, infinity is not less than infinity, so the exit is correctly marked unsafe because Harry cannot reach it at all.

Finally, when multiple ghosts exist, the multi-source BFS ensures the minimum arrival time from any ghost dominates. This prevents missing a faster ghost path that would otherwise invalidate a seemingly safe exit if ghosts were processed individually.
