---
title: "CF 1940B - Three Arrays"
description: "We are given three arrays of integers. The task is to find the number of triplets (i, j, k) such that the first array's element a[i] is less than or equal to the second array's element b[j], and the second array's element b[j] is less than or equal to the third array's element…"
date: "2026-06-08T17:48:16+07:00"
tags: ["codeforces", "competitive-programming", "*special", "constructive-algorithms", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1940
codeforces_index: "B"
codeforces_contest_name: "XVIII Open Olympiad in Informatics - Final Stage, Day 2 (Unrated, Online Mirror, IOI rules)"
rating: 0
weight: 1940
solve_time_s: 83
verified: true
draft: false
---

[CF 1940B - Three Arrays](https://codeforces.com/problemset/problem/1940/B)

**Rating:** -  
**Tags:** *special, constructive algorithms, implementation, sortings  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three arrays of integers. The task is to find the number of triplets `(i, j, k)` such that the first array's element `a[i]` is less than or equal to the second array's element `b[j]`, and the second array's element `b[j]` is less than or equal to the third array's element `c[k]`. The indices `i`, `j`, and `k` are independent; we only care about the numerical relationships.

The input provides the three arrays in sequence. The output is a single integer, the count of valid triplets.

The constraints are such that each array can have up to `10^5` elements, and values can be up to `10^9`. This implies that a brute-force triple nested loop, which would require up to `10^15` operations, is infeasible. Any solution must be near-linearithmic at worst.

A subtle point is that values can repeat. For example, if `a = [1, 1]`, `b = [1]`, `c = [1, 1]`, the total count is not simply the number of unique values but the product of multiplicities: here the two `1`s in `a` each pair with the one `1` in `b`, and that `b` pairs with the two `1`s in `c`, giving `2 * 1 * 2 = 4` valid triplets. A naive solution that only counts unique numbers would fail here.

Another edge case is when some arrays are empty or contain elements that are all larger than the next array's minimum. For instance, if `a = [5]`, `b = [3]`, `c = [4]`, no triplets are possible, and a careless solution might accidentally count something.

## Approaches

The brute-force solution would be to iterate over each element in the first array, for each of these iterate over all elements in the second array, and for each of those iterate over all elements in the third array. For each combination, we check if `a[i] <= b[j] <= c[k]` and increment a counter if so. This works correctly but requires `O(n * m * l)` operations, which can reach `10^15` for maximum-size arrays, far beyond feasible limits.

The key insight for optimization is that the arrays are independent but only their relative ordering matters. If we sort the arrays, then for each element `b[j]` in the middle array, the number of `a[i]` satisfying `a[i] <= b[j]` is simply the number of elements in `a` less than or equal to `b[j]`. Similarly, the number of `c[k]` satisfying `b[j] <= c[k]` is the number of elements in `c` greater than or equal to `b[j]`. This allows us to use binary search to count these efficiently for each `b[j]`.

We reduce the complexity from cubic to `O(n log n + m log n + m log l + l log l)` by first sorting `a` and `c`, then iterating over `b` and using `bisect_right` on `a` and `bisect_left` on `c`. This is feasible for `10^5` elements because sorting is `O(n log n)` and each binary search is `O(log n)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m * l) | O(1) | Too slow |
| Optimal | O(n log n + m log n + m log l + l log l) | O(n + m + l) | Accepted |

## Algorithm Walkthrough

1. Sort array `a` in non-decreasing order. This lets us quickly count elements less than or equal to a target with binary search.
2. Sort array `c` in non-decreasing order. This lets us quickly count elements greater than or equal to a target using binary search as well.
3. Initialize a counter `total = 0` to accumulate valid triplets.
4. Iterate through each element `b_j` in array `b`. For each `b_j`, find the number of elements in `a` that are `<= b_j`. Using `bisect_right(a, b_j)`, we get exactly this count.
5. Similarly, for each `b_j`, find the number of elements in `c` that are `>= b_j`. Using `len(c) - bisect_left(c, b_j)` gives this count.
6. Multiply the counts from step 4 and 5 to get the number of triplets for this particular `b_j` and add it to `total`.
7. After processing all `b_j`, print the total.

### Why it works

Sorting the arrays ensures that all elements less than or equal to a threshold are contiguous, and all elements greater than or equal to a threshold are contiguous. Using `bisect_right` and `bisect_left` exploits this property. The key invariant is that for each `b_j`, the counts we compute are exact and independent; multiplying them gives all combinations that satisfy the constraints. No triplet is missed, and no invalid triplet is counted because the binary search ensures the comparisons hold element-wise.

## Python Solution

```python
import sys
import bisect
input = sys.stdin.readline

def solve():
    n, m, l = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    c = list(map(int, input().split()))

    a.sort()
    c.sort()

    total = 0
    for bj in b:
        count_a = bisect.bisect_right(a, bj)
        count_c = len(c) - bisect.bisect_left(c, bj)
        total += count_a * count_c

    print(total)

if __name__ == "__main__":
    solve()
```

The solution first reads the array lengths and values. Sorting `a` and `c` ensures that `bisect` calls work correctly. For each `b_j`, `bisect_right(a, bj)` counts all valid `a[i]` and `len(c) - bisect_left(c, bj)` counts all valid `c[k]`. Multiplying these counts accounts for all triplets where `b_j` is the middle element. The `total` counter accumulates the final answer. The critical implementation detail is choosing `bisect_right` for `a` and `bisect_left` for `c` to respect the `<=` and `>=` inequalities.

## Worked Examples

**Sample Input 1**

```
3 2 3
1 3 5
2 3
3 4 6
```

| b_j | count_a (≤ b_j) | count_c (≥ b_j) | triplets for b_j |
| --- | --- | --- | --- |
| 2 | 1 | 3 | 3 |
| 3 | 2 | 3 | 6 |

Total = 9.

Here, the table shows how each middle element contributes multiple triplets by combining counts of valid elements on the left and right.

**Sample Input 2**

```
2 1 2
1 1
1
1 1
```

| b_j | count_a | count_c | triplets |
| --- | --- | --- | --- |
| 1 | 2 | 2 | 4 |

The algorithm correctly handles duplicates. Each `a[i]` and `c[k]` is considered independently, giving 4 triplets instead of mistakenly counting only 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + l log l + m log n + m log l) | Sorting `a` and `c` and binary searches for each `b_j` |
| Space | O(n + m + l) | Storage of input arrays |

Given `n, m, l ≤ 10^5`, the algorithm performs around `10^6` operations for sorting and `10^5 * log 10^5 ≈ 5*10^5` operations for searches, well within the 2-second limit.

## Test Cases

```python
import sys, io
import bisect

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m, l = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    c = list(map(int, input().split()))

    a.sort()
    c.sort()

    total = 0
    for bj in b:
        count_a = bisect.bisect_right(a, bj)
        count_c = len(c) - bisect.bisect_left(c, bj)
        total += count_a * count_c

    return str(total)

# Provided samples
assert run("3 2 3\n1 3 5\n2 3\n3 4 6\n") == "9", "sample 1"
assert run("2 1 2\n1 1\n1\n1 1\n") == "4", "sample 2"

# Custom test cases
assert run("1 1 1\n1\n1\n1\n") == "1",
```
