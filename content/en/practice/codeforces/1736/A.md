---
title: "CF 1736A - Make A Equal to B"
description: "This is a Type B (prove) problem. The statement requires a universal claim for all natural numbers $n$, namely that at least one of $S(7n)$ or $S(9n)$ exceeds $S(n)/5$."
date: "2026-06-09T18:00:22+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1736
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 825 (Div. 2)"
rating: 800
weight: 1736
solve_time_s: 117
verified: false
draft: false
---

[CF 1736A - Make A Equal to B](https://codeforces.com/problemset/problem/1736/A)

**Rating:** 800  
**Tags:** brute force, greedy, sortings  
**Solve time:** 1m 57s  
**Verified:** no  

## Solution
## Problem-Type Check

This is a **Type B (prove)** problem. The statement requires a universal claim for all natural numbers $n$, namely that at least one of $S(7n)$ or $S(9n)$ exceeds $S(n)/5$. A valid solution must establish the inequality rigorously for all $n$, not just for small examples or via intuition. Stepwise logical deductions with proper justifications are required.

## Step-by-Step Verification

**Step 1: Exploration with small values of $n$** - VALID. The computations for $n=1,2,10,111$ correctly illustrate the plausibility of the inequality, but they do not constitute a proof.

**Step 2: Lemma 1, claiming $S(9k) \ge S(k)$ for all $k$**
