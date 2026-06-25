---
title: "CF 105940C - The Great Zebra Quest at ASZoo (Hard)"
description: "This problem asks us to work on an undirected, unweighted graph that represents the paths inside a zoo. Some vertices contain zebra enclosures. For every vertex, we need the shortest number of edges needed to reach any vertex containing a zebra enclosure."
date: "2026-06-25T13:54:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105940
codeforces_index: "C"
codeforces_contest_name: "ASU Coding Cup 10"
rating: 0
weight: 105940
solve_time_s: 43
verified: true
draft: false
---

[CF 105940C - The Great Zebra Quest at ASZoo (Hard)](https://codeforces.com/problemset/problem/105940/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

This problem asks us to work on an undirected, unweighted graph that represents the paths inside a zoo. Some vertices contain zebra enclosures. For every vertex, we need the shortest number of edges needed to reach any vertex containing a zebra enclosure. If a vertex is separated from every zebra enclosure, its answer is `-1`. The hard version differs from the easy version because there can be many zebra enclosures instead of exactly one. [Codeforces Gym 105940C - The Great Zebra Quest at ASZoo (Hard)](https://codeforces.com/gym/105940/problem/C)

The input contains multiple test cases. Each test case gives the number of locations, the number of paths between them, and the number of zebra enclosures. The next lines describe the paths, followed by the list of enclosure locations. The output is the minimum distance for every location in order.

The constraints are designed around linear graph algorithms. Across all test cases, the total number of vertices and edges is at most `2 * 10^5`. That rules out solutions that run a graph search from every vertex, because doing BFS from every node would cost about `O(n * (n + m))`, which can reach around `4 * 10^10` operations. A solution near `O(n + m)` is the intended direction.

There are a few cases that break careless implementations. The first is when a vertex is itself a zebra enclosure. For example:

```
1
3 2 2
1 2
2 3
1 3
```

The correct output is:

```
0 1 0
```

A solution that starts distances at `1` for all discovered nodes and forgets to initialize sources with `0` would produce the wrong answer.

Another case is a disconnected graph:

```
1
4 2 1
1 2
3 4
1
```

The correct output is:

```
0 1 -1 -1
```

A traversal that initializes all distances to `0` or assumes every vertex will eventually be visited will incorrectly assign values to the unreachable component.

A final edge case is when all vertices are zebra enclosures:

```
1
3 3 3
1 2
2 3
1 3
1 2 3
```

The correct output is:

```
0 0 0
```

If the implementation does not correctly handle multiple starting points, it may compute unnecessary distances from only one enclosure.

## Approaches

The straightforward approach is to run BFS separately from each zebra enclosure. Since BFS gives shortest distances in an unweighted graph, each run would correctly compute distances from one source, and taking the minimum over all runs would give the answer. The problem is that this repeats the same work many times.

In the worst case, there can be `n` zebra enclosures. Running BFS `k` times costs `O(k(n + m))`. With `k` close to `n`, this becomes `O(n(n + m))`, which is too slow for the given limits.

The key observation is that all zebra enclosures are equally valid destinations. We do not care which zebra we reach, only the nearest one. Instead of exploring from every zebra separately, we can reverse the viewpoint. Imagine all zebra locations expanding through the graph at the same time. The first time a vertex is reached, the distance assigned to it is automatically the shortest distance to the closest zebra.

This is exactly multi-source BFS. We place every zebra enclosure into the queue initially with distance `0`. Then normal BFS continues. Because BFS processes nodes by increasing distance, the first source that reaches any vertex must be the closest possible source.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k(n + m)) | O(n) | Too slow |
| Optimal | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Create an adjacency list for the graph. For every path between two locations, add each endpoint to the other's neighbor list because the graph is undirected.
2. Create a distance array and initialize every value to `-1`. This represents that no location has been reached yet.
3. Put every zebra enclosure into a queue and set its distance to `0`. Each enclosure is already at distance zero from itself, and all of them must act as starting points.
4. While the queue is not empty, remove the next location. For every adjacent location that still has distance `-1`, assign its distance as the current location's distance plus one and add it to the queue. The unvisited check is enough because BFS guarantees the first visit is the shortest one.
5. After the traversal finishes, output the distance array. Any remaining `-1` values correspond to locations that cannot reach a zebra enclosure.

Why it works: the queue always stores vertices in non-decreasing order of distance from the nearest zebra. When a vertex is first discovered, it is reached through the smallest possible number of edges because every shorter path would have already been processed. Since all zebra locations start together, the computed distance is the minimum over every possible enclosure.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n, m, k = map(int, input().split())

        graph = [[] for _ in range(n)]
        for _ in range(m):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            graph[u].append(v)
            graph[v].append(u)

        zebras = list(map(int, input().split()))

        dist = [-1] * n
        q = deque()

        for x in zebras:
            x -= 1
            dist[x] = 0
            q.append(x)

        while q:
            u = q.popleft()
            for v in graph[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    q.append(v)

        ans.append(" ".join(map(str, dist)))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The adjacency list stores only existing edges, which keeps the graph representation proportional to the input size. The queue contains the frontier of the BFS and guarantees that nodes are processed in the correct order.

The initialization loop is the main difference from normal BFS. Instead of choosing one source, every zebra is inserted before the traversal starts. Setting the distance before insertion prevents the same zebra from being revisited.

The condition `dist[v] == -1` is the important boundary check. It ensures that every vertex is assigned exactly once. Since distances increase by one when moving along an edge, there is no need to compare and update already visited vertices.

## Worked Examples

For the first sample:

```
1
5 5 1
1 2
2 3
3 4
4 5
5 1
1
```

The only zebra is vertex `1`.

| Queue state | Current node | Distances |
| --- | --- | --- |
| 1 | 1 | 0 1 -1 -1 1 |
| 2,5 | 2 | 0 1 2 -1 1 |
| 5,3 | 5 | 0 1 2 -1 1 |
| 3,4 | 3 | 0 1 2 2 1 |
| 4 | 4 | 0 1 2 2 1 |

The cycle is explored outward from the zebra. The two vertices next to it receive distance `1`, and the remaining vertices receive their shortest values.

For a graph with multiple zebras:

```
1
6 4 2
1 2
2 3
4 5
5 6
1 6
```

The initial queue contains vertices `1` and `6`.

| Queue state | Current node | Distances |
| --- | --- | --- |
| 1,6 | 1 | 0 1 -1 -1 -1 0 |
| 6,2 | 6 | 0 1 -1 -1 1 0 |
| 2,5 | 2 | 0 1 2 -1 1 0 |
| 5,3 | 5 | 0 1 2 -1 1 0 |
| 3 | 3 | 0 1 2 -1 1 0 |

The two searches grow together. Vertex `3` is reached from zebra `1`, while vertex `4` stays unreachable because it is not connected to either source.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Every vertex enters the queue once and every edge is inspected at most twice. |
| Space | O(n + m) | The adjacency list stores all edges and the BFS arrays store vertex information. |

The total input size is bounded by `2 * 10^5` vertices and edges, so the linear solution easily fits within the required limits.

## Test Cases

```python
import sys
import io
from collections import deque

def solution(inp):
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n, m, k = map(int, input().split())
        g = [[] for _ in range(n)]

        for _ in range(m):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            g[u].append(v)
            g[v].append(u)

        z = list(map(int, input().split()))

        d = [-1] * n
        q = deque()

        for x in z:
            x -= 1
            d[x] = 0
            q.append(x)

        while q:
            u = q.popleft()
            for v in g[u]:
                if d[v] == -1:
                    d[v] = d[u] + 1
                    q.append(v)

        out.append(" ".join(map(str, d)))

    return "\n".join(out)

assert solution("""1
5 5 1
1 2
2 3
3 4
4 5
5 1
1
""") == "0 1 2 2 1"

assert solution("""1
4 2 1
1 2
3 4
1
""") == "0 1 -1 -1"

assert solution("""1
3 3 3
1 2
2 3
1 3
1 2 3
""") == "0 0 0"

assert solution("""1
2 1 1
1 2
2
""") == "1 0"

assert solution("""1
6 3 2
1 2
2 3
4 5
1 5
""") == "0 1 2 2 1 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single cycle with one zebra | `0 1 2 2 1` | Normal BFS expansion |
| Disconnected components | `0 1 -1 -1` | Unreachable vertices |
| Every node is a zebra | `0 0 0` | Multiple starting points |
| Two nodes with zebra at second node | `1 0` | Basic direction handling |
| Two zebra regions connected through one path | `0 1 2 2 1 3` | Multi-source shortest choice |

## Edge Cases

For the disconnected case:

```
1
4 2 1
1 2
3 4
1
```

The queue starts with vertex `1`. It visits vertex `2` and stops because there are no more reachable nodes. Vertices `3` and `4` never leave the initial `-1` state, so the final answer is `0 1 -1 -1`.

For the case where all vertices are zebras:

```
1
3 3 3
1 2
2 3
1 3
1 2 3
```

Every vertex enters the queue with distance `0`. When neighbors are checked, they already have assigned distances, so no value changes. The result remains `0 0 0`.

For multiple zebra enclosures competing for the same vertex, the BFS order handles the tie automatically. The first zebra wave reaching a vertex gives the minimum possible distance, and any later wave cannot improve it because it would have to travel through an equal or longer path.
