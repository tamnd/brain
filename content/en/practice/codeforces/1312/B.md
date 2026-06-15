---
title: "CF 1312B - Bogosort"
description: "We are given an array of integers and are allowed to permute it arbitrarily. After rearranging, we assign each value to a position starting from 1. The array is considered valid if no two positions share the same value of the expression i - a[i]."
date: "2026-06-16T06:49:16+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1312
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 83 (Rated for Div. 2)"
rating: 1000
weight: 1312
solve_time_s: 287
verified: false
draft: false
---

[CF 1312B - Bogosort](https://codeforces.com/problemset/problem/1312/B)

**Rating:** 1000  
**Tags:** constructive algorithms, sortings  
**Solve time:** 4m 47s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers and are allowed to permute it arbitrarily. After rearranging, we assign each value to a position starting from 1. The array is considered valid if no two positions share the same value of the expression `i - a[i]`. In other words, if we look at each element as defining a “diagonal index” computed from its position minus its value, all these diagonal indices must be distinct.

The task is to decide how to reorder the array so that this uniqueness condition holds. The problem guarantees that at least one valid ordering always exists.

The constraints are small: at most 100 test cases, each array has length at most 100, and values are also bounded by 100. This immediately tells us that any solution with quadratic behavior per test case is easily fast enough. Even a cubic approach would still be fine in the worst case, but anything involving exponential search or backtracking over permutations would be unnecessary.

A subtle point is that the condition depends on both index and value. A naive interpretation might suggest that equal values are problematic, but that is not the case. Two identical values are fine as long as they are placed in positions that produce different `i - a[i]` values.

A failure case for naive thinking would be leaving the array unchanged. For example, if we take `[1, 1, 3, 5]` as given, the original ordering might violate the condition because duplicates can align in a way that produces repeated `i - a[i]`. Another misleading case is assuming sorting always works. Sorting `[3, 2, 1]` gives `[1, 2, 3]`, but this does not guarantee distinct `i - a[i]` values in general, so a different construction is required.

## Approaches

The key observation is that we do not need to reason about values interacting with each other directly. The condition only constrains the differences between index and value. If we want all `i - a[i]` to be distinct, we can control it by carefully separating large values from small values.

A brute-force approach would try all permutations of the array and check the condition for each one. This is correct because it exhaustively searches all valid reorderings. However, the number of permutations grows as `n!`, which for `n = 100` is astronomically large. Even for `n = 10`, it becomes borderline in practice, so this approach is completely infeasible.

The structural insight is that we can avoid collisions by ensuring that larger values are placed in earlier positions and smaller values are placed later. If we sort the array in decreasing order, then assign it in that order, the expression `i - a[i]` tends to decrease as well, but more importantly, no two elements can produce the same difference because equal values are separated and their indices are strictly increasing.

The deeper reason this works is that if values are sorted descending, then differences between adjacent elements in the constructed sequence cannot collapse into equality unless both index and value shifts align perfectly, which cannot happen across a strictly ordered arrangement of values under arbitrary duplicates.

This reduces the problem from searching permutations to a single sorting step.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Sort Descending | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the array for the current test case. The goal is to construct any permutation that avoids repeated values of `i - a[i]`.
2. Sort the array in descending order. This ensures that larger values are assigned earlier positions in the final arrangement, which spreads out the computed differences.
3. Output the sorted array as the final arrangement. No further transformation is needed because the sorted order already satisfies the condition.

### Why it works

Once the array is sorted in non-increasing order, elements are arranged so that larger values appear at smaller indices. If two positions `i < j` had the same value of `i - a[i] = j - a[j]`, then rearranging gives `a[i] - a[j] = i - j`. Since `i - j` is negative, this would require `a[i] < a[j]`, contradicting the fact that the array is non-increasing. Therefore no equality can occur, and all values of `i - a[i]` must be distinct.

## Python Solution

```
PythonRun
```

The implementation is direct. Each test case is processed independently. Sorting in reverse order is the only transformation applied. The output is printed immediately.

A common mistake would be forgetting that the sort must be descending rather than ascending. Ascending order can create collisions in the `i - a[i]` expression when small values accumulate early in the array.

## Worked Examples

### Example 1

Input array: `[1, 1, 3, 5]`

Sorted descending: `[5, 3, 1, 1]`

| i | a[i] | i - a[i] |
| --- | --- | --- |
| 1 | 5 | -4 |
| 2 | 3 | -1 |
| 3 | 1 | 2 |
| 4 | 1 | 3 |

All values are distinct, so the arrangement is valid.

This trace shows how duplicates do not interfere because they are placed at different indices producing different differences.

### Example 2

Input array: `[3, 2, 1, 5, 6, 4]`

Sorted descending: `[6, 5, 4, 3, 2, 1]`

| i | a[i] | i - a[i] |
| --- | --- | --- |
| 1 | 6 | -5 |
| 2 | 5 | -3 |
| 3 | 4 | -1 |
| 4 | 3 | 1 |
| 5 | 2 | 3 |
| 6 | 1 | 5 |

Again, all values are distinct. The structure of strictly decreasing values ensures a strictly increasing sequence of differences.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates each test case |
| Space | O(n) | Storage for the array |

The constraints allow up to 100 elements per test case, so sorting is effectively instantaneous. Even with 100 test cases, the total work is negligible.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | itself | base case correctness |
| all equal | unchanged multiset | duplicates safe handling |
| ascending input | fully reversed | sorting effect |
| mixed duplicates | stable multiset ordering | general case robustness |

## Edge Cases

When all elements are identical, any permutation produces identical values of `i - a[i]` only if indices coincide, which they do not, so the condition remains valid. Sorting keeps the array unchanged, and the result is trivially correct.

When the array is already increasing, reversing it produces a strictly decreasing sequence, which maximizes separation between values and prevents any equality of `i - a[i]`.

When duplicates exist in nontrivial positions, the construction ensures they are spread across different indices. Even though values repeat, indices differ enough that the computed differences cannot match across two positions in a way that violates ordering.
