---
title: "CF 470C - Eval"
description: "The task is to evaluate a simple arithmetic expression of the form a?b where a and b are integers between 1 and 999, and ? is a single operator from the set +, -, , /, or %."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 470
codeforces_index: "C"
codeforces_contest_name: "Surprise Language Round 7"
rating: 1900
weight: 470
solve_time_s: 62
verified: true
draft: false
---

[CF 470C - Eval](https://codeforces.com/problemset/problem/470/C)

**Rating:** 1900  
**Tags:** *special  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to evaluate a simple arithmetic expression of the form `a?b` where `a` and `b` are integers between 1 and 999, and `?` is a single operator from the set `+`, `-`, `*`, `/`, or `%`. Conceptually, this is just taking two numbers and applying the indicated operation, then printing the resulting integer.

The input is a single line string containing the expression without spaces. That means we cannot rely on standard tokenization by whitespace; we need to identify the operator in the string, split the two numbers accordingly, and perform the operation.

The constraints are small: the numbers are always in the range 1 to 999, which fits comfortably in a standard 32-bit integer. Integer division `/` must truncate towards zero, and modulo `%` returns the remainder of the division. Because the input is just one line, performance is not a concern; any correct solution will run well under 2 seconds.

The non-obvious edge cases include expressions involving division or modulo, particularly ensuring that division by zero is never attempted. Here it is guaranteed that both `a` and `b` are at least 1, so division by zero cannot occur. Another subtlety is parsing: since the input does not have spaces, multi-digit numbers need to be extracted correctly, and care is required if the operator is `-`, which could be confused with a negative sign. Here, however, all numbers are positive, so the first `-` found is guaranteed to be the operator.

## Approaches

A naive approach is to evaluate the expression using Python's `eval()` function after reading the input as a string. This works because `eval()` can directly parse arithmetic strings, but using `eval()` in competitive programming is discouraged due to potential security concerns and because it obscures the logic of parsing.

The standard approach is to scan the input string for the operator. Once we find it, everything before it is `a` and everything after is `b`. Then we use a simple conditional or a dictionary to map the operator character to the corresponding Python operation. This is both straightforward and efficient, because the input is guaranteed to have exactly one operator and the numbers are small.

The brute-force idea of testing all operators on all splits is unnecessary here because there is exactly one operator, so a single pass to find it suffices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (try all splits) | O(n) | O(1) | Overkill but accepted |
| Single-pass operator scan | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input string and strip any surrounding whitespace to ensure clean parsing. This ensures that accidental trailing newlines do not interfere with conversion to integers.
2. Scan the string character by character until you find the operator. Since the operator is guaranteed to be one of `+`, `-`, `*`, `/`, `%` and there is exactly one, the first occurrence is the operator.
3. Split the string at the operator. The substring before it is `a` and the substring after it is `b`. Convert both substrings to integers.
4. Depending on the operator, perform the corresponding operation: addition, subtraction, multiplication, integer division, or modulo.
5. Print the result as an integer. For division, Python's `//` operator handles truncating division correctly.

Why it works: The algorithm maintains the invariant that at any point before evaluation, `a` and `b` are exactly the integer values from the input string, and the operator is correctly identified. There are no other operations or ambiguity in the input, so this produces the correct arithmetic result.

## Python Solution

```python
import sys
input = sys.stdin.readline

expr = input().strip()

for i, c in enumerate(expr):
    if c in '+-*/%':
        op_index = i
        break

a = int(expr[:op_index])
b = int(expr[op_index+1:])
op = expr[op_index]

if op == '+':
    result = a + b
elif op == '-':
    result = a - b
elif op == '*':
    result = a * b
elif op == '/':
    result = a // b
elif op == '%':
    result = a % b

print(result)
```

The first loop finds the operator by scanning left to right. Converting slices of the string into integers ensures that multi-digit numbers are correctly handled. The conditional mapping from operator character to the arithmetic operation implements the exact evaluation rules.

## Worked Examples

Sample 1 input `123+456`:

| Step | expr | i | c | op_index | a | b | op | result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 123+456 | 0 | '1' | - | - | - | - | - |
| 2 | 123+456 | 1 | '2' | - | - | - | - | - |
| 3 | 123+456 | 2 | '3' | - | - | - | - | - |
| 4 | 123+456 | 3 | '+' | 3 | 123 | 456 | '+' | 579 |

The trace confirms that the operator is identified correctly, the numbers are parsed correctly, and addition produces the expected output.

Another input `999/3`:

| Step | expr | i | c | op_index | a | b | op | result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 999/3 | 0 | '9' | - | - | - | - | - |
| 2 | 999/3 | 3 | '/' | 3 | 999 | 3 | '/' | 333 |

The trace confirms integer division works as intended.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We scan the string once to find the operator; n ≤ 7 since numbers are ≤999 and operator adds 1. |
| Space | O(1) | Only a few integer variables and string slices are stored. |

The solution fits comfortably within 2 seconds and uses negligible memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    expr = input().strip()
    for i, c in enumerate(expr):
        if c in '+-*/%':
            op_index = i
            break
    a = int(expr[:op_index])
    b = int(expr[op_index+1:])
    op = expr[op_index]
    if op == '+':
        result = a + b
    elif op == '-':
        result = a - b
    elif op == '*':
        result = a * b
    elif op == '/':
        result = a // b
    elif op == '%':
        result = a % b
    return str(result)

# provided sample
assert run("123+456") == "579", "sample 1"

# custom cases
assert run("1+1") == "2", "minimum values"
assert run("999*999") == "998001", "maximum values"
assert run("100-100") == "0", "equal numbers subtraction"
assert run("999/3") == "333", "integer division"
assert run("100%3") == "1", "modulo operation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1+1 | 2 | Minimum possible input values |
| 999*999 | 998001 | Maximum input values and multiplication correctness |
| 100-100 | 0 | Subtraction resulting in zero |
| 999/3 | 333 | Integer division correctness |
| 100%3 | 1 | Modulo operation correctness |

## Edge Cases

For the expression `1+1`, the algorithm correctly finds `+` at index 1, parses `a=1` and `b=1`, and outputs 2. For `999/3`, it identifies `/` at index 3, parses `a=999` and `b=3`, performs integer division with `//`, yielding 333. For `100%3`, it identifies `%` and outputs 1. In each case, slicing and operator detection are robust, and the algorithm produces correct results without special handling because the input is guaranteed to match the expected format.
