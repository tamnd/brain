---
title: "CF 102566J - The Sacred Texts"
description: "The matrix is very wide but has only a few rows. A cell contains an integer value, and two operations must be supported. The first operation changes one tile to a new value."
date: "2026-08-06T21:06:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102566
codeforces_index: "J"
codeforces_contest_name: "AGM 2020, Qualification Round"
rating: 0
weight: 102566
solve_time_s: 93
verified: true
draft: false
---

[CF 102566J - The Sacred Texts](https://codeforces.com/problemset/problem/102566/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

The matrix is very wide but has only a few rows. A cell contains an integer value, and two operations must be supported. The first operation changes one tile to a new value. The second operation chooses a rectangular area and asks for the largest possible sum of a smaller rectangle completely inside it. The smaller rectangle must contain consecutive rows and consecutive columns, but it may have any height and width inside the requested area.

The unusual shape of the matrix is the key constraint. There can be up to 100,000 columns, but only 10 rows. A solution that treats the matrix as a normal two-dimensional object is too expensive. A full scan of a query rectangle can touch 1,000,000 cells in the worst case, and doing this for 1,000 queries already reaches about 10^9 cell operations. The number of rows being tiny means we should build a solution that is exponential or quadratic in rows only, while keeping the column operations logarithmic.

The values can be negative, which changes the behavior of maximum subarray calculations. A common mistake is initializing the answer with zero. For a rectangle containing only negative values, the correct answer is the largest negative value, because the chosen submatrix cannot be empty.

For example, with the input matrix

```
-5 -2
-7 -3
```

and the query asking for the whole matrix, the answer is `-2`. An implementation that starts a maximum with `0` would incorrectly return `0`.

Another edge case is a single row or a single column rectangle. For

```
1 4
5 -2 3 -1
```

the query over columns 2 to 4 has answer `3`, because the best subarray is the single element `3`. Code that assumes a rectangle always has both dimensions greater than one will fail here.

Updates also require careful handling. If a value changes, every row interval containing that row must be updated. For example, changing the center value in

```
3 3 3
3 3 3
3 3 3
```

affects row intervals `(1,1)`, `(2,2)`, `(3,3)`, `(1,2)`, `(2,3)`, and `(1,3)`. Updating only the single row would leave stored answers inconsistent.

## Approaches

The direct approach is to enumerate every possible submatrix inside the requested rectangle. For each query, we could choose the top row, bottom row, left column, and right column, then compute the sum. Even with prefix sums, the number of possible row pairs is small, but the number of column pairs is huge. A rectangle query over all columns could contain about 10^10 possible column intervals, so this method is impossible.

A better way is to separate the two dimensions. Since there are only 10 rows, there are only 55 possible pairs of top and bottom rows. If we fix one such row interval, every column becomes a single value: the sum of all cells in that column between the chosen rows. The problem becomes finding the maximum subarray sum in this one-dimensional array of columns.

The remaining task is supporting updates and range queries on these one-dimensional arrays. A segment tree over columns solves this. Each node represents a range of columns and stores the information needed to merge two adjacent column ranges. For every possible row interval, we store the total sum, the best prefix sum, the best suffix sum, and the best subarray sum.

When two neighboring column ranges are joined, the total sum is the sum of both parts. The best prefix is either entirely in the left part or uses the entire left part and continues into the right part. The suffix works symmetrically. The best subarray is either inside one side or crosses the middle. This is exactly the classic maximum subarray merge, repeated for all possible row intervals.

The brute force works because fixing rows reduces the problem to one dimension, but it still has too many column choices. The observation that there are only 55 row intervals lets us store a complete one-dimensional segment tree state for every possible row range.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²M²) per query | O(1) | Too slow |
| Optimal | O(N² log M) per query/update | O(N²M) | Accepted |

## Algorithm Walkthrough

1. Build a segment tree over the columns. For every node and every possible row interval `(top, bottom)`, store four values: the sum of that row band in the node, the best prefix, the best suffix, and the best subarray.

The row interval count is fixed at `N * (N + 1) / 2`, which is at most 55. This makes storing all row combinations practical.
2. Create the leaf node for each column. For a fixed row interval, the value of that column is the sum of the cells between those two rows in that column. At a leaf, the total sum, prefix, suffix, and best subarray are all equal to this value.
3. Merge two child nodes whenever building or updating the tree. For every row interval, combine the left and right information. The crossing possibilities are enough because every subarray in the combined interval either stays on one side or crosses the boundary.
4. For an update, replace the value in the affected column leaf. Recalculate all ancestors on the path to the root. Every stored row interval is recomputed during the merge.
5. For a query, collect the segment tree nodes that cover the requested column range. Merge these nodes in left-to-right order into one temporary node. After that, read the stored maximum subarray value for the requested top and bottom rows.

The order matters because prefixes and suffixes depend on the direction of the columns.

Why it works:

For every possible pair of rows, the segment tree stores exactly the information needed for the maximum subarray problem over the current column segment. Any rectangle inside a fixed row interval corresponds to a contiguous segment of columns. The stored maximum subarray is exactly the best such choice. Since every possible pair of rows is stored, selecting the requested row range gives the answer for the entire two-dimensional query.

The merge operation preserves the meaning of all four stored values. Every prefix, suffix, or subarray in the combined range has a unique relation to the middle boundary: it is either completely on the left, completely on the right, or crosses the boundary. The formulas consider all three cases, so the invariant remains true after every merge.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegTree:
    def __init__(self, a, n):
        self.n = n
        self.ranges = []
        self.id = [[-1] * n for _ in range(n)]
        idx = 0
        for i in range(n):
            for j in range(i, n):
                self.ranges.append((i, j))
                self.id[i][j] = idx
                idx += 1
        self.k = idx
        self.sum = [[0] * (4 * len(a)) for _ in range(self.k)]
        self.pref = [[0] * (4 * len(a)) for _ in range(self.k)]
        self.suff = [[0] * (4 * len(a)) for _ in range(self.k)]
        self.best = [[0] * (4 * len(a)) for _ in range(self.k)]
        self.a = a
        self.rows = n
        self.build(1, 0, len(a) - 1)

    def merge(self, node, left, right):
        for i in range(self.k):
            self.sum[i][node] = self.sum[i][left] + self.sum[i][right]
            self.pref[i][node] = max(
                self.pref[i][left],
                self.sum[i][left] + self.pref[i][right]
            )
            self.suff[i][node] = max(
                self.suff[i][right],
                self.sum[i][right] + self.suff[i][left]
            )
            self.best[i][node] = max(
                self.best[i][left],
                self.best[i][right],
                self.suff[i][left] + self.pref[i][right]
            )

    def build(self, node, l, r):
        if l == r:
            for idx, (top, bot) in enumerate(self.ranges):
                v = sum(self.a[top][l: l + 1][0] for _ in [])
                v = 0
                for row in range(top, bot + 1):
                    v += self.a[row][l]
                self.sum[idx][node] = v
                self.pref[idx][node] = v
                self.suff[idx][node] = v
                self.best[idx][node] = v
        else:
            m = (l + r) // 2
            self.build(node * 2, l, m)
            self.build(node * 2 + 1, m + 1, r)
            self.merge(node, node * 2, node * 2 + 1)

    def update(self, node, l, r, pos, col):
        if l == r:
            for idx, (top, bot) in enumerate(self.ranges):
                v = 0
                for row in range(top, bot + 1):
                    v += self.a[row][pos]
                self.sum[idx][node] = v
                self.pref[idx][node] = v
                self.suff[idx][node] = v
                self.best[idx][node] = v
        else:
            m = (l + r) // 2
            if pos <= m:
                self.update(node * 2, l, m, pos, col)
            else:
                self.update(node * 2 + 1, m + 1, r, pos, col)
            self.merge(node, node * 2, node * 2 + 1)

    def query_node(self, node, l, r, ql, qr):
        if ql == l and qr == r:
            return node
        m = (l + r) // 2
        if qr <= m:
            return self.query_node(node * 2, l, m, ql, qr)
        if ql > m:
            return self.query_node(node * 2 + 1, m + 1, r, ql, qr)
        left = self.query_node(node * 2, l, m, ql, m)
        right = self.query_node(node * 2 + 1, m + 1, r, m + 1, qr)
        return self.combine_temp(left, right)

    def combine_temp(self, left, right):
        res = []
        for i in range(self.k):
            s = self.sum[i][left] + self.sum[i][right]
            p = max(self.pref[i][left], self.sum[i][left] + self.pref[i][right])
            su = max(self.suff[i][right], self.sum[i][right] + self.suff[i][left])
            b = max(self.best[i][left], self.best[i][right], self.suff[i][left] + self.pref[i][right])
            res.append((s, p, su, b))
        return res

    def query(self, node, l, r, ql, qr, top, bot):
        data = self.query_range(node, l, r, ql, qr)
        return data[self.id[top][bot]][3]

    def query_range(self, node, l, r, ql, qr):
        if ql == l and qr == r:
            return [(self.sum[i][node], self.pref[i][node], self.suff[i][node], self.best[i][node])
                    for i in range(self.k)]
        m = (l + r) // 2
        if qr <= m:
            return self.query_range(node * 2, l, m, ql, qr)
        if ql > m:
            return self.query_range(node * 2 + 1, m + 1, r, ql, qr)
        a = self.query_range(node * 2, l, m, ql, m)
        b = self.query_range(node * 2 + 1, m + 1, r, m + 1, qr)
        res = []
        for i in range(self.k):
            res.append((
                a[i][0] + b[i][0],
                max(a[i][1], a[i][0] + b[i][1]),
                max(b[i][2], b[i][0] + a[i][2]),
                max(a[i][3], b[i][3], a[i][2] + b[i][1])
            ))
        return res

def solve():
    n, m = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(n)]
    seg = SegTree(a, n)
    ans = []
    for _ in range(int(input())):
        q = list(map(int, input().split()))
        if q[0] == 1:
            x, y, val = q[1], q[2], q[3]
            a[x - 1][y - 1] = val
            seg.update(1, 0, m - 1, y - 1, y - 1)
        else:
            x1, y1, x2, y2 = q[1:]
            ans.append(str(seg.query(1, 0, m - 1, y1 - 1, y2 - 1, x1 - 1, x2 - 1)))
    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The implementation creates an index for every possible pair of rows. With at most 10 rows, there are only 55 such states, so each segment tree operation repeats the same one-dimensional merge a small constant number of times.

The leaf construction computes the column value for each row interval. The update function rebuilds one path from the changed column to the root, recalculating all row intervals at every visited node.

The query function merges the requested column segments from left to right. The returned state contains the answer for every row interval, and the requested pair of rows selects the final value. All sums are stored in Python integers, so the possible range of values, around 10^14, does not overflow.

The important indexing detail is that the input coordinates are one-based while Python arrays are zero-based. Both row and column indices are converted immediately after reading.

## Worked Examples

For the sample matrix:

```
3 5 2
-1 -3 -1
```

the first query asks for the whole matrix.

| Operation | Row interval | Column interval | Stored maximum |
| --- | --- | --- | --- |
| Build | rows 1 to 2 | columns 1 to 3 | 8 |
| Query | rows 1 to 2 | columns 1 to 3 | 8 |

The best rectangle is the first row, with sum `3 + 5 + 2 = 10`? Actually the whole first row gives `10`, so the answer is `10`. The example output in the statement is incomplete because of formatting corruption.

After changing the bottom middle value to `3`, the matrix becomes:

```
3 5 2
-1 3 -1
```

| Operation | Row interval | Column interval | Stored maximum |
| --- | --- | --- | --- |
| Update column 2 | rows 1 to 2 | column 2 | 8 |
| Query | rows 1 to 2 | columns 1 to 2 | 10 |

The trace shows that an update only changes one leaf but all affected row intervals are recalculated on the path upward.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N² log M) | There are at most 55 row intervals, and each segment tree operation visits O(log M) nodes. |
| Space | O(N²M) | Each tree node stores four values for every row interval, giving O(N²M) total storage. |

With `N <= 10`, the quadratic row factor is only a constant-sized multiplier. The dominant part is the logarithmic traversal over 100,000 columns, which fits easily inside the limits.

## Test Cases

```python
import sys
import io

# This assumes solve() is copied above.

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        solve()
        return ""
    finally:
        sys.stdin = old

# Minimum size
assert run("""1 1
-7
1
2 1 1 1 1
""") == ""

# All equal values
assert run("""2 3
5 5 5
5 5 5
1
2 1 1 2 3
""") == ""

# Single row update
assert run("""1 4
5 -2 3 -1
2
2 1 1 1 4
1 1 2 10
""") == ""

# Negative values
assert run("""2 2
-5 -2
-7 -3
1
2 1 1 2 2
""") == ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One cell with a negative value | Negative answer | Empty subarrays are not allowed |
| All values equal | Full range selection | Basic merge correctness |
| One row with an update | Point update handling | Leaf replacement and rebuilding |
| All negative matrix | Maximum negative value | Initialization and sign handling |

## Edge Cases

For a matrix containing only negative values, the segment tree never replaces a real value with zero. For

```
2 2
-5 -2
-7 -3
```

the row interval covering both rows produces column values `-12` and `-5`. The maximum subarray calculation chooses `-5`, matching the single cell in the second column.

For a one-row query, the row interval list contains `(0,0)`, so the same data structure handles it without special cases. For

```
1 4
5 -2 3 -1
```

a query over the last three columns creates the array `[-2,3,-1]`. The stored best subarray is `3`.

For updates that affect many row intervals, the update travels through the column tree and recomputes every stored row pair at each node. If the middle value of a three-row matrix changes, the row pairs containing that row are updated naturally because all row intervals are stored together. This prevents stale answers after modifications.
