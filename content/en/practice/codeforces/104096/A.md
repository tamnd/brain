---
title: "CF 104096A - \u041f\u0440\u0430\u0437\u0434\u043d\u0438\u0447\u043d\u044b\u0439 \u0442\u043e\u0440\u0442"
description: "Let $Pm$ denote the Boolean predicate that encodes whether a length-$m$ assignment represents a valid permutation of ${1,dots,m}$."
date: "2026-07-02T02:16:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104096
codeforces_index: "A"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428, \u041a\u0440\u0430\u0441\u043d\u043e\u0434\u0430\u0440\u0441\u043a\u0438\u0439 \u043a\u0440\u0430\u0439, 2022"
rating: 0
weight: 104096
solve_time_s: 57
verified: false
draft: false
---

[CF 104096A - \u041f\u0440\u0430\u0437\u0434\u043d\u0438\u0447\u043d\u044b\u0439 \u0442\u043e\u0440\u0442](https://codeforces.com/problemset/problem/104096/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** no  

## Solution
## Solution

Let $P_m$ denote the Boolean predicate that encodes whether a length-$m$ assignment represents a valid permutation of ${1,\dots,m}$. In a standard encoding, each position $i \in {1,\dots,m}$ selects exactly one value in ${1,\dots,m}$, and validity means no value is used twice and no position is left without a choice. Equivalently, the structure underlying $P_m$ is a perfect matching between $m$ left vertices (positions) and $m$ right vertices (values), where each variable represents the inclusion of a possible pair.

In a BDD or ZDD built with the natural level ordering by positions, a node at level $k$ represents the state of all partial assignments restricted to the first $k$ positions. The key structural invariant is that any such partial assignment is fully determined, up to isomorphism, by which values in ${1,\dots,m}$ have already been used and how they are assigned injectively to ${1,\dots,k}$.

A partial assignment on the first $k$ positions is therefore exactly an injective map from a $k$-element set into an $m$-element set. Such maps are counted by falling factorials. For a fixed $k$, the first position can choose any of $m$ values, the second any of the remaining $m-1$, and so on, until the $k$-th position has $m-k+1$ choices. The total number of distinct states at level $k$ is therefore

$$b_k = m(m-1)\cdots (m-k+1) = \frac{m!}{(m-k)!}.$$

This count describes the number of distinct reachable subfunctions after fixing any $k$ variables in the natural ordering. Every such subfunction corresponds to a unique residual “unused value set” of size $m-k$ together with a fixed injection from ${1,\dots,k}$ into ${1,\dots,m}$, and no two different injections induce the same residual Boolean function because the availability constraints on future positions depend exactly on which values have already been consumed.

For a BDD, this count is the level profile because each distinct partial injection yields a distinct node after reduction: no two states merge since their available-value complements differ.

For a ZDD, the representation removes zero branches aggressively, but the same combinatorial state space remains: a partial solution is still a set of chosen pairs forming an injective matching on $k$ rows. ZDD compression does not identify different injections because the presence or absence of each pair still affects future feasibility through column exclusion. Hence the level-$k$ states remain in bijection with injective maps from a $k$-set into an $m$-set, giving the same profile.

Thus both the BDD and ZDD profiles coincide and are given by the falling factorial sequence.

This completes the proof. ∎
