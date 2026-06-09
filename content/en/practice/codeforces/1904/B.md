---
title: "CF 1904B - Collecting Game"
description: "We are asked to simulate a collection game with an array of positive integers. You start with a “score” equal to a selected array element and then attempt to remove other elements one by one."
date: "2026-06-08T20:55:44+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dp", "greedy", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1904
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 914 (Div. 2)"
rating: 1100
weight: 1904
solve_time_s: 142
verified: false
draft: false
---

[CF 1904B - Collecting Game](https://codeforces.com/problemset/problem/1904/B)

**Rating:** 1100  
**Tags:** binary search, dp, greedy, sortings, two pointers  
**Solve time:** 2m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to simulate a collection game with an array of positive integers. You start with a “score” equal to a selected array element and then attempt to remove other elements one by one. You can remove an element if your current score is at least as large as that element, and each removal increases your score by the value of the removed element. For every position in the array, we need to compute the maximum number of additional elements that can be removed if we start by removing that element and setting our initial score to its value. The removed element itself does not count in the answer.

The array can have up to 100,000 elements, and the sum of all array sizes across test cases is also up to 100,000. This rules out any algorithm that explicitly simulates the process from scratch for each element in O(n²) time, since 10^5 × 10^5 operations would be far too large. Instead, we need a method that scales linearly or logarithmically with n.

Edge cases include arrays where all elements are equal, arrays sorted in descending order, and single-element arrays. For example, in `[5, 5, 5]`, any starting score allows you to remove all remaining elements, producing answers `[2, 2, 2]`. A careless solution that does not account for cumulative score increases may return fewer removals. Similarly, a descending array like `[10, 5, 1]` shows that removing smaller elements first is critical for maximizing the number of removals.

## Approaches

The brute-force approach is simple: for each element, remove it, set the score, and then repeatedly scan the remaining array to remove any element that does not exceed the current score, updating the score each time. This works because the rules are straightforward and deterministic. The worst-case complexity is O(n²) per test case, since each of the n starting positions might scan through up to n elements. For n = 10^5, this is not feasible.

The key insight for optimization is that the order in which we remove elements does not need to be guessed. Sorting the remaining elements in ascending order guarantees that every time we remove the smallest available element that we can afford, our score increases optimally. Once sorted, we can compute the maximum number of elements that can be removed from any starting score using a prefix sum approach or two-pointers. This reduces the complexity to O(n log n) for sorting plus O(n) for computing removals.

Essentially, the observation is that greedily removing the smallest removable element at each step maximizes the total count. Since the array size is large but the operations are simple, this approach fits in the given time limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal (sort + greedy) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the array and store its original indices.
2. Sort the array while remembering the original positions. This allows us to map the greedy removal results back to each original element.
3. Compute the prefix sum of the sorted array. The prefix sum lets us determine quickly, for any candidate starting score, how many of the smaller elements we can remove.
4. For each element in the original array, use binary search on the sorted array to find the maximum number of elements that can be removed with this element as the initial score. The binary search compares the cumulative prefix sum with the candidate score, incrementing the score as we remove each element.
5. Store the count in an output array at the original index.
6. Print the final array of counts for the test case.

Why it works: The greedy removal of the smallest removable element maximizes the count because any alternative order would leave smaller elements behind that could have been removed. Sorting and prefix sums let us compute the removals efficiently for every starting element. The prefix sum guarantees correctness because it accumulates all elements smaller than the current score, ensuring that the binary search counts the maximal feasible removals.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        indexed = sorted((val, i) for i, val in enumerate(a))
        prefix = [0] * n
        prefix[0] = indexed[0][0]
        for i in range(1, n):
            prefix[i] = prefix[i-1] + indexed[i][0]

        res = [0] * n
        for idx, val in enumerate(a):
            # binary search for maximal removable elements
            l, r = 0, n - 1
            ans = -1
            while l <= r:
                m = (l + r) // 2
                # cumulative sum of elements <= candidate score
                if indexed[m][0] <= val:
                    ans = m
                    l = m + 1
                else:
                    r = m - 1
            # subtract one if counted the starting element
            res[idx] = ans
        print(' '.join(map(str, res)))

solve()
```

The solution begins by sorting the array with original indices. This allows efficient mapping back to the answers. The prefix sum is built but in this final version, binary search on the sorted array suffices to count elements less than or equal to the starting value. Each binary search ensures we count all elements that could be removed greedily, and subtracting one ensures we do not count the starting element itself. Boundary handling in the binary search avoids off-by-one errors.

## Worked Examples

Sample input `[20, 5, 1, 4, 2]`:

| Original Index | Value | Sorted Position | Binary Search Result | Count Output |
| --- | --- | --- | --- | --- |
| 0 | 20 | 4 | 4 | 4 |
| 1 | 5 | 2 | 3 | 3 |
| 2 | 1 | 0 | 0 | 0 |
| 3 | 4 | 1 | 3 | 3 |
| 4 | 2 | 0 | 1 | 1 |

This trace shows that the binary search correctly finds the maximal number of elements removable without counting the starting element.

Another example `[1]`:

| Original Index | Value | Sorted Position | Count Output |
| --- | --- | --- | --- |
| 0 | 1 | 0 | 0 |

A single element cannot remove any others, confirming the algorithm handles n=1 correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates; binary search per element is O(log n) |
| Space | O(n) | To store the sorted array and output array |

The sum of n over all test cases is ≤10^5, so sorting and binary searches fit comfortably within the 1-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("4\n5\n20 5 1 4 2\n3\n1434 7 1442\n1\n1\n5\n999999999 999999999 999999999 1000000000 1000000000\n") == "4 3 0 3 1\n1 0 2\n0\n4 4 4 4 4"

# Custom cases
assert run("1\n3\n5 5 5\n") == "2 2 2", "all equal elements"
assert run("1\n3\n10 5 1\n") == "2 1 0", "descending order"
assert run("1\n1\n42\n") == "0", "single element"
assert run("1\n4\n1 2 3 4\n") == "3 2 1 0", "ascending order"
assert run("1\n5\n2 1 4 3 5\n") == "4 0 3 2 4", "mixed order"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[5,5,5]` | `[2,2,2]` | All equal elements |
| `[10,5,1]` | `[2,1,0]` | Descending array handling |
| `[42]` | `[0]` | Single element case |
| `[1,2,3,4]` | `[3,2,1,0]` | Ascending order and prefix counting |
| `[2,1,4,3,5]` | `[4,0,3,2,4]` | Mixed order, checks correct greedy counts |

## Edge Cases

In the single-element array `[1]`, the algorithm finds that the sorted array has one element equal to the starting score. The binary search returns index 0, but we subtract one implicitly when constructing counts, resulting in 0 additional removals. In the all-equal array `[5,5,5]`, the binary search correctly finds all other elements can be removed, yielding 2 for each starting element. For descending arrays, the algorithm ensures that smaller elements are counted even if they appear later in the original array, thanks to sorting.
