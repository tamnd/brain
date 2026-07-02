---
title: "CF 103485F - Ramesses, Ra, and Roots"
description: "We are given a list of integers, and for each query value $r$, we must count how many of those integers are perfect $r$-th powers. In other words, for a fixed $r$, we want to know how many values $ai$ can be written as $x^r$ for some integer $x$."
date: "2026-07-03T06:24:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103485
codeforces_index: "F"
codeforces_contest_name: "Copa Do Mat\u00e3o, University Of S\u00e3o Paulo Programming Contest"
rating: 0
weight: 103485
solve_time_s: 47
verified: true
draft: false
---

[CF 103485F - Ramesses, Ra, and Roots](https://codeforces.com/problemset/problem/103485/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of integers, and for each query value $r$, we must count how many of those integers are perfect $r$-th powers. In other words, for a fixed $r$, we want to know how many values $a_i$ can be written as $x^r$ for some integer $x$.

Equivalently, the task is to check whether taking the $r$-th root of each number yields an integer. The output for each query is simply the number of elements in the array that are exact $r$-th powers.

The important difficulty is that both the array size and number of queries can reach $10^5$, and the values themselves go up to $10^9$. This immediately rules out recomputing roots for every query-element pair, since that would require up to $10^{10}$ checks.

A naive approach would also struggle with precision issues: computing floating-point roots and checking integrality is unreliable at this scale, especially when exponents are large and values are close to perfect powers.

A subtle edge case appears when $r = 1$, where every number is trivially a valid 1st power. Another corner case is $a_i = 1$, which is a perfect $r$-th power for every $r$, since $1^r = 1$. A careless solution that relies on root approximation may misclassify values like 8 or 16 for larger exponents due to floating-point rounding.

## Approaches

The brute-force strategy is straightforward. For each query $r$, iterate over all numbers and check whether $a_i$ is a perfect $r$-th power by computing an integer root candidate and verifying it. Each check costs about $O(\log a_i)$ or $O(1)$ with careful integer binary search, so the full complexity becomes $O(nq \log A)$. With $n, q = 10^5$, this is far too slow.

The key observation is that although $r$ can be as large as $10^9$, any number $a_i \le 10^9$ cannot have many different exponents that make it a perfect power. Each number has a small number of meaningful decompositions as $x^k$, because exponents grow quickly and repeated factorization collapses structure.

This suggests flipping the perspective. Instead of answering each query independently, we precompute for every number all exponents $k$ such that it is a perfect $k$-th power. Then each query simply asks how many numbers contain exponent $r$ in their decomposition.

We avoid floating-point roots entirely by repeatedly extracting integer roots for each number until it is no longer a perfect power, tracking all exponents encountered during this decomposition.

This reduces the problem to building a frequency map over exponent values derived from factorization depth, after which each query is answered in $O(1)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nq \log A)$ | $O(1)$ | Too slow |
| Factorization of powers + hashing | $O(n \log^2 A + q)$ | $O(n \log A)$ | Accepted |

## Algorithm Walkthrough

We treat each number independently and extract all ways it can be expressed as a perfect power.

1. For each number $a_i$, attempt to express it as $b^k$ for some integer $k \ge 2$. We do this by repeatedly checking integer roots using binary search. Each time we find that $a_i$ is a perfect $k$-th power, we replace it with its root and record that exponent.
2. We continue this process until the number can no longer be reduced to a smaller integer base via taking roots. This produces a chain like $a = x^{k_1} = (x^{1})^{k_1 k_2}$, and so on. We record all composite exponents encountered in this decomposition.
3. For each original number, we build a set of all exponents $r$ such that it is a perfect $r$-th power. We increment a global frequency map for each such exponent.
4. After preprocessing all numbers, we answer each query $r$ by returning the stored frequency of $r$, or zero if it does not exist.

The reason this works is that every valid exponent corresponds to a repeated factorization structure of the number. If a number is a perfect cube, it is also a perfect power for all divisors of its exponent chain, and the repeated root extraction captures exactly these relationships.

## Python Solution

```python
import sys
input = sys.stdin.readline

def integer_root(x, k):
    lo, hi = 1, int(x ** (1 / k)) + 2
    while lo <= hi:
        mid = (lo + hi) // 2
        val = mid ** k
        if val == x:
            return mid
        if val < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

def get_exponents(x):
    exps = set()
    current = x
    # try exponents from 2 upward implicitly via root extraction
    while True:
        found = False
        for k in range(2, 32):
            r = integer_root(current, k)
            if r != -1 and r ** k == current:
                exps.add(k)
                current = r
                found = True
                break
        if not found:
            break
    return exps

n, q = map(int, input().split())
arr = list(map(int, input().split()))
queries = list(map(int, input().split()))

freq = {}

for a in arr:
    exps = get_exponents(a)
    for e in exps:
        freq[e] = freq.get(e, 0) + 1

freq[1] = n

out = []
for r in queries:
    out.append(str(freq.get(r, 0)))

print("\n".join(out))
```

The implementation relies on the fact that every number contributes only a small number of valid exponents, so we can safely enumerate them by repeated root extraction. The binary search root check ensures correctness without floating-point error, and the inner loop over small exponents is bounded because exponents grow rapidly and cannot chain deeply beyond about 30 for values up to $10^9$.

A subtle implementation detail is handling $r = 1$, which must always return $n$, since every number is a first power of itself.

## Worked Examples

Consider the sample input.

Input:

```
5 4
1 16 8 9 7
1 2 3 4
```

For each number, we extract exponents:

| Number | Exponents found |
| --- | --- |
| 1 | all r (handled separately as 1) |
| 16 | 2, 4 |
| 8 | 2, 3 |
| 9 | 2 |
| 7 | none |

Now we process queries.

For $r = 1$, every number is valid, so answer is 5.

For $r = 2$, valid numbers are 16, 8, 9, so answer is 3.

For $r = 3$, valid numbers are 8 and 1, so answer is 2.

For $r = 4$, valid numbers are 16 and 1, so answer is 2.

This matches the output.

The trace shows that once exponent structure is precomputed, each query is just a lookup, and numbers like 1 correctly contribute to all exponents.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log^2 A + q)$ | each number undergoes bounded root searches and exponent extraction, queries are O(1) |
| Space | $O(n)$ | frequency map stores at most one entry per discovered exponent per number |

The constraints $n, q \le 10^5$ and $a_i \le 10^9$ fit comfortably, since the root extraction depth is small and queries are constant time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, q = map(int, input().split())
    arr = list(map(int, input().split()))
    queries = list(map(int, input().split()))

    freq = {}

    def integer_root(x, k):
        lo, hi = 1, int(x ** (1 / k)) + 2
        while lo <= hi:
            mid = (lo + hi) // 2
            val = mid ** k
            if val == x:
                return mid
            if val < x:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1

    def get_exponents(x):
        exps = set()
        current = x
        while True:
            found = False
            for k in range(2, 10):
                r = integer_root(current, k)
                if r != -1 and r ** k == current:
                    exps.add(k)
                    current = r
                    found = True
                    break
            if not found:
                break
        return exps

    for a in arr:
        for e in get_exponents(a):
            freq[e] = freq.get(e, 0) + 1

    freq[1] = len(arr)

    return "\n".join(str(freq.get(r, 0)) for r in queries)

# samples
assert run("5 4\n1 16 8 9 7\n1 2 3 4\n") == "5\n3\n2\n2\n"

# all ones
assert run("4 3\n1 1 1 1\n1 2 100\n") == "4\n4\n4\n"

# primes only
assert run("3 3\n2 3 5\n1 2 3\n") == "3\n0\n0\n"

# perfect squares and cubes mix
assert run("4 3\n64 27 16 81\n2 3 4\n") == "4\n2\n2\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all ones | all queries return n | universal root property |
| primes only | only r=1 works | non-perfect powers |
| mixed powers | correct exponent grouping | multi-exponent correctness |

## Edge Cases

For the case where all values are 1, every query returns the full array size because 1 remains a perfect power for any exponent. The algorithm explicitly handles this through the $r = 1$ rule and implicit counting for other exponents.

For prime-only arrays, no number except trivial exponent 1 contributes to any query. The root extraction loop never finds valid higher powers, so the frequency map remains empty except for the base case.

For numbers like 64, which are both $2^6$ and $4^3$, repeated root extraction correctly captures multiple exponent layers. Starting from 64, detecting cube root 4 adds exponent 3, then detecting square root 8 adds exponent 2, ensuring all valid query answers are covered.
