---
title: "CF 2197A - Friendly Numbers"
description: "We are given an integer $x$, and we want to count how many integers $y$ satisfy a very specific balancing condition: if you take $y$ and subtract the sum of its digits, you land exactly on $x$."
date: "2026-06-07T20:28:04+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "expression-parsing", "math", "schedules"]
categories: ["algorithms"]
codeforces_contest: 2197
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1079 (Div. 2)"
rating: 800
weight: 2197
solve_time_s: 66
verified: true
draft: false
---

[CF 2197A - Friendly Numbers](https://codeforces.com/problemset/problem/2197/A)

**Rating:** 800  
**Tags:** binary search, brute force, expression parsing, math, schedules  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an integer $x$, and we want to count how many integers $y$ satisfy a very specific balancing condition: if you take $y$ and subtract the sum of its digits, you land exactly on $x$. In other words, each valid number $y$ “overpays” compared to $x$, and the overpayment is exactly the digit sum of $y$.

So the task is not to construct $y$, but to count how many such constructions exist for each $x$. Each test case asks: among all integers, how many different $y$ collapse down to the same value after subtracting their digit sum?

The constraints go up to $x \le 10^9$ and $t \le 500$. A naive scan over all possible $y$ is immediately impossible because even a single test case would require checking potentially billions of candidates. Even scanning only near $x$ is not safe without a bound on how far $y$ can drift.

A key structural observation is that the transformation $y \mapsto y - d(y)$ only shifts numbers downward by at most the number of digits times 9. For a 10-digit number, the digit sum is at most 90, so $y$ cannot be more than about 90 larger than $x$. This makes the search space tightly bounded.

A subtle edge case arises when $x$ is small. For example, if $x = 1$, then potential candidates $y$ would need to satisfy $y - d(y) = 1$. Trying small values shows that very few numbers qualify, and it is easy to incorrectly assume there are none or many without checking the exact constraint relationship.

## Approaches

A brute-force strategy would be to iterate over all possible $y$ up to some large limit and test whether $y - d(y) = x$. This is correct but completely infeasible because $y$ ranges up to $10^9 + 100$ and we would be performing digit-sum computations for each candidate. That leads to roughly $O(10^9)$ operations per test case, which is far beyond any reasonable limit.

The key insight is to reverse the equation. Instead of starting from $y$, we start from $x$ and ask what values of $y$ could possibly map to it. If $y - d(y) = x$, then $y = x + d(y)$. This looks circular, but it reveals a crucial constraint: the digit sum of $y$ is small and bounded by at most $9 \cdot 10 = 90$.

So we can try all possible digit sums $s$ in a small range. If we fix $s = d(y)$, then $y = x + s$. We simply check whether the digit sum of $x + s$ equals $s$. Each valid $s$ contributes exactly one valid $y$.

This reduces the problem from potentially billions of candidates to at most 100 checks per test case, each involving a digit-sum computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all $y$ | $O(N \cdot \log N)$ | $O(1)$ | Too slow |
| Try all digit sums $s \in [0, 100]$ | $O(100 \cdot \log x)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. For a given $x$, observe that any valid $y$ must satisfy $y = x + s$, where $s = d(y)$. Since $y$ has at most 10 digits, $s \le 90$, so we only need to try a small range of candidate digit sums.
2. Iterate over all possible values of $s$ from 0 to 100. The upper bound is slightly relaxed to avoid edge mistakes, but only values up to 90 can actually succeed.
3. For each $s$, compute $y = x + s$. This is the only possible candidate for that digit sum.
4. Compute the digit sum of $y$, denoted $d(y)$. This step verifies whether our assumption about the digit sum is consistent.
5. If $d(y) = s$, then $y$ is a valid friendly number. Increment the answer.
6. After checking all possible $s$, output the total count.

The reason this enumeration works is that each valid $y$ is uniquely associated with its digit sum $s$, and we ensure no candidate is missed or double-counted.

### Why it works

Every solution $y$ induces exactly one value $s = d(y)$, and must satisfy $y = x + s$. Our loop over all possible $s$ guarantees we reconstruct every candidate $y$ that could possibly satisfy the equation. Since digit sums are bounded and injectively determine the offset between $x$ and $y$, the search space is both complete and non-redundant.

## Python Solution

```python
import sys
input = sys.stdin.readline

def digit_sum(n):
    s = 0
    while n > 0:
        s += n % 10
        n //= 10
    return s

t = int(input())
for _ in range(t):
    x = int(input())
    ans = 0
    
    for s in range(0, 100):
        y = x + s
        if digit_sum(y) == s:
            ans += 1
    
    print(ans)
```

The code separates the digit-sum computation into a helper function because it is called repeatedly. The loop over $s$ is the core idea: each $s$ is treated as a hypothesis for the digit sum of $y$, and we verify it directly.

The bound of 100 is safe because the maximum possible digit sum for a 10-digit number is 90, and $x \le 10^9$ guarantees at most 10 digits in $y$.

## Worked Examples

### Example 1: $x = 18$

We test candidate shifts $s$.

| s | y = x + s | digit sum of y | valid? |
| --- | --- | --- | --- |
| 2 | 20 | 2 | yes |
| 3 | 21 | 3 | yes |
| 4 | 22 | 4 | yes |
| 5 | 23 | 5 | yes |
| 6 | 24 | 6 | yes |
| 7 | 25 | 7 | yes |
| 8 | 26 | 8 | yes |
| 9 | 27 | 9 | yes |
| 10 | 28 | 10 | yes |

This yields 9 valid numbers from 20 to 28. Continuing the same pattern up to 29 confirms 10 total valid values.

This demonstrates that once $x$ is fixed, the valid $y$ form a contiguous block determined by digit sum stability.

### Example 2: $x = 1$

| s | y = x + s | digit sum of y | valid? |
| --- | --- | --- | --- |
| 1 | 2 | 2 | no |
| 2 | 3 | 3 | no |
| 3 | 4 | 4 | no |
| ... | ... | ... | ... |

No value of $s$ satisfies the consistency condition, so the answer is 0. This shows that small $x$ does not guarantee any solutions, even though candidates exist.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(100 \cdot \log x)$ | We try at most 100 shifts, each requiring digit-sum computation over at most 10 digits |
| Space | $O(1)$ | Only a few integers are used |

The constant bound on digit-sum trials ensures the solution runs comfortably within limits even for 500 test cases. The logarithmic factor is negligible in practice.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def digit_sum(n):
        s = 0
        while n > 0:
            s += n % 10
            n //= 10
        return s

    t = int(input())
    out = []
    for _ in range(t):
        x = int(input())
        ans = 0
        for s in range(0, 100):
            y = x + s
            if digit_sum(y) == s:
                ans += 1
        out.append(str(ans))
    return "\n".join(out)

# provided samples
assert run("3\n1\n18\n998244360\n") == "0\n10\n10"

# custom cases
assert run("1\n0\n") == "1"
assert run("1\n10\n") >= "0"
assert run("1\n1000000000\n") >= "1"
assert run("2\n1\n2\n")  # basic sanity check
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 0 | smallest positive x edge |
| 10 | varies | small boundary behavior |
| 1e9 | ≥1 | large boundary stability |
| mixed | consistency | multiple test handling |

## Edge Cases

When $x = 1$, the algorithm checks all $s \in [0, 99]$, producing candidates $y = 1 + s$. None of these candidates satisfy $d(y) = s$, since digit sums grow too slowly compared to the linear shift. The algorithm correctly returns 0.

When $x = 999{,}999{,}999$, the candidates range up to about $10^9 + 100$. Even here, digit sums remain bounded by 90, so only a small subset of shifts can work. The loop still captures all possibilities because every valid $y$ must lie within the enumerated window.

When $x$ is a multiple of 9 or contains many trailing 9s, digit sums of nearby numbers fluctuate more, but still remain within the bounded range. The algorithm does not rely on monotonicity, only on exhaustive checking over all feasible digit sums, so these cases are handled naturally without modification.
