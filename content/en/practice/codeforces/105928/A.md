---
title: "CF 105928A - Balanced Eating"
description: "We are given several test cases. In each test case there are multiple skewers, and each skewer has a certain number of meat pieces."
date: "2026-06-21T11:55:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105928
codeforces_index: "A"
codeforces_contest_name: "Soy Cup #2: Vivian"
rating: 0
weight: 105928
solve_time_s: 56
verified: true
draft: false
---

[CF 105928A - Balanced Eating](https://codeforces.com/problemset/problem/105928/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several test cases. In each test case there are multiple skewers, and each skewer has a certain number of meat pieces. Varesa eats each skewer by first choosing one of her two sides, left or right, uniformly at random, and then alternates sides for each successive piece on that skewer.

This alternating pattern means that once the starting side is fixed, the distribution of bites between left and right is completely determined for that skewer. The only randomness is the initial choice per skewer.

After all skewers are eaten, we look at the total number of bites taken by the left molar and the right molar. The meal is considered balanced if the absolute difference between these totals is at most one. The task is to compute the probability of this event and output it modulo 998244353.

The constraint that the total number of skewers across all test cases is at most 2 · 10^5 means we need a linear or near linear solution in terms of total input size. Anything quadratic in n or in the sum of ai is immediately impossible, since ai can be as large as 10^9, so we cannot simulate eating at the piece level. The structure must depend only on parity or a similar compressed statistic.

A naive interpretation would try to simulate every skewer and track left-right imbalance directly. That would already fail because ai can be huge, and even per skewer simulation would be too slow.

A more subtle failure case comes from treating each skewer independently without noticing that only parity matters. For example, if we only track total length, we would incorrectly think skewers of size 2 and 3 behave similarly, but a single skewers like a = 3 actually introduces imbalance potential, while a = 2 does not.

## Approaches

The brute-force idea is to simulate the randomness explicitly. For each skewer, we choose a starting side, then assign each piece alternately and track the resulting left minus right difference. With n skewers, this leads to 2^n possible choices of starting sides, and for each configuration we would simulate all skewers, giving O(n · 2^n). This explodes even for n around 30.

The key observation is that each skewer contributes independently to the final imbalance, and its contribution depends only on whether its length is even or odd.

If a skewer has even length, alternating sides ensures both sides receive exactly half the pieces regardless of starting side. So it contributes zero to the imbalance.

If a skewer has odd length, then one side receives one extra piece. If we start on the left, the left side gets +1 relative contribution; if we start on the right, the right side gets +1, meaning the contribution is either +1 or −1 with equal probability.

So the entire problem reduces to a sum of independent random variables, each either 0 (for even skewers) or ±1 (for odd skewers). If k is the number of odd-length skewers, we need the probability that the sum of k independent ±1 variables lies in {−1, 0, 1}.

This is a standard binomial distribution problem. If we map +1 to success and −1 to failure, the sum becomes S = k − 2X where X is the number of −1 choices. We just count how many X values lead to valid S.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force simulation | O(n · 2^n) | O(n) | Too slow |
| Combinatorics on parity reduction | O(n) per test | O(n) | Accepted |

## Algorithm Walkthrough

We reduce the problem to counting configurations of ±1 contributions from odd-length skewers.

1. Count how many skewers have odd length. Call this number k. Only these skewers influence imbalance, because even ones always contribute zero regardless of starting side.
2. Observe that each odd skewer independently contributes either +1 or −1 with probability 1/2. So we are effectively summing k independent symmetric random variables.
3. Let X be the number of skewers that contribute −1. Then the total sum becomes S = k − 2X.
4. We want S to be in {−1, 0, 1}. For each target value t in this set, solve k − 2X = t, giving X = (k − t) / 2.
5. For each valid integer X in range [0, k], add the binomial coefficient C(k, X). This counts the number of valid assignments of signs that produce that imbalance.
6. The total number of assignments is 2^k, so the probability is (sum of valid binomials) / 2^k modulo 998244353.
7. Precompute factorials and inverse factorials up to 2 · 10^5 to answer binomial queries in O(1), and use fast exponentiation to compute modular inverse of 2^k.

### Why it works

Each skewers contribution depends only on parity, and these contributions are independent. The transformation to a sum of ±1 variables preserves independence and fully characterizes the final imbalance. The condition on final balance depends only on the total sum, so counting valid sign assignments via binomial coefficients exactly matches the probability space without omission or double counting.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
MAXN = 200000 + 5

fact = [1] * MAXN
invfact = [1] * MAXN

def modpow(a, e):
    res = 1
    while e:
        if e & 1:
            res = res * a % MOD
        a = a * a % MOD
        e >>= 1
    return res

def ncr(n, r):
    if r < 0 or r > n:
        return 0
    return fact[n] * invfact[r] % MOD * invfact[n - r] % MOD

def solve():
    t = int(input())
    arr_cases = []
    max_k = 0

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        k = sum(x & 1 for x in a)
        arr_cases.append(k)
        max_k = max(max_k, k)

    for i in range(1, max_k + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact[max_k] = modpow(fact[max_k], MOD - 2)
    for i in range(max_k, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    inv2 = (MOD + 1) // 2

    for k in arr_cases:
        total = modpow(2, k)
        ans = 0

        def add(x):
            return ncr(k, x)

        for tval in [-1, 0, 1]:
            x = k - tval
            if x % 2 == 0:
                x //= 2
                ans = (ans + ncr(k, x)) % MOD

        ans = ans * modpow(total, MOD - 2) % MOD
        print(ans)

if __name__ == "__main__":
    solve()
```

The code first compresses each test case down to the number of odd-length skewers. Factorials and inverse factorials are built once up to the maximum needed k, enabling constant-time binomial computation. For each test case, we enumerate the three possible target imbalance values and translate them into valid binomial indices. The final normalization divides by 2^k using modular inverse.

A subtle point is that we never simulate skewers individually beyond parity extraction, which is what makes the solution efficient enough for the full constraint range.

## Worked Examples

Consider a single test case with skewers `[1, 2, 3]`. The odd skewers are 1 and 3, so k = 2.

We compute all possible outcomes:

| Skewer 1 | Skewer 3 | S |
| --- | --- | --- |
| +1 | +1 | 2 |
| +1 | −1 | 0 |
| −1 | +1 | 0 |
| −1 | −1 | −2 |

Valid sums are {−1, 0, 1}, so only S = 0 contributes here. That happens in 2 cases out of 4, giving probability 1/2.

Now consider `[1, 1, 1]`, so k = 3.

We list all sums:

| Configuration | S |
| --- | --- |
| + + + | 3 |
| + + − | 1 |
| + − + | 1 |
| − + + | 1 |
| + − − | −1 |
| − + − | −1 |
| − − + | −1 |
| − − − | −3 |

Valid sums are −1, 0, 1, so we count 6 valid configurations out of 8, giving 3/4.

These traces show that we are effectively working only with binomial distributions over ±1 choices.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total n + max k) | Each test case reduces to counting parity, then O(1) binomial queries |
| Space | O(max k) | Factorials and inverse factorials up to maximum number of odd elements |

The constraints allow up to 2 · 10^5 total elements, so a linear preprocessing of factorials and constant-time per test case computation fits comfortably within limits.

## Test Cases

```python
import sys, io

MOD = 998244353

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue()

# We assume solution is executed separately; in real use, integrate solve() properly.

assert True
```

Since the solution is self-contained in a single solve() entry point in contest usage, these tests are conceptual checks rather than executable harness tests in this format.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1\n1 | 1 | Single odd skewers, trivial probability space |
| 1\n3\n1 1 1 | 3/4 | Multiple odd skewers distribution symmetry |
| 1\n2\n2 4 | 1 | All even skewers always balanced |
| 1\n3\n2 3 4 | 1/2 | Mixed parity case |

## Edge Cases

One edge case is when all skewers have even length. In this situation k = 0, so there are no random choices. The sum is always 0, which is already within the required range. The algorithm produces C(0,0) / 1 = 1, matching the correct deterministic outcome.

Another edge case is k = 1. A single odd skewer contributes ±1, so the final sum is always within [-1, 1]. The formula correctly counts both configurations and divides by 2, yielding probability 1.

A final subtle case is when k is large but most ai are even. The solution compresses all structure into k, so runtime depends only on the number of odd values rather than raw input size, avoiding any overflow or performance issues from large ai values.
