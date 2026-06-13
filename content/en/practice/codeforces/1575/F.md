---
title: "CF 1575F - Finding Expected Value"
description: "We start with an array whose values lie in the range [0, k - 1]. As long as not all positions contain the same value, we repeatedly choose a random position and a random value, then overwrite that position."
date: "2026-06-10T10:55:13+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1575
codeforces_index: "F"
codeforces_contest_name: "COMPFEST 13 - Finals Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 2900
weight: 1575
solve_time_s: 76
verified: true
draft: false
---

[CF 1575F - Finding Expected Value](https://codeforces.com/problemset/problem/1575/F)

**Rating:** 2900  
**Tags:** math  
**Solve time:** 1m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with an array whose values lie in the range `[0, k - 1]`. As long as not all positions contain the same value, we repeatedly choose a random position and a random value, then overwrite that position.

For a completely specified array `b`, let `f(b)` be the expected number of operations until every element becomes equal.

The input array is only partially specified. Some positions contain `-1`. Each such position is independently replaced by a uniformly random value from `[0, k - 1]`. After all replacements, we obtain a random complete array. The task is to compute the expected value of `f` over all such completions.

The most striking part of the statement is that `k` can be as large as `10^9`. Any solution that depends on iterating over colors is immediately impossible. At the same time, `n` is only `10^5`, which strongly suggests that the final formula should depend on frequency counts rather than on individual colors.

A second observation is that the stochastic process itself has an enormous state space. Even for moderate `n`, storing all possible arrays is hopeless. We need a way to compute the expected hitting time without building the Markov chain.

The tricky cases are the ones involving colors that do not currently appear.

Consider:

```
n = 3, k = 10
a = [0, 0, 1]
```

There are eight colors with frequency zero. Their contribution cannot simply be ignored, because after filling unknown positions they still participate in the expectation formula.

Another easy mistake is to compute expectations only for the currently present colors.

```
n = 3, k = 3
a = [-1, -1, -1]
```

Every color is symmetric. The expected answer depends on how many positions eventually receive each color, not on which colors happen to appear in the input.

A third pitfall is the terminal state. When all elements are equal, the process stops immediately. Any potential-function argument must assign the same value to every terminal configuration, otherwise the stopping-time formula becomes incorrect.

## Approaches

A brute-force viewpoint is to treat every array as a state of a Markov chain and solve a system of linear equations for expected hitting times.

The state count is `k^n`. Even for `n = 10` and `k = 10`, this is already `10^10` states. The approach is mathematically correct but completely unusable.

The key observation is that the process only depends on color frequencies.

Let `cnt(x)` denote the number of occurrences of color `x`. Instead of studying arrays directly, we search for a potential function

$$F = \sum_x g(cnt(x))$$

whose expected change in one operation is always `-1`.

If such a function exists, then the optional stopping theorem immediately gives

$$\mathbb E[\text{time to finish}] = F(\text{initial}) - F(\text{terminal}).$$

This completely avoids solving the Markov chain.

After deriving the recurrence for `g`, the problem becomes purely combinatorial. We only need the expected value of

$$\sum_x g(cnt(x))$$

after the random replacement of all `-1` positions.

Each unknown position independently chooses one of `k` colors. Hence, for every color, the additional occurrences follow a binomial distribution. Summing these contributions carefully yields an `O(n)` solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Markov Chain | Exponential | Exponential | Too slow |
| Potential Function + Binomial Counting | `O(n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

### Deriving the potential

Let

$$F=\sum_x g(cnt(x)).$$

Suppose a color currently has frequency `i`.

If we choose an occurrence of that color and recolor it to a different color, its frequency decreases from `i` to `i-1`.

If we recolor some other position into that color, its frequency increases from `i` to `i+1`.

Define

$$d_i=g(i)-g(i-1).$$

Computing the expected change of `F` and requiring it to be exactly `-1` for every state gives the condition

$$(k-1)i\,d_i-(n-i)d_{i+1}=n.$$

Equivalently,

$$(k-1)i(g(i)-g(i-1)) + (n-i)(g(i)-g(i+1)) = n.$$

We set

$$g(0)=g(1)=0,$$

and compute all remaining values by recurrence:

$$g(i+1) = g(i) + \frac{(k-1)i(g(i)-g(i-1))-n}{n-i}.$$

All arithmetic is performed modulo `10^9+7`.

### Expected contribution after filling unknown positions

Let `c` be the number of `-1` entries.

For each color, suppose its current known frequency equals `j`.

After filling unknown positions, the number of additional occurrences is

$$X \sim \text{Binomial}(c,\tfrac1k).$$

Hence the final frequency equals `j + X`.

Let `b[j]` denote the number of colors whose known frequency is exactly `j`.

Then the expected number of colors whose final frequency equals `i` is

$$\sum_j b[j] \Pr(X=i-j).$$

The binomial probability contributes

$$\binom{c}{i-j} \left(\frac1k\right)^{i-j} \left(\frac{k-1}{k}\right)^{c-(i-j)}.$$

Instead of dividing by powers of `k` repeatedly, we accumulate the numerator

$$\binom{c}{i-j}(k-1)^{c-(i-j)}$$

and divide by `k^c` once at the end.

### Final answer

The expected value of the potential before the process starts is

$$\mathbb E[F] = \sum_i g(i)\cdot \mathbb E[\#\text{colors with final frequency }i].$$

Every terminal state consists of one color appearing `n` times and all others appearing `0` times, so its potential equals

$$g(n).$$

Thus

$$\mathbb E[f(a)] = \mathbb E[F]-g(n).$$

This is exactly the required answer.

### Why it works

The recurrence for `g` was derived so that every operation decreases the expected value of `F` by exactly one, regardless of the current configuration. Consequently,

$$F_t+t$$

is a martingale. Let `T` be the first time when all elements become equal. Applying the stopping-time identity gives

$$\mathbb E[T] = F(\text{start})-F(\text{finish}).$$

The remainder of the solution computes the expected starting potential after random replacement of the unknown entries. Since expectation is linear, summing the binomial contributions of every color yields the exact value of `\mathbb E[F]`. Combining both parts produces the desired expected stopping time.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007

def modpow(a, e):
    res = 1
    while e:
        if e & 1:
            res = res * a % MOD
        a = a * a % MOD
        e >>= 1
    return res

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    freq = {}
    unknown = 0

    for x in a:
        if x == -1:
            unknown += 1
        else:
            freq[x] = freq.get(x, 0) + 1

    inv = [0] * (n + 1)
    inv[1] = 1
    for i in range(2, n + 1):
        inv[i] = (MOD - MOD // i) * inv[MOD % i] % MOD

    g = [0] * (n + 1)

    for i in range(1, n):
        term = ((k - 1) % MOD) * i % MOD
        term = term * ((g[i] - g[i - 1]) % MOD) % MOD
        term = (term + (n - i) * g[i] - n) % MOD
        g[i + 1] = term * inv[n - i] % MOD

    fac = [1] * (n + 1)
    ifac = [1] * (n + 1)

    for i in range(1, n + 1):
        fac[i] = fac[i - 1] * i % MOD

    ifac[n] = modpow(fac[n], MOD - 2)
    for i in range(n, 0, -1):
        ifac[i - 1] = ifac[i] * i % MOD

    def C(N, R):
        if R < 0 or R > N:
            return 0
        return fac[N] * ifac[R] % MOD * ifac[N - R] % MOD

    b = [0] * (n + 1)

    b[0] = k - len(freq)
    for v in freq.values():
        b[v] += 1

    pw = [1] * (unknown + 1)
    for i in range(1, unknown + 1):
        pw[i] = pw[i - 1] * ((k - 1) % MOD) % MOD

    nonzero = [i for i in range(n + 1) if b[i]]

    ans = 0

    for final_cnt in range(1, n + 1):
        ways = 0

        for base in nonzero:
            add = final_cnt - base
            if add < 0 or add > unknown:
                continue

            ways = (
                ways
                + b[base] % MOD
                * C(unknown, add)
                % MOD
                * pw[unknown - add]
            ) % MOD

        ans = (ans + ways * g[final_cnt]) % MOD

    ans = ans * modpow(modpow(k % MOD, unknown), MOD - 2) % MOD
    ans = (ans - g[n]) % MOD

    print(ans)

solve()
```

The first block computes the potential values `g(i)` from the derived recurrence. Only frequencies up to `n` are needed.

The next block prepares factorials and inverse factorials so that every binomial coefficient can be evaluated in constant time.

Array `b` stores how many colors currently have each known frequency. This compresses all colors into only `n + 1` frequency classes.

For every possible final frequency `i`, we compute the expected number of colors ending with that frequency. The binomial coefficient chooses how many unknown positions join a given color, while `(k - 1)^(...)` accounts for the remaining unknown positions choosing other colors.

The accumulated value still contains a common denominator `k^c`, where `c` is the number of unknown positions. We divide once at the end by multiplying with the modular inverse.

Finally we subtract `g(n)`, the potential of every terminal state.

## Worked Examples

### Sample 1

Input:

```
2 2
0 1
```

There are no unknown positions.

| Variable | Value |
| --- | --- |
| `unknown` | 0 |
| Frequencies | `{0:1, 1: |
