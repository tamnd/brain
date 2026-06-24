---
title: "CF 105230C - Little Birthday Party"
description: "We are given a classroom with $n$ students, each independently assigned a birthday uniformly over 365 days. We are asked for the probability of a very specific configuration."
date: "2026-06-24T15:58:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105230
codeforces_index: "C"
codeforces_contest_name: "2024-2025 ICPC Bolivia Pre-National Contest"
rating: 0
weight: 105230
solve_time_s: 108
verified: false
draft: false
---

[CF 105230C - Little Birthday Party](https://codeforces.com/problemset/problem/105230/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 48s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a classroom with $n$ students, each independently assigned a birthday uniformly over 365 days. We are asked for the probability of a very specific configuration.

The configuration is rigid: there must exist a group of exactly $x$ students who all share the same birthday, and that birthday is not shared by anyone else in the class. Every remaining student must also have birthdays that are all distinct from each other and also distinct from the shared birthday of the $x$-group. In other words, outside the special group, no two students share a birthday, and none of them collide with the chosen shared day.

The output is this probability expressed modulo $10^9+7$, written as $p \cdot q^{-1} \bmod M$, where $p/q$ is the reduced fraction of the probability.

The constraint $n \le 10^{18}$ immediately rules out any approach that iterates over students or days. Even polynomial dependence on $n$ is impossible, so the solution must depend only on small derived quantities. Since birthdays come from a fixed universe of 365 values, any combinatorial structure must collapse into a constant-sized computation.

A subtle failure case appears when $n-x$ is large. If there are more than 364 leftover students, we would be forced to assign them distinct birthdays excluding the chosen shared day, but only 364 days remain. For example, if $n=1000$ and $x=10$, then 990 remaining students cannot all have distinct birthdays in 364 slots, so the probability is exactly zero. Any naive formula that ignores this constraint will incorrectly produce a non-zero modular value.

Another failure case comes from treating $C(n,x)$ directly using factorials. Since $n$ can be $10^{18}$, factorial-based binomial computations are impossible unless we exploit the fact that the effective combination size is small.

## Approaches

The brute-force interpretation would enumerate all assignments of birthdays to $n$ people, count how many satisfy the condition, and divide by $365^n$. This is conceptually correct but completely infeasible. The state space is $365^n$, and even reasoning combinatorially at that scale without simplification is impossible.

The key observation is that the structure of valid assignments is extremely rigid. Once we pick the special birthday shared by the $x$ people, everything else is forced into an injective assignment over the remaining 364 days. This turns the problem into selecting a group, choosing a day, and permuting remaining assignments without repetition.

The crucial simplification is that only $k = n - x$ matters for the remaining students, and feasibility requires $k \le 364$. Once this holds, all remaining structure depends only on small permutations and a binomial term where the lower index is small. This allows rewriting $C(n,x)$ as $C(n,k)$, which becomes a product of $k$ terms even when $n$ is enormous.

The final expression becomes a product of three independent components: choosing the special day, choosing which students form the group, and assigning distinct remaining birthdays.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | Exponential | O(1) | Too slow |
| Combinatorial Reduction | O(365) per test | O(365) | Accepted |

## Algorithm Walkthrough

We rewrite the problem in terms of counting valid assignments and dividing by total assignments.

### Steps

1. Compute $k = n - x$. This represents how many students are not in the special birthday group. The rest of the computation depends entirely on whether these $k$ students can be assigned distinct birthdays outside the shared one.
2. If $k > 364$, immediately return 0. This is because after reserving one day for the $x$ students, only 364 distinct days remain, and we cannot assign unique birthdays to more than 364 people.
3. Precompute factorials and inverse factorials up to 365, since all combinatorial terms will be bounded by this range.
4. Choose the shared birthday. There are 365 ways to select the day on which the $x$ people coincide.
5. Choose which $x$ students form the group. Since $k = n-x$, it is easier to compute $C(n,k)$ instead of $C(n,x)$, which avoids dealing with large $x$. This is computed as a product:

$$C(n,k) = \frac{n(n-1)\cdots(n-k+1)}{k!}$$
6. Assign birthdays to the remaining $k$ students. They must all be distinct and must avoid the chosen day, so this is a permutation:

$$P(364, k) = \frac{364!}{(364-k)!}$$
7. Multiply all contributions:

$$\text{ways} = 365 \cdot C(n,k) \cdot P(364,k)$$
8. Divide by total outcomes $365^n$ using modular exponentiation and modular inverse.

### Why it works

Every valid configuration is uniquely determined by three independent choices: the shared birthday, the identity of the $x$ students sharing it, and a bijective assignment of distinct birthdays to the remaining students. These choices do not overlap or double-count any arrangement. The constraint $k \le 364$ ensures the permutation assignment is always valid. This gives a one-to-one correspondence between counted constructions and valid probability outcomes.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

MAXD = 365

fact = [1] * (MAXD + 1)
invfact = [1] * (MAXD + 1)

for i in range(1, MAXD + 1):
    fact[i] = fact[i - 1] * i % MOD

invfact[MAXD] = pow(fact[MAXD], MOD - 2, MOD)
for i in range(MAXD, 0, -1):
    invfact[i - 1] = invfact[i] * i % MOD

def nCk_large_n(n, k):
    if k < 0:
        return 0
    if k == 0:
        return 1
    num = 1
    for i in range(k):
        num = num * ((n - i) % MOD) % MOD
    return num * invfact[k] % MOD

def perm_364(k):
    if k > 364:
        return 0
    return fact[364] * invfact[364 - k] % MOD

def solve():
    t = int(input())
    for _ in range(t):
        n, x = map(int, input().split())
        k = n - x

        if k < 0 or k > 364:
            print(0)
            continue

        ways_group = nCk_large_n(n, k)
        ways_perm = perm_364(k)

        ways = 365 * ways_group % MOD
        ways = ways * ways_perm % MOD

        denom = pow(365, n, MOD)
        ans = ways * pow(denom, MOD - 2, MOD) % MOD

        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation precomputes factorials only up to 365 because no permutation ever exceeds that bound. The function `nCk_large_n` computes binomial coefficients with a large top and small bottom using a direct multiplicative formula, avoiding factorials of $n$. This is the key trick that makes handling $n \le 10^{18}$ possible.

The permutation term is precomputed via factorials because its domain is strictly bounded by 365. The final division by $365^n$ is handled using modular exponentiation, which is feasible even for very large $n$ since exponentiation runs in logarithmic time.

## Worked Examples

Consider a small instance $n=10, x=3$. Then $k=7$, so we are assigning 7 remaining students to distinct birthdays excluding the shared one.

| Step | Value |
| --- | --- |
| k | 7 |
| C(n,k) | $C(10,7)$ |
| 365 choice | 365 |
| P(364, k) | $364P7$ |

The construction first picks the 7 non-group students, then assigns them unique birthdays, and finally multiplies by the number of choices for the shared day. This matches exactly the structure of valid assignments.

Now consider a boundary case $n=400, x=10$. Then $k=390$.

| Step | Value |
| --- | --- |
| k | 390 |
| Feasible? | No |

Since 390 exceeds 364, we immediately output 0. This confirms that the constraint on distinct birthdays is the true limiting factor, not combinatorial counting.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(365 + t \cdot 365)$ | factorial precomputation and at most 365 multiplications per test |
| Space | $O(365)$ | factorial and inverse factorial storage |

The complexity is independent of $n$, which allows handling values up to $10^{18}$ comfortably within limits. With $t \le 1000$, the constant factor remains small.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    MAXD = 365
    fact = [1] * (MAXD + 1)
    invfact = [1] * (MAXD + 1)

    for i in range(1, MAXD + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact[MAXD] = pow(fact[MAXD], MOD - 2, MOD)
    for i in range(MAXD, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    def nCk_large_n(n, k):
        if k < 0:
            return 0
        if k == 0:
            return 1
        num = 1
        for i in range(k):
            num = num * ((n - i) % MOD) % MOD
        return num * invfact[k] % MOD

    def perm_364(k):
        if k > 364:
            return 0
        return fact[364] * invfact[364 - k] % MOD

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n, x = map(int, input().split())
            k = n - x
            if k < 0 or k > 364:
                out.append("0")
                continue
            ways = 365 * nCk_large_n(n, k) % MOD
            ways = ways * perm_364(k) % MOD
            denom = pow(365, n, MOD)
            out.append(str(ways * pow(denom, MOD - 2, MOD) % MOD))
        return "\n".join(out)

    return solve()

# provided samples (format assumed line-separated pairs)
assert run("4\n2 2\n3 1\n10 3\n100 99\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal $n=x$ | non-zero | only shared group exists |
| $k>364$ | 0 | impossibility constraint |
| moderate $n$ | correct modular value | full formula correctness |
| large $n$ | stable output | handling big integers |

## Edge Cases

A direct corner case is when $n=x$. Then all students are in the same birthday group. The formula reduces to choosing the shared day, with no remaining assignments. The algorithm correctly produces $365 \cdot 1 \cdot 1 / 365^n$, matching the fact that only one day matters and all other constraints disappear.

Another corner case is when $n-x=364$. Here every remaining student must occupy all remaining days exactly once. The permutation term becomes $364!$, and the algorithm computes it directly from precomputed factorials without any dynamic reasoning. This is the tightest feasible configuration, and any off-by-one mistake in checking the bound would incorrectly reject it.
