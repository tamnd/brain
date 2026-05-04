---
title: "Chapter 3. Linked Lists and Pointers"
description: "Linked lists are the first data structure in this book where the shape of the data matters as much as the values stored inside it."
tags: ["algorithms", "computer-science", "data-structures", "linked-lists"]
weight: 3000
date: 2026-05-03T15:57:34+07:00
---

Linked lists are the first data structure in this book where the shape of the data matters as much as the values stored inside it. An array gives direct access by index, but a linked list gives access through references from one node to the next. This changes the way algorithms are written. A solution must track not only what value is being inspected, but also which node owns the next link, which pointer must be preserved, and which edge in the list must be rewired.

This chapter develops linked list algorithms as pointer transformations. The basic operations are simple: create a node, follow a `next` pointer, insert a node, delete a node, and stop at `nil`. The difficulty comes from composition. Reversing a list, merging two sorted lists, detecting a cycle, or deleting the nth node from the end all require a small invariant about which part of the list has already been processed and which part remains untouched.

A recurring pattern is the use of sentinel nodes. A sentinel gives the algorithm a stable predecessor before the real head of the list. This removes many special cases, especially when the head itself may be inserted, deleted, or replaced. Another common pattern is the fast and slow pointer method, where two references move at different speeds to detect cycles, locate the middle, or split a list.

The chapter also treats linked lists as a way to study ownership and aliasing. Two variables may refer to the same node. Updating one link may change what another part of the program can reach. This is why linked list bugs are often structural rather than arithmetic: lost tails, accidental cycles, skipped nodes, double deletion, and stale references.

By the end of the chapter, you should be able to reason about linked list algorithms using three questions: which node am I holding, which link will I modify, and what part of the structure must remain reachable after the modification. This discipline will carry forward into trees, graphs, caches, and memory-sensitive systems.
