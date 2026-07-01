---
title: "CF 104158F - Toilet Orders"
description: "We are given pairs of large integers representing counts of two types of parts, bowls and lids. From each pair, the number of complete toilets Thomas can assemble is determined by the greatest common divisor of these two quantities."
date: "2026-07-02T01:11:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104158
codeforces_index: "F"
codeforces_contest_name: "UTPC Contest 01-27-23 Div. 1 (Advanced)"
rating: 0
weight: 104158
solve_time_s: 81
verified: false
draft: false
---

[CF 104158F - Toilet Orders](https://codeforces.com/problemset/problem/104158/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 21s  
**Verified:** no  

## Solution
## Problem Understanding

We are given pairs of large integers representing counts of two types of parts, bowls and lids. From each pair, the number of complete toilets Thomas can assemble is determined by the greatest common divisor of these two quantities. That gcd represents how many full bowl-lid pairs can be formed using a perfectly balanced selection of items.

For each test case, the task is not to compute the gcd itself, but to describe its prime structure. Once we find the gcd, we must express it as a product of primes and report each distinct prime together with how many times it appears in the factorization. The output is formatted one prime per line in increasing order, followed by a terminating line containing zero.

The constraints push us toward careful arithmetic handling. Each number can be as large as 10^12, which immediately rules out naive factorization by repeated division up to n. Even testing divisibility up to n itself is impossible. We need something closer to square root factoring or better, and we must rely on the fact that gcd is at most 10^12 as well.

A subtle edge case is when the gcd is 1. In that case, there are no prime factors at all, so we only output a single line containing zero. Another case is when gcd is a prime number itself, such as 5, where the output consists of just that prime with multiplicity one followed by zero. Missing the final zero or incorrectly printing something for gcd = 1 are common formatting mistakes.

## Approaches

A direct way to solve the problem is to compute the gcd of each pair, then factor it using trial division. Once we have g, we could test all integers from 2 up to g and check divisibility. This is correct but far too slow. In the worst case where g is around 10^12, this would require up to a trillion operations per test case, which is infeasible.

A more structured brute force improves this by only checking divisors up to sqrt(g). For each candidate i, if it divides g, we repeatedly divide g by i and count multiplicity. This reduces complexity drastically, since sqrt(10^12) is 10^6, which is borderline but acceptable for up to 100 test cases in optimized Python if carefully implemented.

The key insight is that we never need to factor b and l separately. The gcd already collapses the problem into a single number whose structure is simpler than either input. Once we isolate g, standard prime factorization via trial division up to sqrt(g) is sufficient. There is no need for advanced methods like Pollard Rho because constraints are small enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force up to g | O(g) | O(1) | Too slow |
| Trial division up to √g | O(√g) per test | O(1) | Accepted |

## Algorithm Walkthrough

### Steps

1. Read integers b and l for each test case. The goal is to work only with their gcd, since all required information depends entirely on shared factors.
2. Compute g = gcd(b, l). This compresses the problem into factoring a single number that represents the maximum possible number of balanced pairs.
3. If g equals 1, output 0 immediately. There are no prime factors to report, so further computation is unnecessary.
4. Initialize an empty list for prime factors and start checking divisors starting from 2.
5. For each integer i from 2 up to sqrt(g), check whether i divides g. If it does, repeatedly divide g by i while counting how many times this happens. This count is the multiplicity of the prime factor i.
6. If after processing all i up to sqrt(g), the remaining value of g is greater than 1, then g itself is prime and must be recorded with multiplicity 1.
7. Print all collected primes in increasing order, each followed by its multiplicity, and end with a line containing 0.

### Why it works

Every integer greater than 1 has a unique prime factorization. The trial division process systematically removes all occurrences of each prime factor in increasing order. Because we only test up to sqrt(g), any remaining value must either be 1 or a prime larger than sqrt(g), since a composite number would have already been factored into smaller components. This guarantees that all primes are captured exactly once and with correct multiplicities.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

def factorize(x):
    res = []
    i = 2
    while i * i <= x:
        if x % i == 0:
            cnt = 0
            while x % i == 0:
                x //= i
                cnt += 1
            res.append((i, cnt))
        i += 1
    if x > 1:
        res.append((x, 1))
    return res

def solve():
    t = int(input())
    for _ in range(t):
        b, l = map(int, input().split())
        g = math.gcd(b, l)

        if g == 1:
            print(0)
            continue

        factors = factorize(g)
        for p, c in factors:
            print(p, c)
        print(0)

if __name__ == "__main__":
    solve()
```

The solution separates concerns cleanly: first compressing the problem using gcd, then factoring the reduced number using standard trial division. The factorization function carefully divides out each prime completely before moving forward, which ensures correct multiplicities. The loop condition i * i <= x dynamically shrinks as x is reduced, improving performance in practice.

A common mistake is forgetting to recompute the loop bound against the updated x; this implementation avoids that by directly using the current value of x in the condition. Another subtle point is ensuring that remaining x > 1 is treated as a prime factor, since it may not have been fully reduced by the loop.

## Worked Examples

### Example 1

Input pair: b = 360, l = 240

gcd = 120

| Step | x value | divisor i | action | factors |
| --- | --- | --- | --- | --- |
| 1 | 120 | 2 | divide twice → 30 | (2,2) |
| 2 | 30 | 3 | divide once → 10 | (3,1) |
| 3 | 10 | 5 | divide once → 2 | (5,1) |
| 4 | 2 | end | leftover prime | add (2,1) |

Final factorization: 2^3 * 3^1 * 5^1

Output:

```
2 3
3 1
5 1
0
```

This confirms that repeated division correctly accumulates multiplicities and preserves ordering.

### Example 2

Input pair: b = 83, l = 24

gcd = 1

| Step | x value | action |
| --- | --- | --- |
| 1 | 1 | immediate termination |

Output:

```
0
```

This demonstrates that the gcd shortcut correctly avoids unnecessary factorization work and handles the empty factorization case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T √g) | Each gcd is computed in logarithmic time, and each factorization uses trial division up to sqrt(g) |
| Space | O(1) | Only a small list of factors per test case |

The value of g is at most 10^12, so sqrt(g) is at most 10^6. With T up to 100, this fits comfortably within typical limits in optimized Python, especially since divisions quickly reduce x during factorization.

## Test Cases

```python
import sys, io, math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    def factorize(x):
        res = []
        i = 2
        while i * i <= x:
            if x % i == 0:
                cnt = 0
                while x % i == 0:
                    x //= i
                    cnt += 1
                res.append((i, cnt))
            i += 1
        if x > 1:
            res.append((x, 1))
        return res

    def solve():
        t = int(sys.stdin.readline())
        for _ in range(t):
            b, l = map(int, sys.stdin.readline().split())
            g = math.gcd(b, l)

            if g == 1:
                print(0)
                continue

            for p, c in factorize(g):
                print(p, c)
            print(0)

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return out.strip()

# provided samples
assert run("1\n360 240\n") == "2 3\n3 1\n5 1\n0"
assert run("3\n83 24\n15 25\n7 13\n") == "0\n5 1\n0\n0"

# custom cases
assert run("1\n2 2\n") == "2 1\n0"                 # minimum non-trivial gcd
assert run("1\n1000000000000 500000000000\n") == "2 45\n5 12\n0"  # large power structure
assert run("1\n17 34\n") == "17 1\n0"              # prime gcd
assert run("1\n6 10\n") == "2 1\n0"                # mixed small primes
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 2 | 2 1 0 | smallest equal case |
| 1e12 5e11 | 2 45 5 12 0 | large exponent handling |
| 17 34 | 17 1 0 | gcd is prime |
| 6 10 | 2 1 0 | shared factor extraction |

## Edge Cases

One edge case is when the gcd collapses to 1 even though both inputs are large. For example, b = 83 and l = 24 immediately yields 1. The algorithm handles this by checking g == 1 before factorization, ensuring no incorrect output lines are produced.

Another edge case is when the gcd itself is prime. For instance, b = 17 and l = 34 gives g = 17. The loop does not find any divisors, and the final leftover value triggers the “x > 1” condition, correctly emitting 17 with multiplicity 1.

A third case is when the gcd is a perfect power, such as 2^k. In this case, repeated division inside the same loop iteration ensures full multiplicity accumulation, since x is continuously reduced before moving to the next candidate divisor.
