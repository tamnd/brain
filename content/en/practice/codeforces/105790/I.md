---
title: "CF 105790I - Itwise Bor"
description: "We have an array of star brightness values. We must split the array into contiguous groups. The beauty of a group is the bitwise OR of all values inside that group. For a partition of the array, we compute the sum of the beauties of all groups."
date: "2026-06-26T03:50:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105790
codeforces_index: "I"
codeforces_contest_name: "UDESC Selection Contest 2024-1"
rating: 0
weight: 105790
solve_time_s: 43
verified: true
draft: false
---

[CF 105790I - Itwise Bor](https://codeforces.com/problemset/problem/105790/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of star brightness values. We must split the array into contiguous groups. The beauty of a group is the bitwise OR of all values inside that group.

For a partition of the array, we compute the sum of the beauties of all groups. Among all possible partitions, we want the maximum possible sum. If several partitions achieve that maximum sum, we must output the one using the fewest groups.

The input contains a single array of length `N`, where `N` can be as large as `3·10^5`, and each value is smaller than `2^30`. The output consists of two numbers:

`S` = maximum possible sum of group beauties.

`K` = minimum number of groups among all partitions that achieve `S`.

The size of `N` immediately rules out any dynamic programming that examines all subarrays. There are roughly `N²/2` subarrays, which would be around 45 billion when `N = 300000`. Even an `O(N log N)` solution would be comfortable, while `O(N²)` is completely impossible.

The key difficulty is understanding how bitwise OR behaves when several elements are merged into one group.

Consider a simple example:

```
2
1 2
```

The partition `[1][2]` gives beauty sum `1 + 2 = 3`.

The partition `[1,2]` gives beauty `1|2 = 3`.

The maximum sum is still `3`, but the second partition uses fewer groups, so the answer is:

```
3 1
```

A careless solution that always starts a new group whenever possible would return `K = 2`, which is not minimal.

Another interesting case is:

```
2
1 1
```

Separate groups give `1 + 1 = 2`.

One merged group gives `1|1 = 1`.

The merged version loses value because the same bit is counted only once inside the OR. The correct answer is:

```
2 2
```

Any solution that merges groups whenever the OR does not decrease would fail here.

A final edge case is the presence of zeros:

```
3
0 5 0
```

The partition `[0,5,0]` has beauty `5`.

The partition `[0][5][0]` also has beauty sum `5`.

Since both achieve the same maximum sum, we must choose the one with fewer groups, namely a single group.

Handling these tie situations correctly is essential.

## Approaches

Let us first think about what happens when several elements are placed into one group.

Suppose a group contains values whose OR is `X`.

Every bit that appears anywhere in the group contributes exactly once to `X`.

Now compare this with keeping all elements separate. If a particular bit appears in multiple elements, then when separated it contributes multiple times to the total sum, but inside one OR it contributes only once.

This immediately gives an important observation:

For any group,

```
OR(group) ≤ sum(elements of group)
```

because every bit can only lose multiplicity when OR is applied.

Summing over all groups, the total beauty can never exceed the sum of all array elements.

The beauty sum reaches this upper bound exactly when no bit is ever counted twice inside any group.

That means inside each group, no bit position may appear in two different elements.

Equivalently, for every pair of elements in the same group:

```
their common set bits must be empty
```

or, more practically, while building a group, the current OR mask and the next value must satisfy:

```
(current_mask & value) == 0
```

If this condition holds, then adding the value introduces only new bits, and the group's OR increases by exactly the value itself.

The brute-force idea would be to try all partitions and check their beauty sums. Since there are `2^(N-1)` possible partitions, it becomes infeasible immediately.

The observation above changes the problem completely. The maximum possible beauty sum is always the sum of all array elements. The only remaining task is to find the minimum number of groups that can achieve that sum.

To achieve the maximum sum, every group must contain pairwise disjoint bits. While scanning from left to right, whenever the next element shares a bit with the current group's OR mask, keeping it in the same group would reduce the total beauty below the maximum. So a new group becomes mandatory.

On the other hand, if the next element has no common bit with the current group's mask, merging it is free: the maximum beauty remains achievable, and using the same group helps minimize the total number of groups.

This naturally leads to a greedy scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over partitions | O(2^N) | O(N) | Too slow |
| Greedy bit-mask scan | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize `total_sum` as the sum of all array values.
2. Start the first group. Maintain `mask`, the bitwise OR of all elements currently inside the group.
3. Process the array from left to right.
4. For the current value `x`, check whether `mask & x` is non-zero.
5. If the intersection is non-zero, some bit already exists in the current group. Keeping `x` in this group would cause that bit to be counted only once inside the OR, reducing the maximum achievable beauty. Start a new group and set `mask = x`.
6. If the intersection is zero, all bits of `x` are new to the current group. Add it to the current group and update `mask |= x`.
7. Count how many times a new group is started. This yields the minimum number of groups that still achieve the maximum beauty sum.
8. Output `total_sum` and the number of groups.

### Why it works

The sum of all array elements is an absolute upper bound on the answer because the OR of a group can never exceed the sum of its elements.

A partition reaches this upper bound exactly when no bit position appears twice inside any group. Whenever `mask & x ≠ 0`, placing `x` into the current group would create such a duplicate bit and force the beauty sum below the upper bound. A cut is mandatory.

Whenever `mask & x = 0`, merging `x` into the current group introduces only new bits, so the group's OR increases by exactly `x`. No beauty is lost, and avoiding a cut reduces the number of groups.

The greedy strategy makes a cut only when it is unavoidable. Every cut it creates is forced in every optimal partition. Consequently, it achieves the maximum beauty sum and uses the smallest possible number of groups among all partitions achieving that sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    total_sum = sum(a)

    groups = 1
    mask = 0

    for x in a:
        if mask & x:
            groups += 1
            mask = x
        else:
            mask |= x

    print(total_sum, groups)

solve()
```

The first part computes the sum of all elements. This value is already the maximum possible beauty sum.

The variable `mask` stores the OR of the current group. It summarizes exactly which bit positions are already present.

For each element `x`, the expression `mask & x` checks whether some bit would appear twice inside the same group. If that happens, a new group must start immediately.

When no common bit exists, we extend the current group by updating `mask |= x`.

The group counter starts at one because even a single-element array contains one group.

The implementation uses only constant extra memory and performs a single pass through the array.

## Worked Examples

### Example 1

Input:

```
5
4 1 2 1 3
```

| Position | Value | Current Mask Before | Conflict? | Groups | Current Mask After |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | 0 | No | 1 | 4 |
| 2 | 1 | 4 | No | 1 | 5 |
| 3 | 2 | 5 | No | 1 | 7 |
| 4 | 1 | 7 | Yes | 2 | 1 |
| 5 | 3 | 1 | Yes | 3 | 3 |

`total_sum = 4 + 1 + 2 + 1 + 3 = 11`

Answer:

```
11 3
```

This trace shows that the first three values can coexist because their set bits are disjoint. The fourth value shares a bit with the current group, making a cut unavoidable.

### Example 2

Input:

```
3
1 2 3
```

| Position | Value | Current Mask Before | Conflict? | Groups | Current Mask After |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | No | 1 | 1 |
| 2 | 2 | 1 | No | 1 | 3 |
| 3 | 3 | 3 | Yes | 2 | 3 |

`total_sum = 6`

Answer:

```
6 2
```

The first two values use different bits, so they can be merged. The third value contains bits already present in the group, forcing a new segment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | One left-to-right scan |
| Space | O(1) | Only a few integer variables are stored |

With `N ≤ 3·10^5`, a linear scan is easily fast enough. The memory usage is constant aside from the input array itself.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))

    total_sum = sum(a)

    groups = 1
    mask = 0

    for x in a:
        if mask & x:
            groups += 1
            mask = x
        else:
            mask |= x

    return f"{total_sum} {groups}"

# provided samples
assert run("5\n4 1 2 1 3\n") == "11 3", "sample 1"
assert run("3\n1 2 3\n") == "6 2", "sample 2"
assert run("4\n7 7 7 7\n") == "28 4", "sample 3"
assert run("5\n1 3 4 8 2\n") == "18 3", "sample 4"

# custom cases
assert run("1\n0\n") == "0 1", "minimum size"
assert run("3\n0 5 0\n") == "5 1", "zeros can merge"
assert run("2\n1 1\n") == "2 2", "duplicate bit forces split"
assert run("4\n1 2 4 8\n") == "15 1", "all bits disjoint"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0` | `0 1` | Smallest possible input |
| `0 5 0` | `5 1` | Zero values do not create conflicts |
| `1 1` | `2 2` | Duplicate bits require a cut |
| `1 2 4 8` | `15 1` | Entire array can remain one group |

## Edge Cases

Consider:

```
2
1 1
```

The algorithm starts with `mask = 0`.

After processing the first `1`, `mask = 1`.

For the second `1`, we get:

```
mask & x = 1
```

so a new group is created. The result is:

```
2 2
```

This is correct because merging them would produce OR value `1`, reducing the beauty sum.

Now consider:

```
3
0 5 0
```

The first zero creates no bits.

The value `5` has no conflict with the current mask.

The final zero also has no conflict.

No cuts are made, giving:

```
5 1
```

The beauty remains maximal and the number of groups is minimized.

Finally:

```
4
7 7 7 7
```

Every new element conflicts with the current mask because all bits are already present.

The algorithm starts a new group before each subsequent element, producing:

```
28 4
```

Every cut is mandatory, since any merge would reduce the beauty sum below the sum of the elements.
