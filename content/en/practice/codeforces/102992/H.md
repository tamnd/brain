---
title: "CF 102992H - Harmonious Rectangle"
description: "Let $alpha$ be a $t$-combination, so $alpha$ is a $t$-element subset of ${0,1,dots,n-1}$. The operator $partialt alpha$ produces all $(t-1)$-combinations obtained by deleting one element of $alpha$. If $alpha={ct,dots,c1}$, then $$partialt alpha={alphasetminus{cj}mid 1le jle t}."
date: "2026-07-04T02:53:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102992
codeforces_index: "H"
codeforces_contest_name: "2020-2021 ACM-ICPC, Asia Nanjing Regional Contest (XXI Open Cup, Grand Prix of Nanjing)"
rating: 0
weight: 102992
solve_time_s: 146
verified: false
draft: false
---

[CF 102992H - Harmonious Rectangle](https://codeforces.com/problemset/problem/102992/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 26s  
**Verified:** no  

## Solution
Let $\alpha$ be a $t$-combination, so $\alpha$ is a $t$-element subset of ${0,1,\dots,n-1}$.

The operator $\partial_t \alpha$ produces all $(t-1)$-combinations obtained by deleting one element of $\alpha$. If $\alpha={c_t,\dots,c_1}$, then

$$\partial_t \alpha=\{\alpha\setminus\{c_j\}\mid 1\le j\le t\}.$$

Each element of $\partial_t \alpha$ is therefore a $(t-1)$-combination of ${0,1,\dots,n-1}$.

The operator $\partial_{t+1} \alpha$ produces all $(t+1)$-combinations that contain $\alpha$, obtained by adjoining one new element not already in $\alpha$. If $\overline{\alpha}={0,1,\dots,n-1}\setminus \alpha$, then

$$\partial_{t+1} \alpha=\{\alpha\cup\{x\}\mid x\in \overline{\alpha}\}.$$

Each element of $\partial_{t+1} \alpha$ is therefore a $(t+1)$-combination containing $\alpha$.
