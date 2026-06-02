---
title: "CF 154B - Colliders"
description: "We manage a set of colliders numbered from 1 to $n$. Initially every collider is turned off. We then receive a sequence of commands. A command can either try to activate a collider or deactivate it."
date: "2026-06-02T16:44:24+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 154
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 109 (Div. 1)"
rating: 1600
weight: 154
solve_time_s: 32
verified: false
draft: false
---

[CF 154B - Colliders](https://codeforces.com/problemset/problem/154/B)

**Rating:** 1600  
**Tags:** math, number theory  
**Solve time:** 32s  
**Verified:** no  

## Solution
## Problem Understanding

We manage a set of colliders numbered from 1 to $n$. Initially every collider is turned off. We then receive a sequence of commands. A command can either try to activate a collider or deactivate it.

The safety rule is the only thing that matters: all active collider numbers must be pairwise coprime. When we try to activate collider $x$, activation is allowed only if every currently active collider has greatest common divisor equal to 1 with $x$. If some active collider shares a prime factor with $x$, activation must be rejected and we must report one conflicting collider. If the collider is already active, we report "Already on".

For deactivation, the behavior is simpler. If the collider is currently active, we remove it and print "Success". Otherwise we print "Already off".

The constraints are large enough that a straightforward simulation is not sufficient. Both $n$ and the number of operations $m$ can reach $10^5$. A solution that compares a newly activated collider against all active colliders would require up to $10^5$ gcd computations per operation. In the worst case this becomes roughly $10^{10}$ operations, which is far beyond what fits in a two second time limit.

The key observation is that conflicts arise because two
