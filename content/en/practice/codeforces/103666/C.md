---
title: "CF 103666C - \u041c\u0430\u0440\u0441\u0438\u0430\u043d\u0441\u043a\u0438\u0435 \u043d\u043e\u043b\u0438\u043a\u0438"
description: "We are working in a positional numeral system with base $k$, where numbers are written using digits from $0$ to $k-1$. A number is called “sufficiently round” if, when written in base $k$, its representation ends with at least $n$ zero digits."
date: "2026-07-02T21:31:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103666
codeforces_index: "C"
codeforces_contest_name: "\u0422\u0443\u0440\u043d\u0438\u0440 \u0410\u0440\u0445\u0438\u043c\u0435\u0434\u0430 2016"
rating: 0
weight: 103666
solve_time_s: 49
verified: true
draft: false
---

[CF 103666C - \u041c\u0430\u0440\u0441\u0438\u0430\u043d\u0441\u043a\u0438\u0435 \u043d\u043e\u043b\u0438\u043a\u0438](https://codeforces.com/problemset/problem/103666/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working in a positional numeral system with base $k$, where numbers are written using digits from $0$ to $k-1$. A number is called “sufficiently round” if, when written in base $k$, its representation ends with at least $n$ zero digits. In other words, the number is divisible by $k^n$.

The task is to list all positive integers with this property in increasing order and return the $i$-th one in ordinary decimal representation.

From the constraints, $k$ can be as large as $10^9$, $n$ can be up to $100$, and $i$ can be up to $10^9$. The answer is guaranteed to fit within $10^{18}$, which means we can safely use 64-bit arithmetic logic and avoid overflow concerns beyond that bound.

A naive interpretation would be to iterate through natural numbers, convert each to base $k$, count trailing zeros, and pick those that qualify. This immediately fails because checking one number costs $O(\log_k x)$, and we may need up to $10^9$ valid numbers, meaning we would simulate up to $10^9$ candidates, which is far beyond feasible limits.

A subtle edge case appears when $n = 0$. Then every number is valid, and the answer is simply $i$. Any solution that incorrectly enforces divisibility by $k^n$ as a strict condition even when $n=0$ must carefully avoid forcing division by $1$-like logic that could distort indexing.

Another edge case is when $k = 2$ and $n$ is large. Even though $k^n$ grows quickly, the problem does not require us to enumerate large numbers; instead, we must reason structurally about how numbers with trailing zeros behave in base $k$.

## Approaches

The key observation is that a number has at least $n$ trailing zeros in base $k$ if and only if it is divisible by $k^n$. This transforms the problem into a simple arithmetic progression question: we are asked to enumerate all positive multiples of $k^n$.

So the sequence of sufficiently round numbers is:

$$k^n,\; 2k^n,\; 3k^n,\; \dots$$

The $i$-th such number is therefore exactly:

$$i \cdot k^n$$

The brute-force approach would explicitly test each integer, convert it to base $k$, and check trailing zeros. This works conceptually because base conversion is straightforward, but it fails computationally because the density of valid numbers is $1/k^n$, so we would still scan up to $i \cdot k^n$ candidates in the worst case.

The optimized approach bypasses representation entirely and relies on the equivalence between trailing zeros in base $k$ and divisibility by $k^n$. Once this equivalence is established, the problem reduces to computing a power and a multiplication.

The only technical difficulty is computing $k^n$ safely. Since $n \le 100$, exponentiation by repeated squaring is sufficient and stable in 64-bit arithmetic due to the guarantee that the final answer does not exceed $10^{18}$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(i \cdot \log_k(i k^n))$ | $O(1)$ | Too slow |
| Optimal | $O(\log n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

## 1. Interpret the condition in base $k$

A number ending with $n$ zeros in base $k$ means it is divisible by $k^n$. This converts a digit-based condition into a pure arithmetic divisibility condition.

## 2. Compute $k^n$

We compute $p = k^n$ using fast exponentiation. This step is necessary because direct multiplication $n$ times could overflow or be inefficient if $n$ were larger.

## 3. Construct the sequence

All valid numbers form an arithmetic progression:

$$p, 2p, 3p, \dots$$

So the $i$-th valid number is simply $i \cdot p$.

## 4. Output the result

Return $i \cdot k^n$ as the answer in decimal form.

### Why it works

The key invariant is that every number with at least $n$ trailing zeros in base $k$ is exactly a multiple of $k^n$, and every multiple of $k^n$ has at least $n$ trailing zeros. This is a direct consequence of positional representation: each trailing zero corresponds to a factor of $k$. Therefore, ordering numbers by increasing value preserves the ordering of multiples, and the $i$-th valid number is exactly the $i$-th multiple of $k^n$.

## Python Solution

```python
import sys
input = sys.stdin.readline

def pow_fast(a, e):
    res = 1
    while e > 0:
        if e & 1:
            res *= a
        a *= a
        e >>= 1
    return res

def solve():
    k = int(input())
    n = int(input())
    i = int(input())

    p = pow_fast(k, n)
    print(i * p)

if __name__ == "__main__":
    solve()
```

The implementation first reads $k$, $n$, and $i$. It computes $k^n$ using binary exponentiation, which repeatedly squares the base and multiplies it into the result when the current exponent bit is set. Finally, it multiplies the result by $i$, directly producing the $i$-th multiple of $k^n$.

A subtle point is that we never explicitly check for trailing zeros or perform base conversion. The entire digit-based condition is absorbed into exponentiation.

## Worked Examples

Consider $k = 10$, $n = 2$, $i = 3$.

| Step | Value |
| --- | --- |
| Compute $10^2$ | 100 |
| Sequence | 100, 200, 300, ... |
| 3rd element | 300 |

This confirms that numbers ending in two zeros in base 10 are exactly multiples of 100, and indexing is direct.

Now consider $k = 2$, $n = 3$, $i = 5$.

| Step | Value |
| --- | --- |
| Compute $2^3$ | 8 |
| Sequence | 8, 16, 24, 32, 40, ... |
| 5th element | 40 |

This example demonstrates that the base does not matter in the final arithmetic form; only $k^n$ matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log n)$ | binary exponentiation for $k^n$ plus constant-time multiplication |
| Space | $O(1)$ | only a few integer variables are used |

The constraints allow up to $n = 100$, so exponentiation is effectively constant-time in practice. The result bound of $10^{18}$ ensures Python integers remain manageable.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def pow_fast(a, e):
        res = 1
        while e > 0:
            if e & 1:
                res *= a
            a *= a
            e >>= 1
        return res

    k = int(sys.stdin.readline())
    n = int(sys.stdin.readline())
    i = int(sys.stdin.readline())

    p = pow_fast(k, n)
    return str(i * p)

# basic cases
assert run("10\n2\n3\n") == "300"
assert run("2\n3\n5\n") == "40"

# n = 0 case
assert run("7\n0\n10\n") == "10"

# small base
assert run("3\n1\n4\n") == "12"

# large i, small exponent
assert run("10\n1\n1000000\n") == "10000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 10,2,3 | 300 | standard decimal trailing zeros |
| 2,3,5 | 40 | non-decimal base behavior |
| 7,0,10 | 10 | edge case n = 0 |
| 3,1,4 | 12 | minimal non-zero exponent |
| 10,1,1000000 | 10000000 | large index scaling |

## Edge Cases

When $n = 0$, every number is valid because every integer has at least zero trailing zeros in any base. The formula still works because $k^0 = 1$, so the answer becomes $i \cdot 1 = i$, matching the expected sequence.

When $k = 2$ and $n$ is large, say $n = 60$, we compute $2^{60}$, which is still within 64-bit range. The sequence becomes multiples of $2^{60}$, and the $i$-th term is simply a scaled integer. The algorithm never depends on binary representation structure directly, so there is no risk of misinterpreting trailing zeros.

When $i = 1$, the answer is exactly $k^n$. This is the smallest valid number, and the algorithm correctly returns it without any off-by-one adjustment because indexing starts from the first multiple.
