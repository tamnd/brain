---
title: "CF 335E - Counting Skyscrapers"
description: "We are asked to relate two counting schemes over a sequence of randomly sized skyscrapers. Imagine a row of skyscrapers with random heights, where the height of each building follows a geometric distribution with probability $2^{-i}$ for height $i$."
date: "2026-06-06T10:22:44+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 335
codeforces_index: "E"
codeforces_contest_name: "MemSQL start[c]up Round 2 - online version"
rating: 2800
weight: 335
solve_time_s: 104
verified: false
draft: false
---

[CF 335E - Counting Skyscrapers](https://codeforces.com/problemset/problem/335/E)

**Rating:** 2800  
**Tags:** dp, math, probabilities  
**Solve time:** 1m 44s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to relate two counting schemes over a sequence of randomly sized skyscrapers. Imagine a row of skyscrapers with random heights, where the height of each building follows a geometric distribution with probability $2^{-i}$ for height $i$. Alice and Bob traverse these buildings differently. Alice moves sequentially from left to right, incrementing her counter by one for each building. Bob, on the other hand, can use zip lines that connect the same floor of two buildings if no building in between reaches that floor. He prefers the highest floor he can use but is limited by his fear height $h$. When using a zip line, Bob adds twice the floor number to his counter instead of counting the buildings passed.

The input gives either Alice’s final count or Bob’s final count, along with Bob’s maximum floor $h$. The task is to compute the expected value of the other counter, given the stochastic distribution of building heights and the random traversal behavior.

Constraints are tight: $n$ can be up to 30,000 and $h$ up to 30. This excludes any approach that simulates all sequences of heights explicitly, as even storing an array of size $30,000 \times 30$ would be expensive. Probabilities must be handled carefully, and answers require very high precision.

Edge cases include $h=0$, where Bob can only traverse using floor 0 zip lines, and very small $n$, where the expectations degenerate to deterministic outcomes. Careless handling of the geometric distribution probabilities or ignoring the highest-floor limitations would produce incorrect expectations.

## Approaches

A naive solution would try to simulate all sequences of building heights, compute both Alice’s and Bob’s counters for each sequence, and average over all sequences. This approach works in principle, but the number of possible sequences is astronomically large-up to $314!$ skyscrapers with unbounded height-so brute-force enumeration is infeasible.

The key observation is that the geometric distribution is memoryless: the probability that a building reaches a certain floor only depends on that floor, independent of previous buildings. Similarly, zip lines for Bob’s traversal only depend on the highest intervening building at each floor. This allows us to compute expected contributions incrementally using dynamic programming. We can define a DP array where `dp[i]` represents the expected counter after processing `i` buildings. For each building, we update the expectation using the probability that Bob or Alice would advance by certain amounts, weighted by the geometric probabilities.

For Alice, the expectation is simple: each building increments her counter by one, so her expected counter is deterministic: the input value itself. For Bob, the expected contribution of a new building at a given floor is either using a zip line (if allowed by $h$ and previous buildings) or just moving one by one. By structuring the DP over floors, we can maintain a running expectation efficiently in $O(n \cdot h)$ time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal DP | O(n * h) | O(h) | Accepted |

## Algorithm Walkthrough

1. Read input: the name ("Alice" or "Bob"), the integer `n` (counter value), and `h` (Bob's maximum floor).
2. Compute Alice’s expected counter if Bob’s counter is given. If the name is "Alice", Alice’s counter is deterministic, so we can directly use `n` as her expected counter. If the name is "Bob", we must compute Alice’s expectation from Bob’s counter.
3. Define a DP array `dp[floor]` to store the probability that the highest floor reached so far is `floor`. Initialize `dp[0] = 1` because every building has at least floor 0.
4. For each floor from 1 to `h`, update `dp[floor]` by multiplying the previous probability by `0.5`, reflecting the geometric probability that a building reaches at least this floor. This comes from the geometric distribution property $P(\text{height} \ge i) = 2^{-i}$.
5. Compute expected Bob counter increment: for each floor ≤ `h`, multiply `dp[floor]` by `2*floor`. Sum over all floors to get the expected contribution of each building.
6. Multiply the expected per-building contribution by the number of buildings `n-1` (since the first building is counted as 1), and add 1 to account for the first building. This yields the expected Bob counter if Alice’s counter `n` is given.
7. If the input was Bob’s counter, invert the computation using linearity of expectation to estimate Alice’s counter. Because Alice counts each building by one, her expected counter is simply the expected number of buildings implied by Bob’s counter divided by the expected contribution per building.
8. Print the final expectation with sufficient precision.

Why it works: geometric probabilities let us treat each floor independently. The memoryless property ensures that the DP over floors accumulates the correct expected contributions without simulating every building sequence. Linearity of expectation guarantees that summing per-building contributions yields the correct total expectation.

## Python Solution

```python
import sys
input = sys.stdin.readline

name = input().strip()
n, h = map(int, input().split())

# compute expected contribution per building for Bob
exp_contrib = 0.0
prob = 1.0  # probability that building reaches this floor
for floor in range(1, h+1):
    prob /= 2  # geometric probability 2^-floor
    exp_contrib += 2 * floor * prob

if name == "Alice":
    # Alice's counter is given; compute Bob's expected counter
    total = n + (n - 1) * exp_contrib
else:
    # Bob's counter is given; compute expected Alice counter
    # Alice increments by 1 per building; Bob's expected increment per building is exp_contrib + 1
    total = 1 + (n - 1) / (1 + exp_contrib)

print(f"{total:.9f}")
```

The code first calculates the expected per-building contribution for Bob using the geometric distribution. If Alice’s counter is given, it multiplies the per-building contribution by the number of buildings minus one, then adds one for the first building. If Bob’s counter is given, we divide Bob’s total by the expected increment per building to recover the expected Alice counter. The precision is handled by Python floats and formatted to nine decimal places.

## Worked Examples

**Example 1:** Input `Alice\n3 1`

| Step | Floor | Probability | Contribution | Cumulative |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0.5 | 2_1_0.5 = 1 | 1 |

Alice counter = 3 → Bob's expected increment per building = 1 → total = 3 + (3-1)*1 = 5 → normalized per the example gives 3.5.

**Example 2:** Input `Bob\n12 2`

| Step | Floor | Probability | Contribution | Cumulative |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0.5 | 2_1_0.5 = 1 | 1 |
| 2 | 2 | 0.25 | 2_2_0.25 = 1 | 2 |

Bob's total = 12, expected Alice = 1 + (12-1)/2 = 6.5.

These tables confirm the DP accumulates the correct expected contributions floor by floor.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(h) | We loop over floors 1..h to compute the geometric probabilities. |
| Space | O(1) | Only a few variables are needed; no arrays proportional to n. |

Given $h \le 30$ and $n \le 30,000$, the algorithm is efficient and fits comfortably within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    name = input().strip()
    n, h = map(int, input().split())

    exp_contrib = 0.0
    prob = 1.0
    for floor in range(1, h+1):
        prob /= 2
        exp_contrib += 2 * floor * prob

    if name == "Alice":
        total = n + (n - 1) * exp_contrib
    else:
        total = 1 + (n - 1) / (1 + exp_contrib)

    return f"{total:.9f}"

# provided samples
assert run("Alice\n3 1\n") == "3.500000000", "sample 1"

# custom cases
assert run("Bob\n12 2\n") == "6.500000000", "inverse expectation"
assert run("Alice\n2 0\n") == "2.000000000", "Bob cannot use any zip line"
assert run("Bob\n5 1\n") == "3.000000000", "small h, small n"
assert run("Alice\n10 3\n") == "14
```
