---
title: "CF 105977G - \u7092\u80a1\u9ad8\u624b"
description: "The problem gives a sequence of stock prices over $n$ days, but the prices are encoded in logarithmic form. On day $i$, the actual price is $e^{ai}$, where $ai$ is a positive integer."
date: "2026-06-22T16:28:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105977
codeforces_index: "G"
codeforces_contest_name: "2025 National Invitational of CCPC (Fujian), The 12th Fujian Collegiate Programming Contest"
rating: 0
weight: 105977
solve_time_s: 58
verified: true
draft: false
---

[CF 105977G - \u7092\u80a1\u9ad8\u624b](https://codeforces.com/problemset/problem/105977/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem gives a sequence of stock prices over $n$ days, but the prices are encoded in logarithmic form. On day $i$, the actual price is $e^{a_i}$, where $a_i$ is a positive integer. This transforms multiplicative gains and losses in the real market into additive differences in the exponent space.

Each query describes a time interval $[s, t]$. On day $s$, we receive a loan of $e^k$ units of money. We are allowed to freely trade the stock during days $s$ through $t$, buying fractional shares and performing unlimited transactions. At the end of day $t$, all holdings are liquidated and the loan is repaid. We want the maximum possible final wealth after repayment, expressed again in exponential form $e^w$, and the task is to output $w$.

So the core task per query is: starting with cash $e^k$, maximize the final amount after arbitrage trading in a known price sequence, then output the resulting exponent.

The key transformation is that since everything is exponential, working in log space turns multiplicative gains into additive gains. A transaction from day $i$ to day $j$ gives a gain factor $e^{a_j - a_i}$, so in exponent space it contributes $a_j - a_i$.

The constraints are large: up to $10^5$ days and $10^5$ queries. That immediately rules out any solution that recomputes optimal trading independently per query in linear time, since that would lead to $10^{10}$ operations.

A naive approach would treat each query independently and simulate optimal trading inside $[s, t]$. However, even finding the optimal strategy for one interval requires scanning the segment multiple times if done carefully, and doing that for all queries is infeasible.

A more subtle failure mode comes from thinking that the answer depends only on the minimum and maximum price in the interval. That is incorrect because multiple alternating increases matter: the optimal strategy is not necessarily one buy and one sell, but a sequence of profitable moves.

## Approaches

The first step is to understand what “optimal trading with unlimited transactions and fractional shares” means in log space. Suppose we buy at day $i$ and sell at day $j > i$. The gain in exponent is $a_j - a_i$. If we perform multiple trades, say we split into segments $i_1 < i_2 < \dots < i_k$, the total gain becomes

$$(a_{i_2} - a_{i_1}) + (a_{i_3} - a_{i_2}) + \dots + (a_{i_k} - a_{i_{k-1}}),$$

which telescopes to $a_{i_k} - a_{i_1}$ if we force strictly alternating buy/sell. But the real constraint is that we are not forced to alternate strictly; we can only gain when moving from a lower price to a higher one across chosen boundaries.

The classical simplification emerges when we interpret trading as accumulating all positive upward differences between consecutive increasing segments. If the sequence goes up, we capture that increase; if it goes down, we ignore it and wait for a better entry point. This reduces the optimal gain over $[s, t]$ to the sum of all positive adjacent differences:

$$\sum_{i=s}^{t-1} \max(0, a_{i+1} - a_i).$$

Then the final answer is simply:

$$w = k + \sum_{i=s}^{t-1} \max(0, a_{i+1} - a_i).$$

The brute force approach evaluates this sum for each query independently, scanning the interval. That is $O(n)$ per query, which becomes $O(nm)$ in total and cannot pass.

The key observation is that the expression depends only on adjacent differences. Define $d_i = \max(0, a_{i+1} - a_i)$. Then each query reduces to a range sum query on the array $d$. With prefix sums, we can answer each query in constant time after preprocessing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nm)$ | $O(1)$ | Too slow |
| Prefix Sum on Differences | $O(n + m)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We transform the price sequence into a difference contribution array and then answer range queries over it.

1. Construct an auxiliary array $d$ of length $n-1$, where each element is $d_i = \max(0, a_{i+1} - a_i)$. This isolates only profitable upward moves and discards downward moves, since losses do not contribute under optimal trading.
2. Build a prefix sum array $p$, where $p[i]$ stores the sum of $d_1$ through $d_i$. This allows us to compute any interval sum in constant time.
3. For each query $[s, t]$, compute the total gain inside the interval as $p[t-1] - p[s-1]$, because only transitions fully inside the interval matter.
4. Add the base exponent $k$ to this gain, producing the final exponent $w$.
5. Output $w$.

The reason the difference array is sufficient is that every profitable trading strategy can be rearranged so that all gains correspond exactly to upward steps without changing the net result. Any sequence of trades collapses into collecting local increases.

### Why it works

The invariant is that at any point in the interval, the best possible strategy maintains the property that we are either holding cash or holding stock bought at the most recent local minimum. Every time the sequence increases, that increase can be fully captured without affecting future decisions. Every decrease is ignored because entering there cannot improve any later exit compared to waiting for a lower price.

This reduces all optimal strategies to independent contributions of local monotone segments, making the sum of positive adjacent differences both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
a = list(map(int, input().split()))
k = int(input())

n = len(a)
d = [0] * (n - 1)

for i in range(n - 1):
    if a[i + 1] > a[i]:
        d[i] = a[i + 1] - a[i]

prefix = [0] * (n)
for i in range(n - 1):
    prefix[i + 1] = prefix[i] + d[i]

out = []
for _ in range(m):
    s, t = map(int, input().split())
    gain = prefix[t - 1] - prefix[s - 1]
    out.append(str(k + gain))

print("\n".join(out))
```

The code first constructs the gain array by scanning adjacent differences once. The prefix array is shifted by one index so that range queries align cleanly with 1-indexed input.

Each query converts directly into a prefix difference. The addition of $k$ is done at query time to avoid repeated arithmetic during preprocessing.

A common pitfall is off-by-one indexing: the gain array has size $n-1$, but queries refer to days. The mapping is that trading opportunities lie between day $i$ and $i+1$, so query $[s, t]$ covers indices $[s, t-1]$ in the difference array.

## Worked Examples

Consider the sample behavior described in the statement.

For the first interval $[2, 4]$ with prices $[2, 4, 5]$, the differences are $+2, +1$. Prefix sums give cumulative gain $3$. Starting from $k = 2$, final exponent becomes $5$.

| Step | Interval | Difference sum | Prefix result | Final w |
| --- | --- | --- | --- | --- |
| 1 | [2,4] | 2 + 1 = 3 | 3 | 5 |

This shows that multiple consecutive increases are accumulated rather than treated as a single buy-sell operation.

For the second interval $[3, 6]$ with prices $[4, 5, 3, 6]$, differences are $+1, 0, +3$, summing to $4$. Adding base $k=2$ yields $6$.

| Step | Interval | Difference sum | Prefix result | Final w |
| --- | --- | --- | --- | --- |
| 1 | [3,6] | 1 + 0 + 3 = 4 | 4 | 6 |

This demonstrates that the algorithm correctly skips downward transitions and accumulates only profitable segments.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + m)$ | One pass builds differences and prefix sums, each query answered in O(1) |
| Space | $O(n)$ | Stores the difference and prefix arrays |

The solution comfortably fits within constraints since both $n$ and $m$ are $10^5$, and all operations are linear or constant time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    k = int(input())

    n = len(a)
    d = [0] * (n - 1)
    for i in range(n - 1):
        if a[i + 1] > a[i]:
            d[i] = a[i + 1] - a[i]

    prefix = [0] * (n)
    for i in range(n - 1):
        prefix[i + 1] = prefix[i] + d[i]

    out = []
    for _ in range(m):
        s, t = map(int, input().split())
        out.append(str(k + prefix[t - 1] - prefix[s - 1]))

    return "\n".join(out)

# minimal size
assert run("1 1\n5\n3\n1 1") == "3"

# strictly decreasing
assert run("5 1\n5 4 3 2 1\n10\n1 5") == "10"

# strictly increasing
assert run("5 1\n1 2 3 4 5\n10\n1 5") == "14"

# alternating
assert run("4 1\n1 3 2 4\n0\n1 4") == "4"

# sample-style
assert run("6 2\n3 2 4 5 3 6\n2\n2 4\n3 6") == "5\n6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 3 | single-day query baseline |
| decreasing sequence | 10 | no profitable trades |
| increasing sequence | 14 | full accumulation of gains |
| alternating | 4 | skipping drops correctly |
| sample-style | 5,6 | multi-query correctness |

## Edge Cases

A subtle case is when the interval starts or ends inside a rising segment. For example, in a sequence like $1, 5, 10, 2, 3$, a query $[2, 4]$ only includes $5, 10, 2$. The algorithm computes difference contributions $+5$ inside the interval and ignores the drop from $10$ to $2$, since it is not profitable. The prefix subtraction correctly isolates only the internal boundary $5 \to 10$.

Another case is a single-day query $[i, i]$. There are no transitions, so the difference sum is zero and the answer is exactly $k$. The prefix formula naturally yields zero because $p[i-1] - p[i-1] = 0$, preventing any accidental out-of-bounds or negative indexing effects when implemented carefully.
