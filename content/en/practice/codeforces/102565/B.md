---
title: "CF 102565B - Broken Python"
description: "The task is to evaluate a single mathematical expression written as a string. The expression contains integers, arithmetic operators, and parentheses."
date: "2026-08-07T06:18:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102565
codeforces_index: "B"
codeforces_contest_name: "AGM 2020, Final Round, Day 2"
rating: 0
weight: 102565
solve_time_s: 406
verified: true
draft: false
---

[CF 102565B - Broken Python](https://codeforces.com/problemset/problem/102565/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to evaluate a single mathematical expression written as a string. The expression contains integers, arithmetic operators, and parentheses. The required result follows normal mathematical precedence: parentheses first, then powers, then multiplication and division, then addition and subtraction. Operators with the same priority are processed from left to right.

The difficulty is not the arithmetic itself. A direct implementation using Python's `eval` or a recursive parser can fail because the expression length can reach 100000 characters. That size immediately rules out approaches that repeatedly copy large substrings or build a deeply recursive parse tree. An O(n) or O(n log n) solution is the realistic target because every character may need to be inspected.

The expression also allows intermediate values that are rational numbers even though the final answer is an integer. A solution that performs integer division will silently produce wrong answers. For example, `(1/2)*2` should evaluate to `1`, while integer division would turn `1/2` into `0`.

Another dangerous case is exponentiation. For input `2^3^2`, many programming languages disagree about associativity, but this problem guarantees that the exponent part is a positive integer and not an expression. A parser that treats powers like multiplication and division without respecting the given structure can misread expressions such as `35^66*0/35`.

Unary operators are also a possible source of mistakes. The statement guarantees they are always surrounded by parentheses, so an expression like `(-5)` appears instead of a free-standing `-5` in the middle of parsing. Ignoring this detail can lead to incorrect handling of negative numbers.

## Approaches

A simple approach is to repeatedly find the operation with the highest priority, calculate it, replace it with its result, and continue until only one value remains. This mirrors how a human evaluates expressions and is easy to verify. The problem is the repeated searching and rebuilding of the expression. If every operation requires scanning most of a 100000-character string, the worst case becomes quadratic, around 10^10 character operations, which is far beyond the limit.

The key observation is that the expression already has a strict grammar. Instead of repeatedly searching for the next operation, we can scan the expression once while maintaining the current evaluation state. The standard way to do this is a stack-based parser.

The parser separates the expression into values and operators. Whenever an operator is seen, its precedence is compared with operators waiting on the stack. Higher priority operations are resolved immediately, while lower priority operations wait until the necessary values are available. Parentheses work as markers that temporarily block evaluation until the matching closing parenthesis appears.

Because powers always have a simple exponent form in this problem, they can be handled when encountered without needing a more complicated recursive parser. Rational intermediate values are stored exactly using fractions, avoiding floating point errors.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Scan the expression from left to right and tokenize numbers, operators, and parentheses. When a complete integer is found, convert it into an exact fraction value. Keeping exact fractions from the beginning prevents precision problems later.
2. Maintain two stacks. One stack stores numbers, and the other stores operators. When a number appears, push it onto the number stack because it cannot be combined until an operator connects it with another value.
3. When an operator appears, resolve operators already waiting on the operator stack while they have higher or equal precedence. Equal precedence is resolved immediately because multiplication, division, addition, and subtraction are left associative.
4. When an opening parenthesis appears, push it as a special marker. It separates the inside expression from operations outside the parentheses.
5. When a closing parenthesis appears, repeatedly apply operators until the matching opening parenthesis is removed. The values inside the parentheses have now become one complete expression result.
6. After the complete scan finishes, apply all remaining operators in the operator stack. The only remaining number is the final value.
7. Convert the final fraction to an integer and print it. The problem guarantees that this conversion is exact.

Why it works:

At every point during the scan, the stacks represent exactly the part of the expression that has been read but cannot yet be finalized. An operator stays on the operator stack only while a future token could still change the order of evaluation. Whenever that is no longer possible, the operator is applied immediately. Since operators are removed according to the required precedence and associativity rules, every operation is performed in the same order as mathematical evaluation.

## Python Solution

```python
import sys
from fractions import Fraction

input = sys.stdin.readline

def solve():
    s = input().strip()

    def precedence(op):
        if op == '^':
            return 3
        if op == '*' or op == '/':
            return 2
        if op == '+' or op == '-':
            return 1
        return 0

    def apply_op(nums, op):
        b = nums.pop()
        a = nums.pop()

        if op == '+':
            nums.append(a + b)
        elif op == '-':
            nums.append(a - b)
        elif op == '*':
            nums.append(a * b)
        elif op == '/':
            nums.append(a / b)
        else:
            nums.append(b ** a)

    nums = []
    ops = []

    i = 0
    n = len(s)

    while i < n:
        c = s[i]

        if c.isdigit():
            value = 0
            while i < n and s[i].isdigit():
                value = value * 10 + ord(s[i]) - ord('0')
                i += 1
            nums.append(Fraction(value))
            continue

        if c == '(':
            ops.append(c)

        elif c == ')':
            while ops[-1] != '(':
                apply_op(nums, ops.pop())
            ops.pop()

        else:
            while ops and ops[-1] != '(' and precedence(ops[-1]) >= precedence(c):
                apply_op(nums, ops.pop())
            ops.append(c)

        i += 1

    while ops:
        apply_op(nums, ops.pop())

    print(nums[0].numerator)

if __name__ == "__main__":
    solve()
```

The parser uses `Fraction` because intermediate divisions can create non-integer values. For example, after reading `(1/2)`, the stack contains an exact rational value rather than a rounded floating point approximation.

The number parser reads consecutive digits manually. This avoids creating many temporary substrings and keeps the scan linear.

The precedence function determines when an operator waiting on the stack should be executed. The comparison uses `>=` because the operations of equal priority are evaluated from left to right.

The exponent operator is slightly different from the others. The problem guarantee that the exponent is already a positive integer value, so applying it through the same stack mechanism is safe.

Python integers do not overflow, which is useful because intermediate values can be much larger than the final answer.

## Worked Examples

For `1+1-1`:

| Current token | Number stack | Operator stack | Action |
| --- | --- | --- | --- |
| `1` | 1 |  | Push number |
| `+` | 1 | + | Push operator |
| `1` | 1, 1 | + | Push number |
| `-` | 2 | - | Resolve `+` |
| `1` | 2, 1 | - | Push number |
| end | 1 |  | Resolve `-` |

The example shows left-to-right handling of addition and subtraction. The `+` operation is completed before the later `-` operation is considered.

For `35^66*0/35`:

| Current token | Number stack | Operator stack | Action |
| --- | --- | --- | --- |
| `35` | 35 |  | Push number |
| `^` | 35 | ^ | Push operator |
| `66` | 35, 66 | ^ | Push number |
| `*` | huge value | * | Resolve power |
| `0` | huge value, 0 | * | Push number |
| `/` | 0 | / | Resolve multiplication |
| `35` | 0, 35 | / | Push number |
| end | 0 |  | Resolve division |

The trace demonstrates why applying operations by precedence matters. The enormous power is calculated first, but it is later multiplied by zero, producing a manageable final result.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every character is scanned once and every operator is pushed and popped once. |
| Space | O(n) | The stacks can contain all tokens in the worst case. |

With an expression length of 100000 characters, a linear parser easily fits the time limit. The memory usage is also acceptable because the stacks store only tokens from the input.

## Test Cases

```
from fractions import Fraction

def evaluate(inp):
    s = inp.strip()

    def precedence(op):
        if op == '^':
            return 3
        if op in '*/':
            return 2
        if op in '+-':
            return 1
        return 0

    def apply(nums, op):
        b = nums.pop()
        a = nums.pop()
        if op == '+':
            nums.append(a + b)
        elif op == '-':
            nums.append(a - b)
        elif op == '*':
            nums.append(a * b)
        elif op == '/':
            nums.append(a / b)
        else:
            nums.append(b ** a)

    nums, ops = [], []
    i = 0

    while i < len(s):
        if s[i].isdigit():
            x = 0
            while i < len(s) and s[i].isdigit():
                x = x * 10 + int(s[i])
                i += 1
            nums.append(Fraction(x))
            continue

        if s[i] == '(':
            ops.append(s[i])
        elif s[i] == ')':
            while ops[-1] != '(':
                apply(nums, ops.pop())
            ops.pop()
        else:
            while ops and ops[-1] != '(' and precedence(ops[-1]) >= precedence(s[i]):
                apply(nums, ops.pop())
            ops.append(s[i])
        i += 1

    while ops:
        apply(nums, ops.pop())

    return str(nums[0].numerator)

assert evaluate("1+1-1") == "1"
assert evaluate("35^66*0/35") == "0"
assert evaluate("(1/2)*2") == "1"

assert evaluate("1") == "1"
assert evaluate("5*5*5") == "125"
assert evaluate("10/(2+3)") == "2"
assert evaluate("(7-3)*(2+1)") == "12"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | Single number handling |
| `5*5*5` | `125` | Left-to-right multiplication |
| `10/(2+3)` | `2` | Parentheses and division |
| `(7-3)*(2+1)` | `12` | Nested expression evaluation |

## Edge Cases

For `(1/2)*2`, the parser first evaluates the division inside the parentheses. The number stack stores `1/2` exactly, then multiplication combines it with `2` to produce `1`. A solution using integer division would incorrectly output `0`.

For `35^66*0/35`, the parser applies the power operation before multiplication because exponentiation has higher priority. The huge intermediate value does not cause a problem because Python integers support arbitrary precision and the later multiplication by zero reduces the result.

For `(5)`, the opening parenthesis is stored as a barrier and removed when the closing parenthesis appears. The algorithm leaves the contained number unchanged, producing `5`.

For `8/4/2`, the first division is applied before the second because equal-priority operators are resolved immediately when the next operator appears. The evaluation becomes `(8/4)/2`, giving `1` rather than `4`.

I can also convert this into a shorter Codeforces-style editorial format if you need something closer to an official contest write-up.
