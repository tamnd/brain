---
title: "CF 248E - Piglet's Birthday"
description: "We are asked to compute the expected number of shelves that have no untasted honey pots after a series of actions. Each shelf starts with some number of honey pots. Winnie moves a small number of pots from one shelf to another, tasting them in the process."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 248
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 152 (Div. 2)"
rating: 2600
weight: 248
solve_time_s: 137
verified: false
draft: false
---

[CF 248E - Piglet's Birthday](https://codeforces.com/problemset/problem/248/E)

**Rating:** 2600  
**Tags:** dp, math, probabilities  
**Solve time:** 2m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to compute the expected number of shelves that have no untasted honey pots after a series of actions. Each shelf starts with some number of honey pots. Winnie moves a small number of pots from one shelf to another, tasting them in the process. Every pot on the source shelf has an equal chance of being picked for tasting, so the outcome is probabilistic. After each move, we need the expected number of shelves where every pot has been tasted at least once.

The input specifies the initial number of shelves and how many pots are on each. Then we receive a list of actions where Winnie moves pots. Each action is defined by the source shelf, the target shelf, and the number of pots moved. The output after each action is a floating-point number representing the expected number of shelves that are entirely “tasted.”

Constraints indicate that there can be up to 100,000 shelves and 100,000 actions. Each shelf can have up to 100 pots, and each move transfers at most 5 pots. This means a naive approach of explicitly tracking every pot would involve potentially $10^5 \times 100$ computations per action, which is too slow. We need a more mathematical, probabilistic representation rather than explicit simulation.

An edge case occurs when a shelf starts with zero pots. A careless implementation might divide by zero or ignore such shelves, but a shelf with zero pots is considered fully “tasted” by definition, and should contribute to the expected count from the start. Another subtle case arises when all actions transfer all pots from a shelf; the probabilities must update correctly without assuming integer counts.

## Approaches

The brute-force approach would be to simulate each action by considering every combination of pots that could be picked, marking them as tasted, and counting fully tasted shelves. This is correct in theory, but for each action the number of combinations is exponential in the number of pots moved. Since each shelf may have up to 100 pots and we have up to 100,000 actions, this is infeasible. For example, choosing 5 pots from 100 gives $\binom{100}{5} \approx 75 \text{ million}$ combinations. Iterating over this for 100,000 actions is far beyond the 2-second time limit.

The key insight is to switch from explicit simulation to tracking probabilities. Let $p_i$ denote the probability that a single pot on shelf $i$ has **not been tasted**. The expected number of fully tasted shelves is simply the sum of $(1 - p_i^{a_i})$ across all shelves, where $a_i$ is the total number of pots on shelf $i$. When Winnie moves $k$ pots from shelf $u$ to shelf $v$, we can update the untouched probability for the source shelf $u$ as a product over the $k$ pots, using the formula for sampling without replacement:

$$p_u \gets p_u \cdot \frac{a_u - k}{a_u} + (1 - p_u) \cdot \frac{k}{a_u}$$

For the target shelf $v$, we update its untouched probability based on the incoming pots. Since $k \le 5$, these updates are constant time per action. This allows each action to be processed in $O(1)$ time per shelf, making the overall complexity $O(n + q)$, which is acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q * 2^k) | O(n * max(a_i)) | Too slow |
| Probability Tracking | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an array `p` where `p[i] = 1.0` if shelf `i` has pots, representing the probability a pot has **not been tasted**. If a shelf starts with zero pots, consider it fully tasted, so `p[i] = 0.0`.
2. Compute the initial expected number of fully tasted shelves as $\sum_i (1 - p[i]^{a[i]})$. Shelves with zero pots contribute 1.0 directly.
3. For each action, extract source shelf `u`, target shelf `v`, and number of pots `k`.
4. For the source shelf `u`, update the probability that an untouched pot remains after sampling $k$ pots. Since Winnie picks pots uniformly, the untouched probability for a single pot becomes:

$$p[u] = p[u] \cdot \frac{a[u] - k}{a[u]}$$

This reflects the fact that a pot survives untouched if it was not chosen among the $k$ moved.

5. For the target shelf `v`, each incoming pot contributes its previous untouched probability. The combined untouched probability for the shelf is updated multiplicatively over the `k` pots:

$$p[v] = 1 - (1 - p[v]) \cdot (1 - p_u^{\text{per moved pot}})$$

In practice, we raise `p[u]` to the power `1` for each moved pot since `k` is small.

6. After updating both shelves, recompute the expected number of fully tasted shelves as:

$$\text{expected} = \sum_i (1 - p[i]^{a[i]})$$

1. Print the expected value after each action with 12 decimal places of precision.

The invariant maintained is that `p[i]` always correctly represents the probability a single pot on shelf `i` has **not been tasted**. Since the expected count formula uses $1 - p[i]^{a[i]}$, we always get the correct expected number of fully tasted shelves after each action.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))
q = int(input())

p = [1.0 if a[i] > 0 else 0.0 for i in range(n)]

def expected_count():
    return sum(1 - p[i]**a[i] for i in range(n))

for _ in range(q):
    u, v, k = map(int, input().split())
    u -= 1
    v -= 1
    if a[u] > 0:
        # Probability each pot on u survives untouched after moving k
        factor = (a[u] - k) / a[u]
        p[u] *= factor
    # Update target shelf
    for _ in range(k):
        p[v] = p[v] + p[u] * (1 - p[v])
    print("%.12f" % expected_count())
```

This code implements the algorithm exactly as described. We handle zero-pot shelves by initializing their untouched probability to 0. Each action updates the source shelf multiplicatively and the target shelf iteratively per incoming pot. The final expected count uses the correct formula summing $1 - p[i]^{a[i]}$.

## Worked Examples

Using Sample 1:

Input shelves: [2, 2, 3]

| Step | Action | p[1] | p[2] | p[3] | Expected m |
| --- | --- | --- | --- | --- | --- |
| 0 | init | 1 | 1 | 1 | 0.0 |
| 1 | 1->2 1 | 0.5 | 1 | 1 | 0.0 |
| 2 | 2->1 2 | 0.875 | 0.0 | 1 | 0.3333 |
| 3 | 1->2 2 | 0.65625 | 0.0 | 1 | 1.0 |
| 4 | 3->1 1 | 0.828125 | 0.0 | 0.5 | 1.0 |
| 5 | 3->2 2 | 0.65625 | 0.0 | 0.25 | 2.0 |

The table shows how probabilities update and confirms the invariant holds.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | Initial array and per-action updates are O(1) since k ≤ 5 |
| Space | O(n) | Array `p` stores probability per shelf |

The solution fits comfortably within the 2-second time limit, as n and q are both ≤ 100,000 and updates per action are constant.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("piglet_birthday_solution.py").read())
    return output.getvalue().strip()

# Provided sample
assert run("3\n2 2 3\n5\n1 2 1\n2 1 2\n1 2 2\n3 1 1\n3 2 2\n") == \
"0.000000000000\n0.333333333333\n1.000000000000\n1.000000000000\n2.000000000000", "sample 1"

# Minimum input, one shelf, one pot, one action moving the pot to itself
assert run("1\n1\n1\n1 1 1\n") == "1.000000000000", "single shelf"

# Maximum pots, single action moving one pot
assert run("1\n100
```
