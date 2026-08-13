---
title: "CF 102341B - Bulbasaur"
description: "The graph consists of (n) layers, each containing exactly (k) vertices. Edges only go from layer (i) to layer (i+1). A vine is a directed path, and two vines cannot share either a vertex or an edge."
date: "2026-08-14T05:18:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102341
codeforces_index: "B"
codeforces_contest_name: "Radewoosh+mnbvmar Contest (supported by AIM Tech)"
rating: 0
weight: 102341
solve_time_s: 331
verified: true
draft: false
---

[CF 102341B - Bulbasaur](https://codeforces.com/problemset/problem/102341/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

The graph consists of (n) layers, each containing exactly (k) vertices. Edges only go from layer (i) to layer (i+1). A vine is a directed path, and two vines cannot share either a vertex or an edge. For two layers (i<j), (f(i,j)) is the maximum number of vertex-disjoint directed paths from layer (i) to layer (j). The task is to sum this value over every pair of distinct layers.

For fixed (i,j), this is a maximum-flow problem with vertex capacities equal to one. Split every vertex into an in-vertex and an out-vertex with a capacity-one edge between them. Tunnels receive infinite capacity, and a super-source is connected to every vertex of layer (i), while every vertex of layer (j) connects to a super-sink. The resulting maximum flow is exactly (f(i,j)).

The constraint (k\leq 9) is the key. The number of layers can be as large as (40000), so anything quadratic in (n) is already too large. There are roughly (8\cdot 10^8) pairs of layers when (n=40000), so explicitly solving a flow problem for every pair is impossible. On the other hand, (2^k\leq512), which makes subset dynamic programming practical. The accepted approach exploits exactly this asymmetry, replacing the quadratic number of intervals by (n) transitions over (2^k) subsets. The resulting complexity is (O(nk^2 2^k)).

There are several boundary cases that are easy to mishandle. With (k=1), a single missing tunnel immediately makes every interval crossing it have flow zero. For example,

```
2 1
0
```

has answer `0`. A solution that assumes every pair of neighboring layers contributes at least one path would incorrectly return `1`.

The opposite case is also useful. With (k=1) and every tunnel present,

```
3 1
1
1
```

every pair of layers has one path, so the answer is `3`. A solution that only counts paths of maximum length would miss the interval from layer 1 to layer 2 and return `1`.

A second subtle case occurs when one vertex in an intermediate layer is unusable. In the first sample, the last matrix contains a zero row, so only three paths can cross from layer 3 to layer 4. Thus (f(3,4)=3), even though the earlier layers admit four disjoint paths. Treating every layer independently and taking the minimum number of vertices without checking connectivity would be incorrect.

## Approaches

The direct approach is to consider every interval ([i,j]), construct its vertex-capacitated flow network, and run a maximum-flow algorithm. This is correct because Menger's theorem identifies the maximum number of vertex-disjoint paths with the minimum vertex cut. After splitting vertices, the problem becomes an ordinary edge-capacitated flow.

The problem is the number of intervals. There are (\Theta(n^2)) of them. An interval of length (L) contains (O(Lk)) vertices and (O(Lk^2)) possible tunnel edges. Even a Ford-Fulkerson style implementation needs up to (k) augmentations, giving (O(Lk^3)) work for one interval. Summed over all intervals, the total is (O(n^3k^3)). For (n=40000), the sum of interval lengths alone is

[
\sum_{1\leq i<j\leq n}(j-i)
=\frac{n(n-1)(n+1)}6,
]

which is about (1.07\cdot10^{13}). With (k=9), the corresponding (k^3) factor gives roughly (7.8\cdot10^{15}) edge-processing units before even accounting for flow overhead.

The brute force works because every individual flow value is small, at most (k), but it fails because it solves essentially the same small problem separately for every pair of layers.

The key observation is to use the min-cut formulation instead of computing the flow value directly. For a fixed right endpoint (r), define, for every (c\in[1,k]), the largest layer (L_c) such that

[
f(L_c,r)\geq c.
]

Because extending an interval to the left can only make the collection of disjoint paths harder, the set of left endpoints supporting (c) paths is a suffix. Consequently, the number of left endpoints (i<r) with (f(i,r)\geq c) is simply (r-L_c). Since

[
f(i,r)=\sum_{c=1}^{k}[f(i,r)\geq c],
]

we get

\sum_{c=1}^{k}(r-L_c).
]

So the whole problem becomes maintaining these (k) threshold positions while scanning the graph from left to right.

The remaining difficulty is describing a minimum cut without explicitly storing all its vertices. Since each layer contains only (k\leq9) vertices, represent the vertices that are still reachable in the current layer by a bitmask (S). For each subset (S) and each cut threshold (c), we maintain the largest possible left endpoint for which a cut of the required size leaves exactly (S) reachable. Moving across one matrix transforms (S) into its neighborhood, and deleting a vertex from the reachable set increases the number of vertices used by the cut. Both operations can be performed with subset DP.

This is the same small-width state compression behind the standard accepted solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^3k^3)) | (O(nk^2)) for one flow network | Too slow |
| Optimal | (O(nk^2 2^k)) | (O(k2^k)) | Accepted |

## Algorithm Walkthrough

1. Represent every subset of the current layer by a (k)-bit mask. A set bit means that the corresponding vertex is still reachable from the left side of the cut.
2. For every mask (S) and every (c\in[0,k]), maintain `dp[S][c]`. Its value is a layer index. It represents the furthest left endpoint for which, after paying the corresponding cut cost, the current reachable set can be exactly (S) while retaining at least (c) units of connectivity. The only information we need from this state is the largest possible left endpoint, because that is exactly what determines how many intervals contribute to the answer.
3. Initially we are at layer 1. If exactly the vertices in (S) remain reachable, the other (k-|S|) vertices can be removed. This gives the initial threshold
[
dp[S][c]=1
]
whenever (c\leq k-|S|). Larger thresholds are impossible, so those entries receive the sentinel value (n+1).
4. Read the matrix between the current layer and the next layer. For every vertex of the old layer, store the bitmask of its outgoing neighbors. For a subset (S), its complete neighborhood is the union of those masks.
5. Before deleting vertices in the new layer, transfer every state from (S) to its neighborhood (N(S)). When several old subsets produce the same new subset, their states describe alternative ways of achieving the same reachable set, so we merge them by keeping the best threshold for every (c).
6. Now process vertex deletions inside the new layer. If the reachable set is (S), deleting a vertex (u\in S) changes the state to (S\setminus{u}) and increases the number of deleted vertices by one. In the DP this is a one-bit subset transition:
[
dp[S\setminus{u}][c]
\leftarrow
\max(dp[S\setminus{u}][c],dp[S][c-1]).
]
Applying this for every set bit performs the entire cut construction for the new layer.
7. The empty set is the state where no vertex in the current layer is reachable from the left endpoint. Thus `dp[0][c]` is precisely the largest left endpoint for which a cut corresponding to threshold (c) can disconnect that endpoint from the current layer.
8. For every (c=1,\ldots,k), add
[
r-dp[0][c]
]
to the answer. This counts the left endpoints (i<r) for which at least (c) disjoint paths exist. Summing this over (c) is exactly the sum of the flow values ending at layer (r).
9. Continue through all (n-1) matrices. Only two DP layers are needed, so the memory consumption remains (O(k2^k)).

The correctness invariant is that after processing layer (r), every state `dp[S][c]` stores the furthest left endpoint compatible with a cut that leaves exactly (S) reachable at layer (r) and still supports threshold (c). The neighborhood transition is exactly the effect of crossing the next layer without cutting a vertex, while the subset transition enumerates every possible choice of cut vertices in that layer. Thus the empty-set state considers every possible vertex cut. By the max-flow min-cut theorem, its threshold is equivalent to the corresponding number of vertex-disjoint paths. Finally, monotonicity in the left endpoint turns each threshold into the simple count (r-dp[0][c]), so every (f(i,r)) is counted exactly once for every unit of flow it contributes.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, k = map(int, input().split())

    size = 1 << k
    inf = n + 1

    popcnt = [0] * size
    for mask in range(1, size):
        popcnt[mask] = popcnt[mask >> 1] + (mask & 1)

    bits = [[] for _ in range(size)]
    for mask in range(1, size):
        x = mask
        cur = bits[mask]
        while x:
            b = x & -x
            cur.append(b.bit_length() - 1)
            x ^= b

    dp = [[inf] * (k + 1) for _ in range(size)]

    for mask in range(size):
        lim = k - popcnt[mask]
        row = dp[mask]
        for c in range(lim + 1):
            row[c] = 1

    ans = 0

    def merge(dst, src):
        a0 = dst[0]
        b0 = src[0]

        if a0 <= b0:
            base = a0
            for c in range(1, k + 1):
                x = src[c]
                if x == b0:
                    x = base
                if x > dst[c]:
                    dst[c] = x
        else:
            base = b0
            old0 = a0
            for c in range(1, k + 1):
                x = dst[c]
                if x == old0:
                    x = base
                y = src[c]
                if y > x:
                    x = y
                dst[c] = x
            dst[0] = base

    def merge_shift(dst, src):
        a0 = dst[0]
        b0 = src[0]

        if a0 <= b0:
            base = a0
            for c in range(1, k + 1):
                x = src[c - 1]
                if x == b0:
                    x = base
                if x > dst[c]:
                    dst[c] = x
        else:
            base = b0
            old0 = a0
            for c in range(1, k + 1):
                x = dst[c]
                if x == old0:
                    x = base
                y = src[c - 1]
                if y > x:
                    x = y
                dst[c] = x
            dst[0] = base

    for layer in range(2, n + 1):
        to = [0] * k

        for u in range(k):
            s = input().strip()
            while not s:
                s = input().strip()

            mask = 0
            for v, ch in enumerate(s):
                if ch == '1':
                    mask |= 1 << v
            to[u] = mask

        # neigh[mask] = union of all outgoing neighbors of vertices in mask.
        neigh = [0] * size
        for mask in range(1, size):
            b = mask & -mask
            u = b.bit_length() - 1
            neigh[mask] = neigh[mask ^ b] | to[u]

        nxt = [[inf] * (k + 1) for _ in range(size)]

        # Cross the current matrix without deleting a vertex.
        for mask in range(size):
            merge(nxt[neigh[mask]], dp[mask])

        dp = nxt

        # Delete vertices in the new layer.
        for mask in range(size - 1, 0, -1):
            src = dp[mask]
            for u in bits[mask]:
                merge_shift(dp[mask ^ (1 << u)], src)

        # A cut cannot need a left endpoint beyond the current layer.
        for mask in range(size):
            lim = k - popcnt[mask]
            row = dp[mask]
            for c in range(lim + 1):
                if row[c] > layer:
                    row[c] = layer

        empty = dp[0]
        for c in range(1, k + 1):
            ans += layer - empty[c]

    print(ans)

if __name__ == "__main__":
    main()
```

The first part of the implementation precomputes `popcnt` and the set bits of every mask. Since the same subset structure is used at every layer, doing this once avoids repeatedly decoding masks.

The `to` array stores the outgoing neighbors of one vertex as a bitmask. The `neigh` array is then built by the standard least-significant-bit recurrence. If `b` is one bit of `mask`, the neighborhood of `mask` is the neighborhood of `mask ^ b` union the neighborhood of that single vertex. This reduces the neighborhood calculation for all (2^k) subsets to (O(2^k)) per layer.

The `merge` routine deserves special attention. A DP row is not simply a collection of independent values. Its zero-th entry determines the boundary of the represented threshold interval. When two ways of obtaining the same subset are combined, entries equal to the source row's zero-th boundary have to be shifted to the better boundary before taking the componentwise maximum. This is exactly the normalization performed by the reference transition.

`merge_shift` is the same operation after deleting one vertex. Instead of constructing a temporary shifted array, it directly treats source entry `src[c - 1]` as the destination's entry `c`. Avoiding temporary row allocations matters because the transition is executed for every subset and every set bit.

The descending mask order in the deletion phase is deliberate. A state for `mask` must be used before states representing larger subsets can overwrite information needed for the current transition. The source code's equivalent operation processes masks from the full mask downward.

The answer is stored in Python's arbitrary-precision integer type, so there is no overflow issue. The largest possible answer is (k\binom n2), which is easily representable by Python integers.

## Worked Examples

### Sample 1

The three matrices are

```
1000
1100
0110
0011

0100
1100
0010
0001

1000
1100
0000
0011
```

The actual flow values are

[
f(1,2)=4,\quad f(1,3)=4,\quad f(1,4)=3,
]

[
f(2,3)=4,\quad f(2,4)=3,\quad f(3,4)=3.
]

The DP does not need to store these six values individually. For each right endpoint (r), it stores the threshold boundary for every (c).

| Right layer (r) | (c) | Left endpoints with (f(i,r)\ge c) | `dp[0][c]` | Contribution (r-dp[0][c]) |
| --- | --- | --- | --- | --- |
| 2 | 1 | 1 | 1 | 1 |
| 2 | 2 | 1 | 1 | 1 |
| 2 | 3 | 1 | 1 | 1 |
| 2 | 4 | 1 | 1 | 1 |
| 3 | 1 | 1,2 | 1 | 2 |
| 3 | 2 | 1,2 | 1 | 2 |
| 3 | 3 | 1,2 | 1 | 2 |
| 3 | 4 | 1,2 | 1 | 2 |
| 4 | 1 | 1,2,3 | 1 | 3 |
| 4 | 2 | 1,2,3 | 1 | 3 |
| 4 | 3 | 1,2,3 | 1 | 3 |
| 4 | 4 | none | 4 | 0 |

The contributions are (4+8+9=21). The last row exercises the boundary where four disjoint paths cease to exist, while three still survive.

### Sample 2

The matrices are

```
000
100
010

000
100
010

010
101
010

010
101
010
```

The resulting flow values are

[
f(1,2)=2,
]

[
f(1,3)=1,\quad f(2,3)=2,
]

[
f(1,4)=1,\quad f(2,4)=2,\quad f(3,4)=2,
]

[
f(1,5)=1,\quad f(2,5)=2,\quad f(3,5)=2,\quad f(4,5)=2.
]

| Right layer (r) | (c) | `dp[0][c]` | Contribution | Sum for this (r) |
| --- | --- | --- | --- | --- |
| 2 | 1 | 1 | 1 |  |
| 2 | 2 | 1 | 1 | 2 |
| 2 | 3 | 2 | 0 |  |
| 3 | 1 | 1 | 2 |  |
| 3 | 2 | 2 | 1 |  |
| 3 | 3 | 3 | 0 | 3 |
| 4 | 1 | 1 | 3 |  |
| 4 | 2 | 2 | 2 |  |
| 4 | 3 | 4 | 0 | 5 |
| 5 | 1 | 1 | 4 |  |
| 5 | 2 | 2 | 3 |  |
| 5 | 3 | 5 | 0 | 7 |

The total is (2+3+5+7=17). This example demonstrates why the threshold formulation is useful: the flow for a fixed right endpoint can drop from two paths to one as the left endpoint moves earlier, and the DP captures all such boundaries simultaneously.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(nk^2 2^k)) | There are (2^k) subset states, each transition considers up to (k) vertices and (k) threshold values. |
| Space | (O(k2^k)) | Only the current and previous layer of subset states are required. |

With (k\leq9), (2^k\leq512), so the exponential part depends only on the small width of a layer rather than on (n). The number of layers can reach (40000), but each layer performs the same bounded-width transition. This is exactly why the subset DP is viable for the original constraints.

## Test Cases

The following tests assume the `main` function from the solution is in the same Python module. The helper replaces standard input and captures standard output.

```python
import sys
import io
from contextlib import redirect_stdout

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    try:
        with redirect_stdout(out):
            main()
    finally:
        sys.stdin = old_stdin
    return out.getvalue().strip()

# Provided sample 1
assert run("""\
4 4
1000
1100
0110
0011

0100
1100
0010
0001

1000
1100
0000
0011
""") == "21", "sample 1"

# Provided sample 2
assert run("""\
5 3
000
100
010

000
100
010

010
101
010

010
101
010
""") == "17", "sample 2"

# Minimum-size graph, no tunnel.
assert run("""\
2 1
0
""") == "0", "minimum size with no path"

# Minimum-size graph, one tunnel.
assert run("""\
2 1
1
""") == "1", "minimum size with one path"

# Two vertices and a complete matching between the layers.
assert run("""\
2 2
10
01
""") == "2", "two disjoint paths"

# A path exists only across the first boundary.
assert run("""\
3 1
1
0
""") == "1", "boundary between usable and unusable layers"

# All possible paths exist for k=1.
assert run("""\
3 1
1
1
""") == "3", "all-equal connected layers"

# Maximum-size structural test for k=1.
n = 40000
maximum_case = str(n) + " 1\n" + "1\n" * (n - 1)
assert run(maximum_case) == str(n * (n - 1) // 2), "maximum n, k=1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1` with tunnel `0` | `0` | Minimum size and disconnected boundary |
| `2 1` with tunnel `1` | `1` | Minimum size and the smallest positive answer |
| `2 2` with identity matrix | `2` | Multiple disjoint paths and (k>1) |
| `3 1` with matrices `1`, `0` | `1` | Off-by-one behavior across a broken boundary |
| `3 1` with matrices `1`, `1` | `3` | Every interval contributes |
| `n=40000, k=1`, all matrices `1` | `799980000` | Maximum (n) and maximum accumulated answer |

## Edge Cases

For the smallest disconnected instance,

```
2 1
0
```

there is no tunnel from layer 1 to layer 2. The DP starts with one subset bit and processes a matrix whose neighborhood is empty. The empty reachable-set state reaches the threshold for one path immediately, so `layer - dp[0][1]` is zero. The final answer is `0`.

For the smallest connected instance,

```
2 1
1
```

the only vertex in layer 1 reaches the only vertex in layer 2. The empty-set threshold remains at the previous boundary, giving one left endpoint with one available path. The answer is `1`.

For two simultaneous paths,

```
2 2
10
01
```

the first vertex connects to the first vertex and the second connects to the second. The full two-bit reachable state survives the transition, so the threshold for (c=1) and (c=2) both counts the only interval. Their contributions are (1+1=2).

For the boundary case

```
3 1
1
0
```

the first interval has one path, but the second boundary is disconnected. At layer 2 the threshold for one path counts the start at layer 1, while at layer 3 it counts no valid interval. The total is exactly `1`, showing why the DP must process every boundary independently rather than assuming connectivity persists.

For the fully connected one-vertex case,

```
3 1
1
1
```

each of the three intervals has one path. At every right endpoint, the threshold for one path includes every earlier layer, so the contributions are (1) for layer 2 and (2) for layer 3. The final answer is `3`.

For the maximum-size case with (n=40000) and (k=1), every interval has flow one, so the answer is

[
\binom{40000}{2}=799980000.
]

The DP never stores all intervals. It keeps only the current threshold boundary, which is why the answer can be accumulated without quadratic memory or time.
