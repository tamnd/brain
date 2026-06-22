---
title: "CF 105408G - GCDland Mystical Arrays"
description: "We are given a list of integers and asked to verify a very specific structural property: every pair of numbers in the list must share exactly the same greatest common divisor."
date: "2026-06-23T04:46:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105408
codeforces_index: "G"
codeforces_contest_name: "2024 ICPC Gran Premio de Mexico Repechaje"
rating: 0
weight: 105408
solve_time_s: 117
verified: true
draft: false
---

[CF 105408G - GCDland Mystical Arrays](https://codeforces.com/problemset/problem/105408/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of integers and asked to verify a very specific structural property: every pair of numbers in the list must share exactly the same greatest common divisor. In other words, if you pick any two positions in the array, compute their gcd, the value must not depend on which pair you chose.

The immediate implication is that the array is highly constrained. If even a single pair produces a different gcd value from another pair, the structure breaks and we must reject it.

The input size can reach one hundred thousand elements, and each value can be as large as ten million. This pushes us away from any approach that tries to explicitly examine all pairs, since that would require roughly $10^{10}$ gcd computations in the worst case, which is far beyond what a one second limit allows. Any acceptable solution must reduce the problem to something close to linear or near linear in the size of the array.

A subtle corner case comes from small values and repeated factors. For example, an array like $[2, 4, 8]$ behaves differently from $[2, 3, 4]$, even though both have small gcds. Another tricky situation is when all numbers share a common factor, but still differ in how that factor interacts with remaining primes, which can affect pairwise gcd consistency.

For instance, consider $[6, 10, 15]$. The gcd of all three is $1$, but pairwise gcds differ: $\gcd(6,10)=2$, $\gcd(6,15)=3$, $\gcd(10,15)=5$. A naive assumption that “global gcd being 1 is enough” fails immediately.

Another failure case is thinking that checking adjacent elements after sorting is sufficient. For $[6, 10, 15]$, sorting gives $[6,10,15]$, and adjacent gcds are $2$ and $5$, which already differ, but even if adjacent gcds matched in some crafted cases, non adjacent pairs could still violate the condition.

## Approaches

A direct interpretation suggests computing gcd for every pair and checking equality. This is correct but extremely expensive. With $N$ up to $10^5$, we would compute roughly $N(N-1)/2$ gcd operations. Each gcd is logarithmic, so this still collapses under the time limit.

The key observation is that if all pairwise gcds are identical, then there exists a single value $g$ such that every pair of elements shares exactly the same gcd $g$. This forces a strong structure: all numbers must be multiples of $g$, and after dividing each element by $g$, any pair of resulting numbers must have gcd equal to $1$. If any two reduced numbers share a prime factor, their gcd would exceed $1$, contradicting the requirement.

This transforms the problem into detecting whether any prime factor appears in more than one number after normalization.

We first compute the global gcd of the entire array. This value must equal the common pairwise gcd if the condition is true. Then we divide all elements by this gcd. The problem now becomes purely about the reduced array: we must ensure that no prime factor is shared between two different elements.

This can be checked efficiently using prime factorization with a sieve of smallest prime factors. Each number is factorized once, and we track which primes have already appeared. If a prime is seen in more than one element, the condition is violated.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force pairwise gcd check | O(N² log A) | O(1) | Too slow |
| GCD + prime factor tracking | O(N log A) | O(A) | Accepted |

## Algorithm Walkthrough

1. Compute the gcd of the entire array and store it as $g$. This value represents the only possible candidate for the common pairwise gcd, since every pairwise gcd must divide all elements.
2. Replace every element $a_i$ with $a_i / g$. This removes the forced common factor so we can focus only on extra shared structure.
3. Build a smallest prime factor table up to the maximum value in the array using a sieve. This allows fast factorization of each number.
4. For each reduced number, extract its distinct prime factors. We only care about whether a prime appears, not its multiplicity, because repeated powers do not change whether a gcd is greater than one.
5. Maintain a set or boolean array marking which primes have already been used in previous numbers.
6. If any prime factor appears in more than one distinct number, immediately conclude that not all pairwise gcds are equal and return NO.
7. If all numbers are processed without conflicts, return YES.

The central idea is that equal pairwise gcd forces disjointness of prime supports after normalization. Any overlap in prime factors between two different elements directly creates a pair whose gcd exceeds the shared baseline, breaking the condition.

## Why it works

After dividing by the global gcd $g$, every number becomes coprime with respect to the intended target structure. If two reduced numbers share a prime factor $p$, then their gcd is at least $p$, which is greater than $1$. That would imply the original pairwise gcd exceeds $g$, contradicting the assumption that all pairwise gcds are equal. Conversely, if no prime factor appears in more than one reduced number, then every pair shares exactly the same gcd $g$, since no additional common structure exists beyond the global factor.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXV = 10_000_000

# smallest prime factor sieve
spf = list(range(MAXV + 1))
for i in range(2, int(MAXV ** 0.5) + 1):
    if spf[i] == i:
        step = i
        start = i * i
        for j in range(start, MAXV + 1, step):
            if spf[j] == j:
                spf[j] = i

def factorize(x):
    res = []
    while x > 1:
        p = spf[x]
        res.append(p)
        while x % p == 0:
            x //= p
    return res

n = int(input())
a = list(map(int, input().split()))

import math

g = 0
for v in a:
    g = math.gcd(g, v)

used = set()

for v in a:
    v //= g
    if v == 1:
        continue
    factors = factorize(v)
    for p in set(factors):
        if p in used:
            print("NO")
            sys.exit()
        used.add(p)

print("YES")
```

The first stage computes a global gcd over all elements. This anchors the minimal common structure that must exist if the condition holds.

The sieve prepares fast factorization, which is essential because repeated trial division would be too slow for one hundred thousand numbers.

Each number is reduced by the global gcd, and then its prime support is extracted. Using a set of primes per number ensures repeated powers do not falsely trigger conflicts.

The global `used` set ensures that each prime appears in at most one reduced number, enforcing the disjointness condition that characterizes valid arrays.

## Worked Examples

### Example 1

Input:

```
5
10 2 4 12 15
```

First we compute the global gcd, which is 1. No reduction changes the array.

| Step | Current Value | Prime Factors | Used Primes | Decision |
| --- | --- | --- | --- | --- |
| 10 | 2, 5 | {2,5} | {2,5} | OK |
| 2 | 2 | {2} | conflict with 2 | NO |

At the second step, the number 2 introduces a prime already used by 10, so we immediately reject. This shows that overlapping prime structure across elements breaks the condition even when the global gcd is small.

### Example 2

Input:

```
3
2 4 6
```

Global gcd is 2, so we divide to get $[1, 2, 3]$.

| Step | Value | Reduced Value | Prime Factors | Used Primes | Decision |
| --- | --- | --- | --- | --- | --- |
| 2 | 1 | 1 | - | {} | OK |
| 4 | 2 | 2 | {2} | {2} | OK |
| 6 | 3 | 3 | {3} | {2,3} | OK |

No prime repeats across different numbers, so the structure is valid and we output YES.

This demonstrates that even when original numbers share multiple gcd patterns, normalization reveals whether the underlying prime structure is disjoint.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(MAXV \log \log MAXV + N \log MAXV)$ | sieve builds smallest prime factors, each number is factorized once |
| Space | $O(MAXV)$ | SPF array and tracking structures |

The sieve dominates preprocessing but is acceptable for the constraint $10^7$. Each element is processed in logarithmic time due to fast factorization, keeping the solution well within limits for $10^5$ elements.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    MAXV = 10_000_000
    spf = list(range(MAXV + 1))
    for i in range(2, int(MAXV ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, MAXV + 1, i):
                if spf[j] == j:
                    spf[j] = i

    def factorize(x):
        res = []
        while x > 1:
            p = spf[x]
            res.append(p)
            while x % p == 0:
                x //= p
        return res

    import math

    n = int(input())
    a = list(map(int, input().split()))

    g = 0
    for v in a:
        g = math.gcd(g, v)

    used = set()

    for v in a:
        v //= g
        if v == 1:
            continue
        for p in set(factorize(v)):
            if p in used:
                return "NO"
            used.add(p)

    return "YES"

# provided samples
assert run("5\n10 2 4 12 15\n") == "NO", "sample 1"
assert run("3\n2 4 6\n") == "YES", "sample 2"
assert run("4\n2 4 6 8\n") == "NO", "sample 3"

# custom cases
assert run("2\n7 7\n") == "YES", "all equal"
assert run("3\n6 10 15\n") == "NO", "distinct primes overlap structure"
assert run("3\n1 1 1\n") == "YES", "all ones"
assert run("3\n2 3 5\n") == "YES", "pairwise coprime after gcd=1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 identical numbers | YES | identical elements behave consistently |
| 6 10 15 | NO | classic overlapping prime conflict |
| all ones | YES | gcd normalization edge case |
| 2 3 5 | YES | fully disjoint prime structure |

## Edge Cases

For arrays where all elements are identical, the global gcd equals the element itself, and after reduction every value becomes 1. Since there are no primes left, no conflicts occur and the algorithm correctly returns YES.

For arrays like $[6, 10, 15]$, the global gcd is 1, so no reduction happens. The prime sets overlap indirectly through different pairs, but in practice the first detected repeated prime immediately violates the uniqueness condition, correctly producing NO.

For arrays containing many 1s, these contribute no prime factors after reduction. They do not interfere with the tracking structure, ensuring correctness even when a large portion of the array is neutral with respect to gcd structure.
