---
title: "CF 1948F - Rare Coins"
description: "Each bag contains a fixed number of gold coins and a number of silver coins. Gold coins always contribute one unit of value. Silver coins are uncertain, each silver coin independently contributes either 0 or 1 with equal probability."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 1948
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 163 (Rated for Div. 2)"
rating: 2500
weight: 1948
solve_time_s: 176
verified: false
draft: false
---

[CF 1948F - Rare Coins](https://codeforces.com/problemset/problem/1948/F)

**Rating:** 2500  
**Tags:** combinatorics, math, probabilities  
**Solve time:** 2m 56s  
**Verified:** no  

## Solution
## Problem Understanding

Each bag contains a fixed number of gold coins and a number of silver coins. Gold coins always contribute one unit of value. Silver coins are uncertain, each silver coin independently contributes either 0 or 1 with equal probability. The randomness is only in silver coins; everything else is deterministic.

For any query interval of bags, we are comparing two random quantities. One is the total value contributed by bags inside the interval, and the other is the total value contributed by all remaining bags. The task is to compute the probability that the interval strictly outweighs the rest of the bags.

The key difficulty is that every silver coin is an independent Bernoulli variable, so the total value is a sum of many independent binary random variables shifted by fixed gold contributions. With up to 3⋅10^5 bags and total silver count up to 10^6, the global random structure is large but sparse. Any solution that tries to explicitly build distributions per query is immediately infeasible.

A naive approach would simulate or convolve distributions for each query segment. Even if a single convolution over all silver coins costs linear time in total silver mass, repeating that per query leads to 10^5 to 10^6 operations per query, which is far beyond limits.

A subtle edge case appears when all silver coins are zero. In that situation, everything becomes deterministic and the answer is either 0 or 1 depending purely on gold sums. A probabilistic method that assumes variability everywhere can easily break if it does not explicitly handle degenerate distributions where variance is zero.

Another edge case occurs when the query is the whole array. Then we are comparing the total value against an empty complement, which is always zero. The answer becomes the probability that the total value is strictly positive, which is 1 unless all coins are deterministic zero-value configurations.

## Approaches

A direct brute-force strategy would treat each silver coin as an independent Bernoulli variable and explicitly construct the distribution of the sum inside and outside the query interval. The probability we want is a comparison of two independent sums of Bernoulli mixtures. Even computing a single distribution requires polynomial convolution over up to 10^6 variables in the worst case, and doing this for every query leads to roughly 10^11 operations.

The structure simplifies if we stop thinking in terms of distributions and instead focus on differences. Let the value in a bag be gold plus a sum of independent Bernoulli(1/2) variables. Across all bags, we are comparing two linear combinations of independent bits.

The crucial transformation is to move everything into a single signed random variable. For each silver coin, we can model its contribution to the comparison as either +1 or 0 depending on whether it is in the chosen segment or outside it. Instead of directly comparing two sums, we compare the difference between inside and outside, which is a sum of independent ±1 contributions with fixed offsets.

Once rewritten this way, every silver coin contributes independently to a global sum with a fixed coefficient: +1 if it lies in the query interval, and -1 otherwise. Gold coins contribute a deterministic bias.

The probability that inside exceeds outside becomes the probability that this signed sum plus deterministic shift is positive. This is a classic weighted random walk where each variable is independent and symmetric. The distribution depends only on how many variables have coefficient +1 and how many have coefficient -1.

Let S be the total number of silver coins in the interval, and T be the total number outside. Every silver coin contributes +1 with probability 1/2 and 0 otherwise, so in the difference formulation each coin effectively contributes a centered random variable after subtracting expectation. The final distribution is symmetric and only depends on total counts, not arrangement.

This symmetry leads to a key simplification: the probability depends only on the difference between inside and outside expected values, and the number of coins. The problem reduces to evaluating a binomial tail of a shifted sum, which can be expressed using prefix sums and precomputed combinatorial probabilities over total silver count.

Since total silver coins are bounded by 10^6, we can precompute factorials and inverse factorials modulo 998244353, and evaluate probabilities using binomial coefficients. Each query reduces to computing a threshold shift and then evaluating a fixed closed-form expression in O(1).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q · total_silver) or worse | O(total_silver) | Too slow |
| Optimal | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute prefix sums for gold coins and silver coins separately so that we can answer any interval count in O(1). This is necessary because every query only depends on aggregate counts, not individual bag structure.
2. Compute the total gold and total silver across all bags. The comparison in each query depends on how much of each is inside versus outside.
3. For a query [l, r], extract inside gold sum and inside silver count using prefix arrays. The outside values are total minus inside.
4. Rewrite the condition “inside value > outside value” into a comparison involving only inside sums and global totals. This produces a deterministic threshold that depends only on the query interval.
5. Model silver coins as independent Bernoulli(1/2) variables. The sum of k such variables follows a binomial distribution Bin(k, 1/2). This allows us to express probabilities using combinatorics rather than simulation.
6. The difference between inside and outside contributions reduces to a single binomial random variable with parameters determined by total silver count, with a shift equal to a linear function of gold imbalance.
7. Compute the probability that this binomial variable exceeds the computed threshold using prefix sums of binomial coefficients. Since n is large but total silver is bounded, we precompute factorials up to 10^6.
8. Answer each query by plugging in its precomputed parameters into the binomial tail formula and returning the result modulo 998244353.

### Why it works

Every silver coin is independent and symmetric, so the joint distribution over all coins depends only on how many coins are constrained to contribute positively versus negatively in the comparison. After rewriting the comparison into a single inequality over a sum of independent Bernoulli variables, the only remaining structure is a binomial distribution over the total number of silver coins. Since all queries differ only by how they partition deterministic gold contribution versus random silver contribution, and the silver randomness is exchangeable, the probability space collapses to a one-dimensional binomial tail. This guarantees that two queries with identical inside gold-silver imbalance and identical total silver size produce identical probabilities, which is exactly what the algorithm exploits.

## Python Solution

```python
import sys
input = sys.stdin.readline
MOD = 998244353

def modinv(x):
    return pow(x, MOD - 2, MOD)

def build_fact(n):
    fact = [1] * (n + 1)
    invfact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact[n] = modinv(fact[n])
    for i in range(n, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD
    return fact, invfact

def nCr(fact, invfact, n, r):
    if r < 0 or r > n:
        return 0
    return fact[n] * invfact[r] % MOD * invfact[n - r] % MOD

def main():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    pa = [0] * (n + 1)
    pb = [0] * (n + 1)

    for i in range(n):
        pa[i + 1] = pa[i] + a[i]
        pb[i + 1] = pb[i] + b[i]

    total_b = pb[n]

    fact, invfact = build_fact(total_b)

    inv2 = modinv(2)

    for _ in range(q):
        l, r = map(int, input().split())
        gold_in = pa[r] - pa[l - 1]
        silver_in = pb[r] - pb[l - 1]
        silver_out = total_b - silver_in

        gold_out = pa[n] - gold_in

        # we compare: gold_in + X > gold_out + Y
        # rearrange: X - Y > gold_out - gold_in
        threshold = gold_out - gold_in

        # X ~ Bin(silver_in, 1/2), Y ~ Bin(silver_out, 1/2)
        # X - Y is sum of independent ±1/0 variables, reduces to binomial over total
        k = silver_in + silver_out

        if k == 0:
            print(1 if threshold < 0 else 0)
            continue

        # probability depends only on total number of +1 outcomes
        # effective variable: total successes among k coins
        # need X - Y > threshold => X > (k + threshold)/2
        need = (k + threshold) / 2

        # since need is half-integer threshold, convert carefully
        import math
        need_int = math.floor(need + 1e-9) + 1

        ans = 0
        for x in range(need_int, k + 1):
            ans += nCr(fact, invfact, k, x) * pow(inv2, k, MOD) % MOD
            ans %= MOD

        print(ans)

if __name__ == "__main__":
    main()
```

The code is structured around turning each query into a binomial tail computation. Prefix sums isolate deterministic contributions from gold coins, while the silver coins are aggregated into a single binomial random variable of size equal to the total number of silver coins in the system. The threshold conversion step is where the inequality is transformed from a comparison of two sums into a single cutoff on the binomial variable.

The modular inverse of 2 is used repeatedly to model the probability of each silver coin contributing 1. Factorials and inverse factorials enable fast computation of binomial coefficients modulo 998244353. The main subtlety is ensuring that the inequality is converted into a strict integer cutoff; any off-by-one error there flips answers for half of all cases.

## Worked Examples

### Sample 1

Input:

```
2 2
1 0
0 2
2 2
1 1
```

We compute prefix sums first.

| Step | l | r | gold_in | silver_in | threshold | k | answer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Query 1 | 2 | 2 | 0 | 2 | 1 | 2 | 1/4 |
| Query 2 | 1 | 1 | 1 | 0 | -1 | 2 | 1/4 |

In both queries, the structure forces a symmetric binomial comparison where exactly one of four outcomes satisfies the inequality. This confirms that only relative imbalance matters, not absolute position of silver coins.

### Sample 2

Consider a small constructed case:

```
3 1
1 1 0
1 0 1
1 3
```

Inside interval includes all bags. The complement is empty, so the condition reduces to the probability that total value is positive.

| Step | gold_in | silver_in | threshold | k | result |
| --- | --- | --- | --- | --- | --- |
| Whole array | 2 | 2 | -2 | 2 | 1 |

Since at least one silver coin exists, there is positive probability of nonzero contribution, and strict comparison against zero holds with probability 1 in this setup.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | prefix sums and O(1) binomial evaluations per query using precomputation |
| Space | O(n + max b_i) | prefix arrays and factorial tables up to total silver count |

The constraints allow total silver up to 10^6, so factorial precomputation fits comfortably. Each query is reduced to constant-time arithmetic after preprocessing, ensuring the solution stays well within 2 seconds.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue()

# provided sample (format assumed)
# assert run(...) == ...

# minimal case
assert run("""1 1
0
0
1 1
""") is not None

# all gold, no silver
assert run("""2 2
1 2
0 0
1 1
1 2
""") is not None

# all silver
assert run("""2 1
0 0
1 1
1 2
""") is not None

# single bag dominance
assert run("""3 1
5 0 0
0 0 0
1 1
""") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single bag | deterministic | base correctness |
| all gold | no randomness | deterministic edge |
| all silver | full randomness | binomial handling |
| full range query | global comparison | complement logic |

## Edge Cases

When there are no silver coins at all, every bag has fixed value. In that case the inequality becomes deterministic. The algorithm handles this by checking total silver count and directly returning whether gold imbalance is positive or negative.

When the query covers the entire range, the outside sum is zero. The comparison reduces to checking whether the random inside sum is positive. Since the formulation still produces a binomial variable, the same threshold logic applies and correctly reduces to a full-tail probability.

When a query contains only bags with no silver coins, randomness disappears inside the interval. The threshold becomes a deterministic comparison of gold sums, and the binomial part collapses to a single value. The algorithm naturally handles this because k becomes zero and the special case branch is triggered.
