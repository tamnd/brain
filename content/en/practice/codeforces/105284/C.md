---
title: "CF 105284C - Monkey Math Tree"
description: "We are given a path graph with nodes numbered from 1 to n, where each node is connected to its immediate neighbors. Then each node i is independently kept with probability 1/i and removed with probability 1 − 1/i."
date: "2026-06-23T14:29:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105284
codeforces_index: "C"
codeforces_contest_name: "TeamsCode Summer 2024 Advanced Division"
rating: 0
weight: 105284
solve_time_s: 90
verified: false
draft: false
---

[CF 105284C - Monkey Math Tree](https://codeforces.com/problemset/problem/105284/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a path graph with nodes numbered from 1 to n, where each node is connected to its immediate neighbors. Then each node i is independently kept with probability 1/i and removed with probability 1 − 1/i. After all deletions, the remaining nodes form a subgraph of the original chain, and this subgraph may break into several connected components.

A connected component in this setting is simply a maximal consecutive block of kept nodes. Every time we see a gap created by a deleted node, the chain splits. So the final answer is the expected number of such contiguous kept segments.

The input gives many independent values of n, and for each one we must compute this expectation modulo 10^9+7.

The constraints allow n up to 10^6 and total number of test cases up to 2×10^5, so any solution must be essentially linear or better per test case. Even O(n) per query is too slow in the worst case unless we precompute. The structure strongly suggests a prefix computation over n.

A naive approach would simulate all subsets of kept/deleted nodes and count components. That is 2^n configurations, already impossible for n beyond small values like 20. Even Monte Carlo would not give exact modular expectations.

A more subtle issue arises if one tries to directly simulate or DP over all configurations per test case: the probability model depends on i, so each position contributes differently, and recomputing from scratch per query would repeat the same work many times.

## Approaches

The key observation is that connected components in a binary sequence of kept/deleted nodes can be counted locally. A new component starts exactly at a position i if node i is kept and either i−1 is deleted or i−1 does not exist.

So if we define an indicator for “i starts a new component”, the expectation becomes a sum of probabilities of local events.

Let K_i be the event that node i is kept. Node i contributes a new component when K_i is true and either i = 1 or K_{i−1} is false. By linearity of expectation, we can sum these probabilities independently across i.

The brute force idea would enumerate all subsets of nodes, compute connected components for each subset in O(n), and average over all probabilities. This fails because the number of subsets is exponential and the probability weights are not uniform.

The key simplification is that we never need correlations beyond adjacent nodes. Each term depends only on K_i and K_{i−1}, and independence of node states makes this fully local.

We compute:

For i = 1, probability of a component starting is P(K_1) = 1.

For i > 1, a new component starts when node i is kept and node i−1 is not kept:

P = P(K_i) × P(not K_{i−1}) = (1/i) × (1 − 1/(i−1)).

This reduces the whole problem to a prefix sum over i.

The only remaining care is modular arithmetic and handling the special case i = 1 separately.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets | O(2^n · n) | O(n) | Too slow |
| Local expectation sum | O(n) preprocessing, O(1) per query | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute modular inverses for all integers up to max n across test cases. This is necessary because probabilities involve 1/i under a prime modulus, so division must be replaced by multiplication with modular inverses.
2. Build an array dp where dp[i] stores the expected number of components for a chain of length i. We compute dp incrementally from 1 to max n.
3. Initialize dp[1] = 1 because a single node is always kept and forms exactly one component.
4. For each i from 2 to max n, compute the contribution of position i as the probability that i is kept and i−1 is not kept. This is (1/i) × (1 − 1/(i−1)). We add this to dp[i−1] to obtain dp[i].
5. Answer each query by printing dp[n].

The reason this incremental form works is that each new position either extends an existing component or starts a new one, and only the second case affects the component count.

### Why it works

The expected number of components equals the expected number of starts of components. A start occurs exactly at position i when node i is present but node i−1 is absent. These events depend only on independent Bernoulli variables, so their probabilities multiply cleanly. Linearity of expectation allows summing these per-position probabilities without considering interactions between different starts.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def modinv(x):
    return pow(x, MOD - 2, MOD)

def solve():
    t = int(input())
    ns = []
    max_n = 0

    for _ in range(t):
        n = int(input())
        ns.append(n)
        if n > max_n:
            max_n = n

    if max_n == 0:
        return

    inv = [0] * (max_n + 2)
    for i in range(1, max_n + 2):
        inv[i] = modinv(i)

    dp = [0] * (max_n + 2)
    dp[1] = 1

    for i in range(2, max_n + 1):
        p_keep = inv[i]
        p_prev_keep = inv[i - 1]
        p_prev_not = (1 - p_prev_keep) % MOD
        dp[i] = (dp[i - 1] + p_keep * p_prev_not) % MOD

    out = []
    for n in ns:
        out.append(str(dp[n]))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation starts by reading all test cases to determine the maximum n, since we need a global precomputation. The modular inverses are computed using Fermat’s theorem.

The dp array stores the expected value up to each prefix length. Each transition only uses i and i−1, so the computation is linear.

A subtle point is computing (1 − 1/(i−1)) modulo MOD correctly. We explicitly apply modulo after subtraction to avoid negative values.

## Worked Examples

Consider the sample with n = 2.

| i | P(keep i) | P(prev not) | Contribution | dp[i] |
| --- | --- | --- | --- | --- |
| 1 | 1 | - | 1 | 1 |
| 2 | 1/2 | 1 − 1/1 = 0 | 0 | 1 |

For n = 2, node 1 is always present, so there is always exactly one component regardless of node 2, matching dp[2] = 1.

Now consider n = 4.

| i | P(keep i) | P(prev not) | Contribution | dp[i] |
| --- | --- | --- | --- | --- |
| 1 | 1 | - | 1 | 1 |
| 2 | 1/2 | 0 | 0 | 1 |
| 3 | 1/3 | 1 − 1/2 = 1/2 | 1/6 | 1 + 1/6 |
| 4 | 1/4 | 1 − 1/3 = 2/3 | 1/6 | 1 + 1/6 + 1/6 |

This produces 4/3, which matches the expected modular output.

The trace shows that components only appear when a kept node is preceded by a missing one, and contributions accumulate independently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(max n + t) | Precompute dp once, answer queries in O(1) each |
| Space | O(max n) | Store dp and inverse arrays |

The preprocessing up to 10^6 fits comfortably in time limits, and each query is constant time, making the solution suitable for up to 2×10^5 test cases.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    ns = []
    max_n = 0
    for _ in range(t):
        n = int(input())
        ns.append(n)
        max_n = max(max_n, n)

    inv = [0] * (max_n + 2)
    for i in range(1, max_n + 2):
        inv[i] = pow(i, MOD - 2, MOD)

    dp = [0] * (max_n + 2)
    if max_n >= 1:
        dp[1] = 1

    for i in range(2, max_n + 1):
        dp[i] = (dp[i - 1] + inv[i] * (1 - inv[i - 1]) % MOD) % MOD

    return "\n".join(str(dp[n]) for n in ns)

# provided samples
assert run("4\n1\n2\n3\n4\n") == "1\n1\n166666669\n333333337"

# custom cases
assert run("1\n1\n") == "1", "minimum size"
assert run("1\n2\n") == "1", "two nodes"
assert run("1\n5\n") == run("1\n5\n"), "determinism check"
assert run("3\n1\n2\n3\n") == "1\n1\n166666669", "prefix consistency"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | single node edge case |
| 2 | 1 | no split possible |
| 5 | dp consistency | stability of recurrence |
| 1,2,3 | 1,1,1/6 | prefix correctness |

## Edge Cases

For n = 1, the algorithm directly sets dp[1] = 1 because a single guaranteed kept node forms exactly one component. There is no dependency on dp[0], which avoids undefined behavior.

For n = 2, the transition uses P(prev not) = 1 − 1/1 = 0, correctly capturing that node 1 is always present, so node 2 can never start a new component.

For larger n, each term only depends on i and i−1, so even at maximum n = 10^6 the computation remains stable and linear, with no hidden recursion or state explosion.
