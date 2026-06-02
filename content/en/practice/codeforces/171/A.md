---
title: "CF 171A - Mysterious numbers - 1"
description: "This problem comes from an April Fools contest where the statement intentionally hides the real task. We are given two non-negative integers. The required operation is: 1. Reverse the decimal representation of the second number. 2. Add the result to the first number. 3."
date: "2026-06-02T08:58:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 171
codeforces_index: "A"
codeforces_contest_name: "April Fools Day Contest"
rating: 1200
weight: 171
solve_time_s: 103
verified: true
draft: false
---

[CF 171A - Mysterious numbers - 1](https://codeforces.com/problemset/problem/171/A)

**Rating:** 1200  
**Tags:** *special, constructive algorithms  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

This problem comes from an April Fools contest where the statement intentionally hides the real task.

We are given two non-negative integers. The required operation is:

1. Reverse the decimal representation of the second number.
2. Add the result to the first number.
3. Output the sum.

For example, if the input is `3 14`, the reverse of `14` is `41`, and the answer is `3 + 41 = 44`. This matches the sample output.

The numbers are at most $10^9$, so each contains at most ten digits. Any operation on the digits of a number takes constant time in practice. There is no need for sophisticated algorithms, data structures, or optimization. A simple digit reversal followed by one addition easily fits within the limits.

The main source of mistakes is handling leading zeros after reversal.

Consider the input:

```
100 200
```

Reversing `"200"` gives `"002"`, which represents the integer `2`. The answer is:

```
100 + 2 = 102
```

A careless implementation that preserves leading zeros as digits could incorrectly treat the reversed value as `200`.

Another edge case is when the second number is zero:

```
5 0
```

The reverse of `0` is still `0`, so the answer is:

```
5
```

Some string-based implementations accidentally produce an empty string when stripping zeros.

A third edge case is when the reversed number ends with zeros before reversal:

```
27 12
```

The reverse of `12` is `21`, giving:

```
27 + 21 = 48
```

This sample confirms that the operation is true digit reversal rather than sorting or rearranging digits.

## Approaches

A brute-force approach would examine every digit of the second number, build its reversed form, convert it back into an integer, and then add it to the first number.

Since the second number contains at most ten digits, this already runs in constant time. Even if we processed millions of test cases, the work per case would remain tiny.

The key observation is simply understanding the hidden operation. Once we recognize that the answer is:

$$a_1 + \text{reverse}(a_2)$$

the implementation becomes straightforward.

There are two common ways to reverse a number. One is arithmetic, repeatedly taking the last digit and appending it to a new number. The other is converting the number to a string and reversing the characters. Because the input size is extremely small, either approach is accepted.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force digit reversal | O(d) | O(1) | Accepted |
| Optimal | O(d) | O(1) | Accepted |

Here $d$ is the number of digits of the second number, at most 10.

## Algorithm Walkthrough

1. Read the integers `a1` and `a2`.
2. Reverse the decimal digits of `a2`.

The easiest method is to repeatedly extract the last digit with `% 10` and append it to a new number.
3. Add the reversed value to `a1`.
4. Output the result.

### Why it works

The problem's hidden rule is exactly to add the first number to the reversed second number. The reversal procedure reconstructs the integer whose decimal representation is written in the opposite order. Every digit of `a2` appears once and in the correct reversed position, so the constructed value is precisely `reverse(a2)`. Adding this value to `a1` yields the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

a1, a2 = map(int, input().split())

rev = 0
if a2 == 0:
    rev = 0
else:
    while a2 > 0:
        rev = rev * 10 + (a2 % 10)
        a2 //= 10

print(a1 + rev)
```

The first part reads the two integers.

The variable `rev` stores the reversed form of the second number. During each iteration, the current last digit is appended to the end of `rev`. For example, if `a2 = 123`, the sequence becomes:

```
rev = 3
rev = 32
rev = 321
```

The special case `a2 = 0` is handled explicitly. Without it, the loop would never execute and the answer would still be correct, but the intent becomes clearer.

Finally, the code adds `a1` and the reversed number and prints the result.

Because Python integers have arbitrary precision, there is no overflow risk. Even in languages with fixed-width 64-bit integers, the largest possible answer is very small compared to the limit.

## Worked Examples

### Example 1

Input:

```
3 14
```

| Step | a2 | Extracted Digit | rev |
| --- | --- | --- | --- |
| Start | 14 | - | 0 |
| 1 | 14 | 4 | 4 |
| 2 | 1 | 1 | 41 |

Final computation:

| a1 | reverse(a2) | Answer |
| --- | --- | --- |
| 3 | 41 | 44 |

The trace shows how each extracted digit is appended to the new number, producing `41`.

### Example 2

Input:

```
100 200
```

| Step | a2 | Extracted Digit | rev |
| --- | --- | --- | --- |
| Start | 200 | - | 0 |
| 1 | 200 | 0 | 0 |
| 2 | 20 | 0 | 0 |
| 3 | 2 | 2 | 2 |

Final computation:

| a1 | reverse(a2) | Answer |
| --- | --- | --- |
| 100 | 2 | 102 |

This example demonstrates that leading zeros disappear naturally when the reversed value is stored as an integer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(d) | Process each digit of the second number once |
| Space | O(1) | Only a few integer variables are used |

Since $d \le 10$, the running time is effectively constant. The solution is far below the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    a1, a2 = map(int, input().split())

    rev = 0
    if a2 == 0:
        rev = 0
    else:
        while a2 > 0:
            rev = rev * 10 + (a2 % 10)
            a2 //= 10

    print(a1 + rev)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    global input
    input = sys.stdin.readline

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided samples
assert run("3 14\n") == "44\n", "sample 1"
assert run("27 12\n") == "48\n", "sample 2"
assert run("100 200\n") == "102\n", "sample 3"

# custom cases
assert run("0 0\n") == "0\n", "both zero"
assert run("5 0\n") == "5\n", "reverse of zero"
assert run("0 1200\n") == "21\n", "leading zeros after reversal"
assert run("1000000000 1000000000\n") == "1000000001\n", "maximum values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0` | `0` | Minimum possible values |
| `5 0` | `5` | Reversal of zero |
| `0 1200` | `21` | Leading zeros disappear after reversal |
| `1000000000 1000000000` | `1000000001` | Largest inputs |

## Edge Cases

Consider the input:

```
100 200
```

The algorithm extracts digits `0`, `0`, and `2`. The reversed value becomes `2`, not `002` as a separate object. The final answer is:

```
100 + 2 = 102
```

This matches the expected behavior and avoids mistakes related to leading zeros.

Consider:

```
5 0
```

The second number already equals zero. The reversed value is also zero. The algorithm prints:

```
5
```

No special formatting issues occur.

Consider:

```
0 1200
```

The digit extraction sequence is:

```
0 -> 0
0 -> 0
2 -> 2
1 -> 21
```

The reversed value is `21`, and the final answer is:

```
21
```

This confirms that trailing zeros in the original number become leading zeros after reversal and are discarded automatically when represented as an integer.
