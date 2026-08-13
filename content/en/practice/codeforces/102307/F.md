---
title: "CF 102307F - Fraction Formula"
description: "Each input line is an arithmetic expression built from fractions, addition, subtraction, and parentheses. A fraction appearing in the expression has a numerator from 0 through 100 and a positive denominator from 1 through 20."
date: "2026-08-13T23:37:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102307
codeforces_index: "F"
codeforces_contest_name: "2019 ICPC Universidad Nacional de Colombia Programming Contest"
rating: 0
weight: 102307
solve_time_s: 187
verified: true
draft: false
---

[CF 102307F - Fraction Formula](https://codeforces.com/problemset/problem/102307/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

Each input line is an arithmetic expression built from fractions, addition, subtraction, and parentheses. A fraction appearing in the expression has a numerator from 0 through 100 and a positive denominator from 1 through 20. Parentheses can be nested arbitrarily, so an expression such as `1/2-(3/4-(1/5+1/10))` is valid.

For every expression, we need its exact rational value and must print that value as a reduced fraction whose denominator is positive. The result itself may be negative, even though every fraction appearing in the input has a nonnegative numerator.

The total number of characters across all input lines is at most `2 * 10^5`. That bound rules out algorithms that repeatedly rescan an expression, since a quadratic algorithm could inspect roughly `2 * 10^10` characters in the worst case. A linear scan is the natural target. The individual denominators are at most 20, which gives us a much stronger property than merely having small input tokens: every denominator divides one fixed small common denominator, the least common multiple of `1, 2, ..., 20`.

Several edge cases can break a careless implementation. For `1/5-2/10`, the correct result is `0/1`. Keeping the unreduced denominator would produce something such as `0/10`, which does not satisfy the required irreducible representation.

For `1/2-(1/2-2/1)`, the correct result is `2/1`. A parser that treats parentheses as ordinary grouping without remembering the sign that preceded the opening parenthesis can incorrectly evaluate the expression as `-2/1` or `-1/1`.

For `1/2-3/2`, the result is `-1/1`. An implementation that assumes the final numerator must be nonnegative because all input fractions are nonnegative would fail here. The restriction applies to the input fractions, not to the expression's value.

For `100/20`, the result is `5/1`. The denominator bound is inclusive, so a parser must accept 20 rather than accidentally treating 19 as the largest possible denominator.

## Approaches

A straightforward brute-force solution could repeatedly locate an innermost parenthesized expression, evaluate it, replace the whole expression by its resulting fraction, and continue until no parentheses remain. Each replacement is mathematically correct because the expression inside the selected parentheses is independent of the surrounding expression.

The problem is the repeated scanning. Consider an expression containing a long chain of nested parentheses. The first search scans almost the entire string, the next search scans almost the entire shortened string, and so on. With `n` characters this takes `Theta(n^2)` character inspections. At `n = 2 * 10^5`, a chain can lead to roughly `n^2 / 2`, around `2 * 10^10`, which is far beyond what a one-second solution can afford.

A recursive parser is already much better because it can evaluate every part of the expression once. However, Python recursion is unsafe here because a valid expression may contain close to `2 * 10^5` nested parentheses. We can avoid recursion completely by keeping the evaluation state explicitly on a stack.

There is also a useful arithmetic simplification. Every input denominator is between 1 and 20, so every denominator divides

`L = lcm(1, 2, ..., 20) = 232792560`.

Instead of storing every fraction as a separate numerator and denominator, convert every input fraction `a/b` into the integer

`a * (L / b)`.

This integer represents the original fraction multiplied by `L`. Since addition and subtraction are linear, the entire expression can then be evaluated using only integer addition and subtraction. Parentheses affect only which accumulated integer receives a sign, so they can be handled by a stack.

After the complete expression has been evaluated, suppose the scaled result is `x`. The actual value is `x/L`. Dividing `x` and `L` by their greatest common divisor gives the required irreducible fraction.

The brute-force method repeatedly revisits the same characters, while the optimal method processes each character once and postpones all fraction reduction until the end.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Set `L = 232792560`, the least common multiple of every possible input denominator. Every fraction `a/b` can be represented as the integer `a * (L/b)`, because its value is exactly that integer divided by `L`.
2. Scan the expression from left to right. Maintain `value`, the current expression value in units of `1/L`, and `sign`, which is either `1` or `-1` and tells us how the next fraction should be added.
3. When a fraction begins, read its numerator and denominator directly from the string. Convert it to the common denominator using `numerator * (L // denominator)`, then add `sign * scaled_fraction` to `value`. We never need floating point arithmetic, so there is no rounding error.
4. When a `+` is encountered, set `sign` to `1`. When a `-` is encountered, set `sign` to `-1`. The sign belongs to the next term, which may be either a fraction or an entire parenthesized expression.
5. When `(` is encountered, push the current `value` and `sign` onto a stack. Then start a fresh expression inside the parentheses with `value = 0` and `sign = 1`. The saved sign is needed because the whole inner expression may have been preceded by `+` or `-`.
6. When `)` is encountered, the inner expression has finished. Pop the saved outer value and outer sign. If the inner result is `inner`, replace the outer state with `outer_value + outer_sign * inner`. This treats the entire parenthesized expression as one term, exactly as the grammar requires.
7. After the scan finishes, the expression has value `value / L`. Compute `g = gcd(abs(value), L)` and print `value // g` over `L // g`. Using the absolute value in the gcd also handles negative results correctly.

### Why it works

The invariant is that at every point in the scan, `value / L` is exactly the value of the portion of the current expression that has already been consumed. The `sign` variable represents the operator waiting to be applied to the next term. Opening a parenthesis saves the complete outer state and starts an independent inner expression. Closing it restores that state and adds the evaluated inner expression with exactly the sign that preceded the opening parenthesis. Since every fraction is converted to the same denominator `L`, all additions and subtractions preserve the exact value represented by `value / L`. At the end, reducing `value/L` by their gcd changes only the representation, not the mathematical value, so the printed fraction is exactly the required answer.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

L = 232792560

def evaluate(s):
    n = len(s)
    i = 0

    value = 0
    sign = 1

    # Each stack entry stores:
    # (value before '(', sign that preceded '(')
    stack = []

    while i < n:
        c = s[i]

        if c.isdigit():
            numerator = 0
            while i < n and s[i].isdigit():
                numerator = numerator * 10 + (ord(s[i]) - ord('0'))
                i += 1

            # Skip '/'
            i += 1

            denominator = 0
            while i < n and s[i].isdigit():
                denominator = denominator * 10 + (ord(s[i]) - ord('0'))
                i += 1

            scaled = numerator * (L // denominator)
            value += sign * scaled

        elif c == '+':
            sign = 1
            i += 1

        elif c == '-':
            sign = -1
            i += 1

        elif c == '(':
            stack.append((value, sign))
            value = 0
            sign = 1
            i += 1

        else:  # ')'
            outer_value, outer_sign = stack.pop()
            value = outer_value + outer_sign * value
            i += 1

    g = gcd(abs(value), L)
    return f"{value // g}/{L // g}"

def main():
    out = []

    for line in sys.stdin:
        s = line.strip()
        if s:
            out.append(evaluate(s))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The constant `L` is the central arithmetic optimization. Since every denominator is at most 20, it divides the least common multiple of `1` through `20`. For example, `1/6` becomes `L/6` units, while `3/10` becomes `3L/10` units. Both are now integers using exactly the same denominator `L`.

The parser reads a complete numerator before skipping `/`, then reads the denominator. There is no unary minus in the input grammar, so a minus sign always acts as the operator between two valid formulas.

The stack stores two values at every opening parenthesis. The first is everything computed before the parenthesis, and the second is the sign that was waiting for the parenthesized expression. Resetting `value` to zero gives the inner expression its own accumulator.

When a closing parenthesis is processed, the expression inside it has already been completely evaluated. The line `value = outer_value + outer_sign * value` is exactly the mathematical operation represented by the surrounding context. After that operation, the parser can continue normally.

Python integers have arbitrary precision, so there is no overflow risk. More importantly, the common denominator is fixed, so the accumulated numerator remains modest. There are at most `O(n)` fractions, each contributing at most `100L`, giving a numerator whose magnitude is at most `O(nL)`, rather than an enormous product of all input denominators.

The final gcd uses `abs(value)` because `value` can be negative. If `value` is zero, `gcd(0, L)` is `L`, so the result automatically becomes `0/1`.

## Worked Examples

Consider the first sample expression, `1/2+1/3`. The common denominator is `L`, so the two fractions contribute `L/2` and `L/3`.

| Position | Character or token | value | sign | Stack |
| --- | --- | --- | --- | --- |
| 0 | `1/2` | 116396280 | 1 | empty |
| 3 | `+` | 116396280 | 1 | empty |
| 4 | `1/3` | 193993800 | 1 | empty |
| end | reduction | `5/6` |  | empty |

The accumulated scaled value is `L/2 + L/3 = 5L/6`. Since `gcd(5L/6, L) = L/6`, the final representation is `5/6`.

Now consider the third sample, `1/2+(1/2-2/1)`. This example exercises both a parenthesized subexpression and subtraction inside it.

| Position | Character or token | value | sign | Stack |
| --- | --- | --- | --- | --- |
| 0 | `1/2` | 116396280 | 1 | empty |
| 3 | `+` | 116396280 | 1 | empty |
| 4 | `(` | 0 | 1 | `(116396280, 1)` |
| 5 | `1/2` | 116396280 | 1 | `(116396280, 1)` |
| 8 | `-` | 116396280 | -1 | `(116396280, 1)` |
| 9 | `2/1` | -116396280 | -1 | `(116396280, 1)` |
| 12 | `)` | 0 | 1 | empty |
| end | reduction | `-1/1` |  | empty |

Inside the parentheses, `1/2 - 2/1 = -3/2`. The outer expression is `1/2 + (-3/2) = -1`, which gives the required `-1/1`. The stack is what preserves the outer `+` while the inner expression is evaluated independently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every character is scanned once, and the final gcd uses integers whose size is bounded by the total number of fractions times the fixed constant `L`. |
| Space | O(n) | The parenthesis stack can contain one entry per nesting level. |

Here `n` is the total length of all input expressions. Since the total is at most `2 * 10^5`, a single linear pass over all input is comfortably within the intended limit. The stack also uses at most linear memory, well below 256 MB.

## Test Cases

```python
import sys
import io
from math import gcd

L = 232792560

def evaluate(s):
    n = len(s)
    i = 0
    value = 0
    sign = 1
    stack = []

    while i < n:
        c = s[i]

        if c.isdigit():
            numerator = 0
            while i < n and s[i].isdigit():
                numerator = numerator * 10 + ord(s[i]) - ord('0')
                i += 1

            i += 1  # '/'

            denominator = 0
            while i < n and s[i].isdigit():
                denominator = denominator * 10 + ord(s[i]) - ord('0')
                i += 1

            value += sign * numerator * (L // denominator)

        elif c == '+':
            sign = 1
            i += 1

        elif c == '-':
            sign = -1
            i += 1

        elif c == '(':
            stack.append((value, sign))
            value = 0
            sign = 1
            i += 1

        else:
            outer_value, outer_sign = stack.pop()
            value = outer_value + outer_sign * value
            i += 1

    g = gcd(abs(value), L)
    return f"{value // g}/{L // g}"

def run(inp: str) -> str:
    old_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO(inp)
        return "\n".join(
            evaluate(line.strip())
            for line in sys.stdin
            if line.strip()
        )
    finally:
        sys.stdin = old_stdin

# Provided samples
assert run("1/2+1/3\n") == "5/6", "sample 1"
assert run("1/5-2/10\n") == "0/1", "sample 2"
assert run("1/2+(1/2-2/1)\n") == "-1/1", "sample 3"

# Minimum-size input
assert run("0/1\n") == "0/1", "minimum fraction"

# Maximum numerator and denominator boundary
assert run("100/20\n") == "5/1", "maximum numerator and denominator"

# All equal values
assert run("1/2+1/2+1/2+1/2\n") == "2/1", "equal fractions"

# Deep nesting and subtraction through parentheses
assert run("1/1-(1/1-(1/1-(1/1)))\n") == "1/1", "nested parentheses"

# Negative result
assert run("1/20-100/1\n") == "-1999/20", "negative result"

# Force the expression length close to the maximum allowed.
terms = ["100/20"] * 28571
large_input = "+".join(terms)
assert len(large_input) <= 200000
assert run(large_input) == f"{5 * len(terms)}/1", "large input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0/1` | `0/1` | Zero numerator and minimum denominator |
| `100/20` | `5/1` | Inclusive numerator and denominator boundaries plus reduction |
| `1/2+1/2+1/2+1/2` | `2/1` | Repeated equal fractions and final reduction |
| `1/1-(1/1-(1/1-(1/1)))` | `1/1` | Nested parentheses and sign propagation |
| `1/20-100/1` | `-1999/20` | Negative final result and a small denominator |
| 28571 copies of `100/20` joined by `+` | `142855/1` | Near-maximum input length and linear scanning |

## Edge Cases

The expression `1/5-2/10` tests reduction to zero. Both fractions become integers with denominator `L`, and their scaled values are equal, so the accumulator becomes zero. The final gcd is `gcd(0, L) = L`, producing `0/1` rather than an unreduced `0/L`.

The expression `1/2-(1/2-2/1)` tests a sign attached to a whole parenthesized expression. Before entering the parentheses, the stack stores the outer value `L/2` and sign `-1`. The inner expression evaluates to `L/2 - 2L = -3L/2`. Closing the parenthesis restores the outer state and computes `L/2 - (-3L/2) = 2L`, which reduces to `2/1`. The same mechanism works for any nesting depth.

The expression `1/2-3/2` produces `-1/1`. The accumulator simply becomes `L/2 - 3L/2 = -L`, and the gcd reduction preserves the negative sign in the numerator. No special case for negative expressions is necessary.

The expression `100/20` checks the maximum allowed values directly. Since `20` divides `L`, the scaled fraction is `100 * (L/20) = 5L`, and the final reduction gives `5/1`. The conversion `L // denominator` is exact because every allowed denominator is a divisor of `L`.

A deeply nested expression such as `1/1-(1/1-(1/1-(1/1)))` also demonstrates why an explicit stack is preferable to recursive parsing in Python. Each opening parenthesis adds one constant-size stack entry, and each closing parenthesis removes it. The parser never depends on the Python call stack, so even a valid expression with very deep nesting remains safe.

Finally, a very long expression made from many fractions tests the actual input bound. The parser does not repeatedly rebuild or rescan the expression, so its work grows directly with the number of input characters. The fixed common denominator also prevents fraction denominators from growing during evaluation, keeping the arithmetic efficient even near the `2 * 10^5` character limit.
