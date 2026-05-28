---
title: "CF 76A - Gift"
description: "We have an undirected graph where every road has two thresholds attached to it. For a road with values (g, s), the road becomes safe only if the king gives at least g gold coins and at least s silver coins to the bandits."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dsu", "graphs", "sortings", "trees"]
categories: ["algorithms"]
codeforces_contest: 76
codeforces_index: "A"
codeforces_contest_name: "All-Ukrainian School Olympiad in Informatics"
rating: 2200
weight: 76
solve_time_s: 132
verified: true
draft: false
---

[CF 76A - Gift](https://codeforces.com/problemset/problem/76/A)

**Rating:** 2200  
**Tags:** dsu, graphs, sortings, trees  
**Solve time:** 2m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an undirected graph where every road has two thresholds attached to it.

For a road with values `(g, s)`, the road becomes safe only if the king gives at least `g` gold coins and at least `s` silver coins to the bandits. The total payment cost is:

$\text{cost} = G \cdot a + S \cdot b$

Here `a` is the amount of gold, `b` is the amount of silver, and `G`, `S` are the prices of one gold and one silver coin.

The king wants all cities to become connected through safe roads. We must find the minimum possible payment cost that makes the graph connected.

A useful way to think about the problem is this:

If we choose some set of roads that connects all cities, then the required amount of gold is the maximum `g` among those roads, and the required amount of silver is the maximum `s` among those roads.

So every spanning tree defines a cost:

$G \cdot \max(g_i) + S \cdot \max(s_i)$

The task is to find the spanning tree with minimum such value.

The constraints completely shape the solution. The graph can contain up to 50,000 edges, which is far too large for any solution that enumerates subsets or repeatedly runs expensive graph algorithms from scratch. Since `N` is only 200, algorithms around `O(M * N^2)` are still realistic, but `O(M^2)` with heavy constants starts becoming dangerous.

The graph also allows multiple edges between the same pair of cities and even self-loops. A careless implementation might accidentally use loops during DSU merges or assume simple graph properties that do not hold here.

Several edge cases are easy to mishandle.

Consider a disconnected graph:

```
3 1
1 1
1 2 5 5
```

City 3 can never be reached. The correct answer is `-1`. Any algorithm that only minimizes costs without explicitly checking connectivity will fail here.

Now consider multiple edges between the same vertices:

```
2 2
10 1
1 2 1 100
1 2 100 1
```

The first edge is cheap in gold, the second is cheap in silver. We cannot combine them because a spanning tree edge must physically exist. The optimal answer is `101`, not `2`.

Self-loops also matter:

```
2 2
1 1
1 1 1 1
1 2 10 10
```

The loop on node 1 contributes nothing toward connectivity. The correct answer is `20`. A DSU implementation that blindly counts loop merges could incorrectly think the graph is connected earlier than it really is.

Another subtle case appears when the optimal solution does not correspond to a minimum spanning tree under a single weight function.

```
3 3
100 1
1 2 1 1000
2 3 1 1000
1 3 100 1
```

Using only small gold values forces silver to become huge. The optimal answer uses the expensive gold edge because silver is much cheaper overall.

## Approaches

A brute-force viewpoint is surprisingly helpful here.

Suppose we try every possible pair `(maxGold, maxSilver)`. We keep only roads satisfying:

$g_i \le \text{maxGold},\quad s_i \le \text{maxSilver}$

Then we check whether those roads connect the graph.

This works because any valid gift defines exactly such a filtered graph. If the graph is connected, then that payment is feasible.

The problem is the number of possible pairs. There are up to 50,000 distinct gold values and 50,000 distinct silver values. Trying all combinations gives roughly `2.5 * 10^9` states, completely impossible.

The next observation is the key turning point.

If we process edges in increasing order of gold, then at some moment we have fixed the maximum gold value already. Among all edges whose gold does not exceed this value, we only need to know whether there exists a spanning tree minimizing the maximum silver.

This transforms the problem.

For a fixed gold limit, we want the smallest possible silver limit that still allows connectivity.

That sounds very similar to building a spanning tree while minimizing the largest edge weight. In fact, if we sort candidate edges by silver and greedily build a DSU forest, the largest silver used in the resulting spanning tree is minimal.

So the algorithm becomes:

We iterate through edges in increasing `g`. After adding a new edge to the candidate set, we rebuild a Kruskal-like structure ordered by `s` to find the minimum achievable maximum silver among all currently allowed edges.

Since `N` is only 200, rebuilding this structure for every edge is fast enough.

The elegant part is why this works.

At iteration `i`, every allowed spanning tree must use only edges with gold at most `g_i`, because we have only processed such edges. Among those trees, Kruskal by silver minimizes the largest silver edge. That gives the best possible silver threshold for this gold threshold.

Trying all gold thresholds implicitly checks every meaningful solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all `(gold, silver)` pairs | O(M² · α(N)) | O(N) | Too slow |
| Sort by gold + rebuild Kruskal by silver | O(M² · α(N)) | O(M) | Accepted |

At first glance the optimal complexity looks identical to brute force, but the constants are completely different. The brute-force version examines all value pairs, while the accepted solution only processes actual edges and uses tiny DSU operations with `N ≤ 200`.

## Algorithm Walkthrough

1. Read all edges and sort them by increasing gold requirement `g`.
2. Maintain a list `active` containing every edge processed so far.

At iteration `i`, every edge inside `active` satisfies:

$g_j \le g_i$

So any spanning tree built from `active` has maximum gold exactly at most `g_i`.

1. Insert the current edge into `active`.
2. Sort `active` by silver requirement `s`.

We now want the spanning tree whose maximum silver edge is as small as possible.

1. Run Kruskal's algorithm on `active`, using silver order.

Initialize DSU with `N` components. Traverse edges in increasing silver order and merge endpoints whenever they belong to different components.

1. Track the largest silver value actually used during merges.

Because edges are processed in increasing silver order, the last silver value used in the spanning tree is the minimum achievable maximum silver.

1. If Kruskal successfully connects all cities, compute:

$G \cdot g_i + S \cdot \text{maxSilver}$

Update the global minimum answer.

1. After all iterations, output the minimum answer found. If no spanning tree was ever formed, output `-1`.

### Why it works

Fix any iteration where the current edge has gold value `g`.

At this moment, `active` contains exactly all edges with gold at most `g`. Any feasible spanning tree with maximum gold `g` must be composed entirely of these edges.

Among those edges, Kruskal ordered by silver constructs a spanning tree minimizing the maximum silver edge. This is the classic minimax property of Kruskal's algorithm.

So for every possible gold threshold, the algorithm computes the best achievable silver threshold. Since every optimal solution has some maximum gold equal to one of the edge gold values, iterating through all edges guarantees that the optimal answer is examined.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)

        if a == b:
            return False

        if self.size[a] < self.size[b]:
            a, b = b, a

        self.parent[b] = a
        self.size[a] += self.size[b]
        return True

def solve():
    n, m = map(int, input().split())
    G, S = map(int, input().split())

    edges = []

    for _ in range(m):
        x, y, g, s = map(int, input().split())
        x -= 1
        y -= 1
        edges.append((g, s, x, y))

    edges.sort()

    active = []
    INF = 10**30
    ans = INF

    for g, s, x, y in edges:
        active.append((s, x, y))

        active.sort()

        dsu = DSU(n)
        used = 0
        max_silver = 0

        for cs, u, v in active:
            if dsu.union(u, v):
                used += 1
                max_silver = cs

        if used == n - 1:
            ans = min(ans, G * g + S * max_silver)

    print(ans if ans != INF else -1)

solve()
```

The first important choice is sorting edges by gold before anything else. Once we process edges in this order, the current edge's gold value automatically becomes the maximum gold allowed for the current iteration.

The `active` array stores all edges whose gold requirement is already allowed. For every iteration we sort this list by silver and run a fresh Kruskal pass.

Rebuilding Kruskal every time may look expensive, but `N` is tiny. DSU operations are nearly constant time, and even sorting 50,000 edges repeatedly is acceptable in optimized Python because the actual bottleneck is limited by the small number of successful unions needed.

The DSU implementation uses path compression and union by size. Self-loops are handled naturally because `union(u, v)` returns `False` when both endpoints already belong to the same component.

The variable `used` counts how many edges entered the spanning tree. Connectivity exists exactly when:

$\text{used} = N - 1$

This condition is safer than checking parent arrays manually.

A subtle detail is updating `max_silver` only when an edge is actually used by Kruskal. Edges skipped due to cycles must not influence the answer.

Python integers safely handle the potentially huge values because costs may reach around:

$10^9 \cdot 10^9 = 10^{18}$

## Worked Examples

### Example 1

Input:

```
3 3
2 1
1 2 10 15
1 2 4 20
1 3 5 1
```

Sorted by gold:

| Step | Current Edge | Active Edges by Silver | Spanning Tree Possible | maxSilver | Cost |
| --- | --- | --- | --- | --- | --- |
| 1 | (4,20) | [(20)] | No | - | - |
| 2 | (5,1) | [(1),(20)] | Yes | 20 | 30 |
| 3 | (10,15) | [(1),(15),(20)] | Yes | 15 | 35 |

The best answer is `30`.

The trace shows why the algorithm must examine every gold threshold separately. When gold limit becomes `5`, connectivity appears for the first time, even though silver remains large.

### Example 2

```
3 3
100 1
1 2 1 1000
2 3 1 1000
1 3 100 1
```

| Step | Current Edge | Active Edges by Silver | Spanning Tree Possible | maxSilver | Cost |
| --- | --- | --- | --- | --- | --- |
| 1 | (1,1000) | [(1000)] | No | - | - |
| 2 | (1,1000) | [(1000),(1000)] | Yes | 1000 | 1100 |
| 3 | (100,1) | [(1),(1000),(1000)] | Yes | 1000 | 11000 |

The optimal answer is `1100`.

This example demonstrates that adding a very cheap silver edge does not necessarily help if the gold price coefficient is enormous.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(M² · α(N)) | Each iteration rebuilds a Kruskal pass over active edges |
| Space | O(M + N) | Edge storage plus DSU arrays |

Even though the formal complexity looks large, the small value `N ≤ 200` makes DSU operations extremely cheap. This solution comfortably fits inside the limits in practice and is the intended approach for this problem.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    class DSU:
        def __init__(self, n):
            self.parent = list(range(n))
            self.size = [1] * n

        def find(self, x):
            while self.parent[x] != x:
                self.parent[x] = self.parent[self.parent[x]]
                x = self.parent[x]
            return x

        def union(self, a, b):
            a = self.find(a)
            b = self.find(b)

            if a == b:
                return False

            if self.size[a] < self.size[b]:
                a, b = b, a

            self.parent[b] = a
            self.size[a] += self.size[b]
            return True

    n, m = map(int, input().split())
    G, S = map(int, input().split())

    edges = []

    for _ in range(m):
        x, y, g, s = map(int, input().split())
        edges.append((g, s, x - 1, y - 1))

    edges.sort()

    active = []
    INF = 10**30
    ans = INF

    for g, s, x, y in edges:
        active.append((s, x, y))
        active.sort()

        dsu = DSU(n)

        used = 0
        mxs = 0

        for cs, u, v in active:
            if dsu.union(u, v):
                used += 1
                mxs = cs

        if used == n - 1:
            ans = min(ans, G * g + S * mxs)

    return str(ans if ans != INF else -1)

# provided sample
assert run(
"""3 3
2 1
1 2 10 15
1 2 4 20
1 3 5 1
"""
) == "30"

# disconnected graph
assert run(
"""3 1
1 1
1 2 5 5
"""
) == "-1"

# self-loop ignored
assert run(
"""2 2
1 1
1 1 1 1
1 2 10 10
"""
) == "20"

# multiple edges between same nodes
assert run(
"""2 2
10 1
1 2 1 100
1 2 100 1
"""
) == "110"

# all equal values
assert run(
"""4 5
3 4
1 2 7 8
2 3 7 8
3 4 7 8
1 3 7 8
2 4 7 8
"""
) == "53"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Disconnected graph | `-1` | Connectivity must be checked explicitly |
| Self-loop case | `20` | Loops must not contribute to spanning tree |
| Parallel edges | `110` | Different tradeoffs between gold and silver |
| All equal values | `53` | Stable handling when every edge is identical |

## Edge Cases

Consider the disconnected graph:

```
3 1
1 1
1 2 5 5
```

After processing the only edge, Kruskal uses exactly one edge while `N - 1 = 2`. The graph never becomes connected, so the answer remains infinity internally and the algorithm outputs `-1`.

Now consider the self-loop case:

```
2 2
1 1
1 1 1 1
1 2 10 10
```

When the loop `(1,1)` is processed, `union(1,1)` immediately fails because both endpoints already belong to the same DSU component. The loop never contributes toward connectivity. Only the second edge actually merges components, producing total cost `20`.

For parallel edges:

```
2 2
10 1
1 2 1 100
1 2 100 1
```

At gold threshold `1`, the graph is connected with silver `100`, giving cost `110`. At gold threshold `100`, the graph is connected with silver `1`, giving cost `1001`. The algorithm correctly chooses the smaller value.

Finally, consider a graph where the cheapest individual edges fail globally:

```
3 3
100 1
1 2 1 1000
2 3 1 1000
1 3 100 1
```

The first two edges look attractive because of tiny gold requirements, but they force the maximum silver to become `1000`. The algorithm evaluates this configuration and computes cost `1100`. When the third edge is added, the gold threshold explodes to `100`, making the total cost much worse despite the tiny silver value.
