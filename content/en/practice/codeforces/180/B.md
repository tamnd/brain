---
title: "CF 180B - Divisibility Rules"
description: "We work in a positional numeral system with base b. For a divisor d, we must determine which kind of divisibility rule exists in this base. The problem defines several categories."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 180
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 116 (Div. 2, ACM-ICPC Rules)"
rating: 2300
weight: 180
solve_time_s: 110
verified: true
draft: false
---

[CF 180B - Divisibility Rules](https://codeforces.com/problemset/problem/180/B)

**Rating:** 2300  
**Tags:** math, number theory  
**Solve time:** 1m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We work in a positional numeral system with base `b`. For a divisor `d`, we must determine which kind of divisibility rule exists in this base.

The problem defines several categories.

A divisor belongs to the 2-type category if divisibility depends only on a fixed number of last digits. In decimal, divisibility by 8 depends only on the last three digits because powers of 10 eventually become divisible by 8.

A divisor belongs to the 3-type category if divisibility can be checked using the sum of digits. In decimal this works for 3 and 9 because `10 ≡ 1 (mod 3)` and `10 ≡ 1 (mod 9)`.

A divisor belongs to the 11-type category if divisibility can be checked using the alternating sum of digits. In decimal this works for 11 because `10 ≡ -1 (mod 11)`.

A divisor belongs to the 6-type category if it can be decomposed into independent factors whose rules come from different categories above. Decimal divisibility by 6 is the classic example: divisibility by 2 and by 3 simultaneously.

If none of these structures work, the divisor is classified as 7-type.

The task is not about constructing the rule itself. We only need to classify the divisor.

The bounds are tiny, both `b` and `d` are at most 100. That means even fairly brute-force number theoretic checks are completely safe. We can afford repeated gcd computations, factorizations, and modular simulations. What matters here is deriving the correct mathematical characterization.

The tricky part is understanding exactly when these rules exist in an arbitrary base.

Consider base 10 and divisor 8. Since `10^3` is divisible by 8, every digit except the last three contributes a multiple of 8. Only the suffix matters. This generalizes directly.

Another subtle case is divisibility by 3 in binary. Since `2 ≡ -1 (mod 3)`, powers of 2 alternate between `1` and `-1`. That means the divisibility rule is based on alternating sums, not ordinary digit sums. A careless implementation that only checks `b ≡ 1 (mod d)` for 3-type would incorrectly classify binary divisibility by 3 as 7-type.

A third edge case is mixed factorization. Suppose `b = 10` and `d = 66 = 2 * 3 * 11`. We have:

`2` gives a suffix rule,

`3` gives a digit-sum rule,

`11` gives an alternating-sum rule.

The whole divisor becomes 6-type. An implementation that checks only the whole divisor against one pattern would miss this decomposition.

One more dangerous situation is overlapping categories. In some bases a divisor can satisfy several conditions. The statement explicitly says we must output the earliest category in this order:

`2-type → 3-type → 11-type → 6-type → 7-type`

For example, if both digit-sum and alternating-sum rules work, we must print 3-type.

## Approaches

The brute-force way to think about the problem is to search directly for divisibility rules.

For 2-type, we could try increasing suffix lengths `k` and test whether every number with the same last `k` digits has the same remainder modulo `d`. This works exactly when `b^k` becomes divisible by `d`.

For 3-type, we could test whether replacing every digit by its sum preserves divisibility. Algebraically this means every power of `b` behaves like `1` modulo `d`.

For 11-type, we could test whether powers of `b` alternate between `1` and `-1` modulo `d`.

Then we could try all factorizations of `d` to detect 6-type behavior.

Even though the limits are small, directly simulating digit expansions is messy and unnecessary. The real structure comes from modular arithmetic.

Suppose a number in base `b` is

$$n = a_0 + a_1 b + a_2 b^2 + \dots$$

If `b ≡ 1 (mod d)`, then every power of `b` is also `1`, so

$$n \equiv a_0 + a_1 + a_2 + \dots \pmod d$$

This is exactly the digit-sum rule.

If `b ≡ -1 (mod d)`, then powers alternate between `1` and `-1`, giving the alternating-sum rule.

For suffix rules, if some power `b^k` is divisible by `d`, then all higher-place digits vanish modulo `d`. Only the last `k` digits matter.

That observation completely characterizes the first three categories.

The remaining insight is that 6-type divisors are precisely those whose prime-power factors can each be handled individually by one of the three rule families. Since the corresponding moduli are coprime, the Chinese Remainder Theorem lets us combine the rules.

So the whole problem reduces to prime factorization and checking each prime power against three modular conditions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(d³) or worse depending on simulation | O(1) | Unnecessarily complicated |
| Optimal | O(√d) | O(1) | Accepted |

## Algorithm Walkthrough

1. Factorize `d` into prime powers.

We write

$$d = p_1^{e_1} p_2^{e_2} \dots p_k^{e_k}$$

because divisibility behavior modulo coprime moduli can be analyzed independently.
2. Check whether `d` itself is 2-type.

A divisor has a suffix rule exactly when every prime factor of `d` also divides `b`. Equivalently, `d` divides some power of `b`.

We repeatedly divide out `gcd(d, b)` until no common factors remain. If the remaining value becomes `1`, then `d` is 2-type.
3. If it is 2-type, compute the minimum suffix length.

We need the smallest `k` such that

$$d \mid b^k$$

We repeatedly multiply by `b` modulo `d`, or equivalently repeatedly remove common factors, until the remaining divisor becomes `1`.
4. If not 2-type, check 3-type.

The digit-sum rule works exactly when

$$b \equiv 1 \pmod d$$

because then every positional weight equals `1`.
5. If not 3-type, check 11-type.

The alternating-sum rule works exactly when

$$b \equiv -1 \pmod d$$
6. If none of the above work, test for 6-type.

For every prime power factor `p^e` of `d`, check whether it individually belongs to one of the previous categories:

`2-type`, `3-type`, or `11-type`.

If every factor can be classified somehow, but the whole divisor itself could not, then the answer is 6-type.
7. Otherwise print 7-type.

### Why it works

Every divisibility rule described in the statement comes from the behavior of powers of the base modulo the divisor.

If powers eventually become zero modulo `d`, only a suffix matters.

If all powers equal `1`, digit sums work.

If powers alternate between `1` and `-1`, alternating sums work.

For coprime factors, these properties can be checked independently and combined through the Chinese Remainder Theorem. That means a divisor admits a mixed rule exactly when every prime-power component admits one of the basic rule types.

No other behaviors are allowed by the statement, so every divisor falls into exactly one reported category.

## Python Solution

```python
import sys
input = sys.stdin.readline

def factorize(n):
    res = []
    p = 2

    while p * p <= n:
        if n % p == 0:
            e = 0
            val = 1

            while n % p == 0:
                n //= p
                e += 1
                val *= p

            res.append(val)

        p += 1

    if n > 1:
        res.append(n)

    return res

def is_2_type(b, d):
    x = d

    while True:
        g = __import__("math").gcd(x, b)

        if g == 1:
            break

        x //= g

    return x == 1

def min_digits(b, d):
    k = 0
    x = d

    while x > 1:
        g = __import__("math").gcd(x, b)
        x //= g
        k += 1

    return k

def is_3_type(b, d):
    return b % d == 1 % d

def is_11_type(b, d):
    return b % d == (d - 1) % d

def solve():
    b, d = map(int, input().split())

    if is_2_type(b, d):
        print("2-type")
        print(min_digits(b, d))
        return

    if is_3_type(b, d):
        print("3-type")
        return

    if is_11_type(b, d):
        print("11-type")
        return

    parts = factorize(d)

    ok = True

    for x in parts:
        if not (
            is_2_type(b, x)
            or is_3_type(b, x)
            or is_11_type(b, x)
        ):
            ok = False
            break

    if ok:
        print("6-type")
    else:
        print("7-type")

solve()
```

The factorization step stores prime powers rather than individual primes. This matters because divisibility rules apply modulo full prime powers, not just modulo primes.

The `is_2_type` function repeatedly removes all factors shared with the base. If the entire divisor disappears, then every prime factor of `d` comes from `b`, so some power of `b` must be divisible by `d`.

The minimum suffix length computation mirrors the same logic. Each multiplication by `b` contributes another copy of the base's prime factors. Repeatedly dividing by `gcd(x, b)` tracks how many base digits are needed before the remaining divisor becomes `1`.

The modular checks for 3-type and 11-type are direct translations of the mathematical conditions:

`b ≡ 1 (mod d)` and `b ≡ -1 (mod d)`.

A subtle implementation detail is the order of checks. The statement requires the earliest category in priority order. Some divisors satisfy multiple conditions simultaneously, so the ordering cannot be changed.

## Worked Examples

### Example 1

Input:

```
10 10
```

Factorization gives:

$$10 = 2 \cdot 5$$

We test 2-type.

| Step | x | gcd(x, b) | New x |
| --- | --- | --- | --- |
| Start | 10 | 10 | 1 |

The divisor becomes `1`, so `10` is 2-type.

Now compute the minimum suffix length.

| Step | x | gcd(x, b) | k |
| --- | --- | --- | --- |
| Start | 10 | 10 | 1 |

Answer:

```
2-type
1
```

This demonstrates the standard decimal divisibility-by-10 rule: only the last digit matters.

### Example 2

Input:

```
2 3
```

We first test 2-type.

| Step | x | gcd(x, b) | Result |
| --- | --- | --- | --- |
| Start | 3 | 1 | stop |

Not 2-type.

Now check 3-type:

$$2 \not\equiv 1 \pmod 3$$

Fail.

Check 11-type:

$$2 \equiv -1 \pmod 3$$

Success.

Answer:

```
11-type
```

This is exactly the alternating-bit-sum rule for divisibility by 3 in binary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(√d) | Trial division factorization dominates |
| Space | O(1) | Only a few integers and factor lists are stored |

Since `d ≤ 100`, the running time is tiny. Even naive factorization completes instantly, and all modular checks are constant-time operations.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from math import gcd

def solve_io(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def factorize(n):
        res = []
        p = 2

        while p * p <= n:
            if n % p == 0:
                val = 1

                while n % p == 0:
                    n //= p
                    val *= p

                res.append(val)

            p += 1

        if n > 1:
            res.append(n)

        return res

    def is_2_type(b, d):
        x = d

        while True:
            g = gcd(x, b)

            if g == 1:
                break

            x //= g

        return x == 1

    def min_digits(b, d):
        x = d
        k = 0

        while x > 1:
            x //= gcd(x, b)
            k += 1

        return k

    def is_3_type(b, d):
        return b % d == 1 % d

    def is_11_type(b, d):
        return b % d == (d - 1) % d

    b, d = map(int, input().split())

    out = []

    if is_2_type(b, d):
        out.append("2-type")
        out.append(str(min_digits(b, d)))
    elif is_3_type(b, d):
        out.append("3-type")
    elif is_11_type(b, d):
        out.append("11-type")
    else:
        ok = True

        for x in factorize(d):
            if not (
                is_2_type(b, x)
                or is_3_type(b, x)
                or is_11_type(b, x)
            ):
                ok = False

        out.append("6-type" if ok else "7-type")

    return "\n".join(out) + "\n"

# provided sample
assert solve_io("10 10\n") == "2-type\n1\n"

# minimum values
assert solve_io("2 2\n") == "2-type\n1\n"

# binary divisibility by 3
assert solve_io("2 3\n") == "11-type\n"

# mixed rule: 66 = 2 * 3 * 11
assert solve_io("10 66\n") == "6-type\n"

# true 7-type
assert solve_io("10 7\n") == "7-type\n"

# power requiring multiple digits
assert solve_io("10 8\n") == "2-type\n3\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 2` | `2-type` with length 1 | Minimum boundary |
| `2 3` | `11-type` | Alternating-sum behavior |
| `10 66` | `6-type` | Mixed-factor classification |
| `10 7` | `7-type` | No supported rule exists |
| `10 8` | `2-type` with length 3 | Multi-digit suffix rule |

## Edge Cases

Consider input:

```
2 3
```

A naive implementation might only check whether `b ≡ 1 (mod d)` for digit-sum rules and otherwise conclude 7-type. Here:

$$2 \equiv -1 \pmod 3$$

so powers alternate:

$$2^0 = 1,\quad 2^1 = -1,\quad 2^2 = 1$$

The algorithm correctly detects the 11-type condition and prints:

```
11-type
```

Now consider:

```
10 66
```

The divisor itself satisfies none of the direct checks:

`66` does not divide any power of `10`,

`10 ≠ 1 (mod 66)`,

`10 ≠ -1 (mod 66)`.

A careless implementation would output 7-type.

The factorization step gives:

$$66 = 2 \cdot 3 \cdot 11$$

Each factor individually has a rule:

`2` is 2-type,

`3` is 3-type,

`11` is 11-type.

Since every component is covered, the algorithm outputs:

```
6-type
```

Finally, consider:

```
10 8
```

The divisor is 2-type because powers of 10 eventually become divisible by 8.

The minimum suffix length matters. We compute:

| Step | Remaining divisor |
| --- | --- |
| Start | 8 |
| Divide by gcd(8,10)=2 | 4 |
| Divide by gcd(4,10)=2 | 2 |
| Divide by gcd(2,10)=2 | 1 |

Three steps are needed, so the correct answer is:

```
2-type
3
```

A buggy implementation that only counts distinct prime factors would incorrectly output `1`.
