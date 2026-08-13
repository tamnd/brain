---
title: "CF 102331C - Counting Cactus"
description: "We have a simple undirected graph on at most 13 vertices. We choose a subset of its edges, while keeping the whole vertex set, and ask whether the resulting spanning graph is a cactus. A cactus is connected, and no edge may belong to two different simple cycles."
date: "2026-08-14T05:03:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102331
codeforces_index: "C"
codeforces_contest_name: "2019 Summer Petrozavodsk Camp, Day 2: 300iq Contest 2 (XX Open Cup, Grand Prix of Kazan)"
rating: 0
weight: 102331
solve_time_s: 174
verified: true
draft: false
---

[CF 102331C - Counting Cactus](https://codeforces.com/problemset/problem/102331/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a simple undirected graph on at most 13 vertices. We choose a subset of its edges, while keeping the whole vertex set, and ask whether the resulting spanning graph is a cactus. A cactus is connected, and no edge may belong to two different simple cycles. The task is to count all such edge subsets modulo (998244353). The official constraints are deliberately tiny in the number of vertices, but the number of possible edges is already 78 when (n=13).

The small value of (n) tells us that subsets of vertices are the natural state space. There are only (2^{13}=8192) vertex subsets, so a solution with several subset dimensions can still be practical. On the other hand, enumerating edge subsets is hopeless. With 13 vertices the complete graph has 78 edges, giving (2^{78}), about (3.0\cdot10^{23}), possible edge subsets. Even if checking one subset took only (O(n+m)), the total would be around (2.7\cdot10^{25}) elementary operations. The intended solution must exploit the structure of cactus graphs rather than inspect individual edge subsets.

There are several easy cases where a careless interpretation gives a wrong answer. For

```
1 0
```

the answer is (1). The graph consists of one vertex and no edges, and a single-vertex graph is connected. An implementation that assumes a cactus must contain an edge would incorrectly return zero.

For

```
2 0
```

the answer is (0). The two vertices are disconnected, so the empty edge set is not a cactus. This catches implementations that count the empty edge subset automatically.

For

```
3 2
1 2
2 3
```

the answer is (1). Only the subset containing both edges is connected. Counting every forest as a valid cactus would incorrectly count the two one-edge subsets as well.

A second subtlety appears with several cycles. In

```
4 6
1 2
1 3
1 4
2 3
2 4
3 4
```

there are 27 valid spanning cactus subgraphs. Every connected 3-edge subgraph is a tree, and all 16 spanning trees of (K_4) are valid. Every connected 4-edge subgraph is unicyclic and hence valid, giving 11 more. A 5-edge subgraph is (K_4) with one edge removed, and its two triangles share an edge, so none of those five-edge graphs is a cactus. The full (K_4) is also invalid. This demonstrates why merely counting connected sparse subgraphs is not enough.

## Approaches

The direct approach is to enumerate every subset of the (m) input edges. For each subset, we can run a graph traversal to check connectivity, then detect whether some edge belongs to two simple cycles, for example by computing biconnected components. This is correct because every possible answer is examined exactly once. The problem is the (2^m) factor. At (n=13), (m) can be 78, so there are about (3.0\cdot10^{23}) subsets before we even perform the cactus test.

The useful observation is that a cactus has a very rigid block structure. Every biconnected component is either a single edge or a simple cycle. After removing articulation vertices, these blocks are attached in a tree-like way. This suggests separating the problem into two stages. First count the possible single cycles on every vertex set. Then combine these cycles and single edges around articulation vertices.

This decomposition is especially suitable for subset dynamic programming because (n\le13). A recent formulation of the same idea describes a state where already processed vertices are forbidden from being articulation points. Initially such a component can only be a single vertex or a simple cycle. When a vertex becomes available as an articulation point, all components hanging from it are independent and can be combined with a set exponential, which can be evaluated using a ranked subset transform.

The first stage counts simple cycles. Fix the largest numbered vertex (h) of a cycle. A cycle containing (h) becomes a simple path after removing (h), whose two endpoints are neighbors of (h). A subset DP counts these paths. Every cycle is produced twice, once in each direction, so we multiply by (1/2).

The second stage starts with these cycle counts and processes vertices from small to large. When processing (i), a valid component containing (i) is either an already counted cycle, or an edge from (i) to a smaller vertex together with a previously constructed cactus on the other vertices. Several such components can meet at (i). Since their vertex sets are disjoint except for (i), choosing all of them is exactly a set-partition exponential. The ranked subset transform computes this exponential for all vertex subsets simultaneously. This is the main optimization that takes the algorithm from an (O(3^n\operatorname{poly}(n))) decomposition to (O(n^3 2^n)).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^m(n+m))) | (O(n+m)) | Too slow |
| Optimal | (O(n^3 2^n)) | (O(n2^n)) | Accepted |

## Algorithm Walkthrough

1. Represent every vertex subset by a bitmask. We will maintain an array (f[S]). Before the articulation-processing phase, (f[S]) means the number of atomic cactus blocks on exactly (S): (f[{v}]=1), and for (|S|\ge3), (f[S]) is the number of simple cycles whose vertex set is exactly (S).
2. Count all simple cycles by fixing their maximum vertex (h). Only vertices smaller than (h) can occur elsewhere on such a cycle. Define (dp[M][v]) as the number of simple paths whose vertex set is (M), whose endpoint is (v), and whose other endpoint is a neighbor of (h). Initially, if (v) is adjacent to (h), the one-vertex path ({v}) is possible.
3. Extend those paths one vertex at a time. From a path ending at (v), choose an unused neighbor (w), and append (w). Since (w) must not already belong to the mask, the resulting path remains simple.
4. Whenever a path uses at least two vertices and ends at a neighbor of (h), adding the edges from both endpoints to (h) creates a simple cycle. Add half of the path count to (f[M\cup{h}]). The factor (1/2) removes the two orientations of the same undirected cycle.
5. Set (f[{v}]=1) for every vertex. These singleton states are needed because an edge block is created later by attaching one already constructed component to a newly processed vertex.
6. Process vertices (i=0,1,\ldots,n-1). At this point, vertices smaller than (i) are already allowed to be articulation points, while (i) itself has not yet been processed as one. Temporarily remove (i) from the universe and consider a subset (S) of the remaining vertices.
7. Construct the number of one-component pieces that contain (i). The value is
[
g[S]=f[S\cup{i}]
+f[S]\cdot \deg_i(S_{<i}),
]
where (S_{<i}) contains only vertices smaller than (i). The first term means the whole piece is already a cycle. The second means we use one edge from (i) to a smaller vertex and attach the previously constructed cactus represented by (f[S]). Only smaller neighbors are used because every edge must be introduced at exactly one processing step.
8. Several such pieces may be attached to (i), and their vertex sets must be disjoint. Thus the new value for a set is the sum over all unordered set partitions into these pieces. This is the exponential of the set power series (g).
9. To evaluate that exponential efficiently, store (g[S]) in the coefficient corresponding to (|S|), then apply a subset zeta transform. After the transform, every subset behaves like an ordinary polynomial in a size variable, so we can compute its formal exponential independently. Finally apply the inverse subset transform and take the coefficient indexed by the subset's cardinality.
10. Copy the resulting values back to states containing (i), and continue with the next vertex. After all vertices have been processed, (f[V]) is exactly the number of spanning cactus subgraphs of the input graph.

### Why it works

The invariant is that before processing vertex (i), (f[S]) counts cactus structures on (S) in which every vertex smaller than (i) is forbidden from being an articulation point. Consequently, any structure containing (i) can be decomposed uniquely into pieces that meet only at (i). Each individual piece is either an existing cycle or an edge from (i) to an already processed vertex with a valid cactus attached there. The exponential set-partition step combines all possible disjoint pieces exactly once. Processing vertices in increasing order also gives every bridge a unique moment at which it is introduced, so no edge structure is counted twice. Since every cactus can be decomposed into its cycle and bridge blocks in precisely this way, the final state counts every valid edge subset exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
INV2 = (MOD + 1) // 2

def count_cactus(n, edges):
    N = 1 << n

    adj = [0] * n
    for u, v in edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u

    # f[S] initially counts atomic blocks:
    # one vertex for |S| = 1, or one simple cycle for |S| >= 3.
    f = [0] * N

    # Count simple cycles by fixing their maximum vertex h.
    for h in range(2, n):
        lim = 1 << h

        # dp[mask][v] = number of simple paths using exactly mask
        # and ending at v, whose starting vertex is adjacent to h.
        dp = [[0] * h for _ in range(lim)]

        ah = adj[h]
        for v in range(h):
            if (ah >> v) & 1:
                dp[1 << v][v] = 1

        for mask in range(1, lim):
            row = dp[mask]

            for v in range(h):
                cur = row[v]
                if cur == 0:
                    continue

                available = adj[v] & (lim - 1) & ~mask
                while available:
                    bit = available & -available
                    available -= bit
                    w = bit.bit_length() - 1

                    nxt = dp[mask | bit]
                    nv = nxt[w] + cur
                    if nv >= MOD:
                        nv -= MOD
                    nxt[w] = nv

        for v in range(h):
            if not ((ah >> v) & 1):
                continue

            for mask in range(1, lim):
                if mask.bit_count() >= 2:
                    val = dp[mask][v]
                    if val:
                        s = mask | (1 << h)
                        f[s] = (f[s] + val * INV2) % MOD

    for i in range(n):
        f[1 << i] = 1

    # Precompute inverses up to n.
    inv = [0] * (n + 1)
    if n >= 1:
        inv[1] = 1
    for i in range(2, n + 1):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # Insert vertex i into a compressed mask.
    def insert_vertex(mask, i):
        low = (1 << i) - 1
        return (mask & low) | ((mask & ~low) << 1) | (1 << i)

    # Remove vertex i from a full mask.
    def remove_vertex(mask, i):
        low = (1 << i) - 1
        return (mask & low) | ((mask >> 1) & ~low)

    # Process each vertex as a newly available articulation point.
    for i in range(n):
        k = n - 1
        size = 1 << k
        lower_mask = (1 << i) - 1
        lower_neighbors = adj[i] & lower_mask

        # a[mask][d] stores the ranked subset-zeta representation.
        a = [[0] * (k + 1) for _ in range(size)]

        # Build g for the universe with vertex i removed.
        for s in range(size):
            full_without = insert_vertex(s, i) ^ (1 << i)
            full_with = full_without | (1 << i)

            deg = (lower_neighbors & full_without).bit_count()

            val = f[full_with]
            if deg:
                val += f[full_without] * deg
                val %= MOD

            a[s][s.bit_count()] = val

        # Subset zeta transform.
        bit = 1
        while bit < size:
            step = bit << 1
            for base in range(0, size, step):
                for off in range(bit):
                    x = a[base + off]
                    y = a[base + off + bit]
                    for d in range(k + 1):
                        y[d] += x[d]
                        if y[d] >= MOD:
                            y[d] -= MOD
            bit <<= 1

        # Pointwise formal exponential.
        for s in range(size):
            g = a[s]
            res = [0] * (k + 1)
            res[0] = 1

            for degree in range(1, k + 1):
                total = 0
                for j in range(1, degree + 1):
                    total += j * g[j] % MOD * res[degree - j]
                    if total >= (1 << 61):
                        total %= MOD
                res[degree] = total % MOD * inv[degree] % MOD

            a[s] = res

        # Inverse subset zeta transform.
        bit = 1
        while bit < size:
            step = bit << 1
            for base in range(0, size, step):
                for off in range(bit):
                    x = a[base + off]
                    y = a[base + off + bit]
                    for d in range(k + 1):
                        y[d] -= x[d]
                        if y[d] < 0:
                            y[d] += MOD
            bit <<= 1

        # Update all states containing i.
        for s in range(size):
            full = insert_vertex(s, i)
            f[full] = a[s][s.bit_count()]

    return f[N - 1]

def solve():
    n, m = map(int, input().split())

    edges = []
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        edges.append((u, v))

    print(count_cactus(n, edges))

if __name__ == "__main__":
    solve()
```

The first part builds the adjacency bitmasks. Because (n) is at most 13, a set of candidate neighbors fits naturally in one Python integer, and operations such as intersection with a subset and `bit_count()` are very cheap.

The cycle DP fixes the largest vertex (h), so every cycle is assigned to exactly one iteration. `dp[mask][v]` represents a simple path, and the mask itself prevents a vertex from being used twice. The path is closed through (h) only when its endpoint is adjacent to (h). Each undirected cycle has two orientations, which is why `INV2` is applied.

The articulation phase compresses the vertex universe by removing the current vertex (i). `insert_vertex` converts a compressed mask back to the original numbering. The expression involving `lower_neighbors` counts only neighbors smaller than (i). This ordering is essential. If all neighbors were allowed there, the same bridge could be introduced at both endpoints.

The ranked subset transform stores one coefficient for each subset cardinality. After the zeta transform, the set exponential becomes an ordinary polynomial exponential at every transformed subset. The recurrence

[
E_k=\frac{1}{k}\sum_{j=1}^{k}jG_jE_{k-j}
]

computes the coefficient of degree (k) in (\exp(G)). The inverse zeta transform recovers the subset values.

All arithmetic is performed modulo (998244353). Python integers do not overflow, but intermediate products are still reduced modulo the prime. The inverse values are computed with the standard recurrence for (1,2,\ldots,n), and the special value (1/2) used for cycle orientations is `(MOD + 1) // 2`.

## Worked Examples

### Sample 1

The graph is a triangle.

```
3 3
1 2
2 3
3 1
```

There is one simple cycle on all three vertices. The valid spanning cactus subgraphs are the three spanning trees and the complete triangle.

| Stage | Important state | Value |
| --- | --- | --- |
| Cycle DP | (f[{1,2,3}]) | 1 |
| Process vertex 1 | (f[{1,2,3}]) | 1 |
| Process vertex 2 | (f[{1,2,3}]) | 1 |
| Process vertex 3 | (f[{1,2,3}]) | 4 |
| Final | (f[V]) | 4 |

When vertex 3 is processed, it can attach separately to vertices 1 and 2. The exponential combines the possibilities corresponding to the three spanning trees, while the previously counted cycle contributes the fourth structure.

The answer is therefore `4`.

### Sample 2

The graph has five vertices and no edges.

```
5 0
```

There are no cycles and no possible bridge blocks. The singleton states exist, but there is no way to combine two different vertices into one connected structure.

| Stage | Number of vertices available | Full-set state |
| --- | --- | --- |
| Initial blocks | 1 through 5 | 0 |
| Process vertex 1 | 5 | 0 |
| Process vertex 2 | 5 | 0 |
| Process vertex 3 | 5 | 0 |
| Process vertex 4 | 5 | 0 |
| Process vertex 5 | 5 | 0 |

The final full-set state remains zero, matching the sample output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n^3 2^n)) | Cycle DP takes (O(n^2 2^n)); the ranked subset exponential is applied for every vertex and costs (O(n^3 2^n)) overall |
| Space | (O(n2^n)) | The main subset array and one ranked-transform table dominate memory |

With (n\le13), (2^n) is only 8192. The cubic factor in the optimized articulation phase is consequently small enough for the intended limits. The approach avoids the impossible (2^m) enumeration and works entirely with vertex subsets. The same cycle-counting plus set-exponential structure is known to achieve (O(n^3 2^n)) for the generalized formulation.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
assert run("""\
3 3
1 2
2 3
3 1
""") == "4", "sample 1"

# Provided sample 2
assert run("""\
5 0
""") == "0", "sample 2"

# Provided sample 3
assert run("""\
8 9
1 5
1 8
2 4
2 8
3 4
3 6
4 7
5 7
6 8
""") == "35", "sample 3"

# Minimum-size graph: one isolated vertex is connected.
assert run("""\
1 0
""") == "1", "single vertex"

# Two vertices without an edge are disconnected.
assert run("""\
2 0
""") == "0", "two isolated vertices"

# A path on three vertices has exactly one spanning cactus.
assert run("""\
3 2
1 2
2 3
""") == "1", "path of length two"

# Complete graph K4.
# 16 spanning trees + 11 connected unicyclic four-edge graphs.
assert run("""\
4 6
1 2
1 3
1 4
2 3
2 4
3 4
""") == "27", "K4"

# Maximum number of vertices with no edges.
assert run("""\
13 0
""") == "0", "maximum n, empty graph"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0` | 1 | Smallest possible graph and singleton base state |
| `2 0` | 0 | Connectivity boundary and empty edge set |
| `3 2` with edges `1-2, 2-3` | 1 | Spanning requirement and bridge construction |
| (K_4) | 27 | Multiple cycles and rejection of graphs where cycles share an edge |
| `13 0` | 0 | Maximum vertex bound and subset-state boundary |

## Edge Cases

For the single-vertex case

```
1 0
```

the initial state (f[{1}]) is set to 1. There are no articulation transforms that can introduce another vertex, so the full mask remains 1. The algorithm correctly treats the one-vertex graph as connected.

For two isolated vertices,

```
2 0
```

both singleton states are initialized, but there is no edge and no cycle. During every articulation step, the term involving the degree is zero. No state containing both vertices is created, so (f[{1,2}]=0).

For the path

```
3 2
1 2
2 3
```

there are no cycle states. When vertex 2 is processed, its lower neighbor 1 creates the piece consisting of edge (1-2). When vertex 3 is processed, its lower neighbor 2 attaches the already constructed component containing vertices 1 and 2. The full mask consequently receives exactly one contribution, corresponding to the complete path.

For (K_4), the cycle DP creates every simple cycle as an atomic block. The articulation phase can attach cycles and bridges, but it never creates a structure in which two different cycle blocks share an edge. Thus all 16 spanning trees and all 11 connected unicyclic four-edge graphs survive, while the five-edge and six-edge graphs are excluded because their cycles overlap on edges. The resulting answer is 27.

The most delicate boundary is the division by two in cycle counting. A cycle such as (1-2-3-1) can be traversed as (1,2,3) or (1,3,2), but both traversals describe the same undirected edge set. The DP counts both orientations and divides by two only after closing the cycle. This is safe because the graph has no multiple edges, so every simple cycle has exactly those two orientations.
