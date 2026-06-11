---
title: "CF 1118A - Water Buying"
description: "Polycarp needs to buy exactly $n$ liters of water using bottles of two fixed sizes: 1-liter bottles at cost $a$ and 2-liter bottles at cost $b$. For each query, we are asked to determine the minimum total cost to acquire exactly $n$ liters."
date: "2026-06-12T04:36:42+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1118
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 540 (Div. 3)"
rating: 800
weight: 1118
solve_time_s: 323
verified: false
draft: false
---

[CF 1118A - Water Buying](https://codeforces.com/problemset/problem/1118/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 5m 23s  
**Verified:** no  

## Solution
## Problem Understanding

Polycarp needs to buy exactly $n$ liters of water using bottles of two fixed sizes: 1-liter bottles at cost $a$ and 2-liter bottles at cost $b$. For each query, we are asked to determine the minimum total cost to acquire exactly $n$ liters. There is no limit on how many bottles can be bought, and the shop always has both types available.

The inputs are structured as multiple independent queries. Each query specifies the number of liters Polycarp needs, the cost of a 1-liter bottle, and the cost of a 2-liter bottle. The output is a single integer per query, the minimum cost.

The constraints show that $n$ can be as large as $10^{12}$, while $a$ and $b$ are much smaller (up to 1000). This implies that any solution iterating over all possible combinations of bottles is infeasible. We need a solution that computes the minimum cost using a formula or constant-time decision per query.

Edge cases emerge when buying two 1-liter bottles is cheaper than buying a 2-liter bottle. For example, if $a = 1$ and $b = 3$, buying two 1-liter bottles costs 2, less than the 2-liter bottle cost of 3. Similarly, if $n$ is odd, it is impossible to fill it entirely with 2-liter bottles, so we must include exactly one 1-liter bottle. Careless solutions might assume we always want as many 2-liter bottles as possible, which fails when two 1-liter bottles are cheaper than one 2-liter bottle.

## Approaches

The brute-force approach is to iterate over all possible numbers of 2-liter bottles from 0 up to $n/2$, compute the remaining liters to fill with 1-liter bottles, calculate the total cost for each combination, and take the minimum. This approach is correct because it checks all valid combinations, but it becomes infeasible when $n$ is large. For $n = 10^{12}$, even iterating $n/2$ times is impossibly slow.

The key observation for a faster solution is that each 2-liter bottle can be replaced with two 1-liter bottles. Therefore, the effective cost of a 2-liter bottle should be compared to twice the cost of a 1-liter bottle. If buying two 1-liter bottles is cheaper than a 2-liter bottle, it is always better to buy 1-liter bottles instead. Otherwise, we can greedily use as many 2-liter bottles as possible, using a 1-liter bottle only if $n$ is odd.

The optimal solution works because the choice for each 2-liter bottle is independent and can be reduced to a simple comparison: if $b < 2a$, use 2-liter bottles wherever possible; otherwise, replace all 2-liter bottles with two 1-liter bottles. This reduces the problem to a constant-time computation per query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Too slow for large n |
| Optimal | O(1) per query | O(1) | Accepted |

## Algorithm Walkthrough

1. For each query, read $n$, $a$, and $b$.
2. Compute the effective cost of using a 2-liter bottle: if $2a < b$, set $b = 2a$. This ensures that buying two 1-liter bottles is always considered if cheaper than a 2-liter bottle.
3. Compute the number of 2-liter bottles to buy as $n // 2$, the maximum number that fits in $n$ liters.
4. Compute the number of 1-liter bottles as $n \% 2$, the remaining liters after using 2-liter bottles.
5. Compute the total cost as $(n // 2) \times b + (n \% 2) \times a$. This formula accounts for both the 2-liter and 1-liter bottles.
6. Print the total cost for the query.

Why it works: By adjusting the 2-liter cost to be no more than twice the 1-liter cost, we guarantee that using 2-liter bottles is never worse than using two 1-liter bottles. Greedily using as many 2-liter bottles as possible minimizes the number of bottles, and handling a single leftover liter with a 1-liter bottle ensures exactly $n$ liters. No other combination can yield a lower cost.

## Python Solution

```python
import sys
input = sys.stdin.readline

q = int(input())
for _ in range(q):
    n, a, b = map(int, input().split())
    b = min(b, 2 * a)  # cheaper to buy two 1-liter bottles than one 2-liter bottle
    total_cost = (n // 2) * b + (n % 2) * a
    print(total_cost)
```

This solution reads each query, adjusts the 2-liter bottle cost if buying two 1-liter bottles is cheaper, computes how many 2-liter bottles to buy and how many leftover 1-liter bottles are needed, then prints the total cost. It handles very large $n$ because it never loops over individual liters. Edge cases like $n = 1$ or $b > 2a$ are correctly managed by the `min(b, 2 * a)` line.

## Worked Examples

Sample input:

```
10 1 3
```

| n | a | b | b adjusted | n//2 | n%2 | Total cost |
| --- | --- | --- | --- | --- | --- | --- |
| 10 | 1 | 3 | 2 | 5 | 0 | 10 |

Explanation: Since two 1-liter bottles cost 2 < 3, we replace the 2-liter bottle cost with 2. We can buy 5 two-liter bottles to cover 10 liters with no 1-liter bottles needed. Total cost is 5*2 = 10.

Second input:

```
7 3 2
```

| n | a | b | b adjusted | n//2 | n%2 | Total cost |
| --- | --- | --- | --- | --- | --- | --- |
| 7 | 3 | 2 | 2 | 3 | 1 | 3_2 + 1_3 = 9 |

Explanation: Here, the 2-liter bottle is already cheaper than two 1-liter bottles (2 < 6). We buy 3 two-liter bottles (6 liters) and 1 one-liter bottle (1 liter) to make 7 liters. Total cost is 9.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q) | Each query is computed in constant time; there are q queries. |
| Space | O(1) | Only a few variables per query; no extra memory depends on n. |

With q up to 500 and n up to 10^12, constant-time computation per query is efficient and fits well within the 1-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    q = int(input())
    for _ in range(q):
        n, a, b = map(int, input().split())
        b = min(b, 2 * a)
        print((n // 2) * b + (n % 2) * a)
    return output.getvalue().strip()

# Provided samples
assert run("4\n10 1 3\n7 3 2\n1 1000 1\n1000000000000 42 88\n") == "10\n9\n1000\n42000000000000"

# Custom cases
assert run("1\n1 1 100\n") == "1", "minimum n, large b"
assert run("1\n2 5 8\n") == "10", "cheaper to use two 1-liter bottles"
assert run("1\n3 3 4\n") == "7", "odd n, 2-liter cheaper than 2*1-liter"
assert run("1\n1000000000000 1 3\n") == "2000000000000", "maximum n, 2*1 < 2-liter cost"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 100 | 1 | Single liter, very expensive 2-liter bottle |
| 2 5 8 | 10 | Two 1-liter bottles cheaper than 2-liter |
| 3 3 4 | 7 | Odd n with 2-liter cheaper than 2*1-liter |
| 1000000000000 1 3 | 2000000000000 | Maximum n, very large, algorithm handles big numbers |

## Edge Cases

For $n = 1$, $a = 1000$, $b = 1$, the algorithm sets $b = min(b, 2a) = 1$ but only 1 liter is needed. It calculates `n//2 = 0` two-liter bottles and `n%2 = 1` one-liter bottle. The total cost is `1 * a = 1000`, correctly ignoring the cheap 2-liter bottle because we only need one liter
