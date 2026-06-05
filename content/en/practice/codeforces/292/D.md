---
title: "CF 292D - Connected Components"
description: "We have an undirected graph representing a computer network. The vertices are computers and the edges are cables. The cables are numbered from 1 to m in the order they appear in the input."
date: "2026-06-05T17:13:14+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "dp", "dsu"]
categories: ["algorithms"]
codeforces_contest: 292
codeforces_index: "D"
codeforces_contest_name: "Croc Champ 2013 - Round 1"
rating: 1900
weight: 292
solve_time_s: 131
verified: true
draft: false
---

[CF 292D - Connected Components](https://codeforces.com/problemset/problem/292/D)

**Rating:** 1900  
**Tags:** data structures, dfs and similar, dp, dsu  
**Solve time:** 2m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an undirected graph representing a computer network. The vertices are computers and the edges are cables. The cables are numbered from 1 to `m` in the order they appear in the input.

Each query removes a contiguous block of edges, from index `l` to index `r`, and asks how many connected components remain in the graph while those edges are temporarily disconnected. After answering, the graph returns to its original state before the next query.

The graph itself is quite small in terms of vertices, only up to 500 nodes. The challenge comes from the number of edges and queries. There can be up to 10,000 edges and 20,000 queries. Any solution that rebuilds the graph and performs a full traversal for every query will be far too expensive.

A useful observation is that every query keeps exactly two edge ranges:

- edges before `l`
- edges after `r`

The removed interval is always contiguous. This structure is what makes the problem tractable.

There are several subtle situations that can easily break an incorrect solution.

Consider parallel edges:

```
2 2
1 2
1 2
1
1 1
```

Removing only the first edge still leaves the second edge, so the graph remains connected and the answer is `1`. A solution that only tracks whether an edge exists between two vertices would incorrectly return `2`.

Another important case is removing all edges:

```
3 2
1 2
2 3
1
1 2
```

The graph becomes three isolated vertices, so the answer is `3`. Any approach that assumes at least one remaining edge would fail here.

A third case is when the graph is already disconnected:

```
4 1
1 2
1
1 1
```

After removing the only edge, all four vertices are isolated, so the answer is `4`. The number of components is not related to the original graph's connectivity.

The constraints strongly suggest that we need something around a few million operations. With `m = 10^4` and `k = 2·10^4`, an `O(m)` or `O(m log n)` answer per query would require hundreds of millions of operations and would not fit comfortably in the time limit.

## Approaches

The most direct solution is to process each query independently.

For a query `[l, r]`, build a graph containing every edge except those in that interval, then run DFS or BFS to count connected components. This is obviously correct because it exactly simulates the experiment described in the statement.

The problem is the cost. A query may require scanning all `m` edges and then traversing the graph. The complexity becomes roughly `O(k · (m + n))`.

With the maximum limits:

```
k = 20000
m = 10000
```

we obtain roughly 200 million edge operations before even accounting for graph traversal overhead. This is too slow.

The key observation is that the graph has only 500 vertices.

Whenever we only care about connected components, a DSU is enough. A DSU state is completely determined by the set of edges already added. Furthermore, each query keeps two disjoint edge segments:

```
[1, l-1]
[r+1, m]
```

This suggests precomputing DSU information for prefixes and suffixes.

For every prefix of edges, we store the sequence of successful unions performed while building that prefix. Similarly, for every suffix, we store the successful unions performed while building that suffix from the end.

Then, for a query `[l, r]`, we start with an empty DSU and replay:

- all unions from prefix `l-1`
- all unions from suffix `r+1`

Since there are only 500 vertices, a DSU can perform at most `n-1 ≤ 499` successful merges. Thus each stored prefix or suffix contains at most 499 union operations.

Instead of processing up to 10,000 edges per query, we process at most about 1000 stored merges per query.

That reduction is enough to pass comfortably.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k(m+n)) | O(m+n) | Too slow |
| Optimal | O(mn + kn) | O(mn) | Accepted |

## Algorithm Walkthrough

1. Read all edges and convert them to 0-based indexing internally.
2. Build prefix information.

Create a DSU and add edges from left to right. Whenever an edge joins two previously separate components, store that pair in `pref[i]`, where `i` represents the first `i` edges.

Only successful unions are stored because failed unions never affect future connectivity.
3. Build suffix information.

Create another DSU and add edges from right to left. Whenever an edge joins two components, store that pair in `suf[i]`, where `i` represents edges from `i` through `m`.
4. For each query `[l, r]`, create a fresh DSU containing `n` isolated vertices.
5. Replay every stored merge from `pref[l-1]`.

These merges represent exactly the connectivity contributed by all edges before the removed interval.
6. Replay every stored merge from `suf[r+1]`.

These merges represent exactly the connectivity contributed by all edges after the removed interval.
7. The DSU's component counter now equals the number of connected components after removing edges `l...r`.
8. Output that counter.

### Why it works

Consider any query `[l, r]`.

The remaining graph consists of two edge sets:

```
Eleft  = edges 1 ... l-1
Eright = edges r+1 ... m
```

The prefix preprocessing stores a spanning forest of `Eleft`. The suffix preprocessing stores a spanning forest of `Eright`.

A spanning forest preserves connected components exactly. Any edge that does not perform a union connects vertices already connected through previously chosen edges and is irrelevant to component structure.

When we replay all successful unions from both forests into a fresh DSU, we reconstruct exactly the same connected components that would be produced by using all remaining edges. Hence the DSU's component count is the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

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
        self.components -= 1
        return True

def solve():
    n, m = map(int, input().split())

    edges = []
    for _ in range(m):
        u, v = map(int, input().split())
        edges.append((u - 1, v - 1))

    pref = [[] for _ in range(m + 1)]

    dsu = DSU(n)
    pref[0] = []

    for i in range(1, m + 1):
        pref[i] = pref[i - 1][:]

        u, v = edges[i - 1]
        if dsu.union(u, v):
            pref[i].append((u, v))

    suf = [[] for _ in range(m + 2)]

    dsu = DSU(n)

    for i in range(m, 0, -1):
        suf[i] = suf[i + 1][:]

        u, v = edges[i - 1]
        if dsu.union(u, v):
            suf[i].append((u, v))

    k = int(input())
    ans = []

    for _ in range(k):
        l, r = map(int, input().split())

        dsu = DSU(n)

        for u, v in pref[l - 1]:
            dsu.union(u, v)

        for u, v in suf[r + 1]:
            dsu.union(u, v)

        ans.append(str(dsu.components))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The prefix construction maintains a DSU containing the first `i` edges. Whenever an edge actually merges two components, that merge is appended to the stored forest. Since at most `n-1` successful unions can occur, every stored list remains small.

The suffix construction is symmetric. `suf[i]` stores a spanning forest for edges `i...m`.

For each query we start from an empty DSU. Replaying the prefix forest and suffix forest reconstructs the connectivity of all surviving edges. The component counter maintained by the DSU directly gives the answer.

The most common implementation mistake is indexing. The input uses 1-based edge numbering. `pref[i]` corresponds to the first `i` edges, so a query `[l, r]` uses `pref[l-1]`. Likewise, the first surviving edge after the removed interval is `r+1`, so we use `suf[r+1]`.

## Worked Examples

### Sample 1

Input:

```
6 5
1 2
5 4
2 3
3 1
3 6
1
1 3
```

Query removes edges 1 through 3.

Remaining edges are:

```
3-1
3-6
```

| Step | Action | Components |
| --- | --- | --- |
| Start | Six isolated vertices | 6 |
| Add 3-1 | Merge | 5 |
| Add 3-6 | Merge | 4 |

Answer:

```
4
```

This demonstrates that only the edges outside the removed interval matter, and the DSU component count immediately gives the result.

### Custom Example

```
4 3
1 2
2 3
3 4
1
2 2
```

Edge 2 is removed.

Remaining edges:

```
1-2
3-4
```

| Step | Action | Components |
| --- | --- | --- |
| Start | Four isolated vertices | 4 |
| Add 1-2 | Merge | 3 |
| Add 3-4 | Merge | 2 |

Answer:

```
2
```

This example shows how the graph can split into multiple large components after removing a middle edge.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(mn + kn) | Each prefix and suffix forest contains at most `n-1` merges |
| Space | O(mn) | We store up to `n-1` merges for each prefix and suffix |

Since `n ≤ 500`, every stored forest has size at most 499. The preprocessing performs roughly `m·n` work, around five million operations at worst. Each query replays at most about one thousand merges, yielding roughly ten million more operations. This comfortably fits within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    class DSU:
        def __init__(self, n):
            self.parent = list(range(n))
            self.size = [1] * n
            self.components = n

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
            self.components -= 1
            return True

    input = sys.stdin.readline

    n, m = map(int, input().split())
    edges = []

    for _ in range(m):
        u, v = map(int, input().split())
        edges.append((u - 1, v - 1))

    pref = [[] for _ in range(m + 1)]
    dsu = DSU(n)

    for i in range(1, m + 1):
        pref[i] = pref[i - 1][:]
        u, v = edges[i - 1]
        if dsu.union(u, v):
            pref[i].append((u, v))

    suf = [[] for _ in range(m + 2)]
    dsu = DSU(n)

    for i in range(m, 0, -1):
        suf[i] = suf[i + 1][:]
        u, v = edges[i - 1]
        if dsu.union(u, v):
            suf[i].append((u, v))

    k = int(input())
    out = []

    for _ in range(k):
        l, r = map(int, input().split())

        dsu = DSU(n)

        for u, v in pref[l - 1]:
            dsu.union(u, v)

        for u, v in suf[r + 1]:
            dsu.union(u, v)

        out.append(str(dsu.components))

    return "\n".join(out)

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

assert run(
"""2 1
1 2
1
1 1
"""
) == "2", "minimum graph"

assert run(
"""3 2
1 2
2 3
1
1 2
"""
) == "3", "remove all edges"

assert run(
"""2 2
1 2
1 2
1
1 1
"""
) == "1", "parallel edges"

assert run(
"""4 3
1 2
2 3
3 4
1
2 2
"""
) == "2", "middle interval removal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single edge graph | 2 | Smallest meaningful instance |
| Remove all edges | 3 | Empty remaining graph |
| Parallel edges | 1 | Multiple identical edges |
| Path with middle edge removed | 2 | Correct interval handling |
| Official sample | Given output | Full integration test |

## Edge Cases

Consider parallel edges:

```
2 2
1 2
1 2
1
1 1
```

The first edge is removed, but the second remains. During preprocessing, one of the parallel edges appears in the spanning forest and the other does not. When the query replays the suffix forest, the surviving edge still connects the two vertices, producing one component. The answer is:

```
1
```

Consider removing every edge:

```
3 2
1 2
2 3
1
1 2
```

The query uses `pref[0]` and `suf[3]`, both empty. The fresh DSU never performs any merge and keeps three components. The answer is:

```
3
```

Consider a graph that starts disconnected:

```
4 1
1 2
1
1 1
```

Again, both replayed forests are empty. The DSU starts with four components and remains unchanged, producing:

```
4
```

These examples illustrate the central invariant: replaying the prefix and suffix spanning forests reconstructs exactly the connectivity of all edges that remain after the queried interval is removed.
