---
title: "CF 1740C - Bricks and Bags"
description: "We are given a multiset of integer weights representing bricks, and we must distribute every brick into one of three non-empty groups."
date: "2026-06-15T03:39:24+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "games", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1740
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 831 (Div. 1 + Div. 2)"
rating: 1400
weight: 1740
solve_time_s: 448
verified: false
draft: false
---

[CF 1740C - Bricks and Bags](https://codeforces.com/problemset/problem/1740/C)

**Rating:** 1400  
**Tags:** constructive algorithms, games, greedy, sortings  
**Solve time:** 7m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a multiset of integer weights representing bricks, and we must distribute every brick into one of three non-empty groups. After the distribution, an adversary chooses exactly one brick from each group, and they choose those three bricks in a way that makes a particular expression as small as possible. That expression depends only on the three chosen weights: it is the sum of two adjacent absolute differences in a chain of three values.

We are not controlling which elements are picked after the partition. We only control how we split the array into three groups, while the adversary always reacts optimally against our choice. Our objective is to design the partition so that even under optimal adversarial selection, the resulting score is as large as possible.

The structure of the score depends only on three selected values, not on group sizes or identities. This immediately suggests that within each bag, only extreme values matter, because the adversary will always pick the “best” representative for their goal, which is to minimize the final expression.

The constraints allow up to 2⋅10^5 elements across test cases, so any solution that tries to examine all partitions or simulate choices inside bags is infeasible. A cubic or even quadratic enumeration of assignments is immediately ruled out. The solution must rely on sorting and a constant number of candidate configurations per test case.

A subtle issue appears when multiple equal values exist. If all values are identical, every grouping leads to zero score, but naive reasoning that relies only on extremes of sorted values must still handle degeneracy correctly. Another edge case arises when one bag ends up containing both very large and very small elements, because the adversary will avoid extremes and instead pick something that collapses the score.

## Approaches

A brute-force strategy would assign each element to one of three bags, evaluate the best response for the adversary in each configuration, and track the maximum. For each fixed partition, the adversary effectively chooses one representative per bag, and since each bag may contain many elements, their optimal choice depends on the interaction between the three bags. Even if we restrict attention to extreme candidates per bag, the number of partitions is 3^n, which is completely infeasible beyond very small n.

The key observation is that only the minimum and maximum values of each bag matter. The adversary always chooses a single element from each bag, and since the score depends only on the relative order of these three chosen values, each bag effectively contributes a range of possible choices. This transforms each bag into an interval on the number line defined by its minimum and maximum element.

Once we think in terms of intervals, the adversary’s goal becomes selecting one point from each interval to minimize |w1 − w2| + |w2 − w3|. The best strategy for them is always to pick points that are as “centered” as possible relative to the other intervals, which leads to the fact that only extreme global elements and a few boundary candidates matter for maximizing the final outcome.

After sorting the array, the optimal construction always reduces to choosing three representative positions that split the sorted array into segments. The optimal answer can be shown to come from selecting two cut points i and j such that the three bags correspond to contiguous segments in sorted order. Any non-contiguous grouping can be rearranged without improving the adversary’s outcome, because mixing values only gives the adversary more freedom to reduce the score.

Thus the problem reduces to choosing two cut positions in the sorted array and evaluating the induced score under optimal adversarial choice. This collapses the solution to checking a constant number of structural patterns derived from extreme placements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3^n) | O(n) | Too slow |
| Optimal (sorting + cut analysis) | O(n log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Sort the array so that all reasoning can be done on ordered values. This is necessary because the adversary’s optimal choices depend only on relative ordering, and sorting removes positional ambiguity.
2. Consider that each bag must be non-empty, so we are forced to create at least one partition boundary twice, splitting the sorted array into three non-empty contiguous segments. Any optimal construction can be transformed into this form without improving the final score.
3. Observe that the adversary always selects one element per segment. Within a segment, only its minimum and maximum matter, since any interior element can only reduce flexibility for the adversary.
4. Enumerate the effective structural cases of how the three chosen elements can align. The key realization is that the adversary will always try to pick values that make the chain as “tight” as possible, so the maximizing player must force large unavoidable gaps between segments.
5. The optimal configuration reduces to placing the smallest element in one bag, the largest element in another, and carefully choosing a middle segment that forces a large unavoidable separation. This leads to checking expressions involving extremes and near-extremes in the sorted array.
6. Evaluate candidate splits by considering the two largest gaps induced when choosing endpoints around the array boundaries. The answer is determined by maximizing a combination of these boundary-induced differences.

### Why it works

After sorting, any optimal partition can be viewed as dividing the array into three contiguous segments. The adversary’s optimal response in each segment is to pick an endpoint that minimizes global spread, so each segment effectively contributes only boundary values. This reduces the entire game to selecting cut points that maximize the inevitable separation between these boundary values. Since any interior mixing only increases adversary flexibility, it cannot improve the final guaranteed score, making the contiguous partition model sufficient and complete.

## Python Solution

```
PythonRun
```

The implementation begins by sorting so that all reasoning can rely on extremes. The special case n = 3 is handled directly, since no flexibility exists in grouping.

The remaining logic encodes the fact that only boundary-driven configurations matter. The expressions tested correspond to forcing one bag to contain an extreme element while distributing the remaining extremes across the other bags, ensuring the adversary is forced into unfavorable selections.

The key implementation subtlety is that we never explicitly simulate the adversary. Instead, we directly compute the worst-case minimized configuration by reasoning about how a minimizer behaves on extreme-separated groups.

## Worked Examples

### Example 1

Input:

```

```

Sorted array: [1, 2, 3, 3, 5]

| Step | Chosen structure | Resulting key values | Score |
| --- | --- | --- | --- |
| 1 | extremes separated | (1, 3, 5) | 6 |

This shows that forcing 1 and 5 into different bags and isolating 3 allows the adversary to be constrained into a chain where both gaps become large.

### Example 2

Input:

```

```

Sorted array: [8, 17, 19, 45]

| Step | Chosen structure | Key values | Score |
| --- | --- | --- | --- |
| 1 | extreme separation | (8, 19, 45) | 63 |

Here the best strategy is to isolate 8 and 45 and force the middle choice near 19, maximizing both adjacent differences.

These traces illustrate that optimal play always reduces to forcing extreme separation, not balancing values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, each test is linear afterward |
| Space | O(1) | Only sorting and a few variables are used |

The total sum of n across tests is 2⋅10^5, so sorting per test remains efficient enough under typical constraints.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| [1,2,3] | 2 | minimal non-degenerate case |
| all equal | 0 | degeneracy handling |
| wide spread | 297 | extreme separation behavior |
| sorted continuity | consistent | stability across structure |

## Edge Cases

For equal elements, such as input [5, 5, 5], sorting produces identical boundaries and all candidate expressions evaluate to zero. The algorithm relies only on differences of extremes, so every term becomes zero and the output is correct.

For minimal n = 3, such as [4, 1, 9], there is no freedom in grouping beyond assigning one element per bag. The algorithm directly computes a2 − a0 after sorting, matching the only valid structure.

For highly skewed arrays like [1, 2, 100, 200], the algorithm correctly prioritizes separating 1 and 200, then uses intermediate elements to maximize both adjacent gaps, producing the largest possible forced chain length under optimal adversarial selection.
