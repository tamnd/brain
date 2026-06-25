---
title: "CF 106347D - \u041c\u043e\u0434\u0443\u043b\u044c\u043d\u044b\u0439 \u0433\u0440\u0430\u0444"
description: "We have a connected undirected graph. Every vertex stores a number, and moving through an edge costs the absolute difference between the numbers written at its two endpoints."
date: "2026-06-25T08:05:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106347
codeforces_index: "D"
codeforces_contest_name: "\u0412\u044b\u0441\u0448\u0430\u044f \u043f\u0440\u043e\u0431\u0430 - 2024. \u0417\u0430\u043a\u043b\u044e\u0447\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f"
rating: 0
weight: 106347
solve_time_s: 53
verified: true
draft: false
---

[CF 106347D - \u041c\u043e\u0434\u0443\u043b\u044c\u043d\u044b\u0439 \u0433\u0440\u0430\u0444](https://codeforces.com/problemset/problem/106347/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a connected undirected graph. Every vertex stores a number, and moving through an edge costs the absolute difference between the numbers written at its two endpoints. Before walking from vertex `1` to vertex `n`, we may replace the numbers in at most `k` vertices with any values we choose. The task is to find the minimum possible travel cost after making the best possible replacements.

The input gives the graph, the initial value of every vertex, and the maximum number of vertices whose values may be changed. The output is the smallest possible cost of a path from the first vertex to the last vertex after those changes.

The main difficulty comes from the fact that a changed vertex can take any value. We do not need to decide the actual new numbers directly. We need to understand what effect removing a small number of vertices from a path has.

The limits are small in terms of graph size but the values are not. There are up to 2000 vertices and 2000 edges, while `k` is at most 10. A solution depending on the numeric values is impossible because values can reach `10^9`. A solution with quadratic graph processing is acceptable, but anything involving all possible paths is not.

The small value of `k` is the key restriction. We can afford algorithms that multiply the graph size by a small factor, such as `O(n * k)` states or exploring paths of depth around `k`. We cannot enumerate all paths because even a sparse graph can contain exponentially many of them.

There are several edge cases that easily break an implementation.

If `k = 0`, no vertex may be modified, so the answer must be the ordinary shortest path with edge weights `|a_u-a_v|`. For example:

```
2 1 0
5 20
1 2
```

The only path has cost `15`, so the answer is:

```
15
```

A solution that always assumes at least one free modification may incorrectly output zero.

The start or finish vertex may be among the changed vertices. Consider:

```
2 1 2
100 200
1 2
```

Both vertices can be changed to the same value, so the answer is:

```
0
```

A solution that only allows changing internal vertices of the path misses this case.

A path can contain more than `k` vertices but still benefit from changes in the middle. For example:

```
4 3 1
1 100 5 10
1 2
2 3
3 4
```

Changing vertex `2` to `5` gives a path cost of `9`. The changed vertex does not need to be assigned one of its neighbors' original values, and the algorithm must allow arbitrary replacements.

## Approaches

The direct approach is to try every possible path and decide which vertices on it should be changed. This is correct because once a path is fixed, the only remaining choice is the new values of at most `k` vertices. However, even a graph with only 2000 vertices can have an enormous number of different paths, so this approach has exponential behavior and is unusable.

A better way to look at the problem is to forget the exact values assigned to changed vertices. Suppose a path contains some vertices that we modify. If we remove those modified vertices from the path, the remaining unchanged vertices appear in their original order. Between two consecutive unchanged vertices, all removed vertices can be assigned values that lie between the two original values, so the whole segment costs exactly the absolute difference of the two unchanged endpoints.

For example, the path

```
A - X - Y - B
```

where `X` and `Y` are changed, has minimum cost:

```
|a[A] - a[B]|
```

because `X` and `Y` can be chosen between the two endpoint values.

This converts the problem into one where we move between unchanged vertices and spend one unit of the modification budget for every skipped vertex. Since `k` is only 10, we only need to know paths that skip at most `k` vertices.

We create transitions between possible unchanged vertices. A transition from `u` to `v` exists if there is a graph path from `u` to `v` whose internal vertices are exactly the modified vertices. If the path has `d` edges, it consumes `d-1` modifications and costs `|a_u-a_v|`.

The start and finish require special handling because they can themselves be modified. We add two virtual vertices. The virtual start represents the situation where the prefix of the path before the first unchanged vertex has been changed. The virtual finish represents the suffix after the last unchanged vertex being changed. These transitions have zero cost and consume the number of vertices that are skipped.

After creating this small expanded graph, the remaining problem is a shortest path problem with an additional resource: how many modifications have already been used. Since the resource is at most 10, we can run Dijkstra on states `(vertex, used_changes)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in the number of paths | O(n) | Too slow |
| Optimal | O(n(n+m) + nk^2) | O(nk + n^2) | Accepted |

## Algorithm Walkthrough

1. Run a breadth-first search from every original vertex, but stop after depth `k + 1`.

We only care about paths that contain at most `k` modified internal vertices. A longer shortest path segment can never be used as one transition between unchanged vertices.
2. For every pair of original vertices `u` and `v` discovered by the BFS from `u`, create a transition if the distance is at least one edge.

If the distance is `d`, all `d - 1` internal vertices can be changed. The transition uses `d - 1` changes and has cost `|a_u - a_v|`.
3. Add a virtual start vertex.

From the virtual start, we can reach any original vertex `v` by changing every vertex before `v` on some path from vertex `1`. If the distance from vertex `1` to `v` is `d`, this transition consumes `d` changes and costs zero.
4. Add a virtual finish vertex.

From an original vertex `u`, we can finish by changing all vertices after `u` on a path to vertex `n`. If the distance is `d`, the transition consumes `d` changes and costs zero.
5. Run Dijkstra on states `(vertex, number_of_changes_used)`.

A state stores the minimum travel cost after reaching a vertex while spending exactly that many modifications. Transitions are only accepted when the new number of modifications does not exceed `k`.
6. The answer is the minimum distance to the virtual finish over all states with at most `k` used modifications.

Why it works:

The invariant is that every Dijkstra state represents an optimal way to reach a vertex after choosing exactly which vertices before it are modified. Whenever a modified segment is crossed, the only information that matters is the two unchanged endpoints, because all internal changed values can be chosen to make the segment cost the absolute difference of those endpoints. The BFS-generated transitions represent every possible segment that can use the available modification budget. Since Dijkstra explores all such transitions and keeps the cheapest cost for every amount of used budget, it cannot discard a better valid solution.

## Python Solution

```python
import sys
import heapq
from collections import deque

input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    a = list(map(int, input().split()))

    g = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    INF = 10**30

    jumps = [[] for _ in range(n)]

    for s in range(n):
        dist = [-1] * n
        q = deque([s])
        dist[s] = 0

        while q:
            v = q.popleft()
            if dist[v] == k + 1:
                continue
            for u in g[v]:
                if dist[u] == -1:
                    dist[u] = dist[v] + 1
                    q.append(u)

        for v in range(n):
            if v != s and dist[v] != -1 and dist[v] <= k + 1:
                jumps[s].append((v, dist[v] - 1, abs(a[s] - a[v])))

    start = n
    finish = n + 1
    total = n + 2

    jumps.extend([[], []])

    # From virtual start to first unchanged vertex.
    dist = [-1] * n
    q = deque([0])
    dist[0] = 0
    while q:
        v = q.popleft()
        if dist[v] == k:
            continue
        for u in g[v]:
            if dist[u] == -1:
                dist[u] = dist[v] + 1
                q.append(u)

    for v in range(n):
        if dist[v] != -1 and dist[v] <= k:
            jumps[start].append((v, dist[v], 0))

    # From unchanged vertex to virtual finish.
    dist = [-1] * n
    q = deque([n - 1])
    dist[n - 1] = 0
    while q:
        v = q.popleft()
        if dist[v] == k:
            continue
        for u in g[v]:
            if dist[u] == -1:
                dist[u] = dist[v] + 1
                q.append(u)

    for v in range(n):
        if dist[v] != -1 and dist[v] <= k:
            jumps[v].append((finish, dist[v], 0))

    # The whole path can consist of changed vertices.
    if dist[0] != -1 and dist[0] + 1 <= k:
        jumps[start].append((finish, dist[0] + 1, 0))

    d = [[INF] * (k + 1) for _ in range(total)]
    d[start][0] = 0

    pq = [(0, start, 0)]

    while pq:
        cur, v, used = heapq.heappop(pq)
        if cur != d[v][used]:
            continue

        for u, add_used, cost in jumps[v]:
            nu = used + add_used
            if nu <= k and cur + cost < d[u][nu]:
                d[u][nu] = cur + cost
                heapq.heappush(pq, (d[u][nu], u, nu))

    print(min(d[finish]))

if __name__ == "__main__":
    solve()
```

The BFS preprocessing constructs every useful compressed path segment. The depth limit is `k + 1` because a transition between unchanged vertices may contain at most `k` changed internal vertices.

The expanded graph stores transitions as `(destination, extra changes, cost)`. The Dijkstra phase does not need to know the actual values assigned to modified vertices. It only tracks how many modifications have been spent.

The virtual vertices are what handle changing the endpoints. Without them, the solution would incorrectly assume that vertices `1` and `n` must keep their original values.

All costs can reach roughly `10^9 * n`, so Python integers are used naturally. The algorithm never builds a dense `n x n` matrix, which keeps memory usage manageable.

## Worked Examples

For the first sample:

```
6 7 1
1 15 5 10 4 10
1 2
2 3
3 6
1 4
4 5
5 6
2 5
```

A useful compressed path is `1 -> 2 -> 5 -> 6`.

| Step | Current segment | Changes used | Cost |
| --- | --- | --- | --- |
| Start | at vertex 1 | 0 | 0 |
| Move to vertex 2 | keep 1 and 2 as endpoints | 0 | 14 |
| Change vertex 2 | replace value 15 with 3 | 1 | 14 |
| Move through 5 | compressed transition 2 to 5 | 1 | 2 |
| Finish at 6 | final unchanged vertex | 1 | 9 |

The important part is that the changed vertex is not stored with a chosen value in the algorithm. The transition directly captures the best possible result.

For the second sample:

```
6 7 3
1 15 5 10 4 10
1 2
2 3
3 6
1 4
4 5
5 6
2 5
```

The whole route can be changed.

| Step | State | Changes used | Cost |
| --- | --- | --- | --- |
| Start | virtual start | 0 | 0 |
| Change vertices before finish | follow a path containing only changed vertices | 3 | 0 |
| Finish | virtual finish | 3 | 0 |

The trace confirms that the virtual start and finish correctly handle cases where all useful vertices are modified.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n(n+m) + nk^2) | We run bounded BFS from every vertex and then Dijkstra over `O(nk)` states. |
| Space | O(nk + n + m) | The expanded state graph and BFS data fit within the limits. |

The graph has only 2000 vertices, and the modification limit is 10. The BFS depth restriction prevents the preprocessing from becoming a full all-pairs shortest path computation.

## Test Cases

```python
import sys, io, heapq
from collections import deque

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)

    def solve():
        n, m, k = map(int, input().split())
        a = list(map(int, input().split()))
        g = [[] for _ in range(n)]
        for _ in range(m):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            g[u].append(v)
            g[v].append(u)

        INF = 10**30
        jumps = [[] for _ in range(n)]

        for s in range(n):
            dist = [-1] * n
            q = deque([s])
            dist[s] = 0
            while q:
                v = q.popleft()
                if dist[v] == k + 1:
                    continue
                for u in g[v]:
                    if dist[u] == -1:
                        dist[u] = dist[v] + 1
                        q.append(u)
            for v in range(n):
                if v != s and dist[v] != -1 and dist[v] <= k + 1:
                    jumps[s].append((v, dist[v] - 1, abs(a[s] - a[v])))

        start, finish = n, n + 1
        jumps.extend([[], []])

        dist = [-1] * n
        q = deque([0])
        dist[0] = 0
        while q:
            v = q.popleft()
            if dist[v] == k:
                continue
            for u in g[v]:
                if dist[u] == -1:
                    dist[u] = dist[v] + 1
                    q.append(u)
        for v in range(n):
            if dist[v] != -1 and dist[v] <= k:
                jumps[start].append((v, dist[v], 0))

        dist = [-1] * n
        q = deque([n - 1])
        dist[n - 1] = 0
        while q:
            v = q.popleft()
            if dist[v] == k:
                continue
            for u in g[v]:
                if dist[u] == -1:
                    dist[u] = dist[v] + 1
                    q.append(u)
        for v in range(n):
            if dist[v] != -1 and dist[v] <= k:
                jumps[v].append((finish, dist[v], 0))

        if dist[0] != -1 and dist[0] + 1 <= k:
            jumps[start].append((finish, dist[0] + 1, 0))

        d = [[INF] * (k + 1) for _ in range(n + 2)]
        d[start][0] = 0
        pq = [(0, start, 0)]

        while pq:
            cur, v, used = heapq.heappop(pq)
            if cur != d[v][used]:
                continue
            for u, add, cost in jumps[v]:
                if used + add <= k and cur + cost < d[u][used + add]:
                    d[u][used + add] = cur + cost
                    heapq.heappush(pq, (d[u][used + add], u, used + add))

        return str(min(d[finish])) + "\n"

    res = solve()
    sys.stdin = old
    return res

assert run("""6 7 1
1 15 5 10 4 10
1 2
2 3
3 6
1 4
4 5
5 6
2 5
""") == "9\n"

assert run("""6 7 3
1 15 5 10 4 10
1 2
2 3
3 6
1 4
4 5
5 6
2 5
""") == "0\n"

assert run("""2 1 0
5 20
1 2
""") == "15\n"

assert run("""2 1 2
100 200
1 2
""") == "0\n"

assert run("""3 2 1
1 100 10
1 2
2 3
""") == "9\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | 9 | Basic compressed transition with one modification |
| Sample 2 | 0 | Entire path can be modified |
| Two vertices, `k=0` | 15 | No-modification boundary case |
| Two vertices, `k=2` | 0 | Changing endpoints |
| Three-vertex chain | 9 | Internal vertex replacement |

## Edge Cases

For `k = 0`, the preprocessing creates only transitions with zero skipped vertices. The Dijkstra states collapse to ordinary shortest path states, so the answer is the original weighted shortest path.

For a path where the start or finish is changed, the virtual vertices provide the missing endpoints. For example:

```
2 1 2
100 200
1 2
```

The transition from the virtual start directly to the virtual finish consumes two changes and costs zero. This represents changing both vertices to the same value.

For paths with several consecutive changed vertices, the BFS transition removes the whole segment at once. In:

```
4 3 2
1 100 200 10
1 2
2 3
3 4
```

changing vertices `2` and `3` leaves the endpoints with cost:

```
|1 - 10| = 9
```

The algorithm reaches the same compressed transition from vertex `1` to vertex `4` using two modifications and never needs to guess the new values of vertices `2` and `3`.
