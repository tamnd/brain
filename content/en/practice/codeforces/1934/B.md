---
title: "CF 1934B - Yet Another Coin Problem"
description: "We are given a fixed set of coin denominations: 1, 3, 6, 10, and 15. For each query, we must construct an exact total value n using any number of these coins, with the goal of minimizing how many coins are used."
date: "2026-06-08T18:08:53+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1934
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 931 (Div. 2)"
rating: 1200
weight: 1934
solve_time_s: 80
verified: true
draft: false
---

[CF 1934B - Yet Another Coin Problem](https://codeforces.com/problemset/problem/1934/B)

**Rating:** 1200  
**Tags:** brute force, dp, greedy, math  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed set of coin denominations: 1, 3, 6, 10, and 15. For each query, we must construct an exact total value n using any number of these coins, with the goal of minimizing how many coins are used.

The key structure here is that coin types are fixed and very small in number, but n can be extremely large, up to one billion. That immediately suggests that enumerating combinations or doing any state-based dynamic programming over n is impossible. A solution must compute the answer per test case in constant or very small amortized time.

A naive reading might suggest this resembles a shortest path or knapsack-style minimization problem. However, the constraints on coin values and their specific structure strongly suggest a greedy or bounded decomposition approach.

One subtle edge case is that greedy strategies based purely on the largest coin can fail if the coin system is not canonical. For example, with coins like 1, 3, 4, greedy fails for 6 (4+1+1 vs 3+3). So we cannot assume greed works without justification. We must rely on the special structure of triangular numbers.

Another edge case is small values of n where the best combination may mix many small coins rather than one large coin. For example, n = 2 cannot use any coin larger than 1, so it must fall back to two 1-coins. Any strategy must correctly handle these low values without assuming availability of larger denominations.

## Approaches

A brute-force approach would treat this as a classic unbounded knapsack: for each n, compute dp[x] as the minimum number of coins needed to form sum x. This requires transitions over five coin types, giving O(n) per test case. With n up to 1e9 and up to 1e4 test cases, this is completely infeasible both in time and memory.

We need a different perspective. The crucial observation is that the coin set is extremely small and structured. The largest coin is 15, and all coins are multiples or combinations in a very tight range. This suggests that for large n, the solution will be dominated by using as many 15-coins as possible, with only a small remainder that can be handled optimally.

This leads to a bounded residue strategy. Any optimal solution can be written as:

n = 15k + r, where r < 15

The key idea is that once we fix how many 15-coins we use, the remaining problem is only about a small remainder r, which can be solved optimally by brute force or precomputation. However, simply taking floor(n / 15) is not always optimal, because reducing one 15-coin can sometimes allow a better combination of smaller coins that reduces total coin count.

So instead of fixing k exactly, we try a small window around n // 15, typically k, k-1, k-2, since the best solution can only deviate slightly due to coin granularity. For each candidate k, we compute the remainder and solve it optimally for small values. The remainder part is bounded (less than 30 or 45 in practice depending on adjustment range), so it can be precomputed via a small DP.

Thus the problem reduces to trying a constant number of possibilities per test case, each evaluated in O(1).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP up to n | O(n) per test | O(n) | Too slow |
| Greedy without correction | O(1) | O(1) | Incorrect |
| Residue + local DP | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

We precompute a small DP table for all values up to a fixed limit, for example 30 or 45, using standard unbounded coin DP with the five denominations. This gives the exact minimum number of coins for any small remainder.

For each test case:

1. Compute k = n // 15. This is the baseline count of the largest coin.

This is chosen because 15 is the largest denomination and dominates large sums efficiently.
2. For candidate values of k, consider k, k-1, and k-2, skipping negative values.

The reason is that replacing one 15-coin increases the remainder by 15, and sometimes this allows a significantly better decomposition in smaller coins.
3. For each candidate k, compute r = n - 15 * k.

This reduces the problem to solving a small fixed-value instance.
4. If r is within the precomputed DP range, take dp[r] as the cost.

This gives the optimal way to form the remainder using coins 1, 3, 6, 10, 15.
5. Track the minimum value of k + dp[r] over all candidates.

This combines large coin usage and optimal remainder decomposition.
6. Output the minimum found value.

### Why it works

Any optimal solution can be viewed as a choice of how many 15-coins are used, plus a remainder composed of smaller coins. If we use too many 15-coins, we leave a small remainder that is expensive to fix. If we use too few, we waste efficiency in large coverage. The optimal solution must lie close to the greedy choice of n // 15 because changing k by more than a small constant would shift at least 15 units of value, and such a shift cannot be compensated by improvements in the small coin system beyond a bounded range.

Thus, restricting k to a constant neighborhood around the greedy choice preserves optimality while reducing the problem to constant-time lookup over a precomputed finite state space.

## Python Solution

```python
import sys
input = sys.stdin.readline

coins = [1, 3, 6, 10, 15]

MAX_R = 45
INF = 10**9

dp = [INF] * (MAX_R + 1)
dp[0] = 0

for i in range(1, MAX_R + 1):
    for c in coins:
        if i >= c:
            dp[i] = min(dp[i], dp[i - c] + 1)

def solve():
    n = int(input())
    k = n // 15
    ans = INF

    for dk in [0, -1, -2]:
        kk = k + dk
        if kk < 0:
            continue
        r = n - 15 * kk
        if 0 <= r <= MAX_R:
            ans = min(ans, kk + dp[r])

    print(ans)

t = int(input())
for _ in range(t):
    solve()
```

The DP table `dp` is computed once for all small residues. This is crucial because it avoids recomputation across test cases.

Inside `solve`, we anchor the solution around the greedy number of 15-coins. We explicitly test nearby values because the coin system is not strictly canonical, and local adjustments can improve the total coin count.

The choice of MAX_R = 45 ensures that even after decreasing k by up to 2, the remainder stays within a range where DP is valid. This constant bound is what guarantees O(1) per test case.

## Worked Examples

### Example 1

Input:

n = 16

We compute k = 1.

| k | remainder r = n - 15k | dp[r] | total k + dp[r] |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 2 |
| 0 | 16 | dp[16] = 2 | 2 |
| -1 | invalid | - | - |

The minimum is 2, achieved either as 15 + 1 or 10 + 6.

This shows that both “one large coin + small residue” and “two medium coins” can be equally optimal, and the algorithm correctly captures both.

### Example 2

Input:

n = 20

k = 1

| k | remainder r | dp[r] | total |
| --- | --- | --- | --- |
| 1 | 5 | 3 | 4 |
| 0 | 20 | dp[20] = 2 | 2 |

The optimal solution is not to use a 15-coin at all. Instead, 20 = 10 + 10 uses only two coins.

This demonstrates why we must consider k-1 or k-2 adjustments. A purely greedy use of 15 would be suboptimal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test | Only 3 candidates and constant DP lookup |
| Space | O(1) | DP table is fixed size (≤ 45) |

The solution comfortably handles 10^4 test cases because each query performs only constant arithmetic and a few array lookups.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    coins = [1, 3, 6, 10, 15]
    MAX_R = 45
    INF = 10**9

    dp = [INF] * (MAX_R + 1)
    dp[0] = 0

    for i in range(1, MAX_R + 1):
        for c in coins:
            if i >= c:
                dp[i] = min(dp[i], dp[i - c] + 1)

    def solve_case(n):
        k = n // 15
        ans = INF
        for dk in [0, -1, -2]:
            kk = k + dk
            if kk < 0:
                continue
            r = n - 15 * kk
            if 0 <= r <= MAX_R:
                ans = min(ans, kk + dp[r])
        return ans

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        out.append(str(solve_case(n)))
    return "\n".join(out)

# provided samples
assert run("""14
1
2
3
5
7
11
12
14
16
17
18
20
98
402931328
""") == """1
2
1
3
2
2
2
3
2
3
2
2
8
26862090"""

# custom cases
assert run("1\n15\n") == "1", "exact large coin"
assert run("1\n30\n") == "2", "two large coins"
assert run("1\n2\n") == "2", "small fallback"
assert run("1\n10\n") == "1", "single medium coin"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 15 | 1 | exact use of largest coin |
| 30 | 2 | multiple large coins |
| 2 | 2 | fallback to 1-coins |
| 10 | 1 | single medium coin works optimally |

## Edge Cases

For n = 2, no coin larger than 1 can be used. The algorithm evaluates k = 0, r = 2 and uses dp[2] = 2, correctly returning two 1-coins.

For n = 15, k = 1 gives r = 0, so the answer is 1. Any attempt to reduce k would increase the number of smaller coins and produce a worse result.

For n = 20, the algorithm explicitly tests k = 1 and k = 0. The second choice yields dp[20] = 2, which is optimal. This demonstrates why the neighborhood search around k is necessary for correctness.
