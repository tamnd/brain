---
title: "CF 1401C - Mere Array"
description: "We are given an array of positive integers. The allowed operation is a swap between two elements if the greatest common divisor (GCD) of those two elements equals the minimum element of the array."
date: "2026-06-11T08:48:38+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math", "number-theory", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1401
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 665 (Div. 2)"
rating: 1300
weight: 1401
solve_time_s: 554
verified: true
draft: false
---

[CF 1401C - Mere Array](https://codeforces.com/problemset/problem/1401/C)

**Rating:** 1300  
**Tags:** constructive algorithms, math, number theory, sortings  
**Solve time:** 9m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of positive integers. The allowed operation is a swap between two elements if the greatest common divisor (GCD) of those two elements equals the minimum element of the array. The goal is to determine whether we can rearrange the array into a non-decreasing order using these swaps.

The input consists of multiple test cases. Each test case has a length `n` and an array of `n` integers. The output for each test case is either "YES" if the array can be sorted into non-decreasing order under the rules, or "NO" otherwise.

The key constraint is that the total sum of `n` over all test cases is at most 100,000. This rules out any solution that attempts to simulate swaps explicitly because that could require up to O(n^2) operations per test case, which is far too slow.

A subtle edge case arises when the array is already non-decreasing or contains multiple copies of the minimum element. For instance, if the array is `[2, 2, 3]`, it is already sorted. If the array is `[3, 6, 2, 9]`, then only elements divisible by the minimum (2) can be swapped. Naively attempting to sort without considering the divisibility restriction would produce an incorrect "YES" or "NO".

Another tricky case is when an element is smaller than the minimum but appears later. Consider `[4, 6, 2, 5]`. The 5 cannot swap with any element that would help it reach its sorted position because `gcd(5, any other number)` is never 2, so the answer must be "NO".

## Approaches

The brute-force approach is to try all possible valid swaps, but this is infeasible because there can be up to 10^5 elements and the number of swaps could be O(n^2). It would also be very hard to ensure termination because swaps can propagate.

The key insight is that the minimum element defines a “swapable group.” Any element that is divisible by the minimum can be freely swapped with each other through a series of allowed swaps. Therefore, the only restriction occurs for elements that are not divisible by the minimum. These elements must already be in the correct relative order in the array compared to other elements not divisible by the minimum.

Using this observation, the optimal approach is:

1. Compute the sorted version of the array.
2. Iterate through the array, and for any element that is not divisible by the minimum, check if it is already in its sorted position. If not, it cannot be moved into place and the answer is "NO".
3. If all elements either are divisible by the minimum or are already in their sorted position, the array can be sorted using swaps involving the minimum.

This reduces the problem to a simple scan and GCD/divisibility checks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n^2) | O(n) | Too slow |
| Sorting + Divisibility Check | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read `n` and the array `a`.
2. Compute the minimum element `mn` in `a`.
3. Construct a sorted copy of `a`, call it `sorted_a`.
4. Iterate through the indices of `a`.

1. If `a[i]` equals `sorted_a[i]`, continue.
2. If `a[i]` is divisible by `mn`, it can be moved freely, continue.
3. Otherwise, `a[i]` is not divisible by `mn` and not in place. Return "NO" for this test case.
5. If the loop completes without returning "NO", return "YES".

Why it works: the invariant is that any element divisible by the minimum can be swapped arbitrarily through a chain of swaps involving the minimum. Elements not divisible by the minimum must already be in the correct sorted position because there is no valid swap that moves them. This guarantees correctness because any needed rearrangement only involves swapable elements, and all restrictions are explicitly checked.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_sort(a):
    mn = min(a)
    sorted_a = sorted(a)
    for original, target in zip(a, sorted_a):
        if original != target and original % mn != 0:
            return "NO"
    return "YES"

def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        print(can_sort(a))

if __name__ == "__main__":
    main()
```

The solution first computes the minimum. The sorted version serves as the target configuration. The loop ensures that any element not in the correct place must be divisible by the minimum; otherwise, sorting is impossible. Using `zip` allows a clean pairwise comparison. This uses O(n log n) per test case because of sorting, which is efficient given the constraints.

## Worked Examples

### Sample Input 2

```
6
4 3 6 6 2 9
```

| Index | a[i] | sorted_a[i] | a[i] % mn == 0? | Action |
| --- | --- | --- | --- | --- |
| 0 | 4 | 2 | 4 % 2 == 0 | ok |
| 1 | 3 | 3 | - | already correct |
| 2 | 6 | 4 | 6 % 2 == 0 | ok |
| 3 | 6 | 6 | - | already correct |
| 4 | 2 | 6 | 2 % 2 == 0 | ok |
| 5 | 9 | 9 | - | already correct |

All elements can be moved correctly via swaps involving 2. Output: YES.

### Sample Input 4

```
7 5 2 2 4
```

| Index | a[i] | sorted_a[i] | a[i] % mn == 0? | Action |
| --- | --- | --- | --- | --- |
| 0 | 7 | 2 | 7 % 2 != 0 | NO |

Output is NO because 7 is not divisible by the minimum (2) and is not in its target position.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) per test case | Sorting dominates; iterating over array is O(n) |
| Space | O(n) | Store sorted array |

Given the sum of `n` over all test cases is ≤ 10^5, total complexity fits comfortably in 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    main()
    return output.getvalue().strip()

# provided samples
assert run("4\n1
```
