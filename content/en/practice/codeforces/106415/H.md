---
title: "CF 106415H - Scratch Expressions"
description: "We need count how many strings of a given length form a valid arithmetic expression whose value is 0 modulo m. The original string is generated uniformly from an alphabet of 15 characters: digits, three binary operators, and two parentheses."
date: "2026-06-25T09:44:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106415
codeforces_index: "H"
codeforces_contest_name: "Winter Cup 8.0 Online Mirror Contest"
rating: 0
weight: 106415
solve_time_s: 44
verified: true
draft: false
---

[CF 106415H - Scratch Expressions](https://codeforces.com/problemset/problem/106415/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We need count how many strings of a given length form a valid arithmetic expression whose value is `0` modulo `m`. The original string is generated uniformly from an alphabet of 15 characters: digits, three binary operators, and two parentheses. The answer is not the count itself, but the probability, so after counting valid winning strings we divide by `15^n` modulo `1e9+7`.

The difficulty comes from the fact that validity is not just a local property. A string can fail because parentheses are wrong, because an operator has no operand, or because the arithmetic value is not zero. Since the maximum length is only 200, we can afford a dynamic programming solution over lengths, but we must avoid parsing individual strings.

A length of 200 is small enough for polynomial dynamic programming. It rules out enumeration because there are `15^200` possible strings, but it allows states involving every length and every residue modulo `m`. Since `m` is at most 100, storing the number of expressions for every residue is feasible.

The main edge cases are expressions where syntax and value interact.

For example:

```
1
```

has no operator and is a valid expression, but the answer is only positive when `m = 1`, because the value is `1`.

Another case:

```
(0)
```

has length 3 and should count as a winning expression for every modulus. A solution that only handles numbers and operators but forgets parentheses loses this case.

A third case:

```
00
```

is a valid number, not two expressions. It evaluates to zero, so it must be counted. A parser that treats consecutive digits as separate tokens would reject it.

## Approaches

A direct approach would generate every possible string of length `n`, check whether it is a valid expression, evaluate it, and count the winners. This is correct because every possible card is examined, but the number of strings is `15^n`, which becomes impossible even for very small `n`.

The useful observation is that valid expressions have a grammar structure. We do not need the actual strings, only how many strings of each length produce each possible residue.

The expression syntax naturally splits into three levels. A number is a sequence of digits. A factor is either a number or a parenthesized expression. A term is a sequence of factors joined by multiplication. An expression is a sequence of terms joined by addition or subtraction.

This matches the precedence rules of arithmetic, so every valid string belongs to exactly one of these categories.

The dynamic programming states are:

`num[len][r]`: numbers of length `len` with value `r`.

`fac[len][r]`: factors of length `len` with value `r`.

`term[len][r]`: multiplication expressions of length `len`.

`expr[len][r]`: complete expressions of length `len`.

The transitions split a longer object at its first operator. For example, a term can be one factor, or a smaller term, a `*`, and another factor.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(15^n) | O(n) | Too slow |
| Dynamic Programming | O(n²m²) | O(nm) | Accepted |

## Algorithm Walkthrough

1. Compute the number of digit strings of every length and residue. Appending a digit transforms a value `x` into `(10*x+d) mod m`, so we can build all number states incrementally.
2. Build factors. A factor is either a number or an expression surrounded by parentheses. The parentheses add two characters, so a factor of length `i` can come from an expression of length `i-2`.
3. Build terms. Start with a single factor. To extend a term, append `*` and another factor. The previous term already represents the left side of the multiplication, so this follows left associativity automatically.
4. Build expressions. Start with one term. To extend an expression, append either `+` or `-` and another term. Both operators are handled separately because subtraction changes the resulting residue.
5. For every requested length, take `expr[n][0]`, because only residue zero is a winning card. Divide by the total number of strings, `15^n`, using modular inverse.

Why it works: every valid expression has a unique decomposition into number, factor, term, and expression levels. The transitions follow the grammar rules exactly, so every valid string is counted once and every invalid string is never created. The stored residue is exactly the value produced by evaluating the corresponding expression modulo `m`.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve_case(m, queries):
    nmax = max(queries)
    
    def conv(a, b, op):
        res = [0] * m
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    if y:
                        if op == 0:
                            k = (i + j) % m
                        else:
                            k = (i * j) % m
                        res[k] = (res[k] + x * y) % MOD
        return res

    num = [[0] * m for _ in range(nmax + 1)]
    num[0][0] = 1
    for length in range(1, nmax + 1):
        for r in range(m):
            if num[length - 1][r]:
                val = num[length - 1][r]
                for d in range(10):
                    num[length][(r * 10 + d) % m] = (
                        num[length][(r * 10 + d) % m] + val
                    ) % MOD

    fac = [[0] * m for _ in range(nmax + 1)]
    term = [[0] * m for _ in range(nmax + 1)]
    expr = [[0] * m for _ in range(nmax + 1)]

    for length in range(1, nmax + 1):
        fac[length] = num[length].copy()
        if length >= 2:
            for r in range(m):
                fac[length][r] = (fac[length][r] + expr[length - 2][r]) % MOD

        term[length] = fac[length].copy()
        for left in range(1, length - 1):
            right = length - left - 1
            add = conv(term[left], fac[right], 1)
            for r in range(m):
                term[length][r] = (term[length][r] + add[r]) % MOD

        expr[length] = term[length].copy()
        for left in range(1, length - 1):
            right = length - left - 1
            plus = conv(expr[left], term[right], 0)
            minus = [0] * m
            for i, x in enumerate(expr[left]):
                if x:
                    for j, y in enumerate(term[right]):
                        if y:
                            minus[(i - j) % m] = (
                                minus[(i - j) % m] + x * y
                            ) % MOD
            for r in range(m):
                expr[length][r] = (
                    expr[length][r] + plus[r] + minus[r]
                ) % MOD

    ans = []
    for n in queries:
        denominator = pow(pow(15, n, MOD), MOD - 2, MOD)
        ans.append(str(expr[n][0] * denominator % MOD))
    return ans

def main():
    t, m = map(int, input().split())
    queries = list(map(int, input().split()))
    print("\n".join(solve_case(m, queries)))

if __name__ == "__main__":
    main()
```

The code first constructs numbers because all higher grammar levels depend on them. The factor transition uses `expr[length - 2]`, which is why lengths are processed from small to large.

The multiplication and addition layers use convolutions over residues. For multiplication the new residue is the product of the two old residues. For addition and subtraction the residue is the sum or difference modulo `m`.

The final conversion to a probability is done only after the counting is finished. The denominator is never divisible by `1e9+7`, so modular inversion is valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²m²) | There are O(n²) grammar splits and each residue combination costs O(m²). |
| Space | O(nm) | Four dynamic programming tables store lengths and residues. |

With `n <= 200` and `m <= 100`, the state space is small enough for the required limits.

## Edge Cases

For the single character input length `1`, the only valid expressions are digits. The number DP creates all ten possible one digit expressions, and the final residue check keeps only the ones equal to zero modulo `m`.

For parenthesized zero, such as `(0)`, the factor transition adds `expr[length - 2]` into the factor table. This is exactly the transition needed to count parentheses without treating them as arithmetic operators.

For multi digit numbers with leading zeroes, such as `00`, the number DP appends digits without restricting the first digit. The resulting residue is computed normally, so all leading zero cases are included.
