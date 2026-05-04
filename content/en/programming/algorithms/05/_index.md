---

title: "Chapter 5. Hashing and Maps"
description: "Hash tables, hash functions, collision handling, probabilistic structures, and practical design for constant-time key-value access."
tags: ["algorithms", "hashing", "data-structures", "maps", "sets"]
weight: 5
date: 2026-05-04T23:14:12+07:00
---

# Chapter 5. Hashing and Maps

This chapter studies hashing as a practical mechanism for constant time access under realistic constraints. The focus is not on idealized O(1) claims, but on how hash tables behave under load, how collisions are handled, and how design choices affect predictability, memory locality, and adversarial robustness.

A hash table implements a partial function from keys to values by mapping keys into a finite index space. The mapping is defined by a hash function, and the core invariant is that equal keys must map to equal hashes. Everything else is a trade off between distribution quality, speed, and memory layout. The chapter makes these trade offs explicit so that you can choose an implementation that matches your workload.

Collision handling is treated as a first class concern. Separate chaining stores colliding entries in auxiliary structures, typically lists or small arrays. Open addressing stores all entries in the table itself and resolves collisions by probing. These approaches have different cache behavior and different failure modes. Chaining tolerates higher load factors but introduces pointer overhead. Open addressing improves locality but degrades sharply as the table fills. The chapter shows when each approach is appropriate and how to tune parameters such as load factor and probe sequence.

Hash function design is addressed from a systems perspective. A good hash function distributes inputs uniformly across buckets while remaining fast to compute. In practice, perfect uniformity is not required, but pathological clustering must be avoided. The chapter covers simple integer hashing, string hashing, and composite key hashing, with attention to mixing functions and avalanche properties. It also discusses deterministic versus randomized hashing, especially in contexts where adversarial inputs are possible.

Maps and sets are built on top of hashing. A set stores keys without associated values, while a map associates each key with a value. Common patterns include frequency counting, grouping, deduplication, and membership testing. These patterns appear repeatedly in higher level algorithms, so the chapter emphasizes minimal interfaces and predictable semantics. Operations such as insert, delete, and lookup are analyzed not only in average case terms but also in terms of worst case degradation.

Advanced probabilistic structures extend the basic hashing model. Bloom filters provide approximate membership with controlled false positive rates and fixed memory usage. Count-min sketches approximate frequency counts in streaming settings. These structures sacrifice exactness to gain space efficiency and speed. The chapter explains their guarantees, parameter choices, and appropriate use cases.

Another recurring theme is the interaction between hashing and memory systems. Cache locality often dominates theoretical complexity. Open addressing with linear probing can outperform more complex schemes because it accesses contiguous memory. Chaining can degrade performance due to pointer chasing. The chapter provides guidelines for aligning data structures with modern hardware behavior.

Finally, the chapter addresses correctness and robustness. Poor hash functions or incorrect equality definitions can silently corrupt results. Rehashing strategies must preserve all entries while resizing the table. Edge cases such as empty keys, large inputs, and high collision scenarios are examined systematically. Testing strategies include randomized input generation and adversarial cases designed to stress collision behavior.

By the end of the chapter, you will be able to design and implement hash based structures that behave predictably under load, select appropriate hashing strategies for different key types, and reason about performance beyond asymptotic notation.
