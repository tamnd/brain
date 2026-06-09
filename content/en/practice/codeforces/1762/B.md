---
title: "CF 1762B - Make Array Good"
description: "We are asked to transform an array of positive integers into one that is \"good\" according to a divisibility property: for every pair of elements, the larger must be divisible by the smaller."
date: "2026-06-09T13:47:39+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation", "number-theory", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1762
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 838 (Div. 2)"
rating: 1100
weight: 1762
solve_time_s: 184
verified: false
draft: false
---

[CF 1762B - Make Array Good](https://codeforces.com/problemset/problem/1762/B)

**Rating:** 1100  
**Tags:** constructive algorithms, implementation, number theory, sortings  
**Solve time:** 3m 4s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to transform an array of positive integers into one that is "good" according to a divisibility property: for every pair of elements, the larger must be divisible by the smaller. The operations allowed are additive, and we can increase any element by any amount up to its current value. The output is a sequence of operations that guarantees the resulting array is good, and we are not required to minimize the number of operations.

The problem’s input constraints are large: $n$ can reach $10^5$ per test case, and the sum of $n$ across all test cases is also bounded by $10^5$. This indicates that our algorithm must be essentially linear in $n$. Nested loops or exhaustive checking for divisibility between every pair would immediately be too slow. Furthermore, since each element can be increased to very large numbers (up to $10^{18}$), we can rely on constructive approaches rather than worrying about hitting a ceiling.

Edge cases include arrays that are already good, arrays where all elements are the same, and arrays where the elements are pairwise coprime. For example, if $a = [2,3,5]$, a naive approach might fail to constructively add numbers so that all divisibility conditions hold simultaneously. The correct output in such cases typically requires increasing elements selectively to match a least common multiple or a shared base.

## Approaches

A brute-force approach would attempt to test each possible increment on each element and check the resulting array for the good property. This is conceptually correct because we could, in principle, find a sequence of operations that works. However, the number of possible sequences is enormous, and iterating through all pairs of elements repeatedly would give $O(n^2)$ complexity, which is too slow given $n \sim 10^5$.

The optimal approach relies on observing that a "good" array is guaranteed if every element is a multiple of the minimum element. Thus, we can fix the smallest element as a reference and adjust all others to be multiples of it. Since the operation allows us to increase elements arbitrarily, it is sufficient to make each element equal to its current value rounded up to the nearest multiple of the minimum. This approach guarantees that every pair satisfies the divisibility property. No element needs to decrease, and every adjustment can be computed in constant time per element.

The construction is simple and linear: we find the minimum, then iterate through all elements, computing the additive increment needed to reach a multiple of the minimum. This produces a solution in at most $n$ operations per test case.

| Approach | Time Complexity | Space Complexity | Verdict
