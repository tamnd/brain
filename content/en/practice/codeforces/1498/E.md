---
title: "CF 1498E - Two Houses"
description: "We are given a city with $n$ houses, where for each pair of houses there is exactly one directed road connecting them, either from the first to the second or vice versa. The input does not specify the directions of these roads."
date: "2026-06-10T21:38:33+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "graphs", "greedy", "interactive", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1498
codeforces_index: "E"
codeforces_contest_name: "CodeCraft-21 and Codeforces Round 711 (Div. 2)"
rating: 2200
weight: 1498
solve_time_s: 160
verified: false
draft: false
---

[CF 1498E - Two Houses](https://codeforces.com/problemset/problem/1498/E)

**Rating:** 2200  
**Tags:** brute force, graphs, greedy, interactive, sortings  
**Solve time:** 2m 40s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a city with $n$ houses, where for each pair of houses there is exactly one directed road connecting them, either from the first to the second or vice versa. The input does not specify the directions of these roads. Instead, we are given an array $k$ where $k_i$ is the number of roads leading into house $i$.

We are asked to find a pair of houses $A$ and $B$ such that $A$ and $B$ are bi-reachable, meaning each can reach the other through some path, and among all such pairs, we want the one maximizing $|k_A - k_B|$. If no such pair exists, we should report $(0, 0)$.

The problem is interactive. We can query whether one house can reach another, but once the judge responds "Yes" to any query, we must stop asking queries and output our answer. There is no upper limit on queries, but the queries must be unique and formatted correctly.

T
