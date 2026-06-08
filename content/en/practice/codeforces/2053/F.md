---
title: "CF 2053F - Earnest Matrix Complement"
description: "For a row $i$, let: - $zi$ = number of -1 cells in that row. - $cnti(u)$ = number of already fixed occurrences of value $u$. Suppose we decide that every blank in row $i$ is filled with the same value $pi$. This is not a restriction."
date: "2026-06-08T08:26:49+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "dp", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 2053
codeforces_index: "F"
codeforces_contest_name: "Good Bye 2024: 2025 is NEAR"
rating: 2600
weight: 2053
solve_time_s: 80
verified: true
draft: false
---

[CF 2053F - Earnest Matrix Complement](https://codeforces.com/problemset/problem/2053/F)

**Rating:** 2600  
**Tags:** brute force, data structures, dp, greedy, implementation, math  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Key Observation

For a row $i$, let:

- $z_i$ = number of `-1` cells in that row.
- $cnt_i(u)$ = number of already fixed occurrences of value $u$.

Suppose we decide that every blank in row $i$ is filled with the same value $p_i$.

This is not a restriction. Because the beauty expression is linear in the counts of the row, any optimal distribution of the $z_i$ blanks can be moved entirely onto a single value that gives the largest coefficient.

So each row is represented by a single chosen value $p_i$.

The final count of value $u$ in row $i$ becomes

$$c_{u,i}=cnt_i(u)+
\begin{cases}
z_i,&u=p_i\\
0,&u\neq p_i
\end{cases}$$

## Contribution of Two Adjacent Rows

For rows $i-1$ and $i$,

$$\sum_u c_{u,i-1}c_{u,i}$$

expands to

$$C_i
+z_{i-1}\,cnt_i(p_{i-1})
+z_i\,cnt_{i-1}(p_i)
+z_{i-1}z_i[p_{i-1}=p_i]$$

where

$$C_i=\sum_u cnt_{i-1}(u)\,cnt_i(u)$$

is a constant independent of the choices.

Define

$$dp_i(v)$$

as the maximum beauty considering rows $1\dots i$ when row $i$ chooses value $v$.

Then

$$dp_i(v)
=
C_i
+
z_i\,cnt_{i-1}(v)
+
\max_p
\Big(
dp_{i-1}(p)
+
z_{i-1}\,cnt_i(p)
+
z_{i-1}z_i[p=v]
\Big)$$

Let

$$A(p)=dp_{i-1}(p)+z_{i-1}cnt_i(p).$$

Then

$$dp_i(v)
=
C_i
+
z_i cnt_{i-1}(v)
+
\max
\Big(
\max_p A(p),
A(v)+z_{i-1}z_i
\Big).$$

This is the crucial simplification.

## Data Structure

For every row transition we need:

$$A(v)$$

for all $v$, and

$$\max_v A(v).$$

Most values never appear in a row. Only values occurring in the current row or previous row matter.

The standard accepted solution stores DP values over all $1\ldots k$ in a lazy segment tree supporting:

- range add,
- point add,
- range chmax with a global value,
- global maximum query.

The transition from row $i-1$ to row $i$ can then be implemented exactly as in the accepted Codeforces solutions in

$$O((\text{distinct values in row }i)+
(\text{distinct values in row }i-1))
\log k.$$

Since the total number of matrix cells over all test cases is at most $6\cdot10^5$, the overall complexity is

$$O((nm)\log k),$$

which fits comfortably within the limits.

## Accepted Python 3 Solution

```python
import sys
input = sys.stdin.readline

class SegTree:
    def __init__(self, n):
        self.n = n
        m = 4 * n + 5
        self.mx = [0] * m
        self.add = [0] * m
        self.tagmax = [0] * m

    def _apply(self, p, addv, maxv):
        self.mx[p] = max(self.mx[p] + addv, maxv)
        self.tagmax[p] = max(self.tagmax[p] + addv, maxv)
        self.add[p] += addv

    def _push(self, p):
        if self.add[p] != 0 or self.tagmax[p] != 0:
            a = self.add[p]
            m = self.tagmax[p]
            self._apply(p * 2, a, m)
            self._apply(p * 2 + 1, a, m)
            self.add[p] = 0
            self.tagmax[p] = 0

    def modify(self, p, l, r, ql, qr, addv, maxv):
        if ql <= l and r <= qr:
            self._apply(p, addv, maxv)
            return

        self._push(p)
        mid = (l + r) >> 1

        if ql <= mid:
            self.modify(p * 2, l, mid, ql, qr, addv, maxv)
        if qr > mid:
            self.modify(p * 2 + 1, mid + 1, r, ql, qr, addv, maxv)

        self.mx[p] = max(self.mx[p * 2], self.mx[p * 2 + 1])

    def clear(self):
        self.mx[:] = [0] * len(self.mx)
        self.add[:] = [0] * len(self.add)
        self.tagmax[:] = [0] * len(self.tagmax)

t = int(input())

for _ in range(t):
    n, m, k = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(n)]

    seg = SegTree(k)

    prev = {}

    for row in a:
        cur = {}

        for x in row:
            cur[x] = cur.get(x, 0) + 1

        z_prev = prev.get(-1, 0)
        z_cur = cur.get(-1, 0)

        for v, c in cur.items():
            if v != -1:
                seg.modify(1, 1, k, v, v, z_prev * c, 0)

        best = seg.mx[1]

        seg.modify(1, 1, k, 1, k, z_prev * z_cur, 0)
        seg.modify(1, 1, k, 1, k, 0, best)

        for v, c in cur.items():
            if v != -1:
                seg.modify(1, 1, k, 1, k, prev.get(v, 0) * c, 0)

        for v, c in prev.items():
            if v != -1:
                seg.modify(1, 1, k, v, v, z_cur * c, 0)

        prev = cur

    print(seg.mx[1])
```

This is the standard accepted DP + lazy segment tree implementation derived from the transition above.
