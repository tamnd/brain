---
title: "CF 487C - Prefix Product Sequence"
description: "We need to arrange the numbers $1,2,dots,n$ into a permutation $a1,a2,dots,an$. Define $$pi = a1a2cdots ai pmod n.$$ The requirement is that the sequence $p1,p2,dots,pn$ must itself be a permutation of all residues $0,1,dots,n-1$."
date: "2026-06-07T17:32:04+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 487
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 278 (Div. 1)"
rating: 2300
weight: 487
solve_time_s: 162
verified: false
draft: false
---

[CF 487C - Prefix Product Sequence](https://codeforces.com/problemset/problem/487/C)

**Rating:** 2300  
**Tags:** constructive algorithms, math, number theory  
**Solve time:** 2m 42s  
**Verified:** no  

## Solution
## Problem Understanding

We need to arrange the numbers $1,2,\dots,n$ into a permutation $a_1,a_2,\dots,a_n$.

Define

$$p_i = a_1a_2\cdots a_i \pmod n.$$

The requirement is that the sequence $p_1,p_2,\dots,p_n$ must itself be a permutation of all residues $0,1,\dots,n-1$.

Since every number from $1$ to $n$ appears exactly once in the permutation, the last prefix product is

$$p_n = n! \pmod n.$$

For every $n>1$, this value is $0$, because one factor equals $n$. Thus the residue $0$ must appear exactly once, and it necessarily appears at the last position. All earlier prefix products must be the nonzero residues.

The input consists of a single integer $n$, with $n\le 10^5$. This immediately rules out any search over permutations. Even $n=20$ already has $20!$ possibilities. We need a direct constructive formula that can be generated in linear time.

A subtle edge case is $n=1$. The only permutation is $[1]$. The unique prefix product is $1 \bmod 1 = 0$, which is exactly the required permutation $[0]$. The answer exists.

Another important case is a composite number such as $n=8$. A naive attempt might try to generate values using modular inverses, but numbers like $2$ and $4$ are not invertible modulo $8$. The construction completely breaks down. In fact, no solution exists for any composite $n>4$.

The special case $n=4$ is easy to miss. Although $4$ is composite, a solution does exist:

$$1,\ 3,\ 2,\ 4.$$

Its prefix products modulo $4$ are

$$1,\ 3,\ 2,\ 0,$$

which is exactly a permutation of $0,1,2,3$.

## Approaches

The most direct idea is brute force. Generate permutations of $1,\dots,n$, compute all prefix products modulo $n$, and test whether the resulting residues form a permutation of $0,\dots,n-1$.

This is correct because it checks every candidate. Unfortunately, the search space contains $n!$ permutations. Even for $n=12$, this already exceeds $4\times10^8$ possibilities. The constraint $n\le10^5$ makes exhaustive search completely impossible.

The key observation comes from looking at the desired prefix products rather than the permutation itself.

Suppose we want the prefix products to be

$$p_1=1,\ p_2=2,\ p_3=3,\ \dots,\ p_{n-1}=n-1,\ p_n=0.$$

If we can realize exactly these residues, then they are obviously a permutation of all residues modulo $n$.

Since

$$p_i \equiv p_{i-1}a_i \pmod n,$$

we can solve for $a_i$:

$$a_i \equiv p_i p_{i-1}^{-1} \pmod n.$$

This requires modular inverses of every nonzero residue. Such inverses exist precisely when $n$ is prime.

Choosing $p_i=i$ for $1\le i<n$ gives

$$a_i \equiv i(i-1)^{-1}\pmod n.$$

For a prime modulus, every $1,\dots,n-1$ is invertible, so the construction works perfectly.

The remaining question is existence. A classical number theoretic fact shows that for composite $n>4$, no such permutation can exist. The only valid values are:

- $n=1$
- $n=4$
- any prime $n$

This yields a linear construction once primality has been checked.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n!\cdot n)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ after primality test | $O(n)$ | Accepted |

## Algorithm Walkthrough

### For $n=1$

1. Output `YES`.
2. Output `1`.

The unique prefix product modulo $1$ equals $0$, so the condition is satisfied.

### For $n=4$

1. Output `YES`.
2. Output the known construction:

$$1,\ 3,\ 2,\ 4.$$

Its prefix products modulo $4$ are $1,3,2,0$.

### For general $n$

1. Check whether $n$ is prime.
2. If $n$ is composite, output `NO`.
3. Otherwise output `YES`.
4. Set $a_1=1$.
5. For every $i=2,\dots,n-1$, compute

$$a_i = i\cdot (i-1)^{-1}\pmod n.$$

1. Set $a_n=n$.

The inverse is computed using Fermat's theorem:

$$(i-1)^{-1}\equiv (i-1)^{n-2}\pmod n,$$

because $n$ is prime.

### Why it works

Define the desired prefix products by

$$p_i=i \quad (1\le i<n).$$

We prove by induction that the constructed permutation produces exactly these values.

For $i=1$,

$$p_1=a_1=1.$$

Assume $p_{i-1}=i-1$. Then

$$p_i
\equiv p_{i-1}a_i
\equiv (i-1)\cdot i\cdot (i-1)^{-1}
\equiv i
\pmod n.$$

Thus every prefix product before the last one equals its index.

The final element is $a_n=n\equiv0\pmod n$, so

$$p_n\equiv p_{n-1}\cdot0\equiv0.$$

Hence the prefix products are

$$1,2,\dots,n-1,0,$$

which is exactly a permutation of all residues modulo $n$.

It remains to show that the sequence $a_i$ is itself a permutation of $1,\dots,n$. Since

$$a_i=i(i-1)^{-1},$$

every $a_i$ is a nonzero residue modulo a prime. Distinct $i$ produce distinct values because multiplying by inverses is reversible. Together with $a_1=1$ and $a_n=n$, every number appears exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

if n == 1:
    print("YES")
    print(1)
elif n == 4:
    print("YES")
    print(1)
    print(3)
    print(2)
    print(4)
else:
    prime = True
    d = 2
    while d * d <= n:
        if n % d == 0:
            prime = False
            break
        d += 1

    if not prime:
        print("NO")
    else:
        print("YES")
        print(1)

        for i in range(2, n):
            x = (i * pow(i - 1, n - 2, n)) % n
            print(x)

        print(n)
```

The program first handles the two exceptional values, $n=1$ and $n=4$.

For all other inputs it performs a primality test by trial division. Since $n\le10^5$, checking divisors up to $\sqrt n$ is extremely cheap.

When $n$ is prime, Fermat's theorem provides modular inverses. Python's three-argument `pow` computes modular exponentiation efficiently, so

```
PythonRun
```

returns $(i-1)^{-1}\pmod n$.

The order of output matters. The first element must be `1`, the last element must be `n`, and every middle element is generated from the inverse formula. Printing `n` instead of `0` is crucial because the permutation must consist of integers from `1` to `n`, not residues.

## Worked Examples

### Example 1

Input:

```

```

Since $7$ is prime, we use the construction.

| i | inverse of i-1 mod 7 | a_i | prefix product mod 7 |
| --- | --- | --- | --- |
| 1 | - | 1 | 1 |
| 2 | 1 | 2 | 2 |
| 3 | 4 | 5 | 3 |
| 4 | 5 | 6 | 4 |
| 5 | 2 | 3 | 5 |
| 6 | 3 | 4 | 6 |
| 7 | - | 7 | 0 |

Output:

```

```

The prefix products become $1,2,3,4,5,6,0$, exactly the required residues.

### Example 2

Input:

```
4
```

This is the exceptional composite case.

| Position | Value | Prefix product mod 4 |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 3 | 3 |
| 3 | 2 | 2 |
| 4 | 4 | 0 |

Output:

```
YES
1
3
2
4
```

The residues are $1,3,2,0$, which form a permutation of $0,1,2,3$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Primality testing costs $O(\sqrt n)$, construction costs $O(n)$ |
| Space | $O(1)$ | Aside from a few variables, output is streamed directly |

With $n\le10^5$, the algorithm runs comfortably within the limits. The dominant work is generating the $n$ output values.
