---
title: "CF 104871H - Human Resources"
description: "We are given a company hierarchy that forms a rooted tree. Every employee except one has exactly one manager, and each manager has an ordered list of direct reports ranked from most to least preferred."
date: "2026-06-28T10:38:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104871
codeforces_index: "H"
codeforces_contest_name: "2023-2024 ICPC Central Europe Regional Contest (CERC 23)"
rating: 0
weight: 104871
solve_time_s: 39
verified: false
draft: false
---

[CF 104871H - Human Resources](https://codeforces.com/problemset/problem/104871/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a company hierarchy that forms a rooted tree. Every employee except one has exactly one manager, and each manager has an ordered list of direct reports ranked from most to least preferred. The input describes this tree either in a structured textual form (ENCODE mode) or as a compact binary string plus a list of employee names (DECODE mode).

In ENCODE mode, the task is to compress the entire hierarchy into two parts. First, we must output all employee names in any order. Second, we must produce a binary string that encodes the entire tree structure, including both parent-child relationships and the order of children for every manager.

In DECODE mode, we are given exactly that output: the unordered list of nam
