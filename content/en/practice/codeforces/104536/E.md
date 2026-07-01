---
title: "CF 104536E - LIS Maximization"
description: "The failure is not coming from the tree logic itself but from the testing harness behavior in the provided solution. The key symptom is this line: and the fact that the output is an empty string inside the test runner rather than the computed value."
date: "2026-06-30T09:43:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104536
codeforces_index: "E"
codeforces_contest_name: "SashaT9 Contest 1"
rating: 0
weight: 104536
solve_time_s: 198
verified: false
draft: false
---

[CF 104536E - LIS Maximization](https://codeforces.com/problemset/problem/104536/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 18s  
**Verified:** no  

## Solution
## Diagnosis

The failure is not coming from the tree logic itself but from the testing harness behavior in the provided solution.

The key symptom is this line:

```
AssertionError
```

and the fact that the output is an empty string inside the test runner rather than the computed value.

This happens because the previous “solution” defined:

```
return ""
```

inside the `run()` helper instead of actually calling the solver logic. So the test is not evaluating the algorithm at all. It is silently returning an empty string, which obviously fails against `"5"`.

Separately, even if that were fixed, there is a second correctness issue in the radius computation:

The formula used was:

```
radius = min(max(dist_u[i], dist_v[i]))
```

This is valid for diameter endpoints but only after ensuring `dist_u` and `dist_v` correspond to true opposite endpoints of the diameter. That part is fine.

However, the real robustness issue is structural: the implementation assumes nodes are 1-indexed up to `len(adj)-1`, which breaks if adjacency size is reused incorrectly or if input parsing is mishandled.

But the immediate crash is purely due to the missing call.

## Correct Solution Idea

We must:

1. Build both trees.
2. Run BFS twice per tree to get diameter endpoints.
3. Compute radius using distances from both endpoints.
4. Combine using:

```
answer = max(d1, d2, r1 + r2 + 1)
```

No test harness logic should interfere with execution.

## Correct Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

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

def tree_info(adj):
    u, _ = bfs(1, adj)
    v, dist_u = bfs(u, adj)
    _, dist_v = bfs(v, adj)

    diameter = dist_u[v]

    radius = 10**18
    for i in range(1, len(adj)):
        radius = min(radius, max(dist_u[i], dist_v[i]))

    return diameter, radius

def solve():
    n = int(input())
    adj1 = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        adj1[u].append(v)
        adj1[v].append(u)

    m = int(input())
    adj2 = [[] for _ in range(m + 1)]
    for _ in range(m - 1):
        u, v = map(int, input().split())
        adj2[u].append(v)
        adj2[v].append(u)

    d1, r1 = tree_info(adj1)
    d2, r2 = tree_info(adj2)

    print(max(d1, d2, r1 + r2 + 1))

if __name__ == "__main__":
    solve()
```
## What was actually wrong

The original failure was not algorithmic. The regression came from mixing “unit-test wrapper code” with the actual solution:

The function used for testing returned an empty string instead of invoking the solver, so every assertion failed regardless of correctness.

Once that is removed, the BFS-diameter + radius-combination approach is fully consistent with the problem constraints and runs in linear time per tree.

If you want, I can also show a cleaner pattern for competitive programming where the solver is isolated from any test harness so this class of bug cannot happen again.
