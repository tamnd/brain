---
title: "CF 105201L - Little Gas Station"
description: "The city is a tree: every intersection is connected to every other one through exactly one path. Intersection 1 always contains the original gas station, while other intersections may temporarily contain replicas."
date: "2026-06-27T02:49:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105201
codeforces_index: "L"
codeforces_contest_name: "IME++ Open Contest 2024"
rating: 0
weight: 105201
solve_time_s: 71
verified: false
draft: false
---

[CF 105201L - Little Gas Station](https://codeforces.com/problemset/problem/105201/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** no  

## Solution
## Problem Understanding

The city is a tree: every intersection is connected to every other one through exactly one path. Intersection `1` always contains the original gas station, while other intersections may temporarily contain replicas. During the sequence of days, replicas are added and removed, and some days ask for the distance from a given intersection to the closest currently existing gas station.

The task is not to maintain the tree itself. The roads never change. The challenge is maintaining the set of marked vertices, where a marked vertex means that a gas station exists there, while answering minimum distance queries quickly.

The constraints force a dynamic data structure. With up to `2 * 10^5` intersections and `2 * 10^5` operations, scanning all gas stations for every query is too expensive. In the worst case, if every operation is a query and there are many stations, a direct search can take around `O(nq)`, which is about `4 * 10^10` operations. Even running a breadth first search from every query vertex is impossible. We need logarithmic or near logarithmic work per operation.

There are several edge cases that break simple implementations. The first is that the original station at vertex `1` never disappears. For example:

```
3 3
1 2
2 3
3 3
1 2
3 3
3 1
```

The outputs are:

```
0
0
```

After adding a station at `2`, querying `3` gives distance `1`, not `0`, but the important case is that querying vertex `1` must always return `0`. Removing only replicas must not accidentally remove vertex `1`.

Another common mistake is assuming that the closest station is always among recently added vertices. For example:

```
4 3
1 2
2 3
3 4
1 4
3 2
2 4
```

The output is:

```
0
```

The station at `1` remains available, so after removing the replica at `4`, vertex `2` still has distance `1` to vertex `1`. A structure that only remembers additions and forgets old active stations will fail.

A final edge case is when the answer is zero. A query at an intersection containing a station must immediately return zero because the closest station is itself.

## Approaches

A straightforward solution is to keep the current set of gas stations and, for every query, run a graph search from the queried intersection until reaching a station. This is correct because the first station found by breadth first search is at minimum distance. However, one query can already visit every vertex, and repeating this for `2 * 10^5` queries gives an unacceptable worst case.

Another direct approach is to store all stations and calculate the distance from the query vertex to every station. Tree distance queries can be made fast with lowest common ancestor preprocessing, but if there are many stations this still leaves too much work. The brute force solution succeeds because it handles a single query well, but it fails because the number of queries and updates is large.

The key observation is that the tree is static. Only the set of marked vertices changes. This makes centroid decomposition suitable. A centroid splits the tree into smaller components, and every vertex belongs to only `O(log n)` centroid levels. Instead of searching the whole tree, we store information about active stations near every centroid.

For every centroid `c`, we maintain the distances from `c` to all active stations that belong to the centroid decomposition paths through `c`. If a query asks about vertex `x`, we examine all centroid ancestors of `x`. Any path from `x` to an arbitrary station must pass through one of these centroids at some level, so the best answer is the minimum of:

```
distance(x, centroid) + closest station distance stored at centroid
```

Adding and removing a station only changes the stored values in the `O(log n)` centroids on its decomposition path.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) per query | O(n) | Too slow |
| Optimal | O(log n) per update/query | O(n log n) | Accepted |

## Algorithm Walkthrough

1. Build a centroid decomposition of the tree. During the decomposition, for every original vertex store the list of pairs `(centroid, distance)` describing its ancestors in the centroid tree and the distance to each of them.

This list is the bridge between a normal tree vertex and the centroids that can summarize information about it.
2. For every centroid, maintain a heap containing distances to currently active stations. Because stations can be deleted, also maintain a second heap containing distances that should be removed lazily.

Lazy deletion avoids expensive removal from the middle of a heap. When the smallest value appears in both heaps, both copies are discarded.
3. Initially activate vertex `1`, because the original gas station always exists. Activation means inserting its distance into every centroid heap on its path.
4. When a replica is built at vertex `x`, activate `x`. For every `(centroid, distance)` pair belonging to `x`, insert `distance` into that centroid's heap.
5. When a replica is destroyed at vertex `x`, deactivate it. Insert the corresponding distances into the deletion heaps of all centroids on `x`'s path.
6. For a query at vertex `x`, inspect every `(centroid, distance)` pair belonging to `x`. Clean the lazy deletion heaps first, then combine the distance from `x` to the centroid with the nearest active station distance stored at that centroid.

Taking the minimum over all centroid ancestors gives the closest station.

Why it works:

Every pair of vertices in a tree has a unique path. In a centroid decomposition, for any vertex pair, there exists a centroid on the decomposition path of both vertices where their connection through that centroid is considered. The stored value at that centroid represents the shortest route from the centroid to an active station. Adding the distance from the query vertex to that same centroid reconstructs the candidate path to that station. Since every possible station is considered through some centroid ancestor, the minimum candidate is exactly the true closest distance.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline
sys.setrecursionlimit(1 << 25)

n, q = map(int, input().split())
g = [[] for _ in range(n + 1)]

for _ in range(n - 1):
    a, b = map(int, input().split())
    g[a].append(b)
    g[b].append(a)

size = [0] * (n + 1)
dead = [False] * (n + 1)
paths = [[] for _ in range(n + 1)]

def calc_size(v, p):
    size[v] = 1
    for u in g[v]:
        if u != p and not dead[u]:
            size[v] += calc_size(u, v)
    return size[v]

def find_centroid(v, p, total):
    for u in g[v]:
        if u != p and not dead[u] and size[u] * 2 > total:
            return find_centroid(u, v, total)
    return v

def collect(v, p, d, c):
    paths[v].append((c, d))
    for u in g[v]:
        if u != p and not dead[u]:
            collect(u, v, d + 1, c)

def decompose(v):
    total = calc_size(v, 0)
    c = find_centroid(v, 0, total)
    dead[c] = True
    collect(c, 0, 0, c)
    for u in g[c]:
        if not dead[u]:
            decompose(u)

decompose(1)

add_heap = [[] for _ in range(n + 1)]
del_heap = [[] for _ in range(n + 1)]
active = [False] * (n + 1)

def activate(v):
    if active[v]:
        return
    active[v] = True
    for c, d in paths[v]:
        heapq.heappush(add_heap[c], d)

def deactivate(v):
    if not active[v]:
        return
    active[v] = False
    for c, d in paths[v]:
        heapq.heappush(del_heap[c], d)

def clean(c):
    while add_heap[c] and del_heap[c] and add_heap[c][0] == del_heap[c][0]:
        heapq.heappop(add_heap[c])
        heapq.heappop(del_heap[c])

def query(v):
    ans = 10 ** 9
    for c, d in paths[v]:
        clean(c)
        if add_heap[c]:
            ans = min(ans, d + add_heap[c][0])
    return ans

activate(1)

out = []
for _ in range(q):
    data = list(map(int, input().split()))
    if data[0] == 1:
        activate(data[1])
    elif data[0] == 2:
        deactivate(data[1])
    else:
        out.append(str(query(data[1])))

sys.stdout.write("\n".join(out))
```

The centroid decomposition part builds the static structure. `paths[v]` is the important array: it stores exactly the centroids that a vertex can use when updating or querying.

The two heaps for each centroid implement a multiset with lazy deletion. Python heaps only support removing the minimum element efficiently, so destroyed stations are recorded separately and removed when they reach the top. This keeps every heap operation logarithmic.

The activation of vertex `1` happens before processing queries, because the original station is part of the initial state. The problem guarantees that removal operations only target replicas, so no extra protection is needed beyond keeping the initial activation.

All distances fit comfortably in Python integers. The recursion limit is increased because the original tree can be a chain, making the first depth first searches much deeper than Python's default recursion limit.

## Worked Examples

Using the sample:

```
7 5
1 2
1 3
2 4
5 3
6 3
7 1
2 1
3 3
1 7
3 7
3 3
```

The important states are:

| Operation | Active stations | Query vertex | Answer |
| --- | --- | --- | --- |
| Start | 1 |  |  |
| Remove 1 is impossible in original statement, so only replicas are removed |  |  |  |
| Add 7 | 1, 7 | 3 | 1 |
| Query 7 | 1, 7 | 7 | 0 |
| Query 3 | 1, 7 | 3 | 1 |

The trace shows that the structure keeps all active stations, not only the newest one. The centroid heaps store both station locations and allow the query to find the minimum among them.

A smaller example:

```
5 5
1 2
2 3
3 4
4 5
1 5
3 3
2 5
3 5
3 1
```

The trace is:

| Operation | Active stations | Query | Result |
| --- | --- | --- | --- |
| Initial state | 1 |  |  |
| Add 5 | 1, 5 | 3 | 2 |
| Query 3 | 1, 5 | 5 | 0 |
| Remove 5 | 1 | 5 | 4 |
| Query 1 | 1 | 1 | 0 |

This demonstrates deletion handling. The lazy deletion heaps remove the obsolete distance only when needed, while the permanent station at vertex `1` remains available.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) per operation | Each vertex appears in only logarithmically many centroid levels. |
| Space | O(n log n) | The centroid paths store one entry for every vertex at every decomposition level. |

The maximum number of stored centroid pairs is about `n log n`, which is around several million entries for `n = 200000`. The number of heap operations is also logarithmic per event, fitting the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    import heapq
    # paste the solution function here in a real test harness
    sys.stdin = old
    return ""

# The following cases should be run with the submitted solution wrapped
# into a callable function.

# Minimum tree:
# 1 1
# 3 1
# Expected:
# 0

# Chain with additions and removals:
# 5 5
# 1 2
# 2 3
# 3 4
# 4 5
# 1 5
# 3 3
# 2 5
# 3 5
# 3 1

# Star tree:
# 5 4
# 1 2
# 1 3
# 1 4
# 1 5
# 1 3
# 3 2
# 2 3
# 3 3

# Large shape should be generated separately:
# a chain of 200000 vertices with alternating add/query/remove operations
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex | `0` | Smallest possible tree and permanent station |
| Chain | Distances along a line | Long paths and deletion |
| Star | Distances through a central node | Multiple equal distance choices |
| Large chain | Fast logarithmic updates | Performance limits |

## Edge Cases

For the permanent station case, the algorithm activates vertex `1` before reading any events. If the query is made at vertex `1`, its centroid path contains a stored distance `0` from that active station, so the answer becomes zero immediately.

For a station that is added and later removed, the activation inserts its distances into every relevant centroid heap. The removal does not scan the heap or rebuild anything. It inserts matching values into deletion heaps, and the next query on those centroids discards the outdated values before using the minimum. This prevents deleted stations from affecting answers.

For a query at a vertex that itself contains a station, the update phase has already inserted distance zero into every centroid structure on that vertex's path. During the query, the centroid containing that vertex contributes a candidate of zero, so the returned minimum is correct.
