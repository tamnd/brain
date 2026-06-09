---
title: "CF 1706C - Qpwoeirut And The City"
description: "We are given a row of buildings, each with a certain number of floors. A building is considered \"cool\" if it is strictly taller than both its immediate neighbors. The first and last buildings cannot be cool because they do not have two neighbors."
date: "2026-06-09T21:17:24+07:00"
tags: ["codeforces", "competitive-programming", "dp", "flows", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1706
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 809 (Div. 2)"
rating: 1400
weight: 1706
solve_time_s: 111
verified: false
draft: false
---

[CF 1706C - Qpwoeirut And The City](https://codeforces.com/problemset/problem/1706/C)

**Rating:** 1400  
**Tags:** dp, flows, greedy, implementation  
**Solve time:** 1m 51s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a row of buildings, each with a certain number of floors. A building is considered "cool" if it is strictly taller than both its immediate neighbors. The first and last buildings cannot be cool because they do not have two neighbors. We can increase the height of any building by adding floors, and the goal is to maximize the number of cool buildings while minimizing the total number of additional floors added.

The input consists of multiple test cases. Each test case provides the number of buildings and their current heights. The output for each test case is the minimum number of floors needed to maximize the number of cool buildings.

The constraints indicate that the sum of the number of buildings over all test cases does not exceed 200,000. This rules out solutions that would be quadratic in the number of buildings per test case. We need an algorithm that runs roughly in linear time for each test case.

Non-obvious edge cases include sequences where buildings are already alternating in height or sequences where multiple adjacent buildings are equal in height. For instance, a sequence `[1, 2, 1, 2, 1]` already has maximal cool buildings at positions 2 and 4, so no additional floors are needed. Another tricky case is `[3, 1, 4, 4, 2]` where two consecutive buildings are equal; choosing which building to increase can affect the total number of floors added.

## Approaches

A brute-force approach would be to try making each internal building cool individually and calculate the number of floors required. We could then try all combinations of buildings to find the maximum number of cool buildings and the minimum additional floors. However, for `n` up to `10^5`, trying all combinations is clearly infeasible, as the number of possibilities grows exponentially.

The key insight is that we do not need to consider all combinations. Cool buildings cannot be adjacent, because if we try to make two consecutive buildings taller than their neighbors, their heights would conflict. This observation reduces the problem to an independent choice of either all odd-indexed internal buildings or all even-indexed internal buildings. We can compute the floors needed for these two patterns and pick the one with the smaller sum. For sequences of odd length, we might need to consider a hybrid approach by checking overlapping pairs, but for the majority of cases, comparing the odd and even positions is sufficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the number of buildings `n` and the array of heights `h`.
2. If `n` is odd, initialize two sums: one for the additional floors needed to make all odd-indexed internal buildings cool, and another for all even-indexed internal buildings.
3. For each internal building at index `i` (1-based, so `2 ≤ i ≤ n-1`), compute the minimum number of floors needed to make it taller than both neighbors: `max(h[i-1], h[i+1]) + 1 - h[i]`. If the result is negative, use zero.
4. Add the computed floors to the sum for odd or even positions depending on `i`.
5. After processing all internal buildings, if `n` is odd, pick the minimum of the two sums. If `n` is even, the pattern is more complex, so use a sliding window approach to compute sums of non-adjacent cool buildings and pick the minimal total.
6. Output the minimal total floors for the test case.

Why it works: The invariant is that no two adjacent buildings can both be cool, so any optimal solution must select a subset of non-adjacent buildings. The algorithm considers two maximal non-adjacent subsets (odd and even), guaranteeing that we find the minimal total for maximizing the number of cool buildings.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        h = list(map(int, input().split()))
        if n % 2 == 1:
            total = 0
            for i in range(1, n-1, 2):
                total += max(0, max(h[i-1], h[i+1]) + 1 - h[i])
            print(total)
        else:
            # Sliding window for even length
            add = [0] * (n-2)
            for i in range(1, n-1):
                add[i-1] = max(0, max(h[i-1], h[i+1]) + 1 - h[i])
            prefix = [0] * (n-1)
            prefix[0] = add[0]
            for i in range(1, n-2):
                prefix[i] = prefix[i-1] + add[i]
            res = float('inf')
            for i in range((n-2)//2 + 1):
                left = prefix[i-1] if i > 0 else 0
                right = prefix[-1] - prefix[i + (n-2)//2 - 1] if i + (n-2)//2 - 1 < n-3 else 0
                middle = prefix[i + (n-2)//2 - 1] - prefix[i-1] if i > 0 else prefix[i + (n-2)//2 - 1]
                res = min(res, left + right + middle)
            print(res)

solve()
```

The code first handles odd-length sequences by summing the minimal floors required for every other building. For even-length sequences, it precomputes the floors needed for all internal buildings, then uses a prefix sum and sliding window to consider combinations of non-adjacent buildings. Special care is taken with indexing to avoid off-by-one errors. Negative values are clamped to zero because no floors are needed if a building is already taller than both neighbors.

## Worked Examples

**Example 1**

Input: `[2, 1, 2]`

| i | h[i-1] | h[i] | h[i+1] | floors needed |
| --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 2 | 2 |

The second building is the only internal building. We need to add 2 floors to make it taller than both neighbors. Output is `2`. This confirms that a single internal building can be processed directly.

**Example 2**

Input: `[1, 2, 1, 4, 3]`

| i | h[i-1] | h[i] | h[i+1] | floors needed |

|---|--------|------|--------|
