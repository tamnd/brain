---
title: "CF 64B - Expression"
description: "The input is a tiny arithmetic expression written as a three-character string. The first and third characters are digits from 0 to 9, and the middle character is either + or -. The task is to evaluate the expression and print the resulting integer."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "expression-parsing"]
categories: ["algorithms"]
codeforces_contest: 64
codeforces_index: "B"
codeforces_contest_name: "Unknown Language Round 1"
rating: 1500
weight: 64
solve_time_s: 99
verified: true
draft: false
---

[CF 64B - Expression](https://codeforces.com/problemset/problem/64/B)

**Rating:** 1500  
**Tags:** *special, expression parsing  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

The input is a tiny arithmetic expression written as a three-character string. The first and third characters are digits from `0` to `9`, and the middle character is either `+` or `-`. The task is to evaluate the expression and print the resulting integer.

For example, the input `1-5` represents the subtraction `1 - 5`, so the correct output is `-4`. The input `7+2` represents `7 + 2`, so the output is `9`.

The constraints are extremely small because the expression always has fixed length. There is no need for parsing libraries, tokenization, recursion, or expression trees. A constant amount of work is enough, since we only need to read three characters and apply one arithmetic operation.

The only subtle part is handling subtraction correctly when the result becomes negative. A careless implementation that assumes all outputs are non-negative would fail on inputs like:

```
1-5
```

The correct output is:

```
-4
```

Another easy mistake is forgetting to convert characters into integers before operating on them. For example, if someone directly subtracts character codes, the result would be meaningless. With input:

```
9-2
```

we must compute integer subtraction `9 - 2 = 7`, not the difference between ASCII values.

A third edge case is zero. Expressions like:

```
0-0
```

must correctly produce:

```
0
```

Some buggy implementations accidentally special-case subtraction and mishandle equal operands.

## Approaches

The most direct approach is to inspect the operator character and compute the result accordingly. Since the expression length is always exactly three, we can access the first digit, the operator, and the second digit by index. After converting the digit characters into integers, we either add or subtract.

Even a brute-force style solution is effectively constant time here. One could manually check all possible expressions from `0+0` through `9-9`, store them in a lookup table, and print the matching result. That would still only involve a few hundred operations because there are only 200 possible expressions. The approach is correct because every valid input belongs to this finite set, but it is unnecessarily rigid and less readable.

The cleaner observation is that the input already encodes everything directly. The middle character completely determines which arithmetic operation to apply. Once we convert the two digits into integers, evaluation becomes a single addition or subtraction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input string.

The expression always has the form `digit operator digit`, so its length is fixed at three characters.
2. Extract the first digit, operator, and second digit.

The first digit is at index `0`, the operator at index `1`, and the second digit at index `2`.
3. Convert the digit characters into integers.

Arithmetic on characters is incorrect, so we must convert them using `int()`.
4. Check the operator.

If the operator is `+`, compute the sum. Otherwise, compute the difference.
5. Print the result.

### Why it works

The expression format guarantees exactly one operator and two single-digit operands. The algorithm reads those three components directly and applies the corresponding arithmetic rule. Since addition and subtraction are implemented exactly as defined in the expression, the produced value always matches the mathematical result.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

a = int(s[0])
op = s[1]
b = int(s[2])

if op == '+':
    print(a + b)
else:
    print(a - b)
```

The program begins by reading the expression string and removing the trailing newline with `strip()`.

The first and third characters are converted into integers immediately. This avoids mistakes caused by operating on characters directly. The middle character is stored as the operator.

The conditional checks whether the operator is `'+'`. If true, the program prints the sum. Otherwise, the only remaining valid operator is `'-'`, so it prints the subtraction result.

There are no boundary issues because the input format guarantees exactly three characters in the expression. Python integers also safely handle negative values, so cases like `1-5` work naturally.

## Worked Examples

### Example 1

Input:

```
1-5
```

| Step | Variable | Value |
| --- | --- | --- |
| Read string | `s` | `"1-5"` |
| First digit | `a` | `1` |
| Operator | `op` | `'-'` |
| Second digit | `b` | `5` |
| Compute | `a - b` | `-4` |

The operator is subtraction, so the algorithm computes `1 - 5`. This example confirms that negative answers are handled correctly.

### Example 2

Input:

```
7+2
```

| Step | Variable | Value |
| --- | --- | --- |
| Read string | `s` | `"7+2"` |
| First digit | `a` | `7` |
| Operator | `op` | `'+'` |
| Second digit | `b` | `2` |
| Compute | `a + b` | `9` |

This trace demonstrates the addition branch. The algorithm correctly identifies the operator and performs the matching arithmetic operation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few character accesses and one arithmetic operation are performed |
| Space | O(1) | The algorithm stores a constant number of variables |

The solution easily fits within the limits because the input size never grows. Runtime and memory usage remain constant regardless of the specific digits used.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    s = input().strip()

    a = int(s[0])
    op = s[1]
    b = int(s[2])

    if op == '+':
        print(a + b)
    else:
        print(a - b)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    backup_stdout = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup_stdout
    return out.getvalue()

# provided sample
assert run("1-5\n") == "-4\n", "sample 1"

# custom cases
assert run("0+0\n") == "0\n", "minimum values"
assert run("9+9\n") == "18\n", "maximum addition result"
assert run("9-0\n") == "9\n", "subtraction with zero"
assert run("0-9\n") == "-9\n", "negative result boundary"
assert run("5-5\n") == "0\n", "equal operands"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0+0` | `0` | Smallest possible operands |
| `9+9` | `18` | Largest addition result |
| `9-0` | `9` | Subtraction with zero |
| `0-9` | `-9` | Negative result handling |
| `5-5` | `0` | Equal operands |

## Edge Cases

Consider the input:

```
1-5
```

The algorithm extracts `a = 1`, `op = '-'`, and `b = 5`. Since the operator is subtraction, it computes `1 - 5 = -4`. The output is:

```
-4
```

This confirms that negative values are handled correctly without any special logic.

Now consider:

```
0-0
```

The extracted values are `a = 0`, `op = '-'`, and `b = 0`. The computation becomes `0 - 0 = 0`, so the algorithm prints:

```
0
```

This case verifies that subtraction does not accidentally introduce sign errors when both operands are equal.

Finally, consider:

```
9+9
```

The algorithm reads `a = 9`, `op = '+'`, and `b = 9`. Since the operator is addition, it computes `9 + 9 = 18`. The output becomes:

```
18
```

This demonstrates that the result is not restricted to a single digit, even though both operands are single digits.
