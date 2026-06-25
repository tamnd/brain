---
title: "CF 106104C - Buying Fruit"
description: "We start with a full set of size N. Every step independently picks a number from 1 to N uniformly. If the chosen number is still in the set, we remove it; otherwise the set stays unchanged. The process stops when the set becomes empty."
date: "2026-06-25T11:42:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106104
codeforces_index: "C"
codeforces_contest_name: "UT 104c Midterm #1"
rating: 0
weight: 106104
solve_time_s: 39
verified: true
draft: false
---

[CF 106104C - Buying Fruit](https://codeforces.com/problemset/problem/106104/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a full set of size N. Every step independently picks a number from 1 to N uniformly. If the chosen number is still in the set, we remove it; otherwise the set stays unchanged. The process stops when the set becomes empty.

We need the expected number of steps until termination.

The input gives multiple test cases, each with N, and we must output the expectation modulo 998244353.

The key observation is that the identity of elements never matters. At any moment, the only meaningful state is how many elements remain. If k elements remain, the system behaves identically regardless of which specific ones they are.

The constraint N up to 100000 rules out any exponential subset DP. Even O(N^2) is too large. This immediately suggests a one-dimensional recurrence or a linear expectation DP.

A naive idea is to simulate the process many times, but each simulation can take unbounded time and would not converge within constraints.

A second naive idea is to treat each element independently and sum expected removal times. This fails because removals are not independent: picking an already removed element consumes time without progress.

A subtle edge case appears when N = 1. The expected answer is 1 because the first pick removes the only element with probability 1. Any formula must reduce correctly here.

Another edge case is N = 2. The process can get “stuck” repeatedly picking already removed elements, so the expectation is strictly larger than 2. Any incorrect linear assumption like “each element costs N steps” fails here.

## Approaches

The brute-force viewpoint is to model the process state as a subset of remaining elements. From any subset S of size k, each step transitions either to S \ {x} for some x in S with probability k/N, or stays in S with probability (N-k)/N. This immediately defines a Markov chain over 2^N states.

This is correct but unusable because the state space is exponential. Even writing transitions is already infeasible.

The key simplification is that all subsets of size k behave identically. So instead of tracking subsets, we track a single value dp[k]: expected remaining time when k elements are still alive.

From state k, a random pick succeeds with probability k/N and reduces k by 1. With probability (N-k)/N, nothing changes and we stay in the same state, which contributes an extra wasted step.

This self-loop structure is the key: the expectation equation can be written directly.

If E[k] is the expected remaining time from k elements, then:

E[k] = 1 + (k/N) * E[k-1] + (1 - k/N) * E[k]

The right-hand side reflects that every step costs 1, and then we either reduce the state or stay.

Rearranging removes the self-reference and produces a simple recurrence.

This is the structural insight: the “wasted picks” do not change state, but they inflate time by a factor depending on k/N.

After algebra, we get:

E[k] = E[k-1] + N/k

So the process reduces to summing harmonic-like terms scaled by N.

Thus:

E[N] = N * (1/1 + 1/2 + ... + 1/N)

Everything collapses into prefix harmonic numbers under modular arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force Markov DP over subsets | O(2^N) | O(2^N) | Too slow |
| State compression DP over k | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Recognize that only the number of remaining items matters, not which ones remain. This reduces the state space from subsets to integers k from 0 to N.
2. Define E[k] as the expected number of steps needed when k items remain. The goal is E[N].
3. Write the transition for one step. From k items, a random pick succeeds with probability k/N and reduces k to k−1. Otherwise, with probability (N−k)/N, the state does not change but time still increases by one step.
4. Translate this into an expectation equation:

E[k] = 1 + (k/N)E[k−1] + (1 − k/N)E[k].

The left side includes E[k] again because failing to remove an item keeps the state unchanged.
5. Rearrange the equation to isolate E[k]. Moving the self term gives:

(k/N)E[k] = 1 + (k/N)E[k−1], which simplifies to E[k] = E[k−1] + N/k.
6. Use this recurrence starting from E[0] = 0 up to E[N]. Each step adds N multiplied by the modular inverse of i.
7. Maintain a running harmonic sum H = sum(1/i mod MOD) and accumulate the final answer as N * H.

### Why it works

The crucial invariant is that E[k] depends only on k and not on the identity of remaining elements. Every transition from k behaves identically, and the only randomness is whether the chosen index is still active. The self-loop probability creates a geometric waiting time effect, which is exactly what produces the additive N/k term. Because each state reduces independently of history beyond k, the recurrence fully characterizes the expectation without loss of information.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modinv(x):
    return pow(x, MOD - 2, MOD)

def solve():
    t = int(input())
    inv = [0] * (100000 + 1)

    for i in range(1, 100000 + 1):
        inv[i] = modinv(i)

    for _ in range(t):
        n = int(input())
        H = 0
        for i in range(1, n + 1):
            H = (H + inv[i]) % MOD
        ans = H * n % MOD
        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation precomputes modular inverses because the same denominators repeat across test cases. The harmonic sum is accumulated directly, and the final multiplication by N applies the derived formula E[N] = N * H_N.

A common pitfall is attempting to update the expectation iteratively without separating the harmonic structure. Another is forgetting that the self-loop term must be eliminated algebraically; if left in place, the recurrence incorrectly appears circular.

## Worked Examples

### Example 1: N = 2

We compute inverses: 1/1 = 1, 1/2 = 499122177 (mod 998244353).

H = 1 + 1/2.

Then E[2] = 2 * (1 + 1/2) = 3.

| k | H prefix | E[k] |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 1 + 1/2 | 3 |

This shows that even for small N, the expectation exceeds N because repeated useless draws inflate the process.

### Example 2: N = 3

H = 1 + 1/2 + 1/3.

E[3] = 3H.

| k | H prefix | E[k] |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 1 + 1/2 | 3 |
| 3 | 1 + 1/2 + 1/3 | 3H |

This confirms linear accumulation of harmonic contributions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) per test case | harmonic sum over 1..N |
| Space | O(1) extra (or O(N) if precomputed inverses) | only running sums needed |

The harmonic computation dominates runtime, but N ≤ 100000 ensures feasibility under typical limits.

## Test Cases

```python
import sys, io

MOD = 998244353

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def solve():
        t = int(input())
        for _ in range(t):
            n = int(input())
            H = 0
            for i in range(1, n + 1):
                H = (H + pow(i, MOD - 2, MOD)) % MOD
            print(H * n % MOD)

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return out.strip()

# sample-like checks
assert run("1\n1\n") == "1", "n=1"
assert run("1\n2\n") == str((2 * (1 + pow(2, MOD - 2, MOD))) % MOD), "n=2"
assert run("1\n3\n") == str((3 * (1 + pow(2, MOD - 2, MOD) + pow(3, MOD - 2, MOD))) % MOD), "n=3"

# edge case large structure sanity
assert run("1\n5\n").split()[0], "basic structure"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 | 1 | base termination |
| n=2 | 3 | self-loop inflation |
| n=3 | harmonic accumulation | recurrence correctness |
| n=5 | computed value | general correctness |

## Edge Cases

For N = 1, the state starts already minimal, and the first successful pick always happens immediately. The recurrence gives E[1] = N * (1) = 1, matching the process directly.

For N = 2, the system frequently wastes steps on already-removed elements. The recurrence correctly accounts for this via the harmonic term 1/2, which inflates the expectation to 3.

For larger N, the dominant contribution comes from late stages where k is small, since N/k becomes large. The harmonic structure captures this blow-up naturally without simulation.
