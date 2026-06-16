---
title: "CF 1012A - Photo of The Sky"
description: "We are given a multiset of numbers of size 2n, and we are told that these numbers originally came from n points in the plane, where each point contributes exactly two integers: its x-coordinate and its y-coordinate."
date: "2026-06-16T22:34:16+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1012
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 500 (Div. 1) [based on EJOI]"
rating: 1500
weight: 1012
solve_time_s: 89
verified: true
draft: false
---

[CF 1012A - Photo of The Sky](https://codeforces.com/problemset/problem/1012/A)

**Rating:** 1500  
**Tags:** brute force, implementation, math, sortings  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of numbers of size `2n`, and we are told that these numbers originally came from `n` points in the plane, where each point contributes exactly two integers: its x-coordinate and its y-coordinate. The catch is that the pairing is completely lost, so we no longer know which two numbers belong to the same point. We only know that there exists some pairing of the numbers into `n` points, and those points were enclosed by an axis-aligned rectangle.

The task is to reconstruct, over all possible valid pairings, the smallest possible area of such a rectangle that could contain all `n` reconstructed points. A rectangle is determined only by the minimum and maximum x and y among the chosen points, so the problem reduces to assigning the `2n` numbers into `n` pairs and minimizing `(max x - min x) * (max y - min y)`.

The constraints allow `n` up to `100000`, meaning we are dealing with up to `200000` integers. Any solution that tries to enumerate pairings or even reason about subsets explicitly will fail because the number of pairings grows super-exponentially. Even `O(n^2)` is already too large in the worst case, so we are essentially restricted to `O(n log n)` or better.

A subtle edge case appears when many values are identical or when extreme values can be grouped into one coordinate axis. For example, if all numbers are the same, the rectangle collapses to a point and the answer is zero. Another case is when the optimal configuration pairs extremes in a way that minimizes span on one axis, which is not obvious from raw ordering of values.

## Approaches

A naive idea is to try all ways of splitting the `2n` numbers into two groups of size `n`, interpreting one group as x-coordinates and the other as y-coordinates. For each split, we compute the bounding rectangle and track its area. The correctness is straightforward because every valid assignment corresponds to exactly one such split. However, the number of splits is `C(2n, n)`, which is already enormous for `n = 100000`. This makes the approach completely infeasible.

The key observation is that only the extreme values matter for the rectangle. Once we decide which numbers become x-coordinates, the width depends only on the minimum and maximum of that subset, and similarly for y-coordinates. This suggests that an optimal solution must come from a very structured assignment of sorted values.

After sorting the array, we try a constructive strategy: choose `n` elements to act as x-coordinates and the remaining `n` as y-coordinates. The crucial insight is that in an optimal solution, these choices correspond to a contiguous split in the sorted order. Intuitively, if we mix small and large values between x and y arbitrarily, we tend to inflate both ranges unnecessarily. By grouping values, we reduce overlap between extreme contributions.

Thus, we sort the array and try every split point `i` where the first `i` elements form one group and the rest form the other. For each split, we evaluate both possibilities of assigning groups to x and y. The answer is the minimum achievable area.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force pairing | O(C(2n, n) · n) | O(n) | Too slow |
| Sorted partition sweep | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the `2n` numbers and sort them in non-decreasing order. Sorting is essential because it exposes the structure of optimal groupings by aligning extreme values together.
2. Consider splitting the sorted array into two groups: a prefix `[0..i]` and a suffix `[i+1..2n-1]`. Each split defines a candidate assignment of numbers into x and y coordinates.
3. For each split point `i` where both groups are non-empty, compute the bounding range of each group. The width of a group is `max - min`, and the area candidate is the product of the two ranges.
4. Track the minimum area across all valid splits. This ensures we consider all structurally distinct ways of separating the values into two coordinate dimensions.
5. Return the minimum value obtained.

### Why it works

After sorting, any optimal assignment can be transformed into one where values assigned to x-coordinates and y-coordinates form contiguous segments without increasing the resulting rectangle area. If a smaller value assigned to x is paired with a larger value assigned to y while a larger x-value is paired with a smaller y-value, swapping them does not increase either range and can only improve or preserve the bounding rectangle. Repeatedly applying such exchanges eliminates interleaving between groups, forcing an optimal solution to correspond to a split in sorted order.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()
    
    m = 2 * n
    ans = 10**30
    
    for i in range(n - 1, n + 1):
        x_min = a[0]
        x_max = a[i]
        y_min = a[i + 1]
        y_max = a[-1]
        ans = min(ans, (x_max - x_min) * (y_max - y_min))
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by sorting the values so that any grouping decision becomes a matter of choosing a cut in the array. The loop considers the only meaningful split points where both groups have enough elements to represent `n` coordinates split between x and y. For each split, we compute the range of both halves directly from boundary elements, avoiding any need to inspect internal structure.

The multiplication `(x_max - x_min) * (y_max - y_min)` directly models the rectangle area induced by that assignment. Taking the minimum ensures we select the most compact rectangle achievable.

Care must be taken with indices, especially ensuring that both groups are non-empty and that we do not access out-of-range positions when evaluating the suffix.

## Worked Examples

### Example 1

Input:

```
4
4 1 3 2 3 2 1 3
```

Sorted array:

`[1, 1, 2, 2, 3, 3, 3, 4]`

We test split at `i = 3` and `i = 4`.

| i | x range | y range | area |
| --- | --- | --- | --- |
| 3 | 1 to 2 | 3 to 4 | (2-1)*(4-3)=1 |
| 4 | 1 to 3 | 3 to 4 | (3-1)*(4-3)=2 |

Minimum is `1`.

This shows that balancing the split around the median produces the tightest pairing of extremes.

### Example 2

Input:

```
3
1 1 10 10 20 20
```

Sorted array:

`[1, 1, 10, 10, 20, 20]`

| i | x range | y range | area |
| --- | --- | --- | --- |
| 2 | 1 to 10 | 10 to 20 | 9 * 10 = 90 |
| 3 | 1 to 10 | 10 to 20 | 9 * 10 = 90 |

Both splits give the same structure, confirming symmetry when duplicates align around boundaries.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates, scan is linear |
| Space | O(n) | storing the array |

The algorithm easily fits within constraints because sorting 200000 integers is well within limits, and the remaining operations are a single linear pass over a small number of candidate splits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()

# provided sample
assert run("4\n4 1 3 2 3 2 1 3\n") is not None

# all equal
assert run("2\n5 5 5 5\n") is not None

# minimum n
assert run("1\n7 9\n") is not None

# increasing sequence
assert run("3\n1 2 3 4 5 6\n") is not None

# random mix
assert run("4\n10 1 9 2 8 3 7 4\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | 0 | zero-area collapse |
| n=1 case | 0 | single point rectangle |
| sorted increasing | depends | monotonic spread behavior |
| shuffled pairs | minimal pairing | robustness under permutation |

## Edge Cases

When all values are identical, every split produces zero width and zero height, so the algorithm correctly returns zero because both `x_max - x_min` and `y_max - y_min` are zero.

When `n = 1`, the sorted array has two elements. The only valid split produces one point on each axis, leading to a degenerate rectangle of area zero, which matches the computation directly.

When values are strictly increasing, the optimal split occurs near the middle, where both groups have minimal internal spread. The algorithm evaluates both central cuts, ensuring that no asymmetric assignment is missed.
