---
title: "CF 105537I - If I Could Turn Back Time"
description: "We are given two sequences of mountain heights of the same length. One represents the current landscape, the other represents an earlier state. The landscape evolves over discrete years."
date: "2026-06-27T00:59:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105537
codeforces_index: "I"
codeforces_contest_name: "2024-2025 ICPC NERC (NEERC), North-Western Russia Regional Contest (Northern Subregionals)"
rating: 0
weight: 105537
solve_time_s: 21
verified: false
draft: false
---

[CF 105537I - If I Could Turn Back Time](https://codeforces.com/problemset/problem/105537/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 21s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two sequences of mountain heights of the same length. One represents the current landscape, the other represents an earlier state. The landscape evolves over discrete years. In each year, a threshold value is chosen, and every mountain whose current height is at least that threshold is reduced by exactly one unit. This operation can affect multiple mountains simultaneously, and different years may use different thresholds.

The task is to determine whether it is possible to transform the older heights into the current heights using some sequence of such yearly operations, and if so, compute the minimum number of years required.

A useful way to interpret the process is to think of each mountain independently receiving a number of decrements, but with a coupling constraint: in a single year, only mountains above a chosen cutoff are affected together. This means we cannot freely decrement arbitrary subsets independently; the structure of which mountains get decremented together matters.

The constraints imply up to 10^5 total mountains across test cases. Any solution must be linear or near-linear per test case. Quadratic comparisons between all pairs of mountains are impossible, and even O(n log n) approaches need to be carefully justified as global sorting plus linear sweeps only.

A subtle failure case arises when the transformation is locally plausible per mountain but globally inconsistent due to the shared yearly threshold constraint.

For example, if one mountain must be reduced many more times than another but starts lower in height difference, a naive per-index subtraction check would accept it incorrectly. Consider:

Input:

n = 2

current = [1, 10]

past = [5, 12]

Differences are [4, 2], suggesting 4 and 2 decrements per mountain. A naive approach might think we can apply 4 and 2 independent steps. But in reality, once we pick a threshold affecting the second mountain, it may also affect the first depending on relative heights, and the coupling can make the schedule infeasible.

The core difficulty is that operations are not per-element but
