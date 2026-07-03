---
title: "CF 103329C - 0 Tree"
description: "Let $rs,dots,r0$ satisfy $$t = rs + cdots + r1 + r0,qquad 0 le rj le mj quad (s ge j ge 0).$$ Write $$Mj = sum{i=0}^j mi,qquad Tj = t - sum{i=j+1}^s ri,$$ so $Tj$ is the remaining sum to be distributed among indices $0,dots,j$ after fixing $rs,dots,r{j+1}$."
date: "2026-07-03T14:02:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103329
codeforces_index: "C"
codeforces_contest_name: "2020-2021 Summer Petrozavodsk Camp, Day 6: XJTU Contest (XXII Open Cup, Grand Prix of XiAn)"
rating: 0
weight: 103329
solve_time_s: 152
verified: false
draft: false
---

[CF 103329C - 0 Tree](https://codeforces.com/problemset/problem/103329/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 32s  
**Verified:** no  

## Solution
## Solution

Let $r_s,\dots,r_0$ satisfy

$$t = r_s + \cdots + r_1 + r_0,\qquad 0 \le r_j \le m_j \quad (s \ge j \ge 0).$$

Write

$$M_j = \sum_{i=0}^j m_i,\qquad T_j = t - \sum_{i=j+1}^s r_i,$$

so $T_j$ is the remaining sum to be distributed among indices $0,\dots,j$ after fixing $r_s,\dots,r_{j+1}$.

At position $j$, the values of $r_j$ are constrained by feasibility of completing the composition. After choosing $r_j$, the remaining value $T_{j-1} = T_j - r_j$ must satisfy

$$0 \le T_{j-1} \le M_{j-1}.$$

Hence

$$T_j - M_{j-1} \le r_j \le T_j,$$

together with $0 \le r_j \le m_j$. The admissible interval is therefore

$$L_j = \max(0,\, T_j - M_{j-1}),\qquad U_j = \min(m_j,\, T_j).$$

Lexicographic order on $(r_s,\dots,r_0)$ is taken with $r_s$ most significant, so $r_0$ varies fastest.

The first solution is obtained by choosing each component at its minimal feasible value with $T_s = t$:

$$r_j = L_j \quad (s \ge j \ge 0).$$

### Algorithm B (Bounded compositions)

Sentinels $M_{-1} = 0$, $r_{s+1} = 0$ are used for uniform indexing.

**B1. [Initialize.]** Set $r_j \leftarrow 0$ for $0 \le j \le s$. Set $r_{s+1} \leftarrow 0$. Set $T \leftarrow t$. Compute $M_j = \sum_{i=0}^j m_i$ for $0 \le j \le s$.

For $j$ from $s$ down to $0$, set

$$r_j \leftarrow \max(0,\, T - M_{j-1}),$$

then update $T \leftarrow T - r_j$.

**B2. [Visit.]** Visit $(r_s,\dots,r_0)$.

**B3. [Find $j$.]** Set $j \leftarrow 0$. While $j \le s$ and

$$r_j = U_j,$$

set $j \leftarrow j+1$.

**B4. [Done?]** If $j > s$, terminate.

**B5. [Increase $r_j$.]** Set $T \leftarrow T + r_j$. Replace $r_j \leftarrow r_j + 1$. Then for $k = j-1, j-2, \dots, 0$, set

$$r_k \leftarrow L_k(T),$$

where $L_k(T) = \max(0,, T - M_{k-1})$ computed with current remaining sum $T$, and update $T \leftarrow T - r_k$. Return to B2.

Correctness follows from invariants on $T_j$ and feasibility bounds. At each step B3, indices $0,\dots,j-1$ are at their maximal feasible values, so any increment of $r_j$ preserves lexicographic minimality of the suffix. Step B5 restores the minimal feasible completion under the updated remaining sum, ensuring the next lexicographic configuration is produced. Exhaustion occurs exactly when no index can be increased, which is equivalent to $r_j = U_j$ for all $j$, so all bounded compositions are generated once and only once.

This completes the proof. ∎
