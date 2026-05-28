---
title: "CF 160A - Twins"
description: "We are given a collection of coins, each with a positive integer value. The task is to choose a subset of these coins such that the total value of our chosen coins is strictly greater than the total value of the coins left for the other person."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 160
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 111 (Div. 2)"
rating: 900
weight: 160
solve_time_s: 75
verified: true
draft: false
---

[CF 160A - Twins](https://codeforces.com/problemset/problem/160/A)

**Rating:** 900  
**Tags:** greedy, sortings  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of coins, each with a positive integer value. The task is to choose a subset of these coins such that the total value of our chosen coins is strictly greater than the total value of the coins left for the other person. We must also minimize the number of coins we take to achieve this goal.

The input provides the number of coins, $n$, and the values of the coins as a sequence of integers. The output is a single integer: the minimum number of coins required to exceed the sum of the remaining coins. Since each coin's value is between 1 and 100, and $n$ is at most 100, all computations fit comfortably within standard integer arithmetic. This means we can freely sum values or sort the array without worrying about overflow or expensive operations.

Edge cases that could trip up a naive approach include situations where all coins are of equal value, or when a single coin is already greater than half the total sum. For example, with input `4\n1 1 1 1`, any attempt to take fewer than 3 coins results in a tie or losing sum. Another subtle case is when one coin has a value equal to the sum of all other coins, such as `2\n3 3`; here we must take both coins to satisfy the strict inequality.

## Approaches

A brute-force approach would be to consider all possible subsets of coins, calculate their sums, and check whether each subset has a sum greater than the sum of remaining coins. This is correct but inefficient: for $n$ coins, there are $2^n$ subsets. Even at $n = 20$, this would require over a million checks, and at the maximum $n = 100$, it is infeasible.

The key observation that simplifies the problem is that the order in which we pick coins matters, and larger coins contribute more to the sum quickly. Therefore, we can sort the coins in descending order and pick coins starting from the largest. At each step, we accumulate their sum until it exceeds half of the total sum. This guarantees the smallest number of coins needed because taking smaller coins first would require more coins to surpass the remaining sum.

The optimal approach leverages sorting and a simple greedy accumulation, avoiding the need to check all subsets.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of coins, $n$, and the array of coin values. We need the full list to compute the total sum and to perform sorting.
2. Calculate the total sum of all coin values. This is necessary to know the threshold we need to exceed.
3. Sort the coins in descending order. This ensures that each coin we pick contributes the maximum possible value, minimizing the number of coins needed.
4. Initialize two variables: one to track the accumulated sum of selected coins and one to count how many coins we have taken.
5. Iterate over the sorted coins, adding each coin's value to the accumulated sum and incrementing the coin count.
6. After adding each coin, check if the accumulated sum exceeds half of the total sum. If it does, stop the iteration and return the count of coins taken.
7. Output the minimum number of coins. This satisfies the condition that our sum is strictly larger than the sum of the remaining coins.

The invariant here is that at any point in the iteration, the accumulated sum is the largest possible sum obtainable with that number of coins. By picking the largest coins first, we are guaranteed that as soon as the accumulated sum exceeds the remaining sum, no smaller subset could have achieved this with fewer coins.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
coins = list(map(int, input().split()))

total_sum = sum(coins)
coins.sort(reverse=True)

accum = 0
count = 0

for coin in coins:
    accum += coin
    count += 1
    if accum > total_sum - accum:
        print(count)
        break
```

We first read the number of coins and the list of values. The `sum` function calculates the total sum efficiently. Sorting in descending order ensures the greedy selection of largest coins first. During iteration, we accumulate the sum and count coins simultaneously. The stopping condition `accum > total_sum - accum` directly implements the strict inequality requirement. Using `break` ensures that we immediately stop as soon as we reach the condition.

## Worked Examples

**Sample 1:** `2\n3 3`

| coin | accum | total_sum - accum | count |
| --- | --- | --- | --- |
| 3 | 3 | 3 | 1 |
| 3 | 6 | 0 | 2 |

The first coin does not suffice because `3` is not greater than `3`. Taking both coins gives `6 > 0`, so the output is `2`.

**Sample 2:** `4\n1 2 2 2`

| coin | accum | total_sum - accum | count |
| --- | --- | --- | --- |
| 2 | 2 | 5 | 1 |
| 2 | 4 | 3 | 2 |

Taking the two largest coins gives `4 > 3`, so the output is `2`. This shows the greedy approach ensures the minimum number of coins.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the coins dominates; iterating to accumulate sum is O(n) |
| Space | O(n) | Storing the coin array |

With $n \leq 100$, sorting and accumulation are negligible within the 2-second time limit. Memory usage is well below the 256 MB constraint.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    coins = list(map(int, input().split()))
    total_sum = sum(coins)
    coins.sort(reverse=True)
    accum = 0
    count = 0
    for coin in coins:
        accum += coin
        count += 1
        if accum > total_sum - accum:
            return str(count)

# provided samples
assert run("2\n3 3\n") == "2", "sample 1"
assert run("4\n1 2 2 2\n") == "2", "sample 2"

# custom cases
assert run("1\n10\n") == "1", "single coin"
assert run("5\n1 1 1 1 1\n") == "3", "all equal small coins"
assert run("3\n2 5 7\n") == "2", "large coin plus another"
assert run("6\n10 10 10 1 1 1\n") == "2", "take two largest"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n10 | 1 | Single coin edge case |
| 5\n1 1 1 1 1 | 3 | Minimal number exceeding half when all coins equal |
| 3\n2 5 7 | 2 | Combination of large and smaller coin selection |
| 6\n10 10 10 1 1 1 | 2 | Greedy picks largest coins correctly |

## Edge Cases

For `2\n3 3`, iterating the sorted coins gives an accumulated sum of `3` after the first coin, which does not exceed `3`. Adding the second coin gives `6 > 0`, so the algorithm correctly outputs `2`. For `5\n1 1 1 1 1`, the algorithm selects three coins to reach `3 > 2`, showing it handles all-equal coins correctly. The stopping condition guarantees that the strict inequality is always satisfied, even in tie or boundary scenarios.
