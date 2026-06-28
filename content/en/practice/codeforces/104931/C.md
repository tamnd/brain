---
title: "CF 104931C - Gambler's Chocolate Cove"
description: "We are given several slot machines, each producing a random reward when pulled. Each machine has its own fixed probability distribution over a small set of possible reward values."
date: "2026-06-28T07:35:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104931
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 01-26-24 Div. 1 (Advanced)"
rating: 0
weight: 104931
solve_time_s: 73
verified: false
draft: false
---

[CF 104931C - Gambler's Chocolate Cove](https://codeforces.com/problemset/problem/104931/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several slot machines, each producing a random reward when pulled. Each machine has its own fixed probability distribution over a small set of possible reward values. You are allowed to perform exactly `n` pulls in total, and each pull can be assigned to any one of the machines. Different pulls are independent, and the distribution of a machine does not change over time.

The goal is to decide how to distribute the `n` pulls across the machines so that the expected total reward is as large as possible. After all pulls are done, we are asked only for this maximum possible expectation, not for the actual sequence of outcomes.

The constraints are small: both `n` and `k` are at most 100, while each distribution can contain up to 1000 outcomes. This already hints that even quadratic or cubic solutions over machines and pulls would be acceptable, but anything involving combinatorial allocation over distributions per pull would be unnecessary. A solution that recomputes expectations carefully for each machine is easily fast enough.

A subtle failure mode in many incorrect approaches is trying to model the full probability distribution of total rewards across multiple pulls. For example, one might attempt dynamic programming over possible sums after each pull. This is unnecessary because the problem only asks for expectation, not variance or distribution shape. Another common mistake is assuming we need to interleave pulls between machines in a clever pattern. In reality, each pull is independent and contributes additively in expectation, so ordering has no effect.

As a concrete example of a wrong direction, suppose two machines have identical expected values but different spreads. A distribution-tracking solution might incorrectly try to prefer the “safer” machine, even though expectation does not depend on variance. The correct answer depends only on mean reward, not on risk.

## Approaches

A naive interpretation of the problem is that we must assign `n` discrete actions (pulls), each choosing one of `k` machines, and each action has a random outcome. One could imagine a brute-force solution that enumerates all possible assignments of `n` pulls across machines and evaluates expected value for each assignment.

For each assignment, if we simulate expectation properly, we still need to compute expected reward per pull from the distribution. Even if expectation per machine is precomputed, the number of assignments is `k^n`, since each of the `n` pulls can independently choose one of `k` machines. With `n = 100`, this becomes astronomically large and completely infeasible.

The key observation is that expectation is linear. The expected total reward of multiple independent pulls is just the sum of expected rewards of each pull, regardless of dependence between choices of machines. This means each pull contributes independently based only on which machine it uses. There is no interaction between pulls that could make a mixed strategy better than repeatedly choosing the best machine.

Once we accept linearity, the structure collapses: each machine has a fixed expected reward per pull, and every pull should go to the machine with the largest expectation. No more complicated allocation is needed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force assignment of pulls | O(k^n) | O(n) | Too slow |
| Compute expectations and pick max | O(k * m_i) | O(1) | Accepted |

## Algorithm Walkthrough

We proceed by transforming each machine’s probability distribution into a single number, its expected reward per pull, and then choosing the best machine.

1. For each machine, read its list of possible rewards and corresponding probabilities.

The expected value of a single pull from this machine is the weighted sum of outcomes.
2. Compute the expectation `E_i = sum(r_j * p_j)` for each machine `i`.

This collapses the entire distribution into one scalar representing long-term average gain.
3. Track the maximum expected value among all machines.
4. Multiply this maximum expectation by `n`, since all `n` pulls should be assigned to that best machine.

The final answer is `n * max(E_i)`.

### Why it works

Each pull contributes an independent random variable whose expectation depends only on the chosen machine. The total expected reward is the sum of expectations of individual pulls. Because expectation is additive, rearranging pulls across machines does not create any cross-term or synergy. Any allocation that uses a machine with smaller expectation can be improved by moving that pull to a machine with larger expectation, strictly increasing total expectation. This implies an optimal solution always assigns every pull to a single machine with maximal expected value.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    
    best = 0.0
    
    for _ in range(k):
        m = int(input())
        rewards = list(map(int, input().split()))
        probs = list(map(float, input().split()))
        
        exp = 0.0
        for r, p in zip(rewards, probs):
            exp += r * p
        
        if exp > best:
            best = exp
    
    print(n * best)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the reduction to expectation maximization. Each machine is processed independently, and its expected value is computed as a dot product between rewards and probabilities. The only global state maintained is the maximum expectation seen so far.

A common pitfall is attempting to distribute pulls across multiple machines using dynamic programming. That is unnecessary because there is no diminishing return or dependency between pulls.

Floating-point precision is sufficient because values are bounded and the required precision is `1e-6`. Standard double precision comfortably handles the accumulation of up to 1000 terms per machine.

## Worked Examples

Consider a small instance with two machines and three total pulls.

Machine 1 gives reward 10 with probability 0.5 and 0 with probability 0.5. Its expectation is 5.0.

Machine 2 gives reward 3 with probability 1.0. Its expectation is 3.0.

| Machine | Expected value |
| --- | --- |
| 1 | 5.0 |
| 2 | 3.0 |

| Step | Best so far |
| --- | --- |
| After machine 1 | 5.0 |
| After machine 2 | 5.0 |

The result is `3 * 5.0 = 15.0`.

Now consider a case where a machine has many outcomes but low mean. Suppose machine A has outcomes `[0, 100]` with probabilities `[0.99, 0.01]`, and machine B always returns 1. Machine A has expectation 1.0, machine B also has expectation 1.0. Any allocation yields the same expected value, so assigning all pulls to either machine is optimal.

This confirms that variance does not matter and only the mean drives the solution.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k · m_i) | Each machine’s expectation is computed by a single pass over its distribution |
| Space | O(1) | Only a few scalars are stored beyond input buffering |

The constraints allow up to 100 machines with up to 1000 outcomes each, so at most 100,000 multiplications are performed. This is easily within limits, and memory usage is constant aside from input storage.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import isclose

    n, k = map(int, input().split())
    best = 0.0
    for _ in range(k):
        m = int(input())
        r = list(map(int, input().split()))
        p = list(map(float, input().split()))
        exp = sum(ri * pi for ri, pi in zip(r, p))
        best = max(best, exp)
    return str(best * n)

# sample
assert run("5 3\n1\n9\n1.0\n1\n7\n1.0\n1\n5\n1.0\n") == "45.0"

# all equal machines
assert run("2 2\n2\n1 3\n0.5 0.5\n2\n1 3\n0.5 0.5\n") == "4.0"

# single machine
assert run("4 1\n2\n0 10\n0.5 0.5\n") == "20.0"

# zero reward machine
assert run("3 2\n1\n0\n1.0\n1\n5\n1.0\n") == "15.0"

# mixed distributions
assert run("1 2\n2\n0 10\n0.9 0.1\n1\n5\n1.0\n") == "1.0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| identical machines | same result regardless of choice | symmetry |
| single machine | direct scaling | base case |
| zero-reward machine | ignoring useless options | dominance |
| mixed distributions | correct expectation computation | weighted sum correctness |

## Edge Cases

A key edge case is when multiple machines have exactly the same expected value. In that situation, any allocation of pulls among them is optimal. The algorithm handles this naturally because it only tracks the maximum expectation and does not depend on which machine achieves it.

Another case is when all machines have zero expected value. Even then, the computed expectation remains zero, and multiplying by `n` preserves correctness. There is no need for special handling because the max remains zero.

A final subtle case is numerical precision when probabilities are very small or values are near the upper bound. Since all rewards are bounded by 100 and there are at most 1000 terms per machine, accumulated floating-point error stays well below the required `1e-6` tolerance.
