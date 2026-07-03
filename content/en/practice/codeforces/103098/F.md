---
title: "CF 103098F - Friendship Circles"
description: "Let $X = a{n-1}a{n-2}cdots a0$ be the binary representation of an $(s,t)$-combination, so $sum ai = t$. Write its associated fencepost form as in equation (14), $$X = 0^{qt}1,0^{q{t-1}}1cdots 1,0^{q0},$$ where each $qi ge 0$ and $sum{i=0}^t qi = s$."
date: "2026-07-04T00:37:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103098
codeforces_index: "F"
codeforces_contest_name: "2020-2021 Winter Petrozavodsk Camp, UPC contest"
rating: 0
weight: 103098
solve_time_s: 82
verified: false
draft: false
---

[CF 103098F - Friendship Circles](https://codeforces.com/problemset/problem/103098/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 22s  
**Verified:** no  

## Solution
## Solution

Let $X = a_{n-1}a_{n-2}\cdots a_0$ be the binary representation of an $(s,t)$-combination, so $\sum a_i = t$. Write its associated fencepost form as in equation (14),

$$X = 0^{q_t}1\,0^{q_{t-1}}1\cdots 1\,0^{q_0},$$

where each $q_i \ge 0$ and $\sum_{i=0}^t q_i = s$. The spread of $X$, denoted $X^{\sim}$, is the composition $(q_t,\ldots,q_0)$ extracted from the zero-block lengths between successive 1s.

Dually, write the same binary string in terms of zero-block structure,

$$X = 1^{p_t}0\,1^{p_{t-1}}0\cdots 0\,1^{p_0},$$

with $p_i \ge 1$ and $\sum_{i=0}^t p_i = n+1$. The core of $X$, denoted $X^{\circ}$, is the composition $(p_t,\ldots,p_0)$ determined by the lengths of 1-blocks and boundary adjustments as in equation (10).

Let $X^{+}$ denote bitwise complement, replacing each $0$ by $1$ and each $1$ by $0$. This operation exchanges zero-blocks and one-blocks without changing their lengths.

Applying $+$ to the fencepost representation of $X$ gives

$$X^{+} = 1^{q_t}0\,1^{q_{t-1}}0\cdots 0\,1^{q_0}.$$

The block structure of $X^{+}$ is therefore governed by the same integers $q_t,\ldots,q_0$, but now interpreted as lengths of consecutive 1-blocks separated by single 0s. Converting this representation into the core data uses exactly the same rule as in equation (10), hence the core of $X^{+}$ is

$$(X^{+})^{\circ} = (q_t,\ldots,q_0)^{\circ}.$$

On the other hand, applying $\sim$ to $X^{\circ}$ corresponds to reversing the interpretation from 1-block structure to 0-block structure, since the dual encoding swaps the roles of selected and unselected elements in the underlying $(s,t)$-combination. This operation converts the same sequence of block lengths $(q_t,\ldots,q_0)$ into the spread representation of the transformed configuration.

Thus both constructions extract the same ordered tuple from the same underlying block decomposition of $X$, obtained after exchanging the roles of 0s and 1s. The block-length data is unchanged by complementation, and only its interpretation as spread or core changes.

Therefore the two transformations coincide,

$$X^{\sim +} = X^{\circ \sim}.$$

This completes the proof. ∎
