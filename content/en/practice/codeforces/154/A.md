---
title: "CF 154A - Hometask"
description: "We are given a string of lowercase letters and a collection of forbidden letter pairs. Each forbidden pair contains two distinct letters, and if a pair (a, b) is forbidden then both \"ab\" and \"ba\" are forbidden as adjacent characters. We may delete any characters from the string."
date: "2026-06-02T16:49:09+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 154
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 109 (Div. 1)"
rating: 1600
weight: 154
solve_time_s: 30
verified: false
draft: false
---

[CF 154A - Hometask](https://codeforces.com/problemset/problem/154/A)

**Rating:** 1600  
**Tags:** greedy  
**Solve time:** 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string of lowercase letters and a collection of forbidden letter pairs. Each forbidden pair contains two distinct letters, and if a pair `(a, b)` is forbidden then both `"ab"` and `"ba"` are forbidden as adjacent characters.

We may delete any characters from the string. After deletions, the remaining characters close up, so characters that were not originally adjacent may become neighbors. Our goal is to remove as few characters as possible so that no forbidden pair appears among adjacent characters in the final string.

The string length is at most `100000`, while there are at most `13` forbidden pairs. A quadratic or dynamic programming solution over all positions would be too expensive. With `n = 100000`, even `O(n²)` means about `10^10` operations, which is completely infeasible. We need something close to linear time.

The unusual restriction is that every letter belongs to at most one forbidden p
