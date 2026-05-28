---
title: "CF 176E - Archaeology"
description: "We are given a weighted tree. Every node represents a village, and every edge represents a road with a length. Villages can appear and disappear over time through online queries. At any moment, only a subset of villages currently exists."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "trees"]
categories: ["algorithms"]
codeforces_contest: 176
codeforces_index: "E"
codeforces_contest_name: "Croc Champ 2012 - Round 2"
rating: 3100
weight: 176
solve_time_s: 132
verified: true
draft: false
---

[CF 176E - Archaeology](https://codeforces.com/problemset/problem/176/E)

**Rating:** 3100  
**Tags:** data structures, dfs and similar, trees  
**Solve time:** 2m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a weighted tree. Every node represents a village, and every edge represents a road with a length. Villages can appear and disappear over time through online queries.

At any moment, only a subset of villages currently exists. Among all roads in the original tree, people only use the minimum set of roads necessary to keep all existing villages connected. Since the graph is already a tree, this subset is exactly the minimal subtree containing all active villages.

For every query `"?"`, we must output the total length of all roads inside that minimal connecting subtree.

Another way to phrase the task is this: maintain a dynamic set of active vertices in a weighted tree, and repeatedly compute the total weight of the Steiner tree induced by those vertices.

The constraints are large enough that rebuilding the subtree from scratch after every update is impossible. Both the number of vertices and the number of queries reach `10^5`, which means the solution must stay near `O(log n)` per operation. Anything quadratic, or even `O(n)` per query, would time out.

A naive approach would mark all active vertices, run DFS to find the minimal connecting subtree, and sum its edge weights. If we have `10^5` queries and each query scans the whole tree, we end up with roughly `10^10` operations in the worst case.

There are several subtle cases that easily break incorrect solutions.

Suppose there is only one active village:

```
1
?
```

The answer must be `0`, because no roads are needed to connect a single vertex. A careless implementation based on pairwise distances can accidentally produce a nonzero answer.

Another tricky case appears when vertices are activated in DFS order versus arbitrary order.

```
3
1 2 5
2 3 7
5
+ 1
+ 3
?
- 1
?
```

The answers are:

```
12
0
```

After removing vertex `1`, only vertex `3` remains active, so the required subtree becomes empty again.

A more subtle failure happens if we forget the cyclic structure of the active vertices in Euler-tour order.

Consider the chain:

```
1 -2- 2 -3- 3 -4- 4
```

with active vertices `{1,3,4}`.

The minimal subtree has weight `2 + 3 + 4 = 9`.

If we only sum distances between consecutive active vertices without wrapping around, we get:

```
dist(1,3) + dist(3,4) = 5 + 4 = 9
```

and dividing by two gives `4`, which is wrong. The cyclic connection back from `4` to `1` is essential.

The core challenge is maintaining this subtree dynamically under insertions and deletions.

## Approaches

The brute-force solution follows the definition directly. For every `"?"` query, we identify all active vertices, run a DFS from one of them, and keep only edges that lie on paths connecting active nodes. The sum of those edge weights is the answer.

This works because a tree contains exactly one simple path between every pair of vertices. The minimal connected subgraph containing all active vertices is uniquely determined.

The problem is performance. If there are `k` active vertices, we may traverse almost the entire tree for every query. With `10^5` vertices and `10^5` operations, the total work becomes far too large.

The key observation is that the answer can be expressed entirely through distances between active vertices ordered by DFS entry time.

Take all active vertices and sort them by Euler-tour order. Connect them cyclically. Then:

```
answer = (sum of distances between consecutive vertices in the cycle) / 2
```

This formula is surprisingly powerful. Every edge inside the minimal subtree gets counted exactly twice in the cyclic walk.

Now the problem becomes dynamic maintenance of a cyclic distance sum.

We preprocess the tree for Lowest Common Ancestor queries so we can compute distances in `O(log n)` time.

Then we store all active vertices inside an ordered set by Euler-tour entry time. When inserting or deleting one vertex, only its two neighboring vertices in cyclic order are affected. That means the total cyclic sum changes locally.

Suppose vertex `x` is inserted between `p` and `nxt` in Euler order. Before insertion, the cycle contains edge contribution:

```
dist(p, nxt)
```

After insertion, it becomes:

```
dist(p, x) + dist(x, nxt)
```

So the total increases by:

```
dist(p, x) + dist(x, nxt) - dist(p, nxt)
```

Deletion is the exact reverse operation.

Every update touches only a constant number of distances, each computed in `O(log n)` through LCA.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| Optimal | O((n + q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Root the tree at an arbitrary vertex, usually `1`.

This lets us compute depths, Euler-tour entry times, and prefix distances from the root.
2. Run DFS preprocessing.

For every vertex, compute:

- `tin[v]`, the DFS entry time
- `depth[v]`
- `dist_root[v]`, distance from the root
- binary lifting ancestors for LCA

Euler-tour order gives us a stable cyclic ordering of vertices.
3. Implement Lowest Common Ancestor queries.

The distance between two vertices becomes:

```
dist(u,v) = dist_root[u] + dist_root[v] - 2 * dist_root[lca(u,v)]
```
4. Maintain all active vertices inside an ordered structure sorted by `tin`.

We need predecessor and successor queries in cyclic order. In Python, we can use a sorted list together with `bisect`.
5. Maintain a variable `total_cycle`.

This stores:

```
Σ dist(consecutive active vertices in cyclic order)
```
6. When inserting a vertex `x`:

1. Find its cyclic predecessor `p`.
2. Find its cyclic successor `nxt`.
3. Add:

```
dist(p,x) + dist(x,nxt) - dist(p,nxt)
```
4. Insert `x` into the ordered set.

This replaces one cycle edge with two new edges.
7. When deleting a vertex `x`:

1. Find its cyclic predecessor `p`.
2. Find its cyclic successor `nxt`.
3. Subtract:

```
dist(p,x) + dist(x,nxt) - dist(p,nxt)
```
4. Remove `x` from the ordered set.

This merges two cycle edges back into one.
8. For every `"?"` query, print:

```
total_cycle // 2
```

Every edge in the Steiner tree is traversed twice in the cyclic tour.

### Why it works

Take the active vertices ordered by Euler-tour time and connect them cyclically. Consider traversing the minimal subtree in DFS order. Every edge of the subtree is crossed exactly twice, once entering the subtree branch and once leaving it.

The cyclic sum of pairwise distances reproduces exactly this traversal length. Since each edge contributes twice, dividing by two gives the subtree weight.

Insertions and deletions only affect neighboring vertices in the cyclic order. All other pairwise connections remain unchanged, so local updates are sufficient.

## Python Solution

```python
import sys
from bisect import bisect_left, insort

input = sys.stdin.readline

LOG = 17

def solve():
    n = int(input())

    g = [[] for _ in range(n + 1)]

    for _ in range(n - 1):
        u, v, w = map(int, input().split())
        g[u].append((v, w))
        g[v].append((u, w))

    tin = [0] * (n + 1)
    depth = [0] * (n + 1)
    dist_root = [0] * (n + 1)

    up = [[0] * (n + 1) for _ in range(LOG + 1)]

    timer = 0

    sys.setrecursionlimit(1 << 25)

    def dfs(v, p):
        nonlocal timer

        timer += 1
        tin[v] = timer

        up[0][v] = p

        for i in range(1, LOG + 1):
            up[i][v] = up[i - 1][up[i - 1][v]]

        for to, w in g[v]:
            if to == p:
                continue

            depth[to] = depth[v] + 1
            dist_root[to] = dist_root[v] + w
            dfs(to, v)

    dfs(1, 1)

    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a

        diff = depth[a] - depth[b]

        for i in range(LOG + 1):
            if diff & (1 << i):
                a = up[i][a]

        if a == b:
            return a

        for i in range(LOG, -1, -1):
            if up[i][a] != up[i][b]:
                a = up[i][a]
                b = up[i][b]

        return up[0][a]

    def dist(a, b):
        c = lca(a, b)
        return dist_root[a] + dist_root[b] - 2 * dist_root[c]

    active = []
    total_cycle = 0

    def add(x):
        nonlocal total_cycle

        key = (tin[x], x)

        if not active:
            active.append(key)
            return

        pos = bisect_left(active, key)

        nxt = active[pos % len(active)][1]
        prv = active[(pos - 1) % len(active)][1]

        total_cycle += dist(prv, x)
        total_cycle += dist(x, nxt)
        total_cycle -= dist(prv, nxt)

        insort(active, key)

    def remove(x):
        nonlocal total_cycle

        key = (tin[x], x)

        pos = bisect_left(active, key)

        if len(active) == 1:
            active.pop()
            total_cycle = 0
            return

        prv = active[(pos - 1) % len(active)][1]
        nxt = active[(pos + 1) % len(active)][1]

        total_cycle -= dist(prv, x)
        total_cycle -= dist(x, nxt)
        total_cycle += dist(prv, nxt)

        active.pop(pos)

    q = int(input())

    out = []

    for _ in range(q):
        s = input().split()

        if s[0] == '+':
            add(int(s[1]))
        elif s[0] == '-':
            remove(int(s[1]))
        else:
            out.append(str(total_cycle // 2))

    print('\n'.join(out))

solve()
```

The preprocessing DFS computes three independent pieces of information. `tin` defines the cyclic order of active vertices. `depth` and `up` support binary lifting LCA queries. `dist_root` converts LCA results into weighted distances.

The update formulas are the heart of the solution. When a new vertex is inserted into the cyclic order, only one old cycle edge disappears and two new edges appear. Every other pairwise connection remains unchanged.

The ordered container stores pairs `(tin[x], x)` instead of just `tin[x]`. This avoids ambiguity and guarantees uniqueness.

Handling the single-vertex case separately is necessary. Otherwise predecessor and successor become the same vertex, and the update formula degenerates incorrectly.

All distances use 64-bit arithmetic. Edge weights reach `10^9`, and the total answer can be around `10^14`.

## Worked Examples

### Sample 1

Input:

```
6
1 2 1
1 3 5
4 1 7
4 5 3
6 4 2
10
+ 3
+ 1
?
+ 6
?
+ 5
?
- 6
- 3
?
```

DFS order from root `1` becomes:

```
1,2,3,4,5,6
```

| Query | Active Vertices | Cyclic Sum | Answer |
| --- | --- | --- | --- |
| +3 | {3} | 0 | - |
| +1 | {1,3} | 10 | - |
| ? | {1,3} | 10 | 5 |
| +6 | {1,3,6} | 28 | - |
| ? | {1,3,6} | 28 | 14 |
| +5 | {1,3,5,6} | 34 | - |
| ? | {1,3,5,6} | 34 | 17 |
| -6 | {1,3,5} | 30 | - |
| -3 | {1,5} | 20 | - |
| ? | {1,5} | 20 | 10 |

This trace shows the central invariant. The maintained value is always twice the subtree weight.

### Custom Example

```
4
1 2 2
2 3 3
3 4 4
7
+ 1
+ 3
?
+ 4
?
- 3
?
```

| Query | Active Vertices | Cyclic Sum | Answer |
| --- | --- | --- | --- |
| +1 | {1} | 0 | - |
| +3 | {1,3} | 10 | - |
| ? | {1,3} | 10 | 5 |
| +4 | {1,3,4} | 18 | - |
| ? | {1,3,4} | 18 | 9 |
| -3 | {1,4} | 18 | - |
| ? | {1,4} | 18 | 9 |

After removing vertex `3`, the minimal subtree does not change because the path from `1` to `4` already contains it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | DFS preprocessing plus logarithmic updates and LCA queries |
| Space | O(n log n) | Binary lifting table dominates memory usage |

With `10^5` vertices and queries, roughly a few million logarithmic operations are performed. This comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from bisect import bisect_left, insort

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    LOG = 17

    n = int(input())

    g = [[] for _ in range(n + 1)]

    for _ in range(n - 1):
        u, v, w = map(int, input().split())
        g[u].append((v, w))
        g[v].append((u, w))

    tin = [0] * (n + 1)
    depth = [0] * (n + 1)
    dist_root = [0] * (n + 1)

    up = [[0] * (n + 1) for _ in range(LOG + 1)]

    timer = 0

    sys.setrecursionlimit(1 << 25)

    def dfs(v, p):
        nonlocal timer

        timer += 1
        tin[v] = timer

        up[0][v] = p

        for i in range(1, LOG + 1):
            up[i][v] = up[i - 1][up[i - 1][v]]

        for to, w in g[v]:
            if to == p:
                continue

            depth[to] = depth[v] + 1
            dist_root[to] = dist_root[v] + w

            dfs(to, v)

    dfs(1, 1)

    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a

        diff = depth[a] - depth[b]

        for i in range(LOG + 1):
            if diff & (1 << i):
                a = up[i][a]

        if a == b:
            return a

        for i in range(LOG, -1, -1):
            if up[i][a] != up[i][b]:
                a = up[i][a]
                b = up[i][b]

        return up[0][a]

    def dist(a, b):
        c = lca(a, b)
        return dist_root[a] + dist_root[b] - 2 * dist_root[c]

    active = []
    total_cycle = 0

    def add(x):
        nonlocal total_cycle

        key = (tin[x], x)

        if not active:
            active.append(key)
            return

        pos = bisect_left(active, key)

        nxt = active[pos % len(active)][1]
        prv = active[(pos - 1) % len(active)][1]

        total_cycle += dist(prv, x)
        total_cycle += dist(x, nxt)
        total_cycle -= dist(prv, nxt)

        insort(active, key)

    def remove(x):
        nonlocal total_cycle

        key = (tin[x], x)

        pos = bisect_left(active, key)

        if len(active) == 1:
            active.pop()
            total_cycle = 0
            return

        prv = active[(pos - 1) % len(active)][1]
        nxt = active[(pos + 1) % len(active)][1]

        total_cycle -= dist(prv, x)
        total_cycle -= dist(x, nxt)
        total_cycle += dist(prv, nxt)

        active.pop(pos)

    q = int(input())

    out = []

    for _ in range(q):
        s = input().split()

        if s[0] == '+':
            add(int(s[1]))
        elif s[0] == '-':
            remove(int(s[1]))
        else:
            out.append(str(total_cycle // 2))

    return '\n'.join(out)

# provided sample
assert run(
"""6
1 2 1
1 3 5
4 1 7
4 5 3
6 4 2
10
+ 3
+ 1
?
+ 6
?
+ 5
?
- 6
- 3
?
""") == "5\n14\n17\n10"

# single vertex active
assert run(
"""1
3
+ 1
?
?
""") == "0\n0"

# chain tree
assert run(
"""4
1 2 2
2 3 3
3 4 4
7
+ 1
+ 3
?
+ 4
?
- 3
?
""") == "5\n9\n9"

# star tree
assert run(
"""5
1 2 1
1 3 1
1 4 1
1 5 1
8
+ 2
+ 3
+ 4
?
- 3
?
+ 5
?
""") == "3\n2\n3"

# add and remove repeatedly
assert run(
"""2
1 2 7
8
+ 1
+ 2
?
- 1
?
- 2
+ 2
?
""") == "7\n0\n0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex tree | `0 0` | Empty subtree handling |
| Chain tree | `5 9 9` | Internal vertices inside paths |
| Star tree | `3 2 3` | Multiple branches from one center |
| Repeated add/remove | `7 0 0` | Correct deletion updates |

## Edge Cases

Consider the smallest possible tree:

```
1
3
+ 1
?
?
```

There are no edges at all. The active set contains only one vertex. The algorithm stores exactly one element in the ordered set, so `total_cycle` remains `0`. Both queries correctly output:

```
0
```

Now consider a chain:

```
3
1 2 5
2 3 7
5
+ 1
+ 3
?
- 1
?
```

After activating `1` and `3`, the cycle contains:

```
dist(1,3) + dist(3,1) = 12 + 12 = 24
```

Dividing by two gives `12`, which matches the path weight.

After removing `1`, only vertex `3` remains. The deletion handler detects that the active set size becomes one and resets the cycle sum to zero. The second answer is correctly `0`.

Another subtle case is when an active vertex lies on the path between two others:

```
4
1 2 2
2 3 3
3 4 4
7
+ 1
+ 3
+ 4
?
- 3
?
```

The subtree for `{1,3,4}` already includes the entire path from `1` to `4`. Removing `3` changes nothing geometrically. The algorithm reflects this automatically because the cyclic replacement preserves the same total cycle length. Both answers remain `9`.
