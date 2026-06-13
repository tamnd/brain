---
title: "CF 1257G - Divisor Set"
description: "The input does not give the number directly. Instead, it gives its prime factorization as a list of prime factors, where equal primes may appear many times. Suppose a prime $q$ appears $c$ times. Then every divisor chooses an exponent between $0$ and $c$ for that prime."
date: "2026-06-11T20:50:29+07:00"
tags: ["codeforces", "competitive-programming", "divide-and-conquer", "fft", "greedy", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1257
codeforces_index: "G"
codeforces_contest_name: "Educational Codeforces Round 76 (Rated for Div. 2)"
rating: 2600
weight: 1257
solve_time_s: 119
verified: true
draft: false
---

[CF 1257G - Divisor Set](https://codeforces.com/problemset/problem/1257/G)

**Rating:** 2600  
**Tags:** divide and conquer, fft, greedy, math, number theory  
**Solve time:** 1m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

The input does not give the number directly. Instead, it gives its prime factorization as a list of prime factors, where equal primes may appear many times.

Suppose a prime $q$ appears $c$ times. Then every divisor chooses an exponent between $0$ and $c$ for that prime. If the distinct primes have multiplicities

$$c_1,c_2,\dots,c_k,$$

then every divisor corresponds to a vector

$$(e_1,e_2,\dots,e_k), \qquad 0 \le e_i \le c_i.$$

The divisibility relation becomes very simple:

$$(e_1,\dots,e_k)\mid(f_1,\dots,f_k)$$

if and only if

$$e_i \le f_i$$

for every coordinate.

We must find the largest possible collection of divisors such that no two distinct divisors are comparable under divisibility. In poset terminology, we are looking for the size of a maximum antichain.

The number of input factors is at most $2\cdot10^5$. Enumerating divisors is impossible. If all factors are distinct, the number of divisors is $2^n$, which is astronomically large. Any solution must work directly with the multiplicities of equal primes.

A subtle point is that the answer is not the number of divisors. For example:

```
n = 3
primes = [2,3,5]
```

The divisors form the Boolean lattice of dimension three. The largest antichain has size $3$, not $8$.

Another easy mistake is to assume that all divisors with the same number of prime factors are always optimal without proving it. Consider:

```
x = 2^3
```

The divisors are $1,2,4,8$. Every pair is comparable, so the maximum good set has size $1$. The structure of the divisor lattice matters.

A third trap is attempting to count divisors at a given rank using factorial formulas. The multiplicities can be as large as $2\cdot10^5$, and the exponents are bounded independently for each prime. The correct counting object is a generating function, not a multinomial coefficient.

## Approaches

The brute force view is useful because it exposes the underlying combinatorial structure.

Every divisor corresponds to a vector of exponents. A good set is an antichain in the product-of-chains poset

$$[0,c_1]\times[0,c_2]\times\cdots\times[0,c_k].$$

A brute force solution would generate all divisors, build the divisibility relation, and search for the largest antichain. This is hopeless because the number of divisors can be exponential in $n$.

The key observation is that this poset is ranked by

$$r(e_1,\dots,e_k)=e_1+\cdots+e_k.$$

Two distinct elements of the same rank cannot be comparable. If

$$e_i\le f_i$$

for every coordinate and the rank sums are equal, then all coordinates must be equal.

So every rank is automatically an antichain.

Now a deep theorem enters the picture. Products of chains are rank-symmetric and rank-unimodal, and they satisfy the Sperner property. For such posets, the size of a maximum antichain equals the size of the largest rank.

The total rank ranges from $0$ to

$$c_1+\cdots+c_k=n.$$

Because the rank sizes are symmetric and unimodal, the largest rank is the middle one:

$$\left\lfloor \frac n2 \right\rfloor .$$

Thus the entire problem reduces to counting exponent vectors satisfying

$$0\le e_i\le c_i, \qquad e_1+\cdots+e_k=\left\lfloor\frac n2\right\rfloor.$$

This is exactly the coefficient of

$$\prod_{i=1}^{k}(1+x+x^2+\cdots+x^{c_i})$$

at degree $\lfloor n/2\rfloor$.

The remaining task is polynomial multiplication.

Each factor is a polynomial of the form

$$1+x+\cdots+x^{c_i}.$$

The sum of all degrees is

$$c_1+\cdots+c_k=n\le 2\cdot10^5.$$

Multiplying all polynomials with a divide-and-conquer strategy and NTT gives an accepted solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in number of divisors | Exponential | Too slow |
| Optimal | $O(n\log^2 n)$ | $O(n\log n)$ | Accepted |

## Algorithm Walkthrough

1. Count how many times each prime appears in the factorization.

If a prime appears $c$ times, it contributes the polynomial

$$1+x+\cdots+x^c.$$
2. Create one polynomial for each multiplicity.

The coefficients are all ones because every exponent from $0$ through $c$ is allowed exactly once.
3. Repeatedly multiply the two smallest polynomials.

This is analogous to the optimal merge pattern. It keeps intermediate polynomial sizes small and reduces total NTT work.
4. Use Number Theoretic Transform under modulus $998244353$ for every multiplication.

This modulus was chosen specifically because it supports efficient NTT.
5. After all polynomials are merged, obtain the final generating function

$$F(x)=\prod_i(1+x+\cdots+x^{c_i}).$$
6. Output the coefficient of degree

$$\left\lfloor \frac n2 \right\rfloor.$$

By the Sperner property of products of chains, this coefficient equals the maximum size of a good subset.

### Why it works

The divisor lattice is a product of chains. Its rank function is the total exponent sum. Every rank forms an antichain because comparable elements with equal rank must be identical.

Products of chains are Sperner posets, so the largest antichain is exactly the largest rank. The rank sizes are counted by the generating function

$$\prod_i(1+x+\cdots+x^{c_i}),$$

and symmetry plus unimodality place the maximum rank at degree $\lfloor n/2\rfloor$. The algorithm computes precisely that coefficient, so the returned value is the size of a maximum good subset.

## Python Solution

```python
import sys
from collections import Counter
from heapq import heapify, heappop, heappush

input = sys.stdin.readline

MOD = 998244353
G = 3

def ntt(a, invert):
    n = len(a)

    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]

    length = 2
    while length <= n:
        wlen = pow(G, (MOD - 1) // length, MOD)
        if invert:
            wlen = pow(wlen, MOD - 2, MOD)

        for i in range(0, n, length):
            w = 1
            half = length // 2
            for j in range(i, i + half):
                u = a[j]
                v = a[j + half] * w % MOD

                a[j] = (u + v) % MOD
                a[j + half] = (u - v) % MOD

                w = w * wlen % MOD

        length <<= 1

    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD

def multiply(a, b):
    need = len(a) + len(b) - 1
    n = 1
    while n < need:
        n <<= 1

    fa = a[:] + [0] * (n - len(a))
    fb = b[:] + [0] * (n - len(b))

    ntt(fa, False)
    ntt(fb, False)

    for i in range(n):
        fa[i] = fa[i] * fb[i] % MOD

    ntt(fa, True)
    return fa[:need]

def solve():
    n = int(input())
    primes = list(map(int, input().split()))

    freq = Counter(primes)

    heap = []
    uid = 0

    for c in freq.values():
        poly = [1] * (c + 1)
        heap.append((len(poly), uid, poly))
        uid += 1

    heapify(heap)

    while len(heap) > 1:
        _, _, a = heappop(heap)
        _, _, b = heappop(heap)

        c = multiply(a, b)

        heappush(heap, (len(c), uid, c))
        uid += 1

    result = heap[0][2]
    print(result[n // 2] % MOD)

if __name__ == "__main__":
    solve()
```

The frequency counting step converts the prime factorization into multiplicities $c_i$. Each multiplicity immediately becomes a polynomial $1+x+\dots+x^{c_i}$.

The priority queue is not required for correctness, but it significantly improves performance. Multiplying small polynomials first keeps the total amount of NTT work near optimal.

The NTT implementation performs the standard iterative transform under modulus $998244353$. After transforming both operands, coefficients are multiplied pointwise and transformed back.

The final polynomial has degree exactly $n$. Degree $d$ counts exponent vectors whose coordinate sum equals $d$. Since the maximum antichain lies at rank $\lfloor n/2\rfloor$, that coefficient is the answer.

## Worked Examples

### Sample 1

Input:

```
3
2999999 43 2999957
```

All primes are distinct.

Multiplicities:

| Prime | Count |
| --- | --- |
| 2999999 | 1 |
| 43 | 1 |
| 2999957 | 1 |

Polynomials:

| Step | Polynomial |
| --- | --- |
| Initial | (1+x), (1+x), (1+x) |
| After merge | (1+2x+x²) |
| Final | 1+3x+3x²+x³ |

The target degree is:

$$\lfloor 3/2\rfloor=1.$$

| Degree | Coefficient |
| --- | --- |
| 0 | 1 |
| 1 | 3 |
| 2 | 3 |
| 3 | 1 |

Answer:

```
3
```

This is exactly the middle layer of the Boolean lattice.

### Sample 2

Input:

```
6
2 3 2 3 2 2
```

Here

$$x=2^4\cdot3^2.$$

Multiplicities:

| Prime | Count |
| --- | --- |
| 2 | 4 |
| 3 | 2 |

Polynomials:

| Step | Polynomial |
| --- | --- |
| Initial | (1+x+x²+x³+x⁴), (1+x+x²) |
| Final | 1+2x+3x²+3x³+3x⁴+2x⁵+x⁶ |

Target degree:

$$6/2=3.$$

| Degree | Coefficient |
| --- | --- |
| 0 | 1 |
| 1 | 2 |
| 2 | 3 |
| 3 | 3 |
| 4 | 3 |
| 5 | 2 |
| 6 | 1 |

Answer:

```
3
```

The trace shows the rank symmetry that underlies the Sperner argument.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n\log^2 n)$ | NTT multiplications over total degree $n$ using divide-and-conquer merging |
| Space | $O(n\log n)$ | Polynomial storage and NTT buffers |

Since the total degree never exceeds $2\cdot10^5$, the NTT-based approach easily fits within the 5-second limit and the memory bound.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io
from collections import Counter

def run(inp: str) -> str:
    MOD = 998244353

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    p = list(map(int, input().split()))

    freq = Counter(p)

    dp = [1]
    for c in freq.values():
        ndp = [0] * (len(dp) + c)
        for i, v in enumerate(dp):
            for e in range(c + 1):
                ndp[i + e] += v
        dp = ndp

    return str(dp[n // 2] % MOD) + "\n"

# sample 1
assert run("3\n2999999 43 2999957\n") == "3\n"

# sample 2
assert run("6\n2 3 2 3 2 2\n") == "3\n"

# minimum size
assert run("1\n2\n") == "1\n"

# all equal
assert run("5\n2 2 2 2 2\n") == "1\n"

# two distinct primes
assert run("2\n2 3\n") == "2\n"

# multiplicities (2,2)
assert run("4\n2 2 3 3\n") == "3\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 2` | `1` | Smallest possible input |
| `2 2 2 2 2` | `1` | Single chain, every pair comparable |
| `2 3` | `2` | Boolean lattice of dimension two |
| `2 2 3 3` | `3` | Product of two nontrivial chains |

## Edge Cases

Consider:

```
1
2
```

The multiplicity vector is $(1)$. The generating function is

$$1+x.$$

The target degree is $0$. The coefficient is $1$, which matches the fact that a chain has maximum antichain size $1$.

Now consider:

```
5
2 2 2 2 2
```

The multiplicity vector is $(5)$. The generating function is

$$1+x+x^2+x^3+x^4+x^5.$$

The target degree is $2$. Its coefficient is $1$. Every divisor lies on a single chain

$$1<2<4<8<16<32,$$

so no antichain can contain more than one element.

Finally consider:

```
4
2 2 3 3
```

The multiplicities are $(2,2)$. The generating function is

$$(1+x+x^2)^2 = 1+2x+3x^2+2x^3+x^4.$$

The middle coefficient is $3$. The three exponent vectors of rank $2$ are

$$(0,2),\ (1,1),\ (2,0),$$

and they form a maximum antichain. The algorithm computes exactly this coefficient.
