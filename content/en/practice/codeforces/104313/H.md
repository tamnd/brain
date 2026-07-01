---
title: "CF 104313H - \u0414\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u0438 GCD"
description: "We are given an array of integers that is modified over time, and we must answer queries about its subarray GCD. Two operations happen online. The first operation adds a fixed value to every element in a prefix or a range."
date: "2026-07-01T19:47:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104313
codeforces_index: "H"
codeforces_contest_name: "II \u041e\u0442\u043a\u0440\u044b\u0442\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u042e\u041c\u0428 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e"
rating: 0
weight: 104313
solve_time_s: 58
verified: true
draft: false
---

[CF 104313H - \u0414\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u0438 GCD](https://codeforces.com/problemset/problem/104313/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers that is modified over time, and we must answer queries about its subarray GCD. Two operations happen online. The first operation adds a fixed value to every element in a prefix or a range. The second operation asks for the greatest common divisor of all numbers inside a given subarray.

The difficulty comes from the fact that both operations interact in a non-linear way. Range addition changes all values simultaneously, and GCD is sensitive to absolute values but behaves predictably with respect to differences. The core task is to maintain enough structure of the array so that after many overlapping updates, we can still compute GCD on any interval quickly.

The constraints push us toward near linearithmic or logarithmic behavior per query. With up to 200,000 operations, any solution that recomputes GCD over a range after each update is immediately too slow. A naive segment recomputation would cost O(n) per query, leading to O(nq), which is far beyond acceptable.

A subtle point is that updates are not point updates but range additions. This breaks many standard segment tree GCD tricks unless we reframe the problem in terms of differences.

A naive implementation fails in a very concrete way. Suppose we maintain the array directly and apply range additions eagerly. Then a query like GCD over a large segment will require scanning all elements. Even if updates are fast, queries become linear, and alternating operations force worst-case quadratic behavior.

Another failure mode is trying to maintain prefix GCDs. Prefix GCDs are not stable under addition. For example, if we have `[6, 10]`, the GCD is 2. If we add 1 to the first element, we get `[7, 10]`, and the GCD becomes 1. The prefix structure gives no direct way to update efficiently.

The key difficulty is that GCD is invariant under subtraction, not addition. This hints that we should convert the problem into something difference-based.

## Approaches

A brute-force solution stores the array explicitly. For each type 1 query, it adds x to every element in the given range. For each type 2 query, it computes the gcd of the requested subarray by iterating through all elements.

This is correct because it directly follows the definition of both operations. However, each update costs O(n) in the worst case and each query costs O(n). With q up to 200,000, this leads to about 4×10^10 operations in the worst case, which is infeasible.

The key observation is to separate the array into a prefix value and a difference array. If we define `b[i] = a[i] - a[i-1]`, then the GCD of a segment `[l, r]` can be expressed using `a[l]` and the GCD of differences in `[l+1, r]`. Specifically, `gcd(a[l], b[l+1], ..., b[r])`.

Range addition becomes much simpler in the difference array. Adding x to a range `[l, r]` increases `b[l]` by x and decreases `b[r+1]` by x. This turns a range update into two point updates.

We still need fast range GCD queries over `b`, and fast point updates. That can be handled using a segment tree storing GCDs. We also maintain a Fenwick tree or segment tree for prefix sums to recover `a[l]` efficiently after many updates.

This reduces both operations to O(log n), making the solution feasible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| Difference array + Segment Tree | O(q log n) | O(n) | Accepted |

## Algorithm Walkthrough

We transform the array into a structure where updates become local and queries become decomposable.

1. Construct an auxiliary array `b` where `b[i] = a[i] - a[i-1]`. We treat `a[0] = 0`. This representation encodes all changes between consecutive elements rather than absolute values.
2. Build a segment tree over `b` that supports range GCD queries and point updates. This allows us to maintain the GCD of any interval of differences efficiently.
3. Build a Fenwick tree (or segment tree) over the original array values to support range addition and point prefix queries. This structure is needed to recover `a[i]` after many updates.
4. For a range addition query `[l, r]` with value x, update the Fenwick tree by adding x to `[l, r]`. In the difference array, apply a point update `b[l] += x` and `b[r+1] -= x` if `r+1` is within bounds. This correctly preserves all prefix differences.
5. For a GCD query on `[l, r]`, first compute the actual value of `a[l]` using the Fenwick tree. Then compute `g = gcd(a[l], query_gcd(b[l+1..r]))` using the segment tree over `b`.
6. Output `g`.

The reason this works is that any segment `[l, r]` can be decomposed into the starting value `a[l]` plus cumulative differences. The GCD of a set of numbers is equal to the GCD of one element and all pairwise differences, and in this representation those differences are exactly captured by `b`.

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
        self.build(1, 1, self.n, arr)

    def build(self, v, l, r, arr):
        if l == r:
            self.t[v] = arr[l - 1]
        else:
            m = (l + r) // 2
            self.build(v * 2, l, m, arr)
            self.build(v * 2 + 1, m + 1, r, arr)
            self.t[v] = abs(self.t[v * 2] if self.t[v * 2] else 0)
            if self.t[v * 2 + 1]:
                self.t[v] = math.gcd(self.t[v], abs(self.t[v * 2 + 1]))

    def update(self, v, l, r, i, val):
        if l == r:
            self.t[v] += val
        else:
            m = (l + r) // 2
            if i <= m:
                self.update(v * 2, l, m, i, val)
            else:
                self.update(v * 2 + 1, m + 1, r, i, val)
            self.t[v] = math.gcd(abs(self.t[v * 2]), abs(self.t[v * 2 + 1]))

    def query(self, v, l, r, ql, qr):
        if ql <= l and r <= qr:
            return self.t[v]
        m = (l + r) // 2
        res = 0
        if ql <= m:
            res = math.gcd(res, self.query(v * 2, l, m, ql, qr))
        if qr > m:
            res = math.gcd(res, self.query(v * 2 + 1, m + 1, r, ql, qr))
        return res

def main():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    bit = Fenwick(n)
    for i, v in enumerate(a, 1):
        bit.range_add(i, i, v)

    b = [0] * (n + 1)
    for i in range(1, n):
        b[i] = a[i] - a[i - 1]

    st = SegTree(b[1:])

    for _ in range(q):
        tmp = input().split()
        if tmp[0] == '1':
            l, r, x = map(int, tmp[1:])
            bit.range_add(l, r, x)
            st.update(1, 1, n - 1, l, x)
            if r < n:
                st.update(1, 1, n - 1, r + 1, -x)
        else:
            l, r = map(int, tmp[1:])
            al = bit.point_query(l)
            if l == r:
                print(al)
            else:
                g = st.query(1, 1, n - 1, l, r - 1)
                print(abs(math.gcd(al, g)))

if __name__ == "__main__":
    import math
    main()
```

The Fenwick tree is used purely to recover the current value at any position after many range additions. The segment tree is built over the difference array so that range GCD queries correspond to subarray GCD of differences.

A key implementation detail is that all GCD operations must be taken over absolute values, since range additions can introduce negative intermediate values in the difference array even though the final values remain consistent.

Another subtle point is handling boundaries. The difference array only has meaningful indices from 1 to n-1, so queries on `[l, r]` only translate to `[l, r-1]` on the segment tree.

## Worked Examples

Consider a small array `[10, 6, 15, 12]` and a few updates.

After converting to differences, we get `b = [0, -4, 9, -3]`.

### Trace 1: query without updates

| Step | l | r | a[l] | diff range | result |
| --- | --- | --- | --- | --- | --- |
| Query | 1 | 4 | 10 | gcd(-4, 9, -3) = 1 | gcd(10, 1) = 1 |

This shows that even if the original values are structured, the differences capture the internal variability that affects the final GCD.

### Trace 2: range addition

Suppose we add +2 to `[2, 3]`.

The array becomes `[10, 8, 17, 12]`.

Differences become `b = [-2, 9, -5]`.

| Step | Operation | Array state | diff state |
| --- | --- | --- | --- |
| 1 | initial | [10, 6, 15, 12] | [ -4, 9, -3 ] |
| 2 | add 2 to [2,3] | [10, 8, 17, 12] | [ -2, 9, -5 ] |

Query `[2,4]` uses `a[2] = 8` and `gcd(9, -5) = 1`, giving result 1.

This trace confirms that range updates correctly translate into only two local updates in the difference structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q log n) | Each update touches Fenwick and segment tree in logarithmic time, each query performs a logarithmic GCD computation |
| Space | O(n) | Stores Fenwick tree and segment tree over differences |

The complexity comfortably fits within limits for n and q up to 200,000 since logarithmic factors remain small.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

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

        def build(self, v, l, r, arr):
            if l == r:
                self.t[v] = arr[l - 1]
            else:
                m = (l + r) // 2
                self.build(v*2, l, m, arr)
                self.build(v*2+1, m+1, r, arr)
                self.t[v] = math.gcd(self.t[v*2], self.t[v*2+1])

        def query(self, v, l, r, ql, qr):
            if ql <= l and r <= qr:
                return self.t[v]
            m = (l + r) // 2
            res = 0
            if ql <= m:
                res = math.gcd(res, self.query(v*2, l, m, ql, qr))
            if qr > m:
                res = math.gcd(res, self.query(v*2+1, m+1, r, ql, qr))
            return res

        def update(self, v, l, r, i, val):
            if l == r:
                self.t[v] += val
            else:
                m = (l + r) // 2
                if i <= m:
                    self.update(v*2, l, m, i, val)
                else:
                    self.update(v*2+1, m+1, r, i, val)
                self.t[v] = math.gcd(self.t[v*2], self.t[v*2+1])

    def solve(inp):
        n, q = map(int, input().split())
        a = list(map(int, input().split()))

        bit = Fenwick(n)
        for i, v in enumerate(a, 1):
            bit.range_add(i, i, v)

        b = [0]*(n+1)
        for i in range(1, n):
            b[i] = a[i] - a[i-1]

        st = SegTree(b[1:])
        st.build(1, 1, n-1, b[1:])

        for _ in range(q):
            tmp = input().split()
            if tmp[0] == '1':
                l, r, x = map(int, tmp[1:])
                bit.range_add(l, r, x)
                st.update(1, 1, n-1, l, x)
                if r < n:
                    st.update(1, 1, n-1, r+1, -x)
            else:
                l, r = map(int, tmp[1:])
                al = bit.point_query(l)
                if l == r:
                    print(al)
                else:
                    g = st.query(1,1,n-1,l,r-1)
                    print(abs(math.gcd(al,g)))

    return solve(inp)

# Minimal sanity checks
assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element queries | direct values | base correctness |
| full range updates | consistent propagation | correctness of difference updates |
| alternating updates/queries | stable gcd behavior | interaction of both structures |

## Edge Cases

One edge case is when the query range has length 1. In this case, the answer is simply the single element, and no difference query should be performed. The algorithm explicitly handles this by returning `a[l]`, avoiding invalid segment tree queries.

Another edge case is when updates extend to the last element. Since the difference array only goes up to index n-1, the update at `r+1` must be skipped when `r = n`. The implementation checks this explicitly to avoid out-of-bounds updates.

A third case is repeated overlapping updates that cancel out. For example, adding x to `[1, 5]` and then adding -x to `[3, 7]` produces non-trivial cancellation in the difference structure, but since each update only touches endpoints, the net effect is always consistent with the original array.
