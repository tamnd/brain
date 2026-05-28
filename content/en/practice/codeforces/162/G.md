---
title: "CF 162G - Non-decimal sum"
description: "We are given several integers written in an arbitrary base between 2 and 36. Digits above 9 are represented with uppercase letters, so in base 16 the digit sequence continues as A, B, C, D, E, F, and in larger bases it may continue up to Z."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 162
codeforces_index: "G"
codeforces_contest_name: "VK Cup 2012 Wild-card Round 1"
rating: 2000
weight: 162
solve_time_s: 106
verified: true
draft: false
---

[CF 162G - Non-decimal sum](https://codeforces.com/problemset/problem/162/G)

**Rating:** 2000  
**Tags:** *special  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several integers written in an arbitrary base between 2 and 36. Digits above 9 are represented with uppercase letters, so in base 16 the digit sequence continues as `A, B, C, D, E, F`, and in larger bases it may continue up to `Z`.

The task is simply to compute the sum of all numbers and print the result in the same base.

The interesting part is that the input numbers are not written in decimal. We must correctly interpret each digit according to the given radix, perform addition, and then convert the final decimal value back into the same numeral system.

The constraints are extremely small. There are at most 10 numbers, and each contains at most 5 digits. Even in the largest base, the maximum value of one number is:

$$36^5 - 1 = 60,\!466,\!175$$

The total sum easily fits inside standard integer types, and Python integers handle values much larger anyway. This means efficiency is not the challenge here. The real challenge is correctly implementing base conversion.

Several edge cases can silently break careless implementations.

A common mistake is mishandling leading zeros. Consider:

```
2
10
0012
0008
```

The correct output is:

```
20
```

The leading zeros are part of the input representation only. They do not affect the numeric value.

Another easy mistake is forgetting that digits above 9 are letters. For example:

```
2
16
A
1
```

The correct output is:

```
B
```

If a solution converts characters using only `'0'` to `'9'`, it will fail on hexadecimal-style digits.

Base 2 also exposes conversion bugs quickly:

```
2
2
1111
1
```

The correct output is:

```
10000
```

This checks whether carries are handled correctly during conversion back to the target base.

One more subtle case appears when the total sum is zero:

```
3
8
0
00
000
```

The correct output is:

```
0
```

A conversion loop that repeatedly divides while the value is positive may accidentally print an empty string instead of `"0"`.

## Approaches

The most direct solution is to manually simulate numeral-system conversion.

For each input string, we can scan digits from left to right and evaluate its decimal value exactly the same way positional notation works:

$$(((d_1)\cdot radix + d_2)\cdot radix + d_3)\cdots$$

After obtaining all decimal values, we add them together.

Finally, we convert the resulting decimal number back into the target base by repeatedly taking the remainder modulo `radix`. Each remainder becomes one output digit.

Because every number has at most 5 digits and there are at most 10 numbers, even a completely manual implementation performs only a few hundred operations.

A brute-force alternative would be digit-by-digit addition directly in the target base, simulating schoolbook addition with carries. That also works because the strings are tiny. We would align all numbers by their least significant digit, sum each column, propagate carries, and construct the answer.

The manual base-conversion approach is simpler because Python already handles arbitrary-size integers safely. Instead of implementing addition logic in every base, we reduce the task to:

1. Convert every input number to decimal.
2. Add them normally.
3. Convert the final value back.

The structure of positional numeral systems makes this reduction natural. Once a number is interpreted as an integer, arithmetic no longer depends on its original representation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force digit simulation | O(n * L) | O(L) | Accepted |
| Optimal conversion approach | O(n * L) | O(L) | Accepted |

Here, `L` is the maximum number of digits, at most 5.

## Algorithm Walkthrough

1. Read `n` and `radix`.
2. Create helper functions for digit conversion.

Characters `'0'` through `'9'` map to values `0` through `9`, while `'A'` through `'Z'` map to `10` through `35`.
3. Convert each input string into decimal form.

Start from value `0`. For every character:

$$value = value \times radix + digit$$

This follows the definition of positional notation.
4. Add all converted values into one integer `total`.
5. Handle the special case `total == 0`.

Output `"0"` immediately. Otherwise the conversion loop would produce an empty string.
6. Convert `total` back into the target base.

Repeatedly:

- take `total % radix`
- convert the remainder into its character representation
- append it
- divide `total //= radix`

The digits appear in reverse order because we extract least significant digits first.
7. Reverse the collected digits and print the result.

### Why it works

The algorithm relies on the positional definition of numeral systems.

When reading a number digit by digit, multiplying the current value by the base shifts all previous digits one position to the left. Adding the new digit inserts the next least significant digit. After processing the entire string, the computed integer equals the mathematical value represented by the original notation.

The reverse conversion also follows positional notation. Taking modulo `radix` extracts the least significant digit, because every higher position is divisible by the base. Repeating division removes processed digits one by one until the entire representation is reconstructed.

Since both conversions exactly preserve numeric value, the final printed string represents the correct sum in the original base.

## Python Solution

```python
import sys
input = sys.stdin.readline

DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def char_to_value(c):
    if '0' <= c <= '9':
        return ord(c) - ord('0')
    return ord(c) - ord('A') + 10

def to_decimal(s, radix):
    value = 0
    for ch in s:
        value = value * radix + char_to_value(ch)
    return value

def from_decimal(x, radix):
    if x == 0:
        return "0"

    result = []

    while x > 0:
        result.append(DIGITS[x % radix])
        x //= radix

    return ''.join(reversed(result))

def solve():
    n = int(input())
    radix = int(input())

    total = 0

    for _ in range(n):
        s = input().strip()
        total += to_decimal(s, radix)

    print(from_decimal(total, radix))

solve()
```

The solution is split into two independent conversion functions.

`to_decimal` interprets a string in the given radix. The multiplication step shifts previously processed digits left by one base position, exactly like constructing numbers by hand.

`from_decimal` performs the inverse transformation. The remainder operation extracts digits from least significant to most significant, so the collected list must be reversed at the end.

The `DIGITS` string provides a clean mapping from numeric digit values back to characters. Index `10` becomes `'A'`, index `15` becomes `'F'`, and so on.

The special handling for zero is essential. Without it, the conversion loop would never execute for `x == 0`, producing an empty string instead of `"0"`.

Python integers already support arbitrary precision, so overflow is never a concern.

## Worked Examples

### Example 1

Input:

```
3
16
F0
20B
004
```

### Converting to decimal

| String | Current digit | Intermediate value |
| --- | --- | --- |
| F0 | F = 15 | 15 |
| F0 | 0 = 0 | 15 × 16 + 0 = 240 |
| 20B | 2 = 2 | 2 |
| 20B | 0 = 0 | 2 × 16 + 0 = 32 |
| 20B | B = 11 | 32 × 16 + 11 = 523 |
| 004 | 0 = 0 | 0 |
| 004 | 0 = 0 | 0 |
| 004 | 4 = 4 | 4 |

Total:

| Values | Sum |
| --- | --- |
| 240 + 523 + 4 | 767 |

### Converting back to base 16

| Current value | Remainder | Digit |
| --- | --- | --- |
| 767 | 15 | F |
| 47 | 15 | F |
| 2 | 2 | 2 |

Digits are collected in reverse order: `F F 2`.

Final answer:

```
2FF
```

This trace shows both directions of conversion working together. Leading zeros in `"004"` disappear naturally because they do not change the numeric value.

### Example 2

Input:

```
2
2
1111
1
```

### Converting to decimal

| String | Current digit | Intermediate value |
| --- | --- | --- |
| 1111 | 1 | 1 |
| 1111 | 1 | 3 |
| 1111 | 1 | 7 |
| 1111 | 1 | 15 |
| 1 | 1 | 1 |

Total:

| Values | Sum |
| --- | --- |
| 15 + 1 | 16 |

### Converting back to base 2

| Current value | Remainder | Digit |
| --- | --- | --- |
| 16 | 0 | 0 |
| 8 | 0 | 0 |
| 4 | 0 | 0 |
| 2 | 0 | 0 |
| 1 | 1 | 1 |

Reversing the digits gives:

```
10000
```

This example demonstrates carry propagation across multiple positions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * L) | Each digit is processed once during parsing and once during output conversion |
| Space | O(L) | The output digit list stores at most the number of digits in the answer |

Here, `n ≤ 10` and `L ≤ 5`, so the actual runtime is tiny. The program performs only a few dozen arithmetic operations and easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def char_to_value(c):
    if '0' <= c <= '9':
        return ord(c) - ord('0')
    return ord(c) - ord('A') + 10

def to_decimal(s, radix):
    value = 0
    for ch in s:
        value = value * radix + char_to_value(ch)
    return value

def from_decimal(x, radix):
    if x == 0:
        return "0"

    result = []

    while x > 0:
        result.append(DIGITS[x % radix])
        x //= radix

    return ''.join(reversed(result))

def solve():
    input = sys.stdin.readline

    n = int(input())
    radix = int(input())

    total = 0

    for _ in range(n):
        total += to_decimal(input().strip(), radix)

    print(from_decimal(total, radix))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided sample
assert run(
"""3
16
F0
20B
004
"""
) == "2FF", "sample 1"

# minimum size
assert run(
"""1
2
0
"""
) == "0", "minimum case"

# carry propagation in binary
assert run(
"""2
2
1111
1
"""
) == "10000", "binary carry"

# leading zeros
assert run(
"""2
10
0012
0008
"""
) == "20", "leading zeros"

# largest digit symbols
assert run(
"""2
36
Z
1
"""
) == "10", "base 36 carry"

# many equal values
assert run(
"""4
16
FF
FF
FF
FF
"""
) == "3FC", "multiple additions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single zero in base 2 | `0` | Correct handling of total sum zero |
| `1111 + 1` in binary | `10000` | Carry propagation across many digits |
| Numbers with leading zeros | `20` | Leading zeros ignored correctly |
| `Z + 1` in base 36 | `10` | Highest legal digit conversion |
| Four copies of `FF` | `3FC` | Repeated addition correctness |

## Edge Cases

### Total sum equals zero

Input:

```
3
8
0
00
000
```

Every number converts to decimal value `0`, so the total is also `0`.

During reverse conversion, the algorithm immediately returns `"0"` before entering the division loop.

Correct output:

```
0
```

Without this special case, the digit list would remain empty.

### Leading zeros

Input:

```
2
10
0012
0008
```

Trace:

| Processed string | Decimal value |
| --- | --- |
| 0012 | 12 |
| 0008 | 8 |

Total becomes `20`.

The leading zeros never affect the accumulated value because multiplying zero by the radix still produces zero.

Correct output:

```
20
```

### Highest supported digit

Input:

```
2
36
Z
1
```

`Z` maps to digit value `35`.

The total becomes:

$$35 + 1 = 36$$

Converting `36` back to base 36 gives:

| Current value | Remainder |
| --- | --- |
| 36 | 0 |
| 1 | 1 |

After reversal, the answer is:

```
10
```

This confirms that letter-digit conversion works correctly at the upper boundary of the radix range.
