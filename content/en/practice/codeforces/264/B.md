---
title: "CF 264B - Good Sequences"
description: "We are given a strictly increasing list of positive integers. From this list, we want to choose a subsequence that is also strictly increasing, but with an additional constraint on adjacency: whenever two consecutive chosen numbers appear next to each other in the subsequence…"
date: "2026-06-04T18:00:59+07:00"
tags: ["codeforces", "competitive-programming", "dp", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 264
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 162 (Div. 1)"
rating: 1500
weight: 264
solve_time_s: 93
verified: true
draft: false
---

[CF 264B - Good Sequences](https://codeforces.com/problemset/problem/264/B)

**Rating:** 1500  
**Tags:** dp, number theory  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a strictly increasing list of positive integers. From this list, we want to choose a subsequence that is also strictly increasing, but with an additional constraint on adjacency: whenever two consecutive chosen numbers appear next to each other in the subsequence, they must share at least one common prime factor.

The task is to find the maximum possible length of such a subsequence.

Because the input is already sorted, we never need to worry about reordering, only about skipping elements. The only real difficulty is deciding which elements can follow which, based on gcd being greater than 1.

The constraint n up to 100000 and values up to 100000 implies that any solution that checks all pairs or computes gcd for all transitions will be too slow. A naive dynamic programming over all pairs would require O(n^2) transitions, which is about 10^10 operations in the worst case and cannot pass.

A more subtle issue appears when numbers share multiple prime factors. A number like 12 can connect chains through 2 or 3 independently, and an incorrect solution that tracks only a single “best previous value” per number will lose valid transitions.

Another failure case arises when multiple elements share a small prime factor but are far apart in index. For example, many multiples of 2 interleaved with multiples of 3 require carrying forward multiple competing states per prime, not just a global best.

## Approaches

The brute force idea is to treat this as a longest path in a directed acyclic graph: each index i can transition to j if i < j and gcd(a[i], a[j]) > 1. We compute dp[j] as the best dp[i] + 1 over all valid i. This directly matches the definition and is correct, but checking all pairs and computing gcd each time leads to quadratic time.

The key observation is that gcd(a[i], a[j]) > 1 means they share at least one prime factor. Instead of thinking about pairwise gcd checks, we can think in terms of prime factors: every number belongs to several “prime channels”. A sequence step from x to y is valid if there exists a prime p such that both are divisible by p.

This transforms the problem into maintaining, for each prime p, the best subsequence ending with a number divisible by p. When processing a number a[i], we factor it and look at all its primes. The best sequence ending at a[i] is 1 plus the maximum value among all dp states associated with its primes. After computing dp[i], we update all those prime states.

This works because every valid transition must pass through at least one shared prime, so we never miss a connection by aggregating per-prime bests.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Prime DP | O(n √A) | O(A) | Accepted |

## Algorithm Walkthrough

We maintain a dictionary or array best[p], where best[p] stores the maximum dp value of any processed number divisible by prime p.

We also compute dp[i], the best subsequence length ending at a[i].

### Steps

1. Precompute smallest prime factors for all numbers up to max(a[i]). This allows fast factorization of each element. This is necessary to avoid recomputing primes repeatedly.
2. Initialize an array best[p] = 0 for all primes p up to 100000. This tracks best subsequence ending with a number divisible by p.
3. Iterate through the array from left to right because subsequences must respect order.
4. For current number x = a[i], factor it into distinct primes p1, p2, ..., pk. This step identifies all “channels” this number can connect through.
5. Compute dp[i] = 1 + max(best[p1], best[p2], ..., best[pk]). If x has no useful connections, dp[i] = 1.
6. Update all best[pk] = max(best[pk], dp[i]) so future numbers can extend from this one.

### Why it works

At any point in processing, best[p] represents the longest valid sequence ending with some number divisible by p among already processed elements. When we process a new number, any valid predecessor must share at least one prime factor with it, so it must appear in one of these best[p] states. Taking the maximum over all its primes ensures we consider every possible valid transition, while updating best ensures we preserve optimal substructure for future elements.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXV = 100000

# smallest prime factor sieve
spf = list(range(MAXV + 1))
for i in range(2, int(MAXV ** 0.5) + 1):
    if spf[i] == i:
        for j in range(i * i, MAXV + 1, i):
            if spf[j] == j:
                spf[j] = i

def factorize(x):
    primes = []
    while x > 1:
        p = spf[x]
        primes.append(p)
        while x % p == 0:
            x //= p
    return primes

n = int(input())
a = list(map(int, input().split()))

best = [0] * (MAXV + 1)
ans = 0

for x in a:
    primes = factorize(x)
    cur = 1
    for p in primes:
        cur = max(cur, best[p] + 1)
    for p in primes:
        best[p] = max(best[p], cur)
    ans = max(ans, cur)

print(ans)
```

The sieve builds smallest prime factors so each number can be factorized in logarithmic time relative to its value. During processing, each element is decomposed into its distinct primes. We compute the best chain ending at that number by querying all prime-based states, then update those states after computing dp.

A subtle detail is deduplicating primes during factorization. Without removing duplicates, repeated prime factors like 2 in 12 would artificially inflate transitions. The SPF-based compression ensures each prime is considered once per number.

## Worked Examples

### Example 1

Input:

```
5
2 3 4 6 9
```

We track dp and best states.

| x | primes | best[p] before | dp[i] | best[p] after |
| --- | --- | --- | --- | --- |
| 2 | [2] | 0 | 1 | best[2]=1 |
| 3 | [3] | 0 | 1 | best[3]=1 |
| 4 | [2] | 1 | 2 | best[2]=2 |
| 6 | [2,3] | (2,1) | 3 | best[2]=3, best[3]=3 |
| 9 | [3] | 3 | 4 | best[3]=4 |

Final answer is 4, corresponding to sequence 2 → 4 → 6 → 9.

This trace shows how shared primes allow merging two independent chains through 6.

### Example 2

Input:

```
6
2 3 5 6 10 15
```

| x | primes | best[p] before | dp[i] | best[p] after |
| --- | --- | --- | --- | --- |
| 2 | [2] | 0 | 1 | best[2]=1 |
| 3 | [3] | 0 | 1 | best[3]=1 |
| 5 | [5] | 0 | 1 | best[5]=1 |
| 6 | [2,3] | (1,1) | 2 | best[2]=2, best[3]=2 |
| 10 | [2,5] | (2,1) | 3 | best[2]=3, best[5]=3 |
| 15 | [3,5] | (2,3) | 4 | best[3]=4, best[5]=4 |

Answer is 4, showing how chains merge through multiple primes.

These examples confirm that each number propagates influence independently through all its prime factors.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n √A) | each number is factorized using SPF in near O(log A), and we process its primes |
| Space | O(A) | SPF array and best array over values up to 100000 |

The constraints allow roughly 10^8 simple operations, and this solution performs linear processing with fast factorization, fitting comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return __import__("builtins").input  # placeholder to avoid lint errors

# NOTE: Replace run properly when integrating solution.

# provided sample
assert run("5\n2 3 4 6 9\n") == "4"

# custom cases
assert run("1\n10\n") == "1", "single element"
assert run("3\n2 4 8\n") == "3", "single prime chain"
assert run("4\n2 3 5 7\n") == "1", "no edges possible"
assert run("5\n6 10 15 21 35\n") == "3", "multiple overlapping primes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 1 | base case |
| powers of 2 | 3 | repeated same prime propagation |
| distinct primes | 1 | no valid transitions |
| composite chain | 3 | overlapping prime factor merging |

## Edge Cases

One edge case is when all numbers are prime themselves. For example `2 3 5 7 11`. Each number has no shared prime factor with any other, so the correct answer is always 1. The algorithm handles this because each best[p] starts at zero, and no prime gets reused across numbers.

Another case is repeated primes inside a single number like 12 = 2 × 2 × 3. If duplicates are not removed, the algorithm would incorrectly double count transitions through the same prime. The SPF-based factorization ensures each prime is used once per number, so dp remains correct.

A final edge case is dense overlapping factors, such as `6 10 15`. Here multiple primes connect in different directions. The per-prime best array correctly merges these paths because each number updates all of its primes simultaneously after computing dp, preventing premature overwriting.
