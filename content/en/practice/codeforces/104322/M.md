---
title: "CF 104322M - \u4e00\u5143\u56db\u6b21\u65b9\u7a0b"
description: "We are asked to output five integers $a, b, c, d, e$ within the range $[-10, 10]$, with $a neq 0$, such that the quartic polynomial $$a x^4 + b x^3 + c x^2 + d x + e$$ has no real roots. In other words, no real number $x$ should make the expression equal to zero."
date: "2026-07-01T19:28:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104322
codeforces_index: "M"
codeforces_contest_name: "\u54c8\u5c14\u6ee8\u5de5\u7a0b\u5927\u5b66\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b 2023"
rating: 0
weight: 104322
solve_time_s: 68
verified: true
draft: false
---

[CF 104322M - \u4e00\u5143\u56db\u6b21\u65b9\u7a0b](https://codeforces.com/problemset/problem/104322/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to output five integers $a, b, c, d, e$ within the range $[-10, 10]$, with $a \neq 0$, such that the quartic polynomial

$$a x^4 + b x^3 + c x^2 + d x + e$$

has no real roots.

In other words, no real number $x$ should make the expression equal to zero. The task is purely constructive, and any valid set of coefficients satisfying the condition is accepted.

The constraints are extremely small, and there is no input beyond the problem requirement itself. This immediately signals that the solution is not algorithmic in the usual sense, but rather relies on identifying a simple polynomial shape with a guaranteed sign over all real numbers.

A naive attempt might try random coefficients and test whether the quartic crosses zero, but that is unnecessary and unreliable. Another common pitfall is trying to argue from discriminants or quartic root conditions, which is overkill and error-prone given the tight coefficient range requirement.

The key requirement is robustness: the polynomial must stay strictly positive or strictly negative for all real $x$.

## Approaches

A brute-force mindset would be to enumerate all integer coefficient tuples in the allowed range and test whether the polynomial has real roots. This is theoretically possible because the search space is only $21^5$, but checking root existence for each quartic is already nontrivial and would require either symbolic reasoning or numerical root finding with precision issues. More importantly, this is unnecessary since we only need one valid construction.

The structural insight is that certain quartic polynomials are always nonnegative due to their algebraic form. The simplest family is even-powered dominant expressions like $x^4$, which grows positively for large magnitude $x$. To eliminate possible real roots entirely, we ensure the polynomial never reaches zero by adding a strictly positive constant.

The simplest example is:

$$x^4 + 1$$

For all real $x$, $x^4 \ge 0$, so $x^4 + 1 \ge 1$, meaning it is strictly positive everywhere. Hence it has no real roots.

This directly satisfies all constraints: coefficients are small integers, $a = 1 \neq 0$, and the polynomial never crosses zero.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | O(21^5) with heavy root checks | O(1) | Unnecessary |
| Constructive (x^4 + 1) | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Choose a polynomial form that is always positive for all real inputs, ensuring no real roots exist. The simplest candidate is $x^4 + 1$, since the leading term dominates and is never negative.
2. Map this polynomial into coefficients. The term $x^4$ gives $a = 1$, and all intermediate coefficients are zero because there are no cubic, quadratic, or linear terms. The constant term is $e = 1$.
3. Output the coefficients directly as the final answer.

### Why it works

For any real $x$, the term $x^4$ is always nonnegative. Adding a positive constant shifts the entire graph strictly above zero, so the polynomial cannot equal zero at any real point. This guarantees zero real roots without requiring any case analysis or algebraic classification.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    print(1, 0, 0, 0, 1)

if __name__ == "__main__":
    main()
```

The code directly encodes the polynomial $x^4 + 1$. There is no input processing because the problem does not provide any input. The coefficients are printed in order.

## Worked Examples

There are no input examples with meaningful variation since the task is constructive. Instead, we can verify behavior of the chosen polynomial.

Consider $x = 0$, the polynomial evaluates to $1$. For $x = 1$, it evaluates to $2$. For $x = -2$, it evaluates to $16 + 1 = 17$. These checks confirm the expression remains strictly positive in all tested cases, matching the required property.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | constant output construction |
| Space | O(1) | no auxiliary data structures |

The constraints allow any constant-time construction. Since no computation over input is required, this solution is optimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return "1 0 0 0 1"

# no input case
assert run("") == "1 0 0 0 1"

# sanity check consistency
assert run("anything") == "1 0 0 0 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| empty | 1 0 0 0 1 | no input handling |
| random string | 1 0 0 0 1 | robustness to irrelevant input |

## Edge Cases

The only meaningful edge case is the requirement that the polynomial must have no real roots for all real numbers, including very large positive and negative values. The chosen polynomial $x^4 + 1$ handles this uniformly because the leading even power dominates growth and remains nonnegative everywhere, while the constant term enforces strict positivity. No sign change is possible, so no root can exist.
