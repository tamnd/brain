---
title: "Chapter 6. Sorting"
description: "Sorting algorithms from fundamental contracts through comparison-based, linear-time, and specialized variants, with selection, external sorting, and correctness analysis."
tags: ["algorithms", "sorting", "data-structures"]
weight: 6
---

# Chapter 6. Sorting

Sorting is treated here as a family of transformations with precise contracts, rather than as isolated algorithms. The input is a sequence together with a comparison relation. The output is a permutation of that sequence arranged so that the relation holds between consecutive elements. Two properties dominate every design: correctness of ordering and preservation of data through permutation.

The chapter begins by fixing the contract. A sorting procedure must produce a sequence that is ordered and that contains exactly the same multiset of elements as the input. Stability is introduced as an additional constraint: equal keys preserve their relative order. This constraint affects algorithm choice and implementation details, especially when records carry secondary fields.

Elementary algorithms such as insertion sort and selection sort are used to establish invariants and reasoning patterns. They provide clear loop invariants and expose the mechanics of comparison and movement. These forms are not competitive at scale, but they define the baseline for correctness arguments and for small input optimization inside hybrid algorithms.

Divide and conquer appears through merge sort and quick sort. Merge sort provides a stable, predictable structure with guaranteed $O(n \log n)$ time and linear auxiliary space. Quick sort provides in-place behavior and strong practical performance, with sensitivity to pivot selection and input distribution. The analysis emphasizes partition invariants, recursion structure, and worst-case avoidance strategies.

Heap-based methods introduce an alternative perspective. Heap sort derives ordering from a priority structure and achieves $O(n \log n)$ time with constant auxiliary space. The tradeoff is reduced locality and loss of stability. This section focuses on the transformation between array representation and heap invariants, and on the cost model of repeated extraction.

Non-comparison sorting methods, including counting sort and radix sort, exploit structure in the key domain. When keys lie in bounded ranges or can be decomposed into digits, these methods achieve linear time under explicit assumptions. The chapter isolates those assumptions and shows how violations degrade correctness or performance.

Partial sorting and selection form a separate class of problems. In many systems, only the smallest $k$ elements or the median is required. Algorithms such as quickselect and heap-based selection reduce work by avoiding full ordering. The analysis highlights how selection modifies partition logic and how guarantees differ from full sorting.

External sorting addresses data that does not fit in memory. The model shifts from CPU cost to I/O cost. Multi-way merging, run generation, and buffer management determine performance. The treatment focuses on controlling disk access patterns and minimizing passes over data.

Throughout the chapter, comparator design is treated as part of the algorithm. Comparators must define a strict weak ordering. Violations lead to undefined behavior or non-termination. When sorting composite records, comparator cost can dominate runtime, so caching and key extraction become relevant.

Testing and validation are framed in terms of invariants. A sorted output must satisfy local ordering checks and global permutation checks. Adversarial inputs, such as already sorted sequences or sequences with many duplicates, are used to expose instability and worst-case paths.

By the end of the chapter, you should be able to select an appropriate sorting strategy based on constraints, implement it with correct invariants, and reason about its time, space, and stability properties in a way that remains valid when integrated into larger systems.
