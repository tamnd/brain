---
title: "CF 102219D - Ali The Multi-billionaire"
description: "I can write the editorial, but the problem statement you supplied is missing the single piece of information that determines the entire solution: the formula defining x from a and b."
date: "2026-08-20T03:45:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102219
codeforces_index: "D"
codeforces_contest_name: "2019 ICPC Malaysia National"
rating: 0
weight: 102219
solve_time_s: 86
verified: false
draft: false
---

[CF 102219D - Ali The Multi-billionaire](https://codeforces.com/problemset/problem/102219/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 26s  
**Verified:** no  

## Solution
I can write the editorial, but the problem statement you supplied is missing the single piece of information that determines the entire solution: the formula defining `x` from `a` and `b`.

The rendered statement literally contains:

> “These two integer is used to calculate another integer `x` using the following formula:”

followed by an omitted image. The official Codeforces statement has the same formula as an image, so the web copy does not expose it as text either. citeturn5view0

This is not a cosmetic omission. Different formulas lead to completely different algorithms. For example, using the sample's final values

`a = [3, 6, 6, 5, 5, 2, 3]`

and

`b = [1, 2, 1, 1, 1, 1, 2]`,

a product formula gives a total of `39`, while a power formula `a^b mod 100007` gives `85`, neither of which matches the sample output `16`.

The official page confirms that each friend starts with `a = b = 1`, that updates are inclusive clockwise circular ranges, and that each final `x` is reduced modulo `100005 + 7`; only
