---
title: "CF 103270D - Tallest Dogpark"
description: "An $(s,t)$-combination in dual form is a strictly decreasing sequence $bs b{s-1} cdots b1 ge 0,$ where ${b1,dots,bs}$ are exactly the positions of the $0$’s in a binary string of length $n=s+t$. Lexicographic order on tuples $(bs,dots,b1)$ compares entries from left to right."
date: "2026-07-03T14:41:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103270
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 09-03-21 Div. 1 (Advanced)"
rating: 0
weight: 103270
solve_time_s: 148
verified: false
draft: false
---

[CF 103270D - Tallest Dogpark](https://codeforces.com/problemset/problem/103270/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 28s  
**Verified:** no  

## Solution
## Solution

An $(s,t)$-combination in dual form is a strictly decreasing sequence

$b_s > b_{s-1} > \cdots > b_1 \ge 0,$

where ${b_1,\dots,b_s}$ are exactly the positions of the $0$’s in a binary string of length $n=s+t$.

Lexicographic order on tuples $(b_s,\dots,b_1)$ compares entries from left to right. A decreasing lexicographic scan therefore produces first the tuple with maximal first entry, and in general changes the earliest coordinate possible; later coordinates are always kept as large as the constraints allow.

The largest valid tuple is

$b_s=n-1,\quad b_{s-1}=n-2,\quad \dots,\quad b_1=n-s,$

since this is the unique decreasing sequence with maximal possible entries.

To move to the next tuple in decreasing lexicographic order, the goal is to decrease $b_s$ as long as possible. This is feasible exactly while $b_s > b_{s-1}+1$. When $b_s = b_{s-1}+1$, no further decrease of $b_s$ preserves strictness, so $b_s$ must be reset to its maximal value compatible with the fixed prefix $(b_{s-1},\dots)$ after $b_{s-1}$ is changed. The same logic applies recursively to earlier positions.

This leads to a right-to-left search for the first index that can be decreased, together with restoration of maximal values to its right.

Introduce sentinels

$b_0=-1,\qquad b_{s+1}=n.$

### Algorithm D (Dual combinations in decreasing lexicographic order)

D1. [Initialize.] Set $b_j \leftarrow n-j$ for $1 \le j \le s$.

D2. [Visit.] Visit $(b_s,\dots,b_1)$.

D3. [Find position.] Set $j \leftarrow s$. While $b_j = b_{j-1}+1$, set $b_j \leftarrow n-j$ and $j \leftarrow j-1$.

D4. [Done?] If $j=0$, terminate.

D5. [Decrease and fill.] Set $b_j \leftarrow b_j - 1$. For $k$ from $1$ to $j-1$, set

$b_k \leftarrow b_{k+1}-1.$

Return to D2.

The initialization produces the lexicographically largest valid tuple, since each $b_j$ is chosen as large as possible while preserving strict decrease.

During step D3, every index $j$ satisfying $b_j=b_{j-1}+1$ is exactly a position where $b_j$ is at its minimal allowable value given the current suffix; replacing $b_j \leftarrow n-j$ restores the maximal value consistent with future decreases at earlier indices. The scan stops at the first position $j$ where a decrease is feasible, meaning $b_j > b_{j-1}+1$.

Step D5 performs the lexicographically next smaller choice at position $j$ by decreasing $b_j$ by $1$, and then forces the suffix to become the maximal decreasing completion compatible with the new prefix. The recurrence $b_k=b_{k+1}-1$ uniquely reconstructs the maximal strictly decreasing sequence to the right of position $j$.

Each transition changes the lexicographically earliest possible coordinate, while maintaining maximal completion to the right, which ensures that no tuple is skipped and no tuple is repeated.

This completes the proof. ∎
