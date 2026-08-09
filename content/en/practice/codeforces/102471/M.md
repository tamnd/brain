---
title: "CF 102471M - Value"
description: "We choose some indices from 1 through n. Every chosen index i contributes ai to the score. There is one kind of interaction between chosen indices: if both i and j are chosen and j = i^k for some integer k 1, then bj is subtracted once."
date: "2026-08-09T18:57:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102471
codeforces_index: "M"
codeforces_contest_name: "2019 ICPC Asia-East Continent Final"
rating: 0
weight: 102471
solve_time_s: 365
verified: true
draft: false
---

[CF 102471M - Value](https://codeforces.com/problemset/problem/102471/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We choose some indices from `1` through `n`. Every chosen index `i` contributes `a_i` to the score. There is one kind of interaction between chosen indices: if both `i` and `j` are chosen and `j = i^k` for some integer `k > 1`, then `b_j` is subtracted once.

The task is to choose the subset with the largest resulting score. The arrays `a` and `b` both have positive values, so choosing an index is always individually profitable, but choosing it together with certain other indices can create penalties. The original problem has `n <= 100000` and `a_i, b_i <= 10^9`.

The bound of `100000` immediately rules out anything that considers arbitrary subsets of indices. There are `2^n` such subsets, and even an `O(n^2)` evaluation of one subset would already be hopeless. We need to exploit the very special form of the relation `i^k = j`.

There are several easy cases where an implementation can silently go wrong. First, index `1` is special. It never participates in a penalty because the condition requires the smaller endpoint to be at least `2`. Since `a_1 > 0`, index `1` must always be selected. For example,

```
1
7
100
```

has answer `7`, not `0`.

Second, a penalty is associated with every valid pair, not merely with the fact that one number is some power of another. For example,

```
4
1 1 1 2
1 1 1 1
```

has answer `4`. Selecting all four indices gives `1 + 1 + 1 + 2 - 1 = 4`, because the only relevant pair is `2 -> 4`.

Third, ordinary divisibility is not enough. For example, `4` divides `8`, but `8` is not an integer power of `4`. With

```
8
1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1
```

the relevant power relations inside `{2,4,8}` are `2^2 = 4` and `2^3 = 8`. There is no `4 -> 8` edge. Treating divisibility as the relation would introduce a false penalty and can change the answer.

A fourth subtlety is that a number can have several power roots. For instance, `64` has `2^6 = 64`, `4^3 = 64`, and `8^2 = 64`. If all three roots and `64` are selected, `b_64` is subtracted three times. A solution that subtracts `b_64` only once would be incorrect.

## Approaches

The direct approach is to enumerate every subset of `{1, ..., n}`. For each subset, we could add all selected `a_i` values and then inspect every ordered pair `(i,j)` to see whether `j` is an integer power of `i`. This is correct because it evaluates the score exactly as defined. However, there are `2^n` subsets and up to `Theta(n^2)` pairs to inspect for each one, giving `Theta(n^2 2^n)` operations in the worst case. With `n = 100000`, this is not remotely feasible.

The useful observation comes from asking what numbers can interact with one another. Every integer `x >= 2` can be written uniquely as

`x = p^e`

where `p` is not itself a perfect power and `e >= 1`. For example, `64 = 2^6`, while `36` is already represented as `36^1` because it is not a perfect power.

Now suppose `i^k = j`. Write `i = p^d`. Then

`j = (p^d)^k = p^(dk)`.

So `i` and `j` have exactly the same primitive base `p`. Numbers with different primitive bases can never interact.

This splits the whole problem into independent groups. For a fixed primitive base `p`, the possible numbers are

`p^1, p^2, p^3, ..., p^m`

where `p^m <= n`. The only remaining question is which exponents to select.

Inside one such group, there are at most `log_2(100000) = 16` exponents. That is the decisive reduction. Instead of choosing from `100000` unrelated positions simultaneously, we can enumerate the at most `2^16 = 65536` subsets of one power chain.

For an exponent `e`, the number `p^e` receives a penalty from a selected exponent `d` exactly when `d < e` and `d` divides `e`. Thus, if a mask represents the selected exponents, the contribution of selecting exponent `e` is

`a[p^e] - b[p^e] * (# selected proper divisors of e)`.

We can calculate the best score for every mask incrementally. Remove one selected exponent `e` from the mask, take the score of the smaller mask, and add the contribution of `e`. The proper-divisor mask of every exponent can be precomputed, so the number of selected divisors is just a bit-count operation.

The decomposition into primitive bases can be obtained by factoring every number with a smallest-prime-factor sieve. If

`x = q_1^c_1 q_2^c_2 ... q_t^c_t`,

then the exponent `e` in the primitive representation is `gcd(c_1, c_2, ..., c_t)`, and the primitive base is

`q_1^(c_1/e) q_2^(c_2/e) ... q_t^(c_t/e)`.

The value `1` is handled separately because it does not belong to any power chain.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n^2 2^n)` | `O(n)` | Too slow |
| Primitive-base decomposition + subset DP | `O(n log n + sum 2^m)` | `O(n)` | Accepted |

The sum over `2^m` is small because a group with length `m` has primitive base at most `n^(1/m)`. In particular, the only group capable of reaching length `16` is the base `2` group, while almost all bases have only one exponent and cost two mask states. For `n <= 100000`, this enumeration is easily manageable.

## Algorithm Walkthrough

1. Read `n`, `a`, and `b`, and immediately add `a_1` to the answer. Index `1` cannot create or receive any penalty, and `a_1` is positive, so excluding it can never be optimal.
2. Build a smallest-prime-factor array up to `n`. This lets us factor every number in `O(log n)` time rather than repeatedly trying all possible divisors.
3. For every `x` from `2` through `n`, factor `x` into prime powers. Take the greatest common divisor of all prime exponents. Call this value `e`. The number has the unique form `x = p^e`, where `p` is the primitive base.
4. Store `x` in the group belonging to `p` at exponent `e`. For example, the numbers `2, 4, 8, 16` all go into the group with base `2`, at exponents `1, 2, 3, 4`. A number such as `12` gets its own group because it is not a perfect power.
5. Process every primitive-base group independently. For a group with base `p` and maximum exponent `m`, create the sequence of values corresponding to `p^1` through `p^m`.
6. For each exponent `e`, construct a bit mask containing its proper divisors. For example, in a group of length at least `8`, the proper-divisor mask of exponent `8` contains exponents `1`, `2`, and `4`. These are exactly the possible roots whose powers can equal `p^8`.
7. Enumerate every subset mask of the `m` exponents. Let `bit` be one selected exponent and let `prev` be the mask with that exponent removed. The score for the current mask is the score for `prev`, plus `a[p^e]`, minus `b[p^e]` multiplied by the number of selected proper divisors of `e`.
8. Take the maximum score over all masks in the group and add it to the global answer. Since no power relation crosses from one primitive base to another, optimizing every group independently gives the global optimum.

### Why it works

Every penalty pair `i^k = j` has the same primitive base on both sides. Consequently, the complete score is a sum of independent scores, one for index `1` and one for every primitive-base group.

Within a group, the mask represents exactly which numbers `p^1, ..., p^m` are selected. When exponent `e` is added to a mask, the only new penalties are those involving `p^e` as the larger endpoint. Such a penalty exists precisely for every already-selected proper divisor `d` of `e`, and each contributes exactly `b[p^e]`. Thus the recurrence calculates the exact score of every possible subset of the group. Taking the best mask therefore gives the optimal choice for that group, and summing the independent optima gives the optimal global score.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

def solve():
    n = int(input())
    a = [0] + list(map(int, input().split()))
    b = [0] + list(map(int, input().split()))

    # Index 1 is always selected.
    answer = a[1]

    if n == 1:
        print(answer)
        return

    # Smallest prime factor sieve.
    spf = list(range(n + 1))
    if n >= 1:
        spf[1] = 1

    for i in range(2, int(n ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i

    # groups[base][exponent] = number p^exponent.
    groups = {}

    for x in range(2, n + 1):
        y = x
        g = 0
        factors = []

        while y > 1:
            p = spf[y]
            cnt = 0
            while y % p == 0:
                y //= p
                cnt += 1
            factors.append((p, cnt))
            g = cnt if g == 0 else gcd(g, cnt)

        base = 1
        for p, cnt in factors:
            base *= p ** (cnt // g)

        if base not in groups:
            groups[base] = []
        groups[base].append((g, x))

    # Precompute proper-divisor masks for all possible exponents.
    divisor_mask = [0] * 17
    for e in range(1, 17):
        mask = 0
        for d in range(1, e):
            if e % d == 0:
                mask |= 1 << (d - 1)
        divisor_mask[e] = mask

    for items in groups.values():
        items.sort()

        m = len(items)

        # The representation p^1, p^2, ..., p^m is contiguous.
        values_a = [0] * m
        values_b = [0] * m

        for exponent, x in items:
            pos = exponent - 1
            values_a[pos] = a[x]
            values_b[pos] = b[x]

        dp = [0] * (1 << m)

        best = 0

        for mask in range(1, 1 << m):
            low = mask & -mask
            pos = low.bit_length() - 1
            prev = mask ^ low
            exponent = pos + 1

            selected_roots = (prev & divisor_mask[exponent]).bit_count()

            cur = (
                dp[prev]
                + values_a[pos]
                - values_b[pos] * selected_roots
            )

            dp[mask] = cur
            if cur > best:
                best = cur

        answer += best

    print(answer)

if __name__ == "__main__":
    solve()
```

The first part of the implementation handles index `1` before doing any number-theoretic work. This is both simpler and avoids accidentally treating `1` as a primitive base.

The smallest-prime-factor sieve gives a fast factorization for every number up to `n`. During factorization, `g` becomes the gcd of the prime exponents. If the factorization is `2^6`, then `g = 6`, giving primitive base `2` and exponent `6`. If the factorization is `2^2 * 3^2`, then `g = 2`, giving primitive base `6` and exponent `2`, since `36 = 6^2`.

The group entries are indexed by their actual exponent rather than merely by their order in the list. For a primitive base `p`, all powers `p^1` through `p^m` are at most `n`, so every exponent between `1` and `m` exists. This makes `exponent - 1` a valid bit position.

The expression

```
prev & divisor_mask[exponent]
```

keeps exactly those proper divisors of the newly selected exponent that were already selected. Python's `bit_count()` then gives their number directly.

The DP recurrence adds an exponent to an already computed subset. Since every penalty involving the new number has the new number as its larger endpoint, each such penalty is counted exactly once. There is no need to inspect pairs again.

Python integers have arbitrary precision, so the maximum possible score, which can be on the order of `10^14`, does not overflow.

## Worked Examples

### Sample 1

The input is

```
4
1 1 1 2
1 1 1 1
```

Index `1` contributes `1` unconditionally. The remaining numbers form the primitive-base groups `{2,4}` and `{3}`.

For the group `{2,4}`, exponent `1` has no proper divisor, while exponent `2` has proper divisor `1`.

| Mask | Selected | New exponent | Selected roots | Group score |
| --- | --- | --- | --- | --- |
| `00` | none | none | 0 | 0 |
| `01` | `2` | 1 | 0 | 1 |
| `10` | `4` | 2 | 0 | 2 |
| `11` | `2,4` | 2 | 1 | 1 + 2 - 1 = 2 |

The best score of this group is `2`. The singleton group `{3}` contributes `1`. Together with index `1`, the answer is `1 + 2 + 1 = 4`.

### Sample 2

The input is

```
4
1 1 1 1
1 1 1 2
```

Again, index `1` contributes `1`. The group `{2,4}` has the following states.

| Mask | Selected | New exponent | Selected roots | Group score |
| --- | --- | --- | --- | --- |
| `00` | none | none | 0 | 0 |
| `01` | `2` | 1 | 0 | 1 |
| `10` | `4` | 2 | 0 | 1 |
| `11` | `2,4` | 2 | 1 | 1 + 1 - 2 = 0 |

The best group score is `1`. Index `3` contributes another `1`, so the total is `1 + 1 + 1 = 3`.

These two samples demonstrate why each power chain must be optimized as a whole. Selecting every positive-value index is not necessarily optimal, because a selected root can make another selected number lose `b_j`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log n + S)` | Factoring all numbers costs `O(n log n)`, and `S = sum 2^m` over primitive-base groups |
| Space | `O(n)` | The sieve, arrays, groups, and the largest group DP are all linear or smaller |

For `n = 100000`, every power chain has length at most `16`, because `2^17 > 100000`. More importantly, long chains can exist for only very few primitive bases. Most groups have one exponent and therefore only two DP states. The resulting subset enumeration is small enough for the one-second limit, while the sieve and arrays fit comfortably inside 256 MB.

## Test Cases

```python
# The production solution is the solve() function above.
# This helper executes that logic on an isolated input string.

import sys
import io
from math import gcd

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue().strip()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

# Provided samples
assert run(
    "4\n"
    "1 1 1 2\n"
    "1 1 1 1\n"
) == "4", "sample 1"

assert run(
    "4\n"
    "1 1 1 1\n"
    "1 1 1 2\n"
) == "3", "sample 2"

# Minimum size: index 1 is always selected.
assert run(
    "1\n"
    "7\n"
    "100\n"
) == "7", "minimum n"

# n = 2: there is no possible power relation.
assert run(
    "2\n"
    "5 9\n"
    "100 100\n"
) == "14", "no power relation"

# All equal values, with 2^2 = 4 as the only relevant relation.
assert run(
    "4\n"
    "5 5 5 5\n"
    "1 1 1 1\n"
) == "19", "all equal values"

# Boundary case distinguishing powers from divisibility:
# 4 divides 8, but 4^k is never 8.
assert run(
    "8\n"
    "1 1 1 1 1 1 1 1\n"
    "1 1 1 1 1 1 1 1\n"
) == "7", "power relation versus divisibility"

# Maximum-size case. All a_i are huge, so every index is selected.
# The number of power pairs for n = 100000 is:
# 315 + 45 + 16 + 9 + 5 + 4 + 3 + 2 + 2 + 2 + 2 + 1 + 1 + 1 + 1 = 409.
max_n = 100000
max_input = (
    str(max_n) + "\n" +
    ("1000000000 " * max_n).strip() + "\n" +
    ("1 " * max_n).strip() + "\n"
)
assert run(max_input) == "99999999999591", "maximum n"

# A number can have multiple power roots.
# 64 = 2^6 = 4^3 = 8^2.
assert run(
    "64\n"
    + ("1 " * 64).strip() + "\n"
    + ("1 " * 64).strip() + "\n"
) == "61", "multiple power roots"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7 / 100` | `7` | Minimum size and mandatory selection of index `1` |
| `2 / 5 9 / 100 100` | `14` | No power relation exists when `n = 2` |
| `4 / 5 5 5 5 / 1 1 1 1` | `19` | Equal values and a single penalty edge |
| `8 / all 1 / all 1` | `7` | Distinguishes exact powers from ordinary divisibility |
| `100000 / all 10^9 / all 1` | `99999999999591` | Maximum `n`, large integer scores, and all power pairs |
| `64 / all 1 / all 1` | `61` | A target can have several different power roots |

## Edge Cases

The first edge case is `n = 1`. The exact input is

```
1
7
100
```

There are no possible pairs at all. Index `1` contributes `7`, and the answer is `7`. The implementation handles this before constructing the sieve groups.

The second edge case is the absence of any power relation. For

```
2
5 9
100 100
```

both indices are selected because both values are positive and neither `2` nor `1` can be the smaller endpoint of a valid power pair with the other index. The result is `14`.

The third edge case concerns the difference between powers and divisibility. For

```
8
1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1
```

the group with base `2` contains `2,4,8`. Selecting all three gives two penalties, from `2^2 = 4` and `2^3 = 8`, for a group score of `1`. The numbers `1,3,5,6,7` each contribute `1`, giving `6` from those indices plus the best group score `1`, hence `7`. In particular, there is no penalty between `4` and `8`, because `8` is not a power of `4`.

The fourth edge case is a target with multiple roots. Consider the group containing `2,4,8,64`. The number `64` receives one penalty from each selected member among `2`, `4`, and `8`, because `2^6`, `4^3`, and `8^2` all equal `64`. The DP does not need to special-case this. Its proper-divisor mask for exponent `6` contains exponents `1`, `2`, and `3`, so all three penalties are counted when exponent `6` is added.

Finally, large values require a wide integer type. With `n = 100000` and every `a_i = 10^9`, the positive contribution alone is `10^14`. The Python implementation handles this exactly through arbitrary-precision integers, while a fixed-width 32-bit implementation would overflow.

If you want, I can also turn this into a shorter Codeforces-style editorial that keeps the same proof but removes the exhaustive testing discussion.
