---
title: "CF 105055N - Nim?"
description: "We start with a pile of stones containing exactly $A cdot B$ stones. Two players alternate moves, with Machado going first. Machado can change the pile by either adding or removing any positive multiple of $A$ or any positive multiple of $B$."
date: "2026-06-28T00:26:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105055
codeforces_index: "N"
codeforces_contest_name: "UDESC Selection Contest 2023-2"
rating: 0
weight: 105055
solve_time_s: 37
verified: false
draft: false
---

[CF 105055N - Nim?](https://codeforces.com/problemset/problem/105055/N)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** no  

## Solution
## Problem Understanding

We start with a pile of stones containing exactly $A \cdot B$ stones. Two players alternate moves, with Machado going first.

Machado can change the pile by either adding or removing any positive multiple of $A$ or any positive multiple of $B$. Cartinha, on the other hand, can only add or remove multiples of $A \cdot B$. The game ends immediately if the pile ever becomes exactly zero, which is a losing condition for Machado. Machado also loses if play continues indefinitely without ever reaching a winning state. Machado wins as soon as the number of stones becomes a positive value in the range $[1, K]$.

The question is whether Machado can force a win starting from $A \cdot B$, assuming Cartinha plays optimally to prevent it.

The constraints allow $A, B, K \le 10^7$, so any solution must run in constant or logarithmic time. Anything involving simulation of moves or graph exploration over states is impossible, since the state space is unbounded and transitions allow arbitrarily large jumps.

A subtle edge case appears when the arithmetic structure of reachable states restricts which values can ever be reached. For example, if $A = B = 2$, then every move preserves evenness of the pile, so reaching an odd target like $1$ is impossible regardless of strategy. Another case is when $A = 6, B = 5, K = 20$: even though the starting value is large, Machado can still navigate the reachable arithmetic space down to a small winning interval.

These examples suggest the problem is not about game strategy in a positional sense, but about which integers are reachable under linear combinations of $A$ and $B$.

## Approaches

A direct simulation of the game would treat each pile size as a node in a state graph, and each move as an edge. Machado’s moves generate transitions of the form $x \to x \pm kA$ or $x \to x \pm kB$, while Cartinha introduces jumps of size $A \cdot B$. This creates an infinite graph with unbounded branching, and even exploring a small neighborhood around the start can immediately reach very large values. This makes brute force completely infeasible.

The key observation is that Machado’s moves generate all integer combinations of $A$ and $B$. Any reachable difference between two states is therefore a multiple of $\gcd(A, B)$. This means the entire game is confined to one residue class modulo $g = \gcd(A, B)$. No move by either player can ever change that invariant.

Once we reduce the problem to this arithmetic constraint, the game structure collapses. Every reachable pile size is a multiple of $g$, and the smallest positive value Machado can ever reach is exactly $g$. Cartinha’s ability to add or subtract multiples of (A \cdot
