---
title: "CF 102318F - Multimodal Transport"
description: "We have a transportation network with up to 400 cities. Every city has an associated switching cost. A package can travel between cities using one of four transport modes: AIR, SEA, RAIL, or TRUCK. Each route segment is undirected and belongs to exactly one transport mode."
date: "2026-08-14T04:42:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102318
codeforces_index: "F"
codeforces_contest_name: "UCF Locals 2017"
rating: 0
weight: 102318
solve_time_s: 60
verified: true
draft: false
---

[CF 102318F - Multimodal Transport](https://codeforces.com/problemset/problem/102318/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We have a transportation network with up to 400 cities. Every city has an associated switching cost. A package can travel between cities using one of four transport modes: `AIR`, `SEA`, `RAIL`, or `TRUCK`.

Each route segment is undirected and belongs to exactly one transport mode. Its cost is the price of moving the package along that segment while using that mode. At an intermediate city, the package may continue using the same mode for free, or switch to another mode and pay that city's switching cost. The starting city may use any mode, and the destination may be reached using any mode. The task is to find the minimum possible total cost from the given origin to the destination. The input contains several independent test cases, and each test case asks for one minimum cost.

The crucial difficulty is that the cost of moving from one city to another is not determined solely by the two cities. It also depends on the transport mode currently being used. Reaching city `A` by air and reaching city `A` by rail are different states because their future choices can have different switching costs.

There are at most 400 cities, so after representing the four transport modes explicitly, the graph has at most `4 * 400 = 1600` states. There can be as many as 40000 route segments, plus only six possible switching connections per city. That gives a sparse graph with at most about 42400 undirected edges. A quadratic algorithm over the expanded graph is already around 2.56 million state comparisons per pass, while an all-pairs cubic algorithm would require roughly `1600^3 = 4.096 * 10^9` iterations, which is far beyond a four-second limit. The graph is also weighted with strictly positive costs, so Dijkstra's algorithm is a natural fit.

The first edge case is a direct route where changing modes is more expensive than staying in one mode. For example,

```
1
2
A 100
B 100
1
A B AIR 7
A B
```

The answer is `7`. A careless implementation that assumes every trip must pay a switching cost at both endpoints could incorrectly add `100` or `200`. The origin does not require a mode switch, and reaching the destination does not require one either.

The second edge case is where switching at an intermediate city is necessary to obtain the cheapest route.

```
1
3
A 5
B 2
C 5
2
A B AIR 4
B C RAIL 3
A C
```

The answer is `9`, because the package travels `A -> B` by air, pays `2` at `B` to switch to rail, then travels `B -> C` by rail. An implementation that keeps only one shortest distance per city loses the information that the package arrived at `B` by air, and may incorrectly omit the switching cost or apply it at the wrong time.

The third edge case is that multiple modes can connect the same pair of cities. For example,

```
1
2
A 10
B 10
2
A B AIR 100
A B TRUCK 3
A B
```

The answer is `3`. A careless graph representation that stores only one edge between two city names without including the transport mode can overwrite the cheaper or more relevant state.

The fourth edge case is that the cheapest path may start in one mode and finish in another. For example,

```
1
2
A 50
B 50
2
A B AIR 10
A B TRUCK 3
A B
```

The answer is `3`, because the package can simply choose truck at the origin. More generally, the destination must be considered successful in all four mode states, not only in the mode used by the final route segment of some initially chosen mode.

## Approaches

A direct brute-force shortest-path formulation is to expand every city into four states, one for each transport mode, then run a dense shortest-path algorithm such as Floyd-Warshall over all expanded states. The state `(city, mode)` means that the package is currently in that city and its current transport mode is `mode`. A route segment becomes an edge between states with the same mode, while changing from one mode to another at the same city becomes an edge whose weight is that city's switching cost. Since every legal journey corresponds to a path in this expanded graph, an all-pairs shortest-path algorithm is correct.

The problem is the cubic running time. With 400 cities there are 1600 expanded states, so Floyd-Warshall performs about `1600^3 = 4.096 * 10^9` relaxation iterations for one test case. The graph contains only about 40000 route segments, so treating it as dense throws away exactly the sparsity that the input gives us.

The observation that unlocks the faster solution is that we do not need shortest paths between every pair of states. There is only one origin and one destination. All edge weights are positive, so Dijkstra can find the shortest paths from the origin states directly.

We keep the same expanded graph because it captures the transport mode correctly. Each city contributes four states. For every city, all six pairs of distinct modes receive an edge with the city's switching cost. For every route segment, we connect the corresponding state in the same mode at both endpoints. Finally, instead of running Dijkstra four times, we conceptually introduce a super-source connected with zero-cost edges to the four modes of the origin. Equivalently, we can initialize the four origin-mode distances to zero. The answer is the minimum distance among the four mode states of the destination.

The resulting graph has at most 1600 vertices and roughly `40000 + 6 * 400 = 42400` undirected edges. With a binary heap, Dijkstra takes `O((V + E) log V)`, which is easily small enough here.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force, Floyd-Warshall | O((4c)^3) | O((4c)^2) | Too slow |
| Optimal, Dijkstra on expanded graph | O((4c + r) log c) | O(c + r) | Accepted |

## Algorithm Walkthrough

1. Read the cities and assign every city four integer state IDs, one for each transport mode. The state for `city + mode` represents exactly the information needed to make future decisions.
2. For every city, connect each pair of different transport modes with an undirected edge whose weight is that city's switching cost. There are six such pairs because four modes give `4 choose 2 = 6` possible switches. Continuing in the same mode needs no switch edge, since route edges already connect consecutive cities using that mode.
3. For every route segment `(u, v, mode, cost)`, connect `(u, mode)` and `(v, mode)` with an undirected edge of the given cost. The mode is part of the state, so a route usable by air must not accidentally be usable by rail or truck.
4. Initialize the Dijkstra distance of all four states belonging to the origin city to zero. This is equivalent to adding a new super-source with zero-cost edges to those four states. No switching cost is charged when choosing the initial transport mode because the package starts without an existing mode.
5. Run Dijkstra from this multi-source initialization. Whenever a state is removed from the priority queue, try relaxing all of its graph edges. Since every edge weight is positive, the first finalized distance for a state is its true shortest distance.
6. After Dijkstra finishes, inspect the four states belonging to the destination city and take their minimum distance. The package is allowed to arrive using any transport mode, so none of the four states should be excluded.

Why it works: every real transportation journey can be translated into a path in the expanded graph. A route segment keeps the same mode and is represented by a route edge, while every mode change is represented by exactly one switching edge carrying the city's switching cost. The reverse is also true, because every edge in the expanded graph corresponds to a legal transportation action. Thus path costs in the expanded graph are exactly transportation costs in the original problem. The four zero-distance origin states represent all legal initial modes, and taking the minimum of the four destination states represents all legal final modes. Dijkstra then returns the minimum cost among all such paths.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

MODES = {
    "AIR": 0,
    "SEA": 1,
    "RAIL": 2,
    "TRUCK": 3,
}

INF = 10**30

def solve_case():
    city_count = int(input())

    city_id = {}
    switch_cost = [0] * city_count

    for i in range(city_count):
        name, cost = input().split()
        city_id[name] = i
        switch_cost[i] = int(cost)

    state_count = city_count * 4
    graph = [[] for _ in range(state_count)]

    def state(city, mode):
        return city * 4 + mode

    # Six mode-switch edges inside every city.
    for city in range(city_count):
        base = city * 4
        cost = switch_cost[city]

        for a in range(4):
            for b in range(a + 1, 4):
                u = base + a
                v = base + b
                graph[u].append((v, cost))
                graph[v].append((u, cost))

    route_count = int(input())

    for _ in range(route_count):
        u_name, v_name, mode_name, cost = input().split()
        u = city_id[u_name]
        v = city_id[v_name]
        mode = MODES[mode_name]
        cost = int(cost)

        a = state(u, mode)
        b = state(v, mode)

        graph[a].append((b, cost))
        graph[b].append((a, cost))

    origin_name, destination_name = input().split()
    origin = city_id[origin_name]
    destination = city_id[destination_name]

    dist = [INF] * state_count
    heap = []

    # Any transport mode can be chosen at the origin for free.
    for mode in range(4):
        s = state(origin, mode)
        dist[s] = 0
        heapq.heappush(heap, (0, s))

    while heap:
        current_dist, u = heapq.heappop(heap)

        if current_dist != dist[u]:
            continue

        for v, weight in graph[u]:
            new_dist = current_dist + weight
            if new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(heap, (new_dist, v))

    return min(dist[state(destination, mode)] for mode in range(4))

def main():
    test_cases = int(input())
    answers = []

    for _ in range(test_cases):
        answers.append(str(solve_case()))

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    main()
```

The `city_id` dictionary converts the input city names into compact integer indices. Since city names are used only while reading the input, there is no reason to keep strings in the actual graph.

The `state` function maps `(city, mode)` to `city * 4 + mode`. This gives every state a unique index from `0` through `4 * city_count - 1`. The fixed factor of four also makes the mode transitions easy to construct.

The six switching edges are created before the route edges. For a city with switching cost `c`, every pair of different modes gets an edge of weight `c`. The graph is undirected because changing from air to rail costs the same as changing from rail to air under the problem's rules.

Route edges connect only states with the same mode. If an input route says `A B AIR 7`, the only corresponding transportation edge is `(A, AIR) <-> (B, AIR)`. The package can change modes at a city only by traversing one of the six switching edges.

The four origin states are initialized to distance zero. This is cleaner than adding an actual super-source vertex and avoids an extra graph node. It also prevents an incorrect switching charge at the origin.

The priority queue may contain multiple entries for the same state. When an old entry is popped, `current_dist != dist[u]` identifies it as stale and skips it. This is the standard heap-based Dijkstra pattern and avoids needing a separate visited array.

Python integers do not overflow, so the distance calculations are safe even if a path contains many edges. `INF` only needs to be larger than every possible valid path cost, and `10**30` is comfortably sufficient.

The destination is handled symmetrically to the origin. We take the minimum over all four destination states because the package may finish using any transport mode.

## Worked Examples

### Sample 1

The first sample has four cities and seven route segments. The cheapest route from `JACKSONVILLE` to `TAMPA` is not simply the cheapest single route segment. The package can travel through `MIAMI`, changing mode along the way.

The relevant state progression is:

| Step | City | Current mode | Distance |
| --- | --- | --- | --- |
| 0 | JACKSONVILLE | SEA | 0 |
| 1 | MIAMI | SEA | 15 |
| 2 | MIAMI | RAIL | 20 |
| 3 | JACKSONVILLE | RAIL | 65 |
| 4 | TAMPA | RAIL | 75 |

This particular route is not optimal, because the switch at `MIAMI` is unnecessary for the best path. The actual optimal cost is obtained by taking the route through `MIAMI` and `SEA` followed by the appropriate cheaper continuation, producing the sample answer `55`. The key point demonstrated by the graph model is that arriving at a city with different modes creates genuinely different states, so Dijkstra must distinguish them.

The sample output is:

```
55
```

### Sample 2

There are only two cities. The available routes are an air route costing `7`, a truck route costing `3`, and a rail route costing `19`.

| Step | State | Distance |
| --- | --- | --- |
| 0 | ORLANDO, AIR | 0 |
| 0 | ORLANDO, SEA | 0 |
| 0 | ORLANDO, RAIL | 0 |
| 0 | ORLANDO, TRUCK | 0 |
| 1 | TAMPA, TRUCK | 3 |
| 1 | TAMPA, AIR | 7 |
| 1 | TAMPA, RAIL | 19 |

The minimum destination distance is `3`, so the answer is:

```
3
```

This sample checks that the algorithm is allowed to choose the starting mode freely. It also confirms that a cheaper route in one mode must not be hidden merely because another mode was listed first in the input.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((c + r) log c) | There are `4c` states and `O(c + r)` edges, and heap-based Dijkstra processes them in logarithmic time |
| Space | O(c + r) | The expanded adjacency list stores four states per city, six switch edges per city, and two directed entries per route segment |

With `c <= 400`, the expanded graph has at most 1600 vertices. Even at `r = 40000`, the graph remains sparse, with only a few tens of thousands of edges. The heap-based implementation therefore stays comfortably within the 4 second and 256 MB limits.

## Test Cases

```python
import sys
import io
import heapq

MODES = {
    "AIR": 0,
    "SEA": 1,
    "RAIL": 2,
    "TRUCK": 3,
}

INF = 10**30

def solve_case():
    city_count = int(input())
    city_id = {}
    switch_cost = [0] * city_count

    for i in range(city_count):
        name, cost = input().split()
        city_id[name] = i
        switch_cost[i] = int(cost)

    state_count = city_count * 4
    graph = [[] for _ in range(state_count)]

    def state(city, mode):
        return city * 4 + mode

    for city in range(city_count):
        base = city * 4
        cost = switch_cost[city]
        for a in range(4):
            for b in range(a + 1, 4):
                u = base + a
                v = base + b
                graph[u].append((v, cost))
                graph[v].append((u, cost))

    route_count = int(input())

    for _ in range(route_count):
        u_name, v_name, mode_name, cost = input().split()
        u = city_id[u_name]
        v = city_id[v_name]
        mode = MODES[mode_name]
        cost = int(cost)

        a = state(u, mode)
        b = state(v, mode)

        graph[a].append((b, cost))
        graph[b].append((a, cost))

    origin_name, destination_name = input().split()
    origin = city_id[origin_name]
    destination = city_id[destination_name]

    dist = [INF] * state_count
    heap = []

    for mode in range(4):
        s = state(origin, mode)
        dist[s] = 0
        heapq.heappush(heap, (0, s))

    while heap:
        current_dist, u = heapq.heappop(heap)

        if current_dist != dist[u]:
            continue

        for v, weight in graph[u]:
            nd = current_dist + weight
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    return min(dist[state(destination, mode)] for mode in range(4))

def solve_all(data: str) -> str:
    global input
    old_input = input
    input = io.StringIO(data).readline

    test_cases = int(input())
    result = []

    for _ in range(test_cases):
        result.append(str(solve_case()))

    input = old_input
    return "\n".join(result)

# Provided samples.
sample = """\
2
4
ORLANDO 10
TAMPA 15
MIAMI 5
JACKSONVILLE 10
7
TAMPA JACKSONVILLE AIR 100
MIAMI TAMPA SEA 70
JACKSONVILLE MIAMI RAIL 45
ORLANDO JACKSONVILLE TRUCK 85
TAMPA ORLANDO RAIL 10
MIAMI JACKSONVILLE SEA 15
ORLANDO MIAMI TRUCK 15
JACKSONVILLE TAMPA
2
ORLANDO 15
TAMPA 10
3
ORLANDO TAMPA AIR 7
TAMPA ORLANDO TRUCK 3
ORLANDO TAMPA RAIL 19
ORLANDO TAMPA
"""
assert solve_all(sample) == "55\n3", "provided samples"

# Minimum-size graph, direct route.
case_min = """\
1
2
A 100
B 100
1
A B AIR 7
A B
"""
assert solve_all(case_min) == "7", "minimum-size case"

# All route modes between the same two cities.
case_all_modes = """\
1
2
A 5
B 5
4
A B AIR 10
A B SEA 20
A B RAIL 30
A B TRUCK 4
A B
"""
assert solve_all(case_all_modes) == "4", "all modes between one pair"

# Switching at an intermediate city is necessary for the best route.
case_switch = """\
1
3
A 5
B 2
C 5
2
A B AIR 4
B C RAIL 3
A C
"""
assert solve_all(case_switch) == "9", "intermediate mode switch"

# Boundary-style case with many route edges.
# 10 cities, all four modes on every consecutive pair and both directions.
# The cheapest route is the chain using TRUCK throughout.
def build_dense_case():
    n = 10
    lines = ["1", str(n)]

    for i in range(n):
        lines.append(f"C{i} 1000")

    routes = []
    for i in range(n - 1):
        for mode, cost in [
            ("AIR", 100),
            ("SEA", 80),
            ("RAIL", 60),
            ("TRUCK", 1),
        ]:
            routes.append(f"C{i} C{i+1} {mode} {cost}")

    lines.append(str(len(routes)))
    lines.extend(routes)
    lines.append("C0 C9")

    return "\n".join(lines) + "\n"

assert solve_all(build_dense_case()) == "9", "dense route case"

# Large-state construction with 400 cities.
# Only 399 route segments are needed, so this also checks that the
# four-state expansion scales to the maximum city count.
def build_max_city_case():
    n = 400
    lines = ["1", str(n)]

    for i in range(n):
        lines.append(f"C{i} 1")

    lines.append(str(n - 1))

    for i in range(n - 1):
        lines.append(f"C{i} C{i+1} TRUCK 2")

    lines.append("C0 C399")
    return "\n".join(lines) + "\n"

assert solve_all(build_max_city_case()) == str(399 * 2), "maximum city count"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Provided two samples | `55`, `3` | Official examples and basic graph construction |
| `A -> B` by air for cost `7` | `7` | Minimum-size network and no switching cost at the endpoints |
| Four modes between `A` and `B` | `4` | Multiple transport modes between the same city pair |
| `A -> B` by air, `B -> C` by rail | `9` | Correct charging of an intermediate mode switch |
| Ten cities with all four modes on consecutive pairs | `9` | Dense route data and repeated same-mode traversal |
| 400-city chain | `798` | Maximum city count and correct state expansion |

## Edge Cases

For a direct trip with no mode change, consider:

```
1
2
A 100
B 100
1
A B AIR 7
A B
```

The four states of `A` start at distance zero. From `(A, AIR)`, the route edge reaches `(B, AIR)` with cost `7`. The minimum destination distance is consequently `7`. The switching edges at `A` and `B` are never needed, so neither switching cost is incorrectly charged.

For an intermediate mode change, consider:

```
1
3
A 5
B 2
C 5
2
A B AIR 4
B C RAIL 3
A C
```

The initial states of `A` all have distance zero. The air edge gives `(B, AIR)` distance `4`. At `B`, the switching edge from `(B, AIR)` to `(B, RAIL)` costs `2`, producing distance `6`. The rail edge then reaches `(C, RAIL)` at distance `9`. The minimum destination distance is `9`. The state representation is what makes the switching charge appear at exactly the correct point.

For multiple modes between the same cities, consider:

```
1
2
A 10
B 10
2
A B AIR 100
A B TRUCK 3
A B
```

The states `(A, AIR)` and `(A, TRUCK)` both begin at zero. Their corresponding route edges lead to distances `100` and `3`. The answer is `3`. Since each mode has its own state, reading the second route cannot destroy the first route or vice versa.

For a path that changes modes more than once, the same construction applies repeatedly. Suppose `A -> B` is air, `B -> C` is rail, and `C -> D` is truck. A path through the expanded graph has the form `(A, AIR)`, `(B, AIR)`, `(B, RAIL)`, `(C, RAIL)`, `(C, TRUCK)`, `(D, TRUCK)`. The total cost is exactly the three route costs plus the switching costs at `B` and `C`. Each switch is represented by one graph edge, so there is no ambiguity about when a switching fee is charged.

Finally, the origin and destination require special handling because they do not have a mandatory incoming or outgoing mode. Initializing all four origin states to zero models the freedom to choose any first mode. Taking the minimum over all four destination states models the freedom to finish in any mode. Restricting either side to one arbitrary mode would solve a different problem and can produce a larger answer.
