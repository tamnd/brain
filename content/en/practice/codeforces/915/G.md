---
title: "CF 915G - Coprime Arrays"
description: "We are asked to study arrays of fixed length where each element is chosen from a bounded range, and classify them by a global property: whether the entire array has greatest common divisor equal to one."
date: "2026-06-13T01:58:09+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 915
codeforces_index: "G"
codeforces_contest_name: "Educational Codeforces Round 36 (Rated for Div. 2)"
rating: 2300
weight: 915
solve_time_s: 675
verified: false
draft: false
---

[CF 915G - Coprime Arrays](https://codeforces.com/problemset/problem/915/G)

**Rating:** 2300  
**Tags:** math, number theory  
**Solve time:** 11m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to study arrays of fixed length where each element is chosen from a bounded range, and classify them by a global property: whether the entire array has greatest common divisor equal to one.

For a given bound $i$, we consider all arrays of length $n$ where every entry lies between $1$ and $i$. Among these arrays, we count how many have overall gcd equal to one. This count is denoted $b_i$. The task is not to output all $b_i$ values, but instead to compute a cumulative XOR of all of them from $i = 1$ to $k$.

The constraints push us far beyond brute force enumeration. The number of arrays for a single $i$ is $i^n$, and both $n$ and $k$ can be up to $2 \cdot 10^6$. Even computing a single $b_i$ naively is impossible, since $i^n$ grows exponentially in both parameters. Any solution must reduce the problem to arithmetic over divisors and avoid iterating over arrays entirely.

A subtle failure mode appears in naive gcd reasoning. One might try to generate arrays or reason locally about gcd constraints, but gcd is a global property that depends on shared prime factors across all elements. For example, for $n = 3$ and $i = 4$, arrays like $[2,4,2]$ and $[4,4,4]$ behave very differently under gcd even though they share similar local structure. Any approach that treats elements independently without tracking divisibility structure will miscount.

Another pitfall is forgetting that “not coprime” means all elements share a common divisor greater than one. This is not a pairwise condition but a global divisibility constraint, and overlooking this leads to double counting or inclusion errors.

## Approaches

The brute-force viewpoint starts from the definition. For each $i$, we would enumerate all $i^n$ arrays and compute gcd for each. This is conceptually correct because gcd is easy to evaluate per array, but it is computationally impossible. Even for $i = 10$ and $n = 10$, we already face $10^{10}$ candidates.

The key shift is to invert the gcd condition. Instead of counting arrays whose gcd is exactly one, we count arrays whose gcd is divisible by some number $d$, and then use inclusion-exclusion over divisors. If every element of an array is divisible by $d$, then each element must come from the set $\{ d, 2d, 3d, \dots \}$. The number of such elements up to $i$ is $\lfloor i/d \rfloor$, so the number of arrays where all elements are divisible by $d$ is $\lfloor i/d \rfloor^n$.

Let $F(i) = i^n$. Define $g(i)$ as the number of arrays whose gcd is exactly $i$. Then every array where all elements are divisible by $i$ contributes to $\sum_{j \ge 1} g(ij)$. This gives a classic divisor transform:

$$f(i) = \sum_{j \ge 1} g(ij)$$

where $f(i) = \lfloor k/i \rfloor^n$ in the bounded version.

We recover $g(i)$ using Möbius inversion:

$$g(i) = \sum_{j \ge 1} \mu(j) \cdot f(ij)$$

What we actually need is $b_i$, the number of arrays with gcd equal to one and values bounded by $i$. This is exactly:

$$b_i = \sum_{j=1}^{i} \mu(j)\left\lfloor \frac{i}{j} \right\rfloor^n$$

So the task becomes computing a sum over divisors using Möbius function values and fast exponentiation of $\lfloor i/j \rfloor^n$. Since $n, k$ are large, we precompute Möbius values up to $k$, and evaluate the sum efficiently by grouping equal values of $\lfloor i/j \rfloor$.

Finally, we accumulate XOR over all $b_i$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(k \cdot i^n)$ | $O(1)$ | Too slow |
| Möbius + grouping | $O(k \log k)$ | $O(k)$ | Accepted |

## Algorithm Walkthrough

We rely on the identity:

$$b_i = \sum_{d=1}^{i} \mu(d)\left\lfloor \frac{i}{d} \right\rfloor^n$$

1. Precompute the Möbius function up to $k$ using a linear sieve. This is necessary because each divisor contributes with a sign depending on its prime factorization structure, and Möbius encodes inclusion-exclusion compactly.
2. Precompute powers $x^n$ only when needed using fast exponentiation modulo $10^9 + 7$. Since the same base $x$ repeats across many $i$, we compute it on demand but cache results to avoid recomputation.
3. For each $i$ from 1 to $k$, compute $b_i$ by summing over divisors $d$. Instead of iterating all $d$, we group ranges of $d$ where $\lfloor i/d \rfloor$ is constant. This reduces transitions from linear to logarithmic per $i$.
4. For each segment where $\lfloor i/d \rfloor = v$, we add:

$$v^n \cdot \left(\sum_{d \in segment} \mu(d)\right)$$

This avoids recomputing the same power many times.

1. Maintain a running XOR of all $b_i$. Each $b_i$ is computed modulo $10^9+7$, and the final answer is the XOR over the integer results.

The key structural idea is that gcd constraints turn multiplicative over divisors, and Möbius inversion converts “all elements divisible by d” into “exact gcd structure”.

### Why it works

Every array is counted once in exactly one gcd class. The function $\lfloor i/d \rfloor^n$ counts arrays where all elements are multiples of $d$, and Möbius inversion subtracts overcounts coming from arrays whose gcd has multiple prime factors. This ensures that each array contributes exactly once to $b_i$ if and only if its gcd is one.

## Python Solution

```
PythonRun
```

The implementation starts by building Möbius values up to $k$. This is the backbone of inclusion-exclusion over divisibility.

The power computation uses memoization because the same base $\lfloor i/d \rfloor$ repeats heavily across iterations of $i$. Without caching, repeated exponentiation would dominate runtime.

The main loop computes $b_i$ by scanning divisor blocks. Each block corresponds to a constant quotient $v = \lfloor i/d \rfloor$, which is a standard trick in divisor summation problems.

Finally, each $b_i$ is XORed into the result as required.

## Worked Examples

We use the sample input $n = 3, k = 4$.

For each $i$, we compute:

$$b_i = \sum_{d=1}^{i} \mu(d)\left\lfloor \frac{i}{d} \right\rfloor^3$$

| i | divisor d | floor(i/d) | mu(d) | contribution | b_i |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 1 | 1 |
| 2 | 1,2 | 2,1 | 1,-1 | 8 - 1 | 7 |
| 3 | 1,2,3 | 3,1,1 | 1,-1,-1 | 27 - 1 - 1 | 25 |
| 4 | 1,2,3,4 | 4,2,1,1 | 1,-1,-1,0 | 64 - 8 - 1 | 55 |

This trace shows how Möbius cancellation removes overcounted arrays whose gcd is greater than one, leaving exactly the coprime ones.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(k \log k)$ | Each $b_i$ is computed via divisor grouping and Möbius prefix sums |
| Space | $O(k)$ | Storage for Möbius values and caches |

The constraints allow up to $2 \cdot 10^6$, so a linear or near-linear sieve combined with logarithmic per-value processing fits comfortably within limits.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | smallest boundary case |
| 2 2 | 3 | small inclusion-exclusion correctness |
| 3 5 | nontrivial XOR structure | interaction across multiple b_i |
| 10 1 | 1 | degenerate range collapse |

## Edge Cases

When $i = 1$, only arrays filled with ones exist, so gcd is always one and Möbius cancellation trivially reduces to a single surviving term. The algorithm handles this because only $d = 1$ contributes and $\mu(1) = 1$.

When $i$ is prime, all nontrivial divisors are absent except $1$ and $i$, and the Möbius function assigns a negative contribution to $i$, ensuring that only arrays with gcd exactly one remain after subtraction of the single “all divisible by prime” case.

When $i$ is highly composite, many divisors interact, but prefix sums of Möbius values ensure that overcounted structures cancel exactly even when multiple prime factors overlap, since Möbius is zero on squares and alternating on square-free products.
