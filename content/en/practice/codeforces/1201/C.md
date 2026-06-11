---
title: "CF 1201C - Maximum Median"
description: "We are given a list of numbers and allowed to repeatedly increase any single element by one unit, with a fixed budget of operations. The goal is to maximize the median after all operations are applied."
date: "2026-06-11T23:49:54+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1201
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 577 (Div. 2)"
rating: 1400
weight: 1201
solve_time_s: 105
verified: false
draft: false
---

[CF 1201C - Maximum Median](https://codeforces.com/problemset/problem/1201/C)

**Rating:** 1400  
**Tags:** binary search, greedy, math, sortings  
**Solve time:** 1m 45s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a list of numbers and allowed to repeatedly increase any single element by one unit, with a fixed budget of operations. The goal is to maximize the median after all operations are applied. Since the median is defined as the middle element once the array is sorted, only the central part of the sorted array really matters: elements strictly below the median do not influence its final value unless they manage to overtake it, which is expensive and unnecessary.

The key difficulty is that operations are not restricted to a single position. We can distribute increments arbitrarily across the array, but each unit increase costs exactly one operation. This turns the problem into a resource allocation task where we try to “push up” the median and possibly some elements above it.

The constraints are large enough that any solution that tries to simulate operations step by step is impossible. With up to 200,000 elements and up to 1e9 operations, even O(nk) reasoning is completely infeasible. Sorting is fine, O(n log n), and then we need a linear or logarithmic strategy on top of it.

A naive but tempting idea is to try greedily increasing elements below or equal to the median in some order, but this fails because the median depends on relative ordering, not absolute values. For example, increasing a small element far below the median does not affect the median unless it crosses many others, which is wasteful compared to directly increasing median-level elements.

A more subtle edge case appears when many elements are equal around the median. If we incorrectly assume we only need to raise a single position, we underestimate the cost of keeping the median position stable as we push it upward. The correct approach must account for all elements in the upper half simultaneously.

## Approaches

The brute-force approach would simulate the process: repeatedly apply operations and track the median after each increment, always choosing a position that seems locally beneficial. This works in principle because every operation is explicitly modeled, but it quickly becomes unusable because each step may require sorting or at least maintaining order, and we may perform up to 1e9 operations.

The key structural insight is that only elements at or above the median index matter. Once the array is sorted, the median is at position m = n // 2 (0-indexed). If we want to raise the median to some value X, then every element from index m to n - 1 must be at least X. If any of these elements are below X, we must spend operations to raise them. There is no benefit in modifying elements below the median, since they do not contribute to pushing the median upward unless they cross the boundary, which is strictly more expensive than raising the upper half directly.

This reduces the problem to checking feasibility: for a candidate median value X, compute how many operations are needed to make all elements in the upper half at least X. If this cost is ≤ k, then X is achievable. This is monotonic: if X is achievable, then any smaller value is also achievable, which makes binary search applicable.

We sort the array and focus on indices from m to n - 1. The cost to raise the median to X is the sum over these indices of max(0, X - a[i]). We binary search the largest X that is feasible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(k log n) or worse | O(n) | Too slow |
| Binary Search + Greedy Check | O(n log(maxA + k)) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the array so that median position and upper half are fixed and stable.
2. Identify the median index m = n // 2, since this is the element we are trying to maximize.
3. Define a function that checks whether a target value X can become the median.
4. In this check, compute the total cost to raise all elements from index m to n - 1 up to X.

This is correct because increasing any element below the median does not help maintain or increase the median efficiently.
5. If the total cost is within k, then X is achievable, so we try larger values.
6. Otherwise, X is too large, so we reduce the search space.
7. Use binary search over the answer space, starting from the current median value up to the median value plus k.
8. Return the largest feasible value found.

### Why it works

After sorting, the median is determined solely by the element at index m, but to increase that value, we must ensure at least half the array elements on the right side are not smaller than it. Any valid final configuration must have the entire upper half raised to at least the median value; otherwise, sorting would push smaller elements into the median position and reduce it. Therefore, the cost function precisely measures the minimal required work to enforce a given median threshold. The monotonicity of feasibility guarantees that binary search finds the maximum reachable median.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()

    m = n // 2

    def can(x):
        cost = 0
        for i in range(m, n):
            if a[i] < x:
                cost += x - a[i]
                if cost > k:
                    return False
        return True

    lo = a[m]
    hi = a[m] + k

    ans = lo
    while lo <= hi:
        mid = (lo + hi) // 2
        if can(mid):
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by sorting the array so that the median position is well-defined. The feasibility check only considers the upper half starting from the median index, because these are the elements that determine whether a candidate median can be sustained after sorting.

The binary search range is chosen carefully: the median cannot decrease below its initial value, and the maximum possible increase happens if all k operations are applied directly to the median element, giving an upper bound of a[m] + k.

The check function accumulates the cost of lifting all upper-half elements to at least the candidate value. Early termination when cost exceeds k is important for efficiency.

## Worked Examples

### Example 1

Input:

```
3 2
1 3 5
```

Sorted array is already `[1, 3, 5]`, median index is 1.

| Step | lo | hi | mid | cost to raise upper half | feasible |
| --- | --- | --- | --- | --- | --- |
| init | 3 | 5 | 4 | 1 (only 5 is fine, 3 needs +1) | yes |
| next | 5 | 5 | 5 | 2 (3→5 costs 2) | yes |

The binary search converges to 5. This shows that even though only one element is directly at median position, raising the entire upper half is still affordable and yields a higher median.

### Example 2

Input:

```
5 4
1 2 3 4 5
```

Sorted array is `[1,2,3,4,5]`, median index is 2.

| Step | lo | hi | mid | cost (upper half ≥ mid index) | feasible |
| --- | --- | --- | --- | --- | --- |
| init | 3 | 7 | 5 | (3→5=2,4→5=1,5→5=0) total=3 | yes |
| next | 5 | 7 | 6 | (3→6=3,4→6=2,5→6=1) total=6 | no |
| next | 5 | 5 | 5 | 3 | yes |

Answer is 5. This demonstrates how pushing the median requires lifting multiple elements together, not just the middle one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log k) | Sorting costs O(n log n), each feasibility check is O(n), and binary search runs in O(log k) steps |
| Space | O(1) extra | Sorting is in-place aside from input storage |

The constraints allow up to 2e5 elements, and log k is around 30, so the total number of operations is comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return str(solve_output(inp))

# Re-implement wrapper for testing
def solve_output(inp: str) -> str:
    data = list(map(int, inp.split()))
    n, k = data[0], data[1]
    a = data[2:]
    a.sort()
    m = n // 2

    def can(x):
        cost = 0
        for i in range(m, n):
            if a[i] < x:
                cost += x - a[i]
                if cost > k:
                    return False
        return True

    lo, hi = a[m], a[m] + k
    ans = lo
    while lo <= hi:
        mid = (lo + hi) // 2
        if can(mid):
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return str(ans)

# samples
assert solve_output("3 2 1 3 5") == "5"

# custom tests
assert solve_output("1 10 100") == "110", "single element"
assert solve_output("5 0 1 2 3 4 5") == "3", "no operations allowed"
assert solve_output("5 100 1 1 1 1 1") == "101", "all equal large k"
assert solve_output("3 1 1 10 10") == "10", "small k shift median"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 10 100 | 110 | single-element behavior |
| 5 0 1 2 3 4 5 | 3 | zero operations constraint |
| 5 100 1 1 1 1 1 | 101 | uniform array growth |
| 3 1 1 10 10 | 10 | minimal adjustment edge case |

## Edge Cases

One important edge case is when all elements are equal. In this situation, every increment directly contributes to raising the median because the upper half is identical. The algorithm handles this cleanly because the cost function simply becomes `(n - m) * (X - value)` and binary search naturally distributes all k operations into increasing the target.

Another case is when k is zero. The binary search range collapses to the initial median value, and the feasibility check never allows any increase, correctly returning the original median without attempting unnecessary operations.

A third subtle case is when the median is already much larger than all elements below it. Since the algorithm ignores the lower half entirely, it still works because only the upper half constrains the median value; the lower elements cannot reduce it once sorting is fixed.
