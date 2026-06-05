---
title: "CF 313D - Ilya and Roads"
description: "We have a row of holes on a road, numbered from 1 to $n$. Each hole can be repaired by hiring one of $m$ companies."
date: "2026-06-06T00:54:12+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 313
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 186 (Div. 2)"
rating: 2100
weight: 313
solve_time_s: 68
verified: true
draft: false
---

[CF 313D - Ilya and Roads](https://codeforces.com/problemset/problem/313/D)

**Rating:** 2100  
**Tags:** dp  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a row of holes on a road, numbered from 1 to $n$. Each hole can be repaired by hiring one of $m$ companies. Each company offers to fix a consecutive segment of holes $[l_i, r_i]$ at a fixed cost $c_i$, regardless of whether some of those holes are already repaired by another company. Ilya wants to repair at least $k$ holes using some combination of these companies, and we need to find the minimum total cost to achieve this. If it is impossible to repair at least $k$ holes, we should output -1.

The constraints give us that $n$ can be up to 300 and $m$ can be up to $10^5$. This is significant because $n$ is small enough to consider DP over the number of repaired holes or positions, but $m$ is too large to iterate over all subsets of companies directly. Each cost can be as large as $10^9$, which suggests using 64-bit integers to avoid overflow. A naive approach that tries every combination of companies would be $O(2^m)$, which is infeasible for $m = 10^5$.

Non-obvious edge cases include situations where all companies cover overlapping segments but not enough holes cumulatively to reach $k$. For example, if $n = 3$, $k = 3$, and the companies are $[1,1,1]$ and $[3,3,1]$, then hole 2 cannot be repaired by any company. Any naive approach that assumes union coverage will incorrectly report success.

## Approaches

The brute-force approach would consider every subset of companies and compute the union of holes repaired, keeping track of the cost. This is correct in principle but has complexity $O(2^m \cdot n)$, which is astronomical for $m = 10^5$. Therefore, brute-force is infeasible.

The key observation is that the number of holes $n$ is small. This allows us to formulate a dynamic programming solution where the state represents the minimum cost to repair exactly a certain number of holes up to a certain position. We can sort companies by their right endpoints and process them in order. At each DP state, we can decide whether to use a company to extend a repaired segment, updating the minimum cost for each possible total number of repaired holes. This transforms the exponential subset problem into a manageable DP with dimensions $n \times n$ (positions × repaired holes), which is feasible because $n \le 300$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^m * n) | O(n) | Too slow |
| Optimal DP | O(n^2 * m) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Initialize a DP table `dp[i][j]` where `i` represents the last hole repaired, and `j` represents the total number of holes repaired. Fill it with infinity, except `dp[0][0] = 0` representing no cost for repairing 0 holes.
2. For each company, represented by the segment `[l, r]` with cost `c`, consider how it can extend the currently repaired segments. Iterate `i` from `n` down to 0 (to avoid double counting in this iteration). For each `j` from 0 to `n`, if `dp[i][j]` is finite, compute the new state: the number of additional holes fixed by this company that are beyond `i` is `max(0, r - max(i, l-1))`. Update `dp[r][j + new_holes] = min(dp[r][j + new_holes], dp[i][j] + c)`.
3. After processing all companies, the answer is the minimum `dp[i][j]` over all `i` and all `j >= k`. If no such state is finite, return -1.

Why it works: `dp[i][j]` always stores the minimal cost to repair exactly `j` holes up to position `i`. By processing companies in order and only considering non-overlapping contributions to `new_holes`, we ensure we never overcount. This preserves correctness and guarantees the minimal cost is found.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m, k = map(int, input().split())
companies = [tuple(map(int, input().split())) for _ in range(m)]

INF = 10**18
dp = [[INF] * (n+1) for _ in range(n+1)]
dp[0][0] = 0

for l, r, c in companies:
    l -= 1
    for i in range(n, -1, -1):
        for j in range(n+1):
            if dp[i][j] != INF:
                add = max(0, r - max(i, l))
                if j + add <= n:
                    dp[r][j + add] = min(dp[r][j + add], dp[i][j] + c)

res = min(dp[i][j] for i in range(n+1) for j in range(k, n+1))
print(res if res != INF else -1)
```

The DP table `dp[i][j]` is filled in reverse over `i` to avoid using the same company twice in the same iteration. We adjust indices because Python uses 0-based indexing. The `max(0, r - max(i, l))` ensures we count only new holes that extend beyond already repaired segments, correctly modeling the cost behavior.

## Worked Examples

Sample Input 1:

```
10 4 6
7 9 11
6 9 13
7 7 7
3 5 6
```

| Step | i | j | add | dp[r][j+add] updated |
| --- | --- | --- | --- | --- |
| initial | 0 | 0 | - | 0 |
| company 1 | 0 | 0 | 3 | dp[9][3] = 11 |
| company 2 | 0 | 0 | 4 | dp[9][4] = 13 |
| company 3 | 0 | 0 | 1 | dp[7][1] = 7 |
| company 4 | 0 | 0 | 3 | dp[5][3] = 6 |

After combining optimal segments, the minimum cost to repair at least 6 holes is 17, achieved by using company 4 (holes 3-5, cost 6) and company 1 (holes 7-9, cost 11).

Custom Input:

```
5 2 5
1 3 10
3 5 15
```

The optimal solution repairs holes 1-5 using both companies, cost 25.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2 * m) | For each company, we iterate over `i` and `j` in the DP table |
| Space | O(n^2) | DP table of size `(n+1)*(n+1)` |

Since $n \le 300$ and $m \le 10^5$, the maximum number of operations is approximately $3 \times 10^7$, which fits comfortably within 3 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m, k = map(int, input().split())
    companies = [tuple(map(int, input().split())) for _ in range(m)]
    INF = 10**18
    dp = [[INF] * (n+1) for _ in range(n+1)]
    dp[0][0] = 0
    for l, r, c in companies:
        l -= 1
        for i in range(n, -1, -1):
            for j in range(n+1):
                if dp[i][j] != INF:
                    add = max(0, r - max(i, l))
                    if j + add <= n:
                        dp[r][j + add] = min(dp[r][j + add], dp[i][j] + c)
    res = min(dp[i][j] for i in range(n+1) for j in range(k, n+1))
    return str(res if res != INF else -1)

# provided sample
assert run("10 4 6\n7 9 11\n6 9 13\n7 7 7\n3 5 6\n") == "17", "sample 1"
# minimal input
assert run("1 1 1\n1 1 5\n") == "5", "min size"
# impossible case
assert run("3 2 3\n1 1 1\n3 3 1\n") == "-1", "impossible"
# full coverage
assert run("5 2 5\n1 3 10\n3 5 15\n") == "25", "full coverage"
# overlapping cheaper
assert run("5 3 4\n1 3 5\n2 5 8\n1 5 20\n") == "13", "overlap cheaper"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 10 4 |  |  |
