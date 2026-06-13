---
title: "CF 1190C - Tokitsukaze and Duel"
description: "We are given a binary string representing a line of cards, each showing either 0 or 1. A move consists of choosing exactly k consecutive positions and forcing all of them to become identical, either all 0 or all 1. The rest of the array is unchanged."
date: "2026-06-13T13:05:30+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "games", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1190
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 573 (Div. 1)"
rating: 2300
weight: 1190
solve_time_s: 260
verified: true
draft: false
---

[CF 1190C - Tokitsukaze and Duel](https://codeforces.com/problemset/problem/1190/C)

**Rating:** 2300  
**Tags:** brute force, games, greedy  
**Solve time:** 4m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary string representing a line of cards, each showing either 0 or 1. A move consists of choosing exactly k consecutive positions and forcing all of them to become identical, either all 0 or all 1. The rest of the array is unchanged. Two players alternate moves, starting with Tokitsukaze. Whoever makes a move that results in the entire array becoming uniform immediately wins that game.

The key aspect is that a move is not a flip of individual bits but a repaint of a contiguous segment. The players are assumed to play optimally, so every move is chosen to maximize their own chance of winning and minimize the opponent’s.

The task is to determine whether Tokitsukaze wins, Quailty wins, or whether the game can continue indefinitely (formally, more than 10^9 moves, treated as a draw).

The constraint n ≤ 10^5 immediately rules out any simulation of the game tree. Each move branches over O(nk) possibilities for segments and two color choices, and even a shallow search becomes exponential. The structure of the problem therefore has to collapse into reasoning about global properties of the initial configuration.

A subtle edge case appears when the string is already almost uniform except for a small cluster of opposite bits. For example, if all 1s are contained inside a segment of length k, then Tokitsukaze can repaint that segment and win immediately. A naive strategy that only considers majority color or local patterns fails here because winning depends on whether the minority color is spatially compressible, not on its count.

Another edge case arises when neither player can force immediate completion, but the board can be kept in a state where both players always have a non-winning move available. This produces the “once again” outcome and typically occurs when the configuration is too “spread out” for any k-window repaint to collapse it in a bounded number of steps.

## Approaches

A brute-force approach would explicitly simulate the game. From a given state, we try all O(n) choices of k-segments and both repaint options. After each move we check if the board is uniform and continue recursively. This correctly models optimal play, but the branching factor is already Θ(n), and depth can also be Θ(n), making the state space explosion immediate for n up to 10^5.

The key simplification is to stop thinking about sequences of moves and instead reason about the _compressibility of each color block_. A move can eliminate an entire color only if that color is fully contained inside a chosen segment. This reduces the problem to tracking the leftmost and rightmost occurrences of 0 and 1.

Let the 1s occupy an interval [l1, r1] and the 0s occupy [l0, r0]. The only way to finish in one move is to choose a k-segment that covers all occurrences of one color, then repaint it to the opposite color. This immediately yields a win condition in terms of interval lengths.

If neither color can be fully covered by a k-window, the game becomes about whether a player can force the other into a losing configuration. The critical observation is that the game becomes infinite precisely when no move can strictly reduce the “irreducible span” of both colors in a decisive way, meaning every move can be answered in a way that restores a similarly complex configuration. This happens when both colors are too spread out relative to k, so no player can isolate a full color block.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | O(n) | Too slow |
| Interval Compression (optimal) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Scan the string and record the first and last occurrence of both 0 and 1. This gives two intervals [l0, r0] and [l1, r1]. This step compresses the entire game state into constant-sized information because only extreme positions matter for full elimination.
2. Compute the length of each interval: len0 = r0 − l0 + 1 and len1 = r1 − l1 + 1. These represent how far each color is spread.
3. Check whether Tokitsukaze can win in a single move. This happens if there exists a k-length segment that covers all occurrences of either 0 or 1. In interval terms, this is equivalent to checking if min(len0, len1) ≤ k. If so, Tokitsukaze selects the segment covering that color and repaints it, immediately winning.
4. If immediate win is not possible, determine whether the game can continue indefinitely. This occurs when neither player can force the game into a position where a single k-segment can isolate an entire color, and any move can be countered symmetrically by the opponent.

The structural condition that characterizes this is that both colors are “too wide” relative to k and overlap in such a way that every attempt to compress one side leaves enough structure for the opponent to restore complexity. In this regime, the game never collapses to a uniform state in bounded time.

1. If neither immediate win nor infinite play condition holds, then the second player has a forced win by responding to every Tokitsukaze move with a finishing move in one step.

### Why it works

The invariant is that the only meaningful progress in the game is reducing the minimal interval that contains all occurrences of a color. A move either fully eliminates a color (winning immediately) or does not reduce both intervals sufficiently. When both intervals exceed k and are interleaved in a way that prevents isolation, every move preserves the possibility of reversal, leading to an endless cycle. If that structural symmetry is broken, the second player can always force the configuration back into a position where Tokitsukaze cannot create a winning compression.

## Python Solution

```
PythonRun
```

The implementation compresses the state into the extreme positions of both colors. That is sufficient because any winning move must eliminate an entire color block, which can only happen if that block is fully contained inside a chosen segment. The immediate win check directly encodes this condition.

The remaining logic distinguishes the pathological case where both colors are so widely distributed that no k-segment can isolate structure in a way that forces termination. The check `k * 2 <= n` ensures that there is enough room for repeated non-interfering moves, and the boundary overlap condition ensures both colors persist across the playable region after any local modification.

Care must be taken with indices, since the solution uses 0-based indexing while reasoning about spans implicitly assumes inclusive ranges.

## Worked Examples

### Example 1

Input:

```

```

| Step | l0,r0 | l1,r1 | len0 | len1 | Decision |
| --- | --- | --- | --- | --- | --- |
| initial scan | 0,2 | 1,3 | 3 | 3 | both spans > k |
| immediate win check | - | - | - | - | false |
| infinite check | overlaps not sufficient |  |  |  | false |
| result | - | - | - | - | quailty |

This configuration has both colors spread out, and no length-2 segment contains all occurrences of either color.

### Example 2

Input:

```

```

| Step | l0,r0 | l1,r1 | len0 | len1 | Decision |
| --- | --- | --- | --- | --- | --- |
| initial scan | 3,4 | 0,2 | 2 | 3 | len0 ≤ k |
| immediate win | yes |  |  |  | Tokitsukaze wins |

Here all zeros are contained in a segment of length 2, so Tokitsukaze can repaint that segment to 1 and finish immediately.

These two cases highlight the difference between compressible minority structure and globally spread configurations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single scan to compute extreme positions |
| Space | O(1) | Only four indices are stored |

The solution is optimal for n up to 10^5 because it reduces the game to constant-size interval reasoning, avoiding any simulation of moves.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | tokitsukaze | already uniform handling |
| compressible block | tokitsukaze | interval ≤ k condition |
| alternating | quailty | spread-out failure case |
| k = n | tokitsukaze | full repaint edge case |

## Edge Cases

When the string is already uniform, both intervals collapse to a single point. The immediate win condition triggers because min(len0, len1) becomes zero, reflecting that no action is required to achieve uniformity.

When k equals n, any move overwrites the entire array. The algorithm correctly classifies this as a winning position since the first player can directly force uniformity regardless of initial structure.

When one color appears in a contiguous block shorter than k, that block is fully eliminable in one move. The interval compression captures this exactly, and the condition min(len0, len1) ≤ k ensures correct detection.

When both colors are highly interleaved, both intervals span nearly the full array, and neither can be isolated. The algorithm routes this into the non-terminating or losing branch depending on whether boundary overlap allows sustained play, reflecting the inability to reduce structural complexity in a single move.
