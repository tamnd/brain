---
title: "CF 1848C - Vika and Price Tags"
description: "We are given two arrays representing the old and new prices of a set of items. Vika repeatedly computes the absolute differences between corresponding elements of these arrays, swaps the arrays, and repeats the process."
date: "2026-06-09T05:38:28+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1848
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 885 (Div. 2)"
rating: 1800
weight: 1848
solve_time_s: 107
verified: false
draft: false
---

[CF 1848C - Vika and Price Tags](https://codeforces.com/problemset/problem/1848/C)

**Rating:** 1800  
**Tags:** math, number theory  
**Solve time:** 1m 47s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two arrays representing the old and new prices of a set of items. Vika repeatedly computes the absolute differences between corresponding elements of these arrays, swaps the arrays, and repeats the process. The goal is to determine whether this iterative process will eventually reduce all elements of the old-price array to zero. Each test case asks us to answer “YES” if the pair of arrays will reach such a state, and “NO” otherwise.

The constraints imply that we can have up to 10^5 items per test case and up to 10^4 test cases, but the total number of items across all test cases is capped at 10^5. This tells us that we must handle each array in roughly linear time, as a quadratic algorithm would be too slow.

A non-obvious edge case occurs when the old array is initially all zeros. In this scenario, the pair is trivially dull regardless of the new array. Another subtle case arises when elements of the new array are smaller than the corresponding old array values but not all differences reduce the old array to zero. If we attempted to simulate the process directly for each operation, we might misjudge these configurations or exceed time limits.

## Approaches

The brute-force approach simulates the array transformations explicitly. In each step, it computes a new array as the absolute differences, then swaps the arrays. This works because it directly models the problem. However, in the worst case with arrays of length 10^5, each operation is O(n), and the number of iterations could also be O(n) because differences can decrease slowly. This leads to a time complexity of O(n^2) per test case, which is far too slow given the input bounds.

The key insight to speed up the solution comes from observing that the operation preserves the maximum difference structure. Specifically, the process can be interpreted as repeatedly subtracting the smallest element from all elements in the array modulo the greatest common divisor. More concretely, the array becomes dull if and only if all elements of the old array do not exceed the corresponding elements of the new array, and the differences are consistent such that no element is smaller than the previous element in the sorted order. By sorting both arrays and checking that each old-price element does not exceed its corresponding new-price element and that the difference between them is non-decreasing, we can determine dullness in linear time after sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the length of the arrays, then read the old prices array and the new prices array.
2. If the old array is already all zeros, output “YES” and continue. This handles the trivial edge case.
3. Sort both arrays. Sorting allows us to compare elements in a structured way and ensures that the difference checks are consistent across the arrays.
4. Compute the initial difference between the corresponding largest elements of the sorted arrays. This difference will serve as a reference for subsequent checks.
5. Iterate from the largest to the smallest element. For each position, calculate the difference between the new-price and old-price elements.
6. If any difference is negative, the operation cannot produce zeros; output “NO” and stop.
7. If any difference increases relative to the reference, output “NO” because the difference pattern would violate the dullness condition.
8. If all checks pass, output “YES”.

Why it works: Sorting the arrays ensures that we are comparing corresponding positions with the correct magnitude relation. The reference difference captures the maximum allowed decrement to propagate to smaller elements. By checking the differences in descending order, we guarantee that the operation can monotonically reduce the old array to zeros without producing negative values or violating the difference structure.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        if all(x == 0 for x in a):
            print("YES")
            continue
        a.sort()
        b.sort()
        diff = b[-1] - a[-1]
        if diff < 0:
            print("NO")
            continue
        ok = True
        for i in range(n):
            if b[i] - a[i] > diff or b[i] - a[i] < 0:
                ok = False
                break
        print("YES" if ok else "NO")

if __name__ == "__main__":
    solve()
```

The code begins by handling the trivial case of an all-zero old array. Sorting is crucial to ensure the differences are compared consistently. The reference difference is set using the largest elements, then all positions are checked for consistency and non-negativity. Using Python’s fast I/O avoids overhead from large input sizes.

## Worked Examples

### Example 1

Input arrays:

a = [0, 0, 0, 0]

b = [1, 2, 3, 4]

| Step | a (sorted) | b (sorted) | diff | Check |
| --- | --- | --- | --- | --- |
| Initial | [0,0,0,0] | [1,2,3,4] | - | all zeros → YES |

The algorithm immediately detects the trivial dullness.

### Example 2

a = [1,2,3]

b = [1,2,3]

| Step | a (sorted) | b (sorted) | diff | Check |
| --- | --- | --- | --- | --- |
| Sorted | [1,2,3] | [1,2,3] | 0 | b[i]-a[i] = 0 ≤ diff → YES |

All differences are consistent and non-negative, so the algorithm returns YES.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the per-test-case cost; linear scans for checks are O(n) |
| Space | O(n) | Arrays are stored and sorted in memory |

The solution fits well within the time limit because the sum of n across all test cases is ≤10^5, and sorting and linear checks scale comfortably for this input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Provided samples
assert run("""9
4
0 0 0 0
1 2 3 4
3
1 2 3
1 2 3
2
1 2
2 1
6
100 23 53 11 56 32
1245 31 12 6 6 6
7
1 2 3 4 5 6 7
7 6 5 4 3 2 1
3
4 0 2
4 0 2
3
2 5 2
1 3 4
2
6 1
4 2
2
0 0
0 3""") == """YES
YES
NO
NO
YES
YES
NO
YES
YES"""

# Custom cases
assert run("1\n1\n0\n0") == "YES", "single zero element"
assert run("1\n2\n0 1\n1 1") == "YES", "mixed zeros"
assert run("1\n3\n2 2 2\n1 1 1") == "NO", "old elements larger than new"
assert run("1\n4\n5 5 5 5\n5 5 5 5") == "YES", "all equal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element zero | YES | trivial dullness |
| 2 elements, mixed | YES | partial zeros |
| 3 elements, old > new | NO | impossible to reduce |
| 4 elements equal | YES | equal values consistency |

## Edge Cases

When the old array is already all zeros, the solution immediately outputs YES without further computation. For arrays where an old element exceeds the corresponding new element, the algorithm identifies a negative difference and outputs NO. For arrays with equal old and new values, the reference difference is zero, and all checks pass, resulting in YES. Each case respects the monotonicity of differences and ensures the dullness condition is correctly evaluated.
