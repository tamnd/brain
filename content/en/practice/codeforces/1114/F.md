---
title: "CF 1114F - Please, another Queries on Array?"
description: "We have an array of integers, each between 1 and 300, and we need to process two types of queries. The first query multiplies a contiguous segment of the array by a given number."
date: "2026-06-12T04:53:50+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "data-structures", "divide-and-conquer", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1114
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 538 (Div. 2)"
rating: 2400
weight: 1114
solve_time_s: 67
verified: true
draft: false
---

[CF 1114F - Please, another Queries on Array?](https://codeforces.com/problemset/problem/1114/F)

**Rating:** 2400  
**Tags:** bitmasks, data structures, divide and conquer, math, number theory  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of integers, each between 1 and 300, and we need to process two types of queries. The first query multiplies a contiguous segment of the array by a given number. The second query asks for the Euler totient of the product of a segment of the array, modulo $10^9 + 7$. The Euler totient function, $\varphi(n)$, counts integers up to $n$ that are coprime with $n$. Because multiplication is distributive over the product, a multiply query changes the prime factorization of each element in the segment, which in turn affects the totient of any segment including those elements.

The constraints are significant: the array can be up to 400,000 elements and there can be 200,000 queries. Naive approaches that recompute the product each time or even recompute prime factorizations for every segment would perform too many operations. Specifically, recomputing a product for each query in $O(n)$ would yield $O(nq)\approx 8 \cdot 10^{10}$ operations, which is far beyond acceptable for a 6-second time limit.

Non-obvious edge cases include segments containing 1. The totient of 1 is 1, so any segment entirely of ones must return 1. Similarly, multiply operations by 1 do not change anything but must still be tracked in our structure. Careless implementations that assume all elements are greater than 1 may compute zero incorrectly if using a formula like $\prod (p_i-1)p_i^{k_i-1}$ for primes $p_i$ dividing the product.

Another subtlety is that the product of segment elements can grow extremely large, quickly exceeding 64-bit integers. This prevents straightforward computation of the product; the solution must work with the multiplicative structure indirectly, ideally via prime exponents.

## Approaches

The brute-force approach would handle a MULTIPLY query by iterating from $l$ to $r$ and multiplying each element, then handle a TOTIENT query by computing the product of the segment and factoring it. This works for small arrays because the array elements are bounded by 300, so their factorization is cheap. However, with 400,000 elements and 200,000 queries, this method could require up to $8 \cdot 10^{10}$ multiplications or factorizations, which is completely infeasible.

The key insight is that both operations are linear in the exponent space of prime factors. Every integer from 1 to 300 has a fixed set of prime factors, and multiplying a segment by a number is equivalent to adding the corresponding prime exponents to each element in that segment. Similarly, computing the totient of a product reduces to combining prime exponents: $\varphi(\prod a_i) = \prod p^{k_i-1}(p-1)$ for all primes $p$ dividing the product. This lets us store, for each segment, either a bitmask of primes or an exponent vector, and update/query it efficiently using a segment tree with lazy propagation.

We precompute prime factorizations for all numbers up to 300. Then we represent each segment in the segment tree by the combined prime information. Multiply queries add exponent vectors, and totient queries combine exponent vectors and compute the totient modulo $10^9 + 7$. Using bitmasks to track which primes divide a segment allows extremely fast combination operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * q * 8) | O(n) | Too slow |
| Segment Tree + Bitmask Exponents | O((n + q) * log n * P) | O(n * P) | Accepted |

Here, $P$ is the number of primes ≤ 300, which is 62.

## Algorithm Walkthrough

1. Precompute all primes up to 300 using a sieve. Each number $1 \le x \le 300$ is associated with a bitmask of primes dividing it. Store $\varphi(x)$ as a separate table for numbers up to 300 if needed.
2. For each element in the array, convert its value into a bitmask representing its prime factors and a vector of exponents for each prime.
3. Build a segment tree over the array, where each node stores two pieces of information: the cumulative exponent vector of primes in that segment and the bitmask representing which primes divide any element in that segment.
4. For MULTIPLY queries, convert the multiplier into its exponent vector and bitmask. Apply a lazy update to the segment tree, adding exponents to the affected range. Use bitwise OR for the bitmask to indicate presence of primes.
5. For TOTIENT queries, query the segment tree to get the cumulative exponent vector and bitmask for the range. Compute the totient using $\varphi(\prod a_i) = \prod_{p} p^{k_p - 1} (p-1)$ modulo $10^9 + 7$, where $k_p$ is the total exponent of prime $p$ in the segment.
6. Output the results in order.

**Why it works:** The segment tree with exponent vectors guarantees that for any query range, we know the exact combined prime factorization of the segment. Lazy propagation ensures that multiple multiplies are correctly accumulated before a totient query, preserving the invariant that each node accurately represents its segment. The bitmask allows rapid combination and avoids recomputation of which primes are present. The correctness relies on the multiplicativity of the totient function and the additive nature of exponents under multiplication.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

# Precompute primes and factorizations
MAX_A = 300
primes = []
is_prime = [True] * (MAX_A+1)
is_prime[0] = is_prime[1] = False
for i in range(2, MAX_A+1):
    if is_prime[i]:
        primes.append(i)
        for j in range(i*i, MAX_A+1, i):
            is_prime[j] = False

prime_index = {p:i for i,p in enumerate(primes)}
P = len(primes)

# Factorization as exponent vector
def factorize(x):
    exps = [0]*P
    for i,p in enumerate(primes):
        while x % p == 0:
            x //= p
            exps[i] += 1
    return exps

class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.tree = [[0]*P for _ in range(2*self.size)]
        self.lazy = [[0]*P for _ in range(2*self.size)]
        for i in range(self.n):
            self.tree[self.size + i] = data[i]
        for i in range(self.size-1, 0, -1):
            for j in range(P):
                self.tree[i][j] = self.tree[2*i][j] + self.tree[2*i+1][j]

    def push(self, v, l, r):
        for j in range(P):
            if self.lazy[v][j]:
                self.tree[v][j] += self.lazy[v][j]*(r-l+1)
                if v < self.size:
                    self.lazy[2*v][j] += self.lazy[v][j]
                    self.lazy[2*v+1][j] += self.lazy[v][j]
                self.lazy[v][j] = 0

    def update(self, ql, qr, add, v=1, l=0, r=None):
        if r is None:
            r = self.size-1
        self.push(v,l,r)
        if qr < l or r < ql:
            return
        if ql <= l and r <= qr:
            for j in range(P):
                self.lazy[v][j] += add[j]
            self.push(v,l,r)
            return
        m = (l+r)//2
        self.update(ql, qr, add, 2*v, l, m)
        self.update(ql, qr, add, 2*v+1, m+1, r)
        for j in range(P):
            self.tree[v][j] = self.tree[2*v][j] + self.tree[2*v+1][j]

    def query(self, ql, qr, v=1, l=0, r=None):
        if r is None:
            r = self.size-1
        self.push(v,l,r)
        if qr < l or r < ql:
            return [0]*P
        if ql <= l and r <= qr:
            return self.tree[v][:]
        m = (l+r)//2
        left = self.query(ql, qr, 2*v, l, m)
        right = self.query(ql, qr, 2*v+1, m+1, r)
        return [left[j]+right[j] for j in range(P)]

def mod_pow(a,b):
    res=1
    while b>0:
        if b&1:
            res=res*a%MOD
        a=a*a%MOD
        b>>=1
    return res

def totient(exps):
    res = 1
    for i,p in enumerate(primes):
        k = exps[i]
        if k > 0:
            res = res *
```
