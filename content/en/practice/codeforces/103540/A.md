---
title: "CF 103540A - I will win"
description: "We are simulating a tournament made of exactly $n$ games, where each game independently either increases or decreases your position on a linear ranking scale. You start at rank $n+1$."
date: "2026-07-03T05:46:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103540
codeforces_index: "A"
codeforces_contest_name: "CP Course Contest"
rating: 0
weight: 103540
solve_time_s: 39
verified: true
draft: false
---

[CF 103540A - I will win](https://codeforces.com/problemset/problem/103540/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a tournament made of exactly $n$ games, where each game independently either increases or decreases your position on a linear ranking scale. You start at rank $n+1$. Every win moves you one step closer to the top by decreasing your rank by 1, while every loss pushes you away from the top by increasing your rank by 1.

The tournament ends successfully for you only if after all $n$ games you end up exactly at rank 1. Since you start at $n+1$, reaching rank 1 means your net movement over all games must be exactly $-n$, which corresponds to winning all $n$ games. Any loss immediately introduces a +1 shift that makes it impossible to compensate later because the number of games is fixed and symmetric with the target displacement.

Each game is won with probability $p/q$, and lost with probability $1 - p/q = (q - p)/q$. The output is the probability that you win all games, expressed modulo $10^9 + 7$ as a fraction $x \cdot y^{-1}$, where $x/y$ is the probability in reduced algebraic form.

The constraints allow up to $2 \cdot 10^5$ test cases, with $n, p, q$ up to $10^{18}$. This immediately rules out any factorial or combinatorial DP over $n$. Even $O(n)$ per test case is impossible, so the solution must reduce each test case to constant-time modular arithmetic.

A subtle edge case appears when $p = 0$, where winning probability is zero unless $n = 0$, but $n \ge 1$ always, so the answer must be 0. Another corner case is $p = q$, where probability becomes 1, and modular inverse logic must not accidentally divide by zero.

A naive mistake is to interpret the process as a random walk and try to compute probabilities of reaching rank 1 via DP over states. That would implicitly depend on paths of length $n$, leading to exponential or polynomial time that is unnecessary.

## Approaches

A direct simulation of the tournament would iterate over all $n$ games, multiplying probabilities depending on win/loss outcomes. This immediately becomes infeasible because $n$ can be as large as $10^{18}$, so even writing down all states is impossible.

A more structured attempt is to model the rank as a random walk and compute the probability that after $n$ steps we are exactly at position 1. That would normally require binomial reasoning: choosing which subset of games are wins. The probability that exactly $k$ wins occur is $\binom{n}{k}(p/q)^k((q-p)/q)^{n-k}$. However, reaching rank 1 requires all $n$ steps to be wins, meaning $k=n$. In that case the binomial coefficient collapses to 1 and all other terms vanish because any loss invalidates the target.

So instead of summing over many configurations, the problem reduces to a single configuration: the sequence of all wins. The probability of that event is simply $(p/q)^n$. The only remaining task is computing modular exponentiation of a fraction, which is done by splitting numerator and denominator powers.

We compute:

$$\left(\frac{p}{q}\right)^n = p^n \cdot (q^n)^{-1} \pmod{10^9+7}$$

This reduces each test case to two fast exponentiations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force simulation | $O(n)$ | $O(1)$ | Too slow |
| Optimal modular exponentiation | $O(\log n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

### Key idea

We only need the probability of winning every single game, since any loss immediately makes reaching rank 1 impossible.

### Steps

1. Read integers $n, p, q$ for each test case. These define the exponent and the success probability per game.
2. Compute $p^n \bmod M$, where $M = 10^9 + 7$. This represents the numerator of the probability of winning all games. We use binary exponentiation because $n$ can be up to $10^{18}$, and repeated multiplication would be too slow.
3. Compute $q^n \bmod M$. This represents the denominator after raising the probability to the $n$-th power.
4. Compute the modular inverse of $q^n$ modulo $M$. Since $M$ is prime, we use Fermat’s theorem:

$$(q^n)^{-1} \equiv (q^n)^{M-2} \pmod{M}$$

1. Multiply $p^n$ with the modular inverse of $q^n$, then output the result.

### Why it works

The rank condition forces a unique successful trajectory: every game must be a win. There is no combinatorial choice of mixed outcomes that can still end at rank 1. Because probabilities multiply across independent events, the total probability factorizes into a single product of identical terms. Modular arithmetic preserves multiplication structure, so computing numerator and denominator separately and combining via modular inverse gives the exact probability in modular form.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def mod_pow(a, e):
    res = 1
    a %= MOD
    while e > 0:
        if e & 1:
            res = (res * a) % MOD
        a = (a * a) % MOD
        e >>= 1
    return res

t = int(input())
for _ in range(t):
    n, p, q = map(int, input().split())

    if p == 0:
        print(0)
        continue

    num = mod_pow(p, n)
    den = mod_pow(q, n)

    ans = num * mod_pow(den, MOD - 2) % MOD
    print(ans)
```

The implementation uses binary exponentiation for both $p^n$ and $q^n$. The modular inverse is computed using Fermat’s little theorem, which is valid because $10^9+7$ is prime. The special case $p = 0$ avoids unnecessary exponentiation and directly outputs zero.

A common pitfall is attempting to compute $(p/q)^n$ by dividing first and then exponentiating, which is invalid in modular arithmetic. The correct approach is to exponentiate numerator and denominator separately and combine via inverse.

## Worked Examples

### Example 1

Input: $n=2, p=1, q=2$

We compute:

| Step | Value |
| --- | --- |
| $p^n$ | $1^2 = 1$ |
| $q^n$ | $2^2 = 4$ |
| inverse of $4$ | $4^{MOD-2}$ |
| answer | $1 \cdot 4^{-1}$ |

This matches probability $1/4$, meaning both games must be won, each with probability $1/2$.

The trace confirms that intermediate rank states never matter because any loss breaks the required final condition.

### Example 2

Input: $n=3, p=2, q=2$

| Step | Value |
| --- | --- |
| $p^n$ | $2^3 = 8$ |
| $q^n$ | $2^3 = 8$ |
| inverse of $8$ | $8^{-1}$ |
| answer | $8 \cdot 8^{-1} = 1$ |

This confirms that when $p=q$, every game is guaranteed to be a win, so the probability of winning the tournament is 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T \log n)$ | Each test case uses binary exponentiation for two powers |
| Space | $O(1)$ | Only a constant number of variables are stored |

The solution easily fits within limits because even with $2 \cdot 10^5$ test cases, logarithmic exponentiation over $10^{18}$ is fast enough in Python.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def mod_pow(a, e):
    res = 1
    a %= MOD
    while e > 0:
        if e & 1:
            res = (res * a) % MOD
        a = (a * a) % MOD
        e >>= 1
    return res

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, p, q = map(int, input().split())

        if p == 0:
            out.append("0")
            continue

        num = mod_pow(p, n)
        den = mod_pow(q, n)
        ans = num * mod_pow(den, MOD - 2) % MOD
        out.append(str(ans))

    return "\n".join(out)

# provided sample (conceptual placeholder)
# assert solve("...") == "..."

# custom tests
assert solve("1\n1 1 1\n") == "1"
assert solve("1\n1 0 5\n") == "0"
assert solve("1\n2 2 2\n") == "1"
assert solve("1\n3 1 2\n") == str((pow(1,3,MOD) * pow(pow(2,3,MOD), MOD-2, MOD)) % MOD)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| $1,1,1$ | 1 | trivial guaranteed win |
| $1,0,5$ | 0 | impossible success case |
| $1,2,2$ | 1 | full certainty probability |
| $3,1,2$ | computed value | modular fraction handling |

## Edge Cases

When $p = 0$, the algorithm immediately returns 0 without exponentiation. This avoids computing $0^n$ for large $n$, which is safe but unnecessary. For example, input $n=100, p=0, q=7$ yields 0 because winning every game is impossible.

When $p = q$, both numerator and denominator become equal powers, so the result simplifies to 1. For instance $n=10^{18}, p=5, q=5$, both $5^n$ cancel exactly under modular inverse, and the algorithm returns 1 correctly.

When $n = 1$, the result becomes simply $p \cdot q^{-1}$, and the algorithm reduces correctly to a single modular fraction without any structural change.
