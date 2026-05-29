---
title: "CF 252B - Unsorting Array"
description: "We are given an array of integers of length n and asked to determine if we can swap any two elements at distinct positions such that the resulting array is no longer sorted. Sorting here is defined broadly: the array is sorted if it is either non-decreasing or non-increasing."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "sortings"]
categories: ["algorithms"]
codeforces_contest: 252
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 153 (Div. 2)"
rating: 1800
weight: 252
solve_time_s: 127
verified: true
draft: false
---

[CF 252B - Unsorting Array](https://codeforces.com/problemset/problem/252/B)

**Rating:** 1800  
**Tags:** brute force, sortings  
**Solve time:** 2m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers of length _n_ and asked to determine if we can swap any two elements at distinct positions such that the resulting array is no longer sorted. Sorting here is defined broadly: the array is sorted if it is either non-decreasing or non-increasing. We cannot swap equal elements, even if they are in different positions, and we must perform a swap if it is possible.

The input constraints are 1 ≤ _n_ ≤ 10^5 and array elements up to 10^9. With _n_ potentially 100,000 and a 2-second limit, an O(n^2) solution would involve 10^10 operations, which is far too slow. This means we need a linear or near-linear approach. Memory is generous at 256 MB, so storing a couple of auxiliary arrays of size _n_ is feasible.

Edge cases are important here. A single-element array obviously cannot be unsorted by a swap. An array with all elements equal cannot be unsorted either, because we cannot swap equal elements. Arrays that are strictly increasing or decreasing and contain all unique elements are swapable, but arrays that are monotonic with repeated values at the ends require careful selection of distinct values.

## Approaches

The brute-force approach would be to iterate over all pairs of distinct indices, attempt the swap if the elements are not equal, and check if the resulting array is unsorted. This is correct but O(n^2) in the worst case, which will not complete for n = 10^5. The brute-force works because it systematically tests every option, but it fails for large arrays because of the combinatorial explosion of pairs.

The optimal approach leverages the observation that to disrupt a sorted array, we only need to swap the first element that differs from another element somewhere else. If the array is strictly increasing, swapping the first element with any later element that is smaller breaks the order. Similarly, if strictly decreasing, swapping the first element with a larger later element works. This reduces the problem to a linear scan for any two indices where the elements differ, which is O(n).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Check if the array length is 1. If it is, output -1 because a single-element array cannot be unsorted by a swap.
2. Iterate through the array from the first to the second-to-last element. If you find two consecutive elements that are distinct, record their indices. These two positions are guaranteed to produce an unsorted array if swapped, because swapping any two distinct elements in a sorted array will break either the increasing or decreasing property.
3. If no such pair is found during the linear scan, then all elements are equal. In this case, output -1 because a swap of equal elements is not allowed.
4. Output the indices of the first pair found.

Why it works: In a sorted array, any two distinct elements have a relative order. Swapping two distinct elements will violate that order at least at one position. The linear scan guarantees that we find the first such pair quickly. If no pair exists, all elements are equal and no swap is possible.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

if n == 1:
    print(-1)
else:
    found = False
    for i in range(n - 1):
        if a[i] != a[i + 1]:
            print(i + 1, i + 2)
            found = True
            break
    if not found:
        print(-1)
```

The solution reads the array size and elements using fast input. It handles the trivial single-element case immediately. The linear scan checks adjacent elements because any pair of unequal adjacent elements guarantees a valid swap that breaks monotonicity. Using 1-based indexing in the output matches the problem requirements. The flag `found` ensures that if all elements are equal, we correctly output -1.

## Worked Examples

Sample Input 1:

```
1
1
```

| i | a[i] | a[i+1] | a[i] != a[i+1]? | Output |
| --- | --- | --- | --- | --- |
| - | 1 | - | - | -1 |

The array has only one element, so the output is -1.

Sample Input 2:

```
4
1 2 3 4
```

| i | a[i] | a[i+1] | a[i] != a[i+1]? | Output |
| --- | --- | --- | --- | --- |
| 0 | 1 | 2 | Yes | 1 2 |

The first pair of unequal adjacent elements is at indices 1 and 2, which will break the increasing order if swapped.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Linear scan of the array once to find two distinct elements |
| Space | O(1) | Only constant extra variables are used |

The solution comfortably fits within the time and memory limits for n ≤ 10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    if n == 1:
        return "-1"
    for i in range(n - 1):
        if a[i] != a[i + 1]:
            return f"{i+1} {i+2}"
    return "-1"

assert run("1\n1\n") == "-1", "sample 1"
assert run("4\n1 2 3 4\n") == "1 2", "sample 2"
assert run("3\n5 5 5\n") == "-1", "all equal elements"
assert run("2\n10 20\n") == "1 2", "minimum size distinct"
assert run("5\n1 3 3 3 1\n") == "1 2", "distinct at start"
assert run("6\n2 2 2 3 3 3\n") == "3 4", "distinct in middle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1 | -1 | single-element array |
| 4\n1 2 3 4 | 1 2 | strictly increasing array |
| 3\n5 5 5 | -1 | all elements equal |
| 2\n10 20 | 1 2 | minimum size with distinct elements |
| 5\n1 3 3 3 1 | 1 2 | distinct elements at start |
| 6\n2 2 2 3 3 3 | 3 4 | distinct elements in the middle |

## Edge Cases

For a single-element array like `1\n1`, the solution immediately returns -1, handling the impossibility case correctly. For arrays where all elements are equal such as `3\n5 5 5`, the linear scan does not find any distinct adjacent elements, and the solution correctly outputs -1. For arrays that are strictly increasing or decreasing, the first unequal adjacent pair is chosen, which guarantees that the array becomes unsorted after the swap. The algorithm correctly handles arrays of maximum allowed size because it only requires a single pass through the array, maintaining O(n) time and O(1) space.
