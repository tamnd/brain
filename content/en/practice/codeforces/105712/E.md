---
title: "CF 105712E - Combination Lock"
description: "We are given two strings of equal length representing a combination lock with digit dials. The first string is the current configuration of the lock, and the second string is the target configuration we want to reach."
date: "2026-06-26T07:56:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105712
codeforces_index: "E"
codeforces_contest_name: "Rutgers University Programming Contest Fall 2024"
rating: 0
weight: 105712
solve_time_s: 22
verified: false
draft: false
---

[CF 105712E - Combination Lock](https://codeforces.com/problemset/problem/105712/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two strings of equal length representing a combination lock with digit dials. The first string is the current configuration of the lock, and the second string is the target configuration we want to reach.

Each position is an independent dial that can be rotated forward or backward in a circular manner, meaning digit 9 wraps around to 0 and 0 wraps around to 9. In one move, we choose a single dial and rotate it any number of steps in either direction until it reaches a desired digit. The cost of adjusting a dial is the minimum number of single-step rotations needed to transform its current digit into the target digit.

The task is to compute the minimum total number of such unit rotations across all positions to transform the initial configuration into the tar
