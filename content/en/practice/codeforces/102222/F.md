---
title: "CF 102222F - Moving On"
description: "We have a complete undirected weighted graph of cities. City i has a risk value r[i], and d[i][j] is the direct travel distance between cities i and j. A query gives two endpoints u and v, together with a risk threshold w."
date: "2026-08-17T22:07:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102222
codeforces_index: "F"
codeforces_contest_name: "2018-2019 ACM-ICPC, China Multi-Provincial Collegiate Programming Contest"
rating: 0
weight: 102222
solve_time_s: 88
verified: true
draft: false
---

[CF 102222F - Moving On](https://codeforces.com/problemset/problem/102222/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a complete undirected weighted graph of cities. City `i` has a risk value `r[i]`, and `d[i][j]` is the direct travel distance between cities `i` and `j`. A query gives two endpoints `u` and `v`, together with a risk threshold `w`.

For that query, we want the shortest route from `u` to `v` under one restriction: every intermediate city on the route must have risk at most `w`. The endpoints themselves are allowed regardless of their risk, because the restriction applies to cities other than the two endpoints. The direct edge from `u` to `v` is consequently always a valid candidate when `u != v`.

The input contains up to 50 independent test cases. Each test case has at most 200 cities and up to 20,000 queries. The distance matrix already gives an edge between every pair of cities, so the graph is dense. Since `n` is only 200, an `O(n^3)` preprocessing algorithm is practical. The large query count changes what we should avoid: running a full shortest path computation independently for every query would be far too expensive.

A useful way to estimate the brute-force cost is to take the largest values, `n = 200` and `q = 20,000`. A Floyd-Warshall computation needs about `200^3 = 8,000,000` relaxation iterations for one query. Repeating that for all queries gives roughly `1.6 * 10^11` iterations in the worst case, before accounting for Python overhead. We need to make the expensive graph computation independent of the number of queries.

There are several edge cases that are easy to mishandle. First, the endpoints do not have to satisfy the threshold. For example, consider

```
1
2 1
10 1
0 5
5 0
1 2 1
```

There is no intermediate city at all, so the direct route from city 1 to city 2 is valid and the answer is `5`. A solution that removes every city whose risk exceeds `w`, including the endpoints, would incorrectly declare the route impossible.

Second, an endpoint can be the same city. For example,

```
1
1 1
100
0
1 1 1
```

The answer is `0`. The city does not need to satisfy the threshold because we are already at the destination, and no intermediate city is used.

Third, a path can use several allowed intermediate cities. For example,

```
1
3 1
1 1 2
0 10 100
10 0 10
100 10 0
1 3 1
```

With threshold `1`, city 2 is allowed as an intermediate city, so the route `1 -> 2 -> 3` costs `20`, which is better than the direct cost `100`. A solution that checks only direct edges, or only one intermediate city without allowing the Floyd-Warshall relaxation to repeat, would miss this improvement.

The phrase "other city" also means that the threshold is a restriction on intermediate vertices, not on the whole path's vertex set. This distinction is the central detail behind the solution.

## Approaches

A straightforward approach is to process every query independently. For a query `(u, v, w)`, we could start with the original distance matrix and run Floyd-Warshall while allowing only cities with `r[i] <= w` as intermediate vertices. Floyd-Warshall is correct here because after processing a set of allowed intermediate cities, `dist[i][j]` represents the shortest route from `i` to `j` whose internal vertices belong to that set.

The problem is the repeated work. With `n = 200`, one Floyd-Warshall run costs `O(n^3) = O(8 * 10^6)`. With `q = 20,000` queries, the worst case is `O(qn^3)`, around `1.6 * 10^11` relaxation operations. The graph itself does not change between queries, only the maximum allowed risk does, so recomputing the same relaxations is wasteful.

The key observation is that the allowed set of intermediate cities grows monotonically as `w` increases. Suppose we sort all cities by their risk. For a small threshold, perhaps only the safest city is available as an intermediate. When the threshold increases enough to include the next city, we do not need to recompute all previous work. We can take the current shortest-path matrix and perform exactly one Floyd-Warshall phase using the newly enabled city.

This is precisely the structure of Floyd-Warshall. Its `k`-th phase adds vertex `k` to the set of vertices that may be used internally. Here, we simply choose the order of those phases according to city risk rather than city index.

We can process the queries in increasing order of `w`. While moving through the sorted queries, we progressively activate every city whose risk is at most the current query's threshold. Whenever a city becomes active, we run one Floyd-Warshall relaxation phase through it. After all cities with `r[i] <= w` have been activated, the matrix contains the shortest paths using exactly the intermediate cities permitted by that query.

The endpoints need special consideration conceptually, but no special modification is necessary in the matrix. Even if `u` or `v` has risk greater than `w`, the direct edge `u -> v` remains present, and the Floyd-Warshall matrix is allowed to use either endpoint as a source or destination. We only control which vertices are used as intermediate vertices.

The resulting comparison is:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(qn^3)` | `O(n^2)` | Too slow |
| Optimal | `O(n^3 + q log q)` | `O(n^2 + q)` | Accepted |

The `q log q` term comes from sorting the queries. The Floyd-Warshall phases contribute `O(n^3)` because each of the `n` cities is activated exactly once.

## Algorithm Walkthrough

1. Read the risk of every city and the complete distance matrix. Keep the matrix as the current shortest-path matrix, initially containing only direct travel distances.
2. Sort the city indices by their risk values. The sorted order determines when each city becomes available as an intermediate vertex.
3. Read all queries and store each query together with its original position. Sort the queries by their threshold `w`, because processing them in this order means the set of allowed intermediate cities only grows.
4. Maintain a pointer into the sorted city list. For the current query threshold `w`, activate every city whose risk is at most `w`. For each newly activated city `k`, perform the Floyd-Warshall relaxation

```
dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
```

for every pair `i, j`.

The order matters here. A city is activated once, and its relaxation is performed after all cities with smaller risk have already been activated. This matches the standard Floyd-Warshall invariant, with risk order replacing numerical vertex order.
5. After all cities with risk at most `w` have been activated, `dist[u][v]` is the answer for the query. Store it at the query's original position so that the final output remains in input order.
6. Print the answers in their original query order, preceded by the required `Case #x:` header.

### Why it works

Consider the moment immediately after a city `k` has been activated. All cities with smaller or equal risk that were activated earlier are already available as intermediate vertices. Before processing `k`, `dist[i][j]` is the shortest path whose intermediate cities belong to the already activated set. Any newly improved path that becomes possible after adding `k` has the form `i -> ... -> k -> ... -> j`, where both sides use only previously activated intermediate cities. The Floyd-Warshall relaxation checks exactly that possibility through `dist[i][k] + dist[k][j]`.

By induction over the activation order, after activating every city with risk at most `w`, `dist[i][j]` is the shortest path whose intermediate cities all have risk at most `w`. Since the endpoints are not restricted, this is exactly the set of routes allowed by the query. Thus `dist[u][v]` is the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    output = []

    for case_id in range(1, t + 1):
        n, q = map(int, input().split())
        risk = list(map(int, input().split()))

        dist = [list(map(int, input().split())) for _ in range(n)]

        cities = sorted(range(n), key=risk.__getitem__)

        queries = []
        for idx in range(q):
            u, v, w = map(int, input().split())
            queries.append((w, u - 1, v - 1, idx))

        queries.sort()

        ans = [0] * q
        city_ptr = 0

        for w, u, v, idx in queries:
            while city_ptr < n and risk[cities[city_ptr]] <= w:
                k = cities[city_ptr]

                dk = dist[k]

                for i in range(n):
                    di = dist[i]
                    dik = di[k]

                    for j in range(n):
                        candidate = dik + dk[j]
                        if candidate < di[j]:
                            di[j] = candidate

                city_ptr += 1

            ans[idx] = dist[u][v]

        output.append(f"Case #{case_id}:")
        output.extend(map(str, ans))

    sys.stdout.write("\n".join(output))

if __name__ == "__main__":
    solve()
```

The first major part of the implementation reads the matrix directly into `dist`. We mutate this matrix throughout the algorithm, so after a city has been activated, `dist` contains the best distances using all currently available intermediate cities.

The `cities` array stores city indices rather than risk values themselves. Sorting it by `risk.__getitem__` gives the exact order in which vertices should be introduced into Floyd-Warshall.

Queries are stored as `(w, u, v, original_index)` and sorted by `w`. The original index is necessary because sorting changes the order in which answers are computed, while the output must follow the order of the input.

The `while` loop activates all cities satisfying `risk[city] <= w`. The comparison is deliberately `<=`, not `<`. A city whose risk equals the query threshold is allowed.

For every activated city `k`, the nested loops perform one complete Floyd-Warshall phase. The variables `dk`, `di`, and `dik` are local references used to reduce Python indexing overhead. Since the time limit is relatively generous for C++ but Python has significantly higher per-operation cost, these small optimizations matter when the matrix reaches its maximum size.

The relaxation uses Python integers, so there is no integer overflow concern. A shortest simple path uses at most `n - 1` edges, and with each edge at most `10^5`, the answer is comfortably within Python's integer range anyway.

The endpoints are never removed based on their risks. The matrix always contains every direct edge, and the algorithm restricts only the vertices chosen as Floyd-Warshall intermediates. Consequently, a query such as `u = 1`, `v = 2`, `w = 1` remains valid even when city 1 has risk `100`.

The self-query case also works without special handling because `dist[u][u]` starts at zero and cannot become positive through a shortest-path relaxation.

## Worked Examples

Only one sample is provided in the statement, so the second trace below uses a small constructed input that exposes the endpoint-threshold behavior.

### Sample 1

The risks are `[1, 2, 3]`, and the direct distances are:

```
0 1 3
1 0 1
3 1 0
```

The queries are processed in threshold order. The relevant state is:

| Query threshold | Newly activated cities | Relevant distance | Answer |
| --- | --- | --- | --- |
| `1` | city 1 | `dist[1][1] = 0` | `0` |
| `1` | none | `dist[1][2] = 1` | `1` |
| `1` | none | `dist[1][3] = 3` | `3` |
| `2` | city 2 | `dist[1][2] = 1` | `1` |
| `2` | none | `dist[1][3] = 2` | `2` |
| `2` | none | `dist[1][1] = 0` | `0` |

When only city 1 is allowed as an intermediate, the path from city 1 to city 3 still costs `3`. Once city 2 becomes available, the relaxation through city 2 changes that distance to `1 + 1 = 2`.

The query order in the input is preserved using the stored original indices, so the resulting output is:

```
Case #1:
0
1
3
0
1
2
```

### Constructed Example

Consider:

```
1
3 3
5 1 1
0 10 100
10 0 10
100 10 0
1 3 1
1 3 5
1 1 1
```

The sorted city order by risk is city 2, city 3, city 1, because their risks are `1, 1, 5`.

The processing state is:

| Query threshold | Newly activated cities | `dist[1][3]` | Query answer |
| --- | --- | --- | --- |
| `1` | city 2, city 3 | `20` | `20` |
| `1` | none | `20` | `0` for `1 -> 1` |
| `5` | city 1 | `20` | `20` |

For threshold `1`, city 1 is not an allowed intermediate, but city 2 is. The route `1 -> 2 -> 3` costs `20`, so the first query is answered with `20`.

For the self-query `1 -> 1`, the risk of city 1 being `5` is irrelevant. No intermediate city is required, and the diagonal entry remains `0`.

When the threshold becomes `5`, city 1 is activated too. It cannot improve the already optimal route in this example, so the distance remains `20`.

This trace demonstrates both the monotonic activation process and the fact that endpoint risks do not restrict the query.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n^3 + q log q)` | Each city causes one `O(n^2)` Floyd-Warshall phase, and all queries are sorted once |
| Space | `O(n^2 + q)` | The distance matrix takes `O(n^2)`, while stored queries and answers take `O(q)` |

For `n <= 200`, the preprocessing requires only `n` Floyd-Warshall phases, or about `8 * 10^6` pair relaxations in the largest test case. The queries add only sorting work and constant-time lookups after preprocessing. The memory usage is also modest because the algorithm keeps only one `n x n` matrix instead of storing a separate shortest-path matrix for every possible threshold.

## Test Cases

The following test harness uses a function version of the same algorithm so that each input can be tested independently.

```python
import sys
import io

def solve_input(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    try:
        input = sys.stdin.readline
        t = int(input())
        output = []

        for case_id in range(1, t + 1):
            n, q = map(int, input().split())
            risk = list(map(int, input().split()))
            dist = [list(map(int, input().split())) for _ in range(n)]

            cities = sorted(range(n), key=risk.__getitem__)

            queries = []
            for idx in range(q):
                u, v, w = map(int, input().split())
                queries.append((w, u - 1, v - 1, idx))

            queries.sort()

            ans = [0] * q
            ptr = 0

            for w, u, v, idx in queries:
                while ptr < n and risk[cities[ptr]] <= w:
                    k = cities[ptr]
                    dk = dist[k]

                    for i in range(n):
                        di = dist[i]
                        dik = di[k]

                        for j in range(n):
                            nd = dik + dk[j]
                            if nd < di[j]:
                                di[j] = nd

                    ptr += 1

                ans[idx] = dist[u][v]

            output.append(f"Case #{case_id}:")
            output.extend(map(str, ans))

        return "\n".join(output)
    finally:
        sys.stdin = old_stdin

# Provided sample.
sample1 = """\
1
3 6
1 2 3
0 1 3
1 0 1
3 1 0
1 1 1
1 2 1
1 3 1
1 1 2
1 2 2
1 3 2
"""

assert solve_input(sample1) == """\
Case #1:
0
1
3
0
1
2
""", "sample 1"

# Minimum-size graph, self query and a direct query.
case2 = """\
1
1 2
7
0
1 1 1
1 1 7
"""

assert solve_input(case2) == """\
Case #1:
0
0
""", "minimum-size graph"

# Endpoint may have risk greater than the threshold.
case3 = """\
1
2 2
100 1
0 5
5 0
1 2 1
1 2 100
"""

assert solve_input(case3) == """\
Case #1:
5
5
""", "endpoint risk must not block direct travel"

# Equality boundary and a useful intermediate city.
case4 = """\
1
3 3
5 2 7
0 10 100
10 0 10
100 10 0
1 3 1
1 3 2
1 3 7
"""

assert solve_input(case4) == """\
Case #1:
100
20
20
""", "risk == w must be allowed"

# All risks equal, so every city is activated for the threshold.
case5 = """\
1
4 3
10 10 10 10
0 8 50 50
8 0 7 50
50 7 0 6
50 50 6 0
1 4 1
1 4 10
2 4 10
"""

assert solve_input(case5) == """\
Case #1:
50
21
13
""", "all equal risks"
```

The custom cases can be summarized as follows:

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `case2` | `0, 0` | Smallest possible graph and diagonal distance |
| `case3` | `5, 5` | An endpoint may exceed the threshold |
| `case4` | `100, 20, 20` | Exact `risk == w` boundary and newly enabled intermediate city |
| `case5` | `50, 21, 13` | All risks equal and repeated Floyd-Warshall improvements |

## Edge Cases

The first edge case is an endpoint whose risk is above the threshold. In `case3`, city 1 has risk `100`, while the query threshold is only `1`. The graph has two cities and direct distance `5`. No intermediate city is needed, so the answer is `5`. The activation loop only controls which city can serve as `k` in a Floyd-Warshall phase. It never removes city 1 from the matrix, so `dist[0][1]` remains `5`.

The second edge case is a query from a city to itself. In `case2`, the only city has risk `7`, while the first query uses threshold `1`. No city is needed as an intermediate vertex because the starting city is already the destination. The diagonal entry starts as `0`, and every Floyd-Warshall update has the form `dist[i][i] <= dist[i][k] + dist[k][i]`, so the zero remains optimal. The answer is consequently `0`.

The third edge case is the equality boundary. In `case4`, city 2 has risk exactly `2`, and the query threshold is `2`. The condition in the activation loop is `risk[cities[ptr]] <= w`, so city 2 becomes available. The route `1 -> 2 -> 3` costs `10 + 10 = 20`, improving the direct distance `100`. Using `< w` instead would incorrectly leave city 2 disabled and return `100`.

The fourth edge case is that multiple intermediate cities may be needed. In `case5`, the route from city 1 to city 4 can use both city 2 and city 3, giving `8 + 7 + 6 = 21` when all cities are available. For the query from city 2 to city 4, the best route is `2 -> 3 -> 4`, costing `7 + 6 = 13`. The sequential Floyd-Warshall phases discover these paths because each phase permits the newly activated city to be combined with paths already formed through earlier cities.

The final subtlety is query ordering. Queries are sorted by threshold internally, so the matrix evolves in the correct monotonic order. Their original indices are retained, and answers are written back into those positions. Without that index, the computed values would be correct but could appear in the wrong order in the output.
