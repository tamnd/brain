---
title: "CF 2190G - Maximize Determinant"
description: "I can't reliably write a complete accepted editorial and proof for Codeforces 2190G from the problem statement alone."
date: "2026-06-07T21:07:13+07:00"
tags: ["codeforces", "competitive-programming", "graphs"]
categories: ["algorithms"]
codeforces_contest: 2190
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 1073 (Div. 1)"
rating: 3300
weight: 2190
solve_time_s: 70
verified: false
draft: false
---

[CF 2190G - Maximize Determinant](https://codeforces.com/problemset/problem/2190/G)

**Rating:** 3300  
**Tags:** graphs  
**Solve time:** 1m 10s  
**Verified:** no  

## Solution
I can't reliably write a complete accepted editorial and proof for Codeforces 2190G from the problem statement alone.

This is a 3300-rated problem whose solution depends on several nontrivial graph-theoretic lemmas about determinants of interval matrices, tree incidence matrices, determinant signs, and a weighted spanning-tree optimization. While I can recover the first part of the solution from the public hints:

- After taking column differences and adding an extra column, each row becomes the incidence vector of an edge $(l_i, r_i+1)$ in a graph on $n+1$ vertices.
- The determinant of the interval matrix is always in $\{-1,0,1\}$.
- The determinant is nonzero iff the corresponding graph is a tree.
- For a rooted tree, the sign can be expressed through a permutation induced by edge indices and parent relations.

the remaining part of the solution, which is the actual optimization problem, requires several additional lemmas (Hints 7-11) that characterize exactly when a single edge edit can flip the determinant sign and how the zero-determinant case reduces to a weighted spanning-tree problem.

Without reconstructing those lemmas completely and verifying them against the official proof, I would risk producing an incorrect editorial and incorrect code.

If you'd like, I can instead provide:

1. A detailed derivation of the determinant ↔ tree correspondence.
2. A proof that $|\det(A)| \le 1$ and $X=1$.
3. A reconstruction of the official solution from the published hints, step by step, until we recover the full accepted algorithm.
4. A review of an existing accepted implementation if you provide one.

That would be much safer than inventing the missing parts of a 3300-rated editorial.
