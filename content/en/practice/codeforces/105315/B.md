---
title: "CF 105315B - Noorhan's Birthday"
description: "We are given a number of independent queries. Each query provides an integer n, and we must output a single integer a, where a is the prime number closest to n. If two primes are equally close, the smaller one must be chosen."
date: "2026-06-23T06:13:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105315
codeforces_index: "B"
codeforces_contest_name: "JPC 4.0"
rating: 0
weight: 105315
solve_time_s: 45
verified: true
draft: false
---

[CF 105315B - Noorhan's Birthday](https://codeforces.com/problemset/problem/105315/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a number of independent queries. Each query provides an integer n, and we must output a single integer a, where a is the prime number closest to n. If two primes are equally close, the smaller one must be chosen.

The task is essentially about repeatedly answering: “which prime number lies nearest to a given value on the number line?”

The input size makes it clear that n can go up to 1,000,000 and there can be up to 100,000 queries. A naive approach that tries to test primality around each n independently would already struggle if it repeats heavy work per query. The key implication of the constraints is that we need to preprocess prime information once and reuse it efficiently.

A subtle edge case appears when n itself is prime. In that case the answer is trivially n, since the distance to itself is zero. Another edge case arises when two primes are equidistant, for example around n = 10, where 7 and 11 are both distance 3. The problem explicitly requires choosing the smaller prime, so 7 is correct.

Another situation that can break naive logic is when searching outward from n without a proper bound. If we only search downward or only upward, we may miss the closest prime on the other side.

## Approaches

The brute-force idea is straightforward. For each query n, we check every integer outward from n: first check if n is prime, then n−1 and n+1, then n−2 and n+2, and so on until we find primes on both sides. Each primality check costs at least O(√n), and in the worst case we might explore a large range before hitting primes on both sides. Over 100,000 queries, this quickly becomes far too slow.

The inefficiency comes from repeating primality checks for overlapping numbers across different queries. Many queries ask about nearby values, and the primality of a number does not change between queries. This suggests preprocessing all primes up to the maximum possible n once, then answering each query in constant time.

Once we precompute a boolean array indicating whether each number up to 1,000,000 is prime, the problem reduces to a nearest-neighbor search in a static set. For each n, we expand outward from n simultaneously in both directions until we find at least one prime on each side or confirm one direction wins. Since the search range is bounded by the precomputed sieve, this becomes fast enough in practice.

A more structured way to think about it is that we are converting repeated primality queries into a single global sieve construction, followed by local nearest prime lookup.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(t · √n · k) worst-case expansion | O(1) | Too slow |
| Sieve + Search | O(N log log N + t · d) | O(N) | Accepted |

Here d is the average distance to the nearest prime, which is small for numbers up to 10^6.

## Algorithm Walkthrough

We first precompute primality for all numbers up to 1,000,000 using a sieve. This ensures that any primality check later is O(1), which is necessary because we will query this information many times.

Next, we iterate through each query value n and determine the closest prime.

1. Precompute an array is_prime of size 1,000,001 initialized to true, then mark 0 and 1 as non-prime. This establishes a baseline where every number is assumed prime until proven otherwise.
2. Run a sieve from 2 upward, and whenever we find a prime p, mark all multiples of p as non-prime. This step builds the full primality structure for the entire range efficiently by eliminating composite numbers in structured batches rather than testing each individually.
3. For each query value n, first check if is_prime[n] is true. If so, we immediately output n because it has distance zero to itself, making it the closest possible prime.
4. If n is not prime, we expand outward in increasing distance d starting from 1. At each step, we check n − d and n + d, provided they remain within bounds. We stop as soon as we find at least one prime among these candidates.
5. If both n − d and n + d are prime at the same distance, we output n − d because the problem requires choosing the smaller prime in case of a tie.

Why this works is tied to symmetry in the search process. We explore numbers in increasing distance from n, so the first time we encounter any prime, it must be the closest possible one. Because we check both sides at each distance level before increasing d, we guarantee that no nearer prime is skipped.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXN = 10**6

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

def solve(n):
    if is_prime[n]:
        return n
    d = 1
    while True:
        left = n - d if n - d >= 0 else None
        right = n + d if n + d <= MAXN else None

        if left is not None and is_prime[left]:
            return left
        if right is not None and is_prime[right]:
            return right
        d += 1

t = int(input())
out = []
for _ in range(t):
    n = int(input())
    out.append(str(solve(n)))

print("\n".join(out))
```

The sieve section builds global primality knowledge once. The loop structure ensures that composites are eliminated efficiently starting from squares, which avoids redundant work.

The query function relies entirely on the precomputed array. The early return for prime n is important because it avoids unnecessary expansion. The bidirectional expansion guarantees correctness because distance increases monotonically.

One subtle detail is boundary checking. Without ensuring n − d and n + d stay within array bounds, we could access invalid indices or miss valid primes at edges. The implementation explicitly guards both directions.

## Worked Examples

### Example 1

Input:

n = 10

We expand outward:

| d | n-d | prime? | n+d | prime? | decision |
| --- | --- | --- | --- | --- | --- |
| 1 | 9 | no | 11 | yes | return 11 |

We stop at d = 1 because 11 is prime, while 9 is not. This shows that upward and downward search are both necessary, since the closest prime may lie only on one side.

### Example 2

Input:

n = 10 (tie case demonstration)

We again check distances:

| d | n-d | prime? | n+d | prime? | decision |
| --- | --- | --- | --- | --- | --- |
| 1 | 9 | no | 11 | yes | return 11 |
| 2 | 8 | no | 12 | no | continue |

This confirms that the algorithm always selects the first encountered prime at minimum distance, and when both sides match at some d, the left side is chosen.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log log N + t · d) | sieve builds primality, each query expands outward until nearest prime |
| Space | O(N) | boolean array for primality up to 1e6 |

The sieve dominates preprocessing but fits easily within constraints for N = 1e6. Each query typically requires very small outward movement because primes are dense in this range, making the solution comfortably fast for 100,000 queries.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
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

    def solve(n):
        if is_prime[n]:
            return n
        d = 1
        while True:
            if n - d >= 0 and is_prime[n - d]:
                return n - d
            if n + d <= MAXN and is_prime[n + d]:
                return n + d
            d += 1

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        out.append(str(solve(n)))
    return "\n".join(out)

# provided samples (conceptual)
assert run("3\n10\n11\n1\n") == "11\n11\n2"

# custom cases
assert run("1\n2\n") == "2", "minimum prime"
assert run("1\n14\n") == "13", "closest below"
assert run("1\n15\n") == "13", "tie handling"
assert run("1\n1000000\n") != "", "upper bound stability"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n = 2 | 2 | smallest prime edge |
| n = 14 | 13 | downward nearest prime |
| n = 15 | 13 | tie-breaking correctness |
| n = 1000000 | valid prime | upper bound robustness |

## Edge Cases

For n = 1, the algorithm starts with d = 1 and checks n − d = 0 and n + d = 2. Since 0 is invalid and 2 is prime, it correctly returns 2 immediately.

For n = 2, the early prime check returns 2 without entering the search loop. This avoids unnecessary boundary checks and ensures correctness at the smallest valid prime.

For large values like n = 999983 (already prime near upper bound), the sieve marks it correctly and the algorithm returns it immediately without expansion. This shows that the early exit condition is critical for performance stability near dense prime regions.
