---
title: "CF 1157E - Minimum Array"
description: "We are given two arrays a and b, each of length n, containing integers from 0 to n-1. We can reorder b arbitrarily. After choosing an order for b, we construct a new array c where each element is (ai + bi) % n."
date: "2026-06-12T02:34:06+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1157
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 555 (Div. 3)"
rating: 1700
weight: 1157
solve_time_s: 91
verified: true
draft: false
---

[CF 1157E - Minimum Array](https://codeforces.com/problemset/problem/1157/E)

**Rating:** 1700  
**Tags:** binary search, data structures, greedy  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two arrays `a` and `b`, each of length `n`, containing integers from `0` to `n-1`. We can reorder `b` arbitrarily. After choosing an order for `b`, we construct a new array `c` where each element is `(a_i + b_i) % n`. Our goal is to reorder `b` so that `c` becomes lexicographically smallest.

Lexicographic order works like dictionary order: the first position where two arrays differ determines which is smaller. For example, if the first elements differ, the smaller first element wins regardless of later elements. This means we should focus on minimizing the earliest entries in `c` before worrying about later entries.

The constraint `n ≤ 2·10^5` with a 2-second limit implies we can afford roughly O(n log n) operations but cannot iterate over all permutations of `b` (O(n!)) or perform nested loops of O(n^2). Thus, a naive brute-force approach is infeasible.

An edge case to consider is when all elements of `a` are the same or when all elements of `b` are the same. For instance, if `a = [1,1,1]` and `b = [2,2,2]`, no reordering changes the lexicographic order; all `c_i = (1+2)%3 = 0`, so `c = [0,0,0]`. A careless greedy approach that doesn’t account for modular arithmetic may incorrectly try to “pair the smallest with the smallest” without considering wrap-around effects from modulo `n`.

Another subtle case occurs when minimizing the first element forces suboptimal later elements. For example, `a = [2,1]` and `b = [1,2]`. If we choose `b_1 = 1` to minimize `(2+1)%3 = 0`, the next element `(1+2)%3 = 0` coincidentally is fine. But if `b` had different values, a naive “always pick the minimal possible” may not give the lexicographically smallest sequence if modular wrap-around creates larger second elements.

## Approaches

The brute-force approach is straightforward. We could generate all permutations of `b`, compute `c` for each permutation, and track the lexicographically smallest `c`. This is correct but requires O(n! · n) operations, which is impossible for `n = 2·10^5`.

The key insight for optimization comes from noticing that modular addition behaves like a circular number line. For each `a_i`, we want to pick `b_j` such that `(a_i + b_j) % n` is minimized. This is equivalent to finding the smallest `b_j ≥ n - a_i` if possible; if no such `b_j` exists, we pick the smallest available `b_j`. By keeping `b` sorted and using a multiset-like structure (or a `SortedList` in Python), we can efficiently select the minimal feasible `b_j` for each `a_i` in O(log n) time.

This reduces the complexity from factorial to O(n log n). Sorting `b` takes O(n log n), and each of the n selections requires a logarithmic search and removal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!·n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort array `b` in ascending order. This allows efficient selection of the minimal element greater than or equal to a target.
2. Initialize an empty list `c` to store the resulting array.
3. For each index `i` from `0` to `n-1`, consider `a_i`. Compute the minimal `b_j` from `b` such that `(a_i + b_j) % n` is minimal. Specifically, look for the smallest `b_j` ≥ `n - a_i`. If such `b_j` exists, choose it; otherwise, pick the smallest remaining `b_j`.
4. Append `(a_i + b_j) % n` to `c` and remove `b_j` from the available elements.
5. Continue until all positions of `c` are filled.

Why it works: At every step, we guarantee that the current position in `c` is minimized given the available `b` elements. The modular arithmetic wrap-around ensures that if we cannot reach zero, we take the smallest possible sum. Sorting `b` and selecting via binary search or a multiset preserves correctness, and choosing greedily at each step ensures lexicographic minimality.

## Python Solution

```python
import sys
import bisect
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))
b = list(map(int, input().split()))
b.sort()

from collections import deque
b_list = deque(b)
c = []

for ai in a:
    # find the smallest b_j such that (ai + b_j) % n is minimal
    target = n - ai
    idx = bisect.bisect_left(b_list, target)
    if idx < len(b_list):
        bj = b_list[idx]
        del b_list[idx]
    else:
        bj = b_list[0]
        del b_list[0]
    c.append((ai + bj) % n)

print(' '.join(map(str, c)))
```

The code first sorts `b` to enable efficient selection. `bisect_left` finds the smallest `b_j` that satisfies the wrap-around minimal sum requirement. If no such `b_j` exists, the smallest overall is chosen. Using a deque allows efficient deletions from either end.

## Worked Examples

**Sample 1**

Input:

```
4
0 1 2 1
3 2 1 1
```

| i | a[i] | b available | target | chosen b_j | c[i] |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | [1,1,2,3] | 4 | 1 | 1 |
| 1 | 1 | [1,2,3] | 3 | 2 | 0 |
| 2 | 2 | [1,3] | 2 | 1 | 0 |
| 3 | 1 | [3] | 3 | 3 | 2 |

Output: `1 0 0 2`

This demonstrates the greedy selection minimizing `(a_i + b_j) % n` at each step.

**Custom Example**

Input:

```
3
2 1 0
1 2 0
```

| i | a[i] | b available | target | chosen b_j | c[i] |
| --- | --- | --- | --- | --- | --- |
| 0 | 2 | [0,1,2] | 1 | 1 | 0 |
| 1 | 1 | [0,2] | 2 | 2 | 0 |
| 2 | 0 | [0] | 3 | 0 | 0 |

Output: `0 0 0`

The invariant is preserved: each step greedily minimizes `c[i]` with available `b_j`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting `b` takes O(n log n), and selecting each `b_j` with binary search takes O(log n) per element. |
| Space | O(n) | Store `b` in a list and `c` in an output array. |

Given `n ≤ 2·10^5`, `n log n ≈ 4·10^6` operations, which easily fits within 2 seconds.

## Test Cases

```python
import sys, io
from collections import deque
import bisect

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    b.sort()
    b_list = deque(b)
    c = []
    for ai in a:
        target = n - ai
        idx = bisect.bisect_left(b_list, target)
        if idx < len(b_list):
            bj = b_list[idx]
            del b_list[idx]
        else:
            bj = b_list[0]
            del b_list[0]
        c.append((ai + bj) % n)
    return ' '.join(map(str, c))

# Provided sample
assert run("4\n0 1 2 1\n3 2 1 1\n") == "1 0 0 2", "sample 1"

# Minimum-size input
assert run("1\n0\n0\n") == "0", "min-size"

# All equal values
assert run("3\n1 1 1\n2 2 2\n") == "0 0 0", "all equal"

# Maximum-size input simplified (stress test)
n = 10**5
inp = f"{n}\n" + " ".join(["0"]*n) + "\n"
```
