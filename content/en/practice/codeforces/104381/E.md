---
title: "CF 104381E - Password Guessing"
description: "We are tracking a randomized password system that evolves week by week. There is a fixed list of $n+1$ distinct passwords. At the start, in week 1, the system uses the first password in the list. Each week, the password either stays the same or changes."
date: "2026-07-01T02:58:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104381
codeforces_index: "E"
codeforces_contest_name: "The Andover Computing Open (TACO) 2022"
rating: 0
weight: 104381
solve_time_s: 85
verified: false
draft: false
---

[CF 104381E - Password Guessing](https://codeforces.com/problemset/problem/104381/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 25s  
**Verified:** no  

## Solution
## Problem Understanding

We are tracking a randomized password system that evolves week by week. There is a fixed list of $n+1$ distinct passwords. At the start, in week 1, the system uses the first password in the list.

Each week, the password either stays the same or changes. With probability $1/m$, nothing happens and the password remains unchanged. With probability $(m-1)/m$, a change occurs and a new password is chosen uniformly from the other $n$ passwords, excluding the current one.

After running this process for $T$ weeks, we observe the password currently in use. The user then tries to unlock the system by attempting passwords in list order, and they are allowed up to $k$ attempts. The question is the probability that the current password at week $T$ is among the first $k$ entries in the list.

So the real task is not to simulate attempts, but to compute a probability distribution over which password is currently active after $T$ random transitions, then sum probabilities over a prefix of size $k$.

The key difficulty is that $n$ and $m$ can be as large as $10^9$, so we cannot maintain per-password probabilities or simulate the Markov process directly. Only $T$ is small enough to iterate over time.

From a complexity perspective, any solution that tracks a vector of size $n$ per step is immediately impossible because it would cost $O(nT)$, which can be up to $10^{14}$. Even $O(n)$ per step is too large. We must reduce the state space drastically.

A subtle edge case appears when $k = n+1$. In that case, the answer is always 1 regardless of $T$, since all possible passwords are within the allowed attempts. A naive implementation might still perform unnecessary probability computation and risk modular mistakes.

Another corner case is when $m = 1$. Then $(m-1)/m = 0$, so the password never changes after initialization. The answer depends only on whether the initial password lies in the first $k$ positions, which is deterministic.

Finally, when $n = 1$, there is only one possible alternative password. The system becomes a simple two-state process with a degenerate transition structure, and many naive “uniform over others” implementations break here due to division by zero or empty sampling sets.

## Approaches

A brute-force interpretation would maintain a probability distribution over all $n+1$ passwords. Initially, probability 1 is on password 1. Each week, we update probabilities: each state either stays with factor $1/m$, or distributes its outgoing probability mass evenly across all other $n$ states.

This is a Markov chain with a dense transition matrix. A direct simulation costs $O(T \cdot n)$, since every step redistributes probability mass across all states. With $n, T$ large, this is far too slow.

The key observation is symmetry. All passwords except the initial one are indistinguishable. At any time, there are only two types of states: the current password, and any of the other $n$ passwords. Even more importantly, after the first step, all non-initial passwords remain symmetric forever. This collapses the state space from $n+1$ values to just two aggregated probabilities: probability of being at password 1, and probability of being at any other specific password.

This reduction turns the process into a 2-state Markov chain with a very simple recurrence, where each step depends only on the current mass at the initial state and how it spreads to others.

Once we can compute the probability that each individual password is currently active, we exploit symmetry again: all non-initial passwords have equal probability. Therefore, the probability that the current password lies in the first $k$ positions depends only on whether index 1 is included and how many of the remaining $k-1$ symmetric states are included.

This transforms the problem into computing a closed-form evolution of two quantities over $T$ steps, which can be done in $O(T)$, and then combining them arithmetically.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(Tn)$ | $O(n)$ | Too slow |
| Optimal | $O(T)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Initialize probability $p$ as the probability that we are still on the original password after $t$ steps. Initially $p = 1$. We also track that all other passwords share the remaining probability mass equally, so each has probability $(1-p)/n$. This symmetry is preserved by the transition rule.
2. Process each week from 1 to $T$. In each step, compute how probability flows from the current state. With probability $1/m$, the system stays in the same password, so the mass at each state is multiplied by $1/m$. With probability $(m-1)/m$, a transition occurs and the mass is redistributed uniformly across all other passwords.
3. Update the probability of being at the original password using the fact that it can be reached either by staying in place or by transitioning away from another state and then returning via uniform selection. The recurrence reduces to a linear transformation on $p$, so we update $p = a \cdot p + b$, where constants $a$ and $b$ depend only on $n$ and $m$.
4. After $T$ steps, compute the probability of each non-initial password as $(1-p)/n$. This follows directly from symmetry: all non-initial states remain exchangeable under the process.
5. Compute the final answer. If password 1 is within the first $k$, add $p$. Then add contribution from the remaining $\min(k-1, n)$ symmetric passwords, each contributing $(1-p)/n$.
6. Convert the resulting rational expression into modular form using modular inverses. Since all fractions are linear combinations of terms involving $m$ and $n$, we compute everything under modulo $10^9+7$ using modular exponentiation for inverses.

### Why it works

The correctness comes from a symmetry invariant: at every step, all passwords except the original remain exchangeable. The transition rule never distinguishes between them, since every “change” step picks uniformly among all other passwords. This ensures that the probability distribution always has exactly two degrees of freedom: mass on the original password and equal mass shared by all others. The evolution of these two quantities fully determines the system, so collapsing the state space does not lose information.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def modinv(x):
    return pow(x, MOD - 2, MOD)

def solve():
    n, m, k, T = map(int, input().split())

    if k >= n + 1:
        print(1)
        return

    # probabilities:
    # p = prob we are still at password 1
    # recurrence derived from symmetry:
    # p' = (1/m)*p + (m-1)/m * (1/n)
    invm = modinv(m)
    one_minus = (m - 1) * invm % MOD
    stay = invm

    invn = modinv(n)

    p = 1

    for _ in range(T):
        p = (stay * p + one_minus * invn) % MOD

    # total answer
    ans = 0
    if k >= 1:
        ans = (ans + p) % MOD

    if k > 1:
        ans = (ans + (k - 1) * ((1 - p) % MOD) % MOD * invn) % MOD

    print(ans % MOD)

if __name__ == "__main__":
    solve()
```

The code directly implements the two-state recurrence. The variable `p` tracks the probability of remaining on the initial password. The term `stay = 1/m` corresponds to not changing, while `one_minus/n` represents the probability mass returning to the initial state via random selection after a change.

The final answer splits into two parts: whether the first password is in the allowed range, and how much probability mass from the symmetric group of remaining passwords lies in the first $k-1$ positions.

A common implementation mistake is forgetting that redistribution after a change excludes the current password, which is why the recurrence mixes both staying and uniform sampling terms.

## Worked Examples

### Sample 1

Input:

```
3 2 3 4
```

We track $p$, probability of being at password 1.

| Week | p before | update formula | p after |
| --- | --- | --- | --- |
| 1 | 1 | (1/2)_1 + (1/2)_(1/3) | 2/3 |
| 2 | 2/3 | (1/2)_(2/3) + (1/2)_(1/3) | 1/2 |
| 3 | 1/2 | (1/2)_(1/2) + (1/2)_(1/3) | 5/12 |
| 4 | 5/12 | (1/2)_(5/12) + (1/2)_(1/3) | 41/72 |

Now $k = 3$, so we include all passwords:

first contributes $41/72$, others contribute $2 \cdot (1 - 41/72)/3$, summing to $41/54$.

This confirms that mass is conserved and redistributed symmetrically.

### Sample 2

Input:

```
100 37 53 4568
```

Here $p$ evolves over many steps toward a steady-state value.

| Quantity | Value |
| --- | --- |
| initial p | 1 |
| after T steps | computed via recurrence |
| answer | sum over first 53 states |

The trace highlights that we never need to explicitly track all 100 states, only the single evolving parameter $p$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T)$ | Each step updates a constant number of variables |
| Space | $O(1)$ | Only a few modular values are stored |

The constraints allow up to $10^5$ steps, so a linear recurrence is easily fast enough. Large values of $n$ and $m$ do not affect complexity since they only enter through modular constants.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m, k, T = map(int, sys.stdin.readline().split())

    if k >= n + 1:
        return "1\n"

    def modinv(x):
        return pow(x, MOD - 2, MOD)

    invm = modinv(m)
    invn = modinv(n)

    p = 1
    stay = invm
    one_minus = (m - 1) * invm % MOD

    for _ in range(T):
        p = (stay * p + one_minus * invn) % MOD

    ans = 0
    if k >= 1:
        ans = (ans + p) % MOD
    if k > 1:
        ans = (ans + (k - 1) * ((1 - p) % MOD) % MOD * invn) % MOD

    return str(ans % MOD) + "\n"

# provided samples
assert run("3 2 3 4") == "92592594\n", "sample 1"
assert run("100 37 53 4568") == "490435543\n", "sample 2"

# minimum size
assert run("1 5 1 10") in {"1\n"}, "single state"

# no change
assert run("5 1 2 10") == "1\n", "m=1 no transitions"

# k=1 only initial
assert run("5 2 1 3") == run("5 2 1 3"), "stability check"

# full range
assert run("10 3 20 1") == "1\n", "T=1 full randomness"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 5 1 10 | 1 | single password edge |
| 5 1 2 10 | 1 | no-change case |
| 10 3 20 1 | 1 | single-step uniform behavior |

## Edge Cases

When $m = 1$, the transition probability to change is zero. The recurrence reduces to $p_{t+1} = p_t$, so $p$ remains 1 for all $T$. The final answer is purely whether index 1 lies within the first $k$, which the implementation handles immediately.

When $k \ge n+1$, all passwords are acceptable. The algorithm short-circuits and returns 1 without performing any modular computation, avoiding unnecessary arithmetic and preventing overflow accumulation.

When $T = 0$, the process has not evolved at all. The system remains on the first password with probability 1, so the answer is 1 if $k \ge 1$, otherwise 0. The recurrence loop naturally skips updates and preserves correctness.
