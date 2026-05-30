---
title: "CF 475E - Strongly Connected City 2"
description: "We start with a connected undirected graph. Every edge must be assigned a direction. After all directions are chosen, some ordered pairs of vertices $(u,v)$ will satisfy that there is a directed path from $u$ to $v$. The goal is not to make the graph strongly connected."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar"]
categories: ["algorithms"]
codeforces_contest: 475
codeforces_index: "E"
codeforces_contest_name: "Bayan 2015 Contest Warm Up"
rating: 2700
weight: 475
solve_time_s: 146
verified: true
draft: false
---

[CF 475E - Strongly Connected City 2](https://codeforces.com/problemset/problem/475/E)

**Rating:** 2700  
**Tags:** dfs and similar  
**Solve time:** 2m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a connected undirected graph. Every edge must be assigned a direction. After all directions are chosen, some ordered pairs of vertices $(u,v)$ will satisfy that there is a directed path from $u$ to $v$.

The goal is not to make the graph strongly connected. The goal is to choose directions that maximize the total number of reachable ordered pairs. Pairs of the form $(u,u)$ count, because every vertex can reach itself.

The graph is connected before orientation. After orientation it becomes a directed graph whose strongly connected components and reachability structure depend entirely on the chosen directions.

The interesting part of the problem is that the original graph may contain cycles. Inside a cycle we can often orient edges so that every vertex reaches every other vertex. Bridges behave very differently, because any direction chosen on a bridge permanently restricts movement across that edge.

The constraints are small enough for an $O(n^2 / 64)$ subset-sum style DP on the final compressed structure, but far too large for anything that tries all orientations. A graph with $m$ edges has $2^m$ possible orientations, which becomes impossible almost immediately.

A common mistake is to think that every bridge should point in the same global direction. Consider

```
1 - 2 - 3
```

If we orient $1 \to 2 \to 3$, we obtain 6 reachable pairs.

If instead we orient $1 \to 2 \leftarrow 3$, we obtain only 5.

The orientation of bridges matters globally, not locally.

Another easy trap is to ignore cycles and treat the graph as a tree. Consider

```
1 - 2
| \ |
4 - 3
```

This graph has no bridges. We can orient it as a directed cycle and every vertex reaches every other vertex, giving $4^2 = 16$ reachable pairs. Any tree-based reasoning would underestimate the answer.

A third subtle case is a graph consisting of several 2-edge-connected blocks connected by bridges. For example:

```
(triangle) -- bridge -- (triangle)
```

Each triangle can be made strongly connected internally. The only real decision is the direction of the bridge. Any solution that counts individual vertices instead of compressing blocks will become unnecessarily complicated.

## Approaches

A brute-force solution would try every orientation of every edge, build the resulting directed graph, compute reachability, and keep the best answer.

That is correct because it literally checks all possibilities. Unfortunately, with $m$ edges there are $2^m$ orientations. Even for $m=50$ this is hopeless.

The first observation is that bridges are the only edges that can separate the graph. Any edge that is not a bridge belongs to some 2-edge-connected component. A classical result due to Robbins says that every bridgeless connected graph admits a strongly connected orientation. After finding all bridges, every maximal bridge-free component can therefore be oriented so that all of its vertices reach each other.

Suppose a component contains $s$ vertices. After orienting it strongly connected, it contributes exactly $s^2$ reachable ordered pairs internally.

This suggests compressing every 2-edge-connected component into a single weighted node whose weight is its size. Bridges become edges between those weighted nodes. The compressed graph is a tree, often called the bridge tree.

Now the problem becomes:

Given a weighted tree, orient its edges to maximize the number of reachable ordered pairs between weighted nodes.

This is much simpler. A key property, mentioned in the official editorial, is that there exists an optimal orientation with a special root component such that every other component either reaches the root or is reachable from the root.

That root must be a centroid of the weighted tree. If we remove a centroid, every remaining piece has weight at most half of the total. Around the centroid, each neighboring side has some weight $a_i$.

Choose some sides to point toward the centroid and the remaining sides to point away from it.

Let

- $r$ be the centroid weight.
- $T = n-r$.
- $X$ be the total weight of sides directed toward the centroid.
- $T-X$ be the total weight of sides directed away from the centroid.

Then the additional reachable pairs contributed by the tree structure are

$$Xr + r(T-X) + X(T-X)$$

which simplifies to

$$rT + X(T-X).$$

For fixed $r$, maximizing the answer means maximizing $X(T-X)$. This is a classic partition problem. We want $X$ as close as possible to $T/2$, but $X$ must be the sum of whole neighboring-side weights.

That becomes a subset-sum DP on the side sizes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^m \cdot (n+m))$ | $O(n+m)$ | Too slow |
| Optimal | $O(n+m+n^2/64)$ | $O(n+m)$ | Accepted |

## Algorithm Walkthrough

1. Run Tarjan's bridge algorithm on the original graph and mark every bridge.
2. Remove all bridges conceptually and DFS through the remaining edges. Each connected region becomes one 2-edge-connected component.
3. Record the size of every component. If a component contains $s$ vertices, add $s^2$ to the answer. This is the contribution obtained by orienting that component strongly connected.
4. Build the bridge tree. Each component becomes a weighted node whose weight equals its size. Every original bridge becomes an edge between two component nodes.
5. Compute subtree weights in the bridge tree and find all weighted centroids. A centroid is a node whose removal leaves no part with weight greater than $n/2$.
6. For each centroid:

1. Let its weight be $r$.
2. For every adjacent side, compute its total weight $a_i$.
3. Run subset-sum DP on the values $a_i$.
4. For every achievable sum $X$, evaluate

$$r(n-r) + X((n-r)-X).$$
5. Keep the maximum value.
7. Add that maximum tree contribution to the internal contribution computed in step 3.

### Why it works

Every non-bridge edge lies inside a 2-edge-connected component. Such a component can be oriented strongly connected, so all pairs of vertices inside it become reachable. Compressing each component into a weighted node loses no information relevant to the optimum.

After compression, the graph is a tree. In an optimal orientation, all paths that create reachability between different branches must pass through a single centroid component. Once the centroid is fixed, each neighboring side is either entirely on the "incoming" side or entirely on the "outgoing" side. Reachability between different sides depends only on the total weights assigned to those two groups.

If the incoming weight is $X$ and the outgoing weight is $T-X$, every vertex in the incoming group can reach every vertex in the outgoing group through the centroid. The resulting contribution is exactly

$$rT + X(T-X).$$

No other orientation can create more cross-group reachability, and maximizing this expression reduces to the subset-sum partition described above.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    g = [[] for _ in range(n)]
    edges = []

    for eid in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        edges.append((u, v))
        g[u].append((v, eid))
        g[v].append((u, eid))

    tin = [-1] * n
    low = [0] * n
    timer = 0
    is_bridge = [False] * m

    sys.setrecursionlimit(1 << 20)

    def dfs_bridge(v, pe):
        nonlocal timer
        tin[v] = low[v] = timer
        timer += 1

        for to, eid in g[v]:
            if eid == pe:
                continue

            if tin[to] != -1:
                low[v] = min(low[v], tin[to])
            else:
                dfs_bridge(to, eid)
                low[v] = min(low[v], low[to])

                if low[to] > tin[v]:
                    is_bridge[eid] = True

    dfs_bridge(0, -1)

    comp = [-1] * n
    comp_size = []

    def dfs_comp(start, cid):
        stack = [start]
        comp[start] = cid
        sz = 0

        while stack:
            v = stack.pop()
            sz += 1

            for to, eid in g[v]:
                if is_bridge[eid]:
                    continue
                if comp[to] == -1:
                    comp[to] = cid
                    stack.append(to)

        return sz

    cc = 0
    base = 0

    for v in range(n):
        if comp[v] == -1:
            sz = dfs_comp(v, cc)
            comp_size.append(sz)
            base += sz * sz
            cc += 1

    if cc == 1:
        print(base)
        return

    tree = [[] for _ in range(cc)]

    for eid, (u, v) in enumerate(edges):
        if is_bridge[eid]:
            a = comp[u]
            b = comp[v]
            tree[a].append(b)
            tree[b].append(a)

    total_weight = n

    parent = [-1] * cc
    sub = [0] * cc

    def dfs_sub(v, p):
        parent[v] = p
        s = comp_size[v]

        for to in tree[v]:
            if to == p:
                continue
            dfs_sub(to, v)
            s += sub[to]

        sub[v] = s

    dfs_sub(0, -1)

    centroids = []

    for v in range(cc):
        mx = total_weight - sub[v]

        for to in tree[v]:
            if to == parent[v]:
                continue
            mx = max(mx, sub[to])

        if mx * 2 <= total_weight:
            centroids.append(v)

    best_extra = 0

    for c in centroids:
        sides = []

        for to in tree[c]:
            if to == parent[c]:
                sides.append(total_weight - sub[c])
            else:
                sides.append(sub[to])

        r = comp_size[c]
        T = total_weight - r

        bits = 1
        for a in sides:
            bits |= bits << a

        best_partition = 0

        for x in range(T + 1):
            if (bits >> x) & 1:
                best_partition = max(best_partition, x * (T - x))

        best_extra = max(best_extra, r * T + best_partition)

    print(base + best_extra)

if __name__ == "__main__":
    solve()
```

The first DFS finds all bridges using the standard low-link technique. An edge is a bridge exactly when the subtree below it cannot reach an ancestor of its parent.

The second DFS ignores bridges and labels 2-edge-connected components. The size of each component becomes the weight of a node in the bridge tree.

The variable `base` stores the sum of $s^2$ over all compressed components. That part of the answer is independent of the bridge orientations.

The bridge tree is then built. Subtree weights are computed once, allowing every neighboring side of a centroid to be obtained in constant time.

The subset-sum DP uses a bitset encoded as a Python integer. If bit `k` is set, then a total side weight of `k` is achievable. Shifting by `a` and OR-ing performs the standard knapsack transition extremely efficiently.

The final answer is the internal contribution plus the best cross-component contribution.

## Worked Examples

### Sample 1

Input:

```
5 4
1 2
1 3
1 4
1 5
```

The graph is already a tree.

After bridge decomposition every vertex forms its own component.

| Quantity | Value |
| --- | --- |
| Component weights | 1,1,1,1,1 |
| Base contribution | 5 |
| Centroid weight | 1 |
| Side weights | 1,1,1,1 |
| T | 4 |

Subset sums can produce $X=2$.

| X | X(T-X) |
| --- | --- |
| 0 | 0 |
| 1 | 3 |
| 2 | 4 |
| 3 | 3 |
| 4 | 0 |

Best tree contribution:

$$1 \cdot 4 + 4 = 8.$$

Total:

$$5 + 8 = 13.$$

### Sample 4

Input:

```
6 7
1 2
2 3
1 3
1 4
4 5
5 6
6 4
```

There are two bridge-free components.

| Component | Size |
| --- | --- |
| {1,2,3} | 3 |
| {4,5,6} | 3 |

Base contribution:

$$3^2 + 3^2 = 18.$$

The bridge tree contains two nodes connected by one bridge.

| Quantity | Value |
| --- | --- |
| Centroid weight | 3 |
| Side weight | 3 |
| T | 3 |

Only $X=0$ or $X=3$ are possible.

$$3 \cdot 3 + 0 = 9.$$

Total:

$$18 + 9 = 27.$$

This example shows why compressing bridge-free components is essential. The whole problem reduces to orienting a single bridge.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + m + n^2/64)$ | Bridge finding, component construction, tree processing, and bitset subset-sum |
| Space | $O(n + m)$ | Graph, bridge tree, DFS arrays |

The graph traversals are linear. The only non-linear part is the subset-sum bitset, whose effective cost is $O(n^2/64)$. That comfortably fits within the contest limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    # paste solve() here and return captured output
    pass

# provided samples
assert run(
"""5 4
1 2
1 3
1 4
1 5
""") == "13"

assert run(
"""4 5
1 2
2 3
3 4
4 1
1 3
""") == "16"

assert run(
"""2 1
1 2
""") == "3"

assert run(
"""6 7
1 2
2 3
1 3
1 4
4 5
5 6
6 4
""") == "27"

# single vertex
assert run(
"""1 0
""") == "1"

# simple path of length 2
assert run(
"""3 2
1 2
2 3
""") == "6"

# triangle, no bridges
assert run(
"""3 3
1 2
2 3
3 1
""") == "9"

# two cycles connected by one bridge
assert run(
"""6 7
1 2
2 3
3 1
3 4
4 5
5 6
6 4
""") == "27"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex | 1 | Smallest possible graph |
| Path of length 2 | 6 | Pure tree behaviour |
| Triangle | 9 | Graph with no bridges |
| Two cycles and one bridge | 27 | Correct component compression |

## Edge Cases

Consider a graph with no bridges:

```
4 5
1 2
2 3
3 4
4 1
1 3
```

The entire graph becomes one component of size 4. The bridge tree contains a single node. The algorithm immediately returns

$$4^2 = 16.$$

No subset-sum phase is needed.

Now consider a pure tree:

```
2 1
1 2
```

Each vertex becomes its own component. The bridge tree has two nodes of weight 1. The centroid has weight 1, the only side has weight 1, and the formula gives

$$1 + (1 \cdot 1) + 0 = 3.$$

This matches the sample.

Finally, consider two large blocks connected by a bridge:

```
1-2-3-1   bridge   4-5-6-4
```

The decomposition produces component weights $3$ and $3$. Internal reachability contributes $18$. The bridge orientation contributes $9$. The answer is $27$.

This case demonstrates the central invariant of the solution: once 2-edge-connected components are compressed, only the bridge tree influences additional reachability.
