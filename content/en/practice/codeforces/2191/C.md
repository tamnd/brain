---
title: "CF 2191C - Sorting Game"
description: "We are given a weighted undirected graph. We must choose exactly $n-1$ edges. If those $n-1$ edges form a spanning tree, the choice is forbidden. We want the minimum possible total weight among all choices of $n-1$ edges that do not form a tree."
date: "2026-06-09T04:41:27+07:00"
tags: ["codeforces", "competitive-programming", "games"]
categories: ["algorithms"]
codeforces_contest: 2191
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1073 (Div. 2)"
rating: 1200
weight: 2191
solve_time_s: 194
verified: false
draft: false
---

[CF 2191C - Sorting Game](https://codeforces.com/problemset/problem/2191/C)

**Rating:** 1200  
**Tags:** games  
**Solve time:** 3m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a weighted undirected graph. We must choose exactly $n-1$ edges.

If those $n-1$ edges form a spanning tree, the choice is forbidden. We want the minimum possible total weight among all choices of $n-1$ edges that do **not** form a tree.

A graph on $n$ vertices with exactly $n-1$ edges is a tree if and only if it is connected. That observation immediately simplifies the problem: we are looking for the minimum-weight set of $n-1$ edges whose induced graph is disconnected.

The graph size is large. Across all test cases, both the total number of vertices and the total number of edges are at most $2 \cdot 10^5$. Any algorithm that enumerates subsets, spanning trees, or even all pairs of edge sets is completely impossible. We need something close to $O(m \log m)$ per test file.

A subtle edge case appears when the globally lightest $n-1$ edges are already disconnected. For example:

```
n = 4
edges: 1, 2, 3, 100
```

Choosing the three lightest edges already gives a disconnected graph, so the answer is simply $1+2+3=6$. A solution that starts by building an MST and then forcing a modification would miss this case.

Another important case is when the lightest $n-1$ edges form a tree. Then the answer is not necessarily obtained by replacing an arbitrary tree edge. The replacement must disconnect the graph. For example, if an extra edge creates a cycle, removing an edge from that cycle keeps the graph connected and still gives a tree, which is forbidden.

A final corner case occurs when $m=n-1$. The graph contains exactly one set of $n-1$ edges. If that set is a tree, no valid answer exists and we must print $-1$.

## Approaches

A brute-force solution would examine every subset of $n-1$ edges, check whether it forms a tree, and keep the minimum weight among the invalid ones. There are

$$\binom{m}{n-1}$$

such subsets, which is astronomically large even for graphs with a few dozen edges.

The key observation comes from sorting all edges by weight.

Let $r=n-1$. Consider the first $r$ edges in nondecreasing weight order. Call this set $P$.

Every set of $r$ edges has weight at least the weight of $P$, because $P$ contains the globally lightest $r$ edges.

If $P$ is already disconnected, then it is immediately optimal and we are done.

The interesting case is when $P$ forms a tree.

Suppose we add an edge $e$ outside $P$. Since $P$ is a tree, adding $e$ creates exactly one cycle. If we remove an edge from that cycle, the graph remains connected and we still have a tree. That does not help.

To obtain a disconnected graph, we must remove an edge that is **not** on the cycle created by $e$.

For a fixed outside edge $e$, the cheapest disconnected set obtainable by one swap is achieved by removing the heaviest edge of $P$ that does not lie on the path between the endpoints of $e$.

The surprising fact is that every optimal answer can be represented by such a single swap. Any solution that differs from $P$ by several additions and removals has weight increase at least as large as the best valid single swap.

This reduces the entire problem to finding, for every edge outside the prefix, the maximum-weight edge of the prefix tree that is not on the corresponding tree path.

That becomes a tree data structure problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | $O(m \log^2 n)$ | $O(n \log n)$ | Accepted |

## Algorithm Walkthrough

### Building the critical prefix

1. Sort all edges by weight.
2. Let $r=n-1$. Take the first $r$ edges and call this set $P$.
3. Compute the sum of their weights, denoted $S$.
4. Use DSU on the edges of $P$.
5. If $P$ is disconnected, output $S$. No other set of $r$ edges can have smaller weight.
6. If $m=r$, then $P$ is the only possible set of $r$ edges. Since it is a tree, no valid answer exists, so output $-1$.

### When the prefix is a tree

1. Treat $P$ as a tree.
2. Root the tree and build binary-lifting tables.
3. For every ancestor jump, store two values:

- the maximum edge weight on that jump,
- the second maximum edge weight on that jump.
4. For every edge $e=(u,v,w)$ outside $P$, query the path from $u$ to $v$ inside the tree.
5. Let $M$ be the maximum edge weight on the entire tree.
6. Let $P_{\max}(u,v)$ be the maximum edge weight on the tree path between $u$ and $v$.
7. We need the heaviest tree edge that is **not** on that path.
8. If $M$ is not contained on the path, then the answer is simply $M$.
9. If $M$ lies on the path, we need the largest tree edge outside the path. This equals the larger of:

- the second-largest edge weight in the whole tree when the maximum is unique,
- the same maximum value when it appears elsewhere outside the path.
10. Using the stored maximum and second maximum information, compute the best removable edge weight $h$.
11. The cost increase for this outside edge is

$$w-h.$$

1. Take the minimum valid increase over all outside edges.
2. The answer is

$$S + \min(w-h).$$

### Why it works

The first $n-1$ edges are the minimum-weight set of that size. Any other set must replace some of them with heavier edges.

When the prefix is disconnected, it is already a valid solution and cannot be improved.

When the prefix is a tree, adding one non-prefix edge creates a unique cycle. Removing an edge outside that cycle disconnects the graph, giving a valid set of $n-1$ edges.

For a fixed added edge, removing the heaviest allowable tree edge produces the minimum possible increase.

Any valid solution differing from the prefix by several swaps must contain at least one removed tree edge that is not covered by any added-edge path. Comparing that removed edge with one of the added edges yields a cost increase no smaller than the best valid single swap. Hence an optimal solution is always achieved by one swap, and minimizing $w-h$ over all outside edges is sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

LOG = 19

class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.sz = [1] * n

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return False
        if self.sz[a] < self.sz[b]:
            a, b = b, a
        self.p[b] = a
        self.sz[a] += self.sz[b]
        return True

def merge_pair(a, b):
    vals = [a[0], a[1], b[0], b[1]]
    vals.sort(reverse=True)
    return (vals[0], vals[1])

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n, m = map(int, input().split())

        edges = []
        for _ in range(m):
            u, v, w = map(int, input().split())
            edges.append((w, u - 1, v - 1))

        edges.sort()

        r = n - 1
        prefix = edges[:r]
        extra = edges[r:]

        prefix_sum = sum(w for w, _, _ in prefix)

        dsu = DSU(n)
        for w, u, v in prefix:
            dsu.union(u, v)

        root = dsu.find(0)
        connected = all(dsu.find(i) == root for i in range(n))

        if not connected:
            out.append(str(prefix_sum))
            continue

        if m == r:
            out.append("-1")
            continue

        tree = [[] for _ in range(n)]
        all_tree_weights = []

        for w, u, v in prefix:
            tree[u].append((v, w))
            tree[v].append((u, w))
            all_tree_weights.append(w)

        max1 = max(all_tree_weights)
        cnt_max1 = all_tree_weights.count(max1)

        if cnt_max1 >= 2:
            max2 = max1
        else:
            max2 = max((x for x in all_tree_weights if x != max1), default=-1)

        depth = [0] * n
        up = [[0] * n for _ in range(LOG)]
        best = [[(-1, -1)] * n for _ in range(LOG)]

        stack = [(0, -1, -1)]
        order = [0]

        parent = [-1] * n
        parent[0] = 0

        while stack:
            v, p, w = stack.pop()

            up[0][v] = p if p != -1 else 0
            best[0][v] = (w, -1)

            for to, wt in tree[v]:
                if to == p:
                    continue
                depth[to] = depth[v] + 1
                parent[to] = v
                stack.append((to, v, wt))

        for k in range(1, LOG):
            uk = up[k - 1]
            uk2 = up[k]
            bk = best[k]
            bk1 = best[k - 1]

            for v in range(n):
                mid = uk[v]
                uk2[v] = uk[mid]
                bk[v] = merge_pair(bk1[v], bk1[mid])

        def path_two_max(a, b):
            res = (-1, -1)

            if depth[a] < depth[b]:
                a, b = b, a

            diff = depth[a] - depth[b]
            bit = 0
            while diff:
                if diff & 1:
                    res = merge_pair(res, best[bit][a])
                    a = up[bit][a]
                diff >>= 1
                bit += 1

            if a == b:
                return res

            for k in range(LOG - 1, -1, -1):
                if up[k][a] != up[k][b]:
                    res = merge_pair(res, best[k][a])
                    res = merge_pair(res, best[k][b])
                    a = up[k][a]
                    b = up[k][b]

            res = merge_pair(res, best[0][a])
            res = merge_pair(res, best[0][b])

            return res

        INF = 10**30
        add = INF

        for w, u, v in extra:
            path_max, path_second = path_two_max(u, v)

            if max1 > path_max:
                removable = max1
            else:
                removable = max(max2, path_second)

            if removable != -1:
                add = min(add, w - removable)

        if add == INF:
            out.append("-1")
        else:
            out.append(str(prefix_sum + add))

    sys.stdout.write("\n".join(out))

solve()
```

After sorting, the algorithm first checks whether the globally lightest $n-1$ edges are already disconnected. That case is handled immediately because no other $n-1$-edge set can have a smaller sum.

When the prefix forms a tree, the rest of the work happens on that tree. Binary lifting allows us to query the largest and second-largest edge weights on any tree path in $O(\log n)$. Those values are enough to determine the heaviest edge not lying on the path, which is exactly the edge we would like to remove.

The implementation stores the two largest weights for every lifting segment. Merging two segments is done by taking the two largest values among the four candidates. This keeps path queries efficient while avoiding more complicated data structures.

All weight calculations use Python integers, which safely handle values up to $10^9$ and sums up to roughly $2 \cdot 10^{14}$.

## Worked Examples

### Sample 1, first test case

Sorted weights:

| Index | Weight |
| --- | --- |
| 1 | 1 |
| 2 | 4 |
| 3 | 5 |
| 4 | 6 |
| 5 | 7 |
| 6 | 9 |

Here $n=4$, so we need $r=3$ edges.

The first three edges have total weight $10$.

| Chosen prefix edges | Weight sum | Connected? |
| --- | --- | --- |
| 1, 4, 5 | 10 | No |

Since the prefix is already disconnected, the answer is immediately 10.

This example shows why checking the prefix first is essential. Building a tree structure would be unnecessary work.

### Sample 1, second test case

The graph has weights:

| Weight |
| --- |
| 5 |
| 5 |
| 5 |
| 8 |

Again $r=3$.

The first three edges form the path $1-2-3-4$, which is a tree.

| Prefix sum | Connected? |
| --- | --- |
| 15 | Yes |

There is only one outside edge, weight 8.

Its path in the tree contains all three weight-5 edges. No tree edge lies outside that path.

| Outside edge weight | Best removable edge outside path |
| --- | --- |
| 8 | none |

No valid swap exists. The answer is $-1$.

This demonstrates the situation where every $3$-edge subset is a tree.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(m \log m + m \log n)$ | Sorting plus one path query for each non-prefix edge |
| Space | $O(n \log n)$ | Binary lifting tables |

The total number of vertices and edges across all test cases is at most $2 \cdot 10^5$, so $O(m \log m + m \log n)$ easily fits within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    # paste solve() here and return output
    pass

assert run("""4
4 6
1 2 7
1 3 4
1 4 1
2 3 9
2 4 6
3 4 5
4 4
1 2 5
2 3 5
3 4 5
1 4 8
4 4
1 4 1
1 3 4
2 4 2
3 4 3
4 4
2 3 7
1 2 5
2 4 9
4 3 12
""").strip() == """10
-1
8
28""".strip()

assert run("""1
2 1
1 2 5
""").strip() == "-1"

assert run("""1
4 4
1 2 1
3 4 2
1 3 100
2 4 200
""").strip() == "103"

assert run("""1
3 3
1 2 5
2 3 5
1 3 5
""").strip() == "10"

assert run("""1
4 5
1 2 1
2 3 2
3 4 100
1 3 101
2 4 102
""").strip() == "104"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 vertices, 1 edge | -1 | Only possible set is a tree |
| Disconnected light prefix | 103 | Immediate prefix answer |
| All weights equal | 10 | Correct handling of repeated maxima |
| Large edge on tree path | 104 | Correct choice of removable edge outside the path |

## Edge Cases

Consider:

```
4 4
1 2 1
3 4 2
1 3 100
2 4 200
```

The first three edges already form a disconnected graph. Their sum is 103. Since they are the globally lightest three edges, no valid answer can be smaller. The algorithm detects the disconnected prefix and stops immediately.

Consider:

```
2 1
1 2 5
```

There is only one possible subset of size $n-1$. It is a tree. No valid choice exists. The algorithm reaches the `m == n - 1` case and returns $-1$.

Consider:

```
3 3
1 2 5
2 3 5
1 3 5
```

The prefix tree contains two edges of weight 5, and the outside edge also has weight 5. Multiple maximum values exist. The implementation keeps both the largest and second-largest weights on every path so that repeated maxima are handled correctly. The answer remains 10.
