---
title: "CF 106113B - La campa\u00f1a de Bob"
description: "Bob wants to spread a message through a network of cities. The cities are vertices of an undirected graph, and an edge means that information can move between two neighboring cities in one week. Bob does not need to visit every city. He has only two possible visiting orders."
date: "2026-06-25T11:37:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106113
codeforces_index: "B"
codeforces_contest_name: "Coding Cup TecNM 2025"
rating: 0
weight: 106113
solve_time_s: 39
verified: true
draft: false
---

[CF 106113B - La campa\u00f1a de Bob](https://codeforces.com/problemset/problem/106113/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

Bob wants to spread a message through a network of cities. The cities are vertices of an undirected graph, and an edge means that information can move between two neighboring cities in one week.

Bob does not need to visit every city. He has only two possible visiting orders. In the first order, he visits cities with odd indices from smaller to larger indices. In the second order, he visits cities with even indices from smaller to larger indices. A city visited in week `k` becomes an additional starting point for spreading information during that week. Every following week, informed voters pass the message to their neighbors.

The task is to choose the better of the two strategies and output the number of weeks needed until every city knows the message. If neither strategy can eventually reach every city, the answer is `-1`.

The important observation is that a city visited later can still be useful. For example, visiting a disconnected component after some weeks allows the message to start there, even though the component could not be reached from earlier visits.

The graph can contain up to `100000` cities, so an approach that simulates every week and repeatedly spreads the message is too expensive. With this size, we need roughly linear or `O((n+m) log n)` work. Running a graph traversal once or twice is acceptable, but doing a separate traversal after every visit is not.

There are a few edge cases that easily break an implementation. If there is only one city, the answer is `1` because Bob must visit it once.

```
Input:
1 0
```

The correct output is:

```
1
```

A solution that only starts a BFS from existing edges or assumes at least one neighbor would fail.

Another case is when one strategy never visits a disconnected component. For example:

```
Input:
4 1
1 2
```

Using only odd cities visits `1` and `3`, so cities `3` and `4` can be covered only if they are reached from those visits. City `4` is isolated and never receives the message. The same issue may happen for the even strategy. The answer is `-1` if neither strategy covers all cities.

A final subtle case is that the visiting time matters. A city visited in week `3` cannot spread information before week `3`. Treating all visited cities as if they were available at week `1` gives an incorrect result.

## Approaches

A direct solution would simulate the campaign week by week. For one chosen strategy, we know which city Bob visits in each week. After every visit, we could run a BFS from all currently informed cities and check whether the whole graph is covered. This is correct because it follows the exact process described in the statement.

The problem is that the same edges would be explored many times. In the worst case, Bob visits about `n/2` cities, and a BFS costs `O(n+m)`. The total work becomes roughly `O(n(n+m))`, which is far beyond what is possible for `n = 100000`.

The key observation is that the entire process can be viewed as shortest paths with delayed starting points.

If Bob visits city `u` in week `t`, then that city can inform another city `v` in:

```
t + shortest_distance(u, v)
```

weeks.

For a fixed strategy, every visited city is a source with a different starting time. We need the minimum arrival time among all sources. This is exactly a shortest path problem where all edges have weight `1`, but each source starts with its own initial distance. We can solve it with a multi-source BFS style traversal using a priority queue.

For odd cities, city `i` is visited in week `(i+1)/2`. For even cities, city `i` is visited in week `i/2`. We initialize the priority queue with all cities from the chosen strategy and their visit weeks, then propagate the earliest possible arrival times.

The same algorithm handles both strategies. We only need to run it twice and take the smaller valid answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n(n+m)) | O(n+m) | Too slow |
| Optimal | O((n+m) log n) | O(n+m) | Accepted |

## Algorithm Walkthrough

1. Build the adjacency list of the city graph. Each edge is stored in both directions because information can travel either way.
2. Solve the problem once for the odd-city strategy. Put every odd-numbered city into a priority queue with its visiting week as the initial arrival time.
3. Run a shortest path traversal. Whenever a city with arrival time `t` is removed from the queue, try to improve each neighbor to time `t+1`. If this gives a better time, update the neighbor and push it into the queue.
4. After the traversal finishes, find the largest arrival time among all cities. If some city still has infinite arrival time, this strategy cannot inform the whole graph.
5. Repeat the same process for the even-city strategy. The only difference is the initial week assigned to each source city.
6. Return the smaller valid result from the two strategies. If both strategies fail, return `-1`.

Why it works:

For a fixed strategy, every visited city is a possible starting point for the message. The priority queue algorithm always keeps the smallest known week when each city can become informed. Because every edge adds exactly one week, the relaxation step considers every possible path from every source. The final value for each city is the minimum over all possible visited cities of:

```
visit_week + graph_distance
```

This is exactly the earliest week when the city can receive the message. Taking the maximum of these values gives the week when the last city becomes informed.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve_strategy(n, graph, start_parity):
    inf = 10**18
    dist = [inf] * (n + 1)
    pq = []

    for city in range(1, n + 1):
        if city % 2 == start_parity:
            week = (city + 1) // 2 if city % 2 == 1 else city // 2
            dist[city] = week
            heapq.heappush(pq, (week, city))

    while pq:
        time, u = heapq.heappop(pq)

        if time != dist[u]:
            continue

        for v in graph[u]:
            if dist[v] > time + 1:
                dist[v] = time + 1
                heapq.heappush(pq, (dist[v], v))

    ans = max(dist[1:])
    if ans == inf:
        return -1
    return ans

def main():
    n, m = map(int, input().split())

    graph = [[] for _ in range(n + 1)]

    for _ in range(m):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

    odd = solve_strategy(n, graph, 1)
    even = solve_strategy(n, graph, 0)

    if odd == -1:
        print(even)
    elif even == -1:
        print(odd)
    else:
        print(min(odd, even))

if __name__ == "__main__":
    main()
```

The function `solve_strategy` contains the whole graph algorithm. Its `start_parity` argument decides which cities Bob visits. The initial distance array is not a normal BFS initialization, because each source has a different starting time. A city visited in week `k` starts with distance `k`, not `0`.

The priority queue is used instead of a normal queue because the initial values are different. A normal BFS works when all sources begin simultaneously, but here a city visited in week `1` must always be processed before one visited in week `20` if both are waiting to expand.

The stale entry check:

```
if time != dist[u]:
    continue
```

is necessary because a city can be inserted into the queue multiple times after finding better paths. Only the newest shortest value should expand.

The final maximum arrival time is the answer for one strategy. If it remains infinite, some city cannot be reached by any visited city in that strategy.

## Worked Examples

### Sample 1

Input:

```
6 6
1 4
1 2
2 3
2 5
2 4
3 6
```

For the odd strategy, Bob visits `1`, `3`, `5`.

| City | Initial week | Final arrival week |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | - | 2 |
| 3 | 2 | 2 |
| 4 | - | 3 |
| 5 | 3 | 3 |
| 6 | - | 3 |

The last city receives the message in week `3`.

For the even strategy, the last city needs more time, so the answer is `3`.

This example shows why different visit orders matter. The first strategy reaches the central part of the graph earlier.

### Sample 2

Input:

```
6 6
1 4
1 2
2 3
2 4
2 5
2 6
```

For the odd strategy, Bob visits `1`, `3`, `5`.

| City | Initial week | Final arrival week |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | - | 2 |
| 3 | 2 | 2 |
| 4 | - | 3 |
| 5 | 3 | 3 |
| 6 | - | 3 |

The campaign finishes in week `3`.

For the even strategy, Bob visits `2`, `4`, `6`.

| City | Initial week | Final arrival week |
| --- | --- | --- |
| 1 | - | 2 |
| 2 | 1 | 1 |
| 3 | - | 2 |
| 4 | 2 | 2 |
| 5 | - | 2 |
| 6 | 3 | 3 |

The second strategy also finishes in week `3`, so the answer remains `3`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n+m) log n) | Each city and edge is processed through the priority queue traversal for each of the two strategies. |
| Space | O(n+m) | The adjacency list stores the graph and the arrays store arrival times. |

The constraints allow this complexity because the graph is traversed only twice. The algorithm avoids repeating BFS after every Bob visit.

## Test Cases

```python
import sys
import io
import heapq

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve_strategy(n, graph, parity):
        inf = 10**18
        dist = [inf] * (n + 1)
        pq = []

        for i in range(1, n + 1):
            if i % 2 == parity:
                t = (i + 1) // 2 if i % 2 else i // 2
                dist[i] = t
                heapq.heappush(pq, (t, i))

        while pq:
            t, u = heapq.heappop(pq)
            if t != dist[u]:
                continue
            for v in graph[u]:
                if dist[v] > t + 1:
                    dist[v] = t + 1
                    heapq.heappush(pq, (t + 1, v))

        return -1 if max(dist[1:]) == inf else max(dist[1:])

    n, m = map(int, input().split())
    graph = [[] for _ in range(n + 1)]

    for _ in range(m):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

    a = solve_strategy(n, graph, 1)
    b = solve_strategy(n, graph, 0)

    if a == -1:
        ans = b
    elif b == -1:
        ans = a
    else:
        ans = min(a, b)

    sys.stdin = old_stdin
    return str(ans) + "\n"

assert run("""6 6
1 4
1 2
2 3
2 5
2 4
3 6
""") == "3\n", "sample 1"

assert run("""6 6
1 4
1 2
2 3
2 4
2 5
2 6
""") == "3\n", "sample 2"

assert run("""1 0
""") == "1\n", "single city"

assert run("""4 1
1 2
""") == "-1\n", "disconnected graph"

assert run("""5 4
1 2
2 3
3 4
4 5
""") == "3\n", "path graph"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0` | `1` | Minimum-size graph handling |
| `4 1` with edge `1 2` | `-1` | Impossible information spread |
| A path of five cities | `3` | Propagation through multiple edges |
| Provided samples | `3` | Strategy comparison |

## Edge Cases

For a single city:

```
Input:
1 0
```

The odd strategy visits city `1` in week `1`. The arrival array becomes `[1]`, so the maximum arrival time is `1`. The algorithm never depends on having edges, so it handles this case directly.

For disconnected graphs:

```
Input:
4 1
1 2
```

The odd strategy starts from cities `1` and `3`. City `4` is isolated and is not a starting city, so its distance stays infinite. The even strategy starts from city `2` and reaches only the first component. It also leaves city `4` unreachable. Since both strategies contain an infinite arrival time, the answer is `-1`.

For delayed visits:

```
Input:
5 4
1 2
2 3
3 4
4 5
```

The even strategy visits city `2` in week `1` and city `4` in week `2`. City `5` can be reached from city `4` in week `3`, which is earlier than waiting for the odd strategy to visit city `5` in week `3`. The priority queue keeps these different starting times separate, so it does not incorrectly assume every source exists at week `1`.
