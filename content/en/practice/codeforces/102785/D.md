---
title: "CF 102785D - We were trying to share an orange ..."
description: "The orange is described only through the number of slices it has. A company with x people can share the orange exactly when the number of slices is divisible by x, so the valid company sizes are exactly the positive divisors of the slice count."
date: "2026-07-27T19:37:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102785
codeforces_index: "D"
codeforces_contest_name: "ICPC Central Russia Regional Contest (CRRC 18)"
rating: 0
weight: 102785
solve_time_s: 75
verified: true
draft: false
---

[CF 102785D - We were trying to share an orange ...](https://codeforces.com/problemset/problem/102785/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

The orange is described only through the number of slices it has. A company with `x` people can share the orange exactly when the number of slices is divisible by `x`, so the valid company sizes are exactly the positive divisors of the slice count.

The task is to find the smallest positive integer `m` whose number of divisors is exactly `k`. If no such number exists, the answer should be `-1`. In this problem every positive integer has at least one divisor, so a valid answer always exists for every positive `k` in the given range.

The input value `k` is at most 1000. This is small enough to allow algorithms that depend on the factors of `k`, but it rules out checking every possible orange size. The smallest number with many divisors can already become very large, so a simulation that tries values of `m` and counts their divisors would quickly become impractical.

A few cases require care. When `k = 1`, the orange must have exactly one divisor, which only happens for `m = 1`. A solution that starts searching from `2` would incorrectly fail on this case. For input `1`, the correct output is `1`.

A second trap is assuming that the answer must be a prime number or a power of one prime. For example, when `k = 4`, the answer is `6`, because its divisors are `1, 2, 3, 6`. A careless search over only prime powers would miss this and produce a larger answer such as `8`.

Another issue is the ordering of prime exponents. For `k = 12`, the factorization of the divisor count can be represented by `(3 * 2 * 2)`, giving exponents `(2, 1, 1)` and number `2² * 3 * 5 = 60`. Using exponents `(1, 2, 1)` gives `2 * 3² * 5 = 90`, which is larger. A construction that does not place larger exponents on smaller primes can produce a correct divisor count but not the minimum number.

## Approaches

A direct approach would try positive integers one by one. For every candidate `m`, we could count its divisors by checking all values from `1` to `sqrt(m)`. This is correct because it eventually reaches the smallest number with exactly `k` divisors, but it has no useful upper bound on how far it might search. The number of candidates and the divisor checks both grow too quickly, making this approach unusable.

The key observation comes from the divisor formula. If

`m = p1^a1 * p2^a2 * ... * pt^at`

then the number of divisors is

`(a1 + 1) * (a2 + 1) * ... * (at + 1)`.

Instead of searching over possible numbers, we can search over possible factorizations of `k`. Each factor in this multiplication becomes one exponent plus one.

To make the number as small as possible, the largest exponents must be assigned to the smallest primes. If we have exponents `5` and `2`, assigning them to primes `2` and `3` gives `2^5 * 3^2`, which is smaller than `2^2 * 3^5`. This means we only need to consider exponent sequences that are non-increasing.

The optimal search recursively splits `k` into factors. A chosen factor `d` means the current prime receives exponent `d - 1`. After choosing it, the remaining divisor count becomes `k / d`. Because `k` is only 1000, the number of such factorizations is very small.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(answer × sqrt(answer)) | O(1) | Too slow |
| Optimal | O(number of multiplicative partitions of k) | O(number of prime factors of k) | Accepted |

## Algorithm Walkthrough

1. Handle the special case `k = 1`. The only number with one divisor is `1`, so the answer is immediately `1`.
2. Start a recursive search with the remaining divisor count equal to `k`, the first available prime equal to `2`, and the current constructed number equal to `1`.
3. Choose a factor `d` of the remaining divisor count. This factor represents the value `exponent + 1` for the current prime, so multiply the current number by `prime^(d - 1)`.
4. Recurse on the remaining part `remaining / d`, moving to the next prime. Restrict the next chosen factor to be no larger than `d`, because factors must be non-increasing to keep exponents non-increasing.
5. When the remaining divisor count becomes `1`, all required exponents have been assigned. Compare the constructed number with the best answer found so far.

The search only explores valid factorizations of `k`. Every path creates a number whose divisor count is exactly `k`, and the ordering restriction guarantees that no equivalent factorization is skipped in a way that could produce a smaller answer.

Why it works: Every positive integer has a unique prime factorization, so every possible answer corresponds to exactly one sequence of exponents. The divisor formula converts the requirement into a factorization of `k`. The recursive search enumerates all possible multiplicative partitions of `k`, and assigning larger exponents to smaller primes gives the minimum number for each partition. Since every valid construction is examined, the smallest recorded value is the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    k = int(input())

    if k == 1:
        print(1)
        return

    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    best = [10 ** 100]

    def dfs(rem, idx, max_factor, cur):
        if rem == 1:
            if cur < best[0]:
                best[0] = cur
            return

        if idx >= len(primes):
            return

        p = primes[idx]

        for factor in range(min(max_factor, rem), 1, -1):
            if rem % factor == 0:
                nxt = cur * (p ** (factor - 1))
                if nxt < best[0]:
                    dfs(rem // factor, idx + 1, factor, nxt)

    dfs(k, 0, k, 1)

    print(best[0] if best[0] != 10 ** 100 else -1)

if __name__ == "__main__":
    solve()
```

The prime list contains enough small primes because `k` is at most 1000. The maximum possible number of factors in a multiplicative partition is limited by repeatedly multiplying by `2`, so only a small number of primes can ever be needed.

The recursive function stores the remaining part of `k`, the index of the next prime, the largest allowed factor, and the number built so far. The `max_factor` argument prevents generating the same exponent set in different orders.

The loop tries factors from large to small. The order itself is not required for correctness, but it tends to find strong candidates early, which makes the pruning condition more effective. The pruning is safe because any continuation only multiplies `cur` by numbers greater than `1`, so a partial value already larger than the best answer cannot improve.

Python integers do not overflow, which avoids the main implementation risk in this problem. The search depth is also very small because the factor count of `k` cannot grow much.

## Worked Examples

For input `1`, the search does not need recursion.

| Input k | Action | Current answer |
| --- | --- | --- |
| 1 | Special case, one divisor only | 1 |

This confirms the minimum possible input and avoids the common mistake of assuming every answer must be greater than one.

For input `6`, the multiplicative partitions are explored.

| Remaining k | Chosen factor | Prime used | Current number |
| --- | --- | --- | --- |
| 6 | 3 | 2 | 4 |
| 2 | 2 | 3 | 12 |
| 1 | stop |  | 12 |
| 6 | 2 | 2 | 2 |
| 3 | 3 | 3 | 18 |
| 1 | stop |  | 18 |

The best value found is `12`. Its divisors are `1, 2, 3, 4, 6, 12`, giving exactly six possible company sizes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(P) | P is the number of multiplicative partitions of `k`, which is small for `k ≤ 1000` |
| Space | O(log k) | The recursion depth equals the number of prime factors used |

The algorithm never iterates through possible orange sizes. It only explores factorizations of the divisor count, so it easily fits the time and memory limits.

## Test Cases

```python
import sys
import io

def solution(inp):
    k = int(inp)

    if k == 1:
        return "1"

    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    best = [10 ** 100]

    def dfs(rem, idx, max_factor, cur):
        if rem == 1:
            best[0] = min(best[0], cur)
            return
        for factor in range(min(max_factor, rem), 1, -1):
            if rem % factor == 0:
                dfs(rem // factor, idx + 1, factor,
                    cur * primes[idx] ** (factor - 1))

    dfs(k, 0, k, 1)
    return str(best[0])

assert solution("1") == "1", "minimum input"
assert solution("4") == "6", "small composite divisor count"
assert solution("6") == "12", "sample-style case"
assert solution("12") == "60", "different exponent ordering"
assert solution("1000") == "810810000", "maximum input size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | Handles the only one-divisor number |
| 4 | 6 | Avoids incorrectly choosing only prime powers |
| 6 | 12 | Checks normal factor partitioning |
| 12 | 60 | Checks exponent ordering for minimum construction |
| 1000 | 810810000 | Confirms the search handles the maximum constraint |

## Edge Cases

For `k = 1`, the algorithm immediately returns `1` without entering the recursive search. The number `1` has only one divisor, itself, so the output is correct.

For `k = 4`, the recursive search can split the divisor count as `2 * 2`. This creates exponents `1` and `1`, giving the number `2 * 3 = 6`. The algorithm does not get trapped by the larger prime power `2^3 = 8`, because it evaluates all multiplicative partitions.

For `k = 12`, one possible split is `3 * 2 * 2`, producing exponents `2, 1, 1`. The algorithm assigns these to `2, 3, 5`, producing `60`. If the exponents were assigned in another order, the divisor count would still be correct but the value would be larger, which is why the decreasing factor restriction is necessary.
