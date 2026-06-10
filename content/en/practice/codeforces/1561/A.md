---
title: "CF 1561A - Simply Strange Sort"
description: "We are given a permutation of odd length n. A permutation here is a sequence containing all integers from 1 to n exactly once, arranged in some order."
date: "2026-06-10T12:15:32+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1561
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 740 (Div. 2, based on VK Cup 2021 - Final (Engine))"
rating: 800
weight: 1561
solve_time_s: 222
verified: false
draft: false
---

[CF 1561A - Simply Strange Sort](https://codeforces.com/problemset/problem/1561/A)

**Rating:** 800  
**Tags:** brute force, implementation, sortings  
**Solve time:** 3m 42s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation of odd length `n`. A permutation here is a sequence containing all integers from `1` to `n` exactly once, arranged in some order. The task is to determine how many iterations a particular sorting procedure will take to fully sort the permutation in ascending order.

The sorting procedure alternates between two passes. On odd-numbered iterations, it compares and swaps adjacent elements starting at index 1, then 3, then 5, up to `n-2`. On even-numbered iterations, it does the same starting at index 2, then 4, up to `n-1`. A swap occurs only if the left element is larger than the right element. Essentially, this is a variant of bubble sort, often called odd-even sort, which repeatedly pushes elements toward their correct position in a staggered pattern.

The constraints are modest. The length `n` of a permutation can be up to 999, and the sum of all `n` across test cases is also bounded by 999. With a time limit of 2 seconds, even an `O(n^2)` simulation is feasible because in the worst case `n^2` operations would be under a million, which is acceptable. Since `n` is odd, we avoid situations where even-length specific optimizations might apply.

Edge cases include already sorted sequences, where the algorithm should immediately return 0, and sequences with the largest element initially at the start or the smallest at the end. For example, for `n = 3` and `[3, 1, 2]`, careful tracking shows multiple iterations are needed even though some elements start in the correct relative order. A naive approach that simply checks inversion counts without simulating the odd-even pattern would produce the wrong number of iterations.

## Approaches

The brute-force approach is to literally simulate the described odd-even sorting procedure. On each iteration, perform all swaps according to the current iteration’s parity, and then check if the sequence is sorted. Repeat until sorted. This is guaranteed to terminate because the odd-even sort is a correct sorting algorithm and `n` is finite. The worst-case number of iterations is bounded by `n`, and each iteration performs roughly `n` comparisons, giving `O(n^2)` operations. For our constraints, this is acceptable.

The key insight for optimization is to notice that the problem's constraints are small enough that a straightforward simulation is already efficient. There is no hidden trick, because the sum of `n` across all test cases is ≤ 999, making an `O(n^2)` simulation per test case fast enough. Any attempt at a purely formulaic approach risks missing the exact interaction of odd-even passes with the specific permutation structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n²) per test case | O(n) | Accepted |
| Optimized / Formulaic | O(n) | O(n) | Unnecessary given constraints |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n` and the permutation `a`.
3. Initialize an iteration counter `iterations = 0`.
4. While the permutation is not sorted:

1. Increment the iteration counter.
2. Determine the starting index for swaps: `start = 0` for odd iterations, `start = 1` for even iterations (0-based indexing).
3. For every index `i` starting from `start` to `n-2` with a step of 2, compare `a[i]` and `a[i+1]`. Swap if `a[i] > a[i+1]`.
5. Once sorted, print the number of iterations.

Why it works: Each iteration moves some elements closer to their correct position. Odd-even sort guarantees that no element will indefinitely stay out of place because every adjacent inversion will eventually be corrected. The iteration count captures the first time the array is fully sorted. The procedure terminates because each swap reduces the number of inversions or leaves them unchanged, and there is a finite number of inversions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def odd_even_sort_iterations(a):
    n = len(a)
    iterations = 0
    while True:
        if all(a[i] <= a[i+1] for i in range(n-1)):
            return iterations
        iterations += 1
        start = 0 if iterations % 2 == 1 else 1
        for i in range(start, n-1, 2):
            if a[i] > a[i+1]:
                a[i], a[i+1] = a[i+1], a[i]

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    print(odd_even_sort_iterations(a))
```

The `odd_even_sort_iterations` function handles the main loop. Checking if the array is sorted using `all` ensures that we return 0 for already sorted arrays. Choosing the start index based on iteration parity is critical to correctly simulate the odd-even pattern. The in-place swap avoids extra memory usage.

## Worked Examples

For the input `[3, 2, 1]`:

| Iteration | Array | Explanation |
| --- | --- | --- |
| 0 | [3, 2, 1] | Initial array, not sorted |
| 1 | [2, 3, 1] | Odd iteration swaps 3>2 |
| 2 | [2, 1, 3] | Even iteration swaps 3>1 |
| 3 | [1, 2, 3] | Odd iteration swaps 2>1, now sorted |

For `[4, 5, 7, 1, 3, 2, 6]`:

| Iteration | Array |
| --- | --- |
| 1 | [4, 5, 1, 7, 2, 3, 6] |
| 2 | [4, 1, 5, 2, 7, 3, 6] |
| 3 | [1, 4, 2, 5, 3, 7, 6] |
| 4 | [1, 2, 4, 3, 5, 6, 7] |
| 5 | [1, 2, 3, 4, 5, 6, 7] |

These traces confirm that the simulation correctly counts the number of iterations until the first sorted state.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) per test case | Each iteration may check all n elements, and up to n iterations may be needed in the worst case |
| Space | O(n) | Only storing the array itself |

The constraints ensure that even worst-case `n²` operations remain well under 10⁶ total, which fits within the 2-second time limit and 512MB memory cap.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    t = int(input())
    out = []
    def odd_even_sort_iterations(a):
        n = len(a)
        iterations = 0
        while True:
            if all(a[i] <= a[i+1] for i in range(n-1)):
                return iterations
            iterations += 1
            start = 0 if iterations % 2 == 1 else 1
            for i in range(start, n-1, 2):
                if a[i] > a[i+1]:
                    a[i], a[i+1] = a[i+1], a[i]
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        out.append(str(odd_even_sort_iterations(a)))
    return "\n".join(out)

# Provided samples
assert run("3\n3\n3 2 1\n7\n4 5 7 1 3 2 6\n5\n1 2 3 4 5\n") == "3\n5\n0"

# Custom cases
assert run("2\n3\n1 3 2\n5\n5 4 3 2 1\n") == "1\n5", "swap-heavy and single swap cases"
assert run("1\n3\n1 2 3\n") == "0", "already sorted minimal"
assert run("1\n9\n9 8 7 6 5 4 3 2 1\n") == "9", "descending large odd length"
assert run("1\n3\n2 3 1\n") == "2", "middle element out of place"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3\n1 3 2\n5\n5 4 3 2 1\n` | `1\n5` | Handles single swaps and worst-case full reversal |
| `1\n3\n1 2 3\n` | `0` | Already sorted array, minimal size |
| `1\n9\n9 8 7 6 5 4 3 2 1\n` | `9` | Largest odd-length, descending array |
| `1\n3\n2 3 1\n` | `2` | Element in the middle moves |
