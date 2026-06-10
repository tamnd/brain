---
title: "CF 1523C - Compression and Expansion"
description: "We are given a sequence of integers, each representing the last number of a nested list item after William accidentally erased everything else. The goal is to reconstruct one valid nested list that could have produced this sequence."
date: "2026-06-10T17:33:54+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "greedy", "implementation", "trees"]
categories: ["algorithms"]
codeforces_contest: 1523
codeforces_index: "C"
codeforces_contest_name: "Deltix Round, Spring 2021 (open for everyone, rated, Div. 1 + Div. 2)"
rating: 1600
weight: 1523
solve_time_s: 73
verified: false
draft: false
---

[CF 1523C - Compression and Expansion](https://codeforces.com/problemset/problem/1523/C)

**Rating:** 1600  
**Tags:** brute force, data structures, greedy, implementation, trees  
**Solve time:** 1m 13s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of integers, each representing the last number of a nested list item after William accidentally erased everything else. The goal is to reconstruct one valid nested list that could have produced this sequence. Each item in a valid nested list is a sequence of integers separated by dots, for example `1.2.3`. A new number can be added either by extending the previous item at the current level (incrementing the last number) or by starting a deeper level (appending `.1`). The reconstructed list must maintain the original increasing lexicographical order.

The input consists of multiple test cases, each giving the number of lines `n` and the sequence of last numbers `a_i`. The maximum `n` across all test cases sums to 1000, which means we can afford O(n^2) or better solutions comfortably. Each `a_i` is at most `n`, so we can track sequences without worrying about large numbers or overflows.

A tricky edge case occurs when consecutive numbers repeat `1`, such as `1 1 1`. A naive approach that simply appends `.1` every time will fail if it doesn't correctly backtrack to the appropriate parent level. Another subtle situation arises when the sequence jumps forward, for example `1 2 1 2`. We must correctly identify when to step back up the hierarchy to attach the next number.

## Approaches

The brute-force approach would be to try all possible valid nested lists and see which one produces the given sequence. This is correct in principle, but each line has multiple valid insert positions and operations, leading to exponential complexity. With `n` up to 1000, the number of combinations becomes astronomical, making this infeasible.

The key insight is that the structure is implicitly hierarchical and we can maintain a current path of numbers representing the last item inserted. Each new number either starts a new sublist (`1`), continues the current level (`prev + 1`), or moves up one or more levels until we can place it. This observation lets us reconstruct the nested list greedily in a single pass. By maintaining a "current sequence" and popping elements when the next number does not continue the last number, we can reconstruct the sequence correctly.

The greedy method works because the given sequence guarantees that at least one valid list exists, and the constraints on how numbers increase and how `.1` sequences start enforce a unique place to append each number.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Greedy Reconstruction | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an empty list `path` to represent the current sequence of numbers for the most recently constructed item.
2. Iterate through each number `x` in the sequence. If `x` is `1`, append `1` to the path. This starts a new sublist at the current or previous level.
3. If `x` is greater than `1`, check whether it can extend the last number in the path. While the last element in the p
