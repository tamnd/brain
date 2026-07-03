---
title: "CF 103388L - Listing Passwords"
description: "The binomial tree $Tn$ used in this section has $2^n$ nodes, each node corresponding to a binary string of length $n$, and $Tinfty$ is the limiting structure in which nodes correspond to all finite binary strings obtained by suppressing leading zeros."
date: "2026-07-03T18:19:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103388
codeforces_index: "L"
codeforces_contest_name: "2021-2022 ACM-ICPC Brazil Subregional Programming Contest"
rating: 0
weight: 103388
solve_time_s: 85
verified: false
draft: false
---

[CF 103388L - Listing Passwords](https://codeforces.com/problemset/problem/103388/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 25s  
**Verified:** no  

## Solution
## Solution

The binomial tree $T_n$ used in this section has $2^n$ nodes, each node corresponding to a binary string of length $n$, and $T_\infty$ is the limiting structure in which nodes correspond to all finite binary strings obtained by suppressing leading zeros. Each node is identified with its bit string, and the tree structure is defined so that extending a string by appending bits corresponds to moving down the tree.

The statement that preorder on $T_\infty$ coincides with increasing binary notation means that preorder lists nodes in the same order as sorting their binary labels as integers written in base $2$ (with leading zeros suppressed). Hence preorder is a linear extension of the natural order on these binary strings interpreted as numbers.

Let $P$ denote the preorder sequence and $Q$ the postorder sequence of $T_\infty$. The tree is a full binary tree where each node has a left child obtained by appending $0$ and a right child obtained by appending $1$. Postorder traversal therefore visits the entire left subtree before the right subtree, and only then visits the root.

For any fixed finite depth $n$, the tree $T_n$ is a complete binary tree of height $n$ whose nodes are exactly the binary strings of length at most $n$, embedded in a uniform left-to-right structure. In such a tree, postorder traversal has the standard recursive form: the postorder list of a tree is obtained by concatenating the postorder list of the left subtree, then the postorder list of the right subtree, and finally the root. Passing to the limit $n \to \infty$ preserves this recursive structure for every finite prefix of nodes, since every finite node lies in a finite subtree.

The preorder enumeration corresponds to increasing binary value. In a full binary tree ordered by appending $0$ to the left and $1$ to the right, this implies that a node with binary string $b_k \dots b_1$ is visited before all nodes whose binary values are larger, which forces preorder to list nodes in lexicographic order with $0 < 1$, and hence in increasing binary notation.

Postorder reverses the structural priority: for any fixed prefix, all nodes in the subtree rooted at a node are visited before the node itself. In a full binary tree this induces a reversal of the recursive construction that builds binary strings from least significant extension. Concretely, if preorder corresponds to interpreting a binary string as a number built from most significant structure outward, postorder corresponds to completing all extensions before recording the prefix, which reverses the effective bit construction order.

This reversal manifests globally as reversal of the binary expansion when the traversal is expressed as a single infinite sequence indexed in preorder order. If the preorder index of a node is determined by its binary string $x_1 x_2 \dots x_m$, then the postorder index is obtained by reading the same structural path in reverse completion order, which corresponds to reversing the sequence of decisions that produced the node from the root. Thus the postorder label is the bit-reversal of the preorder label.

The millionth node in preorder is given as

$$11110100001000111111.$$

Reversing this string gives the postorder label.

Writing the string and reversing digit by digit yields

$$11110100001000111111 \;\mapsto\; 11111100010000101111.$$

Hence the millionth node in postorder is

$$\boxed{11111100010000101111}.$$

This completes the solution. ∎
