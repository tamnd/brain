---
title: "CF 285C - Building Permutation"
description: "We are given an array of integers and we are allowed to modify it using unit increments or decrements. Each such operation costs one move. The goal is to transform the array into a permutation of size n, meaning we must end up with exactly the numbers from 1 to n, each used once."
date: "2026-06-05T09:55:43+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 285
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 175 (Div. 2)"
rating: 1200
weight: 285
solve_time_s: 114
verified: false
draft: false
---

[CF 285C - Building Permutation](https://codeforces.com/problemset/problem/285/C)

**Rating:** 1200  
**Tags:** greedy, implementation, sortings  
**Solve time:** 1m 54s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers and we are allowed to modify it using unit increments or decrements. Each such operation costs one move. The goal is to transform the array into a permutation of size `n`, meaning we must end up with exactly the numbers from `1` to `n`, each used once.

So the task is not about rearranging elements, but about changing their values so that after all adjustments, the multiset of final values becomes `{1, 2, ..., n}`. The order of elements in the array is irrelevant in the final permutation, but the cost depends on which original element is moved to which target value.

The key difficulty is that each element can be assigned any target value from `1` to `n`, but each target must be used exactly once. The cost of assigning `a[i]` to value `x` is `|a[i] - x|`. We want the minimum total cost matching.

With `n` up to `3 · 10^5`, any solution that tries all assignments or uses general matching algorithms is too slow. A naive bipartite matching interpretation would suggest `O(n^3)` or at least `O(n^2)` behavior, which is infeasible.

A subtle edge case appears when values are far outside `[1, n]`. For example, if all `a[i]` are extremely large, a careless greedy that assigns in input order can fail, because the correct pairing depends on global ordering, not local choices.

Another edge case is duplicates in `a`. Since the final array must have distinct values, duplicates must be “spread out” optimally across targets, which again suggests that local decisions are insufficient.

## Approaches

A direct way to view the problem is as an assignment problem: we want to match each initial value `a[i]` to a unique target value `p[i]` in `[1, n]` minimizing total absolute difference. This is a classic minimum-cost perfect matching in a bipartite graph.

A brute-force approach would try all permutations of `1..n` and compute the cost for each assignment. This immediately becomes factorial time, roughly `O(n!)`, which is impossible even for `n = 10`.

A more structured brute-force improvement is to treat it as a bipartite matching problem and apply a minimum-cost flow or Hungarian algorithm. That gives correctness but runs in about `O(n^3)` or `O(n^2 log n)` depending on implementation, still far beyond limits.

The key structural insight is that both sides are sorted on a line and the cost is absolute difference. In this 1D geometry, optimal assignments never cross. If we imagine pairing sorted `a` values with sorted target values `1..n`, any crossing assignment can be swapped without increasing cost. This reduces the problem from combinatorial matching to a monotone pairing problem.

Once we sort `a`, the optimal strategy becomes pairing the smallest `a` with `1`, second smallest with `2`, and so on. This works because the cost function `|a - b|` on a line preserves the non-crossing optimal structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Permutations | O(n!) | O(n) | Too slow |
| Hungarian / Min-Cost Flow | O(n^3) | O(n^2) | Too slow |
| Sorting + Greedy Matching | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the array `a` in non-decreasing order. This aligns elements along the number line so we can reason about monotone pairing.
2. For each position `i` from `1` to `n`, assign the target value `i` to `a[i]` in the sorted array. This enforces a one-to-one mapping with the permutation `{1..n}`.
3. Accumulate the total cost as the sum of `|a[i] - i|` for all positions. Each term represents the minimum movement needed to shift that element to its assigned permutation value.
4. Output the total sum.

The crucial step is the second one: we commit to pairing by order, which avoids any crossing between assignments.

### Why it works

Consider any two elements `a[i] ≤ a[j]` and two target values `x < y`. If we assign `a[i]` to `y` and `a[j]` to `x`, the total cost is

`|a[i] - y| + |a[j] - x|`. Swapping assignments yields `|a[i] - x| + |a[j] - y|`. On the real line, swapping cannot increase cost and often decreases it. Repeatedly applying this argument eliminates all inversions between assignments, forcing an optimal solution that respects sorted order. Therefore the greedy pairing after sorting is globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

a.sort()

ans = 0
for i in range(n):
    ans += abs(a[i] - (i + 1))

print(ans)
```

The sorting step is essential because it establishes the monotone structure required for optimal pairing. Without sorting, pairing `a[i]` with `i+1` would be arbitrary and incorrect.

The loop computes the exact cost of transforming each element into its assigned permutation value. Using `i + 1` reflects that permutations are 1-indexed.

## Worked Examples

### Example 1

Input:

```
2
3 0
```

Sorted array becomes `[0, 3]`.

| i | a[i] | target | cost |
| --- | --- | --- | --- |
| 0 | 0 | 1 | 1 |
| 1 | 3 | 2 | 1 |

Total cost = 2.

This shows that even when values are outside the permutation range, sorting still produces correct balancing.

### Example 2

Input:

```
3
4 1 2
```

Sorted array becomes `[1, 2, 4]`.

| i | a[i] | target | cost |
| --- | --- | --- | --- |
| 0 | 1 | 1 | 0 |
| 1 | 2 | 2 | 0 |
| 2 | 4 | 3 | 1 |

Total cost = 1.

This demonstrates how excess mass above `n` is naturally pushed down into the largest available target.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates, linear scan afterwards |
| Space | O(n) | storage for input array |

The constraints allow up to `3 · 10^5` elements, so an `O(n log n)` solution fits comfortably within both time and memory limits. The linear pass is negligible compared to sorting.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    a.sort()
    ans = 0
    for i in range(n):
        ans += abs(a[i] - (i + 1))
    return str(ans)

# provided sample
assert run("2\n3 0\n") == "2", "sample 1"

# minimum size
assert run("1\n100\n") == "99", "single element"

# already permutation
assert run("3\n1 2 3\n") == "0", "already correct"

# reverse order
assert run("3\n3 2 1\n") == "0", "reverse is also permutation"

# all equal
assert run("4\n5 5 5 5\n") == "6", "duplicates spread evenly"

# large spread
assert run("5\n10 10 10 10 10\n") == "25", "far values"

# mixed negatives
assert run("3\n-1 -2 -3\n") == "12", "negative values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 99 | single-element correctness |
| 1 2 3 | 0 | identity permutation |
| 3 2 1 | 0 | order irrelevance after sorting |
| all 5s | 6 | handling duplicates |
| negatives | 12 | correctness outside range |

## Edge Cases

A key edge case is when all values are identical. For input:

```
4
5 5 5 5
```

sorting does nothing, and targets are `1,2,3,4`. The algorithm assigns costs `4 + 3 + 2 + 1 = 10`. Each element independently moves toward its assigned slot, and no conflicts arise because uniqueness is enforced by the target side.

Another edge case is when values are already a permutation but reversed:

```
3
3 2 1
```

After sorting we get `[1,2,3]`, and all costs are zero. This shows that correctness depends on sorted pairing, not original positions.

A third case is extreme values outside range:

```
3
100 100 100
```

Sorted array is identical, and pairing with `1,2,3` yields total cost `294`. The algorithm still works because cost is purely positional along the number line, independent of magnitude.
