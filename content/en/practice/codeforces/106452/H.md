---
title: "CF 106452H - Fill in the Blanks"
description: "The problem hides a simple base-conversion task behind the notation. The given value is written using some base i, and the goal is to print the same number written using another base j. The confusing part is the notation ai."
date: "2026-06-25T09:17:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106452
codeforces_index: "H"
codeforces_contest_name: "UTPC April Fools Contest 2026"
rating: 0
weight: 106452
solve_time_s: 47
verified: true
draft: false
---

[CF 106452H - Fill in the Blanks](https://codeforces.com/problemset/problem/106452/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem hides a simple base-conversion task behind the notation. The given value is written using some base `i`, and the goal is to print the same number written using another base `j`.

The confusing part is the notation `a_i`. It looks like the `i`-th element of a sequence, but it actually means “the representation of a number `a` in base `i`”. A representation in a larger base generally has fewer digits, which matches the observation that increasing the index makes the written value appear smaller. Base `1` is not a valid positional number system, which explains why the first case is special.

The input gives the original base, the target base, and the digits of the number in the original base. The output is the same integer expressed in the target base.

The constraints are designed so that the converted value fits in a normal 64-bit integer. The target base is at most `10`, so every output digit can be printed using a decimal character. This means we only need linear work in the number of input digits. Any approach involving trying possible numbers or building large tables would be unnecessary.

The main edge cases come from base handling. A number like `0` must remain `0` after conversion. A conversion from a base to itself should return the original representation. Leading zeroes in the input representation must not change the value.

For example, if the input is:

```
2 10
1010
```

the correct output is:

```
10
```

A careless solution that treats the input as a decimal number would interpret `1010` as one thousand ten instead of a binary representation.

Another edge case is:

```
10 2
0
```

The correct output is:

```
0
```

A solution that removes all zeroes or assumes there is always a non-zero digit would fail here.

## Approaches

The direct approach is to simulate the meaning of the digits. A number written in base `b` can be evaluated by processing digits from left to right. If the current accumulated value is `x` and the next digit is `d`, the new value is:

`x * b + d`

Repeating this converts the entire representation into its actual integer value. After that, the same value can be written in another base by repeatedly taking the remainder modulo the target base and dividing by the base.

This works because positional notation is exactly repeated multiplication and addition. The brute-force alternative would be to search for a number whose representation matches the given digits, but the possible values grow exponentially with the number of digits, making that approach unusable.

The observation that the true value is bounded lets us avoid arbitrary precision tricks and use ordinary integer arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in number of digits | O(1) | Too slow |
| Base Conversion | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the original base `i`, the target base `j`, and the representation of the number.
2. Convert the representation from base `i` into an integer value. Start with value `0`, and for every digit multiply the current value by `i` before adding the digit.
3. If the resulting value is `0`, print `0` immediately. This handles the only number that does not produce any digits during normal repeated division.
4. Repeatedly divide the value by `j`. Each remainder is the next digit in the target representation, starting from the least significant digit.
5. Reverse the collected digits and print them, because division discovers digits from right to left.

Why it works: the first phase reconstructs the unique integer represented by the input digits. The second phase uses the inverse process of positional notation. Dividing by a base repeatedly gives the digits of that base representation from least significant to most significant, so reversing them produces exactly the required output.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    data = input().split()
    if not data:
        return

    src = int(data[0])
    dst = int(data[1])
    s = data[2]

    value = 0
    for ch in s:
        value = value * src + int(ch)

    if value == 0:
        print(0)
        return

    ans = []
    while value > 0:
        ans.append(str(value % dst))
        value //= dst

    print("".join(reversed(ans)))

if __name__ == "__main__":
    solve()
```

The conversion loop follows the positional notation formula directly. The variable `value` always stores the numeric value of the prefix processed so far.

The zero check is needed because repeatedly dividing zero would produce no digits, while the representation of zero must contain one digit.

During the output conversion, the remainders are generated backwards. For example, converting decimal `13` to base `2` produces remainders `1`, `0`, `1`, `1`, which correspond to the representation read from right to left. Reversing fixes the order.

No indexing is used, so there are no off-by-one issues. Python integers also avoid overflow problems.

## Worked Examples

Example 1:

Input:

```
2 10
1010
```

| Step | Current value | Action |
| --- | --- | --- |
| Read digit 1 | 1 | Start from 0, multiply by 2 and add 1 |
| Read digit 0 | 2 | Previous value 1 becomes 1×2+0 |
| Read digit 1 | 5 | Previous value 2 becomes 2×2+1 |
| Read digit 0 | 10 | Previous value 5 becomes 5×2+0 |

The binary number `1010` represents decimal `10`, so the answer is:

```
10
```

Example 2:

Input:

```
10 2
15
```

| Step | Current value | Action |
| --- | --- | --- |
| Read digit 1 | 1 | Start from 0 |
| Read digit 5 | 15 | Compute 1×10+5 |
| Divide by 2 | remainder 1 | First output digit |
| Divide by 2 | remainder 1 | Second output digit |
| Divide by 2 | remainder 1 | Third output digit |
| Divide by 2 | remainder 1 | Fourth output digit |

The collected digits are reversed from `1111`, which is the binary form of decimal `15`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each input digit is processed once, and conversion to the output base takes a number of steps proportional to the number of output digits. |
| Space | O(n) | The output digits are stored before reversing. |

The constraints allow this linear solution easily. The algorithm only performs arithmetic operations on the actual value and never explores possible numbers.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    data = sys.stdin.readline().split()
    if not data:
        sys.stdin = old_stdin
        return ""

    src = int(data[0])
    dst = int(data[1])
    s = data[2]

    value = 0
    for ch in s:
        value = value * src + int(ch)

    if value == 0:
        result = "0"
    else:
        res = []
        while value:
            res.append(str(value % dst))
            value //= dst
        result = "".join(reversed(res))

    sys.stdin = old_stdin
    return result + "\n"

assert run("2 10\n1010\n") == "10\n", "binary to decimal"
assert run("10 2\n15\n") == "1111\n", "decimal to binary"

assert run("10 10\n00042\n") == "42\n", "leading zeroes"
assert run("8 2\n17\n") == "1111\n", "octal conversion"
assert run("10 10\n0\n") == "0\n", "zero handling"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 10 / 1010` | `10` | Basic conversion from a smaller base |
| `10 2 / 15` | `1111` | Repeated division output construction |
| `10 10 / 00042` | `42` | Ignoring leading zeroes |
| `8 2 / 17` | `1111` | Non-decimal source base |
| `10 10 / 0` | `0` | Special handling of zero |

## Edge Cases

For input:

```
2 10
1010
```

the algorithm first reconstructs the value as `10`. The output base is decimal, so the division phase immediately produces the single digit `10`.

For input:

```
10 2
0
```

the accumulated value remains zero after reading the only digit. The algorithm uses the explicit zero branch and prints `0` instead of producing an empty string.

For input:

```
10 10
00042
```

the conversion phase processes all digits, but the leading zeroes contribute nothing because multiplying the current value by the base keeps the value unchanged before the first non-zero digit appears. The final value is `42`, and the output representation is also `42`.
