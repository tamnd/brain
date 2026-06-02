---
title: "CF 176E - Archaeology"
description: "We are given a weighted tree. Villages correspond to vertices and roads correspond to weighted edges. At any moment, only some villages are \"alive\". Villages can be added and removed over time."
date: "2026-06-02T17:07:37+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "trees"]
categories: ["algorithms"]
codeforces_contest: 176
codeforces_index: "E"
codeforces_contest_name: "Croc Champ 2012 - Round 2"
rating: 3100
weight: 176
solve_time_s: 160
verified: false
draft: false
---

[CF 176E - Archaeology](https://codeforces.com/problemset/problem/176/E)

**Rating:** 3100  
**Tags:** data structures, dfs and similar, trees  
**Solve time:** 2m 40s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a weighted tree. Villages correspond to vertices and roads correspond to weighted edges.

At any moment, only some villages are "alive". Villages can be added and removed over time. After each update, we may be asked for the total length of the roads that are actually used.

The key phrase is that people use the minimum set of roads that still allows travel between every pair of currently existing villages. Since the original graph is a tree, the answer is simply the total weight of the smallest connected subtree containing all active vertices.

Another way to say this is: among all edges of the original tree, keep exactly those that lie on a path between two active vertices. The sum of their weights is the required answer.

The tree contains up to $10^5$ vertices and there are up to $10^5$ updates and queries. Recomputing the minimal subtree from scratch after every modification is impossible. Even an $O(n)$ traversal per update would require around $10^{10}$ operations in the worst case.

The problem asks for a fully dynamic set of vertices inside a static tree, with insertions, deletions, and subtree-length queries.

Several edge cases are easy to misunderstand.

Consider a single active vertex:

```
1
?
```

No edge is needed to connect one vertex, so the answer is 0.

A careless implementation that always sums distances between active vertices could accidentally produce a positive value.

Consider two active vertices connected by a path:

```
1 --5-- 2 --7-- 3
active = {1,3}
```

The answer is $5+7=12$.

The minimal subtree is exactly the unique path between them.

Now consider three active vertices:

```
    2
    |
1 --3-- 4
```

If all vertices are active, the answer is the sum of all three edges.

A naive idea such as "sum pairwise distances and divide by something" fails because each edge participates in many pairwise paths.

The difficult part is supporting insertions and deletions while maintaining the size of the Steiner tree of the active vertices.

## Approaches

The brute-force solution is straightforward.

After every update, collect all active vertices. Construct the virtual tree of those vertices, or simply mark every edge that belongs to a path between active vertices, and sum the corresponding edge weights.

This is correct because the answer is exactly the minimal connected subtree spanning all active vertices.

Unfortunately, if there are $k$ active vertices, even building the answer from scratch costs at least $O(k \log n)$, often $O(n)$. With $10^5$ updates, this becomes far too large.

The breakthrough comes from a classical property of trees.

Let the active vertices be ordered by Euler-tour entry time. If we connect consecutive active vertices in that cyclic order and sum their pairwise distances, every edge of the Steiner tree is counted exactly twice.

Thus:

$$\text{SteinerWeight}
=
\frac{
\sum d(v_i,v_{i+1})
}{
2
}$$

where the order is cyclic in DFS order.

This transforms the problem from maintaining a subtree into maintaining a cyclic set of vertices.

When a vertex is inserted, only its predecessor and successor in Euler order matter. The global cycle changes locally.

Suppose the inserted vertex is $x$, predecessor is $p$, successor is $s$.

Previously the contribution contained

$$d(p,s)$$

After insertion it becomes

$$d(p,x)+d(x,s)$$

So the maintained cycle sum changes by

$$d(p,x)+d(x,s)-d(p,s).$$

Deletion performs the inverse operation.

The remaining task is computing distances quickly. Since the tree never changes, we preprocess depths, root distances, and LCA.

Then

$$d(u,v)
=
distRoot[u]
+
distRoot[v]
-
2\,distRoot[lca(u,v)].$$

Each update requires only predecessor/successor queries in an ordered set and a constant number of distance computations.

### Comparison

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n)$ per update/query | $O(n)$ | Too slow |
| Optimal | $O((n+q)\log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

### Preprocessing

1. Root the tree at any vertex, for example vertex 1.
2. Run DFS and compute Euler entry times `tin[u]`.
3. Compute depths, root-distance values, and binary-lifting ancestors for LCA.
4. For every vertex, store the pair `(tin[u], u)`. Active vertices will be maintained ordered by `tin`.

### Dynamic maintenance

Maintain:

- An ordered set of active vertices sorted by Euler time.
- A value `cycle_sum`.

`cycle_sum` is

$$\sum d(v_i,v_{i+1})$$

over the cyclic DFS order.

### Inserting a vertex

1. Find the predecessor and successor of the new vertex in Euler order.
2. If this is the first active vertex, simply insert it.
3. Otherwise add

$$d(pred,x)+d(x,succ)-d(pred,succ)$$

to `cycle_sum`.

4. Insert the vertex into the ordered set.

The old edge of the cycle is replaced by two new edges.

### Removing a vertex

1. Find predecessor and successor of the vertex.
2. If it is the only active vertex, remove it and set the cycle contribution to zero.
3. Otherwise add

$$d(pred,succ)-d(pred,x)-d(x,succ)$$

to `cycle_sum`.

4. Remove the vertex.

This exactly reverses the insertion operation.

### Answering a query

1. If fewer than two vertices are active, answer 0.
2. Otherwise output

$$\frac{\text{cycle\_sum}}{2}.$$

### Why it works

Let the active vertices be listed cyclically by DFS order.

Take any edge $e$ of the minimal subtree spanning all active vertices. Removing $e$ splits the tree into two components. Since $e$ belongs to the Steiner tree, both sides contain active vertices.

In the cyclic DFS order, exactly two consecutive pairs cross from one side to the other. Each such crossing contributes the weight of $e$ once to the distance sum.

Hence every Steiner-tree edge contributes exactly twice to the cyclic distance sum. Edges outside the Steiner tree contribute zero times.

Therefore the maintained quantity is always exactly twice the answer. Since insertion and deletion update the cyclic order locally, the invariant remains true after every operation.

## Python Solution

```python
import sys
from bisect import bisect_left, insort

input = sys.stdin.readline

def solve():
    n = int(input())

    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        a, b, c = map(int, input().split())
        a -= 1
        b -= 1
        g[a].append((b, c))
        g[b].append((a, c))

    LOG = 17
    while (1 << LOG) <= n:
        LOG += 1

    tin = [0] * n
    depth = [0] * n
    root_dist = [0] * n
    up = [[0] * n for _ in range(LOG)]

    timer = 0

    stack = [(0, 0, 0, 0)]
    while stack:
        u, p, state, idx = stack.pop()

        if state == 0:
            tin[u] = timer
            timer += 1

            up[0][u] = p

            stack.append((u, p, 1, 0))

            for v, w in reversed(g[u]):
                if v == p:
                    continue
                depth[v] = depth[u] + 1
                root_dist[v] = root_dist[u] + w
                stack.append((v, u, 0, 0))

    for k in range(1, LOG):
        prev = up[k - 1]
        cur = up[k]
        for v in range(n):
            cur[v] = prev[prev[v]]

    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a

        diff = depth[a] - depth[b]
        bit = 0
        while diff:
            if diff & 1:
                a = up[bit][a]
            diff >>= 1
            bit += 1

        if a == b:
            return a

        for k in range(LOG - 1, -1, -1):
            if up[k][a] != up[k][b]:
                a = up[k][a]
                b = up[k][b]

        return up[0][a]

    def dist(a, b):
        c = lca(a, b)
        return root_dist[a] + root_dist[b] - 2 * root_dist[c]

    q = int(input())

    active = []
    cycle_sum = 0

    def add_vertex(x):
        nonlocal cycle_sum

        key = (tin[x], x)

        if not active:
            insort(active, key)
            return

        pos = bisect_left(active, key)

        succ = active[pos % len(active)][1]
        pred = active[(pos - 1) % len(active)][1]

        cycle_sum += (
            dist(pred, x)
            + dist(x, succ)
            - dist(pred, succ)
        )

        active.insert(pos, key)

    def remove_vertex(x):
        nonlocal cycle_sum

        key = (tin[x], x)

        pos = bisect_left(active, key)

        if len(active) == 1:
            active.pop()
            cycle_sum = 0
            return

        pred = active[(pos - 1) % len(active)][1]
        succ = active[(pos + 1) % len(active)][1]

        cycle_sum += (
            dist(pred, succ)
            - dist(pred, x)
            - dist(x, succ)
        )

        active.pop(pos)

    out = []

    for _ in range(q):
        s = input().split()

        if s[0] == '+':
            add_vertex(int(s[1]) - 1)
        elif s[0] == '-':
            remove_vertex(int(s[1]) - 1)
        else:
            out.append(str(cycle_sum // 2))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

After the code block, the key observation is the maintained cyclic distance sum. The active vertices are always stored in DFS order. Every update modifies only one place in that cycle, so we never need to rebuild the Steiner tree.

The LCA preprocessing provides distance queries in $O(\log n)$. Every insertion or deletion performs a constant number of such distance computations and a predecessor/successor search.

In C++, the intended solution uses an ordered set. In Python, a production-quality accepted solution typically uses a balanced-tree implementation. The editorial code above illustrates the mathematical update formula clearly, while the accepted Codeforces implementation uses a true ordered set to preserve $O(\log n)$ updates.

## Worked Examples

### Sample 1

Active vertices are shown in Euler order.

| Operation | Active Set | Cycle Sum | Answer |
| --- | --- | --- | --- |
| +3 | {3} | 0 |  |
| +1 | {1,3} | 10 |  |
| ? | {1,3} | 10 | 5 |
| +6 | {1,3,6} | 28 |  |
| ? | {1,3,6} | 28 | 14 |
| +5 | {1,3,5,6} | 34 |  |
| ? | {1,3,5,6} | 34 | 17 |
| -6 | {1,3,5} | 20 |  |
| -3 | {1,5} | 20 |  |
| ? | {1,5} | 20 | 10 |

The answers are obtained as `cycle_sum / 2`.

### Custom Example

Tree:

```
1 --4-- 2 --6-- 3
```

Operations:

```
+1
+3
?
+2
?
```

| Operation | Active Set | Cycle Sum | Answer |
| --- | --- | --- | --- |
| +1 | {1} | 0 |  |
| +3 | {1,3} | 20 |  |
| ? | {1,3} | 20 | 10 |
| +2 | {1,2,3} | 20 |  |
| ? | {1,2,3} | 20 | 10 |

Adding vertex 2 does not change the Steiner tree because it already lies on the path connecting 1 and 3.

This confirms that the maintained quantity measures the minimal connecting subtree, not the number of active vertices.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n+q)\log n)$ | LCA preprocessing plus logarithmic updates |
| Space | $O(n\log n)$ | Binary lifting table and tree storage |

The tree contains at most $10^5$ vertices and there are at most $10^5$ operations. A logarithmic update cost keeps the total work comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    return "<execute solve() here>"

# sample 1
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
"""
) == "5\n14\n17\n10"

# single vertex
assert run(
"""1
3
+ 1
?
- 1
"""
) == "0"

# simple chain
assert run(
"""3
1 2 4
2 3 6
5
+ 1
+ 3
?
+ 2
?
"""
) == "10\n10"

# add then remove middle
assert run(
"""3
1 2 1
2 3 1
7
+ 1
+ 2
+ 3
?
- 2
?
?
"""
) == "2\n2\n2"

# star tree
assert run(
"""4
1 2 5
1 3 5
1 4 5
6
+ 2
+ 3
?
+ 4
?
?
"""
) == "10\n15\n15"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex tree | 0 | Empty Steiner tree |
| Chain with endpoint activation | 10 | Path distance computation |
| Remove middle active vertex | 2 | Active vertices need not be Steiner vertices |
| Star tree | 10, 15 | Multiple branches joining at one center |

## Edge Cases

### Only one active vertex

Input:

```
1
3
+ 1
?
- 1
```

The active set contains a single vertex. The maintained cycle sum remains zero because there is no edge in the cycle. The answer is `0 / 2 = 0`.

### Active vertex lies on an existing Steiner path

Input:

```
3
1 2 4
2 3 6
5
+ 1
+ 3
?
+ 2
?
```

Initially the answer is 10 because the path from 1 to 3 uses both edges.

After activating vertex 2, the minimal connected subtree is unchanged. The insertion update adds

$$d(1,2)+d(2,3)-d(1,3)
=
4+6-10
=
0.$$

The maintained value does not change, producing the correct answer.

### Empty active set

Input:

```
2
1 2 7
4
+ 1
- 1
?
?
```

After deletion, no active vertices remain.

The data structure becomes empty and `cycle_sum` is reset to zero. Every query correctly outputs 0.

### Two active vertices becoming one

Input:

```
2
1 2 7
5
+ 1
+ 2
- 2
?
?
```

Before deletion the cycle sum is $14$, corresponding to answer $7$.

Deleting vertex 2 leaves only one active vertex. The special case for size one resets the maintained value to zero, avoiding stale contributions from the previous cycle. The answer becomes 0, which is exactly the size of the Steiner tree containing a single vertex.
