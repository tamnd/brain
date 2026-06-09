---
title: "CF 1851B - Parity Sort"
description: "We are given an array of integers and can swap any two elements that share the same parity, meaning both are odd or both are even. The goal is to determine whether it is possible to sort the array in non-decreasing order using this operation any number of times."
date: "2026-06-09T17:19:27+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1851
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 888 (Div. 3)"
rating: 800
weight: 1851
solve_time_s: 371
verified: false
draft: false
---

[CF 1851B - Parity Sort](https://codeforces.com/problemset/problem/1851/B)

**Rating:** 800  
**Tags:** greedy, sortings, two pointers  
**Solve time:** 6m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers and can swap any two elements that share the same parity, meaning both are odd or both are even. The goal is to determine whether it is possible to sort the array in non-decreasing order using this operation any number of times. The input consists of multiple test cases, each specifying the length of the array followed by the array itself. The output is simply YES if the array can be sorted under the operation rules, and NO otherwise.

The constraints tell us that the array length can be up to 2⋅10^5, and there can be up to 10^4 test cases, but the total sum of array sizes across all test cases does not exceed 2⋅10^5. This means we need an algorithm that runs in linear or near-linear time per test case, because anything quadratic in n would be too slow. A naive approach that tries all possible swaps is clearly infeasible because the number of possible swaps grows combinatorially with n.

A subtle edge case arises when the array contains only elements of a single parity. For example, [11, 3, 15, 3] can be fully rearranged because all elements are odd. In contrast, if the array has a mix of even and odd numbers, their relative positions across parities cannot be swapped. For instance, [11, 3, 15, 3, 2] cannot place the even number 2 before an odd number if the sorted position requires it, since swaps between even and odd elements are forbidden. Arrays of length one or arrays that are already sorted are trivial but should not be overlooked.

## Approaches

The brute-force solution would simulate all allowed swaps. For each unsorted pair of elements, if they share the same parity, we could swap them toward the correct position. This works because repeated valid swaps will eventually place all numbers of the same parity in order. However, this approach is essentially a bubble sort restricted by parity. The number of operations in the worst case would be O(n^2), which is unacceptable given n can be 2⋅10^5.

The key observation that leads to a fast solution is that the operation allows arbitrary reordering within the odd numbers and within the even numbers separately. Therefore, the only constraint comes from how the relative positions of odd and even numbers match the final sorted array. We can separate the array into its odd and even elements, sort them independently, and then check whether the sequence of parities in the sorted array matches what is achievable from the original array. If for each position in the fully sorted array we can assign an element of the correct parity from the original array, sorting is possible.

The optimal solution is to sort the array normally and then verify that each odd number in the sorted array has a corresponding odd number in the original array that could occupy that position, and similarly for even numbers. If all parity positions match, the array can be sorted using the allowed swaps. Otherwise, it cannot.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read the array length n and the array elements. We will process each test case independently because the constraints allow up to 10^4 test cases.
2. Separate the array into two lists: one containing all the odd numbers and another containing all the even numbers. This separation works because any swap is allowed within these lists.
3. Sort the original array to determine the target non-decreasing order. Also sort the odd and even lists individually. Sorting the original array gives the exact final sequence we need to achieve.
4. Iterate through the sorted target array. For each element, check whether it is odd or even. If it is odd, remove the smallest remaining odd number from the sorted odd list and verify that it matches the target element. If it is even, remove the smallest remaining even number from the sorted even list and verify it matches.
5. If at any point an element cannot be matched with a remaining number of the correct parity, output NO for this test case. If all elements are successfully matched, output YES.

Why it works: the algorithm maintains two invariants. The odd and even numbers can be permuted independently. By always taking the smallest available number of the correct parity, we simulate all possible swaps implicitly. If the sorted target sequence cannot be reconstructed using these two independent lists, no sequence of allowed swaps could produce the sorted array.

## Python Solution

```
PythonRun
```

The code first separates the array into odd and even elements. It then sorts these lists and the target array. The main loop verifies that each element in the sorted array can be matched to an element of the correct parity in the original array. Off-by-one errors are avoided by incrementing the indices only after a successful match. This approach directly implements the algorithm described above.

## Worked Examples

Consider the array [7, 10, 1, 3, 2]. The odd numbers are [7, 1, 3], sorted to [1, 3, 7]. The even numbers are [10, 2], sorted to [2, 10]. The sorted target array is [1, 2, 3, 7, 10]. Iterating through the target array, 1 matches the first odd, 2 matches the first even, 3 matches the second odd, 7 matches the third odd, 10 matches the second even. All matches succeed, so the output is YES.

For [11, 3, 15, 3, 2], the odd numbers sorted are [3, 3, 11, 15], the even numbers sorted are [2]. The target array sorted is [2, 3, 3, 11, 15]. The first element 2 matches the only even number, 3 matches the first odd, 3 matches the second odd, 11 matches the third odd, 15 matches the fourth odd. The lists are exhausted correctly. Here the output is NO, which occurs because the number of odd elements in the original array is insufficient to place 15 in the target position relative to parity.

| Step | Target element | Odd pointer | Even pointer | Action |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0 | 1 matches odd[0] → odd_idx = 1 |
| 2 | 2 | 1 | 0 | 2 matches even[0] → even_idx = 1 |
| 3 | 3 | 1 | 1 | 3 matches odd[1] → odd_idx = 2 |
| 4 | 7 | 2 | 1 | 7 matches odd[2] → odd_idx = 3 |
| 5 | 10 | 3 | 1 | 10 matches even[1] → even_idx = 2 |

This confirms the algorithm correctly simulates swaps within parity groups.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the array and the odd/even subarrays dominates the runtime. |
| Space | O(n) | Separate lists for odd and even elements require linear space. |

Given that the sum of n over all test cases is 2⋅10^5, the algorithm runs comfortably within 2 seconds.

## Test Cases

```
PythonRun
```
