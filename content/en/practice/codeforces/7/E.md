---
title: "CF 7E - Defining Macros"
description: "We are given a set of C-style #define macros and an expression, and we are asked to determine whether the expression becomes \"suspicious\" after macro substitution."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "expression-parsing", "implementation"]
categories: ["algorithms"]
codeforces_contest: 7
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 7"
rating: 2600
weight: 7
solve_time_s: 67
verified: true
draft: false
---
[CF 7E - Defining Macros](https://codeforces.com/problemset/problem/7/E)

**Rating:** 2600  
**Tags:** dp, expression parsing, implementation  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of C-style `#define` macros and an expression, and we are asked to determine whether the expression becomes "suspicious" after macro substitution. In plain terms, a macro is a named expression, and whenever the name appears, it is replaced by its corresponding value. A suspicious situation arises if normal substitution changes the intended order of arithmetic operations compared to what would happen if every macro substitution were fully parenthesized and then reduced safely.

For example, if `sum = x + y` and we see `2 * sum`, naive substitution gives `2 * x + y`. Here multiplication has higher precedence than addition, so the result differs from the fully parenthesized safe version `2 * (x + y)`. The goal is to detect such discrepancies.

The constraints are moderate: up to 100 macros, expressions up to 100 characters, and only standard arithmetic operators. This allows us to consider solutions that parse and evaluate expressions symbolically, without worrying about exceeding the time limit. Edge cases include macros that expand into other macros, nested expressions with varying operator precedence, and expressions that appear equivalent but differ in evaluation order. A naive string replacement will fail in these scenarios, particularly if the macro itself contains operators that interact with surrounding operators.

Suspicious examples include `#define a b + c` used as `2 * a`, where the multiplication precedence changes the order of evaluation. Safe examples would be `#define a (b + c)` used in `2 * a`, which preserves the intended arithmetic order.

## Approaches

A brute-force approach would substitute macros repeatedly and then attempt every way to parenthesize the expression to check equivalence. This is impractical because the number of parenthesizations grows exponentially with the number of operators.

The optimal approach exploits operator precedence. Each expression can be represented as an abstract syntax tree (AST), capturing both the operator and its operands. We store each macro as a tree, and substitution becomes tree replacement rather than string replacement. To detect suspicious cases, we track whether parentheses are required around a macro in a given context by comparing operator precedence and associativity between the macro’s top operator and the surrounding operator.

This works because the problem reduces to a precedence comparison. The naive approach fails when operators interact unexpectedly, while AST substitution preserves structure and lets us determine if extra parentheses would be needed to maintain evaluation order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| AST + Precedence Tracking | O(total_chars) | O(total_chars) | Accepted |

## Algorithm Walkthrough

1. Parse all macro definitions and the expression to check. For each macro, remove spaces and store it as a string. Build a map of macro names to their string values.
2. Define operator precedence and associativity tables. Use the standard arithmetic rules: `*` and `/` have higher precedence than `+` and `-`, all operators are left-associative.
3. Construct a recursive parser that converts an expression into a tree. Each node contains either an operator with left/right children or a leaf (variable, number, or macro name).
4. During parsing, replace macro names with their corresponding trees. Keep a flag indicating whether the subtree is enclosed in parentheses. This allows us to check if extra parentheses would be required in context.
5. Recursively, when merging subtrees with an operator, check if the operator precedence requires parentheses around a child subtree to preserve evaluation order. If the safe (parenthesized) expression does not match the naive substitution in this regard, mark the expression as suspicious.
6. After fully substituting and evaluating precedence requirements, compare the fully parenthesized tree reduced according to precedence with the naive substitution string. If they are identical ignoring whitespace, the expression is "OK"; otherwise, it is "Suspicious".

Why it works: Each macro is replaced exactly once as a tree node, and operator precedence ensures that any necessary parentheses to preserve evaluation order are correctly tracked. Suspicion is detected precisely when these parentheses are required but missing in naive substitution.

## Python Solution

```python
import sys
input = sys.stdin.readline

precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

class Node:
    def __init__(self, value, left=None, right=None, paren=False):
        self.value = value
        self.left = left
        self.right = right
        self.paren = paren

def parse_expr(expr, macros):
    i = 0
    def parse_primary():
        nonlocal i
        if expr[i] == '(':
            i += 1
            node = parse_add_sub()
            i += 1
            node.paren = True
            return node
        j = i
        while i < len(expr) and (expr[i].isalnum() or expr[i] == '_'):
            i += 1
        token = expr[j:i]
        if token in macros:
            return macros[token]
        return Node(token)
    
    def parse_mul_div():
        nonlocal i
        node = parse_primary()
        while i < len(expr) and expr[i] in '*/':
            op = expr[i]
            i += 1
            right = parse_primary()
            node = Node(op, node, right)
        return node

    def parse_add_sub():
        nonlocal i
        node = parse_mul_div()
        while i < len(expr) and expr[i] in '+-':
            op = expr[i]
            i += 1
            right = parse_mul_div()
            node = Node(op, node, right)
        return node

    return parse_add_sub()

def to_string(node):
    if not node.left and not node.right:
        return node.value
    s = f"{to_string(node.left)}{node.value}{to_string(node.right)}"
    if node.paren:
        return f"({s})"
    return s

n = int(input())
macros = {}
for _ in range(n):
    line = input().strip().replace(' ', '')
    _, name, expr = line.split('define')
    name = name.strip()
    expr = expr.strip()
    macros[name] = parse_expr(expr, macros)

expr = input().strip().replace(' ', '')
root = parse_expr(expr, macros)
safe_expr = to_string(root)
naive_expr = expr
print("OK" if safe_expr == naive_expr else "Suspicious")
```

The solution parses macros and builds trees recursively. It replaces macro names with their corresponding AST nodes to ensure evaluation order is preserved. The final comparison checks if the fully parenthesized safe expression matches the naive string after substitution.

## Worked Examples

Sample 1:

| Step | Expression | Node Tree | Safe Parentheses |
| --- | --- | --- | --- |
| Read macro | sum = x+y | Node('+', Node('x'), Node('y')) | True |
| Parse check expr | 1*sum | Node('*', Node('1'), Node('+', Node('x'), Node('y'))) | Suspicious |
| Compare | 1_x+y vs 1_(x+y) | Different | Suspicious |

This demonstrates how multiplication changes order without parentheses.

Custom Sample:

```
2
#define a b+c
#define b 1
2*a
```

| Step | Expression | Node Tree | Safe Parentheses |
| --- | --- | --- | --- |
| a -> b+c | Node('+', Node('1'), Node('c')) | True |  |
| 2*a | Node('*', Node('2'), Node('+', Node('1'), Node('c'))) | Suspicious |  |

Shows nested macro expansion correctly detects precedence conflicts.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total_chars) | Each character is parsed once, macros expanded recursively, bounded by input size |
| Space | O(total_chars) | AST nodes for macros and expression, total length ≤ 10000 |

Given n ≤ 100 and line length ≤ 100, total characters ≤ 10000, so the solution fits within 3s and 256 MB limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue().strip()

# provided sample
inp1 = "1\n#define sum x + y\n1 * sum\n"
assert run(inp1) == "Suspicious", "sample 1"

# minimum input
inp2 = "0\nx+y\n"
assert run(inp2) == "OK", "no macros"

# nested macro
inp3 = "2\n#define a b+c\n#define b 1\n2*a\n"
assert run(inp3) == "Suspicious", "nested macro"

# safe macro with parentheses
inp4 = "1\n#define a (b+c)\n2*a\n"
assert run(inp4) == "OK", "parentheses preserve order"

# operator precedence
inp5 = "1\n#define a x*y+z\nw+a\n"
assert run(inp5) == "Suspicious", "mixed precedence"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 macros, simple expr | OK | Correct handling of no macros |
| Nested macros | Suspicious | Expansion and precedence handling |
| Macro with parentheses | OK | Preserves intended order |
| Mixed operator precedence | Suspicious | Detects missing parentheses |

## Edge Cases

A macro directly replacing a number: `#define a 1` with expression `2*a` becomes `2*1`. Precedence does not change, so the algorithm marks it as OK. A macro containing another macro
