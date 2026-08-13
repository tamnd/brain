---
title: "CF 102282A - \u041f\u0435\u0440\u0432\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430"
description: "We need to choose a positive integer (x) such that (x^n) is divisible by (m), and among all such positive integers we need the smallest one. If no such (x) exists, we print ABSENT."
date: "2026-08-13T16:12:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102282
codeforces_index: "A"
codeforces_contest_name: "2011, \u041e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u043a\u043e\u043d\u0442\u0435\u0441\u0442 \u0421\u0413\u0410\u0423 \u043d\u0430 \u0447\u0435\u0442\u0432\u0435\u0440\u0442\u044c\u0444\u0438\u043d\u0430\u043b ACM ICPC"
rating: 0
weight: 102282
solve_time_s: 65
verified: true
draft: false
---

[CF 102282A - \u041f\u0435\u0440\u0432\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430](https://codeforces.com/problemset/problem/102282/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to choose a positive integer (x) such that (x^n) is divisible by (m), and among all such positive integers we need the smallest one. If no such (x) exists, we print `ABSENT`.

The value (n) can be as large as (10^9), so an algorithm that depends linearly on (n) is already unnecessary. More importantly, (m) is not arbitrary. It can only be one of the listed values, namely (1,2,3,5,7,11,13,17), or (1000000007). Every value except (1) is prime. This restriction is the central observation of the problem.

The answer can never require us to search through a large range of integers. If (m>1) and (n>0), choosing (x=m) immediately works because (m^n) is divisible by (m). Since (m) itself is the smallest positive integer divisible by (m), no smaller (x) can work when (n=1), and for the larger exponents we still need (x) to contain the prime factor (m), so (x\ge m).

The boundary cases deserve separate attention. For input `0 2`, we have (x^0=1) for every positive (x), and (1) is not divisible by (2), so the answer is `ABSENT`. A careless solution that always prints (m) for (n=0) would output `2`, which is wrong.

For input `0 1`, the answer is `1`, because every positive integer raised to the zeroth power equals (1), and (1) is divisible by (1). A solution that treats (n=0) as automatically impossible would fail here.

For input `1 1`, the answer is also `1`. Since (1) divides every integer, the smallest possible positive (x) is enough.

There is also a formatting problem in the supplied statement excerpt: the displayed example section contains `2 2` and `3 3` without a reliable separation between input and output. Under the mathematical condition stated in the problem, `2 2` has answer `2`, while `3 3` has answer `3`. The solution below follows the formal statement, not the corrupted example formatting.

## Approaches

A direct brute-force solution would try (x=1,2,3,\ldots), compute whether (x^n) is divisible by (m), and stop at the first successful value. This is correct because the candidates are examined in increasing order, so the first valid candidate is necessarily minimal.

The problem is the worst case. Consider (n=1) and (m=1000000007). The first valid (x) is (1000000007), so a brute-force search would inspect exactly (1000000007) candidates. Even if every divisibility check were reduced to a constant-time operation, that is far beyond what a one-second contest solution should do. Computing the powers directly would be even worse because (x^n) can become enormous.

The observation that makes the search disappear is that every allowed (m>1) is prime. Suppose (m=p), where (p) is prime, and (n>0). If (p\mid x^n), then (p\mid x). This follows from the basic property of primes: if a prime divides a product, it must divide one of its factors. Since (x^n=x\cdot x\cdots x), divisibility of the power by (p) forces (p) to divide (x).

The smallest positive (x) divisible by (p) is exactly (p). Thus the answer is simply (m).

The only exception is (m=1), where the smallest positive integer is always (1). The other exceptional case is (n=0), because every positive (x) satisfies (x^0=1). Consequently, for (m>1) there is no solution when (n=0).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(m)) candidates, with power/divisibility work per candidate | (O(1)) | Too slow for (m=1000000007) |
| Optimal | (O(1)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read (n) and (m). We only need these two values because the restricted set of possible (m) values gives us the required number-theoretic property directly.
2. If (m=1), print `1`. Every positive integer raised to any nonnegative power is at least defined here as (1) when (n=0), and (1) is divisible by (1). The smallest positive integer is therefore the answer.
3. If (m>1) and (n=0), print `ABSENT`. For every positive integer (x), (x^0=1), and no (m>1) divides (1).
4. Otherwise (m>1) and (n>0). Since every allowed value of (m) is prime, any (x) satisfying (m\mid x^n) must itself be divisible by (m). The smallest such positive (x) is (m), so print (m).

### Why it works

For (m=1), the answer is obviously (1). For (m>1) and (n=0), every candidate has zeroth power equal to (1), so no candidate works. For (m>1) and (n>0), the allowed values of (m) are prime. If (m\mid x^n), primality forces (m\mid x), so every valid (x) is at least (m). At the same time, (x=m) is valid because (m^n) is divisible by (m). Thus (m) is exactly the minimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    if m == 1:
        print(1)
    elif n == 0:
        print("ABSENT")
    else:
        print(m)

solve()
```

The first branch handles (m=1) before looking at (n). This order matters for input `0 1`, because the answer is `1`, not `ABSENT`.

The second branch handles the only impossible situation. Once (m>1), (x^0) is always (1), so there is no valid positive integer.

The final branch covers every remaining case. Here (n>0) and (m) is one of the allowed primes, so the number itself is the minimum valid base.

There is no exponentiation in the implementation. This avoids both unnecessary work and the possibility of constructing extremely large integers. Python also has arbitrary-precision integers, but relying on that would not solve the algorithmic problem of potentially performing huge computations.

## Worked Examples

### Sample 1

For the mathematically stated sample `2 2`, we have (n=2) and (m=2).

| Step | (n) | (m) | Condition | Answer |
| --- | --- | --- | --- | --- |
| Read input | 2 | 2 | (m\ne1) |  |
| Check (n=0) | 2 | 2 | false |  |
| Final branch | 2 | 2 | (m) is prime and (n>0) | 2 |

The smallest valid base is (2), since (2^2=4) is divisible by (2). The result is `2`.

### Sample 2

For `3 3`, we have (n=3) and (m=3).

| Step | (n) | (m) | Condition | Answer |
| --- | --- | --- | --- | --- |
| Read input | 3 | 3 | (m\ne1) |  |
| Check (n=0) | 3 | 3 | false |  |
| Final branch | 3 | 3 | (m) is prime and (n>0) | 3 |

Here (3^3=27), which is divisible by (3). Any smaller positive integer is either (1) or (2), and neither has a third power divisible by (3). The result is `3`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(1)) | Only a constant number of comparisons and one output operation are performed. |
| Space | (O(1)) | Only the two input integers and a few temporary values are stored. |

The bound (n\le10^9) has no effect on the running time because the algorithm never iterates over (n) and never computes (x^n). Likewise, even the largest possible (m), (1000000007), causes no search. The solution comfortably fits the stated time and memory limits.

## Test Cases

```python
import sys
import io

def solve():
    n, m = map(int, input().split())

    if m == 1:
        print(1)
    elif n == 0:
        print("ABSENT")
    else:
        print(m)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided examples as they appear mathematically in the supplied statement.
assert run("2 2\n") == "2", "sample 1"
assert run("3 3\n") == "3", "sample 2"

# Minimum-size input: n = 0, m = 1.
assert run("0 1\n") == "1", "m = 1 must always return 1"

# Boundary case n = 0 with a prime m.
assert run("0 2\n") == "ABSENT", "x^0 is always 1"

# All-equal values.
assert run("7 7\n") == "7", "prime m with positive exponent"

# Maximum allowed n and maximum allowed m.
assert run("1000000000 1000000007\n") == "1000000007", "maximum n and m"

# Boundary between n = 0 and n = 1.
assert run("1 17\n") == "17", "positive exponent must return m"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 1` | `1` | The special divisor (m=1) must be handled before the (n=0) case. |
| `0 2` | `ABSENT` | Zeroth powers cannot be divisible by a prime greater than (1). |
| `7 7` | `7` | Equal (n) and (m), with a positive exponent. |
| `1000000000 1000000007` | `1000000007` | Maximum values and the fact that the algorithm does not depend on (n). |
| `1 17` | `17` | The smallest positive exponent and a prime divisor. |

## Edge Cases

For `0 2`, the algorithm first checks whether (m=1), which is false. It then sees (n=0) and prints `ABSENT`. This is correct because every positive (x) satisfies (x^0=1), and (2\nmid1).

For `0 1`, the first condition succeeds immediately and prints `1`. The order of these checks prevents the valid (m=1) case from being incorrectly classified as impossible merely because (n=0).

For `1 1`, the first condition again prints `1`. Since (1) divides every integer, the smallest positive base is always sufficient.

For `1 17`, the algorithm reaches the final branch and prints `17`. Here (17^1=17), and no positive integer smaller than (17) is divisible by (17).

For `1000000000 1000000007`, the algorithm still performs only two comparisons before printing the answer. The enormous exponent never causes a loop, and the enormous prime never causes a search. The output is `1000000007`.

The central invariant across all branches is simple: once (m>1) and (n>0), every valid base must be a multiple of the prime (m). The smallest possible multiple is (m) itself, so there is nothing left to search for.
