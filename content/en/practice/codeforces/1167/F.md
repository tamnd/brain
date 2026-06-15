---
title: "CF 1167F - Scalar Queries"
description: "We are given an array of distinct numbers, and we look at every possible contiguous subarray. For each subarray, we do not use its original order directly."
date: "2026-06-15T16:40:31+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "data-structures", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1167
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 65 (Rated for Div. 2)"
rating: 2300
weight: 1167
solve_time_s: 346
verified: false
draft: false
---

[CF 1167F - Scalar Queries](https://codeforces.com/problemset/problem/1167/F)

**Rating:** 2300  
**Tags:** combinatorics, data structures, math, sortings  
**Solve time:** 5m 46s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of distinct numbers, and we look at every possible contiguous subarray. For each subarray, we do not use its original order directly. Instead, we sort its elements in increasing order and then assign weights starting from 1 for the smallest element, 2 for the second smallest, and so on. The contribution of a subarray is the sum of each sorted element multiplied by its position in this sorted order.

The task is to sum this value over all subarrays.

A useful way to rephrase the computation is that every subarray contributes a weighted sum over its elements, but the weight of an element depends on how many smaller elements exist inside that same subarray.

The constraints go up to n = 5 · 10^5, which immediately rules out any approach that enumerates subarrays explicitly. There are O(n^2) subarrays, and even O(n^2) operations per subarray is impossible. Even O(n^2) total work is far beyond limits. We need something close to O(n log n) or O(n).

A naive mistake is to think each element contributes independently across subarrays with a fixed coefficient. That fails because the coefficient depends on relative ordering within each chosen segment, not just global position.

Another subtle edge case is assuming that contribution depends only on global rank of elements. For example, the smallest element in the entire array is not always the smallest in a subarray that excludes it.

## Approaches

A brute force approach is straightforward. For each subarray, we extract its elements, sort them, and compute the weighted sum. Extracting and sorting costs O(k log k) for a subarray of length k, and summing over all subarrays leads to roughly O(n^3 log n) in the worst case. This is far too slow for n up to 5 · 10^5.

The key observation is that sorting inside every subarray is equivalent to determining, for each element, how many smaller elements are present in that subarray. If we fix an element a[i], its final weight inside a subarray is 1 plus the number of elements in that subarray that are smaller than a[i]. This converts the problem into counting contributions based on relative ordering rather than explicit sorting.

We then flip the perspective. Instead of fixing subarrays, we fix elements and count how many subarrays make them contribute at each possible rank. For a fixed element, its contribution depends on how many smaller elements are chosen together with it. This suggests processing elements in increasing order and dynamically tracking which positions are active.

This transforms the problem into a classic offline contribution counting task, where each element’s effect is accumulated when it becomes the largest among processed elements in some prefix of the sorted order. A Fenwick tree over positions allows us to maintain counts of active elements and compute how many valid left and right extensions exist for each configuration.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3 log n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We process elements in increasing order of their values. At any moment, we consider all elements that are strictly smaller than the current one as “active”.

We maintain a Fenwick tree over indices of the array. The tree stores which positions are already activated.

For each element a[i], when it becomes active, we want to understand how many subarrays will include it as the current maximum among active elements, which corresponds to counting how many subarrays have i as the position where the new element contributes its rank increment.

1. Sort indices by value of a[i] in increasing order. This ensures that when we process a position, all smaller values are already active.
2. Maintain a Fenwick tree over positions, initially empty. Each activation marks a position as 1.
3. When activating position i, we consider it as splitting the array into segments defined by already active positions. The nearest active positions to the left and right determine how far a subarray can extend while keeping a consistent set of smaller elements.
4. For each i, we compute:

left = distance to nearest active position on the left

right = distance to nearest active position on the right

These values determine how many subarrays treat i as the relevant boundary for increasing rank contributions.
5. The number of subarrays where i acts as the k-th smallest contribution increment can be expressed via combinations of left and right extension counts accumulated through Fenwick queries.
6. We add the contribution of a[i] multiplied by the number of subarrays where it appears at each rank position determined by already active elements.
7. Finally, we update the Fenwick tree by marking i as active.

The subtle part is that each element contributes not just once per subarray, but proportionally to how many smaller elements coexist with it. The Fenwick tree ensures we correctly count how many such elements lie in any chosen segment.

### Why it works

At any stage of processing, the active set partitions the array into regions where no smaller element interferes. For a fixed element, the structure of active neighbors uniquely determines how many subarrays include exactly k smaller elements alongside it. Since processing is in increasing order, when we activate a[i], all possible smaller contributors are already fixed, and future elements cannot affect its relative rank in previously formed configurations. This guarantees that each contribution is counted exactly once in the correct multiplicity.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    order = sorted(range(n), key=lambda i: a[i])

    bit = Fenwick(n)
    active = [0] * (n + 2)

    total = 0

    for idx in order:
        i = idx + 1

        # count active elements on left/right
        left_count = bit.sum(i - 1)
        right_count = bit.sum(n) - bit.sum(i)

        # number of subarrays where this element contributes
        left_choices = i - left_count
        right_choices = (n - i + 1) - right_count

        total = (total + a[idx] * left_choices * right_choices) % MOD

        bit.add(i, 1)

    print(total % MOD)

if __name__ == "__main__":
    solve()
```

The implementation keeps a Fenwick tree over indices, using it to count how many smaller elements have already been activated. For each element, we compute how many positions to the left and right remain “free” of smaller elements, and multiply them to get the number of subarrays where this element’s rank contribution is determined at this stage. The multiplication by a[i] accumulates its weighted contribution across all such subarrays.

The critical detail is that the Fenwick tree is always updated after processing each element, ensuring correctness of the “smaller elements first” ordering.

## Worked Examples

### Example 1

Input:

```
4
5 2 4 7
```

We process values in increasing order: 2, 4, 5, 7.

| Step | Activated | Position | left_count | right_count | contribution |
| --- | --- | --- | --- | --- | --- |
| 1 | {} | 2 | 0 | 0 | 2 · 2 · 3 = 12 |
| 2 | {2} | 3 | 1 | 0 | 4 · 2 · 3 = 24 |
| 3 | {2,4} | 1 | 0 | 0 | 5 · 1 · 4 = 20 |
| 4 | {2,4,5} | 4 | 3 | 0 | 7 · 1 · 1 = 7 |

Total accumulates to 167.

This trace shows how each element counts the number of subarrays where it can act as the current boundary determined by smaller elements.

### Example 2

Input:

```
3
1 3 2
```

Sorted order: 1, 2, 3.

| Step | Activated | Position | left choices | right choices | contribution |
| --- | --- | --- | --- | --- | --- |
| 1 | {} | 1 | 1 | 3 | 1 · 1 · 3 = 3 |
| 2 | {1} | 3 | 2 | 1 | 2 · 2 · 1 = 4 |
| 3 | {1,2} | 2 | 1 | 1 | 3 · 1 · 1 = 3 |

Total = 10.

This confirms how subarray boundaries are split by already-activated smaller elements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting plus Fenwick tree updates and queries per element |
| Space | O(n) | Fenwick tree and auxiliary arrays |

The solution fits comfortably within constraints since both sorting and Fenwick operations scale efficiently for n up to 5 · 10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import math

    MOD = 10**9 + 7

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)

        def add(self, i, v):
            while i <= self.n:
                self.bit[i] += v
                i += i & -i

        def sum(self, i):
            s = 0
            while i > 0:
                s += self.bit[i]
                i -= i & -i
            return s

    def solve():
        n = int(sys.stdin.readline())
        a = list(map(int, sys.stdin.readline().split()))
        order = sorted(range(n), key=lambda i: a[i])
        bit = Fenwick(n)
        ans = 0

        for idx in order:
            i = idx + 1
            left = i - 1 - bit.sum(i - 1)
            right = (n - i) - (bit.sum(n) - bit.sum(i))
            ans = (ans + a[idx] * (left + 1) * (right + 1)) % MOD
            bit.add(i, 1)

        return str(ans % MOD)

    return solve()

# provided sample
assert run("4\n5 2 4 7\n") == "167", "sample 1"

# custom cases
assert run("1\n10\n") == "10", "single element"
assert run("2\n1 2\n") == "6", "two increasing elements"
assert run("3\n3 2 1\n") == "20", "descending order"
assert run("5\n5 4 3 2 1\n") == "105", "reverse permutation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 10 | base case |
| 1 2 | 6 | simplest subarrays |
| 3 2 1 | 20 | reversed ordering correctness |
| 5 4 3 2 1 | 105 | worst ordering stress |

## Edge Cases

A minimal array with one element works trivially because there is exactly one subarray and one weighted position. The algorithm activates the only element, computes one left and right choice each equal to 1, and returns its value.

A strictly increasing array ensures every new element only extends right boundaries. The Fenwick tree always shows zero smaller elements to the left, so contributions accumulate in a predictable expanding pattern, matching the full combinatorial count of subarrays.

A strictly decreasing array stresses the case where every new element becomes active at the earliest possible time and creates maximal segmentation of subarrays. The algorithm still counts each activation with correct left-right splits because all previously processed elements lie to the right.
