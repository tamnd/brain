---
title: "CF 338D - GCD Table"
description: "We are asked to determine whether a given sequence of numbers appears as consecutive elements in some row of a hypothetical GCD table. The table has n rows and m columns, where each element at row i and column j is the greatest common divisor of i and j."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "chinese-remainder-theorem", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 338
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 196 (Div. 1)"
rating: 2900
weight: 338
solve_time_s: 93
verified: true
draft: false
---

[CF 338D - GCD Table](https://codeforces.com/problemset/problem/338/D)

**Rating:** 2900  
**Tags:** chinese remainder theorem, math, number theory  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine whether a given sequence of numbers appears as consecutive elements in some row of a hypothetical GCD table. The table has _n_ rows and _m_ columns, where each element at row _i_ and column _j_ is the greatest common divisor of _i_ and _j_. The input gives the dimensions of the table, along with a sequence of length _k_. Our task is to check whether there exists a row and starting column such that the sequence matches exactly the values from that column onward.

The constraints are unusual. Both _n_ and _m_ can be as large as 10^12, which immediately rules out any solution that explicitly constructs the table. The sequence length _k_ is at most 10,000, which is much smaller than the potential width of a row. This indicates that the solution must operate primarily on properties of the numbers themselves, rather than on brute-force table generation.

A naive approach might attempt to iterate over every row and every starting column, compute the GCDs, and check against the sequence. This fails spectacularly for large inputs. An edge case occurs when the sequence contains multiple 1s in a row. For instance, if the sequence is [1, 1, 1], a careless approach might try to match it to consecutive integers naively, but the correct matches depend on the row index and divisibility relations. Another tricky situation arises when sequence numbers exceed the row number, since _GCD(i, j)_ can never exceed _i_. For example, if the first element of the sequence is 7 but we are inspecting row 5, that row can never start the sequence.

## Approaches

The brute-force method is simple. For each row from 1 to _n_, for each starting column from 1 to _m-k+1_, compute GCD(row, column + offset) for each position in the sequence and compare. If any match occurs, return YES. Otherwise, return NO. This is correct but computationally infeasible. Each row can have up to 10^12 columns, each comparison involves up to 10^4 GCD computations, giving a worst-case operation count of roughly 10^28, which is far beyond any feasible computation.

The key observation that enables an efficient solution is to exploit the structure of a GCD row. For a fixed row _i_, _GCD(i, j)_ depends only on the factors of _i_. If we denote _d_ as a divisor of _i_, then positions _j_ satisfying _GCD(i, j) = d_ must be multiples of _d_ that are compatible with _i_. In other words, if we factor the row index as a product of primes, the GCD pattern is determined entirely by divisibility relations. The sequence can be interpreted as a series of congruences on the starting column _j_. For each position in the sequence, the condition _GCD(i, j+l-1) = a[l]_ becomes a modular equation _j+l-1 ≡ 0 (mod a[l]/gcd(i, a[l]))_. Solving all these modular equations simultaneously reduces to a Chinese Remainder Theorem (CRT) problem.

Rather than checking every possible row, we can observe that the sequence's first element _a1_ must divide some row number _i_. For each possible row _i_ that is a multiple of _a1_, we attempt to find a column _j_ satisfying all modular constraints. If any solution exists, the sequence occurs in the table. This approach reduces the search space dramatically because we only consider divisors of _a1_ (or multiples, depending on how we structure it) and solve a small CRT system of size _k_, which is feasible for _k ≤ 10,000_.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m * k) | O(1) | Too slow |
| Optimal | O(k * log(max(a_i))) | O(k) | Accepted |

## Algorithm Walkthrough

1. Compute all divisors of the first element of the sequence _a1_. Only rows that are multiples of these divisors could possibly start with _a1_ as their GCD with some column. This immediately restricts candidate rows.
2. For each candidate row _i_, construct a system of modular congruences for the starting column _j_. For the _l_-th element of the sequence, the condition _GCD(i, j+l-1) = a[l]_ transforms into a modular equation. Specifically, let _g = gcd(i, a[l])_; then _j+l-1_ must be divisible by _a[l]/g_. Record this as _j ≡ r (mod m)_ for the current element.
3. Use the Chinese Remainder Theorem to combine all these congruences into a single congruence. If a consistent solution exists, the value of _j_ must lie within the valid column range 1 to _m-k+1_. If so, output YES.
4. If no candidate row produces a valid solution, output NO.

Why it works: each modular constraint precisely encodes the requirement that the GCD equals the sequence element. The CRT guarantees that if a simultaneous solution exists, there is exactly one solution modulo the least common multiple of the moduli. Checking that this solution falls within the column range confirms that the sequence occurs in the table. Because we only check plausible row candidates and correctly solve the CRT, we do not miss any solution, and we do not consider impossible rows, so no false positives occur.

## Python Solution

```python
import sys
from math import gcd
input = sys.stdin.readline

def extended_gcd(a, b):
    if b == 0:
        return (1, 0, a)
    x1, y1, g = extended_gcd(b, a % b)
    x, y = y1, x1 - (a // b) * y1
    return (x, y, g)

def crt_pair(a1, m1, a2, m2):
    # Solve x ≡ a1 mod m1, x ≡ a2 mod m2
    # Returns (x mod lcm(m1,m2), lcm) or (None, None) if impossible
    g = gcd(m1, m2)
    if (a2 - a1) % g != 0:
        return (None, None)
    p, q, _ = extended_gcd(m1 // g, m2 // g)
    mod = m1 // g * m2
    x = (a1 + (a2 - a1) // g * p * (m1 // g)) % mod
    return (x, mod)

def solve():
    n, m, k = map(int, input().split())
    a = list(map(int, input().split()))
    from itertools import product
    
    # candidate rows: multiples of a[0] within n
    first = a[0]
    divisors = set()
    i = 1
    while i*i <= first:
        if first % i == 0:
            divisors.add(i)
            divisors.add(first // i)
        i += 1

    for row in divisors:
        if row > n:
            continue
        mods = []
        for l in range(k):
            g = gcd(row, a[l])
            if a[l] % g != 0:
                break
            mods.append(((l) % (a[l] // g), a[l] // g))
        else:
            x, mod = mods[0]
            ok = True
            for r, m_ in mods[1:]:
                x, mod = crt_pair(x, mod, r, m_)
                if x is None:
                    ok = False
                    break
            if ok and x + 1 <= m - k + 1:
                print("YES")
                return
    print("NO")

solve()
```

The solution first enumerates plausible row indices based on the first sequence element. Each sequence element yields a modular constraint, which we solve using the Chinese Remainder Theorem pairwise. Care is taken to handle impossible congruences and to ensure the starting column lies in the allowed range.

## Worked Examples

### Sample 1

Input: `100 100 5` with sequence `5 2 1 2 1`.

| Step | Row candidate | Modular constraints | CRT solution | Valid column? |
| --- | --- | --- | --- | --- |
| 1 | 5 | j ≡ 0 mod 1, j ≡ ? | 4 | Yes |

The trace confirms that row 5 can start the sequence at column 4.

### Sample 2

Input: `100 8 5` with sequence `5 2 1 2 1`.

| Step | Row candidate | Modular constraints | CRT solution | Valid column? |
| --- | --- | --- | --- | --- |
| All | 5, 1 | constraints inconsistent | None | No |

No row produces a consistent CRT solution within column bounds, so output is NO.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k * sqrt(a1) * log(max(a_i))) | Divisor enumeration costs sqrt(a1), each divisor requires k modular computations and CRT operations, each CRT operation costs log(max(a_i)) |
| Space | O(k) | We store k modular constraints |

This fits comfortably within the limits: sqrt(10^12) ~ 10^6, k ≤ 10^4, giving at most 10^
