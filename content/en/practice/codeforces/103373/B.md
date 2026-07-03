---
title: "CF 103373B - Aliquot Sum"
description: "We are given many positive integers, and for each one we must decide how “rich” its proper divisors are. For a number $n$, we consider all its divisors except $n$ itself, sum them up, and compare that sum against $n$."
date: "2026-07-03T12:36:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103373
codeforces_index: "B"
codeforces_contest_name: "2021 ICPC Asia Taiwan Online Programming Contest"
rating: 0
weight: 103373
solve_time_s: 47
verified: true
draft: false
---

[CF 103373B - Aliquot Sum](https://codeforces.com/problemset/problem/103373/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given many positive integers, and for each one we must decide how “rich” its proper divisors are. For a number $n$, we consider all its divisors except $n$ itself, sum them up, and compare that sum against $n$. If the sum is larger, the number is called abundant, if smaller it is deficient, and if equal it is perfect.

The input is essentially a large batch of queries. Each query is an integer up to one million, and there can be up to one million such queries. The output is a classification string per number, so the key challenge is not computing a single divisor sum, but doing it extremely fast across many repeated queries.

The constraints immediately rule out recomputing divisors from scratch per query. A naive divisor scan up to $n$ would already be too slow for one query in the worst case, and multiplied by $10^6$ queries it becomes impossible. Even scanning up to $\sqrt{n}$ per query is still too heavy at this scale.

A subtle edge case comes from perfect numbers where the sum equals the number exactly. For example, 6, 28, 496. A careless implementation that forgets to exclude the number itself will always classify numbers as “abundant” incorrectly, since the full divisor sum always includes $n$.

Another edge case is repeated queries. Since inputs can contain the same number many times, recomputing its divisor sum each time is wasted work and will likely TLE.

## Approaches

The brute-force idea is straightforward: for each number $n$, iterate from 1 to $n-1$, check divisibility, and accumulate the sum of divisors. This is correct because it directly follows the definition of the aliquot sum. However, each query costs $O(n)$, and with $n$ up to $10^6$ and $10^6$ queries, the total operation count degenerates to $10^{12}$, which is far beyond feasible limits.

A standard improvement is to only check divisors up to $\sqrt{n}$, adding both $d$ and $n/d$ when $d$ divides $n$. This reduces a single query to $O(\sqrt{n})$, but with $10^6$ queries this is still on the order of $10^9$ operations, which is borderline and unsafe in Python.

The key observation is that the value range is small and fixed: all numbers lie between 1 and $10^6$. Instead of recomputing divisor sums per query, we can precompute the sum of proper divisors for every number in this range once using a sieve-like accumulation. Each integer $d$ contributes to all multiples of $d$, so we can iterate over divisors and propagate contributions efficiently. This transforms the problem into a classic divisor-sum sieve, reducing repeated computation entirely.

Once the precomputation is done, each query becomes a simple array lookup and comparison.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(T \cdot n)$ | $O(1)$ | Too slow |
| Square-root per query | $O(T \sqrt{n})$ | $O(1)$ | Too slow |
| Sieve precomputation | $O(N \log N)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

We want the sum of proper divisors for every number up to $10^6$. Instead of processing each number independently, we invert the viewpoint and let each possible divisor “contribute forward”.

1. Create an array `s` of size $N+1$, initialized to zero, where `s[x]` will store the sum of proper divisors of $x$. We do not include $x$ itself in its own sum, so we ensure we never add a number to its own index.
2. For every integer $d$ from 1 to $N/2$, we iterate over all multiples $m = 2d, 3d, 4d, \dots$. For each such multiple $m$, we add $d$ into `s[m]`. This works because $d$ is a proper divisor of every multiple strictly larger than itself.
3. After this process, `s[n]` contains exactly the sum of all proper divisors of $n$, because every divisor $d < n$ contributes exactly once to its multiples.
4. For each query $n_i$, we compare `s[n_i]` with $n_i$. If `s[n_i] > n_i`, we output abundant. If `s[n_i] < n_i`, we output deficient. Otherwise we output perfect.

Why it works comes down to a clean counting invariant. Every pair $(d, m)$ where $d$ divides $m$ and $d < m$ is added exactly once when we process $d$. There is no duplication because each divisor is responsible for all of its multiples independently, and no divisor ever contributes to a number larger than the range boundary in a way that breaks correctness. As a result, each number accumulates exactly the sum of its proper divisors and nothing else.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXN = 10**6

# precompute sum of proper divisors
s = [0] * (MAXN + 1)

for d in range(1, MAXN // 2 + 1):
    for m in range(2 * d, MAXN + 1, d):
        s[m] += d

t = int(input())
nums = list(map(int, input().split()))

out = []
for x in nums:
    if s[x] > x:
        out.append("abundant")
    elif s[x] < x:
        out.append("deficient")
    else:
        out.append("perfect")

sys.stdout.write("\n".join(out))
```

The core implementation detail is the sieve loop. The outer loop chooses a divisor candidate, and the inner loop distributes it to all multiples. Starting the inner loop at `2*d` is crucial because we explicitly exclude the number itself from its own divisor sum.

Another subtle point is that we precompute once up to $10^6$ regardless of input size. This ensures the expensive work is amortized, and each query becomes constant time.

The comparison step is direct since `s[x]` already excludes `x` itself by construction.

## Worked Examples

We use the sample values 12, 21, and 28.

For 12, its proper divisors are 1, 2, 3, 4, 6. The precomputation builds `s[12] = 16`. For 21, divisors are 1, 3, 7 giving `s[21] = 11`. For 28, divisors are 1, 2, 4, 7, 14 giving `s[28] = 28`.

| Number | Proper divisors accumulated | s(n) | Comparison |
| --- | --- | --- | --- |
| 12 | 1, 2, 3, 4, 6 | 16 | 16 > 12 |
| 21 | 1, 3, 7 | 11 | 11 < 21 |
| 28 | 1, 2, 4, 7, 14 | 28 | 28 = 28 |

This trace confirms that the sieve correctly accumulates divisor contributions and that classification depends only on a final constant-time comparison.

A second small example is 6. During preprocessing, contributions come from 1, 2, and 3, producing `s[6] = 6`, which correctly places it in the perfect category. This validates that the algorithm handles symmetric divisor structures correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log N + T)$ | Each integer distributes contributions to its multiples, and harmonic series bounds the total operations; queries are O(1) each |
| Space | $O(N)$ | We store divisor sums for all integers up to $10^6$ |

The preprocessing cost is well within limits for $N = 10^6$, and after that each of the up to $10^6$ queries is just a comparison. This comfortably fits both time and memory constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    MAXN = 10**6
    s = [0] * (MAXN + 1)

    for d in range(1, MAXN // 2 + 1):
        for m in range(2 * d, MAXN + 1, d):
            s[m] += d

    t = int(input())
    nums = list(map(int, input().split()))

    res = []
    for x in nums:
        if s[x] > x:
            res.append("abundant")
        elif s[x] < x:
            res.append("deficient")
        else:
            res.append("perfect")

    return "\n".join(res)

# provided sample
assert run("3\n12 21 28") == "abundant\ndeficient\nperfect"

# minimum case
assert run("1\n1") == "deficient"

# perfect number check
assert run("2\n6 28") == "perfect\nperfect"

# abundant small case
assert run("1\n12") == "abundant"

# mixed case
assert run("5\n2 3 4 5 6") == "deficient\ndeficient\ndeficient\ndeficient\nperfect"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | deficient | smallest boundary case |
| 6, 28 | perfect | known perfect numbers |
| 12 | abundant | smallest abundant example |
| 2,3,4,5,6 | mixed | classification correctness |

## Edge Cases

For the input `1`, the sieve gives `s[1] = 0` because 1 has no proper divisors. The algorithm compares 0 < 1 and correctly outputs deficient. This catches the boundary case where the divisor set is empty.

For `6`, preprocessing adds contributions from 1, 2, and 3, giving `s[6] = 6`. The equality check triggers perfect, confirming that we never accidentally include 6 itself in its own sum.

For `28`, contributions from 1, 2, 4, 7, and 14 accumulate exactly to 28. Since each divisor is processed independently, there is no double counting, and the algorithm reliably classifies it as perfect.
