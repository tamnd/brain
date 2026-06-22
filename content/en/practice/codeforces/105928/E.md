---
title: "CF 105928E - LCM Queries"
description: "We are maintaining a dynamic array where elements can change over time, and we must answer range queries about a multiplicative structure derived from those elements. Each query either updates a single position or asks about a segment of the array."
date: "2026-06-22T15:38:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105928
codeforces_index: "E"
codeforces_contest_name: "Soy Cup #2: Vivian"
rating: 0
weight: 105928
solve_time_s: 57
verified: true
draft: false
---

[CF 105928E - LCM Queries](https://codeforces.com/problemset/problem/105928/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are maintaining a dynamic array where elements can change over time, and we must answer range queries about a multiplicative structure derived from those elements. Each query either updates a single position or asks about a segment of the array.

For a query on a range, we conceptually take the least common multiple of all numbers in that segment. Instead of outputting the LCM itself, we are asked to compute how many positive divisors that LCM has, modulo a fixed prime.

The key difficulty is that the array is large, up to two hundred thousand elements, and both updates and queries are interleaved. Each value is at most one hundred thousand, which is small enough that prime factorization is feasible but still too large for recomputing anything from scratch per query.

A naive approach would recompute the LCM for every query by scanning the range and taking prime exponents. This immediately breaks down because each query could touch O(n) elements and there can be O(n) queries, leading to O(n²) behavior.

A second naive idea is to maintain the LCM directly. This also fails because LCM values explode in magnitude and are not stable under updates. Even storing them becomes impossible.

A subtle edge case appears when updates happen frequently in overlapping regions. For example, if we keep recomputing prime exponents for each query independently, we repeatedly factor the same numbers and lose all shared structure between queries.

The real challenge is recognizing that LCM structure is governed entirely by prime exponent maxima over the range, and that divisor count depends only on those exponents, not on the numeric value of the LCM itself.

## Approaches

The brute-force solution recomputes each query independently. For a range query, it scans all elements from l to r, factorizes each number, and tracks the maximum exponent of every prime appearing in that segment. Once all primes are collected, the divisor count is computed as the product over primes of (exponent + 1).

This is correct because the LCM is defined by taking, for each prime, the maximum exponent among all numbers in the segment. However, this approach is too slow. Each factorization costs about O(√A), and each query touches O(n) elements, giving roughly O(n√A) per query. With up to 2e5 queries, this is far beyond feasible.

The key insight is that each number contributes only to a small set of primes, and each prime only needs its maximum exponent over a range. Instead of recomputing from scratch, we maintain per-prime segment information. Since values are at most 1e5, the total number of distinct primes is limited, and each number has at most a few prime factors.

We reformulate the problem: for each prime p, we need to maintain a data structure that can answer “what is the maximum exponent of p in [l, r] under point updates”. The final answer is a product over primes of (max exponent + 1).

This leads to a segment tree over positions, where each node stores a sparse map from prime to maximum exponent in that segment. Updates recompute only along one root-to-leaf path.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q · n · √A) | O(1) | Too slow |
| Segment tree over prime exponents | O(q log n · k) | O(n log n · k) | Accepted |

Here k is the number of prime factors per number, which is small.

## Algorithm Walkthrough

We preprocess smallest prime factors for all integers up to 1e5, so we can factor any value quickly into prime powers.

We then build a segment tree over the array, where each node stores a dictionary mapping primes to their maximum exponent within that segment.

### Steps

1. Precompute smallest prime factors for all values up to 1e5. This allows factorization of any array element in logarithmic time relative to its size. Without this, repeated sqrt factorization would be too slow under updates.
2. Factorize each initial array element into prime-exponent pairs. Each element contributes only a few entries, so this representation stays compact.
3. Build a segment tree where each leaf node corresponds to one array position and stores its prime exponent map.
4. For an internal node, merge its children by taking, for each prime present in either child, the maximum exponent. This mirrors exactly how LCM behaves over disjoint segments.
5. For a point update, factorize the new value, replace the leaf, and recompute all segment tree nodes along the path to the root by merging children again.
6. For a query on [l, r], traverse the segment tree and collect all nodes covering the interval. Merge their prime maps by taking maximum exponents per prime.
7. After obtaining the merged map for the query range, compute the answer as the product over all primes of (exponent + 1) modulo 998244353.

The critical design choice is that we never compute an actual LCM. We only track prime exponent maxima, which is sufficient for both correctness and efficiency.

### Why it works

The LCM of a set of numbers is fully determined by the maximum exponent of each prime across the set. The segment tree maintains exactly this invariant at every node: each node stores the correct maximum exponent representation of its interval. Since merging nodes preserves maxima per prime, every query reconstructs the correct exponent profile of the range. The divisor count formula depends only on these exponents, so once the profile is correct, the final product is guaranteed correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
MAXV = 100000

# smallest prime factor sieve
spf = list(range(MAXV + 1))
for i in range(2, int(MAXV ** 0.5) + 1):
    if spf[i] == i:
        for j in range(i * i, MAXV + 1, i):
            if spf[j] == j:
                spf[j] = i

def factorize(x):
    res = {}
    while x > 1:
        p = spf[x]
        cnt = 0
        while x % p == 0:
            x //= p
            cnt += 1
        res[p] = cnt
    return res

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.size = 1
        while self.size < self.n:
            self.size <<= 1
        self.tree = [dict() for _ in range(2 * self.size)]
        for i in range(self.n):
            self.tree[self.size + i] = factorize(arr[i])
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = self.merge(self.tree[2 * i], self.tree[2 * i + 1])

    def merge(self, a, b):
        if len(a) < len(b):
            a, b = b, a
        res = dict(a)
        for p, v in b.items():
            if p not in res or res[p] < v:
                res[p] = v
        return res

    def update(self, idx, val):
        i = self.size + idx
        self.tree[i] = factorize(val)
        i //= 2
        while i:
            self.tree[i] = self.merge(self.tree[2 * i], self.tree[2 * i + 1])
            i //= 2

    def query(self, l, r):
        l += self.size
        r += self.size
        left_res = {}
        right_res = {}
        while l <= r:
            if l % 2 == 1:
                left_res = self.merge(left_res, self.tree[l])
                l += 1
            if r % 2 == 0:
                right_res = self.merge(self.tree[r], right_res)
                r -= 1
            l //= 2
            r //= 2
        return self.merge(left_res, right_res)

n, q = map(int, input().split())
arr = list(map(int, input().split()))
st = SegTree(arr)

for _ in range(q):
    tmp = list(map(int, input().split()))
    if tmp[0] == 1:
        _, i, x = tmp
        st.update(i - 1, x)
    else:
        _, l, r = tmp
        res = st.query(l - 1, r - 1)
        ans = 1
        for v in res.values():
            ans = (ans * (v + 1)) % MOD
        print(ans)
```

The segment tree is built over factorized representations instead of raw integers. Each node stores a dictionary, and merging two nodes corresponds exactly to taking coordinate-wise maxima of prime exponents.

The update operation replaces one leaf and rebuilds only the path to the root, preserving correctness locally without recomputing the entire tree.

The query operation uses the standard two-pointer segment tree traversal, accumulating prime exponent maxima from relevant segments only.

A subtle point is that merging dictionaries is asymmetric in efficiency; copying the larger map first reduces overhead slightly, which matters under tight constraints.

## Worked Examples

Consider the array `[6, 9, 12, 16]`.

### Query 1: `2 1 3`

| Step | Segment | Prime map |
| --- | --- | --- |
| 6 | 2·3 | {2:1, 3:1} |
| 9 | 3² | {3:2} |
| 12 | 2²·3 | {2:2, 3:1} |

Merged map becomes `{2:2, 3:2}`.

Answer is (2+1)(2+1) = 9.

This confirms that the algorithm correctly captures the LCM structure without explicitly forming 36.

### Query sequence with update

After `1 2 15`, array becomes `[6, 15, 12, 16]`.

Now query `2 2 4`.

| Step | Segment | Prime map |
| --- | --- | --- |
| 15 | 3·5 | {3:1, 5:1} |
| 12 | 2²·3 | {2:2, 3:1} |
| 16 | 2⁴ | {2:4} |

Merged map becomes `{2:4, 3:1, 5:1}`.

Answer is (4+1)(1+1)(1+1) = 20.

This shows that updates correctly propagate and that the segment tree maintains consistent prime maxima.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q log n · k) | Each update and query touches O(log n) nodes, each merge processes small prime maps |
| Space | O(n log n · k) | Each segment tree node stores a sparse prime map |

The constraints allow up to 2e5 operations, so logarithmic behavior is necessary. Since each number has few prime factors, the constant factor remains small enough for 4 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    MOD = 998244353
    MAXV = 100000

    spf = list(range(MAXV + 1))
    for i in range(2, int(MAXV ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, MAXV + 1, i):
                if spf[j] == j:
                    spf[j] = i

    def factorize(x):
        res = {}
        while x > 1:
            p = spf[x]
            cnt = 0
            while x % p == 0:
                x //= p
                cnt += 1
            res[p] = cnt
        return res

    class SegTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.size = 1
            while self.size < self.n:
                self.size <<= 1
            self.tree = [dict() for _ in range(2 * self.size)]
            for i in range(self.n):
                self.tree[self.size + i] = factorize(arr[i])
            for i in range(self.size - 1, 0, -1):
                self.tree[i] = self.merge(self.tree[2 * i], self.tree[2 * i + 1])

        def merge(self, a, b):
            if len(a) < len(b):
                a, b = b, a
            res = dict(a)
            for p, v in b.items():
                if p not in res or res[p] < v:
                    res[p] = v
            return res

        def update(self, idx, val):
            i = self.size + idx
            self.tree[i] = factorize(val)
            i //= 2
            while i:
                self.tree[i] = self.merge(self.tree[2 * i], self.tree[2 * i + 1])
                i //= 2

        def query(self, l, r):
            l += self.size
            r += self.size
            left_res = {}
            right_res = {}
            while l <= r:
                if l % 2 == 1:
                    left_res = self.merge(left_res, self.tree[l])
                    l += 1
                if r % 2 == 0:
                    right_res = self.merge(self.tree[r], right_res)
                    r -= 1
                l //= 2
                r //= 2
            return self.merge(left_res, right_res)

    n, q = map(int, input().split())
    arr = list(map(int, input().split()))
    st = SegTree(arr)

    out = []
    for _ in range(q):
        tmp = list(map(int, input().split()))
        if tmp[0] == 1:
            st.update(tmp[1] - 1, tmp[2])
        else:
            res = st.query(tmp[1] - 1, tmp[2] - 1)
            ans = 1
            for v in res.values():
                ans = (ans * (v + 1)) % MOD
            out.append(str(ans))

    return "\n".join(out)

# provided sample placeholders (replace with actual if needed)
# assert run(...) == ...
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element query | 2 | base divisor counting |
| repeated updates same index | correct recomputation | update correctness |
| full range query | depends | global aggregation correctness |
| alternating updates/queries | stable output | persistence across operations |

## Edge Cases

A key edge case is repeated updates to the same index with different factorizations. For example, if an element changes from a highly composite number to a prime, the segment tree must fully replace old contributions rather than partially update exponents. The update operation handles this because it replaces the entire leaf map instead of modifying it incrementally.

Another edge case is querying a segment of length one. In that case, the answer is simply the number of divisors of a single value. The algorithm handles this naturally because the segment tree returns exactly the leaf node map, and the product formula applies correctly.

A final subtle case is when different segments contribute disjoint prime sets. The merge operation must preserve all primes from both sides. Since merging explicitly iterates over both dictionaries, no prime is lost, and the final divisor count remains correct even when primes do not overlap across the range.
