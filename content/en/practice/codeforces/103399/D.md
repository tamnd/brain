---
title: "CF 103399D - Fast modular multiplication modulo 64-bit modulus"
description: "We are given two integers and asked to compute their product under a very large modulus, where the modulus is a full 64-bit value."
date: "2026-07-03T12:08:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103399
codeforces_index: "D"
codeforces_contest_name: "Fast modular multiplication"
rating: 0
weight: 103399
solve_time_s: 45
verified: true
draft: false
---

[CF 103399D - Fast modular multiplication modulo 64-bit modulus](https://codeforces.com/problemset/problem/103399/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two integers and asked to compute their product under a very large modulus, where the modulus is a full 64-bit value. The key difficulty is not multiplication itself, but performing it safely without overflow while still preserving correctness modulo that large number.

Conceptually, the task is simple: we want to compute $a \cdot b \bmod m$, but both $a \cdot b$ and intermediate results may exceed 64-bit signed or unsigned limits depending on the language and implementation details. Since $m$ itself is a 64-bit integer, naive multiplication in a fixed-width type can silently wrap around before the modulus is applied, producing incorrect results.

The input represents repeated independent queries, each consisting of two large integers and a modulus. The output for each query is the correct modular product.

The constraint implication is subtle. A single multiplication is constant time mathematically, but in implementation, we cannot rely on built-in 128-bit arithmetic in all environments. A solution must avoid intermediate overflow using a technique that simulates multiplication safely using only 64-bit operations.

Edge cases arise when both operands are close to $2^{64}$. For example, if $a = 2^{63}$, $b = 2$, then the true product exceeds 64 bits immediately. A naive approach in a language with wrapping arithmetic might compute zero or an incorrect wrapped value before applying modulus.

Another problematic case is when the modulus itself is close to $2^{64}$. For example, if $m = 2^{64} - 1$, even intermediate multiplication must be carefully controlled, because any overflow invalidates the modular reduction logic.

## Approaches

The brute-force approach is to compute the product directly using native integer multiplication and then apply modulo. This works in languages with unbounded integers, because the product is computed exactly before reduction. However, in fixed 64-bit arithmetic, multiplication overflows before the modulus is applied, so the computed value is already corrupted.

The failure point is straightforward: multiplying two 64-bit integers can require up to 128 bits of precision. If the environment only supports 64-bit arithmetic, the intermediate result is lost.

The key observation is that modular multiplication can be decomposed into additions. Instead of computing $a \cdot b$ directly, we interpret multiplication as repeated doubling and conditional addition, similar to binary exponentiation logic. This avoids ever forming a large intermediate product. Each step keeps values reduced modulo $m$, ensuring all intermediates stay within range.

We can also accelerate this using bit decomposition: we scan bits of one operand and accumulate contributions of the other operand, doubling safely under modulus at each step.

This transforms multiplication from a potentially overflowing operation into a sequence of controlled additions and doublings, all of which can be safely reduced modulo $m$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) | O(1) | Fails in fixed 64-bit arithmetic |
| Bitwise Modular Multiplication | O(log b) | O(1) | Accepted |

## Algorithm Walkthrough

We compute $a \cdot b \bmod m$ using binary decomposition of the multiplier.

1. Initialize a result variable as zero and reduce both input numbers modulo $m$. Reducing early ensures all later operations stay bounded and prevents unnecessary growth.
2. Iterate over the bits of the multiplier $b$. At each step, we check whether the current bit is set. If it is, we add the current value of the multiplicand into the result, applying modulus immediately. This works because each set bit represents a power-of-two contribution in binary expansion.
3. After processing each bit, we double the multiplicand under modulus. This corresponds to shifting its weight from $2^k$ to $2^{k+1}$ in the binary representation. The modulus keeps this doubling safe from overflow.
4. Continue until all bits of the multiplier have been processed. The accumulated result is the final modular product.

### Why it works

The correctness comes from interpreting multiplication as a sum of shifted contributions. Any integer $b$ can be written as a sum of powers of two, and multiplying by $a$ distributes over this representation. The algorithm mirrors this decomposition exactly: whenever a bit is set, we add the corresponding power-of-two scaled value of $a$, and we maintain correctness by ensuring every intermediate value is reduced modulo $m$. No overflow can affect correctness because no intermediate computation ever exceeds the modulus boundary in a meaningful way.

## Python Solution

```python
import sys
input = sys.stdin.readline

def mod_mul(a, b, m):
    a %= m
    b %= m
    res = 0

    while b > 0:
        if b & 1:
            res = (res + a) % m
        a = (a + a) % m
        b >>= 1

    return res

def solve():
    t = int(input())
    for _ in range(t):
        a, b, m = map(int, input().split())
        print(mod_mul(a, b, m))

if __name__ == "__main__":
    solve()
```

The function `mod_mul` implements binary multiplication under modulus. The key idea is that `a` is repeatedly doubled, representing successive powers of two, while `b` is decomposed bit by bit. Whenever a bit of `b` is active, the current contribution of `a` is added into the result.

A subtle detail is the early reduction of both `a` and `b` modulo `m`. While reducing `a` is essential for keeping values small, reducing `b` is optional for correctness but harmless and sometimes helps reduce loop iterations slightly. The loop structure ensures correctness regardless, because it processes the binary representation directly.

All additions and doublings are immediately reduced modulo `m`, preventing overflow entirely even in a 64-bit constrained environment.

## Worked Examples

### Example 1

Let $a = 3$, $b = 5$, $m = 7$. Binary representation of $b$ is $101$.

| Step | a | b | res |
| --- | --- | --- | --- |
| init | 3 | 5 | 0 |
| bit 1 (LSB) | 3 | 5 | 3 |
| double a | 6 | 2 | 3 |
| bit 0 | 6 | 2 | 3 |
| double a | 5 | 1 | 3 |
| bit 1 | 5 | 1 | 1 |
| double a | 3 | 0 | 1 |

Final result is $1$, matching $15 \bmod 7$.

This trace shows how each binary digit of the multiplier contributes independently and how modular reduction prevents growth beyond the modulus.

### Example 2

Let $a = 10$, $b = 6$, $m = 9$. Binary representation of $b$ is $110$.

| Step | a | b | res |
| --- | --- | --- | --- |
| init | 10 → 1 | 6 | 0 |
| bit 0 | 1 | 6 | 0 |
| double a | 2 | 3 | 0 |
| bit 1 | 2 | 3 | 2 |
| double a | 4 | 1 | 2 |
| bit 1 | 4 | 1 | 6 |
| double a | 8 → 8 mod 9 = 8 | 0 | 6 |

Final result is $6$, matching $60 \bmod 9$.

This example highlights repeated reduction and shows how even when intermediate values exceed the modulus, correctness is preserved through immediate reduction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log b) | Each iteration processes one bit of the multiplier |
| Space | O(1) | Only a constant number of variables are used |

The runtime is efficient for 64-bit integers because the number of bits is at most 64. Even with many test cases, the total number of operations remains small and comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def mod_mul(a, b, m):
        a %= m
        b %= m
        res = 0
        while b > 0:
            if b & 1:
                res = (res + a) % m
            a = (a + a) % m
            b >>= 1
        return res

    t = int(sys.stdin.readline())
    out = []
    for _ in range(t):
        a, b, m = map(int, sys.stdin.readline().split())
        res = mod_mul(a, b, m)
        out.append(str(res))
    return "\n".join(out)

# sample-like tests
assert run("1\n3 5 7\n") == "1", "sample 1"
assert run("1\n10 6 9\n") == "6", "sample 2"

# custom cases
assert run("1\n0 123456 7\n") == "0", "multiplication by zero"
assert run("1\n1 999999 2\n") == "1", "mod 1 behavior"
assert run("1\n2 2 3\n") == "1", "small cycle case"
assert run("1\n18446744073709551615 18446744073709551615 18446744073709551615\n") == "0", "max 64-bit edge"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 × large | 0 | zero absorption |
| mod 2 identity collapse | 1 | reduction correctness |
| small cyclic | 1 | binary decomposition correctness |
| max 64-bit values | 0 | overflow-safe behavior |

## Edge Cases

One important edge case is when one operand is zero. The algorithm immediately returns zero because no bits are set in the multiplier or the multiplicand never contributes. For input `0 123456 7`, the loop never accumulates anything, and the result remains zero.

Another case is when the modulus is very small, such as 1 or 2. For modulus 1, every intermediate reduction forces all values to zero immediately, so the output is always zero. For modulus 2, only parity matters, and the algorithm still works because every addition and doubling preserves correctness modulo 2.

A final edge case is the maximum 64-bit value multiplied by itself under a large modulus. For `18446744073709551615 18446744073709551615 18446744073709551615`, the algorithm reduces both operands immediately to zero modulo the modulus, so the result is zero. Even though the true mathematical product is enormous, the modular reduction prevents any overflow or incorrect computation, and the algorithm terminates cleanly without ever forming large intermediate values.
