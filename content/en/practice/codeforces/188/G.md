---
title: "CF 188G - Array Sorting"
description: "We are given a simple array of integers where each element ranges from 1 to 100. The goal is to produce a sorted version of this array in non-descending order. The input first gives the number of elements, and then each element appears on its own line."
date: "2026-06-03T01:08:05+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 188
codeforces_index: "G"
codeforces_contest_name: "Surprise Language Round 6"
rating: 1600
weight: 188
solve_time_s: 24
verified: false
draft: false
---

[CF 188G - Array Sorting](https://codeforces.com/problemset/problem/188/G)

**Rating:** 1600  
**Tags:** *special, implementation  
**Solve time:** 24s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a simple array of integers where each element ranges from 1 to 100. The goal is to produce a sorted version of this array in non-descending order. The input first gives the number of elements, and then each element appears on its own line. The output should be a single line with the array elements separated by spaces, sorted from smallest to largest, with duplicates appearing in order.

The constraints are very light. The array size n is at most 100, which is small enough that even algorithms with quadratic time complexity, like bubble sort or insertion sort, are feasible within the 2-second limit. Each array element being bounded between 1 and 100 also opens the possibility of using counting sort, though the problem size does not require it.

Non-obvious edge cases include arrays that are already sorted, arrays with all identical elements, and arrays that contain only the smallest or largest possible values. For example, if the input array is `[1, 1, 1, 1]`, the output must be `1 1 1 1`. A naive approach that attempts to remove duplicates or mismanages indexing could produce a wrong answer by compressing repeated values or skipping elements. Another subtle case is a reverse-sorted array like `[100, 99, 50, 1]`, which forces the algorithm to move elements across the entire array.

## Approaches

The brute-force approach is to read the array into a list and apply any standard sorting algorithm, such as bubble sort, selection sort, or insertion sort. These work because repeatedly comparing elements and swapping them eventually results in all elements in the correct order. For n = 100, the maximum number of comparisons in a quadratic sort would be about 10,000, which is negligible for modern CPUs. The correctness comes from the fact that each swap moves the array closer to fully sorted order. The only downside is that the approach does not scale to very large n.

The optimal approach in this context is to use the built-in sort function in Python. Python's `list.sort()` uses Timsort, which is highly efficient, stable, and handles small arrays almost instantly. The array size n = 100 and element range [1, 100] make this approach both trivial to implement and fully within performance limits. The insight here is that the problem does not require algorithmic creativity; it is more about precise input handling and correct formatting in output.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (manual bubble/insertion sort) | O(n^2) | O(n) | Accepted |
| Python built-in sort | O(n log n) | O(n) | Accepted |

##
