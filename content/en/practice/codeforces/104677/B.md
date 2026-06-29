---
title: "CF 104677B - War on Two Fronts"
description: "We are given two separate groups of five integers. Each group represents five people on one side of a classroom, and each person contributes a fixed number of points. Darcy is allowed to choose exactly one of the two groups."
date: "2026-06-29T14:32:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104677
codeforces_index: "B"
codeforces_contest_name: "Sugar Sweet \u2764\ufe0f"
rating: 0
weight: 104677
solve_time_s: 55
verified: true
draft: false
---

[CF 104677B - War on Two Fronts](https://codeforces.com/problemset/problem/104677/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two separate groups of five integers. Each group represents five people on one side of a classroom, and each person contributes a fixed number of points.

Darcy is allowed to choose exactly one of the two groups. After choosing a group, he removes exactly one element from that group, and collects the sum of the remaining four numbers. The task is to maximize the points he can obtain across both choices.

So conceptually, we compute two candidate scores: for each group, we take the total sum and subtract one chosen element. Since we are allowed to remove any single element, the optimal choice inside a group is always to remove the smallest value, because that preserves the largest possible remaining sum.

The input size is fixed and tiny: exactly ten numbers total. This removes any concern about efficiency, and shifts the focus entirely to correctly identifying the best removal choice.

There are no tricky scaling constraints. Any solution up to constant time per input is sufficient. Even a brute-force enumeration of all removals would be instantaneous.

The main subtle failure mode comes from forgetting that the removal choice is independent inside each group. A wrong approach might try to compare elements across groups or assume a global best element to remove, which does not reflect the rule that only one group is chosen.

A concrete incorrect approach would be to always remove the smallest number across both groups combined. For example, if one group is `[100, 100, 100, 100, 1]` and the other is `[50, 50, 50, 50, 50]`, removing the global minimum (1) forces choosing the first group, giving 400, but the second group yields 250 which is worse, so this example does not break it. However, if the structure were different, such reasoning can fail because the decision is “choose a group first, then remove within it”, not “remove globally”.

The correct structure is per-group optimization followed by a final maximum.

## Approaches

The brute-force idea is straightforward: for each of the two groups, try removing each of the five elements and compute the resulting sum of the remaining four. This produces ten candidate values in total, and we take the maximum. This is correct because it explicitly enumerates every valid action Darcy can take.

This approach runs in constant time because the input size is fixed. Even if we generalized it to n elements per group, it would require O(n) per group, which is still trivial for n up to moderate constraints. The redundancy comes from recomputing sums repeatedly.

The key observation is that recomputing full sums is unnecessary. Once we know the sum of a group, removing an element simply subtracts that value. The best result is therefore the total sum minus the minimum element in that group. This reduces each group to a single computation: sum and minimum.

We compute both group scores independently and then take the maximum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the five integers of the first group and compute their sum and minimum value. The minimum identifies the best element to remove because removing anything larger would waste potential score.
2. Compute the best achievable score for the first group as total sum minus its minimum element.
3. Repeat the same process for the second group, independently. The two groups do not interact, so no cross-group comparison is done during computation.
4. Compare the two resulting scores and output the larger one.

### Why it works

Within a single group, any valid action corresponds to selecting exactly one element to discard. Every such action produces a result equal to the total sum minus that element. Since subtraction is monotone, the smallest element produces the largest remaining sum. Therefore, the per-group optimum is uniquely determined by the minimum element. The global optimum is the maximum of the two independent group optima because Darcy must choose exactly one group.

## Python Solution

```python
import sys
input = sys.stdin.readline

a = list(map(int, input().split()))
b = list(map(int, input().split()))

sum_a = sum(a)
sum_b = sum(b)

best_a = sum_a - min(a)
best_b = sum_b - min(b)

print(max(best_a, best_b))
```

The code reads both groups, computes their sums and minima, and then derives the best achievable score per group by subtracting the smallest element. The final output is simply the larger of the two computed values.

A common mistake would be recomputing sums inside a loop for each removal candidate, but here we avoid that entirely by separating aggregation (sum and min) from decision-making (subtract min).

## Worked Examples

### Example 1

Input:

```
5 1 5 5 5
3 3 2 2 2
```

For the first group, the sum is 21 and the minimum is 1, so the best score is 20. For the second group, the sum is 12 and the minimum is 2, so the best score is 10.

| Group | Sum | Min | Best Score |
| --- | --- | --- | --- |
| A | 21 | 1 | 20 |
| B | 12 | 2 | 10 |

The output is 20 because the first group is better.

This confirms the invariant that only the smallest removable element matters.

### Example 2

Input:

```
10 10 10 10 1
7 8 9 10 6
```

For the first group, sum is 41 and min is 1, giving 40. For the second group, sum is 40 and min is 6, giving 34.

| Group | Sum | Min | Best Score |
| --- | --- | --- | --- |
| A | 41 | 1 | 40 |
| B | 40 | 6 | 34 |

The output is 40, confirming that even a high-sum second group cannot beat the first after optimal removal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only fixed-size arrays of length five are processed, each requiring constant-time sum and minimum computation |
| Space | O(1) | Only a constant number of variables are stored |

The solution easily fits within limits since the input size is constant. Even if scaled, it would remain linear in group size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    sum_a = sum(a)
    sum_b = sum(b)

    best_a = sum_a - min(a)
    best_b = sum_b - min(b)

    return str(max(best_a, best_b))

# provided sample
assert run("5 1 5 5 5\n3 3 2 2 2\n") == "20"

# all equal
assert run("1 1 1 1 1\n2 2 2 2 2\n") == "8"

# second group better
assert run("1 1 1 1 10\n9 9 9 9 1\n") == "36"

# minimum edge case
assert run("1 2 3 4 5\n5 4 3 2 1\n") == "14"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | 20 | basic correctness |
| all equal | 8 | symmetry and correct subtraction |
| mixed dominance | 36 | choosing correct group |
| reversed order | 14 | consistent min selection |

## Edge Cases

A key edge case is when both groups contain identical values. For example, if both groups are `[3, 3, 3, 3, 3]`, the sum is 15 and removing any element yields 12. The algorithm computes sum 15 and min 3 for both groups, producing identical results and correctly returning 12.

Another edge case is when the minimum element is unique and much smaller than others. For `[100, 100, 100, 100, 1]`, the algorithm correctly identifies that removing 1 yields 400, whereas removing any 100 yields 301. Because it only depends on the minimum, no enumeration is needed and the correct maximum is guaranteed.

A final case is when the best group is not the one with the largest total sum. For `[10, 10, 10, 10, 1]` versus `[9, 9, 9, 9, 9]`, totals are 41 and 45 respectively, but after optimal removal the results are 40 and 36. The algorithm correctly prioritizes post-removal value rather than raw sum.
