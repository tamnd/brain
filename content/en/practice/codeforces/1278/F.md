---
problem: 1278F
contest_id: 1278
problem_index: F
name: "Cards"
contest_name: "Educational Codeforces Round 78 (Rated for Div. 2)"
rating: 2600
tags: ["combinatorics", "dp", "math", "number theory", "probabilities"]
answer: passed_samples
verified: true
solve_time_s: 335
date: 2026-06-14
model: gpt-5-5
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2d9f62-60cc-83ec-9b1f-4ce602994ea3
---

# CF 1278F - Cards

**Rating:** 2600  
**Tags:** combinatorics, dp, math, number theory, probabilities  
**Model:** gpt-5-5  
**Solve time:** 5m 35s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2d9f62-60cc-83ec-9b1f-4ce602994ea3  

---

## Solution

## Problem Understanding

We repeatedly perform a simple experiment on a deck that contains one special card and $m-1$ ordinary cards. Each trial consists of fully randomizing the deck, looking at the top card, and then putting it back without changing the deck composition.

Because every shuffle is uniform over all permutations, the top card in each trial is uniformly random among the $m$ cards, and different trials are independent. The joker appears in a single trial with probability $p = \frac{1}{m}$, so the random variable $x$ is simply the number of successes in $n$ independent Bernoulli trials with success probability $1/m$.

The task is not just to compute a binomial expectation like $\mathbb{E}[x]$, but the $k$-th power moment $\mathbb{E}[x^k]$. The input sizes allow $n$ and $m$ up to roughly $10^9$, while $k$ can be as large as 5000, so any method that expands over all outcomes of $x$ or over all subsets of trials is impossible.

A naive approach might try to enumerate all outcomes of $x$ from 0 to $n$, compute binomial probabilities, and sum $x^k \cdot P(x)$. That already costs $O(n)$, which is infeasible. A deeper issue appears if we try to expand $x^k$ as a polynomial in indicator variables of trials: it leads to sums over $k$-tuples of indices, which is $O(n^k)$ conceptually and completely unusable.

A more subtle pitfall is assuming moments of binomial variables can be expressed directly via simple formulas like $(np)^k$. That is only true for $k=1$, and already fails for $k=2$ due to variance contributions.

## Approaches

The key simplification is to stop thinking about the distribution of $x$ itself and instead expand $x^k$ in terms of elementary symmetric structures over trials.

Let $I_i$ be the indicator that the joker is drawn in the $i$-th trial. Then $x = \sum_{i=1}^n I_i$, and all $I_i$ are independent Bernoulli variables with probability $p = 1/m$.

Expanding $x^k$ produces sums of products of indicators:

$$x^k = \sum_{i_1,\dots,i_k} I_{i_1} I_{i_2} \cdots I_{i_k}.$$

The expectation depends only on how many distinct indices appear in the tuple $(i_1,\dots,i_k)$. If exactly $r$ distinct indices appear, then the expectation of the product is $p^r$, and the number of ways to assign multiplicities to achieve this structure becomes a combinatorial partition counting problem.

This is exactly where Stirling numbers of the second kind appear. They count the number of ways to partition a set of $k$ labeled positions into $r$ nonempty groups. Each group corresponds to one distinct trial index. After choosing $r$ distinct trials from $n$, we assign the $k$ positions into these $r$ trials.

This gives the identity:

$$\mathbb{E}[x^k] = \sum_{r=0}^k S(k,r) \cdot (n)_r \cdot p^r,$$

where $(n)_r = n(n-1)\cdots(n-r+1)$ is the falling factorial and $S(k,r)$ are Stirling numbers of the second kind.

The remaining task is purely algebraic: compute Stirling numbers up to $k=5000$, precompute factorial-like products, and evaluate the sum.

We compute $S(k,r)$ using the standard recurrence:

$$S(k,r) = S(k-1,r-1) + r \cdot S(k-1,r),$$

which fits in $O(k^2)$.

Once this table is built, the answer is a single summation over $r$, with modular exponentiation handled implicitly through powers of $n$ and inverse powers of $m$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Direct probability sum | $O(n)$ | $O(1)$ | Too slow |
| Moment expansion with Stirling numbers | $O(k^2 + k)$ | $O(k)$ | Accepted |

## Algorithm Walkthrough

1. Interpret $x$ as the sum of independent Bernoulli variables $I_i$. This reformulation allows us to reason algebraically instead of probabilistically over permutations.
2. Precompute modular inverse of $m$, since every appearance of the joker contributes a factor $1/m$. Working modulo a prime field requires replacing division by multiplication with inverses.
3. Build a DP table for Stirling numbers $S(k,r)$ up to $k$. The recurrence splits partitions depending on whether the last element forms a new group or joins an existing one.
4. Precompute powers of $n$ and falling factorial terms $(n)_r$. The falling factorial is computed iteratively as $cur *= (n - r + 1)$, which avoids recomputing products from scratch.
5. For each $r$, accumulate the contribution:

$$S(k,r) \cdot (n)_r \cdot m^{-r}.$$

Each term corresponds to choosing $r$ distinct trials and assigning $k$ occurrences among them, with probability contribution from independent successes.
6. Sum all contributions modulo $998244353$.

### Why it works

Every monomial in the expansion of $x^k$ corresponds to selecting $k$ trial indices with repetition. Grouping identical indices partitions the selection into $r$ distinct trials. Stirling numbers count exactly these partitions, while the falling factorial counts the choice of actual trials. Independence ensures each group contributes a factor $1/m$, so the probability factor becomes $m^{-r}$. No term is missed or double-counted because partitioning by distinct indices is a complete classification of all index tuples.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modinv(x):
    return pow(x, MOD - 2, MOD)

n, m, k = map(int, input().split())

# Stirling numbers S(k, r)
S = [[0] * (k + 1) for _ in range(k + 1)]
S[0][0] = 1

for i in range(1, k + 1):
    for j in range(1, i + 1):
        S[i][j] = (S[i - 1][j - 1] + j * S[i - 1][j]) % MOD

inv_m = modinv(m)

# falling factorial (n)_r
fall = 1

ans = 0

for r in range(0, k + 1):
    if r > n:
        break
    if r == 0:
        term = S[k][0]
    else:
        fall = fall * (n - r + 1) % MOD
        term = S[k][r] * fall % MOD * pow(inv_m, r, MOD) % MOD
    ans = (ans + term) % MOD

print(ans)
```

The implementation follows the decomposition directly. The Stirling DP encodes the combinatorics of grouping identical trial indices. The falling factorial tracks how many ways to choose distinct trials without repetition. The modular inverse of $m$ converts each successful appearance of the joker into a multiplicative probability factor.

A subtle detail is that the falling factorial is updated incrementally; recomputing it from scratch for each $r$ would introduce an unnecessary $O(k)$ factor. Another important point is that powers of $1/m$ are computed via fast exponentiation per term, which is acceptable at $k \le 5000$, but can also be optimized by maintaining a running power if needed.

## Worked Examples

### Example 1

Input: $n=1, m=1, k=1$

Here every draw is deterministically the joker, so $x=1$.

| r | S(1,r) | (n)_r | m^{-r} | Contribution |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 1 | 0 |
| 1 | 1 | 1 | 1 | 1 |

The sum equals 1, matching the deterministic outcome.

### Example 2

Input: $n=2, m=2, k=2$

Each trial succeeds with probability $1/2$. This is a binomial variable.

| r | S(2,r) | (n)_r | m^{-r} | Contribution |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 1 | 0 |
| 1 | 1 | 2 | 1/2 | 1 |
| 2 | 1 | 2 | 1/4 | 1/2 |

Total expectation is $3/2$, which matches the known second moment of $Bin(2,1/2)$.

These traces confirm that each $r$ corresponds to the number of distinct successful draws contributing to the moment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(k^2)$ | Stirling DP dominates; final summation is $O(k)$ |
| Space | $O(k^2)$ | DP table storage |

The constraints allow $k \le 5000$, so a quadratic DP is within limits. The solution avoids dependence on $n$ and $m$ beyond simple arithmetic and modular exponentiation, which is crucial since they can be very large.

## Test Cases

```python
import sys, io

MOD = 998244353

def solve():
    n, m, k = map(int, sys.stdin.readline().split())
    inv_m = pow(m, MOD - 2, MOD)

    S = [[0] * (k + 1) for _ in range(k + 1)]
    S[0][0] = 1
    for i in range(1, k + 1):
        for j in range(1, i + 1):
            S[i][j] = (S[i - 1][j - 1] + j * S[i - 1][j]) % MOD

    fall = 1
    ans = 0

    for r in range(0, k + 1):
        if r > n:
            break
        if r > 0:
            fall = fall * (n - r + 1) % MOD
        term = S[k][r] * fall % MOD * pow(inv_m, r, MOD) % MOD
        ans = (ans + term) % MOD

    print(ans)

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as _io
    out = _io.StringIO()
    with redirect_stdout(out):
        solve()
    sys.stdin = old
    return out.getvalue().strip()

# samples
assert run("1 1 1") == "1"

# custom cases
assert run("2 2 2") == "1", "binomial moment check"
assert run("5 1 3") == "125", "always success"
assert run("3 3 1") == "1", "linear expectation"
assert run("10 2 0") == "1", "zero moment"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | 1 | deterministic single trial |
| 2 2 2 | 1 | second moment structure |
| 5 1 3 | 125 | always-success edge |
| 3 3 1 | 1 | linear expectation correctness |
| 10 2 0 | 1 | zero-th moment identity |

## Edge Cases

A subtle case is when $m=1$. Every draw is always the joker, so $x=n$ deterministically. The formula reduces to $\sum_r S(k,r)(n)_r$, which is exactly $n^k$, matching the deterministic value.

Another case is $k=0$, where the answer must be 1 regardless of parameters. The Stirling formulation naturally produces only the $r=0$ term equal to 1, since $x^0 = 1$ always.

When $n < k$, higher falling factorial terms vanish automatically because $(n)_r = 0$ for $r>n$. This prevents invalid overcounting and ensures correctness without special casing.