---
title: "CF 104021I - Base62"
description: "We are given a number written in an arbitrary positional numeral system with base $x$, where digits are not limited to 0-9 but extend through uppercase and lowercase letters up to a total of 62 distinct symbols."
date: "2026-07-02T04:36:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104021
codeforces_index: "I"
codeforces_contest_name: "The 2019 ICPC Asia Yinchuan Regional Contest"
rating: 0
weight: 104021
solve_time_s: 49
verified: true
draft: false
---

[CF 104021I - Base62](https://codeforces.com/problemset/problem/104021/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a number written in an arbitrary positional numeral system with base $x$, where digits are not limited to 0-9 but extend through uppercase and lowercase letters up to a total of 62 distinct symbols. Our task is to interpret this string as an integer value and then output the same integer represented in another base $y$, using the same 62-symbol alphabet.

In more concrete terms, the input gives us a source base, a target base, and a string encoding of a number in the source base. We must first decode that string into its true integer value, then re-encode that integer into the target base.

The constraints are not large enough to require arbitrary-precision arithmetic libraries, but the presence of bases up to 62 and potentially long input strings means we cannot rely on built-in base conversion functions. We must simulate the conversion carefully using integer arithmetic or manual digit processing.

The main subtlety is that the input number is provided as a string in base $x$, so leading zeros and character mapping matter. A careless implementation often fails by treating characters as raw ASCII values instead of mapping them into their intended numeric values.

A few edge cases are worth making explicit.

If the input number is `"0"`, regardless of base, the correct output is `"0"` in any target base. A naive conversion loop that never handles zero separately may output an empty string.

If the input uses only letters, such as `"FB"` in base 16, it is easy to incorrectly map `'F'` to its ASCII value instead of 15. For example, interpreting `'F' - '0'` gives a meaningless value and breaks the conversion.

If the number is very large, such as a long string in base 62, direct integer parsing via naive exponentiation risks overflow or excessive computation, while a digit-by-digit accumulation remains safe.

## Approaches

A brute-force interpretation would attempt to convert the input string into an integer using repeated exponentiation: for each position, compute $digit \times x^{power}$ and sum them. This is mathematically correct, but computing powers repeatedly leads to unnecessary repeated work. For a string of length $n$, naive exponentiation per digit makes the complexity $O(n^2)$, since each power computation costs up to $O(n)$ if done iteratively.

A more efficient and standard observation is that positional numbers do not need explicit powers. Instead, we can build the value incrementally from left to right. Each new digit shifts the current value by a factor of $x$, then adds the digit. This transforms the conversion into a linear scan.

Once we obtain the integer value, converting it to base $y$ is symmetric. We repeatedly divide by $y$, collecting remainders, which directly correspond to digits in the new base representation. This is the standard greedy decomposition of an integer in a positional system.

The key structural idea is that both conversion directions reduce to repeated application of the same identity: a base representation is just a sequence of multiplications by the base plus additions of digits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Repeated power expansion | O(n²) | O(1) | Too slow |
| Linear parse + repeated division | O(n + log n) | O(1) | Accepted |

## Algorithm Walkthrough

We break the process into two phases: decoding the input string into an integer value, then encoding that integer into the target base.

### 1. Prepare digit mapping

We define a mapping from characters to values: `'0'-'9'` map to 0-9, `'A'-'Z'` map to 10-35, and `'a'-'z'` map to 36-61. This allows constant-time interpretation of each digit.

This mapping is essential because the representation is not ASCII-based arithmetic but a custom alphabet.

### 2. Decode the base-x number into an integer

We initialize an accumulator `value = 0`. For each character `c` in the input string, we convert it to its numeric value `d`, then update:

$$value = value \cdot x + d$$

Each step shifts the current number one digit left in base $x$ and inserts the new digit.

This works because positional notation defines numbers as:

$$(((d_1 \cdot x + d_2)\cdot x + d_3)\cdots)$$

So the recurrence exactly reconstructs the intended value.

### 3. Handle zero explicitly

If the input is `"0"` (or the computed value is zero), we immediately output `"0"`. This avoids producing an empty output during conversion.

### 4. Convert integer to base-y representation

We repeatedly take the remainder modulo $y$ to extract the least significant digit in base $y$. Each remainder is mapped back to a character using the reverse of the digit mapping.

We collect digits in reverse order because modulo extraction produces least significant digits first.

After the loop, we reverse the collected characters to obtain the final representation.

### Why it works

The correctness relies on two invariants. During decoding, after processing the first $i$ characters, `value` equals the integer represented by the prefix of length $i$ in base $x$. During encoding, at each step, the remaining number `value` is exactly the quotient after removing the lower-order digits already emitted, so each modulo operation extracts the correct next digit in base $y$. These properties ensure both phases reconstruct the same integer without ambiguity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def char_to_val(c):
    if '0' <= c <= '9':
        return ord(c) - ord('0')
    if 'A' <= c <= 'Z':
        return ord(c) - ord('A') + 10
    return ord(c) - ord('a') + 36

def val_to_char(v):
    if v < 10:
        return chr(ord('0') + v)
    if v < 36:
        return chr(ord('A') + v - 10)
    return chr(ord('a') + v - 36)

x, y, z = input().split()
x = int(x)
y = int(y)

value = 0
for c in z.strip():
    value = value * x + char_to_val(c)

if value == 0:
    print("0")
    sys.exit()

res = []
while value > 0:
    res.append(val_to_char(value % y))
    value //= y

print("".join(reversed(res)))
```

The decoding loop is the core of the solution. It avoids exponentiation entirely and maintains a rolling value that always represents the parsed prefix in base $x$. The encoding loop mirrors long division: each iteration removes the least significant base-$y$ digit.

A common mistake is forgetting to strip newline characters from the input string, which would break digit parsing. Another is incorrectly handling zero, which would otherwise result in an empty `res` list and incorrect output.

## Worked Examples

### Example 1

Input:

```
16 2 FB
```

We interpret `"FB"` in base 16.

| Step | Character | Digit value | Running value |
| --- | --- | --- | --- |
| 1 | F | 15 | 15 |
| 2 | B | 11 | 15 * 16 + 11 = 251 |

Now convert 251 to base 2.

| Step | Value | Remainder | Next value |
| --- | --- | --- | --- |
| 1 | 251 | 1 | 125 |
| 2 | 125 | 1 | 62 |
| 3 | 62 | 0 | 31 |
| 4 | 31 | 1 | 15 |
| 5 | 15 | 1 | 7 |
| 6 | 7 | 1 | 3 |
| 7 | 3 | 1 | 1 |
| 8 | 1 | 1 | 0 |

Reversing remainders gives `11111011`.

This trace confirms that digit-by-digit construction matches positional evaluation exactly.

### Example 2

Input:

```
62 10 z
```

Here `'z'` is the largest digit value, 61.

| Step | Character | Digit value | Running value |
| --- | --- | --- | --- |
| 1 | z | 61 | 61 |

Now convert 61 to base 10.

| Step | Value | Remainder | Next value |
| --- | --- | --- | --- |
| 1 | 61 | 1 | 6 |
| 2 | 6 | 6 | 0 |

Output is `61`.

This demonstrates handling of single-character inputs and the upper bound digit in base 62.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + log_y N) | Linear scan to decode the string plus repeated division to encode |
| Space | O(1) | Only stores the intermediate integer and output digits |

The input length is bounded such that linear processing is sufficient, and the integer conversion is fast enough under Python’s arbitrary precision integers. The division loop runs in logarithmic time relative to the numeric value, which is well within limits for typical constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    def char_to_val(c):
        if '0' <= c <= '9':
            return ord(c) - ord('0')
        if 'A' <= c <= 'Z':
            return ord(c) - ord('A') + 10
        return ord(c) - ord('a') + 36

    def val_to_char(v):
        if v < 10:
            return chr(ord('0') + v)
        if v < 36:
            return chr(ord('A') + v - 10)
        return chr(ord('a') + v - 36)

    x, y, z = input().split()
    x = int(x)
    y = int(y)

    value = 0
    for c in z.strip():
        value = value * x + char_to_val(c)

    if value == 0:
        return "0"

    res = []
    while value > 0:
        res.append(val_to_char(value % y))
        value //= y

    return "".join(reversed(res))

# provided sample
assert run("16 2 FB") == "11111011"

# minimum size
assert run("2 2 0") == "0"

# single digit max base
assert run("62 10 z") == "61"

# base identity
assert run("10 10 12345") == "12345"

# binary to hex
assert run("2 16 1111") == "F"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 16 2 FB | 11111011 | Multi-digit parsing and binary conversion |
| 2 2 0 | 0 | Zero handling |
| 62 10 z | 61 | Maximum digit value |
| 10 10 12345 | 12345 | Identity conversion |
| 2 16 1111 | F | Power-of-two base conversion |

## Edge Cases

The `"0"` input case is the most important edge case. If we run the decoding loop, `value` remains zero, and without a guard the encoding loop produces an empty list. The explicit zero check ensures we immediately return `"0"`.

For a case like `"0"` in base 62:

Decoding keeps `value = 0`. We skip conversion and output `"0"` directly. This preserves correctness across all bases.

Single-character maximum digit inputs like `"z"` test whether the digit mapping correctly reaches 61. The conversion then reduces to a single modulo operation sequence, and the algorithm still produces correct digits without needing special handling.

These cases confirm that both the mapping layer and the arithmetic conversion layer behave consistently across the full 2-62 range.
