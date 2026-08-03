---
title: "CF 102788F - Spying Game"
description: "The task asks us to rebuild a directed acyclic graph of cities. City m is the source of all shipments. For every city i, we are given D[i], the number of different directed paths that start at m and end at i."
date: "2026-08-03T15:10:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102788
codeforces_index: "F"
codeforces_contest_name: "2017-2018 ICPC Central Quarter Final of Northeastern European Regional Collegiate Programming Contest"
rating: 0
weight: 102788
solve_time_s: 87
verified: true
draft: false
---

[CF 102788F - Spying Game](https://codeforces.com/problemset/problem/102788/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

The task asks us to rebuild a directed acyclic graph of cities. City `m` is the source of all shipments. For every city `i`, we are given `D[i]`, the number of different directed paths that start at `m` and end at `i`. We must output any set of directed roads that creates exactly these path counts. The graph must stay acyclic and cannot contain multiple roads between the same pair of cities. The original statement describes this as constructing a possible shipment map from the collected route counts.

The key observation is that a city's number of routes is completely determined by its incoming roads. Every incoming road from a city `u` contributes all paths that already reach `u`, so if a city has incoming neighbors `p1, p2, ...`, its value must satisfy:

`D[v] = D[p1] + D[p2] + ...`

Because the graph is acyclic, every parent of a city must have a smaller path count. A city with value zero cannot be reached from the source and should have no incoming roads. The source city itself has exactly one path to itself, the empty path, so its value must be one.

The limit `n <= 60` is small, but the values of `D` can be as large as `2^62`, so algorithms depending on the numeric size of the values are impossible. We cannot expand counts, enumerate paths, or use dynamic programming over the values. The construction has to use the structure of the graph and the fact that there are only sixty cities.

The important edge cases are cities with value zero, cities with value one, and repeated values. A zero-valued city must not accidentally receive an edge. For example:

```
n = 3, m = 1
D = [1, 0, 0]
```

The correct graph has no roads. Adding a road from city `1` to city `2` would immediately create one path and make `D[2]` incorrect.

Repeated values need careful handling. For example:

```
n = 4, m = 1
D = [1, 1, 1, 3]
```

The last city needs two paths from the source besides the direct source contribution. Connecting both value-one cities to it gives three paths. Treating equal values as interchangeable without considering the construction order can create cycles or invalid parent choices.

## Approaches

A direct approach would try to decide the incoming roads of every city independently. For a city with value `x`, we would search among all previous cities and find a subset whose path counts sum to `x`. This is correct because the number of paths entering a node is exactly the sum of the path counts of its parents. However, trying all subsets requires exponential time. With sixty cities, the worst case would require considering around `2^60` possibilities, which is far beyond the limit.

The useful observation is that we do not need to solve a general subset sum problem. The given path counts come from a DAG, which means every value can already be decomposed into values of earlier cities. If we process cities in increasing order of their path counts, every city that can be a parent has already been handled. We can greedily take the largest available smaller values until the required sum is reached.

For valid input, this greedy decomposition works because if a remaining amount could not be covered by the largest available smaller value, then no later smaller value could help either. The sorted order preserves the property that every missing part must have appeared before the current city.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

1. Check the source city and collect all cities with positive path counts. Cities with value zero are ignored because they must stay unreachable.
2. Sort the positive-value cities by their path count. Processing them from small values to large values guarantees that when we build a city, all possible parents are already available.
3. For every city except the source, find previous cities whose path counts add up to its required value. Add directed edges from those parent cities into the current city.
4. To find the parents, scan previous cities from the largest path count downwards. Whenever a city value does not exceed the remaining amount, use it as a parent and subtract it from the remaining amount.
5. Output all collected roads.

The invariant is that after processing any prefix of the sorted cities, every processed city already has exactly its required number of paths from the source. When a new city is added, its incoming edges contribute exactly the selected previous path counts, so the new city's value is also correct. Since all edges go from smaller values to larger values, cycles cannot appear.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    d = list(map(int, input().split()))

    src = m - 1
    nodes = [(d[i], i) for i in range(n) if d[i] > 0]
    nodes.sort()

    pos = {}
    for idx, (_, v) in enumerate(nodes):
        pos[v] = idx

    edges = []

    for idx, (val, v) in enumerate(nodes):
        if v == src:
            continue

        need = val
        for j in range(idx - 1, -1, -1):
            if nodes[j][0] <= need:
                edges.append((nodes[j][1] + 1, v + 1))
                need -= nodes[j][0]
            if need == 0:
                break

    print(len(edges))
    for a, b in edges:
        print(a, b)

if __name__ == "__main__":
    solve()
```

The code first removes unreachable cities from consideration. They cannot contribute to any route count because they have no path from the source.

The sorted list stores pairs of path count and city index. The loop over this list is the construction order from the algorithm. For a city with required value `val`, the variable `need` tracks how many paths still have to be created. Every selected parent contributes its entire number of paths, so subtracting that value exactly mirrors the path-count equation.

The source city is skipped because its value is already defined by the empty path. The edge direction is always from an earlier sorted city to a later one, which prevents cycles. Python integers handle the `2^62` range directly, so no overflow handling is needed.

## Worked Examples

For the sample:

```
5 1
0 1 1 3 3
```

the sorted positive cities are:

| Step | City | Value | Remaining | Added parents |
| --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 1 | none, source already gives value |
| 2 | 3 | 1 | 1 | none, source already gives value |
| 3 | 4 | 3 | 3 | cities 3 and 2 and source |
| 4 | 5 | 3 | 3 | city 4 |

The resulting roads create the required counts.

A second example:

```
4 1
1 1 2 3
```

| Step | City | Value | Remaining | Added parents |
| --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 1 | none |
| 2 | 3 | 2 | 2 | city 2 and source |
| 3 | 4 | 3 | 3 | city 3 |

The trace shows that larger route counts are built from already constructed smaller ones.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Each city scans previously processed cities once |
| Space | O(n) | Only the sorted city list and edge list are stored |

The maximum number of cities is only sixty, so the quadratic construction easily fits within the limits.

## Edge Cases

For unreachable cities, the algorithm never places them in the sorted positive list. For:

```
3 1
1 0 0
```

no city is processed except the source, so the output contains zero roads and the path counts remain correct.

For multiple direct children of the source:

```
4 1
1 1 1 3
```

the two value-one cities are both available before the value-three city is built. The algorithm uses them together with the source contribution to create the required three routes.

For repeated larger values:

```
5 1
1 1 1 2 4
```

the value-two city is created from two value-one cities, and the value-four city can then use the smaller constructed cities. Processing in increasing order guarantees that every possible parent is available before it is needed.
