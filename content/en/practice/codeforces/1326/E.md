---
title: "CF 1326E - Bombs"
description: "We are given two permutations of length $n$, called $p$ and $q$. Conceptually, $p$ represents a sequence of values that we will process in order, and $q$ represents a priority order for planting \"bombs."
date: "2026-06-11T16:34:30+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1326
codeforces_index: "E"
codeforces_contest_name: "Codeforces Global Round 7"
rating: 2400
weight: 1326
solve_time_s: 65
verified: false
draft: false
---

[CF 1326E - Bombs](https://codeforces.com/problemset/problem/1326/E)

**Rating:** 2400  
**Tags:** data structures, two pointers  
**Solve time:** 1m 5s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two permutations of length $n$, called $p$ and $q$. Conceptually, $p$ represents a sequence of values that we will process in order, and $q$ represents a priority order for planting "bombs." Each bomb removes the largest element currently in a set $A$ as we traverse $p$. For each prefix of $q$, we want to compute the cost, defined as the largest element remaining in $A$ after processing all elements of $p$ with bombs placed in the positions indicated by that prefix.

The challenge is to compute these costs efficiently for all prefixes of $q$. The naive method-simulating the set $A$ and removing the largest for every bomb placement-takes $O(n^2)$ in the worst case, which is too slow for $n$ up to (300,00
