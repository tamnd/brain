---
title: "CF 102448H - Hellcife is on fire"
description: "Think of each city as a vertex and each road as an undirected weighted edge. City (v) has an additional delay (Tv): once the fire reaches (v), the city does not become completely burnt immediately. It takes another (Tv) seconds. Initially, several cities are ignited at time (0)."
date: "2026-08-09T18:22:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102448
codeforces_index: "H"
codeforces_contest_name: "UFPE Starters Final Try-Outs 2020"
rating: 0
weight: 102448
solve_time_s: 635
verified: true
draft: false
---

[CF 102448H - Hellcife is on fire](https://codeforces.com/problemset/problem/102448/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 10m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

Think of each city as a vertex and each road as an undirected weighted edge. City (v) has an additional delay (T_v): once the fire reaches (v), the city does not become completely burnt immediately. It takes another (T_v) seconds.

Initially, several cities are ignited at time (0). For every city, we need the exact time when that city becomes completely burnt.

Suppose city (u) becomes completely burnt at time (D_u), and there is a road of length (w) from (u) to (v). Fire can reach (v) at time (D_u+w), and then (v) needs another (T_v) seconds to burn completely. Thus this route would make (v) completely burnt at

[
D_u+w+T_v.
]

For an initially ignited city (s), there is no road traversal before the fire reaches it, so its burning time is simply

[
D_s=T_s.
]

The graph can contain up to (10^5) cities and (10^5) roads. With this size, anything quadratic in the number of cities is already too expensive. Even scanning all roads (10^5) times would require around (10^{10}) adjacency examinations, far beyond a one-second limit. We need an algorithm close to (O((N+M)\log N)).

The road lengths and all (T_i) values are positive, so all times are nonnegative. The graph is connected, so every city will eventually burn.

There are several edge cases that can easily lead to incorrect answers.

First, an initially ignited city is not completely burnt at time (0). For example:

```
2 1 1
1 2 5
7 3
1
```

The correct output is

```
7
15
```

City 1 starts burning at time (0), finishes at time (7), and only then does the fire travel for (5) seconds to city 2. City 2 then needs (3) more seconds. An implementation that initializes the source distance to zero would incorrectly obtain (0) and (8).

Second, the burning delay of every intermediate city matters. Consider:

```
2 1 1
1 2 5
10 1
1
```

The correct output is

```
10
16
```

The fire spends (10) seconds burning city 1, travels for (5) seconds, and then spends (1) second burning city 2. Treating the problem as an ordinary shortest path and adding only the destination's (T_v) would give (6), which is wrong because city 1 has to finish burning before it can spread fire.

Third, there can be several initially ignited cities. The earliest one to reach a city determines its answer. For example:

```
3 2 2
1 2 10
2 3 1
1 1 1
1 3
```

The correct output is

```
1
3
1
```

City 2 is reached from city 3 after (1) second, and then takes another (1) second to burn, so its answer is (2), actually making the complete output

```
1
2
1
```

A solution that only starts from the first source would miss this faster route.

Finally, parallel roads must be treated independently. Sample 2 contains multiple roads connecting the same pair of cities with different lengths. The shortest such road can completely change the answer, so an implementation must not collapse parallel edges without retaining the minimum one.

## Approaches

A direct approach is to process every initially burning city separately. For one source (s), we can run a shortest-path algorithm whose transition from (u) to (v) costs

[
w(u,v)+T_v.
]

The source starts with distance (T_s). This gives the correct burning time from that particular source, and after processing all (K) sources we take the minimum answer for every city.

This approach is correct, but it repeats almost the entire graph search for every source. A Dijkstra run takes (O((N+M)\log N)), so processing all sources costs

[
O(K(N+M)\log N).
]

In the worst case (K=N=M=10^5), the algorithm may examine roughly (2KM=2\cdot10^{10}) adjacency entries before even accounting for heap operations. That is far too much for the time limit.

The key observation is that all sources use exactly the same graph and the same transition rule. We do not actually care which source produced the optimal path. We only care about the earliest possible burning time for each city.

This is precisely the situation where Dijkstra can start from multiple sources simultaneously. Instead of running one Dijkstra from every source, initialize every initially burning city with its own value (T_s), put all of them into the same priority queue, and let them compete to reach the remaining cities.

For a current city (u) with finalized burning time (D_u), traversing an edge of length (w) to (v) produces the candidate

[
D_u+w+T_v.
]

The quantity (w+T_v) is always positive, so the resulting state graph has nonnegative edge costs and Dijkstra's greedy choice remains valid.

The brute-force method works because each individual source can be handled by Dijkstra, but it fails when there are many sources because it repeats the same work. The observation that all sources can participate in one shortest-path computation lets us replace (K) Dijkstra runs with one multi-source Dijkstra.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Run Dijkstra once per source | (O(K(N+M)\log N)) | (O(N+M)) | Too slow |
| Multi-source Dijkstra | (O((N+M)\log N)) | (O(N+M)) | Accepted |

## Algorithm Walkthrough

1. Store every road in an adjacency list. For a road between (u) and (v) with length (w), add ((v,w)) to (u)'s list and ((u,w)) to (v)'s list because the road is undirected.
2. Create an array (dist), where (dist[v]) represents the earliest time at which city (v) is completely burnt. Initially every value is infinity because we have not found a route to that city.
3. For every initially ignited city (s), set

[
dist[s]=T_s.
]

Push every such city into the priority queue with key (T_s).

The value is (T_s), rather than zero, because the city starts burning at time zero but becomes completely burnt only after its own burning delay.

1. Repeatedly remove the city (u) with the smallest tentative burning time from the priority queue.

If the extracted value is larger than the current (dist[u]), discard it. This is a stale heap entry created by an earlier, worse relaxation.

1. For every road from (u) to (v) with length (w), compute

[
candidate=dist[u]+w+T_v.
]

The first term is when (u) finishes burning, the second term is the time needed for the fire to cross the road, and the third term is the time needed to burn (v).

1. If the candidate is smaller than (dist[v]), replace (dist[v]) with the candidate and push the new pair into the priority queue.
2. When the priority queue is empty, every city has its minimum possible burning time because the graph is connected. Output the values in city order.

### Why it works

The invariant is that whenever Dijkstra permanently processes a city (u), (dist[u]) is the minimum possible complete-burning time for (u) from any initially ignited city.

Consider any possible route from an initial source to (u). The source contributes its (T) value, every road contributes its length, and every city entered after the source contributes its own (T) value. Thus every route corresponds exactly to a path in an auxiliary directed graph whose transition from (u) to (v) has cost (w(u,v)+T_v), with each source initialized to (T_s).

All these transition costs are positive. Dijkstra therefore finalizes vertices in nondecreasing order of their true shortest-path cost. Since all sources are inserted initially, the shortest path can start at whichever source is best for that city. Consequently, the final (dist[v]) is exactly the earliest time at which (v) can become completely burnt.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())

    graph = [[] for _ in range(n)]

    for _ in range(m):
        a, b, c = map(int, input().split())
        a -= 1
        b -= 1
        graph[a].append((b, c))
        graph[b].append((a, c))

    t = list(map(int, input().split()))

    sources = list(map(int, input().split()))

    INF = 10**30
    dist = [INF] * n
    pq = []

    for x in sources:
        x -= 1
        if t[x] < dist[x]:
            dist[x] = t[x]
            heapq.heappush(pq, (t[x], x))

    while pq:
        cur, u = heapq.heappop(pq)

        if cur != dist[u]:
            continue

        for v, w in graph[u]:
            candidate = cur + w + t[v]

            if candidate < dist[v]:
                dist[v] = candidate
                heapq.heappush(pq, (candidate, v))

    sys.stdout.write("\n".join(map(str, dist)))

if __name__ == "__main__":
    solve()
```

The adjacency list represents the original road network. Each road is inserted in both directions because the fire can travel along it either way.

The initialization is the main difference from ordinary single-source Dijkstra. Every initial source enters the heap simultaneously, with priority (T_s). If the same city appears more than once among the sources, the repeated initialization has no harmful effect because all occurrences have the same value.

The relaxation formula is the central part of the implementation:

```
candidate = cur + w + t[v]
```

Here `cur` is the time when the current city is completely burnt. The fire then spends `w` seconds crossing the road and `t[v]` seconds burning the destination city.

The stale-entry check

```
if cur != dist[u]:
    continue
```

is necessary because Python's `heapq` does not provide a decrease-key operation. When a better distance is discovered, we push another entry instead of modifying the old one. The old entry eventually comes out of the heap and must be ignored.

Python integers have arbitrary precision, so there is no overflow issue. The maximum useful answer is comfortably within ordinary 64-bit integer range anyway, but using `10**30` as infinity keeps the implementation simple.

The graph has at most (10^5) edges, so the adjacency list stores at most (2\cdot10^5) directed adjacency entries. The heap contains at most a linear number of useful or stale entries over the execution, which is appropriate for the memory limit.

## Worked Examples

### Sample 1

The input has one initial source, city 1. Its burning delay is (T_1=1), so city 1 is completely burnt at time 1.

The following table shows the meaningful Dijkstra operations.

| Popped city | `dist[u]` | Edge considered | Candidate | Updated `dist` |
| --- | --- | --- | --- | --- |
| 1 | 1 | (1\to2), length 1 | (1+1+2=4) | (dist[2]=4) |
| 1 | 1 | (1\to5), length 13 | (1+13+5=19) | (dist[5]=19) |
| 2 | 4 | (2\to3), length 4 | (4+4+3=11) | (dist[3]=11) |
| 3 | 11 | (3\to4), length 5 | (11+5+4=20) | (dist[4]=20) |
| 5 | 19 | (5\to4), length 10 | (19+10+4=33) | no change |
| 4 | 20 | remaining edges | no improvement | no change |

The final distances are

```
1
4
11
20
19
```

The interesting part is city 5. It can be reached directly from city 1, giving (1+13+5=19), which is faster than reaching it through cities 2, 3, and 4. Dijkstra does not need to know this route in advance. It discovers both possibilities and keeps the smaller value.

### Sample 2

There is one initial source, city 2, with (T_2=94560). Therefore the initial heap contains

[
(94560,2).
]

City 2 has several parallel roads to other cities. The best candidate for each neighboring city is calculated independently.

| Popped city | `dist[u]` | Best transition | Candidate | Updated city |
| --- | --- | --- | --- | --- |
| 2 | 94560 | (2\to1), length 25722 | (94560+25722+31551=151833) | 1 |
| 2 | 94560 | (2\to3), length 3043 | (94560+3043+84171=181774) | 3 |
| 2 | 94560 | (2\to4), length 49102 | (94560+49102+16742=160404) | 4 |
| 2 | 94560 | (2\to5), length 41563 | (94560+41563+55756=191879) | 5 |
| 1 | 151833 | edges from 1 | all candidates larger | none |
| 4 | 160404 | edges from 4 | all candidates larger | none |
| 3 | 181774 | edge (3\to5), length 32836 | (270366) | none |
| 5 | 191879 | remaining edges | all candidates larger | none |

The final values are

```
151833
94560
181774
160404
191879
```

This example also demonstrates why parallel edges cannot simply be ignored. City 2 has three different roads to city 1, and the road of length (25722) gives a substantially better candidate than the roads of lengths (50743) and (81271).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O((N+M)\log N)) | Each relaxation is processed through a binary heap, and the graph has (O(M)) adjacency entries |
| Space | (O(N+M)) | The adjacency list, distance array, and priority queue are all linear in the graph size |

With (N,M\le 10^5), the algorithm performs one graph traversal with heap operations rather than up to (10^5) separate traversals. The (O((N+M)\log N)) bound is appropriate for the one-second limit, and the (O(N+M)) memory usage fits comfortably within 256 MB.

## Test Cases

```python
import sys
import io
import heapq

def solve():
    input = sys.stdin.readline

    n, m, k = map(int, input().split())
    graph = [[] for _ in range(n)]

    for _ in range(m):
        a, b, c = map(int, input().split())
        a -= 1
        b -= 1
        graph[a].append((b, c))
        graph[b].append((a, c))

    t = list(map(int, input().split()))
    sources = list(map(int, input().split()))

    INF = 10**30
    dist = [INF] * n
    pq = []

    for x in sources:
        x -= 1
        if t[x] < dist[x]:
            dist[x] = t[x]
            heapq.heappush(pq, (t[x], x))

    while pq:
        cur, u = heapq.heappop(pq)

        if cur != dist[u]:
            continue

        for v, w in graph[u]:
            candidate = cur + w + t[v]

            if candidate < dist[v]:
                dist[v] = candidate
                heapq.heappush(pq, (candidate, v))

    sys.stdout.write("\n".join(map(str, dist)))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

sample1 = """\
5 5 1
1 2 1
2 3 4
3 4 5
4 5 10
1 5 13
1 2 3 4 5
1
"""

assert run(sample1) == """\
1
4
11
20
19
""", "sample 1"

sample2 = """\
5 18 1
1 3 14877
2 1 81271
1 2 50743
5 1 46485
2 5 41563
5 4 72606
1 2 88401
5 3 56633
2 1 25722
3 1 78857
2 3 95527
5 4 66046
1 4 87400
4 2 49102
3 2 3043
5 3 32836
3 2 13703
4 1 86008
31551 94560 84171 16742 55756
2
"""

assert run(sample2) == """\
151833
94560
181774
160404
191879
""", "sample 2"

sample3 = """\
7 12 2
6 3 61451
3 5 48225
3 6 18732
5 3 86896
1 5 73979
4 3 49294
3 1 2794
1 5 3449
7 2 86351
4 6 59862
2 1 38972
3 7 20293
36685 6614 81280 91835 68491 81662 10505
2 1
"""

assert run(sample3) == """\
36685
6614
120759
261888
108625
221153
103470
""", "sample 3"

# Minimum valid connected graph, source is city 1.
custom1 = """\
2 1 1
1 2 1
1 1
1
"""

assert run(custom1) == """\
1
3
""", "minimum-size case"

# Source has a large burning time. The destination cannot start
# spreading before the source has completely burnt.
custom2 = """\
2 1 1
1 2 5
10 1
1
"""

assert run(custom2) == """\
10
16
""", "intermediate burning time"

# Multiple sources. City 3 is much closer to city 2 than city 1.
custom3 = """\
3 2 2
1 2 10
2 3 1
1 1 1
1 3
"""

assert run(custom3) == """\
1
2
1
""", "multiple sources"

# Parallel edges with the same endpoints. The shorter road must win.
custom4 = """\
3 3 1
1 2 100
1 2 1
2 3 1
1 1 1
1
"""

assert run(custom4) == """\
1
3
5
""", "parallel edges"

# Large boundary case generated programmatically.
n = 100000
parts = [f"{n} {n - 1} 1"]
for i in range(1, n):
    parts.append(f"{i} {i + 1} 1")
parts.append(" ".join(["1"] * n))
parts.append("1")

large_input = "\n".join(parts) + "\n"
large_output = run(large_input)

expected_large = "\n".join(str(2 * i - 1) for i in range(1, n + 1)) + "\n"
assert large_output == expected_large, "maximum-size case"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 1`, one edge of length 1 | `1, 3` | Minimum valid connected graph and source initialization |
| `2 1 1`, edge 5, (T=[10,1]) | `10, 16` | Burning delay of an intermediate city |
| Three cities with two initial sources | `1, 2, 1` | Competition between multiple sources |
| Three cities with parallel edges | `1, 3, 5` | Choosing the shortest parallel road |
| Chain of (100000) cities | `1, 3, 5, ..., 199999` | Maximum-size graph, unit weights, and performance |

## Edge Cases

The first edge case is an initially ignited city. Consider

```
2 1 1
1 2 1
1 1
1
```

The algorithm initializes `dist[1]` to (T_1=1), not zero. It pops city 1 with time 1 and obtains

[
1+1+1=3
]

for city 2. The output is therefore

```
1
3
```

The source initialization directly captures the fact that ignition and complete burning are different events.

The second edge case is an intermediate city with a large burning delay:

```
2 1 1
1 2 5
10 1
1
```

The only initial distance is (10). When city 1 is processed, the transition to city 2 costs (5+1=6), giving (10+6=16). The output is

```
10
16
```

A shortest-path formulation that charged only road lengths would incorrectly allow city 1 to spread fire immediately at time zero.

The third edge case has multiple sources:

```
3 2 2
1 2 10
2 3 1
1 1 1
1 3
```

The heap starts with `(1, city 1)` and `(1, city 3)`. City 3 reaches city 2 after one second, then city 2 burns for one second, giving `dist[2]=2`. City 1 would reach city 2 much later, at (1+10+1=12), so the second source wins. The final result is

```
1
2
1
```

The multi-source initialization is exactly what lets Dijkstra choose this better source without running a separate search.

The fourth edge case contains parallel roads:

```
3 3 1
1 2 100
1 2 1
2 3 1
1 1 1
1
```

From city 1, the road of length 1 gives city 2 a burning time of (1+1+1=3). The road of length 100 is never competitive. City 3 then receives fire from city 2 and finishes at (3+1+1=5). The output is

```
1
3
5
```

The adjacency list retains both roads, so the shorter one naturally wins during relaxation.

The final boundary case is the chain of (100000) cities with every road length and every (T_i) equal to 1. Starting from city 1 gives

[
dist[1]=1,
]

and every subsequent city adds exactly (1+1=2). Thus city (i) has answer

[
2i-1.
]

The last city has answer (199999). The algorithm processes this entire graph with one Dijkstra run, demonstrating that the intended complexity remains practical even at the largest input size.

If you'd like, I can also turn this into a more typical Codeforces editorial style with a shorter proof and a more intuitive derivation of the modified Dijkstra state.
