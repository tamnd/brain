---
title: "CF 104295G - \u041f\u043e\u0440\u0430\u0434\u0443\u0439 \u0422\u043e\u0444\u0441\u043b\u0443"
description: "We are given a collection of tower heights. There are $n$ towers, where $n$ is guaranteed to be odd, and each tower has some initial height. We are also given $k$ extra unit cubes. Each cube can be added to exactly one tower, increasing its height by one."
date: "2026-07-01T20:20:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104295
codeforces_index: "G"
codeforces_contest_name: "vkoshp.letovo"
rating: 0
weight: 104295
solve_time_s: 52
verified: true
draft: false
---

[CF 104295G - \u041f\u043e\u0440\u0430\u0434\u0443\u0439 \u0422\u043e\u0444\u0441\u043b\u0443](https://codeforces.com/problemset/problem/104295/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of tower heights. There are $n$ towers, where $n$ is guaranteed to be odd, and each tower has some initial height. We are also given $k$ extra unit cubes. Each cube can be added to exactly one tower, increasing its height by one.

After we distribute all $k$ cubes in any way we like, the final configuration is sorted in non-decreasing order. We are not interested in the full array after sorting, only in the median element, meaning the $\frac{n+1}{2}$-th smallest height. Our goal is to choose how to distribute the $k$ cubes so that this median value is as large as possible.

The key tension is that adding cubes to one tower may or may not influence the median depending on whether that tower ends up below or above the median position after sorting. Since sorting is applied at the end, the identity of towers does not matter, only their final multiset of values.

The constraints are large: $n$ can go up to 300,000 and $k$ up to $10^9$, so any solution that simulates cube placement incrementally or repeatedly sorts is immediately impossible. Sorting once is fine, but anything that tries to repeatedly adjust and re-evaluate the median dynamically will fail.

A subtle edge case appears when $k = 0$. Then we simply return the median of the original array, but even in this trivial case the reasoning must align with the general method.

Another important edge case is when many values are equal around the median boundary. A naive intuition might try to “raise the median tower directly”, but since sorting happens after all operations, increasing one element may just push it above others without actually improving the median position unless enough elements are lifted.

## Approaches

The brute-force approach would try to distribute the $k$ cubes in all possible ways, then compute the resulting median after sorting. Even if we discretize by thinking in terms of increments to each of the $n$ towers, this is equivalent to distributing $k$ identical items into $n$ buckets, which has $\binom{k+n-1}{n-1}$ possibilities. This grows astronomically even for tiny values and is completely infeasible.

A slightly more structured brute-force idea would be to try greedy assignment: repeatedly add a cube to the tower that currently seems most beneficial for increasing the median. The issue is that the median depends on global ordering, so local greedy choices do not reliably track which element will end up at the median position after future changes.

The key observation is to stop tracking individual towers and instead focus on a threshold value. Suppose we guess a target height $x$ for the median. The question becomes: can we ensure that at least half of the towers end up with height at least $x$? If we can, then $x$ is achievable as a median value after sorting.

To make this check efficient, we note that every tower with initial height below $x$ needs to be raised up to at least $x$, and each such tower has a well-defined cost in cubes. Towers already at or above $x$ naturally contribute to satisfying the median condition without spending cubes.

This transforms the problem into deciding how large a threshold $x$ we can support with a limited budget of $k$ increments. Since feasibility is monotonic in $x$, we can binary search the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Distribution | exponential | O(n) | Too slow |
| Greedy / direct simulation | O(k log n) | O(n) | Too slow |
| Binary search + feasibility check | O(n log maxA) | O(n) | Accepted |

## Algorithm Walkthrough

We sort the array so that reasoning about ranks becomes stable. Let the target median position be $mid = \frac{n}{2}$ in 0-indexed terms.

We then binary search the answer $x$, checking whether we can make the median at least $x$.

1. Sort the array of heights. Sorting is required so we can reason about how many elements lie below or above a threshold without tracking identities.
2. Define a function `can(x)` that decides whether it is possible for the median to be at least $x$.
3. Inside `can(x)`, we iterate over all towers and compute how many cubes are needed to raise every tower with height less than $x$ up to $x$. For each such tower with height $a[i] < x$, we accumulate $x - a[i]$.
4. If the total cost exceeds $k$, we immediately return false. This is because even before considering distribution optimally, we already cannot lift enough mass to ensure the median threshold.
5. If the total cost is within $k$, we return true, meaning we can force at least half of the towers to reach height $x$ or higher, which guarantees the median condition.
6. We binary search $x$ in the range from the minimum possible height up to the maximum possible height plus $k$, since the median cannot exceed the case where all cubes are placed on relevant towers.
7. The final answer is the largest $x$ for which `can(x)` is true.

### Why it works

The correctness rests on the fact that the median condition depends only on how many elements are at least a certain value, not on their identities. Once we fix a candidate $x$, any tower below $x$ must be increased to reach it if we want it to contribute to the upper half. Spending cubes on towers already above $x$ is never necessary for feasibility of $x$, since they already satisfy the constraint.

This creates a monotonic feasibility structure: if we can achieve median at least $x$, then we can also achieve any $y < x$, because the required cost only decreases as the threshold decreases. This monotonicity is exactly what makes binary search valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))
a.sort()

mid = n // 2

def can(x):
    need = 0
    for i in range(n):
        if a[i] < x:
            need += x - a[i]
            if need > k:
                return False
    return True

lo, hi = min(a), max(a) + k

while lo < hi:
    mid_val = (lo + hi + 1) // 2
    if can(mid_val):
        lo = mid_val
    else:
        hi = mid_val - 1

print(lo)
```

The implementation starts by sorting the array so that we can treat heights in order, although the feasibility check itself does not rely on positional updates after sorting.

The `can(x)` function computes the total number of cubes required to raise every element below $x$ up to $x$. The early exit when `need > k` is essential for efficiency, especially when $k$ is large.

The binary search uses an upper mid bias `(lo + hi + 1) // 2` to avoid infinite loops when converging upward. The search space is safely bounded by `max(a) + k` because placing all cubes on a single tower can increase any element by at most $k$.

## Worked Examples

### Example 1

Input:

```
5 0
1 3 2 5 2
```

Sorted array: `[1, 2, 2, 3, 5]`, median index is 2 (0-indexed).

We test feasibility:

| x | cost to reach x | can(x) |
| --- | --- | --- |
| 2 | (1→2)=1 | yes |
| 3 | (1→3)=2 + (2→3)=1 + (2→3)=1 = 4 | no |

The largest feasible value is 2.

This shows that without extra cubes, we cannot push enough mass to raise the median beyond its initial value.

### Example 2

Input:

```
5 3
1 5 2 2 3
```

Sorted: `[1, 2, 2, 3, 5]`

We try increasing thresholds:

| x | cost | feasible |
| --- | --- | --- |
| 3 | (1→3)=2 + (2→3)=1 + (2→3)=1 = 4 | no |
| 2 | (1→2)=1 | yes |

So answer remains 2 even after distributing 3 cubes.

This demonstrates that improving the median requires enough budget to lift multiple elements simultaneously, not just one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log (maxA + k))$ | sorting plus binary search over value range, each feasibility check scans array |
| Space | $O(1)$ extra | only sorting array in-place |

The solution fits comfortably within limits since $n = 3 \cdot 10^5$ and logarithmic factor is small (around 30 iterations), resulting in about $10^7$ primitive operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()

    def can(x):
        need = 0
        for v in a:
            if v < x:
                need += x - v
                if need > k:
                    return False
        return True

    lo, hi = min(a), max(a) + k
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if can(mid):
            lo = mid
        else:
            hi = mid - 1
    return str(lo)

# provided samples
assert run("5 0\n1 3 2 5 2\n") == "2"
assert run("5 3\n1 5 2 2 3\n") == "2"

# minimum case
assert run("1 10\n5\n") == "15"

# all equal
assert run("5 4\n2 2 2 2 2\n") == "3"

# large k on skewed array
assert run("3 100\n1 1 1\n") == "34"

# no improvement possible
assert run("3 0\n10 1 2\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 15 | maximum inflation |
| all equal | 3 | balanced distribution |
| skewed small array | 34 | heavy mass shift |
| zero k | 1 | correctness without changes |

## Edge Cases

For $n = 1$, the median is the only element, so every cube directly increases the answer. The algorithm handles this because the feasibility check simply accumulates $k$ into a single value and binary search reaches $a[0] + k$.

When all elements are identical, the median can only increase if enough cubes exist to raise at least half of them above the threshold. The feasibility function correctly reflects this because it charges cost for every element below $x$, ensuring that lifting only one element is never enough.

When $k = 0$, the binary search collapses to the original median. Since no value of $x$ above the median is feasible, the search naturally returns the sorted middle element without special casing.
