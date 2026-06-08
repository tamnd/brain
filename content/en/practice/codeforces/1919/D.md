---
title: "CF 1919D - 01 Tree"
description: "We are given the distances from the root to the leaves of a binary tree, listed in DFS leaf order. Every internal vertex has exactly two children. One outgoing edge has weight 0 and the other has weight 1."
date: "2026-06-08T19:34:16+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "dsu", "greedy", "sortings", "trees"]
categories: ["algorithms"]
codeforces_contest: 1919
codeforces_index: "D"
codeforces_contest_name: "Hello 2024"
rating: 2100
weight: 1919
solve_time_s: 46
verified: false
draft: false
---

[CF 1919D - 01 Tree](https://codeforces.com/problemset/problem/1919/D)

**Rating:** 2100  
**Tags:** constructive algorithms, data structures, dsu, greedy, sortings, trees  
**Solve time:** 46s  
**Verified:** no  

## Solution
## Problem Understanding

We are given the distances from the root to the leaves of a binary tree, listed in DFS leaf order.

Every internal vertex has exactly two children. One outgoing edge has weight `0` and the other has weight `1`. The actual shape of the tree is unknown, only the leaf distances are known.

The task is to decide whether some such tree could produce the given array.

The total number of leaves across all test cases is at most `2 · 10^5`, so any solution that is quadratic in `n` is immediately ruled out. Even `O(n√n)` would be uncomfortable. We need something close to linear or `O(n log n)`.

The tricky part is that the DFS order imposes a strong structure. Leaves that belong to the same subtree occupy a contiguous segment. A naive reconstruction attempt can easily make locally valid choices that become impossible later.

One important edge case is the minimum value.

Input:

```
2
0 0
```

Output:

```
NO
```

Two leaves cannot both have distance `0`. Every sibling pair differs by exactly one because one child edge has weight `0` and the other has weight `1`. The root itself corresponds to a single distance `0`, so a valid array must contain exactly one zero.

Another subtle case is:

```
3
0 2 1
```

Output:

```
NO
```

The value `2` needs some neighboring structure that can eventually serve as its parent distance `1`. Although a `1` exists in the array, the DFS ordering prevents it from being used correctly.

A third easy-to-miss example is:

```
3
0 1 2
```

Output:

```
YES
```

The values increase monotonically, but this is still realizable. Looking only at adjacent elements is not enough. We need to reason about the nearest smaller values that remain after recursive merges.

## Approaches

A brute force view is to reverse the tree construction.

If two leaves are siblings, then their distances differ by exactly one. When we merge them into their parent, the parent's distance becomes the smaller of the two values. We could repeatedly search for a valid adjacent pair, merge it, and continue until one value remains.

This mirrors the tree structure exactly, so it is correct. The problem is that there can be many choices. Exploring all merge orders is exponential. Even greedily simulating merges with expensive updates quickly becomes quadratic.

The key observation is that we do not actually need to perform the merges.

Consider a value `x > 0`. Somewhere during the reverse process it must be paired with a node of value `x - 1`. In the current DFS order, the partner must appear on one side of it. If we look for the nearest strictly smaller value on the left and on the right, then at least one of them must equal `x - 1`. Otherwise there is no way to create the parent required by this leaf.

This turns the tree problem into an array problem.

For every position `i`:

- If `a[i] = 0`, it is the unique root-distance leaf.
- If `a[i] > 0`, then among the nearest strictly smaller values on the left and right, at least one must be exactly `a[i] - 1`.

Nearest smaller elements can be computed in linear time with monotonic stacks.

The result is an `O(n)` check per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Merge Simulation | Exponential or O(n²) depending on implementation | O(n) | Too slow |
| Monotonic Stack Validation | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Count how many zeros appear in the array.

A valid tree must contain exactly one value `0`. If the count is not one, answer `NO`.
2. Compute the nearest st
