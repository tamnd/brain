---
title: "CF 1098A - Sum in the tree"
description: "We are given a rooted tree where every vertex originally had a nonnegative value. From those values, Mitya computed a second array where each node stores the sum of values along the path from the root to that node."
date: "2026-06-13T06:24:24+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dfs-and-similar", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 1098
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 530 (Div. 1)"
rating: 1600
weight: 1098
solve_time_s: 654
verified: false
draft: false
---

[CF 1098A - Sum in the tree](https://codeforces.com/problemset/problem/1098/A)

**Rating:** 1600  
**Tags:** constructive algorithms, dfs and similar, greedy, trees  
**Solve time:** 10m 54s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rooted tree where every vertex originally had a nonnegative value. From those values, Mitya computed a second array where each node stores the sum of values along the path from the root to that node. After that, the original values were erased, and then all path sums at even-depth vertices were also erased.

So the input keeps the tree structure and a partially observed version of the root-to-node path sums. For odd-depth nodes, we know the exact prefix sum from the root. For even-depth nodes, the prefix sum is missing. The task is to reconstruct any valid original assignment of node values that is consistent with the remaining information, or determine that no such assignment exists. Among all valid reconstructions, we must minimize the total sum of node values.

The key hidden structure is that each node value is the difference between a node’s prefix sum and its parent’s prefix sum. Since values are nonnegative, prefix sums must be nondecreasing along every root-to-leaf path.

The constraint n up to 100000 forces an O(n) or O(n log n) solution. Any approach that tries to guess missing values independently per node or recompute feasibility per configuration will be too slow because subtree dependencies propagate constraints globally.

A common failure case appears when an even-depth node has multiple odd-depth descendants with fixed sums that conflict. For example, if an even node is an ancestor of a node with known sum 5 and another branch requires it to be at least 10, naive local assignment might choose 0 and immediately break consistency later. Another failure is ignoring that missing values are not free variables, they are bounded both from below by their parent and from above by known descendants.

## Approaches

A brute-force approach
