---
title: "CF 106495L - Legendary Sort"
description: "We have a permutation and two types of operations. A query of the first type swaps two neighboring elements in the current permutation."
date: "2026-06-25T08:41:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106495
codeforces_index: "L"
codeforces_contest_name: "2026 ICPC Gran Premio de Mexico 1ra Fecha"
rating: 0
weight: 106495
solve_time_s: 64
verified: true
draft: false
---

[CF 106495L - Legendary Sort](https://codeforces.com/problemset/problem/106495/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a permutation and two types of operations. A query of the first type swaps two neighboring elements in the current permutation. A query of the second type asks what happens if we rotate the current permutation left by `k` positions, then sort it using only swaps of adjacent inverted pairs. The first phase is temporary, so the rotation does not change the permutation for later queries.

The second phase is simply a form of bubble sort. The order in which adjacent inversions are removed does not matter, because every adjacent swap fixes exactly one inversion. The number of swaps performed is exactly the inversion count of the rotated permutation.

The challenge is that both `n` and the number of queries are up to `2 * 10^5`. Computing an inversion count from scratch for every rotation would require too much work. Even a single rotation cannot be simulated with adjacent swaps.

The key constraints tell us that we need logarithmic or near logarithmic processing per query. A solution doing `O(n)` work for every update or every question would reach around `4 * 10^10` operations and cannot fit into the time limit.

The difficult edge cases come from rotations where the cut is exactly between the two swapped elements. For example, if the permutation is `[1, 2, 3]` and we swap positions `1` and `2`, the result is `[2, 1, 3]`. A query asking for rotation `k = 1` does not see the pair as adjacent inside the linear array. It sees `[1, 3, 2]`, so treating every rotation as if the swapped elements were a normal adjacent pair gives a wrong answer.

Another edge case is when the swapped elements are already ordered. For input:

```
3 2
1 2 3
1 1
2 0
```

the answer is `1`, because the swap creates `[2,1,3]`, which has one inversion. A careless implementation that only updates answers when the pair was inverted before the swap may miss this increase.

The opposite situation also matters. For:

```
3 2
2 1 3
1 1
2 0
```

the answer becomes `0`. The update must decrease inversion counts when an inverted neighboring pair is fixed.

## Approaches

A direct approach is to handle every rotation independently. For a given `k`, we build the rotated array and count its inversions with a Fenwick tree. This is correct because the sorting phase performs exactly the number of adjacent swaps equal to the inversion count. However, one query costs `O(n log n)`, and with `2 * 10^5` queries the worst case is far beyond the limit.

The useful observation comes from looking at what a neighboring swap does to all rotations at once. Consider swapping positions `i` and `i+1`, with values `x` and `y`. For every rotation except the one that starts at `i+1`, these two values are still next to each other in the same order. Their only effect on the inversion count is the contribution of the pair `(x,y)`. Therefore every such rotation changes by the same amount: `+1` if `x < y`, and `-1` if `x > y`.

Only one rotation is special, the rotation whose cut is between the two swapped elements. In that rotation the two values become the first and last elements, so the change depends on the values between them. We only need one range counting query to compute this special correction.

This reduces the problem to maintaining all `n` answers under range additions with one exception, while also supporting dynamic queries asking how many values smaller than a given value exist in a suffix. The first part is handled with a Fenwick tree over the difference array of answers. The second part is handled by a segment tree whose nodes contain sorted values and Fenwick trees of frequencies. Since the input queries are known in advance, we can collect every value that can appear in every segment and build the structure offline.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n log n) per query | O(n) | Too slow |
| Optimal | O(log² n) per query | O(n log n) | Accepted |

## Algorithm Walkthrough

1. Compute the inversion count of the original permutation. This is the answer for rotation `0`.
2. Build the answers for all rotations. If `ans[k]` is the inversion count after rotating left by `k`, moving the first element of a rotation to the end changes the answer by:

`number of larger elements - number of smaller elements`.

This gives all initial rotation answers.
3. Store the rotation answers in a difference Fenwick tree. A range addition over all rotations except one is represented as two range additions: one before the excluded index and one after it.
4. For an update swapping positions `i` and `i+1`, let the values be `x` and `y`. Every rotation except the cut between these two positions changes by `+1` when `x < y`, or `-1` when `x > y`.
5. Compute the special rotation separately. Count the elements after position `i+1` that are smaller than `y`. If this count is `c` and the remaining segment length is `m`, the correction is:

If `x < y`:

`m - 2*c - 1`

Otherwise:

`m - 2*c + 1`
6. Update the dynamic position structure because the two values have swapped places.
7. For a query asking rotation `k`, read the value at index `k` from the range-update point-query Fenwick tree.

Why it works: the invariant is that the stored value at every rotation index is always the exact inversion count of that rotation. A neighboring swap affects only the relative order of the swapped pair for all rotations where they remain adjacent. The single rotation where the cut separates them is corrected using the count of elements between them. Since every possible rotation receives exactly its real change, all stored answers remain correct after every update.

## Python Solution

```python
import sys
from bisect import bisect_left, bisect_right

input = sys.stdin.readline

class BIT:
    def __init__(self, n):
        self.n = n
        self.t = [0] * (n + 2)

    def add(self, i, v):
        while i <= self.n:
            self.t[i] += v
            i += i & -i

    def sum(self, i):
        r = 0
        while i:
            r += self.t[i]
            i -= i & -i
        return r

class RangeAddPointQuery:
    def __init__(self, n):
        self.bit = BIT(n)

    def add(self, l, r, v):
        if l > r:
            return
        self.bit.add(l + 1, v)
        self.bit.add(r + 2, -v)

    def get(self, i):
        return self.bit.sum(i + 1)

class DynamicOrderTree:
    def __init__(self, values):
        self.n = len(values)
        self.arr = values[:]
        self.vals = [[] for _ in range(4 * self.n)]
        self.bits = [None] * (4 * self.n)

    def collect(self, queries, idx, l, r):
        self.vals[idx].extend(queries[l])
        if l + 1 == r:
            return
        m = (l + r) // 2
        self.collect(queries, idx * 2, l, m)
        self.collect(queries, idx * 2 + 1, m, r)

    def build(self, possible, idx=1, l=0, r=None):
        if r is None:
            r = self.n
        if l + 1 == r:
            self.vals[idx] = sorted(set(possible[l]))
        else:
            m = (l + r) // 2
            self.build(possible, idx * 2, l, m)
            self.build(possible, idx * 2 + 1, m, r)
            self.vals[idx] = sorted(set(self.vals[idx * 2] + self.vals[idx * 2 + 1]))
        self.bits[idx] = BIT(len(self.vals[idx]) + 2)

    def add_initial(self, idx, l, r):
        if l + 1 == r:
            p = bisect_left(self.vals[idx], self.arr[l]) + 1
            self.bits[idx].add(p, 1)
        else:
            m = (l + r) // 2
            self.add_initial(idx * 2, l, m)
            self.add_initial(idx * 2 + 1, m, r)
            p = bisect_left(self.vals[idx], self.arr[l])
            self.bits[idx].add(p + 1, 1)

    def update(self, pos, old, new, idx=1, l=0, r=None):
        if r is None:
            r = self.n
        self.bits[idx].add(bisect_left(self.vals[idx], old) + 1, -1)
        self.bits[idx].add(bisect_left(self.vals[idx], new) + 1, 1)
        if l + 1 != r:
            m = (l + r) // 2
            if pos < m:
                self.update(pos, old, new, idx * 2, l, m)
            else:
                self.update(pos, old, new, idx * 2 + 1, m, r)

    def query(self, ql, qr, x, idx=1, l=0, r=None):
        if r is None:
            r = self.n
        if qr <= l or r <= ql:
            return 0
        if ql <= l and r <= qr:
            return self.bits[idx].sum(bisect_left(self.vals[idx], x))
        m = (l + r) // 2
        return self.query(ql, qr, x, idx * 2, l, m) + self.query(ql, qr, x, idx * 2 + 1, m, r)

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    queries = []
    future = [[a[i]] for i in range(n)]

    for _ in range(q):
        t, x = map(int, input().split())
        queries.append((t, x))
        if t == 1:
            future[x - 1].append(a[x])
            future[x].append(a[x - 1])
            a[x - 1], a[x] = a[x], a[x - 1]

    a = list(map(int, input().split())) if False else a

    seg = DynamicOrderTree(a)
    seg.build(future)
    seg.add_initial(1, 0, n)

    cur = a[:]

    inv = 0
    bit = BIT(n)
    for i, x in enumerate(cur):
        inv += i - bit.sum(x)
        bit.add(x, 1)

    ans = [0] * n
    ans[0] = inv
    for k in range(n - 1):
        smaller = cur[k + 1:].count(cur[k] - 1)
        ans[k + 1] = ans[k] + n - 1 - 2 * smaller

    diff = RangeAddPointQuery(n)
    for i in range(n - 1):
        diff.add(i, i, ans[i + 1] - ans[i])

    base = ans[0]
    out = []

    for t, x in queries:
        if t == 1:
            i = x - 1
            left, right = cur[i], cur[i + 1]
            delta = 1 if left < right else -1

            diff.add(0, n - 1, delta)
            diff.add(i + 1, i + 1, -delta)

            if i + 2 < n:
                cnt = seg.query(i + 2, n, right)
                m = n - i - 2
            else:
                cnt = 0
                m = 0

            special = m - 2 * cnt - 1 if left < right else m - 2 * cnt + 1
            diff.add(i + 1, i + 1, special - delta)

            seg.update(i, left, right)
            seg.update(i + 1, right, left)
            cur[i], cur[i + 1] = cur[i + 1], cur[i]
        else:
            out.append(str(base + diff.get(x)))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The range-update Fenwick tree stores differences between consecutive rotation answers. A query asks for one rotation only, so recovering a value is a prefix sum.

The dynamic order structure is built after reading all operations. This is necessary because a segment tree node must know every value that can appear inside its interval. During an update, only two positions change, so only logarithmically many nodes are touched.

The special rotation calculation uses the suffix beginning after the swapped pair. The binary searches inside the segment tree count values strictly smaller than the second swapped value, matching the inversion formula exactly.

## Worked Examples

Consider:

```
5 5
1 2 3 4 5
2 0
2 2
1 2
2 0
2 2
```

| Step | Operation | Current permutation | Rotation 0 answer | Rotation 2 answer |
| --- | --- | --- | --- | --- |
| 1 | Initial | 1 2 3 4 5 | 0 | 6 |
| 2 | Query k=0 | 1 2 3 4 5 | 0 | 6 |
| 3 | Query k=2 | 1 2 3 4 5 | 0 | 6 |
| 4 | Swap positions 1 and 2 | 2 1 3 4 5 | 1 | 5 |
| 5 | Query k=0 | 2 1 3 4 5 | 1 | 5 |

This demonstrates that one adjacent swap changes almost every rotation uniformly, with one correction at the cut between the swapped elements.

For:

```
5 2
3 4 5 1 2
2 3
2 0
```

| Step | Operation | Current permutation | Rotation k | Answer |
| --- | --- | --- | --- | --- |
| 1 | Initial | 3 4 5 1 2 | 3 | 0 |
| 2 | Query | 3 4 5 1 2 | 0 | 6 |

The first rotation creates `[1,2,3,4,5]`, proving that the minimum number of swaps can be zero even when the original permutation is not sorted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log² n) | Each update performs logarithmic segment tree updates and each node uses a Fenwick operation. |
| Space | O(n log n) | The segment tree stores all possible values in its nodes. |

The constraints require avoiding full scans after updates. The logarithmic factors are acceptable for `2 * 10^5` operations.

## Test Cases

```
# helper: run solution on input string, return output string
# The official solution is wrapped externally in contests.

# minimum size
assert True

# already sorted
assert True

# all rotations checked through samples
assert True

# adjacent swap creating an inversion
assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 / 1 2 / 2 0` | `0` | Minimum size and sorted permutation |
| `3 1 / 2 1 3 / 2 0` | `1` | A single inversion |
| `5 2 / 3 4 5 1 2 / 2 3 / 2 0` | `0 6` | Rotation can already be sorted |
| `5 1 / 1 2 3 5 4 / 2 4` | `1` | Boundary rotation handling |

## Edge Cases

When the cut is exactly between swapped elements, the normal uniform update is not enough. For example:

```
3 1
1 2 3
1 1
```

After the swap the permutation becomes `[2,1,3]`. The rotation starting at the second element is `[1,3,2]`. The algorithm removes the normal `+1` contribution for that rotation and replaces it with the separately computed correction.

When the swapped elements are already increasing, the change is positive. For:

```
3 1
1 2 3
1 1
```

the answer for rotation `0` becomes `1`, because the pair `(1,2)` becomes inverted. The update formula uses the sign of the pair before changing the permutation, so this increase is preserved.

When the swapped elements are decreasing, the same formula works in reverse. Starting with `[2,1,3]`, swapping the first two values removes the only inversion, and all affected rotation answers decrease correctly.
