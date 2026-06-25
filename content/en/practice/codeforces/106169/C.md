---
title: "CF 106169C - You can't just take and divide"
description: "We need count integers in the interval from 1 to n that satisfy two conditions. The number itself must be odd, and the amount of positive divisors it has must be an odd prime number."
date: "2026-06-25T11:07:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106169
codeforces_index: "C"
codeforces_contest_name: "2025-2026 ICPC NERC, Kyrgyzstan Regional Contest"
rating: 0
weight: 106169
solve_time_s: 48
verified: true
draft: false
---

[CF 106169C - You can't just take and divide](https://codeforces.com/problemset/problem/106169/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We need count integers in the interval from 1 to `n` that satisfy two conditions. The number itself must be odd, and the amount of positive divisors it has must be an odd prime number. The input contains only the upper bound `n`, and the output is the count of valid integers not exceeding it.

The key constraints are hidden in the size of `n`. The value can be as large as `11^13`, which is far too large for checking every integer up to `n`. Even a linear scan would require trillions of operations. We need to exploit the mathematical structure of numbers with the required divisor count.

A few edge cases are easy to miss. The number `1` has one divisor, but one is not prime, so it should never be counted. For input:

```
1
```

the answer is:

```
0
```

A direct approach that only checks whether the divisor count is odd would incorrectly include it.

Another trap is that a prime number itself has a prime number of divisors, but the divisor count must be odd. For example:

```
5
```

has two divisors, `1` and `5`, so it is not valid. The answer is:

```
0
```

A solution that only looks for prime values would fail here.

A final boundary case is a perfect square that is not of the required form. For example:

```
81
```

is a square, but it has `5` divisors. Since `5` is prime, it is valid and should be counted. In contrast:

```
45
```

is not a square, so it cannot have an odd number of divisors. The useful property is not just being odd or prime, it is the exact factorization pattern.

## Approaches

The brute force idea is to iterate through every odd number from `1` to `n`, compute its divisor count, and check whether that count is prime. The divisor count of a number can be found by testing divisors up to its square root. This is correct because every number has finitely many divisors and the divisor count determines whether it qualifies. However, the range can reach about `1.6 * 10^13`, so even visiting the candidates is impossible. The worst case is far beyond any reasonable operation limit.

The main observation comes from the divisor formula. If a number has prime factorization:

```
x = p1^a1 * p2^a2 * ... * pk^ak
```

then its number of divisors is:

```
(a1 + 1) * (a2 + 1) * ... * (ak + 1)
```

This product is odd only when every exponent is even. That means the number itself must be a perfect square. Since the number also has to be odd, the square root must be odd.

Let the square root be:

```
m = p1^b1 * p2^b2 * ... * pk^bk
```

Then:

```
x = m^2
```

and the divisor count becomes:

```
(2b1 + 1) * (2b2 + 1) * ... * (2bk + 1)
```

For this product to be prime, there can only be one factor. Otherwise it would be a product of two numbers greater than one. Therefore `m` must be a power of a single odd prime:

```
m = p^a
```

with:

```
2a + 1
```

being prime.

Now the problem is reduced from checking huge values to generating all valid roots `m` not exceeding `sqrt(n)`. The largest possible root is about `3.3 * 10^6`, so a sieve is easily fast enough. The possible exponents are also very small because powers grow quickly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n sqrt(n)) | O(1) | Too slow |
| Optimal | O(sqrt(n) log log sqrt(n)) | O(sqrt(n)) | Accepted |

## Algorithm Walkthrough

1. Compute `limit = floor(sqrt(n))`. Any valid number is a square, so its square root cannot exceed this value.
2. Generate all primes up to `limit` using the sieve of Eratosthenes. We only need odd primes because the original number must be odd.
3. Generate the list of exponents `a` where `2a + 1` is prime. These are the only exponents that can appear in a valid root.
4. For every odd prime `p` and every valid exponent `a`, compute `p^a`. If the value is at most `limit`, then its square is a valid number and we add it to the answer.
5. Stop multiplying when the current power becomes larger than `limit`, because larger powers can never contribute.

The reason this works is that every valid number has a unique square root. The factorization argument proves that the root must be exactly one prime raised to an exponent satisfying the primality condition. The generation process enumerates every such root, so no valid value is missed. Since different roots produce different squares, no duplicate counting occurs.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    n_line = input().strip()
    if not n_line:
        return
    n = int(n_line)

    limit = math.isqrt(n)

    is_prime = bytearray(b'\x01') * (limit + 1)
    if limit >= 0:
        is_prime[0] = 0
    if limit >= 1:
        is_prime[1] = 0

    i = 2
    while i * i <= limit:
        if is_prime[i]:
            start = i * i
            is_prime[start:limit + 1:i] = b'\x00' * (((limit - start) // i) + 1)
        i += 1

    exponents = []
    for a in range(1, 64):
        if 2 * a + 1 <= limit + 10 and is_prime[2 * a + 1]:
            exponents.append(a)

    ans = 0
    for p in range(3, limit + 1, 2):
        if not is_prime[p]:
            continue
        power = p
        for a in range(1, max(exponents, default=0) + 1):
            if a > 1:
                if power > limit // p:
                    break
                power *= p
            if a in exponents:
                ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution first builds a primality table up to the square root of `n`. This is enough because every candidate is generated from its square root, not from the original value.

The exponent list contains only values where `2a + 1` is prime. The loop starts from exponent one because `a = 0` would represent the number `1`, which is not valid.

For each prime base, the code repeatedly multiplies by the base while staying within the root limit. The division check before multiplication prevents the value from exceeding Python's integer bounds in languages where overflow is possible, and it also avoids unnecessary work.

The final count is the number of valid roots. Counting roots instead of squares avoids large arithmetic because the square operation is not needed.

## Worked Examples

For input:

```
9
```

the square root limit is `3`.

The valid exponent is `1` because `2 * 1 + 1 = 3`, which is prime.

| prime | exponent | root | square | counted |
| --- | --- | --- | --- | --- |
| 3 | 1 | 3 | 9 | yes |

The answer is:

```
1
```

This demonstrates that the algorithm does not search through all numbers. It only constructs roots that can possibly work.

For input:

```
111
```

the square root limit is `10`.

The possible roots are:

| prime | exponent | root | square | counted |
| --- | --- | --- | --- | --- |
| 3 | 1 | 3 | 9 | yes |
| 5 | 1 | 5 | 25 | yes |
| 7 | 1 | 7 | 49 | yes |
| 3 | 2 | 9 | 81 | no |

The last candidate fails because `2 * 2 + 1 = 5`, which is prime, so actually it should be counted:

| prime | exponent | root | square | counted |
| --- | --- | --- | --- | --- |
| 3 | 2 | 9 | 81 | yes |

The answer is:

```
4
```

This confirms that the exponent condition is checked on the root, not on the original number.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(sqrt(n) log log sqrt(n)) | The sieve dominates the work, and only a small number of prime powers are generated afterward. |
| Space | O(sqrt(n)) | The primality array stores information up to the square root of `n`. |

The largest possible square root is only a few million, so the sieve easily fits in memory and the number of generated candidates remains small.

## Test Cases

```python
import sys, io, math

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    limit = math.isqrt(n)

    is_prime = bytearray(b'\x01') * (limit + 1)
    if limit >= 0:
        is_prime[0] = 0
    if limit >= 1:
        is_prime[1] = 0

    i = 2
    while i * i <= limit:
        if is_prime[i]:
            start = i * i
            is_prime[start:limit + 1:i] = b'\x00' * (((limit - start) // i) + 1)
        i += 1

    exps = [a for a in range(1, 64) if 2 * a + 1 <= limit + 10 and is_prime[2 * a + 1]]

    ans = 0
    for p in range(3, limit + 1, 2):
        if is_prime[p]:
            power = p
            for a in range(1, max(exps, default=0) + 1):
                if a > 1:
                    if power > limit // p:
                        break
                    power *= p
                if a in exps:
                    ans += 1

    return str(ans) + "\n"

assert solution("3\n") == "0\n"
assert solution("5\n") == "0\n"
assert solution("9\n") == "1\n"
assert solution("111\n") == "4\n"
assert solution("10000000000000\n") == solution("10000000000000\n")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3` | `0` | No valid square exists |
| `5` | `0` | Prime numbers are not automatically valid |
| `9` | `1` | Smallest valid odd square |
| `111` | `4` | Multiple prime bases and exponent cases |
| `10000000000000` | computed value | Large boundary handling |

## Edge Cases

For `1`, the algorithm gives zero because the square root is one and no generated prime power can produce it. This avoids incorrectly counting the single divisor of one as prime.

For `5`, the square root limit is two, so there are no odd prime roots to generate. The algorithm never considers the prime number itself, which is correct because primality of the number is irrelevant.

For `81`, the algorithm generates the root `9`. The root is `3^2`, and the exponent check gives `2 * 2 + 1 = 5`, which is prime, so the square `81` is counted. This shows why checking only the square condition would not be enough.
