---
title: "CF 102416A - Palindrome"
description: "We need to inspect a collection of positive integers and count how many have the same sequence of digits when read from left to right and from right to left."
date: "2026-08-14T14:43:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102416
codeforces_index: "A"
codeforces_contest_name: "Edinburgh Competition 2019"
rating: 0
weight: 102416
solve_time_s: 87
verified: false
draft: false
---

[CF 102416A - Palindrome](https://codeforces.com/problemset/problem/102416/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We need to inspect a collection of positive integers and count how many have the same sequence of digits when read from left to right and from right to left. For example, `1221` qualifies because its two halves mirror each other, while `1234` does not because the first and last digits differ.

The first input value gives the number of integers, `n`. The following input contains those `n` integers. The answer is a single count: how many of those integers are palindromes.

The number of values is at most 100, and each value can contain up to 51 decimal digits because the upper bound is `10^50`. The numbers can be much larger than the range of ordinary 64 bit integers, so treating them as strings is the natural representation. Even a direct scan of every digit is tiny here. Across all inputs there are at most `100 * 51 = 5100` digits, so any linear-in-the-number-of-digits solution finishes comfortably within the one second limit.

There are a few edge cases that can make an implementation subtly wrong. A single digit is always a palindrome. For example:

```
1
7
```

The correct output is `1`. An implementation that starts by comparing pairs without handling the middle of the number correctly can accidentally reject this case.

The largest possible value also deserves attention:

```
1
100000000000000000000000000000000000000000000000000
```

This value is `10^50`, which has 51 digits and is not a palindrome, so the output is `0`. A solution that stores the value in a fixed-width integer type can overflow before it ever checks the digits.

A palindrome can have either odd or even length. For example:

```
2
12321
1221
```

Both numbers are palindromes, so the output is `2`. A loop that only checks pairs up to a fixed half without correctly handling both parity cases can introduce an off-by-one error.

The input description presents the numbers after `n`, and the sample places them on separate lines. Reading whitespace-separated tokens rather than assuming all numbers are on exactly one line handles both layouts naturally.

## Approaches

The most direct approach is to examine the digits from both ends toward the center. For a number such as `74647`, compare the first and last digits, then the second and fourth digits. If every corresponding pair matches, the number is a palindrome. If any pair differs, it is not. Since there are at most 51 digits in one number, this requires at most `ceil(51 / 2) = 26` digit comparisons per number, or at most 2600 comparisons across all 100 numbers. There is no point at which this brute-force method becomes too slow under the actual constraints.

A simpler implementation uses the same idea through string operations. Convert each input number to a string `s`, construct its reversed form `s[::-1]`, and compare the two strings. A string equals its reverse exactly when its digits read identically in both directions. The slicing operation processes each digit once, so the asymptotic complexity is still linear in the number of digits.

The key observation is that the problem does not require arithmetic on the value of a number. We only care about the order of its decimal digits. Since a value can contain 51 digits, representing it as a string avoids overflow and gives direct access to the property we need to test.

The brute-force approach and the string approach have the same asymptotic complexity. The string version is preferable here because Python already provides a concise and reliable reverse operation, eliminating manual index management and reducing the chance of an off-by-one mistake.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(D) | O(1) extra per number | Accepted |
| Optimal | O(D) | O(D) per number | Accepted |

Here, `D` is the total number of decimal digits in all input numbers. Since `D <= 5100`, both approaches are easily fast enough.

## Algorithm Walkthrough

1. Read `n`, the number of integers to inspect. The remaining whitespace-separated tokens are the actual numbers, so their line arrangement does not matter.
2. Initialize a counter to zero. This counter will represent how many input numbers have been confirmed to be palindromes.
3. For each input number, keep it as a string instead of converting it to an integer. This avoids any overflow concerns and preserves the exact digit sequence.
4. Reverse the string using `s[::-1]`. The resulting string contains the same digits in the opposite order.
5. Compare the original string with its reversed copy. If they are equal, every digit has the same counterpart from the opposite side, so increment the palindrome counter.
6. After all `n` numbers have been processed, print the counter.

### Why it works

For any string `s`, its reverse contains the digits of `s` in exactly the opposite order. The equality `s == s[::-1]` holds precisely when every position has the same digit as its mirrored position. That is exactly the definition of a numeric palindrome. Since every input number is tested independently and the counter is incremented exactly for those satisfying this property, the final counter is the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    tokens = sys.stdin.read().split()

    if not tokens:
        return

    n = int(tokens[0])
    numbers = tokens[1:1 + n]

    answer = 0

    for s in numbers:
        if s == s[::-1]:
            answer += 1

    print(answer)

if __name__ == "__main__":
    solve()
```

The solution reads all whitespace-separated input tokens, which makes it independent of whether the numbers appear on one line or several lines. The first token is converted to an integer because it controls how many numbers should be processed.

Each number remains a string. This is deliberate because `10^50` is outside the range of a typical 64 bit signed integer, while Python strings can represent it directly without any numerical conversion.

The expression `s[::-1]` creates the reversed digit sequence. Python handles the indexing boundaries internally, so there is no manual midpoint calculation and no separate treatment needed for odd and even lengths.

The final condition compares the complete original and reversed strings. A one digit string compares equal to its reverse automatically, while a non-palindrome fails as soon as the resulting strings differ.

## Worked Examples

### Sample 1

The input contains four numbers. We process each one independently.

| Number | Reversed | Palindrome | Answer after processing |
| --- | --- | --- | --- |
| `3` | `3` | Yes | 1 |
| `546` | `645` | No | 1 |
| `74647` | `74647` | Yes | 2 |
| `74565` | `56547` | No | 2 |

The single digit `3` is equal to its reverse, so it contributes one to the answer. `546` fails because its first digit and last digit differ. `74647` is unchanged by reversal, so it contributes another count. Finally, `74565` becomes `56547`, so it is rejected. The final answer is `2`.

### Custom Example

Consider:

```
5
1
1221
12321
1234
100000000000000000000000000000000000000000000000000
```

The trace is:

| Number | Reversed | Palindrome | Answer after processing |
| --- | --- | --- | --- |
| `1` | `1` | Yes | 1 |
| `1221` | `1221` | Yes | 2 |
| `12321` | `12321` | Yes | 3 |
| `1234` | `4321` | No | 3 |
| `100000000000000000000000000000000000000000000000000` | `000000000000000000000000000000000000000000000000001` | No | 3 |

This example covers a one digit number, an even-length palindrome, an odd-length palindrome, an ordinary non-palindrome, and the maximum-size value. The algorithm treats all of them through exactly the same equality test.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(D) | Every input digit is processed a constant number of times while reversing and comparing strings. |
| Space | O(L) | Reversing one number creates a string containing at most `L <= 51` digits. |

For this problem, the total number of digits is at most 5100. The solution therefore performs only a few thousand character operations and uses negligible memory compared with the 256 MB limit.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    tokens = inp.split()

    if not tokens:
        return ""

    n = int(tokens[0])
    numbers = tokens[1:1 + n]

    answer = sum(s == s[::-1] for s in numbers)
    return str(answer)

def run(inp: str) -> str:
    return solve_data(inp).strip()

assert run("""4
3
546
74647
74565
""") == "2", "sample 1"

assert run("""5
1
11
12
121
122
""") == "3", "single digit and short boundary cases"

assert run("""6
1221
12321
1234
9999
1001
101
""") == "5", "odd and even length palindromes"

assert run("""3
100000000000000000000000000000000000000000000000000
999999999999999999999999999999999999999999999999999
123456789012345678901234567890123456789012345678901
""") == "1", "maximum-size values"

assert run("""4
7
8
9
0
""") == "4", "all one-digit values"

| Test input | Expected output | What it validates |
|---|---|---|
| `1, 11, 12, 121, 122` | `3` | Single digits, two-digit values, and odd-length palindromes |
| `1221, 12321, 1234, 9999, 1001, 101` | `5` | Both even and odd palindrome lengths plus a non-palindrome |
| Three 51-digit values | `1` | Maximum allowed digit length and values beyond fixed-width integer ranges |
| `7, 8, 9, 0` | `4` | Minimum-size numbers and the fact that every one-digit string is a palindrome |

## Edge Cases

A one-digit number such as `7` has no distinct pair of digits to compare. Reversing it gives the same string:

```text
1
7
```

The algorithm computes `s = "7"` and `s[::-1] = "7"`, so the equality test succeeds and the output is `1`. This avoids needing a special case for the middle digit.

For the maximum possible value, consider:

```
1
100000000000000000000000000000000000000000000000000
```

The string has 51 digits. Its first digit is `1`, while its last digit is `0`, so the reversed string cannot equal the original. The algorithm produces `0`. Since the value is never converted to a machine integer, there is no overflow issue.

For an even-length palindrome:

```
1
1221
```

The reverse of `1221` is also `1221`, so the answer is `1`. The algorithm does not need to identify a center or decide whether the length is odd or even. String reversal handles both cases uniformly.

For an odd-length palindrome:

```
1
12321
```

The reverse is again `12321`, producing `1`. The middle digit `3` naturally maps to itself. A manual two-pointer solution would stop once the pointers meet, but the string-based solution avoids that boundary entirely.

Finally, consider a number with a mismatch close to the center:

```
1
12331
```

Its reverse is `13321`, so the output is `0`. The outer digits match, and the next pair also matches, but the inner pair differs. Comparing the complete string with its reverse catches mismatches at every possible position, including those that a careless partial comparison could miss.
