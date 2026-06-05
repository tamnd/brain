---
title: "CF 282A - Bit++"
description: "The problem presents a toy programming language with only one variable, x, initially set to zero. Each line of the program is a statement that either increments or decrements this variable."
date: "2026-06-05T09:29:28+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 282
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 173 (Div. 2)"
rating: 800
weight: 282
solve_time_s: 76
verified: true
draft: false
---

[CF 282A - Bit++](https://codeforces.com/problemset/problem/282/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem presents a toy programming language with only one variable, _x_, initially set to zero. Each line of the program is a statement that either increments or decrements this variable. The operation can appear before or after the variable, so the statement could be `++X`, `X++`, `--X`, or `X--`. Our task is to determine the final value of _x_ after executing all statements in order.

The input starts with the number of statements `n`, followed by `n` lines, each a valid statement. The output is a single integer representing the final value of _x_.

Given the constraints, `n` is at most 150, which is extremely small for modern computers. This means even a naive approach that examines every statement individually will run instantly. There are no concerns about large input sizes, integer overflows, or performance optimizations.

A non-obvious edge case arises from the order of symbols. Since the operation can appear before or after `X`, a naive check for `statement == "++X"` or `statement == "X++"` might miss a decrement operation like `X--`. We must detect increment and decrement by checking for the presence of `++` or `--` anywhere in the statement, not just by position. For example, the input:

```
3
++X
X--
--X
```

should result in a final value of `0`, because the first increments, the second decrements, and the third decrements again.

## Approaches

The brute-force approach is straightforward. Initialize a counter `x` to zero. For each statement, examine the string. If it contains `++`, increment `x`; if it contains `--`, decrement `x`. This works because every statement contains exactly one operation and one variable. Since each statement is examined individually and we perform only a constant-time string search per statement, the total operation count is proportional to `n`. For `n = 150`, this is trivial.

There is no meaningful "faster" algorithm here because the brute-force method already runs in linear time relative to the number of statements. The key insight is that we do not need to parse the statement positionally or tokenize it; the presence of the two-character operator `++` or `--` is sufficient. This observation simplifies the implementation and eliminates edge cases related to the order of characters.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a variable `x` to zero. This represents the current value of the only variable in the program.
2. Read the number of statements, `n`.
3. For each statement in the program, check whether it contains the substring `++`. If it does, increment `x`.
4. If the statement contains `--`, decrement `x`.
5. After processing all statements, print the value of `x`.

Why it works: The algorithm maintains the invariant that `x` always reflects the net effect of all statements processed so far. Each statement modifies `x` by exactly one, either up or down, and every statement is guaranteed to contain exactly one operation. Therefore, by scanning sequentially and updating `x` according to the operation detected, the final value is guaranteed to be correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
x = 0

for _ in range(n):
    statement = input().strip()
    if "++" in statement:
        x += 1
    elif "--" in statement:
        x -= 1

print(x)
```

The solution first reads the number of statements and initializes `x`. For each statement, it removes any trailing newline or spaces and checks for the presence of the increment or decrement operator. We use `in` rather than a positional check because the operator may appear before or after `X`. This ensures correctness for all permutations like `++X` or `X++`. Finally, the result is printed.

## Worked Examples

Trace through the sample input:

```
1
++X
```

| Step | Statement | x before | x after |
| --- | --- | --- | --- |
| 1 | ++X | 0 | 1 |

This confirms that a single increment works correctly.

Another example:

```
3
++X
X--
--X
```

| Step | Statement | x before | x after |
| --- | --- | --- | --- |
| 1 | ++X | 0 | 1 |
| 2 | X-- | 1 | 0 |
| 3 | --X | 0 | -1 |

This demonstrates handling a mix of increments and decrements in any order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each statement is checked exactly once, with a fixed-length substring search. |
| Space | O(1) | Only a single integer `x` is stored; no additional data structures are needed. |

Given `n <= 150`, the solution runs in negligible time and uses minimal memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    x = 0
    for _ in range(n):
        statement = input().strip()
        if "++" in statement:
            x += 1
        elif "--" in statement:
            x -= 1
    return str(x)

# provided samples
assert run("1\n++X\n") == "1", "sample 1"

# custom cases
assert run("3\n++X\nX--\n--X\n") == "-1", "mixed increments and decrements"
assert run("5\n++X\nX++\n++X\nX++\n++X\n") == "5", "all increments"
assert run("4\n--X\nX--\n--X\nX--\n") == "-4", "all decrements"
assert run("1\nX--\n") == "-1", "single decrement"
assert run("2\nX++\n--X\n") == "0", "increment followed by decrement"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 increments and decrements mixed | -1 | Correctly handles multiple operations in different orders |
| 5 increments all | 5 | Correctly handles all increments |
| 4 decrements all | -4 | Correctly handles all decrements |
| Single decrement | -1 | Minimal input handling |
| Increment then decrement | 0 | Operations cancel out correctly |

## Edge Cases

The main edge case is the order of symbols in the statement. For example, `X++` should be treated exactly the same as `++X`. Our algorithm handles this because it checks for the substring `++` or `--` anywhere in the statement.

Input:

```
2
X++
--X
```

Execution trace:

| Step | Statement | x before | x after |
| --- | --- | --- | --- |
| 1 | X++ | 0 | 1 |
| 2 | --X | 1 | 0 |

Output is `0`, confirming the algorithm correctly interprets operator positions. This ensures no off-by-one errors due to the position of the operator relative to the variable.
