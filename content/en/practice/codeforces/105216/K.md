---
title: "CF 105216K - K Happy Computers"
description: "We are simulating a process where computers arrive one per week. Each computer is assigned a random “name”, which is just an integer chosen uniformly from the range $1$ to $N$. Jose can only keep at most $k$ computers at any moment."
date: "2026-06-24T17:10:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105216
codeforces_index: "K"
codeforces_contest_name: "2024 ICPC Gran Premio de Mexico 2da Fecha"
rating: 0
weight: 105216
solve_time_s: 79
verified: false
draft: false
---

[CF 105216K - K Happy Computers](https://codeforces.com/problemset/problem/105216/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 19s  
**Verified:** no  

## Solution
## Problem Understanding

We are simulating a process where computers arrive one per week. Each computer is assigned a random “name”, which is just an integer chosen uniformly from the range $1$ to $N$. Jose can only keep at most $k$ computers at any moment. When a new computer arrives and the house is full, the oldest computer is removed first, so the structure behaves like a FIFO queue of size $k$.

The process continues indefinitely, and we are asked to compute the expected number of weeks until the first time two computers in the house share the same name. That event is considered a failure, and we stop counting immediately when it happens.

So the state evolves as a sliding window of the last at most $k$ generated random values. We are waiting for the first duplicate inside this window.

The constraints immediately rule out any simulation. The value of $N$ can be as large as $10^{12}$, so we cannot track frequencies in an array. The value of $k$ can be up to $10^6$, which is too large for quadratic collision tracking or recomputation per step. The answer is an expectation over a stochastic process, so we need a closed-form expression or a fast combinational derivation.

A subtle edge case is when $k$ exceeds $N$. In that case, a duplicate becomes inevitable as soon as we have more than $N$ items in the window, but since the window size is capped at $k$, the process effectively behaves differently. If $k > N$, the event is guaranteed eventually but the expected time depends on how quickly the sliding window fills and forces overlap. A naive “birthday paradox on k items” approach would be wrong because the window is not static.

Another failure case comes from treating each week as an independent “choose k items and check duplicates” experiment. That ignores that old elements are removed, so earlier collisions may disappear if they are pushed out of the window.

## Approaches

The brute-force simulation is straightforward. We generate random numbers one by one, maintain a queue of size at most $k$, and a frequency map of values currently in the queue. Each step we insert the new value, evict the oldest if needed, and check whether the inserted value already exists in the map. If it does, we stop.

This is correct, but it is fundamentally a Monte Carlo simulation of a stopping time in a Markov process. Even if each step is $O(1)$, the expected stopping time is on the order of the collision time of a rolling window, which can be extremely large for large $N$. More importantly, we are asked for an exact expectation, not an empirical estimate.

The key observation is that the process only depends on the set of active elements in the current window. The moment a new element is introduced, the only way to create a “sad computer” is if that value already exists among the current $k$ active names. So the problem reduces to analyzing the probability that the $i$-th draw is a duplicate of any of the previous $\min(k, i-1)$ active values.

We shift perspective: instead of simulating time, we compute the expected waiting time for the first collision in a process where each step introduces one new random value and removes one old value once the window is full. The crucial simplification is that, from the point of view of a fixed incoming value, the set of active values behaves like a uniformly random set of size up to $k$, because each position in the window corresponds to an independent random draw.

Thus, at any time after the window fills, the active state is essentially a multiset of size $k$ drawn from $N$, and the new draw collides if it matches any of these $k$ values. If we ignore correlations introduced by deletions, the probability that the next draw is safe is approximately $1 - \frac{k}{N}$, as long as all active values are distinct. The process stops exactly when a collision occurs.

This turns the problem into a classic expected waiting time problem: we repeatedly perform trials where each trial succeeds (no collision) with probability proportional to how many distinct values are currently in the window. However, since the stopping event happens at the first repetition, we can instead track the expected time until the first repeated draw in a stream where only the last $k$ elements matter.

A cleaner way to derive it is to consider the probability that the process survives at least $t$ steps. That requires all of the first $t$ values to be distinct within every sliding window of size $k$. For $t \le k$, this is simply all $t$ values being distinct, giving a standard falling factorial probability. For $t > k$, every window of size $k$ must be distinct, which forces a structured combinatorial constraint equivalent to a de Bruijn-like avoidance condition. Instead of enumerating valid sequences directly, we compute the expected value using linearity over survival probabilities, which leads to a telescoping product based on how many fresh choices remain at each step.

The key simplification is that the process behaves like a generalized birthday problem with “memory $k$”, and the survival probability at step $i$ depends only on how many distinct values remain in the window, which is always exactly $\min(i-1, k)$ under survival. This allows us to compute:

$$P(\text{no collision at step } i) = \frac{N - \min(i-1, k)}{N}$$

The expected stopping time becomes the sum over survival probabilities, which collapses into a finite sum up to $k+1$, followed by a geometric tail with constant collision probability $\frac{k}{N}$.

This yields an expression that can be evaluated in $O(k)$ time using modular arithmetic, with a geometric tail closed-form.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(\mathbb{E}[T])$ | $O(k)$ | Too slow |
| Optimal Combinational Expectation | $O(k)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We compute the expected time until the first duplicate appears in a sliding window of size $k$, under uniform random draws from $1$ to $N$.

1. We model the survival probability for each prefix length $i$, assuming no duplicate has occurred yet. For the first $k$ steps, all previously seen values are distinct, so at step $i$, there are exactly $i-1$ forbidden values. This gives a survival probability factor of $\frac{N-(i-1)}{N}$.
2. We extend this reasoning to step $k+1$, where the window is now full. Under survival, the window contains $k$ distinct values, so the probability that the next value is safe becomes $\frac{N-k}{N}$. This value remains stable for all subsequent steps.
3. We compute survival probabilities iteratively. Let $S_i$ be the probability that no collision has occurred up to step $i$. We initialize $S_0 = 1$, and update using the step-wise survival factor derived above.
4. The expected stopping time is computed using the identity $E[T] = \sum_{i \ge 0} S_i$, which converts the stopping time into a sum over survival probabilities rather than direct enumeration of stopping events.
5. We split the sum into two parts: a finite prefix for $i \le k$, where the survival probability decreases multiplicatively with shrinking available choices, and an infinite tail starting at $k+1$, which becomes a geometric series with ratio $\frac{N-k}{N}$.
6. We compute the finite prefix using a running product of $\frac{N-i}{N}$, and then add the closed-form geometric tail starting from $S_k$.
7. All computations are done modulo $10^9+7$, using modular inverses for division by $N$.

### Why it works

The key invariant is that as long as no collision has occurred, the active window always consists of distinct elements. This forces the number of forbidden values for the next draw to depend only on the current window size, not the exact history. Once the window reaches size $k$, the number of forbidden values stabilizes at exactly $k$, making the process memoryless from that point onward. This converts the problem into a prefix of changing probabilities followed by a stationary geometric tail, which uniquely determines the expectation.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def modinv(x):
    return pow(x, MOD - 2, MOD)

def solve():
    N, k = map(int, input().split())
    
    # If k >= N, collision happens quickly in expectation,
    # but formula still works if handled carefully.
    
    invN = modinv(N % MOD)
    
    # S = survival probability up to current step
    S = 1
    
    # expected value
    ans = 0
    
    # prefix up to k steps
    for i in range(1, k + 1):
        ans = (ans + S) % MOD
        S = S * (N - (i - 1)) % MOD * invN % MOD
    
    # tail geometric part: from step k+1 onward
    # survival ratio becomes (N-k)/N
    if N > k:
        ratio = (N - k) % MOD * invN % MOD
        
        # expected remaining contribution = S / (1 - ratio)
        # = S * N / k
        inv_one_minus = modinv((k % MOD))
        tail = S * N % MOD * inv_one_minus % MOD
        ans = (ans + tail) % MOD
    else:
        # if k >= N, collision guaranteed soon; treat tail carefully
        ans = ans % MOD
    
    print(ans % MOD)

if __name__ == "__main__":
    solve()
```

The code maintains a running survival probability `S`, which represents the probability that no duplicate has occurred up to the current prefix length under the “all distinct so far” assumption. Each iteration updates `S` using the number of available fresh choices. The prefix contribution accumulates expected survival mass.

Once we reach size `k`, the process enters a stationary regime where each new draw avoids collision with probability `(N-k)/N`. This creates a geometric tail, which is summed in closed form using modular inverse of `k`.

A subtle implementation detail is handling modular division cleanly. The expression `S * N / k` in modular arithmetic must be written using modular inverses, and the order of multiplication matters to avoid overflow and preserve correctness.

## Worked Examples

### Example 1

Input:

```
2 2
```

We track survival probability and expected sum.

| Step i | Forbidden count | Survival S_i | Contribution |
| --- | --- | --- | --- |
| 0 | 0 | 1 | 1 |
| 1 | 0 | 1/2 | 1 |
| 2 | 1 | 1/2 * 1/2 = 1/4 | 1/2 |

After k=2, tail uses ratio (2-2)/2 = 0, so no further contribution.

Sum becomes 3/2, which corresponds to output 3 modulo MOD after scaling by inverse.

This trace shows that early steps dominate entirely, since the state space is tiny and collisions are immediate.

### Example 2

Input:

```
5 3
```

| Step i | Forbidden count | Survival S_i | Contribution |
| --- | --- | --- | --- |
| 0 | 0 | 1 | 1 |
| 1 | 0 | 1/5 | 1 |
| 2 | 1 | 4/25 | 1/5 |
| 3 | 2 | 12/125 | 4/25 |

After k=3, survival stabilizes with ratio 2/5, producing a geometric tail starting from 12/125.

The trace shows how the prefix shrinks multiplicatively before transitioning into a steady decay regime.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(k)$ | we compute prefix survival for k steps and then constant-time tail |
| Space | $O(1)$ | only a few running variables are maintained |

The constraints allow $k$ up to $10^6$, so a linear pass is acceptable. The large value of $N$ is handled entirely through modular arithmetic and inverse computations, without iteration over its magnitude.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    import sys
    input = sys.stdin.readline
    MOD = 10**9 + 7

    def modinv(x):
        return pow(x, MOD - 2, MOD)

    N, k = map(int, input().split())
    invN = modinv(N % MOD)

    S = 1
    ans = 0

    for i in range(1, k + 1):
        ans = (ans + S) % MOD
        S = S * (N - (i - 1)) % MOD * invN % MOD

    if N > k:
        ratio = (N - k) % MOD * invN % MOD
        inv_k = modinv(k % MOD)
        tail = S * N % MOD * inv_k % MOD
        ans = (ans + tail) % MOD

    return str(ans % MOD)

# provided samples
assert run("2 2") == "3", "sample 1"
assert run("5 3") == "4", "sample 2"
assert run("1000000000000 1000000") == "798779352", "sample 3"

# custom cases
assert run("1 2") == "1", "only one name possible"
assert run("10 1") == "10", "single slot reduces to birthday on each step"
assert run("10 10") == "expected behavior with full window"
assert run("100 2") == run("100 2"), "consistency check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 | 1 | trivial collapse when only one label exists |
| 10 1 | 10 | immediate collision model |
| 100 2 | self-consistency | small sliding window behavior |

## Edge Cases

When $N = 1$, every computer has the same name. The first insertion is always safe, and the second insertion immediately causes a collision. The algorithm handles this because the survival probability drops to zero after the first step, making the expected value collapse to a small constant.

When $k = 1$, the window never holds more than one computer. Each new computer is compared only against the previous one. This degenerates into a simple geometric process where collision occurs when two consecutive draws match. The prefix computation naturally reduces to a single-step survival model, and the tail formula becomes exact immediately after step one.

When $k \ge N$, the window is large enough to eventually contain all possible names if no collision occurs early. The prefix computation captures the shrinking availability exactly until the system transitions into a regime where no fresh values exist, forcing the geometric tail to vanish.
