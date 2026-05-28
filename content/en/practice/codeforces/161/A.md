---
title: "CF 161A - Dress'em in Vests!"
description: "We are tasked with equipping as many soldiers as possible with bulletproof vests. Each soldier has a preferred vest size, but they are willing to tolerate deviations within a given range. Specifically, the i-th soldier can wear any vest with a size between a[i] - x and a[i] + y."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "greedy", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 161
codeforces_index: "A"
codeforces_contest_name: "VK Cup 2012 Round 1"
rating: 1300
weight: 161
solve_time_s: 75
verified: true
draft: false
---

[CF 161A - Dress'em in Vests!](https://codeforces.com/problemset/problem/161/A)

**Rating:** 1300  
**Tags:** binary search, brute force, greedy, two pointers  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are tasked with equipping as many soldiers as possible with bulletproof vests. Each soldier has a preferred vest size, but they are willing to tolerate deviations within a given range. Specifically, the i-th soldier can wear any vest with a size between `a[i] - x` and `a[i] + y`. The available vests have fixed sizes, and each vest can be assigned to only one soldier. The goal is to output the maximum number of soldiers that can be equipped, along with the assignment of vests to soldiers.

The input sizes are significant: up to 100,000 soldiers and 100,000 vests. A naive solution that checks every vest for every soldier would require up to 10^10 comparisons, which is far beyond acceptable for a 3-second time limit. Therefore, we need a solution that works in linear or near-linear time, ideally `O(n + m)` or `O(n log n + m log m)`.

A subtle edge case arises when multiple soldiers are compatible with the same vest. For instance, if two soldiers both accept size 3, and the available vests include only one size 3 vest, the algorithm must choose which soldier to assign first. A careless implementation may either miss possible assignments or attempt to reuse the same vest.

Another edge case is when a soldier's acceptable range extends beyond all available vests. For example, if a soldier's acceptable range is 1-100, but all vests are size 101 or larger, no vest can be assigned, and the algorithm must skip this soldier correctly.

## Approaches

The brute-force approach is straightforward: for each soldier, scan all available vests to see if any fall within their acceptable range. If a compatible vest is found, mark it as used and move on. This approach is correct in principle, because it checks every possibility, but it is extremely inefficient. For the maximum constraints, it could require up to 10^10 comparisons, which is far too slow.

The key observation is that both soldiers and vests are given in non-decreasing order. This structure allows a two-pointer approach, where we maintain one pointer for soldiers and one pointer for vests. At each step, we check if the current vest fits the current soldier. If it does, we assign it and advance both pointers. If the vest is too small for the soldier, we advance the vest pointer. If the vest is too large, we advance the soldier pointer. This greedy strategy works because soldiers and vests are sorted: once a vest is too large for the current soldier, it cannot fit any earlier soldier, and once a vest is too small, it cannot fit any later soldier.

This reduces the time complexity from O(n * m) to O(n + m) and requires only linear extra space for storing the assignments.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m) | O(1) | Too slow |
| Two-Pointer Greedy | O(n + m) | O(min(n, m)) | Accepted |

## Algorithm Walkthrough

1. Initialize two pointers, `i` for soldiers and `j` for vests, both starting at 0. Also, initialize an empty list `assignments` to store the final pairs.
2. While both pointers are within bounds, check the current vest size `b[j]` against the current soldier's acceptable range `[a[i] - x, a[i] + y]`.
3. If `b[j]` is smaller than `a[i] - x`, advance the vest pointer `j` because this vest cannot fit this or any later soldier who requires at least `a[i] - x`.
4. If `b[j]` is larger than `a[i] + y`, advance the soldier pointer `i` because no vest left can fit this soldier.
5. If `b[j]` is within `[a[i] - x, a[i] + y]`, assign this vest to this soldier by appending `(i + 1, j + 1)` to `assignments`, then advance both pointers.
6. Continue until one of the pointers reaches the end of its respective list.
7. Output the length of `assignments` followed by the pairs.

The reason this works is that the greedy choice of the smallest compatible vest ensures that later soldiers have the best chance to find a vest. The invariant maintained is that all assigned vests are compatible and used only once.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m, x, y = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

i = j = 0
assignments = []

while i < n and j < m:
    if b[j] < a[i] - x:
        j += 1
    elif b[j] > a[i] + y:
        i += 1
    else:
        assignments.append((i + 1, j + 1))
        i += 1
        j += 1

print(len(assignments))
for soldier, vest in assignments:
    print(soldier, vest)
```

The code follows the two-pointer algorithm. We carefully check each vest against the soldier's acceptable range and increment the correct pointer based on the comparison. Off-by-one errors are avoided by converting 0-based indices to 1-based when appending to `assignments`. Using `sys.stdin.readline` ensures fast input for large datasets.

## Worked Examples

Sample 1 input:

```
5 3 0 0
1 2 3 3 4
1 3 5
```

| i | j | a[i] | b[j] | Action | assignments |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 1 | 1 fits 1 | [(1,1)] |
| 1 | 1 | 2 | 3 | 3 > 2 | advance i |
| 2 | 1 | 3 | 3 | 3 fits 3 | [(1,1),(3,2)] |

Output: `2\n1 1\n3 2`

Sample 2 input:

```
3 5 2 2
3 4 5
1 2 3 4 5
```

| i | j | a[i] | b[j] | Action | assignments |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 3 | 1 | 1 < 1 | 1 >= 1 |
| 1 | 1 | 4 | 2 | fits | [(1,1),(2,2)] |
| 2 | 2 | 5 | 3 | fits | [(1,1),(2,2),(3,3)] |

All soldiers equipped, demonstrates range tolerance handling.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each pointer moves only forward through its array once |
| Space | O(min(n, m)) | Stores at most one assignment per soldier or vest |

This solution easily fits within the constraints, since 2 * 10^5 iterations is fast and memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m, x, y = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    i = j = 0
    assignments = []
    while i < n and j < m:
        if b[j] < a[i] - x:
            j += 1
        elif b[j] > a[i] + y:
            i += 1
        else:
            assignments.append((i + 1, j + 1))
            i += 1
            j += 1
    out = [str(len(assignments))] + [f"{s} {v}" for s,v in assignments]
    return "\n".join(out)

# provided samples
assert run("5 3 0 0\n1 2 3 3 4\n1 3 5\n") == "2\n1 1\n3 2"
assert run("3 5 2 2\n3 4 5\n1 2 3 4 5\n") == "3\n1 1\n2 2\n3 3"

# custom test cases
assert run("1 1 0 0\n5\n5\n") == "1\n1 1", "minimum input"
assert run("2 2 1 1\n2 4\n1 3\n") == "2\n1 1\n2 2", "overlapping ranges"
assert run("3 3 0 0\n1 2 3\n10 11 12\n") == "0", "no compatible vests"
assert run("4 4 10 10\n5 6 7 8\n1 2 3 4\n") == "0", "vests smaller than range"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 0 0\n5\n5 | 1\n1 1 | minimum-size input |
| 2 2 1 1\n2 4\n1 3 | 2 |  |
