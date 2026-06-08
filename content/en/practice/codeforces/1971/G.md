---
title: "CF 1971G - XOUR"
description: "We are given an array of nonnegative integers and a special swap condition: two elements can be swapped if the bitwise XOR of their values is less than 4. The goal is to produce the lexicographically smallest array possible by performing any number of such swaps."
date: "2026-06-08T17:22:23+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dsu", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1971
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 944 (Div. 4)"
rating: 1700
weight: 1971
solve_time_s: 67
verified: false
draft: false
---

[CF 1971G - XOUR](https://codeforces.com/problemset/problem/1971/G)

**Rating:** 1700  
**Tags:** data structures, dsu, sortings  
**Solve time:** 1m 7s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of nonnegative integers and a special swap condition: two elements can be swapped if the bitwise XOR of their values is less than 4. The goal is to produce the lexicographically smallest array possible by performing any number of such swaps.

The input consists of multiple test cases, each with a length `n` and the array elements. The output is the transformed array for each test case.

The constraints imply that `n` can be up to 2×10^5 across all test cases. This means we cannot attempt brute-force checking of all swap sequences. We must rely on an approach that quickly identifies which elements can be reordered among themselves. Non-obvious edge cases arise when the array contains large numbers whose XORs are ≥4. For instance, an array like `[16, 4, 1, 64]` cannot be changed because all XORs are too large, so the output is the array itself.

## Approaches

The brute-force approach would be to repeatedly scan the array and swap any two elements whose XOR is less than 4 until no more swaps are possible. This guarantees correctness but is extremely slow, because in the worst case it could require O(n^2) swaps per iteration and many iterations.

The optimal approach observes that the swap condition defines **connected components**: elements whose pairwise XORs are less than 4 form a group within which any permutation is possible. All swaps outside a component are forbidden. Therefore, we only need to:

1. Identify all connected components of elements under the XOR<4 relation.
2. Sort each component independently.
3. Place the sorted values back into their original positions.

This ensures the array becomes lexicographically smallest because each group is sorted internally, and elements that cannot be swapped with each other remain in place relative to the other groups.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow |
| Connected Components + Sort | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n` and the array `a`.
3. Initialize a Disjoint Set Union (DSU) structure for `n` elements. This will track which indices can be swapped with each other.
4. For every pair of indices `(i, j)`, if `a[i] XOR a[j] < 4`, merge their
