---
title: "CF 180F - Mathematical Analysis Rocks!"
description: "Each student initially owns a single notebook. There is a fixed hidden permutation p over students, meaning every student has exactly one “best friend” and every student is the best friend of exactly one other student."
date: "2026-06-03T00:50:04+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 180
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 116 (Div. 2, ACM-ICPC Rules)"
rating: 1200
weight: 180
solve_time_s: 35
verified: false
draft: false
---

[CF 180F - Mathematical Analysis Rocks!](https://codeforces.com/problemset/problem/180/F)

**Rating:** 1200  
**Tags:** constructive algorithms, implementation, math  
**Solve time:** 35s  
**Verified:** no  

## Solution
## Problem Understanding

Each student initially owns a single notebook. There is a fixed hidden permutation `p` over students, meaning every student has exactly one “best friend” and every student is the best friend of exactly one other student. Because it is a permutation, following best-friend pointers repeatedly just walks along disjoint directed cycles, with no branching and no missing nodes.

The process describes how notebooks move along this permutation over time. On day 1, every student reads their own notebook. From day 2 onward, all notebooks are simultaneously passed along the permutation: a notebook owned by student `i` moves to student `p[i]` on the next day. This means that on day `t`, the notebook that started at `i` is located at `p^(t-1)[i]`.

We are not given `p`. Instead, we are given two full snapshots: where each notebook is located on day 3 and on day 4. These are permutations `a` and `b`. The value `a[i]` is the student holding notebook `i` on day 3, and `b[i]` is the student holding notebook `i` on day 4. Since day transitions are governed by the same hidden permutation, we must reconstruct `p`.

The key constraint is `n ≤ 10^5`, which rules out any solution that tries to simulate the process for each possible candidate mapping or for each student independently in quadratic time. We need something linear or close to linear, since about `10^8` simple operations is already borderline in Python.

A subtle but important structural property is that `a` and `b` are both permutations. That guarantees that every student appears exactly once in each array, so each snapshot is a bijection between notebooks and students.

A typical failure case for naive thinking is assuming we can track each notebook independently by guessing where it goes from day 3 to day 4 without leveraging permutation structure. For example, if we tried to deduce `p[i]` by “looking where student i is between day 3 and day 4”, we would mix up roles of notebooks and students, because arrays describe positions of notebooks, not transitions of students.

## Approaches

A direct brute-force idea is to try all possible permutations `p` and simulate the movement of all notebooks from day 1 to day 4, then check whether the resulting day 3 and day 4 configurations match `a` and `b`. This is theoretically correct, but there are `n!` candidate permutations, and even checking one requires at least `O(n)` simulation. This becomes astronomically large even for `n = 10`, so it is immediately infeasible.

The key observation comes from rewriting the process in terms of function composition. Let `p` act on notebook positions. Then day 3 corresponds to applying `p^2` to the initial identity configuration, and day 4 corresponds to applying `p^3`. We are given both `p^2` and `p^3`, but not `p`.

This suggests a direct relationship: composing with `p` transforms day 3 into day 4. In other words, if we interpret `a` as a permutation describing where each notebook goes on day 3, and `b` as the same for day 4, then applying `p` maps day 3 configuration to day 4 configuration.

More concretely, if notebook `i` is at student `a[i]` on day 3, then on day 4 that same notebook must be at student `b[i]`. Since a single application of `p` moves the holder forward, we get the constraint:

`p[a[i]] = b[i]`.

This gives a direct reconstruction rule: for each notebook `i`, we know exactly how the student currently holding it (on day 3) moves to the next holder (on day 4). That is precisely the definition of `p`.

So the entire problem reduces to matching transitions between two permutations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We exploit the fact that every notebook transition from day 3 to day 4 corresponds to exactly one application of the hidden permutation `p`.

1. Build the inverse mapping of `a`, so we can quickly locate which notebook is currently at each student on day 3.

This is necessary because `a[i]` is “notebook i is at student a[i]”, but we want to reason from student to notebook.
2. For each student `x`, determine which notebook is currently at `x` on day 3 by using the inverse of `a`.
3. That notebook moves to student `b[notebook]` on day 4.

This gives a direct transition from `x` to `b[notebook]`.
4. Assign `p[x] = b[notebook]` for every student `x`.

This constructs the permutation edge-by-edge.
5. Output the resulting array `p`.

The crucial point is that every student contributes exactly one constraint, and these constraints collectively form the full permutation without ambiguity.

### Why it works

At day 3, each student holds exactly one notebook, and `a` encodes this bijection. Using its inverse, we recover the unique notebook at each student. On day 4, the same notebook must appear exactly once again due to the permutation structure, and its position is given by `b`. Since each notebook moves according to the same hidden permutation `p`, the transition from its day 3 holder to its day 4 holder must be exactly one application of `p`. Because every student appears exactly once in day 3, we recover all edges of `p` without conflict.

## Python Solution
