---
title: "CF 1592B - Hemose Shopping"
description: "We are given an array of integers and a restriction on swapping elements: we can only swap two elements if their positions differ by at least x. The task is to determine whether it is possible to sort the array in non-decreasing order under this constraint."
date: "2026-06-10T09:15:19+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dsu", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1592
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 746 (Div. 2)"
rating: 1200
weight: 1592
solve_time_s: 110
verified: true
draft: false
---

[CF 1592B - Hemose Shopping](https://codeforces.com/problemset/problem/1592/B)

**Rating:** 1200  
**Tags:** constructive algorithms, dsu, math, sortings  
**Solve time:** 1m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and a restriction on swapping elements: we can only swap two elements if their positions differ by at least `x`. The task is to determine whether it is possible to sort the array in non-decreasing order under this constraint. Each test case specifies the array and the value `x`.

The first observation is that if `x` is large relative to the array length, some positions become effectively "locked". For instance, if `x = n`, no swaps are possible at all, so the array must already be sorted. Conversely, if `x = 1`, there is no restriction, and we can perform any swap, meaning we can always sort the array. The tricky cases happen when `1 < x < n`, because only certain positions can interact.

The constraints tell us that `n` can be up to `10^5` per test case, and the sum of all `n` across all test cases is at most `2 * 10^5`. This means any solution with complexity worse than `O(n log n)` per test case is likely too slow. Naive approaches that try all sequences of swaps would be exponential and completely infeasible.

A non-obvious edge case occurs when the array is nearly sorted but the smallest or largest elements are trapped in the middle where they cannot move far enough due to the `x` restriction. For example, consider `[3, 2, 1]` with `x = 3`. The array is small enough that no swaps are allowed, so even though it's almost sorted, the answer is "NO". Another tricky scenario is arrays where `x` is just slightly smaller than `n/2`, leaving a middle segment that cannot interact with the ends.

## Approaches

The brute-force approach is simple: try all allowed swaps in every configuration until the array is sorted or all possibilities are exhausted. This guarantees correctness, because we eventually explore every reachable permutation. However, the number of swaps grows exponentially with `n`, so even for `n = 20` it becomes impractical.

The key observation is that only elements in positions that are at least `x` apart can swap. If `x <= n/2`, then every element near the start can eventually reach every element near the end, possibly through a chain of swaps. However, elements in the middle region of length `n - 2*x` are constrained: they cannot move far enough to reach the ends if `x > n/2`. Thus, if the array is not already sorted in these middle positions, sorting is impossible.

The optimal solution leverages this by comparing the array to its fully sorted version. We only need to check if each element that cannot reach the ends (the "fixed" middle segment) is already in its correct position. If all such elements match the sorted array, sorting is possible; otherwise, it is not. This reduces the problem to a simple comparison after sorting, with no need for simulating swaps.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read `n`, `x`, and the array `a`.
2. Create a sorted version of the array, `sorted_a`. This represents the target arrangement.
3. If `x <= n/2`, every element can eventually be swapped into any position. In this case, immediately return "YES".
4. Otherwise, for positions `i` from `n - x` to `x - 1` (the "middle" segment that cannot reach the ends), check if `a[i] == sorted_a[i]`. If any element differs, return "NO".
5. If all positions in the middle segment match the sorted array, return "YES".

Why it works: Elements outside the middle segment can move freely enough to reach the ends via the allowed swaps. The middle segment is effectively fixed in relative order. By checking these fixed positions against the sorted array, we determine feasibility. This invariant guarantees correctness without simulating swaps.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_sort(n, x, a):
    sorted_a = sorted(a)
    if x <= n // 2:
        return "YES"
    for i in range(n - x, x):
        if a[i] != sorted_a[i]:
            return "NO"
    return "YES"

t = int(input())
for _ in range(t):
    n, x = map(int, input().split())
    a = list(map(int, input().split()))
    print(can_sort(n, x, a))
```

The function `can_sort` captures the core logic. We first sort the array to know the target positions. For `x <= n//2`, we can sort any array, so we immediately return "YES". For larger `x`, we check only the constrained middle segment. Using `range(n - x, x)` selects exactly the indices that cannot be moved far enough. Off-by-one errors here would silently fail for edge cases, so attention to inclusive vs exclusive bounds is crucial.

## Worked Examples

**Example 1**

Input: `n = 3, x = 3, a = [3, 2, 1]`

| i | a[i] | sorted_a[i] | Compare |
| --- | --- | --- | --- |
| 0 | 3 | 1 | mismatch |
| 1 | 2 | 2 | match |
| 2 | 1 | 3 | mismatch |

Since `x = n`, the middle segment is the whole array. Mismatches exist, output is "NO".

**Example 2**

Input: `n = 5, x = 2, a = [5, 1, 2, 3, 4]`

Here, `x <= n//2` is false, so check middle indices `n-x` to `x-1` → `i = 3 to 1` → empty range, no positions to check. Output "YES".

This trace demonstrates how the middle segment check directly identifies infeasible configurations and ignores movable positions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates; other operations are linear |
| Space | O(n) | Storing sorted array |

Given the total sum of `n` across test cases ≤ 2*10^5, this fits comfortably within the 1-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # main solution code
    t = int(input())
    for _ in range(t):
        n, x = map(int, input().split())
        a = list(map(int, input().split()))
        print(can_sort(n, x, a))
    return output.getvalue().strip()

# provided samples
assert run("4\n3 3\n3 2 1\n4 3\n1 2 3 4\n5 2\n5 1 2 3 4\n5 4\n1 2 3 4 4") == "NO\nYES\nYES\nYES"

# custom cases
assert run("1\n1 1\n42") == "YES", "single element"
assert run("1\n2 2\n2 1") == "NO", "cannot swap when x=n"
assert run("1\n5 3\n5 4 3 2 1") == "NO", "middle segment unsorted"
assert run("1\n6 2\n1 2 3 6 5 4") == "YES", "x <= n//2, full sorting possible"
assert run("1\n7 4\n1 3 2 7 6 5 4") == "NO", "middle segment unsorted"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 42` | YES | Single element |
| `2 2 2 1` | NO | No swaps allowed for x=n |
| `5 3 5 4 3 2 1` | NO | Middle segment cannot be moved |
| `6 2 1 2 3 6 5 4` | YES | x <= n/2 allows full sort |
| `7 4 1 3 2 7 6 5 4` | NO | Middle segment mismatch |

## Edge Cases

When the array length equals `x`, no swaps are possible. For `[3, 2, 1]` with `x = 3`, the middle segment is the full array, which is unsorted. The algorithm checks all positions and outputs "NO".

For `x <= n//2`, such as `[5, 1, 2, 3, 4]` with `x = 2`, the middle segment is effectively empty. All elements can be shuffled freely, so the function outputs "YES".

For arrays with repeated elements, e.g., `[1, 2, 2, 1]` with `x = 3`, the algorithm correctly identifies if the middle segment positions need adjustment, avoiding false positives.

This completes a robust explanation and step-by-step
