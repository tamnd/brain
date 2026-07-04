---
title: "CF 102961Z - Nearest Smaller Values"
description: "We are given a sequence of numbers, and for every position we want to find a “nearest smaller value” that appears before it."
date: "2026-07-04T06:58:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102961
codeforces_index: "Z"
codeforces_contest_name: "CSES Problem Set: Sorting and Searching"
rating: 0
weight: 102961
solve_time_s: 29
verified: false
draft: false
---

[CF 102961Z - Nearest Smaller Values](https://codeforces.com/problemset/problem/102961/Z)

**Rating:** -  
**Tags:** -  
**Solve time:** 29s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of numbers, and for every position we want to find a “nearest smaller value” that appears before it. In other words, when standing at an element, we look to the left and try to locate the closest earlier element that is strictly smaller than the current one. If no such element exists, the answer for that position is zero.

The output is therefore a sequence of the same length, where each entry encodes the position (or value, depending on indexing convention) of the closest smaller element to the left, or zero when the left side contains nothing smaller.

The constraints typical for this kind of task imply a large array size, often up to one hundred thousand elements. That immediately rules out quadratic scanning strategies. A nested loop that, for each position, walks backward over all previous elements would perform on the order of n² comparisons in the worst case, which is far beyond what fits in time limits around two seconds. The only viable solutions are those that maintain incremental structure as we traverse the array once.

A naive implementation also tends to fail subtly when all previous elements are larger than the current one. In that case, it might incorrectly return the nearest previous element instead of correctly recognizing that no valid smaller element exists. For example, in the input `[5, 4, 3]`, the correct output is `[0, 0, 0]`. Any approach that only tracks proximity without enforcing the “smaller than current” condition will incorrectly produce `[0, 1, 2]` or similar positional fallbacks.

Another common edge case appears in strictly increasing sequences such as `[1, 2, 3, 4]`. Every element except the first has a valid nearest smaller, and that smaller element is always immediately adjacent. A correct solution must preserve this locality without rescanning the entire prefix.

## Approaches

The brute-force strategy is straightforward. For each index i, we scan backward from i − 1 down to 0 and stop at the first element that is smaller than the current value. This is correct because it explicitly checks all candidates in order of proximity and guarantees the first valid match is indeed the nearest.

The problem with this approach is that it repeatedly re-examines the same elements. In the worst case of a decreasing array, every element scans all previous elements. This leads to roughly n(n − 1)/2 comparisons, which is quadratic behavior and becomes too slow for large inputs.

The key observation is that not all previous elements remain useful once we move forward. If we maintain a structure of candidates for which we have not yet found a “next greater or equal element,” then many elements can be discarded permanently. Specifically, once we see a new element, any previous element that is greater than or equal to it can never be the nearest smaller for any future element to its right. This suggests maintaining a structure that keeps only a decreasing sequence of candidates.

A monotonic stack naturally captures this idea. We keep indices of elements in a stack such that their values are strictly increasing from bottom to top. When a new element arrives, we remove all elements from the stack that are not smaller than it, since they are useless for future comparisons. After cleanup, the top of the stack (if it exists) is the nearest smaller element.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Monotonic Stack | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We process the array from left to right while maintaining a stack of candidate indices.

1. Initialize an empty stack. Each element in the stack represents an index whose value might be the nearest smaller element for future positions.
2. Iterate through the array
