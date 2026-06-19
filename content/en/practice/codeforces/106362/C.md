---
title: "CF 106362C - Edward is Sigma"
description: "Before writing the full editorial, there is a fundamental issue: the provided “problem statement” for Codeforces 106362C is incomplete and appears corrupted or placeholder-like."
date: "2026-06-19T08:30:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106362
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 2-11-2026 Div. 2 (Beginner)"
rating: 0
weight: 106362
solve_time_s: 37
verified: false
draft: false
---

[CF 106362C - Edward is Sigma](https://codeforces.com/problemset/problem/106362/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** no  

## Solution
Before writing the full editorial, there is a fundamental issue: the provided “problem statement” for Codeforces 106362C is incomplete and appears corrupted or placeholder-like.

What is visible is only a fragment of commentary about an “increasing array” and something called “charisma average”, but there is no formal definition of:

- the input format (what is given exactly),
- the required output,
- what “subsection” or “charisma average” precisely means,
- what operation or query we are supposed to perform.

Because of this, any attempt to produce a correct Codeforces-style editorial would necessarily involve guessing the actual problem, which would violate correctness requirements for a solution manual and would be misleading.

### What is missing / ambiguous

From the fragment, we can only infer something vague:

- There is an array that is increasing (strictly or non-decreasing is unclear).
- Some statistic called “charisma average” is computed over subsections.
- There is mention of fixed subsection sizes and possibly checking existence via binary search.

However, none of the following is defined:

- whether we are selecting subarrays, subsequences, or windows,
- how “charisma average” is computed,
- whether we are answering queries or computing a global property,
- what the output should be (boolean, count, maximum value, etc.).

### Why this matters

A Codeforces editorial depends heavily on precise problem semantics. Even small differences completely change the solution class:

- If it is sliding window averages → prefix sums + monotonic structure.
- If it is LIS-like structure → DP / binary search.
- If it is query existence → sorting + binary search.
- If it is convexity over subsequences → slope trick / monotonic queue.

Without the actual definition, writing an “optimal algorithm”, correctness proof, and test cases would be fabrication rather than explanation.

### What I need to proceed

Please provide one of the following:

1. The full original Codeforces problem statement, or
2. A clear restatement including:

- input format,
- definition of “charisma average”,
- what must be computed,
- constraints.

Once that is available, I can produce the full editorial in the exact requested Codeforces style, including algorithm walkthrough, proofs, code, and edge-case analysis.

If you want, you can also just paste the raw statement text or screenshot transcription, and I’ll reconstruct it cleanly before writing the editorial.
