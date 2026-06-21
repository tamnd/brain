---
title: "CF 105791D - Darts"
description: "Each test describes a simple structured battle: there are n waves of enemies, and the i-th wave contains exactly i balloons. Every balloon in a wave has the same power level k, and the cost of destroying a single balloon is i raised to the power k."
date: "2026-06-21T14:24:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105791
codeforces_index: "D"
codeforces_contest_name: "UFPE Starters Final Try-Outs 2025"
rating: 0
weight: 105791
solve_time_s: 58
verified: true
draft: false
---

[CF 105791D - Darts](https://codeforces.com/problemset/problem/105791/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test describes a simple structured battle: there are n waves of enemies, and the i-th wave contains exactly i balloons. Every balloon in a wave has the same power level k, and the cost of destroying a single balloon is i raised to the power k. So the total number of darts needed for the whole level is the sum of i^k over all i from 1 to n.

In other words, the task is to compute a classic power sum of the form S_k(n) = 1^k + 2^k + … + n^k under a large modulus.

The difficulty is not the definition but the scale. The number of terms n can be as large as 10^9, so iterating over all i is impossible. The exponent k is at most 1000, which suggests a polynomial structure in k rather than in n.

A naive implementation would try to loop from 1 to n for each test case and accumulate i^k. This immediately fails even for a single test with n = 10^9 because it would require a billion modular exponentiations.

Another common failure is precomputing powers for all i up to n. This also breaks memory and time constraints since n is too large to materialize.

A more subtle edge case is when k = 0 or k = 1. For k = 0, every term is 1 and the answer is n, and for k = 1 the answer is n(n+1)/2. Any general formula must degenerate correctly to these cases without numerical instability.

## Approaches

The brute force method evaluates each term i^k directly and sums them. This is mathematically correct but computationally infeasible. For each test case, it performs O(n) exponentiations, and each exponentiation costs O(log k), leading to roughly 10^9 operations per test in the worst case, which is far beyond any time limit.

The key observation is that S_k(n) is not an arbitrary function of n. It is a polynomial in n of degree k+1. This is a well known fact about sums of powers and can be derived using finite differences or binomial expansion identities involving Stirling numbers.

Once we accept that structure, the problem becomes one of evaluating a polynomial efficiently at a large point n. Instead of iterating over i, we rewrite i^k using Stirling numbers of the second kind:

i^k = sum over j from 0 to k of S(k, j) * j! * C(i, j)

Now summing over i from 1 to n, we can swap summations:

S_k(n) = sum over j of S(k, j) * j! * sum over i of C(i, j)

The inner sum has a clean closed form:

sum_{i=1..n} C(i, j) = C(n+1, j+1)

This reduces the entire problem to computing Stirling numbers for fixed k and evaluating a few binomial coefficients at n.

So instead of iterating over n, we only iterate over k, which is at most 1000.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · log k) | O(1) | Too slow |
| Stirling + combinatorics | O(k^2) per test | O(k^2) | Accepted |

## Algorithm Walkthrough

1. Read n and k for a test case. The goal is to compute S_k(n), the sum of i^k over i from 1 to n.
2. Precompute Stirling numbers of the second kind S(k, j) for the given k using the recurrence S(k, j) = j * S(k-1, j) + S(k-1, j-1). This builds the coefficients that convert powers into combinations.
3. Precompute factorials up to k since each term also involves a multiplier j!. This allows constant-time access during evaluation.
4. For each j from 0 to k, compute the binomial coefficient C(n+1, j+1). Since n is large, compute it as a falling product (n+1)(n)…(n-j+1) divided by (j+1)! under modulo arithmetic.
5. For each j, multiply S(k, j), j!, and C(n+1, j+1), and accumulate the result into the answer.
6. Output the final sum modulo 10^9 + 7.

Why it works: the transformation replaces each monomial i^k with a linear combination of binomial basis functions C(i, j). The sum over i of these basis functions collapses into a single binomial term C(n+1, j+1), so the entire summation becomes a finite linear combination of closed forms rather than a long prefix sum. The correctness comes from the identity that both representations agree on all integer i, so their sums over any prefix must also agree.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def build_stirling(k):
    S = [[0] * (k + 1) for _ in range(k + 1)]
    S[0][0] = 1
    for i in range(1, k + 1):
        for j in range(1, i + 1):
            S[i][j] = (S[i - 1][j - 1] + j * S[i - 1][j]) % MOD
    return S

def solve():
    t = int(input())
    tests = []
    max_k = 0
    for _ in range(t):
        n, k = map(int, input().split())
        tests.append((n, k))
        max_k = max(max_k, k)

    fact = [1] * (max_k + 2)
    invfact = [1] * (max_k + 2)
    for i in range(1, max_k + 2):
        fact[i] = fact[i - 1] * i % MOD

    invfact[max_k + 1] = pow(fact[max_k + 1], MOD - 2, MOD)
    for i in range(max_k, -1, -1):
        invfact[i] = invfact[i + 1] * (i + 1) % MOD

    stir = build_stirling(max_k)

    for n, k in tests:
        if k == 0:
            print(n % MOD)
            continue

        ans = 0
        # compute C(n+1, j+1) using falling product
        for j in range(0, k + 1):
            # compute numerator (n+1)P(j+1)
            num = 1
            x = n + 1
            for t2 in range(j + 1):
                num = num * (x - t2) % MOD

            comb = num * invfact[j + 1] % MOD

            ans = (ans + stir[k][j] * fact[j] % MOD * comb) % MOD

        print(ans % MOD)

if __name__ == "__main__":
    solve()
```

The solution is structured around separating preprocessing from per-test computation. Stirling numbers are computed once up to the maximum k across all tests, which avoids recomputation. Factorials and inverse factorials are also precomputed once for fast binomial evaluation.

Inside each test, the binomial term C(n+1, j+1) is computed using a falling product rather than factorials of n, since n is too large for direct factorial-based combinations. This avoids overflow and keeps all arithmetic modular.

A common pitfall is forgetting that the sum starts at i = 1, which is why the identity produces C(n+1, j+1) instead of C(n, j+1).

## Worked Examples

Consider n = 3, k = 2. The correct answer is 1^2 + 2^2 + 3^2 = 14.

We compute Stirling numbers for k = 2: S(2,1) = 1, S(2,2) = 1.

| j | S(k,j) | j! | C(n+1,j+1) | Contribution |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 | C(4,1)=4 | 0 |
| 1 | 1 | 1 | C(4,2)=6 | 6 |
| 2 | 1 | 2 | C(4,3)=4 | 8 |

Summing gives 14.

This confirms that the transformation matches direct evaluation and that higher-order structure correctly collapses into binomial terms.

Now consider n = 5, k = 1. The expected result is 1 + 2 + 3 + 4 + 5 = 15.

| j | S(1,j) | j! | C(6,j+1) | Contribution |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 6 | 0 |
| 1 | 1 | 1 | 15 | 15 |

This confirms that the formula reduces correctly to the triangular number identity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k^2) per test | Stirling DP dominates, binomial evaluation is O(k) |
| Space | O(k^2) | storage for Stirling table |

The constraints keep k at most 1000, so even quadratic preprocessing fits comfortably. The number of tests is small enough that repeated O(k^2) work remains within limits.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    def build_stirling(k):
        S = [[0] * (k + 1) for _ in range(k + 1)]
        S[0][0] = 1
        for i in range(1, k + 1):
            for j in range(1, i + 1):
                S[i][j] = (S[i - 1][j - 1] + j * S[i - 1][j]) % MOD
        return S

    t = int(input())
    tests = []
    max_k = 0
    for _ in range(t):
        n, k = map(int, input().split())
        tests.append((n, k))
        max_k = max(max_k, k)

    fact = [1] * (max_k + 2)
    invfact = [1] * (max_k + 2)
    for i in range(1, max_k + 2):
        fact[i] = fact[i - 1] * i % MOD
    invfact[max_k + 1] = pow(fact[max_k + 1], MOD - 2, MOD)
    for i in range(max_k, -1, -1):
        invfact[i] = invfact[i + 1] * (i + 1) % MOD

    stir = build_stirling(max_k)

    out = []
    for n, k in tests:
        if k == 0:
            out.append(str(n % MOD))
            continue
        ans = 0
        for j in range(k + 1):
            num = 1
            x = n + 1
            for t2 in range(j + 1):
                num = num * (x - t2) % MOD
            comb = num * invfact[j + 1] % MOD
            ans = (ans + stir[k][j] * fact[j] % MOD * comb) % MOD
        out.append(str(ans % MOD))

    return "\n".join(out)

# provided samples (placeholders since original sample output not fully visible)
# basic sanity checks
assert run("1\n3 2\n") == "14"
assert run("1\n5 1\n") == "15"
assert run("1\n10 0\n") == "10"

# custom cases
assert run("1\n1 100\n") == "1", "n=1 edge"
assert run("1\n10 2\n") == str((1*1 + 2*2 + 3*3 + 4*4 + 5*5 + 6*6 + 7*7 + 8*8 + 9*9 + 10*10) % MOD), "square sum"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1 100 | 1 | large k, minimal n |
| 1\n10 2 | 385 | correctness of quadratic sum |
| 1\n5 1 | 15 | linear case |

## Edge Cases

When k = 0, every term i^0 equals 1, so the sum should equal n. In the algorithm, this bypasses Stirling expansion entirely and directly returns n modulo MOD, which matches the identity C(n+1,1) = n+1 but shifted by the correct indexing of the sum starting at 1.

When n = 1, all higher structure collapses because the sum contains a single term. The binomial evaluation produces C(2, j+1), which is nonzero only for j = 0, ensuring the result is always 1^k = 1 regardless of k.

When k is large relative to n, many higher Stirling terms still appear in the computation, but binomial coefficients C(n+1, j+1) vanish naturally for j > n, so the formula remains stable and avoids unnecessary contribution from large indices.
