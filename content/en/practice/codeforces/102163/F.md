---
title: "CF 102163F - Research projects"
description: "There are (N) students in total, and (K) of them are already assigned to existing research projects. The remaining (N-K) students still need to be placed into newly created projects. A new project can contain between 1 and 6 students."
date: "2026-08-24T02:58:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102163
codeforces_index: "F"
codeforces_contest_name: "NCD 2019"
rating: 0
weight: 102163
solve_time_s: 1035
verified: false
draft: false
---

[CF 102163F - Research projects](https://codeforces.com/problemset/problem/102163/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 17m 15s  
**Verified:** no  

## Solution
## Problem Understanding

There are (N) students in total, and (K) of them are already assigned to existing research projects. The remaining (N-K) students still need to be placed into newly created projects.

A new project can contain between 1 and 6 students. Since every student can belong to only one project, the task is to divide all (N-K) unassigned students into groups of size at most 6 while using as few groups as possible.

The key observation is that a project can hold at most 6 students, so every new project can accommodate at most six of the students who are still unassigned. The answer is consequently the smallest number of groups of capacity 6 that can contain (N-K) students.

The values of (N) and (K) can be as large as (10^{18}). An algorithm that processes students individually could require up to (10^{18}) iterations, which is far beyond what can run within a 1 second limit. We need a constant-time arithmetic solution for each test case. Python integers also handle values of this size directly, so there is no overflow issue
