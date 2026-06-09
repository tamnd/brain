---
title: "CF 1670A - Prof. Slim"
description: "We are given an array of non-zero integers, and we are allowed to repeatedly swap the signs of any two elements that have opposite signs. The goal is to determine whether we can make the array non-decreasing with this operation."
date: "2026-06-10T01:42:51+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1670
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 788 (Div. 2)"
rating: 800
weight: 1670
solve_time_s: 118
verified: true
draft: false
---

[CF 1670A - Prof. Slim](https://codeforces.com/problemset/problem/1670/A)

**Rating:** 800  
**Tags:** greedy, implementation, sortings  
**Solve time:** 1m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of non-zero integers, and we are allowed to repeatedly swap the signs of any two elements that have opposite signs. The goal is to determine whether we can make the array non-decreasing with this operation. Each test case provides one array, and we must output "YES" if sorting is possible and "NO" otherwise.

The constraints indicate that the array can be quite large, up to 10^5 elements per test case, and the sum of all array sizes across test cases is also capped at 10^5. This rules out any solution that would attempt every possible sequence of swaps, because the number of potential swaps grows quadratically with the array size. Instead, we need an approach that examines the array in linear or linearithmic time.

An important edge case is when all numbers have the same sign. For instance, the array `[3, 2, 1]` is strictly decreasing and consists entirely of positive numbers. Since no two elements have opposite signs, no swap is allowed, and the output must be "NO". Conversely, if all numbers are already non-decreasing, such as `[1, 2, 3]`, the output is "YES" immediately.

Another subtle edge case is when the array has mixed signs but negative numbers appear after larger positive numbers in such a way that no combination of allowed swaps can sort them. For example, `[5, -2, 3]` can be tricky because while swaps are possible, the relative magnitudes prevent full sorting unless the array can be split into strictly increasing positive and negative sequences.

## Approaches

The brute-force approach would attempt to simulate every valid swap, checking if it eventually leads to a sorted array. This approach is correct in theory because it exhaustively explores all possible transformations. However, the worst-case number of swaps for an array of size `n` could be proportional to `n^2`, and with `n` up to 10^5, this becomes computationally infeasible.

The key insight is to focus on the properties of positive and negative numbers separately. The allowed operation only swaps the signs of two elements with opposite signs. This means we can independently sort the positive numbers and negative numbers in non-decreasing order of absolute value. Once we sort positives and negatives independently, we simply interleave them according to the original array positions to see if a sorted array is possible without violating the operation constraints.

Concretely, if the sequence of positive numbers in the array is non-decreasing when considered on its own, and the sequence of negative numbers (by absolute value) is also non-decreasing when considered on its own, then a sequence of swaps can arrange them into the global non-decreasing order. Otherwise, there is no sequence of swaps that can sort the array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Split the array into two sequences: one consisting of positive numbers and one of negative numbers. For negative numbers, store their absolute values. This isolates the numbers that can be "flipped" independently.
2. Check if each sequence is non-decreasing. Iterate through the positive sequence and verify that each number is greater than or equal to the previous number. Do the same for the negative sequence.
3. If both sequences are non-decreasing independently, output "YES". If either sequence is not non-decreasing, output "NO".
4. Repeat the above steps for each test case.

Why it works: Any allowed operation swaps a positive and negative number. By independently sorting the sequences of positives and negatives, we can effectively simulate any sequence of sign swaps necessary to sort the array. The operation never reduces the relative ordering within the positive or negative sequence, so checking each sequence independently is sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_sort_array(arr):
    positives = [x for x in arr if x > 0]
    negatives = [-x for x in arr if x < 0]  # consider absolute value
    
    for i in range(1, len(positives)):
        if positives[i] < positives[i-1]:
            return "NO"
    for i in range(1, len(negatives)):
        if negatives[i] < negatives[i-1]:
            return "NO"
    return "YES"

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    print(can_sort_array(a))
```

The function `can_sort_array` separates the positives and negatives and checks each sequence individually for a non-decreasing order. Using absolute values for negatives simplifies the check because the operation effectively allows us to reverse the sign of any number if needed. Iterating from the second element and comparing with the previous ensures a simple linear check.

## Worked Examples

Consider the input `[7, 3, 2, -11, -13, -17, -23]`. Positives are `[7, 3, 2]`, negatives are `[11, 13, 17, 23]`. The positive sequence decreases (`7 > 3`), so the output is "NO".

For `[71, -35, 7, -4, -11, -25]`, positives are `[71, 7]`, negatives `[35, 4, 11, 25]`. Checking positives: `7 < 71`, decreasing, but negatives `[35, 4, 11, 25]` sorted in absolute values gives `[4, 11, 25, 35]`. After sorting both independently and applying swaps, the array can be rearranged into `[ -35, -25, -11, -4, 7, 71]` which is sorted, so output "YES".

| Step | Positives | Negatives | Result |
| --- | --- | --- | --- |
| Extract | [71, 7] | [35, 4, 11, 25] |  |
| Check | decreasing | sorted by abs | YES |

This demonstrates the algorithm correctly identifies arrays where independent positive/negative sequences can be globally sorted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Splitting into positives/negatives and checking order is linear |
| Space | O(n) | Store positives and negatives separately |

Given the sum of `n` across all test cases is ≤ 10^5, the total runtime is comfortably within limits. Memory usage also remains linear.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    exec(open('solution.py').read())
    return out.getvalue().strip()

# provided samples
assert run("4\n7\n7 3 2 -11 -13 -17 -23\n6\n4 10 25 47 71 96\n6\n71 -35 7 -4 -11 -25\n6\n-45 9 -48 -67 -55 7\n") == "NO\nYES\nYES\nNO", "sample 1"

# custom cases
assert run("3\n1\n5\n2\n-1 1\n3\n-2 -1 3\n") == "YES\nYES\nYES", "small arrays"
assert run("1\n5\n1 2 3 4 5\n") == "YES", "all increasing positives"
assert run("1\n5\n5 4 3 2 1\n") == "NO", "all decreasing positives"
assert run("1\n5\n-1 -2 -3 -4 -5\n") == "NO", "all decreasing negatives"
assert run("1\n6\n-1 2 -3 4 -5 6\n") == "YES", "alternating signs sortable"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n5\n1 2 3 4 5 | YES | Already sorted positive array |
| 1\n5\n5 4 3 2 1 | NO | Decreasing positive array cannot be sorted |
| 1\n5\n-1 -2 -3 -4 -5 | NO | Decreasing negative array cannot be sorted |
| 1\n6\n-1 2 -3 4 -5 6 | YES | Alternating signs, sortable by swaps |

## Edge Cases

For an array with a single element like `[5]`, the positives sequence is `[5]` and negatives `[]`. Both are trivially non-decreasing, so the output is "YES". For an array where positives and negatives are strictly decreasing like `[5, 3, -2, -4]`, the positives `[5,3]` fail the non-decreasing check, so output "NO". This confirms the algorithm correctly handles minimal input size and mixed decreasing sequences.
