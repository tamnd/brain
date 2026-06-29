---
title: "CF 104651G - GCD of Pattern Matching"
description: "We are given a base $m$ and a pattern string $P$ over lowercase letters. We interpret any positive integer as an $m$-ary number, written as a sequence of digits."
date: "2026-06-29T16:28:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104651
codeforces_index: "G"
codeforces_contest_name: "The 2023 CCPC Online Contest"
rating: 0
weight: 104651
solve_time_s: 34
verified: false
draft: false
---

[CF 104651G - GCD of Pattern Matching](https://codeforces.com/problemset/problem/104651/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a base $m$ and a pattern string $P$ over lowercase letters. We interpret any positive integer as an $m$-ary number, written as a sequence of digits. The constraint is that the digits of this number must match the pattern via a bijective relabeling between digit values and letters.

More concretely, each position in the base-$m$ representation of a number is labeled by a letter from $P$. We are allowed to assign distinct digits $0 \ldots m-1$ to letters, but the assignment must be injective: different letters must map to different digits. Once a letter is assigned a digit, every occurrence of that letter must use the same digit. Leading digit is also a digit, but must be non-zero because we consider positive integers with standard positional representation.

We consider all positive integers whose base-$m$ digit strings can be obtained by choosing a valid injective mapping from letters to digits. Among all such integers, we are asked to compute their greatest common divisor in decimal form.

The constraints are extremely large in number of test cases, up to 500,000, but each pattern is very short, length at most 16, and base is at most 16. This strongly suggests that each test case must be processed in constant or near-constant time after some fixed precomputation over small patterns.

A naive interpretation would try to enumerate all injective mappings from letters to digits and then generate all integers, but this immediately explodes. For $k$ distinct letters, there are $P(m,k)$ mappings, and each mapping gives exactly one integer. Even with $m \le 16$, this is already large, and multiplying by up to half a million test cases makes it impossible.

A more subtle issue is that even if we compute values, their magnitudes grow like $m^{|P|}$, which can still be large, but the real obstacle is the combinatorial explosion of valid assignments.

A key structural issue is that different permutations of digit assignments can produce different numbers, but their gcd may collapse to a much smaller value. So we are not asked to enumerate values, but to extract a shared arithmetic invariant.

Edge cases worth noting include patterns with repeated letters, patterns with all distinct letters, and patterns where the leading character appears multiple times. For example, if $P = "aaaa"$, then only one digit is used and every valid number is a repdigit in base $m$, producing a simple geometric series structure. If all characters are distinct, we are permuting digits freely, and the gcd becomes governed by symmetry over all permutations.

## Approaches

A brute-force idea is straightforward. For each test case, enumerate all injective mappings from distinct letters in $P$ to digits $0 \ldots m-1$, enforce that the first position is not mapped to zero, construct the corresponding integer value in base $m$, and compute the gcd over all constructed values.

This is correct but expensive. If there are $k$ distinct letters, the number of injections is $m \cdot (m-1) \cdots (m-k+1)$, which in the worst case is $16!$-scale, about $2 \times 10^{13}$ possibilities per test case in the extreme. Even if pruning is applied, repeated over 500,000 tests, it is infeasible.

The key observation is that we never need the actual numbers, only their greatest common divisor. This means we want the largest integer dividing all constructed values. That suggests focusing on what properties are invariant across all valid injective assignments.

Each valid number can be written as a polynomial in $m$, where coefficients are digits assigned to letters. If we replace letters by variables, each assignment evaluates the same linear combination of digits. The gcd over all injective assignments becomes the gcd over all evaluations of this linear form under all permutations of digits.

This turns into a classical symmetry problem: instead of enumerating assignments, we study the structure induced by permutations of digits over positions grouped by letter identity.

The crucial reduction is that what matters is how many times each digit appears weighted by positional powers. The gcd collapses to a function of two quantities: the sum of positional weights per letter and modular structure of permutations of digits. In fact, the final gcd depends only on the sum of digit positions and whether the pattern enforces uniqueness or repetition constraints, reducing the problem to computing a single number derived from positional weights and combinatorial symmetry of assignments.

This allows each test case to be reduced to counting positional contributions per letter and combining them using a fixed arithmetic rule derived from permutation invariance, avoiding any enumeration.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | exponential in number of distinct letters | O(1) | Too slow |
| Optimal | O( | P | ) per test case |

## Algorithm Walkthrough

We interpret the pattern as assigning digits to letters, then summing contributions of each letter weighted by positional powers of $m$.

1. For each test case, compute positional weights $w_i = m^i$ for each position in the pattern. This encodes the contribution of a digit placed at position $i$.
2. For each distinct letter, compute its total weight $W(c)$, which is the sum of $m^i$ over all positions where that letter appears. This reduces the pattern into a linear combination of letter variables.
3. Identify whether the leading character is forced to be non-zero. This restriction affects which digit permutations are valid and determines whether full symmetry over digits applies or whether we lose one degree of freedom in assignments.
4. Observe that all valid integers are obtained by assigning distinct digits to letters, so every integer is a sum of the
