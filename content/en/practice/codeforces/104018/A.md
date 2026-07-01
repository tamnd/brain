---
title: "CF 104018A - \u0421\u0443\u043c\u043c\u0430 \u043e\u0441\u0442\u0430\u0442\u043a\u043e\u0432"
description: "A domino tiling of the $8times 8$ board assigns to each unit square a partner square so that every square belongs to exactly one $1times 2$ or $2times 1$ domino. The additional tatami condition forbids any grid vertex where four different dominoes meet."
date: "2026-07-02T04:45:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104018
codeforces_index: "A"
codeforces_contest_name: "2022-2023 ICPC NERC (NEERC), Kyrgyzstan Regional Contest"
rating: 0
weight: 104018
solve_time_s: 122
verified: false
draft: false
---

[CF 104018A - \u0421\u0443\u043c\u043c\u0430 \u043e\u0441\u0442\u0430\u0442\u043a\u043e\u0432](https://codeforces.com/problemset/problem/104018/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 2s  
**Verified:** no  

## Solution
## Solution

A domino tiling of the $8\times 8$ board assigns to each unit square a partner square so that every square belongs to exactly one $1\times 2$ or $2\times 1$ domino. The additional tatami condition forbids any grid vertex where four different dominoes meet. Equivalently, at no interior lattice point are all four incident unit squares covered by four distinct dominoes arranged in alternating orientations. This is the only local configuration that violates the rule, so the problem reduces to describing all domino tilings in which this configuration never appears.

A useful way to read the constraint is to look at how orientation changes propagate. If a vertex is not a forbidden crossing, then around that vertex either all incident dominoes are aligned in a coherent way or the orientation change is forced to be “linear,” meaning it continues in a single direction rather than branching. This removes the possibility of a grid-like interleaving of horizontal and vertical structure. As a consequence, the tiling cannot contain a $2\times 2$ region where both orientations mix in a crossing pattern, and every change from horizontal to vertical structure must propagate along a single monotone interface.

This rigidity forces every tatami domino tiling of a rectangle to decompose into a single monotone separating curve between a horizontal-dominated region and a vertical-dominated region. Once one orientation is chosen, say horizontal, the board is filled by horizontal domino rows except along one staircase-like defect path where the orientation flips to vertical and then continues consistently. The defect path starts on one boundary side, ends on another boundary side, and at each step moves monotonically, never reversing direction, because any reversal would force a forbidden four-domino meeting at the turning vertex.

For an $n\times n$ board this structure is completely determined by three independent choices. First, the global orientation of the background tiling can be chosen in $2$ ways, either horizontal-dominant or vertical-dominant. Second, the starting position of the defect path along the boundary can be chosen in $n$ ways. Third, once the start is fixed, the defect path moves across the grid in $n-1$ steps, and at each step it has exactly two admissible monotone choices, corresponding to shifting the interface one unit in one of two directions while preserving tatami legality. These choices are independent because each local decision only affects the next segment of the interface and never creates a branching configuration.

Hence the number of admissible defect paths is $2^{n-1}$. Multiplying by the $n$ possible starting positions and the $2$ global orientations yields the total number of tatami domino tilings of the $n\times n$ board:

$$2 \cdot n \cdot 2^{n-1} = n\cdot 2^n.$$

For $n=8$ this gives

$$8\cdot 2^8 = 8\cdot 256 = 2048.$$

Thus the number of tatami domino tilings of the $8\times 8$ chessboard is

$$\boxed{2048}.$$

## Notes

The essential structural fact is that forbidding four dominoes at a vertex eliminates any possibility of a two-dimensional interaction of orientations. What remains is a one-dimensional interface whose combinatorics reduce to a binary walk across the board, and the counting becomes the enumeration of its starting position and its binary evolution.
