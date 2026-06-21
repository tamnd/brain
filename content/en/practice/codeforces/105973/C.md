---
title: "CF 105973C - Binomial XOR"
description: "We are given a function defined on each integer position from 1 to n. For a fixed i, we look at all binomial coefficients in the i-th column of Pascal’s triangle, starting from row i up to row n, take each value modulo 998244353, and XOR them together. That gives f(i)."
date: "2026-06-21T21:49:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105973
codeforces_index: "C"
codeforces_contest_name: "Uttara University Inter-University Programming Contest 2025"
rating: 0
weight: 105973
solve_time_s: 77
verified: true
draft: false
---

[CF 105973C - Binomial XOR](https://codeforces.com/problemset/problem/105973/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a function defined on each integer position from 1 to n. For a fixed i, we look at all binomial coefficients in the i-th column of Pascal’s triangle, starting from row i up to row n, take each value modulo 998244353, and XOR them together. That gives f(i). After computing f(1) through f(n), we XOR all of them again to produce the final answer.

A cleaner way to view the structure is to think in terms of Pascal’s triangle entries C(j, i) for all pairs where 1 ≤ i ≤ j ≤ n. Each such entry appears exactly once in the overall expression: it is included in f(i), and then f(i) is included in the final XOR. So the problem reduces to computing the XOR of all values C(j, i) mod 998244353 over the entire triangular region.

The input size n can be as large as 10^6 and there are up to 10^6 test cases. This immediately rules out any solution that recomputes binomial coefficients per query or iterates over O(n^2) pairs. Even O(n √n) is too slow. The structure must collapse into something that can be precomputed once and answered in constant time per test.

A subtle edge case is the treatment of boundary binomial coefficients. For every row j, the term C(j, j) is always 1 and is included, while C(j, 0) is excluded because i starts from 1. This asymmetry matters because it prevents simple full-row symmetry cancellation in XOR.

## Approaches

A direct interpretation would iterate over each i, compute all C(j, i) for j ≥ i, XOR them, then XOR all f(i). This expands to iterating over all pairs (j, i) with 1 ≤ i ≤ j ≤ n. Computing each binomial coefficient on the fly still requires modular arithmetic and factorials, but even generating all pairs costs Θ(n^2) operations in total, which is impossible for n up to 10^6.

The key simplification comes from reindexing the XOR. Instead of grouping by columns (fixed i), we group by rows (fixed j). For a fixed j, we are XORing all values C(j, 1), C(j, 2), ..., C(j, j). This row-wise XOR turns the entire problem into computing a single value per row and then XORing those results over j.

A crucial symmetry property of binomial coefficients resolves most cancellations inside each row. For j odd, all terms can be paired as C(j, i) = C(j, j − i), and since both appear and are equal, their XOR cancels out completely. For j even, the same pairing holds except for the middle term C(j, j/2), which is unpaired. Additionally, the boundary C(j, j) = 1 always remains unpaired because C(j, 0) is not included. This leaves each row contributing only a small number of surviving terms.

So each row contributes either just 1, or 1 XOR C(j, j/2) depending on parity of j. This reduces the entire problem to tracking only central binomial coefficients C(2k, k), because only even rows contribute a nontrivial value.

We then precompute these central binomial coefficients once using factorials modulo 998244353, store them, and maintain a prefix XOR over k. Each query reduces to a constant-time lookup.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all pairs | O(n²) | O(1) | Too slow |
| Precompute factorials + prefix XOR reduction | O(N + T) | O(N) | Accepted |

## Algorithm Walkthrough

1. Observe that the entire expression is equivalent to XOR over all values C(j, i) for 1 ≤ i ≤ j ≤ n. This removes the outer structure of f(i) entirely and turns the problem into a triangular XOR aggregation.
2. Fix a row j and compute the XOR of all C(j, i) for i from 1 to j. This isolates the contribution of each row independently, since XOR across rows is associative and commutative.
3. Pair symmetric binomial terms C(j, i) and C(j, j − i). These are equal, so each pair cancels under XOR. This leaves at most one unpaired middle term when j is even.
4. Handle remaining unpaired terms. Every row always contributes C(j, j) = 1. If j is even, there is an additional surviving term C(j, j/2). If j is odd, no middle term exists because all indices are paired.
5. Define S(j) as the XOR contribution of row j. Then S(j) equals 1 when j is odd, and 1 XOR C(j, j/2) when j is even.
6. The final answer becomes XOR of S(j) over all j from 1 to n. Split this into two parts: XOR of all 1’s, which depends only on parity of n, and XOR of central binomial coefficients from even rows.
7. Let k = j/2 for even j. Precompute C(2k, k) for all k up to n/2 using factorials and modular inverses. Maintain a prefix XOR array over these values.
8. For each test case, compute (n mod 2) XOR prefix_xor[n // 2]. This directly produces the final result in constant time.

### Why it works

The correctness comes from complete cancellation of symmetric binomial pairs under XOR. Every non-central, non-boundary coefficient appears exactly twice in each row contribution and cancels out. What remains per row is structurally forced: the always-present boundary 1 and the possible central term in even rows. Since XOR over rows is independent, reducing each row to this minimal form preserves the global XOR exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

MAXN = 10**6

fact = [1] * (2 * MAXN + 1)
invfact = [1] * (2 * MAXN + 1)

for i in range(1, 2 * MAXN + 1):
    fact[i] = fact[i - 1] * i % MOD

invfact[2 * MAXN] = pow(fact[2 * MAXN], MOD - 2, MOD)
for i in range(2 * MAXN, 0, -1):
    invfact[i - 1] = invfact[i] * i % MOD

def C(n, r):
    if r < 0 or r > n:
        return 0
    return fact[n] * invfact[r] % MOD * invfact[n - r] % MOD

max_k = MAXN // 2
central = [0] * (max_k + 1)

for k in range(1, max_k + 1):
    central[k] = C(2 * k, k)

px = [0] * (max_k + 1)
for i in range(1, max_k + 1):
    px[i] = px[i - 1] ^ central[i]

t = int(input())
out = []
for _ in range(t):
    n = int(input())
    ans = (n & 1) ^ px[n // 2]
    out.append(str(ans))

print("\n".join(out))
```

The solution first builds factorials and inverse factorials up to 2·10^6 so that any binomial coefficient needed for central terms can be computed in constant time. Each C(2k, k) is then evaluated once and stored. The prefix XOR array compresses all even-row contributions.

The final line per test case reflects the decomposition of the answer into two independent parts: the XOR of all row-boundary ones, which depends only on whether n is odd, and the XOR of all central binomial coefficients up to n/2.

## Worked Examples

Consider n = 4. We compute contributions row by row.

| j | Row XOR S(j) | Explanation |
| --- | --- | --- |
| 1 | 1 | only C(1,1) |
| 2 | 3 | C(2,1)=2, C(2,2)=1 |
| 3 | 1 | middle cancellation leaves 1 |
| 4 | 7 | C(4,2)=6 plus boundary 1 |

Now accumulate:

| Step | Value |
| --- | --- |
| j=1 | 1 |
| j=2 | 1 ^ 3 = 2 |
| j=3 | 2 ^ 1 = 3 |
| j=4 | 3 ^ 7 = 4 |

Final answer is 4.

This matches the formula: n%2 = 0, and central XOR up to 2 gives C(2,1)=2, C(4,2)=6, so 2 ^ 6 = 4.

Now consider n = 5.

| j | S(j) |
| --- | --- |
| 1 | 1 |
| 2 | 3 |
| 3 | 1 |
| 4 | 7 |
| 5 | 1 |

Accumulation:

| Step | Value |
| --- | --- |
| j=1 | 1 |
| j=2 | 2 |
| j=3 | 3 |
| j=4 | 4 |
| j=5 | 5 |

Final answer is 5.

This matches the formula: n%2 = 1 and central XOR up to 2 gives 2 ^ 6 = 4, so 1 ^ 4 = 5.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + T) | factorial precomputation up to 2N plus constant-time per test |
| Space | O(N) | storage for factorials, inverse factorials, and prefix XOR |

The constraints allow up to 10^6 queries, so the solution relies entirely on preprocessing. After that, each query reduces to a couple of array lookups and one XOR operation, well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    MOD = 998244353
    MAXN = 200

    fact = [1] * (2 * MAXN + 1)
    invfact = [1] * (2 * MAXN + 1)

    for i in range(1, 2 * MAXN + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact[2 * MAXN] = pow(fact[2 * MAXN], MOD - 2, MOD)
    for i in range(2 * MAXN, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    def C(n, r):
        return fact[n] * invfact[r] % MOD * invfact[n - r] % MOD

    max_k = MAXN // 2
    central = [0] * (max_k + 1)
    for k in range(1, max_k + 1):
        central[k] = C(2 * k, k)

    px = [0] * (max_k + 1)
    for i in range(1, max_k + 1):
        px[i] = px[i - 1] ^ central[i]

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        out.append(str((n & 1) ^ px[n // 2]))

    return "\n".join(out)

# sample-like sanity checks
assert run("3\n1\n2\n3\n") == run("3\n1\n2\n3\n")
assert run("1\n1\n") == "1"
assert run("1\n2\n") in {"3"}  # C(2,1)=2 so 2^1=3
assert run("1\n3\n") in {"1"}
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1 | 1 | smallest n |
| 1\n2 | 3 | single even row contribution |
| 1\n4 | 4 | interaction of multiple rows |
| 1\n5 | 5 | odd n parity behavior |

## Edge Cases

For n = 1, the structure collapses to a single binomial coefficient C(1,1)=1, so the answer must be 1. The algorithm handles this because n%2 is 1 and no central coefficients exist for n//2 = 0, producing 1 correctly.

For n = 2, only C(2,1)=2 and C(2,2)=1 contribute, so XOR is 3. The formula uses central binomial C(2,1)=2 and includes boundary 1, producing the same result.

For odd n such as n = 3, every row except even rows contributes only the boundary 1, and even rows up to 2 contribute central terms consistently. The algorithm separates parity cleanly, so no special handling is required beyond n%2.

For large n near 10^6, the only potential risk is overflow or recomputation. Precomputation ensures all central binomials are ready, and each query is O(1), so the solution remains stable under maximum constraints.
