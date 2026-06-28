---
title: "CF 104872H - Scooter Numbers"
description: "We are given a fixed integer $n$. The task is to consider every way of writing $n$ as a sum of positive integers where order does not matter, so each representation is a nondecreasing sequence. Each such representation is treated as a multiset of parts."
date: "2026-06-28T10:27:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104872
codeforces_index: "H"
codeforces_contest_name: "2023-2024 Russia Team Open, High School Programming Contest (VKOSHP XXIV)"
rating: 0
weight: 104872
solve_time_s: 22
verified: false
draft: false
---

[CF 104872H - Scooter Numbers](https://codeforces.com/problemset/problem/104872/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a fixed integer $n$. The task is to consider every way of writing $n$ as a sum of positive integers where order does not matter, so each representation is a nondecreasing sequence. Each such representation is treated as a multiset of parts.

For each multiset, we compute its mex, defined as the smallest positive integer that does not appear among its elements. After computing this value for every valid multiset partition of $n$, we sum all mex values and output the result modulo $10^9+7$.

So the input defines a size $n$, and the output aggregates a function over all integer partitions of $n$, where the function depends only on which small integers appear in the partition, not their order.

The constraint $n \le 1000$ immediately rules out enumerating all partitions. The number of partitions grows roughly like $e^{\Theta(\sqrt{n})}$, which is already large at $n=1000$. A brute force enumeration would require generating every partition and computing mex per partition, which is infeasible.

A subtle edge case is when partitions are dominated by large parts. For example, the partition $[n]$ always contributes mex $1$. Another extreme is $[1,1,\dots,1]$, where mex is $2$. These extremes suggest mex depends on the presence of small integers rather than the full structure of the partition.

A naive approach would overcount or recompute mex inefficiently if it tries to generate partitions explicitly. Another failure mode is recomputing mex for each partition in linear time, which multiplies an already exponential enumeration cost.

## Approaches

A brute force method enumerates all partitions of $n$, stores each multiset, computes its mex by checking integers starting from $1$, and sums results. This is correct because it follows the definition directly. However, the number of partitions of $1000$ is around $2.4 \times 10^{31}$, so even generating them is impossible within time limits.

The key observation is that mex depends only on whether each integer $1,2,3,\dots$ appears in the partition. If we fix a value $k$, then a partition has mex exactly $k$ if it contains all numbers $1$ through $k-1$ at least once, and contains no $k$, while possibly containing numbers greater than $k$.

So the problem becomes counting partitions of $n$ with restricted inclusion constraints. We reduce the global sum into a sum ov
