---

title: "Chapter 2. Arrays and Strings"
description: "This chapter studies linear data as the primary substrate for algorithm design."
tags: ["algorithms", "computer-science", "arrays", "strings"]
weight: 2000
date: 2026-05-03T15:27:09+07:00
---

This chapter studies linear data as the primary substrate for algorithm design. Arrays and strings appear simple, but most high performance solutions reduce to controlled traversal, local state maintenance, and careful boundary handling on these structures. The objective here is to make these operations predictable and composable.

An array is treated as a contiguous block of memory with constant time indexed access. A string is treated as a sequence with additional structural constraints, often over a fixed alphabet. The distinction matters when operations depend on encoding, comparison cost, or normalization rules. The chapter begins by fixing a precise model for indexing, slicing, and mutation, since many errors originate from implicit assumptions about these operations.

A central theme is transforming global problems into local invariants. Techniques such as prefix sums, difference arrays, and sliding windows convert repeated recomputation into incremental updates. These transformations reduce time complexity by preserving a compact summary of past computation. The chapter emphasizes how to define and maintain these summaries so that correctness follows from simple invariants.

Two pointer techniques and partitioning schemes are introduced as controlled ways to scan data with minimal overhead. These methods rely on monotonic movement of indices and clear loop invariants. When applied correctly, they avoid nested loops and reduce quadratic behavior to linear time. The discussion focuses on when such monotonicity exists and how to enforce it.

String processing introduces additional structure. Substring search, pattern matching, and hashing rely on representing segments of a string in a form that supports fast comparison. Rolling hash techniques provide constant time substring comparison after linear preprocessing, at the cost of probabilistic correctness. The chapter makes these trade offs explicit and shows how to control collision risk.

Another recurring concern is in-place transformation. Many array problems can be solved without additional memory by reusing the input structure. This requires careful ordering of operations and explicit reasoning about overwritten data. The chapter presents standard patterns for safe in-place updates, including stable partitioning and cyclic replacement.

Edge cases receive systematic treatment. Empty inputs, single element ranges, duplicate values, and boundary indices are handled as part of the algorithm design rather than as afterthoughts. Each technique is accompanied by a minimal set of conditions that must hold for correctness, and these conditions are checked explicitly.

Performance considerations are tied to memory behavior. Sequential access patterns exploit cache locality, while scattered access patterns degrade performance. The chapter highlights how algorithm design interacts with hardware constraints, especially for large inputs.

By the end of this chapter, you should be able to recognize when a problem over arrays or strings can be reduced to a small set of patterns: prefix accumulation, window maintenance, pointer scanning, or hashing. You should also be able to implement these patterns with clear invariants, correct boundary handling, and predictable performance.
