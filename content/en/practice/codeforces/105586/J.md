---
title: "CF 105586J - \u597d\u5f97\u4e0d\u80fd\u518d\u597d\u4e86\uff01\u6cf0\u62c9\u6295\u8d44\u5927\u5e08\u8bfe"
description: "We are given a repeated experiment where each trial independently results in a win with probability $frac{p}{q}$ and a loss with probability $1 - frac{p}{q}$. We start from zero wins and zero losses, and we keep playing until one of two stopping conditions is reached."
date: "2026-06-22T06:01:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105586
codeforces_index: "J"
codeforces_contest_name: "\u201c\u534e\u4e3a\u676f\u201d 2024 \u5e74\u5e7f\u4e1c\u5de5\u4e1a\u5927\u5b66 ACM \u65b0\u751f\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b\uff08\u51b3\u8d5b\uff09"
rating: 0
weight: 105586
solve_time_s: 55
verified: true
draft: false
---

[CF 105586J - \u597d\u5f97\u4e0d\u80fd\u518d\u597d\u4e86\uff01\u6cf0\u62c9\u6295\u8d44\u5927\u5e08\u8bfe](https://codeforces.com/problemset/problem/105586/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a repeated experiment where each trial independently results in a win with probability $\frac{p}{q}$ and a loss with probability $1 - \frac{p}{q}$. We start from zero wins and zero losses, and we keep playing until one of two stopping conditions is reached. The process stops successfully if we obtain $n$ wins before we accumulate $n$ losses. It fails if losses reach $n$ first.

The task is to compute the probability of success under this stopping rule, and output it modulo $10^9 + 7$.

A useful way to reinterpret the process is as a one-dimensional walk. Each win moves us +1, each loss moves us -1. We start at position 0. The process ends when we hit either $+n$ (success) or $-n$ (failure). The question becomes: what is the probability that a biased random walk hits $+n$ before $-n$?

The constraints allow up to $10^4$ test cases and a total of $5 \cdot 10^6$ across all $n$. This rules out any simulation or DP over all states per test case. Any solution must reduce each test case to logarithmic or constant-time modular exponentiation.

A naive approach that simulates the walk would require exponential time in expectation before absorption, and is immediately impossible. Even a dynamic programming solution over states from $-n$ to $n$ per test case would be $O(n^2)$ or at best $O(n)$, which is too slow for the global constraints.

A subtle edge case appears when $\frac{p}{q} = \frac{1}{2}$. In this symmetric case, the random walk has no drift, and symmetry implies the probability of reaching $+n$ before $-n$ is exactly $\frac{1}{2}$, independent of $n$. A formula-based implementation that blindly divides by $1 - r^{2n}$ will still work, but can suffer from modular instability if not handled carefully.

## Approaches

The brute-force idea is to model the process as a Markov chain over states representing current net score and compute absorption probabilities using dynamic programming. Let $dp[i]$ be the probability of eventually reaching $+n$ starting from state $i$. We would set boundary conditions $dp[n] = 1$ and $dp[-n] = 0$, and then solve a linear recurrence. However, each state depends on two neighbors, and solving this system for all states requires either iterative relaxation or Gaussian elimination on a tridiagonal system. Even with optimizations, doing this independently for each test case is far too slow given total $n$ up to $5 \cdot 10^6$.

The key observation is that this is a classical gambler’s ruin problem with symmetric absorbing boundaries. Such processes admit a closed-form solution depending only on the ratio between step probabilities, not on the absolute structure of the DP graph. Once we express the system in terms of a ratio $r = \frac{q-p}{p}$, the probability collapses into a simple geometric expression derived from solving the recurrence relation.

This reduces each test case to computing a few modular exponentiations and modular inverses.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| DP over states | $O(n)$ per test | $O(n)$ | Too slow |
| Optimal closed form | $O(\log n)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

We transform the probability model into a biased random walk with absorbing boundaries and then evaluate the known closed form.

1. Convert the probability of success into modular arithmetic form. The probability of a win in one step is $\frac{p}{q}$, so we work with modular inverses to represent fractions under $10^9 + 7$.
2. Define the failure probability as $\frac{q-p}{q}$. This allows us to express the bias of the walk using a ratio of failure to success.
3. Construct the drift ratio $r = \frac{q-p}{p}$. This ratio captures how much more likely we are to move downward than upward in a single step, independent of the common denominator $q$.
4. Compute $r^n$ and $r^{2n}$ using fast exponentiation under the modulus. These values correspond to the probability-weighted contributions of paths that reach the absorbing boundaries.
5. If $r = 1$, which occurs when $q = 2p$, directly output $\frac{1}{2}$ modulo $10^9 + 7$, since the walk is symmetric.
6. Otherwise compute the final probability using the closed form:

$$\frac{1 - r^n}{1 - r^{2n}}$$

under modular arithmetic, replacing division with multiplication by modular inverse.

The correctness comes from solving the recurrence for absorption probabilities in a bounded biased random walk. The probability function satisfies a second-order linear recurrence with constant coefficients. Its general solution is a linear combination of powers of $r$, and the boundary conditions at $-n$ and $+n$ uniquely determine the coefficients, yielding exactly the stated formula.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def mod_pow(a, e):
    res = 1
    while e:
        if e & 1:
            res = res * a % MOD
        a = a * a % MOD
        e >>= 1
    return res

def solve():
    T = int(input())
    inv2 = (MOD + 1) // 2

    for _ in range(T):
        n, p, q = map(int, input().split())

        if 2 * p == q:
            print(inv2)
            continue

        # r = (q-p)/p
        r = (q - p) * pow(p, MOD - 2, MOD) % MOD

        rn = mod_pow(r, n)
        r2n = rn * rn % MOD

        numerator = (1 - rn) % MOD
        denominator = (1 - r2n) % MOD

        ans = numerator * pow(denominator, MOD - 2, MOD) % MOD
        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation first converts the probability into a ratio that eliminates the common denominator $q$. This is important because keeping $q$ inside the exponentiation would be unnecessary and slower.

Fast exponentiation is used for $r^n$ because $n$ can be as large as $10^5$, and there are many test cases. The modular inverse is applied only at the final division step, avoiding repeated inversions.

The symmetric case is handled separately to avoid division by zero in the expression $1 - r^{2n}$, which would otherwise become zero when $r = 1$.

## Worked Examples

Consider a simple case $n = 1, p = 1, q = 2$. Here $r = 1$, so we immediately fall into the symmetric branch. The answer is $\frac{1}{2}$.

| Step | r | r^n | r^{2n} | Result |
| --- | --- | --- | --- | --- |
| init | 1 | 1 | 1 | symmetric case |

This confirms that when success and failure are equally likely, the first step decides everything.

Now consider $n = 2, p = 1, q = 3$. Then success probability is $1/3$, failure is $2/3$, so $r = 2$.

| Step | r | r^2 | r^4 | numerator | denominator |
| --- | --- | --- | --- | --- | --- |
| compute | 2 | 4 | 16 | $1-4$ | $1-16$ |

The final probability becomes:

$$\frac{-3}{-15} = \frac{1}{5}$$

This matches the intuition that the process is biased toward failure, so reaching two successes before two failures is relatively unlikely.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T \log n)$ | each test case requires modular exponentiation for powers of $n$ |
| Space | $O(1)$ | only a constant number of variables are maintained |

The constraints allow up to $5 \cdot 10^6$ total $n$, and logarithmic exponentiation per test case is fast enough in Python when implemented iteratively.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7
inv2 = (MOD + 1) // 2

def solve():
    input = sys.stdin.readline
    T = int(input())
    for _ in range(T):
        n, p, q = map(int, input().split())
        if 2 * p == q:
            print(inv2)
            continue
        r = (q - p) * pow(p, MOD - 2, MOD) % MOD
        rn = pow(r, n, MOD)
        r2n = rn * rn % MOD
        ans = (1 - rn) * pow((1 - r2n) % MOD, MOD - 2, MOD) % MOD
        print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio
    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample-like tests
assert run("1\n1 1 2\n") == str(inv2)

# symmetric case
assert run("1\n5 1 2\n") == str(inv2)

# small biased case
assert run("1\n2 1 3\n") == str(pow(5, MOD-2, MOD))

# multiple tests
assert run("2\n1 1 2\n2 1 3\n") == str(inv2) + "\n" + str(pow(5, MOD-2, MOD))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| symmetric $p/q=1/2$ | $1/2$ | equal probability branch |
| small biased case | computed fraction | correctness of formula |
| multiple test cases | per-case independence | handling of T |

## Edge Cases

The most delicate situation is when $q = 2p$. In this case the ratio $r = \frac{q-p}{p} = 1$, which makes the denominator $1 - r^{2n}$ become zero. A naive implementation would attempt modular inversion of zero and crash or produce garbage. The explicit symmetric handling avoids this completely by short-circuiting to $\frac{1}{2}$.

Another subtle case is when $n = 1$. The process ends after a single step, so the answer must be exactly the probability of winning the first trial, which is $\frac{p}{q}$. Plugging into the formula:

$$\frac{1 - r}{1 - r^2} = \frac{1}{1 + r} = \frac{p}{q}$$

which confirms consistency.

Finally, when probabilities are large and modular inverses are computed repeatedly, forgetting to reduce intermediate values can lead to overflow or incorrect modular arithmetic. Keeping all intermediate values modulo $10^9 + 7$ ensures stability throughout the computation.
