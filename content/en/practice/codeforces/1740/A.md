---
title: "CF 1740A - Factorise N+M"
description: "We are given several test cases, and each test case starts with a prime number $n$. For every such $n$, we must choose another prime number $m$ such that the sum $n + m$ is not prime."
date: "2026-06-15T03:39:58+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1740
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 831 (Div. 1 + Div. 2)"
rating: 800
weight: 1740
solve_time_s: 482
verified: false
draft: false
---

[CF 1740A - Factorise N+M](https://codeforces.com/problemset/problem/1740/A)

**Rating:** 800  
**Tags:** constructive algorithms, number theory  
**Solve time:** 8m 2s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several test cases, and each test case starts with a prime number $n$. For every such $n$, we must choose another prime number $m$ such that the sum $n + m$ is not prime. Any valid prime $m$ in the allowed range is acceptable, and different test cases are independent.

The core task is not to compute primality repeatedly in a heavy way, but to construct a valid partner prime for each input prime. The output constraint is generous: $m$ can be any prime up to $10^5$, and there is no requirement to minimize or optimize it beyond validity.

The constraint $n \le 10^5$ and $t \le 10^4$ suggests that solutions must be essentially constant time per test case after some preprocessing. Anything involving repeated primality checks per test case would still be fine only if the checks are $O(1)$, but repeated search over primes per query would be too slow in the worst case.

A subtle edge case arises when $n$ is small. If $n = 2$, then choosing small primes like $m = 2$ or $m = 3$ immediately produces sums $4$ or $5$, and only one of them is non-prime. A naive approach that always picks the first prime in a list might fail if it assumes all sums behave similarly. Another corner case is when $n$ is large and near $10^5$, where careless construction strategies might exceed bounds for $n + m$, although primality of the sum is the only concern, not its magnitude.

## Approaches

A brute-force approach would try every prime $m$ and check whether $n + m$ is prime. For each test case, this could scan all primes up to $10^5$, and for each candidate compute primality of $n + m$. Even if primality is precomputed with a sieve, we would still check up to about 9,500 primes per test case, leading to roughly $10^8$ checks in the worst case over all tests, which is unnecessary.

The key observation is that we do not need to search. We only need to guarantee that at least one simple choice works. The structure of primes immediately gives a shortcut: if we pick a small fixed prime $m$, we only need to check whether $n + m$ is composite. Since $n$ is always prime, we can exploit parity. Except for $n = 2$, every prime is odd. The sum of two odd numbers is even and greater than 2, hence composite. This means that for all odd primes $n$, choosing $m = 3$ always produces a composite sum.

The only problematic case is $n = 2$. Here $n$ is even, so $2 + 3 = 5$ is prime, which fails. We need another fixed small prime. Choosing $m = 2$ gives $2 + 2 = 4$, which is composite. This resolves the only exceptional case.

So the solution reduces to a constant-time conditional selection.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force search over primes | $O(t \cdot \pi(N))$ | $O(N)$ | Too slow |
| Fixed construction (2 or 3) | $O(t)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. For each test case, read the prime number $n$. We treat it purely as an integer; no factorization is needed.
2. Check whether $n = 2$. This is the only even prime and behaves differently from all others because it breaks the odd-plus-odd structure.
3. If $n = 2$, output $m = 2$. This ensures $n + m = 4$, which is not prime.
4. Otherwise, output $m = 3$. Since all primes except 2 are odd, this guarantees $n + 3$ is even and greater than 2, hence composite.

### Why it works

The correctness hinges on a structural property of primes. Every prime greater than 2 is odd. When we add two odd numbers, the result is even. Any even number greater than 2 cannot be prime because it has 2 as a divisor. Thus, for any odd prime $n$, choosing $m = 3$ forces $n + m$ to be composite. The only exception is $n = 2$, where parity breaks, and we explicitly select another prime that avoids producing another prime sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        if n == 2:
            print(2)
        else:
            print(3)

if __name__ == "__main__":
    solve()
```

The code follows the construction directly. The only decision point is the equality check against 2. Everything else is constant output.

A common mistake is attempting to “search” for a valid $m$ dynamically, which is unnecessary and risks timeouts. Another mistake is forgetting that $2 + 3 = 5$ is prime, which makes $m = 3$ invalid for $n = 2$. The explicit branch handles this.

## Worked Examples

### Example 1

Input:

```
3
7
2
75619
```

We process each test case independently.

| n | check n=2 | chosen m | n + m | is n+m prime |
| --- | --- | --- | --- | --- |
| 7 | no | 3 | 10 | no |
| 2 | yes | 2 | 4 | no |
| 75619 | no | 3 | 75622 | no |

The table shows that only a single conditional rule is needed to handle all cases. For odd primes, the sum becomes even and automatically non-prime.

### Example 2

Consider a small additional set:

```
4
2
3
5
11
```

| n | check n=2 | chosen m | n + m | is n+m prime |
| --- | --- | --- | --- | --- |
| 2 | yes | 2 | 4 | no |
| 3 | no | 3 | 6 | no |
| 5 | no | 3 | 8 | no |
| 11 | no | 3 | 14 | no |

This demonstrates uniform behavior across all odd primes. Every output for $n \neq 2$ collapses to the same construction, confirming that no search or precomputation is needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t)$ | One constant-time check and print per test case |
| Space | $O(1)$ | No auxiliary structures beyond variables |

The solution easily fits within constraints since even $10^4$ test cases require only $10^4$ simple integer comparisons and outputs.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        if n == 2:
            out.append("2")
        else:
            out.append("3")
    return "\n".join(out) + "\n"

# provided samples
assert run("3\n7\n2\n75619\n") == "3\n2\n3\n"

# minimum input
assert run("1\n2\n") == "2\n"

# small odd primes
assert run("3\n3\n5\n7\n") == "3\n3\n3\n"

# mixed case
assert run("4\n2\n11\n2\n13\n") == "2\n3\n2\n3\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single 2 | 2 | smallest edge case |
| small odd primes | 3s | parity rule correctness |
| alternating 2 and odd primes | 2/3 pattern | consistency across multiple cases |

## Edge Cases

The only meaningful edge case is $n = 2$. If the algorithm blindly outputs $m = 3$, it produces $5$, which is prime and therefore invalid. The explicit branch ensures correct handling.

For example, with input:

```
1
2
```

the algorithm selects $m = 2$, producing $4$, which is composite. The logic avoids any reliance on parity assumptions that fail when $n$ is even.

All other primes are odd, and the construction $m = 3$ consistently forces an even sum greater than 2, guaranteeing correctness without further checks.
