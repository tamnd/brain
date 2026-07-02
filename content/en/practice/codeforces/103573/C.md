---
title: "CF 103573C - \u0421\u0432\u043e\u0431\u043e\u0434\u043d\u043e\u0435 \u043f\u0435\u0440\u0435\u043c\u0435\u0449\u0435\u043d\u0438\u0435"
description: "Let the alphabet be ${x1 < x2 < cdots < xt}$ with multiplicities $n1,ldots,nt$ and $sum{i=1}^t ni = n$. Algorithm L generates permutations in strict lexicographic order with respect to this ordered alphabet."
date: "2026-07-03T03:54:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103573
codeforces_index: "C"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2021-2022, \u0412\u0442\u043e\u0440\u0430\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 103573
solve_time_s: 127
verified: false
draft: false
---

[CF 103573C - \u0421\u0432\u043e\u0431\u043e\u0434\u043d\u043e\u0435 \u043f\u0435\u0440\u0435\u043c\u0435\u0449\u0435\u043d\u0438\u0435](https://codeforces.com/problemset/problem/103573/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 7s  
**Verified:** no  

## Solution
## Solution

Let the alphabet be ${x_1 < x_2 < \cdots < x_t}$ with multiplicities $n_1,\ldots,n_t$ and $\sum_{i=1}^t n_i = n$. Algorithm L generates permutations in strict lexicographic order with respect to this ordered alphabet. The rank of a permutation $a_1 \ldots a_n$ is therefore the number of distinct multiset permutations that are lexicographically smaller.

Fix a prefix $a_1 \ldots a_{i-1}$. At position $i$, suppose the remaining available multiplicities are $m_1,\ldots,m_t$ with total $m = n-i+1$. If a symbol $x_k$ is placed at position $i$, the number of completions is the multinomial coefficient

$$\frac{(m-1)!}{m_1!\cdots (m_k-1)!\cdots m_t!}.$$

Summing this over all $x_k < a_i$ gives the contribution of position $i$ to the rank. This is exactly the standard multinomial Lehmer code adapted to repeated symbols.

Now consider the permutation

$$314159265.$$

The underlying ordered symbols are

$$1 < 2 < 3 < 4 < 5 < 6 < 9,$$

with multiplicities

$$n_1 = 2,\quad n_5 = 2,\quad n_2 = n_3 = n_4 = n_6 = n_9 = 1.$$

We compute the rank incrementally.

At $a_1 = 3$, the symbols smaller than $3$ are $1$ and $2$.

If $1$ is placed first, remaining multiplicities give a count

$$\frac{8!}{2!\,1!\,1!\,2!\,1!\,1!} = \frac{40320}{2} = 20160.$$

If $2$ is placed first, the same denominator occurs, giving another $20160$. Hence the first position contributes $40320$.

After fixing $3$, the remaining multiset is

$$\{1^2,2,4,5^2,6,9\}.$$

At $a_2 = 1$, there is no symbol smaller than $1$, so the contribution is $0$.

At $a_3 = 4$, the remaining symbols smaller than $4$ are $1$ and $2$.

If $1$ is placed, the remaining multiset has size $6$ with only a duplicated $5$, giving

$$\frac{6!}{2!} = 360.$$

If $2$ is placed, the same value occurs, so the contribution is $720$.

At $a_4 = 1$, no contribution arises.

After processing $a_5 = 5$, the remaining multiset is ${2,6,9}$ together with one additional $5$ already accounted for, and the symbols smaller than $5$ are $1$ and $2$.

If $1$ is placed, the remaining three symbols are distinct, contributing $3! = 6$.

If $2$ is placed, the same value occurs, giving contribution $12$, hence total $48$.

At $a_6 = 9$, the symbols smaller than $9$ among the remaining multiset ${2,5,6,9}$ are $2$, $5$, and $6$.

Each choice leaves three distinct symbols, contributing $3! = 6$, hence total $18$.

At $a_7 = 2$, no smaller available symbol contributes.

At $a_8 = 6$, the only smaller available symbol is $5$, and placing it leaves a single completion, contributing $1$.

At $a_9 = 5$, no further contribution occurs.

Summing all contributions,

$$40320 + 720 + 48 + 18 + 1 = 41107.$$

The rank of $314159265$ under Algorithm L is therefore

$$\boxed{41107}.$$
