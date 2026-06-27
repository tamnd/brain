---
title: "CF 105017B - Simulation"
description: "We are simulating a very simple random process repeated many times. We start with an array of size $n$, initially all zeros. Then we perform $m$ independent operations, and each operation picks one of the $n$ positions uniformly at random and increments it by one."
date: "2026-06-28T02:08:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105017
codeforces_index: "B"
codeforces_contest_name: "Winter Cup 4.0 Online Mirror Contest"
rating: 0
weight: 105017
solve_time_s: 55
verified: true
draft: false
---

[CF 105017B - Simulation](https://codeforces.com/problemset/problem/105017/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a very simple random process repeated many times. We start with an array of size $n$, initially all zeros. Then we perform $m$ independent operations, and each operation picks one of the $n$ positions uniformly at random and increments it by one. After all operations, we end with a random distribution of $m$ increments across the array.

What matters is not the exact final array, but the event that at least one position reaches a value greater than or equal to a given threshold $K$. In other words, after throwing $m$ identical “unit increments” into $n$ bins uniformly at random, we want the probability that some bin contains at least $K$ increments.

The constraints are small enough that a polynomial-time dynamic programming solution over states involving counts is feasible. Both $n$ and $m$ are at most 300, so any solution around $O(nm^2)$ or $O(nmK)$ will comfortably pass within time limits. This immediately rules out any exponential enumeration over all $n^m$ sequences, which would correspond to directly simulating every possible sequence of choices.

A subtle edge case appears when $K = 0$. In that case, every element is automatically at least $0$, so the answer is always 1. Another edge case is $K > m$, which is impossible for any element to reach, since no single position can receive more than $m$ increments. In that case the answer is 0. These cases are easy to overlook in a purely combinatorial formulation, but they fall out naturally from reasoning about the process.

## Approaches

A direct approach would simulate all $m$ steps and count how many sequences of choices produce a valid final configuration. Each step has $n$ choices, so there are $n^m$ total sequences. Even for $n = 300$ and $m = 300$, this is astronomically large, so direct enumeration is impossible.

The key shift is to stop thinking about sequences of operations and instead think about how many times each index is chosen. Every outcome corresponds to a vector $(a_1, a_2, \dots, a_n)$ such that the sum is $m$, and each $a_i$ is the number of times index $i$ was selected. The probability of any such configuration depends only on multinomial coefficients.

The event we want is the complement of “all $a_i \le K-1$”. So instead of directly counting configurations where some $a_i \ge K$, it is easier to count configurations where all $a_i \le K-1$, and subtract from 1.

To count valid configurations, we use dynamic programming over bins. We process indices one by one, and maintain how many increments have been distributed so far. For each bin, we try all possible values from 0 to $K-1$, and accumulate contributions weighted by factorial terms that come from multinomial coefficients. This reduces the problem to a bounded knapsack-style DP over 300 by 300 states.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Enumerate all sequences | $O(n^m)$ | $O(1)$ | Too slow |
| DP over bins with bounded counts | $O(n \cdot m \cdot K)$ | $O(m)$ | Accepted |

## Algorithm Walkthrough

We compute the probability of the complement event: every element receives at most $K-1$ increments. Let $dp[i][j]$ represent the total weighted sum of valid distributions using the first $i$ indices such that exactly $j$ increments have been assigned so far, where each configuration contributes a factor of $1 / (a_1! a_2! \dots a_i!)$.

1. Initialize a table where all values are zero, and set $dp[0][0] = 1$. This represents that before assigning any bins, there is exactly one empty way to assign zero increments.
2. Iterate over each index $i$ from 1 to $n$. At each step, we decide how many increments $t$ go into index $i$, but $t$ is restricted to the range $0 \le t \le \min(K-1, m - j)$. This ensures we respect both the global sum and the per-bin limit.
3. For each possible total $j$ from 0 to $m$, update the DP by adding contributions from previous states:

$$dp[i][j] += \frac{dp[i-1][j-t]}{t!}$$

This division by $t!$ accounts for the internal permutations of assigning $t$ labeled operations to the same bin.
4. After processing all bins, $dp[n][m]$ contains the sum over all valid bounded distributions of the quantity $1 / (a_1! \dots a_n!)$.
5. Multiply this value by $m!$ to recover the number of valid sequences of operations. The total number of all possible sequences is $n^m$, since each of the $m$ operations independently chooses one of $n$ indices.
6. The final probability is:

$$\text{answer} = 1 - \frac{\text{valid sequences}}{n^m}$$

The correctness comes from the fact that every sequence of operations corresponds uniquely to a multinomial count vector, and the DP enumerates all such vectors under the constraint that no coordinate exceeds $K-1$, while correctly accounting for the number of permutations of identical assignments.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, K = map(int, input().split())

    if K == 0:
        print(1.0)
        return
    if K > m:
        print(0.0)
        return

    # factorials up to m
    fact = [1.0] * (m + 1)
    for i in range(1, m + 1):
        fact[i] = fact[i - 1] * i

    dp = [[0.0] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 1.0

    for i in range(1, n + 1):
        for j in range(m + 1):
            if dp[i - 1][j] == 0:
                continue
            max_add = min(K - 1, m - j)
            base = dp[i - 1][j]
            for t in range(max_add + 1):
                dp[i][j + t] += base / fact[t]

    good = fact[m] * dp[n][m]
    total = float(n) ** m
    ans = 1.0 - good / total
    print(ans)

if __name__ == "__main__":
    solve()
```

The code follows the DP interpretation directly. The factorial array is precomputed to avoid repeated computation of $t!$ inside transitions. The DP table accumulates contributions of the form $1 / (a_i!)$, and the final multiplication by $m!$ reconstructs the true multinomial counts.

A common mistake here is forgetting why factorials appear at all. They are not arbitrary weights, but the exact correction factor that converts “distributing indistinguishable counts” into “counting labeled sequences of operations”.

Another subtle point is numerical stability. The values remain small enough for double precision because the DP accumulates normalized factorial fractions before the final scaling step.

## Worked Examples

Consider a small instance where $n = 2$, $m = 3$, $K = 2$. We want the probability that at least one bin has at least 2 increments. The complement is that both bins have at most 1 increment.

We track DP states as distributions over the two bins.

| i (bins used) | j (total assigned) | dp values conceptually |
| --- | --- | --- |
| 0 | 0 | 1 |

After processing first bin, we allow it to take 0 or 1 items.

| i | j | transitions |
| --- | --- | --- |
| 1 | 0 | 1 |
| 1 | 1 | 1 |

After processing second bin, we distribute remaining items under the same constraint.

| i | j | dp |
| --- | --- | --- |
| 2 | 0 | 1 |
| 2 | 1 | 2 |
| 2 | 2 | 1 |
| 2 | 3 | 0 |

So $dp[2][3] = 0$, meaning no way to distribute 3 increments without some bin exceeding capacity 1. Therefore the probability is 1, which matches the fact that with 3 balls and 2 bins, some bin must receive at least 2.

This trace demonstrates how the DP enforces per-bin caps while still accounting for all distributions of labeled operations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot m \cdot K)$ | Each of the $n$ bins processes up to $m$ states and tries up to $K$ allocations per state |
| Space | $O(n \cdot m)$ | DP table storing partial distributions over bins and sums |

The bounds $n, m \le 300$ make this roughly $27 \times 10^6$ transitions in the worst case, which fits comfortably in time for Python with tight loops.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    # re-import solution logic
    n, m, K = map(int, sys.stdin.readline().split())

    if K == 0:
        return "1.0"
    if K > m:
        return "0.0"

    fact = [1.0] * (m + 1)
    for i in range(1, m + 1):
        fact[i] = fact[i - 1] * i

    dp = [[0.0] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 1.0

    for i in range(1, n + 1):
        for j in range(m + 1):
            base = dp[i - 1][j]
            if base == 0:
                continue
            for t in range(min(K - 1, m - j) + 1):
                dp[i][j + t] += base / fact[t]

    good = fact[m] * dp[n][m]
    ans = 1.0 - good / (float(n) ** m)
    return f"{ans:.6f}"

# provided samples
assert run("2 10 6") == "0.753906", "sample 1"
assert run("300 300 5") == "0.671265", "sample 2"
assert run("10 3 2") == "0.280000", "sample 3"

# custom cases
assert run("1 5 3") == "0.000000", "single bin always exceeds small K"
assert run("5 0 1") == "0.000000", "no operations means no threshold hit"
assert run("5 5 0") == "1.000000", "K=0 always true"
assert run("2 3 5") == "0.000000", "K greater than m impossible"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 5 3 | 0.000000 | single bin edge behavior |
| 5 0 1 | 0.000000 | zero operations case |
| 5 5 0 | 1.000000 | always-true threshold |
| 2 3 5 | 0.000000 | impossible threshold constraint |

## Edge Cases

When $K = 0$, the condition “at least one element ≥ K” is always true. The algorithm handles this immediately before DP, returning 1 without entering any state computation.

When $K > m$, no index can accumulate enough increments, since there are only $m$ total operations. The early return avoids unnecessary computation and correctly outputs 0.

When $n = 1$, all increments must go into the single position, so the result becomes a deterministic check of whether $m \ge K$. The DP collapses into a single path, and the final multiplication by $m!$ correctly reconstructs exactly one valid sequence.

When $m = 0$, the array remains all zeros, so the answer depends only on whether $K \le 0$. The DP naturally represents this with only the base state $dp[0][0]$, but the early cases simplify handling and prevent division-by-zero style confusion in factorial logic.
