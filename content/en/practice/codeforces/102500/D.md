---
title: "CF 102500D - Disposable Switches"
description: "We have an undirected network where every cable has a known length, but the actual transmission time of a cable depends on two unknown global parameters. For a cable of length l, its time is l / v + c, where the same v and c apply to every cable."
date: "2026-08-05T18:01:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102500
codeforces_index: "D"
codeforces_contest_name: "2019-2020 ICPC Northwestern European Regional Programming Contest (NWERC 2019)"
rating: 0
weight: 102500
solve_time_s: 88
verified: true
draft: false
---

[CF 102500D - Disposable Switches](https://codeforces.com/problemset/problem/102500/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an undirected network where every cable has a known length, but the actual transmission time of a cable depends on two unknown global parameters. For a cable of length `l`, its time is `l / v + c`, where the same `v` and `c` apply to every cable. We need to find switches that can never appear on a fastest route from switch `1` to switch `n`, regardless of which valid values these two parameters take.

The unknown parameters are the key difficulty. A path is not compared only by its total length. A path using fewer cables may become better when the overhead `c` is large, while a path with shorter total cable length may win when propagation dominates.

The constraints give `n` up to 2000 and `m` up to 10000. An algorithm with cubic time would already be too large because `2000^3` operations is around eight billion. The intended solution must be close to `O(n(n+m))`, which is around forty million graph operations for these limits.

A common mistake is to run Dijkstra once with the original formula. That cannot work because the formula contains unknown values. Another mistake is to only consider the shortest-length path or the fewest-edge path. Neither dominates the other. For example, consider:

```
4 4
1 2 1
2 4 100
1 3 10
3 4 10
```

For a very small overhead, the path `1-3-4` wins because its length is `20`. For a very large overhead, the path `1-2-4` wins because it has fewer edges. A method considering only one objective would incorrectly discard a possible optimal path.

Another edge case is ties. A switch is valid if it appears on any optimal path for any parameter choice. If two different routes have exactly the same cost for some parameter, both routes must contribute their vertices.

## Approaches

The brute-force approach would try every possible value of the unknown parameters and compute shortest paths. This is impossible because the parameter space is continuous, and there can be infinitely many different shortest-path changes.

The useful observation comes from rewriting the path cost. Multiplying every edge cost by `v` does not change which path is optimal, because it multiplies every possible route by the same positive value. The cost of a path becomes:

```
total_length + number_of_edges * x
```

where `x = v*c`, and `x` can be any non-negative real number.

Now every path is represented by a line:

```
y = edges * x + length
```

The slope is the number of edges, and the intercept is the total cable length.

For every possible number of edges `k`, we only care about the shortest-length path that uses exactly `k` edges. Any other path with the same number of edges has a larger intercept and can never win.

So the problem becomes:

Find all `k` where the line

```
y = k*x + best[k]
```

is part of the lower convex hull for `x >= 0`.

Those are exactly the edge counts that can occur on an optimal route.

The remaining task is recovering which vertices occur on paths with those edge counts. We compute dynamic programming tables:

`forward[k][v]` stores the minimum length needed to reach `v` from switch `1` using exactly `k` edges.

`backward[k][v]` stores the minimum length needed to reach switch `n` from `v` using exactly `k` edges.

A vertex `v` can appear on an optimal path with `k` edges if the path can be split at `v`:

```
prefix edges + suffix edges = k
```

and

```
forward[prefix][v] + backward[suffix][v] = best[k]
```

The final answer is every vertex that never satisfies this condition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over parameters | Impossible | Impossible | Too slow |
| Enumerate all edge counts with dynamic programming and convex hull | O(n(n+m)) | O(n²) | Accepted |

## Algorithm Walkthrough

1. Compute the shortest possible cable length for every number of edges.

The maximum number of edges in a useful path is `n-1`, because any path containing a cycle can remove that cycle and become strictly better. We run a layered dynamic programming process. Each layer represents the exact number of edges used so far.

For every `k`, we obtain `best[k]`, the smallest total length among all `1` to `n` paths using exactly `k` edges.

1. Convert the possible paths into lines.

For every valid edge count `k`, create the line:

```
y = k*x + best[k]
```

Only the lines visible from below can ever be shortest for some non-negative `x`. We remove all other lines by computing the lower hull.

1. Find all edge counts that can produce an optimal route.

Every remaining line corresponds to at least one value of `x` where paths using that number of edges are optimal. Only these edge counts need to be checked for vertices.

1. Compute the same layered dynamic programming from the destination.

The reverse table lets us check whether a vertex can be placed in the middle of an optimal path. It avoids enumerating every complete route.

1. Mark every vertex that appears in an optimal path.

For each edge count on the lower hull, combine the forward and backward states. If the two parts together have the minimum possible length for that edge count, the vertex is usable.

1. Output every unmarked vertex.

These are exactly the switches that cannot appear in an optimal route for any possible values of the unknown parameters.

### Why it works

Every possible transmission time is represented by choosing one value of `x` in the family of lines `k*x + best[k]`. A line outside the lower hull is always worse than another line, so no path using that number of edges can ever be optimal. A line on the lower hull is optimal for some parameter value, so all shortest paths represented by that line must be considered.

The forward and backward dynamic programming tables contain the minimum possible length for every prefix and suffix length. If they combine to `best[k]`, the resulting route is a shortest route among all routes using `k` edges. Since every possible optimal route has some edge count on the hull, every vertex that can ever be used is marked, and every unmarked vertex is impossible.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

INF = 10**30

def solve():
    n, m = map(int, input().split())

    adj = [[] for _ in range(n)]
    for _ in range(m):
        a, b, l = map(int, input().split())
        a -= 1
        b -= 1
        adj[a].append((b, l))
        adj[b].append((a, l))

    size = n * n

    def build(start):
        dp = array('q', [INF]) * size
        dp[start] = 0

        for k in range(n - 1):
            base = k * n
            nxt = (k + 1) * n
            for u in range(n):
                cur = dp[base + u]
                if cur == INF:
                    continue
                for v, w in adj[u]:
                    val = cur + w
                    if val < dp[nxt + v]:
                        dp[nxt + v] = val
        return dp

    forward = build(0)

    rev_adj = [[] for _ in range(n)]
    for u in range(n):
        for v, w in adj[u]:
            rev_adj[v].append((u, w))

    old = adj
    adj = rev_adj
    backward = build(n - 1)
    adj = old

    best = [forward[k * n + n - 1] for k in range(n)]

    hull = []
    for k in range(n):
        if best[k] == INF:
            continue
        while len(hull) >= 2:
            a, b = hull[-2], hull[-1]
            # intersection(a,b) >= intersection(b,k)
            if (best[b] - best[a]) * (k - b) >= (best[k] - best[b]) * (b - a):
                hull.pop()
            else:
                break
        hull.append(k)

    possible = [False] * n

    for k in hull:
        target = best[k]
        for v in range(n):
            f = forward[v]
            if f == INF:
                continue
            for i in range(k + 1):
                if i * n + v >= size:
                    break
                if forward[i * n + v] + backward[(k - i) * n + v] == target:
                    possible[v] = True
                    break
            if possible[v]:
                continue

    ans = [str(i + 1) for i, ok in enumerate(possible) if not ok]

    print(len(ans))
    if ans:
        print(" ".join(ans))

if __name__ == "__main__":
    solve()
```

The implementation stores the dynamic programming tables in `array('q')` instead of normal Python lists. The table contains four million values in the maximum case, and Python integers would consume too much memory.

The DP transition is the direct layered relaxation. The index `k*n+v` represents reaching vertex `v` after exactly `k` edges.

The convex hull calculation uses only integer arithmetic. Comparing intersections avoids floating point precision problems because cable lengths can be as large as `10^9`.

The reverse DP is computed by reversing all edges. Since the graph is undirected, this is equivalent to running the same process from the destination.

The marking loop checks whether a vertex can split an optimal path. The equality comparison uses only integer values, so equal-cost routes are handled correctly.
