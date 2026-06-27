---
title: "CF 105584G - Two Sets of Cards"
description: "We are given several independent datasets. Each dataset describes a game setup with a number of participants, and each participant reports a single integer which is the sum of two hidden values."
date: "2026-06-27T00:48:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105584
codeforces_index: "G"
codeforces_contest_name: "The 2024 ICPC Asia Japan Online First-Round Contest"
rating: 0
weight: 105584
solve_time_s: 27
verified: false
draft: false
---

[CF 105584G - Two Sets of Cards](https://codeforces.com/problemset/problem/105584/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several independent datasets. Each dataset describes a game setup with a number of participants, and each participant reports a single integer which is the sum of two hidden values.

Behind the scenes, there are two decks of cards, red and blue, each containing exactly one integer per participant. Both decks contain the same multiset of integers, but the pairing between red and blue cards is unknown. Each participant receives one red card and one blue card, and they report the sum of the two values they received.

The task is to determine whether there exists any assignment of integers to red and blue cards such that all reported sums are consistent with some pairing of two identical multisets. If it is possible, we must construct one such assignment of pairs. Otherwise, we report impossibility.

The key hidden structure is that we are splitting a multiset into two identical copies, then pairing elements position-wise after a permutation, and only the pairwise sums are observed.

The constraint is small per dataset, with at most around 70 participants. This immediately rules out exponential enumeration over all permutations of assignments, since that would be on the order of 70 factorial possibilities, far beyond any feasible computation. Even O(n^4) brute force constructions over pairings would already be too large if repeated across multiple datasets.

The main subtlety is that we are not free to assign arbitrary pairs matching sums independently. The same value must appear exactly twice overall, once in each deck, which couples all choices globally.

A common failure case for naive greedy pairing is when local sum matching works but global multiset consistency fails.

For example, suppose we greedily pick a value for the first participant and try to force its complement in the second deck independently. We may later discover that we run out of copies of a needed value. This happens in cases like:

Input:

n = 3

s = [0, 0, 0]

A naive approach might assign (0,0) to each participant, but this assumes we can reuse the same multiset freely without tracking global consistency. That happens to work here, but in more structured cases such as:

Input:

n = 3

s = [1, 1, 2]

a greedy attempt might assign (0,1), (0,1), (1,1) which breaks multiset equality.

So the core difficulty is global consistency of two identical multisets under pairing constraints.

## Approaches

The brute-force idea is to assign values to both decks explicitly. Since each participant contributes a pair (a[i], b[i]) and both multisets must match, we could try generating all possible multisets of size n and then check if a pairing exists that produces the given sums. This would involve choosing n integers, duplicating them, and then matching them in pairs consistent with sums.

The number of possible multisets of integers in the allowed range is astronomically large. Even restricting values to a bounded range derived from sums does not help, since values can be negative and up to 10^9. This makes enumeration impossible.

The key insight is to reverse the viewpoint. Instead of thinking about constructing two multisets and then pairing them, we directly construct pairs (a[i], b[i]) while ensuring that th
