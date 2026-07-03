---
title: "CF 103443I - Seesaw"
description: "Let the given bit string be interpreted as an $(s,t)$-combination with $s=12$ zeros and $t=14$ ones, hence $n=s+t=26$. The string is $11001001000011111101101010.$ Chase’s sequence $C{st}$, as defined in equation (41), is a generating order on $(s,t)$-combinations."
date: "2026-07-03T07:42:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103443
codeforces_index: "I"
codeforces_contest_name: "The 2021 ICPC Asia Taipei Regional Programming Contest"
rating: 0
weight: 103443
solve_time_s: 38
verified: false
draft: false
---

[CF 103443I - Seesaw](https://codeforces.com/problemset/problem/103443/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 38s  
**Verified:** no  

## Solution
## Solution

Let the given bit string be interpreted as an $(s,t)$-combination with $s=12$ zeros and $t=14$ ones, hence $n=s+t=26$. The string is

$11001001000011111101101010.$

Chase’s sequence $C_{st}$, as defined in equation (41), is a generating order on $(s,t)$-combinations. In this exercise it is used in its lexicographic form on bit strings, so the rank of a combination is determined by the standard lexicographic counting rule: at each position, if a $1$ appears, we may replace it by a $0$ and count all completions with the remaining number of ones.

Let $r$ denote the number of remaining $1$-bits still to be placed. Initially $r=14$. At position $i$, if the bit is $1$, then setting it to $0$ forces a count of

$\binom{26-i}{r}$

completions among the remaining positions. After processing a $1$, we update $r \leftarrow r-1$.

We scan the string from left to right.

At position $1$, the bit is $1$, so the contribution is $\binom{25}{14}=\binom{25}{11}=4,457,400$. Then $r=13$.

At position $2$, the bit is $1$, so the contribution is $\binom{24}{13}=\binom{24}{11}=2,496,144$. Then $r=12$.

Positions $3,4$ are $0$, giving no contribution.

At position $5$, the bit is $1$, so the contribution is $\binom{21}{12}=\binom{21}{9}=293,930$. Then $r=11$.

Positions $6,7$ are $0$.

At position $8$, the bit is $1$, so the contribution is $\binom{18}{11}=\binom{18}{7}=31,824$. Then $r=10$.

Positions $9,10,11,12$ are $0$.

At position $13$, the bit is $1$, so the contribution is $\binom{13}{10}=\binom{13}{3}=286$. Then $r=9$.

At position $14$, the bit is $1$, so the contribution is $\binom{12}{9}=\binom{12}{3}=220$. Then $r=8$.

At position $15$, the bit is $1$, so the contribution is $\binom{11}{8}=\binom{11}{3}=165$. Then $r=7$.

At position $16$, the bit is $1$, so the contribution is $\binom{10}{7}=\binom{10}{3}=120$. Then $r=6$.

At position $17$, the bit is $1$, so the contribution is $\binom{9}{6}=\binom{9}{3}=84$. Then $r=5$.

At position $18$, the bit is $1$, so the contribution is $\binom{8}{5}=\binom{8}{3}=56$. Then $r=4$.

Position $19$ is $0$.

At position $20$, the bit is $1$, so the contribution is $\binom{6}{4}=\binom{6}{2}=15$. Then $r=3$.

At position $21$, the bit is $1$, so the contribution is $\binom{5}{3}=10$. Then $r=2$.

Position $22$ is $0$.

At position $23$, the bit is $1$, so the contribution is $\binom{3}{2}=3$. Then $r=1$.

Position $24$ is $0$.

At position $25$, the bit is $1$, so the contribution is $\binom{2}{1}=2$. Then $r=0$.

Position $26$ is $0$.

Summing all contributions,

$$\begin{aligned}
&4\,457\,400 + 2\,496\,144 + 293\,930 + 31\,824 + 286 + 220 + 165 + 120 + 84 + 56 + 15 + 10 + 3 + 2 \\
&= 7\,280\,259.
\end{aligned}$$

Thus the number of combinations preceding the given bit string in $C_{st}$ is

$\boxed{7\,280\,259}.$

This completes the computation. ∎
