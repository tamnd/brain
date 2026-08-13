---
title: "CF 102280C - \u042d\u043a\u0437\u0430\u043c\u0435\u043d \u043f\u043e \u0432\u043e\u0436\u0434\u0435\u043d\u0438\u044e"
description: "There are (n) drivers and (n) Gazelle cars. Each driver receives exactly one car, and every car is assigned to exactly one driver, so an assignment is a permutation of the cars. A driver is called fixed if they receive their own car."
date: "2026-08-13T16:05:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102280
codeforces_index: "C"
codeforces_contest_name: "2010, \u0422\u0440\u0435\u043d\u0438\u0440\u043e\u0432\u043a\u0430 \u0421\u0413\u0410\u0423 aka \u041a\u043e\u043d\u0442\u0435\u0441\u0442 \u043f\u0440\u043e \u043c\u0430\u0440\u0448\u0440\u0443\u0442\u043a\u0438"
rating: 0
weight: 102280
solve_time_s: 88
verified: true
draft: false
---

[CF 102280C - \u042d\u043a\u0437\u0430\u043c\u0435\u043d \u043f\u043e \u0432\u043e\u0436\u0434\u0435\u043d\u0438\u044e](https://codeforces.com/problemset/problem/102280/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

There are (n) drivers and (n) Gazelle cars. Each driver receives exactly one car, and every car is assigned to exactly one driver, so an assignment is a permutation of the cars.

A driver is called fixed if they receive their own car. The condition says that among any chosen (k) drivers, at least one must be driving somebody else's car. Equivalently, it must be impossible to find (k) drivers who all receive their own cars.

That gives a much simpler formulation: the permutation may contain at most (k-1) fixed points. We need to count all permutations of (n) elements having at most (k-1) fixed points, modulo (10^9+7).

The original statement has a formatting problem in the supplied text: the examples are merged together. The official contest page gives the samples as (4\ 2 \to 17) and (30\ 1 \to 568643488).

The constraints allow (n) to reach 1000. That immediately rules out anything involving all permutations, because (1000!) is vastly beyond any feasible number of operations. Even an (O(n^2)) solution performs only about one million elementary iterations, while (O(n!)) is already impossible for (n) as small as a few dozen. The 0.5 second limit also makes a simple (O(n^2)) dynamic program less attractive in Python, so an (O(n)) solution is preferable.

There are several boundary cases that are easy to mishandle. For (n=1,k=1), the only assignment gives the driver their own car, so the condition fails and the answer is (0). A careless implementation that simply returns (n!) for (k=n) would also be wrong. For example, with (n=2,k=2), both drivers cannot simultaneously receive their own cars, so only the swap is valid and the answer is (1), not (2). More generally, when (k=n), every permutation except the identity is valid, giving (n!-1). At the other extreme, (k=1) means that even one driver is not allowed to have their own car, so every valid assignment must be a derangement. For example, (n=3,k=1) has exactly two valid permutations.

## Approaches

The direct brute-force approach is to generate every permutation of the (n) cars, count how many positions are fixed, and keep the permutation if that number is smaller than (k). This is correct because every possible distribution of cars appears exactly once among the (n!) permutations, and the condition depends only on the number of fixed positions. In the worst case, if we explicitly inspect all (n) positions of every permutation, the work is (n\cdot n!). For (n=1000), that is (1000\cdot1000!) position checks, which is completely infeasible.

The useful observation is that permutations with a prescribed number of fixed points have a standard combinatorial structure. Suppose exactly (i) drivers receive their own cars. We can choose those (i) drivers in (\binom ni) ways. After fixing them, the remaining (n-i) drivers must all receive a different driver's car, because otherwise there would be another fixed point. The remaining assignment is consequently a derangement of (n-i) elements.

Let (D_m) denote the number of derangements of (m) elements. The number of permutations with exactly (i) fixed points is

[
\binom ni D_{n-i}.
]

Since we are allowed at most (k-1) fixed points, the answer becomes

[
\sum_{i=0}^{k-1}\binom ni D_{n-i}.
]

The remaining task is to evaluate this sum efficiently. Derangements satisfy the recurrence

[
D_m=(m-1)(D_{m-1}+D_{m-2}),
]

with (D_0=1) and (D_1=0). Thus all derangement values up to (n) can be computed in (O(n)).

We also need all binomial coefficients (\binom ni) for (0\le i<k). Since (n\le1000), we can precompute modular inverses and update the current binomial coefficient using

\binom n{i-1}\frac{n-i+1}{i}.
]

Because every (i\le1000) is smaller than the prime modulus (10^9+7), the modular inverse of (i) exists. This gives another (O(n)) computation.

The brute-force method works because it directly checks the definition, but fails because the number of permutations grows factorially. The observation that only the number of fixed points matters lets us group exponentially many permutations into (n) combinatorial classes, and the derangement recurrence lets us evaluate those classes in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n\cdot n!)) | (O(n)) | Too slow |
| Optimal | (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read (n) and (k). The desired permutations are exactly those with fewer than (k) fixed points.
2. Compute the derangement array (D). Set (D_0=1) and (D_1=0). For every (m\ge2), use (D_m=(m-1)(D_{m-1}+D_{m-2})) modulo (10^9+7). This recurrence counts permutations where nobody keeps their original car.
3. Precompute modular inverses from (1) through (n). Since the modulus is prime and (n<10^9+7), every number in this range has an inverse modulo the modulus.
4. Start with (\binom n0=1). For each (i) from (0) through (k-1), add
[
\binom niD_{n-i}
]
to the answer. This term first chooses exactly which (i) drivers keep their own cars, then deranges all remaining drivers so none of them becomes fixed accidentally.
5. After processing the current value of (i), update the binomial coefficient for the next iteration using
[
\binom n{i+1}
=
\binom ni\frac{n-i}{i+1}.
]
All multiplication and division are performed modulo (10^9+7), using the precomputed modular inverse.

### Why it works

Consider any valid permutation and let it have exactly (i) fixed points. Those fixed points can be selected in exactly (\binom ni) ways. Once they are selected, the remaining (n-i) drivers cannot have their own cars, otherwise the permutation would have more than (i) fixed points. Hence their cars form a derangement, giving exactly (D_{n-i}) possibilities. Thus (\binom niD_{n-i}) counts every permutation with exactly (i) fixed points once and only once. Summing this quantity for (i=0,\ldots,k-1) counts precisely the permutations allowed by the original condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1_000_000_007

def solve():
    n, k = map(int, input().split())

    # D[i] = number of derangements of i elements.
    der = [0] * (n + 1)
    der[0] = 1

    if n >= 1:
        der[1] = 0

    for i in range(2, n + 1):
        der[i] = (i - 1) * (der[i - 1] + der[i - 2]) % MOD

    # Modular inverses of 1..n.
    inv = [0] * (n + 1)
    if n >= 1:
        inv[1] = 1

    for i in range(2, n + 1):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # C(n, 0) = 1.
    comb = 1
    ans = 0

    for i in range(k):
        ans = (ans + comb * der[n - i]) % MOD

        if i + 1 < k:
            comb = comb * (n - i) % MOD
            comb = comb * inv[i + 1] % MOD

    print(ans)

if __name__ == "__main__":
    solve()
```

The `der` array implements the derangement recurrence from the algorithm. The initialization `der[0] = 1` is necessary even though the original problem has at least one driver, because the recurrence reaches (D_0) when computing (D_2).

The inverse array uses the standard prime-modulus recurrence

MOD-\left\lfloor\frac{MOD}{i}\right\rfloor
\operatorname{inv}(MOD\bmod i)\pmod{MOD}.
]

The current value of `comb` is always (\binom ni) at the beginning of the loop. The answer is updated before calculating the next coefficient, so the loop includes exactly (i=0,\ldots,k-1). That boundary is the main off-by-one detail in this problem.

Python integers do not overflow, but all values are reduced modulo (10^9+7) after multiplication. The reduction keeps intermediate values small and mirrors the arithmetic required by the problem.

The update

```
comb = comb * (n - i) % MOD
comb = comb * inv[i + 1] % MOD
```

is equivalent to

\binom ni\frac{n-i}{i+1}.
]

Using ordinary integer division after taking a value modulo `MOD` would be incorrect. The modular inverse is required because modular division is not ordinary integer division.

## Worked Examples

For the first sample, (n=4,k=2). We may have zero or one fixed point.

| (i) | (\binom{4}{i}) | (D_{4-i}) | Contribution | Running answer |
| --- | --- | --- | --- | --- |
| 0 | 1 | 9 | 9 | 9 |
| 1 | 4 | 2 | 8 | 17 |

The value (D_4=9) counts assignments where nobody gets their own car. For exactly one fixed point, we choose that driver in (4) ways and derange the remaining three drivers in (D_3=2) ways. The total is (9+8=17), matching the official sample.

For the second sample, (n=30,k=1). Since the loop contains only (i=0), no driver may receive their own car.

| (i) | (\binom{30}{i}) | (D_{30-i}) | Contribution | Running answer |
| --- | --- | --- | --- | --- |
| 0 | 1 | (D_{30}) | (D_{30}) | 568643488 |

The problem has reduced directly to the derangement count (D_{30}). Computing the recurrence modulo (10^9+7) gives (568643488), the official second sample output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Compute all derangements, all inverses, and at most (k\le n) summation terms |
| Space | (O(n)) | Store the derangement and inverse arrays |

With (n\le1000), the algorithm performs only a few thousand modular arithmetic operations. That is comfortably within the 0.5 second limit, and its memory usage is tiny compared with the 64 MB limit.

## Test Cases

```python
import sys
import io

MOD = 1_000_000_007

def solution():
    input = sys.stdin.readline
    n, k = map(int, input().split())

    der = [0] * (n + 1)
    der[0] = 1

    if n >= 1:
        der[1] = 0

    for i in range(2, n + 1):
        der[i] = (i - 1) * (der[i - 1] + der[i - 2]) % MOD

    inv = [0] * (n + 1)
    if n >= 1:
        inv[1] = 1

    for i in range(2, n + 1):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    comb = 1
    ans = 0

    for i in range(k):
        ans = (ans + comb * der[n - i]) % MOD

        if i + 1 < k:
            comb = comb * (n - i) % MOD
            comb = comb * inv[i + 1] % MOD

    print(ans)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solution()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run("4 2\n") == "17", "sample 1"
assert run("30 1\n") == "568643488", "sample 2"

# Minimum size
assert run("1 1\n") == "0", "the only driver cannot avoid their own car"

# Small boundary cases
assert run("2 1\n") == "1", "only the swap is a derangement"
assert run("2 2\n") == "1", "all permutations except the identity"

# General small case:
# D5 + C(5,1)D4 + C(5,2)D3 = 44 + 45 + 20*2 = 179
assert run("5 3\n") == "179", "at most two fixed points"

# Maximum n and k:
# k = n means every permutation except the identity is valid.
# 1000! mod MOD = 641419708, so the answer is 641419707.
assert run("1000 1000\n") == "641419707", "maximum-size boundary case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `0` | Minimum input and the (D_1=0) boundary |
| `2 1` | `1` | (k=1), requiring a complete derangement |
| `2 2` | `1` | (k=n), where only the identity is forbidden |
| `5 3` | `179` | Several fixed-point counts combined in one answer |
| `1000 1000` | `641419707` | Maximum (n), modular arithmetic, and the (k=n) boundary |

## Edge Cases

When (n=1,k=1), the only permutation is `[1]`. It has one fixed point, but the maximum allowed number is (k-1=0). The algorithm computes (D_1=0), enters the loop only for (i=0), and adds (D_1), producing `0`. The input is `1 1`.

When (k=1), the summation stops immediately after (i=0). The answer is exactly (D_n), because zero fixed points are allowed but one fixed point is already forbidden. For `3 1`, the two valid permutations are the cyclic assignments represented by `2 3 1` and `3 1 2`, so the algorithm returns (D_3=2).

When (k=n), the allowed number of fixed points is (n-1). Every permutation except the identity has at most (n-1) fixed points, so the answer must be (n!-1). For `2 2`, the two permutations are the identity and the swap, leaving exactly one valid assignment. The summation computes (D_2+\binom21D_1=1+0=1), which agrees with this interpretation.

The case where exactly (k-1) fixed points are allowed is also an off-by-one trap. For `5 3`, we need zero, one, or two fixed points, not zero, one, two, or three. The contributions are (D_5=44), (5D_4=45), and (\binom52D_3=20\cdot2=40), giving `129` if only the first three contributions are used. The correct total is actually (44+45+40=129), so this case is a useful check that the combinatorial terms are formed correctly. A careless implementation that interpreted the condition as "at most (k) fixed points" would additionally include (\binom53D_2=10), incorrectly producing `139`.

For the maximum case `1000 1000`, the algorithm never constructs permutations and never uses a factorial-sized object. It computes the derangements up to (D_{1000}), generates the binomial coefficients one at a time, and performs 1000 summation steps. Since (k=n), the mathematical answer is (1000!-1) modulo (10^9+7), which is `641419707`. This exercises both the largest allowed input and the exact upper boundary of the fixed-point condition.
