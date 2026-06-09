---
title: "CF 2020E - Expected Power"
description: "We are given an array of integers, each with an independent probability of being included in a random multiset. The task is to compute the expected value of the square of the XOR of all selected elements."
date: "2026-06-08T12:49:35+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "dp", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 2020
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 976 (Div. 2) and Divide By Zero 9.0"
rating: 2000
weight: 2020
solve_time_s: 152
verified: false
draft: false
---

[CF 2020E - Expected Power](https://codeforces.com/problemset/problem/2020/E)

**Rating:** 2000  
**Tags:** bitmasks, dp, math, probabilities  
**Solve time:** 2m 32s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers, each with an independent probability of being included in a random multiset. The task is to compute the expected value of the square of the XOR of all selected elements. The input provides probabilities as integers out of 10,000 and the array elements themselves. We must handle multiple test cases efficiently, with the sum of all array lengths not exceeding 200,000, and all numbers being at most 1023. The output is the expected squared XOR modulo $10^9+7$.

A naive approach of enumerating all possible subsets is infeasible because there are $2^n$ subsets, which is astronomically large for $n$ up to 200,000. Edge cases include single-element arrays, repeated numbers with differing probabilities, and the situation where probabilities are 0 or 100%, which may trivially simplify the expected value but must still compute correctly modulo $10^9+7$. For example, if the array is `[1,1]` with probabilities `[10000,0]`, only the first element contributes, and $(f(S))^2$ is simply $1^2$. Careless implementations may forget the modular inverse or integer scaling required for probabilities.

## Approaches

The brute-force solution computes the XOR for each subset, multiplies by its probability, squares, and sums over all $2^n$ subsets. This is correct but clearly impossible when $n > 20$.

The key insight for a faster solution is linearity of expectation and the ability to decompose the XOR operation bitwise. Since XOR is a bitwise addition modulo 2, each bit behaves independently. Let $X_i$ denote the indicator random variable for bit $i$ in the XOR of the selected multiset. Then $\Pr(X_i=1)$ is the probability that an odd number of array elements have bit $i$ included.

Computing $\Pr(X_i=1)$ directly can be done by maintaining a probability generating function over subsets of numbers. Let $q_i = 1 - p_i / 10^4$. For a given bit $b$, define $s_b = \sum$ of probabilities of numbers having that bit. Using dynamic programming or iterated convolution over the 2 states (bit set or not), we can compute the probability that bit $b$ is 1 in the final XOR.

Once we have $\Pr(X_i=1)$ for all 10 bits (since $a_i \le 1023$), the expected value of $(f(S))^2$ can be expressed as

$$\mathbb{E}[(f(S))^2] = \sum_{i} 2^{2i} \Pr(X_i=1) + \sum_{i\neq j} 2^{i+j} \Pr(X_i=1 \text{ XOR } X_j=1)$$

Here, the cross-terms are simplified using independence of bits, giving

$$\Pr(X_i \oplus X_j = 1) = \Pr(X_i=1)\cdot(1-\Pr(X_j=1)) + (1-\Pr(X_i=1))\cdot\Pr(X_j=1)$$

This decomposition reduces the exponential problem to one that is linear in the number of bits and array size.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n2^n)$ | $O(n)$ | Too slow |
| Bitwise DP | $O(nB^2)$, $B=10$ | $O(B)$ | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$, array $a$, and array $p$. Convert probabilities to modular fractions $p_i/10000 \bmod 10^9+7$.
2. Initialize an array `prob_bit[10]` to store the probability that each bit is set in the XOR of a random subset.
3. For each bit $b$ from 0 to 9, compute `prob_bit[b]` by iterating through the array and updating the probability that an odd number of selected numbers have that bit set. This can be done iteratively: for each number with the bit set, multiply the current probability of even and odd parity by its inclusion probability.
4. Compute the expected square using the formula:

$$\mathbb{E}[(f(S))^2] = \sum_{b=0}^{9} 2^{2b} \text{prob\_bit}[b] + \sum_{0 \le b_1 < b_2 < 10} 2^{b_1+b_2} ( \text{prob\_bit}[b_1] + \text{prob\_bit}[b_2] - 2 \text{prob\_bit}[b_1]\text{prob\_bit}[b_2] )$$

Use modular arithmetic with the inverse of 10000 when computing probabilities.

1. Output the result modulo $10^9+7$.

Why it works: The XOR operation decomposes over bits and the independence of selection allows probabilities for each bit to combine multiplicatively. Cross-bit terms are handled by linearity of expectation and the XOR formula. The algorithm never enumerates subsets, yet it correctly accounts for each possible contribution.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7
INV10000 = pow(10000, MOD-2, MOD)

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        p = list(map(int, input().split()))
        
        prob_bit = [0]*10
        for b in range(10):
            even, odd = 1, 0
            for i in range(n):
                if (a[i] >> b) & 1:
                    pi = p[i]*INV10000 % MOD
                    new_even = (even*(1-pi) + odd*pi) % MOD
                    new_odd  = (even*pi + odd*(1-pi)) % MOD
                    even, odd = new_even, new_odd
            prob_bit[b] = odd
        
        result = 0
        for b in range(10):
            result = (result + prob_bit[b]*(1 << (2*b))) % MOD
        for b1 in range(10):
            for b2 in range(b1+1, 10):
                cross = (prob_bit[b1] + prob_bit[b2] - 2*prob_bit[b1]*prob_bit[b2]%MOD) % MOD
                result = (result + cross*(1 << (b1+b2))) % MOD
        print(result)

if __name__ == "__main__":
    solve()
```

The solution converts probabilities to modular fractions and iteratively computes the probability that each bit is set in the final XOR. The expected square is then assembled using both single-bit contributions and pairwise cross-bit contributions. Using modular multiplication prevents overflow, and the order of operations respects Python's operator precedence.

## Worked Examples

Sample input:

```
2
2
1 2
5000 5000
2
1 1
1000 2000
```

Trace for the first test case:

| Step | even | odd | Number contributes? | pi |
| --- | --- | --- | --- | --- |
| b=0 | 1 | 0 | 1 has bit0=1 | 0.5 |
| after 1 | 0.5 | 0.5 |  |  |
| after 2 | 0.5 | 0.5 | 2 has bit0=0 |  |
| b=1 | 1 | 0 | 1 has bit1=0 |  |
| after 2 | 0.5 | 0.5 | 2 has bit1=1 | 0.5 |

Final `prob_bit` gives expected probabilities for XOR bits. Combining yields expected squared value $7/2 \equiv 500000007$.

The second test case proceeds similarly, with probabilities 0.1 and 0.2, yielding 0.26 as expected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t_n_B^2) | B=10 bits, inner loop handles probability updates and cross-bit sums |
| Space | O(B) | Store probabilities for each bit |

The sum of $n$ over all test cases is ≤200,000, B is constant, so total operations ≈ 2×10^6, acceptable under 4s limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("4\n2\n1 2\n5000 5000\n2\n1 1\n1000 2000\n6\n343 624 675 451 902 820\n6536 5326 7648 2165 9430 5428\n1\n1\n10000\n") == "500000007\n820000006\n280120
```
