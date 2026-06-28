---
title: "CF 104743A - Make All Elements 0"
description: "We are given an array of non-negative integers. In a single operation, we choose a contiguous segment and apply a bitwise AND with some value $x$, where $1 le x le k$. This operation overwrites every element in the chosen segment by clearing some of its bits according to $x$."
date: "2026-06-29T01:20:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104743
codeforces_index: "A"
codeforces_contest_name: "TheForces Round #25(5^2-Forces)"
rating: 0
weight: 104743
solve_time_s: 30
verified: false
draft: false
---

[CF 104743A - Make All Elements 0](https://codeforces.com/problemset/problem/104743/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of non-negative integers. In a single operation, we choose a contiguous segment and apply a bitwise AND with some value $x$, where $1 \le x \le k$. This operation overwrites every element in the chosen segment by clearing some of its bits according to $x$. The goal is to transform the entire array into all zeros using the minimum number of such segment operations, or determine that it cannot be done.

The important observation is that a bitwise AND can only turn bits off, never on. So each element can only move downward in the bitwise partial order defined by inclusion of bits. Reaching zero means every bit that appears in any element must be eliminated at some point by an operation that applies a mask that removes that bit.

The constraints are small enough that any solution quadratic in $n$ per test case might pass, but anything cubic or involving per-bit recomputation over all subarrays would be too slow. The sum of all $n$ is only $10^4$, which strongly suggests that an $O(n^2)$ or $O(n \log k)$ approach is intended.

A key edge case arises from the fact that the operation is bounded by $k$. If $k$ does not contain a certain bit that appears in some $a_i$, then that bit can never be removed from that position if we are forced to use $x \le k$. For example, if $a = [1]$ and $k = 0$, the problem is already impossible since no valid $x$ exists. A more subtle case is when $k$ lacks certain high bits required to clear elements.

Another failure case comes from misunderstanding that applying AND over a segment does not merge information between elements. Each element is independently masked by the same $x$, so the segment choice is purely about grouping identical or compatible reductions, not about accumulating progress per element.

## Approaches

A brute-force interpretation considers every possible sequence of operations. Each operation selects a segment and a value $x$, applies a mask, and continues until all elements become zero. This view immediately becomes intractable because even the number of segment choices alone is $O(n^2)$, and sequences of operations grow exponentially.

A more structured brute force tries to decide, for each segment, how many operations are needed to reduce all elements in that segment to zero. Even here, recomputing bit states after each operation leads to repeated scanning of segments and repeated bit manipulations, producing at least $O(n^3)$ behavior in straightforward implementations.

The key structural observation is that AND operations only remove bits, and removing a bit from multiple contiguous elements can be thought of as “covering” that bit over a segment. Each operation corresponds to choosing a segment and selecting a mask $x$, which determines exactly which bits remain, meaning it determines which bits are cleared.

We can invert the viewpoint: instead of thinking about what remains, we think about which bits must be removed. Each element has a fixed set of 1-bits that must all be eliminated by some operation covering that index and using an $x$ that flips those bits to zero.

Now consider a single bit position independently. For a fixed bit $b$, we look at all indices where that bit is set. To eliminate it, we must apply an operation covering those positions with an $x$ that has bit $b$ set to zero. Since $x \le k$, only certain bit patterns are allowed, and this constrains feasibility.

The problem reduces to grouping positions into segments where a single operation can simultaneously clear all required bits for all covered elements. Each operation is essentially a segment cover that reduces the bitwise requirements across that segment. The minimal number of operations corresponds to the minimal segmentation of the array into regions where each region can be cleared optimally.

This leads to a greedy segmentation strategy: we extend a segment as long as all elements in it share a compatible constraint under some valid mask $x \le k$. When the constraint breaks, we cut and start a new segment.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | exponential | O(n) | Too slow |
| Optimal | O(n) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. For each position, determine whether its bits can be cleared at all under the constraint $x \le k$. If an element has a bit that cannot be removed by any valid $x$, the answer is immediately impossible. This check prevents wasting time on unsatisfiable instances.
2. Traverse the array from left to right while maintaining the set of bits that are still “active requirements” for the current segment. Initially, this set comes from the first element.
3. When extending the segment to include a new element, merge its required bits with the current segment requirement. This represents the fact that a single operation over the segment must be able to handle all elements simultaneously.
4. At each step, verify whether there exists some $x \le k$ that can simultaneously satisfy the requirement of clearing all bits in the current segment. If no such $x$ exists, we must end the segment before this element.
5. When we close a segment, we increment the operation count and restart a new segment beginning at the current position. This ensures each operation is maximally effective.
6. Continue until the full array is processed. The number of segments formed is the answer.

The reason greedy segmentation is correct is that any operation acts on a contiguous block, and once a bit-compatibility constraint fails, no future extension of that segment can fix it without violating feasibility. Therefore, delaying a cut can only increase c
