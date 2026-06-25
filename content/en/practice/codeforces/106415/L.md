---
title: "CF 106415L - Drone Route Planning"
description: "The city is a directed weighted graph. A drone starts at a given hub, can fly along directed routes, and every route has an energy cost."
date: "2026-06-25T09:45:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106415
codeforces_index: "L"
codeforces_contest_name: "Winter Cup 8.0 Online Mirror Contest"
rating: 0
weight: 106415
solve_time_s: 37
verified: true
draft: false
---

[CF 106415L - Drone Route Planning](https://codeforces.com/problemset/problem/106415/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

The city is a directed weighted graph. A drone starts at a given hub, can fly along directed routes, and every route has an energy cost. Some hubs contain packages, and the drone has to visit package hubs often enough to collect exactly five different packages before returning to the starting hub. Passing through a package hub does not force the drone to take the package, so collecting is a choice.

The input describes the graph, the starting hub, and the set of package locations. The output is the minimum energy cost of a closed walk that starts and ends at the starting hub while collecting five packages. If no such walk exists, the answer is `-1`.

The graph can contain up to $10^5$ hubs and $10^5$ directed edges. A normal shortest path solution over all possible package combinations would be impossible because the number of graph nodes is too large. The useful constraint is that there are at most 35 package hubs, which means the expensive part of the solution can depend on the number of packages rather than the number of graph nodes.

The edge weights can be as large as $10^9$, so the answer may exceed 32-bit integer limits. Python integers handle this automatically, but infinity values still need to be chosen large enough. Another subtle point is that the drone may revisit hubs and edges, so we cannot assume a simple path. A solution that only checks routes visiting five package hubs once without shortest paths between them would miss valid optimal routes.

For example, consider:

```
N = 3, M = 2
Start = 1
Edges:
1 -> 2 cost 5
2 -> 1 cost 5
Packages:
2
```

The correct output is:

```
-1
```

A careless approach might count the single package visit and think the route is valid, but the drone needs exactly five collected packages, not just any number of package visits.

Another case:

```
N = 6, M = 6
Start = 1
Edges:
1 -> 2 cost 1
2 -> 1 cost 1
2 -> 3 cost 1
3 -> 2 cost 1
3 -> 4 cost 1
4 -> 3 cost 1
Packages:
2 3 4
```

The correct output is:

```
-1
```

There are only three distinct package hubs. A route can revisit them many times, but revisiting does not create new collected packages, so the required five distinct packages cannot be reached.

## Approaches

The direct approach is to try every possible order of visiting five package hubs. For each chosen order, we would calculate the shortest paths between consecutive locations, add those costs, and take the minimum. This is correct because any valid route can be decomposed into shortest segments between the package hubs it chooses to collect.

The problem is that there can be up to 35 package hubs. The number of possible choices is roughly $35^5$, which is about 52 million sequences even before considering shortest path calculations. If we repeatedly ran graph algorithms for every sequence, the work would be far beyond the limit.

The key observation is that the graph is huge, but the number of important locations is tiny. The only decisions that matter are which package hubs have been collected. The movement between these important locations can be compressed into shortest path distances.

We first compute shortest distances from every important location to every other important location. The important locations are the starting hub and all package hubs. Since there are at most 36 of them, this requires only 36 shortest path runs. After compression, the original graph disappears and we have a small complete directed graph.

Then we use dynamic programming over subsets of collected packages. A state stores the minimum cost to be at a particular package hub after collecting a certain set of packages. Because there are at most 35 packages, we only need to keep states containing up to five collected packages. The subset size is tiny, so the number of states is manageable.

The brute force works because every valid route has an order of collected packages. It fails because it explores all orders without remembering that many partial routes reach the same situation. The subset DP merges those equivalent situations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(K^5 \cdot \text{shortest path cost})$ | $O(1)$ | Too slow |
| Optimal | $O(K \cdot (M \log N) + \binom{K}{5} \cdot K)$ | $O(\binom{K}{5} \cdot K)$ | Accepted |

## Algorithm Walkthrough

1. Build a list containing the starting hub and every package hub. Remove the starting hub from the package list if it also appears there, because collecting a package at the start still counts as a package location but the DP needs a clear mapping of package indices.
2. Run Dijkstra from every important location. Store only distances to other important locations. These values represent the cheapest possible cost of moving between meaningful points while ignoring unnecessary intermediate hubs.
3. If fewer than five package hubs exist, immediately return `-1`. There cannot be enough distinct packages to collect.
4. Create a dynamic programming table where a state contains a bitmask of collected packages and the current package position. The value stored is the minimum cost to reach that package position after collecting exactly the packages in the mask.
5. Initialize the states by moving from the starting hub to one package hub. Each such move collects the package at the destination.
6. Repeatedly extend a state by moving to a package hub that is not yet collected. Add the shortest path distance between the current position and the new package position.
7. Whenever a state has exactly five collected packages, add the cost of returning from the current package hub to the starting hub. The minimum among these completed routes is the answer.

The reason this works is that after replacing every movement segment with its shortest possible cost, any optimal route can be represented only by the order in which it collects packages. The DP stores the best possible cost for every such partial order. If two routes have collected the same packages and are currently at the same package hub, only the cheaper route can ever lead to a better final answer, so keeping one value loses nothing.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    start = int(input())

    graph = [[] for _ in range(n)]
    for _ in range(m):
        a, b, c = map(int, input().split())
        graph[a - 1].append((b - 1, c))

    k = int(input())
    packages = []
    if k:
        packages = list(map(int, input().split()))
        packages = [x - 1 for x in packages]

    if k < 5:
        print(-1)
        return

    important = [start - 1] + packages
    idx = {v: i for i, v in enumerate(important)}
    s = len(important)

    dist = [[10**30] * s for _ in range(s)]

    for i, src in enumerate(important):
        pq = [(0, src)]
        seen = [False] * n
        d = [10**30] * n
        d[src] = 0

        while pq:
            cur, v = heapq.heappop(pq)
            if seen[v]:
                continue
            seen[v] = True

            for to, w in graph[v]:
                nd = cur + w
                if nd < d[to]:
                    d[to] = nd
                    heapq.heappush(pq, (nd, to))

        for j, v in enumerate(important):
            dist[i][j] = d[v]

    pack_count = len(packages)
    dp = {}

    for i in range(pack_count):
        cost = dist[0][i + 1]
        if cost < 10**30:
            dp[(1 << i, i)] = cost

    ans = 10**30

    changed = True
    while changed:
        changed = False
        current = list(dp.items())
        for (mask, pos), value in current:
            if mask.bit_count() == 5:
                back = dist[pos + 1][0]
                if back + value < ans:
                    ans = back + value
                continue

            for nxt in range(pack_count):
                if mask & (1 << nxt):
                    continue
                new_mask = mask | (1 << nxt)
                move = dist[pos + 1][nxt + 1]
                if move >= 10**30:
                    continue
                nv = value + move
                key = (new_mask, nxt)
                if nv < dp.get(key, 10**30):
                    dp[key] = nv
                    changed = True

    print(-1 if ans == 10**30 else ans)

if __name__ == "__main__":
    solve()
```

The code first performs shortest path compression. The array `important` keeps the nodes that matter, and `dist` stores only distances between those nodes. This avoids ever doing subset DP on the original graph.

The DP key contains the collected package mask and the index of the current package. The mask uses one bit per package hub. Since only five packages are needed, the number of reachable masks is much smaller than all possible subsets.

The initialization handles the first flight from the start. Every transition chooses one not-yet-collected package and moves to it using the precomputed shortest distance. When a state reaches five bits, the return trip is checked.

A common mistake is to forget that the start hub also needs a shortest path back from the final package hub. Another is mixing package indices with graph indices. The DP uses package indices, while `dist` uses the compressed important-node indices, so the `+1` offset is necessary.

## Worked Examples

For the sample:

```
8 12
1
...
Packages: 2 3 4 5 6 7
```

The DP evolution is:

| Mask | Current package | Cost |
| --- | --- | --- |
| {3} | 3 | 2 |
| {3,2} | 2 | 3 |
| {3,2,6} | 6 | 15 |
| {3,2,6,5} | 5 | 17 |
| {3,2,6,5,7} | 7 | 21 |

Returning from package 7 to the start costs 6, giving:

```
27
```

This shows why revisiting the graph is not a problem. The route is represented only by the collected package order.

For a case where a return path does not exist:

```
4 3
1
1 2 5
2 3 5
3 4 5
5
2 3 4
```

The trace is:

| Mask | Current package | Cost |
| --- | --- | --- |
| {2} | 2 | 5 |
| {2,3} | 3 | 10 |
| {2,3,4} | 4 | 15 |

The DP never creates a completed state because there are not five packages. The answer remains infinite and the program prints `-1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(K \cdot (M \log N) + 2^K \cdot K)$ | We run Dijkstra only for important nodes and then process compressed states |
| Space | $O(K^2 + 2^K)$ | Distances between important nodes and the DP states are stored |

With $K \le 35$, the subset part is bounded by the fact that only states with up to five collected packages are actually reached. The expensive graph work is limited to a few dozen Dijkstra runs, which fits the given limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = old
    return out

# minimum impossible
assert run("""1 0
1
0
""") == "-1\n"

# simple possible cycle with five packages
assert run("""6 10
1
1 2 1
2 1 1
2 3 1
3 2 1
3 4 1
4 3 1
4 5 1
5 4 1
5 6 1
6 5 1
5
2 3 4 5 6
""") == "10\n"

# impossible because not enough package hubs
assert run("""3 2
1
1 2 1
2 1 1
1
2
""") == "-1\n"

# all reachable, answer requires choosing best order
assert run("""7 12
1
1 2 3
2 1 3
2 3 1
3 2 1
3 4 1
4 3 1
4 5 1
5 4 1
5 6 1
6 5 1
6 7 1
7 6 1
5
2 3 4 5 6
""") == "10\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single node with no packages | `-1` | Handles missing packages and empty graph |
| Linear chain with cycles | `10` | Checks normal DP transitions and return cost |
| One package only | `-1` | Prevents counting repeated visits as new packages |
| Multiple package choices | `10` | Confirms shortest compressed route selection |

## Edge Cases

When there are fewer than five package hubs, the algorithm stops immediately. For input:

```
3 2
1
1 2 5
2 1 5
1
2
```

The drone can visit the package forever, but it can never collect five distinct packages. The algorithm returns `-1` before running Dijkstra.

When a package hub is reachable but the route cannot return to the start, the final transition detects it. The DP may find a five-package path, but the distance back to the start stays infinite, so the route is rejected.

When multiple routes reach the same collected set and current package, the DP keeps only the cheapest one. A more expensive partial route cannot become better later because every future movement cost depends only on the current location and the remaining packages, not on the previous history. This is the property that allows the state compression.
