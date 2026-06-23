---
title: "CF 105292C - Crystal Mining"
description: "I cannot honestly produce a correct editorial yet because the statement we have is incomplete. The “Crystal Mining” problem page we can retrieve shows only a partial and partially corrupted statement: we know there is a hexagon-shaped grid of side length $N$, and each cell…"
date: "2026-06-23T14:34:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105292
codeforces_index: "C"
codeforces_contest_name: "National Taiwan University Class Preliminary 2024"
rating: 0
weight: 105292
solve_time_s: 40
verified: false
draft: false
---

[CF 105292C - Crystal Mining](https://codeforces.com/problemset/problem/105292/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** no  

## Solution
I cannot honestly produce a correct editorial yet because the statement we have is incomplete.

The “Crystal Mining” problem page we can retrieve shows only a partial and partially corrupted statement: we know there is a hexagon-shaped grid of side length $N$, and each cell contains one of up to 999 types of values. For every cell considered as a potential center, we are asked to output the side length of the largest centered hexagon in which all values are identical, and the output must be printed in the same triangular/hexagonal layout as the input grid .

However, the crucial missing part is the exact definition of the hexagon coordinates, indexing scheme, and how “side length $k$” translates into which cells are included. The samples suggest a diamond-like triangular lattice (not a square grid), but without the original coordinate rules (offset pattern per row, bounds of expansion), any algorithmic reasoning would risk being wrong or misleading.

A correct Codeforces editorial depends heavily on those geometric details. For example, whether neighbors are in 6 directions (true hex grid), or whether the input is a skewed 2D array encoding hex rows, completely changes the DP transitions and complexity.

If you paste the full original statement (especially the part defining how cells expand for a side length and how rows are structured), I can write the full editorial in the exact format you requested, including a clean DP derivation and implementation.

Right now, anything more would be guesswork rather than a faithful solution explanation.
