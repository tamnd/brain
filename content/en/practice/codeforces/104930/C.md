---
title: "CF 104930C - Gambler's Chocolate Cove"
description: "Each slot machine behaves like a stochastic reward generator. When you pull a machine once, it returns one value from a fixed finite set, each value having a known probability. Those probabilities do not change over time and every pull is independent of previous pulls."
date: "2026-06-28T07:43:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104930
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 01-26-24 Div. 2 (Beginner)"
rating: 0
weight: 104930
solve_time_s: 253
verified: false
draft: false
---

[CF 104930C - Gambler's Chocolate Cove](https://codeforces.com/problemset/problem/104930/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 13s  
**Verified:** no  

## Solution
## Problem Understanding

Each slot machine behaves like a stochastic reward generator. When you pull a machine once, it returns one value from a fixed finite set, each value having a known probability. Those probabilities do not change over time and every pull is independent of previous pulls.

You are allowed to perform exactly $n$ pulls in total, and each pull can be assigned to any of the $k$ machines. The goal is to distribute these $n$ pulls across the machines in a way that maximizes the expected sum of obtained rewards.

The output is a single real number: the maximum possible expected total reward after making all $n$ decisions.

The key observation hidden in the formulation is that nothing in the problem introduces interaction between pulls. A machine does not become worse or better after being used, and there is no constraint linking which machine must be used after another.

From the constraints, $n, k \le 100$, and each distribution has at most 1000 outcomes. Even a solution that recomputes expectations per machine is easily fast enough. The only real difficulty is recognizing that the structure eliminates any need for dynamic programming or combinatorial allocation.

A naive interpretation that often appears in first attempts is to think that distributing pulls might require searching over all allocations, which would mean assigning $n$ pulls among $k$ machines. That would lead to $\binom{n+k-1}{k-1}$ possibilities, which grows rapidly even for small values.

A small example illustrates the trap:

If $n = 3$, $k = 2$, and machine A has expected value 5 while machine B has expected value 4, any allocation like (2,1), (1,2), or (3,0) must be considered in a brute-force view. A naive approach might think different splits produce different behavior. In reality, only the per-pull expectation matters, so (3,0) dominates.

A second subtle edge case is when distributions are non-integer or heavily skewed. For example, a machine that outputs 100 with probability 0.01 and 0 otherwise still has expectation 1. A naive intuition might favor frequent small rewards, but expectation collapses everything into a single scalar.

## Approaches

A brute-force approach would enumerate how many pulls are assigned to each machine, respecting that the counts sum to $n$. For each allocation, we compute the expected value by multiplying counts with precomputed expectations of each machine.

The correctness of that approach is straightforward because expectation is linear and independent per pull. However, the number of allocations is exponential in $k$, since it is equivalent to counting compositions of $n$ into $k$ parts. Even for $n = 100$, this space becomes astronomically large, making enumeration impossible.

The key simplification comes from recognizing that every pull is identical except for which machine is chosen. Since expectation is additive and independent, each pull can be treated in isolation. This collapses the problem into selecting the machine with the maximum expected value and using it for all $n$ pulls.

The allocation structure disappears entirely because there is no diminishing return or shared constraint between pulls beyond the total count.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in $n$ | O(n) | Too slow |
| Optimal | O(k · m) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each machine, compute its expected value by summing over all outcomes $r_j \cdot p_j$. This compresses each distribution into a single scalar because expectation fully characterizes its contribution per pull.
2. Track the maximum expected value among all machines. This represents the best achievable reward per single pull.
3. Multiply this maximum expectation by $n$, since every one of the $n$ pulls should be assigned to the best machine independently of previous choices.

### Why it works

Each pull contributes independently to the total expectation, and the expected value of a sum is the sum of expected values. Since there is no dependency between pulls and no cost for reusing the same machine, the optimal strategy never needs diversification. Any deviation from always choosing the best expected machine strictly decreases the contribution of that pull without affecting others.

The invariant is that after deciding the optimal machine for a single pull, extending the decision to multiple pulls does not change any probabilistic structure. Each additional pull is an identical copy of the same optimization choice.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, k = map(int, input().split())
    
    best = 0.0

    for _ in range(k):
        m = int(input())
        r = list(map(int, input().split()))
        p = list(map(float, input().split()))
        
        exp = 0.0
        for rv, prob in zip(r, p):
            exp += rv * prob
        
        if exp > best:
            best = exp

    print(n * best)

if __name__ == "__main__":
    main()
```

The core of the implementation is the reduction of each machine to a single expected value. The loop over rewards and probabilities is the only place where the distribution structure is used.

A common mistake is attempting to simulate pulls or build a DP over remaining operations. That is unnecessary because the state does not evolve. Another possible mistake is summing floating-point probabilities incorrectly; here they are guaranteed to sum to 1, so no normalization is required.

## Worked Examples

### Example 1

Suppose we have $n = 3$, $k = 2$.

Machine A: outcomes (10 with probability 0.5, 0 with probability 0.5)

Machine B: outcomes (4 with probability 1.0)

Expected values are:

A = 5, B = 4

| Step | Machine A exp | Machine B exp | Best so far | Action |
| --- | --- | --- | --- | --- |
| 1 | 5 | 4 | 5 | choose A |
| 2 | 5 | 4 | 5 | choose A |
| 3 | 5 | 4 | 5 | choose A |

Final answer is $3 \times 5 = 15$.

This trace shows that recomputing choices per pull does not change the decision, reinforcing that the same machine dominates globally.

### Example 2

Let $n = 4$, $k = 3$.

Machine A: always 2

Machine B: 3 with probability 0.5, 0 otherwise

Machine C: 1 with probability 1

Expectations:

A = 2, B = 1.5, C = 1

| Step | A | B | C | Best |
| --- | --- | --- | --- | --- |
| 1 | 2 | 1.5 | 1 | A |
| 2 | 2 | 1.5 | 1 | A |
| 3 | 2 | 1.5 | 1 | A |
| 4 | 2 | 1.5 | 1 | A |

Answer is $4 \times 2 = 8$.

This confirms that even when distributions are varied and non-intuitive, collapsing them to expectation preserves correctness.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(k \cdot m)$ | each machine’s expectation computed once |
| Space | $O(1)$ | only storing current best value |

The bounds $k \le 100$ and $m \le 1000$ make the total work at most $10^5$ multiplications, which is trivial under the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    n, k = map(int, sys.stdin.readline().split())
    best = 0.0

    for _ in range(k):
        m = int(sys.stdin.readline())
        r = list(map(int, sys.stdin.readline().split()))
        p = list(map(float, sys.stdin.readline().split()))
        exp = sum(x * y for x, y in zip(r, p))
        best = max(best, exp)

    return str(n * best)

# sample
assert run("3 2\n2\n10 0\n0.5 0.5\n1\n4\n1.0\n") == "15.0"

# all equal machines
assert run("2 2\n2\n1 2\n0.5 0.5\n2\n1 2\n0.5 0.5\n") == "3.0"

# single machine
assert run("4 1\n2\n3 0\n0.5 0.5\n") == "6.0"

# deterministic best
assert run("5 2\n1\n10\n1.0\n1\n1\n1.0\n") == "50.0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single machine | 6.0 | base case correctness |
| identical machines | 3.0 | symmetry handling |
| deterministic best | 50.0 | greedy selection of best expectation |

## Edge Cases

A machine with highly skewed distribution can look misleading if one focuses on rare outcomes. For instance, a machine outputting 1000 with probability 0.001 and 0 otherwise still contributes only 1 in expectation. The algorithm handles this correctly because it reduces everything to expectation before comparison.

Another edge case is when multiple machines share the same expected value. In that case, any of them is optimal, and the algorithm still returns the correct result since only the maximum value matters, not its identity.

Finally, when $n = 1$, the solution correctly returns the best single expectation among all machines, matching the intuitive interpretation of a single choice problem.
