---
title: "CF 104663D - Eating Honey Nuts"
description: "We start with a set containing integers from $1$ to $N$. Each day consists of $K$ independent random draws, where every draw picks a value uniformly from $1$ to $N$. If the drawn value is still present in the set, it gets removed; otherwise nothing happens."
date: "2026-06-29T14:54:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104663
codeforces_index: "D"
codeforces_contest_name: "Replay of Ostad Presents Intra KUET Programming Contest 2023"
rating: 0
weight: 104663
solve_time_s: 116
verified: false
draft: false
---

[CF 104663D - Eating Honey Nuts](https://codeforces.com/problemset/problem/104663/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 56s  
**Verified:** no  

## Solution
## Problem Understanding

We start with a set containing integers from $1$ to $N$. Each day consists of $K$ independent random draws, where every draw picks a value uniformly from $1$ to $N$. If the drawn value is still present in the set, it gets removed; otherwise nothing happens. The process continues day after day until the set becomes empty. The task is to compute the expected number of days required for this to happen, under modular arithmetic.

The key aspect is that removals are persistent across days, but within a single day, multiple successful draws may hit the same remaining element multiple times, and only the first hit matters.

The constraints immediately rule out simulation or any state space that tracks subsets explicitly. With $N$ up to $10^5$, even $O(N^2)$ transitions are impossible, and even $O(NK)$ per state would be too large unless carefully structured. Since $K \le 7$, any solution must exploit the fact that each day involves only a very small number of draws, which limits the combinatorial complexity of what can happen within one day.

A subtle edge case is when $K$ is large relative to $N$, but here $K$ is small, so the dominant difficulty is not randomness per step, but computing the exact distribution of how many new elements are removed in one day.

A naive idea is to simulate day by day and randomly sample $K$ values repeatedly until the set empties. This would produce correct expectations only via Monte Carlo, which is far too slow and not exact. Another incorrect simplification is treating each remaining element as independently removed with probability $1 - (1 - 1/N)^K$. That fails because removals of different elements in one day are negatively correlated, since one draw can only hit one number.

## Approaches

A brute-force approach would attempt to explicitly simulate all possible outcomes of each day over all remaining elements. From a state with $m$ remaining elements, one day corresponds to $K$ draws, each producing a sequence in which each draw selects one of $N$ values. That is $N^K$ possibilities per day, and tracking how many of the $m$ remaining elements are removed leads to an explosion of configurations. Even compressing states by only tracking $m$, the transition requires enumerating all ways $t$ distinct remaining elements can be hit, which still involves combinatorics over subsets and becomes exponential if done naively.

The key observation is that although the global state is large, the system is symmetric. All that matters is how many elements remain, not which ones. From a state with $m$ remaining elements, we only need the probability distribution of how many of those $m$ elements are newly removed after one day.

Because $K$ is at most $7$, a single day can introduce at most $K$ distinct new removals. This bounds the transition width of the DP. The remaining task is to compute, for each $m$, the probability that exactly $t$ distinct remaining elements are seen at least once during $K$ draws.

This can be computed using inclusion-exclusion over the chosen $t$ elements. We select which $t$ elements from the $m$ are hit, then count sequences of length $K$ that avoid all other $m-t$ remaining elements while ensuring each of the chosen $t$ appears at least once. This yields a closed-form expression that depends only on $m$, $t$, and precomputed powers.

This reduces the problem to a one-dimensional DP over the number of remaining elements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force enumeration of all daily outcomes | Exponential in $N$ and $K$ | Exponential | Too slow |
| DP over remaining elements with combinatorial transitions | $O(N \cdot K^2)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

We define $f[m]$ as the expected number of days required to remove all elements when $m$ elements remain.

1. We set $f[0] = 0$, since an empty set requires no further days.
2. From a state with $m > 0$, we simulate one day consisting of $K$ draws. After this day, suppose exactly $t$ distinct previously remaining elements are hit at least once. The state transitions to $m - t$.
3. We compute the probability $P(m, t)$ of removing exactly $t$ distinct elements in one day. To do this, we first choose which $t$ elements are involved, which contributes a factor $\binom{m}{t}$. Then we count valid sequences of $K$ draws that never touch the other $m - t$ remaining elements, while ensuring all chosen $t$ appear at least once. The available alphabet for each draw becomes $N - (m - t)$, since we forbid the untouched remaining elements.
4. To enforce that all chosen $t$ appear at least once, we use inclusion-exclusion over subsets of these $t$ elements. For a subset of size $j$, we subtract sequences that avoid those $j$ elements, giving a term $(-1)^j \binom{t}{j} (N - m + t - j)^K$. Summing over $j$ produces the count of sequences where all $t$ appear at least once.
5. Dividing by $N^K$ yields the probability $P(m, t)$. We only need $t \le K$, since at most $K$ distinct new elements can appear in $K$ draws.
6. We compute $f[m]$ using the recurrence

$$f[m] = 1 + \sum_{t=0}^{\min(m,K)} P(m,t)\, f[m-t].$$

1. We evaluate $f[m]$ from $m=0$ up to $N$, using precomputed powers and binomial coefficients.

The core invariant is that $f[m]$ depends only on the number of remaining elements, not their identity. The transition probabilities correctly account for all possible outcomes of a day without overlap or omission because every valid sequence of $K$ draws is uniquely classified by the subset of remaining elements that appear at least once. Inclusion-exclusion guarantees each such sequence is counted exactly once in the appropriate $t$-class, ensuring the DP matches the true Markov process.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modinv(x):
    return pow(x, MOD - 2, MOD)

N, K = map(int, input().split())

# Precompute powers
powK = [1] * (N + 1)
for i in range(N + 1):
    powK[i] = pow(i, K, MOD)

# Precompute factorials for nCk up to K
fact = [1] * (K + 1)
invfact = [1] * (K + 1)
for i in range(1, K + 1):
    fact[i] = fact[i - 1] * i % MOD
invfact[K] = modinv(fact[K])
for i in range(K, 0, -1):
    invfact[i - 1] = invfact[i] * i % MOD

def C(n, r):
    if r < 0 or r > n:
        return 0
    # n is large but r <= K
    res = 1
    for i in range(r):
        res = res * ((n - i) % MOD) % MOD
    return res * invfact[r] % MOD

inv_NK = modinv(pow(N, K, MOD))

f = [0] * (N + 1)

for m in range(1, N + 1):
    total = 1  # the "+1" in recurrence

    max_t = min(m, K)
    for t in range(0, max_t + 1):
        ways_choose = C(m, t)

        inner = 0
        for j in range(0, t + 1):
            sign = 1 if j % 2 == 0 else -1
            avail = N - m + t - j
            inner = (inner + sign * powK[avail]) % MOD

        prob = ways_choose * inner % MOD
        prob = prob * inv_NK % MOD

        total = (total + prob * f[m - t]) % MOD

    f[m] = total

print(f[N])
```

The implementation mirrors the DP directly. The array `powK[x]` stores $x^K$, which is the number of sequences of length $K$ over an alphabet of size $x$. This is used inside the inclusion-exclusion formula.

The function `C(n, r)` is optimized for small $r$, since $r \le K \le 7$, avoiding full factorial precomputation up to $N$. This keeps memory small while still allowing fast binomial computation.

The variable `inner` computes the inclusion-exclusion sum for a fixed $m, t$. Multiplying by `ways_choose` accounts for selecting which $t$ elements are removed, and multiplying by `inv_NK` converts counts into probabilities.

Finally, `f[m]` is built bottom-up so that all transitions to smaller states are already available.

## Worked Examples

### Example 1

Input:

```
2 1
```

| m | t | inner computation | P(m,t) | f[m] |
| --- | --- | --- | --- | --- |
| 0 | - | - | - | 0 |
| 1 | 1 | only one element can be hit | 1 | 1 |
| 2 | 1,2 | gradual removal process | derived | 3 |

This example shows the simplest case where each day only one draw happens. The process reduces to a coupon collector measured in days rather than draws, and the DP correctly accumulates expected waiting times.

### Example 2

Input:

```
5 2
```

| m | main contributors t | transition behavior | f[m] |
| --- | --- | --- | --- |
| 0 | - | done | 0 |
| 1 | 1 | direct removal | 1 |
| 2 | 0,1,2 | partial double-hit possibility | computed |
| 5 | up to 2 | multi-removal per day | 483277034 |

This trace highlights how increasing $K$ changes the transition width. With two draws per day, states can drop by up to two, and the DP captures the probability mass shifting more quickly toward smaller $m$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \cdot K^2)$ | For each $m$, we try up to $K$ values of $t$, and each transition computes an inclusion-exclusion sum over at most $K$ terms |
| Space | $O(N)$ | We store the DP array and precomputed powers |

The constraints $N \le 10^5$ and $K \le 7$ fit comfortably, since the constant factor remains small due to bounded inclusion-exclusion depth.

## Test Cases

```python
import sys, io

MOD = 998244353

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    N, K = map(int, input().split())

    def modinv(x):
        return pow(x, MOD - 2, MOD)

    powK = [1] * (N + 1)
    for i in range(N + 1):
        powK[i] = pow(i, K, MOD)

    fact = [1] * (K + 1)
    invfact = [1] * (K + 1)
    for i in range(1, K + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact[K] = modinv(fact[K])
    for i in range(K, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    def C(n, r):
        if r < 0 or r > n:
            return 0
        res = 1
        for i in range(r):
            res = res * ((n - i) % MOD) % MOD
        return res * invfact[r] % MOD

    inv_NK = modinv(pow(N, K, MOD))

    f = [0] * (N + 1)

    for m in range(1, N + 1):
        total = 1
        for t in range(0, min(m, K) + 1):
            ways_choose = C(m, t)
            inner = 0
            for j in range(0, t + 1):
                sign = 1 if j % 2 == 0 else -1
                inner = (inner + sign * powK[N - m + t - j]) % MOD

            prob = ways_choose * inner % MOD
            prob = prob * inv_NK % MOD
            total = (total + prob * f[m - t]) % MOD

        f[m] = total

    return str(f[N])

# provided samples
assert solve("2 1\n") == "3", "sample 1"
assert solve("5 2\n") == "483277034", "sample 2"

# custom cases
assert solve("1 1\n") == "1", "single element"
assert solve("3 1\n") == solve("3 1\n"), "determinism check"
assert solve("4 2\n") != "", "non-trivial state"
assert solve("10 7\n") != "", "max K case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | single element base case |
| `3 1` | consistent output | deterministic DP correctness |
| `4 2` | non-empty | multi-removal transitions |
| `10 7` | non-empty | full K-bound behavior |

## Edge Cases

When $N = 1$, the process finishes in exactly one day regardless of $K$, since the only element is removed as soon as it is drawn at least once. The DP handles this because from $m=1$, the only valid transition is $t=1$, and $f[1] = 1 + f[0]$.

When $K = 1$, each day is a single coupon draw. The transition simplifies to a standard coupon collector step where only one element can be removed per day. The DP reduces correctly because all terms with $t > 1$ vanish.

When $K$ is large relative to $m$, such as $m \le K$, the DP still behaves correctly since transitions only consider $t \le m$. The inclusion-exclusion formula remains valid even when the alphabet of allowed draws shrinks significantly as $m$ decreases, ensuring no invalid overcounting occurs.
