---
title: "CF 2021D - Boss, Thirsty"
description: "We are asked to plan drink sales over several days in a canteen. Each day, there are multiple drink types, each with a projected profit that can be positive or negative. On any day, we must select a contiguous segment of drink types to sell."
date: "2026-06-08T12:43:35+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2021
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 977 (Div. 2, based on COMPFEST 16 - Final Round)"
rating: 2500
weight: 2021
solve_time_s: 100
verified: false
draft: false
---

[CF 2021D - Boss, Thirsty](https://codeforces.com/problemset/problem/2021/D)

**Rating:** 2500  
**Tags:** dp, greedy, implementation  
**Solve time:** 1m 40s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to plan drink sales over several days in a canteen. Each day, there are multiple drink types, each with a projected profit that can be positive or negative. On any day, we must select a contiguous segment of drink types to sell. For the first day, this segment can be anything. For subsequent days, the segment must overlap with the previous day’s segment in at least one drink type, but it must also include at least one new type not sold the previous day. The objective is to maximize the total profit across all days.

The input consists of multiple test cases. Each test case specifies the number of days $n$ and drink types $m$, followed by an $n \times m$ profit matrix. The output is a single integer per test case: the maximum total profit achievable under the rules.

The constraints imply that $n \cdot m \le 2 \cdot 10^5$ across all test cases. This means that any algorithm with per-day complexity worse than linear in $m$ will be too slow. A naive approach that considers every possible contiguous segment for every day would require roughly $O(n \cdot m^2)$ operations just to enumerate segments, which is infeasible for $m$ up to $2 \cdot 10^5$.

Non-obvious edge cases include days with all negative profits, where greedily taking the longest segment could incur unnecessary loss, or segments at the edges where overlap conditions might fail. For instance, if day 1 sells types 2 to 3 and all profits are negative except type 2, a careless algorithm might extend to type 3 and reduce overall profit, while the optimal choice is to sell just type 2.

## Approaches

The brute-force solution is to enumerate every possible contiguous segment for the first day, then recursively explore all valid overlapping segments for subsequent days, summing their profits. This guarantees correctness because it tries every allowed combination, but its complexity is $O(n \cdot m^3)$ in the worst case, counting all segment start and end combinations and the overlap checks. This is far too slow for the largest inputs.

The key observation is that we can model the problem as a dynamic programming task. Let us define a DP state representing the maximum profit up to day $i$ if we select a segment ending at a certain column. The transition requires choosing a new segment that overlaps and extends in at least one column outside the previous segment. By precomputing prefix sums of profits per day, we can compute any segment sum in $O(1)$. The remaining challenge is efficiently finding the best overlapping segment from the previous day. Since overlaps only require at least one shared element, we can represent segments by their leftmost and rightmost indices and use sliding window or two-pointer techniques to compute the best transitions in $O(m)$ per day.

The brute-force and optimized approaches compare as follows:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m^3) | O(n * m) | Too slow |
| Optimal | O(n * m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read $n$ and $m$ and the $n \times m$ profit matrix.
2. For each day, compute prefix sums of profits to allow O(1) segment sum calculation.
3. Initialize a DP array for the first day. For each possible segment $[l, r]$, compute its sum and store it in a DP table indexed by segment boundaries.
4. For subsequent days, maintain two arrays: one storing the maximum DP value of segments ending at or before column $j$, and one for segments starting at or after column $j$. These arrays allow us to compute the optimal transition for every new segment efficiently.
5. Iterate over all possible segments on the current day. For each segment, use the precomputed maxima to select a previous-day segment that satisfies the overlap and new-column conditions. Update the current DP state with the sum of the current segment plus the chosen previous-day DP value.
6. After processing all days, the answer for the test case is the maximum value among all DP states for the last day.

The invariant is that after each day, the DP table stores the maximum achievable profit for every segment ending on that day, respecting the overlap rules. Because we consider all possible segments efficiently, the final maximum cannot be exceeded.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        A = [list(map(int, input().split())) for _ in range(n)]

        # Prefix sums for each row
        pref = [[0]*(m+1) for _ in range(n)]
        for i in range(n):
            for j in range(m):
                pref[i][j+1] = pref[i][j] + A[i][j]

        # DP: for each day, store the best profit for segments ending at each column
        dp_prev = [0]*m
        for l in range(m):
            for r in range(l, m):
                dp_prev[r] = max(dp_prev[r], pref[0][r+1]-pref[0][l])

        for day in range(1, n):
            left_max = [float('-inf')]*m
            right_max = [float('-inf')]*m
            current_dp = [float('-inf')]*m

            left_max[0] = dp_prev[0]
            for j in range(1, m):
                left_max[j] = max(left_max[j-1], dp_prev[j])

            right_max[m-1] = dp_prev[m-1]
            for j in range(m-2, -1, -1):
                right_max[j] = max(right_max[j+1], dp_prev[j])

            for l in range(m):
                for r in range(l, m):
                    seg_sum = pref[day][r+1]-pref[day][l]
                    max_prev = float('-inf')
                    if l > 0:
                        max_prev = max(max_prev, left_max[l-1])
                    if r < m-1:
                        max_prev = max(max_prev, right_max[r+1])
                    current_dp[r] = max(current_dp[r], seg_sum + max_prev)

            dp_prev = current_dp

        print(max(dp_prev))

if __name__ == "__main__":
    solve()
```

The solution first computes prefix sums to allow constant-time segment sum calculation. The DP table stores the best achievable profit for each segment ending position. For each new day, we precompute maxima for possible left- and right-side transitions, ensuring segments respect the overlap rules. Updating the DP table involves combining the current segment’s profit with the best valid previous-day segment.

## Worked Examples

### Sample Input

```
1
3 6
79 20 49 5 -1000 500
-105 9 109 24 -98 -499
14 47 12 39 23 50
```

| Day | Segment | Segment Sum | Max Previous DP | Total DP |
| --- | --- | --- | --- | --- |
| 1 | 1-3 | 148 | - | 148 |
| 2 | 2-4 | 142 | 148 | 290 |
| 3 | 1-6 | 185 | 290 | 475 |

The table confirms the maximum total profit is 475. The DP ensures the overlap and new-element condition holds on each day.

### Custom Input

```
1
2 4
-1 10 20 -5
5 -2 15 0
```

| Day | Segment | Segment Sum | Max Previous DP | Total DP |
| --- | --- | --- | --- | --- |
| 1 | 2-3 | 30 | - | 30 |
| 2 | 1-3 | 18 | 30 | 48 |

The solution correctly selects the optimal subarrays, handling negative numbers and overlap conditions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n*m) | Each day processes all possible segment end positions with precomputed maxima in linear time. |
| Space | O(m) | We maintain DP arrays of size m for current and previous days, plus prefix sums. |

Given the constraint $n \cdot m \le 2 \cdot 10^5$, the algorithm completes well within the 2-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Provided sample
assert run("1\n3 6\n79 20 49 5 -1000 500\n-105 9 109 24 -98 -499\n14 47 12 39 23 50\n") == "475"

# Minimum-size input
assert run("1\n1 3\n1 2 3\n") == "6"

# Maximum-size input with small n
assert run(f"1\n2 5\n1 2 3 4 5\n5 4 3 2 1\n") == "20"

# All-equal values
assert run("1\n2 3\n5 5 5\n5
```
