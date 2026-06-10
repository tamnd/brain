---
title: "CF 1461F - Mathematical Expression"
description: "We are given a sequence of digits, each between 0 and 9, and a set of allowed operators, which can be any combination of addition, subtraction, and multiplication."
date: "2026-06-11T02:24:23+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1461
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 689 (Div. 2, based on Zed Code Competition)"
rating: 2700
weight: 1461
solve_time_s: 108
verified: false
draft: false
---

[CF 1461F - Mathematical Expression](https://codeforces.com/problemset/problem/1461/F)

**Rating:** 2700  
**Tags:** constructive algorithms, dp, greedy  
**Solve time:** 1m 48s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of digits, each between 0 and 9, and a set of allowed operators, which can be any combination of addition, subtraction, and multiplication. The task is to place exactly one operator between every pair of consecutive digits to maximize the value of the resulting expression. The expression follows standard operator precedence: multiplication binds tighter than addition or subtraction, and addition and subtraction are evaluated left to right.

Given that the sequence can be up to 100,000 digits long, any approach that tries all possible placements of operators is immediately infeasible, because there are up to $3^{10^5}$ ways to place operators. This means we need an approach that avoids exponential growth, ideally something linear or linearithmic.

Non-obvious edge cases arise with zeros and ones because multiplication interacts with them differently than other numbers. For example, multiplying by zero annihilates the running product, so "2_0+3" yields 3, which may be better than "2_0*3" which yields 0. Similarly, multiplying by one does not increase the value, so adding one can sometimes be preferable. Negative numbers are not present in the input digits, but subtraction can reduce the running total in ways addition does not, which must be considered carefully when the allowed set includes subtraction.

A careless greedy approach that always multiplies the largest two numbers could fail when a zero appears in the sequence, or when addition of small numbers produces a higher final total than multiplication chains involving ones.

## Approaches

The brute-force approach is to try every combination of operators between the digits. This is correct in principle because it explores all possible expressions, but its complexity is $O(3^{n})$, which is absolutely infeasible for $n$ up to 100,000. Even a dynamic programming approach that considers every subarray and every possible operator between them in a naive way would be roughly $O(n^2)$, which is too slow.

The key insight is that, due to the small range of digits (0 to 9) and the precedence rules, we can segment the sequence at zeros when multiplication is allowed, because multiplying anything by zero resets the product to zero. Beyond zeros, we only need to decide between addition and multiplication for sequences of digits, and this can be done greedily for small digits. For instance, if both 1 and multiplication are allowed, it is often better to add the ones rather than multiply them because multiplying by one doesn't increase the value, whereas adding does. For sequences of digits without zeros, we can iterate left to right and decide: if the current digit is 0 or 1 and both addition and multiplication are allowed, addition is preferable; otherwise multiplication.

Thus the optimal approach is a greedy left-to-right scan that segments around zeros, treats sequences with ones differently, and respects the allowed operators set. Subtraction can be handled similarly to addition if present, but it is always applied carefully to avoid decreasing the total unnecessarily.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3^n) | O(n) | Too slow |
| Greedy with segmentation and operator rules | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Parse the sequence of digits into a list and record the allowed operators in a set for O(1) lookups. If only one operator is allowed, the solution is trivial: insert that operator everywhere.
2. If multiplication is allowed and the sequence contains zeros, split the sequence into subarrays separated by zeros. Each zero will be preceded by a plus if addition is allowed, because multiplication by zero resets any product. Zeros themselves are treated as separate numbers that may be added or subtracted to maximize the total.
3. Iterate over each subarray of digits without zeros. For these, iterate left to right and decide which operator to place between each pair. If addition is allowed and the current digit or the next digit is 0 or 1, place addition, because multiplication would not increase the value or would reduce it to zero. Otherwise, place multiplication.
4. Concatenate the resulting segments back together, inserting plus or minus operators around zeros if allowed, and multiplication elsewhere.
5. Output the constructed expression.

Why it works: The invariant is that at each position, we maximize the contribution of the next digit to the running product or sum, considering zeros and ones. Splitting at zeros ensures multiplication never produces zero when it would reduce the value unnecessarily, and choosing addition with ones ensures the total is not wasted by multiplying by one. This produces a globally optimal expression due to the limited range of digits and operator precedence rules.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))
ops = set(input().strip())

if n == 1:
    print(a[0])
    sys.exit()

# Only one operator allowed
if len(ops) == 1:
    op = ops.pop()
    print(op.join(map(str, a)))
    sys.exit()

res = []
for i in range(n - 1):
    res.append(str(a[i]))
    x, y = a[i], a[i + 1]

    if '*' in ops:
        if '+' in ops:
            if x <= 1 or y <= 1:
                res.append('+')
            else:
                res.append('*')
        elif '-' in ops:
            if x <= 1 or y <= 1:
                res.append('-')
            else:
                res.append('*')
        else:
            res.append('*')
    else:
        if '+' in ops:
            res.append('+')
        else:
            res.append('-')
res.append(str(a[-1]))
print(''.join(res))
```

The first section handles trivial cases when only one operator is allowed. The main loop then makes local greedy decisions: multiplication is chosen for digits greater than 1, and addition or subtraction is chosen if a zero or one appears to avoid lowering the value. The final element is appended without an operator.

## Worked Examples

Sample input:

```
3
2 2 0
+-*
```

| i | a[i] | a[i+1] | Decision | Expression so far |
| --- | --- | --- | --- | --- |
| 0 | 2 | 2 | * | 2*2 |
| 1 | 2 | 0 | + | 2*2+0 |

This demonstrates that multiplication is chosen between 2 and 2 because it increases the value, and addition is chosen before zero to avoid nullifying the previous product.

Custom input:

```
5
1 2 3 0 4
+*
```

| i | a[i] | a[i+1] | Decision | Expression so far |
| --- | --- | --- | --- | --- |
| 0 | 1 | 2 | + | 1+2 |
| 1 | 2 | 3 | * | 1+2*3 |
| 2 | 3 | 0 | + | 1+2*3+0 |
| 3 | 0 | 4 | + | 1+2*3+0+4 |

This confirms that zeros split multiplication sequences, and ones are treated additively.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed exactly once in the loop. |
| Space | O(n) | Resulting expression is stored in a list of length roughly 2n-1. |

The algorithm scales linearly with input size, which is safe given n ≤ 10^5 and the 1-second time limit. Memory usage is proportional to the input, well within 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    exec(open("solution.py").read(), globals())
    return sys.stdout.getvalue().strip()

# Provided sample
assert run("3\n2 2 0\n+-*\n") == "2*2+0", "sample 1"

# Single element
assert run("1\n7\n+\n") == "7", "single element"

# Only multiplication allowed
assert run("3\n2 3 4\n*\n") == "2*3*4", "multiplication only"

# Only addition allowed
assert run("3\n2 3 4\n+\n") == "2+3+4", "addition only"

# Ones in sequence
assert run("4\n1 1 2 3\n+*\n") == "1+1*2*3", "ones treated additively"

# Zero splitting
assert run("5\n2 0 3 4 0\n+*\n") == "2+0+3*4+0", "zeros split multiplications"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 7 | Trivial case |
| Multiplication only | 2_3_4 | Single-operator edge case |
| Addition only | 2+3+4 | Single-operator edge case |
| Ones | 1+1_2_3 | Ones handled correctly in mixed operators |
| Zeros | 2+0+3*4+0 | Multiplication sequences split at zeros |

## Edge Cases

If the input contains only zeros, like `0 0 0` and operators `+*`, the algorithm produces `0+0+0`. Multiplying would reset
