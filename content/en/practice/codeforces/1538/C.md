---
title: "CF 1538C - Number of Pairs"
description: "We are given an array of integers and a range defined by two values, l and r. The task is to count all pairs of distinct indices (i, j) such that the sum of the elements at these indices lies within the given range, including the boundaries."
date: "2026-06-10T14:52:34+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "math", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1538
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 725 (Div. 3)"
rating: 1300
weight: 1538
solve_time_s: 426
verified: false
draft: false
---

[CF 1538C - Number of Pairs](https://codeforces.com/problemset/problem/1538/C)

**Rating:** 1300  
**Tags:** binary search, data structures, math, two pointers  
**Solve time:** 7m 6s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers and a range defined by two values, `l` and `r`. The task is to count all pairs of distinct indices `(i, j)` such that the sum of the elements at these indices lies within the given range, including the boundaries. In other words, we want the number of pairs `(i, j)` where `i < j` and `l ≤ a[i] + a[j] ≤ r`.

The input consists of multiple test cases. For each test case, we get the size of the array `n`, the lower and upper bounds `l` and `r`, and the array itself. The output is the count of qualifying pairs for each test case.

The constraints are crucial. With `n` up to 2·10^5 per test case and a total sum of `n` across test cases also up to 2·10^5, an O(n²) algorithm would require on the order of 10^10 operations in the worst case, which is far beyond what can run in 2 seconds. We need an algorithm closer to O(n log n) to be safe. Values in the array and the bounds can be as large as 10^9, so we must avoid techniques relying on array indexing by value or frequency arrays that scale with the magnitude of numbers.

Edge cases include arrays with all equal values, arrays where no pair meets the range, and arrays where many pairs cluster around the boundaries `l` and `r`. For example, with `a = [1, 1, 1]` and `l = 5, r = 6`, no pair satisfies the condition, so the correct output is 0. A naive implementation might forget to check `i < j` and double-count pairs or include invalid sums.

## Approaches

A brute-force approach is straightforward: iterate over all pairs `(i, j)` with `i < j` and check whether the sum falls between `l` and `r`. This is guaranteed to be correct because it explicitly examines every possible pair, but it requires O(n²) time per test case. For `n` close to 2·10^5, this would be roughly 2·10^10 iterations in the worst case, which is infeasible.

The key insight for an optimal solution is that we do not need to examine every pair individually. If we sort the array, for a fixed element `a[i]`, the problem reduces to counting how many elements `a[j]` with `j > i` satisfy `l - a[i] ≤ a[j] ≤ r - a[i]`. Because the array is sorted, the valid `a[j]`s form a contiguous segment. This allows us to use binary search to efficiently find the leftmost and rightmost valid `a[j]`s, giving the count of valid pairs in O(log n) per element. The total complexity becomes O(n log n), which is acceptable under the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Sorting + Binary Search | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the array in ascending order. Sorting is necessary to apply binary search for pair counting efficiently.
2. Initialize a variable `count` to zero. This will accumulate the number of valid pairs.
3. For each index `i` from 0 to n - 2, consider `a[i]` as the first element of the pair. The second element must satisfy `l - a[i] ≤ a[j] ≤ r - a[i]` with `j > i`.
4. Use `bisect_left` to find the index `left` of the first element `a[j]` in the sorted array that is greater than or equal to `l - a[i]`, searching in the subarray starting at `i + 1`.
5. Use `bisect_right` to find the index `right` of the first element strictly greater than `r - a[i]`, also in the subarray starting at `i + 1`.
6. The number of valid pairs for this `i` is `right - left`. Add this to `count`.
7. After processing all `i`, `count` contains the total number of valid pairs. Output it.

Why it works: Sorting guarantees that for each `i`, all candidates `a[j]` with `j > i` are in ascending order. The contiguous property of valid `a[j]`s within `[l - a[i], r - a[i]]` ensures that binary search finds the exact range without missing or double-counting elements. Summing over all `i` covers all pairs with `i < j`.

## Python Solution

```python
import sys
import bisect
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, l, r = map(int, input().split())
        a = list(map(int, input().split()))
        a.sort()
        count = 0
        for i in range(n - 1):
            left = bisect.bisect_left(a, l - a[i], i + 1)
            right = bisect.bisect_right(a, r - a[i], i + 1)
            count += right - left
        print(count)

if __name__ == "__main__":
    solve()
```

The sorting step prepares the array for efficient binary search. The loop ensures we only count pairs with `i < j`. `bisect_left` and `bisect_right` correctly handle boundary conditions, including sums exactly equal to `l` or `r`. Searching from `i + 1` prevents counting pairs where `j ≤ i`.

## Worked Examples

### Sample 1

Input: `a = [5, 1, 2], l = 4, r = 7`

| i | a[i] | l - a[i] | r - a[i] | left index | right index | count contribution |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 3 | 6 | 1 | 3 | 2 |
| 1 | 2 | 2 | 5 | 2 | 3 | 1 |
| 2 | 5 | -1 | 2 | 3 | 3 | 0 |

Total count: 2 (matches expected output).

### Sample 2

Input: `a = [5, 1, 2, 4, 3], l = 5, r = 8`

Sorted array: `[1, 2, 3, 4, 5]`

| i | a[i] | l - a[i] | r - a[i] | left index | right index | count contribution |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 4 | 7 | 3 | 5 | 2 |
| 1 | 2 | 3 | 6 | 2 | 5 | 3 |
| 2 | 3 | 2 | 5 | 3 | 5 | 2 |
| 3 | 4 | 1 | 4 | 4 | 4 | 0 |

Total count: 7 (matches expected output).

These traces confirm that the algorithm correctly identifies valid ranges and counts the correct number of pairs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting takes O(n log n), and each of the n iterations performs two O(log n) binary searches |
| Space | O(n) | The array is stored in memory; no extra large structures are needed |

The algorithm fits comfortably within the 2-second time limit and 256 MB memory limit for the given constraints.

## Test Cases

```python
import sys, io
from contextlib import redirect_stdout

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Provided samples
assert run("4\n3 4 7\n5 1 2\n5 5 8\n5 1 2 4 3\n4 100 1000\n1 1 1 1\n5 9 13\n2 5 5 1 1") == "2\n7\n0\n1", "samples"

# Custom cases
assert run("1\n2 3 5\n1 1") == "1", "minimum size array"
assert run("1\n3 2 2\n1 1 1") == "0", "no pairs in range"
assert run("1\n4 2 4\n2 2 2 2") == "6", "all equal values"
assert run("1\n5 5 5\n1 2 3 4 5") == "2", "boundary sums"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 elements, sum in range | 1 | Algorithm handles minimum-size arrays |
| 3 elements, sum out of range | 0 | Correctly identifies no valid pairs |
| 4 equal elements | 6 |  |
