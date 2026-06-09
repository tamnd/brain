---
title: "CF 1860C - Game on Permutation"
description: "We are given a permutation and a game played on its positions. The chip starts nowhere. Alice begins by choosing any position and placing the chip there. After that, players alternate moving the chip."
date: "2026-06-09T00:22:08+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "games", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1860
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 153 (Rated for Div. 2)"
rating: 1400
weight: 1860
solve_time_s: 116
verified: false
draft: false
---

[CF 1860C - Game on Permutation](https://codeforces.com/problemset/problem/1860/C)

**Rating:** 1400  
**Tags:** data structures, dp, games, greedy  
**Solve time:** 1m 56s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation and a game played on its positions.

The chip starts nowhere. Alice begins by choosing any position and placing the chip there. After that, players alternate moving the chip. From position `i`, the chip may move only to a position `j` such that `j < i` and `p[j] < p[i]`. In other words, every move goes left and also goes to a strictly smaller value.

The unusual part of the game is the winning condition. If a player cannot make a move, that player wins immediately. This is the opposite of the standard normal-play rule.

For every position of the permutation, we must determine whether choosing that position as the initial placement guarantees a win for Alice regardless of Bob's decisions. Such positions are called lucky. The answer is the number of lucky positions.

The permutation size is up to `3 · 10^5` across all test cases. Any solution that analyzes the game graph separately from every starting position is far too slow. Since the total input size is only a few hundred thousand elements, we need something close to linear or `O(n log n)`.

A subtle point is the reversed winning condition. In ordinary impartial games, terminal positions are losing because the current player cannot move. Here terminal positions are winning because being unable to move immediately ends the game in your favor. Re
