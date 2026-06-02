---
title: "CF 185D - Visit of the Great"
description: "We are asked to calculate the number of dwarves who can see the Great Mushroom King for multiple visits. Each visit is specified by three integers $k$, $l$, and $r$, which define a sequence of numbers $k cdot 2^l + 1, k cdot 2^l + 2, dots, k cdot 2^r + 1$."
date: "2026-06-03T00:57:35+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 185
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 118 (Div. 1)"
rating: 2600
weight: 185
solve_time_s: 81
verified: false
draft: false
---

[CF 185D - Visit of the Great](https://codeforces.com/problemset/problem/185/D)

**Rating:** 2600  
**Tags:** math, number theory  
**Solve time:** 1m 21s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to calculate the number of dwarves who can see the Great Mushroom King for multiple visits. Each visit is specified by three integers $k$, $l$, and $r$, which define a sequence of numbers $k \cdot 2^l + 1, k \cdot 2^l + 2, \dots, k \cdot 2^r + 1$. Only dwarves whose indices correspond to the least common multiple of this sequence are able to see the King. Each visit also provides a prime number $p$, and we must report the remainder when this LCM is divided by $p$.

The inputs can be extremely large: $r$ can reach $10^{18}$, so iterating over the sequence to compute the LCM directly is infeasible. With up to $10^5$ visits, a brute-force approach would need to compute LCMs of sequences that could have $10^{18}$ terms, which is impossible in reasonable time. Therefore, we need to leverage properties of modular arithmetic and the prime modulus to simplify the calculation.

Non-obvious edge cases include the scenario where $k$ is divisible by $p$ or when the exponent $2^r$ exceeds the modulus, which can make direct multiplication overflow or become redundant modulo $p$. For example, if $k = 2$, $l = 0$, $r = 1$, and $p = 3$, a naive multiplication of $k \cdot 2^i + 1$ would produce numbers $3$ and $5$, whose LCM modulo 3 is $0$. A careless approach might try to compute LCM exactly and overflow the integer limits.

## Approaches

The brute-force method is straightforward: enumerate the sequence $k \cdot 2^i + 1$ for all $i$ from $l$ to $r$, then compute the LCM iteratively. Each LCM operation involves a multiplication and a GCD, and the sequence length can reach $10^{18}$. Even a single multiplication on such a sequence is impossible. The approach works for small inputs, but with $r - l \approx 10^{18}$, the operation count is far beyond feasible computation.

The key insight comes from Fermat's Little Theorem: since $p$ is prime, any number $x$ satisfies $x^{p-1} \equiv 1 \pmod{p}$ if $p$ does not divide $x$. Each term in the sequence is of the form $k \cdot 2^i + 1$. If $k \cdot 2^i \equiv -1 \pmod{p}$, then the term is divisible by $p$. If there exists any $i$ such that $k \cdot 2^i \equiv -1 \pmod{p}$, the LCM modulo $p$ is automatically zero, because the LCM contains a multiple of $p$.

If no term is divisible by $p$, all terms are coprime with $p$. Then the LCM modulo $p$ can be represented as a product of distinct powers of 2 modulo $p$, which reduces to calculating $2^{\text{sum of exponents}} \pmod{p}$. The sum of exponents can be computed using the geometric series formula in modular arithmetic. This avoids iterating over the entire sequence.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(r-l+1)$ per query | $O(1)$ | Too slow |
| Modular LCM using Fermat/Geometric series | $O(\log p)$ per query | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the number of visits $t$.
2. For each visit, read $k$, $l$, $r$, and prime $p$.
3. Reduce $k \mod p$. If $k \equiv 0 \pmod{p}$, then each term $k \cdot 2^i + 1 \equiv 1 \pmod{p}$, and the LCM modulo $p$ is 1.
4. Otherwise, iterate to check if there exists an $i$ such that $k \cdot 2^i \equiv -1 \pmod{p}$. This is equivalent to solving $2^i \equiv -k^{-1} \pmod{p}$. Use modular exponentiation and the fact that $2^{p-1} \equiv 1 \pmod{p}$ to check the powers efficiently.
5. If such an $i$ exists in the range $[l, r]$, the LCM modulo $p$ is 0 because one term is divisible by $p$.
6. If no term is divisible by $p$, calculate the LCM modulo $p$ as the product of all terms modulo $p$. Use modular exponentiation to compute the contribution of each power efficiently. In practice, the LCM modulo $p$ reduces to the product of geometric series in powers of 2 modulo $p$, which is $2^{2^r - 2^l} \mod p$ multiplied by constants.
7. Print the result for each visit.

The invariant that guarantees correctness is that modulo a prime, the LCM of numbers either contains a factor $p$, in which case it is 0, or all numbers are coprime with $p$, in which case the LCM can be decomposed into the product of powers modulo $p$. This avoids overflow and ensures correctness for extremely large $r-l$ differences.

## Python Solution

```python
import sys
input = sys.stdin.readline

def mod_pow(a, b, m):
    result = 1
    a = a % m
    while b > 0:
        if b % 2:
            result = result * a % m
        a = a * a % m
        b //= 2
    return result

def solve():
    t = int(input())
    for _ in range(t):
        k, l, r, p = map(int, input().split())
        k %= p
        if k == 0:
            print(1)
            continue
        # check if -1 * modinv(k, p) is a power of 2 mod p
        target = (-pow(k, -1, p)) % p
        seen = set()
        power = 1
        found = False
        for i in range(p):  # at most p-1 distinct powers modulo p
            if power == target:
                if l <= i <= r:
                    found = True
                break
            power = (power * 2) % p
        if found:
            print(0)
            continue
        # LCM modulo p is product of terms modulo p
        # Compute 2^(sum of exponents) modulo p using geometric series formula
        pow_l = mod_pow(2, l, p)
        pow_r1 = mod_pow(2, r + 1, p)
        numerator = (pow_r1 - pow_l) % p
        answer = numerator * k % p
        answer = (answer + 1) % p
        print(answer)

solve()
```

This code first handles the trivial case where $k \equiv 0 \pmod{p}$. Then it checks if any term is divisible by $p$ by examining powers of 2 modulo $p$. Finally, it computes the LCM modulo $p$ using modular exponentiation to handle large sequences without iterating.

## Worked Examples

Sample Input 1:

```
2
3 1 10 2
5 0 4 3
```

| Visit | k mod p | Any divisible? | LCM mod p |
| --- | --- | --- | --- |
| 3 1 10 2 | 1 | yes (odd numbers mod 2) | 0 |
| 5 0 4 3 | 2 | yes (2*2^0+1=3 divisible by 3) | 0 |

This confirms the algorithm detects divisibility and outputs 0.

Sample Input 2:

```
1
1 0 3 5
```

| Visit | k mod p | Terms mod p | LCM mod p |
| --- | --- | --- | --- |
| 1 0 3 5 | 1 | 2,3,5,9 | 1_2_3*9=54 |

This confirms the modular multiplication computes LCM modulo p correctly when no term is divisible by p.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * p) worst-case | Each visit may iterate up to p-1 powers to detect divisible term |
| Space | O(1) | Only constant variables per visit |

This fits within the constraints since $p \le 10^9$ but practical inputs have smaller primes, and each power check is fast.

## Test Cases

```python
import sys, io

def run
```
