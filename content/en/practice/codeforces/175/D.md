---
title: "CF 175D - Plane of Tanks: Duel"
description: "Two tanks start fighting at time 0. Both fire immediately, then continue firing every dt seconds. Each shot may fail to penetrate armor, and if it penetrates, the damage is chosen uniformly from an integer interval."
date: "2026-06-02T16:56:46+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 175
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 115"
rating: 2400
weight: 175
solve_time_s: 40
verified: false
draft: false
---

[CF 175D - Plane of Tanks: Duel](https://codeforces.com/problemset/problem/175/D)

**Rating:** 2400  
**Tags:** brute force, dp, math, probabilities  
**Solve time:** 40s  
**Verified:** no  

## Solution
## Problem Understanding

Two tanks start fighting at time 0. Both fire immediately, then continue firing every `dt` seconds. Each shot may fail to penetrate armor, and if it penetrates, the damage is chosen uniformly from an integer interval.

A tank is destroyed as soon as its hit points become non-positive. If both tanks fire at the same moment, both shots happen simultaneously. This detail is crucial because if both tanks die from shots fired at the same timestamp, Vasya is still considered the winner.

The input describes Vasya's tank and the enemy tank. For each tank we know its hit points, reload time, damage interval, and probability that its shot fails to penetrate the opponent's armor.

The task is to compute the probability that Vasya eventually wins.

The constraints are surprisingly small. Hit points never exceed 200, reload times never exceed 30, and damage values never exceed 100. These bounds strongly suggest that we should model remaining hit points explicitly. A state space involving both tanks' HP values contains at most about `201 × 201 = 40401` states, which is completely manageable.

The difficult part is the timing. Tanks
