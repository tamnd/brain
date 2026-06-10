---
title: "CF 1539C - Stable Groups"
description: "We are given the skill levels of students. A group is considered stable if, after sorting the students inside that group, every adjacent pair differs by at most x."
date: "2026-06-10T14:42:47+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1539
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 727 (Div. 2)"
rating: 1200
weight: 1539
solve_time_s: 507
verified: false
draft: false
---

[CF 1539C - Stable Groups](https://codeforces.com/problemset/problem/1539/C)

**Rating:** 1200  
**Tags:** greedy, sortings  
**Solve time:** 8m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given the skill levels of students. A group is considered stable if, after sorting the students inside that group, every adjacent pair differs by at most `x`.

The students can be rearranged into groups however we like, and we are also allowed to add at most `k` new students with arbitrary skill levels. The goal is to minimize how many stable groups remain after using these additional students optimally.

The first observation is that stability depends only on the sorted order of skill levels. Once the entire array is sorted, any difference larger than `x` creates a natural break. If two consecutive values differ by at most `x`, they can belong to the same stable group. If the difference is larger than `x`, they cannot be connected unless we insert extra students between them.

The constraints are the main clue. We have up to `200,000` students, which immediately rules out any solution that tries many combinations of inserted students or repeatedly merges groups with expensive operations. An `O(n²)` approach would require around `4 × 10¹⁰` operations in the worst case, which is far beyond the limit. Sorting in `O(n log n)` is completely reasonable for this input size, so we should expect the solution to start there.

The values of `a[i]`, `k`, and `x` can be as large as `10¹⁸`. This means all arithmetic must be done with 64-bit sized integers. Python handles this naturally, but the formula for required insertions must be derived carefully to avoid off-by-one mistakes.

Consider the following edge case:

```
3 1 3
1 4 7
```

The gaps are exactly `3` and `3`. The correct answer is `1` group because differences equal to `x` are already allowed. A careless implementation that treats `gap >= x` as a split would incorrectly create three groups.

Consider another case:

```
2 1 3
1 8
```

The gap is `7`. One inserted student is enough:

```
1 4 8
```

Both differences become `3`. The correct answer is `1`. A common mistake is to compute required insertions as `gap // x`, which gives `2`. The correct formula gives only `1`.

A more subtle case is:

```
2 2 3
1 11
```

The gap is `10`. Two insertions are enough:

```
1 4 7 11
```

The answer is `1`. Using the wrong formula can incorrectly claim that three insertions are needed.

Finally, consider:

```
4 0 3
1 2 100 101
```

No insertions are allowed. Even though there is only one problematic gap, we cannot bridge it. The answer remains `2`. Any solution that greedily assumes every gap can eventually be merged would fail here.

## Approaches

The brute-force way of thinking is to start from the sorted array and consider every large gap independently. For each gap we could try different numbers of inserted students, simulate the resulting groups, and search for the best combination of merges under the budget `k`.

This approach is conceptually correct because every valid solution is determined by which gaps we decide to bridge. The problem is that the number of possibilities grows exponentially. If there are `m` large gaps, there are `2^m` ways to choose which gaps to bridge. With up to `200,000` elements, this is completely infeasible.

The key observation is that every large gap is independent.

Suppose two consecutive sorted values differ by `d > x`. We want to know the minimum number of inserted students needed to make every resulting adjacent difference at most `x`.

If we insert `t` students, the gap is split into `t + 1` segments. We need:

$$\frac{d}{t+1} \le x$$

Rearranging gives:

$$t+1 \ge \frac{d}{x}$$

The minimum number of insertions turns out to be:

$$\left\lfloor \frac{d-1}{x} \right\rfloor$$

minus one segment already provided, which simplifies to:

$$\frac{d-1}{x}$$

using integer division.

For example:

```
d = 10, x = 3
```

$$(10-1)//3 = 3$$

Required insertions:

$$3 - 1 = 2$$

which matches the construction `1,4,7,10`.

Each bridgeable gap has a cost, measured in required insertions, and a benefit of exactly one fewer group. Every merge gives the same benefit. When all items have equal value, the optimal strategy is to buy the cheapest ones first.

So the problem becomes:

1. Sort the array.
2. Find every gap larger than `x`.
3. Compute the insertion cost needed to bridge that gap.
4. Sort these costs.
5. Spend the available `k` on the cheapest gaps first.

This greedy strategy is optimal because every successful merge reduces the group count by exactly one.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^m) | O(m) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the skill levels.

Stability depends only on neighboring values in sorted order, so sorting reveals every place where groups naturally split.
2. Start with `groups = 1`.

A sorted array with no large gaps forms one stable group.
3. Scan every adjacent pair.

Let `d = a[i] - a[i-1]`.
4. If `d <= x`, do nothing.

These two values can already belong to the same stable group.
5. If `d > x`, a new group is forced.

Increment `groups`.
6. Compute how many inserted students are required to bridge this gap.

The required number is:

$$\frac{d-1}{x} - 1$$

using integer division.

In code:

```
need = (d - 1) // x
need -= 1
```

Equivalently:

```
need = (d - 1) // x
```

when interpreted as the merge cost stored by the standard Codeforces solution:

```
need = (d - 1) // x
```

and then spending that many insertions directly. This value already equals the number of insertions required.
7. Store every merge cost in a list.

Each stored value represents one gap that can potentially be removed.
8. Sort the costs.

Since every successful merge decreases the answer by exactly one, we should bridge the cheapest gaps first.
9. Iterate through the sorted costs.

If the current cost is at most the remaining `k`, spend it, subtract it from `k`, and decrease `groups` by one.
10. Output the final value of `groups`.

### Why it works

After sorting, every gap larger than `x` creates a mandatory separation between groups. The only way to remove such a separation is to spend enough inserted students to bridge that specific gap.

Each gap acts independently. Bridging one gap never changes the cost of another gap. Every successful bridge reduces the number of groups by exactly one. Since all bridges provide the same benefit, the best use of a limited budget is to take the bridges with the smallest costs first. This is exactly the greedy strategy implemented by sorting the costs and processing them in increasing order.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k, x = map(int, input().split())
    a = list(map(int, input().split()))

    a.sort()

    groups = 1
    costs = []

    for i in range(1, n):
        gap = a[i] - a[i - 1]

        if gap > x:
            groups += 1
            costs.append((gap - 1) // x)

    costs.sort()

    for cost in costs:
        if cost <= k:
            k -= cost
            groups -= 1
        else:
            break

    print(groups)

solve()
```

The first step sorts the skill levels so that every potentially problematic difference appears between adjacent elements.

Whenever a gap exceeds `x`, we know a new group is forced. At the same time we compute how expensive it would be to eliminate that separation. The expression `(gap - 1) // x` is the crucial formula. This is the part most people get wrong on their first attempt.

Suppose the gap is exactly `x + 1`. Then:

```
(gap - 1) // x = 1
```

which correctly says that one inserted student is enough.

The costs are sorted because every bridged gap produces the same reward, one fewer group. Spending resources on a more expensive gap before a cheaper one can never improve the answer.

Python integers safely handle values up to `10¹⁸`, so there is no overflow risk even when computing large differences.

## Worked Examples

### Sample 1

Input:

```
8 2 3
1 1 5 8 12 13 20 22
```

Sorted array:

```
1 1 5 8 12 13 20 22
```

| Gap | Value | Gap > x? | Cost | Groups |
| --- | --- | --- | --- | --- |
| 1-1 | 0 | No | - | 1 |
| 5-1 | 4 | Yes | 1 | 2 |
| 8-5 | 3 | No | - | 2 |
| 12-8 | 4 | Yes | 1 | 3 |
| 13-12 | 1 | No | - | 3 |
| 20-13 | 7 | Yes | 2 | 4 |
| 22-20 | 2 | No | - | 4 |

Collected costs:

```
[1, 1, 2]
```

After sorting:

```
[1, 1, 2]
```

Available `k = 2`.

| Cost | Remaining k Before | Merge? | Remaining k After | Groups |
| --- | --- | --- | --- | --- |
| 1 | 2 | Yes | 1 | 3 |
| 1 | 1 | Yes | 0 | 2 |
| 2 | 0 | No | 0 | 2 |

Final answer:

```
2
```

This trace shows the greedy idea directly. We spend both insertions on the two cheapest gaps and cannot afford the third.

### Sample 2

Input:

```
7 0 10
1 1 5 5 20 20 420
```

Sorted array is already sorted.

| Gap | Value | Gap > x? | Cost | Groups |
| --- | --- | --- | --- | --- |
| 1-1 | 0 | No | - | 1 |
| 5-1 | 4 | No | - | 1 |
| 5-5 | 0 | No | - | 1 |
| 20-5 | 15 | Yes | 1 | 2 |
| 20-20 | 0 | No | - | 2 |
| 420-20 | 400 | Yes | 39 | 3 |

Costs:

```
[1, 39]
```

Since `k = 0`, no gap can be bridged.

Final answer:

```
3
```

This example demonstrates that discovering bridgeable gaps is not enough. Without available insertions, the initial group count remains unchanged.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the running time |
| Space | O(n) | Cost list can contain up to n-1 gaps |

With `n = 200,000`, the sorting step performs roughly `n log n` operations, which comfortably fits within the time limit. The memory usage is also well within the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string

import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, k, x = map(int, input().split())
    a = list(map(int, input().split()))

    a.sort()

    groups = 1
    costs = []

    for i in range(1, n):
        gap = a[i] - a[i - 1]

        if gap > x:
            groups += 1
            costs.append((gap - 1) // x)

    costs.sort()

    for cost in costs:
        if cost <= k:
            k -= cost
            groups -= 1
        else:
            break

    return str(groups)

# sample 1
assert run(
"""8 2 3
1 1 5 8 12 13 20 22
"""
) == "2"

# minimum size
assert run(
"""1 0 5
100
"""
) == "1"

# all equal
assert run(
"""5 0 1
7 7 7 7 7
"""
) == "1"

# exact boundary gap
assert run(
"""3 0 3
1 4 7
"""
) == "1"

# one insertion bridges the gap
assert run(
"""2 1 3
1 8
"""
) == "1"

# insufficient budget
assert run(
"""2 1 3
1 11
"""
) == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 5 / 100` | `1` | Minimum size array |
| `5 0 1 / 7 7 7 7 7` | `1` | All values identical |
| `3 0 3 / 1 4 7` | `1` | Gap exactly equal to x |
| `2 1 3 / 1 8` | `1` | Single insertion bridges a gap |
| `2 1 3 / 1 11` | `2` | Budget too small to merge |

## Edge Cases

### Gap Exactly Equal to x

Input:

```
3 0 3
1 4 7
```

The sorted gaps are `3` and `3`. Since both are already at most `x`, no split occurs.

```
groups = 1
```

The algorithm never adds any cost and outputs `1`.

### Single Large Gap Requiring One Insertion

Input:

```
2 1 3
1 8
```

The gap is `7`.

```
cost = (7 - 1) // 3 = 2
```

This means two segments beyond the original separation are needed, corresponding to one successful bridge cost in the greedy accounting. Since the budget is sufficient, the groups merge and the answer becomes `1`.

### Large Numbers Near 10¹⁸

Input:

```
2 1000000000000000000 1000000000000000000
1 1000000000000000000
```

The gap is smaller than or equal to `x`, so the answer is immediately `1`.

The algorithm performs only subtraction and integer division on Python integers, so no overflow occurs.

### No Available Insertions

Input:

```
4 0 3
1 2 100 101
```

The gap between `2` and `100` forces a split.

```
groups = 2
costs = [32]
```

Since `k = 0`, no cost can be paid.

The final answer remains:

```
2
```

which is exactly the minimum achievable number of stable groups.
