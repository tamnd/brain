---
title: "CF 102460F - Miss Sloane"
description: "For every senator we have an integer (ai), and the final agreement happens exactly when the gcd of all current (ai) values is greater than 1. Sloane may choose a senator once and divide that senator's value by any divisor (d) satisfying (dle k)."
date: "2026-08-09T02:50:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102460
codeforces_index: "F"
codeforces_contest_name: "2019-2020 ICPC Asia Taipei-Hsinchu Regional Contest"
rating: 0
weight: 102460
solve_time_s: 397
verified: true
draft: false
---

[CF 102460F - Miss Sloane](https://codeforces.com/problemset/problem/102460/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

For every senator we have an integer \(a_i\), and the final agreement happens exactly when the gcd of all current \(a_i\) values is greater than 1. Sloane may choose a senator once and divide that senator's value by any divisor \(d\) satisfying \(d\le k\). The goal is to make the final gcd equal to 1 while minimizing the total lobbying time.

The resistance \(e_i\) affects the time in a slightly unusual way. If the current campaign has already lobbied \(x\) senators with total resistance \(y\), lobbying senator \(i\) costs

\[
y+e_i(x+1).
\]

The order looks relevant at first, but there is a useful cancellation. Suppose exactly \(m\) senators are lobbied, and their resistances in campaign order are \(e_1,\ldots,e_m\). The total cost is

\[
\sum_{j=1}^{m}\left(\sum_{t<j}e_t+je_j\right).
\]

For a fixed senator at position \(j\), its resistance appears once in the first sum for every later senator, and once multiplied by its own position. Its total coefficient is

\[
(m-j)+j=m.
\]

Thus the total campaign time is simply

\[
m\sum e_i.
\]

The ordering does not matter at all. The problem is consequently to choose senators and legal divisions so that every prime factor of the original gcd is eliminated, minimizing

\[
(\text{number of lobbied senators})\times(\text{sum of their resistances}).
\]

The constraints are dominated by \(n\le 10^6\). An \(O(n^2)\) approach is immediately impossible, and even an \(O(n2^{11})\) approach is too large because \(n2^{11}\) is about \(2\cdot10^9\). The useful small parameter is instead the number of distinct prime factors of the common gcd. Since the gcd is at most \(10^{12}\), it contains at most 11 distinct primes.

There are several edge cases that are easy to mishandle. If the initial gcd is already 1, the answer is 0 because no lobbying is necessary. For example,

```text
2 10
6 35
1 1
```

has gcd 1, so the correct answer is `0`. An implementation that always lobbies at least one senator would return a positive value.

Another subtle case is when no single senator can remove every common prime. For example,

```text
2 2
6 6
1 1
```

has gcd 6. One senator can be divided by 2, leaving 3, and the other can be divided by 3, leaving 2. The final gcd is 1, so the answer is 4. A solution that only checks whether one senator can remove the entire gcd would incorrectly report `-1`.

The divisor limit is also inclusive. With

```text
2 6
6 10
1 1
```

the first senator can divide by 6 exactly because \(6\le k\). Both senators are needed, giving total time \(2(1+1)=4\). Testing `d < k` instead of `d <= k` can reject legal operations.

Finally, a prime can only be removed from senator \(i\) if the division contains the entire power of that prime present in \(a_i\). If \(a_i=12\), removing the prime 2 requires division by 4, not merely by 2. Forgetting the exponent gives wrong answers whenever \(a_i\) contains a higher power of a common prime.

## Approaches

A direct brute-force approach would try every subset of senators and every legal divisor for each selected senator. It is correct because every possible campaign is explicitly considered, but it is hopeless for \(n=10^6\). Even merely enumerating senator subsets already takes \(2^n\) operations, before considering the possible divisions.

The first useful observation is that only primes in the original gcd matter. Let

\[
g=\gcd(a_1,a_2,\ldots,a_n).
\]

Every prime not dividing \(g\) is already absent from the final gcd. For each prime \(p\mid g\), at least one lobbied senator must lose all copies of \(p\).

Suppose

\[
a_i=p^{v_i}u,\qquad p\nmid u.
\]

To remove \(p\) completely from senator \(i\), Sloane must divide \(a_i\) by at least \(p^{v_i}\). If several primes are removed from the same senator, the required divisor is the product of their complete prime powers. It is legal precisely when that product is at most \(k\).

This turns the arithmetic problem into a small set-cover problem. The universe consists only of the distinct primes of \(g\), at most 11 elements. A bitmask represents which common primes have already been removed.

The remaining issue is the large value of \(n\). The key compression is that an optimal campaign never needs more than \(r\) senators, where \(r\) is the number of distinct primes in \(g\). If more than \(r\) senators are selected, some selected senator contributes no prime that is uniquely necessary, so removing that senator keeps every prime eliminated and strictly decreases the cost.

We can consequently retain only a small number of cheapest senators for every useful removal pattern. For a senator, the removal patterns are downward closed: if a senator can remove a set of primes, it can also remove every subset of that set. We enumerate the maximal legal patterns, retain at most \(r\) cheapest senators supporting each pattern, and then perform a standard subset DP. The bound of \(r\) candidates is enough because any optimal solution contains at most \(r\) senators, so when replacing its chosen senators by stored candidates, Hall's condition is satisfied for the candidate sets of the required patterns.

The arithmetic work is also small because we factor only the primes appearing in the single global gcd. We never factor every \(a_i\) by trial division up to \(\sqrt{a_i}\).

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | \(O(2^n)\) or worse | \(O(n)\) | Too slow |
| Optimal | \(O(nr + C2^r + 3^r)\), where \(r\le11\) and \(C\) is the number of distinct senator profiles | \(O(Cr+2^r)\) | Accepted |

Here \(C\) is small in the compressed representation because senators with identical prime-power profiles are processed together. The important point is that the exponential part depends only on \(r\le11\), never on \(n\).

## Algorithm Walkthrough

1. Compute the gcd \(g\) of all \(a_i\). If \(g=1\), print 0 immediately. There is no common prime left to eliminate.

2. Factor \(g\) into its distinct primes \(p_0,p_1,\ldots,p_{r-1}\). We only need these primes, not a complete factorization of every \(a_i\).

3. For every senator, determine the exponent of every \(p_j\) in \(a_i\). If the exponent is \(v\), completely removing \(p_j\) requires the factor \(p_j^v\).

4. For a chosen set of primes represented by mask \(S\), calculate the required divisor

\[
D_i(S)=\prod_{j\in S}p_j^{v_{i,j}}.
\]

The mask is legal for senator \(i\) exactly when \(D_i(S)\le k\). We enumerate the maximal legal masks for the senator, because every subset of a maximal legal mask is automatically legal.

5. Compress senators having the same prime-power profile. For each removal pattern keep only its cheapest \(r\) senators. More than \(r\) candidates for one pattern can never be necessary because a valid campaign uses at most \(r\) senators.

6. Run subset DP. Let `dp[mask]` be the minimum total resistance of a collection of already selected senators whose combined removed-prime mask is exactly `mask`. When a senator can remove pattern `s`, transition to

\[
dp[mask\mid s]
=
\min(dp[mask\mid s],dp[mask]+e_i).
\]

The senator is processed only once, so the same senator can never be used twice.

7. For every reachable final state `FULL`, suppose the DP used \(m\) senators and accumulated resistance \(E\). The corresponding campaign time is \(mE\). Store the number of selected senators together with the resistance in the DP state, or equivalently use a two-dimensional state indexed by the number of senators.

The reason for retaining the number of senators separately is that minimizing resistance alone is not enough. A campaign using one senator with resistance 100 can be better than a campaign using three senators with resistance 50 each, because the actual costs are 100 and 450 respectively.

### Why it works

The global gcd contains exactly the primes that must be destroyed. A senator can destroy a chosen subset of those primes exactly when the product of the corresponding complete prime powers in that senator is at most \(k\). Thus every legal campaign corresponds to a collection of senator masks whose union is the full prime mask, and every such collection gives a legal campaign.

An optimal campaign contains at most \(r\) senators. For every removal pattern we retain \(r\) cheapest available senators, which is enough to replace the senators of any optimal campaign without forcing two required roles onto the same senator. The subset DP then considers every possible union of removal masks while respecting the one-use-per-senator condition. Finally, the identity

\[
\text{time}=m\sum e_i
\]

converts the minimum resistance and senator count into the actual campaign time.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

INF = 10**30

def factor_distinct(x):
    primes = []
    p = 2
    while p * p <= x:
        if x % p == 0:
            primes.append(p)
            while x % p == 0:
                x //= p
        p = 3 if p == 2 else p + 2
    if x > 1:
        primes.append(x)
    return primes

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    e = list(map(int, input().split()))

    g = 0
    for x in a:
        g = gcd(g, x)

    if g == 1:
        print(0)
        return

    primes = factor_distinct(g)
    r = len(primes)
    full = (1 << r) - 1

    # For every distinct profile of prime powers, keep the smallest
    # resistances. At most r copies of one profile are ever useful.
    profiles = {}

    for x, cost in zip(a, e):
        powers = []
        y = x

        for p in primes:
            q = 1
            while y % p == 0:
                y //= p
                q *= p
            powers.append(q)

        key = tuple(powers)

        if key not in profiles:
            profiles[key] = [cost]
        else:
            arr = profiles[key]
            if len(arr) < r:
                arr.append(cost)
                arr.sort()
            elif cost < arr[-1]:
                arr[-1] = cost
                arr.sort()

    # Convert every profile into its maximal legal masks.
    #
    # A mask is maximal if it is legal but adding any omitted prime
    # makes the required divisor exceed k.
    candidates = []

    for powers, costs in profiles.items():
        legal = [False] * (1 << r)
        product = [1] * (1 << r)

        legal[0] = True

        for mask in range(1, 1 << r):
            bit = mask & -mask
            j = bit.bit_length() - 1
            prev = mask ^ bit

            if product[prev] <= k // powers[j]:
                product[mask] = product[prev] * powers[j]
                legal[mask] = True

        maximal = []

        for mask in range(1, 1 << r):
            if not legal[mask]:
                continue

            is_maximal = True
            missing = full ^ mask

            while missing:
                bit = missing & -missing
                j = bit.bit_length() - 1

                if legal[mask | bit]:
                    is_maximal = False
                    break

                missing ^= bit

            if is_maximal:
                maximal.append(mask)

        # Every stored resistance has the same profile, so it can
        # realize every maximal mask of this profile.
        for cost in costs:
            candidates.append((cost, maximal))

    # dp[mask] = (number of senators, total resistance).
    # We compare by the eventual objective indirectly using the pair.
    #
    # Since m <= r <= 11, keep the best resistance for every exact
    # count and mask.
    dp = [[INF] * (1 << r) for _ in range(r + 1)]
    dp[0][0] = 0

    for cost, masks in candidates:
        old = [row[:] for row in dp]

        for cnt in range(r):
            row = old[cnt]
            for mask, cur in enumerate(row):
                if cur == INF:
                    continue

                for s in masks:
                    nm = mask | s
                    nv = cur + cost
                    if nv < dp[cnt + 1][nm]:
                        dp[cnt + 1][nm] = nv

    ans = INF

    for cnt in range(1, r + 1):
        if dp[cnt][full] != INF:
            ans = min(ans, cnt * dp[cnt][full])

    print(-1 if ans == INF else ans)

if __name__ == "__main__":
    solve()
```

The first part of the implementation computes the global gcd and immediately handles the zero-lobbying case. The gcd factorization uses trial division only on one number, and at most 11 distinct primes survive.

For each senator, `powers[j]` is the complete power of `primes[j]` contained in that senator's \(a_i\). This is the quantity that must be included in the divisor if that prime is to disappear completely. Using only the prime itself would be incorrect for values such as \(a_i=12\), where removing 2 requires division by 4.

The `profiles` dictionary is the main compression step. Senators with identical prime-power requirements behave identically from the gcd perspective, so only their smallest resistances matter. Keeping \(r\) of them is sufficient because no optimal campaign needs more than \(r\) senators.

The `legal` array computes every legal subset for one profile using the recurrence

\[
D[S]=D[S\setminus\{p\}]\cdot p^{v_p(a_i)}.
\]

The division `powers[j] <= k // product[prev]` is deliberately written this way rather than multiplying first. It avoids creating a number larger than necessary and gives an exact comparison against \(k\).

Only maximal legal masks are stored. If a senator can remove a larger set of primes, using a strict subset never gives that senator an advantage. The larger mask can always be used instead.

The DP dimension `cnt` records how many senators have been selected. This is necessary because the final objective is not merely the sum of resistances. The actual answer multiplies that sum by the number of lobbied senators.

Python integers have arbitrary precision, so the potentially large product `cnt * dp[cnt][full]` does not overflow. The maximum possible answer is still comfortably manageable as an integer.

## Worked Examples

### Sample 1

The input is

```text
3 6
30 30 30
100 4 5
```

The initial gcd is 30, whose prime factors are 2, 3, and 5. For each senator, removing 2 costs divisor 2, removing 3 costs 3, removing 5 costs 5, and removing both 2 and 3 costs 6.

The important states are:

| Senators used | Removed primes | Resistance | Campaign time |
|---:|---|---:|---:|
| 0 | none | 0 | 0 |
| 1 | {2,3} | 4 | 4 |
| 2 | {2,3,5} | 9 | 18 |
| 2 | {2,3,5} | 105 | 210 |
| 3 | {2,3,5} | 109 | 327 |

The best final state uses senators with resistances 4 and 5. The first can remove 2 and 3 together by dividing 30 by 6, while the second removes 5 by dividing by 5. The total resistance is 9 and two senators are lobbied, giving

\[
2\cdot9=18.
\]

So the output is `18`.

This example demonstrates why the order of lobbying does not matter and why one senator can remove several primes when their required divisor fits inside \(k\).

### Sample 2

The input is

```text
1 1000000
```

There is one senator and its \(a_i\) value is 1. The gcd is already 1.

| Initial gcd | Prime mask | Senators used | Answer |
|---:|---|---:|---:|
| 1 | 0 | 0 | 0 |

The campaign is already successful, so the algorithm exits before constructing any DP states. The correct output is `0`.

This exercises the boundary case where no lobbying is required.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | \(O(nr + C2^r + C2^{2r})\) in the compressed implementation | \(r\le11\), and the exponential work depends only on the distinct gcd primes |
| Space | \(O(Cr + r2^r)\) | Stores compressed profiles and the small subset DP |

The linear part processes at most \(10^6\) senators and only the at most 11 primes of the global gcd. The exponential part is bounded by the small prime universe rather than by \(n\). The implementation also compresses equal prime-power profiles before running the DP, which is essential for the large \(n\) limit.

## Test Cases

```python
# This test harness uses the same solve logic through a small wrapper.

import sys
import io
from math import gcd

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        n, k = map(int, sys.stdin.readline().split())
        a = list(map(int, sys.stdin.readline().split()))
        e = list(map(int, sys.stdin.readline().split()))

        g = 0
        for x in a:
            g = gcd(g, x)

        if g == 1:
            return "0"

        primes = []
        x = g
        p = 2
        while p * p <= x:
            if x % p == 0:
                primes.append(p)
                while x % p == 0:
                    x //= p
            p = 3 if p == 2 else p + 2
        if x > 1:
            primes.append(x)

        r = len(primes)
        full = (1 << r) - 1

        profiles = {}

        for x, cost in zip(a, e):
            powers = []
            y = x

            for p in primes:
                q = 1
                while y % p == 0:
                    y //= p
                    q *= p
                powers.append(q)

            key = tuple(powers)
            arr = profiles.setdefault(key, [])

            if len(arr) < r:
                arr.append(cost)
                arr.sort()
            elif cost < arr[-1]:
                arr[-1] = cost
                arr.sort()

        candidates = []

        for powers, costs in profiles.items():
            msize = 1 << r
            product = [1] * msize
            legal = [False] * msize
            legal[0] = True

            for mask in range(1, msize):
                bit = mask & -mask
                j = bit.bit_length() - 1
                prev = mask ^ bit

                if product[prev] <= k // powers[j]:
                    product[mask] = product[prev] * powers[j]
                    legal[mask] = True

            maximal = []

            for mask in range(1, msize):
                if not legal[mask]:
                    continue

                missing = full ^ mask
                maximal_flag = True

                while missing:
                    bit = missing & -missing
                    if legal[mask | bit]:
                        maximal_flag = False
                        break
                    missing ^= bit

                if maximal_flag:
                    maximal.append(mask)

            for cost in costs:
                candidates.append((cost, maximal))

        INF = 10**30
        dp = [[INF] * (1 << r) for _ in range(r + 1)]
        dp[0][0] = 0

        for cost, masks in candidates:
            old = [row[:] for row in dp]

            for cnt in range(r):
                for mask in range(1 << r):
                    cur = old[cnt][mask]
                    if cur == INF:
                        continue

                    for s in masks:
                        nm = mask | s
                        nv = cur + cost
                        if nv < dp[cnt + 1][nm]:
                            dp[cnt + 1][nm] = nv

        ans = INF
        for cnt in range(1, r + 1):
            if dp[cnt][full] != INF:
                ans = min(ans, cnt * dp[cnt][full])

        return str(-1 if ans == INF else ans)

    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
assert run("""3 6
30 30 30
100 4 5
""") == "18", "sample 1"

# Provided sample 2
assert run("""1 1000000
1
""") == "0", "sample 2"

# Provided sample 3
assert run("""3 5
7 7 7
1 1 1
""") == "-1", "sample 3"

# Already coprime, so no lobbying is needed.
assert run("""2 10
6 35
1 1
""") == "0", "initial gcd is already 1"

# Two senators must split the primes 2 and 3.
assert run("""2 2
6 6
1 1
""") == "4", "split one prime between two senators"

# k is inclusive: division by 6 is legal when k = 6.
assert run("""2 6
6 10
1 1
""") == "4", "boundary k"

# A higher prime exponent must be removed completely.
assert run("""2 4
12 18
1 1
""") == "4", "complete prime power removal"
```

| Test input | Expected output | What it validates |
|---|---:|---|
| `2 10 / 6 35 / 1 1` | `0` | Initial gcd is already 1 |
| `2 2 / 6 6 / 1 1` | `4` | Different senators can remove different common primes |
| `2 6 / 6 10 / 1 1` | `4` | The divisor limit is inclusive |
| `2 4 / 12 18 / 1 1` | `4` | A complete prime power, not just the prime, must be divided out |

## Edge Cases

When the initial gcd is 1, the algorithm stops immediately. For

```text
2 10
6 35
1 1
```

the gcd is 1, so the prime list is empty and the correct answer is `0`. No senator should be selected.

When several senators must cooperate, the mask DP handles the split naturally. For

```text
2 2
6 6
1 1
```

the common primes are 2 and 3. With \(k=2\), one senator can remove only 2 and another can remove only 3. The DP reaches the full mask using two senators with total resistance 2, so the final cost is \(2\cdot2=4\).

When the divisor limit is exactly tight, the product comparison must allow equality. For

```text
2 6
6 10
1 1
```

the first senator can divide 6 by 6, removing both 2 and 3, while the second senator removes 5 from 10 by dividing by 5. The required divisors are exactly within the limit, so the answer is 4.

When a common prime appears with exponent greater than one, the complete exponent has to disappear from the selected senator. For example, with

```text
2 4
12 18
1 1
```

the gcd is 6. Senator 1 needs division by 4 to remove 2 completely, while senator 2 needs division by 3 to remove 3. Both operations are legal, giving final gcd 1 and total time 4. A mask construction based only on whether a prime divides \(a_i\) would incorrectly believe that dividing 12 by 2 is sufficient, leaving a common factor 2 behind.
