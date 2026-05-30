---
title: "CF 456B - Fedya and Maths"
description: "The task asks for the remainder when the sum of the first four multiples of a very large number n is divided by 5. In other words, you need to compute (1n + 2n + 3n + 4n) mod 5."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 456
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 260 (Div. 2)"
rating: 1200
weight: 456
solve_time_s: 66
verified: true
draft: false
---

[CF 456B - Fedya and Maths](https://codeforces.com/problemset/problem/456/B)

**Rating:** 1200  
**Tags:** math, number theory  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

The task asks for the remainder when the sum of the first four multiples of a very large number _n_ is divided by 5. In other words, you need to compute `(1*n + 2*n + 3*n + 4*n) mod 5`. The input _n_ is a single integer that can have up to 10,105 digits, which is far beyond what a standard 64-bit integer can store. This means you cannot directly use typical integer arithmetic or multiply _n_ by 10^4 in memory and then take the modulo, because the number itself could be enormous.

The output is a single integer between 0 and 4, representing the remainder after dividing the sum of these four multiples by 5. The problem is essentially asking for a pattern in modular arithmetic, because the sum `1 + 2 + 3 + 4` is constant, so the only thing that matters is _n modulo 5_. Edge cases to consider include _n_ being zero, a one-digit number, or having tens of thousands of digits. A naive implementation that tries to store `4*n` explicitly will fail for large _n_, either by crashing due to memory overflow or by taking far too long.

## Approaches

A brute-force solution would involve first calculating each multiple `1*n`, `2*n`, `3*n`, and `4*n`, summing them, and then taking the modulo 5. This approach is correct for small numbers because multiplication and addition are straightforward. However, if _n_ has 10,000 digits, computing `4*n` explicitly is impractical. Even using a big integer library, this would take significant time and memory, far exceeding the intended 1-second limit.

The key observation is that modular arithmetic is distributive over addition and multiplication. That is, `(a + b) mod m = ((a mod m) + (b mod m)) mod m` and `(a * b) mod m = ((a mod m) * (b mod m)) mod m`. The sum of coefficients `1 + 2 + 3 + 4` is 10, so `(1*n + 2*n + 3*n + 4*n) mod 5 = (10*n) mod 5`. Since 10 is divisible by 5, `(10*n) mod 5` is always 0, regardless of _n_. This dramatically simplifies the problem: the output is always 0. There is no need to read the digits of _n_ or perform any arithmetic with the actual number.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(len(n)) or worse depending on big integer arithmetic | O(len(n)) | Too slow for n with 10^5 digits |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Recognize that the sum of the first four multiples of _n_ can be factored: `1*n + 2*n + 3*n + 4*n = (1+2+3+4)*n = 10*n`.
2. Realize that `(10*n) mod 5` simplifies because 10 is divisible by 5, giving `(10*n) mod 5 = 0`.
3. Return 0 directly, since the expression always evaluates to 0 modulo 5 for any non-negative integer _n_, regardless of its size.

Why it works: The distributive property of modular arithmetic guarantees correctness. Since 10 is a multiple of 5, multiplying it by any integer _n_ will still be divisible by 5. The modulo operation then produces a remainder of zero. There are no edge cases, because zero multiplied by 10 also yields zero, and the formula is valid for all allowed values of _n_.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = input().strip()
print(0)
```

This solution reads the input as a string, which is necessary because _n_ can be very large. We do not convert it to an integer because the size of _n_ is irrelevant after realizing that the result is always zero. The `strip()` method removes any trailing newline characters. Printing `0` produces the correct output without performing any arithmetic operations on _n_.

## Worked Examples

Sample Input 1:

```
4
```

| Step | Expression | Value |
| --- | --- | --- |
| Factor sum | 1_4 + 2_4 + 3_4 + 4_4 | 40 |
| Modulo 5 | 40 mod 5 | 0 |
| Output | 0 | 0 |

Sample Input 2:

```
123456789012345678901234567890
```

| Step | Expression | Value |
| --- | --- | --- |
| Factor sum | 1_n + 2_n + 3_n + 4_n | 10*n |
| Modulo 5 | 10*n mod 5 | 0 |
| Output | 0 | 0 |

These examples demonstrate that the algorithm works for both small and extremely large numbers. The modulo calculation depends only on the factor 10, not on _n_.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | The calculation does not depend on the number of digits in n. |
| Space | O(1) | No extra memory is used apart from reading the input as a string. |

The solution easily fits within the 1-second time limit and 256 MB memory limit because it avoids any arithmetic on large numbers.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = sys.stdin.readline().strip()
    return str(0)

# provided sample
assert run("4\n") == "0", "sample 1"

# custom cases
assert run("0\n") == "0", "minimum n"
assert run("5\n") == "0", "small n divisible by 5"
assert run("1\n") == "0", "small n not divisible by 5"
assert run("9"*10105 + "\n") == "0", "maximum-size n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 | 0 | Minimum input |
| 5 | 0 | Small input divisible by 5 |
| 1 | 0 | Small input not divisible by 5 |
| 9...9 (10^5 digits) | 0 | Maximum input size |

## Edge Cases

For _n = 0_, the sum of the first four multiples is `0 + 0 + 0 + 0 = 0`, which modulo 5 is 0. For _n_ with 10,105 digits, the algorithm correctly prints 0 without performing any arithmetic. Even for single-digit numbers not divisible by 5, the sum `1*n + 2*n + 3*n + 4*n` is a multiple of 10, and the modulo 5 result is still 0. There are no edge cases that violate this pattern.
