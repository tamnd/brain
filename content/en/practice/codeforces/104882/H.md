---
title: "CF 104882H - Have fun taking tests"
description: "We are dealing with an interactive multiple-choice test. The test contains $n$ questions, and each question has exactly two possible answers, where exactly one is correct. We do not know the correct answers in advance, and we cannot query them directly."
date: "2026-06-28T09:19:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104882
codeforces_index: "H"
codeforces_contest_name: "Voronezh State University - Sitronics contest II"
rating: 0
weight: 104882
solve_time_s: 36
verified: false
draft: false
---

[CF 104882H - Have fun taking tests](https://codeforces.com/problemset/problem/104882/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** no  

## Solution
## Problem Understanding

We are dealing with an interactive multiple-choice test. The test contains $n$ questions, and each question has exactly two possible answers, where exactly one is correct. We do not know the correct answers in advance, and we cannot query them directly. Instead, we answer questions one by one and only learn a final score at the end of each full attempt.

After finishing an attempt, we are given only a grade derived from the fraction of correct answers. A score of at least 50% is already considered satisfactory, and any such attempt immediately ends the interaction successfully. Otherwise, we are allowed to try again, with at most three attempts in total.

The key difficulty is that we never receive per-question feedback, only the aggregate result of an entire attempt. This means any strategy must rely purely on structure, not learning individual answers.

The constraints are small: $n \le 100$. This rules out anything computationally heavy per question, but more importantly, this is not a computational bottleneck problem. The limitation is informational: we simply do not have enough feedback to reconstruct the answer key in a fine-grained way.

A naive but common misconception is to think we need to "learn" correct answers across attempts. However, since we only receive a single number per attempt, there is no way to isolate correctness of individual questions. Any approach depending on per-question inference will fail.

The only meaningful edge case to consider is adversarial placement of correct answers. For example, if all correct answers are "A", then always choosing "A" immediately succeeds. Conversely, if correct answers are distributed evenly, naive guessing may fail, but we still must guarantee success within three attempts.

The interaction constraint is strict: any wrong format or exceeding attempt limit immediately terminates the program. However, the core challenge is not formatting but designing a strategy that guarantees reaching at least 50% correct.

## Approaches

A brute-force interpretation would be to try to deduce the correct answer for each question. One might imagine using different answer patterns across attempts and comparing scores to infer per-question correctness. For instance, flipping subsets of answers between attempts and solving a system of equations over the unknown correct answers.

This idea quickly becomes infeasible in practice. Even though each attempt gives a scalar result, reconstructing $n$ binary variables from at most three scalar
