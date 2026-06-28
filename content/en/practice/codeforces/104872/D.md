---
title: "CF 104872D - a, ab, ba Strings"
description: "We are maintaining a binary string made only of characters a and b, with two operations applied online. The first operation flips a single position, turning a into b or b into a."
date: "2026-06-28T10:25:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104872
codeforces_index: "D"
codeforces_contest_name: "2023-2024 Russia Team Open, High School Programming Contest (VKOSHP XXIV)"
rating: 0
weight: 104872
solve_time_s: 35
verified: false
draft: false
---

[CF 104872D - a, ab, ba Strings](https://codeforces.com/problemset/problem/104872/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are maintaining a binary string made only of characters `a` and `b`, with two operations applied online. The first operation flips a single position, turning `a` into `b` or `b` into `a`. The second operation asks whether a given substring can be completely partitioned into contiguous blocks, where every block is exactly one of three allowed forms: a single character `a`, or a pair `ab`, or a pair `ba`.

So every valid decomposition is a tiling of the substring using tiles of length 1 or 2, but the length 2 tiles are restricted: they must alternate characters.

The key difficulty is that we must answer up to 100,000 updates and 100,000 queries on a string of length up to 100,000, so any solution that rescans a substring per query is immediately too slow. A direct check of each query substring would cost O(n) per query in the worst case, leading to O(nq), which is completely infeasible.

The subtlety is that the allowed tilings are not arbitrary. For example, a substring like `aa` is always valid because it can be split into two single `a` tiles. But `aaa` is also valid. Meanwhile `aba` is valid as `ab | a`, while `aab` is valid as `a | ab`. The real obstruction is when we are forced to place a length-2 tile but the local parity and adjacency constraints conflict.

A naiv
