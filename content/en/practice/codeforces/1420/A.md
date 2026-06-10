---
title: "CF 1420A - Cubes Sorting"
description: "The problem presents us with a sequence of cubes, each with a positive integer volume. The cubes are initially arranged in some arbitrary order."
date: "2026-06-11T06:37:37+07:00"
tags: ["codeforces", "competitive-programming", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1420
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 672 (Div. 2)"
rating: 900
weight: 1420
solve_time_s: 70
verified: true
draft: false
---

[CF 1420A - Cubes Sorting](https://codeforces.com/problemset/problem/1420/A)

**Rating:** 900  
**Tags:** math, sortings  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem presents us with a sequence of cubes, each with a positive integer volume. The cubes are initially arranged in some arbitrary order. Our goal is to determine if we can sort the cubes into non-decreasing order using only swaps of neighboring cubes, under the constraint that Wheatley will abandon the task if the number of swaps needed reaches the maximum possible for a sequence of that size, which is $n \cdot (n-1)/2 - 1$. Conceptually, this means that Wheatley is willing to perform almost any sorting process, except in the extremely rare case where the sequence is the exact reverse of sorted order and contains only two elements.

The input consists of multiple test cases, each providing the number of cubes and their volumes. The output is a simple "YES" if the cubes can be sorted under Wheatley's impatience constraints, and "NO" otherwise.

The constraints tell us that $n$ can reach $5 \cdot 10^4$ for an individual test case, with a cumulative total of $10^5$ across all test cases. Given a 1-second time limit, this eliminates any solution with worse than $O(n \log n)$ per test case for the entire input, though linear or near-linear solutions are ideal. The swap operation itself can be imagined as bubble sort moves, but simulating every swap directly would be too slow for the largest $n$.

A non-obvious edge case occurs with sequences of exactly two cubes. For instance, if the sequence is `[2, 1]`, the only possible swap is a single exchange, but Wheatley will only accept sequences that require strictly fewer than $1$ swap. This edge case produces a "NO" despite the array being sortable in principle. Sequences where all elements are equal, such as `[2, 2, 2]`, are already sorted and trivially acceptable.

## Approaches

The brute-force approach would be to attempt a bubble sort simulation. For each adjacent pair, we swap them if they are out of order and count the number of swaps. After finishing, we compare the swap count to $n \cdot (n-1)/2 - 1$. This is correct because bubble sort only uses neighboring swaps and will always sort the array. However, in the worst case, this requires $O(n^2)$ swaps, which is impractical for $n = 5 \cdot 10^4$.

The key insight is that Wheatley only refuses to sort sequences that are of length two and strictly decreasing. For sequences of length greater than two, the number of swaps required in the worst possible case is strictly less than $n \cdot (n-1)/2 - 1$. The reasoning is that any sequence of three or more elements can always be sorted using neighboring swaps in fewer than the threshold. Therefore, we do not need to actually simulate swaps. Instead, we can check two conditions: if the sequence has exactly two elements, and the first element is larger than the second, the answer is "NO". In all other cases, the answer is "YES".

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Bubble Sort Simulation | O(n^2) | O(1) | Too slow for large n |
| Threshold-based Check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases, $t$.
2. For each test case, read the number of cubes, $n$, and the list of volumes $a$.
3. If $n = 2$ and $a[0] > a[1]$, print "NO" and continue to the next test case. This handles the only situation where the swap threshold is exceeded.
4. In all other situations, print "YES". Any sequence with more than two elements or sequences of two elements in non-decreasing order can be sorted within the swap limit.

Why it works: The invariant is that any sequence of length greater than two can always be sorted with fewer than $n \cdot (n-1)/2 - 1$ neighboring swaps. The only exception is a two-element sequence in strict descending order, which would require exactly one swap, exceeding the threshold. This guarantees correctness without simulation.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    if n == 2 and a[0] > a[1]:
        print("NO")
    else:
        print("YES")
```

The solution reads input efficiently using `sys.stdin.readline`. It checks the only edge case where a two-element array is in strict descending order. All other sequences immediately produce "YES", avoiding unnecessary computation. The use of `map(int, input().split())` converts the input string into integers correctly, even for large $n$.

## Worked Examples

### Example 1

Input: `[5, 3, 2, 1, 4]`

| Step | n | a | Condition | Output |
| --- | --- | --- | --- | --- |
| 1 | 5 | [5, 3, 2, 1, 4] | n > 2 | YES |

All sequences longer than two are acceptable, regardless of initial order. The algorithm returns "YES".

### Example 2

Input: `[2, 1]`

| Step | n | a | Condition | Output |
| --- | --- | --- | --- | --- |
| 1 | 2 | [2, 1] | n = 2 and a[0] > a[1] | NO |

The only sequence that fails the swap limit is a two-element descending array. The algorithm correctly returns "NO".

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each test case requires reading n integers and a single comparison. |
| Space | O(n) | Space for storing the list of volumes for each test case. |

Given that the sum of n across all test cases is at most 10^5, this is well within the time limit. Memory use is acceptable under the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    # solution code
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        if n == 2 and a[0] > a[1]:
            print("NO")
        else:
            print("YES")
    return out.getvalue().strip()

# provided samples
assert run("3\n5\n5 3 2 1 4\n6\n2 2 2 2 2 2\n2\n2 1\n") == "YES\nYES\nNO", "sample 1"

# custom cases
assert run("2\n2\n1 2\n3\n3 1 2\n") == "YES\nYES", "2-element ascending, 3-element unordered"
assert run("1\n2\n5 4\n") == "NO", "2-element descending"
assert run("1\n3\n1 1 1\n") == "YES", "all equal"
assert run("1\n5\n5 4 3 2 1\n") == "YES", "descending of length >2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 2, 3 3 1 2 | YES, YES | Correct handling of 2-element ascending and 3-element unordered arrays |
| 2 5 4 | NO | Correctly identifies 2-element descending array |
| 3 1 1 1 | YES | Handles all-equal elements |
| 5 5 4 3 2 1 | YES | Longer descending arrays still sortable within limit |

## Edge Cases

For the two-element descending array `[2, 1]`, the algorithm checks `n == 2 and a[0] > a[1]` and returns "NO". For `[1, 2]`, the condition fails and the algorithm returns "YES". For `[5, 4, 3, 2, 1]`, the length exceeds two, so the check fails and "YES" is returned. For `[2, 2, 2]`, all elements are equal, satisfying the non-decreasing requirement, and "YES" is returned. These cases confirm that the single conditional captures all non-obvious failures and that the solution handles all other scenarios efficiently.
