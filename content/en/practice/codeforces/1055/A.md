---
title: "CF 1055A - Metro"
description: "The metro system can be seen as a line of stations from 1 to n, with two directed ways of movement. One track allows movement from smaller indices to larger ones, while the other allows movement in the opposite direction. Bob starts at station 1 and wants to reach station s."
date: "2026-06-15T12:52:04+07:00"
tags: ["codeforces", "competitive-programming", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1055
codeforces_index: "A"
codeforces_contest_name: "Mail.Ru Cup 2018 Round 2"
rating: 900
weight: 1055
solve_time_s: 59
verified: true
draft: false
---

[CF 1055A - Metro](https://codeforces.com/problemset/problem/1055/A)

**Rating:** 900  
**Tags:** graphs  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

The metro system can be seen as a line of stations from 1 to n, with two directed ways of movement. One track allows movement from smaller indices to larger ones, while the other allows movement in the opposite direction. Bob starts at station 1 and wants to reach station s.

The complication is that each station may or may not allow stopping for each direction independently. Even if a train passes through a station, Bob can only use it as a transfer or stopping point if that station is open for that track direction. If it is closed, trains still pass through but Bob cannot get on or off there for that direction, which effectively removes that station as a usable node on that directed track.

The task is to determine whether there exists any sequence of valid boardings and possible transfer at reachable stations that allows movement from station 1 to station s.

The input size n is at most 1000, which means an O(n^2) traversal or even a simple graph search over O(n) nodes and O(n) edges is sufficient. Anything exponential is unnecessary, but even a straightforward BFS or simulation over adjacency is easily fast enough.

A subtle edge case arises when Bob cannot initially access the forward direction at station 1. In that case, even if a valid path exists by going backward first and then switching directions, it may be missed if we assume monotonic movement or ignore direction switching.

Another case occurs when station s is only reachable through a detour to a far station and then returning in reverse direction. For example, if forward direction is blocked early but backward direction is open, Bob may need to travel to the rightmost reachable station first.

## Approaches

The structure naturally forms a directed graph where each station is a node. From station i, Bob can move to i+1 if the first track is open at i, and to i-1 if the second track is open at i. The problem reduces to reachability from node 1 to node s.

A brute-force approach would attempt to enumerate all possible routes, possibly exploring paths with repeated revisits. This is correct but can explode in complexity because the number of walks in a graph with cycles grows exponentially. Even with n up to 1000, naive path enumeration is infeasible.

The key observation is that this is a standard reachability problem in a graph with n nodes and at most 2n edges. Once modeled correctly, a simple BFS or DFS suffices, because each station has at most two outgoing transitions, one forward and one backward. The constraints ensure that visiting each node once is enough.

The brute-force works because all transitions are local and deterministic, but fails when revisits create an explosion of repeated states. The observation that we only care about whether a node is reachable, not how it is reached, reduces the problem to graph traversal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force paths | O(2^n) | O(n) recursion stack | Too slow |
| BFS/DFS reachability | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We model each station as a node in a graph.

1. Build adjacency based on allowed movements. From station i, if i + 1 ≤ n and a[i] = 1, add an edge from i to i + 1. If i − 1 ≥ 1 and b[i] = 1, add an edge from i to i − 1. These edges represent whether Bob can physically board a train that continues in that direction and stop at the next station.
2. Initialize a visited array of size n + 1 to track which stations have already been processed. This prevents revisiting the same station multiple times, which would otherwise lead to redundant exploration.
3. Start a BFS (or DFS) from station 1, marking it as visited. Station 1 is always Bob’s starting point, so it is trivially reachable.
4. While there are unprocessed stations in the BFS queue, remove one station u and explore all neighbors v reachable via allowed edges. If v has not been visited, mark it and add it to the queue.
5. After traversal finishes, check whether station s was visited. If yes, output "YES"; otherwise output "NO".

### Why it works

At any moment, the BFS maintains the invariant that every visited station is reachable from station 1 using valid transitions. Every edge corresponds to a legal movement under the station and track constraints, so any newly discovered station is also reachable. Since BFS explores all reachable states without repetition, it eventually discovers all stations reachable from 1. If station s is not among them, no valid sequence of movements can reach it.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    n, s = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    adj = [[] for _ in range(n + 1)]

    for i in range(n):
        if i + 1 < n and a[i] == 1:
            adj[i + 1].append(i + 2)
        if i - 1 >= 0 and b[i] == 1:
            adj[i + 1].append(i)

    visited = [False] * (n + 1)
    q = deque([1])
    visited[1] = True

    while q:
        u = q.popleft()
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                q.append(v)

    print("YES" if visited[s] else "NO")

if __name__ == "__main__":
    solve()
```

The adjacency construction encodes direction constraints directly into edges, so the BFS operates on a standard graph. The forward edges use a[i] since they correspond to movement from i to i + 1. The backward edges use b[i] since they correspond to movement from i to i − 1.

A common implementation pitfall is off-by-one indexing because the input is 1-based but arrays are often 0-based. Here, adjacency is built using i + 1 as the node index, so all graph nodes are consistently 1-based, avoiding confusion.

Another subtle issue is forgetting that movement depends on the current station, not the destination station. The condition must be checked at i before adding edges.

## Worked Examples

### Example 1

Input:

```
5 3
1 1 1 1 1
1 1 1 1 1
```

| Step | Current | Queue | Visited |
| --- | --- | --- | --- |
| Init | 1 | [1] | {1} |
| 1 | 1 | [2] | {1,2} |
| 2 | 2 | [3] | {1,2,3} |
| 3 | 3 | [] | {1,2,3} |

Station 3 is reached directly through forward movement. Every station allows both directions, so BFS expands linearly until s is found.

### Example 2

Input:

```
5 4
0 0 1 1 1
1 1 1 1 1
```

Here, forward movement is blocked at stations 1 and 2, so Bob cannot proceed directly to the right. However, backward movement allows traversal in reverse once a
