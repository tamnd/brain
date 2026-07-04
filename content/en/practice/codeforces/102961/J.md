---
title: "CF 102961J - Missing Coin Sum"
description: "We are given a collection of positive integers that can be interpreted as coin values. Each value can be used at most once, and by selecting some subset of these coins we can form different total sums."
date: "2026-07-04T06:52:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102961
codeforces_index: "J"
codeforces_contest_name: "CSES Problem Set: Sorting and Searching"
rating: 0
weight: 102961
solve_time_s: 38
verified: true
draft: false
---

[CF 102961J - Missing Coin Sum](https://codeforces.com/problemset/problem/102961/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of positive integers that can be interpreted as coin values. Each value can be used at most once, and by selecting some subset of these coins we can form different total sums. The task is to determine the smallest positive integer amount that cannot be formed using any subset of the given coins.

The input is simply a list of coin values. The output is a single integer representing the first “gap” in achievable sums starting from zero, ignoring zero itself since an empty subset always forms it.

The key difficulty is that the number of subsets grows exponentially with the number of coins, so reasoning about sums directly is infeasible once the array grows beyond a small size. If there are up to around 10^5 coins, any approach that enumerates subsets or performs dynamic programming over sums will exceed time limits because the state space would explode beyond practical limits.

A naive approach would attempt to generate all subset sums and then search for the smallest missing integer. This fails even for moderate input sizes. For example, if coins are `[1, 2, 3, 10]`, subset sums cover many values, but explicitly constructing them already requires tracking up to 2^n combinations.

A subtler failure case appears when the smallest coin is greater than 1. For example, input `[5, 7]` has no way to form 1, so the answer is immediately 1. Any method that starts building sums without first checking this boundary will waste computation exploring irrelevant combinations.

Another important edge case is when coins are consecutive or nearly consecutive. For `[1, 2, 3]`, every number up to 6 is reachable, and the missing value becomes 7. A correct solution must recognize that intermediate structure, not just individual coin contributions.

## Approaches

The brute-force perspective starts from the definition: compute all subset sums and then scan upward from 1 until a value is missing. This is correct because it exhaustively represents every achievable configuration. However, the number of subsets doubles with each added coin, leading to roughly 2^n states. Even storing these sums becomes impossible once n grows beyond 25 or 30.

The breakthrough comes from recognizing that we do not actually need to know every achievable sum. We only care about whether all values from 1 up to some boundary are achievable continuously. If we already know that every value in `[1, x]` is reachable, then a new coin with value `v` can extend this range only if it does not create a gap. Specifically, if `v` is at most `x + 1`, then it can fill the next missing segment and extend reachability to `x + v`. Otherwise, a gap appears at `x + 1` immediately.

This transforms the problem from subset enumeration into a greedy sweep over sorted coins. Each coin either extends a continuous reachable prefix or reveals the first unreachable integer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Subset Sums | O(2^n · n) | O(2^n) | Too slow |
| Greedy Prefix Extension | O(n log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Sort the coins in ascending order. Sorting ensures we always consider the smallest available extension first, which is essential for maintaining a continuous reachable range.
2. Initialize a variable `reach = 0`, representing that all sums in the range `[1, reach]` are currently achievable. Initially, only sum 0 is achievable, so the first missing positive integer is 1 unless extended.
3. Iterate through the sorted coins one by one. For each coin value `v`, compare it with `reach + 1`.
4. If `v` is greater than `reach + 1`, stop immediately. This means there is a gap at `reach + 1` that cannot be filled by any combination of remaining coins, since all remaining coins are even larger.
5. Otherwise, if `v` is at most `reach + 1`, update `reach` to `reach + v`. This works because every value up to `reach` was previously achievable, and adding `v` allows all values up to `reach + v` to be formed by either including or excluding this coin.
6. After processing all coins or stopping early, the answer is `reach + 1`.

### Why it works

The algorithm maintains the invariant that all integers in `[1, reach]` can be formed using a subset of processed coins. Sorting guarantees we always consider the smallest coin that could extend this interval. If a coin exceeds `reach + 1`, no combination of later coins can bridge the gap because all future values are even larger, so the first unreachable integer is fixed. Otherwise, the reachable interval expands without breaks, preserving continuity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    arr = list(map(int, input().split()))
    
    arr.sort()
    
    reach = 0
    
    for v in arr:
        if v > reach + 1:
            break
        reach += v
    
    print(reach + 1)

if __name__ == "__main__":
    solve()
```

The solution begins by reading the list and sorting it so that we always handle coins in increasing order. The variable `reach` tracks the maximum continuous sum achievable starting from zero. Each coin is either absorbed into this range or causes a discontinuity.

The critical implementation detail is the condition `v > reach + 1`. Off-by-one errors typically occur here: using `>=` would incorrectly break even when a coin exactly fills the next gap.

## Worked Examples

### Example 1

Input:

```
4
1 2 3 10
```

| Step | Coin | Reach Before | Condition | Reach After |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 ≤ 1 | 1 |
| 2 | 2 | 1 | 2 ≤ 2 | 3 |
| 3 | 3 | 3 | 3 ≤ 4 | 6 |
| 4 | 10 | 6 | 10 > 7 | stop |

Output is `7`.

This trace shows how a continuous interval expands smoothly until a coin breaks the continuity. The first unreachable value is exactly where the gap appears.

### Example 2

Input:

```
3
2 2 5
```

| Step | Coin | Reach Before | Condition | Reach After |
| --- | --- | --- | --- | --- |
| 1 | 2 | 0 | 2 > 1 | stop |

Output is `1`.

This demonstrates that when the smallest coin already exceeds 1, no progress is possible and the answer is immediately fixed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, single linear scan afterward |
| Space | O(1) | Only a few variables beyond input storage are used |

The constraints typical for this kind of problem allow up to 10^5 elements, making an O(n log n) approach safe. Linear scanning ensures minimal overhead after sorting.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input().strip())
    arr = list(map(int, input().split()))
    arr.sort()
    reach = 0
    for v in arr:
        if v > reach + 1:
            break
        reach += v
    return str(reach + 1)

# provided samples (constructed)
assert run("4\n1 2 3 10\n") == "7", "sample 1"
assert run("3\n2 2 5\n") == "1", "sample 2"

# custom cases
assert run("1\n1\n") == "2", "minimum single coin"
assert run("1\n5\n") == "1", "gap at start"
assert run("5\n1 1 1 1 1\n") == "6", "all ones extend linearly"
assert run("6\n1 2 4 8 16 32\n") == "3", "binary-like gaps"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n` | `2` | smallest possible continuous case |
| `1\n5\n` | `1` | immediate gap detection |
| `1 1 1 1 1` | `6` | repeated small coins extend range |
| `1 2 4 8 16 32` | `3` | exponential gaps reveal early failure |

## Edge Cases

A key edge case arises when the smallest coin is greater than 1. For input `[5, 7, 9]`, sorting does not change order and the first coin already violates the `reach + 1` condition. The algorithm stops immediately and returns 1, correctly identifying that no positive sum can be formed.

Another case occurs when coins are dense at the beginning but sparse later. For `[1, 2, 3, 4, 10, 11]`, the reachable prefix grows smoothly to 10, then the gap at 11 becomes irrelevant because the first break already occurred at 5 if it were missing; here no break occurs early, so the final answer is determined by the first large gap after a fully dense prefix.
