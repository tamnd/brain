---
title: "CF 105122G - Modest Numbers"
description: "We are asked to count integers in a range $[a, b]$ such that each integer has exactly seven positive divisors. The task is not about factoring arbitrary numbers efficiently online, but about understanding the structure of numbers whose divisor function equals seven."
date: "2026-06-27T19:39:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105122
codeforces_index: "G"
codeforces_contest_name: "XXVI Interregional Programming Olympiad, Vologda SU, 2024"
rating: 0
weight: 105122
solve_time_s: 72
verified: false
draft: false
---

[CF 105122G - Modest Numbers](https://codeforces.com/problemset/problem/105122/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to count integers in a range $[a, b]$ such that each integer has exactly seven positive divisors. The task is not about factoring arbitrary numbers efficiently online, but about understanding the structure of numbers whose divisor function equals seven.

The input consists of two very large integers, up to $10^{18}$, defining a closed interval. The output is the number of integers inside this interval whose divisor count is exactly seven.

The constraint immediately rules out any approach that iterates through the range. Even a single pass over a range of size $10^{18}$ is impossible. Any valid solution must instead characterize all numbers with exactly seven divisors and generate only those candidates.

A common pitfall is to attempt on-the-fly factorization per number in the range. Even if each factorization is optimized to $O(\sqrt{n})$, the range size makes this approach unusable.

Another subtle issue is assuming “exactly seven divisors” behaves similarly to common cases like 2, 4, or 6 divisors. For seven, the structure is highly constrained, and missing that structure leads to completely wrong solution spaces.

## Approaches

We start from the most direct idea: for each number $x \in [a, b]$, compute its divisor count by iterating up to $\sqrt{x}$, counting divisor pairs. This is correct but completely infeasible. In the worst case, even checking a single number near $10^{18}$ requires up to $10^9$ iterations, and we would need to do this for up to $10^{18}$ numbers.

The key observation is to classify numbers with exactly seven divisors. Since seven is a prime number, the divisor-count formula forces a very rigid structure on the prime factorization.

If a number $n = p_1^{e_1} p_2^{e_2} \cdots$, then the number of divisors is $(e_1+1)(e_2+1)\cdots$. For this product to equal 7, a prime number, only one factor can exist. That means the number must be of the form $p^6$, where $p$ is prime.

So every valid number is exactly a sixth power of a prime. This reduces the problem to: count primes $p$ such that $p^6 \in [a, b]$. Equivalently, we need primes in the interval:

$$\lceil a^{1/6} \rceil \le p \le \lfloor b^{1/6} \rfloor.$$

The range of $p$ is at most $(10^{18})^{1/6} = 10^3$, so we only need primes up to 1000. We can precompute primes once using a sieve and then count how many satisfy the bound.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(b-a)$ or worse | $O(1)$ | Too slow |
| Optimal (prime sieve + filtering) | $O(\sqrt[6]{b} + \log \log \sqrt[6]{b})$ | $O(\sqrt[6]{b})$ | Accepted |

## Algorithm Walkthrough

1. Compute the integer lower and upper bounds for the prime base. We find all integers $p$ such that $p^6$ lies in $[a, b]$. This is done by computing integer sixth roots of $a$ and $b$, taking care to adjust for rounding errors.
2. Precompute all primes up to $\lfloor b^{1/6} \rfloor$ using a sieve of Eratosthenes. This works efficiently because the limit is at most 1000.
3. Iterate over all primes $p$ from the sieve.
4. For each prime $p$, check whether it lies within the computed range. If yes, it contributes exactly one valid number $p^6$.
5. Count all such primes and output the result.

### Why it works

The divisor-count function is multiplicative and equals 7 only when the prime factorization contains exactly one prime raised to the sixth power. No other factorization can produce a prime number of divisors because any additional prime factor would multiply the divisor count by at least 2. This restriction reduces the entire problem to a bounded prime counting problem over a very small interval.

## Python Solution

```python
import sys
input = sys.stdin.readline

def iroot6(x: int) -> int:
    lo, hi = 1, 10**3 + 5
    while lo <= hi:
        mid = (lo + hi) // 2
        v = mid**6
        if v <= x:
            lo = mid + 1
        else:
            hi = mid - 1
    return hi

def sieve(n: int):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return is_prime

def solve():
    a = int(input().strip())
    b = int(input().strip())

    hi = iroot6(b)
    lo = iroot6(a)

    if lo**6 < a:
        lo += 1

    is_prime = sieve(hi)

    ans = 0
    for p in range(lo, hi + 1):
        if is_prime[p]:
            ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The core of the solution is the sixth-root computation. We avoid floating-point instability by using integer binary search, ensuring correctness even near large boundaries. The adjustment `if lo**6 < a: lo += 1` fixes the edge case where the computed lower bound rounds down to a value whose sixth power is still outside the interval.

The sieve is run only up to about 1000, which makes it extremely fast. We then filter primes in the restricted range, which directly corresponds to valid sixth powers.

## Worked Examples

### Example 1

Input:

```
50
100
```

We compute sixth roots:

$$50^{1/6} \approx 1,\quad 100^{1/6} \approx 2$$

So candidate primes are in $[1, 2]$. Only prime is 2.

| Step | lo | hi | candidate p | p prime? | count |
| --- | --- | --- | --- | --- | --- |
| init | 1 | 2 | - | - | 0 |
| p=1 | 1 | 2 | 1 | no | 0 |
| p=2 | 1 | 2 | 2 | yes | 1 |

Only $2^6 = 64$ lies in the range, so answer is 1.

This confirms that only one valid sixth power exists inside the interval.

### Example 2

Input:

```
1
1000000000000000000
```

We compute:

$$b^{1/6} = 1000$$

So we count primes $p \le 1000$.

| Step | p range | action | count |
| --- | --- | --- | --- |
| init | 2..1000 | sieve primes | 0 |
| scan | primes ≤ 1000 | count all | 168 |

This shows the solution reduces a massive range query into a fixed prime counting task.

The trace confirms that the algorithm depends only on bounding the exponent space, not on scanning the original interval.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\sqrt[6]{b} \log \log \sqrt[6]{b})$ | sieve up to 1000 plus linear scan of primes |
| Space | $O(\sqrt[6]{b})$ | boolean array for sieve |

The bound $\sqrt[6]{10^{18}} \le 1000$ makes the solution effectively constant time in practice. Both memory and runtime are trivial under the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue().strip() if False else ""

# direct inline solution for testing
def solve_test(inp: str) -> str:
    import sys
    from io import StringIO

    def iroot6(x: int) -> int:
        lo, hi = 1, 10**3 + 5
        while lo <= hi:
            mid = (lo + hi) // 2
            v = mid**6
            if v <= x:
                lo = mid + 1
            else:
                hi = mid - 1
        return hi

    def sieve(n: int):
        is_prime = [True] * (n + 1)
        is_prime[0] = is_prime[1] = False
        for i in range(2, int(n**0.5) + 1):
            if is_prime[i]:
                for j in range(i * i, n + 1, i):
                    is_prime[j] = False
        return is_prime

    old = sys.stdin
    sys.stdin = StringIO(inp)

    a = int(input().strip())
    b = int(input().strip())

    hi = iroot6(b)
    lo = iroot6(a)
    if lo**6 < a:
        lo += 1

    is_prime = sieve(hi)

    ans = sum(1 for p in range(lo, hi + 1) if is_prime[p])

    sys.stdin = old
    return str(ans)

# samples
assert solve_test("50\n100\n") == "1"

# custom cases
assert solve_test("1\n63\n") == "0"
assert solve_test("1\n64\n") == "1"
assert solve_test("64\n64\n") == "1"
assert solve_test("1\n1000000000000000000\n") == "168"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 63 | 0 | no sixth power of prime yet |
| 1 64 | 1 | boundary inclusion of 2^6 |
| 64 64 | 1 | single-point range |
| 1 10^18 | 168 | full prime set up to 1000 |

## Edge Cases

One edge case occurs when the lower bound is just above a valid sixth power. For example, if $a = 65$, then $a^{1/6}$ rounds down to 2, but $2^6 = 64$ is not inside the interval. The adjustment step `if lo**6 < a: lo += 1` ensures we exclude this incorrectly included candidate.

Another case is when $a$ and $b$ are very small. For $a = b = 1$, the sixth-root computation produces $lo = hi = 1$, but 1 is not prime, so the sieve correctly yields zero.

A final case is when the range is large but contains all valid numbers. For $a = 1$, $b = 10^{18}$, the algorithm counts all primes up to 1000. The sieve guarantees correctness because every valid number corresponds uniquely to a prime base and no duplicates or gaps exist in the mapping.
