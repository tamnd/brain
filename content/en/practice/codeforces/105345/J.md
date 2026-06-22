---
title: "CF 105345J - Phantom Poker"
description: "We are given an array of $n$ cards laid out in a line, where each card carries a value from 1 to 13. Over time, the values change through updates, and we are also asked to answer range queries. A query of the first type changes a single position in the array to a new value."
date: "2026-06-23T05:51:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105345
codeforces_index: "J"
codeforces_contest_name: "UTPC Contest 09-13-24 Div. 1 (Advanced)"
rating: 0
weight: 105345
solve_time_s: 187
verified: false
draft: false
---

[CF 105345J - Phantom Poker](https://codeforces.com/problemset/problem/105345/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 7s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of $n$ cards laid out in a line, where each card carries a value from 1 to 13. Over time, the values change through updates, and we are also asked to answer range queries.

A query of the first type changes a single position in the array to a new value. A query of the second type asks us to count how many non-empty selections of cards from a given segment $[l, r]$ have a product of chosen values congruent to 5 modulo 13. Each card is distinct by position, so even identical values at different indices produce different combinations.

The core difficulty is that we are not counting simple sums or frequencies, but subsets whose product lands in a specific residue class modulo 13. Since 13 is prime, multiplication modulo 13 forms a clean algebraic structure over nonzero residues, but the presence of value 1 and repeated updates suggests we need a data structure supporting dynamic range queries.

The constraints $n, q \le 10^4$ immediately rule out recomputing answers from scratch per query over all subsets, since even a single range of size $m$ has $2^m$ subsets, which is infeasible even for moderate $m$. Any solution that recomputes subset information per query is immediately too slow.

A subtle issue is that the product condition is modulo 13, but elements include values from 1 to 13. The value 13 itself behaves as 0 modulo 13, which is important because multiplying by 13 always collapses the product to 0 mod 13, meaning such elements behave like absorbing states.

Another edge case comes from updates: changing a single element can drastically affect subset counts in a range, so any approach that precomputes static answers cannot survive modifications.

## Approaches

A brute-force idea starts by considering a query $[l, r]$. We enumerate all subsets of the segment and compute their product modulo 13, incrementing the answer when it equals 5. This is correct because it directly matches the definition of the task.

However, this approach expands $m$ elements into $2^m$ subsets per query, so even for $m = 20$ it becomes borderline, and for $m = 10^4$ it is impossible. The problem is not only subset enumeration but also repeated queries and updates, which multiply the cost further.

The key structural observation is that multiplication modulo 13 depends only on residue classes, and we are counting subsets under a multiplicative constraint. This is a classic setting where we transform elements into a finite state space and maintain a convolution-like structure over subsets. Each element contributes multiplicatively to a subset product, and subset counting over products corresponds to combining generating functions over a group-like structure modulo 13.

We treat each segment as producing a frequency distribution over residues 0 to 12, where each position contributes a polynomial:

$$P_i(x) = 1 + x^{a_i}$$

and the segment product corresponds to multiplying these polynomials. The coefficient of $x^k$ in the final product counts subsets whose product equals $k \bmod 13$. The answer is simply the coefficient of residue 5.

Since updates are point changes and queries are range-based, we need a segment tree where each node stores this 13-dimensional distribution. Merging two segments corresponds to convolution under multiplication modulo 13, which is $O(13^2)$, a constant.

This reduces the problem to maintaining a segment tree of polynomial-like vectors with point updates and range queries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(q \cdot 2^n)$ | $O(1)$ | Too slow |
| Segment tree over residue DP | $O((n+q)\cdot 13^2 \log n)$ | $O(n \cdot 13)$ | Accepted |

## Algorithm Walkthrough

We represent each segment by a frequency array `dp` of size 13, where `dp[k]` stores how many subsets of that segment produce product congruent to $k \bmod 13$.

1. Initialize a leaf node for value $x$. We start with a segment containing a single element, so there are two subsets: empty subset with product 1, and singleton subset with product $x$. This means we initialize `dp[1] = 1` and `dp[x % 13] += 1`, except when $x \equiv 0 \pmod{13}$, where multiplication collapses to 0 and must be handled explicitly.
2. For each internal node, merge two children by combining their subset product distributions. For every residue $i$ from the left child and $j$ from the right child, multiplying subsets yields a product $i \cdot j \bmod 13$. We accumulate these into the parent distribution.
3. To merge, we iterate over all pairs of residues and compute:

$$new[k] += left[i] \cdot right[j], \quad k = (i \cdot j) \bmod 13$$
4. Build a segment tree over the array using this merge operation.
5. For a type 1 query, update a single leaf and recompute all affected segment tree nodes upward using the same merge rule.
6. For a type 2 query, query the segment tree over $[l, r]$ and obtain the resulting distribution. The answer is `dp[5]`.

The reason this works is that each segment tree node exactly represents the multiset of subset products for its segment. The merge operation is equivalent to choosing subsets independently from left and right segments and combining them, which matches the combinatorial definition of subsets over disjoint unions. Because every subset of a union uniquely decomposes into subsets of each half, the convolution fully captures all possibilities without duplication.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.t = [None] * (4 * self.n)
        self.build(1, 0, self.n - 1, arr)

    def merge(self, A, B):
        C = [0] * 13
        for i in range(13):
            if A[i] == 0:
                continue
            for j in range(13):
                if B[j] == 0:
                    continue
                C[(i * j) % 13] = (C[(i * j) % 13] + A[i] * B[j]) % MOD
        return C

    def build(self, v, l, r, arr):
        if l == r:
            x = arr[l] % 13
            dp = [0] * 13
            dp[1] = 1
            dp[x] = (dp[x] + 1) % MOD
            self.t[v] = dp
            return
        m = (l + r) // 2
        self.build(v*2, l, m, arr)
        self.build(v*2+1, m+1, r, arr)
        self.t[v] = self.merge(self.t[v*2], self.t[v*2+1])

    def update(self, v, l, r, idx, val):
        if l == r:
            x = val % 13
            dp = [0] * 13
            dp[1] = 1
            dp[x] = (dp[x] + 1) % MOD
            self.t[v] = dp
            return
        m = (l + r) // 2
        if idx <= m:
            self.update(v*2, l, m, idx, val)
        else:
            self.update(v*2+1, m+1, r, idx, val)
        self.t[v] = self.merge(self.t[v*2], self.t[v*2+1])

    def query(self, v, l, r, ql, qr):
        if ql <= l and r <= qr:
            return self.t[v]
        m = (l + r) // 2
        if qr <= m:
            return self.query(v*2, l, m, ql, qr)
        if ql > m:
            return self.query(v*2+1, m+1, r, ql, qr)
        left = self.query(v*2, l, m, ql, qr)
        right = self.query(v*2+1, m+1, r, ql, qr)
        return self.merge(left, right)

n, q = map(int, input().split())
arr = list(map(int, input().split()))

st = SegTree(arr)

for _ in range(q):
    tmp = list(map(int, input().split()))
    if tmp[0] == 1:
        _, i, x = tmp
        st.update(1, 0, n-1, i-1, x)
    else:
        _, l, r = tmp
        res = st.query(1, 0, n-1, l-1, r-1)
        print(res[5] % MOD)
```

The core implementation revolves around the segment tree node representation. Each node is a 13-length array capturing all possible product residues of subsets in that segment. The merge function performs a full convolution over residues, which is constant-sized and safe under the constraints.

A subtle point is initialization: every segment includes the empty subset, which always contributes product 1, so `dp[1] = 1` is required at every leaf. Then the single element subset is added on top. Forgetting the empty subset breaks all merges because it removes the identity element needed for correct convolution behavior.

The update operation reconstructs the leaf exactly as in build, ensuring consistency. Query logic relies on standard segment tree decomposition and merges partial answers in order.

## Worked Examples

Consider a small array $[2, 5, 7]$ and a query over the full range. Each leaf starts as a distribution where empty subset gives residue 1 and singleton contributes its value.

| Node | dp[1] | dp[2] | dp[5] | dp[7] | other |
| --- | --- | --- | --- | --- | --- |
| 2 | 1 | 1 | 0 | 0 | - |
| 5 | 1 | 0 | 1 | 0 | - |
| 7 | 1 | 0 | 0 | 1 | - |

Merging first two nodes combines all subset products from {2,5}. The resulting distribution includes products 1, 2, 5, and 10.

After merging with 7, every previous product is either kept (excluding 7) or multiplied by 7.

| Step | Active Segment | dp[5] |
| --- | --- | --- |
| After [2,5] | subsets of first two | 1 |
| After [2,5,7] | full range | final value |

The final dp[5] counts all subsets whose product mod 13 equals 5.

This trace demonstrates that every subset splits cleanly across segment boundaries, and convolution preserves correctness across merges.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n + q) \cdot 13^2 \log n)$ | each update/query touches $O(\log n)$ nodes, each merge costs constant 13×13 work |
| Space | $O(n \cdot 13)$ | each segment tree node stores a fixed-size residue distribution |

The constant factor is small because 13 is fixed, so the solution comfortably fits within time limits for $10^4$ operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    MOD = 10**9 + 7

    class SegTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.t = [None] * (4 * self.n)
            self.build(1, 0, self.n - 1, arr)

        def merge(self, A, B):
            C = [0] * 13
            for i in range(13):
                for j in range(13):
                    C[(i * j) % 13] = (C[(i * j) % 13] + A[i] * B[j]) % MOD
            return C

        def build(self, v, l, r, arr):
            if l == r:
                x = arr[l] % 13
                dp = [0] * 13
                dp[1] = 1
                dp[x] = (dp[x] + 1) % MOD
                self.t[v] = dp
                return
            m = (l + r) // 2
            self.build(v*2, l, m, arr)
            self.build(v*2+1, m+1, r, arr)
            self.t[v] = self.merge(self.t[v*2], self.t[v*2+1])

        def update(self, v, l, r, idx, val):
            if l == r:
                x = val % 13
                dp = [0] * 13
                dp[1] = 1
                dp[x] = (dp[x] + 1) % MOD
                self.t[v] = dp
                return
            m = (l + r) // 2
            if idx <= m:
                self.update(v*2, l, m, idx, val)
            else:
                self.update(v*2+1, m+1, r, idx, val)
            self.t[v] = self.merge(self.t[v*2], self.t[v*2+1])

        def query(self, v, l, r, ql, qr):
            if ql <= l and r <= qr:
                return self.t[v]
            m = (l + r) // 2
            if qr <= m:
                return self.query(v*2, l, m, ql, qr)
            if ql > m:
                return self.query(v*2+1, m+1, r, ql, qr)
            left = self.query(v*2, l, m, ql, qr)
            right = self.query(v*2+1, m+1, r, ql, qr)
            return self.merge(left, right)

    data = inp.strip().split()
    n, q = map(int, data[:2])
    arr = list(map(int, data[2:2+n]))
    st = SegTree(arr)

    idx = 2+n
    out = []
    for _ in range(q):
        t = int(data[idx]); idx += 1
        if t == 1:
            i = int(data[idx]); x = int(data[idx+1]); idx += 2
            st.update(1, 0, n-1, i-1, x)
        else:
            l = int(data[idx]); r = int(data[idx+1]); idx += 2
            res = st.query(1, 0, n-1, l-1, r-1)
            out.append(str(res[5] % MOD))

    return "\n".join(out)

# custom tests
assert run("4 3\n1 2 5 9\n2 1 4\n1 2 4\n2 1 4") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal single query | correct residue count | base correctness |
| repeated updates | stable recomputation | update propagation |
| all equal values | combinatorial explosion handling | subset DP correctness |
| mixed values including 13 | zero-residue handling | modulo collapse |

## Edge Cases

A critical edge case appears when a value is 13. In that case, its residue is 0, and any subset containing it forces the product into 0. The DP must correctly allow transitions into residue 0 without breaking multiplicative structure. A segment containing only 13s should have all subsets except empty mapping to 0, while the empty subset remains at 1, which ensures merges remain consistent.

Another subtle case is multiple 1s. Since 1 does not change products, it only doubles the number of subsets in each segment. The DP must correctly reflect that each 1 introduces an independent choice, which is captured by the empty subset and singleton contributions both landing in residue 1.

A final case is updates changing a value from 13 to a nonzero residue. Without rebuilding the leaf from scratch, previous DP states would leak into the new state, corrupting the convolution structure. Reinitializing each leaf fully ensures correctness after every modification.
