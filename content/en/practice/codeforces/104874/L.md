---
title: "CF 104874L - Lengths and Periods"
description: "We are given a single long string over lowercase English letters, and we want to measure how “repetitive” it can be in its most extreme localized form."
date: "2026-06-28T10:09:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104874
codeforces_index: "L"
codeforces_contest_name: "2019-2020 ICPC NERC (NEERC), North-Western Russia Regional Contest (Northern Subregionals)"
rating: 0
weight: 104874
solve_time_s: 24
verified: false
draft: false
---

[CF 104874L - Lengths and Periods](https://codeforces.com/problemset/problem/104874/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 24s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a single long string over lowercase English letters, and we want to measure how “repetitive” it can be in its most extreme localized form. The object we are searching for is not a global repetition pattern, but a contiguous fragment inside the string that behaves like a repeated block, possibly with a final partial copy.

Formally, we imagine choosing a pattern string $x$. Inside the input string $w$, we look for a substring that consists of several full copies of $x$, followed by a prefix of $x$. If this substring has total length $L$, then it represents a fractional number of repetitions of $x$, namely $L / |x|$. The task is to maximize this ratio over all possible choices of $x$ and all substrings that align with this structure.

So the problem reduces to finding the longest “fractional power” substring across all possible periods.

The input size reaches $2 \cdot 10^5$. Any solution that checks all substrings and all candidate periods directly leads to quadratic or worse behavior, since there are $O(n^2)$ substrings and each periodicity check is at least linear. That is far beyond what 2 seconds allows in Python.

A correct solution must therefore avoid iterating over substrings explicitly and instead reuse structure inside the string, especially prefix structure and periodicity information.

There are two subtle edge cases that break naive reasoning.

One is thinking only full repetitions matter. For example, in “abab”, the best pattern is “ab” repeated twice, giving exponent 2. But in strings like “mississippi”, the best structure involves a prefix repetition followed by a partial block, so ignoring partial overlaps loses the answer.

Another is assuming that the best pattern must be a prefix of the string. That is false: optimal patterns can start anywhere, as seen in “ississi” inside “mississippi”, where the repeating unit is not tied to the global prefix.

These two facts force us to consider periodic substrings implicitly, not just global prefixes or exact repeats.

## Approaches

A brute-force approach would try every substring $y = w[l:r]$, then for every possible period length $p$, verify how many full repeats of the candidate pattern of length $p$ occur inside $y$, plus a possible partial suffix. Each verification costs $O(|y|)$, and there are $O(n^2)$ substrings, giving $O(n^3)$ in the worst case. Even with optimizations, this collapses under $n = 200000$.

The key observation is that a substring has a large exponent exactly when it has a short period. If a substring of length $L$ has minimal period $p$, then its exponent is $L/p$. The problem becomes: find
