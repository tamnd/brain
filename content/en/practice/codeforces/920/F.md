---
title: "CF 920F - SUM and REPLACE"
description: "We are given an array of integers, and we need to support two operations over subarrays. One operation repeatedly transforms every value in a segment by replacing each number with its number of divisors. The other operation asks for the sum of values in a segment at that moment."
date: "2026-06-13T02:55:16+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "dsu", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 920
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 37 (Rated for Div. 2)"
rating: 2000
weight: 920
solve_time_s: 398
verified: false
draft: false
---

[CF 920F - SUM and REPLACE](https://codeforces.com/problemset/problem/920/F)

**Rating:** 2000  
**Tags:** brute force, data structures, dsu, number theory  
**Solve time:** 6m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers, and we need to support two operations over subarrays. One operation repeatedly transforms every value in a segment by replacing each number with its number of divisors. The other operation asks for the sum of values in a segment at that moment.

The key difficulty is that the array is not static. Each update changes values in a way that depends on their magnitude, and repeated updates keep shrinking numbers but not in a uniform or linear way. A value like 1 stays stable immediately, while larger numbers may take several transformations before stabilizing.

The constraints push us away from any solution that recomputes divisor counts directly for each update over large ranges. With up to 300,000 elements and 300,000 queries, even a single linear pass per query would already be too slow. A naive approach that recomputes divisors per element per update quickly becomes infeasible because divisor counting itself is not constant time unless preprocessed carefully.

A subtle edge case appears when values become small. For example, once a number becomes 1, further REPLACE operations do nothing. Similarly, values quickly collapse toward small integers like 2, 3, or 4, and after a few iterations the array stabilizes. A naive implementation that keeps reprocessing stabilized segments wastes large amounts of time repeatedly applying identity transformations.

Another failure mode arises if we treat REPLACE as fully recomputing every element in the range every time. Consider a segment of size 200,000 with values already small. Repeated updates over the same range will still scan the entire segment, even though only a few positions actually change after the first few operations.

## Approaches

A direct simulation is straightforward. For each REPLACE query, iterate over all indices in the range and replace each value with its divisor count, computed via a precomputed sieve or trial division. For each SUM query, also iterate over the range and accumulate values. This is correct but catastrophically slow.

The bottleneck is that each REPLACE over a large interval is O(n), and each divisor computation is O(1) if preprocessed or O(sqrt x) otherwise. With 300,000 queries, the worst case is on the order of 10^10 operations.

The key observation is that values shrink extremely quickly under repeated application of the divisor function. For any integer up to 10^6, repeatedly applying D(x) reaches 1 within
