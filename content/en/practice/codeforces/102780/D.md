---
title: "CF 102780D - Power play"
description: "We need find the smallest positive integer x such that the power of a with exponent x is equal to the power of x with exponent b. The two input values are the bases involved in this equation, and the answer is the smallest valid x not exceeding 10^18."
date: "2026-07-27T20:07:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102780
codeforces_index: "D"
codeforces_contest_name: "ICPC Central Russia Regional Contest (CRRC 19)"
rating: 0
weight: 102780
solve_time_s: 71
verified: true
draft: false
---

[CF 102780D - Power play](https://codeforces.com/problemset/problem/102780/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We need find the smallest positive integer x such that the power of a with exponent x is equal to the power of x with exponent b. The two input values are the bases involved in this equation, and the answer is the smallest valid x not exceeding 10^18. If no such integer exists, we print 0.

The values of a and b are at most 10000, so the search space for the input itself is tiny, but x can be extremely large. A direct search over possible x values is impossible because the answer may be close to the upper limit of 10^18. The solution must use the mathematical structure of the equation rather than trying candidates one by one.

The main hidden difficulty is that x appears both as a base and as an exponent. A careless solution may try to compare floating point logarithms, but precision errors can change an equality check into an incorrect result. Another common mistake is assuming that a solution always exists because some small examples work.

For example, input `2 6` has no solution and the correct output is `0`. A search that only checks a small number of candidates might incorrectly stop too early and miss the fact that no value works.

Another edge case is when the valid x is not equal to a. For input `2 4`, the answer is `16`, because `2^16 = 16^4`. Guessing x from the base or checking only x values related to a misses the actual solution.

A third case appears when the prime factors of a have common exponent structure. For input `100 20`, the answer is `10`. The solution comes from reducing the prime exponents of a, not from trying values close to a.

## Approaches

A brute force solution would test every integer x from 1 to 10^18 and check whether `a^x = x^b`. The equality check can be done with integer arithmetic, so the method would be correct, but the number of candidates is far beyond what a program can process. Even one operation per candidate would require around 10^18 operations, while a one second limit allows only a much smaller number of operations.

The useful observation comes from looking at prime factors. Suppose the prime factorization of a is:

```
a = p1^c1 * p2^c2 * ... * pk^ck
```

The right side of the equation is `x^b`, so every prime factor of x must already appear in a. If x contained a new prime, that prime would appear on the right side but not on the left.

For every prime pi, let its exponent in x be ei. Comparing prime exponents in both sides gives:

```
x * ci = b * ei
```

This means every exponent ei is controlled by x. We first remove the common divisor shared by b and all exponents of a. Let:

```
g = gcd(b, c1, c2, ..., ck)
```

Then:

```
b = g * b'
ci = g * ci'
```

The equations become:

```
ei = x * ci' / b'
```

so b' must divide x. Write:

```
x = b' * n
```

Substituting this into the exponent formula gives:

```
ei = n * ci'
```

Therefore:

```
x = p1^(n*c1') * p2^(n*c2') * ... * pk^(n*ck')
```

This can be rewritten as:

```
x = (p1^c1' * p2^c2' * ... * pk^ck')^n
```

Let:

```
q = p1^c1' * p2^c2' * ... * pk^ck'
```

Now the whole problem becomes finding a positive integer n satisfying:

```
q^n = b' * n
```

The value of q is at least 2. Because x = q^n must not exceed 10^18, n can only be around 60 at most. We can simply test all possible n values in this small range.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(10^18) | O(1) | Too slow |
| Optimal | O(log(10^18) + sqrt(a)) | O(number of prime factors of a) | Accepted |

## Algorithm Walkthrough

1. Factorize a and store each prime exponent. This gives the values ci needed for comparing prime powers on both sides of the equation.
2. Compute `g`, the greatest common divisor of b and every exponent from the factorization of a. Dividing by g removes the unnecessary shared part and leaves the reduced values b' and ci'.
3. Build q using the reduced exponents:

```
q = product of p^(ci/g)
```

This value represents the base whose powers can become x after the reduction.

1. Try increasing values of n starting from 1. For each n, compute `q^n` while stopping if it exceeds 10^18. If:

```
q^n == b' * n
```

then `q^n` is a valid x. Since n is checked in increasing order and q is greater than 1, the first answer found is the smallest one.

1. If all possible values of n fail, output 0 because no valid x exists within the allowed range.

Why it works:

The prime factor comparison transforms the original equation into a much smaller equation. Every possible solution must have the form `x = q^n`, and every valid n must satisfy `q^n = b'n`. The algorithm checks exactly these possible values, so it cannot miss a solution. Since the search starts from the smallest n, the first match gives the smallest possible x.

## Python Solution

```python
import sys
input = sys.stdin.readline

LIMIT = 10**18

def factorize(x):
    factors = []
    d = 2
    while d * d <= x:
        if x % d == 0:
            cnt = 0
            while x % d == 0:
                x //= d
                cnt += 1
            factors.append((d, cnt))
        d += 1 if d == 2 else 2
    if x > 1:
        factors.append((x, 1))
    return factors

def solve():
    a, b = map(int, input().split())

    factors = factorize(a)

    g = b
    for _, c in factors:
        g = __import__("math").gcd(g, c)

    b_red = b // g

    q = 1
    for p, c in factors:
        q *= p ** (c // g)

    power = 1
    n = 1
    while True:
        power *= q
        if power > LIMIT:
            break

        if power == b_red * n:
            print(power)
            return

        n += 1

    print(0)

if __name__ == "__main__":
    solve()
```

The factorization function extracts the prime representation of a. The input limit of 10000 makes trial division easily fast enough.

The greatest common divisor calculation reduces the exponents exactly as derived in the proof. The variable `q` stores the reduced base, so every candidate answer has the form generated by repeatedly multiplying by q.

The loop starts with `power = q`, representing n equal to 1. Each iteration increases n by one and updates q^n. Once the value exceeds 10^18, later values are even larger because q is at least 2, so the search can stop safely.

All calculations use Python integers, so there is no overflow risk. The explicit limit check prevents unnecessary growth of huge powers.

## Worked Examples

For the input `2 4`, the factorization is:

| n | q^n | b' * n | Result |
| --- | --- | --- | --- |
| 1 | 2 | 4 | Not equal |
| 2 | 4 | 8 | Not equal |
| 3 | 8 | 12 | Not equal |
| 4 | 16 | 16 | Found |

Here `g = gcd(4, 1) = 1`, so `q = 2` and `b' = 4`. The first matching n is 4, giving x = 16.

For the input `2 6`, the reduced equation is:

| n | q^n | b' * n | Result |
| --- | --- | --- | --- |
| 1 | 2 | 6 | Not equal |
| 2 | 4 | 12 | Not equal |
| 3 | 8 | 18 | Not equal |
| 4 | 16 | 24 | Not equal |
| 5 | 32 | 30 | Not equal |
| 6 | 64 | 36 | Not equal |

The powers of 2 eventually grow faster than the linear expression 6n, and no equality appears before the value limit is reached. The algorithm prints 0.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(sqrt(a) + log(10^18)) | Factorization checks divisors up to sqrt(a), and the search tries only about 60 values of n |
| Space | O(k) | The factor list stores only the prime factors of a |

The constraints on a and b make factorization inexpensive. The transformed search space is tiny because the answer is bounded by 10^18 and q is at least 2, so the algorithm easily fits within the limits.

## Test Cases

```python
import sys
import io
import math

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    a, b = map(int, input().split())

    def factorize(x):
        factors = []
        d = 2
        while d * d <= x:
            if x % d == 0:
                cnt = 0
                while x % d == 0:
                    x //= d
                    cnt += 1
                factors.append((d, cnt))
            d += 1 if d == 2 else 2
        if x > 1:
            factors.append((x, 1))
        return factors

    factors = factorize(a)
    g = b
    for _, c in factors:
        g = math.gcd(g, c)

    b_red = b // g
    q = 1
    for p, c in factors:
        q *= p ** (c // g)

    power = 1
    n = 1
    while True:
        power *= q
        if power > 10**18:
            break
        if power == b_red * n:
            return str(power)
        n += 1

    return "0"

assert solution("2 4") == "16", "sample 1"
assert solution("2 6") == "0", "sample 2"
assert solution("2 32") == "256", "sample 3"
assert solution("100 20") == "10", "sample 4"

assert solution("2 3") == "0", "no solution at small values"
assert solution("10000 9999") == "0", "maximum input size"
assert solution("8 4") == "0", "equal prime exponent pattern"
assert solution("4 8") == "16", "reduced exponent boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 3` | `0` | Smallest values with no valid solution |
| `10000 9999` | `0` | Large input values and quick rejection |
| `8 4` | `0` | Cases where common exponent structure does not create an answer |
| `4 8` | `16` | Reduction of exponents and finding a non-trivial solution |

## Edge Cases

For `2 6`, the algorithm finds `g = 1`, `q = 2`, and `b' = 6`. It checks all possible n values while `2^n` stays below the limit. No value satisfies `2^n = 6n`, so it outputs 0. This handles the situation where a valid-looking equation has no integer solution.

For `2 4`, the algorithm does not assume the answer is close to a. It builds the reduced equation `2^n = 4n`, finds n equal to 4, and returns `2^4 = 16`. This confirms that the generated x can be much larger than the original base.

For `100 20`, the factorization gives `100 = 2^2 * 5^2`. The gcd of b and the exponents is 2, producing `q = 10` and `b' = 10`. The first check gives `10^1 = 10 * 1`, so the algorithm returns 10 immediately. This covers the case where reducing the prime exponents creates a small solution.

I can also adapt this editorial into a shorter Codeforces-style version if you want a more compact contest publication format.
