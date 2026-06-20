---
title: "CF 106298A - Explosive String"
description: "The statement as provided is incomplete in a way that makes the actual task undefined. All we know is that the input contains a string with characters from {L, R, ?} and that we are allowed to replace every ‘?’ either with ‘L’ or with ‘R’."
date: "2026-06-20T22:44:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106298
codeforces_index: "A"
codeforces_contest_name: "OCPC 2024 Summer, Day 4: wuhudsm Contest"
rating: 0
weight: 106298
solve_time_s: 29
verified: false
draft: false
---

[CF 106298A - Explosive String](https://codeforces.com/problemset/problem/106298/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 29s  
**Verified:** no  

## Solution
The statement as provided is incomplete in a way that makes the actual task undefined.

All we know is that the input contains a string with characters from {L, R, ?} and that we are allowed to replace every ‘?’ either with ‘L’ or with ‘R’. What is missing is the objective function: what makes one resulting string better than another, or what property we are supposed to compute after the replacements.

Without that, there is no well-defined optimal strategy. For example, if the goal were to maximize adjacent equal pairs, then the optimal construction would differ completely from a case where we maximize alternating transitions, minimize runs, check lexicographically smallest outcome, or satisfy constraints involving substrings. Each of these leads to a different solution, and the correct editorial depends entirely on that missing condition.

If you can provide the full statement (especially the part describing what makes a valid or optimal “explosive string”), I can write the complete Codeforces-style editorial in the format you requested, including the algorithm derivation, proof, and implementation.
