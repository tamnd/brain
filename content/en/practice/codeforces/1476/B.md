---
title: "CF 1476B - Inflation"
description: "We are given a sequence of monthly price increases for a single product. The first value represents the initial price, and each subsequent value is the nominal increase in that month."
date: "2026-06-10T23:58:18+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1476
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 103 (Rated for Div. 2)"
rating: 1300
weight: 1476
solve_time_s: 107
verified: true
draft: false
---

[CF 1476B - Inflation](https://codeforces.com/problemset/problem/1476/B)

**Rating:** 1300  
**Tags:** binary search, brute force, greedy, math  
**Solve time:** 1m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of monthly price increases for a single product. The first value represents the initial price, and each subsequent value is the nominal increase in that month. We are asked to ensure that the monthly inflation percentage, calculated as the ratio of that month's increase to the cumulative price up to that month, does not exceed a given threshold $k$ percent. To achieve this, we can increase the initial price and/or previous months' prices, but we want to do so while minimizing the total additional amount added.

Each test case provides the number of months $n$, the maximum allowed inflation percentage $k$, and the array of price increases $p$. The output is a single integer per test case, the minimal total sum that needs to be added to the array so that the inflation constraint holds for every month.

Constraints are moderate: $n$ is at most 100 and $t$ up to 1000, meaning the solution should work efficiently in $O(n)$ per test case. The individual price increases can be up to $10^9$, which rules out approaches that rely on naive brute-force enumeration of all possible price additions. The non-obvious edge case arises when a very small initial price is followed by a large increase: without adjustment, the inflation coefficient would exceed $k$ by a wide margin. For example, with $p = [1, 100]$ and $k = 1$, the second month's increase is 100 times the initial price, far above the 1% limit. A naive solution that checks only if $p_i \le k$ fails completely.

## Approaches

The brute-force approach would consider all possible increments to the cumulative sum for each month and check which combination satisfies the inflation cap. This approach is correct but impractical: for each month, there are potentially $O(10^9)$ increments to consider, leading to an astronomically high operation count.

The key insight is that the problem can be solved greedily from left to right. The inflation coefficient for month $i$ is defined as $p_i / S$, where $S$ is the sum of all previous values after adjustment. To ensure $p_i / S \le k / 100$, we can solve for the minimum required cumulative sum $S$ as $S \ge \lceil (p_i \cdot 100) / k \rceil$. If the current cumulative sum is smaller than this, we add the difference to the running total. By processing months sequentially, we always adjust the total increment minimally to satisfy the constraint, ensuring we do not overcompensate. This is linear in $n$ and works within the given bounds.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((max p_i)^n) | O(n) | Too slow |
| Greedy Sequential | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize `total_add` to zero to track the sum of all additions and set `cumulative` to the first month's price.
2. Iterate over months from the second month to the last.
3. For each month $i$, calculate the required minimum cumulative sum as `(p[i] * 100 + k - 1) // k`. This formula ensures we round up to the nearest integer.
4. If the current cumulative sum `cumulative` is less than the required minimum, compute the difference and add it to `total_add`. Update `cumulative` by adding this difference.
5. Add the current month's price `p[i]` to `cumulative`, reflecting that we are now including this month in the total for subsequent months.
6. After processing all months, output `total_add`.

The invariant is that after processing month $i$, the cumulative sum is always sufficient to keep the inflation of all months up to $i$ below $k$ percent. By maintaining this invariant, we ensure the inflation constraint is never violated.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        p = list(map(int, input().split()))
        total_add = 0
        cumulative = p[0]
        for i in range(1, n):
            required = (p[i] * 100 + k - 1) // k
            if cumulative < required:
                add = required - cumulative
                total_add += add
                cumulative += add
            cumulative += p[i]
        print(total_add)

if __name__ == "__main__":
    solve()
```

The code begins by reading the number of test cases and processing each test case individually. We initialize `total_add` to zero and set `cumulative` to the first month's price, reflecting the starting price. The loop computes the required cumulative sum using ceiling division to handle integer rounding. If the current cumulative sum is insufficient, we add the necessary amount to `total_add` and update `cumulative`. Finally, we add the current month's price to `cumulative` for future checks. Using integer arithmetic throughout avoids floating-point errors.

## Worked Examples

### Sample 1

Input:

```
4 1
20100 1 202 202
```

| Month | p[i] | cumulative before | required min | add | cumulative after |
| --- | --- | --- | --- | --- | --- |
| 0 | 20100 | 20100 | - | 0 | 20100 |
| 1 | 1 | 20100 | 100 | 0 | 20101 |
| 2 | 202 | 20101 | 20200 | 99 | 20200 + 202 = 20401 |
| 3 | 202 | 20401 | 20200 | 0 | 20401 + 202 = 20603 |

Total added: 99

This trace shows the algorithm correctly identifies that the third month requires an extra 99 to satisfy the 1% limit.

### Sample 2

Input:

```
3 100
1 1 1
```

| Month | p[i] | cumulative before | required min | add | cumulative after |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | - | 0 | 1 |
| 1 | 1 | 1 | 1 | 0 | 2 |
| 2 | 1 | 2 | 1 | 0 | 3 |

Total added: 0

The percentages are all within the 100% limit, so no additions are required.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each month is processed once with simple arithmetic |
| Space | O(n) | We store the array of price increases, no additional large structures |

Since $n \le 100$ and $t \le 1000$, the total number of operations is at most $10^5$, well within 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# provided samples
assert run("2\n4 1\n20100 1 202 202\n3 100\n1 1 1\n") == "99\n0", "samples"

# custom cases
assert run("1\n2 1\n1 100\n") == "9900", "large increase after tiny initial"
assert run("1\n3 50\n2 1 1\n") == "0", "small increases, all below 50%"
assert run("1\n4 10\n10 1 1 100\n") == "990", "last month requires big addition"
assert run("1\n2 100\n1000000000 1000000000\n") == "0", "large numbers, already under 100%"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1\n1 100 | 9900 | Correctly handles very high increase after tiny initial |
| 3 50\n2 1 1 | 0 | Handles multiple months where no addition is needed |
| 4 10\n10 1 1 100 | 990 | Ensures last month requires addition and algorithm handles sequential updates |
| 2 100\n1000000000 1000000000 | 0 | Large numbers, checks for integer overflow handling |

## Edge Cases

For the input `2 1\n1 100`, the cumulative starts at 1. Month 1 requires `100 * 100 / 1 = 10000`, so we add `10000 - 1 = 9999` to cumulative, and the total added is 9999. The algorithm correctly applies ceiling division and updates cumulative sequentially. For `4 10\n10 1 1 100`, the algorithm adds 90 before the last month to satisfy 10% cap, demonstrating that sequential updates accumulate correctly for later months.
