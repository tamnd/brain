---
title: "CF 105999B - Big Mod"
description: "We are given multiple queries, each describing a base number, an exponent that can be extremely large (so large that it cannot fit into standard integer types), and a modulus."
date: "2026-06-25T13:21:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105999
codeforces_index: "B"
codeforces_contest_name: "La Salle-Pui Ching Programming Challenge \u57f9\u6b63\u5587\u6c99\u7de8\u7a0b\u6311\u6230\u8cfd 2024"
rating: 0
weight: 105999
solve_time_s: 50
verified: true
draft: false
---

[CF 105999B - Big Mod](https://codeforces.com/problemset/problem/105999/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given multiple queries, each describing a base number, an exponent that can be extremely large (so large that it cannot fit into standard integer types), and a modulus. For each query, we need to compute the value of the base raised to that exponent, taken modulo the given modulus.

The key difficulty is not the modular arithmetic itself but the representation of the exponent. Instead of being a normal integer, it is provided as a string of decimal digits, so it can have thousands or even tens of thousands of digits. That immediately rules out parsing it into any built-in numeric type.

From a constraints perspective, the base and modulus are within typical integer limits, so standard 32-bit or 64-bit arithmetic is sufficient once we are working modulo m. The exponent length dominates the complexity. Any solution that tries to expand the exponent or simulate repeated multiplication directly will fail because even a single exponent can represent an astronomically large number of operations.

A subtle edge case comes from small moduli. If the modulus is 1, every result must be 0 regardless of base and exponent, and a careless implementation that skips modulus reduction at intermediate steps may still produce correct-looking but unnecessary computations. Another edge case is when the exponent is zero, including the string "0". In that case the result must be 1 modulo m, even if the base is zero. A naive implementation that interprets exponent as an integer and does special casing inconsistently may incorrectly return 0.

For example, if the input is base 5, exponent "0", modulus 7, the correct answer is 1. A naive loop-based multiplication approach would never enter the loop and might incorrectly return 0 if initialized poorly.

Similarly, if base is 0 and exponent is "0", the mathematically conventional definition in programming problems is 0^0 = 1, so the output should still be 1 modulo m. A careless exponentiation routine might instead return 0 or crash depending on initialization.

## Approaches

The brute-force idea is straightforward: interpret the exponent as an integer and multiply the base by itself repeatedly while taking modulus at each step. This is correct in principle because modular arithmetic preserves multiplication structure, so reducing at each step does not change the final result.

The problem appears when the exponent is not representable as an integer. If the exponent has k digits, its value can be as large as 10^k. Even for k = 100000, the number of multiplications required would be completely infeasible.

A standard fast exponentiation technique solves this when the exponent is small: binary exponentiation reduces the number of multiplications to O(log b). However, binary exponentiation still assumes we can read b as a machine integer, which we cannot here.

The key observation is that we do not actually need the numeric value of the exponent at any point. We only need to process its effect digit by digit in base 10. If we already know a^x mod m for some prefix of the exponent, then appending a digit d transforms the exponent from x to 10x + d. This gives a direct recurrence:

a^(10x + d) = (a^x)^10 * a^d

This identity allows us to process the exponent string from left to right while maintaining the current power value under modulus. Each digit extends the exponent in base 10, and we update the result using modular exponentiation on small exponents only (digits 0 to 9 and fixed power 10).

This removes dependence on the magnitude of the exponent entirely and reduces the problem to O(number of digits × log m) operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(b) | O(1) | Too slow |
| Optimal | O(k log m) | O(1) | Accepted |

Here k is the number of digits in the exponent string.

## Algorithm Walkthrough

We process each test case independently.

1. Read base a, exponent string b, and modulus m. We immediately handle the special case where m is 1, since any number modulo 1 is always 0.
2. Initialize the result as 1. This represents a^0 at the beginning of processing the exponent string.
3. Iterate through each character in the exponent string from left to right. Each character is a decimal digit d.
4. Before incorporating the new digit, raise the current result to the 10th power modulo m. This corresponds to shifting the exponent one decimal place to the left in base 10.
5. Multiply this value by a^d modulo m, where d is a single digit. Since d is at most 9, this can be computed quickly using a small fast exponentiation routine.
6. After processing all digits, the result represents a raised to the full exponent modulo m.

The reason this works is that at every step we maintain the value a^x mod m, where x is exactly the numeric value of the prefix of the exponent string processed so far. Appending a digit d transforms x into 10x + d, and the update rule mirrors this identity exactly under modular exponentiation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def mod_pow(a, e, mod):
    res = 1
    a %= mod
    while e > 0:
        if e & 1:
            res = (res * a) % mod
        a = (a * a) % mod
        e >>= 1
    return res

t = int(input())
for _ in range(t):
    a, b, m = input().split()
    a = int(a)
    m = int(m)

    if m == 1:
        print(0)
        continue

    result = 1

    for ch in b:
        digit = ord(ch) - 48
        result = mod_pow(result, 10, m)
        if digit:
            result = (result * mod_pow(a, digit, m)) % m

    print(result)
```

The helper function performs standard binary exponentiation for small exponents, which is only ever called with exponent 10 or at most 9, so its cost is constant per digit in practice.

The main loop maintains the evolving value of the prefix exponentiation. The first transformation `result = result^10 mod m` is crucial because it shifts the exponent base, and missing this step is the most common implementation mistake. The multiplication by `a^digit` then inserts the contribution of the current digit.

The modulus check at the beginning avoids undefined behavior for modulus 1, which would otherwise cause repeated zero multiplication and unnecessary computation.

## Worked Examples

Consider an input where a = 2, exponent = "13", m = 5.

We track how the exponent is built digit by digit.

| Step | Digit | Result before shift | After power of 10 | After multiply | Meaning |
| --- | --- | --- | --- | --- | --- |
| init | - | 1 | - | 1 | 2^0 |
| 1 | 1 | 1 | 1^10 = 1 | 2 | 2^1 |
| 2 | 3 | 2 | 2^10 = 1024 mod 5 = 4 | 4 * (2^3=8 mod 5=3) = 2 | 2^13 |

The final result is 2.

Now consider a case with leading zero in exponent, a = 3, exponent = "05", m = 7.

| Step | Digit | Result before shift | After power of 10 | After multiply | Meaning |
| --- | --- | --- | --- | --- | --- |
| init | - | 1 | - | 1 | 3^0 |
| 0 | 0 | 1 | 1 | 1 | 3^0 |
| 5 | 5 | 1 | 1^10 = 1 | 3^5 = 5 | 3^5 |

The trace shows that leading zeros do not affect correctness, since multiplying by a^0 leaves the state unchanged.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k log m) | Each of k digits triggers a constant number of modular exponentiations, each done in O(log m) |
| Space | O(1) | Only a fixed number of variables are maintained |

The exponent length dominates, but the operations per digit remain logarithmic in modulus size. With typical constraints, this comfortably fits within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    
    t = int(sys.stdin.readline())
    
    def mod_pow(a, e, mod):
        res = 1
        a %= mod
        while e > 0:
            if e & 1:
                res = (res * a) % mod
            a = (a * a) % mod
            e >>= 1
        return res

    for _ in range(t):
        a, b, m = sys.stdin.readline().split()
        a = int(a)
        m = int(m)

        if m == 1:
            output.append("0")
            continue

        result = 1
        for ch in b:
            digit = ord(ch) - 48
            result = mod_pow(result, 10, m)
            if digit:
                result = (result * mod_pow(a, digit, m)) % m

        output.append(str(result))

    return "\n".join(output)

# provided samples (illustrative, since actual samples not given)
assert run("1\n2 3 5\n") == "3"

# custom cases
assert run("1\n5 0 7\n") == "1", "0 exponent"
assert run("1\n0 0 7\n") == "1", "0^0 convention"
assert run("1\n10 10 1\n") == "0", "mod 1"
assert run("1\n2 10 1000\n") == str(pow(2,10,1000)), "small validation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 0 7 | 1 | zero exponent handling |
| 0 0 7 | 1 | 0^0 convention |
| 10 10 1 | 0 | modulus edge case |
| 2 10 1000 | 1024 mod 1000 | correctness against built-in pow |

## Edge Cases

A first edge case is the exponent being "0". The algorithm initializes result as 1, then processes a single digit 0. The update step computes result^10 which remains 1, and multiplication by a^0 leaves it unchanged, so the output is 1 regardless of base and modulus.

Another edge case is both base and exponent being zero. The computation behaves the same as above, and the final result remains 1, matching the conventional programming definition.

A third edge case is modulus equal to 1. The algorithm immediately returns 0 before processing digits. Without this guard, repeated modular exponentiation would always collapse to 0 anyway, but only after unnecessary computation.

A final edge case involves very long exponent strings. Since each digit is processed independently, the algorithm never attempts to convert the exponent into a numeric type, so there is no risk of overflow or parsing failure, and the runtime scales linearly with digit count.
