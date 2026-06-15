---
title: "CF 1310B - Double Elimination"
description: "We are given a full double elimination tournament with $2^n$ teams, where the bracket structure is completely fixed."
date: "2026-06-16T06:17:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1310
codeforces_index: "B"
codeforces_contest_name: "VK Cup 2019-2020 - Elimination Round (Engine)"
rating: 2500
weight: 1310
solve_time_s: 59
verified: false
draft: false
---

[CF 1310B - Double Elimination](https://codeforces.com/problemset/problem/1310/B)

**Rating:** 2500  
**Tags:** dp, implementation  
**Solve time:** 59s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a full double elimination tournament with $2^n$ teams, where the bracket structure is completely fixed. Every match is predetermined by seeding rules: teams with close indices meet first, then winners progress upward in the upper bracket, while losers drop into a mirrored lower bracket that eventually produces a challenger for the final.

We are also given a set of $k$ favorite teams. We are allowed to decide the outcome of every match arbitrarily. The goal is to maximize how many matches in the entire tournament involve at least one favorite team.

The important viewpoint is that this is not about who wins, but about how often favorite teams can be kept alive and matched against others, either in upper or lower brackets. Each match contributes 1 if at least one participant is a favorite.

The tournament structure is a full binary tree in the upper bracket combined with a layered mirrored structure in the lower bracket. Every match is fixed by segment splits of team indices, so the entire tournament can be seen as recursively dividing intervals of teams.

The constraints $n \le 17$ imply up to $2^{17} = 131072$ teams. The total number of matches is also $O(2^n)$, so any solution must be roughly linear or near-linear in the number of nodes in this implicit tournament tree.

A naive simulation of all possible outcomes is impossible. Even fixing outcomes greedily per match fails because decisions affect future match structures in both brackets.

A subtle failure case for greedy reasoning occurs when two favorite teams meet early. For example, if two favorites are in the same first-round match, only one match is counted, but careful rearrangement of outcomes might increase total participation in later rounds by controlling where losers drop. Local greedy choices do not capture this global tradeoff.

Another edge case is when there is exactly one favorite team. The optimal strategy is not always to make it win everything, because sending it to the lower bracket can increase the number of matches it participates in due to the structure of the loser's bracket, as
