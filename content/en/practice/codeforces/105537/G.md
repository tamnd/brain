---
title: "CF 105537G - Game of Annihilation"
description: "We are given a very large one dimensional board that extends infinitely to the right. On some of its cells, there are stacks of red and blue chips. Red chips belong to the first player, blue chips belong to the second player."
date: "2026-06-27T00:59:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105537
codeforces_index: "G"
codeforces_contest_name: "2024-2025 ICPC NERC (NEERC), North-Western Russia Regional Contest (Northern Subregionals)"
rating: 0
weight: 105537
solve_time_s: 26
verified: false
draft: false
---

[CF 105537G - Game of Annihilation](https://codeforces.com/problemset/problem/105537/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 26s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a very large one dimensional board that extends infinitely to the right. On some of its cells, there are stacks of red and blue chips. Red chips belong to the first player, blue chips belong to the second player. Multiple chips of the same color can sit in the same cell, but initially each occupied cell contains chips of only one color.

The players alternate moves. On a turn, a player either does nothing or picks one of their chips and moves it one step left or right. If the destination cell already contains at least one opponent chip, both sides immediately lose exactly one chip there, effectively canceling a pair. If it contains only their own chips or is empty, the chip simply joins that cell.

A player loses immediately once they run out of chips. If both eventually run out, the game is a draw. If play continues for an extremely long time without termination, it is also considered a draw.

The task is to determine the outcome under perfect play, and if the first player can force a win or a draw/win scenario, also output one valid first move that begins an optimal strategy.

The input describes only non empty cells as pairs of position, number of chips, and color. The positions are up to 10^6, while total chips across all cells can be up to 10^6 per test case scale. This immediately suggests that any solution must be at most linear in the number of occupied cells, because any attempt to simulate chip movements step by step would require time proportional to the number of moves, which can be quadratic or worse.

A naive simulation of alternating optimal play is impossible. Even tracking each chip individually leads to worst case movement counts proportional to distances between far apart cells times number of chips, which easily exceeds 10^12 operations.

A subtle edge case arises when chips are heavily unbalanced in one region. For example, a single red chip far to the right of many blue chips creates long interaction chains. A naive greedy “always move toward nearest enemy” approach can fail because it ignores cancellation dynamics where multiple chips effectively annihilate in bulk rather than one by one.

Another important edge case is when all chips of one color are clustered far from the other color. Even though interaction seems impossible locally, optimal play still allows waiting, skipping turns, and repositioning, so simplistic “distance parity” reasoning is insufficient.

## Approaches

A direct brute force model
