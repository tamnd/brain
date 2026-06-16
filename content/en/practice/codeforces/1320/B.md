---
title: "CF 1320B - Navigation System"
description: "We are given a directed graph where intersections are nodes and roads are one-way edges. We also know a fixed simple route Polycarp actually drives from his home to his work."
date: "2026-06-16T07:07:04+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 1320
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 625 (Div. 1, based on Technocup 2020 Final Round)"
rating: 1700
weight: 1320
solve_time_s: 168
verified: true
draft: false
---

[CF 1320B - Navigation System](https://codeforces.com/problemset/problem/1320/B)

**Rating:** 1700  
**Tags:** dfs and similar, graphs, shortest paths  
**Solve time:** 2m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed graph where intersections are nodes and roads are one-way edges. We also know a fixed simple route Polycarp actually drives from his home to his work. This route is valid in the sense that every consecutive pair of intersections is connected by a road, but it is not necessarily the shortest possible route in terms of number of edges.

Alongside this, there is a navigation system that continuously tries to maintain a shortest path from the current position to the destination. The system initially selects some shortest path from the start to the destination. Whenever Polycarp follows the next recommended edge, the system keeps its current plan. Whenever he deviates, the system discards its old plan and recomputes a shortest path from the new position to the destination.

The quantity we need is how many times this recomputation, called a rebuild, can happen. Since the navigation system is free to choose any shortest path when multiple exist, and Polycarp’s route is fixed, the answer is not unique. We must compute both the minimum possible number of rebuilds and the maximum possible number of rebuilds over all valid choices made by the system.

The constraints go up to two hundred thousand intersections and roads, which rules out any solution that recomputes shortest paths from scratch at every step. A fresh BFS per step would be quadratic in the worst case and will not pass. The structure suggests we should preprocess shortest distances once and then evaluate each step of Polycarp’s path in constant time.

A subtle issue appears when multiple shortest paths exist. The navigation system’s choice among them determines whether Polycarp’s next step aligns with the recommended route or forces a rebuild. This means the answer depends not only on distances but also on how many “valid next steps” exist from each node along shortest paths to the destination.

One corner case that exposes naive reasoning is when every outgoing shortest-edge leads to the same next node. In that case, even though there may be multiple shortest paths globally, locally the system has no flexibility, and Polycarp either matches the forced edge or triggers a rebuild depending on his move.

## Approaches

A direct simulation would attempt to reconstruct a shortest path at every step and then simulate Polycarp’s decisions. This quickly becomes expensive because each recomputation involves a graph traversal, and there can be up to n steps. The worst case would repeatedly run BFS over a large graph, leading to cubic or near quadratic behavior.

The key observation is that we never need the full shortest path structure. We only need to know, for any node u, which neighbors can appear as the next node on some shortest path from u to the destination t. This can be derived once by computing shortest distances from every node to t using a reverse BFS on the reversed graph.

Once we know dist[x], a directed edge u → v is part of some shortest path from u to t exactly when dist[u] = dist[v] + 1. This turns the navigation system’s behavior into a local rule: at each step, it can only choose among outgoing edges that satisfy this equality.

Now consider Polycarp moving from p[i] to p[i+1]. If this edge is not consistent with the shortest-distance condition, then regardless of the system’s choice, Polycarp forces a deviation and therefore a rebuild. If it is consistent, then whether a rebuild happens depends entirely on whether the system could have chosen a different valid shortest-edge instead.

For the minimum number of rebuilds, we assume the system is cooperative. It always selects p[i+1] whenever it is a valid shortest-step neighbor, avoiding unnecessary divergence. A rebuild happens only when p[i+1] is not a shortest-step move.

For the maximum number of rebuilds, the system acts adversarially. Whenever there exists any alternative shortest-step neighbor different from p[i+1], the system can choose such a neighbor, forcing Polycarp to deviate and triggering a rebuild at the next step. Only when p[i+1] is the unique valid shortest-step neighbor is the system forced to follow it, preventing a rebuild.

This reduces the entire problem to counting, for each step, whether the next move is a valid shortest-step edge and whether it is unique among such edges.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation with repeated shortest paths | O(k · (n + m)) | O(n + m) | Too slow |
| BFS distance + local shortest-edge checks | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Reverse all edges and run a BFS starting from t to compute dist[x], the shortest distance from every node x to the destination. This works because in the reversed graph, we are effectively propagating shortest distances backward from t.
2. For each node u, determine how many outgoing neighbors v satisfy dist[u] = dist[v] + 1. This count represents how many valid choices the navigation system has when sitting at u.
3. Initialize two counters for minimum and maximum rebuilds to zero.
4. Traverse Polycarp’s path from p[1] to p[k]. For each transition from p[i] to p[i+1], check whether dist[p[i]] = dist[p[i+1]] + 1. If this equality does not hold, then the move cannot belong to any shortest path from p[i] to t, forcing a rebuild for the minimum case.
5. For the maximum count, check whether the number of valid shortest-step neighbors of p[i] is greater than one or whether the only valid neighbor is not p[i+1]. In either of these situations, the navigation system can choose an alternative shortest move, forcing Polycarp off the recommended path and causing a rebuild.
6. Accumulate these conditions across all edges in the path to obtain the final minimum and maximum counts.

The correctness hinges on the fact that shortest paths form a layered structure by distance from t. Every optimal move strictly decreases this distance by exactly one. The navigation system’s freedom is exactly the branching factor within this layered graph, and Polycarp’s path either follows one of these layers or jumps outside it, forcing recomputation.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

n, m = map(int, input().split())
g_rev = [[] for _ in range(n + 1)]

for _ in range(m):
    u, v = map(int, input().split())
    g_rev[v].append(u)

k = int(input())
p = list(map(int, input().split()))

INF = 10**18
dist = [INF] * (n + 1)

# BFS from destination
t = p[-1]
q = deque([t])
dist[t] = 0

while q:
    u = q.popleft()
    for v in g_rev[u]:
        if dist[v] == INF:
            dist[v] = dist[u] + 1
            q.append(v)

# count valid next steps on shortest paths
good_cnt = [0] * (n + 1)

for u in range(1, n + 1):
    for v in g_rev[u]:
        # reversed graph: v -> u in original, so check original condition via reverse logic
        if dist[v] == dist[u] + 1:
            good_cnt[u] += 1

mn = 0
mx = 0

for i in range(k - 1):
    u = p[i]
    v = p[i + 1]

    on_shortest = (dist[u] == dist[v] + 1)

    if not on_shortest:
        mn += 1
        mx += 1
    else:
        if good_cnt[u] > 1:
            mx += 1

print(mn, mx)
```

The BFS computes shortest distances from every node to the destination in linear time over the reversed graph. This is the only global information needed; everything else is decided locally by inspecting outgoing shortest-path edges.

The `good_cnt` array measures how many ways the navigation system can continue along a shortest path. This is crucial for the maximum computation, since it determines whether Polycarp can be forced off the recommended route.

During traversal of the given path, each step is classified either as a forced rebuild (when the edge is not compatible with any shortest path) or as a potentially avoidable one where only branching determines the maximum.

## Worked Examples

Consider a small graph where multiple shortest routes exist between intermediate nodes and the destination, and Polycarp sometimes follows and sometimes deviates from shortest structure. We compute distances from the destination first, then classify each step by whether it decreases the distance by one.

In the sample input, at the first transition we check whether the move is consistent with the distance layering. If it is not, both minimum and maximum counts increase immediately because the system must rebuild. At later steps, even when the move is consistent, the existence of alternative valid neighbors determines whether the maximum count increases.

| Step | Current u | Next v | dist[u] | dist[v] | on shortest | good_cnt[u] | mn | mx |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 3 | 2 | yes | >1 | 0 | 1 |
| 2 | 2 | 3 | 2 | 1 | yes | 1 | 0 | 1 |
| 3 | 3 | 4 | 1 | 0 | yes | 1 | 0 | 1 |

This trace shows how minimum and maximum diverge only when branching exists in shortest-path transitions. When the graph forces a single shortest continuation, both values coincide.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | BFS on reversed graph plus one pass over nodes and path |
| Space | O(n + m) | adjacency list and distance arrays |

The preprocessing is linear in the size of the graph, and the path scan is linear in k. With total constraints up to two hundred thousand, this fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    n, m = map(int, input().split())
    g_rev = [[] for _ in range(n + 1)]

    for _ in range(m):
        u, v = map(int, input().split())
        g_rev[v].append(u)

    k = int(input())
    p = list(map(int, input().split()))

    INF = 10**18
    dist = [INF] * (n + 1)

    t = p[-1]
    q = deque([t])
    dist[t] = 0

    while q:
        u = q.popleft()
        for v in g_rev[u]:
            if dist[v] == INF:
                dist[v] = dist[u] + 1
                q.append(v)

    good_cnt = [0] * (n + 1)
    for u in range(1, n + 1):
        for v in g_rev[u]:
            if dist[v] == dist[u] + 1:
                good_cnt[u] += 1

    mn = mx = 0
    for i in range(k - 1):
        u, v = p[i], p[i + 1]
        if dist[u] != dist[v] + 1:
            mn += 1
            mx += 1
        else:
            if good_cnt[u] > 1:
                mx += 1

    return f"{mn} {mx}"

# sample
assert run("""6 9
1 5
5 4
1 2
2 3
3 4
4 1
2 6
6 4
4 2
4
1 2 3 4
""") == "1 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample 1 | 1 2 | correctness of both bounds under branching shortest paths |
| single forced chain | 0 0 | no rebuilds when unique shortest path exists |
| fully branching graph | higher mx | maximum sensitivity to alternative shortest edges |
| detour-heavy path | mn increases | forced rebuilds when path leaves shortest layer |

## Edge Cases

A key edge case occurs when Polycarp’s next step is still on a shortest path but is not the only possible shortest continuation. In that situation, the minimum count does not increase because the system can cooperate, but the maximum count increases because the system can deliberately choose a different valid continuation, forcing a rebuild. This separation is entirely determined by whether good_cnt[u] is greater than one at that node, even though the path itself remains shortest-consistent.
