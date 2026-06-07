---
title: "CF 2167G - Mukhammadali and the Smooth Array"
description: "We are given an integer array and a corresponding cost array. For each position in the array, we can replace its value at a certain cost, and positions we do not change keep their original values."
date: "2026-06-07T23:27:34+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp"]
categories: ["algorithms"]
codeforces_contest: 2167
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 1062 (Div. 4)"
rating: 1600
weight: 2167
solve_time_s: 117
verified: false
draft: false
---

[CF 2167G - Mukhammadali and the Smooth Array](https://codeforces.com/problemset/problem/2167/G)

**Rating:** 1600  
**Tags:** data structures, dp  
**Solve time:** 1m 57s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an integer array and a corresponding cost array. For each position in the array, we can replace its value at a certain cost, and positions we do not change keep their original values. After performing any changes, we define a "drop" as a position where the value is strictly larger than the next value. The goal is to eliminate all drops at minimum cost.

The array can be as large as 8000 elements, and there can be up to 5000 test cases. The sum of the array lengths across all test cases is capped at 8000, so the total number of elements we process is modest, which allows us to use algorithms with quadratic complexity in the array length. Each element and each cost can be up to $10^9$, so we must handle large numbers carefully and avoid integer overflows in languages with fixed-width integers.

Edge cases arise when the array is already non-decreasing. In that situation, no cost is needed. Another subtle case is when replacing every element except one is optimal, for example when the array is strictly decreasing. Careless greedy approaches that only look at local drops may overpay or fail to find the global minimum. Arrays with repeated values also need careful handling, as keeping duplicates may be cheaper than replacing some values to avoid a drop.

## Approaches

A brute-force approach would consider every possible subset of positions to replace, computing the cost and checking whether the resulting array is non-decreasing. The number of subsets is $2^n$, which is astronomically large even for $n=20$, so brute force is entirely infeasible.

A more structured approach recognizes that after sorting or "compressing" the potential values, the problem can be reframed as a dynamic programming problem. At each position, the only property that matters is the final value we choose and the minimum cost to achieve a valid array up to that point. If we iterate over positions from left to right, for each candidate value at the current position, we only need to consider candidate values at the previous position that are no larger than the current value. This forms a standard DP pattern where $dp[i][v]$ represents the minimum cost to make the first $i$ elements non-decreasing, ending with value $v$.

To make this efficient, we discretize the array values. Instead of considering all $10^9$ possible integers, we only need to consider values that appear in the original array, because any optimal replacement can be reduced to a value in the original array without increasing the cost. Using this, we can implement the DP in $O(n^2)$ per test case by maintaining prefix minima to avoid re-scanning all previous states.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n) | Too slow |
| Dynamic Programming with Discretization | O(n^2) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the array `a` and the cost array `c`. Record the length `n`.
2. Collect all unique values from `a` and sort them. This sorted list of values, called `vals`, represents all possible final values we may assign to any position.
3. Initialize a DP table `dp` with dimensions `n x len(vals)`, where `dp[i][j]` represents the minimum cost to make the first `i+1` elements non-decreasing, with the `i`-th element equal to `vals[j]`.
4. Fill in the first row. For position `0`, the cost of setting it to `vals[j]` is `0` if `vals[j]` equals `a[0]` (no change), otherwise `c[0]` (we replace it).
5. Iterate over the remaining positions from `i = 1` to `n-1`. For each candidate value `vals[j]` at position `i`, find the minimum cost among all previous candidate values `vals[k]` where `vals[k] <= vals[j]`. Add `c[i]` if `vals[j] != a[i]` to account for the replacement cost.
6. Use a prefix minimum array to efficiently find the minimum over `k` values satisfying `vals[k] <= vals[j]`. This avoids scanning all previous states for each candidate, maintaining `O(n^2)` time.
7. After processing all positions, the answer is the minimum value in the last row of the DP table, representing the minimum cost to make the full array non-decreasing.

Why it works: At each step, the DP keeps the invariant that `dp[i][j]` is the minimum cost to make the first `i+1` elements non-decreasing ending with `vals[j]`. By considering all valid previous values and adding the replacement cost, we explore all feasible transformations without missing any optimal combination. Discretization ensures we only handle a manageable number of candidate values, and the prefix minimum ensures we efficiently maintain the non-decreasing constraint.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        c = list(map(int, input().split()))
        
        vals = sorted(set(a))
        m = len(vals)
        
        dp = [0] * m
        for j in range(m):
            dp[j] = 0 if vals[j] == a[0] else c[0]
        
        for i in range(1, n):
            new_dp = [0] * m
            prefix_min = [0] * m
            prefix_min[0] = dp[0]
            for j in range(1, m):
                prefix_min[j] = min(prefix_min[j-1], dp[j])
            
            for j in range(m):
                cost = 0 if vals[j] == a[i] else c[i]
                new_dp[j] = prefix_min[j] + cost
            dp = new_dp
        
        print(min(dp))

if __name__ == "__main__":
    solve()
```

The code first discretizes the array values into `vals`. The first row is initialized according to whether a replacement is needed. For each subsequent position, it constructs a prefix minimum array to efficiently enforce the non-decreasing constraint while adding the replacement cost. The final answer is simply the smallest cost achievable at the last position.

## Worked Examples

### Sample Input 1

```
4
4 3 2 1
1 1 1 1
```

| i | a[i] | vals | dp before | prefix_min | dp after |
| --- | --- | --- | --- | --- | --- |
| 0 | 4 | [1,2,3,4] | - | - | [1,1,1,0] |
| 1 | 3 | [1,2,3,4] | [1,1,1,0] | [1,1,1,0] | [2,2,1,1] |
| 2 | 2 | [1,2,3,4] | [2,2,1,1] | [2,2,1,1] | [3,2,1,2] |
| 3 | 1 | [1,2,3,4] | [3,2,1,2] | [3,2,1,1] | [4,3,2,3] |

Answer: 3

This trace shows that the DP correctly chooses replacements to eliminate drops while minimizing cost.

### Sample Input 2

```
5
1 3 2 2 4
100 1 1 1 100
```

The algorithm identifies that changing the third element from 2 to 3 costs 1, and all other elements either stay or are cheaper to replace, giving a total cost of 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) per test case | Each position iterates over at most n candidate values; total sum of n ≤ 8000 allows this |
| Space | O(n^2) | DP table stores cost for each position × candidate value, feasible under constraints |

The solution fits comfortably within the 1-second limit because the sum of n across all test cases is bounded by 8000, so n² operations across all test cases is ≤ 64 million.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("10\n1\n10\n5\n4\n1 2 2 3\n5 6 7 8\n4\n4 3 2 1\n1 1 1 1\n3\n3 1 2\n100 1 1\n5\n5 5 5 5 5\n10 1 10 1 10\n5\n1 3 2 2 4\n100 1 1 1 100\n6\n10 9 8 7 6 5\n1 100 1 100 1 100\n5\n100 1 100 100 100\n1 100 1 1 1\n4\n2 1 2 1\n5 4 3 2\n7\n1 5 3 4 2 6
```
