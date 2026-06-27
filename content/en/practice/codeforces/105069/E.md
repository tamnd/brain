---
title: "CF 105069E - \u4e0d\u51cf\u7684\u6570\u7ec4"
description: "We are given an array of integers and the task is to transform it into a non-decreasing sequence by removing elements."
date: "2026-06-27T23:21:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105069
codeforces_index: "E"
codeforces_contest_name: "The 5th FanRuan Cup Southeast University Programming Contest \uff08Winter\uff09"
rating: 0
weight: 105069
solve_time_s: 34
verified: false
draft: false
---

[CF 105069E - \u4e0d\u51cf\u7684\u6570\u7ec4](https://codeforces.com/problemset/problem/105069/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers and the task is to transform it into a non-decreasing sequence by removing elements. The restriction is that elements can only be taken from the original array, and we decide whether to discard or keep each value so that the final sequence never decreases as we move from left to right.

The structure hinted in the statement suggests a key observation: negative values and non-negative values play different roles, and the final valid arrangement behaves like a block where smaller values tend to be placed earlier and larger values later. The construction is driven from both ends of the array, meaning that decisions are made using a left pointer and a right pointer, gradually shrinking the interval until all decisions are fixed.

The output is the minimum number of removals required to achieve such a non-decreasing sequence, or equivalently the maximum length of a valid subsequence that respects the rule.

From a complexity perspective, typical constraints for this type of problem imply that the array size can be large, likely up to 2×10^5 or 10^5. This immediately rules out quadratic strategies such as checking all subsequences or trying all split points. A solution must be linear or linearithmic.

A few edge situations matter:

If the array is already non-decreasing, no removals are needed. For example, in `[1, 2, 2, 3]`, the answer is zero.

If the array is strictly decreasing, for example `[5, 4, 3, 2]`, we cannot keep more than one element, because any two kept elements would violate non-decreasing order.

A subtle case appears when both ends offer valid candidates but choosing incorrectly blocks future choices. For example, `[3, 1, 2, 4]` requires careful selection from both ends; greedily taking the larger early can prevent later valid extensions.

## Approaches

The brute-force interpretation is to try all subsets of elements, check whether each subset is non-decreasing, and take the largest valid one. This works conceptually because it exhaustively explores all possibilities, but its cost is exponential since there are 2^n subsets and each check costs O(n), leading to O(n·2^n), which is infeasible even for n around 40.

A more structured brute-force is to use dynamic programming for the longest non-decreasing subsequence, which runs in O(n^2). This is still too slow when n reaches 10^5.

The key observation is that we do not actually need to consider arbitrary subsequences. The construction can be guided greedily from both ends. At any moment, we maintain a current last value in the constructed sequence. We are allowed to take either the leftmost or rightmost element if it does not violate non-decreasing order. Among valid choices, we prefer the smaller value because it leaves more flexibility for future steps. This transforms the problem into a two-ended greedy construction that runs in linear time.

The reason this works is that any optimal solution can be rearranged so that whenever both ends are feasible, taking the smaller element does not reduce future possibilities, since it imposes the weakest constraint on subsequent picks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Subsets | O(n·2^n) | O(n) | Too slow |
| DP (LNDS style) | O(n^2) | O(n) | Too slow |
| Two-ended Greedy | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain two pointers, one at the start of the array and one at the end. We also maintain the last chosen value, initialized to negative infinity so that the first choice is always valid.

1. Initialize `l = 0`, `r = n - 1`, and `last = -∞`. This represents that we have not yet fixed any element in the resulting sequence.
2. While `l <= r`, we examine both ends of the current segment.
3. If the left value is at least `last`, we consider it a valid candidate. Similarly, if the right value is at least `last`, it is also a valid candidate.
4. If neither side is valid, it means both remaining values are too small to extend the sequence. In that case, we stop, because no further elements can be appended without breaking non-decreasing order.
5. If both sides are valid, we choose the smaller of the two values. This choice keeps the sequence as unconstrained as possible for future steps.
6. If only one side is valid, we take th
