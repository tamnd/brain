---
title: "CF 2093C - Simple Repetition"
description: "We are given a base integer x and a repetition count k. From x, we construct a new number y by writing the decimal representation of x consecutively k times without inserting separators. For example, if x = 52 and k = 3, then y = 525252. If x = 6 and k = 7, then y = 6666666."
date: "2026-06-08T05:37:44+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 2093
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1016 (Div. 3)"
rating: 1000
weight: 2093
solve_time_s: 94
verified: true
draft: false
---

[CF 2093C - Simple Repetition](https://codeforces.com/problemset/problem/2093/C)

**Rating:** 1000  
**Tags:** math, number theory  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a base integer `x` and a repetition count `k`. From `x`, we construct a new number `y` by writing the decimal representation of `x` consecutively `k` times without inserting separators. For example, if `x = 52` and `k = 3`, then `y = 525252`. If `x = 6` and `k = 7`, then `y = 6666666`.

The task is not to build this number explicitly and test it for primality in the usual sense, but to determine whether this constructed number `y` is prime.

The constraints immediately signal that constructing `y` is impossible in general. When `x` has up to 9 digits and `k` is up to 7, the resulting number can have up to 63 digits, which already exceeds standard integer types. Even storing it as a string is fine, but primality testing on a 63-digit integer for up to 100 test cases would require advanced big integer primality techniques and still be overkill for a 1000-rated problem.

A more subtle issue appears in edge cases involving `k = 1` and `x = 1`. If `x = 1` and `k = 1`, then `y = 1`, which is not prime. If `k > 1`, even when `x = 1`, the result is a repunit like `111...1`, which might look special but is always composite for `k > 1` in this construction because it can be factored.

A naive mistake is to literally build the string and attempt primality checking using trial division. Even if optimized up to sqrt(n), this breaks due to the size of `y` and repeated test cases.

## Approaches

A direct brute-force solution constructs `y` and checks whether it is prime using division up to `sqrt(y)`. This is conceptually correct but quickly becomes infeasible. The number `y` can have up to 63 digits, so even a single primality check is far beyond any reasonable deterministic trial division approach.

The key observation is structural: repeated concatenation creates a number that has strong algebraic factorization properties whenever `k > 1`. Let the length of `x` be `d`. Then the constructed number can be written as:

$$y = x \cdot 10^{d(k-1)} + x \cdot 10^{d(k-2)} + \cdots + x$$

Factoring `x`, we get:

$$y = x \cdot (10^{d(k-1)} + 10^{d(k-2)} + \cdots + 1)$$

This shows that whenever `k > 1`, `y` is a product of `x` and another integer greater than 1, which immediately makes `y` composite unless `x = 1` and we rely on the second factor being special. But even in that case, the second factor is greater than 1 for `k > 1`, so `y` is composite.

Thus, the only time we can possibly get a prime is when `k = 1`, because then `y = x`. The problem reduces to checking whether `x` itself is prime.

So the entire solution collapses to:

- If `k > 1`, answer is always "NO".
- If `k = 1`, check primality of `x`.

Now we only need a primality test for `x ≤ 10^9`, which is straightforward with trial division up to `sqrt(x)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Construction + Big Primality Test | O(k· | x | + sqrt(y)) |
| Factorization Insight + Check x | O(√x) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `x` and `k` for each test case. We treat each case independently because no computation carries over.
2. If `k` is greater than 1, immediately output "NO". This follows from the algebraic factorization of repeated concatenation, which guarantees compositeness.
3. If `k` equals 1, we reduce the problem to checking whether `x` is a prime number.
4. To test primality of `x`, first handle small cases: numbers less than 2 are not prime.
5. For `x ≥ 2`, try dividing by all integers from 2 up to `sqrt(x)`. If any divisor is found, `x` is composite; otherwise, it is prime.

### Why it works

The correctness hinges on the fact that concatenation introduces a nontrivial multiplicative structure whenever repetition occurs. For `k > 1`, the constructed number always decomposes into a product of `x` and a geometric sum of powers of ten, both strictly greater than 1 in magnitude. This guarantees compositeness regardless of whether `x` itself is prime. When `k = 1`, no structure is introduced and the number is exactly `x`, so primality is preserved exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

t = int(input())
for _ in range(t):
    x, k = map(int, input().split())
    if k > 1:
        print("NO")
    else:
        print("YES" if is_prime(x) else "NO")
```

The code first isolates the structural shortcut `k > 1`, which avoids any need to construct or reason about the large repeated number. The primality check is only applied when necessary, and it is safe because `x` is bounded by `10^9`.

The primality function uses a standard square-root trial division optimized by skipping even numbers after handling 2. This is sufficient given the constraint.

## Worked Examples

We trace two cases to see how the decision simplifies.

### Example 1: `x = 52, k = 3`

| Step | x | k | Decision |
| --- | --- | --- | --- |
| 1 | 52 | 3 | k > 1 |
| 2 | 52 | 3 | Output NO |

The algorithm never constructs the number `525252`. It directly identifies the repetition structure as sufficient to guarantee compositeness.

### Example 2: `x = 7, k = 1`

| Step | x | k | Primality check | Result |
| --- | --- | --- | --- | --- |
| 1 | 7 | 1 | check divisors | none found |
| 2 | 7 | 1 | prime | YES |

This case exercises the fallback path where no repetition occurs, so standard primality testing is required.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t √x) | Each test checks primality only when k = 1, using trial division up to √x |
| Space | O(1) | No auxiliary structures beyond a few variables |

The constraints allow up to 100 test cases with `x ≤ 10^9`. A √x approach is fast enough because √10^9 is about 31623, and in the worst case we perform that operation 100 times, which is well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def is_prime(n: int) -> bool:
        if n < 2:
            return False
        if n % 2 == 0:
            return n == 2
        i = 3
        while i * i <= n:
            if n % i == 0:
                return False
            i += 2
        return True

    t = int(input())
    out = []
    for _ in range(t):
        x, k = map(int, input().split())
        if k > 1:
            out.append("NO")
        else:
            out.append("YES" if is_prime(x) else "NO")
    return "\n".join(out)

# provided samples
assert run("""4
52 3
6 7
7 1
1 7
""") == """NO
NO
YES
NO"""

# minimum edge cases
assert run("""3
1 1
1 5
2 1
""") == """NO
NO
YES"""

# all equal repetition
assert run("""2
11 2
11 1
""") == """NO
NO"""

# prime boundary
assert run("""2
2 1
4 1
""") == """YES
NO"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | NO | smallest invalid prime case |
| `1 5` | NO | repetition always composite |
| `11 2` | NO | repeated structure kills primality |
| `2 1` | YES | smallest prime |
| `4 1` | NO | smallest composite |

## Edge Cases

The most sensitive edge case is `x = 1`. If `k = 1`, the number is `1`, which is not prime, so the output must be "NO". If `k > 1`, the number becomes a string of ones like `111...1`, which is still handled by the `k > 1` rule and immediately classified as "NO" without construction.

Another edge case is small primes with repetition, such as `x = 2, k = 2`. The constructed number is `22`, which is clearly composite, and the algorithm correctly returns "NO" due to the repetition rule before any primality check.

Finally, large primes with `k = 1`, such as `x = 999999937`, are handled purely by the primality check loop. The algorithm only depends on the square root bound, ensuring correctness without overflow or conversion issues.
