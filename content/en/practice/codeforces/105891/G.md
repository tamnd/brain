---
title: "CF 105891G - student"
description: "We are given a row of students, each with a fixed score. A teacher repeatedly selects a student and checks whether that student can be removed from the row."
date: "2026-06-21T15:10:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105891
codeforces_index: "G"
codeforces_contest_name: "The 13th Shaanxi Provincial Collegiate Programming Contest"
rating: 0
weight: 105891
solve_time_s: 72
verified: true
draft: false
---

[CF 105891G - student](https://codeforces.com/problemset/problem/105891/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a row of students, each with a fixed score. A teacher repeatedly selects a student and checks whether that student can be removed from the row. Whether student `i` disappears depends only on the relative values of students on the left and right side of `i` at that moment.

A student becomes removable if the sequence around them is “mixed” in a specific way. Concretely, the student disappears if there is evidence of both higher and lower scores split across the left and right sides in either of two symmetric patterns. One pattern requires a not-smaller value on the left and a not-greater value on the right, and the other swaps these roles.

The teacher can choose removals in any order, and after a removal the remaining students shift, so the conditions are evaluated dynamically. The goal is to maximize how many students can be removed, or equivalently to minimize how many can never be removed no matter how cleverly we choose the deletion order.

The constraints allow up to `2 × 10^5` students, so any solution that tries all deletions or recomputes conditions repeatedly with scans over the array is immediately too slow. A quadratic or even near-quadratic dynamic simulation over removals cannot work. We need a characterization of which elements are inherently “stable” under all valid deletion orders.

A subtle edge case appears when the array is monotone. In a strictly increasing array like `1 2 3 4 5`, every middle element has both smaller elements on the left and larger elements on the right, so many of them become removable. However, endpoints behave differently because one side is empty, which prevents the condition from being satisfied. Any correct solution must handle boundary positions correctly.

Another tricky case is when values repeat, for example `3 1 3 2 3`. Local comparisons alone are not sufficient; what matters is whether there exists at least one strictly larger and one strictly smaller element on opposite sides of a position.

## Approaches

A direct simulation would repeatedly scan the array, find all currently removable students, delete one, and repeat until no more deletions are possible. Each check for a student requires scanning both sides, costing `O(n)`, and this happens potentially `O(n)` times, leading to `O(n^2)` or worse. With `n` up to `2 × 10^5`, this is far beyond feasible limits.

The key observation is that the removal condition does not depend on adjacency or local structure, but only on whether certain inequalities exist on each side. Once we rephrase everything in terms of prefix and suffix information, we can determine whether a position is ever removable without simulating deletions.

A student becomes removable only when their value is “sandwiched” in a split way: there is a value on one side that is at least as large, and a value on the other side that is at most as large (or the symmetric situation). This means removability depends on whether the array contains both a larger and a smaller value distributed across positions relative to `i`.

The students that can never be eliminated are exactly those that remain extremal in at least one directional sense: prefix maximum, prefix minimum, suffix maximum, or suffix minimum. Any position that is not protected by at least one of these extremal properties can eventually be exposed and removed by choosing a suitable deletion order.

Thus, instead of simulating deletions, we precompute four sets: prefix maxima, prefix minima, suffix maxima, and suffix minima. Any index that belongs to at least one of these sets is safe and will remain in the final configuration. The answer is the size of their union.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation of deletions | O(n²) | O(n) | Too slow |
| Prefix/Suffix extremal classification | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute prefix maximums while scanning from left to right, marking every position that is the largest value seen so far. This captures elements that cannot be dominated from the left.
2. Compute prefix minimums in the same scan, marking positions that are the smallest seen so far. These elements cannot be “surpassed downward” from the left side.
3. Compute suffix maximums while scanning from right to left, marking positions that are the largest value in their suffix. These cannot be dominated from the right.
4. Compute suffix minimums similarly from right to left.
5. Mark every index that appears in any of the four categories. The final answer is the number of marked indices.

The reason each category matters is that removal requires the existence of both a larger and a smaller value in conflicting directions. If a position is a prefix maximum, then nothing on the left is larger, which blocks one of the two ways removability can be triggered. The same idea applies symmetrically to the other three cases.

### Why it works

The removability condition requires simultaneously witnessing both a value not smaller than `a[i]` on one side and a value not larger than `a[i]` on the other side, in some split configuration. If a position is extremal in any of the four directional senses, at least one side fails to provide the required inequality structure needed to “sandwich” it. Therefore such positions can never be fully exposed by any sequence of deletions. Conversely, any position that is not protected by these extremal constraints can be made removable by first eliminating blocking elements, which eventually creates the required split configuration. This reduces the problem to identifying all indices that are extremal in at least one direction.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

pref_max = [False] * n
pref_min = [False] * n
suf_max = [False] * n
suf_min = [False] * n

cur = -10**18
for i in range(n):
    if a[i] >= cur:
        pref_max[i] = True
        cur = a[i]

cur = 10**18
for i in range(n):
    if a[i] <= cur:
        pref_min[i] = True
        cur = a[i]

cur = -10**18
for i in range(n - 1, -1, -1):
    if a[i] >= cur:
        suf_max[i] = True
        cur = a[i]

cur = 10**18
for i in range(n - 1, -1, -1):
    if a[i] <= cur:
        suf_min[i] = True
        cur = a[i]

ans = 0
for i in range(n):
    if pref_max[i] or pref_min[i] or suf_max[i] or suf_min[i]:
        ans += 1

print(ans)
```

The code computes four linear scans over the array. Each scan maintains the best value seen so far in the corresponding direction and marks positions that achieve a new extremum.

The final loop simply counts indices that belong to at least one extremal category. This avoids any simulation of deletions, which would be too slow and also unnecessary once the structural characterization is known.

## Worked Examples

Consider the array `1 2 3 4 5`.

Prefix maxima occur at every position, since each new element is larger than all previous ones.

| i | value | prefix max? | prefix min? | suffix max? | suffix min? |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | yes | yes | no | no |
| 2 | 2 | yes | no | no | no |
| 3 | 3 | yes | no | no | no |
| 4 | 4 | yes | no | no | no |
| 5 | 5 | yes | no | yes | yes |

The union of marked positions includes all indices, so all students remain.

Now consider `5 1 4 2 3`.

We track extremal positions:

| i | value | prefix max? | prefix min? | suffix max? | suffix min? |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | yes | yes | yes | no |
| 2 | 1 | no | yes | no | yes |
| 3 | 4 | yes | no | no | no |
| 4 | 2 | no | no | no | yes |
| 5 | 3 | no | no | yes | yes |

Every index is covered by at least one extremal property, so the final answer is 5.

These examples show that the surviving set is not tied to monotonic segments alone, but to whether a position ever sets or matches a directional extremum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Four linear scans plus one final pass |
| Space | O(n) | Boolean arrays for four directional markers |

The solution runs comfortably within limits for `n ≤ 2 × 10^5`, since it performs only a constant number of passes over the input and uses linear auxiliary memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    pref_max = [False] * n
    pref_min = [False] * n
    suf_max = [False] * n
    suf_min = [False] * n

    cur = -10**18
    for i in range(n):
        if a[i] >= cur:
            pref_max[i] = True
            cur = a[i]

    cur = 10**18
    for i in range(n):
        if a[i] <= cur:
            pref_min[i] = True
            cur = a[i]

    cur = -10**18
    for i in range(n - 1, -1, -1):
        if a[i] >= cur:
            suf_max[i] = True
            cur = a[i]

    cur = 10**18
    for i in range(n - 1, -1, -1):
        if a[i] <= cur:
            suf_min[i] = True
            cur = a[i]

    ans = 0
    for i in range(n):
        if pref_max[i] or pref_min[i] or suf_max[i] or suf_min[i]:
            ans += 1

    return str(ans)

# minimum size
assert run("1\n5") == "1", "single element"

# strictly increasing
assert run("5\n1 2 3 4 5") == "5", "increasing"

# strictly decreasing
assert run("5\n5 4 3 2 1") == "5", "decreasing"

# mixed values
assert run("5\n5 1 4 2 3") == "5", "mixed"

# all equal
assert run("4\n7 7 7 7") == "4", "equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 1 | minimum boundary handling |
| increasing sequence | 5 | prefix extremum propagation |
| decreasing sequence | 5 | suffix extremum propagation |
| mixed sequence | 5 | union logic correctness |
| all equal | 4 | duplicate handling |

## Edge Cases

For a single element array like `10`, all four scans immediately mark the only position as extremal in every direction. There is no left or right side, so the algorithm correctly counts it as a survivor.

For a strictly increasing sequence like `1 2 3 4 5`, every position is a prefix maximum. During the prefix scan, each element becomes the new running maximum, so all positions are marked, producing a full survivor set.

For a sequence with equal values like `3 3 3 3`, every element is simultaneously a prefix maximum and prefix minimum at different times depending on equality handling. The scans mark all positions, and the final union correctly includes every index.
