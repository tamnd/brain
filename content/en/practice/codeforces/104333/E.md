---
title: "CF 104333E - A Random Traveller"
description: "We are repeatedly picking a city uniformly at random from the set of $n$ cities, and each time we pick a city we pay its associated cost. The process stops only when every city has been seen at least once."
date: "2026-07-01T18:55:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104333
codeforces_index: "E"
codeforces_contest_name: "Replay of BU - PSTU Programming club collaborative contest"
rating: 0
weight: 104333
solve_time_s: 65
verified: true
draft: false
---

[CF 104333E - A Random Traveller](https://codeforces.com/problemset/problem/104333/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are repeatedly picking a city uniformly at random from the set of $n$ cities, and each time we pick a city we pay its associated cost. The process stops only when every city has been seen at least once. The question is not about the number of steps, but about the total expected cost accumulated until all distinct cities have appeared.

Each time we “draw” a city, we pay its cost immediately, even if we have seen it before. This means the total cost is the sum of costs of all samples in a random process that continues until the full set of indices is covered.

The difficulty is that the stopping time depends on randomness, and the cost of each draw depends on which city is selected. This makes the expected value nontrivial, because the number of times each city is visited before termination is not independent.

The constraints allow $n$ up to $10^5$, so any solution that simulates the process or tracks subsets explicitly is impossible. Even maintaining subsets over $2^n$ states or doing DP over visited sets is ruled out. A valid solution must reduce the problem to a closed-form expression or a linear-time computation over the array.

A subtle issue appears when all costs are equal. A naive approach might try to compute expected number of draws times average cost, but that fails because the stopping time and the cost accumulation are not separable in a naive way without justification.

Another corner case is $n = 1$, where the process ends immediately after one draw, so the answer is simply $a_1$. Any derived formula must collapse cleanly to this base case.

## Approaches

The brute-force mental model is to simulate the stochastic process: start with an empty set of visited cities, repeatedly pick a random index, accumulate its cost, and mark it as seen. Repeat until all cities are visited. One could try Monte Carlo simulation or full enumeration of states, but both are infeasible. Even a single simulation has expected length $n H_n$, and averaging many runs would be far beyond limits.

A more structured brute-force is to model the process as a Markov chain over subsets of visited cities. From a state $S$, the next transition adds a random city, and each transition contributes expected cost depending on selection probabilities. This leads to $O(2^n)$ states, which is immediately impossible.

The key observation is to decouple “when the process ends” from “how often each city is paid”. Instead of reasoning about subsets, we analyze contributions city by city. Each city contributes its cost every time it is drawn, and we only need the expected number of times each city appears before the process stops.

This suggests focusing on expected visit counts. A standard trick for coupon-collector-like stopping conditions is to condition on the last newly discovered city. Instead of tracking full history, we consider the moment when the final unseen city is discovered. The probability structure of that event allows us to express expected counts using symmetry over permutations of discovery order.

Once we switch perspective to ordering, each permutation of cities can be seen as the order in which cities are first discovered. The stopping time corresponds to the last element in this permutation being discovered. This converts the problem into reasoning over ranks in random permutations and geometric waiting times between discoveries.

The final transformation yields a linear expression in the costs, where each $a_i$ is multiplied by the expected number of times city $i$ is drawn before it becomes irrelevant in the covering process. That expectation depends only on its position among subsets of unseen elements, leading to a harmonic structure.

This reduces the problem to computing a single harmonic-weighted sum over all cities.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Simulation / Markov DP | Exponential | Exponential | Too slow |
| Contribution + harmonic analysis | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Observe that the process continues until all cities are seen at least once, so we are dealing with a full coverage event over uniform random sampling.
2. Instead of tracking subsets of visited cities, focus on the moment each city is first discovered. The order of first appearances forms a random permutation of all cities, which is uniformly distributed over all $n!$ possibilities.
3. For a fixed city $i$, consider its contribution to the total cost. Every time it is drawn before the process ends, it adds $a_i$ to the total. So we want the expected number of times city $i$ is sampled before the last unseen city is discovered.
4. Condition on the event that city $i$ is the $k$-th new city to appear in the discovery order. Before this happens, there are $k-1$ already discovered cities and $n-k+1$ unseen cities including $i$. The process continues drawing until $i$ appears for the first time.
5. While $i$ is unseen, every draw hits an unseen city with probability $\frac{n-k+1}{n}$. The waiting time until discovering a new city among the unseen set contributes a geometric expectation of $\frac{n}{n-k+1}$. This determines how long $i$ remains unseen and thus how many total draws occur before it contributes its first appearance.
6. Summing over all possible ranks $k$, weighted uniformly because all permutations are equally likely, yields that each city contributes an expected factor equal to the $n$-th harmonic number $H_n$.
7. Therefore the expected total cost becomes $H_n \cdot \sum a_i$.
8. Compute the harmonic number modulo $10^9+7$ as $H_n = \sum_{i=1}^n i^{-1}$, and multiply by the sum of costs.

### Why it works

The process is symmetric across all cities, and the only structure that matters is how many unseen cities remain when a draw occurs. Each city behaves identically under relabeling, so its expected number of appearances before full coverage depends only on the decreasing pool size of unseen elements. This reduces the problem to a coupon collector structure where each phase contributes an expected $\frac{n}{k}$ steps for $k$ remaining unseen elements. Linearity of expectation allows summing contributions independently, ensuring the total expectation decomposes cleanly into a product of the total cost and the harmonic number.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def modinv(x):
    return pow(x, MOD - 2, MOD)

n = int(input())
a = list(map(int, input().split()))

S = sum(a) % MOD

H = 0
for i in range(1, n + 1):
    H = (H + modinv(i)) % MOD

print((S * H) % MOD)
```

The implementation directly follows the derived formula. The only nontrivial part is computing modular inverses for all integers up to $n$, since the harmonic number is defined as a sum of reciprocals under modular arithmetic.

The sum of costs is computed once. Then we accumulate $H_n$ using modular inverses. Finally, we multiply both values.

A common mistake is attempting to simulate the stochastic process, which would never finish within constraints. Another mistake is forgetting that division must be handled via modular inverse rather than integer division.

## Worked Examples

### Example 1

Input:

```
3
1 2 3
```

We compute $\sum a_i = 6$.

We compute:

$H_3 = 1 + 1/2 + 1/3 = 1 + 500000004 + 333333336 = 833333341$

| Step | Value |
| --- | --- |
| sum(a) | 6 |
| H_1 | 1 |
| H_2 | 500000004 |
| H_3 | 833333341 |
| result | 6 × 833333341 |

Final answer is $11$.

This demonstrates modular arithmetic cancellation and confirms the harmonic accumulation matches the expected closed form.

### Example 2

Input:

```
1
5
```

We have only one city, so:

$H_1 = 1$

| Step | Value |
| --- | --- |
| sum(a) | 5 |
| H_1 | 1 |
| result | 5 |

The process always stops after one draw, so the cost is exactly the single value, matching the formula.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | One pass to sum costs and one pass to compute harmonic sum |
| Space | $O(1)$ | Only a few accumulators are used |

The solution easily fits within constraints since $n = 10^5$ allows linear iteration comfortably, and modular exponentiation is constant time per value in practice.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    S = sum(a) % MOD
    def inv(x): return pow(x, MOD-2, MOD)
    H = 0
    for i in range(1, n+1):
        H = (H + inv(i)) % MOD
    return str((S * H) % MOD)

# provided samples
assert run("3\n1 2 3\n") == "11", "sample 1"
assert run("1\n5\n") == "5", "sample 2"

# custom cases
assert run("2\n1 1\n") == "3", "minimum nontrivial case"
assert run("4\n1 2 3 4\n") == str((10 * sum(pow(i, MOD-2, MOD) for i in range(1,5))) % MOD), "manual harmonic check"
assert run("5\n5 5 5 5 5\n") == str((25 * sum(pow(i, MOD-2, MOD) for i in range(1,6))) % MOD), "uniform costs"
assert run("1\n100000\n") == "100000", "single element large value"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | 3 | smallest multi-city case |
| `1 2 3 4` | harmonic-based | correctness of summation |
| `5 × identical` | scaled harmonic | uniform cost scaling |
| `n=1 large` | direct cost | base termination case |

## Edge Cases

When $n = 1$, the process never loops. The harmonic number $H_1 = 1$, so the formula reduces directly to $a_1$. The algorithm computes sum $= a_1$ and multiplies by $1$, producing the correct output without special casing.

When all $a_i$ are equal, say all are $c$, the expected value becomes $c \cdot n \cdot H_n$. The implementation handles this correctly because the cost sum becomes $n \cdot c$, and the harmonic factor remains unchanged.

When $n$ is large, the harmonic sum is still computed in linear time, and modular inverses are safe since the modulus is prime and all denominators are invertible.
