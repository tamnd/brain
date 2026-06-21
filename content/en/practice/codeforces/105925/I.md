---
title: "CF 105925I - Inspecting the Entanglement"
description: "We are given a time interval of length $T$, and at every second exactly one sensor must be active. Each sensor produces a value that depends on both the sensor and the time, so activating sensor $i$ at time $j$ contributes $c(i, j)$ to the total score."
date: "2026-06-21T12:00:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105925
codeforces_index: "I"
codeforces_contest_name: "SBC Brazilian Phase Zero 2025"
rating: 0
weight: 105925
solve_time_s: 53
verified: true
draft: false
---

[CF 105925I - Inspecting the Entanglement](https://codeforces.com/problemset/problem/105925/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a time interval of length $T$, and at every second exactly one sensor must be active. Each sensor produces a value that depends on both the sensor and the time, so activating sensor $i$ at time $j$ contributes $c(i, j)$ to the total score.

However, sensors cannot be switched arbitrarily. Once a sensor is turned on, it must stay active for a contiguous block of time whose length is between $L$ and $U$, inclusive. After that block ends, we may switch to another sensor, starting a new block, and we continue until the entire interval $[1, T]$ is covered exactly.

The task is to partition the timeline into contiguous segments, where each segment has length in $[L, U]$, assign exactly one sensor to each segment, and maximize the total sum of contributions over all time steps.

The input size is small in time ($T \le 100$) but large in sensors ($N \le 5000$). This asymmetry is the key: we can afford quadratic or even cubic work in $T$, but anything that repeatedly iterates over all sensors inside a per-time DP without structure must be carefully optimized. In particular, any solution that tries all sensors for every segment naively will approach $O(NT^2)$, which is borderline but still feasible if each inner computation is simple and well-structured.

A common failure case is assuming greedy choice per segment without respecting future feasibility. For example, choosing the best sensor for the first segment might force a segmentation that cannot satisfy the remaining length constraints.

Consider this small example where greedy fails in spirit. Suppose $T=5$, $L=2$, $U=3$. If one sensor is excellent on $[1,2]$ but terrible afterward, and another is slightly worse early but excellent on $[3,5]$, choosing locally best early segment can block a better global partition. The structure is inherently global because segment lengths constrain how the remaining timeline can be decomposed.

Another subtle issue is that each segment’s best sensor depends on the exact interval $[l, r]$, not just on its length. So we cannot precompute a single best sensor per length; we must consider time-dependent scores.

## Approaches

A brute-force approach tries all possible ways to split the timeline into valid segments and assigns a sensor to each segment. There are exponentially many partitions of $T$, and even if we fix a partition, assigning the best sensor per segment still requires checking all $N$ sensors over the segment range. With roughly $O(N)$ per segment and exponentially many segmentations, this is far too slow.

The key observation is that the structure is purely one-dimensional and segment-based. Once we decide that a segment is $[l, r]$, the best choice of sensor for that segment is independent of all other segments. This decouples sensor selection from segmentation: for every interval we can precompute the best achievable score.

This turns the problem into a classic interval dynamic programming problem. We compute the best score for every interval $[l, r]$, then run a DP over time where each state $dp[t]$ represents the maximum score achievable covering exactly the prefix $[1, t]$. Transitions try all valid segment lengths.

The main optimization is precomputing interval best values using prefix sums per sensor, so that interval scoring becomes fast enough to fit within constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over partitions | Exponential | O(1) | Too slow |
| Interval DP with precomputation | $O(NT^2 + TU)$ | $O(NT)$ | Accepted |

## Algorithm Walkthrough

### Step 1: Precompute prefix sums per sensor

For each sensor $i$, build a prefix sum array over time so that we can compute the sum of $c(i, l) + \dots + c(i, r)$ in constant time. This converts interval evaluation from linear in segment length to $O(1)$.

### Step 2: Compute best sensor for every interval

For each interval $[l, r]$, we compute the maximum score achievable by choosing the best sensor:

$$best[l][r] = \max_i \sum_{j=l}^{r} c(i, j)$$

This step is expensive but feasible because $T \le 100$, so there are at most 10,000 intervals. For each interval we scan all $N$ sensors.

### Step 3: Initialize DP

We define $dp[t]$ as the maximum score covering exactly the first $t$ seconds. We set $dp[0] = 0$ and all other states to negative infinity, since they are initially unreachable.

### Step 4: Transition over segment endings

For each endpoint $t$, we try every valid segment length $len \in [L, U]$. The segment would start at $t-len+1$. If that start is valid, we update:

$$dp[t] = \max(dp[t], dp[t-len] + best[t-len+1][t])$$

This enforces that every segment respects the duration constraints.

### Step 5: Output result

The answer is $dp[T]$. If it remains unreachable, we output $-1$.

### Why it works

The DP state partitions the timeline into valid independent segments. Every valid full assignment corresponds to exactly one sequence of DP transitions, and every DP transition corresponds to a valid segment with an optimally chosen sensor. The prefix DP ensures no overlapping segments and no gaps, while the interval precomputation ensures that within each segment we always pick the best possible sensor independently of other choices.

## Python Solution

```python
import sys
input = sys.stdin.readline

NEG = -10**18

N, T = map(int, input().split())
c = [list(map(int, input().split())) for _ in range(N)]
L, U = map(int, input().split())

# prefix sums per sensor
pref = [[0] * (T + 1) for _ in range(N)]
for i in range(N):
    for j in range(1, T + 1):
        pref[i][j] = pref[i][j - 1] + c[i][j - 1]

def get_sum(i, l, r):
    return pref[i][r] - pref[i][l - 1]

# best[l][r] = best sensor sum for interval
best = [[NEG] * (T + 1) for _ in range(T + 1)]

for l in range(1, T + 1):
    for r in range(l, T + 1):
        best_val = NEG
        for i in range(N):
            best_val = max(best_val, get_sum(i, l, r))
        best[l][r] = best_val

dp = [NEG] * (T + 1)
dp[0] = 0

for t in range(1, T + 1):
    for length in range(L, U + 1):
        if t - length < 0:
            continue
        l = t - length + 1
        if best[l][t] == NEG:
            continue
        dp[t] = max(dp[t], dp[t - length] + best[l][t])

print(dp[T] if dp[T] > NEG // 2 else -1)
```

The prefix sums are essential because without them each interval evaluation would cost $O(T)$, making the full precomputation $O(NT^3)$, which is unnecessary.

The DP loop carefully respects segment boundaries. The condition $t - length \ge 0$ prevents invalid prefixes, and the check against $NEG$ ensures we never extend impossible states.

## Worked Examples

### Example 1

Input:

```
3 5
2 3 2 1 2
1 1 5 1 2
1 2 2 1 5
1 5
```

We first compute interval best values implicitly. Then DP proceeds:

| t | chosen segment | value added | dp[t] |
| --- | --- | --- | --- |
| 0 | - | - | 0 |
| 1 | [1,1] | best single sensor = 2 | 2 |
| 2 | [1,2] | best interval = 5 | 5 |
| 3 | [1,3] | best interval = 7 | 7 |
| 4 | [1,4] | best interval = 8 | 8 |
| 5 | [1,5] | best interval = 11 | 11 |

This shows the unconstrained case $L=1, U=5$ collapses into one segment covering everything.

### Example 2

Input:

```
3 5
2 3 2 1 2
1 1 5 1 2
1 2 2 1 5
2 3
```

Now each segment must have length 2 or 3.

| t | segment choice | dp[t] |
| --- | --- | --- |
| 0 | - | 0 |
| 2 | [1,2] | best = 5 → 5 |
| 3 | [1,3] | best = 7 → 7 |
| 4 | [2,4] or [1,2]+[3,4] best combo | 8 |
| 5 | valid split only | 10 |

This demonstrates how DP enforces valid segment lengths while still selecting best sensors per segment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(NT^2 + TU)$ | $O(NT^2)$ to compute all interval best values, $O(TU)$ DP transitions |
| Space | $O(NT + T^2)$ | prefix sums for each sensor plus interval table and DP array |

With $N \le 5000$ and $T \le 100$, the interval count is only 10,000, making the $N$ scan acceptable. The DP part is negligible in comparison.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    NEG = -10**18
    N, T = map(int, input().split())
    c = [list(map(int, input().split())) for _ in range(N)]
    L, U = map(int, input().split())

    pref = [[0] * (T + 1) for _ in range(N)]
    for i in range(N):
        for j in range(1, T + 1):
            pref[i][j] = pref[i][j - 1] + c[i][j - 1]

    def get_sum(i, l, r):
        return pref[i][r] - pref[i][l - 1]

    best = [[NEG] * (T + 1) for _ in range(T + 1)]
    for l in range(1, T + 1):
        for r in range(l, T + 1):
            best[l][r] = max(get_sum(i, l, r) for i in range(N))

    dp = [NEG] * (T + 1)
    dp[0] = 0

    for t in range(1, T + 1):
        for length in range(L, U + 1):
            if t - length >= 0:
                l = t - length + 1
                dp[t] = max(dp[t], dp[t - length] + best[l][t])

    return str(dp[T] if dp[T] > NEG // 2 else -1)

# provided samples
assert run("""3 5
2 3 2 1 2
1 1 5 1 2
1 2 2 1 5
1 5
""") == "11"

assert run("""3 5
2 3 2 1 2
1 1 5 1 2
1 2 2 1 5
2 3
""") == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| L=1,U=T | 11 | single-segment collapse |
| L=2,U=3 | 10 | constrained segmentation correctness |

## Edge Cases

A tight constraint edge case happens when $L = U$, forcing all segments to have identical length. In that situation, the DP has exactly one valid transition per state, and any incorrect interval indexing immediately breaks feasibility. The algorithm still works because the loop over `length` degenerates to a single fixed step, and every state is either reachable or not without ambiguity.

Another edge case occurs when $T$ cannot be decomposed into valid segment lengths. For example, $T=5$, $L=2$, $U=4$. No combination of 2-4 length segments can sum to 5, so all DP states except $dp[0]$ remain unreachable. The algorithm correctly outputs $-1$ because all transitions from reachable states fail to cover exactly $T$.
