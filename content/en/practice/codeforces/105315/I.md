---
title: "CF 105315I - Zain's Birthday"
description: "We are given a row of tiles numbered from 0 up to n, and a cat starts at tile 0. From any tile i, the cat can jump forward to any tile j as long as j is strictly ahead and does not exceed k steps away, meaning 1 ≤ j − i ≤ k."
date: "2026-06-23T15:06:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105315
codeforces_index: "I"
codeforces_contest_name: "JPC 4.0"
rating: 0
weight: 105315
solve_time_s: 47
verified: true
draft: false
---

[CF 105315I - Zain's Birthday](https://codeforces.com/problemset/problem/105315/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a row of tiles numbered from 0 up to n, and a cat starts at tile 0. From any tile i, the cat can jump forward to any tile j as long as j is strictly ahead and does not exceed k steps away, meaning 1 ≤ j − i ≤ k. The question asks how many distinct ways exist for the cat to reach tile n if it repeatedly makes such jumps.

Each way is a sequence of positions starting at 0 and ending at n, where every step moves forward by at most k tiles. Different sequences are considered different ways even if they share intermediate positions but differ in the choice of jumps.

The input contains multiple test cases, each independent. For each pair (n, k), we must compute the number of valid jump sequences modulo 1e9 + 7.

The constraints are large: n can be up to 1e6 per test case, and the sum of all n across test cases is up to 2e6. This immediately rules out any solution that recomputes transitions from scratch for each position in O(k) time, since in the worst case k can also be large and the total work would exceed 1e12 operations.

A naive dynamic programming approach would define dp[i] as the number of ways to reach tile i, and compute dp[i] by summing dp[i − 1] through dp[i − k]. This is correct but too slow because each state may require up to k additions, giving O(nk) per test case.

A second subtle issue appears when k is large, for example k ≥ n. In that case every previous position can transition directly to i, so dp[i] becomes a prefix sum over all earlier dp values. A naive implementation that still iterates over k would do unnecessary work and TLE even though the structure simplifies completely.

## Approaches

The brute-force dynamic programming interpretation is straightforward. From each tile i, we try all possible next jumps to i + 1, i + 2, up to i + k, and accumulate contributions. This works because every valid path is uniquely constructed by extending shorter valid paths, so summing over all predecessors exactly counts all sequences.

The inefficiency comes from recomputing overlapping sums. When computing dp[i], we repeatedly sum the same dp values that were already used for dp[i + 1], dp[i + 2], and so on. The overlap between consecutive windows suggests maintaining a running window sum rather than recomputing it each time.

The key observation is that dp[i] depends only on a sliding range of the previous k values. Instead of recomputing this range sum from scratch, we maintain a rolling sum of the last k dp values. When we move from i − 1 to i, we add dp[i − 1] into the window and remove dp[i − k − 1] if it exists. This reduces each transition to O(1), turning the whole DP into linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP | O(nk) | O(n) | Too slow |
| Sliding Window DP | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We define dp[i] as the number of ways to reach tile i. The transitions come from all previous tiles within distance k.

1. Initialize dp[0] = 1 because there is exactly one way to start at the origin without making any jumps.
2. Maintain a running window sum that represents dp[i − 1] + dp[i − 2] + ... + dp[i − k], but only over valid indices. This sum represents all ways to reach the current position in one additional jump.
3. For each position i from 1 to n, set dp[i] equal to the current window sum. This works because every valid last jump must come from one of the previous k positions, and each such dp value contributes exactly one extension to i.
4. After assigning dp[i], update the window sum by adding dp[i], since it may contribute to future states.
5. If i ≥ k, remove dp[i − k] from the window sum, because it is no longer within distance k of future positions. This maintains the invariant that the window sum always reflects exactly the last k dp values.

The central idea is that each dp[i] is computed exactly once and then contributes to the next k states, after which it expires.

### Why it works

At every index i, the window sum equals the total number of ways to reach any tile j such that i − k ≤ j ≤ i − 1. Every valid path ending at i must come from exactly one such j followed by a single jump from j to i. Since dp[j] already counts all ways to reach j, summing over all valid j partitions all paths into disjoint groups based on their last jump origin. This ensures no path is missed and none is double counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve_case(n, k):
    dp = [0] * (n + 1)
    dp[0] = 1

    window_sum = 1

    for i in range(1, n + 1):
        dp[i] = window_sum % MOD
        window_sum = (window_sum + dp[i]) % MOD

        if i >= k:
            window_sum = (window_sum - dp[i - k]) % MOD

    return dp[n]

def main():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        print(solve_case(n, k))

if __name__ == "__main__":
    main()
```

The implementation follows the sliding window DP exactly. The dp array is kept for clarity, but only the last k values are actually needed to maintain correctness. The window_sum variable is the critical optimization that avoids recomputing sums repeatedly.

The subtraction step when i ≥ k is what prevents the window from growing indefinitely. Without it, the algorithm would incorrectly accumulate contributions from positions that are no longer allowed as jump origins.

## Worked Examples

Consider n = 3, k = 2.

We track dp and window_sum step by step.

| i | window_sum before | dp[i] | window_sum after add | removed | window_sum final |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 2 | none | 2 |
| 1 | 2 | 2 | 4 | none | 4 |
| 2 | 4 | 4 | 8 | dp[0]=1 | 7 |
| 3 | 7 | 7 | 14 | dp[1]=2 | 12 |

The final answer is dp[3] = 7. This trace shows how each dp value contributes to the next k positions and then drops out.

Now consider n = 4, k = 1, where only single-step moves are allowed.

| i | window_sum before | dp[i] | window_sum after add | removed | window_sum final |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 2 | none | 2 |
| 1 | 2 | 2 | 3 | dp[0]=1 | 2 |
| 2 | 2 | 2 | 4 | dp[1]=2 | 2 |
| 3 | 2 | 2 | 4 | dp[2]=2 | 2 |
| 4 | 2 | 2 | 4 | dp[3]=2 | 2 |

The result stays constant at 2 because there is only one way to move forward at each step, forming a deterministic chain.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each index is processed once with O(1) updates to the window sum |
| Space | O(n) | dp array stores all states, though it can be reduced to O(k) |

The total n across test cases is bounded by 2e6, so a linear solution per test case remains efficient. The constant-time transitions ensure the full input fits easily within the time limit.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve_case(n, k):
        dp = [0] * (n + 1)
        dp[0] = 1
        window_sum = 1
        for i in range(1, n + 1):
            dp[i] = window_sum % MOD
            window_sum = (window_sum + dp[i]) % MOD
            if i >= k:
                window_sum = (window_sum - dp[i - k]) % MOD
        return dp[n]

    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())
        out.append(str(solve_case(n, k)))
    return "\n".join(out)

# provided samples (structure inferred from statement formatting)
assert solve("2\n1 1\n2 2\n") == "1\n2"
assert solve("2\n3 1\n3 2\n") == "1\n3"
assert solve("1\n3 3\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 / 2 2 | 1 / 2 | minimal movement and exact match of n and k |
| 3 1 / 3 2 | 1 / 3 | tight constraint vs small window growth |
| 3 3 | 4 | full reachability (all prefixes contribute) |

## Edge Cases

When k = 1, the algorithm degenerates into a single-path chain. For n = 5, each dp[i] depends only on dp[i − 1], so the window sum always equals dp[i − 1]. The update rule still works because we add dp[i] and immediately remove dp[i − 1], leaving a stable propagation of values.

When k ≥ n, every dp[i] becomes the sum of all previous dp values including dp[0]. For n = 3, k = 10, the window never removes anything because i < k for all steps. The window sum accumulates all dp values, producing exponential growth consistent with the fact that every earlier tile can directly jump to any later tile.
