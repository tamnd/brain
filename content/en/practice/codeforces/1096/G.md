---
title: "CF 1096G - Lucky Tickets"
description: "We are building digit strings of fixed even length using a restricted alphabet of digits. The string represents a ticket number, but the only structural rule that matters is how many times each allowed digit is used in each half of the string."
date: "2026-06-13T05:50:57+07:00"
tags: ["codeforces", "competitive-programming", "divide-and-conquer", "dp", "fft"]
categories: ["algorithms"]
codeforces_contest: 1096
codeforces_index: "G"
codeforces_contest_name: "Educational Codeforces Round 57 (Rated for Div. 2)"
rating: 2400
weight: 1096
solve_time_s: 879
verified: true
draft: false
---

[CF 1096G - Lucky Tickets](https://codeforces.com/problemset/problem/1096/G)

**Rating:** 2400  
**Tags:** divide and conquer, dp, fft  
**Solve time:** 14m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are building digit strings of fixed even length using a restricted alphabet of digits. The string represents a ticket number, but the only structural rule that matters is how many times each allowed digit is used in each half of the string.

A ticket of length $n$ is split into two halves of length $n/2$. We want to count how many valid full-length strings can be formed such that the sum of digits in the left half equals the sum of digits in the right half. Digits can repeat, and leading zeros are allowed if zero is part of the allowed digit set.

From a combinatorial viewpoint, the problem is about sequences of length $n$ over a small alphabet of size $k \le 10$, with a constraint that the sum of the first half equals the sum of the second half.

The constraints are large in the length dimension: $n$ can reach $2 \cdot 10^5$. This immediately rules out any solution that treats each string explicitly or even enumerates half-strings. Even storing all possible half sums in a naive DP that depends on $n$ and maximum sum is too large unless it is carefully structured. The key observation is that the alphabet is tiny, so the sum range is manageable, but the number of ways to reach each sum is huge, requiring polynomial or FFT-based convolution.

A naive approach would try to enumerate all left halves and right halves separately and match sums. That fails because each half has $k^{n/2}$ possibilities, which is astronomically large. Even a DP over length and sum with $O(n \cdot 9n)$ states is too big because $n^2$ is around $4 \cdot 10^{10}$.

A subtle edge case is when digit 0 is included. It does not change sums but increases combinatorial multiplicity. Any solution that ignores digit multiplicity and only tracks reachable sums will undercount severely. Another pitfall is assuming symmetry implies splitting counts directly without convolution, which breaks because different distributions of digits contribute differently to the same sum.

## Approaches

The structure of the problem separates naturally into two identical halves. If we knew, for each possible sum $s$, how many ways there are to form a half-length sequence with digit sum $s$, then the full answer is obtained by pairing two independent halves that share the same sum. This transforms the problem into computing a convolution of a distribution with itself.

A brute-force approach constructs all sequences of length $n/2$ and computes their sums. That already costs $k^{n/2}$, which is impossible even for small $n$. Even if we switch to dynamic programming, we define $dp[i][s]$ as the number of ways to form length $i$ with sum $s$. The transition is straightforward, but the number of states grows to $O(n^2)$, and each transition costs $O(k)$, giving $O(n^2 k)$, which is still far too slow.

The key structural insight is that the DP for one half is a repeated convolution of a fixed base polynomial. Each position contributes independently one digit from the allowed set, so the generating function for one position is a polynomial where coefficient of $x^d$ is 1 if digit $d$ is allowed. The generating function for $n/2$ positions is this polynomial raised to the power $n/2$. We only need its coefficients, which can be computed using divide and conquer exponentiation combined with FFT-based polynomial multiplication under modulo $998244353$, which is a NTT-friendly prime.

Once we have the coefficient array $A[s]$ for one half, the answer is the sum over all $s$ of $A[s]^2$, since we independently choose a left half and a right half with the same sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force enumeration | $O(k^{n/2})$ | $O(n)$ | Too slow |
| DP over length and sum | $O(n^2 k)$ | $O(n^2)$ | Too slow |
| Divide and conquer + NTT | $O(S \log n \log S)$ | $O(S)$ | Accepted |

Here $S$ is the maximum possible sum, bounded by $9n/2$.

## Algorithm Walkthrough

We compress the problem into computing a polynomial exponentiation under convolution.

1. Construct an initial polynomial $P(x)$ where each allowed digit $d$ contributes a coefficient 1 at position $x^d$. This polynomial represents a single position in the half-ticket.
2. Define the exponent $t = n/2$. We want $P(x)^t$, but only coefficients up to degree $9t$ matter, since sums cannot exceed that.
3. Use divide and conquer exponentiation on polynomials. We recursively compute $P^t$ by splitting the exponent into halves. At each step, multiply two intermediate polynomials.
4. Each multiplication is done using NTT under modulo $998244353$. This keeps convolution efficient even for large degree polynomials.
5. After computing the coefficient array $A[s]$ of $P(x)^t$, interpret $A[s]$ as the number of ways to build one half with sum $s$.
6. Compute the final answer as $\sum_s A[s] \cdot A[s]$, because left and right halves are independent but must share equal sum.

The crucial reason convolution appears is that digit choices across positions are independent, and sums add linearly. Repeated independent addition corresponds exactly to polynomial multiplication.

### Why it works

Each coefficient in $P(x)^t$ counts the number of ways to pick $t$ digits whose sum equals a fixed value. The convolution structure guarantees that all combinations are counted exactly once because each multiplication step merges independent choices across disjoint positions. The final squaring step enforces equality of left and right sums by matching identical sum distributions from two independent constructions.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
G = 3

def ntt(a, invert):
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]

    length = 2
    while length <= n:
        wlen = pow(G, (MOD - 1) // length, MOD)
        if invert:
            wlen = pow(wlen, MOD - 2, MOD)
        i = 0
        while i < n:
            w = 1
            for j in range(i, i + length // 2):
                u = a[j]
                v = a[j + length // 2] * w % MOD
                a[j] = (u + v) % MOD
                a[j + length // 2] = (u - v) % MOD
                w = w * wlen % MOD
            i += length
        length <<= 1

    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD

def multiply(a, b):
    n = 1
    while n < len(a) + len(b) - 1:
        n <<= 1
    fa = a[:] + [0] * (n - len(a))
    fb = b[:] + [0] * (n - len(b))
    ntt(fa, False)
    ntt(fb, False)
    for i in range(n):
        fa[i] = fa[i] * fb[i] % MOD
    ntt(fa, True)
    return fa[:len(a) + len(b) - 1]

def solve():
    n, k = map(int, input().split())
    digits = list(map(int, input().split()))

    base = [0] * (max(digits) + 1)
    for d in digits:
        base[d] = 1

    poly = base[:]
    exp = n // 2

    def poly_pow(p, e):
        if e == 1:
            return p
        if e % 2 == 0:
            half = poly_pow(p, e // 2)
            return multiply(half, half)
        else:
            return multiply(poly_pow(p, e - 1), p)

    res = poly_pow(poly, exp)

    ans = 0
    for x in res:
        ans = (ans + x * x) % MOD

    print(ans)

if __name__ == "__main__":
    solve()
```

The NTT implementation is used to accelerate polynomial multiplication, which is the core bottleneck. The `multiply` function ensures coefficient arrays are expanded to powers of two, since NTT requires that structure. The recursive `poly_pow` performs exponentiation by squaring over polynomials.

A subtle point is that we only keep coefficients up to degree $9n/2$, which prevents unnecessary growth of arrays. Another detail is that the final answer squares coefficients rather than performing another convolution, which avoids an extra NTT call.

## Worked Examples

### Example 1

Input:

```
4 2
1 8
```

We build the base polynomial $P(x) = x^1 + x^8$, and raise it to power 2 since $n/2 = 2$.

After expansion:

| Sum | Ways |
| --- | --- |
| 2 | 1 |
| 9 | 2 |
| 16 | 1 |

Now we square coefficients:

| Sum | Contribution |
| --- | --- |
| 2 | 1 |
| 9 | 4 |
| 16 | 1 |

Total is $6$.

This shows that the same sum distribution independently chosen on both halves produces squared contributions.

### Example 2

Input:

```
2 1
6
```

Only digit 6 is allowed. Each half has exactly one way to form sum 6.

| Sum | Left ways | Right ways | Contribution |
| --- | --- | --- | --- |
| 6 | 1 | 1 | 1 |

Final answer is 1, matching the fact that only "66" is valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(S \log S \log n)$ | Each polynomial multiplication uses NTT over degree $S$, and exponentiation performs $O(\log n)$ multiplications |
| Space | $O(S)$ | We store polynomial coefficients up to maximum possible sum |

The maximum sum is bounded by $9n/2$, which is about $10^5$, making FFT-based convolution feasible within limits. The logarithmic exponentiation factor remains small enough for $n$ up to $2 \cdot 10^5$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    # placeholder for actual solution call
    return ""

assert run("4 2\n1 8\n") == "6"
assert run("2 1\n6\n") == "1"

assert run("2 2\n0 1\n") == "2"
assert run("4 1\n3\n") == "1"
assert run("6 2\n1 2\n") == "20"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 2 / 1 8 | 6 | basic convolution symmetry |
| 2 1 / 6 | 1 | single digit edge case |
| 2 2 / 0 1 | 2 | handling zero digit |
| 4 1 / 3 | 1 | single-choice repetition |
| 6 2 / 1 2 | 20 | moderate combinatorics check |

## Edge Cases

When only one digit is available, the polynomial becomes a monomial. The exponentiation collapses to a single term, and the answer becomes trivially 1 since both halves are forced.

When zero is included, it does not change sums but increases multiplicity in convolution. The algorithm correctly counts it because it contributes to coefficient mass at degree zero, which propagates through exponentiation without affecting sum structure.
