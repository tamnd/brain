---
title: "CF 102904A - Coins"
description: "Let $n ge m ge 1$ and let $a1 ge a2 ge cdots ge am ge 1$ be a partition of $n$ such that $ Indeed, if $a1$ is the maximum part and $am$ is the minimum part, the condition gives $a1 - am le 1$, hence $am in {a1, a1 - 1}$. Therefore every part equals either $a1$ or $a1 - 1$."
date: "2026-07-04T08:13:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102904
codeforces_index: "A"
codeforces_contest_name: "\u0426\u0438\u043a\u043b \u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434, \u0421\u0435\u0437\u043e\u043d 2020-21, \u041f\u044f\u0442\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102904
solve_time_s: 176
verified: false
draft: false
---

[CF 102904A - Coins](https://codeforces.com/problemset/problem/102904/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 56s  
**Verified:** no  

## Solution
## Solution

Let $n \ge m \ge 1$ and let $a_1 \ge a_2 \ge \cdots \ge a_m \ge 1$ be a partition of $n$ such that $|a_i - a_j| \le 1$ for all $i,j$. Then the set of distinct part values contains at most two consecutive integers.

Indeed, if $a_1$ is the maximum part and $a_m$ is the minimum part, the condition gives $a_1 - a_m \le 1$, hence $a_m \in {a_1, a_1 - 1}$. Therefore every part equals either $a_1$ or $a_1 - 1$.

Let $k$ denote the number of parts equal to $a_1$. Then $m-k$ parts equal $a_1 - 1$, and the sum condition becomes

$$n = k a_1 + (m-k)(a_1 - 1).$$

Expanding gives

$$n = k a_1 + m a_1 - k a_1 - m + k = m(a_1 - 1) + k.$$

Hence

$$k = n - m(a_1 - 1).$$

Since $0 \le k \le m$, the integer $a_1$ is constrained by

$$m(a_1 - 1) \le n \le m(a_1 - 1) + m,$$

which is equivalent to

$$a_1 - 1 \le \frac{n}{m} \le a_1.$$

Thus $a_1 = \left\lceil \frac{n}{m} \right\rceil$. Writing $n = qm + r$ with $0 \le r < m$, this yields $q = \left\lfloor \frac{n}{m} \right\rfloor$ and

$$a_1 =
\begin{cases}
q, & r = 0,\\
q+1, & r > 0.
\end{cases}$$

If $r = 0$, then $k = n - m(q-1) = mq - m(q-1) = m$, so all parts equal $q$.

If $r > 0$, then $a_1 = q+1$, and

$$k = n - m q = r.$$

Thus exactly $r$ parts equal $q+1$, and the remaining $m-r$ parts equal $q$.

Because the partition is nonincreasing, the first $r$ parts are $q+1$ and the remaining $m-r$ parts are $q$, so the $j$th part is

$$a_j =
\begin{cases}
q+1, & 1 \le j \le r,\\
q, & r < j \le m.
\end{cases}$$

Any optimally balanced partition must have this form since the number of parts equal to the larger value is uniquely determined by the sum constraint, and no other choice of values differing by at most $1$ can satisfy the required total. This completes the proof. ∎
