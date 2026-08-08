---
title: "CF 102461A - Expression Formatting"
description: "The input is a valid arithmetic expression written without spaces. Its operands are single lowercase letters, and the expression may contain the binary operators +, -, , / together with parentheses."
date: "2026-08-09T03:06:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102461
codeforces_index: "A"
codeforces_contest_name: "Innopolis Open 2019-2020, qualification, contest 2"
rating: 0
weight: 102461
solve_time_s: 129
verified: true
draft: false
---

[CF 102461A - Expression Formatting](https://codeforces.com/problemset/problem/102461/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

The input is a valid arithmetic expression written without spaces. Its operands are single lowercase letters, and the expression may contain the binary operators `+`, `-`, `*`, `/` together with parentheses. The task is purely cosmetic: preserve the expression exactly as it is, but put one space immediately before and immediately after every arithmetic operator.

For example, `a+b*(c-d)` becomes `a + b * (c - d)`. Parentheses themselves are not changed, and no spaces are added around them.

The expression has at most 200 characters, so even a quadratic algorithm performs only a small number of operations for the official constraints. There is no need for parsing, operator precedence handling, or evaluation of the expression. The input is already guaranteed to be syntactically correct, which means every `+`, `-`, `*`, and `/` that we encounter is an operator that needs formatting.

A linear scan is the natural solution because every character needs to be inspected once. With at most 200 characters, this is comfortably inside the one second limit and uses negligible memory. Even an `O(n^2)` construction would pass these particular constraints, but there is no reason to use it when the required transformation can be performed directly in `O(n)`.

The first edge case is an expression containing no operator. For input `a`, the correct output is `a`. A careless implementation that always inserts spaces at the ends of the expression would produce something such as `a`, which changes characters that were not supposed to be modified.

The second edge case is an operator next to parentheses. For input `(a)/(b)`, the correct output is `(a) / (b)`. The spaces belong around `/`, not around `(` or `)`. An implementation that treats every non-letter character as something requiring surrounding spaces would incorrectly modify the parentheses.

The third edge case is a deeply nested expression. For input `((a))-b+(c*(d))`, the correct output is `((a)) - b + (c * (d))`. Parentheses can appear immediately before or after operators, so the implementation must decide based on the character itself rather than its position in the expression.

The fourth edge case is several operators separated by single-letter variables. For input `a+b+c+d`, the correct output is `a + b + c + d`. A solution that only handles the first operator, or that inserts spaces into the original string while moving an index forward without accounting for the inserted characters, can skip later operators.

## Approaches

A straightforward brute-force solution can repeatedly search for an operator and construct a new string with spaces around it. If the current expression has length `m`, inserting spaces by rebuilding the whole string can copy `O(m)` characters. If there are `k` operators, the lengths increase after every insertion, so the total work is `O(nk)`, which is `O(n^2)` in the worst case. For an expression of the maximum practical length here, around 200 characters, this is only on the order of tens of thousands of character operations, so this approach is actually fast enough for the given constraints.

The brute-force approach works because every operator can be handled independently. Its weakness is not correctness but unnecessary repeated work. After processing one operator, it may copy many characters that were already processed just to reach the next operator.

The key observation is that the desired output depends only on the current input character. If the character is one of `+`, `-`, `*`, or `/`, we append a space, then the operator, then another space. Every other character is copied unchanged. There is no interaction between different operators, and inserting spaces does not change how any later input character should be interpreted.

This lets us process the original expression from left to right exactly once. We never modify the input string and never need to adjust an index because of inserted spaces. The result is built separately, so each input character is handled in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n^2)` | `O(n)` | Accepted for `n <= 200` |
| Optimal | `O(n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Read the complete expression as a string. Since the statement guarantees that the input contains no spaces, reading one line is sufficient.
2. Create an empty list that will store pieces of the final expression. A list is convenient because appending to it is constant time, and joining it once at the end avoids repeatedly creating new immutable Python strings.
3. Scan the input from the first character to the last character. For every character, check whether it is one of the four arithmetic operators.
4. If the character is an operator, append three pieces to the result: a space, the operator itself, and another space. This directly implements the required formatting rule.
5. If the character is not an operator, append it unchanged. In particular, parentheses and variables must remain exactly where they are.
6. Join all result pieces into one string and print it. Since the input contains no existing spaces, this creates exactly one space on each side of every operator and nowhere else.

### Why it works

After processing any prefix of the input, the result list contains exactly the correctly formatted version of that prefix. A variable or parenthesis is copied unchanged, while every arithmetic operator is replaced by the operator surrounded by exactly one space. Processing the next character preserves this property, so by induction the entire expression is correctly formatted when the scan finishes. Because every decision is based only on the current input character, no operator can be skipped or processed twice.

## Python Solution

```python
import sys
input = sys.stdin.readline

def format_expression(s):
    operators = {"+", "-", "*", "/"}
    result = []

    for ch in s:
        if ch in operators:
            result.append(" ")
            result.append(ch)
            result.append(" ")
        else:
            result.append(ch)

    return "".join(result)

def main():
    s = input().strip()
    print(format_expression(s))

if __name__ == "__main__":
    main()
```

The `operators` set contains exactly the four characters that require formatting. Checking membership in this set takes constant time for each input character.

The `result` list represents the output under construction. When an operator is found, the code appends three separate strings instead of modifying the input string. This is a useful implementation detail in Python because strings are immutable, so repeatedly inserting into a string could require copying a large portion of it each time.

The loop processes the original input, not the growing output. That distinction eliminates the most common indexing mistake in this problem. If we inserted spaces into the string being scanned, the current position would shift after every operator. Here, the input never changes, so the loop index always refers to the correct original character.

The final `"".join(result)` performs one construction of the output string. There is no integer arithmetic, so integer overflow is irrelevant, and the input length is so small that standard Python I/O is more than sufficient.

## Worked Examples

### Sample 1

For the input `a+b`, the scan behaves as follows.

| Step | Input character | Action | Result pieces |
| --- | --- | --- | --- |
| 1 | `a` | Copy unchanged | `a` |
| 2 | `+` | Add space, `+`, space | `a`, ` `, `+`, ` ` |
| 3 | `b` | Copy unchanged | `a`, ` `, `+`, ` `, `b` |

Joining the pieces gives `a + b`. The trace demonstrates the core invariant: ordinary characters are copied exactly, while the operator contributes precisely the two required spaces.

### Sample 2

For the input `((a))-b+(c*(d))`, the scan is longer but follows exactly the same rule.

| Step | Input character | Action | Result prefix |
| --- | --- | --- | --- |
| 1 | `(` | Copy unchanged | `(` |
| 2 | `(` | Copy unchanged | `((` |
| 3 | `a` | Copy unchanged | `((a` |
| 4 | `)` | Copy unchanged | `((a)` |
| 5 | `)` | Copy unchanged | `((a))` |
| 6 | `-` | Add spaces around operator | `((a)) - ` |
| 7 | `b` | Copy unchanged | `((a)) - b` |
| 8 | `+` | Add spaces around operator | `((a)) - b + ` |
| 9 | `(` | Copy unchanged | `((a)) - b + (` |
| 10 | `c` | Copy unchanged | `((a)) - b + (c` |
| 11 | `*` | Add spaces around operator | `((a)) - b + (c * ` |
| 12 | `(` | Copy unchanged | `((a)) - b + (c * (` |
| 13 | `d` | Copy unchanged | `((a)) - b + (c * (d` |
| 14 | `)` | Copy unchanged | `((a)) - b + (c * (d)` |
| 15 | `)` | Copy unchanged | `((a)) - b + (c * (d))` |

The final output is `((a)) - b + (c * (d))`. This example specifically confirms that parentheses are never modified, even when they are adjacent to an operator.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n)` | Every input character is inspected once and contributes a constant amount of work. |
| Space | `O(n)` | The result contains the original characters plus at most two spaces per operator. |

Here `n` is the length of the input expression, with `n <= 200`. A single linear pass is far below the available time limit, and the output itself is only `O(n)` characters, so the memory usage is also negligible compared with the 512 MB limit.

## Test Cases

```python
import sys
import io

def format_expression(s):
    operators = {"+", "-", "*", "/"}
    result = []

    for ch in s:
        if ch in operators:
            result.append(" ")
            result.append(ch)
            result.append(" ")
        else:
            result.append(ch)

    return "".join(result)

def run(inp: str) -> str:
    return format_expression(inp.strip())

# Provided samples
assert run("a+b") == "a + b", "sample 1"
assert run("((a))-b+(c*(d))") == "((a)) - b + (c * (d))", "sample 2"
assert run("(a)/(b-b)+((d)+((c)))") == "(a) / (b - b) + ((d) + ((c)))", "sample 3"

# Minimum-size input: a single variable, no operators.
assert run("a") == "a", "single variable"

# All variables are equal and many operators occur.
assert run("a+a+a+a+a") == "a + a + a + a + a", "repeated equal variables"

# Every supported operator occurs.
assert run("a-b*c/d+e") == "a - b * c / d + e", "all operators"

# Operators adjacent to parentheses.
assert run("(a)/(b)+(c)*(d)") == "(a) / (b) + (c) * (d)", "parentheses boundaries"

# Maximum-length valid expression for this grammar.
# 100 variables and 99 plus operators give length 199.
max_expr = "+".join(["a"] * 100)
expected_max = " + ".join(["a"] * 100)
assert len(max_expr) == 199
assert run(max_expr) == expected_max, "maximum length"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `a` | Minimum-size input and the absence of operators |
| `a+a+a+a+a` | `a + a + a + a + a` | Repeated operators and equal operands |
| `a-b*c/d+e` | `a - b * c / d + e` | All four supported operators |
| `(a)/(b)+(c)*(d)` | `(a) / (b) + (c) * (d)` | Operators next to parentheses |
| 100 `a` variables joined by `+` | The same expression with spaces around every `+` | Maximum input length and repeated processing |

## Edge Cases

For the expression `a`, the algorithm sees only one character. Since `a` is not in the operator set, it is copied directly into the result. The final output is `a`, so the solution does not introduce unwanted spaces when no formatting is necessary.

For `(a)/(b)`, the first three characters are `(`, `a`, and `)`, all of which are copied unchanged. When `/` is reached, the algorithm appends `/` as one logical operation. The remaining characters are copied unchanged, producing `(a) / (b)`. This handles the boundary between an operator and parentheses without treating the parentheses themselves as operators.

For `((a))-b+(c*(d))`, every opening and closing parenthesis is copied exactly as it appears. When `-`, `+`, and `*` are encountered, each one receives one space on both sides. The result is `((a)) - b + (c * (d))`. The nested structure has no effect on the algorithm because the task does not require parsing the expression.

For `a+a+a+a+a`, each `+` is processed independently. After the first operator the result contains `a + `, after the second it contains `a + a + `, and so on. The final output is `a + a + a + a + a`. This confirms that the scan continues over every original character and never loses its position because of the spaces added to the separate result.

For the maximum-length expression consisting of 100 `a` variables joined by 99 `+` operators, the scan performs one constant-time decision for each of the 199 input characters. Every one of the 99 operators produces exactly two spaces, so the output has 397 characters. The algorithm remains linear in the input size and handles the largest valid expression comfortably.
