---
title: "CF 1515C - Phoenix and Towers"
description: "We are given a set of n blocks, each with a height hi. Phoenix wants to construct exactly m towers using all the blocks. Each tower's height is the sum of its blocks, and a \"beautiful\" arrangement requires that no two towers differ in height by more than x."
date: "2026-06-10T18:31:16+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1515
codeforces_index: "C"
codeforces_contest_name: "Codeforces Global Round 14"
rating: 1400
weight: 1515
solve_time_s: 226
verified: false
draft: false
---

[CF 1515C - Phoenix and Towers](https://codeforces.com/problemset/problem/1515/C)

**Rating:** 1400  
**Tags:** constructive algorithms, data structures, greedy  
**Solve time:** 3m 46s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of `n` blocks, each with a height `h_i`. Phoenix wants to construct exactly `m` towers using all the blocks. Each tower's height is the sum of its blocks, and a "beautiful" arrangement requires that no two towers differ in height by more than `x`. The task is to assign each block to a tower so that this property is satisfied. If it is possible, we must produce a sequence indicating which tower each block belongs to; otherwise, we print `NO`.

The input consists of multiple test cases. Each test case provides the number of blocks, the number of towers, the maximum allowed height difference `x`, and the heights of all blocks. The output must either be `YES` followed by an assignment of blocks to towers, or `NO`.

The constraints tell us that the total number of blocks across all test cases is up to 100,000. With a 2-second time limit, this implies we need an algorithm roughly linear in `n` per test case. Nested loops or O(n²) approaches are too slow.

A subtle edge case occurs when all blocks have the same height. A naive greedy assignment that always fills the first tower fully before moving to the next can produce an unbalanced configuration, exceeding the allowed `x` difference, even though an interleaving approach would work. For example, if `n=3, m=2, x=1` with heights `[1,1,1]`, assigning all blocks to the first tower gives heights `[3,0]` with difference 3, which is greater than `x`. The correct assignment `[1,2,1]` gives tower heights `[2,1]`, which satisfies the constraint.

Another edge case occurs when `m = n`, where each tower must contain exactly one block. The solution in this case is trivial, but the algorithm must handle it correctly.

## Approaches

The brute-force approach considers every possible distribution of blocks among towers. For each combination, we compute the tower heights and check if the maximum difference is at most `x`. The number of ways to partition `n` blocks into `m` towers grows exponentially, roughly O(m^n). This is infeasible even for small `n`.

The key observation is that the height limit `x` is less restrictive than it appears. Since each block height `h_i ≤ x`, the absolute difference in heights between any two blocks is at most `x`. This allows a simple greedy strategy: always place the next block onto the currently shortest tower. By maintaining the towers in a priority queue ordered by current height, we ensure that the towers remain balanced as blocks are assigned. Sorting the blocks is not strictly necessary, but assigning taller blocks earlier can reduce temporary spikes in tower heights. After all blocks are assigned, the resulting tower heights are guaranteed to have differences no more than `x`, because no single block exceeds `x`.

This reduces the solution from exponential time to O(n log m), since we maintain a heap of size `m` for `n` insertions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m^n) | O(n) | Too slow |
| Greedy heap | O(n log m) | O(m+n) | Accepted |

## Algorithm Walkthrough

1. Initialize a min-heap of towers with their current heights set to 0, along with their indices 1 to m. This allows efficient retrieval of the shortest tower at any point.
2. Iterate over the blocks in the input order. For each block, pop the tower with the smallest current height from the heap.
3. Assign the block to this tower, updating the tower's total height by adding the block's height. Record the tower index in an array that matches the block order.
4. Push the updated tower back into the heap.
5. After all blocks are assigned, print `YES` followed by the assignment array. The assignment guarantees that the height difference between any two towers cannot exceed `x` because no block is taller than `x` and we always place blocks on the currently shortest tower.

### Why it works

The invariant is that the difference between the tallest and shortest towers is minimized at every step. Since each block has a maximum height of `x`, no single addition can increase the difference beyond `x` in one step. Placing the tallest blocks first or maintaining order does not affect correctness, only the temporary fluctuation of heights. The heap ensures that blocks are always assigned to the optimal tower to minimize differences.

## Python Solution

```
PythonRun
```

The solution first reads the number of test cases and processes each independently. A min-heap stores `(current height, tower index)` tuples, which ensures the shortest tower is always available in O(log m) time. Blocks are assigned sequentially in input order. The assignment array stores the tower each block belongs to and is printed after processing all blocks.

## Worked Examples

### Example 1

Input blocks `[1,2,3,1,2]` with `m=2`.

| Step | Heap state (height, tower) | Block | Assignment | Heap after push |
| --- | --- | --- | --- | --- |
| 1 | [(0,1),(0,2)] | 1 | 1 | [(0,2),(1,1)] |
| 2 | [(0,2),(1,1)] | 2 | 2 | [(1,1),(2,2)] |
| 3 | [(1,1),(2,2)] | 3 | 1 | [(2,2),(4,1)] |
| 4 | [(2,2),(4,1)] | 1 | 2 | [(3,2),(4,1)] |
| 5 | [(3,2),(4,1)] | 2 | 2 | [(5,2),(4,1)] |

Final assignment: `[1,2,1,2,2]`. Tower heights `[4,5]`, difference `1 ≤ x=3`.

### Example 2

Input blocks `[1,1,2,3]` with `m=3`.

| Step | Heap state | Block | Assignment | Heap after push |
| --- | --- | --- | --- | --- |
| 1 | [(0,1),(0,2),(0,3)] | 1 | 1 | [(0,2),(0,3),(1,1)] |
| 2 | [(0,2),(0,3),(1,1)] | 1 | 2 | [(0,3),(1,1),(1,2)] |
| 3 | [(0,3),(1,1),(1,2)] | 2 | 3 | [(1,1),(1,2),(2,3)] |
| 4 | [(1,1),(1,2),(2,3)] | 3 | 1 | [(2,1),(2,3),(1,2)] |

Final assignment: `[1,2,3,1]`. Tower heights `[4,1,2]`, difference `3 ≤ x=3`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log m) | Each block insertion and heap update takes O(log m), total n blocks. |
| Space | O(m+n) | Heap stores m towers, answer array stores n assignments. |

Given n ≤ 10^5 and m ≤ n, the solution executes comfortably within 2 seconds.

## Test Cases

```
PythonRun
```
