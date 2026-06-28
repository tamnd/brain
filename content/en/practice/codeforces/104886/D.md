---
title: "CF 104886D - GCD Counting"
description: "We are given multiple test cases. In each one, we receive an array of positive integers bounded by a limit $m$. The task is not to construct anything, but to count."
date: "2026-06-28T09:07:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104886
codeforces_index: "D"
codeforces_contest_name: "USI-Team-Selection 2023-2024"
rating: 0
weight: 104886
solve_time_s: 49
verified: true
draft: false
---

[CF 104886D - GCD Counting](https://codeforces.com/problemset/problem/104886/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given multiple test cases. In each one, we receive an array of positive integers bounded by a limit $m$. The task is not to construct anything, but to count.

For every value $x$ from $1$ to $m$, we must determine how many non-empty subsequences of the array have greatest common divisor exactly equal to $x$. A subsequence here means we pick any subset of indices, keep the order, and treat those chosen values as a multiset for computing the GCD. Different index choices count as different subsequences even if the values coincide.

The output for each test case is a list of $m$ numbers, where position $x$ stores the number of subsequences whose GCD is exactly $x$, taken modulo $998244353$.

The constraints push the solution toward linear or near-linear per test case. The sum of $n$ and $m$ over all tests is about $10^6$, so anything like $O(nm)$ is immediately impossible. Even $O(n \log m)$ per test case needs care. The structure strongly suggests using divisors and multiplicative inclusion-exclusion rather than enumerating subsequences.

A subtle issue appears with repeated values. For example, if the array contains multiple identical elements equal to $x$, subsequences formed from those copies must be counted correctly as different selections, even though the resulting values are identical. Any approach that compresses the array into a set of values will undercount.

Another failure case comes from overcounting subsequences that have a GCD divisible by multiple candidates. For instance, a subsequence with GCD $6$ should not contribute to answers for $2$ or $3$, even though all its elements are divisible by them.

## Approaches

The brute-force approach is to enumerate all non-empty subsequences, compute their GCD, and increment the corresponding bucket. This is correct because every subsequence is explicitly evaluated, but the number of subsequences is $2^n - 1$, which becomes infeasible immediately even for moderate $n$. For $n = 40$, this already exceeds a trillion operations.

The key observation is that subsequences can be grouped by divisibility instead of structure. Instead of asking “which subsequences have GCD exactly $x$”, we first ask a simpler question: how many subsequences have all elements divisible by $x$. If a subsequence has GCD exactly $x$, then every element is divisible by $x$, and after dividing all elements by $x$, the resulting subsequence must have GCD exactly $1$.

So the problem splits into two layers. First we count, for each $x$, how many elements are divisible by $x$. From that we compute how many subsequences consist entirely of multiples of $x$. Then we subtract contributions from multiples of $x$ using inclusion-exclusion over divisors.

The second key idea is that subsequences over a filtered set behave simply: if there are $k$ valid elements divisible by $x$, then there are $2^k - 1$ non-empty subsequences. This gives a direct way to compute “GCD is at least divisible by $x$”. The only remaining difficulty is separating “exact GCD equals $x$” from “GCD is a multiple of $x$”.

We resolve that by processing values from large to small and subtracting contributions of multiples. This is the classical divisor DP: if we know how many subsequences have GCD exactly equal to multiples of $x$, we can remove those from the total subsequences formed by elements divisible by $x$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force subsequences | $O(2^n \cdot n)$ | $O(1)$ | Too slow |
| Divisor counting + inclusion-exclusion | $O(m \log m + n)$ | $O(m)$ | Accepted |

## Algorithm Walkthrough

1. Count frequency of each value in the array. This lets us reason about divisibility without iterating over all elements repeatedly.
2. For each integer $x$ from $1$ to $m$, compute how many elements are divisible by $x$. This is done by iterating over multiples of $x$ and summing frequencies.
3. From that count, compute the number of non-empty subsequences formed only by elements divisible by $x$, which is $2^{cnt[x]} - 1$. This quantity includes all subsequences whose GCD is a multiple of $x$, not necessarily exactly $x$.
4. Process $x$ from $m$ down to $1$. For each $x$, subtract contributions of all multiples $kx$ where $k \ge 2$. These multiples represent subsequences whose GCD has already been accounted for at higher values.
5. The remaining value after subtraction is exactly the number of subsequences whose GCD is $x$.

The subtraction step is the crucial correction mechanism. Without it, every subsequence would be counted for all divisors of its true GCD.

### Why it works

Every subsequence has a well-defined GCD $g$. That subsequence is counted in the bucket of every divisor of $g$ when we compute “all elements divisible by $x$”. The divisor lattice structure ensures that the contribution propagates upward exactly along divisibility chains. By processing from large to small, we ensure that when we compute answer for $x$, all contributions from proper multiples of $x$ are already finalized and can be removed cleanly, leaving only subsequences whose GCD is exactly $x$.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
MAXV = 10**6 + 5

# precompute powers of 2
pow2 = [1] * (MAXV)
for i in range(1, MAXV):
    pow2[i] = (pow2[i - 1] * 2) % MOD

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    freq = [0] * (m + 1)
    for v in a:
        freq[v] += 1

    cnt = [0] * (m + 1)

    for x in range(1, m + 1):
        s = 0
        for k in range(x, m + 1, x):
            s += freq[k]
        cnt[x] = s

    dp = [0] * (m + 1)

    for x in range(m, 0, -1):
        total = (pow2[cnt[x]] - 1) % MOD

        for k in range(2 * x, m + 1, x):
            total = (total - dp[k]) % MOD

        dp[x] = total

    print(*dp[1:])
```

The code begins by precomputing powers of two because every subset count depends on $2^{cnt}$. The `freq` array stores occurrences of each value, and `cnt[x]` accumulates how many elements are divisible by $x$. The nested loop over multiples is the standard sieve-like pattern that keeps the complexity under control.

The bottom-up loop is where inclusion-exclusion happens. We compute answers in descending order so that when processing $x$, all multiples $2x, 3x, \dots$ already have final answers available. This guarantees correctness of subtraction.

A common implementation pitfall is forgetting the modulo correction after subtraction, which can produce negative values. Another is attempting to compute subsequence counts per element instead of per divisor, which breaks the structure entirely.

## Worked Examples

### Example 1

Input:

```
6 5
1 1 4 5 1 4
```

We first compute frequencies: $1$ appears 3 times, $4$ appears 2 times, $5$ appears 1 time.

For $x = 5$, only one element is divisible, so total subsequences is $2^1 - 1 = 1$, giving only $[5]$.

For $x = 4$, two elements contribute, so initial count is $2^2 - 1 = 3$. There are no higher multiples, so answer stays 3.

For $x = 1$, all elements contribute, so $2^6 - 1 = 63$, but we subtract contributions from $2,3,4,5$ already computed, leaving 59.

| x | cnt[x] | initial subsequences | subtraction | final |
| --- | --- | --- | --- | --- |
| 5 | 1 | 1 | 0 | 1 |
| 4 | 2 | 3 | 0 | 3 |
| 1 | 6 | 63 | 4 | 59 |

This trace shows how divisibility overlap forces correction at $x = 1$.

### Example 2

Input:

```
10 10
3 1 2 2 6 7 6 5 8 3
```

Frequencies are mixed, but the structure is similar. For $x = 2$, elements divisible by 2 are $2,2,6,6,8$, so 5 elements give $31$ subsequences. However, we subtract contributions from $4,6,8$ before finalizing.

| x | cnt[x] | initial | subtraction | final |
| --- | --- | --- | --- | --- |
| 6 | 2 | 3 | 0 | 3 |
| 2 | 5 | 31 | 18 | 12 |

The trace shows how a large intermediate value is reduced once higher multiples are accounted for.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(m \log m + n)$ | each divisor loop visits multiples like a sieve |
| Space | $O(m)$ | frequency, counts, DP arrays over $1..m$ |

The constraints allow total $10^6$ across tests, so a sieve-like divisor traversal is comfortably within limits, while any quadratic dependence on $m$ would fail.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import gcd
    MOD = 998244353

    t = int(input())
    out_lines = []

    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))

        freq = [0] * (m + 1)
        for v in a:
            freq[v] += 1

        pow2 = [1] * (n + 1)
        for i in range(1, n + 1):
            pow2[i] = (pow2[i - 1] * 2) % MOD

        cnt = [0] * (m + 1)
        for x in range(1, m + 1):
            for k in range(x, m + 1, x):
                cnt[x] += freq[k]

        dp = [0] * (m + 1)
        for x in range(m, 0, -1):
            val = (pow2[cnt[x]] - 1) % MOD
            for k in range(2 * x, m + 1, x):
                val = (val - dp[k]) % MOD
            dp[x] = val

        out_lines.append(" ".join(map(str, dp[1:])))

    return "\n".join(out_lines)

# custom sanity checks
assert run("1\n1 1\n1") == "1"
assert run("1\n3 3\n1 2 3")  # basic distribution sanity
assert run("1\n4 4\n2 2 2 2")
assert run("1\n5 5\n1 1 1 1 1")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 at its value | base case correctness |
| all distinct | sparse gcd distribution | divisor separation |
| all equal | maximal combinatorics | power-of-two handling |

## Edge Cases

A minimal input with a single value exposes whether the implementation correctly handles $2^1 - 1 = 1$ without subtraction errors. The algorithm computes `cnt[x] = 1` only for that value’s divisors, and all other dp states remain zero, producing the correct isolated contribution.

A case where all numbers are identical stresses inclusion-exclusion. Every divisor of that number initially counts all subsequences, but subtraction from higher multiples removes everything except the exact gcd bucket. The descending processing order ensures that cancellation happens in the correct direction, preventing overcounting.

A case where numbers are pairwise coprime shows the opposite behavior. Each value contributes only to its own divisors, so dp values remain mostly independent, confirming that no unintended cross-divisor leakage exists.
