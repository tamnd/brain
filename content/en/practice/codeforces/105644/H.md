---
title: "CF 105644H - Holiday Regifting"
description: "I can’t write a correct, detailed editorial for this problem yet because the statement we have is incomplete/garbled in a way that changes the meaning of the process in critical places."
date: "2026-06-26T16:12:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105644
codeforces_index: "H"
codeforces_contest_name: "Osijek Competitive Programming Camp, Winter 2023, Day 8: Dilhan Salgado Contest (The 1st Universal Cup. Stage 5: Osijek)"
rating: 0
weight: 105644
solve_time_s: 58
verified: false
draft: false
---

[CF 105644H - Holiday Regifting](https://codeforces.com/problemset/problem/105644/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** no  

## Solution
I can’t write a correct, detailed editorial for this problem yet because the statement we have is incomplete/garbled in a way that changes the meaning of the process in critical places.

In particular, the rules around how gifts are propagated are ambiguous in the version you pasted:

- whether “mentor” edges are directed from lower index to higher index for every friendship, or defined per endpoint
- what exactly triggers a “nearly full house” recursion in terms of capacity equality versus strict inequality
- what exactly is meant by “all remaining leftover gifts are incinerated” in terms of state changes per operation
- and most importantly, what constitutes a single “day” state transition

These details determine whether the system is a linear DAG flow, a stack-based simulation, or a number-theoretic recurrence. The sample outputs (like 24 and 8739360) strongly suggest a structured combinational invariant (likely DP over a DAG with multiplicative contributions), but without the exact transition rules, multiple fundamentally different solutions fit the same high-level description.

If you can paste the original Codeforces statement (or confirm the exact rules for mentor direction and the overflow condition), I can produce the full editorial in the requested format, including a clean optimal derivation and implementation.

Right now, anything more specific would risk inventing mechanics that aren’t actually part of the problem.
