---
title: "CF 105756B - Maximum Combo"
description: "I can write the editorial, but the problem statement for Codeforces Gym 105756B appears to be inconsistent with its samples. The statement says that jumping from portal i to portal j gives i j points, starting from portal 1."
date: "2026-06-25T16:03:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105756
codeforces_index: "B"
codeforces_contest_name: "AlgoChief Sprint Round 4"
rating: 0
weight: 105756
solve_time_s: 52
verified: false
draft: false
---

[CF 105756B - Maximum Combo](https://codeforces.com/problemset/problem/105756/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** no  

## Solution
I can write the editorial, but the problem statement for Codeforces Gym 105756B appears to be inconsistent with its samples.

The statement says that jumping from portal `i` to portal `j` gives `i * j` points, starting from portal `1`. Under that rule, for `n = 3` you could jump:

`1 -> 3`

and get `1 * 3 = 3` points, which matches the sample. However, for `n = 4`, the path

`1 -> 3 -> 4`

would give:

`1 * 3 + 3 * 4 = 15`

which is larger than the sample answer `10`.

So the examples do not correspond to the written transition rule. I do not want to invent an editorial and code for the wrong problem.

If you provide the original statement PDF, a link to the contest editorial, or the intended transition formula, I can produce the full editorial in the exact format you requested.
