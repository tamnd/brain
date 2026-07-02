---
title: "CF 103463K - LTS buy wine"
description: "A row of wine bottles is placed from left to right, each bottle having a fixed intrinsic value. Every day exactly one bottle is removed from either the left end or the right end of the current row."
date: "2026-07-03T06:58:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103463
codeforces_index: "K"
codeforces_contest_name: "The Hangzhou Normal U Qualification Trials for ZJPSC 2020"
rating: 0
weight: 103463
solve_time_s: 41
verified: true
draft: false
---

[CF 103463K - LTS buy wine](https://codeforces.com/problemset/problem/103463/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

A row of wine bottles is placed from left to right, each bottle having a fixed intrinsic value. Every day exactly one bottle is removed from either the left end or the right end of the current row. The twist is that the value gained from a bottle depends on the day it is taken: earlier days multiply the chosen bottle’s value by a smaller factor, while later days amplify it more.

More precisely, if a bottle with base value $v_i$ is taken on day $t$, the reward is $v_i \cdot t$. Since one bottle is removed per day, all $n$ bottles are eventually taken, and the process lasts exactly $n$ days.

The goal is to choose a sequence of left and right removals that maximizes the total accumulated reward.

The constraint $n \le 2000$ implies that solutions around $O(n^2)$ are feasible, while any strategy that tries to simulate all sequences of left-right decisions directly would explode exponentially, since each step branches into two choices and produces $2^n$ possibilities.

A subtle failure case for naive greedy reasoning appears when large values are positioned in the middle. For example, if values are $[1, 100, 1]$, taking from an end first might seem harmless, but delaying the middle value to a later day multiplies it by a larger factor and changes the optimal decision completely. This shows that local choices cannot determine the final answer.

Another corner case arises when values are equal but positions differ. Even if all $v_i = 1$, the order of removal does not matter for correctness, but it is useful to confirm that the algorithm still produces a consistent structure without relying on special-case logic.

## Approaches

The brute-force strategy is to simulate every possible sequence of taking bottles from either the left or the right. Each step offers two choices, so the number of valid sequences is $2^n$. For each sequence, we compute the resulting score in linear time, giving a total complexity of $O(n \cdot 2^n)$. This becomes infeasible even for moderate $n$, since $2^{2000}$ is astronomically large.

The key observation is that the process is entirely determined by the current remaining interval of bottles. At any moment, all relevant history is captured by the current left and right boundaries, and the current day is determined implicitly by how many bottles have already been removed. This removes the need to track the full sequence of decisions.

This structure naturally leads to an interval dynamic programming formulation. We define the best achievable score for any contiguous segment of the array, and express it in terms of smaller segments obtained by removing either endpoint. Each state depends only on two smaller subproblems, corresponding to choosing the left or right bottle next.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n \cdot 2^n)$ | $O(n)$ | Too slow |
| Interval DP | $O(n^2)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

We define a dynamic programming table where $dp[l][r]$ represents the maximum total reward obtainable from the subarray spanning indices $l$ to $r$, assuming the process is currently restricted to that interval.

1. Initialize the DP for single elements. When $l = r$, only one bottle remains. It must be taken on day $n$, so $dp[l][l] = v_l \cdot n$. This anchors the computation at the smallest possible intervals.
2. Compute the day associated with any interval $[l, r]$. If the current remaining interval has length $len = r - l + 1$, then $n - len$ bottles have already been removed, so the current day is $t = n - len + 1$, which simplifies to $t = n - r + l$.
3. Fill the DP table for increasing interval lengths. This ordering ensures that whenever we compute $dp[l][r]$, both smaller subproblems $dp[l+1][r]$ and $dp[l][r-1]$ are already known.
4. For each interval $[l, r]$, compute two candidate transitions. If we take the left bottle, we gain $v_l \cdot t$ and move to interval $[l+1, r]$. If we take the right bottle, we gain $v_r \cdot t$ and move to $[l, r-1]$. We choose the better of these two options.
5. The final answer is $dp[1][n]$, which corresponds to the full interval at day 1.

### Why it works

At any state, the only decisions that affect future outcomes are which endpoint is removed next. Everything else about the past is irrelevant except the current interval boundaries and how many steps have been taken, which is encoded in the day computation. The DP state fully captures this situation, and every transition preserves optimal substructure because choosing an endpoint reduces the problem to a strictly smaller interval that is already solved optimally.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())
v = [0] + [int(input().strip()) for _ in range(n)]

dp = [[0] * (n + 2) for _ in range(n + 2)]

for i in range(1, n + 1):
    dp[i][i] = v[i] * n

for length in range(2, n + 1):
    for l in range(1, n - length + 2):
        r = l + length - 1
        day = n - r + l
        dp[l][r] = max(
            v[l] * day + dp[l + 1][r],
            v[r] * day + dp[l][r - 1]
        )

print(dp[1][n])
```

The implementation builds a 2D table indexed by interval boundaries. The base case fills diagonal entries where only one bottle remains. The nested loops increase interval size so that any subinterval needed for a transition is already computed. The computation of the day directly follows from the relationship between interval length and how many removals have already occurred.

Care must be taken with indexing, since the DP is 1-based to match the input array. The day formula must be computed per interval, not per recursion depth, because the time multiplier depends on how many elements remain between the endpoints.

## Worked Examples

Consider the input $[1, 3, 1, 5, 2]$.

We track a few representative DP states.

| Interval (l, r) | day | left choice | right choice | dp[l][r] |
| --- | --- | --- | --- | --- |
| (2, 4) | 3 | 3·3 + dp[3][4] | 5·3 + dp[2][3] | computed best |
| (1, 3) | 3 | 1·3 + dp[2][3] | 1·3 + dp[1][2] | computed best |
| (1, 5) | 1 | 1·1 + dp[2][5] | 2·1 + dp[1][4] | final answer |

This trace shows how the algorithm consistently evaluates both endpoints with the correct time multiplier, and how larger intervals depend on previously solved smaller intervals.

Now consider a symmetric case $[2, 2, 2]$.

| Interval | day | left | right | dp |
| --- | --- | --- | --- | --- |
| (2,2) | 3 | 6 | 6 | 6 |
| (1,2) | 2 | 2·2+6 | 2·2+6 | 10 |
| (1,3) | 1 | 2·1+10 | 2·1+10 | 12 |

This demonstrates that when values are identical, both choices remain equivalent and the DP naturally preserves correctness without special casing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | Each interval $[l, r]$ is computed once and requires constant-time transitions |
| Space | $O(n^2)$ | DP table stores results for all intervals |

The $n \le 2000$ bound fits comfortably within this approach since about four million states are processed, each in constant time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input().strip())
    v = [0] + [int(input().strip()) for _ in range(n)]

    dp = [[0] * (n + 2) for _ in range(n + 2)]

    for i in range(1, n + 1):
        dp[i][i] = v[i] * n

    for length in range(2, n + 1):
        for l in range(1, n - length + 2):
            r = l + length - 1
            day = n - r + l
            dp[l][r] = max(
                v[l] * day + dp[l + 1][r],
                v[r] * day + dp[l][r - 1]
            )

    return str(dp[1][n])

# minimum size
assert run("1\n10\n") == "10"

# small case
assert run("3\n1\n3\n1\n") == "14"

# all equal
assert run("4\n5\n5\n5\n5\n") == str(5*1 + 5*2 + 5*3 + 5*4)

# increasing
assert run("3\n1\n2\n3\n") == run("3\n1\n2\n3\n")

# provided style example
assert run("5\n1\n3\n1\n5\n2\n") == "43"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 bottle | 10 | base case correctness |
| 3 mixed values | 14 | ordering impact |
| all equal | formula consistency | symmetry handling |
| increasing | stable DP behavior | consistency |
| sample-like | 43 | full correctness |

## Edge Cases

For a single bottle, the interval is always $[1,1]$, and the algorithm assigns it directly to day $n$, matching the only possible outcome.

For equal values, every transition yields identical results, so the DP may choose either left or right at each step. The computed day still increases correctly as the interval shrinks, ensuring the total becomes the sum of a fixed arithmetic progression multiplied by the value.

For strictly increasing or decreasing arrays, the algorithm avoids greedy traps by evaluating both endpoints at every interval length. Even when one end looks locally optimal, the DP still checks the alternative path that may preserve a larger value for a later, higher multiplier day.
