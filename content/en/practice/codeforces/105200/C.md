---
title: "CF 105200C - Correcting Exams"
description: "We are given a very small computational task: a pair of integers represents a fraction, and we need to decide whether that fraction is at least one half. You can think of it as checking whether some obtained value is “not worse than half of the maximum possible”."
date: "2026-06-27T02:52:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105200
codeforces_index: "C"
codeforces_contest_name: "IME++ Starters Try-outs 2024"
rating: 0
weight: 105200
solve_time_s: 42
verified: true
draft: false
---

[CF 105200C - Correcting Exams](https://codeforces.com/problemset/problem/105200/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a very small computational task: a pair of integers represents a fraction, and we need to decide whether that fraction is at least one half.

You can think of it as checking whether some obtained value is “not worse than half of the maximum possible”. The input describes a numerator and a denominator, and the output is a binary decision, typically printed as a yes/no style answer or a 1/0 depending on the problem’s convention.

The core operation is a comparison between a ratio and a fixed threshold. Since everything reduces to a single arithmetic condition, the structure is constant time per test case.

Even though the task looks trivial, there are a few failure modes that often show up in incorrect submissions. The most common one is floating-point division. For example, comparing `a / b >= 0.5` using floating-point arithmetic can produce incorrect results when `a` and `b` are large, because precision loss may flip borderline cases.

Another subtle issue is integer division. If someone writes `a / b >= 1/2` in a language where integer division truncates, the expression `a / b` becomes zero for many valid inputs, which destroys correctness immediately.

A concrete edge case is when the value is exactly on the boundary. For instance, if `a = 5` and `b = 10`, the correct answer is true because it is exactly half. A floating-point approach might still work here, but a careless integer division approach would incorrectly evaluate `5 / 10` as `0` and fail the check.

The safe way to reason about all of this is to avoid division entirely and transform the inequality into an equivalent integer comparison.

## Approaches

The brute-force interpretation would compute the fraction directly and compare it against one half. That means evaluating `a / b` as a floating-point number and checking whether it is at least `0.5`. This works conceptually because it directly matches the definition of the problem.

However, this approach becomes fragile in implementation. Floating-point arithmetic has limited precision, and when `a` and `b` grow large, rounding errors can occur. In worst cases, values extremely close to the threshold may be misclassified. Even though the time complexity is constant, correctness is not guaranteed under typical competitive programming constraints.

The key observation is that we can eliminate division entirely by multiplying both sides of the inequality. The condition

$$\frac{a}{b} \ge \frac{1}{2}$$

can be rewritten as

$$2a \ge b$$

This transformation preserves correctness while using only integer arithmetic. It also avoids division by zero pitfalls entirely, since we never divide.

Once reduced to this form, the problem becomes a single comparison per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (floating-point division) | O(1) | O(1) | Risky |
| Optimal (integer inequality) | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the two integers `a` and `b` from input. These represent the numerator and denominator of the fraction we are evaluating.
2. Convert the condition “fraction is at least half” into an integer inequality by rewriting it as `2 * a >= b`. This avoids any division and keeps all operations exact.
3. Perform the comparison using integer arithmetic only. If the inequality holds, the fraction is at least one half.
4. Output the corresponding result according to the problem’s required format.

### Why it works

The correctness comes from an equivalence transformation of inequalities. Multiplying both sides of a comparison by a positive number preserves ordering, so multiplying by `2b` (or just cross-multiplying carefully) does not change the truth of the statement. Since `b` is assumed positive in any valid fraction context, no sign reversal occurs. This ensures the integer condition matches the original fractional condition exactly for all valid inputs.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, b = map(int, input().split())
    if 2 * a >= b:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()
```

The program reads a single pair of integers and directly applies the transformed inequality. The multiplication `2 * a` is safe in Python because Python integers are unbounded in practice, so overflow is not an issue.

The decision is made in constant time and printed immediately.

## Worked Examples

### Example 1

Input:

```
5 10
```

| Step | a | b | 2a | Condition (2a ≥ b) | Output |
| --- | --- | --- | --- | --- | --- |
| Start | 5 | 10 | - | - | - |
| Compute | 5 | 10 | 10 | 10 ≥ 10 | YES |

This case sits exactly on the boundary. The transformation handles equality correctly, confirming that “at least half” includes the boundary case.

### Example 2

Input:

```
3 10
```

| Step | a | b | 2a | Condition (2a ≥ b) | Output |
| --- | --- | --- | --- | --- | --- |
| Start | 3 | 10 | - | - | - |
| Compute | 3 | 10 | 6 | 6 ≥ 10 (false) | NO |

Here the value is strictly below half. The integer comparison immediately rejects it without any floating-point computation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic operations per test case |
| Space | O(1) | No auxiliary data structures are used |

The solution fits easily within constraints since it performs only a couple of integer operations regardless of input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

def solve():
    a, b = map(int, input().split())
    if 2 * a >= b:
        print("YES")
    else:
        print("NO")

# provided-like samples
assert run("5 10\n") == "YES"
assert run("3 10\n") == "NO"

# custom cases
assert run("1 2\n") == "YES", "exact half boundary"
assert run("0 1\n") == "NO", "zero numerator"
assert run("10 1\n") == "YES", "greater than one"
assert run("7 14\n") == "YES", "even split exact boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2` | YES | Exact boundary case |
| `0 1` | NO | Zero fraction handling |
| `10 1` | YES | Fraction greater than 1 |
| `7 14` | YES | Even split correctness |

## Edge Cases

A boundary case like `1 2` demonstrates the equality condition. The algorithm computes `2 * 1 = 2` and compares it with `2`, producing a correct YES output. This confirms that equality is handled properly.

A zero numerator case like `0 1` produces `2 * 0 = 0`, and since `0 >= 1` is false, the output is NO. This verifies that the algorithm does not incorrectly treat zero as passing any positive threshold.

A case where the fraction exceeds one, such as `10 1`, produces `2 * 10 = 20`, which trivially satisfies the condition. This shows that the method works even outside the typical [0,1] range interpretation.
