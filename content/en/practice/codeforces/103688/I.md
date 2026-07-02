---
title: "CF 103688I - Equal Sum Arrays"
description: "We are asked to count how many different ordered arrays of positive integers sum up to a given number $k$. Order matters, so $[1,2]$ and $[2,1]$ are considered different, even though they have the same sum."
date: "2026-07-02T20:53:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103688
codeforces_index: "I"
codeforces_contest_name: "The 17th Heilongjiang Provincial Collegiate Programming Contest"
rating: 0
weight: 103688
solve_time_s: 44
verified: true
draft: false
---

[CF 103688I - Equal Sum Arrays](https://codeforces.com/problemset/problem/103688/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count how many different ordered arrays of positive integers sum up to a given number $k$. Order matters, so $[1,2]$ and $[2,1]$ are considered different, even though they have the same sum. Every element must be at least 1, and the array can have any length as long as the sum of all elements equals exactly $k$.

This is equivalent to asking how many ways we can break $k$ into a sequence of positive steps where each step contributes some positive integer amount, and different step orders produce different results. For example, when $k = 3$, we can either take three 1s, or a 1 followed by a 2, or a 2 followed by a 1, or a single 3.

The constraint $k \le 20$ is extremely small. Even if we tried to enumerate all possibilities, exponential growth is still manageable. A naive recursion that branches on all possible first elements would still terminate comfortably within limits for $k = 20$, but it would repeat a lot of overlapping subproblems, which suggests dynamic programming.

A subtle edge case is $k = 1$. There is exactly one array $[1]$. Any method that mistakenly assumes at least two elements or tries to split further would incorrectly produce zero or negative counts. Another edge case is treating permutations incorrectly: for example, someone might incorrectly assume $[1,2]$ and $[2,1]$ should be the same, which would lead to counting integer partitions instead of compositions.

## Approaches

The brute-force idea is to generate all arrays whose sum is $k$. At each step, we choose the next element of the array from 1 up to the remaining sum. If we are currently building a prefix that sums to $s$, and the remaining sum is $k - s$, then we branch into all choices of the next element $x$ where $1 \le x \le k - s$. We continue until the remaining sum becomes zero, which corresponds to a valid full array.

This works correctly because every valid array corresponds to exactly one path in this recursion tree. However, the number of such paths grows exponentially. For $k = 20$, the number of compositions is $2^{19} = 524288$, which is still manageable, but recursion recomputes identical suffix states many times.

The key observation is that the problem depends only on the remaining sum. If we define $dp[s]$ as the number of arrays that sum to $s$, then from state $s$, we try choosing the first element $x$, and reduce the problem to $s - x$. This means every state depends only on smaller states, and many different prefixes lead to the same remaining sum. That overlap makes memoization or bottom-up DP natural.

We can also see a direct recurrence: $dp[0] = 1$, and for $s > 0$, we sum over all possible first elements:

$$dp[s] = \sum_{x=1}^{s} dp[s-x]$$

This is a classic composition DP. It also simplifies to a well-known identity where $dp[s] = 2^{s-1}$ for $s \ge 1$, but since $k$ is tiny, deriving DP is sufficient and safer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force recursion | $O(2^k)$ | $O(k)$ | Acceptable but redundant |
| DP over sum states | $O(k^2)$ | $O(k)$ | Accepted |

## Algorithm Walkthrough

1. Define an array `dp` where `dp[i]` represents the number of valid ordered arrays that sum to `i`. This shifts the problem from constructing sequences to counting ways to reach a target sum.
2. Initialize `dp[0] = 1`. This corresponds to the empty construction, which is the only way to achieve sum zero without choosing any elements. This base case ensures that later transitions have a valid starting point.
3. For each value `i` from 1 to `k`, compute `dp[i]` by considering all possible first elements of an array that sums to `i`.
4. For a fixed `i`, try every possible first element `x` from 1 to `i`. After choosing `x`, the remaining sum becomes `i - x`, so we add `dp[i - x]` to `dp[i]`. This correctly accounts for all arrays whose first element is `x`.
5. After filling the DP table up to `k`, output `dp[k]` as the final answer.

Why it works: every valid array summing to `i` has a unique first element, and removing that first element leaves a valid array summing to a smaller value. This creates a one-to-one correspondence between arrays counted in `dp[i]` and pairs consisting of a first element and a valid suffix, ensuring no overlaps or omissions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    k = int(input().strip())
    
    dp = [0] * (k + 1)
    dp[0] = 1

    for i in range(1, k + 1):
        total = 0
        for x in range(1, i + 1):
            total += dp[i - x]
        dp[i] = total

    print(dp[k])

if __name__ == "__main__":
    solve()
```

The code directly implements the DP recurrence. The outer loop fixes the sum `i`, while the inner loop enumerates all possible first elements. The variable `total` accumulates contributions from all valid splits. Using a separate accumulator avoids repeated writes into the DP array during computation.

A common implementation mistake is forgetting to initialize `dp[0] = 1`. Without it, all states remain zero because every transition depends on smaller subproblems eventually reaching zero. Another subtle point is ensuring the inner loop starts from 1, since zero is not allowed as an array element.

## Worked Examples

### Example 1: k = 3

We compute DP step by step.

| i | x (first element) | i - x | dp[i - x] | dp[i] |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 1 |
| 2 | 1, 2 | 1, 0 | 1, 1 | 2 |
| 3 | 1, 2, 3 | 2, 1, 0 | 2, 1, 1 | 4 |

For $k = 3$, we get 4 sequences: $[1,1,1]$, $[1,2]$, $[2,1]$, and $[3]$. The DP table confirms that each decomposition of the first element contributes correctly to the total count.

### Example 2: k = 4

| i | x | i - x | dp[i - x] | dp[i] |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 1 |
| 2 | 1,2 | 1,0 | 1,1 | 2 |
| 3 | 1,2,3 | 2,1,0 | 2,1,1 | 4 |
| 4 | 1,2,3,4 | 3,2,1,0 | 4,2,1,1 | 8 |

This shows the doubling pattern emerging, which reflects the fact that each new sum introduces a new binary decision structure over whether to extend previous compositions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(k^2)$ | For each sum $i$, we iterate over all possible first elements $1 \dots i$ |
| Space | $O(k)$ | We store DP values for all sums up to $k$ |

With $k \le 20$, the solution runs in constant time effectively. Even a naive exponential recursion would pass, but DP keeps the structure clean and avoids redundant recomputation.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import prod

    k = int(inp.strip())
    dp = [0] * (k + 1)
    dp[0] = 1
    for i in range(1, k + 1):
        dp[i] = sum(dp[i - x] for x in range(1, i + 1))
    return str(dp[k])

# provided samples
assert run("1") == "1", "k=1"

# custom cases
assert run("2") == "2", "k=2"
assert run("3") == "4", "k=3"
assert run("4") == "8", "k=4"
assert run("5") == "16", "k=5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | smallest base case |
| 2 | 2 | first non-trivial split |
| 4 | 8 | exponential growth pattern |
| 5 | 16 | consistency of recurrence |

## Edge Cases

For $k = 1$, the DP initializes with `dp[0] = 1`, then `dp[1] = dp[0] = 1`. The algorithm correctly produces a single array $[1]$. Any implementation missing the base case would incorrectly output zero.

For $k = 2$, the computation goes `dp[2] = dp[1] + dp[0] = 1 + 1 = 2`, corresponding to $[1,1]$ and $[2]$. This verifies that both continuation and termination cases are counted.

For $k = 0$, although not in input constraints, the definition implies exactly one empty construction, and the initialization `dp[0] = 1` preserves correctness if extended.
