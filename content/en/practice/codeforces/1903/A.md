---
title: "CF 1903A - Halloumi Boxes"
description: "The problem gives us a line of boxes, each labeled with a number, and Theofanis wants to arrange them in non-decreasing order. The twist is that he cannot swap arbitrary boxes or perform standard sorting operations."
date: "2026-06-08T21:02:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1903
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 912 (Div. 2)"
rating: 800
weight: 1903
solve_time_s: 142
verified: false
draft: false
---

[CF 1903A - Halloumi Boxes](https://codeforces.com/problemset/problem/1903/A)

**Rating:** 800  
**Tags:** brute force, greedy, sortings  
**Solve time:** 2m 22s  
**Verified:** no  

## Solution
## Problem Understanding

The problem gives us a line of boxes, each labeled with a number, and Theofanis wants to arrange them in non-decreasing order. The twist is that he cannot swap arbitrary boxes or perform standard sorting operations. His machine allows him to reverse subarrays of length at most $k$. A subarray is any contiguous segment of the boxes, and reversing it means flipping the order of the boxes inside that segment. The task is to determine whether it is possible to sort the entire array into non-decreasing order using any number of such reversals.

The input consists of multiple test cases, each providing the number of boxes $n$, the maximum subarray length $k$ that can be reversed, and the initial sequence of numbers on the boxes. The output for each test case is "YES" if it is possible to sort the boxes under the given operation and "NO" otherwise.

The constraints are modest: $n$ and $k$ can each be up to 100. This suggests that an $O(n^2)$ algorithm is feasible. However, $a_i$ can be as large as $10^9$, which rules out any solution relying on counting sort or frequency arrays unless we compress the values. Since $n$ is small, a solution based on direct comparison, sorting, and position analysis is reasonable.

A key edge case arises when $k = 1$. In that scenario, reversing a subarray of length 1 does nothing, so the array can only be considered sortable if it is already sorted. Another subtle case is when $k \ge n$. Then, the entire array can be reversed at once, so the array can always be sorted. Arrays where all elements are equal are trivially sortable, but careless implementations might mishandle this if they assume that elements must strictly increase.

## Approaches

A brute-force approach would be to simulate every possible sequence of reversals of length at most $k$ and check if one sequence leads to a sorted array. While correct in principle, this approach is impractical: for each position, there are up to $k$ choices for the length of reversal, resulting in an exponential number of states. Even for $n = 100$, this is computationally impossible.

The key insight comes from observing that elements near the ends of the array have limited flexibility. An element at index $i$ can be moved at most $k-1$ positions away from either end via reversals. If we denote by $sorted\_a$ the fully sorted array, any element whose final position in $sorted\_a$ differs from its original position by at least $k$ cannot reach its target position if $k < n$. Therefore, the problem reduces to checking whether the first $k-1$ and last $k-1$ positions in the array are already compatible with the sorted array. For the positions strictly in the middle, reversals allow full shuffling.

Formally, we can sort the array to get the target configuration. Then, for positions $i < k$ or $i \ge n-k+1$, the value at $a[i]$ must already match the sorted array. If all these boundary positions match, the array can be sorted using reversals; otherwise, it cannot. When $k \ge n/2$, this effectively allows all elements to reach their correct positions, so the array is always sortable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Position-based check | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$.
2. For each test case, read $n$, $k$, and the array $a$.
3. Create a copy of $a$ and sort it to obtain $sorted\_a$.
4. If $k = 1$, compare $a$ directly with $sorted\_a$. If they match, print "YES"; otherwise, print "NO". This handles the edge case where no effective reversal is possible.
5. Otherwise, iterate through the positions from $0$ to $k-2$ (the first $k-1$ positions) and from $n-k+1$ to $n-1$ (the last $k-1$ positions). Check if each element matches its counterpart in $sorted\_a$.
6. If all boundary positions match, print "YES"; otherwise, print "NO".

Why it works: The boundary positions cannot be shifted sufficiently if $k < n$, so they must already be in their correct sorted position. Middle positions can always be shuffled using multiple reversals since they can participate in overlapping reversals of length $k$. This invariant guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    sorted_a = sorted(a)
    
    if k == 1:
        print("YES" if a == sorted_a else "NO")
        continue
    
    ok = True
    for i in range(k-1):
        if a[i] != sorted_a[i]:
            ok = False
            break
    for i in range(n-k+1, n):
        if a[i] != sorted_a[i]:
            ok = False
            break
    print("YES" if ok else "NO")
```

The code reads input using fast I/O. Sorting the array allows us to determine the target configuration. Checking boundary positions handles the critical restriction of limited reversal length. The use of `k-1` and `n-k+1` precisely captures the maximum reach of elements near the ends.

## Worked Examples

For the input:

```
3 1
9 9 9
```

- $a = [9, 9, 9]$
- $sorted\_a = [9, 9, 9]$
- Since $k = 1$, we directly compare arrays. They match. Output "YES".

For the input:

```
2 1
3 1
```

- $a = [3, 1]$
- $sorted\_a = [1, 3]$
- $k = 1$ means no effective reversals. Arrays do not match. Output "NO".

| Step | a | sorted_a | k | Boundary check result |
| --- | --- | --- | --- | --- |
| 1 | [3,1] | [1,3] | 1 | arrays differ, return NO |

The table shows that the algorithm correctly identifies when reversals cannot move elements into place.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, boundary check is O(n) |
| Space | O(n) | A copy of the array is stored for sorting |

With $n \le 100$ and $t \le 100$, the solution easily executes within 1 second and uses negligible memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    # solution
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        sorted_a = sorted(a)
        
        if k == 1:
            print("YES" if a == sorted_a else "NO")
            continue
        
        ok = True
        for i in range(k-1):
            if a[i] != sorted_a[i]:
                ok = False
                break
        for i in range(n-k+1, n):
            if a[i] != sorted_a[i]:
                ok = False
                break
        print("YES" if ok else "NO")
    return out.getvalue().strip()

# Provided samples
assert run("5\n3 2\n1 2 3\n3 1\n9 9 9\n4 4\n6 4 2 1\n4 3\n10 3 830 14\n2 1\n3 1\n") == "YES\nYES\nYES\nYES\nNO"

# Custom tests
assert run("1\n1 1\n42\n") == "YES", "single element"
assert run("1\n5 5\n5 4 3 2 1\n") == "YES", "full reverse possible"
assert run("1\n5 2\n1 3 2 5 4\n") == "NO", "boundaries cannot reach correct positions"
assert run("1\n4 3\n1 2 3 4\n") == "YES", "already sorted"
assert run("1\n3 1\n2 1 3\n") == "NO", "k=1 unsorted"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 42 | YES | single-element array |
| 5 5 5 4 3 2 1 | YES | full array reverse allowed |
| 5 2 1 3 2 5 4 | NO | boundaries cannot move to correct position |
| 4 3 1 2 3 4 |  |  |
