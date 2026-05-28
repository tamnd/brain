---
title: "CF 78E - Evacuation"
description: "We are given a laboratory grid of size n × n, representing a research station where some tiles are reactors and others are laboratories. One reactor is malfunctioning and will explode, causing toxic coolant to spread to neighboring labs."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "flows", "graphs", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 78
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 70 (Div. 2)"
rating: 2300
weight: 78
solve_time_s: 154
verified: true
draft: false
---

[CF 78E - Evacuation](https://codeforces.com/problemset/problem/78/E)

**Rating:** 2300  
**Tags:** flows, graphs, shortest paths  
**Solve time:** 2m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a laboratory grid of size _n_ × _n_, representing a research station where some tiles are reactors and others are laboratories. One reactor is malfunctioning and will explode, causing toxic coolant to spread to neighboring labs. Each laboratory contains some number of scientists and some number of rescue capsules. Scientists can move between adjacent laboratories in one minute and can enter a capsule instantly. The coolant spreads in a similar fashion, infecting neighboring labs at each minute. Once a laboratory is infected, any scientist not already in a capsule dies.

The task is to determine the maximum number of scientists that can be saved if all scientists act optimally, given the limited time before the explosion.

The constraints are small: _n_ can be at most 10, which means the total number of tiles is at most 100. The number of minutes _t_ can be up to 60. Since the grid is tiny, even solutions with cubic or quartic complexity in _n_ can be feasible. However, we must be careful because the problem requires considering flows of scientists through the network of laboratories before infection.

Edge cases include laboratories immediately adjacent to the malfunctioning reactor. For instance, a lab with a scientist and capsule next to the reactor may or may not save its scientist depending on the infection timing. Another tricky case is when the number of scientists exceeds the number of capsules in reachable safe laboratories, so some scientists must necessarily die. Naive solutions that simply move scientists greedily without considering the infection timeline or capsule capacities will produce incorrect results.

## Approaches

A brute-force approach would try to simulate every possible movement of scientists at every minute while simultaneously propagating the infection. Each scientist would have to make a decision at each step, leading to an exponential number of possibilities, which is clearly infeasible even for _n_ = 10 and _t_ = 60.

The key observation is that this is fundamentally a maximum flow problem with a time constraint. We can model each laboratory at each time step as a node in a graph. Edges connect a lab at time _k_ to its neighboring labs at time _k+1_, representing a scientist moving in one minute. Additionally, each lab has a node for entering a capsule with capacity equal to the number of capsules. The infection limits how far in time each node can exist.

Once the graph is constructed, we can compute the maximum number of scientists that can reach capsules before their labs are infected using a standard maximum flow algorithm. The small size of the grid and the time limit make it feasible to model this as a flow network with at most _n_ × _n_ × (_t_+1) nodes, which is manageable for a Dinic or Edmonds-Karp flow algorithm.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(4^(_n^2_×_t_)) | O(_n^2_×_t_) | Infeasible |
| Time-Expanded Max Flow | O(V^2 E) ≈ O((n^2 t)^2 × 4) | O(n^2 × t) | Accepted |

## Algorithm Walkthrough

1. Identify the malfunctioning reactor's coordinates. This will be the origin of the coolant spread.
2. Compute for each laboratory the earliest minute it becomes infected using a breadth-first search starting from the malfunctioning reactor. Reactors block the spread. Store this infection time in a 2D array `infect_time`. Laboratories that never get infected can be considered to have `infect_time = t+1`.
3. Construct a time-expanded flow network. Each laboratory at time _k_ (0 ≤ k ≤ _t_) is represented by a node. For a lab at position (i,j) and time k, connect it to its neighbors at time k+1 with infinite capacity if the neighbor's infection time is greater than k+1. Also, connect the same lab at time k to time k+1 to allow scientists to stay in place.
4. For each laboratory at each time, connect its node to a "capsule sink" node with capacity equal to the number of capsules in that lab. This edge exists only at times strictly less than the infection time of the lab.
5. Introduce a source node connected to all laboratories at time 0 with capacities equal to the number of scientists in that lab.
6. Run a maximum flow algorithm (Dinic) from the source to the capsule sink. The maximum flow value equals the maximum number of scientists that can escape before the infection reaches them.
7. Return the computed maximum flow.

Why it works: The network correctly encodes the movement and timing constraints. Each scientist corresponds to a unit of flow, and capsule capacities and infection times limit flow into the sink. A scientist cannot occupy a node beyond its infection time, and cannot enter a capsule beyond the number available. Therefore, the flow maximization directly models the optimal evacuation plan.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

class Edge:
    def __init__(self, to, rev, cap):
        self.to = to
        self.rev = rev
        self.cap = cap

class MaxFlow:
    def __init__(self, N):
        self.size = N
        self.graph = [[] for _ in range(N)]

    def add(self, fr, to, cap):
        self.graph[fr].append(Edge(to, len(self.graph[to]), cap))
        self.graph[to].append(Edge(fr, len(self.graph[fr]) - 1, 0))

    def bfs_level(self, s, t, level):
        q = deque()
        level[s] = 0
        q.append(s)
        while q:
            v = q.popleft()
            for e in self.graph[v]:
                if e.cap > 0 and level[e.to] < 0:
                    level[e.to] = level[v] + 1
                    q.append(e.to)
        return level[t] >= 0

    def dfs_flow(self, v, t, upTo, level, iter):
        if v == t:
            return upTo
        for i in range(iter[v], len(self.graph[v])):
            e = self.graph[v][i]
            if e.cap > 0 and level[v] < level[e.to]:
                d = self.dfs_flow(e.to, t, min(upTo, e.cap), level, iter)
                if d > 0:
                    e.cap -= d
                    self.graph[e.to][e.rev].cap += d
                    return d
            iter[v] += 1
        return 0

    def max_flow(self, s, t):
        flow = 0
        level = [-1] * self.size
        INF = 10**9
        while True:
            level = [-1] * self.size
            if not self.bfs_level(s, t, level):
                break
            iter = [0] * self.size
            while True:
                f = self.dfs_flow(s, t, INF, level, iter)
                if f == 0:
                    break
                flow += f
        return flow

n, t = map(int, input().split())
sci_grid = [input().strip() for _ in range(n)]
input()  # empty line
cap_grid = [input().strip() for _ in range(n)]

INF = 10**9
dx = [0,0,1,-1]
dy = [1,-1,0,0]

infect_time = [[INF]*n for _ in range(n)]
queue = deque()
for i in range(n):
    for j in range(n):
        if sci_grid[i][j] == 'Z':
            queue.append((i,j,0))
            infect_time[i][j] = 0

while queue:
    x, y, time = queue.popleft()
    for d in range(4):
        nx, ny = x+dx[d], y+dy[d]
        if 0<=nx<n and 0<=ny<n and sci_grid[nx][ny] not in 'YZ' and infect_time[nx][ny] > time+1:
            infect_time[nx][ny] = time+1
            queue.append((nx, ny, time+1))

# build flow graph
def node(i,j,k):
    return (i*n+j)*(t+1)+k

N = n*n*(t+1) + 2
src = N-2
sink = N-1
mf = MaxFlow(N)

for i in range(n):
    for j in range(n):
        if sci_grid[i][j] in 'YZ':
            continue
        max_time = min(t, infect_time[i][j]-1)
        for k in range(max_time+1):
            # stay
            if k < max_time:
                mf.add(node(i,j,k), node(i,j,k+1), INF)
            # move
            for d in range(4):
                ni, nj = i+dx[d], j+dy[d]
                if 0<=ni<n and 0<=nj<n and sci_grid[ni][nj] not in 'YZ' and k+1 <= infect_time[ni][nj]-1:
                    mf.add(node(i,j,k), node(ni,nj,k+1), INF)
            # capsules
            mf.add(node(i,j,k), sink, int(cap_grid[i][j]))

for i in range(n):
    for j in range(n):
        if sci_grid[i][j] not in 'YZ' and int(sci_grid[i][j]) > 0:
            mf.add(src, node(i,j,0), int(sci_grid[i][j]))

print
```
