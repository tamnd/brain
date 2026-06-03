---
title: "CF 200A - Cinema"
description: "We are given a theater with n rows and m seats per row, forming an n × m grid. A line of k people is waiting to buy tickets. Each person has a preferred seat, represented as coordinates (x, y). When a person reaches the box office, they attempt to take their preferred seat."
date: "2026-06-03T16:29:32+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 200
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 126 (Div. 2)"
rating: 2400
weight: 200
solve_time_s: 37
verified: false
draft: false
---

[CF 200A - Cinema](https://codeforces.com/problemset/problem/200/A)

**Rating:** 2400  
**Tags:** brute force, data structures  
**Solve time:** 37s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a theater with `n` rows and `m` seats per row, forming an `n × m` grid. A line of `k` people is waiting to buy tickets. Each person has a preferred seat, represented as coordinates `(x, y)`. When a person reaches the box office, they attempt to take their preferred seat. If it is already occupied, they must choose an alternative empty seat that is closest in Manhattan distance to their original choice. If multiple empty seats share the same minimal distance, the person chooses the one with the smallest row number, and if still tied, the smallest column number. Our goal is to assign each person an actual seat according to this procedure.

The constraints imply a fairly large seating area of up to `2000 × 2000 = 4,000,000` seats, while the number of people is capped at `105`. A naive algorithm that scans all seats for each person could take `O(k * n * m)` operations, potentially exceeding 10^11 operations, which is far too slow for a 2-second time limit. This observation rules out brute-force search over the entire seating grid.

Edge cases to consider include multiple people choosing the same seat at the front of the line, people whose nearest empty seat is far away, and situations
