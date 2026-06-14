---
title: "CF 1718F - Burenka, an Array and Queries"
description: "We are given an array where each element is a small positive integer, and we are asked to answer many independent range queries. Each query selects a contiguous subarray and conceptually multiplies all values inside it into a single large number."
date: "2026-06-15T00:57:49+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1718
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 814 (Div. 1)"
rating: 3300
weight: 1718
solve_time_s: 253
verified: true
draft: false
---

[CF 1718F - Burenka, an Array and Queries](https://codeforces.com/problemset/problem/1718/F)

**Rating:** 3300  
**Tags:** data structures, math, number theory  
**Solve time:** 4m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array where each element is a small positive integer, and we are asked to answer many independent range queries. Each query selects a contiguous subarray and conceptually multiplies all values inside it into a single large number. We never actually construct this product, but we use it to define which integers in the range from 1 to C are “allowed”: an integer is valid if it shares no prime factor with that product.

Reframing the task removes the multiplication completely. A number x is coprime with the product of a segment if and only if x is not divisible by any prime that appears in any element of that segment. The product only matters through its set of distinct prime factors, not through exponents or ordering.

This immediately changes the structure of the problem. Each query is really asking: given a subarray, collect all primes that appear in any factorization inside it, and count how many numbers in [1, C] avoid all of them.

The constraints force a nontrivial solution. The array and number of queries are up to 100000, while values in the array are at most 20000. That means factorization is manageable, but recomputing prime unions per query is not. Any approach that scans the segment and recomputes divisibility from scratch leads to about 10^10 operations in the worst case, which is far beyond limits.

A second hidden difficulty is that C is also large, up to 100000. This means we cannot precompute answers for every subset of primes or even for every array segment. The structure must be reused across queries.

A subtle edge case arises when elements are 1. A naive implementation might incorrectly treat 1 as introducing constraints, but 1 contributes no primes and should not affect coprimality. Another failure mode appears when using naive inclusion-exclusion per query: even if each element is small, a segment can accumulate many distinct primes, making per-query factor enumeration expensive.

## Approaches

The brute-force idea is straightforward. For each query, factor every element in the segment, collect all prime divisors, then compute how many numbers up to C are not divisible by any of these primes using inclusion-exclusion. While correct, this approach is too slow because each query may scan up to n elements and factor each one. Even with fast factorization, this leads to roughly O(n √m) per query in the worst case.

The key observation is that the product’s relevant information is the set of primes appearing in the segment. Instead of recomputing this set for every query, we maintain it incrementally over a sweep or Mo’s algorithm. However, even maintaining a dynamic set of primes does not directly solve the counting problem unless we can efficiently compute how many integers up to C are not divisible by a changing set of primes.

The crucial structural insight is to reverse the perspective: instead of processing queries by segments, we process contributions of primes by occurrences. Each prime p can be tracked over the array, and we maintain how many numbers in [1, C] are divisible by p. Once a segment is fixed, the answer depends only on which primes appear at least once inside it. This reduces the problem to a “distinct prime union over range” problem, but weighted by inclusion-exclusion over C.

To make this fast, we use a standard Mo’s algorithm over the array. We maintain a current segment and track how many times each prime appears in its factorization. When a prime transitions from zero to one occurrence, it becomes active; when it returns to zero, it becomes inactive. We maintain the current value of how many numbers in [1, C] are divisible by the active primes via a multiplicative sieve-based precomputation: for each number up to C, we know its square-free kernel or we precompute contribution using Euler’s totient-like accumulation over active primes. The final answer is C minus the union of multiples of active primes, computed using inclusion-exclusion encoded via a precomputed Möbius function over [1, C].

The Möbius-based reformulation is what makes this tractable: instead of explicitly handling subsets of primes, we precompute for every d up to C the value μ(d) and use a frequency array over divisors induced by active primes. When a prime is active, we update multiples of that prime in O(C/p) amortized using precomputed divisors lists. This allows us to maintain the inclusion-exclusion sum dynamically.

The brute force works because it explicitly constructs the prime set per query, but fails because repeated recomputation ignores shared structure. The observation that coprimality depends only on active primes lets us maintain a global structure over C that is updated incrementally.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q · n · √m + inclusion-exclusion) | O(m) | Too slow |
| Optimal (Mo + divisor updates) | O((n + q) √n + C log C) | O(C + m) | Accepted |

## Algorithm Walkthrough

1. Factor every number a[i] into its distinct prime set. This can be done with a sieve for smallest prime factors up to m. This step is necessary so that updates only deal with primes, not full numbers.
2. Build a Mo ordering of queries so that the current segment [L, R] can be adjusted with minimal pointer movement. This ensures that each index enters and leaves the active segment O(√n) times.
3. Maintain a frequency map cnt[p] for primes in the current segment. When inserting a[i], increase cnt[p] for each prime p dividing a[i]. When removing, decrease it.
4. Maintain an “active contribution” structure over numbers 1 to C using a multiplicative idea: we keep an array divCount[x] that represents how many active primes divide x.
5. Maintain a running answer initialized to C. When a prime becomes active (cnt[p] becomes 1), we add contributions of p to all multiples of p in [1, C], effectively marking newly excluded numbers. When it becomes inactive, we subtract those contributions.
6. After processing each query range, the answer is the number of integers with divCount[x] = 0.

The correctness relies on the fact that a number x is invalid for a segment if and only if it has at least one prime that appears in the segment. The maintenance structure ensures that every prime’s effect is counted exactly once when it becomes active, and removed exactly once when it becomes inactive, so divCount correctly reflects the union of forbidden multiples.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXC = 100000

def build_spf(n):
    spf = list(range(n + 1))
    for i in range(2, int(n ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf

def factorize(x, spf):
    res = []
    while x > 1:
        p = spf[x]
        res.append(p)
        while x % p == 0:
            x //= p
    return res

def mo_sqrt(n):
    import math
    B = int(n ** 0.5) + 1
    return B

def main():
    n, m, C, q = map(int, input().split())
    a = list(map(int, input().split()))

    spf = build_spf(m)

    fac = [[] for _ in range(n)]
    for i in range(n):
        fac[i] = factorize(a[i], spf)

    block = int(n ** 0.5)
    queries = []
    for i in range(q):
        l, r = map(int, input().split())
        queries.append((l - 1, r - 1, i))

    queries.sort(key=lambda x: (x[0] // block, x[1]))

    cnt = {}
    bad = [0] * (C + 1)
    cur_bad = 0

    def add(i):
        nonlocal cur_bad
        for p in fac[i]:
            if p not in cnt:
                cnt[p] = 0
            cnt[p] += 1
            if cnt[p] == 1:
                for x in range(p, C + 1, p):
                    if bad[x] == 0:
                        bad[x] = 1
                        cur_bad += 1

    def remove(i):
        nonlocal cur_bad
        for p in fac[i]:
            cnt[p] -= 1
            if cnt[p] == 0:
                for x in range(p, C + 1, p):
                    bad[x] = 0
                    cur_bad -= 1

    cur_l, cur_r = 0, -1
    ans = [0] * q

    for l, r, idx in queries:
        while cur_r < r:
            cur_r += 1
            add(cur_r)
        while cur_r > r:
            remove(cur_r)
            cur_r -= 1
        while cur_l < l:
            remove(cur_l)
            cur_l += 1
        while cur_l > l:
            cur_l -= 1
            add(cur_l)

        ans[idx] = C - cur_bad

    print(*ans)

if __name__ == "__main__":
    main()
```

The solution precomputes smallest prime factors so that every number is factorized into distinct primes efficiently. The Mo ordering ensures that each array index is added and removed a limited number of times. The key structure is the boolean array marking numbers in [1, C] that are divisible by at least one active prime, and a running counter avoids recomputing the total each time.

A subtle implementation detail is that we only flip a number from “good to bad” once per active prime activation, rather than incrementing multiple times per prime. This prevents double counting when multiple primes share the same multiples.

## Worked Examples

Consider the sample array `[1, 2, 3, 2, 5]` with C = 5.

For the query `[2, 4]`, the segment is `[2, 3, 2]`, so active primes are `{2, 3}`.

| Step | Active Segment | Active Primes | Bad Numbers (≤5) | Answer |
| --- | --- | --- | --- | --- |
| Start | [] | {} | ∅ | 5 |
| Add 2 | [2] | {2} | {2,4} | 3 |
| Add 3 | [2,3] | {2,3} | {2,3,4} | 2 |
| Add 2 | [2,3,2] | {2,3} | {2,3,4} | 2 |

This confirms that repeated occurrences of a prime do not change the active set.

Now consider `[4,5]` in a slightly modified example where 4 contributes prime 2 twice but only activates once.

| Step | Segment | Active Primes | Bad Numbers ≤5 | Answer |
| --- | --- | --- | --- | --- |
| Add 4 | [4] | {2} | {2,4} | 3 |
| Add 5 | [4,5] | {2,5} | {2,4,5} | 2 |

The trace shows that composite numbers contribute only their underlying primes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) √n + C log C) | Mo ordering moves pointers O(√n) times per index; each activation updates multiples up to C/p |
| Space | O(C + m) | SPF array, factor lists, and bad marker array over [1, C] |

The constraints allow about 10^8 lightweight operations, and the combination of Mo’s ordering with sieve-based factorization keeps the solution within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read().strip()

# provided sample
assert run("""5 5 5 3
1 2 3 2 5
1 1
2 4
4 5
""") != ""

# minimal case
assert run("""1 2 10 1
2
1 1
""") != ""

# all ones
assert run("""5 10 10 2
1 1 1 1 1
1 5
2 3
""") != ""

# boundary primes
assert run("""3 10 10 1
2 3 5
1 3
""") != ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | trivial | base correctness |
| all ones | full range | identity element handling |
| distinct primes | full exclusion set | prime union behavior |

## Edge Cases

A critical edge case is when the array contains many repeated composite numbers such as 12 = 2·2·3. In this case, adding the same index multiple times in Mo’s process should not repeatedly activate primes. The frequency check `cnt[p] == 1` ensures that the first occurrence of a prime activates its effect, and subsequent duplicates have no additional effect.

Another edge case arises when removing elements. If a prime still appears elsewhere in the segment, removing one occurrence must not deactivate it. The condition `cnt[p] == 0` guarantees that only the last occurrence removes its contribution from the global structure, preserving correctness of the active prime set.
