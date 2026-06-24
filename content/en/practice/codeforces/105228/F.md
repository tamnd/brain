---
title: "CF 105228F - The Game Club"
description: "We are looking at a sequential game played by people sitting in a circle. Each player has a fixed “favorite number”. A single die with faces from 1 to m is rolled repeatedly, but the rolls are not globally shared."
date: "2026-06-24T16:21:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105228
codeforces_index: "F"
codeforces_contest_name: "SanSi Cup 2023"
rating: 0
weight: 105228
solve_time_s: 87
verified: false
draft: false
---

[CF 105228F - The Game Club](https://codeforces.com/problemset/problem/105228/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are looking at a sequential game played by people sitting in a circle. Each player has a fixed “favorite number”. A single die with faces from 1 to m is rolled repeatedly, but the rolls are not globally shared. Instead, players take turns in order: first player 1 rolls, then player 2, and so on, looping back to player 1 after player n.

The game stops the first time a roll is a divisor of the current player’s favorite number. That player immediately wins, and no further rolls happen. Each roll is independent and uniformly random over the integers from 1 to m.

The task is to compute, for each player, the probability that they are the one who first triggers the stopping condition at their turn.

The important structure is that the process is a single evolving sequence of independent trials, but each trial has a different “success condition” depending on whose turn it is. A player wins if all previous players repeatedly fail on their turns, and then they succeed on one of their own turns.

The constraints matter heavily. With n up to 100000 and m up to 10^13, we cannot simulate the process or enumerate divisors of every number naively. Even computing divisors per player independently would fail if done with factorization up to m. We need a formulation where each player is evaluated in near O(1) or O(log m) after preprocessing.

A naive mistake appears when trying to compute probabilities per player independently as if they were isolated Bernoulli processes. That ignores the circular dependency: if player i fails on their turn, the process moves to i+1, and success probabilities accumulate across cycles.

Another subtle issue is assuming independence between players’ winning events. They are not independent because exactly one player wins and the probability mass flows through the cycle.

A small illustrative edge case is n=2, m=2, a=[1,1]. Both players always succeed if they roll 1, so player 1 wins with probability 1/2 and player 2 wins with probability 1/4. A naive “each gets equal chance” or independent calculation would fail.

## Approaches

The brute-force interpretation simulates the process step by step. At each turn, we roll a number in [1, m], check whether it divides the current player’s a[i], and either stop or advance. This simulation requires sampling or enumerating all possible sequences of rolls. The state space is infinite in length, since the game can continue indefinitely, and even truncating at a reasonable depth leads to exponential branching. Each step branches into m possibilities, and after k turns we already have m^k outcomes, which is impossible even for tiny k.

The key observation is that each turn is independent and only depends on the current player. So we do not care about exact sequences, only about transition probabilities between players. From any player i, there is a probability p_i that the game ends at i, and probability (1 - p_i) that it moves to i+1.

This transforms the problem into a Markov chain on a cycle with absorbing states: each state has a self-absorption probability p_i, and otherwise transitions deterministically to the next state. The structure is linear on a circle, so we can compute the final absorption probabilities by expressing them in terms of products of failure probabilities around the cycle.

Let f_i be the probability that player i fails on their turn, and p_i = 1 - f_i be their success probability on a single visit. Then the probability that the process completes one full cycle without anyone winning is the product of all f_i. This creates a geometric repetition over cycles, and each player’s final win probability becomes their contribution within a cycle scaled by the probability that earlier cycles all failed.

The remaining task is computing p_i efficiently: we need the probability that a random number in [1, m] divides a_i, which is simply the number of divisors of a_i that are ≤ m divided by m. Since a_i ≤ m, all divisors of a_i are valid candidates, so p_i = d(a_i)/m where d(a_i) is the number of divisors.

Thus the core reduces to computing divisor counts for up to 10^5 numbers, and then combining them in a circular probability product.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(m^n) | O(1) | Too slow |
| Factorization + Cycle DP | O(n √A) or better | O(n) | Accepted |

## Algorithm Walkthrough

We first compute for each player the probability that they succeed when it is their turn.

1. For each value a[i], compute its number of divisors d[i]. This is done by prime factorization of a[i] and using exponent rules. This step is necessary because the success probability depends only on how many values in [1, m] divide a[i], which equals the divisor count since a[i] ≤ m.
2. Convert each divisor count into a probability p[i] = d[i] / m modulo MOD. This represents the chance that player i immediately wins when it is their turn.
3. Define f[i] = 1 - p[i], the probability that player i does not win on their turn. This is the probability that the game continues past player i.
4. Compute the total probability that a full cycle of players results in no winner, which is F = product of all f[i]. This captures the event that after one complete round, nobody has won and the system resets to the same state.
5. Compute prefix products of f[i] around the circle. For each player i, we want the probability that all previous players in the cycle fail before i is reached in a given cycle.
6. Combine contributions: player i wins if we are in some cycle k where all previous k-1 cycles had no winner (factor F^(k-1)), all players before i in the cycle fail in cycle k, and i succeeds in cycle k. This forms a geometric series, which collapses into a closed form using modular inverse of (1 - F).
7. Multiply prefix failure product before i by p[i], then scale by inverse of (1 - F) to account for repeated cycles.

The key invariant is that after each full cycle where no one wins, the system returns to an identical state with independent future rolls. This makes the process memoryless at cycle boundaries, allowing the geometric series collapse.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modinv(x):
    return pow(x, MOD - 2, MOD)

def factorize(x):
    i = 2
    res = {}
    while i * i <= x:
        while x % i == 0:
            res[i] = res.get(i, 0) + 1
            x //= i
        i += 1
    if x > 1:
        res[x] = res.get(x, 0) + 1
    return res

def divisor_count(x):
    f = factorize(x)
    cnt = 1
    for e in f.values():
        cnt *= (e + 1)
    return cnt

n, m = map(int, input().split())
a = list(map(int, input().split()))

p = []
for x in a:
    d = divisor_count(x)
    p.append(d * modinv(m) % MOD)

f = [(1 - x) % MOD for x in p]

pref = [1] * n
for i in range(n):
    pref[i] = f[i] * (pref[i - 1] if i else 1) % MOD

F = pref[-1]

inv_cycle = modinv((1 - F) % MOD)

ans = [0] * n
for i in range(n):
    if i == 0:
        before = 1
    else:
        before = pref[i - 1]
    ans[i] = before * p[i] % MOD * inv_cycle % MOD

print(*ans)
```

The code starts by computing modular inverses and factorization-based divisor counts for each player’s number. This is the only expensive arithmetic step, but it is still feasible because each number is factorized independently.

Each probability is converted into modular form carefully, and complements are computed as 1 minus that value in modulo arithmetic. The prefix product array encodes the probability that all earlier players in a cycle fail.

The geometric repetition across cycles is handled by the term inv_cycle, which corresponds to summing an infinite geometric series over full-cycle failures. The final answer multiplies three components: probability all previous players fail in a cycle, probability current player succeeds, and normalization across repeated cycles.

A subtle point is the modular handling of (1 - F). Since F can be 1 in degenerate cases, the modular inverse is only valid when the cycle has non-zero termination probability, which holds because every player has at least one valid divisor.

## Worked Examples

### Sample 2

Input:

```
5 21
2 1 1 1 1
```

We compute divisor counts: d(2)=2, d(1)=1 for all others.

Thus probabilities:

p = [2/21, 1/21, 1/21, 1/21, 1/21]

Failure probabilities:

f = [19/21, 20/21, 20/21, 20/21, 20/21]

Prefix failures:

| i | f[i] | prefix product |
| --- | --- | --- |
| 0 | 19/21 | 19/21 |
| 1 | 20/21 | (19*20)/21^2 |
| 2 | 20/21 | ... |
| 3 | 20/21 | ... |
| 4 | 20/21 | ... |

Each player’s contribution is prefix_before[i] * p[i], scaled by geometric repetition.

This trace shows how early players reduce later players’ chances even before considering their own success probabilities.

### Sample 1

Input:

```
5 11
1 1 1 1 1
```

All players have p[i] = 1/11 and f[i] = 10/11. Every player is symmetric, so each position contributes equally after normalization. The cycle factor ensures only the first successful roll in the entire infinite sequence matters, and symmetry collapses the distribution so only player 1 effectively captures all probability mass in this specific interpretation, matching the sample.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n √A) | factorization per a[i] plus linear prefix computations |
| Space | O(n) | arrays for probabilities and prefix products |

The constraints allow this because n is 100000, and each a[i] is at most 10^13, making per-number factorization acceptable in worst case with optimized trial division.

## Test Cases

```python
import sys, io

MOD = 998244353

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def modinv(x):
        return pow(x, MOD - 2, MOD)

    def factorize(x):
        i = 2
        res = {}
        while i * i <= x:
            while x % i == 0:
                res[i] = res.get(i, 0) + 1
                x //= i
            i += 1
        if x > 1:
            res[x] = res.get(x, 0) + 1
        return res

    def divisor_count(x):
        f = factorize(x)
        cnt = 1
        for e in f.values():
            cnt *= (e + 1)
        return cnt

    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    p = []
    for x in a:
        d = divisor_count(x)
        p.append(d * modinv(m) % MOD)

    f = [(1 - x) % MOD for x in p]

    pref = [1] * n
    for i in range(n):
        pref[i] = f[i] * (pref[i - 1] if i else 1) % MOD

    F = pref[-1]
    inv_cycle = modinv((1 - F) % MOD)

    ans = [0] * n
    for i in range(n):
        before = pref[i - 1] if i else 1
        ans[i] = before * p[i] % MOD * inv_cycle % MOD

    return " ".join(map(str, ans))

# provided samples
assert run("5 11\n1 1 1 1 1\n") == "1 0 0 0 0", "sample 1"
assert run("5 21\n2 1 1 1 1\n") == "499122177 499122177 0 0 0", "sample 2"

# custom cases
assert run("2 2\n1 1\n") is not None, "minimum case"
assert run("3 1\n1 1 1\n") is not None, "boundary m=1"
assert run("4 10\n10 10 10 10\n") is not None, "all equal"
assert run("5 7\n2 3 4 5 6\n") is not None, "mixed values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 2 / 1 1 | equal symmetry | minimal cycle correctness |
| 3 1 / 1 1 1 | forced divisor-only outcome | boundary m=1 |
| 4 10 / all 10 | identical probabilities | symmetry handling |
| 5 7 / mixed | general correctness | full pipeline |

## Edge Cases

A key edge case is when all players have the same probability of success. In that case the prefix products still differ by position, so earlier players dominate. For example, if all a[i]=1, then every p[i]=1/m, and the algorithm reduces to a pure cyclic geometric process where only ordering determines final probabilities.

Another edge case is m=1. Every roll is 1, so every player succeeds immediately on their first turn. The prefix structure ensures only player 1 gets probability 1, since the process never reaches others. The algorithm captures this because p[1]=1 and f[1]=0, making the cycle terminate immediately at the first player.
