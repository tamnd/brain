---
title: "CF 104442I - C\u00e1lculo num\u00e9rico"
description: "We are given several independent scenarios on a 2D integer plane. In each scenario, a robot starts at a coordinate $I = (x1, y1)$ and must reach a target coordinate $F = (x2, y2)$."
date: "2026-06-30T18:07:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104442
codeforces_index: "I"
codeforces_contest_name: "AdaByron Regional Madrid 2023"
rating: 0
weight: 104442
solve_time_s: 57
verified: true
draft: false
---

[CF 104442I - C\u00e1lculo num\u00e9rico](https://codeforces.com/problemset/problem/104442/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent scenarios on a 2D integer plane. In each scenario, a robot starts at a coordinate $I = (x_1, y_1)$ and must reach a target coordinate $F = (x_2, y_2)$. The robot moves on integer grid points, but the plane is otherwise unbounded, meaning it is not restricted to the initial coordinate range.

Some grid points are forbidden. If a coordinate is listed as an obstacle, the robot is not allowed to stand on it. It may move freely through all other integer coordinates.

Movement happens between neighboring grid points. The cost depends on the type of move: some moves cost 8 and others cost 16. If no valid path exists from start to finish without stepping on forbidden points, the answer is $-1$. Otherwise we must compute the minimum possible total cost.

The key interpretation is that we are solving a shortest path problem on an implicit infinite graph where vertices are all integer coordinates except blocked ones, and edges connect geometric neighbors with two possible weights.

The constraints on coordinates are small, between $-50$ and $50$, and there are at most 100 obstacles per test case. However, the robot is allowed to leave this box, so the graph is not explicitly bounded. This immediately rules out any approach that tries to build the entire grid or perform dense DP over a large rectangle, since the reachable area is unbounded in principle.

The most dangerous edge case is when obstacles form a tight barrier that forces detours outside the initial bounding box. For example, if start is at $(0,0)$, end at $(2,0)$, and all points $(1,y)$ for $y \in [-50,50]$ are blocked, a naive BFS restricted to the bounding rectangle would incorrectly conclude unreachable or miss the true detour that goes around the barrier at $y=51$.

Another subtle case is when start or end is adjacent to many obstacles. A greedy or heuristic-based approach that tries to “step closer” can get trapped in local minima, because the cheapest immediate move may lead into a dead region surrounded by blocked nodes.

## Approaches

A brute-force idea is to treat every integer coordinate as a node and run BFS or Dijkstra over the infinite grid. From each node, we would attempt all 8 possible moves, skipping obstacles. This is correct because it directly models the graph, but it is impossible to execute as stated since the number of nodes is infinite.

The key observation is that although the grid is infinite, the only relevant “holes” are the obstacle points, and there are very few of them. The shortest path in a grid with unit structure does not benefit from wandering arbitrarily far away, because movement cost grows with distance and there is no reward for exploring empty space. Any optimal path can be assumed to stay inside a bounding box that contains the start, end, and all obstacles, possibly expanded by a small margin to allow detours around boundary-adjacent obstacles.

This reduces the problem to a finite shortest path problem. We restrict ourselves to a grid covering all points from $\min(x)$ to $\max(x)$, similarly for $y$, extended by 1 in each direction. On this finite set of nodes, we run Dijkstra since edges have two different weights.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Infinite BFS over $\mathbb{Z}^2$ | O(infinite) | O(infinite) | Not feasible |
| Bounded grid + Dijkstra | $O(HW \log(HW))$ | $O(HW)$ | Accepted |

## Algorithm Walkthrough

We treat the grid as a weighted graph whose nodes are integer coordinates inside a carefully chosen bounding rectangle.

1. We read start, end, and obstacle coordinates, and collect all x and y values. From these we compute the minimum and maximum x and y. We expand this range by 1 unit in all directions. The expansion ensures we can route around obstacles that lie exactly on the boundary of the useful region.
2. We build a set of blocked coordinates for O(1) membership checks. This is essential because obstacle lookup happens during every relaxation step.
3. We run Dijkstra’s algorithm starting from the initial coordinate. We maintain a priority queue of states $(cost, x, y)$.
4. From each popped state, we try moving in all 8 directions. Each move leads to a neighbor coordinate. If that coordinate is outside the bounding box or is blocked, we discard it.
5. Each valid move has a fixed cost depending on direction type. Straight moves cost 8 and diagonal moves cost 16. We relax the neighbor if we found a cheaper path.
6. We stop early once we reach the target coordinate, because Dijkstra guarantees this is the minimum possible cost at that moment.
7. If the target is never reached, we output $-1$.

The reason this works is that any optimal path can be embedded in the finite bounding box. Outside this region, any detour can be projected back without increasing cost because movement costs are uniform and depend only on step type, not on absolute position. Thus restricting the graph does not remove optimal solutions.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

INF = 10**18

# 8 directions: (dx, dy, cost)
dirs = [
    (1, 0, 8), (-1, 0, 8), (0, 1, 8), (0, -1, 8),
    (1, 1, 16), (1, -1, 16), (-1, 1, 16), (-1, -1, 16)
]

P = int(input())
for _ in range(P):
    x1, y1 = map(int, input().split())
    x2, y2 = map(int, input().split())

    n = int(input())
    blocked = set()

    xs = [x1, x2]
    ys = [y1, y2]

    for _ in range(n):
        x, y = map(int, input().split())
        blocked.add((x, y))
        xs.append(x)
        ys.append(y)

    minx, maxx = min(xs) - 1, max(xs) + 1
    miny, maxy = min(ys) - 1, max(ys) + 1

    def inside(x, y):
        return minx <= x <= maxx and miny <= y <= maxy

    dist = {}
    pq = []

    start = (x1, y1)
    if start in blocked:
        print(-1)
        continue

    dist[start] = 0
    heapq.heappush(pq, (0, x1, y1))

    ans = -1

    while pq:
        d, x, y = heapq.heappop(pq)

        if d != dist.get((x, y), INF):
            continue

        if (x, y) == (x2, y2):
            ans = d
            break

        for dx, dy, w in dirs:
            nx, ny = x + dx, y + dy
            if not inside(nx, ny):
                continue
            if (nx, ny) in blocked:
                continue

            nd = d + w
            if nd < dist.get((nx, ny), INF):
                dist[(nx, ny)] = nd
                heapq.heappush(pq, (nd, nx, ny))

    print(ans)
```

The implementation relies on Dijkstra because edge weights are not uniform. The priority queue ensures that whenever we finalize a node, we already have its optimal cost.

The bounding box restriction is what makes the infinite grid manageable. Without it, the algorithm would never terminate.

## Worked Examples

Consider a simple case where start is $(0,0)$, end is $(1,1)$, and there are no obstacles.

We compare two possible paths: diagonal directly, or two straight moves.

| Step | Position | Cost | Action |
| --- | --- | --- | --- |
| 1 | (0,0) | 0 | start |
| 2 | (1,1) | 16 | diagonal move |

The algorithm chooses the diagonal immediately since it is the shortest path.

Now consider a case where the diagonal is blocked: start $(0,0)$, end $(1,1)$, obstacle at $(1,1)$ is invalid so we adjust example: obstacle at $(1,0)$.

| Step | Position | Cost | Action |
| --- | --- | --- | --- |
| 1 | (0,0) | 0 | start |
| 2 | (0,1) | 8 | up |
| 3 | (1,1) | 16 | right |

This shows how the algorithm naturally routes around blocked cells and accumulates cost through alternative paths.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(K \log K)$ | Dijkstra over at most $K = (dx \cdot dy)$ bounded grid points |
| Space | $O(K)$ | Distance map and priority queue storage |

The bounding box is small because coordinates are limited to around 100 in each direction, so the effective grid is at most about $200 \times 200$, making the solution easily fast under the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    INF = 10**18
    dirs = [
        (1, 0, 8), (-1, 0, 8), (0, 1, 8), (0, -1, 8),
        (1, 1, 16), (1, -1, 16), (-1, 1, 16), (-1, -1, 16)
    ]

    P = int(input())
    out = []

    for _ in range(P):
        x1, y1 = map(int, input().split())
        x2, y2 = map(int, input().split())
        n = int(input())

        blocked = set()
        xs = [x1, x2]
        ys = [y1, y2]

        for _ in range(n):
            x, y = map(int, input().split())
            blocked.add((x, y))
            xs.append(x)
            ys.append(y)

        minx, maxx = min(xs) - 1, max(xs) + 1
        miny, maxy = min(ys) - 1, max(ys) + 1

        def inside(x, y):
            return minx <= x <= maxx and miny <= y <= maxy

        if (x1, y1) in blocked:
            out.append("-1")
            continue

        dist = {}
        import heapq
        pq = [(0, x1, y1)]
        dist[(x1, y1)] = 0
        ans = -1

        while pq:
            d, x, y = heapq.heappop(pq)
            if d != dist.get((x, y), INF):
                continue
            if (x, y) == (x2, y2):
                ans = d
                break
            for dx, dy, w in dirs:
                nx, ny = x + dx, y + dy
                if not inside(nx, ny): 
                    continue
                if (nx, ny) in blocked:
                    continue
                nd = d + w
                if nd < dist.get((nx, ny), INF):
                    dist[(nx, ny)] = nd
                    heapq.heappush(pq, (nd, nx, ny))

        out.append(str(ans))

    return "\n".join(out)

# custom cases
assert run("1\n0 0\n1 1\n0") == "16"
assert run("1\n0 0\n2 0\n1\n1 0") == "32"
assert run("1\n0 0\n0 0\n0") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| direct diagonal | 16 | diagonal cost correctness |
| blocked middle | 32 | detour handling |
| same start/end | 0 | zero-length path |

## Edge Cases

A key edge case is when the shortest path requires moving outside the immediate rectangle defined by start, end, and obstacles. The algorithm handles this because the bounding box is expanded by one unit, allowing a minimal detour corridor around tight obstacle formations.

Another case is when the start or end is surrounded on most sides. For example, if $(x_1, y_1)$ has all adjacent nodes blocked except one diagonal escape, Dijkstra still explores that remaining valid edge because it considers all 8 directions uniformly and does not rely on greedy progression.

A final edge case is when start equals end. The algorithm correctly initializes distance to zero and immediately returns without entering the expansion loop, since the first extracted node already matches the target.
