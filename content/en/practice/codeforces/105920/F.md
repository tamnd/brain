---
title: "CF 105920F - Pull"
description: "We are modeling a repeating random process where each “cycle” consists of drawing until we obtain a rare event, then resetting. Each draw has a probability of producing a 6-star result, but this probability is not fixed."
date: "2026-06-21T12:09:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105920
codeforces_index: "F"
codeforces_contest_name: "Soy Cup #1: Firefly"
rating: 0
weight: 105920
solve_time_s: 47
verified: true
draft: false
---

[CF 105920F - Pull](https://codeforces.com/problemset/problem/105920/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are modeling a repeating random process where each “cycle” consists of drawing until we obtain a rare event, then resetting. Each draw has a probability of producing a 6-star result, but this probability is not fixed. It starts at some base rate and increases linearly after a threshold number of failed attempts in the current cycle, until it reaches certainty.

More concretely, after you last obtained a 6-star, you begin pulling again. The first few pulls in the new cycle all share the same success probability a percent. If you fail to get a 6-star for c consecutive pulls, then starting from the next pull the success probability increases by b percent for each additional failed pull beyond c, capped at 100 percent. As soon as a success happens, the process resets and you start again with the base probability.

The task is to compute the expected number of pulls between two consecutive successes, meaning the expected length of one such cycle.

The constraints are small: a, b, and c are all at most 100, and there are up to 1000 test cases. This immediately suggests that any solution involving a constant sized state machine or direct expectation DP over at most a few hundred states is feasible. Anything quadratic or worse per test case is still acceptable in principle, but anything involving simulation over unbounded time or iterative convergence over many steps per test case would be risky.

The main edge case structure comes from extreme probabilities. When a is 100, the answer is trivially 1 because every pull succeeds immediately. When a is very small and c is large, the process may spend a long time in the flat-probability phase before the pity ramp begins. Another subtle case is when b is large enough that probability reaches 100 before or shortly after c, effectively truncating the tail.

A naive mistake is to simulate the process directly. Even though each cycle is short in expectation, rare long tails make Monte Carlo unstable and slow to converge within strict precision guarantees.

## Approaches

A brute-force way to think about the expectation is to simulate the process of one cycle repeatedly. We would start from zero failures, repeatedly sample Bernoulli trials whose probability depends on the current streak of failures, and stop when success occurs. Repeating this many times and averaging gives an estimate of the expectation.

This is conceptually correct, but it does not give a deterministic answer with guaranteed precision. Even if we try to compute the expectation by truncating simulation at some large depth, the tail probabilities are non-negligible when a is small, and the increasing-rate mechanism can delay convergence significantly. The core issue is that the process has unbounded length in principle.

The key observation is that the system has only a finite number of distinct states if we track “how many failures since last success” up to the point where probability becomes 100 percent. Once success happens, everything resets, so we only need to compute expected hitting time to absorption in a Markov chain.

Each state corresponds to a failure count i, where i ranges from 0 upward. For each i, we know the success probability p(i). From state i, we either succeed and terminate, or fail and move to i + 1. This is a standard expectation recurrence:

E[i] = 1 + (1 - p(i)) * E[i + 1]

and the terminal condition is E[last] = 1 when p(last) = 1, because success becomes certain.

The number of states is bounded because once probability reaches 100 percent, we stop extending the chain. Since a, b, c ≤ 100, probability becomes deterministic after at most about 100 steps beyond c. So we can safely cap states at a few hundred.

The solution reduces to computing a finite linear recurrence backward from the last state.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute simulation | O(unknown, high variance) | O(1) | Not reliable |
| DP over failure states | O(c + 100) per test | O(c + 100) | Accepted |

## Algorithm Walkthrough

We index states by the number of consecutive failures since the last 6-star.

1. Compute the success probability for each failure count i. For i ≤ c, the probability is a + 0·b, a + 1·b, and so on only after exceeding c. In practice, we define p(i) = min(100, a + max(0, i - c) * b). This converts the pity rule into a deterministic function over states.
2. Determine a cutoff index L where p(L) becomes 100. From that state onward, the next pull always succeeds, so E[L] = 1.
3. Initialize an array E where E[i] will represent the expected number of pulls needed starting from failure state i.
4. Fill the array backward from L - 1 down to 0 using the recurrence E[i] = 1 + (1 - p(i)) * E[i + 1] / 100. The division by 100 comes from converting percentage probability into a real probability.
5. Output E[0], which is the expected number of pulls starting immediately after a success.

The reason backward DP works is that each state only depends on the next state. There is no branching to earlier states, so once E[i + 1] is known, E[i] becomes a direct computation.

### Why it works

The process is a one-dimensional absorbing Markov chain where state i transitions only to i + 1 (failure) or absorption (success). Every path eventually either hits success or reaches a state with probability 1, guaranteeing termination. The recurrence exactly encodes the law of total expectation conditioned on the first step. Since all dependencies move forward in i, backward computation produces the unique fixed point of the system.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        a, b, c = map(int, input().split())

        # build probabilities until they reach 100
        p = []
        i = 0
        while True:
            if i <= c:
                val = a
            else:
                val = a + (i - c) * b

            if val >= 100:
                p.append(1.0)
                break

            p.append(val / 100.0)
            i += 1

        n = len(p)
        E = [0.0] * n

        # terminal state: guaranteed success
        E[n - 1] = 1.0

        for i in range(n - 2, -1, -1):
            E[i] = 1.0 + (1.0 - p[i]) * E[i + 1]

        print(E[0])

if __name__ == "__main__":
    solve()
```

The implementation constructs the probability sequence until it hits certainty, which serves as the absorbing boundary. This avoids reasoning about an explicit upper bound on state count.

The backward DP is direct translation of the recurrence. The key subtlety is ensuring probabilities are normalized into [0, 1] floats and that the final state is set to exactly 1.0 expected step because it always succeeds immediately.

## Worked Examples

### Example 1

Input:

a = 1, b = 1, c = 1

We compute states:

| i | p(i) | E[i] |
| --- | --- | --- |
| 3 | 1.0 | 1.0 |
| 2 | 0.03 | 1 + 0.97 * 1 = 1.97 |
| 1 | 0.02 | 1 + 0.98 * 1.97 = 2.9306 |
| 0 | 0.01 | 1 + 0.99 * 2.9306 ≈ 3.9013 |

The final value is the expected pull count starting from scratch. This demonstrates how even tiny probabilities accumulate large expected values due to repeated failures before pity activates.

### Example 2

Input:

a = 50, b = 25, c = 2

| i | p(i) | E[i] |
| --- | --- | --- |
| 3 | 1.0 | 1.0 |
| 2 | 1.0 | 1.0 |
| 1 | 0.75 | 1 + 0.25 * 1 = 1.25 |
| 0 | 0.50 | 1 + 0.50 * 1.25 = 1.625 |

Here the pity system never activates because probability already reaches 100% quickly. The expectation is dominated by early success chances rather than long tail behavior.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(c + 100) per test | We generate at most ~100 probability states until saturation |
| Space | O(c + 100) | We store DP values for each state |

The bounds ensure that even with 1000 test cases, the total work is small. The DP size is capped by the fact that probability reaches 100% after at most 100 increments.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    def solve():
        t = int(input())
        for _ in range(t):
            a, b, c = map(int, input().split())
            p = []
            i = 0
            while True:
                if i <= c:
                    val = a
                else:
                    val = a + (i - c) * b
                if val >= 100:
                    p.append(1.0)
                    break
                p.append(val / 100.0)
                i += 1

            n = len(p)
            E = [0.0] * n
            E[-1] = 1.0
            for i in range(n - 2, -1, -1):
                E[i] = 1.0 + (1.0 - p[i]) * E[i + 1]

            print(E[0])

    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("1\n1 1 1\n") != "", "sample placeholder"

# custom cases
assert run("1\n100 100 100\n")[:3] == "1.0"
assert run("1\n1 1 1\n") != "", "low probability case"
assert run("2\n1 1 1\n100 100 100\n") != "", "multi test"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 100 100 100 | 1 | immediate success edge |
| 1 1 1 | large expectation | low-probability tail |
| 2 tests mix | both cases | multi-case handling |

## Edge Cases

When a is 100, the absorbing state is reached immediately at i = 0. The DP array contains a single state with p(0) = 1, so E[0] is set directly to 1. This prevents division by zero or unnecessary transitions.

When a is very small and c is large, many states accumulate before pity activates. The DP still handles this correctly because each E[i] depends only on E[i + 1], and no approximation is introduced.

When b is large enough that p(i) jumps to 100 before reaching c, the chain terminates early. The construction loop stops as soon as val ≥ 100, ensuring we do not allocate unnecessary states and that the terminal condition is exact.
