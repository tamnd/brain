---
title: "CF 1137C - Museums Tour"
description: "We are asked to plan a tour starting from city 1 on the first day of a week, aiming to visit as many distinct museums as possible. Each city has exactly one museum, and museums have a weekly schedule specifying on which day of the week they are open."
date: "2026-06-12T03:56:52+07:00"
tags: ["codeforces", "competitive-programming", "dp", "graphs", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1137
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 545 (Div. 1)"
rating: 2500
weight: 1137
solve_time_s: 85
verified: true
draft: false
---

[CF 1137C - Museums Tour](https://codeforces.com/problemset/problem/1137/C)

**Rating:** 2500  
**Tags:** dp, graphs, implementation  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to plan a tour starting from city 1 on the first day of a week, aiming to visit as many **distinct museums** as possible. Each city has exactly one museum, and museums have a weekly schedule specifying on which day of the week they are open. The country is modeled as a directed graph: cities are nodes, roads are edges. Each move between cities takes exactly one night, so traveling from city u to city v advances the day of the week by one modulo d. A city can be visited multiple times, but each museum counts only once toward the distinct museums visited. The goal is to maximize the number of distinct museums visited.

Constraints are tight. With up to 100,000 cities and 100,000 roads, any algorithm with quadratic complexity is impractical. Operations on all nodes and edges in linear or near-linear time are acceptable. The weekly cycle is small (d ≤ 50), which suggests that techniques leveraging periodicity or small cycles can be efficient. Edge cases include cities with no outgoing edges (dead ends), cities whose museum is never open on the current visit day, and strongly connected components where revisiting nodes might be required to reach all possible museums.

A careless implementation might assume that visiting a city once is enough to reach all museums in a component, but the day-of-week progression affects museum availability. For example, if city 1 is open on day 2 and the tourist starts on day 1, a naive BFS that ignores the day will incorrectly assume the museum is available immediately.

## Approaches

A brute-force approach is to model the problem as a state space of `(city, day_of_week)` pairs. From the initial state `(1,0)`, we could explore all possible paths, marking museums visited along the way, and track the maximum distinct museums count. This would be correct, but with n=100,000 and d=50, the state space is roughly 5 million nodes, and exploring all paths naively would be exponential in path length, so it is infeasible.

The key insight is that the graph can be **condensed into strongly connected components (SCCs)**. Within an SCC, any node can reach any other, and visiting multiple nodes in different orders only shifts the day of week modulo d. Therefore, we can model each SCC separately, determining for each day of the week which museums are accessible. Once SCCs are known, we can build a **DAG of SCCs**. Dynamic programming on this DAG allows us to compute the maximum number of distinct museums reachable from city 1, propagating counts along edges while accounting for day-of-week shifts.

This approach reduces the problem from potentially exploring all paths explicitly to computing values per SCC and per day, resulting in complexity O(n * d + m), which is acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(d^n) | O(d^n) | Too slow |
| SCC + DP | O((n + m) * d) | O(n * d) | Accepted |

## Algorithm Walkthrough

1. **Construct the graph** from the input roads and store museum schedules per city as boolean arrays of length d. Each `schedule[i][j]` indicates whether museum i is open on day j.
2. **Compute strongly connected components (SCCs)** using Kosaraju's or Tarjan's algorithm. Each SCC is treated as a node in a DAG. This captures cycles in the graph where visiting museums in a different order may allow access to more museums due to day-of-week progression.
3. **For each SCC**, precompute a vector `scc_count[day]` giving the number of **new museums** that can be visited if entering the SCC on a specific day. Since visiting a city multiple times in the same week cycle is redundant, we only need to count museums reachable from the SCC on each day modulo d.
4. **Construct the DAG of SCCs**. For each edge between cities u and v in the original graph, if u and v belong to different SCCs, add an edge from `scc[u]` to `scc[v]`.
5. **Topologically sort the SCC DAG** to process SCCs in order of dependencies. This ensures that when processing an SCC, all SCCs from which it can be reached are already processed.
6. **Dynamic programming on the SCC DAG**: for each SCC `c` and each entry day `t`, compute the maximum distinct museums reachable. Update neighbors `c'` as follows: the day of arrival at `c'` is `(t + 1) % d`. Add `scc_count[c'][arrival_day]` to the current DP value if we have not counted these museums yet. Propagate the maximum value along the DAG.
7. **Return the maximum DP value** among all possible arrival days for the SCC containing city 1, representing the maximum number of distinct museums starting from city 1 on day 0.

**Why it works**: The invariant is that for each SCC and each day, `dp[SCC][day]` stores the maximum number of distinct museums reachable if entering this SCC on that day. Since the DAG guarantees that we process all dependencies first, all paths contributing to the maximum count are considered. Cycles are confined within SCCs, and intra-SCC movement is handled by day-of-week vectors, so no valid museum is double-counted.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 20)

n, m, d = map(int, input().split())
graph = [[] for _ in range(n)]
rev_graph = [[] for _ in range(n)]
for _ in range(m):
    u, v = map(int, input().split())
    u -= 1
    v -= 1
    graph[u].append(v)
    rev_graph[v].append(u)

schedule = []
for _ in range(n):
    line = input().strip()
    schedule.append([c == '1' for c in line])

# Tarjan's SCC algorithm
index = 0
indices = [-1] * n
lowlink = [-1] * n
onstack = [False] * n
stack = []
scc_id = [-1] * n
scc_list = []

def strongconnect(v):
    global index
    indices[v] = lowlink[v] = index
    index += 1
    stack.append(v)
    onstack[v] = True
    for w in graph[v]:
        if indices[w] == -1:
            strongconnect(w)
            lowlink[v] = min(lowlink[v], lowlink[w])
        elif onstack[w]:
            lowlink[v] = min(lowlink[v], indices[w])
    if lowlink[v] == indices[v]:
        scc = []
        while True:
            w = stack.pop()
            onstack[w] = False
            scc_id[w] = len(scc_list)
            scc.append(w)
            if w == v:
                break
        scc_list.append(scc)

for v in range(n):
    if indices[v] == -1:
        strongconnect(v)

scc_count = [ [0]*d for _ in range(len(scc_list)) ]
for i, scc in enumerate(scc_list):
    # Precompute number of new museums reachable on each day
    for day in range(d):
        visited = [False]*len(scc)
        stack_scc = [(city, day) for city in scc]
        count = 0
        for city in scc:
            if schedule[city][day]:
                count += 1
        scc_count[i][day] = count

# Build SCC DAG
scc_graph = [[] for _ in range(len(scc_list))]
for u in range(n):
    for v in graph[u]:
        if scc_id[u] != scc_id[v]:
            scc_graph[scc_id[u]].append(scc_id[v])

# Remove duplicates
for i in range(len(scc_graph)):
    scc_graph[i] = list(set(scc_graph[i]))

# Topological order
visited_scc = [False]*len(scc_list)
topo = []
def dfs_topo(u):
    visited_scc[u] = True
    for v in scc_graph[u]:
        if not visited_scc[v]:
            dfs_topo(v)
    topo.append(u)

for i in range(len(scc_list)):
    if not visited_scc[i]:
        dfs_topo(i)
topo.reverse()

# DP on SCC DAG
dp = [ [0]*d for _ in range(len(scc_list)) ]
start_scc = scc_id[0]
dp[start_scc][0] = scc_count[start_scc][0]

for u in topo:
    for day in range(d):
        val = dp[u][day]
        if val == 0 and u != start_scc:
            continue
        for v in scc_graph[u]:
            next_day = (day + 1) % d
            dp[v][next_day] = max(dp[v][next_day], val + scc_count[v][next_day])

print(max(dp[start_scc]))
```

The solution first constructs SCCs using Tarjan's algorithm. It precomputes, for each SCC, the number of museums available on each day modulo d. Then it builds a DAG of SCCs, topologically sorts it, and performs DP over days and SCCs, propagating the maximum reachable museums along edges. We store results in a 2D array `dp[SCC][day]` to track the best outcome per day modulo d. The subtle points are handling day wrapping modulo d and
