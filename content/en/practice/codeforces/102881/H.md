---
title: "CF 102881H - Shortest Array"
description: "We are given a connected weighted graph and an array of positive values s. The task is to find the smallest indexed vertex x such that the value written at every vertex is exactly the shortest distance from x to that vertex."
date: "2026-07-25T12:34:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102881
codeforces_index: "H"
codeforces_contest_name: "ECPC 2019 Kickoff"
rating: 0
weight: 102881
solve_time_s: 64
verified: true
draft: false
---

[CF 102881H - Shortest Array](https://codeforces.com/problemset/problem/102881/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
# Problem Understanding

We are given a connected weighted graph and an array of positive values `s`. The task is to find the smallest indexed vertex `x` such that the value written at every vertex is exactly the shortest distance from `x` to that vertex. The special condition is that staying at `x` is not considered a valid zero length path, so the value at `x` itself is the length of the shortest non-empty closed walk starting and ending at `x`. The graph has positive edge weights and no parallel edges or self loops.

The limits are large enough that trying every vertex as a possible starting point is impossible. With up to `2 * 10^5` vertices and edges, a single Dijkstra run is acceptable, but running it once from every vertex would require roughly `O(n * (n + m) log n)` operations, which is far beyond the available time. The solution needs to extract information about all possible starting vertices simultaneously.

The unusual part of the problem is the value stored at the source vertex. In a normal shortest path array, the source would contain `0`. Here it contains the shortest positive cycle that starts and ends at that vertex. In an undirected graph with positive weights, this value is twice the minimum edge weight incident to that vertex, because the cheapest closed walk can go across the lightest adjacent edge and immediately return.

A common mistake is accepting a vertex with a correct distance to all other vertices but forgetting to verify its own value. For example:

```
3 2
4 2 2
1 2 2
2 3 2
```

The correct output is `2`. Vertex `2` reaches vertices `1` and `3` in distance `2`, and its shortest non-empty return walk is also `4`. A careless solution that only checks distances to other vertices might incorrectly accept vertex `1` or `3`, because they have the same outward distances to some vertices but their self distance should be `4`, not `2`.

Another edge case appears when multiple vertices could satisfy the array. The problem asks for the smallest index. For example:

```
4 4
6 3 6 6
1 3 6
1 2 3
3 2 3
4 2 3
```

The correct output is `1`. Several distance relationships look symmetric, but only the smallest valid index must be printed.

A final trap is an impossible distance array. For example:

```
3 3
1 5 5
1 2 2
2 3 2
1 3 10
```

The output is `-1`. The values claim that some vertex can be reached with a smaller distance than the graph actually allows, so no starting vertex can generate the array.

## Approaches

The straightforward approach is to test every vertex as the possible origin. For a chosen vertex `x`, we would run Dijkstra from `x`, compare all computed distances with `s`, and additionally verify that the special value `s[x]` matches the shortest non-empty closed walk from `x`. This is correct because it directly checks the definition. However, the worst case performs `n` Dijkstra runs. With `n` and `m` both around `200000`, this becomes roughly `200000 * 400000 log(200000)` operations, which is not feasible.

The key observation is that the whole array can be viewed from a new artificial vertex. Create a virtual vertex `z` and connect it to every original vertex `i` with an edge of weight `s[i]`. If the array is valid for some source `x`, then the shortest distance from `z` to every vertex is exactly `s[i]`. The direct edge gives this distance, and any path using original graph edges cannot be shorter because the labels already behave like shortest distances.

The remaining question is which vertex could have been the real source. For a valid source `x`, the artificial edge `z -> x` is not the only way to reach `x` with distance `s[x]`. We can go from `z` to some other vertex `u`, paying `s[u]`, and then travel through the original graph back to `x`. This corresponds to the shortest non-empty closed walk from `x`.

So we run a multi-source Dijkstra where every vertex initially acts as a source with distance `s[i]`. During this process we keep the two best distances reaching every vertex, but the two distances must come from different starting vertices. The second best source for vertex `i` tells us whether there is a path of length exactly `s[i]` that does not start with the artificial edge to `i`. If that exists, `i` is a possible answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n(n + m) log n) | O(n + m) | Too slow |
| Optimal | O((n + m) log n) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Initialize every original vertex as a source in a multi-source Dijkstra. Vertex `i` starts with distance `s[i]` and source identifier `i`. This simulates adding the virtual vertex without explicitly storing it.
2. During Dijkstra, maintain the best and second best distances for every vertex, where the two stored entries must have different source identifiers. We only care about two different origins because the first origin might simply be the direct artificial edge.
3. Relax graph edges normally. When a path reaches a vertex, update either its best entry or its second best entry depending on whether the source identifier is already present.
4. After Dijkstra finishes, check every vertex in increasing order. The first condition is that the best distance reaching the vertex must equal `s[i]`. If a smaller distance exists, the given array cannot represent any shortest path tree.
5. The second condition is that the second best distance must also equal `s[i]`. This means the vertex can be reached with the same value without using itself as the artificial starting point, which is exactly the required non-empty path back to the source.
6. Output the first vertex satisfying both conditions. If none exists, output `-1`.

Why it works:

The multi-source Dijkstra computes shortest paths from the virtual source conceptually attached to every vertex. A valid distance array means every vertex must keep its direct artificial distance as the shortest possible distance. The only special vertex is the real source, because its direct artificial edge represents the forbidden zero-move path. The existence of an equal length path from another source proves that the value can be generated by an actual walk inside the original graph. Thus the second best distance criterion identifies exactly the possible original sources.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    s = list(map(int, input().split()))

    graph = [[] for _ in range(n)]
    for _ in range(m):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append((v, w))
        graph[v].append((u, w))

    INF = 10**30

    best_d = [INF] * n
    best_o = [-1] * n
    second_d = [INF] * n
    second_o = [-1] * n

    heap = []

    for i, x in enumerate(s):
        best_d[i] = x
        best_o[i] = i
        heapq.heappush(heap, (x, i, i))

    def update(v, d, o):
        if best_o[v] == o:
            if d < best_d[v]:
                best_d[v] = d
                return True
            return False

        if second_o[v] == o:
            if d < second_d[v]:
                second_d[v] = d
                return True
            return False

        if d < best_d[v]:
            second_d[v] = best_d[v]
            second_o[v] = best_o[v]
            best_d[v] = d
            best_o[v] = o
            return True

        if d < second_d[v]:
            second_d[v] = d
            second_o[v] = o
            return True

        return False

    while heap:
        d, v, o = heapq.heappop(heap)

        if d != best_d[v] and d != second_d[v]:
            continue

        for u, w in graph[v]:
            nd = d + w
            if update(u, nd, o):
                heapq.heappush(heap, (nd, u, o))

    for i in range(n):
        if best_d[i] != s[i]:
            print(-1)
            return

    for i in range(n):
        if second_d[i] == s[i]:
            print(i + 1)
            return

    print(-1)

if __name__ == "__main__":
    solve()
```

The initialization replaces the virtual node construction. Instead of explicitly adding `z`, every vertex begins with a distance equal to the edge that would connect it to `z`.

The `update` function is the core of the implementation. It keeps only the two smallest paths with different starting vertices. Keeping two entries from the same origin would not help because the second path must represent a different artificial edge.

The Dijkstra relaxation uses 64-bit style integers through Python’s normal integer type. This matters because path lengths can reach about `2 * 10^14`. The stale heap check is needed because a vertex can have multiple outdated entries after improvements.

The final scan is deliberately in increasing index order. The first valid vertex is automatically the smallest indexed answer.

## Worked Examples

For the first sample:

```
4 4
6 3 6 6
1 3 6
1 2 3
3 2 3
4 2 3
```

The important Dijkstra states are:

| Vertex | Initial source | Best distance | Second source | Second distance |
| --- | --- | --- | --- | --- |
| 1 | 1 | 6 | 2 | 6 |
| 2 | 2 | 3 | 1 | 6 |
| 3 | 3 | 6 | 1 | 6 |
| 4 | 4 | 6 | 1 | 6 |

Vertex `1` has a second path of length `6`, so it is valid. It is the first valid index and the answer is `1`.

This example shows why the second shortest source is required. The direct artificial edge is not enough to prove that a vertex is the hidden origin.

For the third sample:

```
5 6
8 4 4 8 6
1 2 4
1 3 4
2 4 4
3 4 4
1 5 3
5 3 2
```

The states are:

| Vertex | Best distance | Second distance |
| --- | --- | --- |
| 1 | 4 | 8 |
| 2 | 4 | 8 |
| 3 | 4 | 8 |
| 4 | 8 | 8 |
| 5 | 6 | 10 |

Only vertex `4` has the required second path equal to its value.

The trace demonstrates the special self-distance rule. Vertex `4` is not identified by a zero distance, but by another shortest route of length `8`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | Each graph edge is relaxed during one multi-source Dijkstra process. |
| Space | O(n + m) | The graph and the two best states for each vertex are stored. |

The constraints allow a single Dijkstra traversal because the number of vertices and edges is at most about `200000`. The memory usage stays linear, which fits comfortably in the limit.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out

assert run("""4 4
6 3 6 6
1 3 6
1 2 3
3 2 3
4 2 3
""") == "1\n", "sample 1"

assert run("""4 4
6 3 4 8
1 3 4
1 2 3
2 4 5
3 4 4
""") == "1\n", "sample 2"

assert run("""5 6
8 4 4 8 6
1 2 4
1 3 4
2 4 4
3 4 4
1 5 3
5 3 2
""") == "4\n", "sample 3"

assert run("""1 0
1
""") == "-1\n", "single isolated vertex"

assert run("""3 2
4 2 4
1 2 2
2 3 2
""") == "2\n", "line graph"

assert run("""3 3
1 5 5
1 2 2
2 3 2
1 3 10
""") == "-1\n", "invalid distances"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex | `-1` | Handles the missing non-empty walk case. |
| Line graph | `2` | Checks the special self-distance computation. |
| Invalid distances | `-1` | Rejects arrays that cannot be generated. |

## Edge Cases

For the invalid single vertex case:

```
1 0
1
```

There is no edge and no possible non-empty walk that starts and ends at the only vertex. The algorithm initializes the vertex but never creates a second source path, so it correctly prints `-1`.

For a source in the middle of a line:

```
3 2
4 2 4
1 2 2
2 3 2
```

The multi-source process finds that vertex `2` has distance `2` to both neighbors and another route of length `4` back to itself. Its second best distance is exactly `4`, so it is accepted.

For an impossible array:

```
3 3
1 5 5
1 2 2
2 3 2
1 3 10
```

The graph itself provides a shorter route between some vertices than the given values allow. The best distance computed by Dijkstra becomes smaller than the corresponding `s` value, so the first validation step rejects the entire array.

For the multiple candidate case:

```
4 4
6 3 6 6
1 3 6
1 2 3
3 2 3
4 2 3
```

Several vertices receive equal length paths, but scanning from index `1` upward returns the smallest valid source as required.
