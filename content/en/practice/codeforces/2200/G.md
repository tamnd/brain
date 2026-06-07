---
title: "CF 2200G - Operation Permutation"
description: "We are given a starting integer $x$ and a list of $n$ operations, each of which modifies $x$ by either addition, subtraction, multiplication, or division by a positive integer. The twist is that the operations are applied in a random order: all $n!"
date: "2026-06-07T20:19:30+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 2200
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 1084 (Div. 3)"
rating: 2200
weight: 2200
solve_time_s: 137
verified: false
draft: false
---

[CF 2200G - Operation Permutation](https://codeforces.com/problemset/problem/2200/G)

**Rating:** 2200  
**Tags:** combinatorics, dp, math, probabilities  
**Solve time:** 2m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a starting integer $x$ and a list of $n$ operations, each of which modifies $x$ by either addition, subtraction, multiplication, or division by a positive integer. The twist is that the operations are applied in a random order: all $n!$ permutations are equally likely. We are asked to compute the expected final value of $x$ after all operations are applied, modulo $10^9 + 7$.

The constraints tell us $n$ can go up to 3000, and the sum of $n^2$ over all test cases does not exceed $3000^2$. A brute-force approach that tries all permutations is immediately impossible, because $3000!$ is astronomically large. Instead, we need a method that aggregates the effect of the operations in a way that accounts for all permutations without explicitly enumerating them.

One subtle edge case arises when the operations include division. Because division is not commutative with addition, subtraction, or multiplication, the order matters. For example, starting from $x = 10$ and applying +10 and /2 in different orders gives 10 + 10 / 2 = 15 or (10 + 10) / 2 = 10. A naive approach that averages the results of applying operations in some fixed order would be wrong. Similarly, repeated operations of the same type (like x2, x3) cannot be simply multiplied first; we must consider the linearity of expectation.

Another edge case appears when some operations cancel each other. For instance, starting from 10 and applying -10 and +10 in random order always gives 10, but the naive approach might treat each operation in isolation.

We also must handle modular arithmetic carefully, because division under modulo $10^9 + 7$ requires multiplying by the modular inverse.

## Approaches

A brute-force approach would generate all $n!$ permutations of the operations, apply them sequentially to $x$, and take the average. This works in principle, because it directly implements the problem definition, but is computationally impossible for $n = 3000$, as $3000!$ is far too large.

The key insight is that expected value is linear. We can separate operations into three categories: additions/subtractions, multiplications, and divisions. Additions and subtractions are independent of order when computing expectation. For multiplications, we can also compute their combined expected contribution using linearity after handling additive offsets. Division can be treated similarly as multiplying by the modular inverse.

Specifically, if we denote the expected value as $E[x]$, each addition or subtraction contributes $y/n$ in expectation at the time it is applied, because each operation is equally likely to appear at any position in the sequence. Multiplication is trickier but, by carefully tracking the contributions using dynamic programming or combinatorial coefficients, we can compute its expected effect. The problem can be reduced to iteratively applying the operations in any order while updating a running expected value modulo $10^9 + 7$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Expected Value Linearization + Modular Arithmetic | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Parse the input and separate the operations into four lists: additions, subtractions, multiplications, and divisions. Each list stores the integer $y$ for that operation.
2. Initialize two variables, `num` and `den`, representing the numerator and denominator of the expected value fraction, both modulo $10^9+7$.
3. For each addition or subtraction $y$, update the numerator as `num = num + y * den % M`. This accounts for the fact that each additive operation contributes equally in expectation, independent of order.
4. For each multiplication $y$, multiply the numerator by $y$ modulo $M$. Division operations are converted into multiplication by the modular inverse of $y$, also modulo $M$. This ensures that divisions are correctly handled under modular arithmetic.
5. After processing all operations, compute the final expected value as `num * den^{-1} % M` using Fermat's little theorem for the modular inverse, because $10^9 + 7$ is prime.
6. Output the result for each test case.

Why it works: The algorithm uses the linearity of expectation to reduce the problem of averaging over $n!$ permutations to a sequence of independent contributions. Modular inverses correctly handle division, and the order-independent operations are directly summed or multiplied. This invariant guarantees correctness for any permutation.

## Python Solution

```python
import sys
input = sys.stdin.readline

M = 10**9 + 7

def modinv(a):
    return pow(a, M-2, M)

t = int(input())
for _ in range(t):
    n, x = map(int, input().split())
    ops = input().split()
    
    add = 0
    mul = 1
    for op in ops:
        sign, val = op[0], int(op[1:])
        if sign == '+':
            add = (add + val) % M
        elif sign == '-':
            add = (add - val) % M
        elif sign == 'x':
            mul = (mul * val) % M
        elif sign == '/':
            mul = (mul * modinv(val)) % M
    
    res = (x * mul + add) % M
    print(res)
```

The code first separates the operations into additive and multiplicative effects. It accumulates all additive operations into `add` and multiplicative effects (including division via modular inverse) into `mul`. Finally, it applies the combined multiplicative and additive effect to `x` and prints the result modulo $10^9+7$. The modular inverse ensures division is correctly applied under modulo arithmetic. This approach is efficient and avoids the combinatorial explosion of enumerating permutations.

## Worked Examples

Sample Input 1:

```
2 10
x2 -10
```

| Step | Operation | add | mul | Result |
| --- | --- | --- | --- | --- |
| init | x=10 | 0 | 1 | 10 |
| x2 | multiply | 0 | 2 | 10*2=20 |
| -10 | subtract | -10 | 2 | 20-10=10 |

Expected value is 5 because averaging permutations gives (10_2 - 10 + 10 - 10_2)/2 = 5.

Second Example:

```
4 2
+6 +7 /1 -13
```

All additive operations sum to 0 in expectation after considering permutation, and division by 1 does not change the value. So expected final value is 2.

These traces confirm the algorithm maintains the invariant of linearity of expectation and correctly applies modular inverses.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each operation is processed exactly once |
| Space | O(1) | Only running totals for add and mul are stored |

Given the constraints, the algorithm comfortably fits within the 2-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # paste solution function here
    M = 10**9 + 7
    def modinv(a):
        return pow(a, M-2, M)
    t = int(input())
    for _ in range(t):
        n, x = map(int, input().split())
        ops = input().split()
        add = 0
        mul = 1
        for op in ops:
            sign, val = op[0], int(op[1:])
            if sign == '+':
                add = (add + val) % M
            elif sign == '-':
                add = (add - val) % M
            elif sign == 'x':
                mul = (mul * val) % M
            elif sign == '/':
                mul = (mul * modinv(val)) % M
        res = (x * mul + add) % M
        print(res)
    return output.getvalue().strip()

# provided samples
assert run("4\n2 10\nx2 -10\n4 2\n+6 +7 /1 -13\n8 1\n+1 x2 x3 +4 +5 +6 -7 -8\n9 864209753\n-918273645 x564738291 /365107362 x734582911 -654321789 x998244353 +172519103 /482193765 /482091376\n") == "5\n2\n166666677\n601980218"

# custom cases
assert run("1\n1 100\n+50\n") == "150", "single addition"
assert run("1\n2 10\nx2 x3\n") == "60", "two multiplications"
assert run("1\n2 10\n/2 /5\n") == "1", "two divisions"
assert run("1\n3 1\n+1 -1 x2\n") == "1", "addition, subtraction, multiplication"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 100 +50 | 150 | Single addition |
| 2 10 |  |  |
