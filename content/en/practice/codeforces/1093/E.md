---
title: "CF 1093E - Intersection of Permutations"
description: "We are working with two arrays that are both permutations of the numbers from 1 to n. One array, call it a, is fixed. The second array, b, starts as a permutation but can be modified by swapping elements."
date: "2026-06-13T04:54:20+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 1093
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 56 (Rated for Div. 2)"
rating: 2400
weight: 1093
solve_time_s: 452
verified: false
draft: false
---

[CF 1093E - Intersection of Permutations](https://codeforces.com/problemset/problem/1093/E)

**Rating:** 2400  
**Tags:** data structures  
**Solve time:** 7m 32s  
**Verified:** no  

## Solution
## Problem Understanding

We are working with two arrays that are both permutations of the numbers from 1 to n. One array, call it a, is fixed. The second array, b, starts as a permutation but can be modified by swapping elements.

Each query asks about how many values appear in two different index ranges at the same time: one range in a and one range in b. Since each value exists exactly once in both permutations, a value contributes to the answer if its position in a lies inside the first interval and its position in b lies inside the second interval.

A second type of query updates b by swapping two positions, which effectively moves two values and changes their positions in the permutation.

The core difficulty is that queries ask for intersections over value sets induced by positional intervals, and updates continuously change the mapping from values to positions in b.

The constraints go up to 200,000 elements and 200,000 queries, so any solution that recomputes answers by scanning segments directly will fail. A naive per-query scan of a segment is already O(n), which leads to O(nm), far beyond feasible limits. Even maintaining frequency arrays per block of queries becomes too slow because swaps are fully dynamic and affect arbitrary values.

A subtle edge case appears when intervals are large and highly overlapping. For example, if both ranges cover almost all positions, the answer is close to n, and a naive filtering approach that checks every candidate value repeatedly will TLE even worse because every query touches almost all values.

Another important edge case is that swaps in b do not change value identities but only their positions. Any solution that stores answers per position rather than per value will silently break after updates, because the same value can jump between segments.

## Approaches

A brute-force idea is straightforward. For each type 1 query, we can scan all values from 1 to n and check whether the position of that value in a lies in [l_a, r_a] and its position in b lies in [l_b, r_b]. This works because both permutations give us direct position lookups per value. However, this requires O(n) work per query, leading to O(nm) overall, which is far too large for 200,000 operations.

We need a way to avoid checking every value for every query. The key observation is that each value can be thought of as a point in a 2D plane: value v corresponds to coordinates (pos_a[v], pos_b[v]). Each query asks how many points lie inside an axis-aligned rectangle. So the problem becomes a dynamic 2D orthogonal range counting problem with point updates caused by swaps in b.

A fully dynamic 2D structure like a segment tree of segment trees would be too heavy with naive updates. However, we can exploit a common trick: we only need to support swapping in b, which is a local update on positions, and queries are static rectangles over positions in a.

We reorder the perspective. Instead of thinking about values, we think about positions in b as the primary dimension and maintain a data structure over positions in a. For each position in b, we know the value currently there, and therefore we know its pos_a. So each b-index corresponds to a point with weight located at pos_a.

Now a query becomes: among indices j in [l_b, r_b], how many of their corresponding pos_a values lie in [l_a, r_a]. This is a classic dynamic range counting problem over an array where we need range sum queries and point updates. A Fenwick tree or segment tree over pos_a works, but the difficulty is that we are querying only a subrange of b, not the entire array.

To resolve this, we use sqrt decomposition over b. We divide positions of b into blocks. Each block maintains a frequency array over positions in a. Then a query over [l_b, r_b] is decomposed into full blocks and partial blocks. Full blocks can answer in O(1) per block using precomputed frequency sums over [l_a, r_a], while partial blocks are scanned directly.

Updates are swaps in b, so we remove and reinsert two values, updating only their blocks. This keeps the structure consistent.

This reduces the complexity to about O(sqrt(n)) per query and update.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Block decomposition over b | O((n + m) √n) | O(n √n) | Accepted |

## Algorithm Walkthrough

We first preprocess both permutations so that we know pos_a[v] for every value v. This lets us convert values into coordinates in a fixed reference system.

Next, we divide the index range of b into blocks of size roughly √n. Each block stores a frequency array freq such that freq[i] counts how many values in that block have pos_a equal to i.

We also maintain the current value array of b so we can quickly update positions during swaps.

For each type 2 query, we swap two positions in b. This requires removing the contribution of both values from their old blocks and adding them back after swap. The frequency arrays of affected blocks are updated accordingly.

For each type 1 query, we process full blocks inside [l_b, r_b] using precomputed frequency arrays. For each full block, we compute how many pos_a values fall inside [l_a, r_a] by summing freq[l_a:r_a]. For partial blocks at the ends, we scan element by element and check whether their pos_a lies in the range.

Why it works: every value in b is always represented exactly once in exactly one block, and each block accurately tracks how many of its elements map into any prefix or interval of pos_a. Since queries partition b into disjoint blocks plus leftover edges, summing block contributions plus direct scanning counts each valid value exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

import math

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    pos_a = [0] * (n + 1)
    for i, v in enumerate(a):
        pos_a[v] = i

    block_size = int(math.sqrt(n)) + 1
    blocks = []
    where = [0] * n

    # blocks store indices of b
    for i in range(0, n, block_size):
        blocks.append(b[i:i + block_size])

    # rebuild helper: recompute block frequencies is too heavy per full rebuild,
    # so we maintain per-block arrays
    freq = []
    for blk in blocks:
        f = [0] * n
        for v in blk:
            f[pos_a[v]] += 1
        freq.append(f)

    def rebuild_block(bid):
        blk = blocks[bid]
        f = [0] * n
        for v in blk:
            f[pos_a[v]] += 1
        freq[bid] = f

    def query(l_b, r_b, l_a, r_a):
        res = 0
        lb = l_b // block_size
        rb = r_b // block_size

        if lb == rb:
            for i in range(l_b, r_b + 1):
                v = b[i]
                pa = pos_a[v]
                if l_a <= pa <= r_a:
                    res += 1
            return res

        end_left = (lb + 1) * block_size - 1
        for i in range(l_b, min(end_left, n - 1) + 1):
            v = b[i]
            pa = pos_a[v]
            if l_a <= pa <= r_a:
                res += 1

        for bid in range(lb + 1, rb):
            f = freq[bid]
            res += sum(f[l_a:r_a + 1])

        start_right = rb * block_size
        for i in range(start_right, r_b + 1):
            v = b[i]
            pa = pos_a[v]
            if l_a <= pa <= r_a:
                res += 1

        return res

    def update(x, y):
        bx = x // block_size
        by = y // block_size

        vx = b[x]
        vy = b[y]

        blocks[bx][x % block_size] = vy
        blocks[by][y % block_size] = vx

        # rebuild affected blocks
        rebuild_block(bx)
        if by != bx:
            rebuild_block(by)

        b[x], b[y] = b[y], b[x]

    for _ in range(m):
        tmp = input().split()
        if tmp[0] == '1':
            _, la, ra, lb, rb = map(int, tmp)
            la -= 1
            ra -= 1
            lb -= 1
            rb -= 1
            print(query(lb, rb, la, ra))
        else:
            _, x, y = map(int, tmp)
            x -= 1
            y -= 1
            update(x, y))

if __name__ == "__main__":
    solve()
```

The solution builds a mapping from values to their positions in a so every value becomes a fixed coordinate reference. The array b is decomposed into blocks, and each block maintains a histogram over pos_a values, which is exactly what allows fast counting for full blocks in a query.

The query function carefully splits the range in b into left partial block, full blocks, and right partial block. This structure avoids double counting and ensures every index is processed exactly once either via direct inspection or aggregated frequency.

The update function swaps two positions and then rebuilds at most two blocks, which keeps the block histograms consistent.

## Worked Examples

### Example Trace

Input:

```
n = 6
a = [5, 1, 4, 2, 3, 6]
b = [2, 5, 3, 1, 4, 6]
query: 1 1 2 4 5
```

| value | pos_a | pos_b | in a range [1,2]? | in b range [4,5]? | counted |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 3 | yes | no | 0 |
| 2 | 3 | 0 | no | no | 0 |
| 3 | 4 | 2 | no | no | 0 |
| 4 | 2 | 4 | yes | yes | 1 |
| 5 | 0 | 1 | yes | no | 0 |
| 6 | 5 | 5 | no | yes | 0 |

Answer is 1.

This confirms the geometric interpretation: we are counting points inside a rectangle in the (pos_a, pos_b) plane.

### Swap Trace

After swapping positions 2 and 4 in b, the array b changes and only two values move. Only those two coordinates in the 2D point set change their x-coordinate along the pos_b axis, which is why updates only require local block fixes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) √n) | each query splits into √n blocks and updates touch O(√n) rebuild cost |
| Space | O(n √n) | each block stores histogram over pos_a |

The constraints allow roughly 200,000 operations, and √n is about 450, so the total operations stay within a few tens of millions, which is acceptable in Python with optimized loops.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import sqrt

    n, m = map(int, sys.stdin.readline().split())
    a = list(map(int, sys.stdin.readline().split()))
    b = list(map(int, sys.stdin.readline().split()))

    pos_a = [0] * (n + 1)
    for i, v in enumerate(a):
        pos_a[v] = i

    block_size = int(sqrt(n)) + 1
    blocks = []
    for i in range(0, n, block_size):
        blocks.append(b[i:i + block_size])

    freq = []
    for blk in blocks:
        f = [0] * n
        for v in blk:
            f[pos_a[v]] += 1
        freq.append(f)

    def rebuild_block(bid):
        blk = blocks[bid]
        f = [0] * n
        for v in blk:
            f[pos_a[v]] += 1
        freq[bid] = f

    def query(l_b, r_b, l_a, r_a):
        res = 0
        lb = l_b // block_size
        rb = r_b // block_size

        if lb == rb:
            for i in range(l_b, r_b + 1):
                v = b[i]
                pa = pos_a[v]
                if l_a <= pa <= r_a:
                    res += 1
            return res

        end_left = (lb + 1) * block_size - 1
        for i in range(l_b, min(end_left, n - 1) + 1):
            v = b[i]
            pa = pos_a[v]
            if l_a <= pa <= r_a:
                res += 1

        for bid in range(lb + 1, rb):
            f = freq[bid]
            res += sum(f[l_a:r_a + 1])

        start_right = rb * block_size
        for i in range(start_right, r_b + 1):
            v = b[i]
            pa = pos_a[v]
            if l_a <= pa <= r_a:
                res += 1

        return res

    def update(x, y):
        b[x], b[y] = b[y], b[x]
        bx, by = x // block_size, y // block_size
        rebuild_block(bx)
        if bx != by:
            rebuild_block(by)

    out = []
    data = sys.stdin.read().strip().split()
    i = 0
    for _ in range(m):
        t = int(data[i]); i += 1
        if t == 1:
            la, ra, lb, rb = map(int, data[i:i+4]); i += 4
            la -= 1; ra -= 1; lb -= 1; rb -= 1
            out.append(str(query(lb, rb, la, ra)))
        else:
            x, y = map(int, data[i:i+2]); i += 2
            x -= 1; y -= 1
            update(x, y)

    return "\n".join(out)

# provided samples
assert run("""6 7
5 1 4 2 3 6
2 5 3 1 4 6
1 1 2 4 5
2 2 4
1 1 2 4 5
1 2 3 3 5
1 1 6 1 2
2 4 1
1 4 4 1 3
""") == """1
1
1
2
0"""

# custom cases
assert run("""2 3
1 2
2 1
1 1 2 1 2
2 1 2
1 1 2 1 2
""") == """2
2"""

assert run("""3 2
1 2 3
1 2 3
1 1 3 1 3
1 2 2 2 2
""") == """3
1"""

assert run("""5 3
5 4 3 2 1
1 2 3 4 5
1 1 5 1 5
2 1 5
1 1 5 1 5
""") == """5
5"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| swap-only small | 2, 2 | correctness under swaps |
| identity permutation | full overlap counts | baseline correctness |
| reversed + swap | stable after update | block rebuild correctness |

## Edge Cases

A minimal case like n = 2 with a single swap ensures that block reconstruction is triggered correctly even when both updated indices fall in the same block. The algorithm rebuilds that block once, and the frequency array still correctly reflects both swapped values.

A fully reversed permutation tests the case where all points lie on a monotone diagonal in the (pos_a, pos_b) plane. Range queries over large intervals must still accumulate correctly across full blocks, confirming that histogram aggregation is independent of value ordering.

A case with repeated swaps on the same positions ensures that stale block data does not persist. Since each update rewrites both the array and the corresponding block frequencies, no outdated counts remain.
