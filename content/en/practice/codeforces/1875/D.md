---
title: "CF 1875D - Jellyfish and Mex"
description: "We are given an array of nonnegative integers. The task is to remove elements from the array one by one, and after each removal, we add the MEX of the remaining array to a running total. The goal is to minimize this total by choosing the deletion order optimally."
date: "2026-06-09T00:57:52+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 1875
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 901 (Div. 2)"
rating: 1600
weight: 1875
solve_time_s: 30
verified: false
draft: false
---

[CF 1875D - Jellyfish and Mex](https://codeforces.com/problemset/problem/1875/D)

**Rating:** 1600  
**Tags:** dp  
**Solve time:** 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of nonnegative integers. The task is to remove elements from the array one by one, and after each removal, we add the MEX of the remaining array to a running total. The goal is to minimize this total by choosing the deletion order optimally. The MEX of an array is the smallest nonnegative integer not present in the array, so the sequence of MEX values depends entirely on which elements are deleted first.

The input gives multiple test cases, each with an array up to length 5000. The sum of all array lengths across test cases is at most 5000. Each element can be very large, up to $10^9$. This means we cannot use a direct frequency array indexed by the element values. Our algorithm must avoid operations proportional to the maximum element.

A naive solution that recalculates the MEX after every deletion is too slow, because each recalculation requires scanning or maintaining the entire array, which is $O(n^2)$ in total. Edge cases arise when the array contains repeated elements or when some small numbers are missing initially, as these determine the early MEX values. For instance, in the array `[1,2]`, the initial MEX is 0. A careless approach that always deletes the largest element first might incorrectly increment the total unnecessarily. Similarly, arrays with gaps in the first few nonnegative integers require careful deletion to avoid adding unnecessary MEX values.

## Approaches

The brute-force solution is to try every permutation of deletions, recompute the MEX after each removal, and sum them. This guarantees the minimum sum, but it is factorial in $n$ and completely impractical for $n = 5000$.

The key observation is that the contribution of each number to the total depends only on how many copies of numbers less than the MEX remain. Once a number is deleted that affects the current MEX, the MEX either stays the same or increases. We can exploit this by thinking in terms of frequency counts of each number, only for numbers up to $n$, because MEX cannot exceed $n$.

We maintain a frequency array for numbers $0$ to $n$ and simulate deletion in two phases. First, we remove enough duplicates of numbers less than the current MEX to avoid increasing it, minimizing the total. Then we remove numbers equal to the current MEX to increase it only when unavoidable. Using dynamic programming, we track the minimum total for having removed a certain number of elements, knowing how many duplicates we can afford to delete without increasing MEX. This reduces the problem from factorial complexity to quadratic in $n$, which fits the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal (Frequency + DP) | O(n^2) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Count the frequency of each integer in the array that is less than or equal to $n$. Ignore numbers greater than $n$ because they do not affect MEX until all numbers 0 through n are removed.
2. Initialize a dynamic programming table `dp[i][j]` where `i` is the current MEX candidate and `j` is the number of extra duplicates removed beyond the first copy of each number. Set all values to infinity initially except `dp[0][0] = 0`.
3. Iterate MEX candidates from 0 to $n$. For each candidate `i`, consider deleting `k` duplicates (0 ≤ k ≤ frequency[i]) of `i` before the MEX reaches `i`. Update `dp[i+1][new_j]` as `dp[i][j] + (frequency[i] - k)`, wh_]()
