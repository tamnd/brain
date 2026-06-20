---
title: "CF 106084B - Twin Guardians"
description: "We are given several independent queries. Each query contains two integers, and we need to decide whether these two numbers form a pair of twin primes."
date: "2026-06-20T12:59:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106084
codeforces_index: "B"
codeforces_contest_name: "2025 ICPC Asia Taiwan Online Programming Contest"
rating: 0
weight: 106084
solve_time_s: 43
verified: true
draft: false
---

[CF 106084B - Twin Guardians](https://codeforces.com/problemset/problem/106084/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent queries. Each query contains two integers, and we need to decide whether these two numbers form a pair of twin primes. The notion of twin primes here is very specific: two numbers qualify only if they are both prime and their difference is exactly two.

So for each pair, the task is not to factorize or compute anything complicated beyond primality and a simple relationship check between the two values. The output is a simple binary decision per test case: print a positive response if both numbers are prime and differ by exactly two, otherwise print a negative response.

The constraints are small enough that we can afford direct primality checks per number. Each value is at most 1,000,000 and there are at most 10 test cases. This immediately rules out anything like heavy preprocessing per query but comfortably allows a straightforward primality test in $O(\sqrt{n})$ or a precomputed sieve in $O(N \log \log N)$. Even the slower per-query approach is easily within limits because the total number of primality checks is tiny.

The only subtle edge cases come from inputs that almost satisfy the condition. A number pair might differ by two but include a composite number like (12, 14), or both numbers might individually be prime but not differ by two like (11, 13) which actually is valid, or (5, 7) which is also valid. Another edge case is when one number is prime and the other is not, for example (3, 5) is valid but (2, 4) fails because 4 is not prime even though the difference is correct. These cases matter because a naive implementation might only check the difference and forget primality entirely.

## Approaches

The brute-force idea is straightforward. For each test case, we independently check whether both numbers are prime. The simplest primality check tries dividing the number by every integer from 2 up to its square root. If neither number has a divisor, we accept the pair only if their difference is exactly two.

This works correctly because primality is defined directly and no structural trick is needed. The inefficiency appears when we consider the worst case: checking primality for a number up to one million requires about 1,000 divisions, so a single test case costs roughly 2,000 checks. With 10 test cases this is only about 20,000 operations, which is already trivial, so even this brute-force approach is acceptable under the constraints.

Still, we can simplify reasoning further by precomputing all primes up to one million using a sieve. Once that array is built, each query becomes constant time: two lookups and one subtraction check. The sieve shifts work from query time to preprocessing time, which is negligible for this constraint size.

The key observation is that the problem is purely about membership in the set of primes, and that set is fixed for all queries. That makes preprocessing strictly better in terms of simplicity and repeated queries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Primality Check | $O(t \sqrt{n})$ | $O(1)$ | Accepted |
| Sieve + Lookup | $O(N \log \log N + t)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

We use a sieve to mark all primes up to one million.

1. Build a boolean array `is_prime` of size 1,000,001, initially assuming all numbers are prime except 0 and 1. This establishes a baseline where we only remove known composites.
2. Run a sieve from 2 upward. For each number that is still marked as prime, mark all of its multiples as non-prime. This step ensures every composite number gets eliminated exactly once per smallest prime factor.
3. After preprocessing, read each query pair (a, b).
4. For each pair, first check whether `b - a == 2`. This is necessary because twin primes must be exactly two apart.
5. If the difference condition fails, immediately output N because no primality test is needed.
6. If the difference condition holds, check whether both `a` and `b` are marked as prime in the sieve table.
7. Output Y only if both are prime, otherwise output N.

### Why it works

The sieve guarantees correct classification of every integer up to the limit. Since twin primes are defined purely by two independent primality conditions plus a fixed difference constraint, checking membership in the precomputed prime set is equivalent to performing full primality testing. The algorithm never relies on partial or heuristic checks, so every accepted pair satisfies both defining properties exactly, and every rejected pair violates at least one of them.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXN = 10**6

# Sieve of Eratosthenes
is_prime = [True] * (MAXN + 1)
is_prime[0] = is_prime[1] = False

p = 2
while p * p <= MAXN:
    if is_prime[p]:
        step = p
        start = p * p
        for x in range(start, MAXN + 1, step):
            is_prime[x] = False
    p += 1

t = int(input())
for _ in range(t):
    a, b = map(int, input().split())
    if b - a == 2 and is_prime[a] and is_prime[b]:
        print("Y")
    else:
        print("N")
```

The sieve is constructed once before handling any queries. This ensures every later check is a simple array lookup. The condition `b - a == 2` is checked first to avoid unnecessary prime table access in obvious failures, although this is mostly stylistic given the small constraints.

The core idea is that primality information is fully cached, so each query reduces to constant-time verification.

## Worked Examples

### Example 1

Input:

`11 13`

| Step | a | b | b - a | is_prime[a] | is_prime[b] | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 11 | 13 | 2 | True | True | Y |

Both numbers are prime and differ by exactly two, so the output is Y.

### Example 2

Input:

`12 14`

| Step | a | b | b - a | is_prime[a] | is_prime[b] | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 12 | 14 | 2 | False | False | N |

Even though the difference condition holds, neither number is prime, so the pair is rejected.

These examples show that both conditions are independently necessary, and failing either one invalidates the pair.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log \log N + t)$ | sieve preprocessing plus constant-time queries |
| Space | $O(N)$ | boolean array storing primality up to 1e6 |

The constraints allow up to 10 queries, and each query becomes a constant-time lookup. The sieve runs once and fits easily within both time and memory limits for $N = 10^6$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from io import StringIO as _StringIO

    # Re-run solution inline for testing
    input = sys.stdin.readline

    MAXN = 10**6
    is_prime = [True] * (MAXN + 1)
    is_prime[0] = is_prime[1] = False

    p = 2
    while p * p <= MAXN:
        if is_prime[p]:
            for x in range(p * p, MAXN + 1, p):
                is_prime[x] = False
        p += 1

    t = int(input())
    out = []
    for _ in range(t):
        a, b = map(int, input().split())
        if b - a == 2 and is_prime[a] and is_prime[b]:
            out.append("Y")
        else:
            out.append("N")

    return "\n".join(out)

# provided samples (as described in statement)
assert run("5\n2 3\n11 13\n12 14\n3 5\n5 7\n") == "N\nY\nN\nY\nY"

# custom cases
assert run("1\n2 4\n") == "N", "one prime, one composite"
assert run("1\n17 19\n") == "Y", "valid twin primes"
assert run("1\n19 21\n") == "N", "difference ok but composite"
assert run("1\n4 6\n") == "N", "both composite"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 4 | N | one number is composite despite correct gap |
| 17 19 | Y | valid twin prime pair |
| 19 21 | N | correct gap but second number not prime |
| 4 6 | N | both numbers non-prime |

## Edge Cases

One important edge case is when the difference condition is satisfied but primality fails. For example, input (12, 14) passes the gap check but both numbers are composite. The sieve marks both as false, so the algorithm correctly outputs N.

Another case is when both numbers are prime but the gap is not exactly two, such as (11, 13) is valid but (11, 17) is rejected despite both being primes. The algorithm first checks the difference and immediately rejects mismatched gaps, preventing unnecessary lookup work.

A final case is the smallest primes. For (2, 3), the difference is 1, so it is rejected even though both are prime. For (3, 5), both conditions hold and the algorithm correctly identifies it as a twin prime pair.
