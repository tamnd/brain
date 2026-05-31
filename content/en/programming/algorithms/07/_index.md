---
title: "Chapter 7. Binary Search and Ordered Data"
description: "Binary search as an invariant-maintenance algorithm, extended to answer bisection and monotone predicates, then to ordered data structures: BSTs, balanced trees, augmented structures, and range queries."
tags: ["algorithms", "binary-search", "ordered-data", "trees"]
weight: 7
date: 2026-06-01T01:45:00+07:00
---

# Chapter 7. Binary Search and Ordered Data

Binary search is one of the most deceptively simple ideas in computer science. Given a sorted array and a target, you repeatedly cut the search space in half by comparing the target with the middle element. Each comparison eliminates half the remaining candidates, so the algorithm terminates in $O(\log n)$ steps. The simplicity is real — the code is short — but the correctness is fragile. Off-by-one errors in the boundary update or the termination condition are among the most common bugs in competitive programming, and they arise precisely because most programmers do not reason from a loop invariant.

The chapter opens with the binary search template and its invariant. The invariant is the key: it states exactly what is true about the search interval before every iteration. Once you have the invariant, the boundary updates and the termination condition follow from it mechanically, leaving no room for guessing. From this foundation the chapter derives lower bound and upper bound as direct variants, and then extends binary search to a much more general principle: any monotone predicate over an ordered domain can be bisected. This view, sometimes called *search on answer*, lets you solve problems like "find the minimum speed such that all packages are delivered in time" by binary searching over the answer space and checking feasibility.

Floating-point binary search applies the same template to real-valued domains, replacing exact equality with a precision threshold. Rotated arrays and peak finding introduce complications where the array is not globally sorted but retains a local structure that binary search can still exploit, provided the invariant is stated carefully for the modified domain.

The second half of the chapter moves from sequences to ordered data structures. An ordered map — whether implemented as a balanced BST, a treap, or a B-tree — supports the same lower-bound and upper-bound queries as a sorted array, but also supports dynamic insertion and deletion in $O(\log n)$ time. The chapter covers the major self-balancing tree families: AVL trees (strict height balance), red-black trees (relaxed balance with two-color invariant), treaps (randomized balance via heap priorities), and B-trees (wide branching for cache and disk efficiency). Each is presented in terms of its invariant and the operations required to restore it after a structural change.

Order statistics trees extend balanced BSTs to answer rank and selection queries: given a key, what is its rank? Given a rank, what is the key? This requires augmenting each node with a subtree size, and updating that count through rotations and rebalancing. The coordinate compression technique reduces a set of large or real-valued keys to a compact integer range so that array-based data structures can be applied; it is a preprocessing step that implicitly sorts and re-indexes the input.

Range queries and parametric search tie the chapter together. Interval search — finding all intervals that overlap a query point — maps naturally onto an augmented BST. Parametric search, a more advanced technique, solves optimization problems by binary searching over a parameter and using a decision procedure as the comparator. Boundary bugs — the persistent tendency to write `<` instead of `<=`, or to update `hi = mid` instead of `hi = mid - 1` — are catalogued with their symptoms and the invariant-based fixes.

By the end of this chapter you will be able to implement binary search from an invariant rather than from memory, apply bisection to answer-space problems, choose among the major balanced tree implementations based on their trade-offs, and reason about augmented tree operations in terms of the invariants they must preserve.
