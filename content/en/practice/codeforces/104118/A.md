---
title: "CF 104118A - An Easy Calculus Problem"
description: "We are given a function $f(x)$ defined on real numbers, but split into three regions of $x$. Each region uses a different formula: a linear expression on the far left, another linear expression in the middle, and a cubic polynomial on the right."
date: "2026-07-02T01:50:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104118
codeforces_index: "A"
codeforces_contest_name: "2022 ICPC Asia-Manila Regional Contest"
rating: 0
weight: 104118
solve_time_s: 43
verified: true
draft: false
---

[CF 104118A - An Easy Calculus Problem](https://codeforces.com/problemset/problem/104118/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a function $f(x)$ defined on real numbers, but split into three regions of $x$. Each region uses a different formula: a linear expression on the far left, another linear expression in the middle, and a cubic polynomial on the right.

The task is not to derive the constants, since the problem already provides the unique values that make the function smooth everywhere. Instead, we directly evaluate the function using those fixed coefficients for a single integer input $x$. The input is guaranteed to be small, between $-10$ and $10$, so we only need constant-time evaluation.

The key structural detail is that the function is piecewise. That means the only nontrivial part of the computation is deciding which formula applies for the given $x$. Once the correct segment is chosen, the evaluation is straightforward arithmetic.

A naive mistake here is to misinterpret interval boundaries. The left piece includes $x \le -3$, the middle piece includes $-3 < x \le 2$, and the right piece includes $x > 2$. The boundary points $-3$ and $2$ are therefore especially important. For example, at $x = -3$, using the wrong branch would change the answer completely even though both formulas are valid expressions.

Because the input range is tiny, there is no performance concern. Any correct implementation that evaluates one branch in constant time is sufficient.

## Approaches

A brute-force interpretation would attempt to encode the function exactly as written, possibly even trying to compute or verify differentiability conditions. That is unnecessary here because the coefficients are already fixed. The only remaining work is evaluating a piecewise expression once.

The key observation is that the function is fully determined by interval membership. We do not need calculus reasoning or symbolic manipulation. We only need to check where $x$ lies and apply the corresponding formula.

The brute-force effort would still run in constant time per query, but it might introduce unnecessary complexity such as recomputing formulas or handling symbolic expressions. The optimal approach simplifies everything into three direct computations and a couple of comparisons.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Evaluation of General Piecewise Form | O(1) | O(1) | Accepted |
| Direct Branch Evaluation | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We first rewrite the function using the provided constants so that evaluation becomes mechanical.

For $x \le -3$, the function is

$f(x) = -(x + 4) + 8 = -x + 4$.

For $-3 < x \le 2$, the function is

$f(x) = -2x + 1$.

For $x > 2$, the function is

$f(x) = x^3 - 14x + 17$.

Now the computation becomes a simple decision process.

1. Read the integer $x$. This is the only input value and determines the branch completely.
2. Check whether $x \le -3$. If this condition holds, compute $-x + 4$. This branch corresponds to the leftmost linear segment, so no other terms are relevant.
3. Otherwise, check whether $x \le 2$. If this is true, compute $-2x + 1$. This is the middle segment and includes both $x = -2$ and $x = 2$, so the inequality must be inclusive on the right endpoint.
4. If neither of the above holds, then $x > 2$. Compute $x^3 - 14x + 17$. This is the only remaining region, so no additional checks are needed.

The correctness comes from the fact that these three intervals form a complete, non-overlapping partition of the real line. Every possible integer input belongs to exactly one branch, so exactly one formula is applied.

## Python Solution

```python
import sys
input = sys.stdin.readline

x = int(input().strip())

if x <= -3:
    print(-x + 4)
elif x <= 2:
    print(-2 * x + 1)
else:
    print(x**3 - 14 * x + 17)
```

The implementation mirrors the interval logic directly. The first condition handles all values up to and including $-3$, so it must be checked first. The second condition automatically implies the range $-3 < x \le 2$ because the previous branch excluded smaller values. Everything else falls into the cubic case.

The only subtlety is ensuring the order of conditions is preserved. Reordering them incorrectly could cause boundary values like $-3$ or $2$ to be assigned to the wrong expression.

## Worked Examples

Consider $x = -3$. This lies in the first interval because $x \le -3$, so we compute $-(-3) + 4 = 7$.

| Step | Condition Check | Expression Used | Result |
| --- | --- | --- | --- |
| 1 | $x \le -3$ is true | $-x + 4$ | 7 |

This shows how boundary values are absorbed into the left segment.

Now consider $x = 3$. This lies in the third interval since it is greater than 2, so we use the cubic form.

| Step | Condition Check | Expression Used | Result |
| --- | --- | --- | --- |
| 1 | $x \le -3$ false | skip |  |
| 2 | $x \le 2$ false | skip |  |
| 3 | default case | $x^3 - 14x + 17$ | $27 - 42 + 17 = 2$ |

This confirms that once the value exceeds 2, only the cubic expression matters and linear parts are irrelevant.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of comparisons and arithmetic operations are performed. |
| Space | O(1) | No additional data structures are used beyond a single variable. |

The constraints restrict $x$ to a tiny range, but even without that restriction, the solution would remain constant time because the function evaluation does not scale with input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    x = int(sys.stdin.readline().strip())

    if x <= -3:
        return str(-x + 4)
    elif x <= 2:
        return str(-2 * x + 1)
    else:
        return str(x**3 - 14 * x + 17)

# sample-style checks
assert run("-3") == "7"
assert run("3") == "2"

# boundary cases
assert run("-10") == "14"
assert run("-4") == "8"
assert run("2") == "-3"
assert run("0") == "1"

# cubic edge
assert run("10") == str(1000 - 140 + 17)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| -10 | 14 | extreme left branch correctness |
| -3 | 7 | left boundary inclusion |
| 2 | -3 | middle boundary inclusion |
| 0 | 1 | middle interval correctness |
| 10 | 877 | cubic branch correctness |

## Edge Cases

The most important edge cases are exactly the interval boundaries at $x = -3$ and $x = 2$.

For $x = -3$, the input triggers the first branch because the condition is $x \le -3$. The computation is $-(-3) + 4 = 7$. If a programmer mistakenly used strict inequality or checked the middle branch first, this value would incorrectly fall into the linear middle formula.

For $x = 2$, the second branch applies because it is defined as $x \le 2$. The computation becomes $-2 \cdot 2 + 1 = -3$. If the condition were written incorrectly as $x < 2$, then $x = 2$ would incorrectly jump to the cubic expression, producing a completely different result.

Both cases show that correctness depends not on arithmetic but on preserving the exact interval partition.
