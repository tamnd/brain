---
title: "CF 103186E - Zztrans \u7684\u5e84\u56ed"
description: "We are simulating a simplified fishing system where each cast produces exactly one fish according to a known probability distribution over fish types."
date: "2026-07-03T16:12:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103186
codeforces_index: "E"
codeforces_contest_name: "The 2021 Shanghai Collegiate Programming Contest"
rating: 0
weight: 103186
solve_time_s: 48
verified: true
draft: false
---

[CF 103186E - Zztrans \u7684\u5e84\u56ed](https://codeforces.com/problemset/problem/103186/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a simplified fishing system where each cast produces exactly one fish according to a known probability distribution over fish types. Each fish type belongs to one of five rarity classes, and each class has a fixed selling value, except for the highest rarity which is valued differently.

Each fishing attempt costs a fixed amount of bait, so every cast produces a net gain equal to the value of the caught fish minus this cost. The player performs a fixed number of independent casts, and we are asked to compute the expected total profit.

The input gives a list of fish types, each with a rarity label and a probability of being caught. The probabilities sum to 1, so each cast always produces exactly one fish drawn from this distribution.

The output is the expected profit after k casts, where profit includes both the fish selling value and the deduction of bait cost per cast.

The constraints n ≤ 100 and k ≤ 100 immediately indicate that even O(nk) or O(n) per state methods are easily fast enough. There is no need for simulation or dynamic programming over complex states, since each cast is independent and identically distributed. This strongly suggests that linear expectation properties will collapse the entire problem into a single expected value per cast multiplied by k.

A subtle point is that the “legendary fish” category overrides its usual value. Even though all probabilities are independent and identical, forgetting to replace the value for S-type fish would produce a consistent but incorrect expectation.

Another potential pitfall is floating-point accumulation error if one tries to simulate k steps repeatedly with repeated summation. Since k is small, both approaches work, but repeated multiplication is unnecessary and less stable than computing a single expectation.

## Approaches

A naive interpretation of the process is to simulate each of the k fishing attempts independently. For each attempt, we sample a fish according to the given distribution, add its value, subtract bait cost, and repeat. The expected value could be approximated by Monte Carlo simulation, but that would introduce randomness and error, and is unnecessary given deterministic probabilities.

A deterministic brute-force expectation approach would explicitly compute the expected gain of one cast by summing over all fish types, multiplying probability by value, and then subtracting bait cost. After that, one would repeat this computation k times or multiply the single-cast expectation by k.

The key observation is linearity of expectation. Each fishing attempt is independent, and the total reward is a sum of k identical random variables. Therefore, the total expected reward is simply k times the expected reward of one cast. No joint distribution or state tracking is required.

This reduces the entire problem to computing a single weighted average over fish values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Simulation | O(k · samples) | O(1) | Too slow / imprecise |
| Expected value per cast | O(n + k) | O(1) | Accepted |
| Optimized (multiply expectation) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. Read all fish types and their probabilities, and group them by rarity value mapping.

We need to translate each rarity character into its monetary value. The only non-standard rule is that S-type fish uses 10000 instead of 100.
2. For each fish type, compute its contribution to expected value as probability multiplied by its assigned value.

This directly follows from the definition of expectation: each outcome contributes value weighted by its likelihood.
3. Sum all contributions to obtain the expected value of a single fishing attempt.

This represents the average reward before considering bait cost.
4. Subtract the fixed cost of bait (23) from the expected value of one cast.

Since bait cost is paid every time, it is a deterministic subtraction and does not interact with probability.
5. Multiply the resulting per-cast expectation by k.

Linearity of expectation ensures that total expected reward over k independent casts is exactly k times the single-cast expectation.

### Why it works

Each fishing attempt is an independent random variable with identical distribution. The total profit is the sum of k such variables, each already incorporating the deterministic bait cost. Expectation distributes over summation, so the expectation of the total is the sum of expectations. No correlations or conditional dependencies exist between casts, so no additional state is needed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, k = map(int, input().split())
    
    value = {
        'D': 16,
        'C': 24,
        'B': 54,
        'A': 80,
        'S': 10000
    }
    
    exp_one = 0.0
    
    for _ in range(n):
        t, p = input().split()
        p = float(p)
        exp_one += p * value[t]
    
    exp_one -= 23.0
    ans = exp_one * k
    
    print(f"{ans:.4f}")

if __name__ == "__main__":
    main()
```

The code directly implements the expectation computation. The dictionary maps rarity classes to values, with the special override for S-type fish. Each fish contributes probability times value into a running sum.

The subtraction of 23 is done once per cast, not per fish, because bait cost is independent of outcome but dependent on number of attempts. Finally, multiplying by k aggregates k identical independent trials.

A common mistake is subtracting bait cost inside the loop over fish types, which would incorrectly scale cost by n instead of k.

## Worked Examples

We construct a small example to illustrate computation.

Input:

```
3 2
D 0.50
C 0.30
S 0.20
```

Step-by-step expectation:

| Fish | Probability | Value | Contribution |
| --- | --- | --- | --- |
| D | 0.50 | 16 | 8.0 |
| C | 0.30 | 24 | 7.2 |
| S | 0.20 | 10000 | 2000.0 |

Sum per cast = 2015.2

Subtract bait = 2015.2 − 23 = 1992.2

Two casts = 3984.4

This confirms linear scaling.

Another example:

Input:

```
2 3
D 1.00
S 0.00
```

Per cast value = 16

After cost = -7

Total = -21

This shows that expectation can be negative when bait cost exceeds fish value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single pass over fish types to compute expectation |
| Space | O(1) | only fixed mapping and accumulator variables |

The constraints n ≤ 100 and k ≤ 100 make this trivial in terms of performance. Even multiple floating-point operations per input line are negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    value = {'D':16,'C':24,'B':54,'A':80,'S':10000}
    
    exp_one = 0.0
    for _ in range(n):
        t, p = input().split()
        p = float(p)
        exp_one += p * value[t]
    
    exp_one -= 23
    ans = exp_one * k
    return f"{ans:.4f}"

# provided sample (format reconstructed)
assert run("3 2\nD 0.50\nC 0.30\nS 0.20\n") == "3984.4000"

# minimum case
assert run("1 1\nD 1.00\n") == f"{(16-23):.4f}"

# all S fish
assert run("1 2\nS 1.00\n") == f"{(10000-23)*2:.4f}"

# mixed zero probability edge
assert run("2 3\nD 1.00\nS 0.00\n") == f"{(16-23)*3:.4f}"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single D | negative expectation | bait cost dominance |
| all S | large value scaling | rare high-value override |
| zero-prob S | ignored categories | probability handling correctness |
| single type | deterministic behavior | base correctness |

## Edge Cases

A key edge case is when probabilities assign zero weight to high-value fish. The algorithm still includes them in the mapping, but their contribution becomes zero, so they do not affect expectation.

For example:

```
2 2
S 0.00
D 1.00
```

Per cast expectation is 16, minus 23 gives -7, total -14. The S fish is completely ignored despite being present.

Another case is when all fish values are lower than bait cost. The expectation becomes negative, which is valid because expected profit does not need to be positive.
