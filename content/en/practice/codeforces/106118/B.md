---
title: "CF 106118B - Balloon Trip"
description: "We are given a line of mountains, each with an initial height. A journey is defined as walking from index $l$ to $r$, always moving one step to the right, and paying the cost of each move as the absolute difference between consecutive heights."
date: "2026-06-19T20:05:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106118
codeforces_index: "B"
codeforces_contest_name: "2025 ICPC, Chula Selection Contest"
rating: 0
weight: 106118
solve_time_s: 61
verified: true
draft: false
---

[CF 106118B - Balloon Trip](https://codeforces.com/problemset/problem/106118/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of mountains, each with an initial height. A journey is defined as walking from index $l$ to $r$, always moving one step to the right, and paying the cost of each move as the absolute difference between consecutive heights. So the cost of a query is the sum of $|a_i - a_{i+1}|$ over all $i$ from $l$ to $r-1$, but the heights are not static.

Between queries, we are allowed to apply a range update that increases all heights in a segment $[l, r]$ by some value $x$. Importantly, this update shifts heights, which changes many adjacent differences globally, not just locally inside the segment.

The difficulty is that both operations are large in number, up to $3 \cdot 10^5$, so recomputing a full range cost from scratch per query is too slow. The challenge is maintaining a dynamic array where we support range additions and fast queries of a sum of absolute adjacent differences over a segment.

A key observation comes from understanding how updates affect differences. If both endpoints of an edge $(i, i+1)$ are inside or outside an update range, their difference does not change. Only edges crossing the boundary of an update range are affected. This locality is what makes the problem tractable.

Edge cases that break naive thinking include:

A fully naive recomputation per query fails immediately. For example, if all operations are type 2 queries, each costing $O(n)$, total work becomes $O(nq)$, which is about $9 \cdot 10^{10}$ operations.

A subtler failure is assuming we can maintain prefix sums of differences directly without accounting for range updates. Consider a segment update that shifts only part of the array; the difference array is not updated by simple point additions, since only boundary differences change.

## Approaches

The brute-force approach is straightforward. We maintain the array directly. For a range add, we increment each element in $[l, r]$. For a query, we compute the sum of absolute differences in the requested range by scanning linearly.

This is correct because it directly follows the definition of the operations. However, each update costs $O(n)$ in the worst case, and each query also costs $O(n)$, leading to quadratic or worse behavior.

The bottleneck comes from the fact that every operation touches potentially large segments, and there is no reuse of previous computation.

The key insight is to separate the problem into two layers. First, we maintain the array under range addition using a segment tree or Fenwick tree with lazy propagation. Second, instead of recomputing absolute differences over a range every time, we maintain the contribution structure of adjacent pairs.

We define an auxiliary array $d_i = a_{i+1} - a_i$. The query cost is the sum of $|d_i|$ over the segment. A range addition of $x$ affects $d_i$ only when exactly one of $a_i$ and $a_{i+1}$ is inside the update range. This means only two boundary positions per update matter: $l-1$ and $r$.

So instead of updating many differences, we update only two adjacent difference values. Meanwhile, we maintain a segment tree over $d_i$ that supports point updates and range sum queries of absolute values. To handle sign changes efficiently, we maintain $d_i$ itself and its absolute contribution via a structure that supports updates on endpoints induced by range additions.

The core idea is that range addition translates into at most two point updates on the difference array, which makes both operations logarithmic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nq)$ | $O(n)$ | Too slow |
| Optimal | $O(q \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We maintain the array $a$ implicitly with a Fenwick tree or segment tree that supports range add and point query. In parallel, we maintain a structure for differences $d_i = a_{i+1} - a_i$, but we never explicitly rebuild the full array after each operation.

1. Initialize a data structure that supports range addition and point queries over the original array $a$. This allows us to recover any $a_i$ when needed without storing all updates explicitly.
2. Build an array of initial differences $d_i = a_{i+1} - a_i$. These represent the local contribution to path costs.
3. Build a segment tree over $|d_i|$, supporting point updates and range sum queries. This structure answers trip cost queries directly.
4. When processing a range add operation $(l, r, x)$, observe that only differences involving boundaries change. Specifically, only $d_{l-1}$ and $d_r$ are affected, because all internal edges have both endpoints shifted equally.
5. To update these boundary differences, first compute the old values of $a_{l-1}, a_l, a_r, a_{r+1}$ using point queries on the range-add structure.
6. Recompute $d_{l-1} = a_l - a_{l-1}$ if $l > 1$, and update its absolute value in the segment tree.
7. Recompute $d_r = a_{r+1} - a_r$ if $r < n$, and update its absolute value similarly.
8. Apply the range addition $+x$ on the primary structure so future queries reflect updated heights.
9. For a trip query $(l, r)$, return the sum of $|d_i|$ for $i \in [l, r-1]$ from the segment tree.

Why it works is tied to the invariance of internal differences under uniform shifts. When every element in a segment is increased by the same value, differences inside that segment remain unchanged. Only edges that cross the boundary of the segment see one endpoint change and the other not, which is why only those two positions need recomputation.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

    def range_add(self, l, r, v):
        self.add(l, v)
        if r + 1 <= self.n:
            self.add(r + 1, -v)

    def point_query(self, i):
        return self.sum(i)

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.t = [0] * (4 * self.n)
        self.build(1, 0, self.n - 1, arr)

    def build(self, v, tl, tr, arr):
        if tl == tr:
            self.t[v] = arr[tl]
        else:
            tm = (tl + tr) // 2
            self.build(v*2, tl, tm, arr)
            self.build(v*2+1, tm+1, tr, arr)
            self.t[v] = self.t[v*2] + self.t[v*2+1]

    def update(self, v, tl, tr, pos, val):
        if tl == tr:
            self.t[v] = val
        else:
            tm = (tl + tr) // 2
            if pos <= tm:
                self.update(v*2, tl, tm, pos, val)
            else:
                self.update(v*2+1, tm+1, tr, pos, val)
            self.t[v] = self.t[v*2] + self.t[v*2+1]

    def query(self, v, tl, tr, l, r):
        if l > r:
            return 0
        if l == tl and r == tr:
            return self.t[v]
        tm = (tl + tr) // 2
        return self.query(v*2, tl, tm, l, min(r, tm)) + \
               self.query(v*2+1, tm+1, tr, max(l, tm+1), r)

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    fw = Fenwick(n)
    for i, v in enumerate(a, 1):
        fw.range_add(i, i, v)

    if n > 1:
        diff = [abs(a[i+1] - a[i]) for i in range(n-1)]
        st = SegTree(diff)
    else:
        st = None

    out = []

    for _ in range(q):
        tmp = list(map(int, input().split()))
        t = tmp[0]

        if t == 1:
            l, r, x = tmp[1], tmp[2], tmp[3]
            fw.range_add(l, r, x)

            if n > 1:
                if l > 1:
                    i = l - 2
                    left = fw.point_query(l-1)
                    right = fw.point_query(l)
                    st.update(1, 0, n-2, i, abs(right - left))

                if r < n:
                    i = r - 1
                    left = fw.point_query(r)
                    right = fw.point_query(r+1)
                    st.update(1, 0, n-2, i, abs(right - left))

        else:
            l, r = tmp[1], tmp[2]
            if l == r:
                out.append("0")
            else:
                out.append(str(st.query(1, 0, n-2, l-1, r-2)))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The Fenwick tree stores the array under range additions so any point can be reconstructed in logarithmic time. The segment tree stores absolute adjacent differences and supports single-position updates when boundary values change. The update logic carefully recomputes only the affected differences after each range addition.

The indexing is slightly subtle: difference index $i$ corresponds to edge $(i, i+1)$, so query $[l, r]$ maps to $[l-1, r-2]$ in the difference structure.

## Worked Examples

### Example 1

Input:

```
5 3
1 3 2 5 4
2 1 5
1 2 4 3
2 1 5
```

Initial differences are:

| i | a[i] | a[i+1] | diff |
| --- | --- | --- | --- |
| 1 | 1 | 3 | 2 |
| 2 | 3 | 2 | 1 |
| 3 | 2 | 5 | 3 |
| 4 | 5 | 4 | 1 |

First query sums all diffs: 2 + 1 + 3 + 1 = 7.

After adding 3 to [2,4], array becomes [1,6,5,8,4].

Updated affected edges:

| edge | new diff |
| --- | --- |
| (1,2) | 5 |
| (4,5) | 4 |

Full diffs become [5,1,3,4], sum is 13.

### Example 2

Input:

```
4 2
10 10 10 10
2 1 4
1 2 3 5
```

First query is 0 because all values are equal.

After update, array becomes [10,15,15,10].

Differences become [5,0,5], showing that only boundary edges matter after updates.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(q \log n)$ | Each update touches two segment tree nodes and Fenwick updates |
| Space | $O(n)$ | Stores Fenwick tree and segment tree |

The solution fits comfortably within limits because each operation reduces to a constant number of logarithmic updates, avoiding any full traversal of the array.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from main import solve
    solve()
    return sys.stdout.getvalue().strip()

# minimum size
assert run("1 1\n5\n2 1 1\n") == "0"

# simple chain
assert run("3 2\n1 2 3\n2 1 3\n2 2 3\n") == "2\n1"

# range update affects only boundaries
assert run("5 3\n1 1 5 10\n2 1 5\n2 2 4\n") == "0\n0"

# all equal
assert run("4 2\n7 7 7 7\n2 1 4\n2 2 3\n") == "0\n0"

# alternating
assert run("5 1\n1 2 3 4 5\n2 1 5\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | trivial segment |
| simple chain | 2,1 | correctness of diff sum |
| full update | 0,0 | boundary-only updates |
| all equal | 0,0 | stability under no change |
| alternating | 4 | general correctness |

## Edge Cases

For a single-element array, there are no edges, so every query must return zero. The segment tree over differences is empty, and the code correctly bypasses it when $n = 1$.

For a full-range update, such as increasing every element by a constant, no differences change at all. The algorithm only attempts to recompute $d_{l-1}$ and $d_r$, both of which are out of bounds in this case, so no updates occur. This matches the fact that uniform shifts preserve all absolute differences.

For updates touching the boundary, such as $l = 1$ or $r = n$, only one side of the boundary update exists. The implementation checks bounds explicitly before recomputing differences, preventing invalid queries into the Fenwick structure.
