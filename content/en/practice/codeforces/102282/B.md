---
title: "CF 102282B - \u0415\u0449\u0451 \u043e\u0434\u043d\u0430"
description: "We need to count the positive integers from 1 through r that are coprime with n. Two numbers are coprime when their greatest common divisor is exactly 1. The input contains two integers, n and r, each at most 10^9."
date: "2026-08-13T16:11:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102282
codeforces_index: "B"
codeforces_contest_name: "2011, \u041e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u043a\u043e\u043d\u0442\u0435\u0441\u0442 \u0421\u0413\u0410\u0423 \u043d\u0430 \u0447\u0435\u0442\u0432\u0435\u0440\u0442\u044c\u0444\u0438\u043d\u0430\u043b ACM ICPC"
rating: 0
weight: 102282
solve_time_s: 76
verified: true
draft: false
---

[CF 102282B - \u0415\u0449\u0451 \u043e\u0434\u043d\u0430](https://codeforces.com/problemset/problem/102282/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to count the positive integers from `1` through `r` that are coprime with `n`. Two numbers are coprime when their greatest common divisor is exactly `1`.

The input contains two integers, `n` and `r`, each at most `10^9`. The value of `r` is large enough that checking every number individually is not viable. Even if one greatest-common-divisor computation were very cheap, iterating through all `10^9` candidates would require up to `10^9` gcd computations. The factorization of `n` is much more promising because `n <= 10^9`, so trial division only needs to consider divisors up to `sqrt(n) <= 31623`. Once the distinct prime factors of `n` are known, there can be at most nine of them, because the product of the first ten primes already exceeds `10^9`.

The main edge case is `n = 1`. Every positive integer is coprime with `1`, so for `1 5` the answer is `5`. A formula that blindly assumes that `n` has at least one prime factor could accidentally return zero or leave its initial answer unchanged incorrectly.

The boundary `r` must be inclusive. For `n = 2, r = 2`, the numbers under consideration are `1` and `2`, and only `1` is coprime with `2`, so the answer is `1`. A loop over `range(1, r)` would accidentally exclude `r` and happen to give the wrong result for many inputs.

Repeated prime factors must also be handled correctly. For `n = 12, r = 12`, the relevant prime factors are only `2` and `3`, not `2, 2, 3`. The answer is `4`, corresponding to `1, 5, 7, 11`. Treating repeated factors as separate inclusion-exclusion choices would count the same forbidden condition multiple times.

A final boundary case is when `n` itself is much larger than `r`. For `n = 7, r = 3`, all three numbers `1, 2, 3` are coprime with `7`, so the answer is `3`. There is no reason to restrict the candidates according to the size of `n`; only their common divisors matter.

## Approaches

The direct solution is to inspect every integer `x` from `1` through `r` and test whether `gcd(x, n) = 1`. This is correct because the definition of the required set is exactly that gcd condition. However, with `r = 10^9`, the algorithm may perform `10^9` gcd computations. Even though Euclid's algorithm itself is fast, a billion iterations is far beyond the intended time budget.

The useful observation is that whether `x` is coprime with `n` depends only on the distinct prime factors of `n`. Suppose those primes are `p1, p2, ..., pk`. An integer fails to be coprime with `n` exactly when it is divisible by at least one of these primes.

We can count the integers that are divisible by at least one forbidden prime using inclusion-exclusion. For every nonempty subset of the distinct prime factors, let `d` be the product of the primes in that subset. The numbers divisible by every prime in the subset are exactly the multiples of `d`, so there are `r // d` of them among `1` through `r`.

For subsets containing an odd number of primes, these multiples are added. For subsets containing an even number of primes, they are subtracted. If `bad` is the resulting count, the desired answer is `r - bad`.

The only remaining task is finding the distinct prime factors of `n`. Trial division up to the square root is sufficient for `n <= 10^9`. After extracting every occurrence of a prime factor, we keep that prime only once, because inclusion-exclusion needs distinct divisibility conditions.

There is also a useful equivalent interpretation through Euler's totient function. If the upper bound were exactly `n`, the answer would be `phi(n)`. Here the interval ends at arbitrary `r`, so the usual closed-form formula for `phi(n)` is not enough. Inclusion-exclusion applies directly to an arbitrary `r`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(r log n)` | `O(1)` | Too slow |
| Optimal | `O(sqrt(n) + 2^k)` | `O(k)` | Accepted |

Here `k` is the number of distinct prime factors of `n`. Since `n <= 10^9`, `k <= 9`, so the subset enumeration has at most `512` cases.

## Algorithm Walkthrough

1. Factorize `n` by trying divisors from `2` through `sqrt(n)`. Whenever a divisor `p` divides the current value of `n`, record `p` once and repeatedly divide it out. Removing all copies is necessary because only the presence of the prime matters for coprimality.
2. After trial division, if the remaining value is greater than `1`, record it as another prime factor. A remaining value greater than `1` cannot have a smaller unprocessed factor, so it must itself be prime.
3. Enumerate every subset of the distinct prime factors. For a subset, multiply its selected primes to obtain `d`. The integers divisible by every selected prime are precisely the multiples of `d`, giving `r // d` such integers.
4. Add `r // d` when the subset contains an odd number of primes and subtract it when the subset contains an even number of primes. This is the inclusion-exclusion correction for overlaps between divisibility conditions.
5. Subtract the number of non-coprime integers from `r`. The remaining count is exactly the number of integers in `[1, r]` whose gcd with `n` equals `1`.

### Why it works

Let `P` be the set of distinct prime factors of `n`. An integer `x` is not coprime with `n` exactly when at least one prime in `P` divides `x`. Thus the unwanted integers form the union of the sets `A_p = {x : p divides x}` for `p` in `P`.

For any subset of these primes with product `d`, its intersection contains exactly the multiples of `d`, and there are `r // d` such integers up to `r`. Inclusion-exclusion counts the union exactly by alternating addition and subtraction according to subset size. Consequently, `bad` is precisely the number of integers sharing a nontrivial divisor with `n`, and `r - bad` counts exactly the coprime integers.

The factorization stage supplies every prime in `P` exactly once, so the inclusion-exclusion stage represents every possible common prime divisor and no irrelevant condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, r = map(int, input().split())

    x = n
    primes = []

    p = 2
    while p * p <= x:
        if x % p == 0:
            primes.append(p)
            while x % p == 0:
                x //= p
        p += 1 if p == 2 else 2

    if x > 1:
        primes.append(x)

    k = len(primes)
    bad = 0

    for mask in range(1, 1 << k):
        product = 1
        bits = 0

        for i in range(k):
            if mask & (1 << i):
                product *= primes[i]
                bits += 1

        count = r // product

        if bits % 2 == 1:
            bad += count
        else:
            bad -= count

    print(r - bad)

if __name__ == "__main__":
    solve()
```

The code first copies `n` into `x`, because trial division repeatedly reduces the number being factored. The list `primes` contains each distinct prime factor exactly once.

The loop starts with `p = 2`, then checks only odd values after `2`. This avoids testing even divisors that cannot be prime. The condition `p * p <= x` is safe because if `x` has a composite factorization, one of its factors is at most its square root. When the loop ends, a remaining `x > 1` must be prime.

The subset loop uses a bitmask. Bit `i` determines whether `primes[i]` belongs to the current subset. `product` becomes the product of the selected primes, while `bits` records the subset size and determines the inclusion-exclusion sign.

The calculation uses integer division `r // product`, not `(r - 1) // product`, because `r` itself belongs to the interval. Python integers also remove any concern about overflow, although all intermediate products here are small enough for ordinary 64-bit integers as well.

For `n = 1`, the factor list remains empty. The subset loop has no iterations, so `bad = 0` and the answer becomes `r`, which is exactly correct.

## Worked Examples

For the first sample, `n = 2` has one distinct prime factor, `2`.

| Mask | Selected primes | Product | Subset size | `r // product` | `bad` |
| --- | --- | --- | --- | --- | --- |
| `1` | `{2}` | `2` | `1` | `1` | `1` |

The only bad number up to `2` is `2` itself. Subtracting it from the two candidates gives `2 - 1 = 1`, so the output is `1`.

For the second sample, `n = 10` has distinct prime factors `2` and `5`.

| Mask | Selected primes | Product | Subset size | `r // product` | `bad` |
| --- | --- | --- | --- | --- | --- |
| `01` | `{2}` | `2` | `1` | `4` | `4` |
| `10` | `{5}` | `5` | `1` | `1` | `5` |
| `11` | `{2, 5}` | `10` | `2` | `0` | `5` |

Among `1` through `9`, four numbers are divisible by `2`, one is divisible by `5`, and their intersection contains no number. Thus five numbers are not coprime with `10`, leaving `9 - 5 = 4`. The coprime numbers are `1, 3, 7, 9`, which also demonstrates why being prime is unrelated to the required property.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(sqrt(n) + 2^k k)` | Trial division takes `O(sqrt(n))`, and each of the `2^k` subsets checks at most `k` primes |
| Space | `O(k)` | Only the distinct prime factors and a constant number of variables are stored |

For `n <= 10^9`, `sqrt(n) <= 31623`, so the factorization requires only a small number of trial divisions. Also, `k <= 9`, making the subset enumeration tiny. The algorithm therefore avoids any dependence on the potentially billion-sized value of `r` and comfortably fits the given limits.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        n, r = map(int, sys.stdin.readline().split())

        x = n
        primes = []

        p = 2
        while p * p <= x:
            if x % p == 0:
                primes.append(p)
                while x % p == 0:
                    x //= p
            p += 1 if p == 2 else 2

        if x > 1:
            primes.append(x)

        k = len(primes)
        bad = 0

        for mask in range(1, 1 << k):
            product = 1
            bits = 0

            for i in range(k):
                if mask & (1 << i):
                    product *= primes[i]
                    bits += 1

            count = r // product

            if bits & 1:
                bad += count
            else:
                bad -= count

        print(r - bad)

        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert solve_data("2 2\n") == "1", "sample 1"
assert solve_data("10 9\n") == "4", "sample 2"

# Minimum-size input: the only positive integer is coprime with itself when it is 1.
assert solve_data("1 1\n") == "1", "minimum input"

# n = 1 means every number up to r is coprime with n.
assert solve_data("1 1000000000\n") == "1000000000", "n = 1"

# Equal values with repeated prime factors: gcd(1, 10)=1, gcd(3,10)=1,
# gcd(7,10)=1, gcd(9,10)=1.
assert solve_data("10 10\n") == "4", "equal values"

# Boundary where r itself is divisible by n's prime factor.
assert solve_data("2 2\n") == "1", "inclusive upper boundary"

# Large composite n with repeated factors: 1e9 = 2^9 * 5^9.
# Count = 1e9 * (1 - 1/2) * (1 - 1/5) = 400000000.
assert solve_data("1000000000 1000000000\n") == "400000000", "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Minimum input and the empty prime-factor set |
| `1 1000000000` | `1000000000` | Every candidate is coprime with `1` |
| `10 10` | `4` | Equal `n` and `r`, with multiple distinct prime factors |
| `2 2` | `1` | Inclusive upper boundary |
| `1000000000 1000000000` | `400000000` | Maximum-size values and repeated prime factors |

## Edge Cases

For `n = 1, r = 5`, the factorization produces an empty list because `1` has no prime factors. There are no inclusion-exclusion subsets, so `bad` remains zero. The final calculation is `5 - 0 = 5`, correctly counting every number from `1` to `5`.

For `n = 2, r = 2`, the factor list is `[2]`. The single subset represents numbers divisible by `2`, and `2 // 2 = 1`. Thus one candidate is rejected and the answer is `2 - 1 = 1`. This confirms that the upper endpoint `r` is included.

For `n = 12, r = 12`, factorization produces `[2, 3]`, not `[2, 2, 3]`. Inclusion-exclusion counts `6` multiples of `2`, `4` multiples of `3`, and subtracts `2` multiples of `6`. Hence `bad = 6 + 4 - 2 = 8`, giving `12 - 8 = 4`. The four valid values are `1, 5, 7, 11`.

For `n = 7, r = 3`, factorization produces `[7]`, but `3 // 7 = 0`. No number up to `3` is divisible by `7`, so `bad = 0` and the answer is `3`. This shows why the method works even when every candidate is smaller than `n`.

For the maximum-size case `n = r = 10^9`, the distinct factors are `2` and `5`. The bad count is `500000000 + 200000000 - 100000000 = 600000000`, leaving `400000000` valid numbers. The algorithm reaches this result without iterating over any of the `10^9` candidate integers.
