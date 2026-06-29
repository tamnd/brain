---
title: "CF 104637A - Red and Blue Beans"
description: "We are given two piles of indistinguishable items, red beans and blue beans. In each test case we must decide whether it is possible to split all beans into several groups, where each group contains both colors, and within every group the difference between the number of red and…"
date: "2026-06-29T16:58:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104637
codeforces_index: "A"
codeforces_contest_name: "\u041c\u0438\u0441\u0438\u0441 2023 \u043e\u0441\u0435\u043d\u044c - \u0431\u0430\u0437\u043e\u0432\u0430\u044f \u043c\u0430\u0442\u0435\u043c\u0430\u0442\u0438\u043a\u0430, \u0443\u0441\u043b\u043e\u0432\u0438\u044f, \u0446\u0438\u043a\u043b\u044b"
rating: 0
weight: 104637
solve_time_s: 30
verified: false
draft: false
---

[CF 104637A - Red and Blue Beans](https://codeforces.com/problemset/problem/104637/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two piles of indistinguishable items, red beans and blue beans. In each test case we must decide whether it is possible to split all beans into several groups, where each group contains both colors, and within every group the difference between the number of red and blue beans does not exceed a fixed threshold.

Formally, every packet must contain at least one red and one blue bean, and if a packet contains $r_i$ red and $b_i$ blue beans, then $|r_i - b_i| \le d$. All beans must be assigned to packets with no leftovers.

The constraints allow up to $10^9$ beans of each color and up to $1000$ test cases, so any solution must be constant time per test case. Any approach that tries to construct packets explicitly or simulate distributions will fail immediately because the number of beans is far too large.

A subtle failure case appears when one color is significantly larger than the other. For example, if $r = 6, b = 1, d = 4$, one might try to put all beans in one packet, but that violates the difference condition since $|6 - 1| = 5 > 4$. Splitting into multiple packets does not help because every packet must contain at least one of each color, and the total imbalance is conserved across all packets.

Another edge case is when $d = 0$. In that case every packet must have exactly equal numbers of red and blue beans. This immediately forces the total counts to be equal as well; otherwise some imbalance will remain unresolvable.

The key observation is that packets do not change the global difference between red and blue totals. Each packet contributes a local difference bounded by $d$, but since every packet must contain at least one of each color, the total number of packets is constrained by the smaller pile. This leads to a simple inequality condition on the global counts.

## Approaches

A brute-force idea would try to explicitly construct packets. We could repeatedly form a valid packet by choosing some $r_i \ge 1$ and $b_i \ge 1$ such that $|r_i - b_i| \le d$, subtracting from the totals until no beans remain. This quickly becomes ambiguous because there are many valid choices at each step, and exploring all possibilities leads to exponential branching. Even a greedy construction is not reliable because early choices can block feasibility later.

The key structural simplification comes from observing what actually limits feasibility. Every packet must contain at least one red and one blue bean, so if we form $k$ packets, then we must have $k \le r$ and $k \le b$. Thus $k \le \min(r,b)$. Also, distributing beans across packets cannot reduce the total imbalance $r-b$; it is just partitioned across packets. The worst imbalance in any packet is at least the average imbalance spread across packets, which is $\frac{|r-b|}{k}$. Since each packet allows at most $d$, we need

$$\frac{|r-b|}{k} \le d.$$

To make this as permissive as possible, we maximize $k$, so we set $k = \min(r,b)$. This gives the necessary and sufficient condition:

$$|r-b| \le d \cdot \min(r,b).$$

This condition is also sufficient because we can always distribute beans in a balanced way, giving each packet at least one of the sma
