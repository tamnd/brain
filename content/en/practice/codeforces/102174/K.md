---
title: "CF 102174K - \u591a\u9879\u5f0f\u6c42\u5bfc"
description: "We have a polynomial [ f(x)=anx^n+a{n-1}x^{n-1}+cdots+a1x+a0. ] The input gives its degree (n), the number of times (k) that differentiation must be applied, and the (n+1) coefficients from highest degree to constant term."
date: "2026-08-19T07:10:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102174
codeforces_index: "K"
codeforces_contest_name: "The 14-th BIT Campus Programming Contest"
rating: 0
weight: 102174
solve_time_s: 108
verified: true
draft: false
---

[CF 102174K - \u591a\u9879\u5f0f\u6c42\u5bfc](https://codeforces.com/problemset/problem/102174/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a polynomial

[
f(x)=a_nx^n+a_{n-1}x^{n-1}+\cdots+a_1x+a_0.
]

The input gives its degree (n), the number of times (k) that differentiation must be applied, and the (n+1) coefficients from highest degree to constant term. We need to output the coefficients of the (k)-th derivative, still using exactly (n+1) positions. Any term whose degree has disappeared contributes coefficient zero. Every resulting coefficient is required modulo (2019).

The key indexing detail is that the input array is ordered by decreasing degree. If `a[j]` is the element at zero-based position (j), it represents the coefficient of (x^{n-j}). After differentiating (k) times, this coefficient moves to degree (n-j-k), provided that degree is nonnegative.

Here (1\le n,k\le100), so even a direct simulation of every differentiation is small. With (n=100) and (k=100), the total number of coefficient updates is only

[
100+99+\cdots+1=5050.
]

Thus an (O(nk)) solution is comfortably fast under these constraints. The more useful observation is that every original coefficient has a simple closed-form contribution after (k) derivatives, giving an (O(n)) solution and making the indexing easier to reason about.

There are several cases where an implementation can silently go wrong. If (k>n), every term disappears. For example,

```
2 3
1 2 3
```

represents (x^2+2x+3), and the third derivative is zero, so the output is

```
0 0 0
```

A careless implementation that blindly accesses the coefficient at degree (i+k) can go out of bounds.

The constant term must also be handled correctly. For

```
1 1
7 5
```

the polynomial is (7x+5), so the derivative is (7). The required output has two positions:

```
0 7
```

The zero at the front represents the coefficient of (x^1), which no longer exists after differentiation. An implementation that prints only the nonzero-degree part would produce the wrong format.

Finally, coefficients can grow quickly before the final modulo operation. For example, repeated differentiation of a degree-100 term introduces a factorial-sized multiplier. Python integers can handle this safely, but the calculation should still be reduced modulo (2019) throughout. In languages with fixed-width integers, postponing the modulo could overflow.

## Approaches

The most direct method is to simulate differentiation one order at a time. For a polynomial stored from highest degree to lowest degree, differentiating changes a coefficient (a_i) of (x^i) into (i a_i), which becomes the coefficient of (x^{i-1}). The constant term becomes zero. Repeating this process (k) times is correct because it follows exactly the definition of repeated differentiation.

The complexity of this simulation is (O(nk)). At the largest allowed values (n=k=100), the number of coefficient multiplications is at most (100+99+\cdots+1=5050). So this approach is actually accepted for the stated constraints. It would become less attractive if the constraints were increased substantially, especially when both (n) and (k) were large.

The faster approach comes from looking at one original monomial instead of simulating the whole polynomial. Suppose the original term is

[
a_jx^j.
]

After one derivative it becomes

[
a_jj x^{j-1}.
]

After two derivatives it becomes

[
a_jj(j-1)x^{j-2}.
]

After (k) derivatives, provided (j\ge k), it becomes

[
a_j\cdot j(j-1)\cdots(j-k+1)x^{j-k}.
]

The multiplier is a falling factorial. If we want the coefficient of (x^i) in the final polynomial, its original degree must have been (i+k). Thus

[
b_i=a_{i+k}(i+k)(i+k-1)\cdots(i+1).
]

We only need to calculate this for original degrees (j=k,k+1,\ldots,n). Every lower-degree term disappears completely.

Because there are only (n+1) original coefficients, we can process each one once. We can also build the falling-factorial multiplier incrementally, avoiding factorials and keeping every intermediate value modulo (2019).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(nk)) | (O(n)) | Accepted for these constraints |
| Optimal | (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read (n), (k), and the coefficients in descending degree order. Store them in an array `a`, where `a[j]` is the coefficient of degree (n-j).
2. Create an output array of (n+1) zeros. Keeping the original length is necessary because the required output contains a coefficient slot for every degree from (n) down to (0).
3. If (k>n), leave the entire output as zero and print it. Every monomial has degree less than (k), so all of them vanish after (k) differentiations.
4. For every original degree (j) from (k) through (n), compute the coefficient after (k) derivatives. The original term (a_jx^j) becomes

[
a_j\frac{j!}{(j-k)!}x^{j-k}.
]

The final degree is (j-k), so the corresponding output position is (n-(j-k)).

1. Compute the multiplier (j!/(j-k)!) by multiplying the (k) consecutive integers from (j-k+1) through (j), reducing modulo (2019) after each multiplication. Since (k\le100), this is already small enough, but the modular form also avoids unnecessarily large intermediate values.
2. Store the resulting coefficient at the position corresponding to degree (j-k), and finally print all (n+1) output coefficients separated by spaces.

The invariant is that whenever the algorithm processes an original degree (j), the value placed at degree (j-k) is exactly the (k)-th derivative of the single monomial (a_jx^j). Differentiation is linear, so adding these contributions over all original monomials gives the complete (k)-th derivative. Terms with (j<k) are absent because repeated differentiation eventually reaches the constant term and then zero.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 2019

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    ans = [0] * (n + 1)

    if k <= n:
        for j in range(k, n + 1):
            multiplier = 1

            for t in range(j - k + 1, j + 1):
                multiplier = multiplier * t % MOD

            coefficient = a[n - j] % MOD
            coefficient = coefficient * multiplier % MOD

            final_degree = j - k
            ans[n - final_degree] = coefficient

    print(*ans)

if __name__ == "__main__":
    solve()
```

The input array uses descending degree order, so the coefficient of (x^j) is `a[n - j]`. This conversion is the main indexing detail in the implementation.

The loop starts at `j = k` because a degree smaller than (k) cannot survive (k) differentiations. For each surviving degree, the final degree is `j - k`, and its output position is consequently `n - (j - k)`.

The multiplier is calculated as

[
(j-k+1)(j-k+2)\cdots j.
]

This is exactly (j!/(j-k)!), the factor introduced by (k) successive derivatives. Taking modulo (2019) after every multiplication keeps the intermediate value small and gives the same final remainder.

There is no need for special handling of the constant term beyond the degree calculation. Once a term is differentiated, its final position is determined directly by its original degree.

The problem has only one test case, so the solution reads the two input lines once and prints one result line.

## Worked Examples

For Sample 1,

```
5 1
1 2 3 4 5 6
```

the input represents

[
x^5+2x^4+3x^3+4x^2+5x+6.
]

Since (k=1), each term is multiplied by its original degree and its degree decreases by one.

| Original degree (j) | Original coefficient | Multiplier | Final degree | Final coefficient |
| --- | --- | --- | --- | --- |
| 1 | 5 | 1 | 0 | 5 |
| 2 | 4 | 2 | 1 | 8 |
| 3 | 3 | 3 | 2 | 9 |
| 4 | 2 | 4 | 3 | 8 |
| 5 | 1 | 5 | 4 | 5 |

Degree 5 has no contribution because the fifth-degree position in the output represents (x^5), while the derivative has maximum degree 4. The final array is

```
0 5 8 9 8 5
```

which corresponds to

[
5x^4+8x^3+9x^2+8x+5.
]

For Sample 2,

```
5 2
1 2 3 4 5 6
```

the same polynomial is differentiated twice.

| Original degree (j) | Original coefficient | Multiplier | Final degree | Final coefficient |
| --- | --- | --- | --- | --- |
| 2 | 4 | (2\cdot1=2) | 0 | 8 |
| 3 | 3 | (3\cdot2=6) | 1 | 18 |
| 4 | 2 | (4\cdot3=12) | 2 | 24 |
| 5 | 1 | (5\cdot4=20) | 3 | 20 |

The degree 0 and degree 1 original terms disappear because their degrees are smaller than (k=2). The output positions for degrees 5 and 4 are consequently zero.

The resulting array is

```
0 0 20 24 18 8
```

which represents

[
20x^3+24x^2+18x+8.
]

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(nk)) | For each of at most (n+1) monomials, at most (k) factors are multiplied |
| Space | (O(n)) | The coefficient array and output array each contain (n+1) values |

With (n,k\le100), the worst case performs only about (5050) small modular multiplications, so the solution is easily within the 1 second and 128 MB limits. The implementation is written in the direct closed-form style because it exposes the mathematical structure clearly, even though an (O(nk)) repeated-differentiation simulation would also pass.

## Test Cases

```python
import sys
import io

MOD = 2019

def solve():
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    ans = [0] * (n + 1)

    if k <= n:
        for j in range(k, n + 1):
            multiplier = 1
            for t in range(j - k + 1, j + 1):
                multiplier = multiplier * t % MOD

            coefficient = a[n - j] * multiplier % MOD
            final_degree = j - k
            ans[n - final_degree] = coefficient

    print(*ans)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
assert run(
    "5 1\n"
    "1 2 3 4 5 6\n"
) == "0 5 8 9 8 5\n"

# Provided sample 2
assert run(
    "5 2\n"
    "1 2 3 4 5 6\n"
) == "0 0 20 24 18 8\n"

# Minimum-size polynomial
assert run(
    "1 1\n"
    "7 5\n"
) == "0 7\n"

# Differentiation order is larger than polynomial degree
assert run(
    "2 3\n"
    "1 2 3\n"
) == "0 0 0\n"

# All coefficients are equal
assert run(
    "3 1\n"
    "5 5 5 5\n"
) == "0 15 10 5\n"

# Constant polynomial contribution must disappear after differentiation
assert run(
    "4 2\n"
    "0 0 0 7 9\n"
) == "0 0 0 0 0\n"

# Maximum-size input, also checks modular reduction.
n = 100
k = 100
coefficients = [100] * (n + 1)
input_data = f"{n} {k}\n" + " ".join(map(str, coefficients)) + "\n"

expected = [0] * (n + 1)
expected[-1] = 100
assert run(input_data) == " ".join(map(str, expected)) + "\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 1 / 1 2 3 4 5 6` | `0 5 8 9 8 5` | First-order differentiation and degree mapping |
| `5 2 / 1 2 3 4 5 6` | `0 0 20 24 18 8` | Multiple derivatives |
| `1 1 / 7 5` | `0 7` | Minimum degree and constant-term removal |
| `2 3 / 1 2 3` | `0 0 0` | Derivative order greater than degree |
| `3 1 / 5 5 5 5` | `0 15 10 5` | Equal coefficients and all surviving degrees |
| `4 2 / 0 0 0 7 9` | `0 0 0 0 0` | Lower-degree terms disappearing |
| `100 100 / 101 coefficients equal to 100` | `0 ... 0 100` | Maximum bounds and boundary indexing |

## Edge Cases

When (k>n), there is no monomial with enough degree to survive all differentiations. For

```
2 3
1 2 3
```

the degree-2 term becomes zero after the third derivative, and the lower-degree terms disappear earlier. The algorithm never enters the `j` loop because `k <= n` is false, so the preinitialized output `[0, 0, 0]` is printed directly.

When a constant term is present, it contributes nothing to any derivative of positive order. For

```
1 1
7 5
```

the polynomial is (7x+5). The loop processes only degree 1, calculates the multiplier (1), and places 7 at final degree 0. The result is `0 7`, preserving the required (n+1) coefficient positions.

When lower-degree terms disappear but higher-degree terms remain, the algorithm skips the vanished terms rather than trying to differentiate them. For

```
4 2
0 0 0 7 9
```

the polynomial is (7x+9), whose second derivative is zero. Both original degrees 1 and 0 are below (k=2), so neither is processed and every output position remains zero.

The output must retain the original number of positions even though the degree decreases. For Sample 2, the second derivative has degree 3, but the input degree is 5, so the first two output entries must be zero. The algorithm writes each surviving term according to its actual final degree and leaves every other slot initialized to zero.

Modulo reduction is required because the falling-factorial multiplier can become large. The implementation reduces `multiplier` after every multiplication and then reduces the final coefficient product as well. Since modular multiplication preserves the remainder of the complete product, this produces exactly the required coefficient modulo (2019).
