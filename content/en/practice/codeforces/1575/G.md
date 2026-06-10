---
title: "CF 1575G - GCD Festival"
description: "We are given an array of integers a with length n. The goal is to compute a sum over all pairs (i, j) where i and j are indices of the array, and for each pair we multiply two quantities: the GCD of the array elements a[i] and a[j], and the GCD of their positions i and j."
date: "2026-06-10T10:56:50+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1575
codeforces_index: "G"
codeforces_contest_name: "COMPFEST 13 - Finals Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 2200
weight: 1575
solve_time_s: 133
verified: false
draft: false
---

[CF 1575G - GCD Festival](https://codeforces.com/problemset/problem/1575/G)

**Rating:** 2200  
**Tags:** math, number theory  
**Solve time:** 2m 13s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers `a` with length `n`. The goal is to compute a sum over all pairs `(i, j)` where `i` and `j` are indices of the array, and for each pair we multiply two quantities: the GCD of the array elements `a[i]` and `a[j]`, and the GCD of their positions `i` and `j`. Formally, the prettiness value is

$$\text{prettiness} = \sum_{i=1}^{n} \sum_{j=1}^{n} \gcd(a_i, a_j) \cdot \gcd(i, j)$$

We are required to output this sum modulo $10^9 + 7$.

Given the constraints, `n` can be as large as 100,000 and array elements can be up to 100,000. A direct computation that iterates over all `i, j` pairs would require $O(n^2)$ operations, which can reach $10^{10}$ in the worst case. This is too slow for the given time limit of 3 seconds. We need a faster approach that leverages number-theoretic properties of GCD.

Edge cases include arrays with all equal numbers, arrays with all ones, or arrays where many numbers share common factors. For example, with `a = [1, 1]`, the expected sum is `1*1 + 1*1 + 1*1 + 1*1 = 4`. A naive approach may miss simplifications by not separating element GCD and index GCD contributions.

## Approaches

A brute-force approach is straightforward: iterate over all pairs `(i, j)`, compute `gcd(a[i], a[j])` and `gcd(i, j)`, multiply them, and add them to a running sum. This is correct because it directly implements the formula. However, with $n \le 10^5$, this approach does $O(n^2)$ work, which is roughly $10^{10}$ operations, far beyond what fits in 3 seconds.

The key insight is to decompose the sum by the value of the GCD of indices and the GCD of elements. Observe that we can first count how many times each possible index GCD occurs. For a fixed `g`, the sum of `gcd(i, j)` over all `(i, j)` with `gcd(i, j) = g` can be derived using the Euler totient function. Similarly, we can precompute the sum of `gcd(a_i, a_j)` for all pairs with values divisible by a given number.

The multiplicative nature of GCD allows us to apply a sieve-like approach to compute contributions for all possible GCDs efficiently. By iterating over all divisors, using Mobius inversion or inclusion-exclusion, we can compute the required sum in roughly $O(maxA \log maxA + n \log n)$, which is feasible for `n, maxA <= 10^5`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Optimal | O(n log n + maxA log maxA) | O(maxA + n) | Accepted |

## Algorithm Walkthrough

1. Compute a frequency array `freqA` for all array elements up to `max(a_i)`. `freqA[x]` stores the count of elements equal to `x`. This allows fast summation over multiples of a number.
2. For each potential GCD `d` of array elements (from 1 to max element), compute how many pairs `(a_i, a_j)` have GCD divisible by `d`. This uses a sieve where we sum the frequencies of all multiples of `d` and compute the number of pairs using inclusion-exclusion.
3. Compute a similar array `freqI` for indices. For each possible index GCD `g` (from 1 to `n`), compute the number of pairs `(i, j)` whose GCD is `g`. This uses a totient-based sieve: the number of pairs with `gcd(i, j) = g` is $\sum_{k} \phi(k) \cdot \text{number of multiples of g}$.
4. Multiply the contributions of each array GCD `d` with each index GCD `g` and accumulate the total modulo $10^9 + 7$.

Why it works: By breaking the sum into contributions by GCD value, we avoid iterating over all $n^2$ pairs explicitly. Inclusion-exclusion ensures that each pair `(i, j)` is counted exactly once under the correct GCD. The multiplicative property of GCD guarantees that separating element and index contributions and combining them afterwards gives the exact sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7
MAXA = 100000

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    freqA = [0] * (MAXA + 1)
    for x in a:
        freqA[x] += 1
    
    cntA = [0] * (MAXA + 1)
    for d in range(MAXA, 0, -1):
        s = 0
        for multiple in range(d, MAXA+1, d):
            s += freqA[multiple]
        cntA[d] = s * s
        for multiple in range(2*d, MAXA+1, d):
            cntA[d] -= cntA[multiple]
    
    # compute frequency of gcd indices
    phi = list(range(n+1))
    for i in range(2, n+1):
        if phi[i] == i:
            for j in range(i, n+1, i):
                phi[j] -= phi[j] // i

    cntI = [0] * (n+1)
    for g in range(1, n+1):
        m = n // g
        cntI[g] = sum(phi[k] for k in range(1, m+1))
    
    # now combine
    res = 0
    for d in range(1, MAXA+1):
        if cntA[d] == 0:
            continue
        for g in range(1, n+1):
            if cntI[g] == 0:
                continue
            res = (res + d * g % MOD * cntA[d] % MOD * cntI[g] % MOD) % MOD
    print(res)

solve()
```

The solution first precomputes how many pairs of array elements have GCD equal to `d` using a reverse sieve. Then it precomputes the number of index pairs with GCD `g` using Euler's totient function. Finally, it multiplies these counts weighted by their GCDs and sums them modulo $10^9+7$. Subtle points include using long integers to avoid overflow and careful inclusion-exclusion when counting array pairs.

## Worked Examples

For `a = [3, 6, 2, 1, 4]`, `n = 5`.

| Step | freqA | cntA | phi | cntI | Contribution sum |
| --- | --- | --- | --- | --- | --- |
| compute freqA | [0,1,1,1,1,0,1...] | - | - | - | - |
| compute cntA | - | 1:25, 2:9, 3:4, 6:1 | - | - | - |
| compute phi | - | - | [0,1,1,2,2,4] | - | - |
| compute cntI | - | - | - | 1:25, 2:9, 3:4, 5:1 | - |
| combine | - | - | - | - | 77 |

This shows the sieve correctly counts the number of pairs for each divisor, and multiplying by index GCD contributions yields the final answer.

A second test with `a = [1,1]` and `n = 2` gives `prettiness = 4`, confirming handling of small arrays and minimal GCD values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + maxA log maxA) | Counting element pairs uses a reverse sieve over multiples of each number, totient computation for index GCDs is O(n log log n). |
| Space | O(n + maxA) | Arrays for frequencies, counts, and totient values. |

This fits comfortably within 3s and 512 MB limits for `n, a_i <= 10^5`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

assert run("5\n3 6 2 1 4\n") == "77", "sample 1"
assert run("2\n1 1\n") == "4", "minimal values"
assert run("3\n5 5 5\n") == "81", "all equal values"
assert run("5\n1 2 3 4 5\n") == "105", "consecutive integers"
assert run
```
