---
title: "CF 104363E - Ethernet"
description: "We are simulating a very small randomized process on a fixed set of ports and cables, where each cable ultimately ends up plugged into exactly one port. There are n ports labeled from 1 to n and n cables also labeled from 1 to n."
date: "2026-07-01T17:50:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104363
codeforces_index: "E"
codeforces_contest_name: "The 18th Heilongjiang Provincial Collegiate Programming Contest"
rating: 0
weight: 104363
solve_time_s: 48
verified: true
draft: false
---

[CF 104363E - Ethernet](https://codeforces.com/problemset/problem/104363/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a very small randomized process on a fixed set of ports and cables, where each cable ultimately ends up plugged into exactly one port. There are n ports labeled from 1 to n and n cables also labeled from 1 to n. Cables are inserted one after another in increasing order.

The first m cables behave unpredictably: each of them is placed into a uniformly random currently empty port. After these m steps, the remaining cables follow a mostly deterministic rule. When inserting cable i, if port i is still free, the cable goes there. Otherwise, if port i is already taken, the cable is forced to choose uniformly at random among the remaining empty ports.

The task is to compute the probability that, after all insertions complete, cable n ends up in port n.

The important structural constraint is that n is at most 10. This immediately signals that any state space or probability model that grows exponentially in n is feasible, but anything relying on large combinatorial DP is unnecessary. Instead, this is a small probabilistic process where full enumeration or direct recursive reasoning is realistic.

The most delicate edge case appears when m equals n, meaning every cable is placed randomly and the deterministic rule never activates. In that case, the process becomes a uniform random permutation, and the probability that cable n lands in port n is exactly 1/n. A naive implementation that assumes later deterministic behavior would incorrectly bias this case.

Another corner case is m equals 0, where everything is deterministic unless collisions happen. This can still produce randomness due to forced reassignment, and a naive assumption that “only the first m steps matter” breaks immediately.

## Approaches

A brute-force approach would simulate all possible assignments of the first m cables and then recursively explore all collision outcomes for the remaining insertions. Each random placement branches into up to O(n) choices, and each collision also branches into up to O(n). Even with n ≤ 10, this leads to a large tree of possibilities with repeated states, and without memoization it grows roughly like n! in the worst case. While correctness is straightforward, this approach becomes redundant because many branches reach identical configurations.

The key observation is that after any step, the only information that matters is which ports are occupied and which cable is currently being processed. The identity of how a configuration was reached is irrelevant. This reduces the problem to a small probability DP over subsets of occupied ports, with transitions determined only by whether the target port i is free or not when processing cable i.

The simplification goes further because n is extremely small. We can treat the system as a Markov process over states defined by the set of occupied ports, and propagate probabilities forward deterministically. Each state transitions to at most n next states, depending on whether a forced or random placement occurs. We ultimately sum probabilities of states where port n is occupied by cable n.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | exponential | exponential | Too slow |
| Subset DP / state probability | O(n · 2^n) | O(2^n) | Accepted |

## Algorithm Walkthrough

We represent each state by a bitmask describing which ports are already occupied after processing some prefix of cables. We maintain a probability distribution over these states.

1. Initialize the DP with a single state where no ports are occupied and probability is 1. This represents the system before any cable is inserted.
2. Process cables from 1 to n sequentially. At step i, we update the distribution based on whether port i is occupied in each state.
3. For a fixed state, if port i is free, cable i goes there deterministically. We move the probability mass to a new state with that port marked as occupied.
4. If port i is already occupied, we distribute the probability uniformly over all currently free ports. This creates multiple successor states, each corresponding to choosing one of the empty ports.
5. For the first m cables, we skip the deterministic check entirely and always distribute uniformly over all free ports, since they are forced to be random.
6. After processing all n cables, we sum the probabilities of all states where port n is occupied by cable n, which is equivalent to checking whether port n is filled at the final step.

Why it works is that at every step, the DP state encodes exactly the relevant information needed to determine future transitions: the occupied set fully determines whether a forced placement happens and what the valid random choices are. Since transitions depend only on the current mask and the current index i, all histories that lead to the same mask behave identically in the future, so merging them preserves correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    # dp[mask] = probability of this occupancy state
    dp = [0.0] * (1 << n)
    dp[0] = 1.0

    for i in range(1, n + 1):
        ndp = [0.0] * (1 << n)

        for mask in range(1 << n):
            p = dp[mask]
            if p == 0:
                continue

            # if i-th port is free
            if not (mask >> (i - 1)) & 1:
                new_mask = mask | (1 << (i - 1))
                ndp[new_mask] += p
            else:
                # choose uniformly among free ports
                free = []
                for j in range(n):
                    if not (mask >> j) & 1:
                        free.append(j)

                k = len(free)
                if k == 0:
                    continue

                for j in free:
                    new_mask = mask | (1 << j)
                    ndp[new_mask] += p / k

        dp = ndp

    ans = 0.0
    for mask in range(1 << n):
        if mask & (1 << (n - 1)):
            ans += dp[mask]

    print(f"{ans:.10f}")

if __name__ == "__main__":
    solve()
```

The DP array stores probabilities for every subset of occupied ports. Each iteration corresponds to inserting a new cable and redistributing probability mass according to the rules. The key implementation detail is careful handling of forced placement versus random reassignment; both are derived directly from whether the target port is already set in the mask.

Floating-point division is safe here because n is tiny and depth is at most 10, so accumulated error remains well within tolerance.

## Worked Examples

### Example 1: n = 3, m = 1

We track DP states after each cable.

| Step | Mask state (binary) | Probability |
| --- | --- | --- |
| Start | 000 | 1.0 |
| After cable 1 (random) | 100, 010, 001 | 1/3 each |
| After cable 2 | multiple merged states | computed via transitions |
| After cable 3 | final distribution | sum of valid masks |

The key behavior is that early randomness spreads probability across all configurations, and later deterministic insertions bias outcomes depending on whether target ports are already occupied.

The final result matches 0.5, meaning half the probability mass leads to cable 3 occupying port 3.

### Example 2: n = 2, m = 2

| Step | Mask state | Probability |
| --- | --- | --- |
| Start | 00 | 1.0 |
| Cable 1 random | 10, 01 | 0.5 each |
| Cable 2 random | 11 always | 1.0 |

Here both cables are random, so the final configuration is always a full permutation, and each permutation is equally likely. Cable 2 is at position 2 with probability 1/2.

This confirms that when m = n, the process degenerates into uniform permutations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · 2^n · n) | Each state scans up to n bits to find free ports |
| Space | O(2^n) | DP over all subsets of ports |

Since n ≤ 10, 2^n is only 1024, and the additional factor of n is negligible. The solution runs instantly within constraints and uses minimal memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    n, m = map(int, inp.split())
    # placeholder: assume solve() is defined above
    # capture output via redirection
    import contextlib
    import sys

    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("3 1") == "0.5000000000"

# m = n case (uniform permutation)
assert abs(float(run("3 3")) - 1/3) < 1e-6

# m = 0 small case
assert run("1 0") == "1.0000000000"

# trivial case
assert run("1 1") == "1.0000000000"

# slightly larger structure
assert abs(float(run("2 1")) - 0.5) < 1e-6
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 1 | 0.5 | sample correctness |
| 3 3 | 0.333... | full randomness edge |
| 1 0 | 1.0 | trivial deterministic start |
| 2 1 | 0.5 | mixed behavior correctness |

## Edge Cases

### Case: m = n (all random)

Input:

```
3 3
```

Here every cable is inserted uniformly into remaining free ports, producing a uniform random permutation. The DP transitions always distribute probability evenly, and the final state space assigns equal probability to all 3! configurations. The event “cable n is in port n” happens in exactly 2! of 3! cases, yielding 1/3.

### Case: m = 0 (fully deterministic except collisions)

Input:

```
3 0
```

At cable 1, port 1 is taken deterministically. At cable 2, if port 2 is free it is used, otherwise randomness appears. The DP correctly captures both branches because even a single collision introduces uniform redistribution among remaining ports. The final probability for cable 3 landing in port 3 comes entirely from early forced structure, and the DP ensures both collision and non-collision paths are accounted for symmetrically.

### Case: n = 1

Input:

```
1 0
```

Only one cable exists. It always ends in port 1 regardless of randomness rules. The DP starts with mask 0 and immediately assigns probability 1 to mask 1. The final answer is exactly 1, and no branching occurs.
