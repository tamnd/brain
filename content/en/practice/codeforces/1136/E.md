---
title: "CF 1136E - Nastya Hasn't Written a Legend"
description: "We have an array a and another array k. The array always satisfies a monotonic-type constraint: $$a{i+1} ge ai + ki$$ for every adjacent pair. There are two operations. The first operation increases one position a[i] by some value x."
date: "2026-06-12T04:02:41+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 1136
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 546 (Div. 2)"
rating: 2200
weight: 1136
solve_time_s: 120
verified: true
draft: false
---

[CF 1136E - Nastya Hasn't Written a Legend](https://codeforces.com/problemset/problem/1136/E)

**Rating:** 2200  
**Tags:** binary search, data structures  
**Solve time:** 2m  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array `a` and another array `k`.

The array always satisfies a monotonic-type constraint:

$$a_{i+1} \ge a_i + k_i$$

for every adjacent pair.

There are two operations.

The first operation increases one position `a[i]` by some value `x`. After that increase, the constraint may become violated for the next element. If it does, we must raise `a[i+1]` to the minimum value that restores the constraint. That change may then force `a[i+2]` to increase, and so on. The update propagates to the right until the constraint becomes valid again.

The second operation asks for the sum of a contiguous segment.

The difficulty is that both `n` and the number of queries are up to `100000`. A single update can potentially affect almost the entire suffix of the array. Performing that propagation explicitly would require `O(n)` time per update, which becomes `O(nq)` in the worst case, roughly `10^10` operations. That is far beyond the limit.

The key challenge is to represent the propagated structure in a form where both updates and range sums can be handled in logarithmic time.

A subtle point is that updates never decrease any element. Once a position grows, it never becomes smaller later. This monotonicity is the reason an efficient data structure exists.

Another easy mistake is to think propagation stops immediately after changing one neighbor. Consider:

```
a = [5, 7, 9]
k = [3, 3]
```

After adding `2` to `a[1]`, we get:

```
a[1] = 7
```

Now:

```
a[2] < a[1] + 3
```

so `a[2]` becomes `10`.

Then:

```
a[3] < a[2] + 3
```

so `a[3]` becomes `13`.

The effect reaches the entire suffix.

Another dangerous case comes from negative values in `k`.

```
a = [10, 20]
k = [-100]
```

The constraint is

```
20 >= -90
```

which is already true.

Increasing `a[1]` slightly may still leave the constraint satisfied. A solution that assumes every update propagates at least one step would be incorrect.

A final trap is range sums after many overlapping updates. The actual array values are changing implicitly. If we only store update positions and forget the induced suffix modifications, later sum queries become wrong.

## Approaches

The brute-force solution follows the statement literally.

When we receive `+ i x`, we increase `a[i]`, then scan rightward. Whenever

$$a_{j+1} < a_j + k_j$$

we replace `a[j+1]` by `a_j + k_j`.

For a sum query we simply add the requested elements.

This is correct because it directly simulates the process. The problem is complexity. A single update may touch every remaining position. With `100000` updates, the worst case is about

$$100000 \times 100000 = 10^{10}$$

operations.

To find something faster, we need to understand the structure of the constraint.

Define a prefix sum array:

$$d_1 = 0$$

$$d_i = \sum_{j=1}^{i-1} k_j$$

Now define

$$b_i = a_i - d_i$$

The original condition

$$a_{i+1} \ge a_i + k_i$$

becomes

$$b_{i+1} \ge b_i$$

So after this transformation, the entire array `b` is simply nondecreasing.

What does an update do?

Increasing `a[i]` by `x` increases `b[i]` by `x`.

Then propagation enforces the nondecreasing property again. Every position to the right whose value is smaller than the new `b[i]` gets raised to exactly that value.

In other words, the update becomes:

"Add `x` at position `i`, then replace a maximal consecutive segment starting at `i` by one constant value."

Now the structure is much clearer.

Since `b` is always nondecreasing, we can find the last affected position with binary search. The update becomes a range assignment to one value. Range sums become weighted sums because

$$a_i = b_i + d_i.$$

The array `d` never changes, so its contribution can be precomputed. The dynamic part is entirely inside `b`.

We need a data structure supporting:

1. Range assignment to a constant.
2. Range sum queries.
3. Binary search on values in a nondecreasing array.

A lazy segment tree provides all three.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| Optimal | O(q log² n) | O(n) | Accepted |

## Algorithm Walkthrough

### Transformation

Let

$$d_1 = 0$$

and

$$d_i = k_1 + k_2 + \dots + k_{i-1}.$$

Define

$$b_i = a_i - d_i.$$

The given guarantee implies that `b` starts nondecreasing.

### Segment tree contents

The segment tree stores:

1. The sum of `b` on each segment.
2. The maximum value on each segment.
3. Lazy range-assignment tags.

The maximum lets us binary search for the end of an update range.

### Processing an update

Suppose we receive:

```
+ i x
```

1. Read the current value `b[i]`.
2. Set

$$v = b[i] + x.$$
3. Find the largest position `r` such that every element in `[i,r]` is strictly smaller than `v`.

Since `b` is nondecreasing, the affected positions form one contiguous segment.
4. Assign value `v` to the whole range `[i,r]`.

After assignment, the array remains nondecreasing.

### Processing a sum query

For

```
s l r
```

we need

$$\sum_{i=l}^{r} a_i.$$

Since

$$a_i=b_i+d_i,$$

we compute

$$\sum b_i$$

from the segment tree and

$$\sum d_i$$

from a static prefix-sum array.

Their sum is the answer.

### Why it works

The transformed array `b` is always nondecreasing. Increasing one element can only violate monotonicity to its right. Every position smaller than the new value must become exactly that value, and every larger position remains unchanged. Because the array is sorted, those affected positions form one contiguous interval. Assigning that interval to the new value reproduces exactly the propagation described in the statement.

The segment tree always stores the current `b` array, and every query computes

$$a_i=b_i+d_i$$

exactly. Since `d` never changes, reconstructing sums from the dynamic part `b` and static part `d` is correct for every operation.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr) - 1

        size = 4 * self.n + 5
        self.sum = [0] * size
        self.mx = [0] * size
        self.lazy = [None] * size

        self._build(1, 1, self.n, arr)

    def _build(self, v, tl, tr, arr):
        if tl == tr:
            val = arr[tl]
            self.sum[v] = val
            self.mx[v] = val
            return

        tm = (tl + tr) // 2
        self._build(v * 2, tl, tm, arr)
        self._build(v * 2 + 1, tm + 1, tr, arr)
        self._pull(v)

    def _pull(self, v):
        self.sum[v] = self.sum[v * 2] + self.sum[v * 2 + 1]
        self.mx[v] = max(self.mx[v * 2], self.mx[v * 2 + 1])

    def _apply(self, v, tl, tr, val):
        self.sum[v] = (tr - tl + 1) * val
        self.mx[v] = val
        self.lazy[v] = val

    def _push(self, v, tl, tr):
        if self.lazy[v] is None or tl == tr:
            return

        tm = (tl + tr) // 2
        val = self.lazy[v]

        self._apply(v * 2, tl, tm, val)
        self._apply(v * 2 + 1, tm + 1, tr, val)

        self.lazy[v] = None

    def assign(self, l, r, val):
        self._assign(1, 1, self.n, l, r, val)

    def _assign(self, v, tl, tr, l, r, val):
        if l > r:
            return

        if l == tl and r == tr:
            self._apply(v, tl, tr, val)
            return

        self._push(v, tl, tr)

        tm = (tl + tr) // 2

        self._assign(v * 2, tl, tm, l, min(r, tm), val)
        self._assign(v * 2 + 1, tm + 1, tr,
                     max(l, tm + 1), r, val)

        self._pull(v)

    def query_sum(self, l, r):
        return self._query_sum(1, 1, self.n, l, r)

    def _query_sum(self, v, tl, tr, l, r):
        if l > r:
            return 0

        if l == tl and r == tr:
            return self.sum[v]

        self._push(v, tl, tr)

        tm = (tl + tr) // 2

        return (
            self._query_sum(v * 2, tl, tm, l, min(r, tm))
            + self._query_sum(v * 2 + 1, tm + 1, tr,
                              max(l, tm + 1), r)
        )

    def query_point(self, pos):
        return self._query_point(1, 1, self.n, pos)

    def _query_point(self, v, tl, tr, pos):
        if tl == tr:
            return self.mx[v]

        self._push(v, tl, tr)

        tm = (tl + tr) // 2

        if pos <= tm:
            return self._query_point(v * 2, tl, tm, pos)
        return self._query_point(v * 2 + 1, tm + 1, tr, pos)

    def first_ge(self, l, value):
        return self._first_ge(1, 1, self.n, l, value)

    def _first_ge(self, v, tl, tr, l, value):
        if tr < l or self.mx[v] < value:
            return -1

        if tl == tr:
            return tl

        self._push(v, tl, tr)

        tm = (tl + tr) // 2

        res = self._first_ge(v * 2, tl, tm, l, value)
        if res != -1:
            return res

        return self._first_ge(v * 2 + 1, tm + 1, tr, l, value)

def solve():
    n = int(input())

    a = list(map(int, input().split()))
    k = list(map(int, input().split()))

    d = [0] * (n + 1)

    for i in range(2, n + 1):
        d[i] = d[i - 1] + k[i - 2]

    b = [0] * (n + 1)

    for i in range(1, n + 1):
        b[i] = a[i - 1] - d[i]

    seg = SegmentTree(b)

    pref_d = [0] * (n + 1)
    for i in range(1, n + 1):
        pref_d[i] = pref_d[i - 1] + d[i]

    q = int(input())
    out = []

    for _ in range(q):
        s = input().split()

        if s[0] == '+':
            pos = int(s[1])
            x = int(s[2])

            cur = seg.query_point(pos)
            nv = cur + x

            nxt = seg.first_ge(pos + 1, nv)

            if nxt == -1:
                r = n
            else:
                r = nxt - 1

            seg.assign(pos, r, nv)

        else:
            l = int(s[1])
            r = int(s[2])

            dyn = seg.query_sum(l, r)
            static = pref_d[r] - pref_d[l - 1]

            out.append(str(dyn + static))

    sys.stdout.write("\n".join(out))

solve()
```

After the transformation, the whole problem revolves around the nondecreasing array `b`. The segment tree stores sums and maxima of `b`, together with lazy range assignments.

The update first reads the current value at one position. The new propagated value is simply that value plus `x`. We then search for the first position to the right whose value is already at least the new value. Everything before that position must be raised. If no such position exists, the update reaches the end of the array.

The search uses the stored segment maxima. Because `b` is nondecreasing, the first position with value at least `nv` uniquely determines the affected interval.

Range-sum queries split into a dynamic contribution from `b` and a static contribution from `d`. The latter is precomputed once using prefix sums.

A common implementation mistake is forgetting that the update range includes the modified position itself. Another is searching from `pos` instead of `pos + 1`, which would immediately find the newly updated element and produce an empty interval.

## Worked Examples

### Sample 1

Input:

```
3
1 2 3
1 -1
5
s 2 3
+ 1 2
s 1 2
+ 3 1
s 2 3
```

We compute:

```
d = [0, 1, 0]
b = [1, 1, 3]
```

| Operation | b before | Action | b after |
| --- | --- | --- | --- |
| s 2 3 | [1,1,3] | sum | [1,1,3] |
| + 1 2 | [1,1,3] | set positions 1..2 to 3 | [3,3,3] |
| s 1 2 | [3,3,3] | sum | [3,3,3] |
| + 3 1 | [3,3,3] | set position 3 to 4 | [3,3,4] |
| s 2 3 | [3,3,4] | sum | [3,3,4] |

The trace shows how propagation becomes a simple range assignment in the transformed array.

### Propagation Through Many Positions

Consider:

```
a = [5, 7, 9, 11]
k = [2, 2, 2]
```

Then:

```
d = [0,2,4,6]
b = [5,5,5,5]
```

Apply:

```
+ 2 3
```

| Step | Value |
| --- | --- |
| current b[2] | 5 |
| new value | 8 |
| first position ≥ 8 | none |
| assigned range | [2,4] |
| final b | [5,8,8,8] |

Reconstructing:

```
a = [5,10,12,14]
```

which is exactly the result of repeatedly enforcing the original constraints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q log² n) | each update performs one logarithmic search and one logarithmic assignment |
| Space | O(n) | segment tree and prefix arrays |

With `n, q ≤ 100000`, `log n` is about 17. Even `O(q log² n)` stays comfortably within the limit, resulting in only a few tens of millions of primitive operations.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    # paste solve() implementation and capture stdout
    pass

# sample 1
assert run(
"""3
1 2 3
1 -1
5
s 2 3
+ 1 2
s 1 2
+ 3 1
s 2 3
"""
) == "5\n7\n8"

# minimum size
assert run(
"""2
1 5
3
2
s 1 2
s 2 2
"""
) == "6\n5"

# propagation to end
assert run(
"""4
5 7 9 11
2 2 2
2
+ 2 3
s 1 4
"""
) == "41"

# negative k
assert run(
"""2
10 20
-100
2
+ 1 1
s 1 2
"""
) == "31"

# single position update
assert run(
"""3
1 10 20
0 0
2
+ 3 5
s 1 3
"""
) == "36"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum size array | direct sums | smallest valid instance |
| Propagation to end | 41 | suffix update reaching `n` |
| Negative k | 31 | no unnecessary propagation |
| Single position update | 36 | right boundary handling |

## Edge Cases

Consider:

```
2
10 20
-100
2
+ 1 1
s 1 2
```

The constraint is already extremely loose. After increasing `a[1]` to `11`, we still have:

```
20 >= -89
```

so nothing propagates. In transformed form:

```
d = [0,-100]
b = [10,120]
```

Updating position 1 produces:

```
b = [11,120]
```

No assignment extends further because the next value is already larger. The sum becomes `31`, which matches the true array.

Now consider a full-suffix propagation:

```
4
5 7 9 11
2 2 2
1
+ 2 3
```

Initially:

```
b = [5,5,5,5]
```

The new value is `8`. There is no later element with value at least `8`, so the affected interval is `[2,4]`. After assignment:

```
b = [5,8,8,8]
```

Reconstructing gives:

```
a = [5,10,12,14]
```

which is exactly what repeated propagation in the original statement produces. The segment tree update matches the intended behavior even when every remaining element changes.
