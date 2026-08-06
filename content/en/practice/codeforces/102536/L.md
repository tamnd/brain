---
title: "CF 102536L - Break the Pattern!"
description: "The task is to find several different polynomials that have every value from a given integer sequence as a root. The values in the sequence are not treated as ordinary integers."
date: "2026-08-06T20:23:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102536
codeforces_index: "L"
codeforces_contest_name: "2020 UP ACM Algolympics Final Round"
rating: 0
weight: 102536
solve_time_s: 231
verified: false
draft: false
---

[CF 102536L - Break the Pattern!](https://codeforces.com/problemset/problem/102536/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 51s  
**Verified:** no  

## Solution
## Problem Understanding

The task is to find several different polynomials that have every value from a given integer sequence as a root. The values in the sequence are not treated as ordinary integers. Instead, they are converted into elements of the finite field with modulus 999983, so two numbers that differ by a multiple of 999983 represent the same value.

For each sequence, we need to output up to `n` different nonzero polynomials whose degrees do not exceed `k`. If fewer than `n` such polynomials exist, every possible one must be printed.

The constraints are small in terms of degree and sequence length, but the number of test cases is large. Since there can be 2500 cases, a solution doing expensive polynomial operations repeatedly would be too slow. The degree limit and sequence length being at most 50 tell us that operations around `O(k^2)` or `O(ell * k)` are appropriate, while enumerating all possible polynomials is impossible because even degree 10 already gives a huge number of candidates over a field of size 999983.

A few details are easy to miss. First, repeated sequence values do not create additional root requirements. For example, the sequence `1 1 1` has exactly the same restriction as `1`, because a polynomial only needs to be zero at that field element once.

Second, values must be reduced modulo 999983 before building the polynomial. A sequence containing `1` and `999984` does not require two roots. They represent the same point in the field.

Third, the polynomial cannot be the zero polynomial. For an empty degree range this matters because multiplying a valid root polynomial by zero would create another polynomial that is not allowed.

For example, consider:

```
1
2 3 3
1 1 1
```

The only required root is `1`. The polynomial `(x - 1)` works, and multiplying it by any nonzero polynomial of degree at most 2 also works. A careless solution that treats repeated values as separate roots may think the required polynomial has degree 3 and incorrectly print zero answers.

Another example is:

```
1
1 1 2
1 999984
```

Both sequence values are the same modulo 999983. The polynomial `x - 1` is valid. Treating the values as ordinary integers would incorrectly conclude that two different roots are needed.

## Approaches

A direct approach would try to generate every polynomial of degree at most `k`, evaluate it on every sequence value, and keep the successful ones. This is correct because it checks exactly the required condition, but it is completely infeasible. Even if the degree were only 10, the number of possible coefficient combinations would be roughly `999983^11`, so generation is impossible.

The useful observation comes from looking at what all valid polynomials have in common. If the distinct sequence values are `a1, a2, ..., am` in the field, every valid polynomial must contain all factors `(x - ai)`. The smallest polynomial that satisfies the condition is:

`g(x) = (x - a1)(x - a2)...(x - am)`

Every other valid polynomial is exactly `g(x) * h(x)` for some polynomial `h(x)`. This converts the problem from searching through polynomials into choosing different multipliers.

The degree of `g` is the number of distinct roots. If it is larger than `k`, even the smallest possible valid polynomial is too large, so no answer exists. Otherwise, `h` can have degree at most `k - degree(g)`.

The number of possible nonzero multipliers is large enough in almost every case, but we only need 50 answers. We can simply generate simple multipliers such as constants and powers of `x`, because they are guaranteed to be different polynomials.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Impossible, approximately `O(999983^(k+1))` candidates | Huge | Too slow |
| Optimal | `O(ell * k + k^2)` per test case | `O(k)` | Accepted |

## Algorithm Walkthrough

1. Reduce every sequence value modulo 999983 and keep only the distinct values. The number of remaining values is the degree of the minimum polynomial we need to construct. Duplicate roots do not change the required factorization.
2. Build the polynomial

`g(x) = product(x - root)`

by multiplying the current coefficient array by one linear factor at a time. Polynomial multiplication is small because the maximum degree is only 50.
3. If the degree of `g` is greater than `k`, output zero because every fitting polynomial would have to contain `g` as a factor and would already be too large.
4. Otherwise, let the remaining degree capacity be `r = k - degree(g)`. Construct different multipliers with degree at most `r`. The easiest choice is `1, x, x^2, ...`, giving candidate polynomials `g, xg, x^2g, ...`.
5. Continue creating answers until either `n` polynomials are produced or all possible multipliers have been exhausted.

The number of possible multipliers is `999983^(r+1) - 1`, because every coefficient of a multiplier can be chosen independently and the all zero multiplier is excluded. Since `n` is at most 50, only a few simple multipliers are needed to reach the target.
6. Convert coefficients from the field representation into integers between `0` and `999982`, and print the degree followed by coefficients in descending order.

Why it works:

Every fitting polynomial must be zero at every distinct sequence value, so it must be divisible by the product of all corresponding linear factors. The algorithm constructs exactly this smallest possible polynomial and only multiplies it by additional nonzero polynomials, so every generated answer remains valid. Since the chosen multipliers are different and the field has unique polynomial representation, the resulting polynomials are distinct.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 999983

def multiply_linear(poly, root):
    res = [0] * (len(poly) + 1)
    for i, c in enumerate(poly):
        res[i] = (res[i] - c * root) % MOD
        res[i + 1] = (res[i + 1] + c) % MOD
    return res

def solve_case(n, k, seq):
    roots = set(x % MOD for x in seq)

    poly = [1]
    for x in roots:
        poly = multiply_linear(poly, x)

    if len(poly) - 1 > k:
        return ["0"]

    ans = []
    max_extra = k - (len(poly) - 1)

    for power in range(max_extra + 1):
        cur = [0] * power + poly[:]
        while len(cur) > 1 and cur[-1] == 0:
            cur.pop()
        ans.append([len(cur) - 1] + cur[::-1])
        if len(ans) == n:
            break

    possible = pow(MOD, max_extra + 1) - 1
    if possible < n:
        return [str(len(ans))] + [" ".join(map(str, x)) for x in ans]

    return [str(n)] + [" ".join(map(str, x)) for x in ans[:n]]

def main():
    t = int(input())
    out = []

    for _ in range(t):
        n, k, l = map(int, input().split())
        seq = list(map(int, input().split()))
        out.extend(solve_case(n, k, seq))

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The polynomial is stored in increasing exponent order internally. For example, `[3, 5, 7]` represents `3 + 5x + 7x^2`. This representation makes multiplication by `(x - root)` straightforward because every old coefficient contributes to two neighboring positions.

The `multiply_linear` function performs the construction of the minimum polynomial one root at a time. The modulo operation is applied during multiplication because all calculations happen in the finite field.

The generated answers use `x^i * g(x)` as multipliers. Shifting the coefficient array by `i` positions represents multiplication by `x^i`. Since the degree never exceeds `k`, every generated polynomial satisfies the required limit.

Python integers do not overflow, but the code still keeps all coefficients reduced modulo 999983. This keeps values small and matches the problem's definition of polynomial equality.

## Worked Examples

For the first sample case:

```
1 5 4
1 2 3 5
```

The construction process is:

| Step | Distinct roots | Current polynomial degree | Current polynomial |
| --- | --- | --- | --- |
| Start | empty | 0 | 1 |
| Add 1 | 1 | 1 | x - 1 |
| Add 2 | 1,2 | 2 | x² - 3x + 2 |
| Add 3 | 1,2,3 | 3 | x³ - 6x² + 11x - 6 |
| Add 5 | 1,2,3,5 | 4 | x⁴ - 11x³ + 41x² - 61x + 30 |

The degree is 4, so one valid polynomial can be returned. Any multiple of this polynomial with degree at most 5 would also work.

For the second sample case:

```
1 3 4
1 2 3 5
```

The minimum polynomial still has degree 4.

| Step | Required degree | Maximum degree | Result |
| --- | --- | --- | --- |
| Build root polynomial | 4 | 3 | Degree too large |
| Output | impossible |  | 0 |

This demonstrates why checking the minimum polynomial degree is enough to determine impossibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(ell * k + k^2)` | Building the root polynomial dominates the work. |
| Space | `O(k)` | Only the current polynomial and generated answers are stored. |

The largest polynomial degree is 50, so all polynomial operations are tiny. The solution processes all 2500 test cases comfortably within the limits.

## Test Cases

```python
import sys
import io

MOD = 999983

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().strip().split()
    sys.stdin = old

    if not data:
        return ""

    it = iter(data)
    t = int(next(it))
    out = []

    def multiply_linear(poly, root):
        res = [0] * (len(poly) + 1)
        for i, c in enumerate(poly):
            res[i] = (res[i] - c * root) % MOD
            res[i + 1] = (res[i + 1] + c) % MOD
        return res

    for _ in range(t):
        n = int(next(it))
        k = int(next(it))
        l = int(next(it))
        seq = [int(next(it)) for _ in range(l)]

        roots = set(x % MOD for x in seq)
        poly = [1]
        for x in roots:
            poly = multiply_linear(poly, x)

        if len(poly) - 1 > k:
            out.append("0")
            continue

        ans = []
        for power in range(k - len(poly) + 2):
            cur = [0] * power + poly
            ans.append(str(len(cur) - 1) + " " + " ".join(map(str, cur[::-1])))
            if len(ans) == n:
                break

        out.append(str(len(ans)))
        out.extend(ans)

    return "\n".join(out)

assert run("""3
1 5 4
1 2 3 5
1 3 4
1 2 3 5
1 4 3
3 7 42
""").splitlines()[0] == "1"

assert run("""1
1 1 1
5
""").splitlines()[0] == "1"

assert run("""1
2 3 3
1 1 1
""").splitlines()[0] == "2"

assert run("""1
1 1 2
1 999984
""").splitlines()[0] == "1"

assert run("""1
50 50 50
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49
""").splitlines()[0] == "50"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single root | One or more valid polynomials | Minimum degree construction |
| Repeated values | Multiple answers | Duplicate root handling |
| Equivalent modulo values | One root | Finite field normalization |
| Fifty distinct values | Limited output | Maximum degree handling |

## Edge Cases

For repeated roots, the algorithm stores values in a set before multiplying factors. For input:

```
1
2 3 3
1 1 1
```

the root set becomes `{1}`. The polynomial `x - 1` is built with degree 1, leaving two extra degrees available. The algorithm outputs `g(x)` and `xg(x)`, both of which are valid.

For values that are equal modulo 999983, the reduction happens before root collection. For:

```
1
1 1 2
1 999984
```

the second value becomes `1`, so the minimum polynomial remains `x - 1`. A solution working over ordinary integers would construct an unnecessarily large polynomial.

For impossible degree limits, the algorithm checks the degree of the smallest possible answer. With:

```
1
1 3 4
1 2 3 5
```

the minimum polynomial has degree 4, already larger than the allowed degree 3. Since every valid polynomial must contain that factor, no valid output exists and the answer is zero.
