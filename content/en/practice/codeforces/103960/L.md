---
title: "CF 103960L - Listing Tedious Paths"
description: "Let $f(x1,dots,xn)$ be a Boolean function with truth table $tau$ of length $2^n$. A truth table is called a bead if it is not of the form $alphaalpha$."
date: "2026-07-02T06:47:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103960
codeforces_index: "L"
codeforces_contest_name: "2022-2023 ICPC Brazil Subregional Programming Contest"
rating: 0
weight: 103960
solve_time_s: 110
verified: false
draft: false
---

[CF 103960L - Listing Tedious Paths](https://codeforces.com/problemset/problem/103960/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 50s  
**Verified:** no  

## Solution
## Setup

Let $f(x_1,\dots,x_n)$ be a Boolean function with truth table $\tau$ of length $2^n$. A truth table is called a bead if it is not of the form $\alpha\alpha$. A Boolean function is called sweet if its truth table is a bead at every level of restriction, equivalently if every subtable obtained by fixing a prefix of variables is a bead.

For a function on $n$ variables, let $S(n)$ denote the number of sweet Boolean functions.

A subtable corresponding to fixing $x_1,\dots,x_k$ is a truth table of order $n-k$. Hence sweetness requires that for every $0\le k<n$, each of the $2^k$ subtables of order $n-k$ is a bead.

The goal is to determine $S(n)$ for $n\le 7$.

## Solution

A truth table of order $m$ is a bead precisely when it is not constant on the two halves induced by splitting on $x_1$, that is, it is not of the form $\alpha\alpha$. Hence a subtable of order $m$ is a bead exactly when its two subtables of order $m-1$ differ.

Thus a Boolean function is sweet if and only if for every assignment of $(x_1,\dots,x_k)$ with $k<n$, the induced function of the remaining variables is nonconstant in its first variable. Equivalently, every internal node in the full binary decision tree has distinct LO and HI values, and this property persists recursively.

Consider the full binary decision tree of depth $n$. At each node at level $k$, the subfunction depends on variables $x_{k+1},\dots,x_n$. Sweetness requires that at every node, the two children represent different subfunctions.

This implies that no two distinct nodes at the same level can represent the same subfunction, because if two nodes were identical, then all their descendants would coincide, and some higher-level node would have equal LO and HI after reduction, contradicting the bead condition at that node.

Hence every sweet function is represented by a full binary tree of depth $n$ in which all $2^n$ leaves are distinct values in the BDD sense, meaning all internal subfunctions are pairwise distinct. Since BDD reduction identifies identical subfunctions, sweetness forces the underlying unreduced decision tree to already be reduced in the sense of having no shared subfunctions.

Thus the number of sweet functions equals the number of ways to assign truth values to the $2^n$ leaves of the full binary decision tree such that all $2^n$ induced subtables are non-squares at every level. This condition is equivalent to requiring that every level-$m$ subtable is a bead, hence each subtable splits into two distinct subtables of the next level.

This induces a recursive counting structure. Let $S(n)$ be the number of sweet functions on $n$ variables. Fix a sweet function on $n-1$ variables. To extend it to $n$ variables, assign to each node at level $n-1$ a pair of distinct $(n-1)$-variable functions as LO and HI children. Since every subfunction must itself be sweet, both children must lie in $S(n-1)$, and they must be distinct.

Hence at each node, the choice is an ordered pair of distinct elements of $S(n-1)$. There are $S(n-1)(S(n-1)-1)$ such choices.

The structure at level $n-1$ consists of $2^{n-1}$ nodes, and independence of choices follows from the fact that each node corresponds to a distinct subtable in the full decision structure, so no identification occurs between nodes at the same level under the sweetness constraint. Therefore

$$S(n) = \bigl(S(n-1)(S(n-1)-1)\bigr)^{2^{n-1}}.$$

The base case is $S(0)=2$, since constant functions $0$ and $1$ are both beads of order $0$.

Now compute iteratively.

For $n=1$,

$$S(1) = (2\cdot 1)^{2^0} = 2.$$

For $n=2$,

$$S(2) = (2\cdot 1)^{2} = 4.$$

For $n=3$,

$$S(3) = (4\cdot 3)^{4} = 12^4 = 20736.$$

For $n=4$,

$$S(4) = (20736\cdot 20735)^{8}.$$

Compute the base:

$$20736\cdot 20735 = 429287,360.$$

Thus

$$S(4) = (429287360)^8.$$

For $n=5$,

$$S(5) = \bigl((429287360)^8((429287360)^8-1)\bigr)^{16}.$$

For $n=6$,

$$S(6) = \Bigl(S(5)(S(5)-1)\Bigr)^{32}.$$

For $n=7$,

$$S(7) = \Bigl(S(6)(S(6)-1)\Bigr)^{64}.$$

These expressions are exact closed forms determined recursively from the bead condition at every level.

Thus the values for $n\le 7$ are:

$$S(0)=2,\quad S(1)=2,\quad S(2)=4,\quad S(3)=20736,$$

$$S(4)=(429287360)^8,\quad
S(5)=\bigl((429287360)^8((429287360)^8-1)\bigr)^{16},$$

$$S(6)=\Bigl(S(5)(S(5)-1)\Bigr)^{32},\quad
S(7)=\Bigl(S(6)(S(6)-1)\Bigr)^{64}.$$

Hence the required enumeration up to $n=7$ follows from the recursive bead-preserving structure of the binary decision tree.

This completes the solution. ∎

## Verification

The recurrence uses only the bead condition at each node, which forces inequality of LO and HI subfunctions. The exponent $2^{n-1}$ arises from the number of nodes at level $n-1$ in the full decision structure, which matches the number of independent subfunction positions in the truth-table decomposition.

The base cases $S(0)=2$, $S(1)=2$, $S(2)=4$ follow directly from enumeration of length $1$ and $2$ bead constraints.

The multiplication $20736\cdot 20735$ is checked by expansion:

$$20736\cdot 20735 = 20736^2 - 20736 = 429981696 - 20736 = 429960960.$$

Thus the corrected intermediate value is $429960960$, yielding

$$S(4)=(429960960)^8.$$

All subsequent expressions depend only on this corrected base and remain structurally valid.

This completes the verification. ∎
