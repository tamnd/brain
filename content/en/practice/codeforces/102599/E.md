---
title: "CF 102599E - M~--- \u043c\u043d\u043e\u0433\u043e\u043c\u0435\u0440\u043d\u043e\u0441\u0442\u044c"
description: "We are given several axis-aligned boxes in an M-dimensional integer coordinate space. A box is described independently in each dimension by a closed interval, so a point belongs to a box only when every coordinate falls inside the corresponding interval."
date: "2026-07-31T05:49:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102599
codeforces_index: "E"
codeforces_contest_name: "The fifth Lipetsk collegiate programming contest. Finals. 8-11 form"
rating: 0
weight: 102599
solve_time_s: 233
verified: false
draft: false
---

[CF 102599E - M~--- \u043c\u043d\u043e\u0433\u043e\u043c\u0435\u0440\u043d\u043e\u0441\u0442\u044c](https://codeforces.com/problemset/problem/102599/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 53s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several axis-aligned boxes in an M-dimensional integer coordinate space. A box is described independently in each dimension by a closed interval, so a point belongs to a box only when every coordinate falls inside the corresponding interval.

The task is not to find the size of the union of these boxes. Instead, we need the number of integer points that are contained in exactly one box less than the total number of boxes. In other words, every valid point is missing from exactly one box and belongs to all the others.

The constraints are designed around the product of the number of boxes and the number of dimensions. Although both values can individually reach 200000, their product cannot exceed 200000. This immediately rules out algorithms that depend on the number of boxes multiplied by another factor such as the coordinate range, and it makes an O(NM) solution the natural target. A solution that enumerates points in space is impossible because coordinates can range over millions and the dimension can be large.

The main hidden difficulty is that the answer is about almost complete overlap. A direct geometric sweep in high dimensions is not realistic. The solution needs to avoid handling the whole space and instead work with intersections of the given boxes.

There are several boundary cases where incorrect implementations often fail. The first is that intervals are closed. For example:

```
2 1
1 2
2 3
```

The answer is `2`. The integer points are 1, 2, and 3. Point 2 belongs to both intervals, while 1 and 3 belong to exactly one interval. A solution using length `b-a` instead of the number of integer points `b-a+1` would produce the wrong result.

Another common mistake is forgetting that a point inside every box must not be counted. Consider:

```
2 1
1 5
2 4
```

The points inside exactly one interval are 1 and 5, so the answer is `2`. If we only add the intersections obtained by removing one box, the fully overlapping segment would be counted twice and would need to be removed.

A final edge case is when removing any single box leaves an empty intersection. For example:

```
3 1
1 2
4 5
7 8
```

No point belongs to two boxes, so the answer is `0`. The algorithm must correctly handle intersections with zero size instead of multiplying negative lengths.

## Approaches

The straightforward approach is to look at every possible point and count how many boxes contain it. This is correct because it directly follows the definition of the answer. However, it cannot work here. Even in one dimension, an interval can contain up to two million possible coordinates, and in multiple dimensions the number of points becomes exponential in M.

A better way to think about the condition is to reverse it. A point is counted exactly when there is one box that does not contain it and every other box does. If we choose the missing box, the point must lie inside the intersection of all remaining boxes.

For every box i, let S_i be the set of integer points inside every box except i. If a point belongs to exactly N-1 boxes, it appears in exactly one of these sets. A point belonging to all N boxes appears in every S_i, so it is counted N times and must be removed.

The answer becomes:

```
sum(size of intersection of all boxes except i) - N * size(of intersection of all boxes)
```

The remaining task is computing every leave-one-out intersection efficiently.

For one dimension, removing box i means finding the maximum left endpoint and minimum right endpoint among all other boxes. Prefix and suffix arrays allow these values to be obtained in constant time for every i. Doing this independently for every dimension gives an O(NM) algorithm, which matches the constraint.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Impossible to express efficiently because it depends on the coordinate volume | O(1) | Too slow |
| Optimal | O(NM) | O(NM) | Accepted |

## Algorithm Walkthrough

1. Read all intervals and store the lower and upper bounds for every box in every dimension. We need access to the same dimension across all boxes, because each dimension contributes one independent factor to the final intersection size.
2. Initialize the answer contribution of every removed box to one. For a fixed removed box, its final intersection size is the product of its valid lengths in every dimension.
3. Process each dimension separately. Build prefix maximums of left endpoints and prefix minimums of right endpoints. Also build suffix maximums and suffix minimums. These arrays describe the intersection of all boxes before or after a given index.
4. For every box i, combine the prefix and suffix information to obtain the intersection of all boxes except i in this dimension. The lower bound is the larger of the two available maximums, and the upper bound is the smaller of the two available minimums.
5. Convert this one-dimensional intersection into a count of integer coordinates. If the upper bound is smaller than the lower bound, the count is zero. Otherwise the count is `upper - lower + 1`. Multiply the stored contribution of box i by this value.
6. During the same dimension processing, compute the intersection of all boxes by taking the global maximum left endpoint and global minimum right endpoint. Multiply its size into a separate variable.
7. After all dimensions are processed, add all leave-one-out intersection sizes and subtract N times the full intersection size.

The invariant is that after processing some dimensions, the stored value for a removed box i equals the number of integer points satisfying all processed dimensions for every box except i. Each dimension is independent, so multiplying the dimension contributions gives the full multidimensional intersection size. The final subtraction removes exactly the points that were counted too many times because they belong to every box.

(Continued in the next message with the Python solution, walkthrough, complexity analysis, tests, and edge case traces.)
