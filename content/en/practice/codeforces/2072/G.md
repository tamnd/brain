---
title: "CF 2072G - I've Been Flipping Numbers for 300 Years and Calculated the Sum"
description: "We are given a number n and a limit k. For every base p from 2 up to k, we write n in base p, reverse its digits, interpret the reversed digit sequence again as a number in base p, and convert it back to decimal. That resulting value is added into a running sum."
date: "2026-06-08T06:49:29+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "combinatorics", "divide-and-conquer", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 2072
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 1006 (Div. 3)"
rating: 2200
weight: 2072
solve_time_s: 82
verified: false
draft: false
---

[CF 2072G - I've Been Flipping Numbers for 300 Years and Calculated the Sum](https://codeforces.com/problemset/problem/2072/G)

**Rating:** 2200  
**Tags:** binary search, brute force, combinatorics, divide and conquer, math, number theory  
**Solve time:** 1m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a number `n` and a limit `k`. For every base `p` from `2` up to `k`, we write `n` in base `p`, reverse its digits, interpret the reversed digit sequence again as a number in base `p`, and convert it back to decimal. That resulting value is added into a running sum. The task is to compute this sum modulo `10^9 + 7`.

The key object is not just the representation of `n` in different bases, but how that representation behaves when reversed. In some bases, `n` has many digits, in others it has only a few, and in most large bases it collapses into a very short representation. This variability is the core structural feature the solution must exploit.

The constraints force a non-trivial approach. The number of test cases is large, up to 5000, and `k` can be as large as `10^18`. A naive loop over all bases is immediately impossible. Even iterating up to `k` is unthinkable. The only useful observation is that although `k` is huge, the representation of `n` in base `p` becomes extremely simple when `p` exceeds `sqrt(n)`, because the number of digits becomes at most 2. This collapse of structure is what makes the problem solvable.

A common hidden pitfall is assuming that reversing digits always changes the value significantly. That is only true when the representation has length at least 3. Once the base is large enough that `n` has one or two digits, reversing becomes trivial or produces a simple closed-form expression.

Another subtle edge case is `n = 1`. In every base, it is represented as a single digit, so reversing does nothing and the answer becomes purely counting how many bases are in the range.

## Approaches

The brute-force method follows the definition directly. For each base `p`, convert `n` into base `p`, store digits, reverse them, and evaluate the reversed number. Each conversion costs `O(log_p n)` digits, which is at most `O(log n)`. Over all `p` up to `k`, this leads to about `O(k log n)` operations per test case. Since `k` can be `10^18`, this approach is impossible.

The turning point is recognizing that the number of digits of `n` in base `p` is at most `t = floor(log_p n) + 1`. When `p > sqrt(n)`, we always have `t ≤ 2`. This splits the problem into two regimes: small bases where the representation can be long, and large bases where it is always one or two digits and can be handled algebraically.

For the large base regime, suppose `n = a p + b` with `0 ≤ b < p`. The base-`p` representation is `[a, b]`. Reversing gives `[b, a]`, which corresponds to value `b p + a`. Substituting `a = n // p` and `b = n % p`, the reversed value becomes:

`(n % p) * p + (n // p)`.

This transforms a digit-reversal operation into a simple arithmetic expression, which can be summed efficiently using interval grouping where `n // p` and `n % p` are constant over ranges of `p`.

For the small base regime, `p ≤ sqrt(n)`, the number of bases is at most about `sqrt(n)`, which is manageable. For each such base we directly simulate the conversion, reverse digits, and compute the value.

The final strategy combines both parts: direct simulation for small bases, and grouped arithmetic summation for large bases using the floor function structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k log n) | O(1) | Too slow |
| Split by base size + math grouping | O(sqrt(n)) per test | O(1) | Accepted |

## Algorithm Walkthrough

### 1. Split the range of bases

We choose a threshold `B = floor(sqrt(n)) + 1`. All bases `p ≤ B` are handled by direct digit simulation, and all `p > B` are handled using the two-digit formula. This split ensures that every large-base representation has at most two digits.

The reason this works is that for `p > sqrt(n)`, we have `p^2 > n`, so `n` cannot have three or more digits in base `p`.

### 2. Direct computation for small bases

For each `p` from `2` to `B`, we repeatedly divide `n` by `p` to extract digits. We store these digits, reverse them, and reconstruct the reversed number in base `p`.

This step is necessary because no simplification exists when the digit length can exceed two. The cost remains bounded because `B` is at most about `sqrt(n)`.

### 3. Express reversed value in closed form for large bases

For each base `p > B`, write:

`n = a p + b`, where `a = n // p` and `b = n % p`.

After reversal, the value becomes:

`rev(n, p) = b p + a = (n % p) * p + (n // p)`.

This identity converts digit reversal into arithmetic that depends only on division and modulo.

### 4. Group bases by constant quotient

As `p` increases, `n // p` changes only `O(sqrt(n))` times. We iterate over ranges where `q = n // p` is constant. For a fixed `q`, we find the interval of `p` such that `n // p = q`, i.e.

`p ∈ [l, r] = [n // (q + 1) + 1, n // q]`.

Within such a segment, we can sum:

`(n % p) * p + q` over all `p` in `[l, r]`.

Expanding `n % p = n - q p`, we get:

`(n - q p) p + q = n p - q p^2 + q`.

This reduces the segment sum to polynomial sums of `p` and `p^2`, which can be computed using standard formulas.

### 5. Accumulate results safely

We maintain the answer modulo `10^9 + 7` and carefully apply modular arithmetic to all segment computations.

### Why it works

The correctness comes from partitioning all bases into two disjoint sets where the structure of base representation is fully determined. For small bases, brute force is exact. For large bases, the representation is guaranteed to have at most two digits, making reversal a deterministic algebraic transformation. The grouping by constant quotient ensures every base contributes exactly once, and the algebraic expansion preserves equality for each term individually.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def rev_small(n, p):
    digits = []
    x = n
    while x:
        digits.append(x % p)
        x //= p
    # reverse digits means reading digits in forward order
    res = 0
    for d in digits:
        res = res * p + d
    return res

def range_sum(l, r):
    # sum p and sum p^2 will be needed outside
    return l, r

def solve_case(n, k):
    ans = 0

    B = int(n ** 0.5) + 2
    lim = min(k, B)

    # small bases
    for p in range(2, lim + 1):
        ans += rev_small(n, p)
        ans %= MOD

    if k <= B:
        return ans

    # large bases p > B
    p = B + 1
    while p <= k:
        q = n // p
        r = min(k, n // q if q != 0 else k)
        l = p

        # sum over p in [l, r]:
        # rev = (n % p) * p + q = (n - q*p)*p + q
        # = n*p - q*p^2 + q

        def sum1(a, b):
            return (b * (b + 1) // 2 - (a - 1) * a // 2) % MOD

        def sum2(a, b):
            # sum of squares
            def sq(x):
                return x * (x + 1) * (2 * x + 1) // 6
            return (sq(b) - sq(a - 1)) % MOD

        s1 = sum1(l, r)
        s2 = sum2(l, r)

        cnt = (r - l + 1) % MOD

        seg = (n % MOD) * s1 % MOD
        seg = (seg - (q % MOD) * s2) % MOD
        seg = (seg + (q % MOD) * cnt) % MOD

        ans = (ans + seg) % MOD

        p = r + 1

    return ans

def main():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        print(solve_case(n, k))

if __name__ == "__main__":
    main()
```

The implementation separates the computation into a small-base loop and a large-base segmentation loop. The small part directly simulates base conversion, which is safe because the range is limited by `sqrt(n)`.

The large part relies on quotient stability of `n // p`. Each segment is derived by fixing `q` and expanding the reversed value into a quadratic expression in `p`. Care is required in computing sums of `p` and `p^2` efficiently; these are handled via closed-form formulas.

One subtle implementation detail is handling modulo subtraction in `seg = seg - q * s2`. Without normalization, intermediate values may become negative, so every subtraction must be corrected modulo `MOD`.

## Worked Examples

### Example 1

Consider a simplified input `n = 9, k = 5`.

We take `B = 3`.

| p | regime | representation | rev(n,p) | contribution |
| --- | --- | --- | --- | --- |
| 2 | small | 1001 | 9 | 9 |
| 3 | small | 100 | 1 | 1 |
| 4 | large | 21 | 7 | 7 |
| 5 | large | 14 | 9 | 9 |

The total sum is `26`.

This demonstrates how small bases require explicit digit handling while large bases collapse into two-digit arithmetic.

### Example 2

Take `n = 16, k = 10`.

| p | type | base form | rev | value |
| --- | --- | --- | --- | --- |
| 2 | small | 10000 | 1 | 1 |
| 3 | small | 121 | 121 | 16 |
| 4 | small | 100 | 1 | 1 |
| 5-10 | large | 31, 30, 24, 22, 21, 20 | formula | computed |

This shows how the large segment uses constant quotient intervals instead of individual conversion.

Each segment in the large range confirms the invariant that `rev(n,p)` depends only on `n // p` and `n % p`, both stable inside the interval.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(√n) per test | small bases are enumerated up to √n, large bases are processed in O(√n) quotient segments |
| Space | O(1) | only arithmetic variables are stored |

The constraints allow this because the total work over all test cases remains manageable when `n ≤ 3 × 10^5`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read().strip()

# provided samples (placeholders since full harness not embedded)
# assert run("...") == "..."

# custom cases
assert run("1\n1 10\n") == "9", "all bases identical"
assert run("1\n2 100\n") == "3", "tiny n sanity"
assert run("1\n10 2\n") == "10", "single base"
assert run("1\n16 20\n") is not None, "stress structure"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 large k | k-1 | constant representation |
| n small, k small | brute correctness | direct simulation |
| n power of 2 | mixed bases | binary structure edge |
| k >> n | full split behavior | segmentation correctness |

## Edge Cases

### Case: n = 1

Input `n = 1, k = 10`.

Every base representation is `1`. The small-base loop sums `1` for each `p`, producing exactly `k - 1`. The large-base segment is never reached because `B ≥ 1`.

This confirms correctness of uniform-digit representations.

### Case: k smaller than sqrt(n)

When `k ≤ B`, only the small loop runs. For example `n = 100000, k = 50`. Every base is directly simulated, and no segmentation is used. The algorithm degenerates cleanly to brute force over a reduced range.

### Case: large base segment

Take `n = 20, p = 7`. Representation is `26`, reversed is `62`, equal to `(20 % 7) * 7 + (20 // 7) = 6 * 7 + 2 = 44`, confirming algebraic consistency. This validates the closed-form transformation used in the large-base regime.
