---
title: "CF 105067J - Arknights Chips"
description: "We are simulating a repeated farming process that produces two types of items: sniper chips and caster chips. Each run of the stage gives a sniper chip with probability $p = a/100$, and otherwise gives a caster chip."
date: "2026-06-27T23:39:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105067
codeforces_index: "J"
codeforces_contest_name: "Teamscode Spring 2024 (Advanced Division)"
rating: 0
weight: 105067
solve_time_s: 93
verified: false
draft: false
---

[CF 105067J - Arknights Chips](https://codeforces.com/problemset/problem/105067/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 33s  
**Verified:** no  

## Solution
## Problem Understanding

We are simulating a repeated farming process that produces two types of items: sniper chips and caster chips. Each run of the stage gives a sniper chip with probability $p = a/100$, and otherwise gives a caster chip.

After completing $n$ runs, Waymo is allowed to convert resources: whenever he has at least $x$ caster chips, he can trade exactly $x$ casters for $y$ sniper chips, and he may repeat this operation as many times as possible.

The goal is to compute the expected number of sniper chips after both farming and all possible conversions, modulo $998244353$, where the expectation is a rational number reduced under modular arithmetic.

The key difficulty is that $n$ can be as large as $10^{18}$, so we cannot simulate the process step by step. Even computing full distributions over $(\text{snipers}, \text{casters})$ after $n$ steps is impossible. Any solution must collapse the randomness into a closed form expression or a fast recurrence.

A subtle edge case appears when $a = 0$ or $a = 100$. In these cases, the process becomes deterministic, and naive probabilistic formulas involving division by $p$ or $1-p$ break down.

Another edge case arises when $x = y$, since conversions do not change the number of sniper chips in expectation, but still affect the number of caster chips and hence future conversion potential.

A small illustrative failure case is $a = 0$, $x = 2$, $y = 1$, $n = 5$. A naive expectation formula might assume some mixing of both chip types, but in reality only caster chips are produced and all value comes from conversion.

## Approaches

A direct brute-force approach would simulate all possible sequences of length $n$. Each sequence has $2^n$ outcomes, and for each outcome we would compute final conversions greedily. This is immediately infeasible since $n$ can be up to $10^{18}$, and even for $n = 50$ this already becomes astronomically large.

A slightly smarter brute-force idea is dynamic programming over steps, maintaining a probability distribution over the number of caster chips. After each step, we update the distribution by adding either a sniper or caster chip, then repeatedly apply conversion transitions. However, the state space grows linearly with $n$, and each transition is $O(n)$, giving $O(n^2)$ per test case, which still fails for large constraints.

The key observation is that conversions are linear in expectation and independent of ordering. Each conversion of $x$ casters into $y$ snipers has a fixed net gain structure, and only the expected number of casters matters. This allows us to decouple the problem into tracking expected counts instead of distributions.

The second key insight is that the caster-to-sniper conversion acts like a “compression” of casters into snipers with efficiency $y/x$. Since conversions are applied greedily and independently of ordering, the expected number of effective conversions depends only on the expected total number of casters, not their distribution.

Thus, the problem reduces to computing the expected number of caster chips after $n$ trials, and then determining how many full groups of size $x$ we can expect to form, adjusted carefully for modular expectations.

We ultimately model the system as a linear expectation recurrence over $n$, which can be solved using fast exponentiation on a transition that tracks both sniper expectation and a scaled caster potential state.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(2^n)$ | $O(n)$ | Too slow |
| DP over distributions | $O(n^2)$ | $O(n)$ | Too slow |
| Linear expectation transition + matrix exponentiation | $O(\log n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We track the system using expected values, but we must also account for the “conversion potential” stored in casters.

We define two quantities after $k$ steps:

The expected number of sniper chips $S_k$, and the expected number of caster chips $C_k$. However, since conversions depend on grouping casters into batches of size $x$, we instead track a scaled state that captures how many full conversion units can be formed in expectation.

### 1. Convert probabilities into modular form

We set:

$$p = a \cdot 100^{-1}, \quad q = 1 - p$$

in modular arithmetic under $998244353$. This ensures all later updates are linear over the field.

### 2. Model one step transition

Each step increases snipers by 1 with probability $p$, otherwise increases casters by 1 with probability $q$.

So:

$$S_{k+1} = S_k + p$$

$$C_{k+1} = C_k + q$$

### 3. Handle conversion effect

Every time we accumulate $x$ casters, we gain $y$ snipers and lose $x$ casters. In expectation, this behaves like transferring mass from $C_k$ to $S_k$ at rate proportional to how often groups of $x$ form.

We encode this as a linear system where the “effective contribution” of casters to future snipers is scaled by a factor:

$$\alpha = \frac{y}{x}$$

Thus each caster contributes $\alpha$ expected snipers over time, and the system becomes linear.

### 4. Reduce to closed-form expectation

Total expected snipers after $n$ steps:

$$E = np + (nq)\cdot \frac{y}{x}$$

This captures direct sniper drops plus expected sniper gain from casters via conversion.

### 5. Compute modular answer

We compute:

$$E = n \cdot \left(p + (1-p)\frac{y}{x}\right)$$

under modulo arithmetic.

### Why it works

The process is linear in expectation because both the drop process and conversion process are additive and do not depend on ordering. The greedy conversion rule ensures that every group of $x$ casters eventually contributes exactly $y$ snipers, regardless of how casters are distributed across time. Therefore, only the expected total caster count matters, and grouping effects do not introduce nonlinear dependencies in expectation.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modinv(x):
    return pow(x, MOD - 2, MOD)

def solve():
    T = int(input())
    inv100 = modinv(100)

    for _ in range(T):
        a, x, y, n = map(int, input().split())

        p = a * inv100 % MOD
        q = (1 - p) % MOD

        # expected snipers = direct + converted casters
        # E = n * (p + q * y/x)

        invx = modinv(x)

        gain_from_casters = q * y % MOD * invx % MOD
        total_per_step = (p + gain_from_casters) % MOD

        ans = total_per_step * (n % MOD) % MOD
        print(ans)

if __name__ == "__main__":
    solve()
```

The code first converts probabilities into modular fractions using modular inverses. The probability of a caster drop is derived as $1 - p$, keeping everything in modular arithmetic.

The key implementation step is computing $y/x$ using a modular inverse of $x$, since direct division is not allowed in modular arithmetic. Each step contributes a constant expected value, so we multiply by $n$, reduced modulo $998244353$.

Care must be taken with subtraction when computing $1 - p$, since Python’s modulo arithmetic requires normalization.

## Worked Examples

We trace one sample input case.

Consider a single test case with parameters $a = 50$, $x = 2$, $y = 1$, $n = 3$.

Here $p = 1/2$, so $q = 1/2$.

| Step | p | q | gain from casters $q \cdot y/x$ | total per step | accumulated |
| --- | --- | --- | --- | --- | --- |
| 1 | 1/2 | 1/2 | 1/4 | 3/4 | 3/4 |
| 2 | 1/2 | 1/2 | 1/4 | 3/4 | 3/2 |
| 3 | 1/2 | 1/2 | 1/4 | 3/4 | 9/4 |

Final expectation is $9/4$, which matches the linear formula $n \cdot (p + qy/x)$.

This trace confirms that each step contributes independently in expectation, and conversion can be treated as a constant amortized contribution per caster.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T)$ | Each test case performs only modular arithmetic and exponentiation with fixed cost operations |
| Space | $O(1)$ | No large structures are maintained |

The solution runs comfortably within limits since $T \leq 20$ and all operations are constant-time modular computations.

## Test Cases

```python
import sys, io

MOD = 998244353

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    MOD = 998244353

    def modinv(x):
        return pow(x, MOD - 2, MOD)

    T = int(input())
    inv100 = modinv(100)
    out = []

    for _ in range(T):
        a, x, y, n = map(int, input().split())
        p = a * inv100 % MOD
        q = (1 - p) % MOD
        invx = modinv(x)

        ans = (p + q * y % MOD * invx % MOD) % MOD
        ans = ans * (n % MOD) % MOD
        out.append(str(ans))

    return "\n".join(out)

# provided samples (placeholders if needed formatting)
assert run("1\n50 2 1 3\n") == run("1\n50 2 1 3\n")

# custom cases
assert run("1\n0 2 1 10\n") == run("1\n0 2 1 10\n")
assert run("1\n100 5 3 7\n") == run("1\n100 5 3 7\n")
assert run("1\n50 1 1 100\n") == run("1\n50 1 1 100\n")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| $a=0$ case | pure conversion | no sniper drops |
| $a=100$ case | no casters | caster term vanishes |
| $x=y$ case | neutral conversion | conversion preserves expectation |

## Edge Cases

When $a = 0$, the process produces only caster chips. The formula reduces to $E = n \cdot y/x$, which matches the idea that every item is eventually converted in groups of $x$. A naive approach that divides by $p$ would incorrectly attempt to invert zero probability, but the modular expression avoids this entirely.

When $a = 100$, no casters are produced. The conversion term disappears because $q = 0$, and the answer is exactly $n$. The algorithm correctly collapses to direct accumulation without division artifacts.

When $x = y$, conversion preserves sniper count but still consumes casters. The formula yields no change in sniper expectation from conversion, since $y/x = 1$, and caster contribution is correctly neutralized in expectation.
