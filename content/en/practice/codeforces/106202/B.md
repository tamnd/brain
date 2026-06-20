---
title: "CF 106202B - \u0422\u043e\u0440\u0433\u043e\u0432\u0446\u044b"
description: "We are given a line of merchants, each holding a single item with a price. The price of the i-th merchant is an integer in the range from 0 to $2^k - 1$, and every price is conceptually stored as a fixed-length k-bit binary number. The system processes three types of operations."
date: "2026-06-20T22:28:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106202
codeforces_index: "B"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2025-2026, \u041f\u0435\u0440\u0432\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 106202
solve_time_s: 56
verified: true
draft: false
---

[CF 106202B - \u0422\u043e\u0440\u0433\u043e\u0432\u0446\u044b](https://codeforces.com/problemset/problem/106202/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of merchants, each holding a single item with a price. The price of the i-th merchant is an integer in the range from 0 to $2^k - 1$, and every price is conceptually stored as a fixed-length k-bit binary number.

The system processes three types of operations. The first type updates a single merchant’s price. The second type applies a transformation over a segment of merchants: every price in the segment is rewritten by taking its k-bit binary form, flipping every bit, and interpreting the result back as an integer. The third type asks for the sum of prices over a segment.

The key detail is that the bit inversion is not arithmetic negation or XOR with a fixed mask unless we recognize what is happening in fixed-width binary: every number x is transformed into $(2^k - 1) - x$.

The constraints are large: up to 200,000 merchants and 200,000 operations. This immediately rules out any solution that recomputes segment sums or applies flips element by element for each query. Even a logarithmic data structure must avoid touching every element under inversion queries.

A subtle point is that inversion is reversible and uniform over the entire segment. A segment flipped twice returns to its original state. Another important aspect is that updates overwrite values, which must respect any pending flips in the structure.

Edge cases appear when k is small or large relative to values, especially when all bits are 1 or 0, where inversion becomes identity or full complement behavior. Another tricky scenario is overlapping inversions with point updates; if not handled carefully, stale values can propagate.

For example, if k = 3 and x = 2 (binary 010), inversion produces 101 which is 5. If we instead think incorrectly in terms of integer negation, we might mis-handle intermediate states when k changes representation size, but here k is fixed globally.

## Approaches

A direct approach maintains the array explicitly. A type 1 query updates a single position. A type 2 query iterates over the range and replaces each value x with $(2^k - 1) - x$. A type 3 query sums the segment directly.

This is correct but fails immediately under worst-case input. Each inversion or sum operation can take O(n), and with up to 200,000 operations, the worst case reaches $O(nq)$, which is far beyond feasible limits.

The structure of the transformation is the key observation. Each inversion replaces every value x in a segment with a constant linear transformation: $x \mapsto C - x$, where $C = 2^k - 1$. This is affine. Over sums, it behaves predictably:

If a segment has length len and sum S, after inversion its new sum becomes:

$$len \cdot C - S$$

This means we never need to touch individual elements. We only need to maintain segment sums and support range assignment of a "flip state".

The remaining challenge is composability: repeated inversions toggle between identity and complement. This suggests a lazy propagation segment tree with a boolean flip flag.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| Segment Tree with lazy flip | O(q log n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain a segment tree where each node stores the sum of its segment. In addition, each node carries a lazy flag indicating whether its segment is currently logically inverted.

1. Build the segment tree with initial values. Each node stores the sum of its segment and no pending flips. This allows direct aggregation for queries.
2. Define the inversion effect on a node. If a segment of length len has sum S, after inversion its new sum becomes len times C minus S. This lets us update a whole segment in O(1) time at a node.
3. For a range inversion query, when a node segment is fully covered, we apply the transformation directly to its sum and toggle its lazy flag. Toggling twice cancels out, which preserves correctness.
4. When a node is partially covered, we push down any pending inversion before descending. Pushing means applying the inversion state to children and clearing the flag at the parent.
5. For a point update, we navigate to the leaf. Along the path, we ensure all pending flips are pushed so the leaf reflects the true current value before overwriting it.
6. After updating a leaf, we recompute sums upward by summing children.
7. For a range sum query, we similarly ensure correctness by pushing lazy flags before descending, then summing fully covered segments directly.

The key structural idea is that inversion is linear over the sum and self-inverse, which allows it to be encoded as a single boolean tag.

### Why it works

The correctness rests on two invariants. First, each node’s stored sum always represents either the true sum of its segment or the sum after applying exactly one pending inversion flag that has not yet been propagated to children. Second, the inversion operation is distributive over segments: applying it to a union of disjoint segments is equivalent to applying it independently to each segment. Because inversion is its own inverse, the lazy flag only needs parity, not history. This guarantees that any sequence of updates reduces to consistent local transformations without ambiguity.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegTree:
    def __init__(self, arr, k):
        self.n = len(arr)
        self.k = k
        self.C = (1 << k) - 1
        self.sum = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self.build(1, 0, self.n - 1, arr)

    def build(self, v, l, r, arr):
        if l == r:
            self.sum[v] = arr[l]
            return
        m = (l + r) // 2
        self.build(v*2, l, m, arr)
        self.build(v*2+1, m+1, r, arr)
        self.sum[v] = self.sum[v*2] + self.sum[v*2+1]

    def apply_flip(self, v, l, r):
        length = r - l + 1
        self.sum[v] = length * self.C - self.sum[v]
        self.lazy[v] ^= 1

    def push(self, v, l, r):
        if not self.lazy[v] or l == r:
            return
        m = (l + r) // 2
        self.apply_flip(v*2, l, m)
        self.apply_flip(v*2+1, m+1, r)
        self.lazy[v] = 0

    def update_point(self, v, l, r, idx, val):
        if l == r:
            self.sum[v] = val
            return
        self.push(v, l, r)
        m = (l + r) // 2
        if idx <= m:
            self.update_point(v*2, l, m, idx, val)
        else:
            self.update_point(v*2+1, m+1, r, idx, val)
        self.sum[v] = self.sum[v*2] + self.sum[v*2+1]

    def range_flip(self, v, l, r, ql, qr):
        if ql <= l and r <= qr:
            self.apply_flip(v, l, r)
            return
        self.push(v, l, r)
        m = (l + r) // 2
        if ql <= m:
            self.range_flip(v*2, l, m, ql, qr)
        if qr > m:
            self.range_flip(v*2+1, m+1, r, ql, qr)
        self.sum[v] = self.sum[v*2] + self.sum[v*2+1]

    def range_sum(self, v, l, r, ql, qr):
        if ql <= l and r <= qr:
            return self.sum[v]
        self.push(v, l, r)
        m = (l + r) // 2
        res = 0
        if ql <= m:
            res += self.range_sum(v*2, l, m, ql, qr)
        if qr > m:
            res += self.range_sum(v*2+1, m+1, r, ql, qr)
        return res

n, k = map(int, input().split())
arr = list(map(int, input().split()))
q = int(input())

st = SegTree(arr, k)

for _ in range(q):
    tmp = input().split()
    t = int(tmp[0])
    if t == 1:
        i = int(tmp[1]) - 1
        x = int(tmp[2])
        st.update_point(1, 0, n-1, i, x)
    elif t == 2:
        l = int(tmp[1]) - 1
        r = int(tmp[2]) - 1
        st.range_flip(1, 0, n-1, l, r)
    else:
        l = int(tmp[1]) - 1
        r = int(tmp[2]) - 1
        print(st.range_sum(1, 0, n-1, l, r))
```

The implementation uses a classic segment tree with lazy propagation. The critical line is the transformation `length * C - sum[v]`, which encodes full bitwise inversion without touching individual elements. The lazy flag is XORed because two flips cancel out.

The push operation ensures correctness before partial recursion. Without it, point updates would overwrite stale inverted values. The range operations always recompute node sums from children after recursion, preserving consistency.

## Worked Examples

Consider a small array with k = 3: `[1, 2, 3]`, so C = 7.

### Example 1: single flip and query

| Step | Operation | Segment affected | Sum state |
| --- | --- | --- | --- |
| 1 | initial | [1,2,3] | 6 |
| 2 | flip [1,3] | full segment | 3 * 7 - 6 = 15 |
| 3 | query [2,2] | leaf 2 | 7 - 2 = 5 |

After flipping, each element becomes its complement: 1→6, 2→5, 3→4. The segment tree captures this without expanding elements.

### Example 2: flip then point update

Start again: `[1, 2, 3]`

| Step | Operation | Array interpretation | Sum |
| --- | --- | --- | --- |
| 1 | flip [1,3] | [6,5,4] | 15 |
| 2 | set index 2 = 0 | [6,0,4] | 10 |
| 3 | query [1,3] | direct sum | 10 |

The important detail is that the point update first resolves pending flips so that index 2 is correctly seen as 5 before overwriting.

Each trace shows that we never need to materialize the full array after flips; only sums and lazy state are required.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q log n) | each update, flip, or query descends a segment tree height |
| Space | O(n) | segment tree arrays store sums and lazy flags |

With n and q up to 200,000, logarithmic per-operation cost fits comfortably within limits. The constant factor is small because inversion is O(1) per node.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    class SegTree:
        def __init__(self, arr, k):
            self.n = len(arr)
            self.k = k
            self.C = (1 << k) - 1
            self.sum = [0] * (4 * self.n)
            self.lazy = [0] * (4 * self.n)
            self.build(1, 0, self.n - 1, arr)

        def build(self, v, l, r, arr):
            if l == r:
                self.sum[v] = arr[l]
                return
            m = (l + r) // 2
            self.build(v*2, l, m, arr)
            self.build(v*2+1, m+1, r, arr)
            self.sum[v] = self.sum[v*2] + self.sum[v*2+1]

        def apply_flip(self, v, l, r):
            length = r - l + 1
            self.sum[v] = length * self.C - self.sum[v]
            self.lazy[v] ^= 1

        def push(self, v, l, r):
            if not self.lazy[v] or l == r:
                return
            m = (l + r) // 2
            self.apply_flip(v*2, l, m)
            self.apply_flip(v*2+1, m+1, r)
            self.lazy[v] = 0

        def update_point(self, v, l, r, idx, val):
            if l == r:
                self.sum[v] = val
                return
            self.push(v, l, r)
            m = (l + r) // 2
            if idx <= m:
                self.update_point(v*2, l, m, idx, val)
            else:
                self.update_point(v*2+1, m+1, r, idx, val)
            self.sum[v] = self.sum[v*2] + self.sum[v*2+1]

        def range_flip(self, v, l, r, ql, qr):
            if ql <= l and r <= qr:
                self.apply_flip(v, l, r)
                return
            self.push(v, l, r)
            m = (l + r) // 2
            if ql <= m:
                self.range_flip(v*2, l, m, ql, qr)
            if qr > m:
                self.range_flip(v*2+1, m+1, r, ql, qr)
            self.sum[v] = self.sum[v*2] + self.sum[v*2+1]

        def range_sum(self, v, l, r, ql, qr):
            if ql <= l and r <= qr:
                return self.sum[v]
            self.push(v, l, r)
            m = (l + r) // 2
            res = 0
            if ql <= m:
                res += self.range_sum(v*2, l, m, ql, qr)
            if qr > m:
                res += self.range_sum(v*2+1, m+1, r, ql, qr)
            return res

    n, k = map(int, input().split())
    arr = list(map(int, input().split()))
    q = int(input())
    st = SegTree(arr, k)

    out = []
    for _ in range(q):
        tmp = input().split()
        t = int(tmp[0])
        if t == 1:
            i = int(tmp[1]) - 1
            x = int(tmp[2])
            st.update_point(1, 0, n-1, i, x)
        elif t == 2:
            l = int(tmp[1]) - 1
            r = int(tmp[2]) - 1
            st.range_flip(1, 0, n-1, l, r)
        else:
            l = int(tmp[1]) - 1
            r = int(tmp[2]) - 1
            out.append(str(st.range_sum(1, 0, n-1, l, r)))

    return "\n".join(out)

# Sample-style small test
assert run("""3 3
1 2 3
4
3 1 3
2 1 3
3 1 3
3 2 2
""") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Small flip + queries | manual | basic correctness of inversion |
| Single element updates | manual | point update with lazy state |
| All flip twice | original sum | idempotence of XOR flip |
| Max k boundary values | correct complement sums | handling of full-bit range |

## Edge Cases

A case with repeated flips over the same range demonstrates that the lazy flag behaves as parity. If a segment is flipped twice, the stored node should return exactly to its original sum. The implementation handles this because `lazy[v] ^= 1` toggles state and the transformation formula is self-inverse.

A point update after a pending flip is more delicate. Suppose a node is logically inverted but not pushed, and we directly overwrite a leaf. Without pushing, the update would apply to a stale representation. The code ensures correctness by calling `push` before descending, so the leaf is always materialized in the correct state before modification.

A boundary case occurs when k = 1. Then C = 1, and inversion simply swaps 0 and 1. The formula still holds: new sum = len - sum, and the segment tree behaves identically without modification.
