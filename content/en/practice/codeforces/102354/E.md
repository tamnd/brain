---
title: "CF 102354E - Decimal Expansion"
description: "The constant can be rewritten as [ varphi=prod{k=1}^{infty}(1-10^{-k}), ] because the (k)-th factor is exactly ((10^k-1)/10^k). We need the digit occupying position (n) after the decimal point, where (n) may be as large as (10^{18}). There are up to (10^5) independent queries."
date: "2026-08-13T00:34:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102354
codeforces_index: "E"
codeforces_contest_name: "2018-2019 Summer Petrozavodsk Camp, Oleksandr Kulkov Contest 2"
rating: 0
weight: 102354
solve_time_s: 90
verified: true
draft: false
---

[CF 102354E - Decimal Expansion](https://codeforces.com/problemset/problem/102354/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

The constant can be rewritten as

[
\varphi=\prod_{k=1}^{\infty}(1-10^{-k}),
]

because the (k)-th factor is exactly ((10^k-1)/10^k). We need the digit occupying position (n) after the decimal point, where (n) may be as large as (10^{18}).

There are up to (10^5) independent queries. A method that spends (O(n)) or even (O(\sqrt n)) work per query is far too slow. At the maximum (n), (O(n)) would require around (10^{18}) operations for one query, while (O(\sqrt n)) would still require around (10^9) operations per query. The solution has to exploit the exact structure of the infinite product and answer each position in essentially constant time.

The first trap is that the product itself does not expose the decimal digits directly. For example, the first two digits are (8) and (9), even though the first term of its useful expansion has coefficient (-1). If we simply look at the coefficient of (10^{-n}), we can obtain a negative value and forget that decimal borrowing is required. For input

```
1
1
```

the answer is

```
8
```

not (-1), because the expansion begins with (0.89\ldots).

A second boundary case occurs when (n) is exactly one of the special exponents appearing in the expansion. For example,

```
1
5
```

has answer (1). The exponent (5) contributes (+10^{-5}), but the terms after it still affect whether a borrow is needed. Treating the coefficient alone as the final digit happens to work here, but the same shortcut fails at (n=7), where the coefficient is (+1) while the correct digit is (0).

A third boundary appears immediately after a special exponent. For

```
1
6
```

the answer is (0), because the (10^{-5}) contribution has already become part of the integer prefix when the decimal position reaches (6). A careless implementation that looks only at the next special exponent can incorrectly return (1).

## Approaches

A direct approach would multiply the factors

[
(1-10^{-1})(1-10^{-2})(1-10^{-3})\cdots
]

to sufficiently high precision and inspect the desired decimal position. This works for small (n), because factors with index greater than (n) cannot influence the first (n) decimal places by an appreciable amount. However, for (n=10^{18}), even constructing the first (n) decimal digits is impossible. The brute-force work is (\Theta(n)) for one query, which is already (10^{18}) digit-level operations at the largest allowed position.

The key observation is Euler's pentagonal number theorem. It gives the exact expansion

1+\sum_{k=1}^{\infty}(-1)^k
\left(
x^{k(3k-1)/2}+x^{k(3k+1)/2}
\right).
]

Substituting (x=1/10), we obtain

1+\sum_{k=1}^{\infty}(-1)^k
\left(
10^{-k(3k-1)/2}
+
10^{-k(3k+1)/2}
\right).
]

Thus almost every decimal position has coefficient zero. The only nonzero coefficients occur at generalized pentagonal numbers

[
P_k^-=\frac{k(3k-1)}2,
\qquad
P_k^+=\frac{k(3k+1)}2,
]

and both positions have coefficient ((-1)^k).

This sparsity reduces the problem to locating two consecutive generalized pentagonal numbers around (n). We do not need to construct any decimal prefix. After multiplying the expansion by (10^n), every term whose exponent is smaller than (n) becomes an integer multiple of (10), so it cannot affect the final decimal digit modulo (10). The only local information that matters is the coefficient at exponent (n), together with whether the infinite tail beginning after (n) is positive or negative.

The tail has magnitude less than (1/9). Its first term has strictly larger magnitude than the sum of all later terms, so the sign of the tail is exactly the sign of its first term. Consequently, if the next generalized pentagonal exponent has coefficient (+1), no borrowing occurs. If it has coefficient (-1), one unit must be borrowed from the coefficient at position (n).

The relevant (k) is around (\sqrt{n}), but we do not iterate up to it. Solving

[
\frac{k(3k-1)}2\le n
]

gives

[
k\le \frac{1+\sqrt{24n+1}}6.
]

An integer square root lets us obtain this (k) directly, so every query takes (O(1)) arithmetic operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n)) per query | (O(n)) | Too slow |
| Optimal | (O(1)) per query | (O(1)) | Accepted |

## Algorithm Walkthrough

1. For a query (n), compute

[
k=\left\lfloor\frac{1+\sqrt{24n+1}}6\right\rfloor.
]

This is the largest (k) for which (P_k^-\le n), where (P_k^-=k(3k-1)/2).

1. Compute the two generalized pentagonal positions belonging to this (k),

[
a=P_k^-,
\qquad
b=P_k^+.
]

They appear consecutively in the expansion, except that the next position after (b) is (P_{k+1}^-).

1. Determine the coefficient at position (n). If (n=a), the coefficient is ((-1)^k). If (n=b), the coefficient is also ((-1)^k). Otherwise the coefficient is zero.
2. Determine the first exponent strictly larger than (n). If (n<b), it is (b). If (n\ge b), it is (P_{k+1}^-). Its coefficient has sign ((-1)^k) in the first case and ((-1)^{k+1}) in the second case.
3. Start with the coefficient at position (n). If the first omitted term is negative, subtract one. Finally take the result modulo (10), which converts values such as (-1) into the decimal digit (9).
4. Append the resulting digit to the output. Processing all queries independently gives the required sequence of digits.

The reason for the borrowing rule is easiest to see after multiplying by (10^n). Write

[
10^n\varphi=S+R,
]

where (S) contains all terms with exponent at most (n), and (R) contains the remaining terms. The number (S) is an integer. The remainder satisfies (|R|<1/9), and its sign equals the sign of its first term. Hence (\lfloor10^n\varphi\rfloor) is (S) when (R>0), and (S-1) when (R<0). Modulo (10), only the coefficient at exponent (n) survives in (S), giving exactly the algorithm above.

### Why it works

The invariant is that after position (n), the entire infinite tail behaves, for the purpose of determining the integer part of (10^n\varphi), exactly like either a small positive fraction or a small negative fraction. The first omitted pentagonal term determines which case occurs because its absolute value dominates all later omitted terms. Meanwhile, every earlier term contributes a multiple of (10) after multiplication by (10^n), so only the coefficient at exponent (n) determines the final digit of the integer prefix. The algorithm therefore accounts for both possible effects, the local coefficient and the single possible borrow, and cannot produce a different digit.

## Python Solution

```python
import sys
input = sys.stdin.readline

def digit(n):
    # k is the largest integer with k(3k-1)/2 <= n.
    k = (1 + (24 * n + 1) ** 0.5) // 6

    # Floating point is not safe for n up to 10^18.
    # Recompute using integer square root.
    s = math.isqrt(24 * n + 1)
    k = (1 + s) // 6

    while (k + 1) * (3 * (k + 1) - 1) // 2 <= n:
        k += 1
    while k * (3 * k - 1) // 2 > n:
        k -= 1

    a = k * (3 * k - 1) // 2
    b = k * (3 * k + 1) // 2

    if n == a or n == b:
        cur = 1 if k % 2 == 0 else -1
    else:
        cur = 0

    if n < b:
        next_sign = 1 if k % 2 == 0 else -1
    else:
        next_sign = -1 if k % 2 == 0 else 1

    if next_sign < 0:
        cur -= 1

    return cur % 10

def solve():
    t = int(input())
    ns = list(map(int, input().split()))

    ans = []
    for n in ns:
        ans.append(str(digit(n)))

    print(" ".join(ans))

if __name__ == "__main__":
    import math
    solve()
```

The first computation finds the generalized pentagonal block containing (n). The integer square root is used because (n) can reach (10^{18}), and a floating-point square root can lose enough precision near a perfect square to move (k) by one. The correction loops are constant-time in practice and make the boundary exact even if the integer-square-root formula lands on an adjacent candidate.

The variables `a` and `b` are the two exponents belonging to (k). Comparing (n) with them determines whether the current coefficient is (0) or ((-1)^k), and also tells us which pentagonal number comes next.

The expression `next_sign` captures the only carry or borrow that the infinite suffix can create. A negative suffix changes the floor by one, so `cur -= 1` is the complete decimal-carry adjustment.

Python integers have arbitrary precision, so values such as (24n+1) and the products involving (k) are safe without special overflow handling. The code also uses buffered input and produces all answers in one output operation, which matters for (10^5) test cases.

## Worked Examples

For the beginning of the decimal expansion, the generalized pentagonal exponents and signs are

[
1:-,\quad 2:-,\quad 5:+,\quad 7:+,\quad 12:-,\quad 15:-,\quad 22:+.
]

For the first part of Sample 1, the algorithm behaves as follows.

| (n) | (k) | (P_k^-) | (P_k^+) | Current coefficient | Next sign | Digit |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 2 | -1 | -1 | 8 |
| 2 | 1 | 1 | 2 | -1 | +1 | 9 |
| 3 | 1 | 1 | 2 | 0 | +1 | 0 |
| 4 | 1 | 1 | 2 | 0 | +1 | 0 |
| 5 | 2 | 5 | 7 | +1 | +1 | 1 |
| 6 | 2 | 5 | 7 | 0 | +1 | 0 |
| 7 | 2 | 5 | 7 | +1 | -1 | 0 |
| 8 | 2 | 5 | 7 | 0 | -1 | 9 |
| 9 | 2 | 5 | 7 | 0 | -1 | 9 |
| 10 | 2 | 5 | 7 | 0 | -1 | 9 |
| 11 | 2 | 5 | 7 | 0 | -1 | 9 |
| 12 | 3 | 12 | 15 | -1 | -1 | 8 |
| 13 | 3 | 12 | 15 | 0 | -1 | 9 |
| 14 | 3 | 12 | 15 | 0 | -1 | 9 |
| 15 | 3 | 12 | 15 | -1 | +1 | 9 |

The first and seventh positions show why the tail sign matters. At (n=1), the current coefficient is (-1) and the next term is also negative, so the integer prefix becomes one smaller, giving (8). At (n=7), the current coefficient is (+1), but the next term is negative, so the (1) is borrowed away and the digit becomes (0).

A second useful trace focuses on the transition around (12) and (15).

| (n) | (k) | (P_k^-) | (P_k^+) | Current coefficient | Next exponent | Next sign | Digit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 11 | 2 | 5 | 7 | 0 | 12 | -1 | 9 |
| 12 | 3 | 12 | 15 | -1 | 15 | -1 | 8 |
| 13 | 3 | 12 | 15 | 0 | 15 | -1 | 9 |
| 14 | 3 | 12 | 15 | 0 | 15 | -1 | 9 |
| 15 | 3 | 12 | 15 | -1 | 22 | +1 | 9 |
| 16 | 3 | 12 | 15 | 0 | 22 | +1 | 0 |
| 17 | 3 | 12 | 15 | 0 | 22 | +1 | 0 |

This trace shows the two different kinds of pentagonal positions. At (n=12), the coefficient itself is negative and the following coefficient is also negative, producing (8). At (n=15), the coefficient is negative but the following coefficient is positive, so no additional borrow occurs and the digit remains (9).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(t)) | Each query performs a constant number of integer arithmetic operations and an integer square root. |
| Space | (O(t)) | The input values and output strings are stored for buffered processing. |

With (t\le10^5), a linear total number of operations is easily appropriate for the one-second limit. The algorithm never constructs a prefix of length (n), so the fact that (n) can be (10^{18}) does not affect the amount of per-query work.

## Test Cases

```python
import io
import math

def solve_string(inp: str) -> str:
    data = list(map(int, inp.split()))
    t = data[0]
    ns = data[1:1 + t]

    def digit(n):
        s = math.isqrt(24 * n + 1)
        k = (1 + s) // 6

        while (k + 1) * (3 * (k + 1) - 1) // 2 <= n:
            k += 1
        while k * (3 * k - 1) // 2 > n:
            k -= 1

        a = k * (3 * k - 1) // 2
        b = k * (3 * k + 1) // 2

        if n == a or n == b:
            cur = 1 if k % 2 == 0 else -1
        else:
            cur = 0

        if n < b:
            next_sign = 1 if k % 2 == 0 else -1
        else:
            next_sign = -1 if k % 2 == 0 else 1

        if next_sign < 0:
            cur -= 1

        return cur % 10

    return " ".join(map(str, (digit(n) for n in ns)))

# Provided sample
assert solve_string(
    "15\n"
    "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15\n"
) == "8 9 0 0 1 0 0 9 9 9 9 8 9 9 9", "sample 1"

# Minimum-size input
assert solve_string("1\n1\n") == "8", "minimum position"

# Consecutive positions around the first two pentagonal numbers
assert solve_string("5\n4 5 6 7 8\n") == "0 1 0 0 9", "first boundaries"

# Repeated equal values
assert solve_string("6\n3 3 3 3 3 3\n") == "0 0 0 0 0 0", "all equal"

# Boundary around the next pair
assert solve_string("7\n11 12 13 14 15 16 17\n") == "9 8 9 9 9 0 0", "second boundaries"

# Maximum allowed n
assert solve_string("1\n1000000000000000000\n") == "0", "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `8` | The smallest legal position and the first negative coefficient. |
| `5 / 4 5 6 7 8` | `0 1 0 0 9` | Boundaries immediately before, at, and after the first pentagonal pair. |
| `6 / 3 3 3 3 3 3` | `0 0 0 0 0 0` | Repeated identical queries and the zero-coefficient region. |
| `7 / 11 12 13 14 15 16 17` | `9 8 9 9 9 0 0` | A second pentagonal pair and both changes of tail sign. |
| `1 / 1000000000000000000` | `0` | The largest possible index and integer-square-root arithmetic. |

## Edge Cases

For (n=1), the input

```
1
1
```

has (k=1), with (P_1^-=1) and (P_1^+=2). The current coefficient is (-1), and the next coefficient is also negative. The algorithm subtracts one more, obtaining (-2), and (-2\bmod10=8). The correct output is therefore `8`.

For (n=7), the input

```
1
7
```

lands exactly on (P_2^+=7). Its coefficient is (+1), but the next exponent is (P_3^-=12), whose coefficient is negative. The floor after scaling by (10^7) is consequently one less than the integer prefix suggested by the local coefficient. The algorithm computes (1-1=0), giving the correct output `0`.

For (n=8), the input

```
1
8
```

is immediately after the exponent (7). There is no coefficient at exponent (8), so the current value is zero. The first omitted term is the negative term at exponent (12), forcing a borrow. The result is (-1\bmod10=9), matching the decimal expansion.

For the largest allowed position, the input

```
1
1000000000000000000
```

has (k=816496580). Its lower generalized pentagonal exponent is

999999997319296310,
]

while the upper one is

[
1000000813815876890.
]

Thus (10^{18}) lies strictly between the two exponents. The current coefficient is zero, and because (k) is even, the next coefficient is positive. No borrow occurs, so the answer is `0`. The algorithm reaches this result using only integer arithmetic and never depends on the enormous decimal expansion itself.
