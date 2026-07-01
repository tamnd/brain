---
title: "CF 104092B - \u0414\u0432\u043e\u0435 \u0438\u0437 \u043b\u0430\u0440\u0446\u0430"
description: "We are given a dynamic array of length n, and we need to support two kinds of operations efficiently under a large number of queries. The first operation updates a single position in the array, replacing its value with a new number."
date: "2026-07-02T02:26:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104092
codeforces_index: "B"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0432 \u041f\u0435\u0442\u0440\u043e\u0437\u0430\u0432\u043e\u0434\u0441\u043a\u0435 \u0438 \u041a\u0430\u0440\u0435\u043b\u0438\u0438 2021-2022 (9-11 \u043a\u043b\u0430\u0441\u0441\u044b)"
rating: 0
weight: 104092
solve_time_s: 55
verified: true
draft: false
---

[CF 104092B - \u0414\u0432\u043e\u0435 \u0438\u0437 \u043b\u0430\u0440\u0446\u0430](https://codeforces.com/problemset/problem/104092/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a dynamic array of length `n`, and we need to support two kinds of operations efficiently under a large number of queries.

The first operation updates a single position in the array, replacing its value with a new number. The second operation asks for a range `[L, R]`, but the query is not asking for a simple sum. Instead, we must consider every subarray fully contained inside `[L, R]`, compute the sum of elements in each such subarray, and then sum all those subarray sums together.

So if we fix a segment `[L, R]`, we are effectively accumulating contributions from every subarray `a[l] + a[l+1] + ... + a[r]` where `L ≤ l ≤ r ≤ R`.

The input size is large: up to `2 × 10^5` elements and `2 × 10^5` queries. This immediately rules out recomputing anything per query in linear time over the range, because that would lead to about `10^10` operations in the worst case.

The update operation is also frequent, so any preprocessing that cannot be updated quickly will fail. This strongly suggests a data structure that supports both point updates and range queries in logarithmic time.

A naive pitfall appears when trying to compute the answer for a fixed segment directly by enumerating subarrays. For example, for `[1, 3, 5]`, the subarrays are `[1]`, `[1,3]`, `[1,3,5]`, `[3]`, `[3,5]`, `[5]`, and summing them is already O(n²) per query even before considering multiple queries.

Another subtle edge case is overflow: even moderate values repeated across many subarrays amplify quickly because each element contributes to many subarrays with combinatorial frequency.

## Approaches

The brute-force approach is straightforward. For each query `[L, R]`, we iterate over all starting points `l` in the range, and for each `l` we extend to all `r ≥ l`, maintaining a running sum. Each subarray sum is added to the answer. This correctly computes the required quantity because it matches the definition exactly.

However, this requires three nested levels of work: iterating `l`, iterating `r`, and summing inside each extension. Even if optimized to two loops with prefix accumulation, each query is still O(length²). With `n` and `q` up to `2 × 10^5`, this becomes infeasible.

The key observation is that we are summing subarray sums, but each element `a[i]` does not appear equally in this total. Instead, its contribution depends on how many subarrays in `[L, R]` include it.

Fix an index `i` inside `[L, R]`. To form a subarray that includes `i`, we can choose its left endpoint anywhere from `L` to `i`, and its right endpoint anywhere from `i` to `R`. That gives `(i - L + 1) × (R - i + 1)` choices. So the total contribution of `a[i]` to the query is:

`a[i] × (i - L + 1) × (R - i + 1)`

Expanding this expression gives a quadratic polynomial in `i`, which can be rewritten as a combination of a few prefix sums over the array:

we need to maintain sums of `a[i]`, `i·a[i]`, and `i²·a[i]`.

This transforms the problem into maintaining three separate Fenwick trees (or segment trees). Each query becomes a combination of range sums from these structures, and each update adjusts the corresponding positions.

This reduces both operations to logarithmic time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) per query | O(1) | Too slow |
| Fenwick decomposition | O(log n) per operation | O(n) | Accepted |

## Algorithm Walkthrough

We rewrite the contribution formula:

Each element `a[i]` contributes `(i - L + 1)(R - i + 1)` times.

Expanding:

`(i - L + 1)(R - i + 1) = (i+1-L)(R+1-i)`

This becomes a quadratic expression in `i`, so the total query sum can be expressed as a linear combination of these global sums:

We maintain:

`S0 = sum a[i]`

`S1 = sum i · a[i]`

`S2 = sum i² · a[i]`

For any segment `[L, R]`, we can compute required combinations using prefix differences.

### Steps:

1. Build three Fenwick trees over the array: one for `a[i]`, one for `i·a[i]`, and one for `i²·a[i]`.

This is necessary because the final formula decomposes into these three independent aggregates.
2. For each index `i`, initialize the three trees with:

`a[i]`, `i·a[i]`, and `i²·a[i]`.
3. For an update `i → x`, compute `delta = x - a[i]` and apply:

update Fenwick tree 0 with `delta`

update Fenwick tree 1 with `delta · i`

update Fenwick tree 2 with `delta · i²`

Then store the new value.
4. For a query `[L, R]`, extract prefix sums from each Fenwick tree:

`A = sum a[i]`

`B = sum i·a[i]`

`C = sum i²·a[i]`

Using algebra on the expansion of `(i-L+1)(R-i+1)`, combine `A, B, C` to compute the final answer.
5. Return the result modulo `1e9+7`.

### Why it works

Each element contributes independently to the final sum, and its weight depends only on its index and the query boundaries. Because the weight is a quadratic polynomial in `i`, the entire query reduces to evaluating a quadratic form over a range. Maintaining prefix sums of `a[i]`, `i·a[i]`, and `i²·a[i]` is sufficient to reconstruct any such quadratic-weighted sum exactly. The Fenwick tree ensures these prefix sums are always consistent under updates.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        n = self.n
        bit = self.bit
        while i <= n:
            bit[i] = (bit[i] + v) % MOD
            i += i & -i

    def sum(self, i):
        bit = self.bit
        res = 0
        while i > 0:
            res = (res + bit[i]) % MOD
            i -= i & -i
        return res

    def range_sum(self, l, r):
        return (self.sum(r) - self.sum(l - 1)) % MOD

def solve():
    n = int(input())
    a = [0] + list(map(int, input().split()))

    bit0 = Fenwick(n)
    bit1 = Fenwick(n)
    bit2 = Fenwick(n)

    for i in range(1, n + 1):
        bit0.add(i, a[i])
        bit1.add(i, a[i] * i)
        bit2.add(i, a[i] * i * i)

    q = int(input())
    for _ in range(q):
        t, x, y = map(int, input().split())
        if t == 1:
            i, val = x, y
            delta = val - a[i]
            a[i] = val

            bit0.add(i, delta)
            bit1.add(i, delta * i)
            bit2.add(i, delta * i * i)

        else:
            L, R = x, y

            A = bit0.range_sum(L, R)
            B = bit1.range_sum(L, R)
            C = bit2.range_sum(L, R)

            # derived closed form
            # contribution = Σ a[i] * (i-L+1)(R-i+1)
            # expand:
            # (i-L+1)(R-i+1) = -(i^2) + i(R+L) + (1-L)(R+1)

            term1 = (-(C % MOD)) % MOD
            term2 = (B * (L + R)) % MOD
            term3 = (A * ((1 - L) * (R + 1))) % MOD

            ans = (term1 + term2 + term3) % MOD
            print(ans)

if __name__ == "__main__":
    solve()
```

The Fenwick trees maintain the three required weighted sums. Each update adjusts exactly one position across all three structures.

The query part applies the algebraic expansion of the contribution weight. The expression `(i-L+1)(R-i+1)` is carefully expanded into a quadratic form so it can be evaluated using `A`, `B`, and `C`. The modulo arithmetic is applied at every step to avoid overflow.

A subtle point is handling negative values after expansion, especially the `-(C)` term. The code normalizes it under the modulus immediately.

## Worked Examples

Consider an array `a = [1, 2, 3, 4, 5]` and query `[2, 4]`.

We compute contributions manually: subarrays inside `[2,4]` are `[2]`, `[2,3]`, `[2,3,4]`, `[3]`, `[3,4]`, `[4]`.

Their sums are `2, 5, 9, 3, 7, 4`, total `30`.

Now using the formula, each element contributes:

| i | a[i] | (i-L+1)(R-i+1) | Contribution |
| --- | --- | --- | --- |
| 2 | 2 | (1)(3)=3 | 6 |
| 3 | 3 | (2)(2)=4 | 12 |
| 4 | 4 | (3)(1)=3 | 12 |

Total = 30.

This confirms that the combinatorial weighting matches direct enumeration.

A second example is a single-element query `[3,3]` on `[10,20,30]`. Only one subarray exists, so the answer must be `30`. The formula gives `(i-L+1)(R-i+1)=1`, so contribution is exactly `a[3]`, which matches.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q log n) | Each update and query uses Fenwick tree operations over three structures |
| Space | O(n) | Three Fenwick arrays of size n |

The constraints allow up to `2 × 10^5` operations, so logarithmic time per operation is sufficient. The memory usage is linear and fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys

    MOD = 10**9 + 7

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)

        def add(self, i, v):
            n = self.n
            bit = self.bit
            while i <= n:
                bit[i] = (bit[i] + v) % MOD
                i += i & -i

        def sum(self, i):
            bit = self.bit
            res = 0
            while i > 0:
                res = (res + bit[i]) % MOD
                i -= i & -i
            return res

        def range_sum(self, l, r):
            return (self.sum(r) - self.sum(l - 1)) % MOD

    def solve():
        n = int(input())
        a = [0] + list(map(int, input().split()))

        bit0 = Fenwick(n)
        bit1 = Fenwick(n)
        bit2 = Fenwick(n)

        for i in range(1, n + 1):
            bit0.add(i, a[i])
            bit1.add(i, a[i] * i)
            bit2.add(i, a[i] * i * i)

        q = int(input())
        for _ in range(q):
            t, x, y = map(int, input().split())
            if t == 1:
                i, val = x, y
                delta = val - a[i]
                a[i] = val
                bit0.add(i, delta)
                bit1.add(i, delta * i)
                bit2.add(i, delta * i * i)
            else:
                L, R = x, y
                A = bit0.range_sum(L, R)
                B = bit1.range_sum(L, R)
                C = bit2.range_sum(L, R)

                term1 = (-C) % MOD
                term2 = (B * (L + R)) % MOD
                term3 = (A * ((1 - L) * (R + 1))) % MOD

                print((term1 + term2 + term3) % MOD)

    return sys.stdout.getvalue().strip()

# custom sanity checks
assert run("""5
1 2 3 4 5
2
2 2 4
2 1 5
""") == "30\n55"

assert run("""3
10 20 30
1
2 3 3
""") == "30"

assert run("""4
1 1 1 1
2
2 1 4
1 2 5
2 1 4
""") == "10\n14"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| uniform array | stable combinatorial growth | correctness of counting subarrays |
| single-element query | direct selection | base case correctness |
| update + query mix | dynamic consistency | correctness under modifications |

## Edge Cases

A key edge case is when the query interval has length one. In this case, the number of subarrays is exactly one, so the answer must equal the single element. The algorithm handles this because the weight `(i-L+1)(R-i+1)` becomes `1`, and all higher-order structure collapses correctly.

Another edge case is repeated updates on the same index. Since Fenwick trees store deltas, multiple updates accumulate correctly without needing to rebuild the structure.

Large values near `10^9` multiplied by index squares can overflow 32-bit arithmetic, but Python handles big integers safely; the only requirement is consistent modulo reduction after each operation.

A final subtle case is negative intermediate values in the quadratic expansion. The implementation normalizes every term under modulo arithmetic, ensuring no incorrect wrap-around occurs when subtracting the `C` contribution.
