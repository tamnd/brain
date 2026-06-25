---
title: "CF 106098I - MEDAA and Totients"
description: "For every number $ai$, Meda computes $$f(ai)=prod{p mid ai}left(1-frac1pright)$$ where the product runs over the distinct prime divisors of $ai$."
date: "2026-06-25T11:56:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106098
codeforces_index: "I"
codeforces_contest_name: "The American University in Cairo CSEA Fall 2025 contest"
rating: 0
weight: 106098
solve_time_s: 60
verified: true
draft: false
---

[CF 106098I - MEDAA and Totients](https://codeforces.com/problemset/problem/106098/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

For every number $a_i$, Meda computes

$$f(a_i)=\prod_{p \mid a_i}\left(1-\frac1p\right)$$

where the product runs over the distinct prime divisors of $a_i$.

We are given an array of up to $2 \cdot 10^5$ integers, each at most $10^6$, and must determine how many distinct rational values appear among all computed $f(a_i)$.

The first observation is that exponents do not matter. The value depends only on which primes divide the number, not on how many times they divide it. For example,

$$f(12)=\left(1-\frac12\right)\left(1-\frac13\right)$$

and

$$f(36)=\left(1-\frac12\right)\left(1-\frac13\right)$$

because both numbers have the same set of distinct prime factors.

The constraints immediately rule out factorizing every number by trial division up to $\sqrt{10^6}$. In the worst case that would require roughly $2 \cdot 10^5 \cdot 1000$ operations, which is already too large in Python. Since all values are at most $10^6$, a sieve-based preprocessing approach is the natural direction.

A subtle point is that two different sets of prime divisors never produce the same value of $f$. A solution that stores floating-point approximations can fail because distinct rational numbers may become indistinguishable after rounding.

Consider the numbers:

```
6 10
```

Their values are

$$f(6)=\frac12\cdot\frac23=\frac13$$

and

$$f(10)=\frac12\cdot\frac45=\frac25$$

These are different rationals. Any approach based on low-precision floating-point arithmetic risks merging values that should remain distinct.

Another easy mistake is to distinguish numbers by their full factorization instead of their distinct prime set.

For example:

```
2 4 8 16
```

All four numbers have the same prime divisor set $\{2\}$, so every value equals $1/2$, and the answer is 1.

## Approaches

A brute-force solution would factor each number, explicitly compute the rational value of

$$\prod_{p \mid n}\left(1-\frac1p\right),$$

reduce the fraction, and insert it into a set.

This is correct because the formula directly defines the value. The bottleneck is factorization. Trial division up to $\sqrt{n}$ costs about 1000 checks per number when $n$ is near $10^6$. With $2 \cdot 10^5$ numbers, that becomes hundreds of millions of operations.

The key observation is that

$$f(n)=\prod_{p\mid n}\frac{p-1}{p}.$$

The value depends only on the set of distinct prime divisors.

Now comes the crucial number theoretic fact. Suppose two numbers have prime sets $S_1$ and $S_2$. Then

$$\prod_{p\in S_1}\frac{p-1}{p}
=
\prod_{p\in S_2}\frac{p-1}{p}.$$

Multiplying both sides by the product of all involved primes gives

$$\prod_{p\in S_1}(p-1)\prod_{q\in S_2\setminus S_1}q
=
\prod_{p\in S_2}(p-1)\prod_{q\in S_1\setminus S_2}q.$$

Take a prime $r$ that belongs to exactly one set, say $r\in S_1\setminus S_2$. The right side is divisible by $r$, because it contains the factor $r$. The left side is not divisible by $r$, since $r\nmid (r-1)$ and $r\nmid (p-1)$ for every other prime factor appearing there. Contradiction.

Hence equal values imply identical prime sets.

The problem is now much simpler. We only need to count how many distinct sets of prime divisors appear in the array.

Since $a_i \le 10^6$, we can precompute the smallest prime factor for every number using a sieve. Then each number can be factorized in logarithmic time, its distinct prime divisors extracted, and the resulting tuple inserted into a set.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n\sqrt A)$ | $O(n)$ | Too slow |
| Optimal | $O(A \log\log A + n\log A)$ | $O(A)$ | Accepted |

Here $A = 10^6$.

## Algorithm Walkthrough

1. Read the array and determine the maximum value appearing in it.
2. Build a smallest-prime-factor sieve up to that maximum value.
3. For each number, repeatedly divide by its smallest prime factor.
4. Whenever a new prime factor is encountered, append it to a list of distinct primes.
5. Skip all repeated occurrences of the same prime before continuing factorization. This extracts only the distinct prime divisor set.
6. Convert the list of distinct primes into a tuple and insert it into a set.
7. After processing all numbers, output the size of the set.

The reason step 6 works is that the tuple uniquely identifies the prime divisor set, and the proof above shows that the value of $f(n)$ is uniquely determined by that set.

### Why it works

For every number $n$, the value $f(n)$ depends only on its distinct prime divisors.

We proved that two different prime-divisor sets cannot produce the same value of $f$. Thus there is a one-to-one correspondence between values of $f$ and sets of distinct prime divisors.

The algorithm stores exactly those sets. Every occurrence of the same set contributes the same tuple, and every different set contributes a different tuple. The number of distinct tuples is exactly the number of distinct values of $f$.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

mx = max(a)

spf = list(range(mx + 1))
for i in range(2, int(mx ** 0.5) + 1):
    if spf[i] == i:
        for j in range(i * i, mx + 1, i):
            if spf[j] == j:
                spf[j] = i

seen = set()

for x in a:
    primes = []

    while x > 1:
        p = spf[x]
        primes.append(p)

        while x % p == 0:
            x //= p

    seen.add(tuple(primes))

print(len(seen))
```

The sieve stores the smallest prime factor for every number. This allows each factorization to repeatedly peel off one prime at a time.

The inner loop removes all copies of the same prime. That is the critical detail because the function depends on distinct prime divisors only. Without removing repetitions, numbers such as 2 and 4 would generate different signatures even though they produce the same value.

Using tuples inside a Python set provides a compact representation of prime-divisor sets. Since factorization naturally discovers primes in increasing order when using the SPF sieve, the tuple representation is canonical and needs no extra sorting.

## Worked Examples

### Example 1

Input:

```
3
2 3 4
```

| Number | Distinct primes | Stored tuple | Set size |
| --- | --- | --- | --- |
| 2 | {2} | (2,) | 1 |
| 3 | {3} | (3,) | 2 |
| 4 | {2} | (2,) | 2 |

Answer: `2`.

This demonstrates that powers of the same prime collapse to the same signature.

### Example 2

Input:

```
6
3 9 93842 123 2 1024
```

| Number | Distinct primes | Stored tuple |
| --- | --- | --- |
| 3 | {3} | (3,) |
| 9 | {3} | (3,) |
| 93842 | {2, 11, 4261} | (2, 11, 4261) |
| 123 | {3, 41} | (3, 41) |
| 2 | {2} | (2,) |
| 1024 | {2} | (2,) |

Distinct tuples are:

$$(3,),\ (2,11,4261),\ (3,41),\ (2,)$$

so the answer is `4`.

This example shows that repeated powers do not create new values, while a different prime set always does.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(A \log \log A + n \log A)$ | SPF sieve plus factorization of all numbers |
| Space | $O(A)$ | Smallest-prime-factor array |

With $A \le 10^6$ and $n \le 2 \cdot 10^5$, this easily fits within the contest limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    mx = max(a)

    spf = list(range(mx + 1))
    for i in range(2, int(mx ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, mx + 1, i):
                if spf[j] == j:
                    spf[j] = i

    seen = set()

    for x in a:
        cur = []
        while x > 1:
            p = spf[x]
            cur.append(p)
            while x % p == 0:
                x //= p
        seen.add(tuple(cur))

    return str(len(seen))

# provided samples
assert run("3\n2 3 4\n") == "2", "sample 1"
assert run("6\n3 9 93842 123 2 1024\n") == "4", "sample 2"

# custom cases
assert run("1\n2\n") == "1", "minimum size"
assert run("4\n2 4 8 16\n") == "1", "same prime set"
assert run("3\n6 10 15\n") == "3", "three different prime sets"
assert run("5\n30 60 90 210 2310\n") == "3", "mixed repeated sets"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 2` | `1` | Minimum input size |
| `2 4 8 16` | `1` | Powers of same prime collapse |
| `6 10 15` | `3` | Different prime sets stay distinct |
| `30 60 90 210 2310` | `3` | Repeated and expanded prime sets |

## Edge Cases

Consider:

```
4
2 4 8 16
```

Factorizations produce the same distinct-prime tuple `(2,)` every time. The set ends with one element, so the answer is `1`. A solution that keeps exponents would incorrectly count four different signatures.

Consider:

```
2
6 10
```

The tuples are `(2,3)` and `(2,5)`. Both are inserted separately, giving answer `2`. This confirms that different prime sets are never merged.

Consider:

```
3
6 12 18
```

Every number has distinct prime divisors `{2,3}`. The algorithm extracts `(2,3)` for all three numbers, inserts it once, and outputs `1`. This verifies that repeated exponents are completely ignored, exactly as required by the definition of $f(n)$.
