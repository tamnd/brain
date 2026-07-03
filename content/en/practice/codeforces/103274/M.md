---
title: "CF 103274M - Moon Dancers"
description: "We are missing one crucial piece: the actual algorithmic structure of the task is not fully recoverable from the partial statement we initially saw, and the problem page text itself is incomplete/fragmented in typical Gym scraping output. The key line “F."
date: "2026-07-03T14:36:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103274
codeforces_index: "M"
codeforces_contest_name: "2021 ICPC Gran Premio de Mexico 1ra Fecha"
rating: 0
weight: 103274
solve_time_s: 27
verified: false
draft: false
---

[CF 103274M - Moon Dancers](https://codeforces.com/problemset/problem/103274/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 27s  
**Verified:** no  

## Solution
We are missing one crucial piece: the actual algorithmic structure of the task is not fully recoverable from the partial statement we initially saw, and the problem page text itself is incomplete/fragmented in typical Gym scraping output. The key line “F. Lantern Hopping” and other unrelated neighboring tasks confirm the context is a multi-problem contest dump, and what we retrieved earlier was only partial narrative, not the full specification of Moon Dancers.

To avoid hallucinating a wrong solution (which would completely break the editorial quality requirement you gave), I need the complete statement of **103274M - Moon Dancers**, especially the formal definition of:

what constitutes a valid “pairing” or configuration,

what transformations or constraints are allowed (rotation amount, matching rule),

and what exactly “maximum number of pairs” means in terms of computable structure.

Right now we only reliably know:

there are N dancers positioned on a circle by angles,

and some operation involves rotating K dancers counterclockwise and matching them with sitting dancers,

and we must maximize the number of resulting pairs.

But the missing formal condition is exactly what determines whether this is:

a circular matching problem,

a cyclic shift alignment problem,

a convolution/frequency problem,

or a geometric pairing under rotation invariance.

Those lead to completely different solutions.

If you paste the full statement (or even a screenshot/text dump), I’ll immediately produce a full Codeforces-style editorial in the exact format you specified, including brute force reasoning, optimal transformation insight, invariant proof, and a complete implementation.
