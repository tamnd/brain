---
title: "CF 1286A - Garland"
description: "We are given a row of n bulbs, each numbered from 1 to n. Some bulbs are missing, indicated by zeros in the input array."
date: "2026-06-11T19:09:52+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1286
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 612 (Div. 1)"
rating: 1800
weight: 1286
solve_time_s: 162
verified: true
draft: false
---

[CF 1286A - Garland](https://codeforces.com/problemset/problem/1286/A)

**Rating:** 1800  
**Tags:** dp, greedy, sortings  
**Solve time:** 2m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a row of `n` bulbs, each numbered from `1` to `n`. Some bulbs are missing, indicated by zeros in the input array. Our goal is to fill in the missing bulbs using the numbers that are not already present, and to place them in a sequence that minimizes the number of adjacent pairs with different parity. Complexity, in this problem, counts how many adjacent pairs have one even and one odd number. For example, if a sequence is `1 4 2 3 5`, there are two transitions between odd and even: `(1,4)` and `(2,3)`.

The input size is small: `n` can go up to 100. This means we can afford an `O(n^3)` or even `O(n^4)` approach, but an `O(n^2)` dynamic programming solution is cleaner and robust. A careless approach that just greedily places the smallest missing numbers without considering parity can easily create unnecessary transitions. For instance, if `n=4` and the sequence is `0 0 1 0`, filling zeros from left to right without thinking of parity could yield `[2,3,1,4]`, producing three parity transitions, whereas `[3,2,1,4]` yields only one.

An edge case occurs when all missing positions are consecutive or at the ends. In these cases, we need to track the parity of the last placed bulb to avoid extra complexity.

## Approaches

A naive brute-force solution would try every possible permutation of the missing numbers, count the resulting complexity for each, and return the minimum. This works because there are `k` missing numbers, so in principle it requires `k!` arrangements. However, in the worst case `k=n=100`, which is astronomically large (`100!`) and obviously infeasible. Even trying all ways to partition missing numbers into odd and even groups quickly explodes in combinations.

The key observation is that the complexity only depends on the parity of adjacent numbers, not their exact values. This allows us to reduce the problem to a **dynamic programming problem over positions and remaining counts of odd and even numbers**. Specifically, for each position in the array, we can track the minimum complexity if the previous number is odd or even, and the number of unused odd and even bulbs remaining. The DP state is `(pos, odd_remaining, even_remaining, prev_parity)` and the transition places an odd or even number at the current zero position, updating the complexity if it differs from `prev_parity`.

This structure works because every decision depends only on the parity of the previous number and how many bulbs of each type remain. We never need to know the exact values. We use memoization to store intermediate results and avoid recomputation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k!) | O(n) | Too slow |
| DP over parity | O(n^3) | O(n^3) | Accepted |

## Algorithm Walkthrough

1. Identify which numbers are missing from the array and classify them into odd and even counts. If the total numbers are from `1` to `n`, compute the missing ones by subtracting the numbers already present.
2. Define a DP table `dp[pos][odd_left][even_left][prev_parity]`, where `pos` is the current index, `odd_left` and `even_left` count how many unused odd and even bulbs remain, and `prev_parity` is the parity of the previous bulb placed. Initialize all values to infinity, except the starting position where no bulbs are placed and `prev_parity` can be undefined.
3. Iterate over positions. If a bulb is already placed (non-zero), update the DP by only considering transitions consistent with its parity, incrementing complexity if its parity differs from `prev_parity`. If the bulb is missing (zero), try placing an odd or even bulb if any remain. Update the DP table by taking the minimum complexity over both choices.
4. At the end, the answer is the minimum value among `dp[n][0][0][0]` and `dp[n][0][0][1]`, representing all bulbs placed with the last bulb being even or odd.
5. Return this minimum as the minimum complexity of the garland.

Why it works: The DP guarantees correctness because at each step we consider all valid choices of parity for zeros and track the exact number of remaining odd/even bulbs. Since complexity only depends on parity transitions, the DP state fully captures the information needed for optimal decisions. The memoization ensures that overlapping subproblems are computed only once.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
p = list(map(int, input().split()))

used = [False] * (n + 1)
for x in p:
    if x != 0:
        used[x] = True

odd_left = sum(1 for i in range(1, n+1) if not used[i] and i % 2 == 1)
even_left = sum(1 for i in range(1, n+1) if not used[i] and i % 2 == 0)

INF = 10**9
dp = [[[INF, INF] for _ in range(even_left+1)] for _ in range(odd_left+1)]
dp[odd_left][even_left][0] = 0
dp[odd_left][even_left][1] = 0

for idx, val in enumerate(p):
    new_dp = [[[INF, INF] for _ in range(even_left+1)] for _ in range(odd_left+1)]
    for o in range(odd_left+1):
        for e in range(even_left+1):
            for prev_parity in [0,1]:
                if dp[o][e][prev_parity] >= INF:
                    continue
                if val != 0:
                    cur_parity = val % 2
                    add = 0 if idx == 0 or cur_parity == prev_parity else 1
                    new_dp[o][e][cur_parity] = min(new_dp[o][e][cur_parity], dp[o][e][prev_parity] + add)
                else:
                    if o > 0:
                        cur_parity = 1
                        add = 0 if idx == 0 or cur_parity == prev_parity else 1
                        new_dp[o-1][e][cur_parity] = min(new_dp[o-1][e][cur_parity], dp[o][e][prev_parity] + add)
                    if e > 0:
                        cur_parity = 0
                        add = 0 if idx == 0 or cur_parity == prev_parity else 1
                        new_dp[o][e-1][cur_parity] = min(new_dp[o][e-1][cur_parity], dp[o][e][prev_parity] + add)
    dp = new_dp

res = min(dp[0][0][0], dp[0][0][1])
print(res)
```

Explanation: We first count unused odd and even numbers. Then we use a DP over `(odd_left, even_left, prev_parity)` instead of full indices for efficiency. For each position, we propagate the previous state to the next, incrementing the complexity if the parity changes. We carefully check boundaries to avoid negative indices. The minimum complexity is taken after processing all positions.

## Worked Examples

### Example 1

Input: `5\n0 5 0 2 3\n`

| idx | val | o | e | prev_parity | new_dp[odd][even][cur_parity] |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 2 | 1 | - | Try odd:1, even:2 |
| 1 | 5 | - | - | - | Only parity=1 considered, add 0 if same parity, else 1 |
| 2 | 0 | 1 | 1 | - | Try odd/even placement |
| 3 | 2 | - | - | - | Only parity=0 considered |
| 4 | 3 | - | - | - | Only parity=1 considered |

Result: `2` transitions.

### Example 2

Input: `7\n0 7 3 5 0 0 0\n`

Processing all zeros while tracking remaining odd/even bulbs leads to a single transition in optimal placement.

These traces confirm that our DP handles both internal and terminal zeros correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^3) | Three nested loops: odd_left (≤n/2), even_left (≤n/2), prev_parity (2) |
| Space | O(n^3) | DP table of size (odd_left+1) * (even_left+1) * 2 |

Given `n≤100`, worst-case operations are on the order of 50^2_2_100=~500,000, which is acceptable under 1s time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    exec(open('solution.py').read())  # assuming code above is saved as solution.py
    return sys.stdout.getvalue().strip()

# provided samples
assert run("5\n0 5 0
```
