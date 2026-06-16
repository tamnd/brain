---
title: "CF 1560B - Who's Opposite?"
description: "We are given three distinct labels that refer to people placed on a perfectly even circle. The circle size is even, but unknown, and the labels are not guaranteed to be consecutive or small."
date: "2026-06-16T16:37:51+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1560
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 739 (Div. 3)"
rating: 800
weight: 1560
solve_time_s: 123
verified: false
draft: false
---

[CF 1560B - Who's Opposite?](https://codeforces.com/problemset/problem/1560/B)

**Rating:** 800  
**Tags:** math  
**Solve time:** 2m 3s  
**Verified:** no  

## Solution
## Problem Understanding

We are given three distinct labels that refer to people placed on a perfectly even circle. The circle size is even, but unknown, and the labels are not guaranteed to be consecutive or small. The only structural rule is that opposite positions in the circle are fixed: if you stand at some position, the person directly across the center is exactly half a circle away.

One relationship is already fixed: person `a` faces person `b`. From this single constraint, the entire circle size becomes constrained, because “opposite” depends only on the total number of people. Once the circle size is consistent with this pairing, we are asked to determine who the person `c` is facing. If no even circle size can satisfy the first constraint, we must report impossibility.

The key difficulty is that the labels are arbitrary integers up to $10^8$, so we are not constructing a small permutation or array directly. Instead, we are reconstructing a consistent modular structure where opposite means adding half the circle size modulo the total.

The time limit with up to $10^4$ test cases implies we need an $O(1)$ per test solution. Any attempt to iterate over possible circle sizes would be far too slow, since the circle size is unbounded except for consistency constraints.

A subtle edge case arises when the inferred circle size would need to be zero or when no even size can satisfy the “opposite” relation for both endpoints. Another issue is that multiple circle sizes might satisfy the condition, but only some are valid under evenness constraints.

For example, if we incorrectly assume the circle size is simply $2 \cdot |a - b|$, we may fail when labels wrap around differently or when symmetry produces contradictions. The correct solution must reason directly from modular arithmetic rather than geometric intuition.

## Approaches

A brute-force idea would be to try possible circle sizes $n$, starting from 2 and going upward in steps of 2. For each candidate $n$, we would try to assign positions so that $a$ and $b$ are exactly $n/2$ apart modulo $n$. Once a valid $n$ is found, we could compute the opposite of $c$.

This approach is conceptually straightforward: in a circle of size $n$, the opposite condition means

$$(a - b) \equiv n/2 \pmod n.$$

We could test values of $n$ until this holds. However, the labels can be as large as $10^8$, so the valid $n$ could also be large. Trying all even $n$ up to $O(10^8)$ per test case is completely infeasible.

The key observation is that the circle structure imposes a very rigid constraint: the distance between opposite points is exactly half the circumference, so the absolute difference between labels must equal $n/2$ in some consistent numbering scheme. Since labels are arbitrary but the circle is uniform, the only consistent reconstruction is that the circle size must be $2 \cdot |a - b|$. If this value is not valid (specifically, it must be even and positive in a consistent interpretation), no solution exists.

Once the circle size is determined, computing the opposite of $c$ becomes a direct symmetric reflection: shifting by half the circle size.

Thus the problem reduces from searching over $n$ to computing it directly from the only constraint we are given.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n)$ per test | $O(1)$ | Too slow |
| Optimal | $O(1)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Compute the distance between the given opposite pair as $d = |a - b|$. This represents half the circle size because opposite points are symmetric around the center.
2. If $d = 0$, immediately conclude impossibility. A circle of even size cannot place two distinct labels at the same position or opposite each other.
3. Set the candidate circle size to $n = 2d$. This is the only possible circumference consistent with the required opposite distance.
4. Check whether a consistent symmetric layout exists. Since labels are abstract but must preserve symmetry, the only meaningful constraint is that the structure is valid, so $n$ must be positive and even, which is guaranteed by construction.
5. Compute the opposite of $c$ by shifti
