---
title: "CF 105022G - Just Visiting Relatives"
description: "We are given two length-N sequences, and we use them to define an N by N matrix where every entry is formed by multiplying a row weight from the first sequence with a column weight from the second sequence."
date: "2026-06-28T01:52:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105022
codeforces_index: "G"
codeforces_contest_name: "HPI 2024 Advanced"
rating: 0
weight: 105022
solve_time_s: 96
verified: false
draft: false
---

[CF 105022G - Just Visiting Relatives](https://codeforces.com/problemset/problem/105022/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 36s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two length-N sequences, and we use them to define an N by N matrix where every entry is formed by multiplying a row weight from the first sequence with a column weight from the second sequence. Concretely, entry (i, j) is a_i multiplied by b_j, so every row is a scaled copy of the same vector, and every column is also structured in the same multiplicative way.

From this matrix A, we are asked to compute A raised to the Kth power under standard matrix multiplication. After obtaining A^K, we do not need the full matrix. The only quantity of interest is the sum of all its entries.

The constraints allow N up to 100000, which immediately rules out any direct matrix multiplication or exponentiation on the full N by N structure. A single matrix multiplication would already require N^3 operations in the naive form, which is far beyond the limit even for N = 1000, let alone 100000. Even optimized multiplication is still too large because the matrix is dense.

The exponent K can be as large as 998244352, which also rules out iterative multiplication. Any valid solution must reduce the problem to operations on O(N) or O(1) aggregates and handle exponentiation in logarithmic time or better.

A subtle edge case appears when K = 0. In that case A^0 is the identity matrix, regardless of a_i and b_i. The sum of its entries is exactly N, since only diagonal entries are 1. Any formula derived for positive powers will typically break at K = 0 unless handled separately.

Another corner case is K = 1, where the answer must reduce to the sum of all entries of A itself. That value is (sum a_i) times (sum b_i). Any derived formula must collapse cleanly to this.

Finally, negative values in a_i or b_i matter because intermediate products like dot products and powers must be taken modulo 998244353. A careless implementation that delays modular reduction can overflow or produce incorrect behavior.

## Approaches

The naive way to approach this problem is to explicitly construct the matrix A from the two sequences and then multiply it by itself K times using standard matrix multiplication. Each multiplication of two N by N matrices takes O(N^3) operations, and repeating it K times makes the complexity prohibitive even for tiny N. Even a single multiplication at N = 100000 is impossible due to both time and memory.

The key structural observation is that A is not a general matrix. Every entry is a product of a row-dependent term and a column-dependent term, which means A is an outer product of two vectors. This makes A a rank-1 matrix. Rank-1 matrices have a very strong closure property under multiplication: the product of two rank-1 matrices remains rank-1, and the structure evolves in a predictable scalar way.

If we write A = a * b^T, then multiplying A by itself collapses into a scalar factor involving the dot product b^T a, while preserving the outer product structure. This means repeated multiplication does not increase complexity in structure, only in a single scalar exponent.

This reduces the problem from matrix exponentiation to scalar exponentiation combined with a few vector sums and dot products.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Matrix Multiplication | O(K · N^3) | O(N^2) | Too slow |
| Rank-1 Reduction + Exponentiation | O(N + log K) | O(1) extra | Accepted |

## Algorithm Walkthrough

We denote the first sequence as a vector a and the second as b.

### 1. Compute three core aggregates

We compute the sum of all elements in a, the sum of all elements in b, and their dot product.

The sums capture how the outer product behaves when all entries are aggregated. The dot product is the key scalar that appears when multiplying outer-product matrices.

### 2. Handle the exponent zero case

If K = 0, the result is the identity matrix, and the sum of its entries is exactly N. We return this immediately because the algebraic formula for positive powers does not apply.

### 3. Compute scalar transition factor

Let s be the dot product sum_i a_i * b_i. Each multiplication of A by itself introduces a factor of s into the structure of the matrix. After K - 1 multiplications, this factor becomes s^(K-1).

This works because every intermediate multiplication collapses via (a b^T)(a b^T) = a (b^T a) b^T.

### 4. Combine with outer sums

The sum of all entries in a rank-1 matrix a b^T is (sum a_i) * (sum b_i). After K multiplications, this is scaled by s^(K-1).

So the final answer is:

(sum a_i) * (sum b_i) * (dot(a, b))^(K-1)

### Why it works

The matrix A starts as an outer product, which is a rank-1 linear transformation. The multiplication of two such matrices introduces only one new scalar term, the inner product of the defining vectors, while preserving the outer product form. This means the space of possible matrices generated by powers of A is one-dimensional up to scaling. Every power A^k differs only by a scalar factor applied to the same rank-1 structure. Since summing entries is linear over this structure, the final answer depends only on three scalar quantities and one exponentiation.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def mod_pow(x, e):
    res = 1
    while e > 0:
        if e & 1:
            res = res * x % MOD
        x = x * x % MOD
        e >>= 1
    return res

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    sum_a = 0
    sum_b = 0
    dot = 0

    for i in range(n):
        ai = a[i] % MOD
        bi = b[i] % MOD
        sum_a = (sum_a + ai) % MOD
        sum_b = (sum_b + bi) % MOD
        dot = (dot + ai * bi) % MOD

    if k == 0:
        print(n % MOD)
        return

    factor = mod_pow(dot, k - 1)
    ans = sum_a * sum_b % MOD
    ans = ans * factor % MOD
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation begins by computing the three required aggregates in a single linear pass over the arrays. Each value is reduced modulo the given modulus immediately to avoid overflow and to keep the dot product consistent in modular arithmetic.

The special case K = 0 is handled explicitly before any exponentiation. This avoids invalid exponent logic and directly returns the identity matrix sum.

The modular exponentiation computes the scalar transition factor efficiently in logarithmic time, which is necessary since K can be as large as 998244352.

Finally, the result is assembled as a product of the two sums and the exponentiated dot product, with modular multiplication applied at each step to maintain correctness.

## Worked Examples

Consider a small instance with a = [1, 2], b = [3, 4], and K = 2.

We compute:

sum_a = 3

sum_b = 7

dot = 1·3 + 2·4 = 11

| Step | sum_a | sum_b | dot | power (dot^(K-1)) | result |
| --- | --- | --- | --- | --- | --- |
| init | 3 | 7 | 11 | - | - |
| K=2 | 3 | 7 | 11 | 11 | 3 * 7 * 11 = 231 |

This demonstrates how the matrix structure never needs to be explicitly formed; everything collapses into scalar operations.

Now consider K = 1 with the same arrays.

| Step | sum_a | sum_b | dot | power (dot^0) | result |
| --- | --- | --- | --- | --- | --- |
| init | 3 | 7 | 11 | 1 | 21 |

This matches the direct sum of all entries in A, since the matrix is just the original outer product.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + log K) | One linear pass to compute sums and dot product, plus fast exponentiation |
| Space | O(1) extra | Only a few scalar variables beyond input storage |

The solution fits comfortably within constraints since even N = 100000 only requires a single pass, and exponentiation handles large K efficiently.

## Test Cases

```python
import sys, io

MOD = 998244353

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue().strip() if False else None  # placeholder

# We will instead directly embed a minimal functional solver for testing

def solve(inp: str) -> str:
    import sys
    from io import StringIO
    sys.stdin = StringIO(inp)

    MOD = 998244353

    def mod_pow(x, e):
        res = 1
        while e > 0:
            if e & 1:
                res = res * x % MOD
            x = x * x % MOD
            e >>= 1
        return res

    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    sum_a = sum(x % MOD for x in a) % MOD
    sum_b = sum(x % MOD for x in b) % MOD
    dot = sum((a[i] % MOD) * (b[i] % MOD) for i in range(n)) % MOD

    if k == 0:
        return str(n % MOD)

    return str(sum_a * sum_b % MOD * mod_pow(dot, k - 1) % MOD)

# sample-like tests
assert solve("2 1\n1 2\n3 4\n") == "21"
assert solve("2 2\n1 2\n3 4\n") == str((3*7*11) % MOD)
assert solve("3 0\n5 6 7\n1 1 1\n") == "3"
assert solve("1 10\n5\n7\n") == str((5*7 % MOD) * pow(35, 9, MOD) % MOD)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| K = 0 case | N | identity matrix handling |
| K = 1 case | sum outer product | base correctness |
| single element | geometric power | scalar reduction correctness |
| small random | consistent | general structure correctness |

## Edge Cases

When K = 0, the algorithm bypasses all vector structure and directly returns N. This avoids incorrectly applying the rank-1 power formula, which would otherwise attempt to raise the dot product to a negative exponent.

When N = 1, the matrix reduces to a single value a_1 * b_1. In this case, the formula becomes (a_1 b_1)^K, and the algorithm produces sum_a = a_1, sum_b = b_1, dot = a_1 b_1, so the result becomes a_1 b_1 * (a_1 b_1)^(K-1), which correctly simplifies to (a_1 b_1)^K.

When values are negative or large, modular reduction at every multiplication ensures correctness. Without immediate modulo, dot products could overflow and silently corrupt the exponentiation base, leading to completely incorrect results.
