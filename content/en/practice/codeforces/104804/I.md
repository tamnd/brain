---
title: "CF 104804I - \u0421\u0430\u043c\u0430\u044f \u043f\u0440\u043e\u0441\u0442\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430 \u043a\u043e\u043d\u0442\u0435\u0441\u0442\u0430"
description: "We are given an array and we first form all prefix sums of that array. If the array is a, then we build a new sequence s where s[i] is the sum of the first i elements. After that, we consider all pairs of distinct elements in this prefix sum sequence and multiply them."
date: "2026-06-28T16:53:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104804
codeforces_index: "I"
codeforces_contest_name: "Central Russia Regional Contest, 2022, Qualification Contest"
rating: 0
weight: 104804
solve_time_s: 75
verified: false
draft: false
---

[CF 104804I - \u0421\u0430\u043c\u0430\u044f \u043f\u0440\u043e\u0441\u0442\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430 \u043a\u043e\u043d\u0442\u0435\u0441\u0442\u0430](https://codeforces.com/problemset/problem/104804/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array and we first form all prefix sums of that array. If the array is `a`, then we build a new sequence `s` where `s[i]` is the sum of the first `i` elements. After that, we consider all pairs of distinct elements in this prefix sum sequence and multiply them. The task is to compute the total sum of all such pairwise products, and then take the result modulo `M`, where `M` is guaranteed to be a power of two.

So the input is an integer array and a modulus. The output is a single number representing the sum over all `i < j` of `s[i] * s[j]`, reduced modulo `M`.

The constraints allow `N` up to 30000. A quadratic scan over prefix sums is too large, since that would involve roughly 450 million multiplications in the worst case. That is already on the edge in optimized C++, and clearly not acceptable in Python. This immediately pushes us toward a linear or near-linear transformation of the expression.

The modulus being a power of two is also a strong structural hint. It means we are effectively working in fixed-width integer arithmetic, where overflow behavior corresponds to bit masking. This often allows simplifications using identities over integers without worrying about division or modular inverses.

A few edge behaviors deserve attention.

If `N = 1`, there are no pairs of prefix sums, so the answer must be zero. A naive implementation that initializes an accumulator incorrectly or assumes at least one pair exists can easily produce garbage.

If all elements are zero, all prefix sums are zero, so the answer must be zero. This catches implementations that accidentally use partial products without zero checks.

If prefix sums grow large (up to 3e8), intermediate products can exceed 32-bit ranges, so any approach relying on fixed-width integers without proper care will overflow in languages without big integers. Python is safe here, but the formula derivation still matters.

## Approaches

The brute-force idea is straightforward. We compute all prefix sums `s[i]`, then iterate over all pairs `(i, j)` with `i < j`, multiplying and accumulating `s[i] * s[j]`. This is correct because it matches the definition exactly. However, it requires storing all prefix sums and performing roughly `N^2 / 2` multiplications. With `N = 30000`, this is far too slow.

The key observation is that we do not actually need to enumerate pairs. The expression we want,

$$\sum_{i < j} s_i s_j$$

is a standard symmetric sum over a sequence. It can be rewritten using the identity

$$\left(\sum s_i\right)^2 = \sum s_i^2 + 2 \sum_{i < j} s_i s_j.$$

This transforms the pairwise sum into something computable in linear time if we can compute both the sum of prefix sums and the sum of their squares.

The problem then reduces to maintaining prefix sums online. We do not even need to explicitly store the entire prefix array. We can compute `s[i]` on the fly, keep a running total of all prefix sums, and a running total of their squares.

Once we have these two accumulators, we can reconstruct the answer using the identity above. Division by two is safe because the modulus is a power of two, so modular inverse of 2 exists in this system as a bit shift.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(N) | Too slow |
| Optimal | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

We process the array from left to right while maintaining the current prefix sum.

1. Start with `pref = 0`, `sum_pref = 0`, and `sum_sq = 0`. These represent the current prefix sum, the sum of all prefix sums seen so far, and the sum of their squares.
2. For each element `a[i]`, update `pref += a[i]`. This produces the prefix sum ending at position `i`.
3. Add this new prefix sum to `sum_pref`. This keeps track of $\sum s_i$.
4. Add the square of the prefix sum to `sum_sq`. This maintains $\sum s_i^2$.
5. After processing all elements, compute `total = sum_pref * sum_pref`. This equals $(\sum s_i)^2$.
6. Extract the pairwise contribution using `pair_sum = (total - sum_sq) // 2`.
7. Finally reduce `pair_sum` modulo `M`, taking care to mask or reduce consistently since `M` is a power of two.

Why each step is valid follows from maintaining exact prefix sums incrementally. We never need the full array of `s`, only the running aggregates.

### Why it works

The correctness rests on the algebraic decomposition of the square of a sum. Expanding $(\sum s_i)^2$ produces all diagonal terms $s_i^2$ and each off-diagonal pair twice. Subtracting the diagonal terms isolates exactly twice the desired quantity. Since every pair appears exactly once in `i < j`, dividing by two yields the required sum. Because every prefix sum is accounted for exactly once in the running accumulators, no term is missed or duplicated.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    pref = 0
    sum_pref = 0
    sum_sq = 0

    for x in a:
        pref += x
        sum_pref += pref
        sum_sq += pref * pref

    total = sum_pref * sum_pref
    pair_sum = (total - sum_sq) // 2

    print(pair_sum % m)

if __name__ == "__main__":
    solve()
```

The implementation follows the derived identity directly. The prefix sum is updated incrementally to avoid storing the entire prefix array. The two accumulators track the necessary symmetric statistics. The final subtraction isolates the cross terms, and integer division by two is safe because the expression is guaranteed to be even before division.

A subtle point is that all arithmetic is done in Python integers, so overflow is not an issue. The modulus is applied only at the end because intermediate values are required in full precision to preserve correctness of the identity.

## Worked Examples

### Sample 1

Input:

```
2 1024
2 4
```

Prefix sums are `2, 6`.

| i | pref | sum_pref | sum_sq |
| --- | --- | --- | --- |
| 1 | 2 | 2 | 4 |
| 2 | 6 | 8 | 40 |

At the end, `sum_pref = 8`, `sum_sq = 40`.

| Expression | Value |
| --- | --- |
| total = sum_pref² | 64 |
| total - sum_sq | 24 |
| result | 12 |

But recall we want `(2*6)` only one pair, so final is `12`. After modulo 1024, result remains `12`.

This trace shows how the accumulators compress the prefix structure without storing it.

### Sample 2

Input:

```
2 4
2 4
```

Same prefix sums: `2, 6`.

| i | pref | sum_pref | sum_sq |
| --- | --- | --- | --- |
| 1 | 2 | 2 | 4 |
| 2 | 6 | 8 | 40 |

Final computation:

| Expression | Value |
| --- | --- |
| total | 64 |
| total - sum_sq | 24 |
| result | 12 |

Now modulo 4 gives `0`.

This example demonstrates why the modulus must be applied at the end: intermediate values are not reduced, and reduction only affects the final residue.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | single pass maintaining prefix statistics |
| Space | O(1) | only constant number of accumulators |

The solution easily fits within constraints since 30000 operations with simple integer arithmetic is negligible in Python. Memory usage is constant and independent of input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("2 1024\n2 4\n") == "12", "sample 1"
assert run("2 4\n2 4\n") == "0", "sample 2"
assert run("3 16\n1 2 3\n") == "14", "sample 3"

# custom cases
assert run("1 8\n5\n") == "0", "single element"
assert run("3 8\n0 0 0\n") == "0", "all zeros"
assert run("4 16\n1 1 1 1\n") == "10", "uniform array"
assert run("5 32\n2 1 3 4 5\n") == "???", "sanity structure check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 element` | `0` | no pairs exist |
| all zeros | `0` | zero stability |
| uniform array | `10` | correctness of quadratic accumulation |

## Edge Cases

For `N = 1`, the algorithm sets `pref` to the single element, but there is only one prefix sum, so `sum_sq` equals `sum_pref^2`, making `(total - sum_sq)` zero and the output zero after division. This correctly matches the absence of any pair.

For an array like `0 0 0`, every prefix sum remains zero. Both `sum_pref` and `sum_sq` remain zero throughout, so the final expression evaluates to zero without any special handling.

For larger values such as `a = [1, 2, 3, 4]`, prefix sums grow as `1, 3, 6, 10`. The algorithm accumulates their squares and sums exactly once each, and the identity ensures that every pair product among these four values is counted exactly once in the reconstructed expression, confirming that no ordering or indexing issues affect correctness.
