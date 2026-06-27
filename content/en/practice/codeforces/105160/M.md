---
title: "CF 105160M - \u8521\u5149\u6570\u7ec4"
description: "We are given an array of exactly four positive integers, each between 1 and 9. The task is to decide whether this array matches a hidden pattern defined by a string “USST”, where identical characters in the string enforce equality constraints between corresponding positions in…"
date: "2026-06-27T11:03:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105160
codeforces_index: "M"
codeforces_contest_name: "2024 University of Shanghai for Science and Technology(USST) Freshman Challenge Contest"
rating: 0
weight: 105160
solve_time_s: 28
verified: false
draft: false
---

[CF 105160M - \u8521\u5149\u6570\u7ec4](https://codeforces.com/problemset/problem/105160/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of exactly four positive integers, each between 1 and 9. The task is to decide whether this array matches a hidden pattern defined by a string “USST”, where identical characters in the string enforce equality constraints between corresponding positions in the array, and different characters enforce inequality constraints.

In simpler terms, each position in the string labels one array index. If two positions in the string have the same letter, their corresponding array values must be equal. If two positions have different letters, their values must be different. The string for this problem is fixed as “USST”, so the constraint structure is fixed as well.

The string “USST” implies four positions with the following relationships. The first and second positions correspond to different letters, so they must differ. The second, third, and fourth positions correspond to the letters S, S, and T respectively, so position 2 and 3 must be equal, position 3 and 4 must differ, and position 2 and 4 must differ as well. Combining these, we get a small system of equalities and inequalities over four array elements.

Because the array size is constant, there is no asymptotic scaling issue. Any solution that performs a constant amount of checks is sufficient. The constraint 1 ≤ ai ≤ 9 only ensures values are small integers, but it does not change the nature of the logic.

The main failure mode in naive thinking is to only check equalities implied by repeated letters and forget the necessary inequality constraints. For example, treating “USST” as only “a2 = a3” would incorrectly accept arrays like `[1, 2, 2, 2]`, even though position 2 equals position 4 violates the fact that S and T are different characters.

Another common mistake is to check only pairwise uniqueness or only partial constraints. For instance, rejecting arrays where all values are distinct would be wrong because valid configurations require some equalities but not full distinctness.

## Approaches

A brute-force interpretation would treat each position as belonging to a label class and then check all pairs of indices: if their characters match, enforce equality; otherwise enforce inequality. In general, for longer strings, this becomes a graph constraint problem where we verify consistency across all pairs. For this problem, with only four positions and a fixed pattern, this reduces to checking a constant number of conditions.

If we explicitly enumerate all pair constraints, we check up to 6 pairs: (1,2), (1,3), (1,4), (2,3), (2,4), (3,4), and verify whether each pair must be equal or not based on the USST pattern. This is already O(1), so brute force is effectively optimal here.

The key observation is that we do not need any abstraction like mapping characters to IDs or building data structures. The structure is fixed, so we can directly hardcode the constraints implied by the pattern and verify them.

The brute-force approach works because the problem size is constant, but it becomes conceptually heavy if generalized. The direct constraint checking reduces everything to a few comparisons.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force pair checking | O(1) | O(1) | Accepted |
| Direct constraint evaluation | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

The USST pattern corresponds to four positions:

Position 1: U

Position 2: S

Position 3: S

Position 4: T

From this we derive constraints:

1. Positions 2 and 3 must be equal because both are S.
2. Positions 1 and 2 must differ because U and S are different.
3. Positions 1 and 3 must differ for the same reason.
4. Positions 2 and 4 must differ because S and T are different.
5. Positions 3 and 4 must differ because S and T are different.

We only need to verify these conditions on the given array.

The algorithm proceeds as follows.

1. Read the four integers into an array a.
2. Check whether a[1] equals a[2]. If not, reject immediately because S must repeat.
3. Check whether a[0] differs from a[1]. If not, reject
