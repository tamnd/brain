---
title: "CF 104091B - \u0412\u0441\u0442\u0443\u043f\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u0435 \u0438\u0441\u043f\u044b\u0442\u0430\u043d\u0438\u0435 \u0432 \u041a\u043e\u043b\u043b\u0435\u0433\u0438\u044e \u0412\u0438\u043d\u0442\u0435\u0440\u0445\u043e\u043b\u0434\u0430"
description: "We are given a positional numeral system with base $b$. Every integer has a representation in that base, and we are interested in the number of trailing zeros in that representation."
date: "2026-07-02T02:28:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104091
codeforces_index: "B"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0432 \u041f\u0435\u0442\u0440\u043e\u0437\u0430\u0432\u043e\u0434\u0441\u043a\u0435 \u0438 \u041a\u0430\u0440\u0435\u043b\u0438\u0438 2022-2023"
rating: 0
weight: 104091
solve_time_s: 48
verified: true
draft: false
---

[CF 104091B - \u0412\u0441\u0442\u0443\u043f\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u0435 \u0438\u0441\u043f\u044b\u0442\u0430\u043d\u0438\u0435 \u0432 \u041a\u043e\u043b\u043b\u0435\u0433\u0438\u044e \u0412\u0438\u043d\u0442\u0435\u0440\u0445\u043e\u043b\u0434\u0430](https://codeforces.com/problemset/problem/104091/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a positional numeral system with base $b$. Every integer has a representation in that base, and we are interested in the number of trailing zeros in that representation.

A number is considered valid if, when written in base $b$, its last digits contain at least $d$ zeros. In other words, the number must be divisible by $b^d$. The task is to count how many integers in the range $[l, r]$ satisfy this divisibility condition.

The constraints immediately push us away from any direct enumeration. The range can go up to $10^{18}$, so iterating over all numbers is impossible. The base $b$ is at most 100, so $b^d$ is still manageable because $d \le 9$, but the range of numbers is too large for naive checking.

A common failure case appears when thinking in decimal intuition only. For example, in base 10, counting numbers ending in at least 2 zeros means counting multiples of 100. But in base 2 or base 7, the spacing between valid numbers changes drastically. A naive loop checking divisibility for each number in $[l, r]$ will time out for ranges like $10^{18}$.

Another subtle pitfall is handling $d = 0$. In that case, every number is valid, since having at least zero trailing zeros is always true. Any implementation that forgets this special case will incorrectly try to compute divisibility by $b^0 = 1$, which is fine mathematically, but may introduce unnecessary complexity or edge-case bugs in logic if handled inconsistently.

## Approaches

The brute-force idea is straightforward: iterate over every integer $x$ from $l$ to $r$, convert it to base $b$, count trailing zeros, and check whether the count is at least $d$. This is correct because it directly follows the definition. However, converting a number to base $b$ costs $O(\log_b x)$, and we do this for up to $10^{18}$ numbers. Even with fast arithmetic, this is far beyond feasible.

The key observation is that trailing zeros in base $b$ are equivalent to divisibility by $b^d$. If a number ends with at least $d$ zeros in base $b$, then it must be of the form $k \cdot b^d$. So the problem reduces to counting how many multiples of $b^d$ lie in $[l, r]$.

This turns the problem into a classic prefix counting task. We compute how many multiples of $b^d$ are less than or equal to $r$, subtract how many are less than $l$, and obtain the answer in constant time.

The only subtlety is ensuring correctness for edge cases like $l = 1$ and large values of $b^d$, which may exceed $10^{18}$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O((r-l+1)\log_b r)$ | $O(1)$ | Too slow |
| Optimal | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We reduce the problem to counting multiples of a fixed value $p = b^d$ inside a range.

1. Compute $p = b^d$. This represents the smallest number whose base-$b$ representation has at least $d$ trailing zeros.
2. If $d = 0$, immediately return $r - l + 1$, since every number satisfies the condition.
3. Compute how many multiples of $p$ are less than or equal to $r$, which is $\left\lfloor \frac{r}{p} \right\rfloor$.
4. Compute how many multiples of $p$ are strictly less than $l$, which is $\left\lfloor \frac{l-1}{p} \right\rfloor$.
5. Subtract these two values to obtain the count of valid numbers in $[l, r]$.

The reasoning behind step 4 is important: we are counting prefixes up to $r$ and removing everything before $l$, so we must exclude numbers strictly smaller than $l$, not those less than or equal to $l$.

### Why it works

Every integer divisible by $b^d$ has at least $d$ trailing zeros in base $b$, because multiplying by $b$ shifts digits left in base $b$ and appends a zero. Conversely, any number with at least $d$ trailing zeros must be divisible by $b^d$. This establishes a one-to-one correspondence between valid numbers and multiples of $b^d$, so counting valid numbers reduces exactly to counting multiples in an interval.

## Python Solution

```python
import sys
input = sys.stdin.readline

b = int(input().strip())
d = int(input().strip())
l = int(input().strip())
r = int(input().strip())

if d == 0:
    print(r - l + 1)
else:
    p = pow(b, d)
    def count(x):
        if x <= 0:
            return 0
        return x // p

    ans = count(r) - count(l - 1)
    print(ans)
```

The solution is built around reducing the problem to arithmetic on multiples. The crucial step is computing $b^d$ efficiently using built-in exponentiation, which safely handles large values within Python’s big integer range.

The subtraction `count(r) - count(l - 1)` ensures correct inclusion of the left boundary, since any multiple of $p$ equal to $l$ must be counted.

## Worked Examples

Consider a base-10 case where we count numbers with at least 1 trailing zero in the range $[1, 20]$.

Let $b = 10$, $d = 1$, so $p = 10$.

| Step | Value |
| --- | --- |
| p | 10 |
| count(r) = 20 // 10 | 2 |
| count(l-1) = 0 // 10 | 0 |
| answer | 2 |

The valid numbers are 10 and 20, which matches the computation.

Now consider a binary example: $b = 2$, $d = 3$, $l = 1$, $r = 20$. Here $p = 8$.

| Step | Value |
| --- | --- |
| p | 8 |
| count(20) | 2 |
| count(0) | 0 |
| answer | 2 |

The valid numbers are 8 and 16, both divisible by 8, matching the requirement of at least three trailing zeros in binary.

These traces confirm that the algorithm behaves consistently across different bases and not just in decimal intuition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a few arithmetic operations and one exponentiation |
| Space | $O(1)$ | No auxiliary data structures |

The constraints allow $l, r \le 10^{18}$, so any per-number processing would be impossible. Reducing the problem to constant-time arithmetic ensures it runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    b = int(input().strip())
    d = int(input().strip())
    l = int(input().strip())
    r = int(input().strip())

    if d == 0:
        return str(r - l + 1)
    p = pow(b, d)

    def count(x):
        if x <= 0:
            return 0
        return x // p

    return str(count(r) - count(l - 1))

# provided sample-like checks
assert run("10\n1\n1\n20") == "2"

# custom cases
assert run("2\n3\n1\n20") == "2"      # 8, 16
assert run("10\n0\n5\n5") == "1"      # all numbers valid
assert run("5\n2\n1\n24") == str(24 // 25)  # no multiples of 25
assert run("3\n2\n9\n27") == "3"      # 9,18,27
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 3 1 20 | 2 | binary multiple counting |
| 10 0 5 5 | 1 | d = 0 edge case |
| 5 2 1 24 | 0 | no valid multiples |
| 3 2 9 27 | 3 | exact boundary inclusion |

## Edge Cases

When $d = 0$, the definition becomes vacuous: every number has at least zero trailing zeros. The algorithm handles this by immediately returning the full interval size, avoiding unnecessary exponentiation.

When $b^d > r$, there are no valid numbers except possibly zero, which is outside the range since $l \ge 1$. The division-based formula naturally returns zero because both $\lfloor r / p \rfloor$ and $\lfloor (l-1)/p \rfloor$ are zero.

When $l$ itself is a multiple of $b^d$, the subtraction with $l - 1$ ensures inclusion. For example, with $l = 8$, $b^d = 8$, the term $count(l - 1) = count(7) = 0$, so 8 is correctly counted.

These cases confirm that the arithmetic formulation matches the original trailing-zero definition across all boundary conditions.
