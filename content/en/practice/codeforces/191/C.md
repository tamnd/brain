---
title: "CF 191C - Fools and Roads"
description: "The input describes a tree of cities. Since there is exactly one simple path between every pair of cities, the road network forms a connected acyclic graph. Then we are given several pairs of cities."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "trees"]
categories: ["algorithms"]
codeforces_contest: 191
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 121 (Div. 1)"
rating: 1900
weight: 191
solve_time_s: 115
verified: true
draft: false
---

[CF 191C - Fools and Roads](https://codeforces.com/problemset/problem/191/C)

**Rating:** 1900  
**Tags:** data structures, dfs and similar, trees  
**Solve time:** 1m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

The input describes a tree of cities. Since there is exactly one simple path between every pair of cities, the road network forms a connected acyclic graph.

Then we are given several pairs of cities. Each pair represents one trip: a fool travels from city `a` to city `b` along the unique simple path in the tree. For every road, we must count how many trips use that road.

A direct interpretation would be: for every query `(a, b)`, find the path from `a` to `b` and increment the count on every edge of that path. That is logically correct, because the tree guarantees uniqueness of the route.

The constraints immediately rule out that approach. The tree has up to `10^5` vertices, and there can also be `10^5` queries. A single path can contain `O(n)` edges in the worst case, for example in a chain-shaped tree. That gives `O(nk)` operations, which can become `10^10`, far beyond the limit.

The structure of a tree gives us something much stronger. Every path between two nodes can be represented using their Lowest Common Ancestor, usually abbreviated as LCA. Instead of explicitly walking every edge on every query, we can mark endpoints and later aggregate contributions with one DFS.

Several edge cases are easy to mishandle if the implementation is careless.

Consider a query where both endpoints are the same city:

```
3
1 2
2 3
1
2 2
```

No road is used, so the correct output is:

```
0 0
```

A naive implementation that always increments along the path without checking for empty paths may accidentally count edges.

Another subtle case appears when one endpoint is the ancestor of the other:

```
4
1 2
2 3
3 4
1
2 4
```

The path uses only edges `(2,3)` and `(3,4)`. If the LCA handling subtracts twice from the parent of the LCA instead of the LCA itself, the counts become incorrect.

A star-shaped tree also stresses correctness:

```
5
1 2
1 3
1 4
1 5
2
2 3
4 5
```

The center edge counts should be:

```
2 2 2 2
```

Every trip passes through the root. Mistakes in subtree accumulation often undercount such configurations because many paths overlap at one node.

## Approaches

The brute-force solution processes each query independently. For every pair `(a, b)`, we find the path between them and increment all edges on that path.

Since the graph is a tree, one way to do this is with DFS or parent climbing. The solution is correct because every pair has exactly one simple path, so visiting those edges directly matches the problem definition.

The problem is scale. A single path may contain `n - 1` edges. With `10^5` queries, the worst-case work becomes roughly:

```
10^5 × 10^5 = 10^10
```

That is several orders of magnitude too slow.

The key observation is that we do not actually need to update edges immediately. We only need the final number of paths passing through each edge.

Suppose we add `+1` at both endpoints of a query path, then subtract `2` at their LCA. If we later perform a DFS from the leaves upward, every subtree accumulates how many active paths pass through it.

Why does this work?

Imagine an edge connecting a node `u` to its parent. After aggregation, the value stored at `u` equals the number of paths that enter the subtree rooted at `u` minus the number of paths that also leave it inside the subtree. Exactly those remaining paths must cross the edge between `u` and its parent.

This transforms expensive per-path edge updates into:

1. Constant-time endpoint marking per query.
2. One DFS accumulation over the tree.

The only remaining challenge is computing LCAs efficiently. Binary lifting solves that in `O(log n)` per query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nk) | O(n) | Too slow |
| Optimal | O((n + k) log n) | O(n log n) | Accepted |

## Algorithm Walkthrough

1. Build the tree adjacency list from the input edges.

We need a structure that allows DFS traversal and ancestor preprocessing.
2. Run a DFS from an arbitrary root, usually node `1`.

During this DFS, store:

- the parent of every node
- the depth of every node
- the edge index connecting a node to its parent

These values are needed both for LCA computation and for assigning answers back to edges in input order.
3. Build the binary lifting table.

Let `up[v][j]` be the `2^j`-th ancestor of node `v`.

This allows us to move upward in logarithmic time instead of climbing one edge at a time.
4. For every query `(a, b)`, compute `lca(a, b)`.

Then apply:

- `cnt[a] += 1`
- `cnt[b] += 1`
- `cnt[lca] -= 2`

This encodes the path implicitly instead of touching every edge directly.
5. Run a second DFS from the root.

For every child subtree, recursively compute its accumulated value and add it to the current node.

If a child subtree returns value `x`, then exactly `x` paths cross the edge between that child and its parent.
6. Store the returned subtree value as the answer for the edge connecting the child to its parent.

Since each edge belongs to exactly one child-parent relationship in the rooted tree, every edge gets exactly one answer.
7. Output answers in original input order.

### Why it works

Each query adds one unit at both endpoints of its path. When subtree sums are aggregated upward, contributions cancel inside the path except along the actual route between the endpoints.

Subtracting `2` at the LCA is the crucial correction. Without it, the shared ancestor region would be counted twice. After cancellation, every edge receives exactly the number of query paths that cross from one side of that edge to the other.

For an edge between parent `p` and child `u`, the subtree sum at `u` equals the number of query endpoints inside that subtree minus the number of complete paths entirely contained there. Every remaining unmatched path must cross the edge `(p, u)`. That count is exactly the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1 << 25)

LOG = 17 + 1

def solve():
    n = int(input())

    graph = [[] for _ in range(n + 1)]

    edges = []

    for idx in range(n - 1):
        u, v = map(int, input().split())
        graph[u].append((v, idx))
        graph[v].append((u, idx))
        edges.append((u, v))

    parent = [[0] * (n + 1) for _ in range(LOG)]
    depth = [0] * (n + 1)
    edge_id = [-1] * (n + 1)

    def dfs(v, p):
        parent[0][v] = p

        for to, idx in graph[v]:
            if to == p:
                continue

            depth[to] = depth[v] + 1
            edge_id[to] = idx
            dfs(to, v)

    dfs(1, 0)

    for j in range(1, LOG):
        for v in range(1, n + 1):
            parent[j][v] = parent[j - 1][parent[j - 1][v]]

    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a

        diff = depth[a] - depth[b]

        for j in range(LOG):
            if diff & (1 << j):
                a = parent[j][a]

        if a == b:
            return a

        for j in range(LOG - 1, -1, -1):
            if parent[j][a] != parent[j][b]:
                a = parent[j][a]
                b = parent[j][b]

        return parent[0][a]

    k = int(input())

    cnt = [0] * (n + 1)

    for _ in range(k):
        a, b = map(int, input().split())

        g = lca(a, b)

        cnt[a] += 1
        cnt[b] += 1
        cnt[g] -= 2

    ans = [0] * (n - 1)

    def dfs2(v, p):
        total = cnt[v]

        for to, idx in graph[v]:
            if to == p:
                continue

            subtotal = dfs2(to, v)

            ans[idx] = subtotal
            total += subtotal

        return total

    dfs2(1, 0)

    print(*ans)

solve()
```

The first DFS roots the tree and records structural information. The `edge_id` array remembers which input edge connects a node to its parent. That mapping is necessary because answers must be printed in original input order rather than DFS order.

The binary lifting table stores ancestors at powers of two distances. The value of `LOG` only needs to satisfy `2^LOG > n`. With `n ≤ 10^5`, eighteen levels are enough.

The LCA function first equalizes depths, then lifts both nodes upward together until their parents match. This gives logarithmic complexity per query.

The path encoding step is the heart of the solution. Adding to both endpoints and subtracting twice from the LCA creates a difference-array style representation over the tree. No edges are updated directly.

The second DFS performs the accumulation. The returned value from a child subtree equals the number of paths crossing the edge connecting that subtree to its parent. That is why `ans[idx] = subtotal` is correct.

One subtle implementation detail is assigning the edge answer before adding the subtotal into the current node. The subtotal represents traffic through exactly that edge. After it merges into the parent total, that distinction disappears.

Another detail is recursion depth. A chain-shaped tree may have depth `10^5`, so the recursion limit must be increased.

## Worked Examples

### Sample 1

Input:

```
5
1 2
1 3
2 4
2 5
2
1 4
3 5
```

Tree structure:

```
    1
   / \
  2   3
 / \
4   5
```

Queries are `(1,4)` and `(3,5)`.

LCA computations:

| Query | LCA |
| --- | --- |
| 1 4 | 1 |
| 3 5 | 1 |

After endpoint updates:

| Node | cnt value |
| --- | --- |
| 1 | -2 |
| 2 | 0 |
| 3 | 1 |
| 4 | 1 |
| 5 | 1 |

Now aggregate bottom-up.

| Node Processed | Returned Sum | Edge Answer |
| --- | --- | --- |
| 4 | 1 | edge(2,4)=1 |
| 5 | 1 | edge(2,5)=1 |
| 2 | 2 | edge(1,2)=2 |
| 3 | 1 | edge(1,3)=1 |

Final output:

```
2 1 1 1
```

This trace shows how multiple paths naturally combine through subtree sums. The edge `(1,2)` belongs to both routes, so its accumulated value becomes `2`.

### Custom Example

Input:

```
4
1 2
2 3
3 4
2
1 4
2 3
```

Tree:

```
1 - 2 - 3 - 4
```

LCA computations:

| Query | LCA |
| --- | --- |
| 1 4 | 1 |
| 2 3 | 2 |

Difference updates:

| Node | cnt |
| --- | --- |
| 1 | -1 |
| 2 | -1 |
| 3 | 1 |
| 4 | 1 |

Bottom-up aggregation:

| Node Processed | Returned Sum | Edge Answer |
| --- | --- | --- |
| 4 | 1 | edge(3,4)=1 |
| 3 | 2 | edge(2,3)=2 |
| 2 | 1 | edge(1,2)=1 |

Output:

```
1 2 1
```

This example demonstrates overlapping paths on a chain. The middle edge belongs to both routes, so it accumulates count `2`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + k) log n) | DFS preprocessing is linear, each query needs one LCA computation |
| Space | O(n log n) | Binary lifting table dominates memory usage |

With `n` and `k` both up to `10^5`, this complexity easily fits the limits. Around a few million operations are performed, which is well within a 2-second limit in Python when implemented carefully.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    sys.setrecursionlimit(1 << 25)

    LOG = 18

    n = int(input())

    graph = [[] for _ in range(n + 1)]

    for idx in range(n - 1):
        u, v = map(int, input().split())
        graph[u].append((v, idx))
        graph[v].append((u, idx))

    parent = [[0] * (n + 1) for _ in range(LOG)]
    depth = [0] * (n + 1)

    def dfs(v, p):
        parent[0][v] = p

        for to, idx in graph[v]:
            if to == p:
                continue

            depth[to] = depth[v] + 1
            dfs(to, v)

    dfs(1, 0)

    for j in range(1, LOG):
        for v in range(1, n + 1):
            parent[j][v] = parent[j - 1][parent[j - 1][v]]

    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a

        diff = depth[a] - depth[b]

        for j in range(LOG):
            if diff & (1 << j):
                a = parent[j][a]

        if a == b:
            return a

        for j in range(LOG - 1, -1, -1):
            if parent[j][a] != parent[j][b]:
                a = parent[j][a]
                b = parent[j][b]

        return parent[0][a]

    k = int(input())

    cnt = [0] * (n + 1)

    for _ in range(k):
        a, b = map(int, input().split())

        g = lca(a, b)

        cnt[a] += 1
        cnt[b] += 1
        cnt[g] -= 2

    ans = [0] * (n - 1)

    def dfs2(v, p):
        total = cnt[v]

        for to, idx in graph[v]:
            if to == p:
                continue

            subtotal = dfs2(to, v)

            ans[idx] = subtotal
            total += subtotal

        return total

    dfs2(1, 0)

    return " ".join(map(str, ans))

# provided sample
assert run(
"""5
1 2
1 3
2 4
2 5
2
1 4
3 5
"""
) == "2 1 1 1", "sample 1"

# minimum tree
assert run(
"""2
1 2
1
1 2
"""
) == "1", "single edge"

# no queries
assert run(
"""3
1 2
2 3
0
"""
) == "0 0", "no paths"

# chain with overlapping paths
assert run(
"""4
1 2
2 3
3 4
2
1 4
2 3
"""
) == "1 2 1", "overlapping chain"

# same-node query
assert run(
"""3
1 2
2 3
1
2 2
"""
) == "0 0", "empty path"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single edge tree | `1` | Smallest non-trivial tree |
| No queries | `0 0` | Correct handling of empty workload |
| Overlapping chain | `1 2 1` | Shared edge accumulation |
| Same-node query | `0 0` | Empty paths must not affect edges |

## Edge Cases

Consider the case where the query starts and ends at the same node:

```
3
1 2
2 3
1
2 2
```

The LCA of `(2,2)` is `2`. The update sequence becomes:

```
cnt[2] += 1
cnt[2] += 1
cnt[2] -= 2
```

So the net effect is zero. During subtree aggregation, every subtree returns zero, and all edge answers remain zero. This correctly models that no road is traversed.

Now consider an ancestor-descendant query:

```
4
1 2
2 3
3 4
1
2 4
```

The LCA is `2`. Updates become:

```
cnt[2] += 1
cnt[4] += 1
cnt[2] -= 2
```

Net values:

```
cnt[2] = -1
cnt[4] = 1
```

Bottom-up aggregation gives:

```
edge(3,4) = 1
edge(2,3) = 1
edge(1,2) = 0
```

The path correctly excludes the edge above the ancestor.

Finally, consider a star-shaped tree:

```
5
1 2
1 3
1 4
1 5
2
2 3
4 5
```

Every query passes through node `1`. The subtree sums from all leaves become:

```
child 2 -> 1
child 3 -> 1
child 4 -> 1
child 5 -> 1
```

So every edge connected to the center gets count `1`, and because each pair uses two different spokes, the final answers are:

```
1 1 1 1
```

This confirms that overlapping traffic through the root is aggregated correctly without double counting.
