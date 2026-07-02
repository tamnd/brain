---
title: "CF 103566B - \u0411\u0430\u0440\u0438\u0441\u0442\u0430"
description: "We are given two integers, representing quantities $a$ and $b$, and we need to classify their ratio into one of three coffee types based on how large $a$ is compared to $b$. Instead of working with floating-point ratios, the decision is made using inequalities."
date: "2026-07-03T04:57:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103566
codeforces_index: "B"
codeforces_contest_name: "2021-2022 Olympiad Cognitive Technologies, Final Round"
rating: 0
weight: 103566
solve_time_s: 42
verified: true
draft: false
---

[CF 103566B - \u0411\u0430\u0440\u0438\u0441\u0442\u0430](https://codeforces.com/problemset/problem/103566/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two integers, representing quantities $a$ and $b$, and we need to classify their ratio into one of three coffee types based on how large $a$ is compared to $b$.

Instead of working with floating-point ratios, the decision is made using inequalities. If $a$ is less than three times $b$, the output should be the first drink. If $a$ is greater than five times $b$, the output should be the second drink. Otherwise, it falls into the middle category.

The input is therefore a single pair of integers, and the output is exactly one of three fixed strings.

The constraints are not explicitly shown, but the structure of the problem makes it clear that the solution must be constant time per test case. Any solution involving simulation or repeated subtraction would be unnecessary and would fail under typical competitive programming limits where $a$ and $b$ can be large.

The main subtle edge cases come from boundary equality. For example, when $a = 3b$, the first condition is not satisfied, so the answer must move to the next check. Similarly, when $a = 5b$, the second condition is also not satisfied, which forces the default case.

A careless implementation often fails by using strict floating-point division with rounding errors or by mixing up strict and non-strict inequalities.

For instance, if $a = 3$ and $b = 1$, the correct output is the middle category since $a$ is not less than $3b$ and not greater than $5b$. Any implementation using floating-point comparisons like $a / b < 3$ can incorrectly misclassify due to precision issues in other settings.

## Approaches

The most direct approach is to literally compute the ratio $a / b$ as a floating-point number and compare it to 3 and 5. This is logically correct in theory, but it introduces unnecessary floating-point arithmetic and risks precision errors in borderline cases. It also requires division, which is slower than integer multiplication and less clean in integer-heavy problems.

A more robust approach avoids division entirely by rewriting the inequalities. The condition $a / b < 3$ is equivalent to $a < 3b$, and similarly $a / b > 5$ becomes $a > 5b$. This transformation preserves correctness while ensuring all computations stay in integer arithmetic, which is exact and safe.

The key insight is that we never actually need the ratio, only its position relative to two thresholds. Once that is recognized, the problem reduces to two comparisons and a default case.

The brute-force interpretation works because the decision depends only on a single comparison of magnitudes, but it becomes unnecessary once we observe that scaling both sides by $b$ removes division entirely.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Floating-point division | O(1) | O(1) | Risky |
| Integer comparison (optimal) | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read integers $a$ and $b$ from input. These represent the two quantities whose ratio determines the output classification.
2. Check whether $a < 3b$. If this holds, immediately output the first drink. This check is placed first because it captures the smallest region of values.
3. If the first condition is false, check whether $a > 5b$. If this holds, output the second drink. This identifies the large-ratio regime.
4. If neither condition is satisfied, output the middle drink. This corresponds exactly to the interval $3b \le a \le 5b$.

### Why it works

The logic partitions the number line for $a$ into three disjoint regions relative to $b$: values strictly below $3b$, values strictly above $5b$, and values in between. Every integer pair $(a, b)$ falls into exactly one of these regions because the inequalities are complementary and cover all possibilities without overlap. Since each region is mapped to a unique output, the algorithm cannot assign conflicting results.

## Python Solution

```python
import sys
input = sys.stdin.readline

a, b = map(int, input().split())

if a < 3 * b:
    print("macchiato")
elif a > 5 * b:
    print("latte")
else:
    print("cappuccino")
```

The implementation directly mirrors the derived inequalities. The multiplication replaces division, which ensures exact integer comparisons without precision issues. The ordering of conditions matters: the small threshold is checked first, then the large threshold, and everything else falls into the middle category.

A subtle point is that both comparisons must use strict inequalities exactly as derived. Changing them to $\le$ or $\ge$ would shift boundary values into the wrong category.

## Worked Examples

### Example 1

Input:

```
2 1
```

| Step | a | b | Condition a < 3b | Condition a > 5b | Output |
| --- | --- | --- | --- | --- | --- |
| Start | 2 | 1 | true | false | macchiato |

Here $2 < 3\cdot1$, so the first condition triggers immediately. This confirms that small ratios are classified correctly without evaluating later conditions.

### Example 2

Input:

```
10 2
```

| Step | a | b | Condition a < 3b | Condition a > 5b | Output |
| --- | --- | --- | --- | --- | --- |
| Start | 10 | 2 | false | true | latte |

Here $10 > 5\cdot2 = 10$ is false, so actually we must be careful: it equals 10, not greater. So neither condition holds, and the result becomes cappuccino.

This trace highlights the importance of strict inequality. Equality cases sit exactly in the middle interval.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic operations and comparisons are performed |
| Space | O(1) | No auxiliary data structures are used |

The solution is optimal for any input size since it reduces the decision to a fixed number of integer operations, independent of magnitude.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    a, b = map(int, input().split())

    if a < 3 * b:
        return "macchiato"
    elif a > 5 * b:
        return "latte"
    else:
        return "cappuccino"

# provided samples (constructed)
assert run("2 1\n") == "macchiato"
assert run("10 2\n") == "cappuccino"

# custom cases
assert run("0 10\n") == "macchiato", "minimum a"
assert run("100 1\n") == "latte", "large ratio"
assert run("3 1\n") == "cappuccino", "boundary 3b"
assert run("5 1\n") == "cappuccino", "boundary 5b"
assert run("15 3\n") == "cappuccino", "exact middle region"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 10 | macchiato | lower extreme ratio |
| 100 1 | latte | large ratio behavior |
| 3 1 | cappuccino | exact lower boundary |
| 5 1 | cappuccino | exact upper boundary |
| 15 3 | cappuccino | typical middle case |

## Edge Cases

When $a = 3b$, the first inequality fails because it is strict. For example, input $a=3, b=1$ yields neither the first nor second condition, so the output becomes cappuccino. The algorithm handles this correctly because equality naturally falls into the else branch.

When $a = 5b$, the second condition also fails. For example, $a=10, b=2$ produces equality and is correctly classified into the middle category. This confirms that the strictness of the upper bound is essential.

When $b$ is large, such as $a=0, b=10^9$, the multiplication $3b$ and $5b$ still fits within 64-bit integer range, so no overflow concerns arise in Python. The first condition triggers immediately, producing macchiato as expected.

These cases confirm that the algorithm behaves consistently across boundary and extreme inputs without requiring special handling.
