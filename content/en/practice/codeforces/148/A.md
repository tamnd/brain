---
title: "CF 148A - Insomnia cure"
description: "The problem asks us to figure out how many dragons get affected by a princess who has a unique way of defending herself. She targets every k-th, l-th, m-th, and n-th dragon with different actions. The total number of dragons is d."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 148
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 105 (Div. 2)"
rating: 800
weight: 148
solve_time_s: 94
verified: false
draft: false
---

[CF 148A - Insomnia cure](https://codeforces.com/problemset/problem/148/A)

**Rating:** 800  
**Tags:** constructive algorithms, implementation, math  
**Solve time:** 1m 34s  
**Verified:** no  

## Solution
## Problem Understanding

The problem asks us to figure out how many dragons get affected by a princess who has a unique way of defending herself. She targets every _k_-th, _l_-th, _m_-th, and _n_-th dragon with different actions. The total number of dragons is _d_. The input gives us five integers: _k_, _l_, _m_, _n_, and _d_. The output is a single integer representing the number of dragons that are hit by at least one of these actions.

The key observation is that a dragon can be affected multiple times, but we only count it once. For example, if a dragon is both the 6th dragon (affected by the 2nd action) and the 12th dragon (affected by the 3rd action), it still counts as a single damaged dragon. The challenge is efficiently counting these unique indices among all dragons.

The constraints are moderate. The maximum number of dragons, _d_, can be 10^5, which allows us to iterate over all dragons in a simple loop. The divisors _k_, _l_, _m_, _n_ are all ≤10, so checking whether a dragon index is divisible by these numbers is inexpensive. Edge cases to consider include the smallest _d_ of 1, or the divisors being 1, which will affect every dragon. A naive solution might miss edge cases where all divisors are 1 and should return _d_ itself.

## Approaches

A brute-force solution is straightforward. We can iterate over every dragon from 1 to _d_ and check if the index is divisible by _k_, _l_, _m_, or _n_. If it is, we increment a counter. This works because _d_ is only 10^5, so a simple loop with up to four modulo operations per iteration totals 4 × 10^5 operations, which is acceptable within the 2-second time limit. The brute-force approach works because the problem is essentially a counting problem with a small enough range for iteration, but it might feel inelegant compared to a formula-based approach.

The optimal approach uses the principle of inclusion-exclusion to count all dragons divisible by any of the numbers. Count dragons divisible by _k_, then those divisible by _l_, and so on, but subtract counts of overlaps, add triple overlaps, and subtract quadruple overlaps. The observation that makes this possible is that these numbers are small and their multiples repeat regularly, so we can calculate the count mathematically without iterating. For a problem of this scale, the brute-force is efficient enough and easier to implement and reason about, so we can stick to it without performance concerns.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(d) | O(1) | Accepted |
| Inclusion-Exclusion | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integers _k_, _l_, _m_, _n_, and _d_. These represent the attack frequencies and total dragons.
2. Initialize a counter `damaged` to zero. This will track the number of dragons affected.
3. Loop over all dragon indices from 1 to _d_. For each dragon:

1. Check if the index is divisible by _k_, _l_, _m_, or _n_. If any of these conditions hold, increment `damaged`.
4. After the loop, output the value of `damaged`.

Why it works: Every dragon is considered exactly once, and we check all four conditions for being attacked. Any dragon divisible by at least one of the numbers will be counted, and those divisible by multiple numbers are still counted only once. This guarantees correctness without double counting.

## Python Solution

```python
import sys
input = sys.stdin.readline

k = int(input())
l = int(input())
m = int(input())
n = int(input())
d = int(input())

damaged = 0
for i in range(1, d + 1):
    if i % k == 0 or i % l == 0 or i % m == 0 or i % n == 0:
        damaged += 1

print(damaged)
```

The code directly follows the algorithm. Each `input()` reads a single integer. The loop runs from 1 to `d` inclusive, checking divisibility with modulo. Using `or` ensures a dragon affected by multiple actions is counted only once. The final `print` outputs the correct count.

## Worked Examples

**Sample 1**

Input values: k=1, l=2, m=3, n=4, d=12

| i | i%k==0 | i%l==0 | i%m==0 | i%n==0 | damaged |
| --- | --- | --- | --- | --- | --- |
| 1 | True | False | False | False | 1 |
| 2 | True | True | False | False | 2 |
| 3 | True | False | True | False | 3 |
| ... | ... | ... | ... | ... | ... |
| 12 | True | True | True | True | 12 |

All dragons are affected because k=1 hits every dragon.

**Sample 2**

Input values: k=2, l=3, m=4, n=5, d=12

| i | i%k==0 | i%l==0 | i%m==0 | i%n==0 | damaged |
| --- | --- | --- | --- | --- | --- |
| 1 | False | False | False | False | 0 |
| 2 | True | False | False | False | 1 |
| 3 | False | True | False | False | 2 |
| 4 | True | False | True | False | 3 |
| ... | ... | ... | ... | ... | ... |
| 12 | True | True | True | False | 9 |

This demonstrates counting dragons divisible by multiple numbers without double counting.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(d) | Each dragon index from 1 to d is checked once against four divisors. |
| Space | O(1) | Only a single counter and loop variable are used. |

Given the constraints, O(10^5) operations are fast enough for a 2-second limit, and memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    k = int(input())
    l = int(input())
    m = int(input())
    n = int(input())
    d = int(input())

    damaged = 0
    for i in range(1, d + 1):
        if i % k == 0 or i % l == 0 or i % m == 0 or i % n == 0:
            damaged += 1
    return str(damaged)

# Provided samples
assert run("1\n2\n3\n4\n12\n") == "12", "sample 1"
assert run("2\n3\n4\n5\n12\n") == "9", "sample 2"

# Custom cases
assert run("1\n1\n1\n1\n1\n") == "1", "minimum d"
assert run("10\n10\n10\n10\n100000\n") == "10000", "maximum d with large k,l,m,n"
assert run("2\n2\n2\n2\n7\n") == "3", "all equal divisors, small d"
assert run("2\n3\n5\n7\n30\n") == "20", "combination of primes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 1 1 | 1 | Minimum d, all dragons affected |
| 10 10 10 10 100000 | 10000 | Large d with large divisors |
| 2 2 2 2 7 | 3 | Equal divisors, small d, off-by-one handling |
| 2 3 5 7 30 | 20 | Mixed prime divisors, counting multiples correctly |

## Edge Cases

When k=l=m=n=1 and d=1, the only dragon is affected, and the code returns 1 correctly because the modulo check triggers. If d=100000 with divisors all 10, the damaged count is 100000 divided by 10, producing 10000. When some divisors are larger than d, for instance k=50 and d=30, no dragon satisfies i%50==0, so the loop correctly ignores these without double counting or errors.
