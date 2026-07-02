---
title: "CF 103800D - Ginger's line"
description: "We are given a collection of straight lines in the plane, each described by an equation of the form $y = ai x + bi$. The task is to count how many unordered pairs of distinct lines intersect at exactly one point. Geometrically, two lines intersect if they are not parallel."
date: "2026-07-02T08:42:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103800
codeforces_index: "D"
codeforces_contest_name: "The 2022 SDUT Summer Trials"
rating: 0
weight: 103800
solve_time_s: 51
verified: true
draft: false
---

[CF 103800D - Ginger's line](https://codeforces.com/problemset/problem/103800/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of straight lines in the plane, each described by an equation of the form $y = a_i x + b_i$. The task is to count how many unordered pairs of distinct lines intersect at exactly one point.

Geometrically, two lines intersect if they are not parallel. For lines in slope-intercept form, parallelism happens exactly when their slopes are equal, that is when $a_i = a_j$. The problem explicitly adds one more detail: if two lines are identical, meaning both slope and intercept match, they should not be considered as intersecting pairs.

So the output is essentially the number of pairs $(i, j)$ with $i < j$ such that the lines are not parallel and not identical.

The constraints are $n \le 5 \cdot 10^3$. This is small enough that an $O(n^2)$ approach is acceptable. Any attempt that is worse than quadratic, such as checking each pair with heavy computation or using sorting inside nested loops, would risk timing out. A linear or $n \log n$ approach is not strictly necessary, but a clean combinational counting solution is expected.

A subtle case arises when multiple identical lines exist. For example, if the input contains:

```
1 1
1 1
1 1
```

all three lines overlap exactly. Naively counting “non-parallel pairs” would count all 3 pairs, but none of them should be considered intersecting. The correct answer is 0 because identical lines are excluded.

Another edge case is when many lines share the same slope but different intercepts:

```
2 0
2 1
2 2
```

These are all parallel but distinct, so no pair intersects, and the answer is 0.

## Approaches

The most direct way to solve the problem is to consider every pair of lines and check whether they intersect. Two lines $y = a_i x + b_i$ and $y = a_j x + b_j$ intersect if and only if $a_i \ne a_j$. If slopes are equal, they never meet unless they are identical, and identical lines are explicitly excluded anyway.

This leads to a straightforward brute force solution: iterate over all pairs $(i, j)$, check whether $a_i \ne a_j$, and count them. This is correct because every pair of non-parallel lines in the plane intersects exactly once.

However, this approach performs $\frac{n(n-1)}{2}$ comparisons, which is about 12.5 million operations in the worst case when $n = 5000$. This is already borderline but still acceptable in Python if done minimally. Still, we can simplify further by shifting from pairwise checking to counting how many pairs are excluded.

Instead of counting intersecting pairs directly, we count all pairs and subtract those that do not intersect. The non-intersecting pairs are exactly pairs of lines with equal slope. If a slope value appears $k$ times, then it contributes $\frac{k(k-1)}{2}$ non-intersecting pairs. The only remaining issue is identical lines, but identical lines are already included inside slope groups, and subtracting all equal-slope pairs correctly removes both parallel and duplicate contributions as required for this problem definition, since duplicates never contribute intersections anyway.

Thus the problem reduces to grouping lines by slope and summing combinations inside each group.

## Algorithm Walkthrough

1. Read all lines and group them by slope $a_i$, storing how many times each slope appears. We only need counts because intercepts do not affect whether lines intersect.
2. Compute the total number of unordered pairs among all lines using $\frac{n(n-1)}{2}$. This represents the maximum possible number of intersections if no lines were parallel.
3. For each slope group with size $k$, compute the number of pairs that cannot intersect, which is $\frac{k(k-1)}{2}$. Subtract this from the total.
4. Output the resulting value.

The reason step 3 is valid is that any pair of lines with equal slope never intersects, so we are precisely removing all invalid pairs from the full set of pairs.

### Why it works

Every pair of lines falls into exactly one of two categories: either their slopes differ or their slopes are equal. If slopes differ, the lines intersect exactly once. If slopes are equal, the lines are parallel and never intersect, regardless of intercepts, including the degenerate case of identical lines. Therefore, counting all pairs and subtracting same-slope pairs isolates exactly the intersecting pairs.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import defaultdict

def solve():
    n = int(input())
    cnt = defaultdict(int)

    for _ in range(n):
        a, b = map(int, input().split())
        cnt[a] += 1

    total = n * (n - 1) // 2
    bad = 0

    for k in cnt.values():
        bad += k * (k - 1) // 2

    print(total - bad)

if __name__ == "__main__":
    solve()
```

The code groups lines only by slope, which is sufficient because the intercept does not influence intersection existence. The total number of pairs is computed once, and then each slope group contributes a correction term removing all pairs that are parallel.

A common mistake would be to try checking all pairs explicitly, which is unnecessary. Another mistake is to treat identical lines separately from parallel lines, but both are naturally handled inside the same slope grouping.

## Worked Examples

### Example 1

Input:

```
3
1 1
2 2
3 3
```

| Step | Action | State |
| --- | --- | --- |
| 1 | Count slopes | {1:1, 2:1, 3:1} |
| 2 | Total pairs | 3 |
| 3 | Subtract same-slope pairs | 0 |
| 4 | Answer | 3 |

Each pair has different slopes, so every pair intersects exactly once.

### Example 2

Input:

```
4
1 0
1 1
2 0
2 1
```

| Step | Action | State |
| --- | --- | --- |
| 1 | Count slopes | {1:2, 2:2} |
| 2 | Total pairs | 6 |
| 3 | Subtract same-slope pairs | 1 + 1 = 2 |
| 4 | Answer | 4 |

Within each slope group, lines are parallel and do not intersect, so only cross-group pairs remain valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to count slopes and one pass over groups |
| Space | O(n) | Storage for frequency map of slopes |

The algorithm is linear in the number of lines, which is easily efficient for $n \le 5000$, and well within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import defaultdict

    n = int(sys.stdin.readline())
    cnt = defaultdict(int)

    for _ in range(n):
        a, b = map(int, sys.stdin.readline().split())
        cnt[a] += 1

    total = n * (n - 1) // 2
    bad = 0
    for k in cnt.values():
        bad += k * (k - 1) // 2

    return str(total - bad)

# provided samples (illustrative, as exact samples were not fully specified)
assert run("3\n1 1\n2 2\n3 3\n") == "3"
assert run("4\n1 0\n1 1\n2 0\n2 1\n") == "4"

# custom cases
assert run("1\n5 7\n") == "0", "single line"
assert run("3\n1 1\n1 1\n1 1\n") == "0", "all identical lines"
assert run("3\n1 0\n1 1\n1 2\n") == "0", "all parallel lines"
assert run("3\n1 0\n2 0\n3 0\n") == "3", "all intersecting"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 line | 0 | minimum case |
| identical slopes all equal | 0 | duplicates and overlap handling |
| same slope different intercepts | 0 | parallel correctness |
| distinct slopes | 3 | full intersection case |

## Edge Cases

For a single line such as:

```
1
10 20
```

the slope map contains only one entry with count 1. The total number of pairs is 0, and no subtraction occurs, so the result is correctly 0.

For fully identical lines:

```
3
1 1
1 1
1 1
```

the slope group is {1:3}. Total pairs is 3, and bad pairs inside the group is also 3, giving final answer 0. This correctly avoids counting overlapping lines as intersecting.

For many parallel but distinct lines:

```
4
2 0
2 1
2 2
2 3
```

the slope group is {2:4}. Total pairs is 6, bad pairs is 6, final answer is 0, correctly reflecting that no intersections exist among parallel lines.
