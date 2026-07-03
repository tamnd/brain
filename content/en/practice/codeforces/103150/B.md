---
title: "CF 103150B - Arrowing Process"
description: "Let κt(N) be the leading parameter in the degree-$t$ combinatorial representation of $N$, so that κt(N) is the unique integer $nt$ satisfying $$binom{nt}{t} le N < binom{nt+1}{t}."
date: "2026-07-03T19:54:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103150
codeforces_index: "B"
codeforces_contest_name: "EZ Programming Contest #1"
rating: 0
weight: 103150
solve_time_s: 78
verified: false
draft: false
---

[CF 103150B - Arrowing Process](https://codeforces.com/problemset/problem/103150/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** no  

## Solution
## Solution

Let κ_t(N) be the leading parameter in the degree-$t$ combinatorial representation of $N$, so that κ_t(N) is the unique integer $n_t$ satisfying

$$\binom{n_t}{t} \le N < \binom{n_t+1}{t}.$$

This characterization follows from the greedy construction implicit in Theorem K and the representation in exercise 75, where κ_t(N) is the largest index appearing in the $t$-representation of $N$.

Write $n_t = \kappa_t(N)$. Then there exists a remainder $R$ such that

$$N = \binom{n_t}{t} + R, \qquad 0 \le R < \binom{n_t+1}{t} - \binom{n_t}{t}.$$

In particular, the defining inequality implies

$$0 \le R < \binom{n_t+1}{t} - \binom{n_t}{t},$$

and since $\binom{n_t+1}{t} > \binom{n_t}{t}$, the increment $N \mapsto N+1$ changes $n_t$ only when $R$ reaches its maximum possible value before a carry into the next binomial threshold occurs.

For $N+1$, there are two cases.

If $R+1 < \binom{n_t+1}{t} - \binom{n_t}{t}$, then $N+1$ still lies in the same interval

$$\binom{n_t}{t} \le N+1 < \binom{n_t+1}{t},$$

so κ_t(N+1) = n_t and therefore κ_t(N+1) - κ_t(N) = 0.

If $R$ attains its maximal value compatible with $n_t$, then $N+1$ reaches the next binomial boundary, meaning

$$N+1 = \binom{n_t+1}{t}.$$

In this case the maximality property of κ_t forces

$$\kappa_t(N+1) = n_t+1,$$

since $\binom{n_t+1}{t}$ is the first value requiring a leading index larger than $n_t$ in the combinatorial representation.

No larger jump can occur, since the defining inequality for κ_t shows that increasing $N$ by $1$ can cross at most one binomial threshold of the form $\binom{m}{t}$.

Therefore,

$$\kappa_t(N+1) - \kappa_t(N) =
\begin{cases}
1, & \text{if } N+1 = \binom{m}{t} \text{ for some } m,\\[4pt]
0, & \text{otherwise}.
\end{cases}$$

Equivalently, the increment occurs exactly when $N+1$ is a $t$-th binomial coefficient in the Pascal triangle enumeration, and in all other cases the leading combinatorial index remains unchanged.

$$\boxed{\kappa_t(N+1)-\kappa_t(N)\in\{0,1\},\ \text{equal to }1 \text{ iff } N+1=\binom{m}{t}\text{ for some }m.}$$

This completes the solution. ∎
