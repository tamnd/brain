---
title: "CF 105669I - Partition"
description: "We are given a single integer ( n ). The task is to count how many different ways we can express ( n ) as a sum of positive integers, where order matters."
date: "2026-06-26T09:56:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105669
codeforces_index: "I"
codeforces_contest_name: "Combinatorics Contest - Brazilian ICPC Summer School 2025"
rating: 0
weight: 105669
solve_time_s: 37
verified: true
draft: false
---

[CF 105669I - Partition](https://codeforces.com/problemset/problem/105669/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single integer \( n \). The task is to count how many different ways we can express \( n \) as a sum of positive integers, where order matters. For example, writing \( 3 \) as \( 1+2 \) is considered different from \( 2+1 \), and even the single term \( 3 \) itself is also a valid representation. Every sequence of positive integers whose sum is exactly \( n \) contributes one way.

This is the classic problem of counting ordered integer compositions of \( n \). The answer grows quickly, and the final result must be reported modulo \( 10^9+7 \).

The constraint \( n \le 10^6 \) is the key signal here. Any approach that enumerates partitions or builds all compositions explicitly is impossible because even for moderate \( n \), the number of compositions is exponential in \( n \). The structure of the problem must therefore be reduced to a simple recurrence or closed-form identity computable in linear time.

A subtle edge case appears at \( n = 1 \). There is exactly one composition: \([1]\). A naive interpretation that disallows using the number itself would incorrectly output zero. Another common mistake is to confuse ordered compositions with unordered partitions; for instance, for \( n=3 \), the correct answer is \(4\), not \(3\), because order is counted.

## Approaches

A brute-force solution would try to generate every possible sequence of positive integers summing to \( n \). From a recursion standpoint, at each step we choose the next summand \( k \ge 1 \) and recurse on \( n-k \). This creates a branching factor of up to \( n \) at the top level, then \( n-1 \), and so on. The total number of recursive states expands roughly like the number of compositions itself, which is \( 2^{n-1} \). For \( n = 10^6 \), this is completely infeasible.

The key observation is that the problem does not depend on the actual values chosen, only on the remaining sum. Let \( f(n) \) be the number of valid compositions of \( n \). Any composition of \( n \) either starts with \( 1 \), or \( 2 \), or \( 3 \), and so on up to \( n \). This gives the recurrence
\[
f(n) = f(n-1) + f(n-2) + \dots + f(0),
\]
with the convention \( f(0) = 1 \), representing the empty decomposition.

A direct computation of this recurrence is still \( O(n^2) \) if implemented naively, but it can be simplified by noticing a telescoping relationship. Subtracting the recurrence for \( f(n-1) \) from that of \( f(n) \) yields
\[
f(n) - f(n-1) = f(n-1),
\]
which simplifies to
\[
f(n) = 2 \cdot f(n-1).
\]

This collapses the entire structure into a simple doubling process: each integer composition of \( n-1 \) can either remain unchanged with a leading \( 1 \), or be extended in a way that preserves bijection with compositions of \( n \). This establishes a one-to-one correspondence that doubles the count at every step.

We therefore get the closed form:
\[
f(n) = 2^{n-1}.
\]

This can be computed in linear time via a simple recurrence or in logarithmic time via modular exponentiation.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force Enumeration | \( O(2^n) \) | \( O(n) \) | Too slow |
| Prefix-sum DP over states | \( O(n^2) \) | \( O(n) \) | Too slow |
| Closed-form \( 2^{n-1} \) | \( O(\log n) \) | \( O(1) \) | Accepted |

## Algorithm Walkthrough

1. We recognize that every valid construction of \( n \) corresponds to a sequence of cuts between integers \( 1 \) through \( n \). Between each adjacent pair of positions, we either place a cut or we do not, which determines whether numbers are grouped or separated. This converts the problem into a binary decision process over \( n-1 \) gaps.

2. Since each of the \( n-1 \) positions independently has two choices, the total number of configurations is \( 2^{n-1} \). This is the central combinatorial transformation that avoids recursion entirely.

3. We compute \( 2^{n-1} \bmod (10^9+7) \) using fast exponentiation. The exponent is large, so we repeatedly square the base and reduce the exponent by half at each step.

4. The final value is returned as the answer.

### Why it works

The invariant is that every composition of \( n \) corresponds uniquely to a subset of the \( n-1 \) possible separators between consecutive integers. Choosing a subset determines exactly where a segment ends, and thus uniquely determines a valid ordered partition. No two different subsets produce the same composition, and every composition corresponds to exactly one subset. This bijection guarantees correctness of the \( 2^{n-1} \) count.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

n = int(input().strip())

# number of compositions of n is 2^(n-1)
if n == 0:
    print(1)
else:
    print(pow(2, n - 1, MOD))
```

The implementation directly applies modular exponentiation. The special case \( n = 0 \) is included for completeness, though the problem guarantees \( n \ge 1 \).

The key simplification is avoiding any DP table or recursion. The entire structure of the problem reduces to counting independent binary choices across the gaps between integers.

## Worked Examples

### Example 1: n = 3

We track how compositions arise from the binary gap interpretation.

| Gap decisions (between 1 and 2, 2 and 3) | Resulting composition |
|---|---|
| cut, cut | 1 + 1 + 1 |
| cut, no cut | 1 + 2 |
| no cut, cut | 2 + 1 |
| no cut, no cut | 3 |

This produces 4 valid compositions, matching \( 2^{2} = 4 \).

This trace confirms that every subset of gaps corresponds to exactly one valid decomposition.

### Example 2: n = 4

| Gap decisions | Composition |
|---|---|
| 1,1,1 | 1+1+1+1 |
| 1,1,0 | 1+1+2 |
| 1,0,1 | 1+2+1 |
| 1,0,0 | 1+3 |
| 0,1,1 | 2+1+1 |
| 0,1,0 | 2+2 |
| 0,0,1 | 3+1 |
| 0,0,0 | 4 |

There are 8 outcomes, matching \( 2^{3} = 8 \). The structure of independent gap decisions is fully exposed here.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | \( O(\log n) \) | fast exponentiation computes \( 2^{n-1} \) in logarithmic steps |
| Space | \( O(1) \) | only a few integers are maintained |

The constraint \( n \le 10^6 \) is easily handled because exponentiation under modulus is extremely fast even for large exponents. The solution runs well within both time and memory limits.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(sys.stdin.readline().strip())
    if n == 0:
        return "1"
    return str(pow(2, n - 1, MOD))

# provided samples
assert run("1") == "1"
assert run("3") == "4"

# custom cases
assert run("2") == "2", "1+1, 2"
assert run("4") == "8", "check small correctness"
assert run("10") == str(pow(2, 9, MOD)), "power correctness"
assert run("1000000") == str(pow(2, 999999, MOD)), "large stress case"
```

| Test input | Expected output | What it validates |
|---|---|---|
| 1 | 1 | minimal boundary |
| 2 | 2 | smallest non-trivial composition |
| 4 | 8 | exponential growth consistency |
| 1000000 | 2^999999 mod | performance and large exponent |

## Edge Cases

### n = 1

For input `1`, the algorithm computes \( 2^{0} = 1 \). The only composition is the single element `[1]`, so the result is correct. The gap interpretation has zero gaps, meaning exactly one configuration exists.

### Very large n (up to 10^6)

For `n = 1000000`, the exponentiation step runs in \( O(\log n) \). The computation repeatedly squares the base 2 and reduces the exponent, never storing large intermediate values beyond the modulus. This ensures the algorithm remains stable and fast even at maximum input size.
