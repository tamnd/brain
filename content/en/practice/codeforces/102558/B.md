---
title: "CF 102558B - \u0417\u0430\u043a\u0440\u044b\u0442\u044b\u0439 \u043a\u043b\u044e\u0447"
description: "The public key is created from a private pair of positive integers (p, q). The first public value is the greatest common divisor of the pair, and the second is the least common multiple."
date: "2026-08-04T09:18:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102558
codeforces_index: "B"
codeforces_contest_name: "Contest for Yandex interns 2019"
rating: 0
weight: 102558
solve_time_s: 93
verified: true
draft: false
---

[CF 102558B - \u0417\u0430\u043a\u0440\u044b\u0442\u044b\u0439 \u043a\u043b\u044e\u0447](https://codeforces.com/problemset/problem/102558/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

The public key is created from a private pair of positive integers `(p, q)`. The first public value is the greatest common divisor of the pair, and the second is the least common multiple. We are given the public pair `(x, y)` and need to count how many ordered private pairs `(p, q)` could have generated it.

The two given numbers can be as large as `10^12`. This rules out trying possible values of `p` and `q`, because even iterating over all divisors of `y` without using the structure of gcd and lcm would be too expensive. A successful solution has to exploit the mathematical relationship between gcd and lcm and reduce the task to factoring a single number. Since the square root of `10^12` is only `10^6`, trial division up to that limit is practical in Python.

The main cases that break careless solutions are related to divisibility and the number `1`. If `x` does not divide `y`, there is no possible private key. For example, input `10 11` has output `0`, because the lcm is always a multiple of the gcd, so a gcd of `10` cannot produce an lcm of `11`.

Another edge case is when the two public values are equal. For input `7 7`, the only possible private key is `(7, 7)`, so the answer is `1`. A solution that only counts prime assignments and forgets that the remaining product can be `1` may mishandle this case.

A third case is when `y / x` contains repeated prime factors. For input `4 36`, the ratio is `9`. The valid normalized pairs are `(1,9)` and `(9,1)`, giving private keys `(4,36)` and `(36,4)`. The exponent of a prime does not create additional choices because both numbers cannot share the same prime factor after removing the gcd.

## Approaches

A direct approach would be to search through possible private keys. Since the lcm of the pair must be `y`, both numbers must be divisors of `y`. We could enumerate every divisor pair `(p, q)` of `y`, check whether `gcd(p, q) = x` and `lcm(p, q) = y`, and count the matches. This is correct because every possible private key must appear in that enumeration. However, generating and checking divisors of a number near `10^12` can already require many operations, and the method does not use the special relationship between gcd and lcm.

The key observation comes from separating out the gcd. Suppose:

`p = x * a`

and

`q = x * b`.

After removing the common part, the remaining values `a` and `b` must be coprime. The lcm becomes:

`lcm(p, q) = x * a * b`.

Therefore:

`a * b = y / x`.

The original problem is now asking how many ordered coprime factorizations the number `y / x` has. If this number has a prime factorization:

`n = r1^e1 * r2^e2 * ... * rk^ek`

then each complete prime power `ri^ei` must go entirely to `a` or entirely to `b`. Splitting a prime power would make the two numbers share that prime, violating the coprime condition. Each of the `k` distinct primes gives two choices, so the answer is `2^k`.

The only remaining task is finding the number of distinct prime factors of `y / x`. Because that value is at most `10^12`, checking divisors up to `10^6` is enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(number of divisors of y) with expensive gcd checks | O(1) | Too slow and ignores structure |
| Optimal | O(sqrt(y / x)) | O(1) | Accepted |

## Algorithm Walkthrough

1. First check whether `y` is divisible by `x`. If it is not, no pair can have gcd `x` and lcm `y`, so the answer is immediately `0`. The lcm must always be a multiple of the gcd.
2. Compute `n = y / x`. This is the product of the two remaining coprime parts after removing the gcd from both private key values.
3. Factorize `n` by trying possible divisors from `2` upward. When a divisor is found, count it as one distinct prime factor and remove all occurrences of it from `n`. Removing the full power is necessary because only the number of different primes affects the answer.
4. If after trial division a value greater than `1` remains, it is a prime factor larger than the square root of the original number. Count it as one more distinct prime.
5. Return `2` raised to the number of distinct prime factors found. Each prime power can be assigned independently to either side of the coprime pair.

Why it works:

After dividing both private numbers by their gcd, the remaining parts must have gcd equal to `1`. The product of these parts is fixed as `y / x`. In a coprime factorization, every prime factor of the product belongs to exactly one side. For every distinct prime, there are exactly two choices: place its full power in the first number or in the second number. These choices are independent, so multiplying the choices gives `2^k`, where `k` is the number of distinct prime factors. Every counted assignment creates exactly one valid private key, and every valid private key corresponds to one assignment.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    x, y = map(int, input().split())

    if y % x != 0:
        print(0)
        return

    n = y // x
    cnt = 0

    d = 2
    while d * d <= n:
        if n % d == 0:
            cnt += 1
            while n % d == 0:
                n //= d
        d += 1

    if n > 1:
        cnt += 1

    print(1 << cnt)

if __name__ == "__main__":
    solve()
```

The first condition handles impossible public keys before doing any factorization. If `x` does not divide `y`, the ratio required by the gcd and lcm relationship is not an integer.

The variable `n` stores the part of the lcm that remains after removing the gcd contribution. The factorization loop counts only distinct primes. Whenever a divisor is found, the inner loop removes its entire exponent because values like `2`, `4`, and `8` do not create separate assignment choices.

The loop condition uses `d * d <= n` rather than calculating a square root. This avoids floating point precision issues for values near `10^12`. Python integers do not overflow, so the multiplication is safe.

The final check for `n > 1` handles a remaining prime factor. For example, after removing small factors from `12`, the remaining value becomes `3`, which still contributes one independent choice.

## Worked Examples

For the first sample, the input is:

```
5 10
```

The execution is:

| Variable | Value | Meaning |
| --- | --- | --- |
| x | 5 | required gcd |
| y | 10 | required lcm |
| n | 2 | normalized product |
| distinct prime count | 1 | prime factor `2` |
| answer | 2 | `2^1` assignments |

The ratio `2` has one distinct prime. That prime power can be assigned to either side, producing `(5,10)` or `(10,5)`.

For the second sample:

```
10 11
```

The execution is:

| Variable | Value | Meaning |
| --- | --- | --- |
| x | 10 | required gcd |
| y | 11 | required lcm |
| y % x | 1 | gcd does not divide lcm |
| answer | 0 | impossible |

The algorithm stops before factorization because no lcm can be smaller than a multiple relationship of the gcd. This confirms the early rejection condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(sqrt(y / x)) | Trial division checks possible factors up to the square root of the remaining value |
| Space | O(1) | Only a few integer variables are stored |

The largest possible value to factor is `10^12`, so the loop performs at most about one million divisor checks. This fits comfortably within typical Codeforces limits.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    x, y = map(int, input().split())

    if y % x != 0:
        return "0\n"

    n = y // x
    cnt = 0
    d = 2

    while d * d <= n:
        if n % d == 0:
            cnt += 1
            while n % d == 0:
                n //= d
        d += 1

    if n > 1:
        cnt += 1

    return str(1 << cnt) + "\n"

assert solution("5 10\n") == "2\n", "sample 1"
assert solution("10 11\n") == "0\n", "sample 2"
assert solution("527 9486\n") == "4\n", "sample 3"

assert solution("1 1\n") == "1\n", "minimum values"
assert solution("7 7\n") == "1\n", "equal public values"
assert solution("4 36\n") == "2\n", "repeated prime factor"
assert solution("1 1000000000000\n") == "16\n", "large composite value"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | The ratio is `1`, so only one private key exists |
| `7 7` | `1` | Equal gcd and lcm case |
| `4 36` | `2` | Prime powers are counted once, not by exponent |
| `1 1000000000000` | `16` | Large input and full factorization boundary |

## Edge Cases

For input `10 11`, the algorithm checks divisibility first. Since `11 % 10` is not zero, it returns `0` immediately. A method based only on factoring `y` might incorrectly continue searching for pairs and waste time on an impossible case.

For input `7 7`, the ratio becomes `1`. The factorization loop finds no primes, so the distinct prime count is zero and the answer is `2^0 = 1`. This correctly represents the single pair `(7,7)`.

For input `4 36`, the ratio is `9`, which factors as `3^2`. The algorithm counts only one distinct prime, giving `2^1 = 2`. The two assignments are `(1,9)` and `(9,1)`, which become `(4,36)` and `(36,4)`. It does not count splitting the two factors of `3` because that would make the normalized values non-coprime.
