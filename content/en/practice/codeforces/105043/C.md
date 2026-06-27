---
title: "CF 105043C - \u041c\u0430\u0440\u0441\u0438\u0430\u043d\u0441\u043a\u0438\u0435 \u0447\u0438\u0441\u043b\u0430"
description: "We are given a fixed integer a and an interval [l, r]. A number x from that interval is considered compatible with a if gcd(a, x) = 1. The task is to count how many integers in the interval are coprime with a. The most striking constraint is that l and r can be as large as 10^18."
date: "2026-06-28T01:31:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105043
codeforces_index: "C"
codeforces_contest_name: "\u0424\u0438\u043d\u0430\u043b \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b \u041d\u0422\u041e: \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u043e\u043d\u043d\u0430\u044f \u0431\u0435\u0437\u043e\u043f\u0430\u0441\u043d\u043e\u0441\u0442\u044c. \u0421\u0435\u043a\u0446\u0438\u044f - \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0430"
rating: 0
weight: 105043
solve_time_s: 72
verified: true
draft: false
---

[CF 105043C - \u041c\u0430\u0440\u0441\u0438\u0430\u043d\u0441\u043a\u0438\u0435 \u0447\u0438\u0441\u043b\u0430](https://codeforces.com/problemset/problem/105043/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed integer `a` and an interval `[l, r]`. A number `x` from that interval is considered compatible with `a` if `gcd(a, x) = 1`. The task is to count how many integers in the interval are coprime with `a`.

The most striking constraint is that `l` and `r` can be as large as `10^18`. Although the interval endpoints are enormous, the value of `a` is at most `10^7`. This immediately tells us that any algorithm depending on the size of the interval is impossible. Even iterating through an interval of length `10^9` would already be far too slow, while the interval here can be vastly larger.

On the other hand, factoring a number up to `10^7` is inexpensive. Trial division up to `√a` requires at most about 3162 iterations, which is tiny. This suggests that the solution should depend only on the prime factors of `a`, not on the interval length.

One easy mistake is to count multiples of every prime factor independently without correcting for overlaps.

For example,

```
a = 6
l = 1
r = 6
```

The correct answer is `2`, since only `1` and `5` are coprime with `6`. Simply subtracting multiples of `2` and multiples of `3` gives `6 - 3 - 2 = 1`, because the number `6` is subtracted twice.

Another common mistake is to use every prime factor with multiplicity.

For example,

```
a = 12
l = 1
r = 12
```

The prime factorization is `2² · 3`, but only the distinct prime factors `{2, 3}` matter. Whether a number shares a factor of `2` with `12` does not depend on how many times `2` appears in the factorization.

A final edge case occurs when `a = 1`.

```
a = 1
l = 10
r = 20
```

Every integer is coprime with `1`, so the answer is `11`. An implementation that always performs inclusion-exclusion without checking that there are actually prime factors could incorrectly produce zero.

## Approaches

The most direct solution checks every integer in the interval. For each number `x`, compute `gcd(a, x)` and increase the answer if the gcd equals `1`. This is obviously correct because it tests exactly the required property.

Unfortunately, this approach depends on the interval length. In the worst case the interval contains almost `10^18` numbers, making even a single pass completely impossible.

The key observation is that a number fails to be coprime with `a` exactly when it is divisible by at least one distinct prime factor of `a`. Once the distinct prime divisors are known, the problem becomes counting numbers in the interval divisible by at least one of those primes.

Counting multiples of a single number in an interval is easy. The difficulty is that a number may be divisible by several prime factors simultaneously, causing double counting. This is exactly the situation where the inclusion-exclusion principle applies.

Since `a ≤ 10^7`, it can have only a small number of distinct prime factors. The product of the first nine primes already exceeds `10^7`, so there are at most eight distinct prime divisors. This means there are at most `2^8 = 256` subsets, making inclusion-exclusion extremely fast.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((r - l + 1) log a) | O(1) | Too slow |
| Optimal | O(√a + 2^k · k) | O(k) | Accepted |

Here, `k` is the number of distinct prime factors of `a`.

## Algorithm Walkthrough

1. Factorize `a` using trial division and store only its distinct prime divisors.
2. Let `total = r - l + 1`, the number of integers in the interval.
3. Enumerate every non-empty subset of the distinct prime divisors.
4. For each subset, compute the product of its primes. Because all factors are distinct primes, this product is simply their least common multiple.
5. Count how many numbers in `[l, r]` are divisible by this product using

```
r // product - (l - 1) // product
```
6. If the subset contains an odd number of primes, add this count to the inclusion-exclusion total. If it contains an even number of primes, subtract it.
7. The inclusion-exclusion total equals the number of integers sharing at least one prime factor with `a`.
8. Subtract this value from `total`. The result is exactly the number of integers coprime with `a`.

### Why it works

Every integer in the interval either shares no prime factor with `a` or shares at least one. Inclusion-exclusion counts exactly those integers divisible by at least one distinct prime divisor of `a`, correcting for every overlap between divisibility conditions. Since a number is coprime with `a` precisely when it is excluded from this union, subtracting the union size from the interval size gives the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

a, l, r = map(int, input().split())

primes = []
x = a
d = 2
while d * d <= x:
    if x % d == 0:
        primes.append(d)
        while x % d == 0:
            x //= d
    d += 1 if d == 2 else 2
if x > 1:
    primes.append(x)

bad = 0
k = len(primes)

for mask in range(1, 1 << k):
    prod = 1
    bits = 0
    for i in range(k):
        if (mask >> i) & 1:
            prod *= primes[i]
            bits += 1
    cnt = r // prod - (l - 1) // prod
    if bits & 1:
        bad += cnt
    else:
        bad -= cnt

print((r - l + 1) - bad)
```

The first part factorizes `a` and stores only distinct prime divisors. The inner `while` loop removes every occurrence of the current prime so repeated factors never appear in the list.

The next section iterates through every non-empty subset of these primes using a bitmask. Each mask uniquely represents one subset. The subset product is built by multiplying the selected primes together.

The interval count uses the standard formula for counting multiples inside a closed interval. Since Python integers have arbitrary precision, products and interval endpoints up to `10^18` are handled safely.

Finally, odd-sized subsets are added and even-sized subsets are subtracted according to the inclusion-exclusion principle. The resulting count of non-coprime numbers is removed from the interval size to obtain the answer.

## Worked Examples

### Sample 1

Input:

```
5 4 8
```

The distinct prime factors are `{5}`.

| Step | Current subset | Product | Multiples in interval | Inclusion-exclusion total |
| --- | --- | --- | --- | --- |
| 1 | {5} | 5 | 1 | 1 |

The interval contains `5` numbers. One of them is divisible by `5`, so four numbers are coprime with `5`.

Answer: `4`.

### Sample 2

Input:

```
3 1 20
```

The distinct prime factors are `{3}`.

| Step | Current subset | Product | Multiples in interval | Inclusion-exclusion total |
| --- | --- | --- | --- | --- |
| 1 | {3} | 3 | 6 | 6 |

The interval has `20` numbers, and `6` are divisible by `3`. The remaining `14` are coprime with `3`.

Answer: `14`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(√a + 2^k · k) | Trial division factorization plus inclusion-exclusion over all subsets |
| Space | O(k) | Stores the distinct prime divisors |

Since `a ≤ 10^7`, trial division is extremely small. The number of distinct prime factors is at most eight, so at most `255` non-empty subsets are processed. The running time is effectively constant with respect to the interval size, allowing intervals reaching `10^18`.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    a, l, r = map(int, input().split())

    primes = []
    x = a
    d = 2
    while d * d <= x:
        if x % d == 0:
            primes.append(d)
            while x % d == 0:
                x //= d
        d += 1 if d == 2 else 2
    if x > 1:
        primes.append(x)

    bad = 0
    k = len(primes)

    for mask in range(1, 1 << k):
        prod = 1
        bits = 0
        for i in range(k):
            if (mask >> i) & 1:
                prod *= primes[i]
                bits += 1
        cnt = r // prod - (l - 1) // prod
        if bits & 1:
            bad += cnt
        else:
            bad -= cnt

    print((r - l + 1) - bad)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    global input
    input = sys.stdin.readline
    out = io.StringIO()
    old = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = old
    return out.getvalue()

assert run("5 4 8\n") == "4\n", "sample 1"
assert run("3 1 20\n") == "14\n", "sample 2"
assert run("1 1 1\n") == "1\n", "minimum case"
assert run("12 1 12\n") == "4\n", "repeated prime factors"
assert run("6 6 6\n") == "0\n", "single non-coprime value"
assert run("2 999999999999999999 1000000000000000000\n") == "1\n", "large boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `1` | No prime factors |
| `12 1 12` | `4` | Duplicate prime factors handled correctly |
| `6 6 6` | `0` | Single element interval |
| `2 999999999999999999 1000000000000000000` | `1` | Very large endpoints and interval boundaries |

## Edge Cases

When `a = 1`, there are no prime divisors. Consider

```
1 10 20
```

The prime list is empty, so the inclusion-exclusion loop performs no iterations and the count of non-coprime numbers remains zero. The interval contains `11` numbers, so the algorithm returns `11`, which is correct because every integer is coprime with `1`.

When `a` contains repeated prime factors, only distinct primes are stored.

```
12 1 12
```

The factorization step produces `{2, 3}` instead of `{2, 2, 3}`. Inclusion-exclusion counts numbers divisible by `2` or `3`, giving `8`, and subtracting from `12` leaves `4`, namely `1`, `5`, `7`, and `11`.

When the interval contains only one number, the same counting formulas still work.

```
6 6 6
```

The interval size is `1`. Inclusion-exclusion finds that `6` is divisible by both `2` and `3`, so it belongs to the union of forbidden numbers. The final answer is `0`, exactly as expected.

When the interval endpoints are extremely large,

```
2 999999999999999999 1000000000000000000
```

the algorithm never iterates over the interval. It computes the number of even integers using integer division, subtracts that from the interval length of `2`, and correctly returns `1`. The running time depends only on the factorization of `2`, not on the size of the interval.
