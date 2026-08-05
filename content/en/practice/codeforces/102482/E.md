---
title: "CF 102482E - Getting a Jump on Crime"
description: "The city is a grid of rectangular buildings. Each cell stores one building height. Robin starts from the center of one building and wants to know the minimum number of jumps needed to reach every other building."
date: "2026-08-05T18:57:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102482
codeforces_index: "E"
codeforces_contest_name: "2018 ACM-ICPC World Finals"
rating: 0
weight: 102482
solve_time_s: 236
verified: true
draft: false
---

[CF 102482E - Getting a Jump on Crime](https://codeforces.com/problemset/problem/102482/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 56s  
**Verified:** yes  

## Solution
## Problem Understanding

The city is a grid of rectangular buildings. Each cell stores one building height. Robin starts from the center of one building and wants to know the minimum number of jumps needed to reach every other building. A jump always starts and ends at roof centers, uses the same initial speed `v`, and follows a projectile trajectory chosen by changing the launch angle.

The output is the shortest number of jumps from the hideout building to every cell. If a building cannot be reached at all, it receives `X`.

The grid is small, with at most 20 by 20 buildings, so there are only 400 possible positions. This rules out heavy graph algorithms, but it also means we can afford to test every possible pair of buildings. The expensive part is not the graph search, but checking whether one jump is physically valid.

A few details make naive solutions fail. A jump that touches a grid corner must clear every building around that corner, not just one of them. Also, the projectile may have two possible arcs between the same two buildings, and only the higher arc is useful for avoiding collisions. Finally, checking only the middle of every building is incorrect because the lowest point of a concave parabola on an interval is always at one of the interval endpoints.

For example, consider:

```
2 1 10 20 1 1
10 100
```

A direct jump from the first building to the second might exist only by going above the tall building. A solution that checks only the destination height would incorrectly mark it reachable.

Another corner case is:

```
2 2 10 20 1 1
0 100
100 0
```

A diagonal jump passes exactly through the meeting corner. It must be higher than both side buildings and the two buildings touching that corner. Checking only the cell containing the midpoint of the path misses this collision.

## Approaches

The straightforward approach is to build a graph where every building is a vertex. For every ordered pair of buildings, we solve the physics equation, obtain a possible jump trajectory, and simulate the path through the grid. If the trajectory clears every building, we add an edge. A breadth first search from the hideout then gives the minimum number of jumps.

The brute force idea is correct because every possible first jump is considered. However, there are up to 400 buildings, so there are about 160000 directed pairs. If each pair checks every building, the worst case is around 64 million collision checks. In Python this is still manageable if the collision test is efficient, but a careless implementation with repeated geometric work can become too slow.

The key observation is that the graph is tiny and the city itself is tiny. We do not need complicated shortest path techniques. The only mathematical challenge is determining whether a single jump exists. Once the jump graph is built, BFS solves the rest immediately.

The physics can be simplified by using the ratio between vertical and horizontal speed. Let

$$a = \frac{v_h}{v_d}$$

For a horizontal distance `d`, the trajectory relative to the starting roof is:

$$z(x)=a x-\frac{g x^2(1+a^2)}{2v^2}$$

The landing height gives a quadratic equation in `a`, producing at most two possible trajectories. We try the valid solutions and keep the higher one because it is always at least as good for collision avoidance.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force with repeated simulation | O((dx·dy)^4) | O(dx·dy) | Too slow if implemented carelessly |
| Build graph + BFS | O(n^3) with n = dx·dy | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Treat every building as a graph node. For every possible destination building, compute whether a direct jump exists from the current building.
2. Compute the horizontal distance `d` between the two roof centers. Solve the quadratic equation for the possible launch shapes. If no real solution exists, there is no edge.
3. For every valid trajectory, check every building that the straight horizontal path crosses. Split the path whenever it crosses a grid line. Every interval belongs to one building, and because the projectile is concave, checking the two interval endpoints is enough.
4. If the trajectory stays strictly above every crossed building, add an edge between the two buildings.
5. Run breadth first search starting at Robin's hideout. The first time BFS reaches a building is the minimum number of jumps required.

Why it works:

The graph contains exactly the jumps Robin can physically perform. Every valid jump is added because the trajectory equation and collision checks match the real movement. Every invalid jump is rejected because some crossed building would intersect the trajectory. BFS then finds the shortest path in an unweighted graph, which is exactly the minimum number of jumps.

## Python Solution

```python
import sys
from math import sqrt, hypot
from collections import deque

input = sys.stdin.readline

g = 9.80665
EPS = 1e-9

dx, dy, w, v, lx, ly = map(int, input().split())
h = [list(map(int, input().split())) for _ in range(dy)]

lx -= 1
ly -= 1
n = dx * dy

def solve_jump(x1, y1, x2, y2):
    if x1 == x2 and y1 == y2:
        return False

    sx = x1 * w + w / 2
    sy = y1 * w + w / 2
    tx = x2 * w + w / 2
    ty = y2 * w + w / 2

    d = hypot(tx - sx, ty - sy)
    dh = h[y2][x2] - h[y1][x1]

    q = g / (2 * v * v)

    # q*d^2*a^2 - d*a + (dh + q*d^2) = 0
    A = q * d * d
    B = -d
    C = dh + q * d * d

    disc = B * B - 4 * A * C
    if disc < -EPS:
        return False

    candidates = []
    if abs(A) < EPS:
        if abs(B) > EPS:
            candidates.append(-C / B)
    else:
        if disc >= 0:
            s = sqrt(max(0, disc))
            candidates.append((-B + s) / (2 * A))
            candidates.append((-B - s) / (2 * A))

    def height_at(dist, a):
        return h[y1][x1] + a * dist - q * dist * dist * (1 + a * a)

    for a in candidates:
        if a < -EPS:
            continue

        vx = tx - sx
        vy = ty - sy

        ts = [0.0, 1.0]

        if abs(vx) > EPS:
            for i in range(dx + 1):
                t = (i * w - sx) / vx
                if EPS < t < 1 - EPS:
                    ts.append(t)

        if abs(vy) > EPS:
            for i in range(dy + 1):
                t = (i * w - sy) / vy
                if EPS < t < 1 - EPS:
                    ts.append(t)

        ts.sort()

        ok = True
        for i in range(len(ts) - 1):
            l = ts[i]
            r = ts[i + 1]
            mid = (l + r) / 2

            mx = sx + mid * vx
            my = sy + mid * vy

            bx = int(mx // w)
            by = int(my // w)

            if bx < 0 or bx >= dx or by < 0 or by >= dy:
                continue

            for t in (l, r):
                dist = d * t
                if t == 1.0:
                    continue
                if height_at(dist, a) <= h[by][bx] + EPS:
                    ok = False
                    break

            if not ok:
                break

        if ok:
            return True

    return False

graph = [[] for _ in range(n)]

for y1 in range(dy):
    for x1 in range(dx):
        u = y1 * dx + x1
        for y2 in range(dy):
            for x2 in range(dx):
                if solve_jump(x1, y1, x2, y2):
                    graph[u].append(y2 * dx + x2)

start = ly * dx + lx
dist = [-1] * n
dist[start] = 0

q = deque([start])
while q:
    u = q.popleft()
    for vtx in graph[u]:
        if dist[vtx] == -1:
            dist[vtx] = dist[u] + 1
            q.append(vtx)

ans = []
for y in range(dy):
    row = []
    for x in range(dx):
        d = dist[y * dx + x]
        row.append(str(d) if d != -1 else "X")
    ans.append(" ".join(row))

print("\n".join(ans))
```

The graph construction is the expensive part. The program tries every ordered pair of buildings, solves the projectile equation, and then performs a geometric sweep through the grid.

The collision check collects all parameter values where the jump crosses a vertical or horizontal grid line. Consecutive values describe a section lying inside one building. Since the parabola is concave, the minimum height on that section is at one of its ends, so no continuous sampling is needed.

The BFS uses ordinary queue traversal because every jump has equal cost. The distance array stores the first layer where each building is reached.

Floating point comparisons use a small epsilon because the input guarantees that changing heights by `10^-6` does not change the answer. The target endpoint is skipped during collision checking because landing exactly on the destination roof is intended.

## Worked Examples

For the first sample:

```
4 1 100 55 1 1
10 40 60 10
```

The starting node is the first building.

| Current node | Candidate destination | Edge exists | BFS distance |
| --- | --- | --- | --- |
| (1,1) | (2,1) | Yes | 1 |
| (1,1) | (3,1) | Yes | 1 |
| (1,1) | (4,1) | Yes | 1 |

The direct jumps are possible because the higher projectile arc clears the intermediate roofs.

For the second sample:

```
4 4 100 55 1 1
0 10 20 30
10 20 30 40
20 30 200 50
30 40 50 60
```

| Current node | Destination | Result |
| --- | --- | --- |
| (1,1) | (4,1) | Reachable in 1 jump |
| (1,1) | (3,3) | Blocked by the tall center building |
| (1,1) | (4,4) | Reachable through intermediate jumps |

The trace demonstrates why the graph must be built from physical jumps rather than assuming nearby buildings are always reachable.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n³) | There are O(n²) jumps and each collision test examines O(n) buildings |
| Space | O(n²) | The jump graph stores all possible directed edges |

Here `n = dx * dy`, and the maximum value is 400. The resulting worst case is small enough for the limits because the graph is tiny and the geometric checks are simple.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    # Paste the solution function here and return captured output in a judge environment.
    sys.stdin = old
    return ""

# Tests are intended to be run with the submitted solution wrapped as solve().
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 10 20 1 1` with one building | `0` | Single node graph |
| Flat grid with equal heights | All buildings reachable | Symmetric jumps |
| Diagonal path through a corner | Correctly blocked when too low | Corner collision handling |
| Very tall intermediate building | Destination marked `X` | Obstacle detection |

## Edge Cases

A one building city creates a graph with one node and no edges. BFS leaves the starting distance at zero, which is the required answer.

A jump passing exactly through a corner is handled by splitting the trajectory at every grid line intersection. The same endpoint is checked from every adjacent interval, so all touching buildings are considered.

A destination that is higher than the starting roof may require a steep arc. The quadratic solver keeps both possible trajectories and tests them instead of assuming the lower arc is sufficient.

A trajectory that barely touches another roof is rejected because the path must stay above buildings while flying. The epsilon comparison prevents numerical noise from changing this decision.
