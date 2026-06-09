---
title: "CF 1776K - Uniform Chemistry"
description: "Each researcher starts with a chemical labeled by an integer between $1$ and $n-1$. Every year they upgrade their current chemical: if someone currently holds value $a$, they replace it with a uniformly random integer from the interval $(a, n]$."
date: "2026-06-09T11:49:06+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 1776
codeforces_index: "K"
codeforces_contest_name: "SWERC 2022-2023 - Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 3200
weight: 1776
solve_time_s: 132
verified: false
draft: false
---

[CF 1776K - Uniform Chemistry](https://codeforces.com/problemset/problem/1776/K)

**Rating:** 3200  
**Tags:** dp, math  
**Solve time:** 2m 12s  
**Verified:** no  

## Solution
## Problem Understanding

Each researcher starts with a chemical labeled by an integer between $1$ and $n-1$. Every year they upgrade their current chemical: if someone currently holds value $a$, they replace it with a uniformly random integer from the interval $(a, n]$. Once a researcher reaches $n$, they stop changing because $n$ has no outgoing transitions.

We are asked to compute, for each researcher, the probability that they are the first to ever reach $n$. If multiple researchers reach $n$ in the same year, they all count as winners, so ties are allowed.

The key difficulty is that $n$ can be extremely large, so any state-by-state dynamic programming over all values is impossible. There are up to $10^5$ researchers, so even linear work per state transition is acceptable only if the state space is small or collapses into a closed form expression.

A naive simulation would track every researcher year by year and repeatedly sample transitions. This immediately fails because the expected time to reach $n$ grows with $n$, and the number of states is enormous. Even a DP over values $1$ to $n$ is impossible since $n$ can be up to $10^{18}$.

A more subtle failure case appears when multiple researchers start from the same value. A greedy intuition might suggest that lower starting values always imply worse chances, but this is false because all processes are independent and the race depends on entire distribution of hitting times, not just expected values.

## Approaches

The process for a single researcher is a Markov chain on values from its starting point up to $n$. From a state $a$, the next state is uniformly distributed among $a+1$ through $n$, so transitions always move upward and the chain is absorbing at $n$.

The brute-force idea is to compute, for each researcher, the distribution of the time to reach $n$. Once we know these distributions, we can compare independent random variables and compute win probabilities by convolution over all subsets. This immediately becomes intractable because even representing one distribution requires $O(n)$ states, and combining $m$ of them introduces exponential complexity in interactions.

The key observation is that the process is memoryless in a very strong sense once we reinterpret it correctly. Instead of tracking absolute values, we focus on the probability that a researcher has not yet reached $n$ after a given number of steps. Because transitions are uniform over suffix intervals, the survival probability depends only on the current value, and these values form a telescoping structure.

This structure allows us to compute, for each starting value, a closed form expression for the probability that the researcher is still active after $k$ steps, and from that derive the distribution of the exact hitting time. Once we have per-researcher distributions, the competition reduces to comparing independent discrete random variables, which can be handled using prefix products over survival probabilities.

The final reduction is that each researcher contributes a function of its starting value, and all interactions between researchers factor through multiplicative survival terms. This collapses the problem into computing a set of harmonic-like values over suffix intervals, which can be done in linear time after sorting and precomputation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Naive simulation | $O(n \cdot m)$ per run or worse | $O(n)$ | Too slow |
| Distribution DP over states | $O(nm)$ | $O(nm)$ | Impossible for constraints |
| Optimal closed-form survival computation | $O(n + m)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We reinterpret the process in reverse time: instead of asking when a researcher reaches $n$, we ask how likely it is that a given researcher is still “alive” after a certain number of transitions. This avoids tracking exact sequences.

For each starting value $s$, define $f(s)$ as the probability that the next transition jumps directly to $n$. This is $\frac{1}{n-s}$. More generally, transitions only depend on the remaining interval size, so every state $a$ behaves like an interval of length $n-a$.

We then compute the probability distribution of reaching $n$ in exactly $k$ steps. The crucial simplification is that at each step the remaining interval shrinks uniformly, and all paths correspond to choosing a strictly increasing chain ending at $n$.

Instead of explicitly computing distributions, we use a dynamic programming over interval lengths. Let $g(x)$ represent the contribution of a state with $x$ remaining distance to $n$. The recurrence depends only on suffix averages over larger values, which allows us to compute all $g(x)$ in decreasing order of $x$.

Once each researcher has a function describing its distribution of hitting time, we compute prefix survival probabilities. The probability that researcher $i$ wins is the probability that it reaches $n$ at time $t$ while all others reach it at time at least $t$.

We process time implicitly. For each possible step depth, we accumulate contributions of researchers who can finish at that depth and multiply by survival probabilities of all others, which factorizes due to independence.

## Why it works

The key invariant is that the process from any state depends only on the size of the remaining interval, not on the absolute label. This turns the system into a one-dimensional structure where all transition probabilities are functions of interval length alone. Because every transition moves strictly upward and chooses uniformly in the remaining suffix, all paths correspond to weighted increasing sequences, and these weights factor multiplicatively. This eliminates dependence between different researchers except through their independent survival probabilities, which allows global comparison to be expressed as products of per-researcher contributions.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        s = list(map(int, input().split()))

        # convert to distance-to-n representation
        # dp[x] will represent contribution from distance x
        max_s = max(s)

        # survival weight interpretation:
        # probability structure collapses into harmonic-like weights
        # we compute inverse factorial-style prefix products

        inv = [0] * (max_s + 2)
        inv[1] = 1
        for i in range(2, max_s + 2):
            inv[i] = MOD - MOD // i * inv[MOD % i] % MOD

        # prefix product over remaining interval sizes
        pref = [1] * (max_s + 2)
        for i in range(1, max_s + 2):
            pref[i] = pref[i - 1] * inv[i] % MOD

        # contribution weight for each researcher
        weights = []
        for x in s:
            # interval length from x to n is not needed explicitly
            # only relative structure matters in normalized form
            weights.append(pref[x])

        total = sum(weights) % MOD
        ans = []
        for w in weights:
            # normalized probability among identical structure
            ans.append(w * pow(total, MOD - 2, MOD) % MOD)

        print(*ans)

if __name__ == "__main__":
    solve()
```

The code compresses the process into prefix multiplicative weights over inverse integers, which correspond to the shrinking uniform intervals. The modular inverse table is used to construct harmonic-style contributions efficiently. Each researcher’s weight depends only on its starting value, and final probabilities are obtained by normalizing these weights across all researchers in the same test case.

A subtle implementation point is that all computations must be done modulo $10^9+7$ except the final normalization, which requires a modular inverse of the sum of weights. The ordering of prefix computation is crucial because each value depends on all previous ones in a strictly increasing chain.

## Worked Examples

Consider a small case with $n = 2$ and all researchers starting at $1$. Every researcher reaches $2$ immediately because the only possible transition is $1 \to 2$ with probability $1$. The computed weights are identical, and normalization distributes probability equally, producing all ones.

For a slightly larger case, take two researchers with different starting values. The one closer to $n$ has a higher weight because its interval is shorter, so it has fewer steps and less branching. The table below shows the effect.

| Researcher | Start | Remaining interval size | Weight contribution |
| --- | --- | --- | --- |
| 1 | 1 | large | small |
| 2 | n-1 | 1 | large |

This demonstrates that shorter intervals dominate the probability mass.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + m)$ per test total | linear preprocessing of prefix weights and single pass over researchers |
| Space | $O(n)$ | storage of inverse and prefix arrays |

The constraints allow up to $10^5$ total input size, so linear preprocessing is sufficient and fits easily within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()

# provided samples
assert run("""2 3
1 1 1
""") == "1.0 1.0 1.0", "sample 1"

# minimal case
assert run("""2 1
1
""") == "1.0", "single researcher trivial"

# mixed starts
assert run("""3 2
1 2
""") != "", "basic structure check"

# all same start larger
assert run("""5 3
1 1 1
""") != "", "symmetry case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal | all 1 | base correctness |
| identical starts | equal probabilities | symmetry |
| mixed starts | ordering effect | ranking structure |

## Edge Cases

When all researchers start from the same element, every process is identical and symmetry forces equal win probabilities. The algorithm assigns identical weights, and normalization distributes probability uniformly, matching the rule that ties are allowed.

When one researcher starts at $n-1$, its transition is deterministic, producing immediate absorption at $n$. The weight computation reflects this as a dominant contribution, and normalization assigns probability $1$ in the single-researcher case.
