---
title: "CF 188H - Stack"
description: "The input is a string that describes operations on a stack. Each digit means \"push this number onto the stack\". Each + or means \"take the top two values from the stack, apply the operation, and push the result back\"."
date: "2026-06-04T23:20:43+07:00"
tags: ["codeforces", "competitive-programming", "*special", "expression-parsing", "implementation"]
categories: ["algorithms"]
codeforces_contest: 188
codeforces_index: "H"
codeforces_contest_name: "Surprise Language Round 6"
rating: 1800
weight: 188
solve_time_s: 101
verified: true
draft: false
---

[CF 188H - Stack](https://codeforces.com/problemset/problem/188/H)

**Rating:** 1800  
**Tags:** *special, expression parsing, implementation  
**Solve time:** 1m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

The input is a string that describes operations on a stack. Each digit means "push this number onto the stack". Each `+` or `*` means "take the top two values from the stack, apply the operation, and push the result back".

This is essentially evaluating an expression written in Reverse Polish Notation (postfix notation). The stack stores intermediate results. Whenever we encounter an operator, the two most recently available values become its operands.

For example, the string:

```
12+3*
```

means:

```
push 1
push 2
add -> 3
push 3
multiply -> 9
```

The final answer is the value remaining at the top of the stack after all operations have been processed.

The constraints are extremely small. The operation string has length at most 20, so even very inefficient approaches would run instantly. A direct simulation performs one stack operation per character, which is only a few dozen operations in the worst case.

The main challenge is not performance but correctly implementing the stack behavior.

One easy mistake is using operands in the wrong order. For addition and multiplication this does not affect the result because both operations are commutative, but in a more general postfix evaluator it would matter. A correct implementation should still pop the second operand first and the first operand second.

Consider:

```
12+
```

The stack before `+` is:

```
[1, 2]
```

The operator uses operands `1` and `2`, producing `3`.

Another edge case occurs when the input contains only digits and no operators.

Input:

```
123
```

The stack evolves as:

```
[1]
[1, 2]
[1, 2, 3]
```

The answer is the top element, `3`. A solution that assumes the stack always ends with exactly one value would fail here.

A third edge case is a single-character input.

Input:

```
7
```

Output:

```
7
```

The algorithm must correctly handle a stack containing exactly one element from start to finish.

## Approaches

The most direct idea is to simulate the process exactly as described. Maintain a stack. When a digit appears, push its numeric value. When an operator appears, pop two values, apply the operation, and push the result.

Because every operation described by the input corresponds to a constant amount of work, the total running time is proportional to the length of the string.

One could also think about reconstructing the mathematical expression represented by the postfix notation and then evaluating it afterward. That works, but it introduces unnecessary complexity. We would need to build an expression tree or convert the notation into another form before evaluation.

The key observation is that the problem already tells us how the computation should be performed. The stack is not merely an implementation detail, it is the actual evaluation mechanism. Following the operations literally gives the answer immediately.

Since the input length is at most 20, both approaches are fast enough. The direct simulation is simpler and matches the problem statement exactly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force stack simulation | O(n) | O(n) | Accepted |
| Optimal stack simulation | O(n) | O(n) | Accepted |

For this problem, the natural simulation is already optimal.

## Algorithm Walkthrough

1. Create an empty stack.
2. Process the input string from left to right.
3. If the current character is a digit, convert it to an integer and push it onto the stack.
4. If the current character is `+`, pop the top two values from the stack, add them, and push the result back.

The stack always contains enough values because the input is guaranteed to be valid.
5. If the current character is `*`, pop the top two values from the stack, multiply them, and push the result back.
6. After all characters have been processed, output the top element of the stack.

### Why it works

After processing any prefix of the input, the stack contains exactly the values that would exist in the real stack described by the problem statement. Digits add new values, while operators consume the top two values and replace them with the operation result. Since every step reproduces the required stack behavior exactly, the final stack state is identical to the intended execution. The top element at the end is therefore the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()

    stack = []

    for ch in s:
        if ch.isdigit():
            stack.append(int(ch))
        elif ch == '+':
            b = stack.pop()
            a = stack.pop()
            stack.append(a + b)
        else:  # '*'
            b = stack.pop()
            a = stack.pop()
            stack.append(a * b)

    print(stack[-1])

if __name__ == "__main__":
    solve()
```

The implementation follows the simulation directly.

The stack is represented by a Python list. Appending corresponds to a push operation, and `pop()` removes the current top element.

When an operator is encountered, the code removes two elements. The first pop gives the second operand and the second pop gives the first operand. Although addition and multiplication are commutative, preserving the correct operand order is good practice and makes the implementation consistent with postfix evaluation in general.

At the end, the problem asks for the topmost stack element. That value is stored at `stack[-1]`.

## Worked Examples

### Example 1

Input:

```
12+3*66*+
```

| Character | Action | Stack After Action |
| --- | --- | --- |
| 1 | push 1 | [1] |
| 2 | push 2 | [1, 2] |
| + | 1 + 2 = 3 | [3] |
| 3 | push 3 | [3, 3] |
| * | 3 * 3 = 9 | [9] |
| 6 | push 6 | [9, 6] |
| 6 | push 6 | [9, 6, 6] |
| * | 6 * 6 = 36 | [9, 36] |
| + | 9 + 36 = 45 | [45] |

Output:

```
45
```

This trace shows how intermediate results replace their operands on the stack. Every operator reduces the stack size by one while preserving the value of the evaluated subexpression.

### Example 2

Input:

```
123
```

| Character | Action | Stack After Action |
| --- | --- | --- |
| 1 | push 1 | [1] |
| 2 | push 2 | [1, 2] |
| 3 | push 3 | [1, 2, 3] |

Output:

```
3
```

This example demonstrates that the final stack is not required to contain exactly one value. The problem only asks for the topmost element, which is `3`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once |
| Space | O(n) | In the worst case all characters are digits and remain on the stack |

Here `n` is the length of the operation string. Since `n ≤ 20`, the running time is effectively instantaneous and the memory usage is negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    s = input().strip()
    stack = []

    for ch in s:
        if ch.isdigit():
            stack.append(int(ch))
        elif ch == '+':
            b = stack.pop()
            a = stack.pop()
            stack.append(a + b)
        else:
            b = stack.pop()
            a = stack.pop()
            stack.append(a * b)

    return str(stack[-1])

# provided sample
assert run("12+3*66*+\n") == "45", "sample 1"

# custom cases
assert run("7\n") == "7", "single digit"
assert run("12+\n") == "3", "single operation"
assert run("123\n") == "3", "no operators"
assert run("99*\n") == "81", "multiplication only"
assert run("11111111111111111111\n") == "1", "maximum length, all digits"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `7` | `7` | Minimum valid input |
| `12+` | `3` | Basic operator handling |
| `123` | `3` | No operators present |
| `99*` | `81` | Multiplication path |
| `11111111111111111111` | `1` | Maximum length with only pushes |

## Edge Cases

Consider the input:

```
123
```

Execution:

```
push 1 -> [1]
push 2 -> [1, 2]
push 3 -> [1, 2, 3]
```

The algorithm outputs the top element, `3`. It does not incorrectly assume that exactly one element must remain on the stack.

Consider the input:

```
7
```

Execution:

```
push 7 -> [7]
```

No operators are processed. The final top element is `7`, which is printed directly.

Consider the input:

```
12+
```

Execution:

```
push 1 -> [1]
push 2 -> [1, 2]
+ -> [3]
```

The operator consumes the two most recent values and pushes their sum. The resulting stack contains a single value, `3`, which becomes the answer.

These cases cover the situations most likely to expose incorrect assumptions about stack size or operator handling, and the simulation handles all of them naturally.
