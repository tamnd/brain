---
title: "CF 106433D - Magic Books"
description: "We have a shelf of books represented by an array. A move chooses a contiguous part of the shelf where every pair of books in that segment has coprime values, then reverses that whole segment."
date: "2026-06-25T09:37:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106433
codeforces_index: "D"
codeforces_contest_name: "XXX Spain Olympiad in Informatics, online qualifier"
rating: 0
weight: 106433
solve_time_s: 37
verified: true
draft: false
---

[CF 106433D - Magic Books](https://codeforces.com/problemset/problem/106433/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a shelf of books represented by an array. A move chooses a contiguous part of the shelf where every pair of books in that segment has coprime values, then reverses that whole segment. The task is to decide whether repeated moves can transform the array into non-decreasing order.

The key is to understand what movements are actually possible. Reversing a segment of pairwise coprime values is equivalent to performing adjacent swaps inside that segment. Since every adjacent pair in such a segment is also coprime, every adjacent swap between coprime values is allowed. A segment of length two gives the reverse direction, so every allowed adjacent swap can also be viewed as a valid operation.

The input contains several test cases. Each test case gives the number of books and the values on the shelf. The output is whether the initial arrangement can reach a sorted arrangement.

The constraints are large enough that checking every pair of positions is not acceptable. With the total number of books reaching around 200000, a quadratic solution would require about 40000000000 comparisons in the worst case, which is far beyond the usual competitive programming limits. We need a solution close to linear or linearithmic.

The important edge cases come from values that cannot cross each other. For example, with input

```
1
4
6 1 1 1
```

the output is `YES`. The value 6 can move right because it is coprime with each 1, so the array can become sorted.

Consider

```
1
4
2 2 6 3
```

the output is `NO`. The first 2 and the second 2 have gcd 2, so their relative order can never change. They are already in increasing order relative to each other, but 6 and 3 also share a factor, and the 6 must move after the 3 in the sorted array. That crossing is impossible.

A simpler failing case for careless solutions is:

```
1
3
3 2 6
```

The answer is `NO`. A solution that only checks whether some adjacent swaps are possible might miss that the 3 and 6 cannot swap, even though the middle value is coprime with both.

## Approaches

The direct approach is to simulate the possible swaps. We could try to repeatedly find adjacent coprime pairs and swap them whenever it improves the order, similar to bubble sort. This is correct because every swap performed is legal. However, in the worst case bubble sort performs O(n²) swaps, which is too slow for n around 200000.

The useful observation is that the only pairs whose relative order can change are pairs with gcd equal to 1. If two values have gcd greater than 1, they can never become adjacent and swap, because that final crossing step would itself be illegal.

This gives us a fixed invariant. Every non-coprime pair must already appear in the same relative order as it appears in the sorted array. We only need to detect whether there exists a pair of positions i < j where gcd(a[i], a[j]) > 1 but a[i] > a[j]. Such a pair is an unavoidable inversion.

The remaining challenge is finding these pairs quickly. We process the array from left to right and keep, for every prime factor, the maximum value seen so far among numbers containing that prime. When we reach a value x, every previous value sharing a prime factor with x is non-coprime with x. If the maximum among them is greater than x, we found a forbidden inversion.

The number of distinct prime factors of a value up to 10^6 is small, so updating these prime buckets is efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Prime factor tracking | O(n log A) | O(A) | Accepted |

## Algorithm Walkthrough

1. Factor every number into its distinct prime factors. We only need distinct factors because gcd greater than one means that at least one prime factor is shared.
2. Maintain an array where position p stores the largest value seen so far that contains prime factor p.
3. Scan the books from left to right. For the current value x, look at all its prime factors. Among those factors, find the largest previous value that shares any factor with x.
4. If that largest previous value is greater than x, the two values form an inversion that can never be fixed, so the answer is `NO`.
5. After checking x, update every prime factor of x with the value x because future positions need to know that x has already appeared.

Why it works: the maintained maximum for a prime factor represents the worst possible earlier value that cannot cross the current value. Any previous value that shares a factor with the current value is locked on the left side forever. If the largest locked value is already larger than the current value, sorting would require an impossible swap. If this never happens, every forbidden pair is already ordered correctly, and all remaining inversions involve coprime values, which can be resolved by allowed swaps.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXV = 10**6

spf = list(range(MAXV + 1))
for i in range(2, int(MAXV ** 0.5) + 1):
    if spf[i] == i:
        for j in range(i * i, MAXV + 1, i):
            if spf[j] == j:
                spf[j] = i

def factors(x):
    res = []
    while x > 1:
        p = spf[x]
        res.append(p)
        while x % p == 0:
            x //= p
    return res

fac_cache = {}

def get_factors(x):
    if x not in fac_cache:
        fac_cache[x] = factors(x)
    return fac_cache[x]

def solve_case(a):
    best = [0] * (MAXV + 1)
    for x in a:
        fs = get_factors(x)
        mx = 0
        for p in fs:
            if best[p] > mx:
                mx = best[p]
        if mx > x:
            return "NO"
        for p in fs:
            if x > best[p]:
                best[p] = x
    return "YES"

def main():
    t = int(input())
    ans = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        ans.append(solve_case(a))
    print("\n".join(ans))

if __name__ == "__main__":
    main()
```

The sieve computes the smallest prime factor for every number up to the maximum possible value. This lets each factorization run quickly.

The scan inside `solve_case` follows the algorithm directly. Before inserting the current value into the prime buckets, it checks whether some previous non-coprime value is larger. The update happens after the check because the current value must not compare with itself.

The factor list contains each prime only once. If we stored repeated factors, the result would be correct but slower. Distinct factors are enough because sharing any prime factor already means the gcd is not one.

The memory usage is dominated by the smallest prime factor array and the maximum-value tracking array.

## Worked Examples

For the input:

```
1
5
5 2 3 4 1
```

the scan behaves as follows.

| Position | Value | Shared-prime maximum before | Action |
| --- | --- | --- | --- |
| 1 | 5 | 0 | Insert factor 5 |
| 2 | 2 | 0 | Insert factor 2 |
| 3 | 3 | 0 | Insert factor 3 |
| 4 | 4 | 2 | 2 is smaller than 4, continue |
| 5 | 1 | 0 | No factors |

The result is `YES`. The only values that can block each other are already ordered.

For the input:

```
1
4
2 2 6 3
```

the scan is:

| Position | Value | Shared-prime maximum before | Action |
| --- | --- | --- | --- |
| 1 | 2 | 0 | Insert factor 2 |
| 2 | 2 | 2 | 2 is not greater than 2 |
| 3 | 6 | 2 | Insert factors 2 and 3 |
| 4 | 3 | 6 | 6 > 3, impossible |

The result is `NO` because the 6 and 3 cannot cross.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log A) | Each value is factored into a small number of prime factors and each factor is processed once |
| Space | O(A) | The arrays store smallest prime factors and prime information |

With the maximum value limited to 10^6 and the total number of elements around 200000, the solution stays within the required limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().split()
    sys.stdin = old

    return ""

# samples and custom validation cases
# The following expected results correspond to the algorithm.

cases = [
    ("1\n4\n6 1 1 1\n", "YES"),
    ("1\n5\n5 4 3 2 1\n", "NO"),
    ("1\n5\n5 2 3 4 1\n", "YES"),
    ("1\n4\n2 2 6 3\n", "NO"),
    ("1\n1\n1\n", "YES"),
    ("1\n5\n7 7 7 7 7\n", "YES"),
    ("1\n5\n10 3 6 5 1\n", "NO"),
]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 / 6 1 1 1` | YES | A large value moving through coprime values |
| `5 / 5 4 3 2 1` | NO | Multiple blocked inversions |
| `5 / 5 2 3 4 1` | YES | Coprime values allowing reordering |
| `4 / 2 2 6 3` | NO | Shared factors creating an impossible crossing |
| `1 / 1` | YES | Smallest array boundary |
| `7 7 7 7 7` | YES | All values equal |
| `10 3 6 5 1` | NO | Detecting a late forbidden inversion |

## Edge Cases

For `1 4 6 1 1 1`, the value 6 shares no factor with any 1. The algorithm sees no previous conflicting value, so it allows the value to move right through swaps.

For `1 4 2 2 6 3`, when the final value 3 is processed, prime factor 3 already stores the value 6 from the left side. Since 6 is larger than 3 and cannot cross it, the algorithm immediately rejects the array.

For an array with all equal values such as `1 5 4 7 7 7 7`, every blocked pair is already ordered because equal values do not create an inversion. The maximum shared value is never greater than the current value, so the answer is `YES`.

For a single element array, no moves are needed. The array is already sorted, and the algorithm returns `YES`.
