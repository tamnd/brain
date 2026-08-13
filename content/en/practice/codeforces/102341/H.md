---
title: "CF 102341H - Hypno"
description: "We have a connected undirected graph with up to 200,000 intersections and 200,000 roads. We start at vertex 1 and want to reach vertex n. Traversing a road takes one minute, but every road hides one of two kinds of Hypno."
date: "2026-08-14T05:10:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102341
codeforces_index: "H"
codeforces_contest_name: "Radewoosh+mnbvmar Contest (supported by AIM Tech)"
rating: 0
weight: 102341
solve_time_s: 158
verified: true
draft: false
---

[CF 102341H - Hypno](https://codeforces.com/problemset/problem/102341/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a connected undirected graph with up to 200,000 intersections and 200,000 roads. We start at vertex 1 and want to reach vertex n. Traversing a road takes one minute, but every road hides one of two kinds of Hypno. With probability 1/2 the Hypno is harmless to us, in which case every traversal succeeds. With probability 1/2 it is harmful, in which case every traversal succeeds independently with probability 1/2.

We do not know the type of a road before using it. A failed traversal is especially valuable information: it proves that the road is harmful. A successful traversal does not completely identify the Hypno, but when we continue from the new vertex, the information obtained so far is enough to make adaptive strategies useful.

The task is to compute the minimum possible expected travel time from vertex 1 to vertex n. The required absolute or relative error is at most 10^-9.

The constraints rule out algorithms that repeatedly inspect large portions of the graph. With 200,000 vertices and 200,000 edges, an O(nm) method could perform about 4 * 10^10 adjacency operations in the worst case, which is far beyond a two second limit. We need essentially linear or O((n + m) log n) work.

The first small edge case is the graph with only two vertices.

```
2 1
1 2
```

The answer is 1.5. A careless solution that treats every road as having expected traversal time 2 would output 2, forgetting the 1/2 probability of immunity.

A second edge case is a direct road to the destination together with irrelevant alternatives.

```
3 2
1 3
1 2
```

The answer is again 1.5. The destination can be reached using the first road, so information about vertex 2 is irrelevant. A solution that averages over all outgoing roads instead of optimizing can produce a worse value.

The interesting edge case is several equally good alternatives. In the graph

```
4 4
1 2
2 4
1 3
3 4
```

each two-edge route by itself costs 3 in expectation, but the optimal answer is 2.875. After a failed first attempt at one route, trying the other route can be better than immediately retrying the known bad road. A solution that assigns every road a fixed cost of 1.5 and simply runs ordinary shortest path therefore misses the central observation.

## Approaches

A direct brute-force approach would keep, for every vertex, the distances of all already-discovered neighboring vertices and recompute the best local strategy every time another neighbor becomes available. To evaluate a local strategy, we sort the known neighbor values and inspect the prefix that could be useful. This is correct because the neighbors are considered in increasing order of their optimal continuation values.

The problem is that doing a complete scan after every update can inspect the same adjacency list many times. For a vertex of degree d, this can take O(d^2), and over the whole graph the worst case is O(m^2). With m = 200,000, that can reach roughly 4 * 10^10 adjacency inspections.

The key observation is that the neighbors become known in increasing order of their optimal values if we process the graph with Dijkstra's algorithm starting from the destination. Once the first useful neighbor of a vertex is known, every later neighbor arrives in nondecreasing order of its distance. We can update the expected value incrementally instead of recomputing the whole prefix.

Consider a vertex u whose best neighbor has optimal continuation value x. Suppose we have already failed on k fresh roads from u. The first failed road is the best known fallback, and it is now known to be harmful. Crossing that road from this point takes an expected two more minutes, after which the continuation costs x.

Before considering another fresh road with continuation value y, the fallback costs 2 + x. Trying the fresh road costs one minute immediately. With probability 3/4 it succeeds, giving continuation y. With probability 1/4 it fails, after which the fallback costs 2 + x. Thus the expected cost of trying this additional road is

1 + 3/4 y + 1/4(2 + x).

Trying it is useful exactly when

1 + 3/4 y + 1/4(2 + x) < 2 + x,

which simplifies to

y < x + 2/3.

This threshold is the reason the algorithm can stop processing neighbors permanently once their distance becomes too large.

For the first road, the probability of successful traversal is 3/4, because either we are immune or we are susceptible and the random endpoint is the opposite one. If it fails, which happens with probability 1/4, the road is known to be harmful.

If the useful neighbors have values x1, x2, ..., xk in increasing order, the expected value is

E_k = Σ from i=1 to k of (1/4)^(i-1) * (3/4) * (i + x_i)
+ (1/4)^k * (k + 2 + x_1).

The important part is that E_k can be updated in constant time. Starting with E_1 = 1.5 + x_1, adding x_k changes the answer by

(1/4)^(k-1) * (3/4 * (x_k - x_1) - 1/2).

So every edge needs to be processed only once, when its endpoint is finalized by Dijkstra.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m²) | O(n + m) | Too slow |
| Optimal | O((n + m) log n) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Reverse the point of view and run Dijkstra from vertex n. The value stored for a vertex will represent the minimum expected remaining time from that vertex to n.

The graph is undirected, so this does not require physically changing the edges. We simply initialize n with distance zero and propagate information to its neighbors.

1. Maintain, for every vertex u, the smallest finalized neighbor distance `first[u]`. Before the first neighbor is finalized, u has no candidate strategy.

When a first neighbor v with distance d is finalized, the best strategy currently known is to use that road until it succeeds. A fresh road takes expected 1.5 minutes, so we set

`value[u] = d + 1.5`.

1. After the first neighbor has been processed, maintain the probability `p` of reaching the next fresh road after all previous useful fresh roads have failed.

Every fresh road fails with probability 1/4, so after processing k useful roads this probability is `(1/4)^k`.

1. When another neighbor with distance d is finalized, compare it with `first[u]`.

If `d >= first[u] + 2/3`, it can never improve the strategy. All subsequently finalized neighbors have distance at least d, so they cannot improve it either. We can stop processing neighbors of u.

If `d < first[u] + 2/3`, include it in the strategy. The current expected value changes by

`p * (0.75 * (d - first[u]) - 0.5)`.

Then multiply p by 1/4, because reaching the next fresh road requires another failure.

1. Every time the current value of u improves, insert the new pair `(value[u], u)` into the priority queue.

Several entries for the same vertex may exist. When an entry is popped, discard it if it is no longer equal to the current best value. This is the standard lazy-deletion technique used in Dijkstra implementations.

1. Once vertex 1 is finalized, its value is the answer.

The Dijkstra ordering is valid because a vertex's useful neighbors satisfy

`d < first[u] + 2/3`.

The current value of u is always larger than `first[u] + 2/3`, so every useful neighbor must be finalized before u itself can be finalized. Thus, when u leaves the priority queue, every neighbor that could improve its answer has already been incorporated.

### Why it works

For a fixed vertex u, an optimal strategy considers candidate neighbors in nondecreasing order of their optimal continuation values. After the first failed road, that road becomes a known harmful fallback with expected remaining crossing time 2. A new road is useful precisely when its continuation value is less than `first[u] + 2/3`, so the useful neighbors form a prefix of the Dijkstra order.

The maintained value is exactly the expected cost of trying that prefix and then repeatedly using the first failed road if every fresh attempt fails. The incremental formula is algebraically equivalent to the full expectation formula, so every update preserves the exact optimal value among all currently available useful neighbors.

Since every potentially useful neighbor has a smaller distance than the value at u, all such neighbors are finalized before u. Consequently, when Dijkstra finalizes u, no future neighbor can improve its value. This gives the same correctness invariant as ordinary Dijkstra: the smallest unfinalized value is already optimal.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    graph = [[] for _ in range(n)]

    for _ in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        graph[a].append(b)
        graph[b].append(a)

    INF = float("inf")

    dist = [INF] * n

    # first[u] is the smallest finalized neighbor distance.
    first = [INF] * n

    # value[u] is the best expected value currently known for u.
    value = [INF] * n

    # prob[u] is the probability of reaching the next fresh edge
    # after all currently useful edges have failed.
    prob = [0.0] * n

    # Whether we have already found the first neighbor.
    seen = [False] * n

    pq = [(0.0, n - 1)]
    dist[n - 1] = 0.0

    while pq:
        cur, u = heapq.heappop(pq)

        if cur != dist[u]:
            continue

        if u == 0:
            print(f"{cur:.12f}")
            return

        du = cur

        for v in graph[u]:
            d = du

            if not seen[v]:
                seen[v] = True
                first[v] = d

                # One fresh edge has expected traversal cost 3/2.
                value[v] = d + 1.5

                # To reach the second fresh edge, the first one
                # must have failed, which happens with probability 1/4.
                prob[v] = 0.25

                if value[v] < dist[v]:
                    dist[v] = value[v]
                    heapq.heappush(pq, (dist[v], v))

            else:
                # Later neighbors are processed in nondecreasing d.
                # Once this threshold fails, no later neighbor can help.
                if d >= first[v] + 2.0 / 3.0:
                    continue

                # Add this neighbor to the useful prefix.
                value[v] += prob[v] * (
                    0.75 * (d - first[v]) - 0.5
                )

                prob[v] *= 0.25

                if value[v] < dist[v]:
                    dist[v] = value[v]
                    heapq.heappush(pq, (dist[v], v))

if __name__ == "__main__":
    solve()
```

The adjacency list stores the undirected graph in the usual way. There is no need to construct a separate reversed graph because every road is bidirectional.

`dist` is the Dijkstra value. `value` stores the incremental local expression, while `first` remembers the best continuation value among the neighbors processed so far. `prob` stores the probability of reaching the next unused road.

The first neighbor needs special handling. Its road is fresh, so its unconditional expected crossing time is 3/2. The probability of failing that first attempt is 1/4, which becomes the probability of reaching the second fresh road.

For every later neighbor, the expression

```
prob[v] * (0.75 * (d - first[v]) - 0.5)
```

is exactly the change in expected value caused by adding that neighbor to the useful prefix.

The threshold uses `2.0 / 3.0`, not `1.0 / 2.0`. This is a common place for an incorrect implementation. The fresh road attempt itself always costs one minute, then succeeds with probability 3/4 and falls back with probability 1/4. Comparing those two strategies gives the 2/3 threshold.

Floating point is sufficient here. The multiplier `prob` decreases by a factor of four for every additional useful neighbor, so after only a few dozen useful neighbors its contribution is far below the required 10^-9 precision. Python integers do not participate in the numerical recurrence, so there is no integer overflow issue.

The priority queue uses lazy deletion. A vertex can receive several progressively better estimates before it is finalized. Only the entry matching the current `dist[u]` is processed.

## Worked Examples

### Sample 1

The graph is a triangle, and vertex 3 is the destination.

```
3 3
1 2
1 3
2 3
```

From vertex 3, both vertices 1 and 2 initially have a continuation value of zero.

| Finalized vertex | Neighbor updated | First value | Current value |
| --- | --- | --- | --- |
| 3 | 1 | 0 | 1.500000 |
| 3 | 2 | 0 | 1.500000 |

Vertex 1 receives the direct edge to the destination, giving 1.5. The other edge cannot improve it because its continuation value is also zero, but the vertex is already finalized before another useful update could matter.

The answer is therefore 1.500000000000.

The trace demonstrates why a single fresh road has expected cost 1.5. The first attempt succeeds with probability 3/4. If it fails, the road is known harmful and the remaining expected number of attempts is two, giving a total expected time of 2 conditional on the road being harmful.

### Sample 2

The graph is

```
4 4
1 2
2 4
4 3
3 1
```

with destination 4.

Vertices 2 and 3 each have one fresh road to the destination, so both obtain value 1.5.

| Finalized vertex | Updated vertex | First value | Added neighbor | New value |
| --- | --- | --- | --- | --- |
| 4 | 2 | 1.500000 | none | 1.500000 |
| 4 | 3 | 1.500000 | none | 1.500000 |
| 2 | 1 | 1.500000 | none | 3.000000 |
| 3 | 1 | 1.500000 | 1.500000 | 2.875000 |

For vertex 1, using only vertex 2 gives 3. After the road to vertex 2 fails, however, the other route through vertex 3 is worth trying because its continuation value is equal to the first route's value and is below the `first + 2/3` threshold.

The second attempt is reached with probability 1/4. Its inclusion reduces the value from 3 to 2.875, giving the required sample answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | Every adjacency is processed once, and every useful value update is inserted into a binary heap |
| Space | O(n + m) | The adjacency lists, distance arrays, and priority queue require linear space |

The graph contains at most 200,000 edges, so the algorithm performs only O(m) local edge processing and O(m) heap insertions. The resulting O((n + m) log n) complexity is easily suitable for the stated constraints, while the memory usage is linear in the graph size.

## Test Cases

```python
import io
import heapq
import math

def run(inp: str) -> str:
    data = inp.strip().split()
    it = iter(data)

    n = int(next(it))
    m = int(next(it))

    graph = [[] for _ in range(n)]

    for _ in range(m):
        a = int(next(it)) - 1
        b = int(next(it)) - 1
        graph[a].append(b)
        graph[b].append(a)

    INF = float("inf")
    dist = [INF] * n
    first = [INF] * n
    value = [INF] * n
    prob = [0.0] * n
    seen = [False] * n

    pq = [(0.0, n - 1)]
    dist[n - 1] = 0.0

    while pq:
        cur, u = heapq.heappop(pq)

        if cur != dist[u]:
            continue

        if u == 0:
            return f"{cur:.12f}"

        for v in graph[u]:
            d = cur

            if not seen[v]:
                seen[v] = True
                first[v] = d
                value[v] = d + 1.5
                prob[v] = 0.25

                if value[v] < dist[v]:
                    dist[v] = value[v]
                    heapq.heappush(pq, (value[v], v))
            else:
                if d >= first[v] + 2.0 / 3.0:
                    continue

                value[v] += prob[v] * (
                    0.75 * (d - first[v]) - 0.5
                )
                prob[v] *= 0.25

                if value[v] < dist[v]:
                    dist[v] = value[v]
                    heapq.heappush(pq, (value[v], v))

    return ""

def check(inp: str, expected: float, message: str):
    actual = float(run(inp))
    assert math.isclose(actual, expected, rel_tol=1e-10, abs_tol=1e-10), (
        message, actual, expected
    )

# Sample 1
check(
    """\
3 3
1 2
1 3
2 3
""",
    1.5,
    "sample 1",
)

# Sample 2
check(
    """\
4 4
1 2
2 4
4 3
3 1
""",
    2.875,
    "sample 2",
)

# Minimum-size graph
check(
    """\
2 1
1 2
""",
    1.5,
    "minimum graph",
)

# A simple chain of three vertices.
# Each of the two roads has expected cost 1.5.
check(
    """\
3 2
1 2
2 3
""",
    3.0,
    "simple chain",
)

# Three equally good two-edge routes.
# The useful values at vertex 1 are 1.5, 1.5, 1.5.
# E1 = 3
# E2 = 2.875
# E3 = 2.84375
check(
    """\
5 6
1 2
2 5
1 3
3 5
1 4
4 5
""",
    2.84375,
    "three equal alternatives",
)

# Large boundary case: a chain with 200000 vertices.
# There are 199999 roads, each contributing 1.5 in expectation.
n = 200000
parts = [f"{n} {n - 1}"]
for i in range(1, n):
    parts.append(f"{i} {i + 1}")

large_input = "\n".join(parts) + "\n"
check(
    large_input,
    1.5 * (n - 1),
    "maximum-size chain",
)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 / 1 2` | `1.500000000000` | Minimum graph and the basic 3/4 success probability |
| `3 2 / 1 2 / 2 3` | `3.000000000000` | A graph with no alternative route |
| Three parallel two-edge routes through vertices 2, 3, 4 | `2.843750000000` | Several equal useful neighbors and repeated incremental updates |
| Chain with 200,000 vertices | `299998.500000000000` | Maximum input size and linear graph structure |

## Edge Cases

For the two-vertex graph

```
2 1
1 2
```

Dijkstra starts at vertex 2 with value zero. When vertex 2 is finalized, vertex 1 receives its first neighbor with `first[1] = 0`. Its candidate value becomes `0 + 1.5 = 1.5`. No second neighbor exists, so the answer is exactly 1.5.

For a graph containing a direct destination edge,

```
3 2
1 3
1 2
```

vertex 3 is finalized first. The direct edge gives vertex 1 a value of 1.5. Even though vertex 2 will also eventually be processed, its distance cannot provide a better route than the already finalized direct destination edge. The answer remains 1.5.

For the graph with three equal alternatives,

```
5 6
1 2
2 5
1 3
3 5
1 4
4 5
```

vertices 2, 3, and 4 all receive value 1.5 from vertex 5. The first such neighbor gives vertex 1 the value 3. The second neighbor changes it by

`(1/4) * (-1/2) = -1/8`,

giving 2.875. The third changes it by

`(1/16) * (-1/2) = -1/32`,

giving 2.84375. A fourth equal alternative would improve it by only 1/128, and so on. The geometric probability factor is exactly what makes the incremental representation efficient.

For a vertex whose next neighbor has distance at least `first + 2/3`, the algorithm ignores it. Suppose the best known neighbor has value x and the new neighbor has value y. If `y >= x + 2/3`, trying that fresh road costs at least as much as immediately using the known harmful road. Since all future neighbors have even larger finalized values, none of them can become useful either. This is the stopping condition that prevents repeated scans of the same adjacency list.

For the maximum-size chain, every vertex has only one useful neighbor toward the destination. No alternative road is ever considered, so every edge contributes exactly 1.5 to the expected time. With 199,999 roads, the result is `199999 * 1.5 = 299998.5`. The algorithm processes every edge once and remains within O((n + m) log n) time.
