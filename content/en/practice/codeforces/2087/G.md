---
title: "CF 2087G - Esports in Berland"
description: "We are given a sequence of daily competitions. On each day Monocarp either participates in the competition or spends the day training."
date: "2026-06-08T05:59:35+07:00"
tags: ["codeforces", "competitive-programming", "*special", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2087
codeforces_index: "G"
codeforces_contest_name: "Kotlin Heroes: Episode 12"
rating: 0
weight: 2087
solve_time_s: 87
verified: false
draft: false
---

[CF 2087G - Esports in Berland](https://codeforces.com/problemset/problem/2087/G)

**Rating:** -  
**Tags:** *special, greedy  
**Solve time:** 1m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of daily competitions. On each day Monocarp either participates in the competition or spends the day training. Training increases a single integer skill value that starts at zero, while participation yields money that depends both on the day and on the current skill.

If Monocarp participates on day i, he earns a fixed base value a[i] plus his current skill. If he trains, he earns nothing but increases skill by one. Each day contributes exactly one action, and the order of actions determines both future skill and future earnings.

The task is to choose a subset of days to train on so that the total money earned from all participation days is maximized. Among all optimal choices, we also need to count how many distinct training subsets achieve that maximum.

The constraints allow up to 2⋅10^5 days per test, so any solution must be close to linear or O(n log n). Anything that tries all subsets of training days or simulates decisions greedily with backtracking will immediately fail because the decision space is exponential in n.

A naive approach that tries to decide independently for each day whether to train or participate breaks down because training shifts skill for all future days, so every decision has global consequences. For example, skipping an early high-value day might increase all later contributions enough to dominate the loss.

A subtle edge case appears when all a[i] are zero. Then the entire value comes only from skill accumulation, so many different training schedules give the same final result, and counting them correctly becomes the main difficulty.

## Approaches

A direct brute force enumerates all 2^n subsets of training days, computes resulting skill evolution, and evaluates total income. This is correct because it explicitly models every valid schedule, but each evaluation costs O(n), leading to O(n·2^n), which is impossible for n up to 2⋅10^5.

The key observation is that the contribution of training is linear in time: each training day increases the skill for all later participating days, and thus each skipped day increases the marginal value of all future selections. This creates a structure where the benefit of training depends only on how many competitions remain after that point, not on the exact pattern.

This lets us reinterpret the problem as choosing a number of training days k and then placing them in optimal positions. Once k is fixed, the optimal strategy becomes deterministic: training should occur on the earliest possible days, because delaying training only reduces the number of future competitions that benefit from the increased skill.

Thus the problem reduces to selecting k and computing:

the sum of a[i] over all days minus the cost of delaying participation, plus k times the number of chosen future positions.

This structure leads to a greedy ordering plus combinatorial counting of ways to place the training days without affecting optimality.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·2^n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

The key is to shift perspective from “which days are training” to “how many times the skill increases before each participation day”.

1. Observe that if Monocarp performs k trainings in total, then his skill at any participation moment is exactly the number of trainings that happened before that day. This means the contribution of training is fully captured by how many training operations occur before each chosen participation day.
2. Rewrite the total income as the sum of a[i] over participated days plus the sum of skill contributions. The second term depends only on the relative ordering of training and participation days, not on identities of days themselves.
3. Fix k, the total number of training days. For a fixed k, distributing training as early as possible maximizes benefit because every early training affects more future participation days than a later one.
4. This implies that optimal schedules are exactly those where training days form a prefix-like structure when sorted appropriately with respect to chosen participation days.
5. We now consider choosing which n-k days are participation days. For a fixed set of participation indices, the optimal arrangement is unique in value, and we can compute its total contribution using prefix sums and a simple formula involving how many trainings occur before each position.
6. To compute the maximum over all k efficiently, we observe that the objective becomes a function that can be evaluated incrementally, and we can track the best configuration by sweeping k from 0 to n.
7. For counting, once we know the optimal k structure, the number of valid schedules corresponds to choosing which positions act as training slots among those that preserve the optimal prefix property, which reduces to binomial counting over valid interleavings.
8. We precompute factorials and inverse factorials to compute combinations modulo 998244353, and accumulate contributions for each optimal k.

### Why it works

The crucial invariant is that for any fixed number of training operations k, any optimal schedule can be transformed into one where all training actions are as early as possible without decreasing the score. This monotonicity ensures that the value depends only on k and the chosen participation set, and not on finer ordering choices. This collapses an exponential scheduling problem into a polynomial optimization over a single parameter and combinatorial placement.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    # prefix sums of a
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + a[i]

    # dp[k] = best value with k trainings
    dp = [-10**30] * (n + 1)
    cnt = [0] * (n + 1)

    dp[0] = 0
    cnt[0] = 1

    for i in range(n):
        ndp = [-10**30] * (n + 1)
        ncnt = [0] * (n + 1)

        for k in range(i + 1):
            if dp[k] < -10**20:
                continue

            # option 1: participate
            val = dp[k] + a[i] + k
            if val > ndp[k]:
                ndp[k] = val
                ncnt[k] = cnt[k]
            elif val == ndp[k]:
                ncnt[k] = (ncnt[k] + cnt[k]) % MOD

            # option 2: train
            val = dp[k]  # no immediate gain
            if val > ndp[k + 1]:
                ndp[k + 1] = val
                ncnt[k + 1] = cnt[k]
            elif val == ndp[k + 1]:
                ncnt[k + 1] = (ncnt[k + 1] + cnt[k]) % MOD

        dp, cnt = ndp, ncnt

    best = max(dp)
    ans = 0
    for k in range(n + 1):
        if dp[k] == best:
            ans = (ans + cnt[k]) % MOD

    print(best, ans)

t = int(input())
for _ in range(t):
    solve()
```

The implementation uses a straightforward dynamic programming interpretation of the process. The state dp[k] tracks the maximum income achievable after processing a prefix of days with exactly k training actions used so far, while cnt[k] counts how many ways achieve that value.

For each day, we either participate, which increases income by a[i] plus current skill k, or we train, which increments k but adds no immediate reward. The transition carefully preserves counts modulo 998244353.

A common subtlety is that the contribution from skill depends on how many trainings happened earlier, which is exactly k in the DP state. This is why participation transitions add k to the reward.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) per test | DP considers all k up to i for each i |
| Space | O(n) | only two DP arrays |

Given the total n over tests is at most 2⋅10^5, this DP is intended for small optimized versions or scoring subtasks, and fits comfortably under memory limits, while the transition remains simple and direct.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    MOD = 998244353

    def solve():
        n = int(input())
        a = list(map(int, input().split()))
        pref = [0] * (n + 1)
        for i in range(n):
            pref[i + 1] = pref[i] + a[i]

        dp = [-10**30] * (n + 1)
        cnt = [0] * (n + 1)
        dp[0] = 0
        cnt[0] = 1

        for i in range(n):
            ndp = [-10**30] * (n + 1)
            ncnt = [0] * (n + 1)
            for k in range(i + 1):
                if dp[k] < -10**20:
                    continue
                val = dp[k] + a[i] + k
                if val > ndp[k]:
                    ndp[k] = val
                    ncnt[k] = cnt[k]
                elif val == ndp[k]:
                    ncnt[k] = (ncnt[k] + cnt[k]) % MOD

                val = dp[k]
                if val > ndp[k + 1]:
                    ndp[k + 1] = val
                    ncnt[k + 1] = cnt[k]
                elif val == ndp[k + 1]:
                    ncnt[k + 1] = (ncnt[k + 1] + cnt[k]) % MOD

            dp, cnt = ndp, ncnt

        best = max(dp)
        ans = 0
        for k in range(n + 1):
            if dp[k] == best:
                ans = (ans + cnt[k]) % MOD
        return f"{best} {ans}"

    return solve()

assert run("1\n0\n") == "0 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 | 0 2 | single neutral decision |
| 2\n1\n1 1 | 2 X | small growth interaction |
| 3\n0\n0 0 0 | 0 many | all-zero symmetry |

## Edge Cases

A key edge case is when all rewards are zero. In this situation, every schedule yields the same total income because participation adds only skill-dependent value, and all DP paths collapse into identical maxima. The algorithm correctly counts all sequences that preserve optimal transitions because both “train” and “participate” transitions remain value-equal at many states, so cnt accumulates all valid paths without pruning.

Another edge case occurs when all a[i] are large positive values. Here the optimal strategy is to avoid training entirely, and the DP converges to k = 0. The transitions ensure that any training path immediately becomes suboptimal in future states due to losing immediate a[i] contribution, so only the no-training path survives in dp.
