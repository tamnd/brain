---
title: "CF 104279O - \u722c\u5854"
description: "Let $S={1,dots,m}$ denote the selector variables and $T={m+1,dots,m+2^m}$ the data variables of the multiplexer $Mm$. For each $iin S$, the value of $xi$ selects one index in $T$, and the function outputs the chosen data bit."
date: "2026-07-01T21:16:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104279
codeforces_index: "O"
codeforces_contest_name: "21st UESTC Programming Contest - Preliminary"
rating: 0
weight: 104279
solve_time_s: 129
verified: false
draft: false
---

[CF 104279O - \u722c\u5854](https://codeforces.com/problemset/problem/104279/O)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 9s  
**Verified:** no  

## Solution
## Solution

Let $S={1,\dots,m}$ denote the selector variables and $T={m+1,\dots,m+2^m}$ the data variables of the multiplexer $M_m$. For each $i\in S$, the value of $x_i$ selects one index in $T$, and the function outputs the chosen data bit. The Boolean structure depends only on the induced mapping from $S$ to $T$.

Let $\pi$ be a permutation of $S\cup T$. Write $\pi=(\pi_1,\dots,\pi_{m+2^m})$ and define

$$S_k=\{\pi_1,\dots,\pi_k\}\cap S,\qquad T_k=\{\pi_1,\dots,\pi_k\}\cap T.$$

Let $s_k=|S_k|$ and $t_k=|T_k|$. The state of the BDD construction after processing the first $k$ variables is determined by the partition of remaining selector bits, since each remaining selector bit still ranges over two branches, while each remaining data bit contributes a terminal constant once its addressing pattern is fixed.

For a partial assignment to the first $k$ variables, the subfunction still depends on some unprocessed selector variable if and only if $s_k<m$. In that case, both LO and HI branches at level $k$ remain nonterminal and correspond to distinct subfunctions, since at least one selector bit has not yet been resolved and therefore the selected index in $T$ is not fixed.

Once $s_k=m$, all selector variables have been exposed. The function reduces to a single data variable $x_j$ with $j\in T$, where $j$ is determined by the full assignment to $S$. From that point onward, each remaining variable in $T$ contributes only a binary decision on a fixed leaf, and no further dependence on earlier structure arises.

Hence the bead condition from Section 7.1.4 applies as follows: a node at level $k$ is a branch node if and only if the corresponding subfunction depends on the next variable, which occurs exactly while $s_k<m$. After the last selector appears, no new beads corresponding to selector structure occur.

Therefore the profile of $M^\pi_m$ is determined entirely by the positions of selector variables in $\pi$. For each $k$ with $s_k<m$, the contribution to the profile is $1$, since the subfunction at that level still distinguishes LO and HI through unresolved selection. For each $k$ with $s_k=m$, no further selector-driven branching occurs, and subsequent structure is a binary tree over the remaining data variables.

Thus the profile is the sequence

$$\mathrm{prof}(k)=
\begin{cases}
1, & s_k<m,\\
0, & s_k=m,
\end{cases}$$

interpreted at selector-resolution levels, with the transition point determined by the last occurrence of a selector variable in $\pi$.

For the quasi-profile, each data variable in $T$ acts only after the selector path has determined a unique index. When $s_k<m$, each encountered data variable does not resolve the function but duplicates the unresolved selection structure across both branches, producing no new bead at that level. When $s_k=m$, each data variable contributes exactly one binary decision node corresponding to the final selected leaf, so each such step contributes one unit to the quasi-profile.

Hence the quasi-profile is

$$\mathrm{qprof}(k)=
\begin{cases}
0, & s_k<m,\\
1, & s_k=m.
\end{cases}$$

Equivalently, if $k_1<\cdots<k_m$ are the positions of the selector variables in $\pi$, then the profile has value $1$ for all levels $k<k_m$, and the quasi-profile has value $1$ precisely on levels $k\ge k_m$ corresponding to traversal of the remaining $2^m$ data bits after full selection is resolved.

This completes the determination of the profile and quasi-profile for $M^\pi_m$. ∎
