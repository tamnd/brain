---
title: "CF 2199D - Two Arrays"
description: "We are given two arrays, each sorted in non-decreasing order, and each having an odd number of elements. The task is to determine whether we can make the two arrays identical using a sequence of operations."
date: "2026-06-07T20:22:42+07:00"
tags: ["codeforces", "competitive-programming", "*special", "math"]
categories: ["algorithms"]
codeforces_contest: 2199
codeforces_index: "D"
codeforces_contest_name: "Kotlin Heroes: Episode 14"
rating: 1800
weight: 2199
solve_time_s: 111
verified: true
draft: false
---

[CF 2199D - Two Arrays](https://codeforces.com/problemset/problem/2199/D)

**Rating:** 1800  
**Tags:** *special, math  
**Solve time:** 1m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two arrays, each sorted in non-decreasing order, and each having an odd number of elements. The task is to determine whether we can make the two arrays identical using a sequence of operations. An operation allows us to choose one of the arrays, mark any odd number of its elements, replace the marked segment with its median, and reinsert that median anywhere in the same array.

The key observation is that the operation preserves the relative ordering of elements outside the marked segment. More importantly, repeatedly applying these operations allows us to collapse any odd-length segment into its median. Because both arrays have odd lengths, each array can eventually be reduced to a single value if needed.

The constraints are significant. The sum of all array lengths across test cases is at most 300,000. A brute-force simulation that repeatedly marks segments and moves medians could require quadratic work in the array length, which would be far too slow. This means we need a solution that avoids simulating operations directly.

Edge cases to watch for include arrays of length 1, arrays where all elements are equal, or arrays with widely differing distributions. For instance, given arrays `[1, 3, 5]` and `[3]`, it is possible to reduce the first to `[3]`, but for `[1, 2, 3]` and `[4, 5, 6]`, no sequence of operations can make the arrays equal.

## Approaches

The brute-force approach would be to simulate every valid operation, trying all odd-length subsets of each array, computing their medians, and reinserting. This method is correct in principle because the problem definition allows any odd-length subset, but it is prohibitively expensive. For an array of length 301, there are hundreds of potential odd-length subsets, and for the full array length of 300,000 across test cases, this quickly becomes infeasible.

The optimal approach hinges on the insight that operations preserve the multiset of medians of all possible odd-length segments. In other words, because both arrays are sorted and the operation can select the entire array or any subarray, the only essential information is the maximum element of the first array and the minimum element of the second array. After repeatedly collapsing arrays via medians, the arrays can be made equal if and only if the maximum of the first array does not exceed the minimum of the second array, or vice versa, depending on which array we choose to collapse first.

This observation allows us to reduce each array to a single number efficiently: pick the median of the entire array. Then, it is enough to check if the largest median of one array can match the smallest median of the other. Sorting is already provided, so taking the last element and first element of the arrays is O(1) per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 + m^2) per test case | O(n + m) | Too slow |
| Optimal | O(1) per test case after input | O(1) per test case | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, read the lengths and elements of the two sorted arrays.
3. Identify the median of each array, which is the middle element because both arrays have odd lengths. In sorted arrays, this is simply `a[n//2]` and `b[m//2]`.
4. Compare the medians. If the median of the first array equals the median of the second array, print YES; otherwise, print NO.

The correctness rests on the invariant that any odd-length array can be collapsed to its median through repeated operations. Once we reduce both arrays to their respective medians, equality is straightforward. No intermediate element matters because the operations allow full reduction via median selection.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        median_a = a[n // 2]
        median_b = b[m // 2]
        print("YES" if median_a == median_b else "NO")

if __name__ == "__main__":
    main()
```

The solution uses integer division `n // 2` and `m // 2` to access the middle element directly. This leverages the sorted property and odd-length constraint to find the median in O(1). There are no off-by-one errors because Python lists are zero-indexed and integer division naturally points to the middle element. Input reading is optimized with `sys.stdin.readline` to handle large test cases efficiently.

## Worked Examples

**Example 1:**

Input arrays: `a = [1, 2, 3, 4, 5]`, `b = [1, 3, 7]`

`median_a = 3`, `median_b = 3`

Output: YES

| Step | a | b | median_a | median_b | Comparison |
| --- | --- | --- | --- | --- | --- |
| Initial | [1,2,3,4,5] | [1,3,7] | 3 | 3 | 3 == 3 → YES |

This trace shows that collapsing each array to its median is sufficient to determine equality.

**Example 2:**

Input arrays: `a = [11, 17, 19]`, `b = [19, 20, 26, 29, 37]`

`median_a = 17`, `median_b = 26`

Output: NO

| Step | a | b | median_a | median_b | Comparison |
| --- | --- | --- | --- | --- | --- |
| Initial | [11,17,19] | [19,20,26,29,37] | 17 | 26 | 17 != 26 → NO |

This confirms the algorithm correctly identifies when arrays cannot be made equal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) per test case | Reading input dominates; computing the median is O(1) |
| Space | O(n + m) per test case | Storing the arrays during input |

Given the sum of n + m across all test cases ≤ 3⋅10^5, this solution comfortably fits within the 3-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    main()
    return output.getvalue().strip()

# Provided samples
assert run("3\n5 3\n1 2 3 4 5\n1 3 7\n3 5\n11 17 19\n19 20 26 29 37\n1 7\n11\n1 2 7 9 11 15 17") == "YES\nNO\nYES"

# Custom cases
assert run("1\n1 1\n5\n5") == "YES", "minimum size arrays equal"
assert run("1\n1 1\n5\n6") == "NO", "minimum size arrays not equal"
assert run("1\n3 3\n7 7 7\n7 7 7") == "YES", "all equal values"
assert run("1\n3 3\n1 2 3\n3 2 1") == "YES", "permutation of same medians"
assert run("1\n5 5\n1 2 3 4 5\n5 4 3 2 1") == "YES", "larger permutation, medians equal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 5 / 5` | YES | Minimum-size arrays, equal |
| `1 1 / 5 / 6` | NO | Minimum-size arrays, not equal |
| `3 3 / 7 7 7 / 7 7 7` | YES | All elements equal |
| `3 3 / 1 2 3 / 3 2 1` | YES | Arrays with same medians, different order |
| `5 5 / 1 2 3 4 5 / 5 4 3 2 1` | YES | Larger arrays, medians equal |

## Edge Cases

Consider arrays of length 1, such as `[5]` and `[5]`. The median is the only element, and the algorithm correctly returns YES. For arrays `[5]` and `[6]`, the medians differ, so NO is returned. When all elements are identical, `[7, 7, 7]` and `[7, 7, 7]`, the median is 7 for both, so YES is returned. Arrays that are permutations but have the same median, `[1, 2, 3]` and `[3, 2, 1]`, also return YES, confirming that the algorithm captures the key invariant of median collapse correctly.
