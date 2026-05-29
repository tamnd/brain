---
title: "CF 327E - Axis Walking"
description: "We are given a multiset of positive segment lengths. Any permutation of these lengths defines a walk along the number line starting from 0, where we cumulatively add each chosen segment."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "combinatorics", "constructive-algorithms", "dp", "meet-in-the-middle"]
categories: ["algorithms"]
codeforces_contest: 327
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 191 (Div. 2)"
rating: 2300
weight: 327
solve_time_s: 85
verified: true
draft: false
---

[CF 327E - Axis Walking](https://codeforces.com/problemset/problem/327/E)

**Rating:** 2300  
**Tags:** bitmasks, combinatorics, constructive algorithms, dp, meet-in-the-middle  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of positive segment lengths. Any permutation of these lengths defines a walk along the number line starting from 0, where we cumulatively add each chosen segment. After each segment, we “pause” at the current position, and these pause positions are exactly the prefix sums of the permutation.

The goal is to count how many permutations avoid a small set of forbidden positions. A permutation is valid if none of its prefix sums ever equals one of the forbidden coordinates.

A key structural point is that the total sum of all segments is fixed and equals the destination point, so every valid permutation is a reordering of the same steps with the same final endpoint. The only thing that changes is the order in which prefix sums appear.

The constraints drive the solution style. With $n \le 24$, the factorial space is far too large for direct enumeration, so any solution must avoid iterating over permutations. At the same time, $k \le 2$ makes the “bad conditions” extremely small, which strongly suggests tracking states only relative to whether we have hit one or both forbidden sums. This combination usually signals a meet-in-the-middle or DP over subsets approach where prefix sums are encoded implicitly.

A subtle edge case arises when a forbidden number equals the total sum $d$. In that case every permutation is immediately invalid because the last prefix sum is always $d$. Another tricky case is when a forbidden value is unreachable by any subset sum of the given array; then it has no effect, but a naive DP might still spend effort tracking it unnecessarily.

Finally, duplicates in the array matter only combinatorially: different permutations of identical values are distinct, so we must count permutations over indices, not over values.

## Approaches

A brute-force solution would generate all $n!$ permutations, compute prefix sums for each, and check whether any prefix sum equals a forbidden value. This is correct but immediately infeasible since $24!$ is astronomically large.

The key observation is that the process depends only on subset sums along prefixes, and prefix sums are just sums of chosen elements in a particular order. Instead of thinking in terms of permutations, we can think in terms of choosing a subset as the first part of the permutation. Every permutation corresponds to a sequence of growing subsets, and we can encode DP states by which subset has been used and what sum it produces.

Since $n$ is small but exponential, we use subset DP. The additional simplification comes from the fact that there are at most two forbidden prefix sums. This allows us to track whether we have hit 0, 1, or 2 forbidden values during construction.

We define a DP over subsets that accumulates both the current sum and whether a forbidden sum has been triggered. However, storing raw sums up to $10^9$ is impossible, so we instead precompute all subset sums implicitly during DP transitions. The structure is standard: we build subsets incrementally and maintain a map from subset to its sum, and then propagate counts.

A more efficient viewpoint is to use DP where state is a bitmask and transitions add one element. We maintain for each mask whether its prefix-sum history has already hit a bad value, and we update it when adding a new element by checking whether the new cumulative sum equals a forbidden value.

The final answer is the number of full masks (all elements used) that never triggered a forbidden prefix sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n! \cdot n)$ | $O(1)$ | Too slow |
| Optimal | $O(n \cdot 2^n)$ | $O(2^n)$ | Accepted |

## Algorithm Walkthrough

We build a DP over subsets where each state represents a partial permutation encoded as a bitmask.

1. Precompute the total sum of all elements. If this sum is in the forbidden set, we immediately return 0 because every permutation ends there.
2. Store forbidden values in a set for O(1) membership checks. Since $k \le 2$, this is constant-time in practice.
3. Define a DP table where `dp[mask]` stores all reachable states for that subset, grouped by current prefix sum. We represent this efficiently using a dictionary per mask: sum → count of ways to reach this subset with that sum.
4. Initialize `dp[0] = {0: 1}` since the empty prefix has sum 0 in exactly one way.
5. Iterate over all masks in increasing order of size. For each mask, try adding each unused element. If we extend a state with current sum `s` by adding value `a[i]`, we form new sum `s + a[i]`. If this new sum is forbidden, we discard this transition.
6. Otherwise, we add the transition to `dp[mask | (1 << i)]`, accumulating counts.
7. After processing all masks, the answer is the sum of counts in `dp[(1 << n) - 1]`.

The key reason this works is that each permutation corresponds uniquely to a path through subset masks where each step adds exactly one new element, and the DP enumerates all such paths while filtering invalid prefix sums locally at each transition.

### Why it works

Every permutation is a unique ordering of indices, and every ordering corresponds to a unique chain of subset masks from empty to full set. The DP counts each chain exactly once because each transition appends one unused element. Since we reject a transition immediately when it creates a forbidden prefix sum, no invalid permutation can reach the final state. Conversely, any valid permutation never triggers a rejection, so its path is fully counted.

## Python Solution

```
PythonRun
```

The DP is structured around subsets, and each state explicitly tracks reachable prefix sums for that subset. The early termination when hitting a forbidden total sum removes a universal invalid case.

The inner loop carefully avoids revisiting used elements by checking the mask bit. The transition updates both the subset and the running sum, which is the only value needed to validate constraints.

A common pitfall is assuming sums are unique per mask, which is false because different permutations of the same subset can produce different intermediate prefix sums.

## Worked Examples

### Example 1

Input:

```

```

We track dp states by mask and sum.

| Step | Mask | Sum states | Action |
| --- | --- | --- | --- |
| init | 000 | {0:1} | start |
| add 2 | 001 | {2:1} | valid |
| add 3 | 010 | {3:1} | valid |
| add 5 | 100 | {5:1} | valid |
| expand | 011,101,110,... | filtered | remove sums hitting 5 or 7 |
| final | 111 | {10:1} | one valid permutation |

Only one ordering avoids forbidden prefix sums.

This confirms that forbidden sums prune entire branches early, not just final states.

### Example 2

Input:

```
3
1 2 3
1
6
```

| Step | Mask | Sum states | Action |
| --- | --- | --- | --- |
| init | 000 | {0} | start |
| build | all subsets | multiple sums | expand |
| invalid pruning | any path hitting 6 | removed | prune |
| final | 111 | valid counts | remaining permutations |

This shows how a forbidden value that equals the total sum eliminates all permutations immediately.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot 2^n \cdot S)$ | each subset expands |
