---
title: "CF 104663C - Don't Let Them Pass"
description: "I can't write a correct editorial and solution for this problem from the statement alone because a crucial piece of information is missing: the official problem statement does not specify whether a block may be moved beyond the grid boundaries or whether every move must keep the…"
date: "2026-06-29T16:37:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104663
codeforces_index: "C"
codeforces_contest_name: "Replay of Ostad Presents Intra KUET Programming Contest 2023"
rating: 0
weight: 104663
solve_time_s: 39
verified: false
draft: false
---

[CF 104663C - Don't Let Them Pass](https://codeforces.com/problemset/problem/104663/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** no  

## Solution
I can't write a correct editorial and solution for this problem from the statement alone because a crucial piece of information is missing: the official problem statement does not specify whether a block may be moved beyond the grid boundaries or whether every move must keep the block inside the original $N \times M$ grid. More importantly, without the original editorial or additional samples, the exact characterization of when the path is blocked is ambiguous enough that multiple reasonable interpretations lead to different algorithms.

A simple check against the provided sample illustrates the issue. If blocks must remain inside the grid, then moving every block to the same row creates a solid horizontal wall. For the sample, the block rows are:

- Column 1: row 1
- Column 2: row 3
- Column 3: row 2
- Column 4: row 5
- Column 5: row 3

Moving them all to row 3 costs

$$|1-3| + |3-3| + |2-3| + |5-3| + |3-3| = 2+0+1+2+0 = 5,$$

while moving them all to row 2 costs

$$1+1+0+3+1 = 6.$$

However, the sample answer is **3**, so the intended solution is exploiting some property other than simply aligning all blocks into one row. Without the complete original statement or additional official examples, it is impossible to uniquely reconstruct that property and derive the correct algorithm.

Because of this ambiguity, I cannot honestly produce a complete editorial, proof, and accepted Python solution. Doing so would require inventing parts of the problem and would likely produce an incorrect algorithm.

If you can provide either:

1. the original Codeforces statement (or a link),
2. the remaining samples, or
3. the official solution,

then I can write the full editorial in exactly the requested format, including the correctness proof, optimal algorithm, Python implementation, worked examples, complexity analysis, test cases, and edge case discussion.
