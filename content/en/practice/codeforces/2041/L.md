---
title: "CF 2041L - Building Castle"
description: "I can't provide a correct editorial for Codeforces 2041L from the problem statement alone because the key geometric optimization step is nontrivial, and I do not have enough information about the official solution to reconstruct a provably correct accepted algorithm."
date: "2026-06-08T09:46:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 2041
codeforces_index: "L"
codeforces_contest_name: "2024 ICPC Asia Taichung Regional Contest (Unrated, Online Mirror, ICPC Rules, Preferably Teams)"
rating: 2900
weight: 2041
solve_time_s: 82
verified: false
draft: false
---

[CF 2041L - Building Castle](https://codeforces.com/problemset/problem/2041/L)

**Rating:** 2900  
**Tags:** -  
**Solve time:** 1m 22s  
**Verified:** no  

## Solution
I can't provide a correct editorial for Codeforces 2041L from the problem statement alone because the key geometric optimization step is nontrivial, and I do not have enough information about the official solution to reconstruct a provably correct accepted algorithm.

For a 2900-rated geometry problem, inventing the missing derivation would likely produce an incorrect editorial and incorrect code.

One useful observation that can be derived rigorously is the following:

Let $P$ be the original convex polygon and let $P_c$ be its reflection through a point $c$. For a fixed center $c$, among all centrally symmetric sets with center $c$, the minimum possible symmetric-difference distance to $P$ is achieved by

$$P \cap P_c.$$

The resulting cost is

$$\frac{1}{2}\operatorname{area}(P \triangle P_c)
=
\operatorname{area}(P)-\operatorname{area}(P\cap P_c).$$

So the whole problem reduces to

$$\max_c \operatorname{area}(P\cap P_c),$$

which is equivalent to finding the largest centrally symmetric convex subset of $P$.

For the sample triangle, the maximum intersection area is $22/3$, giving

$$11-\frac{22}{3}=\frac{11}{3},$$

which matches the sample output.

However, the remaining step, computing

$$\max_c \operatorname{area}(P\cap P_c)$$

for a convex polygon with $n\le 500$, is exactly the difficult part of the problem and requires the official geometric machinery. Without that derivation, I would not be able to provide a trustworthy editorial or accepted implementation.

If you can provide either:

1. the official editorial,
2. a solution code that needs to be explained,
3. the contest tutorial PDF,
4. or even a short hint from the editorial,

I can then write the full Codeforces-style editorial in the format you requested.
