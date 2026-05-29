---
title: "CF 292D - Connected Components"
description: "We have an undirected graph representing a computer network. The vertices are computers and the edges are cables. The edges are stored in a fixed order from 1 to m."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "dp", "dsu"]
categories: ["algorithms"]
codeforces_contest: 292
codeforces_index: "D"
codeforces_contest_name: "Croc Champ 2013 - Round 1"
rating: 1900
weight: 292
solve_time_s: 107
verified: true
draft: false
---

[CF 292D - Connected Components](https://codeforces.com/problemset/problem/292/D)

**Rating:** 1900  
**Tags:** data structures, dfs and similar, dp, dsu  
**Solve time:** 1m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an undirected graph representing a computer network. The vertices are computers and the edges are cables. The edges are stored in a fixed order from `1` to `m`.

Each query removes one contiguous segment of edges, from index `l` to index `r`, and asks how many connected components remain in the graph after those edges disappear temporarily.

The graph is restored after every query, so queries are independent.

The main difficulty is that there can be up to `2 * 10^4` queries, while the graph itself has up to `10^4` edges. Rebuilding the graph from scratch for every query is expensive unless we exploit the structure of the removed interval.

The graph is small in terms of vertices, only `n <= 500`. That changes the tradeoff completely. Many graph problems become manageable when the number of vertices is tiny, even if the number of queries is large.

A straightforward approach would process every query independently. For a query `[l, r]`, we would add all edges outside that interval, then run DFS or DSU to count connected components. Each query touches `O(m)` edges, so the total complexity becomes `O(k * m)` union operations. With `m = 10^4` and `k = 2 * 10^4`, that is roughly `2 * 10^8` edge operations before even counting DFS overhead. In Python, this is too slow.

The key observation is that every query keeps exactly two edge ranges:

- edges before `l`
- edges after `r`

That means the graph for a query can be represented as:

```
prefix(l - 1) + suffix(r + 1)
```

This structure allows preprocessing.

There are several edge cases that easily break careless implementations.

Suppose all edges are removed.

```
3 2
1 2
2 3
1
1 2
```

The correct answer is `3` because every vertex becomes isolated. A buggy implementation may accidentally start the component count at `0` and only count successful unions.

Multiple edges between the same vertices also matter.

```
2 2
1 2
1 2
2
1 1
1 2
```

Removing only the first edge still leaves the graph connected because the second parallel edge remains. Removing both disconnects the graph into two components. Any solution that treats edges as unique pairs instead of indexed cables gives the wrong result.

Another common mistake is mishandling boundaries when the removed interval touches the beginning or end.

```
4 3
1 2
2 3
3 4
2
1 1
3 3
```

For query `[1,1]`, we keep edges `2` and `3`.

For query `[3,3]`, we keep edges `1` and `2`.

Off-by-one errors in prefix or suffix preprocessing often appear here.

## Approaches

The brute-force solution is conceptually simple. For every query `[l, r]`, we build a fresh DSU with `n` components. Then we iterate over all edges and add every edge whose index is outside the removed interval. Every successful union decreases the number of connected components by one.

This works because DSU correctly maintains connectivity in an undirected graph. After processing all remaining edges, the number of DSU sets equals the number of connected components.

The problem is the cost. Every query scans all `m` edges, so the total complexity is `O(k * m * α(n))`. With the maximum constraints, this reaches roughly two hundred million edge checks. Python struggles at that scale.

The structure of the query gives a way out. Every query removes one contiguous segment. Instead of rebuilding the graph from scratch, we can preprocess DSU states for every prefix and every suffix.

Define:

- `pref[i]` as the DSU after adding edges `1...i`
- `suff[i]` as the DSU after adding edges `i...m`

Then a query `[l, r]` keeps exactly:

```
edges 1...(l-1)
edges (r+1)...m
```

So we can reconstruct the answer by combining the DSU information from:

```
pref[l-1]
suff[r+1]
```

There is one complication: DSU structures are not directly mergeable. We cannot simply glue two parent arrays together.

The small vertex limit solves this. Since `n <= 500`, we can explicitly rebuild a DSU for every query by replaying component relations from the two precomputed states.

For every prefix and suffix, we store the list of edges that successfully merged two components during construction. These are exactly the edges of a spanning forest. Each list contains at most `n-1` edges.

Now every query processes at most:

```
(n - 1) + (n - 1)
```

edges instead of `m`.

That changes the complexity from roughly `2 * 10^8` operations to about `2 * 10^7`, which is fast enough in Python.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(k * m * α(n))` | `O(n)` | Too slow |
| Optimal | `O(m * n + k * n * α(n))` | `O(m * n)` | Accepted |

## Algorithm Walkthrough

1. Read all edges into an array indexed from `1` to `m`.
2. Build prefix spanning forests.

Create a fresh DSU. Process edges from left to right. Whenever an edge connects two previously separate components, store that edge inside `pref[i]`.

The stored edges are enough to reproduce the connectivity of the entire prefix because every redundant edge can be ignored.
3. Build suffix spanning forests.

Create another DSU. Process edges from right to left. Whenever an edge merges two components, store it inside `suff[i]`.

Now `suff[i]` represents a spanning forest for edges `i...m`.
4. For every query `[l, r]`, create a fresh DSU with `n` components.
5. Replay all edges from `pref[l-1]`.

These edges reconstruct the connectivity created by all edges before the removed segment.
6. Replay all edges from `suff[r+1]`.

These edges reconstruct the connectivity created by all edges after the removed segment.
7. Count how many connected components remain in the DSU and print the result.

Why it works:

A spanning forest preserves connectivity information. Any edge that connects vertices already in the same component does not change which vertices are reachable from each other.

`pref[l-1]` contains enough edges to reproduce exactly the same connected components as the entire prefix `1...(l-1)`. Similarly, `suff[r+1]` reproduces the connectivity of the suffix `(r+1)...m`.

When we replay both forests together, we reconstruct exactly the graph formed by all edges outside the removed interval. Since DSU correctly tracks connected components under edge insertions, the final component count is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.size = [1] * (n + 1)
        self.components = n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)

        if ra == rb:
            return False

        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra

        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True

def solve():
    n, m = map(int, input().split())

    edges = [None] * (m + 1)

    for i in range(1, m + 1):
        u, v = map(int, input().split())
        edges[i] = (u, v)

    pref = [[] for _ in range(m + 1)]

    dsu = DSU(n)

    for i in range(1, m + 1):
        pref[i] = pref[i - 1][:]

        u, v = edges[i]

        if dsu.union(u, v):
            pref[i].append((u, v))

    suff = [[] for _ in range(m + 2)]

    dsu = DSU(n)

    for i in range(m, 0, -1):
        suff[i] = suff[i + 1][:]

        u, v = edges[i]

        if dsu.union(u, v):
            suff[i].append((u, v))

    k = int(input())

    ans = []

    for _ in range(k):
        l, r = map(int, input().split())

        dsu = DSU(n)

        for u, v in pref[l - 1]:
            dsu.union(u, v)

        for u, v in suff[r + 1]:
            dsu.union(u, v)

        ans.append(str(dsu.components))

    print("\n".join(ans))

solve()
```

The DSU implementation keeps track of the current number of connected components directly inside the structure. Every successful union decreases this count by one.

The prefix preprocessing builds a spanning forest incrementally. `pref[i]` copies the forest from `pref[i-1]`, then possibly adds the current edge if it merges two different DSU components.

The suffix preprocessing is symmetric. `suff[i]` stores a spanning forest for edges `i...m`.

The query phase is intentionally simple. We rebuild connectivity from two compact forests instead of scanning all edges.

One subtle detail is the array sizing for `suff`. We allocate `m + 2` elements so that `suff[m + 1]` exists naturally as an empty forest. This avoids special cases when the removed interval ends at the last edge.

Another easy mistake is forgetting that the copied forests are mutable lists. Using slicing like `[:]` creates independent copies.

## Worked Examples

### Example 1

Input:

```
6 5
1 2
5 4
2 3
3 1
3 6
1
2 4
```

The query removes edges `2,3,4`.

Remaining edges:

```
1-2
3-6
```

### Prefix preprocessing

| i | Edge | Successful union | pref[i] |
| --- | --- | --- | --- |
| 1 | (1,2) | Yes | [(1,2)] |
| 2 | (5,4) | Yes | [(1,2),(5,4)] |
| 3 | (2,3) | Yes | [(1,2),(5,4),(2,3)] |
| 4 | (3,1) | No | unchanged |
| 5 | (3,6) | Yes | [(1,2),(5,4),(2,3),(3,6)] |

### Suffix preprocessing

| i | Edge | Successful union | suff[i] |
| --- | --- | --- | --- |
| 5 | (3,6) | Yes | [(3,6)] |
| 4 | (3,1) | Yes | [(3,6),(3,1)] |
| 3 | (2,3) | Yes | [(3,6),(3,1),(2,3)] |
| 2 | (5,4) | Yes | [(3,6),(3,1),(2,3),(5,4)] |
| 1 | (1,2) | No | unchanged |

For query `[2,4]`:

- use `pref[1] = [(1,2)]`
- use `suff[5] = [(3,6)]`

After replaying these edges, components are:

```
{1,2}, {3,6}, {4}, {5}
```

Answer: `4`.

This trace shows why redundant edges can be discarded safely. Edge `(3,1)` never appears in the prefix forest because it does not create a new connection.

### Example 2

Input:

```
4 3
1 2
2 3
3 4
1
1 2
```

Removing edges `1` and `2` leaves only:

```
3-4
```

### Query reconstruction

| Step | Edge added | Components |
| --- | --- | --- |
| Initial | none | 4 |
| Add (3,4) | merge | 3 |

Final answer: `3`.

This example exercises the boundary case where the removed interval starts at the first edge. The algorithm correctly uses `pref[0]`, which is an empty forest.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(m * n + k * n * α(n))` | Every prefix and suffix forest contains at most `n-1` edges |
| Space | `O(m * n)` | We store forests for all prefixes and suffixes |

Since `n <= 500`, each stored forest is tiny. Query processing touches at most about `1000` edges, even though the original graph may contain `10000` edges. The solution comfortably fits within the limits.

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
            self.parent = list(range(n + 1))
            self.size = [1] * (n + 1)
            self.components = n

        def find(self, x):
            while self.parent[x] != x:
                self.parent[x] = self.parent[self.parent[x]]
                x = self.parent[x]
            return x

        def union(self, a, b):
            ra = self.find(a)
            rb = self.find(b)

            if ra == rb:
                return False

            if self.size[ra] < self.size[rb]:
                ra, rb = rb, ra

            self.parent[rb] = ra
            self.size[ra] += self.size[rb]
            self.components -= 1
            return True

    n, m = map(int, input().split())

    edges = [None] * (m + 1)

    for i in range(1, m + 1):
        edges[i] = tuple(map(int, input().split()))

    pref = [[] for _ in range(m + 1)]

    dsu = DSU(n)

    for i in range(1, m + 1):
        pref[i] = pref[i - 1][:]

        u, v = edges[i]

        if dsu.union(u, v):
            pref[i].append((u, v))

    suff = [[] for _ in range(m + 2)]

    dsu = DSU(n)

    for i in range(m, 0, -1):
        suff[i] = suff[i + 1][:]

        u, v = edges[i]

        if dsu.union(u, v):
            suff[i].append((u, v))

    k = int(input())

    ans = []

    for _ in range(k):
        l, r = map(int, input().split())

        dsu = DSU(n)

        for u, v in pref[l - 1]:
            dsu.union(u, v)

        for u, v in suff[r + 1]:
            dsu.union(u, v)

        ans.append(str(dsu.components))

    return "\n".join(ans)

# provided sample
assert run(
"""6 5
1 2
5 4
2 3
3 1
3 6
6
1 3
2 5
1 5
5 5
2 4
3 3
"""
) == """4
5
6
3
4
2""", "sample 1"

# minimum graph
assert run(
"""2 1
1 2
1
1 1
"""
) == """2""", "minimum case"

# parallel edges
assert run(
"""2 2
1 2
1 2
2
1 1
1 2
"""
) == """1
2""", "parallel edges"

# remove middle edge
assert run(
"""4 3
1 2
2 3
3 4
1
2 2
"""
) == """2""", "middle edge removal"

# remove all edges
assert run(
"""5 4
1 2
2 3
3 4
4 5
1
1 4
"""
) == """5""", "all edges removed"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum graph | 2 | Correct handling of fully disconnected result |
| Parallel edges | 1, 2 | Multiple identical edges must be treated separately |
| Remove middle edge | 2 | Correct reconstruction from prefix and suffix |
| Remove all edges | 5 | Empty remaining graph |

## Edge Cases

Consider the case where every edge is removed.

```
3 2
1 2
2 3
1
1 2
```

The query removes the entire edge set. The algorithm uses:

```
pref[0]
suff[3]
```

Both forests are empty. The DSU starts with `3` components and no unions occur, so the answer remains `3`. This correctly treats isolated vertices as separate connected components.

Now consider parallel edges.

```
2 2
1 2
1 2
2
1 1
1 2
```

For query `[1,1]`, edge `2` still exists, so replaying the suffix forest performs one union and the answer becomes `1`.

For query `[1,2]`, no edges remain. Both forests are empty, so the answer becomes `2`.

The algorithm works because it treats edges by index, not by endpoint pair.

Finally, consider boundary intervals.

```
4 3
1 2
2 3
3 4
2
1 1
3 3
```

For `[1,1]`, the algorithm combines:

```
pref[0]
suff[2]
```

which reconstructs edges `2` and `3`.

For `[3,3]`, it combines:

```
pref[2]
suff[4]
```

where `suff[4]` is empty.

The extra slot in the suffix array avoids special-case handling and prevents out-of-bounds errors.
