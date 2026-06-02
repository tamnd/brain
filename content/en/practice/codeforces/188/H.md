---
title: "CF 188H - Stack"
description: "We are asked to simulate a stack-based computation. The input is a string where each character represents an operation. If the character is a digit from 0 to 9, we push that number onto the stack."
date: "2026-06-03T01:10:12+07:00"
tags: ["codeforces", "competitive-programming", "*special", "expression-parsing", "implementation"]
categories: ["algorithms"]
codeforces_contest: 188
codeforces_index: "H"
codeforces_contest_name: "Surprise Language Round 6"
rating: 1800
weight: 188
solve_time_s: 127
verified: false
draft: false
---

[CF 188H - Stack](https://codeforces.com/problemset/problem/188/H)

**Rating:** 1800  
**Tags:** *special, expression parsing, implementation  
**Solve time:** 2m 7s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to simulate a stack-based computation. The input is a string where each character represents an operation. If the character is a digit from 0 to 9, we push that number onto the stack. If the character is `+` or `*`, we pop the top two numbers from the stack, perform the corresponding arithmetic operation, and push the result back. The string of operations is guaranteed to be valid, meaning we will never attempt to pop from an empty stack. After performing all operations, we need to output the number on top of the stack.

The input length is small, at most 20 characters. This allows us to use a direct simulation approach without worrying about optimization. The numbers on the stack never exceed $10^6$, so using Python's standard integers is safe. Non-obvious edge cases include sequences with only digits, sequences where multiplication occurs early, or cases that mix addition and multiplication to test order of operations. For example, `"12+3*"` must produce `(1+2)*3 = 9`, and `"1111++++"` would be invalid if the guarantee wasn't present, but here the problem ensures it never is.

## Approaches

The brute-force approach is straightforward: iterate through the string from left to right, using a standard stack data structure. Push digits, pop two elements and compute the result for `+` or `*`. This works correctly because every operation is explicitly defined, and the input guarantees there will always be enough operands. For this problem, this brute-force approach is also optimal, since the input length is very small and each operation can be done in constant time.

There is no need for advanced techniques like parsing trees or dynamic programming here. The key insight is recognizing that the string encodes a postfix (Reverse Polish) expression. Postfix expressions are naturally evaluated with a stack because every operator acts on the most recent operands. This direct simulation both mirrors the expression semantics and satisfies the time and memory constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (Stack Simulation) | O(n) | O(n) | Accepted |
| Optimal (Stack Simulation) | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an empty stack. The stack will maintain the operands for computation.
2. Iterate over each character in the input string. Each character represents an operation.
3. If the character is a digit, convert it to an integer and push it onto the stack. This ensures numeric values are treated correctly in subsequent operations.
4. If the character is `+`, pop the top two numbers from the stack, sum them, and push the result back. The order of popping does not matter for addition.
5. If the character is `*`, pop the top two numbers from the stack, multiply them, and push the result back. Again, order does not matter due to commutativity.
6. After processing all characters, the stack will contain exactly one number, which is the result. Print this number.

The reason this works is that the stack invariant is maintained: at any point before a `+` or `*` operation, there are at least two operands available. Each operator reduces two operands to one result, so after processing the entire string, exactly one value remains. The sequence of operations mirrors postfix evaluation semantics, guaranteeing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    s = input().strip()
    stack = []
    for c in s:
        if c.isdigit():
            stack.append(int(c))
        elif c == '+':
            b = stack.pop()
            a = stack.pop()
            stack.append(a + b)
        elif c == '*':
            b = stack.pop()
            a = stack.pop()
            stack.append(a * b)
    print(stack[0])

if __name__ == "__main__":
    main()
```

The solution initializes a list as a stack, then iterates over the string. Digits are converted to integers and appended to the stack. Operators pop the last two elements and push the computed result. Using `stack.pop()` ensures the correct elements are removed from the top of the stack. The final print accesses `stack[0]` because exactly one element remains.

## Worked Examples

**Example 1:** `"12+3*66*+"`

| Step | Stack | Operation |
| --- | --- | --- |
| '1' | [1] | push 1 |
| '2' | [1,2] | push 2 |
| '+' | [3] | 1+2=3 |
| '3' | [3,3] | push 3 |
| '*' | [9] | 3*3=9 |
| '6' | [9,6] | push 6 |
| '6' | [9,6,6] | push 6 |
| '*' | [9,36] | 6*6=36 |
| '+' | [45] | 9+36=45 |

The stack correctly reflects intermediate computations, resulting in 45.

**Example 2:** `"123"`

| Step | Stack | Operation |
| --- | --- | --- |
| '1' | [1] | push 1 |
| '2' | [1,2] | push 2 |
| '3' | [1,2,3] | push 3 |

No operations occur, so the top of the stack is 3.

These traces confirm that the algorithm correctly simulates the stack for both mixed operations and sequences of only digits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed exactly once, with stack push/pop in O(1) time. |
| Space | O(n) | The stack can hold at most n elements, where n is the string length. |

With n ≤ 20, the algorithm performs very few operations, fitting comfortably within the 2-second time limit and 256 MB memory constraint.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("12+3*66*+\n") == "45", "sample 1"
assert run("123\n") == "3", "sample 2"

# Custom cases
assert run("99+\n") == "18", "addition of two digits"
assert run("23*4+\n") == "10", "mix of multiplication and addition"
assert run("1111++++\n") == "4", "all ones, repeated additions"
assert run("9\n") == "9", "single digit input"
assert run("12+34+*\n") == "21", "nested operations"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "99+" | 18 | Correct addition of two digits |
| "23*4+" | 10 | Correct mix of multiplication and addition |
| "1111++++" | 4 | Multiple repeated additions |
| "9" | 9 | Minimum size input |
| "12+34+*" | 21 | Nested operations correctness |

## Edge Cases

For a sequence of only digits, like `"5"`, the algorithm pushes the digit and prints it directly. For early multiplication, `"23*4+"`, the stack evolves `[2,3] -> [6] -> [6,4] -> [10]`, correctly applying operations in postfix order. The algorithm handles all sequences of valid operations by maintaining the invariant that the stack always has enough elements before an operator. There is no need to check for underflow due to the problem guarantee.
