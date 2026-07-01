---
title: "CF 104076J - Skills"
description: "Let $f(x1,ldots,xn)$ have truth table $tau$, and let $f^Z$ have truth table $tau^Z$. For $0 le k le n$, let $Sk(x1,ldots,xn)$ denote the subfunction obtained by fixing $x1=cdots=xk=1$, so its truth table is the subtable of $tau$ of order $n-k$ starting at position $2^k$ in the…"
date: "2026-07-02T02:50:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104076
codeforces_index: "J"
codeforces_contest_name: "2022 International Collegiate Programming Contest, Jinan Site"
rating: 0
weight: 104076
solve_time_s: 127
verified: false
draft: false
---

[CF 104076J - Skills](https://codeforces.com/problemset/problem/104076/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 7s  
**Verified:** no  

## Solution
## Solution

Let $f(x_1,\ldots,x_n)$ have truth table $\tau$, and let $f^Z$ have truth table $\tau^Z$. For $0 \le k \le n$, let $S_k(x_1,\ldots,x_n)$ denote the subfunction obtained by fixing $x_1=\cdots=x_k=1$, so its truth table is the subtable of $\tau$ of order $n-k$ starting at position $2^k$ in the lexicographic ordering of inputs. The goal is to determine the corresponding subfunction $S_k^Z$ of $f^Z$.

The Z-transform is defined recursively on concatenations $\alpha\beta$ by splitting at equal-length blocks and replacing certain structured concatenations by either duplication, zero padding, or recursive application of the transform to smaller blocks. Every clause in the definition preserves the property that the transform acts independently on blocks corresponding to fixed prefixes of variables. The decomposition of a truth table into subtables by fixing $x_1,\ldots,x_k$ depends only on the first $k$ levels of this recursive block structure.

The crucial observation is that the definition of $\tau^Z$ is compatible with restriction to any initial segment of the variable ordering. If $\tau$ is written as a concatenation of $2^k$ blocks of length $2^{n-k}$ corresponding to assignments of $(x_1,\ldots,x_k)$, then each clause in the Z-transform applies either uniformly to whole blocks or recursively inside blocks of equal structure. No clause mixes bits from different blocks determined by the first $k$ variables.

Therefore the restriction of $\tau^Z$ obtained by fixing $x_1=\cdots=x_k=1$ is exactly the Z-transform of the restricted string $\tau_{x_1=\cdots=x_k=1}$. This yields an identity of truth tables

$$(\tau_{x_1=\cdots=x_k=1})^Z = (\tau^Z)_{x_1=\cdots=x_k=1}.$$

Interpreting both sides as Boolean functions gives that the subfunction of $f^Z$ corresponding to fixing the first $k$ variables equals the Z-transform of the corresponding subfunction of $f$. In the notation of the exercise,

$$S_k^Z(x_1,\ldots,x_n) = (S_k(x_1,\ldots,x_n))^Z.$$

Since this equality holds for every $k$ with $0 \le k \le n$, the entire $k$-profile of $f^Z$ is obtained by applying the Z-transform levelwise to the $k$-profile of $f$, matching the correspondence established in Exercise 192 between profiles and z-profiles.

Thus

$$\boxed{S_k^Z = (S_k)^Z \quad \text{for all } 0 \le k \le n.}$$

This completes the proof. ∎
