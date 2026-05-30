---
title: "CF 449B - Jzzhu and Cities"
description: "We are given an undirected weighted graph representing cities and roads. City 1 is the capital. In addition to normal roads, there are special train routes that connect the capital directly to some city. The government wants to close as many train routes as possible."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "graphs", "greedy", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 449
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 257 (Div. 1)"
rating: 2000
weight: 449
solve_time_s: 86
verified: true
draft: false
---

[CF 449B - Jzzhu and Cities](https://codeforces.com/problemset/problem/449/B)

**Rating:** 2000  
**Tags:** graphs, greedy, shortest paths  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected weighted graph representing cities and roads. City 1 is the capital. In addition to normal roads, there are special train routes that connect the capital directly to some city.

The government wants to close as many train routes as possible. The restriction is that after removing those trains, the shortest distance from every city to the capital must remain exactly the same as before.

The task is not to find shortest paths after removing trains. Instead, we must determine how many train routes are unnecessary while preserving all shortest distances from the capital.

The graph contains up to $10^5$ cities, $3 \cdot 10^5$ roads, and $10^5$ train routes. Those limits immediately rule out any approach that repeatedly recomputes shortest paths. Running Dijkstra even a few thousand times would already be too expensive. We need something close to $O((n+m+k)\log n)$.

The most subtle part of the problem is that multiple train routes may go to the same city. Some of them can be redundant even if trains are required for that city.

Consider:

```
1 --(10)-- 2

Train: 1 -> 2 length 5
Train: 1 -> 2 length 7
```

The shortest distance to city 2 is 5. The train of length 7 can obviously be removed.

Another tricky case is when a train achieves the shortest distance, but a road-based shortest path of equal length also exists.

```
1 --(2)-- 3 --(3)-- 2

Train: 1 -> 2 length 5
```

The shortest distance to city 2 is 5. Removing the train does not change anything because the road path also has length 5. A solution that keeps every train participating in some shortest path would be incorrect.

A third subtle case occurs when a city's shortest distance can only be achieved through a train.

```
1 --(100)-- 2

Train: 1 -> 2 length 5
```

Here the train is essential. Removing it changes the shortest distance from 5 to 100.

The challenge is identifying exactly which trains are indispensable.

## Approaches

A brute-force approach would examine each train route independently. For every train, temporarily remove it, recompute shortest paths from the capital, and check whether any city's distance changes.

This is correct because it directly tests the condition from the statement. Unfortunately it is hopelessly slow. There can be $10^5$ trains, and each Dijkstra execution costs roughly $O((n+m)\log n)$. The worst case reaches around $10^5 \times 4 \cdot 10^5 \log 10^5$ operations, far beyond the limit.

The key observation is that train routes can be treated as edges in the graph. A train from city 1 to city $s$ with length $y$ is simply another edge $(1,s,y)$.

If we run Dijkstra on the graph containing both roads and trains, we obtain the true shortest distance to every city.

After that, the problem becomes: which train edges are actually needed to preserve those shortest distances?

Suppose a city $v$ has shortest distance $dist[v]$. Any edge $(u,v,w)$ satisfying

$$dist[u] + w = dist[v]$$

can be part of a shortest path tree.

If city $v$ has at least one incoming shortest-path road edge, then a train ending at $v$ is not required. We can reach $v$ through roads while preserving the same shortest distance.

If no road edge can produce $dist[v]$, then at least one train must remain to realize that shortest distance.

This turns the problem into counting how many train routes are actually required by the shortest-path structure.

### Approach Comparison

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(k(n+m)\log n)$ | $O(n+m)$ | Too slow |
| Optimal | $O((n+m+k)\log n)$ | $O(n+m+k)$ | Accepted |

## Algorithm Walkthrough

### Step 1

Build the graph using all road edges.

Store every train separately. For Dijkstra, also add each train as an edge between city 1 and its destination city.

At this point roads and trains are treated uniformly as graph edges.

### Step 2

Run Dijkstra from city 1 on the complete graph.

The resulting array `dist` contains the shortest possible distance from the capital to every city when all trains are available.

These distances are exactly the values that must remain unchanged after closing routes.

### Step 3

For every city, determine whether there exists a road edge that can be the last edge of a shortest path.

For each road $(u,v,w)$:

If

$$dist[u] + w = dist[v]$$

then city $v$ can be reached optimally through a road.

Similarly, if

$$dist[v] + w = dist[u]$$

then city $u$ can be reached optimally through a road.

Maintain an array `roadParentPossible`.

`roadParentPossible[x] = True` means city `x` has at least one shortest-path predecessor connected by a normal road.

### Step 4

Process all train routes.

For a train ending at city `s` with length `y`, it contributes to a shortest path only if

$$y = dist[s]$$

because the train starts directly from the capital whose distance is zero.

Any train with

$$y > dist[s]$$

can never belong to a shortest path and is immediately removable.

### Step 5

Among trains satisfying `y == dist[s]`, decide which are necessary.

If `roadParentPossible[s]` is true, then city `s` already has a shortest-path road predecessor. Every train achieving the same distance is redundant and can be removed.

If `roadParentPossible[s]` is false, then some shortest-path train must remain for city `s`.

Multiple shortest trains may exist for the same city. In that situation, keep exactly one and remove all others.

Use a counter per city to track how many shortest-valid trains arrive there.

### Step 6

Count removable trains.

A train is removable if:

1. It is longer than the shortest distance.
2. It reaches a city that already has a shortest-path road predecessor.
3. It is an extra duplicate among multiple shortest-valid trains for a city that requires a train.

### Why it works

After Dijkstra, `dist[v]` is the shortest possible distance for every city. Any preserved solution must still realize those distances.

A city with a shortest-path road predecessor can obtain its optimal distance entirely through roads, so no train ending there is required.

A city without such a predecessor must receive its shortest distance directly from a train. Keeping one shortest-valid train is sufficient because all trains start from the capital and produce the same distance value. Additional trains to the same city contribute nothing.

Thus every removed train is provably unnecessary, and every retained train is required to preserve at least one shortest distance. The count of removed trains is therefore maximal.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())

    graph = [[] for _ in range(n + 1)]
    roads = []

    for _ in range(m):
        u, v, w = map(int, input().split())
        roads.append((u, v, w))
        graph[u].append((v, w))
        graph[v].append((u, w))

    trains = []

    for _ in range(k):
        s, y = map(int, input().split())
        trains.append((s, y))
        graph[1].append((s, y))
        graph[s].append((1, y))

    INF = 10**30
    dist = [INF] * (n + 1)
    dist[1] = 0

    pq = [(0, 1)]

    while pq:
        d, u = heapq.heappop(pq)

        if d != dist[u]:
            continue

        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))

    road_parent_possible = [False] * (n + 1)

    for u, v, w in roads:
        if dist[u] + w == dist[v]:
            road_parent_possible[v] = True
        if dist[v] + w == dist[u]:
            road_parent_possible[u] = True

    valid_train_count = [0] * (n + 1)

    for s, y in trains:
        if y == dist[s]:
            valid_train_count[s] += 1

    removable = 0

    for s, y in trains:
        if y > dist[s]:
            removable += 1
        elif road_parent_possible[s]:
            removable += 1
        else:
            if valid_train_count[s] > 1:
                removable += 1
                valid_train_count[s] -= 1

    print(removable)

if __name__ == "__main__":
    solve()
```

### Implementation Discussion

The first phase constructs a graph containing both roads and trains. Dijkstra does not need to distinguish between them because all we care about initially is the true shortest distance.

After shortest distances are known, only road edges are inspected to populate `road_parent_possible`. This array identifies cities that already have a shortest-path route ending with a normal road.

The array `valid_train_count` counts trains whose length exactly equals the shortest distance of their destination. Only such trains could possibly be useful.

During the final pass, every train is classified. Trains longer than the shortest distance are immediately redundant. If a shortest-path road predecessor exists, every train to that city is redundant. Otherwise exactly one shortest-valid train must survive, and all additional copies are removed.

A common mistake is trying to decide train necessity during Dijkstra. Equal-distance situations make that approach error-prone. Computing all shortest distances first and then analyzing the shortest-path graph is much cleaner.

## Worked Examples

### Sample 1

Input:

```
5 5 3
1 2 1
2 3 2
1 3 3
3 4 4
1 5 5
3 5
4 5
5 5
```

After Dijkstra:

| City | Distance |
| --- | --- |
| 1 | 0 |
| 2 | 1 |
| 3 | 3 |
| 4 | 5 |
| 5 | 5 |

Checking roads:

| City | Has shortest-path road predecessor? |
| --- | --- |
| 2 | Yes |
| 3 | Yes |
| 4 | No |
| 5 | Yes |

Train analysis:

| Train | Shortest-valid? | Road predecessor exists? | Removable? |
| --- | --- | --- | --- |
| (3,5) | No | Yes | Yes |
| (4,5) | Yes | No | No |
| (5,5) | Yes | Yes | Yes |

Total removable trains = 2.

### Example Showing Duplicate Trains

Input:

```
3 1 3
1 2 10
2 3 10
3 20
3 20
3 20
```

After Dijkstra:

| City | Distance |
| --- | --- |
| 1 | 0 |
| 2 | 10 |
| 3 | 20 |

No road edge can achieve distance 20 for city 3.

| Train | Valid? |
| --- | --- |
| 20 | Yes |
| 20 | Yes |
| 20 | Yes |

One train must remain.

| Remaining needed | Removable |
| --- | --- |
| 1 | 2 |

The answer is 2.

This example demonstrates why counting duplicate shortest trains correctly is necessary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n+m+k)\log n)$ | One Dijkstra plus linear scans of roads and trains |
| Space | $O(n+m+k)$ | Graph storage, distance array, auxiliary arrays |

The graph contains at most $m+k$ edges beyond symmetry in the adjacency list. Dijkstra dominates the running time. With $n \le 10^5$ and $m+k \le 4 \cdot 10^5$, this comfortably fits within the limits.

## Test Cases

```
# helper verification logic would call solve() and compare output

# Sample 1
assert answer == 2  # provided sample

# Single essential train
# 1--100--2, train length 5
assert answer == 0  # train cannot be removed

# Train worse than road path
# road distance 5, train distance 10
assert answer == 1  # train removable

# Duplicate shortest trains
# three trains of equal optimal length
assert answer == 2  # keep one, remove two

# Road provides same shortest distance
# 1-3 (2), 3-2 (3), train to 2 length 5
assert answer == 1  # train redundant

# Multiple cities requiring trains
assert answer == 1  # only redundant train removed

# Large chain with no trains useful
assert answer == k  # all trains removable

# City reachable only by train
assert answer == 0  # must keep train
```

### Test Summary

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | 2 | Official example |
| Single essential train | 0 | Required train cannot be removed |
| Train worse than road | 1 | Non-shortest train removal |
| Duplicate shortest trains | 2 | Keep exactly one shortest train |
| Equal road alternative | 1 | Shortest train can still be redundant |
| Multiple train destinations | Varies | Independent city handling |
| Large chain | k | Mass train removal |
| Train-only access | 0 | Necessity detection |

## Edge Cases

### Multiple Trains to the Same City

Consider:

```
3 1 3
1 2 10
2 3 10
3 20
3 20
3 20
```

The shortest distance to city 3 is 20. No road predecessor can achieve that value. One train must remain, but the other two are redundant. The algorithm counts all shortest-valid trains and removes all but one.

### A Train Equals the Shortest Distance but Is Still Unnecessary

Consider:

```
3 2 1
1 3 2
3 2 3
2 5
```

City 2 has shortest distance 5. The train also has length 5. A naive solution might keep it because it lies on a shortest path. However, the road path already achieves distance 5. `road_parent_possible[2]` becomes true, so the train is removed.

### Trains Longer Than the Optimal Distance

Consider:

```
2 1 1
1 2 5
2 10
```

The shortest distance to city 2 is 5 through the road. The train length is 10, which is not part of any shortest path. The algorithm detects `10 > dist[2]` and removes it immediately.

### Multiple Shortest Road Predecessors

Consider:

```
1--2 (2)
1--3 (2)
2--4 (2)
3--4 (2)
Train 1->4 (4)
```

City 4 has multiple shortest road predecessors. The shortest distance remains achievable entirely through roads. The train is removable, and the algorithm correctly marks city 4 as having a shortest-path road predecessor when scanning the road edges.
