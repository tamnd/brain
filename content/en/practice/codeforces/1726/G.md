---
title: "CF 1726G - A Certain Magical Party"
description: "I can't reliably write a complete correctness-proof editorial and accepted implementation for Codeforces 1726G from the problem statement alone."
date: "2026-06-09T18:59:26+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "data-structures", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1726
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 819 (Div. 1 + Div. 2) and Grimoire of Code Annual Contest 2022"
rating: 3300
weight: 1726
solve_time_s: 48
verified: false
draft: false
---

[CF 1726G - A Certain Magical Party](https://codeforces.com/problemset/problem/1726/G)

**Rating:** 3300  
**Tags:** combinatorics, data structures, greedy, sortings  
**Solve time:** 48s  
**Verified:** no  

## Solution
I can't reliably write a complete correctness-proof editorial and accepted implementation for Codeforces 1726G from the problem statement alone.

This is a 3300-rated problem, and the publicly available editorial material I could verify only exposes a few hints:

- The final common value is uniquely determined as $T = M + n - 1$, where $M$ is the maximum initial happiness.
- For every $x < T$, there can be at most one person of type $(x,1)$.
- The intended solution uses a nontrivial greedy ordering rule: whenever several candidates can immediately reach $T$, prefer the larger happiness value, and for equal happiness prefer personality $1$ over personality $0$.

Those hints are not sufficient to reconstruct the full accepted algorithm, proof, counting method, and implementation with the level of rigor your prompt requests. Producing a full editorial anyway would risk inventing details and giving an incorrect solution.

If you can provide either:

1. the official editorial text for problem G,
2. an accepted code (C++ or Python),
3. or a link/screenshot of the full editorial section for 1726G,

then I can turn it into the detailed Codeforces-style editorial format you requested, including the reasoning, proof sketch, walkthrough, Python implementation, worked examples, complexity analysis, and test cases.
