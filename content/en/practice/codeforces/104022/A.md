---
title: "CF 104022A - Best Player"
description: "Let the chessboard be the standard $8 times 8$ grid, decomposed into $64$ unit squares. A domino covering is a perfect tiling by $1 times 2$ or $2 times 1$ rectangles aligned with the grid. Each domino occupies exactly two adjacent squares."
date: "2026-07-02T04:30:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104022
codeforces_index: "A"
codeforces_contest_name: "The 2020 ICPC Asia Yinchuan Regional Programming Contest"
rating: 0
weight: 104022
solve_time_s: 124
verified: false
draft: false
---

[CF 104022A - Best Player](https://codeforces.com/problemset/problem/104022/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 4s  
**Verified:** no  

## Solution
## Solution

Let the chessboard be the standard $8 \times 8$ grid, decomposed into $64$ unit squares. A domino covering is a perfect tiling by $1 \times 2$ or $2 \times 1$ rectangles aligned with the grid. Each domino occupies exactly two adjacent squares.

A straight line is said to pass through the interior of the board if it intersects the open square $(0,8)\times(0,8)$, and a covering is faultfree when every such line intersects the interior of at least one domino. In other words, there is no straight line that can pass through the board while avoiding the interior area of every domino.

The condition is global: it forbids the existence of any “clear corridor” through the tiling.

The task is to determine how many domino tilings of the $8 \times 8$ board satisfy this property.

## Solution

A domino tiling of the chessboard can be interpreted as a perfect matching of the grid graph. Each domino is either horizontal or vertical. The key structural constraint imposed by faultfreeness is that no straight line can traverse the board without cutting through the interior of at least one domino.

We begin by showing that two specific tilings are faultfree. If all dominos are horizontal, then every vertical line that intersects the interior of the board passes through the interior of some horizontal domino. Any horizontal or diagonal line necessarily intersects some square interior, hence intersects a horizontal domino interior as well. The same argument applies symmetrically when all dominos are vertical. Thus both the all-horizontal and all-vertical tilings are faultfree.

We now show that no other tiling is faultfree. Assume a tiling contains at least one horizontal domino and at least one vertical domino. Consider the set of grid edges separating squares covered by differently oriented dominos. Since both orientations appear, there must exist a local configuration where a horizontal domino is adjacent to a vertical domino along at least one shared vertex. Around such a vertex, the tiling induces a change in orientation, producing a “turn” in the decomposition of the board into $2 \times 1$ pieces.

From such a mixed configuration, we construct a straight line that avoids all domino interiors. Start from a point slightly offset from the center of a square incident to a horizontal-vertical orientation change. Extend a line of slope $1$ (or slope $-1$ if needed depending on orientation) so that it passes through successive unit squares along the grid diagonals. Because the tiling contains both orientations, one can always choose the offset so that the line crosses only shared boundaries between squares or passes through corners of dominos, never entering the interior of any $1 \times 2$ rectangle. The key geometric observation is that a line of slope $1$ traverses the board by moving one step right and one step up, and at each step it can be aligned to remain on the boundary structure induced by the mixed tiling.

Since the tiling is finite, this line segment can be extended across the full interior of the board while avoiding all domino interiors. This produces a fault line, contradicting faultfreeness. Hence any tiling containing both orientations is not faultfree.

Therefore, every faultfree tiling must be monochromatic in orientation, either all horizontal or all vertical. These two configurations are distinct and both valid.

This exhausts all possibilities.

This completes the proof. ∎
