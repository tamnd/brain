---
title: "CF 183C - Cyclic Coloring"
description: "We have a directed graph where every edge enforces a strict relationship between the colors of its endpoints. If a vertex has color c, then every outgoing neighbor must have color c + 1, wrapping around modulo k."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar"]
categories: ["algorithms"]
codeforces_contest: 183
codeforces_index: "C"
codeforces_contest_name: "Croc Champ 2012 - Final"
rating: 2200
weight: 183
solve_time_s: 212
verified: true
draft: false
---

[CF 183C - Cyclic Coloring](https://codeforces.com/problemset/problem/183/C)

**Rating:** 2200  
**Tags:** dfs and similar  
**Solve time:** 3m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a directed graph where every edge enforces a strict relationship between the colors of its endpoints. If a vertex has color `c`, then every outgoing neighbor must have color `c + 1`, wrapping around modulo `k`.

Another way to write the condition is:

$color(v) \equiv color(u)+1 \pmod{k}$

Every directed edge increases the color by exactly one step in a cyclic numbering system.

The task is to find the largest possible `k` for which such an assignment exists.

The graph may contain self-loops and multiple edges. Self-loops are especially restrictive because an edge from a vertex to itself requires:

$color(u) \equiv color(u)+1 \pmod{k}$

which means `k = 1`.

The constraints are large enough that we need an almost linear solution. With up to `10^5` vertices and edges, any algorithm that tries all `k` values and validates them independently would become too slow. Quadratic graph traversals are ruled out immediately. We should expect something around `O(n + m)` or `O((n + m) log n)`.

The tricky part is understanding what the coloring constraints really imply globally.

Suppose we walk along a directed path of length `d`. Every edge advances the color by one, so after traversing the path, the color difference between endpoints is forced to be `d mod k`.

Now consider a directed cycle of length `L`. Starting from a vertex and returning to it means:

$L \equiv 0 \pmod{k}$

So every directed cycle length must be divisible by `k`.

That observation completely changes the problem. Instead of thinking about colors directly, we only need to understand cycle lengths.

Several edge cases are easy to mishandle.

Consider a self-loop:

```
1 1
1 1
```

The only valid answer is:

```
1
```

A careless implementation that only looks at ordinary cycles might miss that a cycle of length `1` forces `k = 1`.

Another dangerous case is a disconnected graph:

```
4 2
1 2
3 4
```

There are no directed cycles at all. In a DAG, we can use arbitrarily large `k`, because no contradiction ever appears. Since the problem requires `k ≤ n`, the correct answer is `n = 4`.

An implementation that only computes gcds over existing cycles might accidentally return `0`.

A more subtle example is:

```
3 3
1 2
2 3
3 1
```

This graph has a cycle of length `3`, so the answer is `3`.

But if we add another edge:

```
3 4
1 2
2 3
3 1
1 3
```

we create a cycle of length `2` as well:

`1 -> 3 -> 1`

Now both `2` and `3` must be divisible by `k`, so only:

```
1
```

works.

A solution that only examines one DFS cycle at a time could incorrectly return `3`.

## Approaches

The brute-force idea is straightforward. Try every possible `k` from `n` down to `1`, and check whether a valid coloring exists.

For a fixed `k`, we can assign colors with DFS or BFS. Every edge enforces:

```
color[v] = (color[u] + 1) mod k
```

If we ever derive two different colors for the same vertex, that `k` is invalid.

This verification takes `O(n + m)` time. Doing it for every `k` gives:

```
O(n(n + m))
```

With `n = 10^5`, this becomes far too large.

The key observation is that edge constraints accumulate along paths. A path of length `d` forces a color difference of `d mod k`. Whenever two different paths connect the same pair of vertices, their lengths must agree modulo `k`.

Suppose DFS assigns each vertex a depth. For every edge `u -> v`, we know:

```
depth[v] = depth[u] + 1
```

along tree edges.

If we encounter a non-tree edge, then:

```
depth[u] + 1 - depth[v]
```

represents the length difference between two ways of reaching `v`.

That difference must be divisible by `k`.

Collecting these constraints across the whole graph gives:

$k \mid (depth[u]+1-depth[v])$

for every edge.

So the maximum valid `k` is simply the gcd of all such values.

Why does this work?

Every directed cycle contributes one of these differences, and the gcd captures exactly the common divisor shared by all cycle lengths.

If the graph has no directed cycles, then all differences are zero, meaning there is no restriction at all. In that case the answer is `n`.

The final algorithm performs one DFS over the graph and computes the gcd incrementally.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n(n + m)) | O(n) | Too slow |
| Optimal | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Build the adjacency list of the directed graph.
2. Maintain a depth array initialized to `-1`. A value of `-1` means the vertex has not been visited yet.
3. Start DFS from every unvisited vertex. Set the starting depth to `0`.
4. During DFS, for every edge `u -> v`:

If `v` is unvisited, assign:

```
depth[v] = depth[u] + 1
```

and continue DFS.
5. If `v` was already visited, compute:

```
diff = depth[u] + 1 - depth[v]
```

This value represents a cycle constraint. Any valid `k` must divide this number.
6. Maintain the gcd of all nonzero `diff` values encountered during DFS.
7. After processing the whole graph:

If the gcd is `0`, the graph contains no cycle constraints, so any `k` works. The maximum allowed answer is `n`.
8. Otherwise, output the absolute value of the gcd.

### Why it works

DFS depths encode path lengths from the DFS root.

For every edge `u -> v`, the expression:

```
depth[u] + 1 - depth[v]
```

measures the difference between two path lengths leading to `v`.

A valid coloring requires all path lengths between the same vertices to agree modulo `k`. That means every such difference must be divisible by `k`.

The gcd of all differences is exactly the largest number dividing every cycle length constraint simultaneously. Any larger number would violate at least one cycle.

If all differences are zero, then the graph behaves like a DAG with respect to these constraints, and no restriction on `k` exists.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

def solve():
    sys.setrecursionlimit(1 << 25)

    n, m = map(int, input().split())

    graph = [[] for _ in range(n)]

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append(v)

    depth = [-1] * n
    g = 0

    def dfs(u):
        nonlocal g

        for v in graph[u]:
            if depth[v] == -1:
                depth[v] = depth[u] + 1
                dfs(v)
            else:
                diff = depth[u] + 1 - depth[v]
                g = gcd(g, abs(diff))

    for i in range(n):
        if depth[i] == -1:
            depth[i] = 0
            dfs(i)

    if g == 0:
        print(n)
    else:
        print(g)

solve()
```

The adjacency list stores all outgoing edges. Multiple edges and self-loops work naturally without any special handling.

The `depth` array serves two purposes. It marks visited vertices and records the DFS depth needed to derive cycle constraints.

When DFS follows a tree edge, the child depth becomes one greater than the parent depth. This matches the fact that every directed edge advances the color by one.

For an already visited vertex, the computed `diff` captures the discrepancy between two paths. Taking gcds incrementally is enough because gcd is associative:

```
gcd(a, b, c) = gcd(gcd(a, b), c)
```

The absolute value is important. Depending on traversal order, `diff` may become negative, but divisibility constraints depend only on magnitude.

The special case `g == 0` occurs when every difference is zero. That means no nontrivial cycle constraints were discovered. In this situation, the graph allows any `k`, so the largest permitted value is `n`.

## Worked Examples

### Sample 1

Input:

```
4 4
1 2
2 1
3 4
4 3
```

DFS traversal:

| Edge | depth[u] | depth[v] before | diff | gcd |
| --- | --- | --- | --- | --- |
| 1 → 2 | 0 | -1 | - | 0 |
| 2 → 1 | 1 | 0 | 2 | 2 |
| 3 → 4 | 0 | -1 | - | 2 |
| 4 → 3 | 1 | 0 | 2 | 2 |

Final gcd is `2`, so the answer is:

```
2
```

This trace shows that both connected components impose the same cycle length restriction. Every cycle length is divisible by `2`.

### Example 2

Input:

```
3 3
1 2
2 3
3 1
```

DFS traversal:

| Edge | depth[u] | depth[v] before | diff | gcd |
| --- | --- | --- | --- | --- |
| 1 → 2 | 0 | -1 | - | 0 |
| 2 → 3 | 1 | -1 | - | 0 |
| 3 → 1 | 2 | 0 | 3 | 3 |

Final gcd is `3`.

So the answer is:

```
3
```

The cycle has length `3`, meaning colors must repeat every three steps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each vertex and edge is processed once |
| Space | O(n + m) | Adjacency list and DFS state |

The graph size reaches `10^5`, so linear complexity is exactly what we need. The solution easily fits within both the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string

import sys
import io
from math import gcd

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    sys.setrecursionlimit(1 << 25)

    n, m = map(int, input().split())

    graph = [[] for _ in range(n)]

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append(v)

    depth = [-1] * n
    g = 0

    def dfs(u):
        nonlocal g

        for v in graph[u]:
            if depth[v] == -1:
                depth[v] = depth[u] + 1
                dfs(v)
            else:
                diff = depth[u] + 1 - depth[v]
                g = gcd(g, abs(diff))

    for i in range(n):
        if depth[i] == -1:
            depth[i] = 0
            dfs(i)

    return str(n if g == 0 else g)

# provided sample
assert run(
"""4 4
1 2
2 1
3 4
4 3
"""
) == "2", "sample 1"

# single self-loop
assert run(
"""1 1
1 1
"""
) == "1", "self-loop forces k = 1"

# DAG, no cycles
assert run(
"""4 2
1 2
3 4
"""
) == "4", "acyclic graph allows any k up to n"

# cycle of length 3
assert run(
"""3 3
1 2
2 3
3 1
"""
) == "3", "simple 3-cycle"

# mixed cycle lengths, gcd becomes 1
assert run(
"""3 4
1 2
2 3
3 1
1 3
"""
) == "1", "cycle lengths 2 and 3"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single self-loop | 1 | Self-loops force `k = 1` |
| DAG with disconnected components | 4 | No cycle constraints means answer is `n` |
| Simple 3-cycle | 3 | Single cycle length determines answer |
| Mixed 2-cycle and 3-cycle constraints | 1 | GCD logic across multiple cycles |

## Edge Cases

A self-loop immediately forces the answer to `1`.

Input:

```
1 1
1 1
```

DFS starts at vertex `1` with depth `0`.

For edge `1 -> 1`:

```
diff = 0 + 1 - 0 = 1
```

The gcd becomes `1`, so the final answer is `1`.

This works because a self-loop requires the color to equal its own next color.

Now consider a graph with no cycles:

```
4 2
1 2
3 4
```

DFS assigns increasing depths, but every edge goes to an unvisited node. No non-tree edge ever appears, so the gcd remains `0`.

The algorithm outputs `n = 4`.

This correctly reflects that acyclic graphs impose no modular restriction.

Finally, consider conflicting cycle lengths:

```
3 4
1 2
2 3
3 1
1 3
```

The graph contains both a 3-cycle and a 2-cycle.

DFS produces constraints with gcd:

```
gcd(3, 2) = 1
```

So only `k = 1` works.

The algorithm correctly combines all cycle information instead of relying on a single detected cycle.
