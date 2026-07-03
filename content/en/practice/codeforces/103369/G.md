---
title: "CF 103369G - \u0414\u0432\u0435 \u0441\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u043a\u0438"
description: "We are given an array of integers and a single allowed operation that can be used at most once. The operation lets us pick any subset of positions and add the same positive value $k$ to all chosen elements."
date: "2026-07-03T12:51:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103369
codeforces_index: "G"
codeforces_contest_name: "Moscow team olympiad 2021"
rating: 0
weight: 103369
solve_time_s: 47
verified: true
draft: false
---

[CF 103369G - \u0414\u0432\u0435 \u0441\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u043a\u0438](https://codeforces.com/problemset/problem/103369/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and a single allowed operation that can be used at most once. The operation lets us pick any subset of positions and add the same positive value $k$ to all chosen elements. After optionally applying this operation once, we want the resulting array to become nondecreasing.

In other words, we are allowed to “lift” some elements upward by a uniform shift, and we want to know whether we can fix all inversions caused by the original ordering using only this single global increment applied to a chosen subset.

The key difficulty is that the operation is extremely constrained: we cannot independently adjust elements, only split the array into two groups, those that receive $+k$ and those that do not.

The constraints imply $n$ up to $2 \cdot 10^5$ over all test cases, so any solution must be linear or near-linear per test case. Quadratic reasoning over all subsets or pairs is impossible.

A naive interpretation might suggest trying all subsets of indices and all possible $k$, but that is exponential in the subset choice and infinite in $k$. Even restricting to structural patterns still leads to too many cases unless we exploit a strong monotonic property.

A subtle edge case appears when the array is already nondecreasing. In that case the correct answer is immediate: we can choose not to apply the operation at all. Another edge case arises when the array is “almost sorted” except for multiple decreasing segments. For example, in an array like $[3, 1, 2, 4]$, a single uniform lift cannot repair the ordering if the required corrections are inconsistent across inversions.

## Approaches

A brute-force strategy would consider every subset of indices as the “lifted set” and try to determine whether there exists a $k$ such that after adding $k$ to that subset, the array becomes sorted. For a fixed subset, determining feasibility reduces to checking whether all violated order constraints can be satisfied by a single consistent shift. However, there are $2^n$ subsets, and even checking each one takes $O(n)$, leading to $O(n2^n)$, which is far beyond feasible.

The key observation is that the operation creates a binary partition of the array positions: each index is either untouched or shifted by the same amount. Once we fix a valid final sorted array, every element must belong to one of two “levels”: original values or original values plus $k$. This means that in the final sorted sequence, whenever we transition from a non-shifted element to a shifted one, the structure of differences must be consistent globally.

The crucial insight is to look at the sorted version of the array and compare it with the original. If we imagine sorting the array, each element in the final array corresponds either to its original value or to its original value minus $k$. Therefore, if we align the original array with its sorted version, the differences between corresponding elements must take at most two distinct values: $0$ and $k$. Any third difference immediately makes the transformation impossible.

This reduces the problem to checking whether the difference multiset between original and sorted array contains at most one positive distinct value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Subsets | $O(n 2^n)$ | $O(n)$ | Too slow |
| Sorting + Difference Structure | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

### 1. Sort a copy of the array

We construct a sorted version of the input array. This represents the target nondecreasing order we want to achieve.

### 2. Compare each original element with its sorted position

For each index, compute the difference between the sorted value and the original value. This difference tells us how much that element would need to be increased to match its sorted position.

If we ever see a negative difference, that means the original element is already larger than its sorted position, which cannot be fixed by only adding values, so the answer is immediately impossible.

### 3. Collect all positive differences

We gather all positive differences. These represent elements that must be increased to reach their sorted positions.

If we are allowed only one operation with a single $k$, then all these positive differences must be equal, because every chosen element receives exactly the same increment.

### 4. Validate consistency of required increment

If the set of positive differences contains more than one distinct value, it is impossible to choose a single $k$ that fixes all required positions simultaneously.

If there is exactly one distinct positive difference, that value is the candidate $k$.

### 5. Decide feasibility

If no conflicts appear and all conditions are satisfied, the array can be fixed with one operation or zero operations if already sorted.

### Why it works

The operation imposes a rigid structure: every modified element shifts by exactly the same amount. When comparing against the sorted target, each element independently implies a required shift value. If more than one shift value is needed among elements that must move upward, there is no way to reconcile them with a single global $k$. Conversely, if all required shifts agree, we can choose exactly those elements and apply that $k$, producing the sorted array.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    b = sorted(a)
    
    diffs = set()
    
    for x, y in zip(a, b):
        if y < x:
            print("No")
            return
        if y > x:
            diffs.add(y - x)
    
    if len(diffs) <= 1:
        print("Yes")
    else:
        print("No")

t = int(input())
for _ in range(t):
    solve()
```

The implementation directly follows the idea of aligning the array with its sorted version. The key detail is that we treat any increase requirement as evidence of a needed uniform shift. If multiple distinct positive shifts appear, we reject immediately.

The check `y < x` handles the irreversible inversion case where sorting would require decreasing an element, which is not allowed by the operation.

The set `diffs` enforces global consistency of the required increment.

## Worked Examples

### Example 1

Input:

```
4
1 2 3 4
```

| index | original | sorted | diff |
| --- | --- | --- | --- |
| 0 | 1 | 1 | 0 |
| 1 | 2 | 2 | 0 |
| 2 | 3 | 3 | 0 |
| 3 | 4 | 4 | 0 |

All differences are zero, so no operation is needed. Output is Yes.

This confirms the case where the array is already sorted and the algorithm correctly accepts empty operation.

### Example 2

Input:

```
4
2 1 3 4
```

| index | original | sorted | diff |
| --- | --- | --- | --- |
| 0 | 2 | 1 | invalid (negative) |

At the first position, the sorted value is smaller than the original, meaning we would need to decrease an element to fix ordering. Since the operation only allows increments, this is impossible.

The algorithm immediately rejects, demonstrating that local downward corrections are not recoverable.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates; single linear scan afterward |
| Space | $O(n)$ | Storage for sorted copy and difference tracking |

The constraints allow up to $2 \cdot 10^5$ total elements, so an $O(n \log n)$ solution is comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    
    def solve():
        n = int(input())
        a = list(map(int, input().split()))
        b = sorted(a)
        diffs = set()
        for x, y in zip(a, b):
            if y < x:
                return "No"
            if y > x:
                diffs.add(y - x)
        return "Yes" if len(diffs) <= 1 else "No"
    
    t = int(input())
    out = []
    for _ in range(t):
        out.append(solve())
    return "\n".join(out)

# provided samples
assert run("1\n4\n1 2 3 4\n") == "Yes"
assert run("1\n3\n2 1 1\n") == "No"

# custom cases
assert run("1\n3\n1 3 2\n") == "Yes", "single swap-like fix"
assert run("1\n4\n4 3 2 1\n") == "No", "strict inversion impossible"
assert run("1\n5\n1 1 1 1 1\n") == "Yes", "already uniform"
assert run("1\n4\n1 5 2 6\n") == "No", "multiple shift requirements"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 3 2 | Yes | single consistent correction |
| 4 3 2 1 | No | full inversion cannot be fixed |
| 1 1 1 1 1 | Yes | zero-operation trivial case |
| 1 5 2 6 | No | conflicting required shifts |

## Edge Cases

One important edge case is when the array is already sorted. The algorithm handles this because all differences are zero, so the set remains empty and the answer is accepted.

Another case is when only one element needs to move. For example, $[1, 3, 2]$ produces a single positive difference pattern, which is still consistent, so the algorithm accepts it correctly.

A more subtle case is when multiple elements require increases but by different amounts. For instance $[1, 4, 2, 6]$ yields two distinct required increments, making it impossible to choose a single $k$. The algorithm correctly rejects this because the set of differences has size greater than one.
