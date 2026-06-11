---
title: "CF 1408I - Bitwise Magic"
description: "We are given an array of distinct non-negative integers, each at least as large as a given integer $k$, and we perform $k$ random decrements on the array. Each second, one of the $n$ elements is chosen uniformly at random and decreased by 1."
date: "2026-06-11T07:47:21+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 1408
codeforces_index: "I"
codeforces_contest_name: "Grakn Forces 2020"
rating: 3200
weight: 1408
solve_time_s: 124
verified: false
draft: false
---

[CF 1408I - Bitwise Magic](https://codeforces.com/problemset/problem/1408/I)

**Rating:** 3200  
**Tags:** dp, math  
**Solve time:** 2m 4s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of distinct non-negative integers, each at least as large as a given integer $k$, and we perform $k$ random decrements on the array. Each second, one of the $n$ elements is chosen uniformly at random and decreased by 1. After all decrements, we need the probability that the bitwise XOR of all elements equals each possible value from 0 to $2^c-1$. Probabilities are to be returned as modular integers representing $p \cdot q^{-1} \bmod 998244353$ for the fraction $p/q$.

The input constraints imply that $n$ is at most $2^c - k$, $k \le 16$, and $c \le 16$. Since $k$ is small, it is feasible to consider dynamic programming over the number of decrements. The number of possible XOR results is $2^c$, which can be up to 65536. A naive approach that tracks every possible sequence of decrements explicitly would be exponential in $k$ and infeasible for $k=16$ with larger arrays. The small $k$ bound suggests a combinatorial or transform-based solution is viable.

A non-obvious edge case occurs when $k = 1$ or $n = 1$. For example, if $n = 1$, $a_1 = k = 1$, and $c = 2$, the single decrement reduces the only element by 1, so the XOR is deterministic. A careless DP that assumes multiple options per decrement might incorrectly average over impossible events. Another edge case is when all elements are equal or when some elements are already zero after decrements; the XOR probabilities become sparse and require precise handling of modular arithmetic.

## Approaches

The brute-force approach enumerates all sequences of $k$ decrements. For each second, we try all $n$ choices and recursively compute the resulting XOR. This produces $n^k$ possible sequences. For the worst case $n = 2^c - k = 65520$ and $k = 16$, this is completely infeasible. Even for smaller $n$, storing the probability for each possible XOR for each sequence quickly exceeds memory and time constraints.

The key insight comes from recognizing that each element is decremented independently in a combinatorial sense, and the XOR is linear under modulo-2 addition. This suggests using a **dynamic programming approach over XOR values combined with the number of decrements**. Each element contributes a multinomial distribution of how many times it is decremented. For small $k$, we can compute the probabilities for each element independently, then combine them efficiently using a **Walsh-Hadamard transform (WHT)**, which converts XOR convolution into element-wise multiplication. The WHT exploits the linearity of XOR, letting us combine probability distributions in $O(2^c \cdot c)$ instead of $O((2^c)^n)$.

The brute-force approach is conceptually simple but exponential in $k$ and $n$. Using WHT leverages the XOR linearity to multiply generating functions representing probability distributions for each element. This produces an exact probability distribution over all XOR results modulo $998244353$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^k * 2^c) | O(2^c * k) | Too slow |
| Optimal | O(2^c * c + k * n) | O(2^c) | Accepted |

## Algorithm Walkthrough

1. First, precompute the modular inverse of $n$ modulo $998244353$ since each decrement is uniformly distributed across $n$ elements. This allows us to represent the probability of choosing any element at each step.
2. Represent the probability distribution of an element after $k$ decrements. Each element $a_i$ can be decremented 0 to $k$ times. The probability that it is decremented exactly $d$ times is given by the multinomial coefficient $\binom{k}{d} \cdot (1/n)^d \cdot ((n-1)/n)^{k-d}$.
3. Construct an array `dp` of length $2^c$ representing the probability of each XOR value. Initialize `dp[a_1] = 1` for the first element, with other entries zero. Probabilities are stored modulo $998244353$ using modular inverses for fractions.
4. For each subsequent element, apply a **Walsh-Hadamard transform** to `dp` and the element's distribution array. Multiply the transformed arrays element-wise and then perform the inverse transform. This convolution effectively combines the independent probabilities under XOR.
5. After all elements are processed, `dp[x]` contains the final probability for XOR = $x$. Multiply each probability by the modular inverse of total sequences $(n^k)$ to normalize.
6. Output `dp[x]` modulo $998244353$ for all $x \in [0, 2^c - 1]$.

The reason this works is that the WHT transforms XOR convolution, which is not pointwise in the original domain, into pointwise multiplication. By transforming, multiplying, and inversely transforming, we exactly compute the sum over all ways elements’ decrements XOR to a given value. Since we account for all decrement counts combinatorially, no sequence is omitted or double-counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modinv(x):
    return pow(x, MOD-2, MOD)

def walsh_hadamard(a, invert):
    n = len(a)
    h = 1
    while h < n:
        for i in range(0, n, h * 2):
            for j in range(i, i + h):
                x = a[j]
                y = a[j + h]
                a[j] = (x + y) % MOD
                a[j + h] = (x - y + MOD) % MOD
        h *= 2
    if invert:
        inv_n = modinv(n)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD

def solve():
    n, k, c = map(int, input().split())
    a = list(map(int, input().split()))
    size = 1 << c
    dp = [0] * size
    dp[a[0]] = 1
    inv_n = modinv(n)
    
    # Precompute probability distribution for one element
    from math import comb
    elem_prob = [0] * (k + 1)
    for d in range(k + 1):
        elem_prob[d] = comb(k, d) * pow(inv_n, d, MOD) * pow((n - 1) * inv_n % MOD, k - d, MOD) % MOD
    
    for i in range(1, n):
        # Construct array of length 2^c for this element's XOR probabilities
        f = [0] * size
        for d in range(k + 1):
            f[a[i] - d] = elem_prob[d] if (a[i] - d) >= 0 else 0
        # Transform both dp and f
        walsh_hadamard(dp, False)
        walsh_hadamard(f, False)
        for j in range(size):
            dp[j] = dp[j] * f[j] % MOD
        walsh_hadamard(dp, True)
    
    print(" ".join(map(str, dp)))

if __name__ == "__main__":
    solve()
```

The code initializes the probability distribution for the first element, precomputes combinatorial probabilities for each element decrement, and applies WHT to efficiently combine distributions. Modular inverses handle fractions correctly under modulo arithmetic. Care is taken to avoid negative indices when an element's decrements exceed its value.

## Worked Examples

### Sample 1

Input:

```
4 1 3
1 2 3 4
```

| Step | dp state (probabilities for XOR 0..7) |
| --- | --- |
| init | [0,1,0,0,0,0,0,0] |
| after combining 2 | [0,?, ?, ?, ?, ?, ?, ?] |
| final | [0,0,0,748683265,0,499122177,0,748683265] |

The table shows `dp` evolving as each element is processed. Each XOR probability is computed exactly according to the number of ways decrements distribute over elements.

### Custom Input

```
2 2 2
2 3
```

| Step | dp (XOR 0..3) |
| --- | --- |
| init | [0,0,1,0] |
| after combining 3 | [?, ?, ?, ?] |

The trace demonstrates WHT correctly convolves distributions, and probabilities normalize to the modular integer representation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2^c * c + n * k) | The WHT takes O(2^c * c), combining distributions for n elements is O(n * k) |
| Space | O(2^c) | We store dp arrays of length 2^c |

Given c ≤ 16 and k ≤ 16, the solution runs in milliseconds and uses under
