---
title: "CF 913A - Modular Exponentiation"
description: "The problem asks us to compute the remainder when an integer m is divided by $2^n$, where n and m are positive integers. In other words, we are given the size of a power-of-two modulus and a dividend, and we must find what is left after dividing the dividend by that modulus."
date: "2026-06-13T01:04:43+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 913
codeforces_index: "A"
codeforces_contest_name: "Hello 2018"
rating: 900
weight: 913
solve_time_s: 376
verified: true
draft: false
---

[CF 913A - Modular Exponentiation](https://codeforces.com/problemset/problem/913/A)

**Rating:** 900  
**Tags:** implementation, math  
**Solve time:** 6m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to compute the remainder when an integer _m_ is divided by $2^n$, where _n_ and _m_ are positive integers. In other words, we are given the size of a power-of-two modulus and a dividend, and we must find what is left after dividing the dividend by that modulus. The input _n_ specifies the number of times we multiply 2 by itself to obtain the divisor, while _m_ is the number to be reduced modulo that divisor. The output is a single integer between 0 and $2^n - 1$, representing the remainder.

The constraints are moderate but have subtle implications. Both _n_ and _m_ can be as large as 10^8. Directly computing $2^n$ is impractical, because storing or operating with numbers of roughly $10^{30,000,000}$ digits is impossible in memory. This rules out any approach that literally constructs $2^n$. The algorithm must therefore rely on a property of powers of two, rather than computing them explicitly.

Edge cases arise where _m_ is smaller than $2^n$, in which case the remainder is simply _m_, or when _m_ is exactly divisible by $2^n$, yielding a remainder of zero. For example, if _n_ = 5 and _m_ = 32, $2^5 = 32$ and the remainder is 0. A careless implementation that tries to compute $2^n$ literally would fail or overflow in such cases.

## Approaches

The brute-force approach would attempt to compute $2^n$ and then perform _m_ modulo $2^n$. This is correct in principle, but with _n_ up to 10^8, the number $2^n$ is astronomically large and cannot be represented in standard integer types. Attempting to construct it directly would require exponential time and memory, far exceeding the problem limits.

The key insight is that $2^n$ has a very simple binary representation: it is a 1 followed by _n_ zeros in binary. Computing _m_ modulo $2^n$ is equivalent to taking the last _n_ bits of _m_. In practice, this is exactly what the bitwise AND operation with $2^n - 1$ achieves, because $2^n - 1$ in binary is _n_ ones. This observation reduces the problem to a single fast operation that works even for the largest constraints, and it avoids constructing massive numbers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(n) | Too slow, impossible for large n |
| Bitwise Modulo | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integers _n_ and _m_. These specify the exponent of 2 and the number to reduce, respectively.
2. Compute $mask = 2^n - 1$. This creates a number with _n_ ones in binary. The reason is that any number modulo a power of two is equivalent to its last _n_ bits, which this mask isolates.
3. Compute the remainder as $result = m \& mask$. The bitwise AND operation keeps exactly the last _n_ bits of _m_, discarding the higher bits. This operation directly produces $m \bmod 2^n$ without any large-number arithmetic.
4. Print the result. This completes the calculation efficiently.

Why it works: the invariant is that for any integer _m_, the remainder of division by $2^n$ depends solely on the lowest _n_ bits of _m_. The AND operation with $2^n - 1$ preserves those bits while zeroing out the higher-order bits, which have no effect on the remainder. This guarantees correctness regardless of how large _m_ or _n_ is.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
m = int(input())

# 2^n - 1 is a mask with n ones in binary
mask = (1 << n) - 1

# remainder of m divided by 2^n
result = m & mask

print(result)
```

The code reads input using fast I/O, computes the mask using a left-shift to avoid computing large powers explicitly, and then applies a bitwise AND to extract the last _n_ bits. Using `1 << n` is both fast and safe in Python because Python integers are unbounded. The final print outputs the remainder as required.

## Worked Examples

**Sample 1:** n = 4, m = 42

| Step | Value | Explanation |
| --- | --- | --- |
| n | 4 | read from input |
| m | 42 | read from input |
| mask | 15 | $2^4 - 1 = 16 - 1 = 15$ |
| result | 10 | 42 & 15 = 101010 & 1111 = 1010 (binary) = 10 |

This shows that the last 4 bits of 42 are 1010, which gives the remainder 10.

**Sample 2:** n = 1, m = 58

| Step | Value | Explanation |
| --- | --- | --- |
| n | 1 | read from input |
| m | 58 | read from input |
| mask | 1 | $2^1 - 1 = 1$ |
| result | 0 | 58 & 1 = 111010 & 1 = 0 |

This demonstrates the edge case where m is divisible by $2^n$, yielding remainder 0.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | single bitwise AND operation |
| Space | O(1) | only three integers stored (n, m, mask) |

The time complexity does not depend on the magnitude of _n_ or _m_, so it easily fits within the 1-second limit. Space usage is minimal, well within the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    m = int(input())
    mask = (1 << n) - 1
    return str(m & mask)

# provided samples
assert run("4\n42\n") == "10", "sample 1"
assert run("1\n58\n") == "0", "sample 2"

# custom cases
assert run("5\n32\n") == "0", "m equals 2^n"
assert run("5\n31\n") == "31", "m just below 2^n"
assert run("8\n300\n") == "44", "medium n and m"
assert run("30\n1073741825\n") == "1", "large n with overflow-like value"
assert run("10\n1023\n") == "1023", "m exactly 2^n - 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5\n32\n | 0 | remainder zero when m = 2^n |
| 5\n31\n | 31 | remainder equal to m when m < 2^n |
| 8\n300\n | 44 | typical case, checks correct masking |
| 30\n1073741825\n | 1 | large n, tests correctness with big numbers |
| 10\n1023\n | 1023 | m = 2^n - 1 edge case |

## Edge Cases

When _m_ is smaller than $2^n$, the algorithm correctly returns _m_ itself. For example, n = 5, m = 3 results in mask = 31, and 3 & 31 = 3. When _m_ equals $2^n$, such as n = 5, m = 32, the mask is 31, and 32 & 31 = 0. Large _n_ such as 30 and m = 1073741825 still works because Python supports arbitrary precision integers, and the bitwise AND isolates the correct last 30 bits. These cases confirm the algorithm handles all boundaries correctly.
