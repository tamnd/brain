---
title: "CF 105204A - \u0420\u0430\u0437\u0431\u0438\u0432\u0430\u0435\u043c \u043b\u0430\u0433\u0435\u0440\u044c"
description: "We are given three types of participants who must be placed into identical tents, each tent having capacity for up to three people. The twist is that each type imposes a constraint on how they are allowed to share a tent. Introverts insist on being alone in their tent."
date: "2026-06-27T02:41:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105204
codeforces_index: "A"
codeforces_contest_name: "\u0412\u041a\u041e\u0428\u041f.Junior 2024"
rating: 0
weight: 105204
solve_time_s: 50
verified: false
draft: false
---

[CF 105204A - \u0420\u0430\u0437\u0431\u0438\u0432\u0430\u0435\u043c \u043b\u0430\u0433\u0435\u0440\u044c](https://codeforces.com/problemset/problem/105204/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** no  

## Solution
## Problem Understanding

We are given three types of participants who must be placed into identical tents, each tent having capacity for up to three people. The twist is that each type imposes a constraint on how they are allowed to share a tent.

Introverts insist on being alone in their tent. They still occupy a full tent of capacity three, but no one else can be placed with them. Extroverts require the opposite extreme: every extrovert must be in a tent with exactly two other people, meaning every tent containing any extrovert must be completely filled with three people. Universals are flexible and can be placed in any configuration, alone or alongside others, as long as no other constraint is violated.

The task is to determine the minimum number of tents needed to accommodate everyone while respecting all constraints, or decide that no valid arrangement exists.

The constraints allow counts up to 10^9, so any solution must run in constant time per test case. Any approach involving searching over distributions of people into tents or trying combinations explicitly would be far too slow.

A few situations are easy to get wrong if approached greedily without structure.

If there are no universals and the number of extroverts is not divisible by three, for example input `0 2 0`, we cannot form a full tent for the remaining two extroverts, so the answer is impossible. A naive solution that simply computes `ceil(b / 3)` would incorrectly claim feasibility.

Another failure case appears when universals are barely insufficient to complete the final extrovert group. For example `0 1 1` cannot work, because the single extrovert needs two more people to form a valid tent, but only one universal exists.

The core difficulty is that extroverts impose strict “full group of three” constraints, while introverts impose strict “no sharing” constraints, and universals act as flexible padding that must be carefully allocated.

## Approaches

A brute-force interpretation would try t
