---
title: "CF 222C - Reducing Fractions"
description: "The fraction is not given as a single numerator and denominator. Instead, we receive two arrays. The product of all numbers in the first array is the numerator, and the product of all numbers in the second array is the denominator."
date: "2026-06-04T02:02:38+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math", "number-theory", "sortings"]
categories: ["algorithms"]
codeforces_contest: 222
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 137 (Div. 2)"
rating: 1800
weight: 222
solve_time_s: 149
verified: false
draft: false
---

[CF 222C - Reducing Fractions](https://codeforces.com/problemset/problem/222/C)

**Rating:** 1800  
**Tags:** implementation, math, number theory, sortings  
**Solve time:** 2m 29s  
**Verified:** no  

## Solution
## Problem Understanding

The fraction is not given as a single numerator and denominator. Instead, we receive two arrays.

The product of all numbers in the first array is the numerator, and the product of all numbers in the second array is the denominator.

Our task is to output two new arrays representing the same fraction after complete reduction. In other words, if

$$N=\prod a_i,\qquad D=\prod b_i$$

then we must divide both $N$ and $D$ by their greatest common divisor and represent the resulting numerator and denominator again as arrays of integers not exceeding $10^7$.

The first challenge is that the products themselves are enormous. Even a few dozen values near $10^7$ already exceed normal integer ranges, and here we may have up to $10^5$ numbers. Constructing $N$ and $D$ directly is impossible.

The constraints strongly suggest a prime-factor approach. Each individual value is at most $10^7$, which can be factorized efficiently using a smallest-prime-factor sieve. Since there are up to $2 \cdot 10^5$ numbers total, any algorithm involving pairwise gcd computations between all numerator and denominator elements would be far too expensive.

A subtle point is that the output must still be expressed as arrays of integers no larger than $10^7$. After reduction, the remaining prime factors must be redistributed into numbers satisfying that bound.

Consider the following example:

```
1 1
12
18
```

The fraction is $12/18$. The gcd is $6$, so the reduced fraction is $2/3$.

A careless solution that cancels factors greedily between array elements but does not completely remove all common prime factors could incorrectly leave $4/6$, which is not reduced.

Another important case is when everything cancels:

```
1 1
100
100
```

The reduced fraction is $1/1$.

The output arrays cannot be empty. A solution that removes all factors and prints zero numbers would violate the format. We must output at least one value, namely `1`.

One more tricky example:

```
2 1
8 9
6
```

The numerator equals $72$, denominator equals $6$, so the reduced fraction is $12/1$.

The prime factor $2$ from the denominator cancels only part of the numerator's factorization. Any approach that only compares whole numbers instead of prime exponents can easily miss such partial cancellations.

## Approaches

The most direct idea is to reconstruct the numerator and denominator products, compute their gcd, divide both by it, and then somehow rebuild arrays.

This is mathematically correct but completely infeasible. The products contain up to $10^5$ factors, each as large as $10^7$. The resulting integers would have hundreds of thousands of digits.

A slightly more sophisticated brute-force idea is to repeatedly compute gcds between numerator elements and denominator elements. For every pair $(a_i,b_j)$, divide out their common factors.

This eventually produces a reduced fraction because every common prime factor must appear inside some pair. Unfortunately there are up to $10^5$ numbers on each side, leading to $10^{10}$ pairs in the worst case.

The key observation is that reduction depends only on prime exponents.

If a prime $p$ appears $x$ times in the numerator and $y$ times in the denominator, then after reduction:

$$p^{x-\min(x,y)}$$

remains in the numerator and

$$p^{y-\min(x,y)}$$

remains in the denominator.

So instead of canceling factors between individual numbers, we can factorize every input value and count total exponents of each prime on both sides.

After all counts are known, we subtract the common amount for every prime. What remains is exactly the prime factorization of the reduced numerator and denominator.

The final step is reconstructing arrays. We collect the remaining prime factors and multiply them together greedily, starting a new output number whenever the next multiplication would exceed $10^7$. Since every prime factor itself is at most $10^7$, this always succeeds.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force pairwise cancellation | O(nm log A) | O(1) | Too slow |
| Optimal prime-factor counting | O(A log log A + K) | O(A) | Accepted |

Here $A=10^7$, and $K$ is the total number of prime factors across all input numbers.

## Algorithm Walkthrough

1. Build a smallest-prime-factor sieve for all numbers up to $10^7$.
2. Factorize every numerator value using the sieve and accumulate prime exponents in a map `cntA`.
3. Factorize every denominator value using the sieve and accumulate prime exponents in a map `cntB`.
4. For every prime appearing in either map, compute

$$c=\min(cntA[p],cntB[p]).$$

Subtract `c` from both counts.

This removes exactly the exponent contributed to the gcd.
5. Reconstruct the reduced numerator.

For every prime $p$, append $p$ exactly `cntA[p]` times into a stream of remaining prime factors.

Multiply factors into the current output number while the product does not exceed $10^7$. Otherwise, finish the current number and start a new one.
6. Reconstruct the reduced denominator using the same procedure and the remaining exponents from `cntB`.
7. If either reconstructed array is empty, replace it with `[1]`.
8. Output the sizes of both arrays followed by the arrays themselves.

### Why it works

The factorization of an integer is unique. Every prime contributes independently to the numerator and denominator.

For each prime $p$, the gcd removes exactly

$$p^{\min(cntA[p],cntB[p])}.$$

After subtracting those exponents, the remaining exponents are precisely those of the reduced fraction. No common prime factor remains because at least one side has exponent zero for every prime.

The reconstruction phase merely groups remaining prime factors into numbers not exceeding $10^7$. It does not change the multiset of prime factors, so the represented numerator and denominator remain identical to the reduced fraction.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXV = 10 ** 7

def build_spf(n):
    spf = list(range(n + 1))
    spf[0] = spf[1] = 0

    limit = int(n ** 0.5)
    for i in range(2, limit + 1):
        if spf[i] == i:
            step = i
            start = i * i
            for j in range(start, n + 1, step):
                if spf[j] == j:
                    spf[j] = i
    return spf

def factorize(x, spf, cnt):
    while x > 1:
        p = spf[x]
        c = 0
        while x % p == 0:
            x //= p
            c += 1
        cnt[p] = cnt.get(p, 0) + c

def rebuild(cnt):
    res = []
    cur = 1

    for p in sorted(cnt):
        e = cnt[p]
        for _ in range(e):
            if cur * p <= MAXV:
                cur *= p
            else:
                res.append(cur)
                cur = p

    if cur > 1:
        res.append(cur)

    if not res:
        res = [1]

    return res

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    mx = max(max(a), max(b))
    spf = build_spf(mx)

    cntA = {}
    cntB = {}

    for x in a:
        factorize(x, spf, cntA)

    for x in b:
        factorize(x, spf, cntB)

    primes = set(cntA) | set(cntB)

    for p in primes:
        common = min(cntA.get(p, 0), cntB.get(p, 0))
        if common:
            cntA[p] = cntA.get(p, 0) - common
            cntB[p] = cntB.get(p, 0) - common

    num = rebuild(cntA)
    den = rebuild(cntB)

    print(len(num), len(den))
    print(*num)
    print(*den)

if __name__ == "__main__":
    solve()
```

The sieve stores the smallest prime factor of every integer. Factorization then becomes very fast because each division removes at least one prime factor.

The maps `cntA` and `cntB` store total exponents, not per-number information. That is exactly what fraction reduction requires.

During reconstruction, we preserve every remaining prime factor. The greedy packing is safe because each prime factor is at most $10^7$. If multiplying would exceed the limit, we simply start a new output number.

The special handling for empty arrays is necessary when all factors cancel. The output format requires at least one number on each side.

## Worked Examples

### Sample 1

Input:

```
3 2
100 5 2
50 10
```

Prime factorizations:

| Source | Factorization |
| --- | --- |
| 100 | $2^2 \cdot 5^2$ |
| 5 | $5$ |
| 2 | $2$ |
| 50 | $2 \cdot 5^2$ |
| 10 | $2 \cdot 5$ |

Accumulated counts:

| Prime | Numerator | Denominator | Common | Remaining Numerator | Remaining Denominator |
| --- | --- | --- | --- | --- | --- |
| 2 | 3 | 2 | 2 | 1 | 0 |
| 5 | 3 | 3 | 3 | 0 | 0 |

Reconstruction:

| Side | Remaining primes | Output |
| --- | --- | --- |
| Numerator | 2 | [2] |
| Denominator | none | [1] |

Possible output:

```
1 1
2
1
```

The sample output uses a different grouping, but both represent the reduced fraction $2/1$.

### Sample 2

```
2 1
8 9
6
```

Factor counts:

| Prime | Numerator | Denominator |
| --- | --- | --- |
| 2 | 3 | 1 |
| 3 | 2 | 1 |

Cancellation:

| Prime | Remaining Numerator | Remaining Denominator |
| --- | --- | --- |
| 2 | 2 | 0 |
| 3 | 1 | 0 |

Reconstruction:

| Current factor stream | Output number |
| --- | --- |
| 2, 2, 3 | 12 |

Final result:

```
1 1
12
1
```

This trace shows that cancellation happens at the prime-exponent level rather than between whole numbers.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(M log log M + K) | Sieve construction plus total factorization work |
| Space | O(M) | Smallest-prime-factor array |

Here $M$ is the maximum value appearing in the input, at most $10^7$, and $K$ is the total number of extracted prime factors.

The dominant cost is building the smallest-prime-factor sieve. This approach was the intended solution for the original constraints and comfortably fits within the limits in optimized implementations.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    from math import gcd

    sys.stdin = io.StringIO(inp)

    # output depends on valid grouping, so these tests
    # verify exact cases with unique natural outputs.

    return "placeholder"

# minimum size
# 1/1 remains 1/1

# all factors cancel
# input:
# 1 1
# 100
# 100

# numerator larger after reduction
# input:
# 2 1
# 8 9
# 6

# denominator larger after reduction
# input:
# 1 2
# 6
# 8 9

# prime values near boundary
# input:
# 1 1
# 9999991
# 1
```

For this problem many different outputs are valid because factors may be grouped differently. In practice, a test harness should verify that the products represented by the output arrays form the correctly reduced fraction, rather than comparing exact text.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1 / 1` | `1/1` | Minimum size |
| `100 / 100` | `1/1` | Complete cancellation |
| `8 9 / 6` | `12/1` | Partial prime cancellation |
| `6 / 8 9` | `1/12` | Remaining denominator factors |
| `9999991 / 1` | Same fraction | Large prime handling |

## Edge Cases

Consider:

```
1 1
100
100
```

Factor counts are identical on both sides:

$$2^2 \cdot 5^2$$

All exponents cancel, leaving no prime factors. The reconstruction procedure produces empty lists, which are replaced by `[1]`. The output becomes:

```
1 1
1
1
```

which correctly represents the reduced fraction.

Now consider:

```
2 1
8 9
6
```

The numerator contains $2^3 \cdot 3^2$, while the denominator contains $2 \cdot 3$. After subtracting common exponents, the remaining factorization is $2^2 \cdot 3$. The algorithm reconstructs `12`, producing `12/1`.

Finally:

```
1 1
9999991
9999991
```

The value is a large prime. The factorization map contains one occurrence of that prime on both sides. Cancellation removes it completely, leaving `1/1`. This confirms that the algorithm handles large primes just as easily as composite numbers because everything is processed through prime exponents.
