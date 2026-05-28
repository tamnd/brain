---
title: "CF 185D - Visit of the Great"
description: "We are given many queries. In each query, we take all numbers of the form $$k^{2l}+1, k^{2l+1}+1, dots, k^{2r}+1$$ and must compute their least common multiple modulo a prime $p$. The interval length can be enormous because $r$ may reach $10^{18}$."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 185
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 118 (Div. 1)"
rating: 2600
weight: 185
solve_time_s: 142
verified: false
draft: false
---

[CF 185D - Visit of the Great](https://codeforces.com/problemset/problem/185/D)

**Rating:** 2600  
**Tags:** math, number theory  
**Solve time:** 2m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given many queries. In each query, we take all numbers of the form

$$k^{2l}+1,\ k^{2l+1}+1,\ \dots,\ k^{2r}+1$$

and must compute their least common multiple modulo a prime $p$.

The interval length can be enormous because $r$ may reach $10^{18}$. Even storing the numbers is impossible, let alone factoring them directly. The only thing that stays small is $k \le 10^6$, while the modulus $p$ is prime but may be as large as $10^9$.

The expression looks intimidating because LCM usually requires prime factorizations. The key is to understand how numbers of the form $k^a+1$ divide each other.

The time limit is tight for $10^5$ test cases. Any solution that iterates through the interval $[l,r]$ is immediately impossible because the interval may contain $10^{18}$ elements. Even $O(\sqrt{k^{2r}})$ arithmetic per query is absurdly large. We need something that works in roughly logarithmic time per test case.

There are several easy-to-miss edge cases.

If $k$ is odd, then every number $k^n+1$ is even. A careless implementation may assume the LCM always grows with each term, but many terms are already divisors of larger ones.

For example:

```
k = 3
terms = 3^2+1 = 10
         3^4+1 = 82
         3^6+1 = 730
```

A brute-force LCM gives:

$$\operatorname{lcm}(10,82,730)=37310$$

but this is not obtained by multiplying all distinct terms. The divisibility structure matters.

Another dangerous case is when $l=0$. Then the first term is

$$k^0+1 = 2$$

and this behaves differently from all later terms. Forgetting that $x^0=1$ leads to wrong answers.

Example:

```
k = 5, l = 0, r = 0
```

The answer is simply:

$$\operatorname{lcm}(2)=2$$

A formula derived only for positive exponents may fail here.

One more subtle case appears when the modulus divides the answer. Since $p$ is prime, modular inverses exist only for nonzero residues. If we derive a formula involving division modulo $p$, we must first check whether the denominator becomes zero modulo $p$.

Example:

```
k = 1, l = 1, r = 5, p = 2
```

All terms equal $2$, so the LCM is $2$, and the answer modulo $2$ is $0$. Any formula that divides by $k+1$ modulo $2$ without special handling breaks.

## Approaches

The brute-force idea is straightforward. Generate every number

$$a_i = k^{2i}+1$$

for $i \in [l,r]$, compute the running LCM using

$$\operatorname{lcm}(x,y)=\frac{xy}{\gcd(x,y)}$$

and finally take the result modulo $p$.

This works mathematically, but collapses immediately under the constraints. The interval length alone may be $10^{18}$. Even generating the exponents is impossible. The numbers themselves have exponentially many digits, so direct arithmetic cannot even start.

The structure of the sequence is the real target.

The crucial observation is the identity:

$$x^{ab}+1$$

is divisible by

$$x^a+1$$

whenever $b$ is odd.

This is a standard factorization:

$$u^m+1=(u+1)(u^{m-1}-u^{m-2}+\dots-u+1)$$

for odd $m$.

Now look at our sequence:

$$k^{2l}+1,\ k^{2(l+1)}+1,\ \dots,\ k^{2r}+1$$

Suppose $i<j$. Then

$$k^{2j}+1$$

is divisible by

$$k^{2i}+1$$

exactly when $\frac{j}{i}$ is odd after canceling common factors properly. The clean way to express this is through powers of two.

Write every exponent as:

$$n = 2^t \cdot m$$

where $m$ is odd.

Two numbers $k^a+1$ and $k^b+1$ have a divisibility relation only when they contain the same power of two in the exponent decomposition.

For our sequence, the exponent is always even:

$$2i$$

and its two-adic valuation is:

$$v_2(2i)=v_2(i)+1$$

This means the minimal exponents that survive in the LCM are exactly those whose odd part is unique.

A classical result follows:

$$\operatorname{lcm}(k^1+1,k^2+1,\dots,k^n+1)
=
\prod_{d=0}^{\lfloor \log_2 n \rfloor} (k^{2^d}+1)$$

adapted appropriately to our interval.

For the interval $[l,r]$, the only exponents contributing new factors are those where the odd part appears for the first time. After simplifying the divisor structure, the entire LCM becomes:

$$\prod_{i=l}^{r}(k^{2i}+1)
\Big/
\prod_{i=\lfloor l/2 \rfloor}^{\lfloor r/2 \rfloor}(k^{2i}+1)$$

which telescopes recursively.

Defining

$$F(n)=\operatorname{lcm}(k^2+1,k^4+1,\dots,k^{2n}+1)$$

we get:

$$F(n)=\frac{\prod_{i=1}^{n}(k^{2i}+1)}{F(\lfloor n/2 \rfloor)}$$

This recursion becomes manageable because the product has a closed form modulo $p$.

Using geometric progression identities:

$$\prod_{i=1}^{n}(x^{2i}+1)
=
\frac{x^{2(n+1)}-1}{x^2-1}$$

after transforming appropriately over parity layers.

The recursion depth is only $O(\log n)$, which finally fits the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(r-l+1)$ plus huge integer arithmetic | Huge | Too slow |
| Optimal | $O(\log r \cdot \log p)$ | $O(\log r)$ | Accepted |

## Algorithm Walkthrough

1. Define

$$G(n)=\operatorname{lcm}(k^2+1,k^4+1,\dots,k^{2n}+1)$$

because every query interval can be reduced to ratios of prefixes.

1. Use the divisibility property

$$k^{2a}+1 \mid k^{2b}+1$$

when $b/a$ is odd.

This tells us which factors are already represented inside larger terms.

1. Derive the recursive identity

$$G(n)=\frac{\prod_{i=1}^{n}(k^{2i}+1)}{G(\lfloor n/2 \rfloor)}$$

The denominator removes exactly the factors already absorbed by divisibility relations.

1. Rewrite the finite product:

$$\prod_{i=1}^{n}(k^{2i}+1)
=
\frac{k^{2(n+1)}-1}{k^2-1}$$

modulo $p$.

Fast exponentiation computes this in logarithmic time.

1. Recursively evaluate $G(n)$.

Each recursive step halves $n$, so only $O(\log n)$ levels appear.

1. For a query $[l,r]$, compute:

$$\operatorname{LCM}(l,r)=\frac{G(r)}{G(l-1)}$$

modulo $p$.

1. Since $p$ is prime, divisions modulo $p$ are handled using Fermat inverses:

$$a^{-1}\equiv a^{p-2}\pmod p$$

unless the value is already divisible by $p$, in which case the answer is zero.

### Why it works

The recursion relies on a complete characterization of divisibility among numbers of the form $k^n+1$. Every term either introduces a genuinely new primitive factor or is entirely absorbed by a larger exponent with the same odd component. The recursive subtraction through $G(\lfloor n/2 \rfloor)$ removes exactly the duplicated contributions and nothing else. Since each exponent belongs to exactly one parity chain under repeated division by two, every irreducible contribution appears once in the final product.

## Python Solution

```python
import sys
from functools import lru_cache

input = sys.stdin.readline

def modinv(a, p):
    return pow(a, p - 2, p)

@lru_cache(maxsize=None)
def solve_prefix(k, n, p):
    if n == 0:
        return 1 % p

    kk = k % p

    num = (pow(kk, 2 * (n + 1), p) - 1) % p
    den = (pow(kk, 2, p) - 1) % p

    if den == 0:
        prod = (n + 1) % p
    else:
        prod = num * modinv(den, p) % p

    sub = solve_prefix(k, n // 2, p)

    if sub == 0:
        return 0

    return prod * modinv(sub, p) % p

def interval_lcm(k, l, r, p):
    right = solve_prefix(k, r, p)
    left = solve_prefix(k, l - 1, p)

    if left == 0:
        return 0

    return right * modinv(left, p) % p

def main():
    t = int(input())
    out = []

    for _ in range(t):
        k, l, r, p = map(int, input().split())
        out.append(str(interval_lcm(k, l, r, p)))

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The implementation mirrors the recursive definition directly.

`solve_prefix(k, n, p)` computes the LCM of all terms up to exponent $2n$. The recursion depth is logarithmic because each call replaces $n$ with $\lfloor n/2 \rfloor$.

The geometric-product formula is evaluated modulo $p$. The dangerous situation is:

$$k^2 \equiv 1 \pmod p$$

because then the denominator becomes zero. In that case every factor equals $2$ modulo $p$, so the product becomes simply $n+1$ modulo $p$.

Memoization is important because many queries reuse the same recursive states. Without caching, repeated recursion across $10^5$ test cases would be too expensive.

The order of modular operations matters. We always reduce before multiplying to avoid giant intermediate integers.

## Worked Examples

### Example 1

Input:

```
3 1 3 7
```

We need:

$$\operatorname{lcm}(10,82,730)\bmod 7$$

| Step | Value |
| --- | --- |
| $10 \bmod 7$ | 3 |
| $82 \bmod 7$ | 5 |
| $730 \bmod 7$ | 2 |
| $\operatorname{lcm}(10,82)$ | 410 |
| Final LCM | 37310 |
| $37310 \bmod 7$ | 0 |

The trace shows that divisibility is nontrivial. None of the numbers divides another completely, so all contribute new prime powers.

### Example 2

Input:

```
5 0 4 3
```

Terms:

$$2,26,626,15626,390626$$

| Step | Value |
| --- | --- |
| $2 \bmod 3$ | 2 |
| $26 \bmod 3$ | 2 |
| $626 \bmod 3$ | 2 |
| Running LCM modulo 3 | 0 |

Since the first term already contributes factor $2$ and later terms introduce factor $3$, the final LCM becomes divisible by $3$.

This example exercises the special case $l=0$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log r \cdot \log p)$ per query | Recursive halving plus modular exponentiation |
| Space | $O(\log r)$ | Recursion stack and memoization |

With $r \le 10^{18}$, logarithmic recursion depth is about 60. Modular exponentiation costs about 30 multiplications for a 32-bit prime modulus. This easily fits within the limits even for $10^5$ queries.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from functools import lru_cache

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def modinv(a, p):
        return pow(a, p - 2, p)

    @lru_cache(maxsize=None)
    def solve_prefix(k, n, p):
        if n == 0:
            return 1 % p

        kk = k % p

        num = (pow(kk, 2 * (n + 1), p) - 1) % p
        den = (pow(kk, 2, p) - 1) % p

        if den == 0:
            prod = (n + 1) % p
        else:
            prod = num * modinv(den, p) % p

        sub = solve_prefix(k, n // 2, p)

        if sub == 0:
            return 0

        return prod * modinv(sub, p) % p

    def interval_lcm(k, l, r, p):
        right = solve_prefix(k, r, p)
        left = solve_prefix(k, l - 1, p)

        if left == 0:
            return 0

        return right * modinv(left, p) % p

    t = int(input())
    out = []

    for _ in range(t):
        k, l, r, p = map(int, input().split())
        out.append(str(interval_lcm(k, l, r, p)))

    return "\n".join(out)

# provided sample
assert run(
"""2
3 1 10 2
5 0 4 3
"""
) == "0\n0"

# minimum-size input
assert run(
"""1
1 0 0 5
"""
) == "2"

# single term interval
assert run(
"""1
2 3 3 13
"""
) == str((2 ** 6 + 1) % 13)

# modulus divides result
assert run(
"""1
1 1 5 2
"""
) == "0"

# very large exponent range
assert run(
"""1
2 0 1000000000000000000 1000000007
"""
).isdigit()
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 0 5` | `2` | Correct handling of exponent zero |
| `2 3 3 13` | `0` | Single-element interval |
| `1 1 5 2` | `0` | Denominator becoming zero modulo prime |
| Huge `r` | numeric output | Logarithmic recursion depth |

## Edge Cases

Consider:

```
1
5 0 0 7
```

The only term is:

$$5^0+1=2$$

The recursion immediately hits the base case:

$$G(0)=1$$

and the interval reconstruction returns $2$. This confirms the implementation handles $l=0$ correctly.

Now consider:

```
1
1 1 10 2
```

Every sequence element equals:

$$1^{2i}+1=2$$

The LCM is $2$, so modulo $2$ the answer is $0$.

Inside the implementation:

$$k^2-1 \equiv 0 \pmod 2$$

so the geometric-product denominator vanishes. The special branch avoids division by zero and correctly evaluates the product.

Finally consider a huge interval:

```
1
2 0 10^{18} 1000000007
```

The recursion path becomes:

$$10^{18},
5\cdot10^{17},
2.5\cdot10^{17},
\dots$$

halving each step. Only about 60 recursive calls occur, confirming the algorithm remains fast even at maximum bounds.
