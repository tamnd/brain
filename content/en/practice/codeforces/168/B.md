---
title: "CF 168B - Wizards and Minimal Spell"
description: "We are given an entire text file representing a spell. The spell consists of lines, and each line belongs to one of two categories. A line is amplifying if its first non-space character is . For these lines, spaces are meaningful and must remain exactly as they appear."
date: "2026-06-02T16:55:02+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 168
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 114 (Div. 2)"
rating: 1700
weight: 168
solve_time_s: 27
verified: false
draft: false
---

[CF 168B - Wizards and Minimal Spell](https://codeforces.com/problemset/problem/168/B)

**Rating:** 1700  
**Tags:** implementation, strings  
**Solve time:** 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an entire text file representing a spell. The spell consists of lines, and each line belongs to one of two categories.

A line is **amplifying** if its first non-space character is `#`. For these lines, spaces are meaningful and must remain exactly as they appear. Amplifying lines also act as barriers that prevent neighboring lines from being merged across them.

Every other line is **non-amplifying**. In such lines, spaces carry no meaning and must all be removed. Furthermore, newlines between consecutive non-amplifying lines are unnecessary, so those lines must be concatenated together into a single output line.

The task is to delete as many spaces and line breaks as the rules allow while preserving the spell's meaning.

The total input size is at most $2^{20}$ bytes, roughly one million characters. That immediately suggests that any solution must process the text essentially once. An $O(n)$ scan over all characters is easily fast enough, while repeatedly rebuilding large strings could become expensive if implemented careless
