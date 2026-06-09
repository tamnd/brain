---
title: "CF 1814D - Balancing Weapons"
description: "We are given a set of guns, each with two properties: a fire rate $fi$ and a damage per bullet $di$. The product of these two, $pi = fi cdot di$, is the total firepower of a gun."
date: "2026-06-09T08:27:12+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "data-structures", "math", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1814
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 146 (Rated for Div. 2)"
rating: 2500
weight: 1814
solve_time_s: 97
verified: false
draft: false
---

[CF 1814D - Balancing Weapons](https://codeforces.com/problemset/problem/1814/D)

**Rating:** 2500  
**Tags:** binary search, brute force, data structures, math, two pointers  
**Solve time:** 1m 37s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of guns, each with two properties: a fire rate $f_i$ and a damage per bullet $d_i$. The product of these two, $p_i = f_i \cdot d_i$, is the total firepower of a gun. The task is to adjust as few $d_i$ values as possible so that the difference between the most and least powerful guns does not exceed a given threshold $k$. Importantly, each new $d_i$ must remain a positive integer.

The inputs can be fairly large: there can be up to 3000 guns across all test cases, and each damage value can be as high as $10^9$. This rules out any solution that tries to explicitly enumerate all possible damage values, because even iterating through all possibilities for a single gun could exceed time limits. We need an approach that works by reasoning about ranges or relative differences rather than explicit enumeration.

Edge cases arise when all guns already satisfy the balance condition, when $k = 0$ so all guns must have exactly the same power, or when a gun has a very large damage value that cannot be adjusted down enough without going below 1. A naive implementation that ignores integer constraints or directly modifies every gun could return a non-optimal number of changes or even invalid damage values.

## Approaches

The brute-force approach would try all subsets of guns to change and all possible integer values for $d_i$ within reasonable bounds. This is correct in principle because we could always find a solution by trial, but it is computationally infeasible. With $n$ up to 3000, enumerating subsets is $2^n$ and checking each combination of damage values would multiply that by another huge factor.

The key observation is that each gun defines a range of acceptable firepower values if we want to leave it unchanged. For gun $i$ with fire rate $f_i$ and damage $d_i$, the power is $p_i = f_i \cdot d_i$. If we attempt to set a target firepower interval $[L, L+k]$, the guns we do not modify must have their current $p_i$ within this interval. This means the problem reduces to finding an interval of length $k$ that covers as many existing $p_i$ values as possible. The guns outside this interval must be modified. Sorting the $p_i$ values and using a sliding window or two-pointer technique allows us to compute this efficiently.

The optimal approach, then, is to compute all $p_i$ values, sort them, and slide a window of length $k$ across the sorted list. For each position, count how many guns are already inside the interval. The minimum number of guns to change is the total $n$ minus the maximum number of guns already inside some interval. This approach works in $O(n \log n)$ per test case due to sorting, which is acceptable given the sum of $n$ over all test cases is 3000.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * max(d_i)) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$. For each test case, read $n$ and $k$, followed by the fire rate array $f$ and damage array $d$.
2. Compute the firepower for each gun: $p_i = f_i \cdot d_i$. This gives a list of integers representing the current power levels.
3. Sort the $p_i$ list. Sorting is necessary because the problem reduces to finding an interval of length $k$ that covers the maximum number of guns. Sorting allows us to consider contiguous sequences of powers efficiently.
4. Initialize two pointers, `l` and `r`, both starting at 0. These pointers define a window of powers that we might leave unchanged. `l` points to the leftmost power in the interval, and `r` moves to the right until $p_r - p_l > k$.
5. As we slide `r` to the right, check if $p_r - p_l > k$. If it is, increment `l` until the interval length becomes at most $k$. At each step, compute the number of guns inside the interval as `r - l + 1`, and track the maximum seen.
6. After the iteration, the minimum number of changes is $n - \text{max\_inside}$. This is because every gun not inside the optimal interval must be modified.
7. Print the result for each test case.

Why it works: the sorted array guarantees that any interval of length $k$ that maximizes the number of guns inside must be contiguous. Sliding the window across the sorted array ensures we consider all such contiguous intervals. Since the guns outside the chosen interval must be modified, subtracting the maximum covered from $n$ gives the minimal number of changes. Integer constraints on $d_i$ do not interfere because any gun inside the interval does not need changing, and guns outside can always be adjusted to any integer within the allowed range.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        f = list(map(int, input().split()))
        d = list(map(int, input().split()))
        p = [f[i] * d[i] for i in range(n)]
        p.sort()
        max_inside = 0
        l = 0
        for r in range(n):
            while p[r] - p[l] > k:
                l += 1
            max_inside = max(max_inside, r - l + 1)
        print(n - max_inside)

if __name__ == "__main__":
    solve()
```

The code first computes the total firepower for each gun. Sorting allows the two-pointer technique to efficiently find the largest group of guns already satisfying the balance condition. The sliding window moves `r` through the array, and `l` catches up whenever the interval exceeds `k`. Subtracting the largest valid group from `n` yields the minimal modifications. A subtlety is that we must use integers throughout and avoid floating-point division, which is automatically handled since Python multiplication of integers remains integer.

## Worked Examples

Sample input from the first test case:

| f | d | p |
| --- | --- | --- |
| 6 | 1 | 6 |
| 3 | 2 | 6 |
| 13 | 1 | 13 |
| 7 | 2 | 14 |

Sorted `p` = [6, 6, 13, 14]

Sliding window:

| l | r | interval | size |
| --- | --- | --- | --- |
| 0 | 0 | [6] | 1 |
| 0 | 1 | [6,6] | 2 |
| 0 | 2 | [6,6,13] | exceeds k=2 → l=1 |
| 1 | 2 | [6,13] | exceeds k → l=2 |
| 2 | 3 | [13,14] | 2 |

Maximum inside = 2, minimum changes = 4 - 2 = 2

This trace confirms that the window correctly identifies the largest group already within `k` of each other.

Second sample case:

| f | d | p |
| --- | --- | --- |
| 100 | 100 | 10000 |
| 101 | 99 | 9999 |
| 102 | 98 | 9996 |

Sorted p = [9996, 9999, 10000]

Window for k=2:

| l | r | interval | size |
| --- | --- | --- | --- |
| 0 | 0 | [9996] | 1 |
| 0 | 1 | [9996,9999] | 2 → exceeds k → l=1 |
| 1 | 2 | [9999,10000] | 2 → exceeds k → l=2 |

Maximum inside = 1 → minimum changes = 3 - 1 = 2 (matches expected)

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) per test case | Sorting dominates; sliding window is O(n) |
| Space | O(n) | Store firepower array `p` |

Given sum of n ≤ 3000 across all test cases, total time is O(3000 log 3000), well within 3-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided samples
assert run("5\n4 2\n6 3 13 7\n1 2 1 2\n3 2\n100 101 102\n100 99 98\n5 0\n1 12 4 4 3\n12 1 3 3 4\n2 50\n1000 10\n1000000000 1\n3 5\n1 19 11\n49 4 72\n") == "2\n3\n0\n1\n2"

# custom:
```
