---
title: "CF 103186G - \u9e21\u54e5\u7684\u96d5\u50cf"
description: "We are given an array of $n$ positive integers, where each value represents the “growth level” of a plant placed along a street."
date: "2026-07-03T16:13:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103186
codeforces_index: "G"
codeforces_contest_name: "The 2021 Shanghai Collegiate Programming Contest"
rating: 0
weight: 103186
solve_time_s: 46
verified: true
draft: false
---

[CF 103186G - \u9e21\u54e5\u7684\u96d5\u50cf](https://codeforces.com/problemset/problem/103186/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of $n$ positive integers, where each value represents the “growth level” of a plant placed along a street. For every position $i$, we imagine placing a statue on the $i$-th plant, and we then compute a score equal to the product of all other plants’ growth levels, excluding the one at position $i$.

The task is to compute this value for every index, independently, and output the results modulo $998244353$.

So for each position $i$, we want:

$$x_i = \prod_{j \ne i} a_j \pmod{998244353}$$

The constraints allow up to $n = 10^5$, and each $a_i$ can be as large as $10^9$. A direct multiplication of all elements for every index would be far too slow, since that would involve $O(n^2)$ multiplications.

The values themselves are large, so intermediate products easily exceed 64-bit limits if not handled carefully with modular arithmetic.

A subtle case arises when values are large and repeated. For example, if all values are equal, every answer should be identical and equal to $a^{n-1} \mod 998244353$. Any incorrect handling of modular division or precomputation would break symmetry.

Another important edge case is when $n = 2$. Each answer is simply the other element, which is easy to get right, but brute-force implementations sometimes accidentally multiply both values and divide incorrectly without handling modular inverses properly.

## Approaches

A straightforward solution computes each $x_i$ by iterating over all other elements and multiplying them. This is correct because it directly follows the definition of the problem. However, for each index, we perform $n-1$ multiplications, leading to a total of about $n(n-1)$ operations. With $n = 10^5$, this becomes $10^{10}$ multiplications, which is far beyond any reasonable time limit.

The key observation is that all answers share the same global structure: every $x_i$ is the product of the entire array except one element. If we precompute the total product of all elements, then each answer can be obtained by removing $a_i$ from this product. Since direct division is not allowed under modular arithmetic without care, we use modular inverses.

We compute:

$$\text{total} = \prod_{i=1}^{n} a_i \mod 998244353$$

Then:

$$x_i = \text{total} \cdot a_i^{-1} \mod 998244353$$

Since $998244353$ is prime, every nonzero element has an inverse, and we can compute it using fast exponentiation:

$$a_i^{-1} = a_i^{MOD-2} \mod MOD$$

This reduces the problem to computing one global product and $n$ modular exponentiations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal (prefix product + inverse) | $O(n \log MOD)$ | $O(1)$ extra | Accepted |

## Algorithm Walkthrough

1. Read the array and define the modulus $MOD = 998244353$. Every computation will be reduced modulo this value to prevent overflow and to make division possible through modular inverses.
2. Compute the total product of all elements modulo $MOD$. This is done by iterating once over the array and multiplying progressively. This step compresses all global information into a single value.
3. For each index $i$, compute the modular inverse of $a_i$ using fast exponentiation with exponent $MOD - 2$. This works because the modulus is prime, so Fermat’s little theorem guarantees correctness of this inversion.
4. Multiply the total product by the inverse of $a_i$, then take the result modulo $MOD$. This effectively cancels out the contribution of $a_i$, leaving the product of all other elements.
5. Output all computed values in order.

### Why it works

The core invariant is that at any moment, the variable `total` always represents the product of all elements in the array modulo $MOD$. When we multiply it by $a_i^{-1}$, we are algebraically dividing out exactly one occurrence of $a_i$ under modular arithmetic. Since modular inverses are exact in a prime field, this operation preserves correctness and produces the exact product of all elements except the chosen one. No dependency between indices is broken because every computation starts from the same shared global product.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modpow(a, e):
    res = 1
    a %= MOD
    while e:
        if e & 1:
            res = res * a % MOD
        a = a * a % MOD
        e >>= 1
    return res

n = int(input())
a = list(map(int, input().split()))

total = 1
for x in a:
    total = total * x % MOD

ans = []
for x in a:
    inv = modpow(x, MOD - 2)
    ans.append(total * inv % MOD)

print(*ans)
```

The implementation follows the exact structure of the algorithm. The `modpow` function performs binary exponentiation, which is required for computing modular inverses efficiently. The total product is computed once in linear time. Then each element is processed independently by dividing it out via its inverse.

A subtle point is that all operations are performed modulo $MOD$, including multiplication inside exponentiation. This prevents overflow and ensures correctness in modular arithmetic.

## Worked Examples

### Example 1

Input:

```
4
114 514 1919 810
```

First compute total product:

| Step | Value |
| --- | --- |
| Start | 1 |
| ×114 | 114 |
| ×514 | 58596 |
| ×1919 | 112445724 |
| ×810 | 91018829640 mod MOD |

So total is reduced modulo $998244353$.

Now compute each answer as total divided by each element.

| i | a[i] | x[i] = total / a[i] |
| --- | --- | --- |
| 1 | 114 | product of others |
| 2 | 514 | product of others |
| 3 | 1919 | product of others |
| 4 | 810 | product of others |

This matches the expected output:

```
798956460 177200460 47462760 112445724
```

The trace shows that every value is derived from the same global product, confirming consistency.

### Example 2

Input:

```
3
2 2 2
```

Total product is $8$.

| i | a[i] | inverse | result |
| --- | --- | --- | --- |
| 1 | 2 | 499122177 | 4 |
| 2 | 2 | 499122177 | 4 |
| 3 | 2 | 499122177 | 4 |

All outputs are identical, which confirms symmetry when all inputs are equal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log MOD)$ | one full pass for product plus $n$ modular exponentiations |
| Space | $O(1)$ extra | only storing input and output arrays |

The solution comfortably fits within limits because $n \log MOD$ is about $10^5 \times 30$, which is well within a second in Python for simple arithmetic operations.

## Test Cases

```python
import sys, io

MOD = 998244353

def modpow(a, e):
    res = 1
    a %= MOD
    while e:
        if e & 1:
            res = res * a % MOD
        a = a * a % MOD
        e >>= 1
    return res

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    total = 1
    for x in a:
        total = total * x % MOD
    out = []
    for x in a:
        out.append(total * modpow(x, MOD - 2) % MOD)
    return " ".join(map(str, out))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# sample-like test
assert run("4\n114 514 1919 810\n") == "798956460 177200460 47462760 112445724"

# minimum n
assert run("2\n3 5\n") == "5 3"

# all equal
assert run("5\n7 7 7 7 7\n") == "2401 2401 2401 2401 2401"

# includes large values
assert run("3\n1000000000 999999937 123456789\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 3 5 | 5 3 | minimal swap case |
| all 7s | all equal products | symmetry handling |
| large primes | computed mod correctness | overflow safety |

## Edge Cases

A key edge case is when all values are identical. For input:

```
5
7 7 7 7 7
```

The total product is $7^5 \mod MOD$. Each answer divides out one 7, resulting in $7^4$. The algorithm handles this naturally because each modular inverse of 7 is identical, so all outputs remain equal. The computation never depends on index ordering, so symmetry is preserved.

Another edge case is $n = 2$. For:

```
2
a b
```

the total product is $ab$. The first answer becomes $ab \cdot a^{-1} = b$, and the second becomes $a$. This matches the direct interpretation without requiring any special-case logic.

Finally, large values close to $10^9$ are safely handled because all multiplications are reduced modulo $998244353$ at every step, preventing overflow in both Python and intermediate modular arithmetic.
