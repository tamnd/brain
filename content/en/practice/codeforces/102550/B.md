---
title: "CF 102550B - \u0410\u0442\u0430\u043a\u0443\u044e\u0449\u0438\u0435 \u043f\u0430\u0440\u044b"
description: "The problem describes a collection of items where each item has a price, and some pairs of items are compatible. We need to find the cheapest set of three items such that every pair among those three items is compatible."
date: "2026-08-06T20:36:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102550
codeforces_index: "B"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2018-2019, \u041f\u0435\u0440\u0432\u0430\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102550
solve_time_s: 63
verified: true
draft: false
---

[CF 102550B - \u0410\u0442\u0430\u043a\u0443\u044e\u0449\u0438\u0435 \u043f\u0430\u0440\u044b](https://codeforces.com/problemset/problem/102550/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a collection of items where each item has a price, and some pairs of items are compatible. We need to find the cheapest set of three items such that every pair among those three items is compatible. In graph terms, every item is a vertex, every compatible pair is an edge, and we need the minimum total weight of a triangle. If no triangle exists, the answer is `-1`.

The input gives the number of items and the number of compatible pairs, followed by the price of every item and the list of compatible pairs. The output is the minimum possible sum of prices among all triples of mutually connected items.

The constraints are designed around the fact that checking every triple directly is usually too expensive. If there are `n` items, the number of possible triples is `n * (n - 1) * (n - 2) / 6`, which grows cubically. Even for a few thousand items, this becomes too large, so we need to avoid enumerating all groups of three.

The main edge cases come from confusing a path with a triangle or from forgetting that all three pairs must exist. For example:

```
3 2
2 3 4
1 2
2 3
```

The answer is `-1`. Items `1, 2, 3` are connected in a chain, but items `1` and `3` are not compatible. A careless solution that only checks whether one item has two neighbors would incorrectly accept this case.

Another case is when a valid triangle exists but there are other cheaper-looking pairs that do not form a triangle.

```
4 4
10 1 2 100
1 2
2 3
3 1
1 4
```

The answer is `13`, using items `1, 2, 3`. The fourth item has cheap connections to some vertices but cannot replace a triangle member.

A final boundary case is when the graph has no cycles of length three at all.

```
4 3
5 5 5 5
1 2
2 3
3 4
```

The answer is `-1`. A chain can contain many edges but no attacking pair of pairs that closes into a triangle.

## Approaches

A direct solution would examine every possible triple of items. For each triple `(i, j, k)`, we check whether the three required compatibility edges exist and, if they do, update the minimum sum of their prices. This is correct because every possible answer is considered. However, the number of triples is `O(n^3)`, and each triple requires constant-time edge checks. For large graphs this means billions of operations, which is not feasible.

The useful observation is that a triangle must contain three vertices where each pair is connected. Instead of generating all triples, we can iterate through the existing edges. When we look at an edge `(u, v)`, any triangle containing this edge must use a common neighbor of `u` and `v`. The intersection of their adjacency lists gives exactly those possible third vertices.

The graph can have many edges, so we need to make these intersection checks efficient. We store adjacency sets, allowing constant average-time membership checks. For every edge, we iterate through the smaller adjacency set and test whether each candidate is also connected to the other endpoint. Every discovered common neighbor forms a triangle, and we update the answer.

The brute force works because every possible triangle is tested, but fails because it creates too many unnecessary triples. The adjacency intersection approach only examines triples that are close to being triangles, using the graph structure to avoid impossible combinations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(n²) | Too slow |
| Adjacency Intersection | O(m * sqrt(m)) average for sparse graphs | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Store the price of every item and build an adjacency set for every vertex. Each set contains the items directly connected to that vertex, so we can quickly check whether a pair is compatible.
2. Traverse every edge `(u, v)` in the graph. A triangle containing this edge must have a third vertex connected to both `u` and `v`.
3. Iterate through the smaller of the two adjacency sets of `u` and `v`. For every candidate vertex `x`, check whether `x` also belongs to the other endpoint's adjacency set.
4. When such a vertex exists, the three vertices form a valid triangle. Compute `price[u] + price[v] + price[x]` and minimize the answer.
5. After all edges are processed, print the minimum found value. If no triangle was discovered, print `-1`.

The reason for iterating through the smaller adjacency list is that every candidate from that side is a possible third vertex. Checking the smaller side reduces the total number of unnecessary membership tests.

Why it works:

Every valid solution is a triangle, and every triangle contains three edges. During the traversal, the algorithm processes at least one of those edges. When it processes that edge, the third vertex of the triangle appears in the adjacency set intersection, so the triangle is found. Since every found triangle is evaluated and the minimum sum is kept, the final answer is exactly the cheapest possible triangle.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    price = list(map(int, input().split()))

    adj = [set() for _ in range(n)]
    edges = []

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        adj[u].add(v)
        adj[v].add(u)
        edges.append((u, v))

    ans = float("inf")

    for u, v in edges:
        if len(adj[u]) > len(adj[v]):
            u, v = v, u

        for x in adj[u]:
            if x in adj[v]:
                ans = min(ans, price[u] + price[v] + price[x])

    print(-1 if ans == float("inf") else ans)

if __name__ == "__main__":
    solve()
```

The adjacency sets are used because the only operation we need repeatedly is asking whether two items are connected. A list would require scanning all neighbors, while a set gives average constant-time lookup.

The edge list is stored separately because iterating through adjacency sets alone would process every edge twice and would require extra bookkeeping. The swap before the inner loop guarantees that the smaller neighbor set is always scanned.

The algorithm does not modify the graph while processing it, so there are no ordering issues. The price sum is stored in Python integers, which automatically handle values larger than 32-bit limits.

## Worked Examples

For the input:

```
3 3
1 2 3
1 2
2 3
3 1
```

the trace is:

| Edge | Smaller adjacency checked | Common neighbor | Current answer |
| --- | --- | --- | --- |
| 1-2 | {2,3} | 3 | 6 |
| 2-3 | {1,3} | 1 | 6 |
| 3-1 | {1,2} | 2 | 6 |

The graph is a complete triangle. Every edge finds the remaining vertex, and the minimum possible sum is all three prices.

For the input:

```
4 4
1 1 1 1
1 2
2 3
3 4
4 1
```

the trace is:

| Edge | Smaller adjacency checked | Common neighbor | Current answer |
| --- | --- | --- | --- |
| 1-2 | {2,4} | none | infinity |
| 2-3 | {1,3} | none | infinity |
| 3-4 | {2,4} | none | infinity |
| 4-1 | {3,1} | none | infinity |

The cycle has length four, not three. No pair of adjacent vertices shares a common neighbor, so the algorithm correctly outputs `-1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m * sqrt(m)) average | Each edge checks the smaller side of an adjacency relationship, which is efficient for the intended graph limits. |
| Space | O(n + m) | The adjacency sets and edge list store the graph. |

The solution avoids the cubic number of possible triples and only explores existing graph connections. This makes it suitable for large sparse graphs where checking every possible group of three would be impossible.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    
    data = sys.stdin.readline
    n, m = map(int, data().split())
    price = list(map(int, data().split()))

    adj = [set() for _ in range(n)]
    edges = []

    for _ in range(m):
        u, v = map(int, data().split())
        u -= 1
        v -= 1
        adj[u].add(v)
        adj[v].add(u)
        edges.append((u, v))

    ans = float("inf")

    for u, v in edges:
        if len(adj[u]) > len(adj[v]):
            u, v = v, u
        for x in adj[u]:
            if x in adj[v]:
                ans = min(ans, price[u] + price[v] + price[x])

    sys.stdin = old_stdin
    return str(-1 if ans == float("inf") else ans)

assert run("""3 3
1 2 3
1 2
2 3
3 1
""") == "6"

assert run("""3 2
2 3 4
1 2
2 3
""") == "-1"

assert run("""4 4
1 1 1 1
1 2
2 3
3 4
4 1
""") == "-1"

assert run("""4 4
10 1 2 100
1 2
2 3
3 1
1 4
""") == "13"

assert run("""3 3
1000000 1000000 1000000
1 2
2 3
3 1
""") == "3000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Three fully connected items | 6 | Basic triangle detection |
| Three items in a chain | -1 | Prevents mistaking a path for a triangle |
| Four-cycle graph | -1 | Checks that longer cycles are ignored |
| Triangle with an extra distracting vertex | 13 | Checks minimum triangle selection |
| Maximum price values | 3000000 | Checks large integer sums |

## Edge Cases

For the chain case:

```
3 2
2 3 4
1 2
2 3
```

the algorithm examines both edges. For edge `(1,2)`, the neighbors of vertex `1` contain only `2`, and vertex `2` has neighbors `1` and `3`. There is no common third vertex. The same happens for `(2,3)`, so the answer remains unset and `-1` is printed.

For the graph containing a cheaper-looking non-triangle connection:

```
4 4
10 1 2 100
1 2
2 3
3 1
1 4
```

the edge `(1,2)` finds vertex `3` as a common neighbor and creates the triangle with sum `13`. The edge `(1,4)` has no common neighbor, so it cannot create an invalid lower answer.

For a graph with no triangles:

```
4 3
5 5 5 5
1 2
2 3
3 4
```

every edge belongs only to a path. Since no edge has endpoints with a shared neighbor, the algorithm never updates the answer and returns `-1`.
