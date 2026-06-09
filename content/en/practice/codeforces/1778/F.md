---
title: "CF 1778F - Maximizing Root"
description: "We are asked to maximize the value of the root of a tree after performing at most $k$ operations. Each operation allows us to pick a vertex $v$ that has not been selected before, choose a number $x$ that divides all values in $v$'s subtree, and multiply every value in that…"
date: "2026-06-09T11:36:25+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dp", "graphs", "math", "number-theory", "trees"]
categories: ["algorithms"]
codeforces_contest: 1778
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 848 (Div. 2)"
rating: 2600
weight: 1778
solve_time_s: 34
verified: false
draft: false
---

[CF 1778F - Maximizing Root](https://codeforces.com/problemset/problem/1778/F)

**Rating:** 2600  
**Tags:** dfs and similar, dp, graphs, math, number theory, trees  
**Solve time:** 34s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to maximize the value of the root of a tree after performing at most $k$ operations. Each operation allows us to pick a vertex $v$ that has not been selected before, choose a number $x$ that divides all values in $v$'s subtree, and multiply every value in that subtree by $x$. The input provides a tree structure, initial vertex values, and the limit $k$. The output is the largest possible value of the root node after applying the operations optimally.

Because the tree can have up to $10^5$ nodes per test case and there can be up to $50{,}000$ test cases, any algorithm with $O(n^2)$ complexity or that tries all subsets of nodes is too slow. We need something linear in $n$ or at worst $n \log n$. Values at nodes are bounded by 1000, which hints that operations based on prime factorization or divisors might be feasible.

A subtle edge case arises when $k=0$, where no operations are allowed. A careless algorithm that always attempts multiplications would incorrectly modify the root value. Another edge case is when the tree has a chain of nodes with the same values, because greedy local choices of multiplication could block larger gains from choosing deeper subtrees first.

## Approaches

The brute-force method would enumerate all subsets of at most $k$ nodes and all divisors of each subtree. For each choice, we would simulate multiplying the subtree, then recursively continue. This works in principle, but the number of possible sets of nodes is $O(\binom{n}{k})$, and for $k$ even around 10 on a tree with 100,000 nodes, this is astronomically large. Calculating subtree divisors is also non-trivial if done repeatedly.

The key insight is that the multiplier for a subtree is determined by the greatest common divisor (GCD) of the subtree, and multiplication operations propagate up the tree. This means we can reason recursively: for a node $v$, we can compute the GCDs of all its children, combine them with its own value to determine possible multipliers, and then choose the largest multipliers first to maximize the root. We can formalize this using a depth-first search and dynamic programming: each node maintains a list of "best products achievable with $j$
