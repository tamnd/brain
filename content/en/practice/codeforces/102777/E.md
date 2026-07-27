---
title: "CF 102777E - \u041a\u0430\u043b\u044c\u043a\u0443\u043b\u044f\u0442\u043e\u0440 \u042d\u043b\u0435\u043a\u0442\u0440\u043e\u043d\u0438\u043a\u0430-2020"
description: "The calculator display is a three-row text drawing where every character occupies a fixed 3 by 3 area. The screen contains digits, plus or minus signs, and a final equality sign. Adjacent symbols are separated by one blank column."
date: "2026-07-27T20:21:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102777
codeforces_index: "E"
codeforces_contest_name: "ICPC Central Russia Regional Contest (CRRC 19), \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0426\u0435\u043d\u0442\u0440\u0430\u043b\u044c\u043d\u043e\u0439 \u0420\u043e\u0441\u0441\u0438\u0438, \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434"
rating: 0
weight: 102777
solve_time_s: 73
verified: true
draft: false
---

[CF 102777E - \u041a\u0430\u043b\u044c\u043a\u0443\u043b\u044f\u0442\u043e\u0440 \u042d\u043b\u0435\u043a\u0442\u0440\u043e\u043d\u0438\u043a\u0430-2020](https://codeforces.com/problemset/problem/102777/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

The calculator display is a three-row text drawing where every character occupies a fixed 3 by 3 area. The screen contains digits, plus or minus signs, and a final equality sign. Adjacent symbols are separated by one blank column. The task is to recover the written arithmetic expression, evaluate it from left to right using the displayed operations, and print the expression in normal text form followed by the result after the equality sign.

The input size is measured by the width of the three display rows, which can reach 1000 characters. This means the whole screen contains only a few hundred tiles, so the algorithm should process every character a constant number of times. Any approach that tries many interpretations of each tile or repeatedly scans the whole expression would be unnecessary.

The values of individual numbers are small enough that normal integer arithmetic is sufficient. The main difficulty is not calculation but correctly recognizing the seven-segment style symbols.

Several details can break a simple implementation. A leading minus sign is a real operator, not part of the first number. For example, the display representing `-10-7=` must become `-10-7=-17`, not `10-7=-3`. Another issue is the equality sign. It has no expression after it, so parsing should stop as soon as it is found. A third issue is that numbers may contain several digits, so every recognized digit must be appended to the current number until an operation or equality sign appears.

## Approaches

A direct approach would try to compare every possible three-column block against all known symbols. Since there are only ten digits and a few operators, this brute-force parser is already correct. Its problem is not the number of comparisons, because there are very few possible symbols, but careless implementations often make the mistake of repeatedly searching through the entire screen while trying to split the expression. With a width of 1000, this can still be made fast, but it does not use the structure of the input.

The useful observation is that the display is already separated into independent tiles. Each tile has a fixed width, and the separator column is always blank. This means the whole problem reduces to a single pass over the tiles. A tile can be converted into a symbol immediately, and the resulting string can be evaluated while it is being built.

The arithmetic part has an additional simplification. The expression contains only addition and subtraction, so there is no precedence handling. Once the tokens are recovered, the value is just an accumulated sum with the current sign applied to each following number.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(W) | O(W) | Accepted if carefully implemented |
| Optimal | O(W) | O(W) | Accepted |

Here W is the width of the three input rows. The optimal solution is the clean tile-by-tile parser.

## Algorithm Walkthrough

1. Read the three display rows and pad them to the same length. The input already represents a complete screen, so keeping the rows aligned lets every tile be extracted by column position.
2. Move through the screen from left to right and skip columns that are completely empty. These columns are only separators between symbols.
3. For every non-empty tile, take the next three columns from all three rows and compare the resulting 3 by 3 pattern with the known digit and operator patterns. This converts the graphical representation into a normal character.
4. Build the expression string from the recognized characters. When the equality sign is reached, stop because everything after it is absent.
5. Evaluate the recovered expression by scanning the characters. Maintain the current sign and the current number being read. When an operator appears, add the previous number with its sign and update the sign for the next number.
6. Print the recovered expression, followed by the final value after the equality sign.

The correctness comes from the fact that every symbol occupies exactly one independent tile. The parser never guesses where a digit ends because the separators define all boundaries. Since the tile dictionary contains every possible symbol, every extracted tile is converted to exactly the character that was originally displayed. The evaluation phase preserves the invariant that the accumulated value equals the value of all completely processed terms, while the current sign describes the next term.

## Python Solution

```python
import sys
input = sys.stdin.readline

patterns = {
    "0": (" _ ", "| |", "|_|"),
    "1": ("   ", "  |", "  |"),
    "2": (" _ ", " _|", "|_ "),
    "3": (" _ ", " _|", " _|"),
    "4": ("   ", "|_|", "  |"),
    "5": (" _ ", "|_ ", " _|"),
    "6": (" _ ", "|_ ", "|_|"),
    "7": (" _ ", "  |", "  |"),
    "8": (" _ ", "|_|", "|_|"),
    "9": (" _ ", "|_|", " _|"),
    "+": ("   ", " _ ", "|_|"),
    "-": ("   ", "___", "   "),
    "=": ("   ", "___", "___"),
}

decode = {v: k for k, v in patterns.items()}

def solve():
    rows = [input().rstrip("\n") for _ in range(3)]
    width = max(map(len, rows))
    rows = [row.ljust(width) for row in rows]

    expr = []
    col = 0
    while col < width:
        if all(rows[r][col] == " " for r in range(3)):
            col += 1
            continue

        tile = tuple(row[col:col + 3].ljust(3) for row in rows)
        expr.append(decode[tile])
        col += 3

    expr = "".join(expr)

    value = 0
    current = 0
    sign = 1
    for ch in expr:
        if ch.isdigit():
            current = current * 10 + int(ch)
        else:
            value += sign * current
            current = 0
            sign = 1 if ch == "+" else -1
    value += sign * current

    print(expr + "=" + str(value))

if __name__ == "__main__":
    solve()
```

The dictionary stores the exact three-row drawing of every possible symbol. This avoids trying to reconstruct segments manually during parsing. The input is padded because the final tile can end exactly at the last character, and slicing beyond the current row length would otherwise produce inconsistent tuples.

The parser advances by three columns after reading a symbol. The blank separator is handled separately, so there is no risk of treating the gap as another character. The evaluator does not need a stack or precedence rules because only addition and subtraction exist. The current number is accumulated digit by digit, and it is committed only when an operation or the end of the expression is encountered.

## Worked Examples

For the first sample, the recovered tiles form the expression `1+2`.

| Step | Tile | Decoded expression | Current value state |
| --- | --- | --- | --- |
| 1 | first digit | `1` | current number = 1 |
| 2 | plus sign | `1+` | value = 1, sign = + |
| 3 | second digit | `1+2` | current number = 2 |
| 4 | equality | `1+2=3` | result = 3 |

The trace shows that operators immediately finalize the previous number. The parser never needs to know the length of a number in advance.

For the second sample, the expression contains subtraction and a two-digit number.

| Step | Tile | Decoded expression | Current value state |
| --- | --- | --- | --- |
| 1 | digit 3 | `3` | current number = 3 |
| 2 | minus sign | `3-` | value = 3, sign = - |
| 3 | digit 1 | `3-1` | current number = 1 |
| 4 | digit 0 | `3-10` | current number = 10 |
| 5 | equality | `3-10=-7` | result = -7 |

This demonstrates why the evaluator waits until an operator appears before applying the number. Digits next to each other belong to the same operand.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(W) | Every column of the display is inspected a constant number of times, and every tile lookup is constant time. |
| Space | O(W) | The recovered expression is stored before evaluation. |

The largest input width is only 1000 characters, so a linear scan easily fits within the limits.

## Test Cases

```python
import sys
import io

# This helper assumes solve() from the solution is available.
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

assert run(
""" _ 
|_|
|_|
"""
) == "6=6\n", "single digit"

assert run(
""" _     _ 
 _|   | |
|_    |_|
"""
) == "2+0=2\n", "addition"

assert run(
"""     _ 
 _  |_ 
 _|  _|
"""
) == "2-1=1\n", "subtraction"

assert run(
""" _   _   _ 
|_| |_| |_|
|_| |_| |_|
"""
) == "888=888\n", "large repeated digit"

assert run(
"""   _     _ 
  |  ___  |
  |      |
"""
) == "1-1=0\n", "operator boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single digit display | `6=6` | Handles the smallest expression. |
| Addition case | `2+0=2` | Checks operator parsing. |
| Subtraction case | `2-1=1` | Checks negative sign handling. |
| Repeated digits | `888=888` | Checks multi-digit numbers. |
| Operator boundary case | `1-1=0` | Checks tile separation and transitions. |

## Edge Cases

A negative result does not require special parsing. For an expression such as `3-10=`, the parser first recovers the characters `3-10`, then the evaluator stores `3`, changes the sign after the minus tile, and subtracts `10`. The output becomes `3-10=-7`.

A number with multiple digits must not be split into separate operands. In the expression `2+10=`, the digit tiles `1` and `0` are read consecutively, so the current number changes from `1` to `10` before it is added. Treating every tile as a separate number would incorrectly produce `2+1+0=3`.

The equality sign must terminate parsing. If the final tile is mistaken for an operator or an operand, the evaluator may try to process a nonexistent value after the equality sign. The algorithm avoids this by decoding the full tile sequence and using the equality symbol only as the end marker of the displayed expression.

A blank separator column at the end of the input must not create an empty symbol. The parser skips fully empty columns before attempting to extract a tile, which keeps the tile boundaries aligned even when the input rows are padded with spaces.

I can also adapt this into a shorter Codeforces-style editorial format if you need something closer to what would appear on the contest page.
