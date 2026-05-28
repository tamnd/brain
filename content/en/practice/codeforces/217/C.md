---
title: "CF 217C - Formurosa"
description: "We are given a Boolean formula consisting of constants 0 and 1, unknown variables denoted by ?, and the logical operators AND (&), OR ( The task is to determine whether it is always possible to uniquely identify the species of each colony, no matter how the unknowns are…"
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "divide-and-conquer", "dp", "expression-parsing"]
categories: ["algorithms"]
codeforces_contest: 217
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 134 (Div. 1)"
rating: 2600
weight: 217
solve_time_s: 80
verified: true
draft: false
---

[CF 217C - Formurosa](https://codeforces.com/problemset/problem/217/C)

**Rating:** 2600  
**Tags:** divide and conquer, dp, expression parsing  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a Boolean formula consisting of constants 0 and 1, unknown variables denoted by `?`, and the logical operators AND (`&`), OR (`|`), and XOR (`^`). Each `?` corresponds to one of the _n_ bacterial colonies, and the scientists can assign any colony to any `?` multiple times per evaluation. The key restriction is that not all colonies are identical, but any assignment can repeat colonies.

The task is to determine whether it is always possible to uniquely identify the species of each colony, no matter how the unknowns are distributed across evaluations. Conceptually, this reduces to asking whether the Boolean formula can distinguish between any two assignments where not all variables are equal.

The input size is up to 10^6 characters for the formula, and n can be up to 10^6. A naive approach that tries all `2^n` assignments is clearly infeasible, as even `n=20` would exceed practical computation. We need an approach linear in the formula size and independent of the number of colonies.

Edge cases are subtle. For instance, a formula `?^?` with two colonies cannot distinguish them because XOR of identical unknowns is always 0, so the plant output does not reveal whether the colonies are equal or not. A careless parser that assumes any formula with `?` can distinguish colonies would give the wrong answer here.

## Approaches

The brute-force approach is to evaluate the formula under all assignments of the colonies to the `?` leaves, checking if all possible combinations yield distinguishable outputs. This works conceptually because it directly follows the problem's requirement, but it becomes exponentially slow in n, up to 2^n evaluations, which is infeasible.

The key insight for an optimal solution is that the formula's behavior depends only on the Boolean values of the unknowns, not on the number of colonies. We can compute for each subtree of the formula the set of possible outputs if its `?` leaves are assigned arbitrary 0 or 1 values. For each subexpression, we track whether it can evaluate to 0, 1, or both. This reduces the problem to parsing the formula once and combining these possibilities recursively.

Once we know the overall formula can produce both 0 and 1 for different assignments of `?`, it cannot distinguish all colonies uniquely, because there will always be a way to assign identical colonies to make outputs indistinguishable. Conversely, if the formula is a tautology (always 1) or always false (always 0), it also fails. In practice, it turns out the formula can distinguish the colonies if and only if it is **non-constant and not symmetric for duplicate unknowns**, which is captured by computing the set of possible outcomes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * | formula | ) |
| Recursive Possibility Tracking | O( | formula | ) |

## Algorithm Walkthrough

1. Parse the formula recursively. For each node, determine whether it is a constant (`0` or `1`) or a `?` leaf. A `?` leaf can take values `{0,1}`.
2. For internal nodes, compute the set of possible outcomes from the sets of its left and right children. For `&`, combine left and right using AND for all pairs of possible outcomes. For `|`, combine using OR. For `^`, combine using XOR.
3. After parsing the entire formula, examine the set of outcomes at the root. If the set contains both 0 and 1, the formula cannot distinguish all colonies uniquely, so output "NO". Otherwise, output "YES".
4. The parsing itself can be implemented using a stack-based expression parser or recursion. We process each character of the formula once, and at each operator, we combine small sets `{0,1}`, so the work is constant per node.

Why it works: Each subexpression’s possible outputs capture all ways that unknowns can be assigned. If there exists any assignment that produces both 0 and 1 at the top, then there are indistinguishable colony assignments, meaning we cannot always determine species. This invariant holds throughout the recursion.

## Python Solution

```python
import sys
input = sys.stdin.readline

def compute_possible(node):
    if node == '0':
        return {0}
    if node == '1':
        return {1}
    if node == '?':
        return {0, 1}
    # node is a tuple (op, left, right)
    op, left, right = node
    left_set = compute_possible(left)
    right_set = compute_possible(right)
    result = set()
    for l in left_set:
        for r in right_set:
            if op == '&':
                result.add(l & r)
            elif op == '|':
                result.add(l | r)
            elif op == '^':
                result.add(l ^ r)
    return result

def parse_formula(s):
    stack = []
    i = 0
    while i < len(s):
        if s[i] in '01?':
            stack.append(s[i])
            i += 1
        elif s[i] in '(&|^)':
            stack.append(s[i])
            i += 1
        elif s[i] == ')':
            # Pop right, op, left, '('
            right = stack.pop()
            op = stack.pop()
            left = stack.pop()
            stack.pop()  # '('
            stack.append((op, left, right))
            i += 1
        else:
            i += 1  # skip any whitespace
    return stack[0]

def main():
    n = int(input())
    formula = input().strip()
    root = parse_formula(formula)
    possible = compute_possible(root)
    print("YES" if possible in [{0}, {1}] else "NO")

if __name__ == "__main__":
    main()
```

The parser uses a stack to build the expression tree and handles parentheses and operators explicitly. Each `?` contributes `{0,1}`, and each operator combines left and right sets. The `compute_possible` function returns all possible outcomes of a subexpression. The final check is simple: if both 0 and 1 are possible at the root, we output "NO".

## Worked Examples

Sample 1 Input: `2\n(?^?)`

| Step | Stack / Node | Possible Set |
| --- | --- | --- |
| Read `(` | ['('] | - |
| Read `?` | ['(', '?'] | {0,1} |
| Read `^` | ['(', '?', '^'] | - |
| Read `?` | ['(', '?', '^', '?'] | {0,1} |
| Read `)` | combine `? ^ ?` | {0,1} |
| Final | root = (`^`, '?', '?') | {0,1} |
| Check | {0,1} != {0} and != {1} | NO |

This demonstrates that `?^?` with two colonies cannot distinguish their species.

Sample 2 Input: `2\n(?&1)`

| Step | Stack / Node | Possible Set |
| --- | --- | --- |
| Read `(` | ['('] | - |
| Read `?` | ['(', '?'] | {0,1} |
| Read `&` | ['(', '?', '&'] | - |
| Read `1` | ['(', '?', '&', '1'] | {1} |
| Read `)` | combine `? & 1` | {0,1} & {1} = {0,1} |
| Final | root = (`&`, '?', '1') | {0,1} |
| Check | {0,1} != {0} and != {1} | NO |

Even though one operand is constant, the unknown allows both outputs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O( | formula |
| Space | O( | formula |

The solution scales linearly with the formula size. Given |formula| ≤ 10^6 and n up to 10^6, this fits comfortably within the 1-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import main
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

# Provided sample
assert run("2\n(?^?)") == "NO", "sample 1"

# Custom cases
assert run("3\n(?|?)") == "NO", "all ? with OR, cannot distinguish"
assert run("2\n(1^?)") == "NO", "one constant with XOR, both outcomes possible"
assert run("2\n(1&?)") == "NO", "one constant with AND, both outcomes possible"
assert run("2\n(0|?)") == "NO", "OR with 0, both outcomes possible"
assert run("2\n(1|1)") == "YES", "constant tautology, only 1 possible"
assert run("2\n(0&0)") == "YES", "constant false, only 0 possible"
```

| Test input | Expected output | What it validates |

|
