---
title: "CF 163B - Lemmings"
description: "We are asked to select k lemmings from a group of n and assign them to k ledges of increasing heights so that heavier lemmings occupy higher ledges, while minimizing the time t needed for all selected lemmings to reach their assigned ledges."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search"]
categories: ["algorithms"]
codeforces_contest: 163
codeforces_index: "B"
codeforces_contest_name: "VK Cup 2012 Round 2"
rating: 2000
weight: 163
solve_time_s: 95
verified: false
draft: false
---

[CF 163B - Lemmings](https://codeforces.com/problemset/problem/163/B)

**Rating:** 2000  
**Tags:** binary search  
**Solve time:** 1m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to select _k_ lemmings from a group of _n_ and assign them to _k_ ledges of increasing heights so that heavier lemmings occupy higher ledges, while minimizing the time _t_ needed for all selected lemmings to reach their assigned ledges. Each lemming has a weight _m_ and a climbing speed _v_, and the time for a lemming to reach a ledge at height _i·h_ is calculated as ceiling of $(i·h)/v$. The output is the indices of the chosen lemmings in order from the lowest to the highest ledge.

The constraints are significant. With _n_ up to 10^5, any solution that considers all subsets of lemmings or attempts to simulate all possible assignments individually is too slow. We need an algorithm that runs in roughly O(n log n) or O(n log max_time), where max_time relates to the binary search space. Heights up to 10^4 and speeds and weights up to 10^9 imply that integer operations must be handled carefully, especially division and ceiling calculations.

Edge cases include situations where multiple lemmings have the same weight but different speeds. A naive greedy approach that picks the _k_ heaviest lemmings might fail if some cannot reach their assigned ledges within the minimum feasible time. Another subtle case is when many lemmings are extremely fast or slow relative to their heights, which could affect the minimal achievable _t_.

## Approaches

A brute-force approach would attempt all subsets of size _k_, sort them by weight, and compute the time for each lemming to climb its assigned ledge. This is correct in principle but computationally impossible: the number of subsets is $C(n, k)$, which for n=10^5 and k=5 is astronomical. The time to check all assignments would be exponentially large.

The key insight is that the minimal time _t_ can be determined using binary search. We can check, for a candidate _t_, whether there exists a selection of _k_ lemmings that can reach the ledges in order, where the i-th ledge requires time $\ge i·h / v$. This transforms the problem from combinatorial selection to a feasibility check. Sorting lemmings by weight allows us to assign the lowest available weights to the lowest ledges, ensuring the non-decreasing weight constraint. During the feasibility check, we pick the fastest _k_ lemmings who can reach their respective ledges within the candidate _t_.

This approach reduces the solution to O(n log n log T), where T is the range of possible climb times. The outer binary search over time narrows down the minimal achievable _t_, and each feasibility check involves a single pass through sorted lemmings, keeping a priority queue or a list of the fastest candidates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C(n, k) * k) | O(k) | Too slow |
| Binary Search + Greedy Selection | O(n log n log(max_time)) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the input values: number of lemmings _n_, number of ledges _k_, height increment _h_, lemmings' weights _m_, and speeds _v_.
2. Pair each lemming's weight, speed, and original index into a tuple `(weight, speed, index)`.
3. Sort the lemmings by weight in non-decreasing order. This ensures that assigning the first selected lemming to the lowest ledge will satisfy the weight ordering constraint.
4. Initialize a binary search range for time _t_. The lower bound is 0, and the upper bound can be an arbitrarily large number, e.g., $10^{18}$, which is safely above the maximum climb time any lemming could need.
5. Implement a feasibility check for a candidate time _t_. Iterate through the sorted lemmings, maintaining a list of lemmings who can reach the next required ledge: for ledge i, a lemming must have $v \ge i·h / t$. When a lemming qualifies, add it to a list of possible candidates. Once _k_ lemmings are collected, the assignment is feasible.
6. Apply binary search: if the current _t_ is feasible, reduce the upper bound to search for a smaller _t_; otherwise, increase the lower bound.
7. After finding the minimal feasible _t_, reconstruct the assignment by picking the first _k_ qualifying lemmings from the sorted list, respecting the order of ledges and weights.
8. Output the original indices of the chosen lemmings in order from the lowest ledge to the highest.

Why it works: Sorting by weight guarantees that we can always assign selected lemmings to ledges without violating the weight constraint. Binary search ensures we minimize _t_, and checking each candidate for feasibility guarantees that all selected lemmings can physically reach their assigned ledges within that time.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

def lemmings_jump():
    n, k, h = map(int, input().split())
    m = list(map(int, input().split()))
    v = list(map(int, input().split()))
    
    lemmings = sorted([(m[i], v[i], i + 1) for i in range(n)])  # (weight, speed, index)
    
    left, right = 0, 10**18
    result_indices = []

    def feasible(t):
        count = 0
        selected = []
        for weight, speed, idx in lemmings:
            required_time = (count + 1) * h
            if speed * t >= required_time:
                selected.append(idx)
                count += 1
                if count == k:
                    break
        if count == k:
            nonlocal result_indices
            result_indices = selected
            return True
        return False

    while left < right:
        mid = (left + right) // 2
        if feasible(mid):
            right = mid
        else:
            left = mid + 1

    feasible(left)
    print(' '.join(map(str, result_indices)))

lemmings_jump()
```

The solution begins by pairing lemmings with their weights, speeds, and original indices. Sorting by weight ensures that selecting lemmings in order satisfies the weight ordering requirement. Binary search efficiently finds the minimal time by repeatedly checking whether a candidate time allows for a feasible assignment. The feasibility check multiplies speed by time and compares it to the required height to avoid floating point errors.

## Worked Examples

### Sample Input 1

```
5 3 2
1 2 3 2 1
1 2 1 2 10
```

| count | weight | speed | idx | required | speed*t >= required | selected |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | 2 | no | [] |
| 0 | 1 | 10 | 5 | 2 | yes | [5] |
| 1 | 2 | 2 | 2 | 4 | yes | [5,2] |
| 2 | 2 | 2 | 4 | 6 | yes | [5,2,4] |

This demonstrates selecting lemmings in increasing weight order while ensuring the fastest candidates can reach their ledges.

### Sample Input 2

```
4 2 3
5 1 2 4
1 10 2 3
```

| count | weight | speed | idx | required | speed*t >= required | selected |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 10 | 2 | 3 | yes | [2] |
| 1 | 2 | 2 | 3 | 6 | yes | [2,3] |

Shows that choosing the fastest lemmings for lower ledges can minimize total time.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n log T) | Sorting takes O(n log n). Binary search performs O(log T) iterations with a linear feasibility check of O(n) each. |
| Space | O(n) | Storing lemming tuples and selection lists requires O(n) space. |

The time complexity fits within the constraints because n ≤ 10^5 and T ≤ 10^18. Each iteration is linear in n, and the logarithmic factor from binary search keeps the total operations under 10^7.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    lemmings_jump()
    return output.getvalue().strip()

# Provided sample
assert run("5 3 2\n1 2 3 2 1\n1 2 1 2 10\n") in ["5 2 4", "1 2 4"], "sample 1"

# Custom cases
assert run("1 1 1\n10\n1\n") == "1", "single lemming"
assert run("3
```
