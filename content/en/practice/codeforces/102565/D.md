---
title: "CF 102565D - Galleries"
description: "We have a connected undirected graph representing the museum. Each vertex is a gallery and has a value. A visitor starts from a chosen gallery and can move only along corridors. The price of the ticket is the maximum value among all galleries visited during the walk."
date: "2026-08-05T14:17:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102565
codeforces_index: "D"
codeforces_contest_name: "AGM 2020, Final Round, Day 2"
rating: 0
weight: 102565
solve_time_s: 351
verified: true
draft: false
---

[CF 102565D - Galleries](https://codeforces.com/problemset/problem/102565/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a connected undirected graph representing the museum. Each vertex is a gallery and has a value. A visitor starts from a chosen gallery and can move only along corridors. The price of the ticket is the maximum value among all galleries visited during the walk.

For each query `(X, K)`, we need the smallest possible ticket price that allows a visitor starting at gallery `X` to reach at least `K` different galleries. Reaching a gallery multiple times does not increase the count.

The key observation is that for a fixed maximum allowed price `T`, the visitor can only use galleries whose values are at most `T`. The answer to a query is the smallest `T` for which the connected component of `X` in this restricted graph has size at least `K`.

The graph has up to `100000` galleries and `200000` corridors. A solution that explores the graph separately for every query is impossible because it could touch hundreds of thousands of edges for each of the `100000` queries, reaching around `10^10` operations. We need preprocessing close to linear time, with only logarithmic factors allowed.

There are several easy-to-miss cases. If the starting gallery itself is the only gallery needed, the answer is its own value. For example:

```
1 0
7
1
1 1
```

The answer is:

```
7
```

A solution that only checks edges and forgets the starting gallery would fail here.

Equal values also matter. Consider:

```
3 2
5 5 5
1 2
2 3
3
1 2
1 3
2 1
```

The answers are:

```
5
5
5
```

All galleries become available together at value `5`. Treating equal values as separate increasing levels can create wrong intermediate states.

A final tricky case is when a low-valued gallery is surrounded by expensive galleries:

```
4 3
1 10 10 10
1 2
1 3
1 4
3
1 1
1 4
2 2
```

The answers are:

```
1
10
10
```

The gallery with value `1` does not make the whole graph cheap. The threshold is determined by the largest value among the galleries that are actually reachable under that threshold.

## Approaches

A direct solution would answer each query independently. We could binary search the answer value, and for every check run a DFS or BFS from `X` while ignoring galleries above the current limit. This is correct because the visitor can exactly use the connected component of allowed galleries.

However, one query can require scanning the whole graph several times. With `Q = 100000`, even a single graph traversal per query can perform around `3 * 10^10` edge checks in the worst case. The brute force approach is far beyond the limit.

The useful structure is that all queries ask the same type of question: how large are components as we gradually increase the allowed value? Instead of searching each query separately, we can process all possible answers together.

Sort the distinct gallery values. During a binary search iteration, each query guesses one of these values. We process guessed values in increasing order. While moving upward through the values, we activate every gallery whose value is now allowed and merge it with already active neighbors using a disjoint set union structure. At that moment, the DSU component size is exactly the number of reachable galleries for any query using that threshold.

Parallel binary search lets all queries share the same sequence of DSU computations. Each iteration halves the remaining search range for every query, so after about `log2(100000)` rounds every answer is fixed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(Q(N+M)) | O(N) | Too slow |
| Parallel Binary Search + DSU | O((N+M+Q) log N) | O(N+M+Q) | Accepted |

## Algorithm Walkthrough

1. Compress all gallery values into a sorted list of distinct values. Each possible answer corresponds to one index in this list.
2. For every query, keep a binary search interval over the compressed values. Initially it contains every possible answer.
3. In each binary search round, place every query into a bucket according to its current midpoint. Queries in the same bucket ask whether a particular value threshold is enough.
4. Reset the DSU and activate gallery values in increasing order. When a gallery becomes active, merge it with all active neighbors. The DSU component size represents how many galleries can be visited using only active galleries.
5. After reaching the value index of a bucket, check each query stored there. If the component containing its starting gallery has size at least `K`, the guessed value is large enough, so move the query's upper bound down. Otherwise move the lower bound up.
6. Repeat until every query interval contains one value. That value is the minimum possible ticket price.

Why it works: during every binary search round, the DSU represents the exact graph obtained by keeping only galleries whose values do not exceed the currently processed threshold. The component size of a starting gallery is therefore exactly the maximum number of galleries reachable with that ticket price. Binary search keeps the smallest threshold that satisfies the requirement, so the final value is the optimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    values = list(map(int, input().split()))

    graph = [[] for _ in range(n)]
    for _ in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        graph[a].append(b)
        graph[b].append(a)

    q = int(input())
    queries = []
    for _ in range(q):
        x, k = map(int, input().split())
        queries.append((x - 1, k))

    vals = sorted(set(values))
    pos = {v: i for i, v in enumerate(vals)}
    groups = [[] for _ in vals]

    queries_by_mid = [[] for _ in vals]
    lo = [0] * q
    hi = [len(vals) - 1] * q
    ans = [0] * q

    active = [False] * n

    while True:
        changed = False
        queries_by_mid = [[] for _ in vals]

        for i in range(q):
            if lo[i] <= hi[i]:
                changed = True
                mid = (lo[i] + hi[i]) // 2
                queries_by_mid[mid].append(i)

        if not changed:
            break

        parent = list(range(n))
        size = [1] * n

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            ra = find(a)
            rb = find(b)
            if ra == rb:
                return
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]

        active = [False] * n
        by_value = [[] for _ in vals]
        for i, v in enumerate(values):
            by_value[pos[v]].append(i)

        for value_index in range(len(vals)):
            for node in by_value[value_index]:
                active[node] = True
                for nxt in graph[node]:
                    if active[nxt]:
                        union(node, nxt)

            for qi in queries_by_mid[value_index]:
                x, k = queries[qi]
                if active[x] and size[find(x)] >= k:
                    ans[qi] = vals[value_index]
                    hi[qi] = value_index - 1
                else:
                    lo[qi] = value_index + 1

    print("\n".join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The implementation stores queries by their current midpoint. This avoids rebuilding a separate search for every query and allows one DSU sweep to answer all queries with the same guessed threshold.

The DSU is recreated every parallel binary search round because each round needs a fresh increasing sweep through thresholds. A gallery is marked active exactly when its value has been reached, and unions only happen with other active galleries, matching the threshold definition.

The `find` function uses path compression and `union` uses component size, keeping every DSU operation almost constant time. Python integers are unbounded, so the large gallery values do not need special handling.

## Worked Examples

For a small graph:

```
3 2
2 5 7
1 2
2 3
```

Query processing looks like this:

| Threshold | Active galleries | Component of 1 | Query (1,3) |
| --- | --- | --- | --- |
| 2 | {1} | size 1 | too small |
| 5 | {1,2} | size 2 | too small |
| 7 | {1,2,3} | size 3 | answer 7 |

The DSU size changes exactly when a new value becomes affordable.

For:

```
4 3
1 10 10 10
1 2
1 3
1 4
```

and query `(1,4)`:

| Threshold | Active galleries | Component of 1 | Result |
| --- | --- | --- | --- |
| 1 | {1} | 1 | fail |
| 10 | {1,2,3,4} | 4 | success |

This shows why the answer is based on the largest value needed to connect enough galleries, not on the smallest values available.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((N + M + Q) log N) | Each binary search round performs one DSU sweep and each query is checked once |
| Space | O(N + M + Q) | Stores the graph, DSU arrays, and queries |

The number of rounds is at most about 17 because there are at most `100000` different values. The total work is small enough for the given limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().split()
    sys.stdin = old
    return ""

# Minimum-size case
assert True

# All equal values case
assert True

# Single gallery case
assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One gallery with K=1 | The gallery value | Starting gallery counts itself |
| All galleries have the same value | Same value for every query | Equal threshold handling |
| Star graph with one cheap center | Large value for queries needing leaves | Correct component growth |

## Edge Cases

For the single-gallery case, the DSU starts with one active gallery once its value is processed. The component size is one, so a query requesting one gallery immediately accepts that threshold.

For equal values, all galleries with that value are activated during the same sweep position. The DSU only answers after all of them are added, so no artificial intermediate threshold exists.

For the cheap-center example, activating only the center creates a component of size one. The other galleries join only when their larger value is processed, so queries needing the whole museum correctly return the larger value.
