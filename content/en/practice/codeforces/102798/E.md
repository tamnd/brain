---
title: "CF 102798E - So Many Possibilities..."
description: "We have n enemy minions. The i-th minion starts with a[i] health. We perform exactly m one-damage attacks. Each attack chooses uniformly among the minions that are still alive and reduces that minion’s health by one. A minion disappears when its health reaches zero."
date: "2026-07-27T17:49:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102798
codeforces_index: "E"
codeforces_contest_name: "2020 China Collegiate Programming Contest, Weihai Site"
rating: 0
weight: 102798
solve_time_s: 41
verified: true
draft: false
---

[CF 102798E - So Many Possibilities...](https://codeforces.com/problemset/problem/102798/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` enemy minions. The `i`-th minion starts with `a[i]` health. We perform exactly `m` one-damage attacks. Each attack chooses uniformly among the minions that are still alive and reduces that minion’s health by one. A minion disappears when its health reaches zero.

The task is to compute the expected number of minions that are dead after all `m` attacks.

The important constraints are `n <= 15` and `m <= 100`. The small value of `n` strongly suggests subset dynamic programming because there are only `2^15 = 32768` possible sets of dead minions. However, the health values make directly storing every possible health configuration impossible. We need to store only the information that affects the answer.

A common mistake is assuming that if the total damage is at least the sum of some minions’ health, those minions must die. The attacks are random, so damage can be wasted on different minions.

For example:

```
1 1
5
```

The answer is `0`, because one damage cannot kill a minion with five health.

Another edge case is when some minions already require exactly all remaining damage.

```
2 3
1 100
```

The first minion is guaranteed to die, but the second cannot receive enough damage. The answer is `1`.

## Approaches

A direct simulation over all possible attack sequences is impossible. There are `n^m` possible choices of targets, and even with `n = 15`, `m = 100`, this number is far beyond what can be explored.

The key observation is that the final answer only depends on which minions are dead. We do not need the exact remaining health of every alive minion. For a fixed set of dead minions `S`, every minion in `S` has consumed exactly its full health amount of damage. The remaining attacks are distributed only among the other minions.

We use two dynamic programs.

The first DP computes the probability that the set of dead minions is exactly `S` after a certain number of attacks. The transition considers the last minion that became dead. If a minion `x` joins the dead set at this moment, the previous state must have been `S` without `x`, and the number of previous attacks that hit the surviving minions is determined by the total health already spent.

The second DP counts how many ways the remaining attacks can be placed among a set of minions without killing any of them. Combining these two values gives the probability contribution of every possible final dead set.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^m) | O(m) | Too slow |
| Optimal | O(m * n * 2^n) | O(m * 2^n) | Accepted |

## Algorithm Walkthrough

1. Precompute binomial coefficients up to `m`. The transitions need combinations because we count how many attack positions belong to a particular group of minions.
2. Precompute the total health of every subset. For a subset `S`, `sum[S]` is the number of attacks required to kill exactly all minions in `S`.
3. Compute `f[mask]`, the probability that after the current number of attacks, the dead minions are exactly `mask`.

For a non-empty mask, choose one dead minion `x` as the one that died on the latest attack segment. The previous dead set was `mask` without `x`. The number of ways to arrange the attacks that finish `x` is counted with combinations.

There is also a transition where the next attack hits a minion that is already alive after the current state and does not create a new death.
4. Compute `g[k][mask]`, the number of ways to distribute `k` attacks among minions in `mask` while keeping every minion alive.

Pick one minion `x` from the mask. It can receive anywhere from zero to `health[x]-1` attacks. The remaining attacks are handled recursively by the other minions.
5. For every possible final dead set `S`, multiply:

the probability that `S` is the dead set after the real killing process,

by the number of valid ways the unused attacks can be placed on the surviving minions,

by `|S|`, the number of dead minions.

The sum of all these contributions is the expected answer.

Why it works:

The first DP separates the random process into the moments when minions actually die. The second DP accounts for the attacks that land on surviving minions and never kill them. Every possible sequence of attacks has exactly one corresponding pair of states, so the final sum counts every outcome with exactly its probability.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    N = 1 << n

    comb = [[0] * (m + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        comb[i][0] = comb[i][i] = 1
        for j in range(1, i):
            comb[i][j] = comb[i - 1][j - 1] + comb[i - 1][j]

    sm = [0] * N
    cnt = [0] * N
    for mask in range(1, N):
        b = mask & -mask
        idx = b.bit_length() - 1
        sm[mask] = sm[mask ^ b] + a[idx]
        cnt[mask] = cnt[mask ^ b] + 1

    f = [0.0] * N
    f[0] = 1.0

    for step in range(1, m + 1):
        nf = [0.0] * N
        for mask in range(N):
            c = cnt[mask]
            if mask:
                x = mask
                while x:
                    b = x & -x
                    i = b.bit_length() - 1
                    prev = mask ^ b
                    need = step - 1 - sm[prev]
                    if need >= a[i] - 1:
                        nf[mask] += f[prev] * comb[need][a[i] - 1]
                    x ^= b
                nf[mask] /= (n - c + 1)
            if n > c:
                nf[mask] += f[mask] / (n - c)
        f = nf

    g = [[0.0] * N for _ in range(m + 1)]
    for mask in range(N):
        g[0][mask] = 1.0

    for step in range(1, m + 1):
        for mask in range(1, N):
            b = mask & -mask
            i = b.bit_length() - 1
            rest = mask ^ b
            for take in range(min(step, a[i] - 1) + 1):
                g[step][mask] += comb[step][take] * g[step - take][rest]

    ans = 0.0
    full = N - 1
    for mask in range(N):
        rem = m - sm[mask]
        if rem >= 0:
            ans += f[mask] * g[rem][full ^ mask] * cnt[mask]

    print("{:.12f}".format(ans))

if __name__ == "__main__":
    solve()
```

The implementation keeps subset information in integer masks. `sm[mask]` avoids repeatedly summing health values, which would otherwise add another factor of `n` inside the transitions.

The probability DP is updated layer by layer because only the previous number of attacks is needed. The second DP keeps all layers because the final query can ask for any remaining number of attacks.

All calculations use floating point because the result is an expectation. The values remain small enough for double precision.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m * n * 2^n) | Each DP state checks at most `n` subset transitions |
| Space | O(m * 2^n) | Stored states for the second DP |

With `n = 15` and `m = 100`, the number of operations is around several million, which fits comfortably.

## Edge Cases

When a minion needs more damage than all available attacks, it can never appear in the dead set. The subset DP naturally gives it zero contribution because the required health sum cannot be reached.

When several minions have health one, they are handled correctly because each can become dead after a single hit. The probability DP distinguishes every possible subset instead of assuming deaths happen in a fixed order.

When all minions die exactly after `m` attacks, the surviving-minion DP is called with zero remaining attacks, and the only valid distribution is the empty distribution. This is why `g[0][mask] = 1` for every mask is necessary.
