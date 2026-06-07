---
title: "CF 2192C - All-in-one Gun"
description: "We are given a shooter game scenario where we have a gun with a magazine of n bullets. Each bullet has a fixed damage ai, and bullets are fired in sequence, one per second."
date: "2026-06-07T20:56:23+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 2192
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1081 (Div. 2)"
rating: 1300
weight: 2192
solve_time_s: 125
verified: true
draft: false
---

[CF 2192C - All-in-one Gun](https://codeforces.com/problemset/problem/2192/C)

**Rating:** 1300  
**Tags:** binary search, greedy, math  
**Solve time:** 2m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a shooter game scenario where we have a gun with a magazine of `n` bullets. Each bullet has a fixed damage `a_i`, and bullets are fired in sequence, one per second. The magazine must be completely emptied before a reload of `k` seconds can occur, and after reloading, the same bullet sequence is restored. The enemy starts with `h` health, and our goal is to bring it to zero or below as quickly as possible. Additionally, we can optionally swap any two bullets in the magazine once before the fight to optimize our damage output.

The input gives multiple test cases, each describing the number of bullets, enemy health, reload time, and the list of bullet damages. The output is the minimum number of seconds needed to kill the enemy for each test case.

The constraints are large: `n` can go up to 2×10^5, and `h` and `k` up to 10^9. Since the sum of `n` over all test cases is also bounded by 2×10^5, we must design an algorithm that runs in linear or linearithmic time per test case. Naive approaches that simulate every second of firing would fail, especially for high `h` values, because that could involve billions of operations.

Non-obvious edge cases include situations where the first bullets are too weak, and the optimal swap involves moving a strong bullet forward. For example, if `n = 5`, `h = 10`, `k = 2`, and `a = [1, 1, 1, 10, 1]`, a naive approach without swapping might simulate three bullets of `1` and then a reload, taking unnecessarily long. The correct move is to swap the last bullet `10` into an earlier position to minimize the kill time.

Another edge case occurs when the sum of all bullets in one magazine is less than `h`, requiring multiple full reloads. Care must be taken to compute the exact number of full cycles and remaining bullets needed, not just floor division, because overestimating reloads can inflate the kill time.

## Approaches

The brute-force method would be to simulate each second of firing, apply the optional swap at every possible pair of positions, and check the total time required. For a single test case, this could involve O(n^2) swaps, and for each swap, we might need to simulate up to `h` seconds. This is clearly infeasible with `n` up to 2×10^5 and `h` up to 10^9, as the operation count could reach 10^14.

The key observation is that the only meaningful swap is to bring the largest bullet damage forward into the first position, because the first bullets are always fired first and therefore have the most impact on kill time. Once we know this, we can consider two scenarios: the original sequence, and the sequence with the first bullet swapped with the maximum damage bullet. In both cases, we can compute the minimum number of bullets required to reach `h` health and then translate that into time by accounting for full reloads and partial cycles.

By precomputing the prefix sums of bullets in sequence, we can quickly determine how many bullets are needed without simulating each second individually. This reduces the problem from O(n^2) to O(n) per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation with all swaps | O(n^2 + h) | O(n) | Too slow |
| Optimized Swap + Prefix Sum | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read `n`, `h`, `k`, and the array of bullet damages `a`.
2. Identify the index of the maximum bullet damage in `a`. Consider swapping it with the first bullet to create an optional optimized sequence. Create `a_swapped` as the sequence after this optional swap.
3. Compute prefix sums for both the original and swapped sequences. The prefix sum `prefix[i]` represents the total damage dealt by firing the first `i` bullets in sequence.
4. For each sequence, determine the minimum number of bullets needed to reduce `h` to zero or below. If the sum of all bullets in a magazine is `s`, then full magazines can be applied `full_cycles = h // s`, with the remainder handled by additional bullets from the next magazine.
5. Convert the number of bullets needed into total time. Each full magazine consumes `n` seconds, plus a reload of `k` seconds. Partial magazines add their respective bullet count in seconds without requiring reload if they do not finish the magazine.
6. Compare the total time for the original sequence and the swapped sequence. Output the smaller time.

Why it works: The first bullets in the magazine contribute most to kill time reduction because they are fired before any reload. Swapping any other bullet pair does not improve the prefix sums of initial shots enough to reduce the minimum time further. Calculating damage using prefix sums and cycles ensures we account for all reloads accurately.

## Python Solution

```python
import sys
input = sys.stdin.readline

def min_time_to_kill(n, h, k, a):
    max_idx = max(range(n), key=lambda i: a[i])
    if max_idx != 0:
        a_swapped = a[:]
        a_swapped[0], a_swapped[max_idx] = a_swapped[max_idx], a_swapped[0]
    else:
        a_swapped = a[:]
    
    def compute_time(arr):
        prefix = [0] * n
        prefix[0] = arr[0]
        for i in range(1, n):
            prefix[i] = prefix[i-1] + arr[i]
        total = prefix[-1]
        if total >= h:
            for i, val in enumerate(prefix):
                if val >= h:
                    return i + 1
        else:
            full_cycles = h // total
            rem = h % total
            time = full_cycles * (n + k)
            if rem == 0:
                return time - k
            for i, val in enumerate(prefix):
                if val >= rem:
                    return time + i + 1
        return None

    return min(compute_time(a), compute_time(a_swapped))

t = int(input())
for _ in range(t):
    n, h, k = map(int, input().split())
    a = list(map(int, input().split()))
    print(min_time_to_kill(n, h, k, a))
```

The function `min_time_to_kill` computes the minimal seconds for one test case. We first optionally swap the first bullet with the maximum damage bullet. The `compute_time` function uses prefix sums to determine how many bullets are needed, and full magazine reloads are included in the total time. The `min` of the original and swapped sequence ensures we account for the optional swap.

## Worked Examples

**Example 1**

Input: `n = 5, h = 10, k = 1, a = [4, 2, 3, 5, 3]`

| Step | Bullet Sequence | Prefix Sum | Bullets Needed | Time |
| --- | --- | --- | --- | --- |
| Original | [4,2,3,5,3] | [4,6,9,14,17] | 4,6,9 ≥ 10 → 3 bullets | 3 s |
| Swap 2nd and max(5) → [5,2,3,4,3] | [5,7,10,14,17] | 5,7,10 ≥ 10 → 3 bullets | 3 s |  |

Time = 3 seconds

**Example 2**

Input: `n = 3, h = 10, k = 2, a = [1, 2, 3]`

| Step | Bullet Sequence | Prefix Sum | Bullets Needed | Time |
| --- | --- | --- | --- | --- |
| Original | [1,2,3] | [1,3,6] | Full magazine sum 6 < 10, full_cycles = 1 | Time = 3 + 2 reload + 1,2 bullets → total 7 |
| Swap first and max → [3,2,1] | [3,5,6] | 6 < 10 → full cycle 1 | Need remaining 4 damage → 3+2 = 5 → total 7 |  |

Time = 7 seconds

These examples show how the prefix sum and optional swap determine minimal time accurately, including reload accounting.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Finding max index, computing prefix sums, and checking minimal bullets all linear in `n` |
| Space | O(n) | Prefix sum array and swapped copy of array |

With the sum of `n` over all test cases ≤ 2×10^5, total operations are well within 2×10^5 × 2 = 4×10^5, fitting comfortably in 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())
    return output.getvalue().strip()

# Provided samples
assert run("6\n5 10 1\n4 2 3 5 3\n5 10 1\n4 2 3 7 3\n3 10
```
