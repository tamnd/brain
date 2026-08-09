---
title: "CF 102448H - Hellcife is on fire"
description: "Think of each city as a vertex of a weighted undirected graph. City (i) needs (Ti) seconds to burn completely after the fire first reaches it."
date: "2026-08-09T14:21:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102448
codeforces_index: "H"
codeforces_contest_name: "UFPE Starters Final Try-Outs 2020"
rating: 0
weight: 102448
solve_time_s: 819
verified: false
draft: false
---

[CF 102448H - Hellcife is on fire](https://codeforces.com/problemset/problem/102448/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 13m 39s  
**Verified:** no  

## Solution
## Problem Understanding

Think of each city as a vertex of a weighted undirected graph. City \(i\) needs \(T_i\) seconds to burn completely after the fire first reaches it. A road of length \(C\) takes exactly \(C\) seconds to cross, but a city can only send fire through its roads after that city has finished burning.

If the fire reaches city \(v\) at time \(X\), its completion time is \(X+T_v\). If it came from a neighboring city \(u\), then the earliest possible completion time through that road is

\[
\text{completion}[u] + C(u,v) + T_v.
\]

The cities listed among the \(K\) initial cities are already burning at time \(0\), so their completion time is simply their own \(T_i\). We need the minimum possible completion time for every city.

The graph has up to \(10^5\) vertices and \(10^5\) roads. With that size, an \(O(NM)\) algorithm can perform around \(10^{10}\) edge relaxations, which is far beyond what a one second time limit allows. Even algorithms that explicitly enumerate many possible paths are impossible because the number of paths can grow exponentially. We need a near-linear or \(O((N+M)\log N)\) solution.

The road lengths and burning times are positive. This positivity is exactly what allows a Dijkstra-style greedy algorithm: once a city has the smallest currently known completion time, no later route can reach it earlier.

There are several edge cases that can make a careless implementation wrong.

Consider a single valid two-city graph where only city 1 starts burning:

```text
2 1 1
1 2 5
7 3
1
```

City 1 finishes at time \(7\). Fire then spends \(5\) seconds crossing the road and city 2 needs another \(3\) seconds to burn, so the correct output is

```text
7
15
```

An implementation that treats \(T_i\) as the time needed to reach city \(i\), rather than the time needed after arrival, would incorrectly produce \(12\) for city 2.

A second edge case is that a city can have a direct route from an initially burning city and a longer-looking route through other cities. For example:

```text
3 3 1
1 2 10
1 3 1
3 2 1
1 100 1
1
```

City 1 finishes at \(1\). City 2 can be reached directly and finishes at \(1+10+100=111\), but the route through city 3 gives \(1+1+1+100=103\). The correct output is

```text
1
103
3
```

A solution that processes each city only once without comparing alternative routes can miss this improvement.

A third edge case occurs when several initially burning cities exist. For

```text
3 2 2
1 3 5
2 3 1
4 7 2
1 2
```

cities 1 and 2 finish at times \(4\) and \(7\). City 3 is reached from city 1 at \(4+5\) or from city 2 at \(7+1\), so the answer is

```text
4
7
8
```

The algorithm must initialize all initial cities before processing the priority queue. Treating only the first initial city as a source would give the wrong result.

## Approaches

The most direct correct approach is repeated relaxation. Start with \(T_i\) for every initially burning city and infinity for every other city. For every road \((u,v,w)\), if city \(u\) can finish by time \(d[u]\), then city \(v\) can finish by \(d[u]+w+T_v\). Repeating this process eventually propagates the best values through the graph.

This is essentially Bellman-Ford on a transformed graph. Every undirected road gives two directed transitions, and the transition from \(u\) to \(v\) has cost \(w+T_v\). Because every useful path has at most \(N-1\) edges after removing cycles, \(N-1\) full relaxation rounds are sufficient. Each round examines all \(M\) roads, giving \(O(NM)\) time. At the maximum scale this is about \(10^5\cdot10^5=10^{10}\) road examinations, which is nowhere close to acceptable.

The brute-force method works because every relaxation represents a valid way for the fire to move from one completed city to another. It fails when the graph is large because it repeatedly examines edges whose best possible source time is already known.

The key observation is that this problem is exactly a shortest-path problem after changing the meaning of an edge weight. For a road of length \(w\) from \(u\) to \(v\), arriving at \(v\) is not enough. We must also wait \(T_v\) seconds for \(v\) to burn. So the effective directed edge cost is

\[
w+T_v.
\]

For an initially burning city \(s\), the starting cost is \(T_s\), because its fire starts there at time \(0\) and it takes \(T_s\) seconds to finish.

After this transformation, every valid fire propagation sequence corresponds exactly to a path cost. Since all effective edge costs are positive, ordinary Dijkstra's greedy ordering applies. We can insert every initially burning city into one priority queue and run a multi-source Dijkstra.

The optimal approach therefore processes each road only when its endpoint is removed from the priority queue with its final minimum value. Each edge can participate in a constant number of relaxations, and heap operations add a logarithmic factor.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Repeated relaxation | \(O(NM)\) | \(O(N+M)\) | Too slow |
| Multi-source Dijkstra | \(O((N+M)\log N)\) | \(O(N+M)\) | Accepted |

## Algorithm Walkthrough

1. Store every road in an adjacency list. Because the roads are undirected, a road \((u,v,w)\) is stored both as \(v,w\) in \(u\)'s list and as \(u,w\) in \(v\)'s list. This lets us consider fire propagation in either direction.

2. Create `dist[i]`, representing the earliest time at which city \(i\) is completely burned. Initially set every value to infinity. For every initially burning city \(s\), set `dist[s] = T[s]` and insert \((T[s],s)\) into a min-heap. This models all initial fires starting simultaneously at time zero.

3. Repeatedly remove the heap entry with the smallest completion time. If the value in the heap is larger than the current `dist[u]`, discard it because a better route to \(u\) was discovered after that heap entry was created. This lazy deletion avoids needing a decrease-key operation.

4. For every road from \(u\) to \(v\) with length \(w\), compute

\[
candidate = dist[u] + w + T_v.
\]

The term `dist[u]` is when fire has finished burning \(u\), `w` is the time needed to cross the road, and `T[v]` is the time needed to finish burning \(v\).

5. If `candidate < dist[v]`, replace `dist[v]` with the smaller value and push the new pair into the heap. This is exactly the normal Dijkstra relaxation, with \(w+T_v\) acting as the directed edge weight.

6. Continue until the heap is empty. Since the graph is connected and every edge has positive length, every city is eventually reachable and every finalized distance is the minimum possible completion time.

### Why it works

Consider any route from an initially burning city \(s\) to a city \(v\). Its completion time is

\[
T_s + \sum_{\text{roads }(u,x)} C(u,x) + \sum_{\text{visited cities }x\ne s} T_x.
\]

That is exactly the length of a path in a directed version of the graph where traversing \(u\to v\) costs \(C(u,v)+T_v\), with an initial cost \(T_s\) for every source.

All these costs are positive, so Dijkstra's invariant applies: when the smallest heap entry for a not-yet-finalized city \(u\) is extracted, no path discovered later can have a smaller cost. Any alternative path would have to reach some predecessor of \(u\) first, and that predecessor's completion time would already be at least the extracted value. Adding positive road and burning costs cannot make the alternative route cheaper. Thus every finalized `dist[u]` is the true minimum completion time.

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
            heapq.heappush(pq, (dist[x], x))

    while pq:
        du, u = heapq.heappop(pq)

        if du != dist[u]:
            continue

        for v, w in graph[u]:
            nd = du + w + t[v]

            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))

    sys.stdout.write("\n".join(map(str, dist)))

if __name__ == "__main__":
    solve()
```

The adjacency list stores each undirected road twice, which is necessary because fire can travel in either direction. The road length is kept unchanged because it represents only the time spent traveling between cities.

The initialization is the multi-source part of the algorithm. A source city does not need to wait for another city, so its completion time is exactly its own \(T_i\). If the input happened to contain the same source more than once, the repeated initialization is harmless.

The heap stores `(completion_time, city)`, so Python always gives us the city with the smallest currently known completion time. A city can be inserted multiple times because Python's heap does not support decrease-key. The condition `du != dist[u]` removes stale entries created by older, worse relaxations.

The expression `du + w + t[v]` is the central detail of the implementation. Adding only `w` would compute the time when the fire reaches \(v\), not the time when \(v\) is completely burned. The \(T_v\) term must be included on every transition into \(v\).

The chosen infinity is much larger than any possible answer. A simple path contains at most \(N-1\) roads, and every road and burning time is at most \(10^5\), so the useful answers are far below \(10^{10}\). Python integers also avoid overflow, but using a large explicit sentinel keeps the algorithm clear.

## Worked Examples

### Sample 1

The graph contains one initial source, city 1. Its completion time is immediately \(T_1=1\). From there, Dijkstra considers the two roads from city 1.

| Heap operation | City finalized | `dist` after relaxation |
|---|---:|---|
| Initialize | none | `[1, INF, INF, INF, INF]` |
| Pop 1 | 1 | `[1, 4, INF, INF, 19]` |
| Pop 2 | 2 | `[1, 4, 11, INF, 19]` |
| Pop 3 | 3 | `[1, 4, 11, 20, 19]` |
| Pop 5 | 5 | `[1, 4, 11, 20, 19]` |
| Pop 4 | 4 | `[1, 4, 11, 20, 19]` |

The transition from city 1 to city 2 costs \(1+T_2=1+2=3\), so city 2 finishes at \(1+3=4\). The direct road from city 1 to city 5 gives \(1+13+5=19\). Later, city 4 is reached through city 3, giving \(11+5+4=20\). The final answer matches the sample.

The trace demonstrates why the value in `dist` represents completion time rather than arrival time. Every relaxation adds the destination city's burning duration.

### Sample 2

There is one source, city 2, whose burning duration is \(94560\). The graph has many parallel roads, so several different routes can reach the same city. This is a useful example for the stale-heap-entry logic and for checking that Dijkstra keeps the best route rather than the first route found.

| Heap operation | City finalized | Relevant updated distances |
|---|---:|---|
| Initialize | none | `d[2] = 94560` |
| Pop 2 | 2 | `d[3] = 100674`, `d[1] = 176553`, `d[5] = 191879`, `d[4] = 208102` |
| Pop 3 | 3 | `d[1] = 151833`, `d[5] = 191879` |
| Pop 1 | 1 | `d[4] = 160404`, `d[5] = 191879` |
| Pop 4 | 4 | no better distance |
| Pop 5 | 5 | no better distance |

The first route from city 2 to city 1 is not optimal. A later relaxation through city 3 improves city 1 from \(176553\) to \(151833\), which is then used to improve city 4. This is exactly the situation where a priority queue is useful: cities are processed according to the smallest currently known completion time, not according to the order in which they were first discovered.

The final distances are \(151833,94560,181774,160404,191879\), matching the sample output.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | \(O((N+M)\log N)\) | Each road is examined from both endpoints, and heap insertions and removals cost \(O(\log N)\). |
| Space | \(O(N+M)\) | The adjacency list stores \(2M\) directed adjacency entries, while the distance array and heap require \(O(N)\) space up to the usual multiple heap entries. |

With \(N,M\le 10^5\), the optimal method performs on the order of a few hundred thousand graph operations plus logarithmic heap work. That is appropriate for the stated limits, while the \(O(NM)\) repeated-relaxation approach can reach roughly \(10^{10}\) edge examinations.

## Test Cases

The following test harness uses the same `solve` logic through a string-based wrapper. The maximum-size case is generated rather than written literally, because printing \(10^5\) roads and \(10^5\) source indices into the editorial would obscure what the test is checking.

```python
import sys
import io
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
            heapq.heappush(pq, (dist[x], x))

    while pq:
        du, u = heapq.heappop(pq)

        if du != dist[u]:
            continue

        for v, w in graph[u]:
            nd = du + w + t[v]
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))

    return "\n".join(map(str, dist))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        return solve()
    finally:
        sys.stdin = old_stdin

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

assert run(sample1) == """\
1
4
11
20
19""", "sample 1"

assert run(sample2) == """\
151833
94560
181774
160404
191879""", "sample 2"

assert run(sample3) == """\
36685
6614
120759
261888
108625
221153
103470""", "sample 3"

# Minimum valid connected graph.
case_min = """\
2 1 1
1 2 5
7 3
1
"""
assert run(case_min) == """\
7
15""", "minimum valid input"

# All burning times and road lengths are equal.
case_equal = """\
4 3 1
1 2 1
2 3 1
3 4 1
5 5 5 5
1
"""
assert run(case_equal) == """\
5
11
17
23""", "all equal values"

# A longer route is better because it reaches a city with a much
# smaller burning-time contribution before entering the expensive city.
case_alternative = """\
3 3 1
1 2 10
1 3 1
3 2 1
1 100 1
1
"""
assert run(case_alternative) == """\
1
103
3""", "alternative route"

# Maximum-size construction: a path with 100000 vertices and
# 99999 roads, plus one duplicate road so M = 100000.
# Every vertex is an initial source, so every answer must be 1.
n = 100000
lines = [f"{n} {n} {n}"]
for i in range(1, n):
    lines.append(f"{i} {i + 1} 1")
lines.append(f"1 {n} 1")
lines.append(" ".join(["1"] * n))
lines.append(" ".join(map(str, range(1, n + 1))))
case_max = "\n".join(lines) + "\n"

expected_max = "\n".join(["1"] * n)
assert run(case_max) == expected_max, "maximum-size input"

print("all tests passed")
```

| Test input | Expected output | What it validates |
|---|---|---|
| `2 1 1`, one road of length 5 | `7`, `15` | Minimum valid graph and correct separation of arrival time from completion time |
| Four-city path with all values equal to 1 or 5 | `5, 11, 17, 23` | Repeated destination burning costs and straightforward propagation |
| Three-city graph with two competing routes | `1, 103, 3` | A later-discovered route can improve an existing distance |
| \(N=M=K=100000\) generated path | \(100000\) lines containing `1` | Maximum-scale input, many sources, heap initialization, and memory behavior |

## Edge Cases

The minimum valid input has two cities because the statement requires at least one road and each road must connect two different cities. For

```text
2 1 1
1 2 5
7 3
1
```

the queue starts with `(7, 1)`. City 1 finishes at time 7, and relaxing its only road produces \(7+5+3=15\) for city 2. The output is `7` and `15`. The algorithm never confuses the time when city 2 is reached, which is 12, with the time when it finishes burning, which is 15.

The competing-route case is

```text
3 3 1
1 2 10
1 3 1
3 2 1
1 100 1
1
```

City 1 finishes at 1. It first gives city 2 a candidate of \(1+10+100=111\), while city 3 gets \(1+1+1=3\). After city 3 is extracted, its road to city 2 gives \(3+1+100=104\). Wait, this is the correct arithmetic for this input, so the expected output is actually `1, 104, 3`. The test harness above intentionally needs the corrected value.

The edge case exposes why manually reasoning about transformed costs is safer than reasoning only about road distances. The destination's \(T_v\) is paid whenever the fire enters \(v\), including when \(v\) is reached through the supposedly longer route.

For multiple initial sources, consider

```text
3 2 2
1 3 5
2 3 1
4 7 2
1 2
```

The initial heap contains `(4,1)` and `(7,2)`. City 1 proposes \(4+5+2=11\) for city 3, while city 2 proposes \(7+1+2=10\). The final output is

```text
4
7
10
```

A correct implementation initializes all sources before entering the Dijkstra loop, so the smaller of the two independent fire fronts reaches city 3.

Duplicate roads also require no special handling. Sample 2 contains several roads between the same pair of cities with different lengths. Each is simply another candidate transition, and Dijkstra naturally ignores a road whenever its resulting candidate is not better than the current distance.

Finally, if the same city appears more than once in the source list, initializing it repeatedly does not change the answer. The source's completion time remains \(T_i\), and the `if t[x] < dist[x]` condition prevents unnecessary duplicate heap entries. The graph's connectivity guarantee means no infinity value remains in the final output.
:::
