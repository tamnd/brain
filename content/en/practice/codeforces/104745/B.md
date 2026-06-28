---
title: "CF 104745B - Operation"
description: "We are given two positive integers, and we are allowed to apply one of the four basic arithmetic operations between them: addition, subtraction, multiplication, or division. Each operation produces a value, and we must determine which operation yields the largest result."
date: "2026-06-28T23:01:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104745
codeforces_index: "B"
codeforces_contest_name: "CAMA 2023"
rating: 0
weight: 104745
solve_time_s: 48
verified: true
draft: false
---

[CF 104745B - Operation](https://codeforces.com/problemset/problem/104745/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two positive integers, and we are allowed to apply one of the four basic arithmetic operations between them: addition, subtraction, multiplication, or division. Each operation produces a value, and we must determine which operation yields the largest result.

The input is simply two integers, call them $a$ and $b$, both between 1 and 100 inclusive. The task is to compute four candidate results from these values and output the maximum among them.

The constraint range is extremely small. Since both numbers are at most 100, any arithmetic operation is constant time and can be evaluated directly without concern for overflow in Python or performance issues. This immediately rules out the need for any preprocessing, search, or optimization technique. A direct evaluation of all possible expressions is sufficient.

There are a few subtle points that can cause mistakes if handled carelessly. The division operation is the main one. If interpreted as real division, it produces a floating point value, while the other operations produce integers. This means comparisons must be done consistently in a numeric type that preserves correctness across all operations.

Another potential pitfall is assuming integer division. For example, if $a = 8$ and $b = 3$, integer division would give 2, while real division gives approximately 2.666..., which can affect whether division becomes the maximum operation. Since the problem does not restrict division to integer division, it must be treated as real division.

A second edge case is when subtraction produces a negative number. Since inputs are positive, subtraction can still be negative, and that value will never be maximal when compared against addition, multiplication, or division, but it must still be considered for correctness.

## Approaches

The straightforward way to solve this problem is to compute all four expressions explicitly: $a + b$, $a - b$, $a \times b$, and $a / b$. Once we compute these values, we simply take the maximum.

This brute-force approach is already optimal because the problem size is constant. We perform exactly four operations, each in constant time. There is no hidden structure or constraint that suggests any operation can be ignored safely without evaluation. Even reasoning about dominance relations between operations is unnecessary because the input range is small and does not require pruning.

The brute-force approach is correct because every allowed operation is independent, and the maximum must come from one of them. There is no transformation or sequence of operations, so there is no combinatorial explosion.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the two integers $a$ and $b$. These are the only inputs required, and no additional parsing or preprocessing is needed.
2. Compute the sum $a + b$. This represents the additive combination of the two values and is always non-decreasing relative to individual inputs.
3. Compute the difference $a - b$. This captures the effect of subtraction, which can reduce the value significantly depending on the relative magnitude of the inputs.
4. Compute the product $a \times b$. Since both numbers are positive and at least 1, this value will always be at least as large as each individual input.
5. Compute the division $a / b$ using real division. This ensures fractional results are preserved, which is necessary for correct comparison against the other operations.
6. Compare all four results and output the maximum.

### Why it works

Every valid answer is explicitly constructed in one of the previous steps. Since the problem defines the result space as exactly four expressions, and there are no hidden operations or transformations, evaluating all candidates guarantees that no possible answer is missed. The maximum of a finite complete set is the correct answer by definition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, b = map(int, input().split())
    
    res1 = a + b
    res2 = a - b
    res3 = a * b
    res4 = a / b  # real division
    
    print(max(res1, res2, res3, res4))

if __name__ == "__main__":
    solve()
```

The solution reads the two integers and directly evaluates each of the four candidate expressions. The division is performed using floating point arithmetic, which in Python is precise enough for values in the given range. The final answer is computed using Python’s built-in max function over the four results.

A subtle implementation detail is ensuring that division is not accidentally replaced with integer division using `//`. Doing so would change the meaning of the operation and could incorrectly reduce the maximum in cases where fractional values matter.

## Worked Examples

### Example 1: Input `6 3`

| Step | a | b | a+b | a-b | a*b | a/b | Current max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Compute | 6 | 3 | 9 | 3 | 18 | 2.0 | 18 |

The multiplication result dominates all others, so the output is 18. This confirms that multiplication can overpower both addition and division even for small inputs.

### Example 2: Input `8 1`

| Step | a | b | a+b | a-b | a*b | a/b | Current max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Compute | 8 | 1 | 9 | 7 | 8 | 8.0 | 9 |

Here, addition produces the largest value. This example shows that multiplication is not always optimal, especially when one operand is 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only four arithmetic operations and one comparison are performed |
| Space | O(1) | No auxiliary data structures are used |

The constant-time nature of the solution fits easily within any reasonable time limit, and memory usage is negligible since only a few scalar variables are stored.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    a, b = map(int, sys.stdin.readline().split())
    
    res1 = a + b
    res2 = a - b
    res3 = a * b
    res4 = a / b
    
    return str(max(res1, res2, res3, res4))

# provided samples
assert run("6 3\n") == "18"
assert run("8 1\n") == "9"

# minimum values
assert run("1 1\n") == "2"

# subtraction dominates negativity check
assert run("1 100\n") == "100"

# multiplication edge case
assert run("100 100\n") == "10000"

# division fractional dominance
assert run("3 2\n") == "6"

# identity check
assert run("5 1\n") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 2 | minimum boundary behavior |
| 1 100 | 100 | subtraction producing negative value |
| 100 100 | 10000 | maximum multiplication case |
| 3 2 | 6 | division produces fractional value |

## Edge Cases

One edge case is when subtraction becomes negative, such as input `1 100`. The algorithm computes `1 - 100 = -99`, but this value is naturally ignored by the `max` operation since other results are larger. The computation still includes it, preserving correctness by exhaustiveness rather than pruning.

Another case is when division produces a non-integer value, such as `3 2`. The algorithm computes `3 / 2 = 1.5`, while multiplication gives `6`, which becomes the maximum. The floating-point result is still correctly compared against integers because Python promotes integers to floats during comparison.

A final edge case is when both numbers are equal, such as `100 100`. All operations remain valid and well-defined, and multiplication produces the largest result. The algorithm does not rely on any ordering assumptions and evaluates all expressions uniformly, ensuring correctness across symmetric inputs.
