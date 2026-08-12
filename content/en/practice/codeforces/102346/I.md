---
title: "CF 102346I - Interplanetary"
description: "We have an undirected weighted graph whose vertices are planets and whose edges are direct travel routes. Every planet has a temperature."
date: "2026-08-13T01:35:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102346
codeforces_index: "I"
codeforces_contest_name: "2019-2020 ACM-ICPC Brazil Subregional Programming Contest"
rating: 0
weight: 102346
solve_time_s: 487
verified: true
draft: false
---

[CF 102346I - Interplanetary](https://codeforces.com/problemset/problem/102346/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 8m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an undirected weighted graph whose vertices are planets and whose edges are direct travel routes. Every planet has a temperature. A customer asks for the shortest route from planet (A) to planet (B), but places a restriction on every intermediate planet: depending on the request, an intermediate planet must belong to the coldest (K) temperature levels or the hottest (K) temperature levels.

The source and destination are exempt from the temperature restriction. Only vertices strictly between them on the route have to satisfy it. The answer is the minimum total edge length of a valid route, or (-1) when no valid route exists.

The phrase "coldest (K) temperatures" is best understood through the temperature threshold induced by the (K)-th smallest temperature. Equal temperatures must be treated as one boundary group. For example, if the temperatures are (5,10,10,20), the two coldest temperatures are (5) and (10), so both planets with temperature (10) are allowed. The same applies symmetrically to the hottest side. The second sample depends on exactly this behavior: with (K=2) on the hot side, the temperatures (20) and (10) are allowed, so all three planets at temperature (10) can be used.

The graph has at most 400 vertices, while there can be up to (N(N-1)/2), roughly 80,000, edges, and as many as 100,000 queries. The small number of vertices strongly suggests an all-pairs shortest-path technique, while the huge number of queries rules out running a shortest-path algorithm independently for every request. The official archived statement gives a 1 second time limit and 1024 MB memory limit, so the intended implementation is a compact (O(N^3)) Floyd-Warshall style solution.

Several details can cause a seemingly reasonable implementation to return a wrong answer.

First, the endpoints are unrestricted. Consider:

```
2 1
0 10
1 2 7
1
1 2 1 0
```

The answer is `7`. Planet 1 is coldest, but planet 2 does not need to satisfy the restriction because it is the destination. A solution that simply deletes every planet outside the allowed temperature set would delete planet 2 and incorrectly return `-1`.

Second, equal temperatures have to be handled as a group. Consider:

```
4 3
1 2 2 3
1 2 1
2 3 1
3 4 1
2
1 4 2 0
1 4 2 1
```

For the cold request, the second coldest temperature is `2`, so both planets 2 and 3 are allowed. The route has length `3`. For the hot request, the second hottest temperature is also `2`, so the same route is valid and the answer is again `3`. An implementation that selects exactly two planet indices rather than using the temperature threshold could accidentally allow only one of the two planets with temperature `2`.

Third, a direct edge must remain available even when neither endpoint belongs to the permitted temperature set. For example:

```
3 1
0 50 100
1 3 9
1
1 3 1 0
```

The answer is `9`, because the route has no intermediate planet at all. A solution that requires every vertex of the route to be in the allowed set would incorrectly reject it.

Finally, disconnected graphs must remain disconnected throughout the computation. For example:

```
2 0
0 1
1
1 2 1 0
```

The answer is `-1`, not a large finite value. The implementation therefore needs an infinity value and must translate an unreachable distance back to `-1`.

## Approaches

The most direct approach is to process each customer independently. For one query, we can determine the allowed temperature threshold, ignore forbidden intermediate planets, and run Dijkstra's algorithm from (A) to (B). Since all route lengths are positive, Dijkstra is correct for each individual request.

The problem is the number of requests. In the worst case there are about 80,000 edges and 100,000 queries. Even using a good heap implementation, processing every request independently costs (O(Q(R+N)\log N)). With the maximum bounds, that means on the order of (10^5 \cdot 8\cdot10^4), roughly billions of edge-related operations before accounting for the logarithmic factor. Recomputing an all-pairs solution per query would be even worse, at (O(QN^3)), around (6.4\cdot10^{11}) Floyd-Warshall relaxations.

The structure that makes a faster solution possible is that the allowed set is nested. As we move from the coldest temperature to hotter temperatures, we only add planets. For a cold request, the allowed intermediate vertices are all planets whose temperature is at most some threshold. A request with a larger (K) therefore has a superset of the vertices available to a request with a smaller (K). The same nesting exists when processing temperatures from hottest to coldest.

This is exactly the setting where Floyd-Warshall can be viewed as a dynamic program over the set of permitted intermediate vertices. Suppose the first (k) temperature groups have been activated. Let `dist[i][j]` be the shortest distance from (i) to (j) whose internal vertices all belong to those activated groups. When a new planet (v) becomes allowed, every new shortest path either does not use (v), or can be split into a path from (i) to (v) followed by a path from (v) to (j). The recurrence is the usual Floyd-Warshall relaxation:

[
dist[i][j] = \min(dist[i][j], dist[i][v] + dist[v][j]).
]

We run this process once from cold to hot and once from hot to cold. Queries are stored according to the number of temperature groups that their threshold activates, so each query is answered exactly when its required state of the distance matrix has been reached.

The equal-temperature issue fits naturally into this formulation. We do not answer queries halfway through a temperature group. Every planet having the same temperature is activated first, and only then are queries whose threshold reaches that temperature answered.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force with Dijkstra per query | (O(QR\log N)) in the dense worst case | (O(N+R)) | Too slow |
| Optimal grouped Floyd-Warshall | (O(N^3+Q)) | (O(N^2+Q)) | Accepted |

The two Floyd passes contribute (2N^3), which is still (O(N^3)). With (N\le400), this is the intended asymptotic solution. A compiled implementation is the safest choice under the archived 1 second limit. The Python implementation below uses local variables and in-place matrices to keep the constant factors as low as practical.

## Algorithm Walkthrough

1. Read the graph and build an (N\times N) distance matrix. Set the diagonal to zero, put every direct route into the matrix, and leave nonexistent routes at infinity. The graph is undirected, so an edge between (u) and (v) initializes both `dist[u][v]` and `dist[v][u]`.
2. Sort all planet temperatures and construct the distinct temperature levels in ascending order. Planets with the same temperature are placed in the same group because a threshold at that temperature must allow all of them.
3. For every possible value of (K), determine which temperature group is reached by the (K)-th smallest temperature. If the sorted temperature at position (K-1) is (x), every planet with temperature at most (x) is allowed. Store the corresponding number of cold temperature groups.
4. Do the symmetric preprocessing for hot requests. The (K)-th largest temperature defines the upper threshold, so every planet with temperature at least that value is allowed. Store the corresponding number of hot temperature groups.
5. Put every query into a bucket according to its effective number of cold or hot temperature groups. A query does not need to be processed immediately because all queries requiring the same group count use the same distance matrix.
6. For cold queries, process the temperature groups from the coldest to the hottest. When a group is reached, run the Floyd-Warshall relaxation once for every planet in that group. Adding all planets in the group before answering queries is necessary because equal-temperature planets are all permitted by the same threshold.
7. After an entire group has been activated, answer every cold query in that group's bucket by reading `dist[A][B]`. If it is still infinity, store `-1`.
8. Reinitialize the distance matrix to the original graph and process the temperature groups from hottest to coldest. Apply exactly the same Floyd-Warshall relaxation, but answer the hot query buckets instead.
9. Finally, print the stored answers in their original query order. The two passes never need to coexist as distance matrices, so only one (N\times N) matrix is kept at a time.

### Why it works

After a particular number of temperature groups has been activated, the Floyd-Warshall invariant is that `dist[i][j]` equals the shortest route from (i) to (j) whose internal planets belong to the activated groups. When a new planet (v) is added, every route using (v) internally can be decomposed at (v), so the relaxation through (v) considers every newly possible route. Routes not using (v) remain unchanged. Applying this to every planet in a temperature group gives the exact shortest paths whose intermediate temperatures satisfy that threshold. Since a query is answered only after its entire boundary temperature group has been activated, all planets tied at the threshold are available. The endpoints are never removed from the matrix, so they remain usable regardless of their temperatures.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**15

def process_orientation(n, groups, buckets, dist, answers):
    rng = range(n)

    for level, vertices in enumerate(groups, 1):
        for k in vertices:
            dk = dist[k]

            for i in rng:
                di = dist[i]
                dik = di[k]

                if dik >= INF:
                    continue

                for j in rng:
                    cand = dik + dk[j]
                    if cand < di[j]:
                        di[j] = cand

        for qi, a, b in buckets[level]:
            d = dist[a][b]
            answers[qi] = -1 if d >= INF else d

def solve():
    n, r = map(int, input().split())
    temp = list(map(int, input().split()))

    edges = []
    for _ in range(r):
        x, y, d = map(int, input().split())
        x -= 1
        y -= 1
        edges.append((x, y, d))

    q = int(input())

    queries = []
    for qi in range(q):
        a, b, k, typ = map(int, input().split())
        queries.append((a - 1, b - 1, k, typ))

    sorted_temp = sorted(temp)

    unique_temp = []
    for x in sorted_temp:
        if not unique_temp or unique_temp[-1] != x:
            unique_temp.append(x)

    groups_asc = []
    current = []
    last_temp = None

    for v in sorted(range(n), key=lambda x: temp[x]):
        if last_temp is None or temp[v] == last_temp:
            current.append(v)
        else:
            groups_asc.append(current)
            current = [v]
        last_temp = temp[v]

    if current:
        groups_asc.append(current)

    groups_desc = list(reversed(groups_asc))
    group_count = len(groups_asc)

    # cold_level[k] = number of cold temperature groups allowed
    # by the K-th smallest temperature.
    cold_level = [0] * (n + 1)

    # hot_level[k] = number of hot temperature groups allowed
    # by the K-th largest temperature.
    hot_level = [0] * (n + 1)

    # Map each planet temperature to its group from the cold side.
    temp_to_cold_group = {}
    for idx, x in enumerate(unique_temp):
        temp_to_cold_group[x] = idx + 1

    # Map each planet temperature to its group from the hot side.
    temp_to_hot_group = {}
    for idx, x in enumerate(unique_temp):
        temp_to_hot_group[x] = group_count - idx

    for k in range(1, n + 1):
        cold_level[k] = temp_to_cold_group[sorted_temp[k - 1]]
        hot_level[k] = temp_to_hot_group[sorted_temp[n - k]]

    cold_buckets = [[] for _ in range(group_count + 1)]
    hot_buckets = [[] for _ in range(group_count + 1)]

    for qi, (a, b, k, typ) in enumerate(queries):
        if typ == 0:
            level = cold_level[k]
            cold_buckets[level].append((qi, a, b))
        else:
            level = hot_level[k]
            hot_buckets[level].append((qi, a, b))

    answers = [-1] * q

    def initial_dist():
        dist = [[INF] * n for _ in range(n)]

        for i in range(n):
            dist[i][i] = 0

        for x, y, d in edges:
            if d < dist[x][y]:
                dist[x][y] = d
                dist[y][x] = d

        return dist

    if any(cold_buckets):
        dist = initial_dist()
        process_orientation(
            n,
            groups_asc,
            cold_buckets,
            dist,
            answers
        )

    if any(hot_buckets):
        dist = initial_dist()
        process_orientation(
            n,
            groups_desc,
            hot_buckets,
            dist,
            answers
        )

    sys.stdout.write("\n".join(map(str, answers)))

if __name__ == "__main__":
    solve()
```

The first part of the implementation constructs the original graph matrix. Because every route length is positive and (N\le400), an infinity value of (10^{15}) is comfortably larger than every possible simple route, whose length is at most roughly (399\cdot1000).

The temperature preprocessing is the subtle part. `unique_temp` contains each distinct temperature once, while `groups_asc` contains the actual planet indices belonging to each temperature. The two structures serve different purposes. The unique values tell us which threshold a query reaches, while the groups tell Floyd-Warshall which vertices must be activated at that threshold.

The arrays `cold_level` and `hot_level` convert the original query parameter (K) into a group number. For a cold query, `sorted_temp[k - 1]` is the (K)-th smallest temperature. Every planet with that temperature must be allowed, so `temp_to_cold_group` gives the complete group boundary. The hot calculation uses `sorted_temp[n - k]` for the (K)-th largest temperature.

This conversion also handles duplicates correctly. If the temperatures are `5, 10, 10, 20` and `K=2`, the cold threshold is `10`, and both planets with temperature `10` belong to the activated groups. If all temperatures are equal, even `K=1` activates the single temperature group containing every planet.

The query buckets are what remove the (Q) factor from the expensive part. Every query with the same effective threshold can be answered from the same distance matrix state, so there is no reason to run another shortest-path computation for it.

Inside `process_orientation`, the outer loop walks through temperature groups. Each planet in the current group becomes a legal intermediate vertex, and the standard Floyd-Warshall relaxation is applied. The query bucket is processed only after every vertex of the group has been added.

The source and destination are never filtered out. They remain present in the matrix from the beginning, which directly handles the rule that endpoint temperatures do not matter.

The implementation rebuilds the original distance matrix before the second orientation. Mutating the matrix during the cold sweep cannot be reused for the hot sweep because the two sweeps have different sets of allowed intermediate vertices.

Python integers do not overflow, and the chosen infinity is far above any valid route length. The archived contest has a very tight 1 second limit, so the Python version should be considered a PyPy-oriented implementation of the intended algorithm rather than a guarantee of matching a C++ submission's runtime. The algorithm itself is (O(N^3)), which is the intended bound for (N\le400).

## Worked Examples

### Sample 1

The temperatures in ascending order are:

```
planet 5: -210
planet 2: -180
planet 1:  -53
planet 6:   15
planet 7:  150
planet 4:  420
planet 3:  456
```

All temperatures are distinct here, so every temperature group contains exactly one planet.

For the hot sweep, the groups are processed as `3, 4, 7, 6, 1, 2, 5`.

| Hot groups activated | Newly available planet | Query affected | Distance |
| --- | --- | --- | --- |
| 1 | 3 | `1 -> 2`, K=1 | 2 |
| 2 | 4 | `1 -> 5`, K=2 | 11 |
| 2 | 4 | `1 -> 7`, K=2 | 3 |

The first query already has a direct edge from 1 to 2, so its answer is 2. After planets 3 and 4 are available, the route `1 -> 3 -> 4 -> 5` has length `1 + 6 + 4 = 11`. The route `1 -> 3 -> 7` has length `1 + 2 = 3`.

The cold sweep starts with planet 5, so the query from 5 to 6 with (K=1) cannot use planet 4, the only useful connection toward planet 6. It remains unreachable.

The official sample output is `11, 2, -1, 3`.

### Sample 2

The temperatures are:

```
planet 1: 5
planet 2: 10
planet 3: 20
planet 4: 10
planet 5: 10
planet 6: 8
```

There are four distinct temperature groups:

```
{1}: 5
{6}: 8
{2,4,5}: 10
{3}: 20
```

For hot queries, the processing order is:

```
{3}, {2,4,5}, {6}, {1}
```

| Hot groups activated | Allowed temperature values | Query | Distance |
| --- | --- | --- | --- |
| 1 | `{20}` | `1 -> 6`, K=1 | -1 |
| 2 | `{20, 10}` | `1 -> 6`, K=2 | 25 |
| 1 | `{20}` | `2 -> 4`, K=1 | 10 |

After the first group, only planet 3 may be used as an intermediate, so the chain from 1 to 6 cannot be completed. After the second group, planets 2, 4, and 5 all become available because they share temperature 10. The full path

```
1 -> 2 -> 3 -> 4 -> 5 -> 6
```

has length `5 + 5 + 5 + 5 + 5 = 25`.

For the cold query from 4 to 5 with (K=1), the coldest temperature is 5, corresponding to planet 1. The direct edge from 4 to 5 is already enough, so the answer is 5.

The final sample output is `25, -1, 5, 10`.

The second sample is especially useful because it catches the most dangerous interpretation mistake. Selecting exactly (K) planet indices would not allow all three planets at temperature 10, while selecting the (K)-th temperature as a threshold does.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N^3 + Q)) | Each of the two temperature sweeps performs at most (N) Floyd-Warshall vertex insertions, each costing (O(N^2)), while every query is bucketed and answered once. |
| Space | (O(N^2 + Q)) | The distance matrix uses (O(N^2)), and the query buckets plus answer array use (O(Q)). |

There are two Floyd-Warshall sweeps, one for each temperature direction, but the constant factor of two disappears in the asymptotic bound. With (N=400), the cubic term is bounded by (2\cdot400^3=128,000,000) elementary matrix relaxations in the worst case. The query processing itself is linear in (Q), so even 100,000 requests add little compared with the matrix computation.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()

        solve()

        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
sample1 = """\
7 9
-53 -180 456 420 -210 15 150
1 2 2
1 3 1
2 3 4
2 4 2
2 5 5
3 4 6
6 4 10
4 5 4
3 7 2
4
1 5 2 1
1 2 1 1
5 6 1 0
1 7 2 1
"""

assert run(sample1) == "11\n2\n-1\n3", "sample 1"

# Provided sample 2
sample2 = """\
6 5
5 10 20 10 10 8
1 2 5
2 3 5
3 4 5
4 5 5
5 6 5
4
1 6 2 1
1 6 1 1
4 5 1 0
2 4 1 1
"""

assert run(sample2) == "25\n-1\n5\n10", "sample 2"

# Minimum-size graph, direct edge, endpoints must remain unrestricted.
case_min = """\
2 1
-5 100
1 2 7
2
1 2 1 0
1 2 1 1
"""

assert run(case_min) == "7\n7", "minimum-size direct route"

# No edges, so even though the endpoints themselves may have any
# temperature, no route exists.
case_disconnected = """\
2 0
0 1
2
1 2 1 0
1 2 1 1
"""

assert run(case_disconnected) == "-1\n-1", "disconnected graph"

# Equal temperatures at the boundary must all be admitted.
case_equal_boundary = """\
4 3
1 2 2 3
1 2 1
2 3 1
3 4 1
2
1 4 2 0
1 4 2 1
"""

assert run(case_equal_boundary) == "3\n3", "equal-temperature boundary"

# All temperatures equal. K=1 already includes every planet.
case_all_equal = """\
4 3
10 10 10 10
1 2 2
2 3 3
3 4 4
2
1 4 1 0
1 4 1 1
"""

assert run(case_all_equal) == "9\n9", "all equal temperatures"

# Maximum-size N and Q, with no edges. This exercises the query limit
# without requiring a huge expected-output literal.
n = 400
q = 100000

parts = [
    f"{n} 0",
    " ".join(["0"] * n),
    str(q),
]

for i in range(q):
    a = (i % n) + 1
    b = ((i + 1) % n) + 1
    parts.append(f"{a} {b} 1 {i & 1}")

case_max = "\n".join(parts) + "\n"

expected_max = "-1\n" * q
assert run(case_max) == expected_max[:-1], "maximum N and Q"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum graph with one edge | `7`, `7` | Minimum (N), direct routes, unrestricted endpoints |
| Two isolated planets | `-1`, `-1` | Unreachable pairs and infinity handling |
| Four planets with two equal boundary temperatures | `3`, `3` | All planets tied at the threshold must be activated |
| Four planets with identical temperatures | `9`, `9` | A single temperature group can contain every planet |
| (N=400,\ Q=100000), no edges | 100,000 lines of `-1` | Maximum query count, maximum vertex count, large-output handling |

## Edge Cases

### Endpoints outside the allowed temperature range

Consider:

```
2 1
0 100
1 2 7
1
1 2 1 0
```

The coldest temperature is 0, so only planet 1 belongs to the allowed intermediate set. The route from 1 to 2 is nevertheless valid because planet 2 is the destination, not an intermediate planet. The distance matrix contains the direct edge from the beginning, so the algorithm answers `7` before any intermediate vertex is needed.

### Equal temperatures at the threshold

Consider:

```
4 3
1 2 2 3
1 2 1
2 3 1
3 4 1
1
1 4 2 0
```

The second smallest temperature is 2. Both planets 2 and 3 have that temperature, so both are activated before the query is answered. Floyd-Warshall finds `1 -> 2 -> 3 -> 4` with distance 3. If the implementation activated only one planet for the second temperature position, it would incorrectly report that the destination is unreachable.

### All planets have the same temperature

Consider:

```
4 3
10 10 10 10
1 2 2
2 3 3
3 4 4
1
1 4 1 0
```

The first coldest temperature is 10, and every planet has that temperature. The entire temperature group is activated immediately, so the route `1 -> 2 -> 3 -> 4` is allowed and costs 9. The same is true for a hottest request. This is why the algorithm works with temperature groups rather than individual sorted positions.

### No route exists

Consider:

```
2 0
0 1
1
1 2 1 0
```

The distance matrix starts with `dist[1][2] = INF`. There is no edge and no possible intermediate planet, so no Floyd-Warshall relaxation can make the pair reachable. The query sees infinity and converts it to `-1`.

### Direct route with forbidden intermediate planets

Consider:

```
3 1
0 50 100
1 3 9
1
1 3 1 0
```

The only edge goes directly from source 1 to destination 3. Planet 2 is irrelevant because it is not used. The cold restriction does not invalidate the direct route, and the answer is 9. The matrix representation naturally handles this because direct edges are present before any temperature group is activated.

### (K=N)

When (K=N), the (K)-th smallest temperature is the maximum temperature, so every planet belongs to the allowed cold set. Symmetrically, the (K)-th largest temperature is the minimum temperature, so every planet belongs to the allowed hot set. The preprocessing maps both cases to all temperature groups, giving ordinary all-pairs shortest paths.

### Queries with duplicate temperatures and (K) inside a tie

Suppose the temperatures are `5, 10, 10, 10, 20`. For (K=2), the second smallest temperature is 10, not a particular one of the three planets with temperature 10. The allowed cold temperatures are therefore 5 and 10, which activates all four planets at those temperatures. The `cold_level` calculation uses the temperature value itself, so it automatically expands the threshold to the whole tie group.

### Empty edge set

When (R=0), every off-diagonal distance starts at infinity. The Floyd-Warshall loops still run correctly, but there is never a finite pair to relax. Queries consequently return `-1` unless a query could have (A=B), which the input explicitly forbids.
