---
title: "CF 102916J - Lost Island"
description: "Let $a1 ge a2 ge cdots ge am ge 1$ be a partition of $n$ into $m$ parts that is optimally balanced, meaning $ Let $t$ be the number of parts equal to $x$ and $m-t$ the number of parts equal to $x-1$. The partition has total sum $$n = tx + (m-t)(x-1) = mx - (m-t)."
date: "2026-07-04T08:03:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102916
codeforces_index: "J"
codeforces_contest_name: "Samara Farewell Contest 2020 (XXI Open Cup, Grand Prix of Samara)"
rating: 0
weight: 102916
solve_time_s: 152
verified: false
draft: false
---

[CF 102916J - Lost Island](https://codeforces.com/problemset/problem/102916/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 32s  
**Verified:** no  

## Solution
## Solution

Let $a_1 \ge a_2 \ge \cdots \ge a_m \ge 1$ be a partition of $n$ into $m$ parts that is optimally balanced, meaning $|a_i-a_j|\le 1$ for all $1\le i,j\le m$. The condition is equivalent to requiring that the largest and smallest parts differ by at most $1$, so if $a_1 = x$, then every part satisfies $a_m \in {x, x-1}$ and no other value is possible.

Let $t$ be the number of parts equal to $x$ and $m-t$ the number of parts equal to $x-1$. The partition has total sum

$$n = tx + (m-t)(x-1) = mx - (m-t).$$

Solving for $x$ gives

$$mx = n + m - t,\quad x = \frac{n+m-t}{m}.$$

Since $x$ is an integer, $n+m-t \equiv 0 \pmod m$, hence $t \equiv n \pmod m$. Write

$$n = mq + r,\quad 0 \le r < m,$$

so $q = \lfloor n/m \rfloor$ and $r = n \bmod m$.

Substituting into the expression for $n$,

$$n = m q + r.$$

An optimally balanced partition must use parts differing by at most $1$, so the only possible values are $q$ and $q+1$. Let $t$ be the number of parts equal to $q+1$, and $m-t$ the number of parts equal to $q$. Then the sum constraint becomes

$$n = t(q+1) + (m-t)q = mq + t.$$

Comparing with $n = mq + r$ gives $t = r$. Hence exactly $r$ parts are $q+1$ and the remaining $m-r$ parts are $q$.

This determines a unique partition since the sequence is forced to be nonincreasing, with all larger parts placed first:

$$a_1 = \cdots = a_r = q+1,\quad a_{r+1} = \cdots = a_m = q.$$

To verify optimal balance, any pair of parts differs by either $0$ or $1$ since the only values present are $q$ and $q+1$, so $|a_i-a_j|\le 1$ holds. Any other partition into $m$ parts must deviate from this distribution of quotients and remainders, which would force some part to be at least $q+2$ or at most $q-1$, contradicting either the sum constraint or the nonincreasing condition with minimal spread.

Thus there is exactly one optimally balanced partition.

The $j$th part is therefore

$$a_j =
\begin{cases}
\left\lfloor \frac{n}{m} \right\rfloor + 1 & \text{if } 1 \le j \le n \bmod m,\\[6pt]
\left\lfloor \frac{n}{m} \right\rfloor & \text{if } n \bmod m < j \le m.
\end{cases}$$

This completes the proof. ∎
