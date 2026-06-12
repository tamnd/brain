---
title: "CF 920G - List Of Integers"
description: "The problem asks us to generate a special list of integers for multiple queries. For a given query with integers x, p, and k, we need to find the k-th integer greater than x that is coprime with p. Coprime means that the greatest common divisor (gcd) of the number and p is 1."
date: "2026-06-13T02:54:45+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "bitmasks", "brute-force", "combinatorics", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 920
codeforces_index: "G"
codeforces_contest_name: "Educational Codeforces Round 37 (Rated for Div. 2)"
rating: 2200
weight: 920
solve_time_s: 274
verified: true
draft: false
---

[CF 920G - List Of Integers](https://codeforces.com/problemset/problem/920/G)

**Rating:** 2200  
**Tags:** binary search, bitmasks, brute force, combinatorics, math, number theory  
**Solve time:** 4m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to generate a special list of integers for multiple queries. For a given query with integers `x`, `p`, and `k`, we need to find the `k`-th integer greater than `x` that is coprime with `p`. Coprime means that the greatest common divisor (gcd) of the number and `p` is 1. For example, if `x = 7` and `p = 22`, the numbers greater than 7 and coprime to 22 are 9, 13, 15, 17, and so on. The query wants the `k`-th number in this sequence.

The constraints give us up to 30,000 queries, and each query has numbers up to 1,000,000. A naive approach that checks each integer above `x` one by one would need to compute gcd for potentially millions of numbers per query, which is far too slow. With `t` as 30,000 and numbers reaching `10^6`, we need a method that scales roughly in the order of logarithms or linear in the number of prime factors of `p`.

A subtle edge case occurs when `p` has many small prime factors. For instance, if `p = 6`, numbers that are multiples of 2 or 3 must be skipped. A naive approach might incorrectly count numbers that are divisible by any prime factor of `p`. Similarly, `x` could be just below a number coprime to `p`, so off-by-one errors in counting or indexing could lead to returning the wrong number. For example, with `x = 5`, `p = 6`, and `k = 1`, the correct answer is 7, not 6.

## Approaches

The brute-force method is straightforward: starting from `x + 1`, check each number sequentially and count how many are coprime to `p`. Once the count reaches `k`, that number is the answer. This works because it directly simulates the definition of the sequence. The problem is the worst case: if `p` is small like 2, about half the numbers are coprime, and we may have to iterate up to `10^6` numbers per query. With `t` as 30,000, this could reach `3 * 10^10` operations, which is clearly infeasible.

The key observation is that coprimality is determined by the prime factors of `p`. If we know the prime factorization of `p`, we can use inclusion-exclusion to count how many numbers less than or equal to some value `y` are coprime to `p`. With this, we can treat the problem as a search: find the smallest number `y` greater than `x` such that there are exactly `k` numbers between `x` and `y` that are coprime to `p`. This reduces the problem to binary search combined with a fast counting function. Counting via inclusion-exclusion is efficient because the number of distinct prime factors of any number up to `10^6` is at most 7 (since 2 * 3 * 5 * 7 * 11 * 13 * 17 > 10^6).

The brute-force and optimal approaches can be compared as follows:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k * log p) per query | O(1) | Too slow for large k or small p |
| Inclusion-Exclusion + Binary Search | O(2^m * log(range)) per query, m = #prime factors of p | O(m) | Efficient and Accepted |

## Algorithm Walkthrough

1. Precompute all prime numbers up to `10^6` using the sieve of Eratosthenes. This lets us factor any `p` efficiently.
2. For each query `(x, p, k)`, factor `p` into its distinct prime factors. The number of factors `m` is small.
3. Define a function `count_coprime(y)` that counts how many integers ≤ `y` are coprime to `p`. Using inclusion-exclusion, iterate over all subsets of the prime factors of `p`. For each subset, compute the product of the primes and subtract or add the floor division `y // product` according to the parity of the subset size.
4. Perform a binary search for the smallest integer `y` such that `count_coprime(y) - count_coprime(x) == k`. Initialize `low = x + 1` and `high` as `x + k * p` (this is an upper bound; in the worst case, every `p` numbers contain at least one coprime number).
5. Return `y` as the `k`-th number in the sequence.

This works because the inclusion-exclusion count gives an exact number of integers coprime to `p` up to any limit. Binary search efficiently finds the number where exactly `k` coprimes appear after `x`. The invariant is that at every step of the search, the true answer remains within the search interval.

## Python Solution

```python
import sys
input = sys.stdin.readline

def sieve(n):
    spf = list(range(n + 1))
    for i in range(2, int(n**0.5) + 1):
        if spf[i] == i:
            for j in range(i*i, n+1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf

def factorize(n, spf):
    primes = set()
    while n > 1:
        primes.add(spf[n])
        n //= spf[n]
    return list(primes)

def count_coprime(y, primes):
    from itertools import combinations
    res = y
    m = len(primes)
    for sz in range(1, m+1):
        for comb in combinations(primes, sz):
            prod = 1
            for c in comb:
                prod *= c
            if sz % 2 == 1:
                res -= y // prod
            else:
                res += y // prod
    return res

def solve():
    spf = sieve(10**6)
    t = int(input())
    for _ in range(t):
        x, p, k = map(int, input().split())
        primes = factorize(p, spf)
        low = x + 1
        high = x + k * p
        while low < high:
            mid = (low + high) // 2
            if count_coprime(mid, primes) - count_coprime(x, primes) >= k:
                high = mid
            else:
                low = mid + 1
        print(low)

solve()
```

The sieve is used to factor `p` efficiently. The `count_coprime` function applies inclusion-exclusion on the prime factors to determine the exact number of integers coprime to `p` up to any value. Binary search locates the `k`-th coprime number greater than `x`. Care is taken to set the search upper bound safely as `x + k * p` to avoid overshooting.

## Worked Examples

Sample Input 1:

```
x = 7, p = 22, k = 3
```

Prime factors of 22: 2, 11.

Binary search counts coprime numbers using inclusion-exclusion:

| mid | count_coprime(mid) | count_coprime(mid) - count_coprime(7) | binary search decision |
| --- | --- | --- | --- |
| 13 | 6 | 2 | increase low |
| 15 | 7 | 3 | decrease high |

Result: `15`.

Sample Input 2:

```
x = 5, p = 6, k = 4
```

Prime factors: 2, 3. Coprime numbers >5: 7, 11, 13, 17. Result: `17`.

This demonstrates the algorithm handles small `x` and small `p` correctly, skipping numbers divisible by 2 or 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * 2^m * log(k*p)) | Binary search over `y` with inclusion-exclusion on `m` prime factors of `p` |
| Space | O(n) | Sieve storage up to 10^6, prime factors array per query |

For `t = 3 * 10^4` and `m ≤ 7`, this is fast enough under the 5-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# provided samples
assert run("3\n7 22 1\n7 22 2\n7 22 3\n") == "9\n13\n15", "sample 1"

# minimum-size input
assert run("1\n1 1 1\n") == "2", "minimum input"

# maximum-size p
assert run("1\n1 1000000 5\n") == "6\n7\n11\n13\n17".split()[4], "large p"

# all equal values
assert run("1\n5 6 3\n") == "13", "skip multiples"

#
```
