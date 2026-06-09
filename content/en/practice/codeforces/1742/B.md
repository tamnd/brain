---
title: "CF 1742B - Increasing"
description: "We are given multiple independent arrays. For each one, we are allowed to reorder its elements arbitrarily, and we need to decide whether it is possible to arrange them so that every element is strictly smaller than the next one."
date: "2026-06-09T16:12:19+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1742
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 827 (Div. 4)"
rating: 800
weight: 1742
solve_time_s: 86
verified: false
draft: false
---

[CF 1742B - Increasing](https://codeforces.com/problemset/problem/1742/B)

**Rating:** 800  
**Tags:** greedy, implementation, sortings  
**Solve time:** 1m 26s  
**Verified:** no  

## Solution
## Problem Understanding

We are given multiple independent arrays. For each one, we are allowed to reorder its elements arbitrarily, and we need to decide whether it is possible to arrange them so that every element is strictly smaller than the next one.

In more concrete terms, we are checking whether the multiset of values can be turned into a sequence with no equal adjacent values after sorting or rearranging.

The constraints are small. Each test case has at most 100 elements and there are at most 100 test cases, so even an $O(n \log n)$ sort per test case is comfortably fast. This immediately rules out any need for optimization tricks beyond standard sorting or counting.

A key edge case is when duplicates exist. For example, if all elements are the same like `[5, 5, 5]`, no rearrangement can make the sequence strictly increasing because strict ordering forbids equality anywhere. On the other hand, if all elements are distinct, sorting them always produces a valid strictly increasing sequence.

Another subtle case is when duplicates exist but are not obvious at first glance, such as `[1, 2, 2, 3]`. Even though most elements are distinct, the repeated `2` prevents strict increase, since any ordering will place both copies of `2` somewhere in the sequence and they must violate strictness.

## Approaches

The brute-force idea is to try every permutation of the array and check whether any permutation is strictly increasing. This is correct because it explores the full solution space. However, the number of permutations is $n!$, which becomes infeasible even for moderate values like $n = 15$, where this already exceeds billions of configurations.

The key observation is that ordering freedom does not actually give us many degrees of freedom in this problem. The condition we want depends only on whether we can assign strictly increasing ranks to all elements. Sorting reveals the best possible structure immediately. If after sorting there are any equal adjacent elements, then no rearrangement can avoid them being adjacent somewhere in value order, and strict increase becomes impossible.

So the problem reduces to a simple check: sort the array and ensure every adjacent pair is strictly increasing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n!)$ | $O(n)$ | Too slow |
| Optimal (sorting) | $O(n \log n)$ |  |  |
