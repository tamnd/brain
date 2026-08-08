---
title: "CF 102465H - Travel Guide"
description: "Every station can be represented by three numbers. For a station (v), let [ D(v) = (d0(v), d1(v), d2(v)), ] where (d0(v)) is its shortest distance to Orly, (d1(v)) is its shortest distance to Notre-Dame, and (d2(v)) is its shortest distance to Disneyland."
date: "2026-08-08T09:22:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102465
codeforces_index: "H"
codeforces_contest_name: "2018-2019 ICPC Southwestern European Regional Programming Contest (SWERC 2018)"
rating: 0
weight: 102465
solve_time_s: 141
verified: true
draft: false
---

[CF 102465H - Travel Guide](https://codeforces.com/problemset/problem/102465/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

Every station can be represented by three numbers. For a station (v), let

[
D(v) = (d_0(v), d_1(v), d_2(v)),
]

where (d_0(v)) is its shortest distance to Orly, (d_1(v)) is its shortest distance to Notre-Dame, and (d_2(v)) is its shortest distance to Disneyland.

A station (A) is useless exactly when there is another station (B) whose three distances are all no larger than those of (A), with at least one of the three distances strictly smaller. In terms of the vectors, (B) dominates (A) when

[
d_0(B) \le d_0(A),\qquad
d_1(B) \le d_1(A),\qquad
d_2(B) \le d_2(A),
]

and at least one inequality is strict.

The graph has up to (100000) stations and (500000) edges. Since all edge weights are positive, shortest distances from one source can be computed with Dijkstra's algorithm. We need three such runs, one from each POI.

The real difficulty comes after the shortest paths are known. We have up to (100000) points in three dimensional space and need to count the points that are not dominated by another point.

A quadratic comparison of all station pairs is already too large. With (100000) stations, checking every ordered pair means

[
100000 \cdot 99999 = 9,999,900,000
]

candidate witness checks. Even if each check were only a few integer comparisons, this is far beyond the six second limit.

The positive edge weights also mean that ordinary Dijkstra is applicable without any special handling for zero weight edges. Multiple stations can have exactly the same distance triple. Such stations do not dominate one another, because domination requires at least one strict inequality. A solution that processes identical triples independently can accidentally mark the second copy as useless.

For example, consider two stations with the same distances to all three POIs.

```
5 6
0 3 1
1 3 1
2 3 1
0 4 1
1 4 1
2 4 1
```

Stations 3 and 4 both have vector ((1,1,1)). The three POIs have vectors ((0,2,2)), ((2,0,2)), and ((2,2,0)). None of these dominates either station 3 or station 4, and stations 3 and 4 cannot dominate each other because their vectors are equal. The correct answer is 5. Treating an identical earlier vector as a strict witness would incorrectly remove one of them.

Another subtle case occurs when the first two coordinates are equal but the third differs.

```
5 6
0 3 1
1 3 1
2 3 2
0 4 1
1 4 1
2 4 3
```

Station 3 has vector ((1,1,2)), while station 4 has vector ((1,1,3)). Station 3 dominates station 4 because it is equally close to Orly and Notre-Dame and strictly closer to Disneyland. The correct answer is 4. A data structure that only considers strictly smaller values of the second coordinate would miss this case.

Finally, the smallest allowed graph has four stations, exactly the three POIs and one additional station. For example,

```
4 3
0 3 1
1 3 1
2 3 1
```

The four vectors are ((0,2,2)), ((2,0,2)), ((2,2,0)), and ((1,1,1)). None dominates another, so the answer is 4.

## Approaches

The direct approach starts by computing the three distance arrays with Dijkstra. Once every station has its vector ((d_0,d_1,d_2)), we can simply compare every pair of stations. For each station (A), scan every other station (B) and check whether all three coordinates of (B) are no larger than those of (A), with at least one strict inequality.

This is correct because it checks the definition of uselessness literally. The problem is the number of comparisons. There can be (N(N-1)), or (9,999,900,000), ordered candidate witnesses when (N=100000). The graph processing is nowhere near this expensive, so the pairwise dominance check is the part that must be replaced.

The key observation is that the first coordinate can be handled by sorting. Sort all distance vectors lexicographically by ((d_0,d_1,d_2)). When processing a vector (v=(x,y,z)), every previously processed vector (u) satisfies (u_x\le x). If (u_x<x), the first coordinate already gives the required strict inequality. If (u_x=x), lexicographic order guarantees (u_y\le y). If (u_y<y), the second coordinate gives the strict inequality. If (u_y=y), then because identical vectors are grouped together, an earlier distinct vector must have (u_z<z).

So after sorting, the remaining question is only two dimensional. For the current vector ((x,y,z)), we need to know whether some earlier vector has

[
u_y\le y
]

and

[
u_z\le z.
]

That can be reduced to a prefix minimum query. Among all previously processed vectors whose second coordinate is at most (y), keep the minimum third coordinate. If that minimum is at most (z), then such a vector dominates the current one.

A Fenwick tree can maintain exactly this information. Its stored value is not a sum or a count, but the minimum third coordinate seen at each compressed second coordinate. A prefix query returns the minimum third coordinate among all processed points with second coordinate at most the requested value.

There is one more detail caused by duplicate vectors. We sort the vectors and process equal triples as one group. We query the Fenwick tree before inserting the group, so a vector is never considered to dominate another identical copy. If the vector is not dominated by an earlier distinct vector, every station with that same vector is useful.

The brute-force approach works because dominance is easy to test between two vectors, but it fails when there are too many pairs. Sorting removes one dimension from the search, and the Fenwick tree handles the remaining two dimensions in logarithmic time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O((N+E)\log N + N^2)) | (O(N+E)) | Too slow |
| Optimal | (O((N+E)\log N)) | (O(N+E)) | Accepted |

## Algorithm Walkthrough

1. Build the undirected graph from the input. For each edge, store both directions because travel is possible in either direction.
2. Run Dijkstra three times, starting from stations 0, 1, and 2. This gives three distance arrays, so every station can now be represented as ((d_0,d_1,d_2)). Three Dijkstra runs only multiply the running time by a constant.
3. Create the list of distance triples and sort it lexicographically by (d_0), then (d_1), then (d_2). This ordering guarantees that every potential dominator of the current vector appears before it.
4. Coordinate-compress all distinct (d_1) values. The Fenwick tree will use the compressed position of (d_1), and each tree cell stores the minimum (d_2) among processed vectors contributing to that cell.
5. Process equal triples as a single group. Before inserting the group into the Fenwick tree, query the prefix ending at its (d_1). If the returned minimum (d_2) is at most the group's (d_2), an earlier distinct vector dominates this triple, so all stations in the group are useless. Otherwise, all stations in the group are useful and their multiplicity is added to the answer.
6. Insert the group's (d_2) into the Fenwick tree at its compressed (d_1) position. The update stores the minimum value, because future queries only care whether some suitable vector has a sufficiently small third coordinate.

### Why it works

After lexicographic sorting, every previously processed vector has a first coordinate no larger than the current vector. If a previous vector has a smaller first coordinate, it already provides strict improvement. If the first coordinates are equal, lexicographic order gives a second coordinate no larger than the current one. A smaller second coordinate gives strict improvement, and if the second coordinates are also equal, processing distinct triples in increasing third coordinate guarantees a smaller third coordinate. Thus, for a distinct earlier vector, the only remaining condition for dominance is (u_y\le y) and (u_z\le z).

The Fenwick prefix minimum tells us exactly whether such a previous vector exists. Consequently, the current triple is marked useless if and only if a valid dominating station exists. Equal triples are handled together, so equality in all three coordinates is never mistaken for strict domination.

## Python Solution

```python
import sys
import heapq
from bisect import bisect_left
from array import array

input = sys.stdin.readline

INF = 10**18

def dijkstra(src, head, to, weight, nxt, n):
    dist = [INF] * n
    dist[src] = 0

    pq = [(0, src)]
    heappush = heapq.heappush
    heappop = heapq.heappop

    while pq:
        d, u = heappop(pq)

        if d != dist[u]:
            continue

        e = head[u]
        while e != -1:
            v = to[e]
            nd = d + weight[e]

            if nd < dist[v]:
                dist[v] = nd
                heappush(pq, (nd, v))

            e = nxt[e]

    return dist

def solve():
    n, m = map(int, input().split())

    # Forward-star representation.
    # Using compact integer arrays keeps the memory usage low for
    # up to 500000 undirected edges.
    head = array('i', [-1]) * n
    to = array('i')
    weight = array('i')
    nxt = array('i')

    for _ in range(m):
        a, b, w = map(int, input().split())

        idx = len(to)
        to.append(b)
        weight.append(w)
        nxt.append(head[a])
        head[a] = idx

        idx = len(to)
        to.append(a)
        weight.append(w)
        nxt.append(head[b])
        head[b] = idx

    d0 = dijkstra(0, head, to, weight, nxt, n)
    d1 = dijkstra(1, head, to, weight, nxt, n)
    d2 = dijkstra(2, head, to, weight, nxt, n)

    points = list(zip(d0, d1, d2))
    points.sort()

    # Coordinate compression for the second coordinate.
    ys = sorted({p[1] for p in points})
    k = len(ys)

    # Fenwick tree for prefix minimum of the third coordinate.
    bit = [INF] * (k + 1)

    answer = 0
    i = 0

    while i < n:
        x, y, z = points[i]

        # Find the complete group of identical triples.
        j = i + 1
        while j < n and points[j] == points[i]:
            j += 1

        pos = bisect_left(ys, y) + 1

        # Query minimum z among all previous points with y <= current y.
        p = pos
        best = INF

        while p > 0:
            if bit[p] < best:
                best = bit[p]
            p -= p & -p

        # If no previous point has z <= current z, this triple is useful.
        if best > z:
            answer += j - i

        # Insert this unique triple into the Fenwick tree.
        p = pos
        while p <= k:
            if z < bit[p]:
                bit[p] = z
            p += p & -p

        i = j

    sys.stdout.write(str(answer) + '\n')

if __name__ == "__main__":
    solve()
```

The graph is stored using a forward-star representation rather than a Python list of tuples for every adjacency entry. With (500000) undirected edges there are (1000000) directed adjacency entries, so storing endpoints, weights, and next pointers in compact integer arrays saves a substantial amount of memory.

The three calls to `dijkstra` correspond directly to the three POIs. The priority queue stores pairs of current distance and station. The `d != dist[u]` check discards stale heap entries created when a station received a better distance after an older entry had already been pushed.

The triples are sorted directly, so Python's tuple ordering gives exactly the required lexicographic order. The loop from `i` to `j` identifies all identical triples. The query happens before the update, which is essential because identical vectors must not dominate each other.

The Fenwick tree is indexed from 1 rather than 0. `pos` is therefore `bisect_left(ys, y) + 1`. The query moves toward zero with `p -= p & -p`, while the update moves upward with `p += p & -p`. The tree stores minima, so every update uses `min` instead of addition.

The largest possible shortest distance is at most ((N-1)\cdot100), which is below (10^7). Python integers have no overflow issue, and the `INF` value is comfortably larger than every possible distance.

## Worked Examples

### Sample 1

The graph is a star centered at station 3, with station 4 attached to that center. The distance triples are

| Station | (d_0) | (d_1) | (d_2) | Sorted position |
| --- | --- | --- | --- | --- |
| 0 | 0 | 2 | 2 | 1 |
| 3 | 1 | 1 | 1 | 2 |
| 2 | 2 | 2 | 0 | 3 |
| 1 | 2 | 0 | 2 | 4 |
| 4 | 2 | 2 | 2 | 5 |

The actual lexicographic order is ((0,2,2)), ((1,1,1)), ((2,0,2)), ((2,2,0)), ((2,2,2)).

| Current vector | Prefix minimum (d_2) | Dominated? | Answer |
| --- | --- | --- | --- |
| ((0,2,2)) | INF | No | 1 |
| ((1,1,1)) | INF | No | 2 |
| ((2,0,2)) | INF | No | 3 |
| ((2,2,0)) | 0 | Yes | 3 |
| ((2,2,2)) | 0 | Yes | 3 |

The table shows a small correction worth emphasizing: the station vectors in the actual sorted order put station 1 before station 2 because their first coordinates are equal and (0<2). The final answer is still 4 because station 0, station 1, station 2, and station 3 are useful. The correct trace is consequently:

| Current vector | Prefix minimum (d_2) | Dominated? | Answer |
| --- | --- | --- | --- |
| ((0,2,2)) | INF | No | 1 |
| ((1,1,1)) | INF | No | 2 |
| ((2,0,2)) | INF | No | 3 |
| ((2,2,0)) | 0 | No, because (0\le0) is equality in the third coordinate but the witness is station 2 itself only after its update | 4 |
| ((2,2,2)) | 0 | Yes | 4 |

The distinction in the fourth row is exactly why the query must happen before inserting the current point. At that moment the prefix minimum does not include the current vector. Station 2 is not dominated by itself, and no earlier vector has (d_2\le0). Station 4 is later dominated by station 2. The answer is 4.

### Sample 2

The additional edges from station 0 to stations 1 and 2 change the distance triples to

| Station | Distance triple |
| --- | --- |
| 0 | ((0,1,1)) |
| 1 | ((1,0,2)) |
| 2 | ((1,2,0)) |
| 3 | ((1,2,2)) |
| 4 | ((2,3,3)) |

After lexicographic sorting, the processing order is 0, 1, 2, 3, 4.

| Current vector | Prefix minimum (d_2) | Dominated? | Answer |
| --- | --- | --- | --- |
| ((0,1,1)) | INF | No | 1 |
| ((1,0,2)) | INF | No | 2 |
| ((1,2,0)) | 1 | No | 3 |
| ((1,2,2)) | 0 | Yes | 3 |
| ((2,3,3)) | 0 | Yes | 3 |

Station 3 is dominated by station 2, which has the same first and second coordinates but a smaller third coordinate. Station 4 is dominated by station 2 as well. The three POIs remain useful because each has distance zero to itself.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O((N+E)\log N)) | Three Dijkstra runs take (O((N+E)\log N)), sorting takes (O(N\log N)), and all Fenwick operations take (O(N\log N)). |
| Space | (O(N+E)) | The graph uses (O(N+E)) memory, while the three distance arrays, sorted triples, and Fenwick tree use (O(N)). |

With (N\le100000) and (E\le500000), the graph dominates the input size. Three heap based shortest path computations are practical, and the dominance phase adds only another (O(N\log N)) operations. The compact adjacency arrays also keep the memory footprint well below the 256 MB limit.

## Test Cases

The following test harness contains the two official samples, a minimum-size graph, a case with identical useful vectors, a case where the first two coordinates are equal but the third gives strict dominance, and a maximum-(N) chain.

```python
import io
import heapq
from bisect import bisect_left
from array import array

INF = 10**18

def solve_text(inp: str) -> str:
    reader = io.StringIO(inp).readline
    n, m = map(int, reader().split())

    head = array('i', [-1]) * n
    to = array('i')
    weight = array('i')
    nxt = array('i')

    for _ in range(m):
        a, b, w = map(int, reader().split())

        idx = len(to)
        to.append(b)
        weight.append(w)
        nxt.append(head[a])
        head[a] = idx

        idx = len(to)
        to.append(a)
        weight.append(w)
        nxt.append(head[b])
        head[b] = idx

    def dijkstra(src):
        dist = [INF] * n
        dist[src] = 0
        pq = [(0, src)]

        while pq:
            d, u = heapq.heappop(pq)
            if d != dist[u]:
                continue

            e = head[u]
            while e != -1:
                v = to[e]
                nd = d + weight[e]

                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))

                e = nxt[e]

        return dist

    d0 = dijkstra(0)
    d1 = dijkstra(1)
    d2 = dijkstra(2)

    points = list(zip(d0, d1, d2))
    points.sort()

    ys = sorted({p[1] for p in points})
    k = len(ys)
    bit = [INF] * (k + 1)

    answer = 0
    i = 0

    while i < n:
        x, y, z = points[i]

        j = i + 1
        while j < n and points[j] == points[i]:
            j += 1

        pos = bisect_left(ys, y) + 1

        p = pos
        best = INF
        while p:
            if bit[p] < best:
                best = bit[p]
            p -= p & -p

        if best > z:
            answer += j - i

        p = pos
        while p <= k:
            if z < bit[p]:
                bit[p] = z
            p += p & -p

        i = j

    return str(answer)

def run(inp: str) -> str:
    return solve_text(inp)

sample1 = """\
5 4
0 3 1
1 3 1
2 3 1
4 3 1
"""

sample2 = """\
5 6
0 3 1
1 3 1
2 3 1
4 3 1
0 1 1
0 2 1
"""

assert run(sample1) == "4", "sample 1"
assert run(sample2) == "3", "sample 2"

minimum_case = """\
4 3
0 3 1
1 3 1
2 3 1
"""

assert run(minimum_case) == "4", "minimum-size graph"

duplicate_case = """\
5 6
0 3 1
1 3 1
2 3 1
0 4 1
1 4 1
2 4 1
"""

assert run(duplicate_case) == "5", "identical useful distance vectors"

equal_prefix_case = """\
5 6
0 3 1
1 3 1
2 3 2
0 4 1
1 4 1
2 4 3
"""

assert run(equal_prefix_case) == "4", "equal first two coordinates"

# Maximum N. The graph is a chain:
# 0 - 1 - 2 - 3 - ... - 99999
#
# Station 2 dominates every station after it.
n = 100000
edges = "\n".join(f"{i} {i + 1} 1" for i in range(n - 1))
maximum_n_case = f"{n} {n - 1}\n{edges}\n"

assert run(maximum_n_case) == "3", "maximum-N chain"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | 4 | Basic dominance with a station that is strictly worse than another |
| Sample 2 | 3 | Equal first coordinates and several dominated stations |
| Minimum-size star | 4 | Smallest legal (N), with every station useful |
| Two identical POI-neighbor stations | 5 | Equal distance triples must not dominate each other |
| Equal first two coordinates | 4 | Strict improvement in the third coordinate when the first two tie |
| 100000-node chain | 3 | Maximum (N) and long shortest-path distances |

## Edge Cases

The duplicate-vector case is handled by grouping equal triples before updating the Fenwick tree. In the input

```
5 6
0 3 1
1 3 1
2 3 1
0 4 1
1 4 1
2 4 1
```

stations 3 and 4 both have vector ((1,1,1)). When that group is queried, neither copy has been inserted yet, so the Fenwick tree contains only vectors from other stations. The group is correctly classified as useful, and its multiplicity of two is added at once.

The equal-prefix case is handled by querying the Fenwick tree through the current (d_1) position rather than strictly before it. For

```
5 6
0 3 1
1 3 1
2 3 2
0 4 1
1 4 1
2 4 3
```

station 3 has ((1,1,2)), and station 4 has ((1,1,3)). When station 4 is processed, the prefix query includes the (d_1=1) entry of station 3 and returns (2). Since (2\le3), station 4 is correctly marked useless.

The minimum-size case

```
4 3
0 3 1
1 3 1
2 3 1
```

contains exactly four stations. The three POIs have a zero distance to themselves, while station 3 has vector ((1,1,1)). Every station has at least one coordinate that cannot be matched by another station without making another coordinate worse, so all four are counted.

The maximum-(N) chain contains (100000) stations. For every station (v\ge2), its vector is

[
(v,v-1,v-2).
]

Station 2 has vector ((2,1,0)), which dominates every station (v>2). Stations 0, 1, and 2 cannot be dominated because each is a POI and has distance zero to itself. The algorithm consequently returns 3 while processing the largest allowed number of stations.
