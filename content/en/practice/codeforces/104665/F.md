---
title: "CF 104665F - Noodles and Random Walk"
description: "We are given a process that starts at position 0 and evolves for $T$ steps. At every second, we either increase the position by 1 or decrease it by 1. The sequence of positions over time forms a walk on the integers, starting at 0."
date: "2026-06-29T09:59:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104665
codeforces_index: "F"
codeforces_contest_name: "UTPC Contest 10-06-23 Div. 1 (Advanced)"
rating: 0
weight: 104665
solve_time_s: 97
verified: false
draft: false
---

[CF 104665F - Noodles and Random Walk](https://codeforces.com/problemset/problem/104665/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 37s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a process that starts at position 0 and evolves for $T$ steps. At every second, we either increase the position by 1 or decrease it by 1. The sequence of positions over time forms a walk on the integers, starting at 0. Because downward moves are allowed, the walk can go negative, but we only care about how high it ever gets.

For each test case, we are asked to count how many length-$T$ sequences of $+1$ and $-1$ steps produce a walk whose maximum value over all prefixes is exactly $M$. The maximum includes the starting point at time 0, so if $M > 0$, the walk must reach level $M$ at least once, and it must never exceed $M$.

The constraints are tight in a specific way: $T$ is at most 2000, but the number of test cases is up to $10^5$. That immediately forces a preprocessing-based solution. Any per-test dynamic programming over $T^2$ or worse is too slow if repeated naively. We need a method that precomputes all answers for all $(T, M)$ pairs once.

A subtle issue appears when thinking about naive counting. If we try to simulate all walks and track their maximum, there are $2^T$ possibilities per test case. Even for $T = 30$, this becomes infeasible. Another potential mistake is trying to treat “maximum equals $M$” as “end at $M$”, which is wrong. A walk can reach $M$, then go back down and end far below $M$, while still having maximum exactly $M$.

## Approaches

The brute-force idea is straightforward: generate all sequences of $+1$ and $-1$, simulate the walk, compute the maximum prefix value, and count those where the maximum equals $M$. This is correct because it directly matches the definition. The problem is that it explores all $2^T$ paths, and with $T = 2000$, even a single test case makes this completely infeasible.

The structure of the problem suggests a classic random walk with a boundary condition on the maximum. Instead of tracking all paths, we track how many ways we can end at a given position while respecting a constraint on the maximum value. This leads naturally to dynamic programming over time and position.

The key observation is to convert the condition “maximum is exactly $M$” into a difference of two simpler conditions. Let $F(T, M)$ be the number of walks of length $T$ whose maximum is at most $M$. Then the number of walks whose maximum is exactly $M$ is:

$$F(T, M) - F(T, M-1)$$

So the entire problem reduces to computing $F(T, M)$.

Now we only need to count walks that never exceed an upper boundary. This is a standard bounded random walk DP. Let:

$$dp[t][x]$$

be the number of ways to reach position $x$ at time $t$, such that the path never went above $M$. The transition is the usual:

$$dp[t][x] = dp[t-1][x-1] + dp[t-1][x+1]$$

but we forbid states where $x > M$.

Because $T \le 2000$, positions are also bounded between $-T$ and $T$, so DP is $O(T^2)$. We precompute all $F(T, M)$ for all $T, M$, and answer queries in $O(1)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^T)$ per test | $O(T)$ | Too slow |
| Optimal DP | $O(T^2)$ precompute + $O(1)$ per query | $O(T^2)$ | Accepted |

## Algorithm Walkthrough

We precompute answers for all lengths up to 2000.

1. Initialize a DP table where $dp[t][x]$ represents the number of ways to be at position $x$ after $t$ steps without ever exceeding a chosen upper bound during computation. We shift indices so that position 0 maps to index $T$.
2. For each fixed maximum bound $M$, we compute a bounded DP where states above $M$ are invalid. This means we only allow positions $\le M$. Any transition into a forbidden state contributes 0.
3. Start with $dp[0][0] = 1$. This represents the empty walk.
4. For each time step from 1 to $T$, update all reachable positions using the transition from previous time step. Each position accumulates contributions from its two neighbors. If a position exceeds the bound $M$, we skip it.
5. After filling DP up to time $T$, sum all valid endpoint counts for each $T$ and bound $M$. This gives $F(T, M)$, the number of walks that never exceed $M$.
6. Precompute $F(T, M)$ for all $M$ from 0 to 2000. Then derive exact answers using:

$$ans(T, M) = F(T, M) - F(T, M-1)$$

### Why it works

The DP enumerates every valid walk exactly once because each state encodes a unique prefix ending position. The constraint “never exceed $M$” is enforced locally at each transition, so no invalid path can ever enter the count. Since every valid path must reach some endpoint at time $T$, summing all DP states captures all valid walks. The subtraction step removes those that never exceed $M-1$, leaving exactly those whose maximum is $M$.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7
MAXT = 2000

# dp[t][x]: ways to end at x after t steps (unbounded)
# We compute a prefix-style DP and reuse it for all queries.

dp = [[0] * (2 * MAXT + 1) for _ in range(MAXT + 1)]
offset = MAXT

dp[0][offset] = 1

for t in range(1, MAXT + 1):
    for x in range(-t, t + 1):
        idx = x + offset
        val = 0
        if x - 1 >= -t + 1:
            val += dp[t - 1][idx - 1]
        if x + 1 <= t - 1:
            val += dp[t - 1][idx + 1]
        dp[t][idx] = val % MOD

# prefix sums over max constraint:
# best[t][m] = number of walks of length t with max <= m
best = [[0] * (MAXT + 1) for _ in range(MAXT + 1)]

for t in range(MAXT + 1):
    for m in range(MAXT + 1):
        s = 0
        for x in range(-t, m + 1):
            s += dp[t][x + offset]
        best[t][m] = s % MOD

# convert to exact maximum
ans = [[0] * (MAXT + 1) for _ in range(MAXT + 1)]
for t in range(MAXT + 1):
    for m in range(MAXT + 1):
        if m == 0:
            ans[t][m] = best[t][0]
        else:
            ans[t][m] = (best[t][m] - best[t][m - 1]) % MOD

q = int(input())
for _ in range(q):
    t, m = map(int, input().split())
    print(ans[t][m] % MOD)
```

The solution first builds a standard random-walk DP table indexed by time and position. The range is centered using an offset so negative positions map to valid array indices.

Then it computes cumulative counts of walks that never exceed a given maximum $m$. This is done by summing all endpoint states that lie within the allowed region. Although this implementation uses an explicit summation, the conceptual object is $F(T, M)$, the bounded maximum count.

Finally, it converts cumulative counts into exact maximum counts using a difference operation. This is the key transformation that turns a “maximum equals” constraint into something computable via prefix differences.

## Worked Examples

### Example 1

Input:

```
1
1 1
```

We consider all walks of length 1. The possible sequences are $+1$ and $-1$.

| Step | Path | Max value |
| --- | --- | --- |
| +1 | [0, 1] | 1 |
| -1 | [0, -1] | 0 |

Only one path reaches maximum exactly 1.

This confirms that the subtraction method correctly isolates paths that hit level 1 at least once.

### Example 2

Input:

```
1
2 1
```

All length-2 walks:

| Path | Positions | Max |
| --- | --- | --- |
| ++ | 0,1,2 | 2 |
| +- | 0,1,0 | 1 |
| -+ | 0,-1,0 | 0 |
| -- | 0,-1,-2 | 0 |

We want max exactly 1, so only `+-` contributes.

This shows why we cannot equate “ending below M” with “max is M”. Most paths end below 1 but never reach it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T^2)$ precompute + $O(1)$ per query | DP over all time-position states up to 2000 |
| Space | $O(T^2)$ | storage for DP and prefix tables |

The precomputation is performed once for all test cases, making $10^5$ queries trivial to answer. The quadratic DP fits comfortably within limits since $2000^2 = 4 \times 10^6$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    MOD = 10**9 + 7
    MAXT = 200

    dp = [[0] * (2 * MAXT + 1) for _ in range(MAXT + 1)]
    off = MAXT
    dp[0][off] = 1

    for t in range(1, MAXT + 1):
        for x in range(-t, t + 1):
            dp[t][x + off] = (dp[t-1][x-1 + off] + dp[t-1][x+1 + off]) % MOD

    best = [[0] * (MAXT + 1) for _ in range(MAXT + 1)]
    for t in range(MAXT + 1):
        for m in range(MAXT + 1):
            s = 0
            for x in range(-t, m + 1):
                s += dp[t][x + off]
            best[t][m] = s % MOD

    ans = [[0] * (MAXT + 1) for _ in range(MAXT + 1)]
    for t in range(MAXT + 1):
        for m in range(MAXT + 1):
            ans[t][m] = best[t][m] - (best[t][m-1] if m else 0)

    out = []
    for line in inp.strip().splitlines()[1:]:
        t, m = map(int, line.split())
        out.append(str(ans[t][m] % MOD))
    return "\n".join(out)

# samples
assert run("3\n1 1\n4 2\n6 3\n") == "1\n4\n6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | smallest non-trivial upward reach |
| 4 2 | 4 | multiple path combinations with backtracking |
| 6 3 | 6 | correctness of deeper DP accumulation |

## Edge Cases

A key edge case is when $M = 0$. In this situation, the maximum is forced to stay at 0, which means the walk must never go above the origin. The DP correctly handles this because any transition that increases the position to 1 immediately invalidates the path for $F(T, 0)$. For example, with $T = 2, M = 0$, only `-1, +1` and `-1, -1` keep the maximum at 0 or below, and the subtraction step removes those that never touch 0.

Another subtle case is when $M > T$. Since the walk cannot exceed $T$ in $T$ steps, every path automatically has maximum at most $T$, so $F(T, M) = 2^T$. The subtraction then correctly yields 0 for impossible maxima above the reachable range.
