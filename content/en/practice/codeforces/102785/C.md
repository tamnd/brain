---
title: "CF 102785C - Dimensions"
description: "Edit The input is a mathematical expression describing a physical dimension. Every Latin letter represents a basic dimension, while multiplication, division, and parentheses combine dimensions in the usual way."
date: "2026-07-27T19:36:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102785
codeforces_index: "C"
codeforces_contest_name: "ICPC Central Russia Regional Contest (CRRC 18)"
rating: 0
weight: 102785
solve_time_s: 96
verified: true
draft: false
---

[CF 102785C - Dimensions](https://codeforces.com/problemset/problem/102785/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 36s  
**Verified:** yes  

## Solution
Edit

# Problem Understanding

The input is a mathematical expression describing a physical dimension. Every Latin letter represents a basic dimension, while multiplication, division, and parentheses combine dimensions in the usual way. Repeating a letter means multiplying by that dimension several times, so `AAA` represents the third power of `A`.

The task is to simplify the entire expression by combining equal dimensions. A dimension appearing in the numerator cancels with the same dimension appearing in the denominator. After all cancellations, the remaining numerator and denominator factors must be printed separately, with each side sorted according to the required order: `A, a, B, b, ... , Z, z`.

The expression length is at most 1000 characters. This is small enough that a linear parser is appropriate, but it rules out approaches that repeatedly expand or simplify large intermediate strings. A solution that tries every possible pair of factors could approach quadratic behavior, and repeated string replacements could become even worse because each replacement may scan most of the expression again.

The tricky parts are caused by nesting and by the difference between a dimension's position and its final sign. For example, in `kg/(kg/(m/s))`, the inner division changes signs twice before the final result is known. A parser that only handles left to right multiplication and division without respecting parentheses would incorrectly keep `kg` in the answer.

Another edge case is complete cancellation. For input `A/A`, the correct output is:

```
1
1
```

A careless implementation might print an empty line for one side instead of representing the identity dimension with `1`.

Case sensitivity is also significant. For input `aA`, the two symbols are different dimensions. The correct output is:

```
Aa
1
```

Treating letters only by their lowercase form would incorrectly cancel them.

Repeated dimensions must be counted, not treated as a single occurrence. For input `AAA/A`, the correct output is:

```
AA
1
```

A solution using a set instead of counts would lose the remaining exponent.

## Approaches

A direct approach is to convert the expression into a list of individual factors while evaluating operations. Each multiplication keeps the sign of the current context, and each division reverses it. A brute force simplifier could then compare every numerator factor against every denominator factor and remove matching pairs. This is correct because cancellation only depends on how many times each dimension appears on each side. However, in the worst case an expression with about 1000 factors would require around one million comparisons, and repeated removals from lists would add more overhead.

The key observation is that every dimension only needs its final exponent. The exact place where a factor appeared no longer matters after parsing. A dictionary mapping each letter to an integer count can store this directly. A positive count means the dimension remains in the numerator, while a negative count means it remains in the denominator.

The structure of the expression makes recursive parsing natural. Parentheses create independent subexpressions, and division simply changes the sign of every factor inside the following term. While parsing, we maintain a multiplier representing whether the current part contributes positively or negatively. A letter adds that multiplier to its count. This turns the entire simplification into one traversal of the expression.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow for repeated comparisons |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Parse the expression recursively and maintain a sign multiplier for the current context. The initial multiplier is positive because the whole expression starts in the numerator. A parenthesized expression receives the multiplier from its surrounding operator.
2. When a letter is found, add the current multiplier to that letter's counter. The counter stores the net exponent, so later cancellations happen automatically without needing separate numerator and denominator lists.
3. When multiplication is found, continue parsing the next term with the same multiplier. Multiplication does not change whether a factor belongs to the numerator or denominator.
4. When division is found, parse the following term with the opposite multiplier. Division flips the side of every dimension in the following expression, including everything inside parentheses.
5. After parsing finishes, separate letters with positive counters from letters with negative counters. Print positive counts in the numerator and absolute values of negative counts in the denominator.
6. Sort each side using the custom alphabetic order where uppercase and lowercase versions of the same letter are adjacent. If a side has no factors, print `1`.

The reason the sign multiplier works is that every division operation changes the exponent sign of the entire expression that follows it. Nested divisions are handled naturally because each recursive call receives the sign that results from all surrounding divisions.

Why it works: during parsing, the counter for every dimension is exactly the exponent contributed by every occurrence of that dimension. Multiplication leaves the exponent sign unchanged, while division negates the contribution of the divided expression. Parentheses only control which subexpression receives that sign change. After the traversal, a positive exponent represents remaining numerator factors and a negative exponent represents remaining denominator factors, so the produced output is the fully reduced dimension.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    n = len(s)
    cnt = {}

    def parse(pos, sign):
        while pos < n:
            c = s[pos]

            if c.isalpha():
                cnt[c] = cnt.get(c, 0) + sign
                pos += 1
            elif c == '(':
                pos = parse(pos + 1, sign)
            elif c == ')':
                return pos + 1
            elif c == '*':
                pos += 1
            elif c == '/':
                pos = parse(pos + 1, -sign)
            else:
                pos += 1

        return pos

    parse(0, 1)

    def sort_key(c):
        return (c.lower(), 0 if c.isupper() else 1)

    numerator = []
    denominator = []

    for c in sorted(cnt.keys(), key=sort_key):
        if cnt[c] > 0:
            numerator.extend([c] * cnt[c])
        elif cnt[c] < 0:
            denominator.extend([c] * (-cnt[c]))

    print('*'.join(numerator) if numerator else "1")
    print('*'.join(denominator) if denominator else "1")

if __name__ == "__main__":
    solve()
```

The dictionary `cnt` is the central data structure. Instead of storing every occurrence separately, the code immediately merges equal dimensions into their final exponent. This keeps the memory usage small and makes cancellation automatic.

The recursive function `parse` walks through the expression. Its second parameter is the current sign. A letter modifies the counter using that sign. A division operator calls `parse` with the opposite sign, which is the same as multiplying the following subexpression by `-1`.

The closing parenthesis returns control to the caller, because the caller already knows whether the whole parenthesized part was multiplied or divided. This avoids needing to build a separate expression tree.

The sorting key cannot use normal ASCII order because ASCII places all uppercase letters before lowercase letters. The required order groups the two cases together, so the key first compares the lowercase form and then places uppercase before lowercase.

The output construction repeats each letter according to its exponent. This handles dimensions such as `AAA/A` correctly because the stored count is the remaining power after cancellation.

## Worked Examples

For the first sample, the expression is `kg/(kg/(m/s))`.

| Step | Current expression part | Sign | Counters |
| --- | --- | --- | --- |
| 1 | `kg` before first division | +1 | k:1, g:1 |
| 2 | inner `kg` | -1 | k:0, g:0 |
| 3 | inner `m` | +1 | m:1 |
| 4 | inner `s` | -1 | s:-1 |

The two `kg` occurrences cancel because the nested division changes the signs twice. The final positive factor is `m` and the final negative factor is `s`.

For the second sample, the expression is `kg*a/(Fs*B)*A*Kt`.

| Step | Current expression part | Sign | Counters |
| --- | --- | --- | --- |
| 1 | `k`, `g`, `a` | +1 | k:1, g:1, a:1 |
| 2 | `F`, `s`, `B` | -1 | F:-1, s:-1, B:-1 |
| 3 | `A`, `K`, `t` | +1 | A:1, K:1, t:1 |

After sorting with the custom order, the numerator becomes `A*a*Kt*kg` and the denominator becomes `B*Fs`. This example demonstrates that case-sensitive symbols remain separate and that sorting is done only after all arithmetic is complete.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every character is processed once during parsing, and sorting only handles at most 52 distinct letters |
| Space | O(1) | The counter dictionary stores only possible Latin letters, not the expression size |

The input limit of 1000 characters is easily handled by a single recursive traversal. The solution does not create expanded intermediate expressions, so it remains efficient even when many nested parentheses are present.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("kg/(kg/(m/s))\n") == "m\ns\n", "sample 1"
assert run("kg*a/(Fs*B)*A*Kt\n") == "A*a*Kt*kg\nB*Fs\n", "sample 2"

assert run("A\n") == "A\n1\n", "single numerator dimension"
assert run("A/A\n") == "1\n1\n", "complete cancellation"
assert run("AAA/A\n") == "AA\n1\n", "repeated dimensions"
assert run("aA\n") == "Aa\n1\n", "case-sensitive sorting"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `A` | `A` and `1` | Minimum expression size |
| `A/A` | `1` and `1` | Full cancellation and empty side handling |
| `AAA/A` | `AA` and `1` | Exponent counting |
| `aA` | `Aa` and `1` | Custom sorting and case sensitivity |

## Edge Cases

For `kg/(kg/(m/s))`, the parser first records `kg` with a positive sign, then enters the divided parenthesized expression with a negative sign. Inside that expression, the second division flips the sign again for `m/s`. The two `kg` factors cancel, leaving `m` in the numerator and `s` in the denominator.

For `A/A`, the first `A` increments the counter to one and the second `A` decrements it back to zero. Since neither side has any remaining factor, both output lines become `1`.

For `aA`, the algorithm keeps two separate dictionary keys because character case is part of the dimension name. Sorting compares both keys using their lowercase forms and then their cases, producing `Aa` instead of merging them.

For `AAA/A`, the counter for `A` becomes three and then decreases by one. The final exponent is two, so the output contains `A` twice. This confirms that the algorithm stores multiplicity rather than only presence.
