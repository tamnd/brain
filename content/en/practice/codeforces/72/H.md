---
title: "CF 72H - Reverse It!"
description: "We are given an integer in string form that can be very large, up to 10,000 digits, and it may include leading zeros. The goal is to reverse its digits while preserving the sign if it is negative and removing any leading zeros from the final reversed number."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 72
codeforces_index: "H"
codeforces_contest_name: "Unknown Language Round 2"
rating: 1600
weight: 72
solve_time_s: 78
verified: true
draft: false
---

[CF 72H - Reverse It!](https://codeforces.com/problemset/problem/72/H)

**Rating:** 1600  
**Tags:** *special, implementation  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an integer in string form that can be very large, up to 10,000 digits, and it may include leading zeros. The goal is to reverse its digits while preserving the sign if it is negative and removing any leading zeros from the final reversed number. For example, an input of `00420` should produce `24`, and an input of `-1200` should produce `-21`.

The constraints indicate that the number may exceed the size of standard numeric types, so we cannot rely on converting it directly to an integer and using arithmetic operations. Instead, we must work with it as a string. The time limit of 4 seconds is generous relative to the input size, so an `O(n)` solution, where `n` is the length of the string, is acceptable. Edge cases arise around leading zeros, negative signs, and inputs that are all zeros. For instance, an input of `0000` should output `0`, not an empty string. Similarly, `-00012` should reverse to `-21`, correctly removing both the negative’s leading zeros and the trailing zeros from the reversed portion.

## Approaches

The brute-force approach is straightforward. We could parse the string character by character, reverse it, handle the negative sign, and then convert it back to a number to drop leading zeros. This works because string reversal is `O(n)` and Python handles arbitrarily large integers, but the conversion to `int` and back might be unnecessary and slightly slower for extremely large strings.

The optimal approach treats the input purely as a string. We first strip any leading zeros, then detect if the number is negative. We then reverse the remaining numeric characters and remove any leading zeros from the reversed string. If the original number was negative, we prepend a `-` to the reversed string. This approach is linear in the length of the input and does not depend on numeric conversion, making it simple, robust, and efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (int conversion) | O(n) | O(n) | Accepted but slightly heavier for max-size input |
| String manipulation | O(n) | O(n) | Accepted, optimal for problem constraints |

## Algorithm Walkthrough

1. Read the input number as a string and strip any surrounding whitespace.
2. Check if the first character is `-`. If it is, mark the number as negative and remove the sign for now. This simplifies string reversal.
3. Remove any leading zeros from the remaining numeric portion. If this leaves an empty string, set it to `0` to handle cases like `0000`.
4. Reverse the string using slicing. The last character becomes the first, the second-to-last becomes second, etc.
5. Remove any leading zeros from the reversed string. If the result is empty, set it to `0`.
6. If the original number was negative and the reversed string is not `0`, prepend a `-` sign.
7. Print the final result.

The invariant here is that at every step, the string accurately represents the integer we intend to reverse, with no leading zeros except for the single zero case. By handling the negative sign separately and using string operations, we ensure correctness even for extremely large inputs.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = input().strip()

negative = n.startswith('-')
if negative:
    n = n[1:]

# remove leading zeros
n = n.lstrip('0')
if not n:
    n = '0'

# reverse digits
reversed_n = n[::-1].lstrip('0')
if not reversed_n:
    reversed_n = '0'

if negative and reversed_n != '0':
    reversed_n = '-' + reversed_n

print(reversed_n)
```

The solution reads the input efficiently and handles all edge cases with string operations. Removing leading zeros before and after the reversal ensures we never output a string like `00421` or `0000`. Handling the negative sign separately avoids mistakes when the number is zero after reversal.

## Worked Examples

### Example 1

Input: `23`

| Step | Value of n | Reversed n | Notes |
| --- | --- | --- | --- |
| Initial | `23` | - | input |
| Strip sign | `23` | - | not negative |
| Remove leading zeros | `23` | - | none to remove |
| Reverse | `32` | `32` | reversed |
| Remove leading zeros | `32` | `32` | no zeros |
| Add negative | `32` | `32` | not negative |

Output: `32`

### Example 2

Input: `-00120`

| Step | Value of n | Reversed n | Notes |
| --- | --- | --- | --- |
| Initial | `-00120` | - | input |
| Strip sign | `00120` | - | negative flagged |
| Remove leading zeros | `120` | - | `00` removed |
| Reverse | `021` | `021` | reversed |
| Remove leading zeros | `21` | `21` | zeros removed |
| Add negative | `21` | `-21` | prepend negative |

Output: `-21`

These traces demonstrate correct handling of leading zeros, negative numbers, and the reversal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each step-stripping zeros, reversing, prepending sign-is linear in string length |
| Space | O(n) | Reversed string and intermediate copies require linear space |

The solution easily handles the input limit of 10,000 characters, staying well within time and memory constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = input().strip()
    negative = n.startswith('-')
    if negative:
        n = n[1:]
    n = n.lstrip('0')
    if not n:
        n = '0'
    reversed_n = n[::-1].lstrip('0')
    if not reversed_n:
        reversed_n = '0'
    if negative and reversed_n != '0':
        reversed_n = '-' + reversed_n
    return reversed_n

# Provided sample
assert run("23\n") == "32", "sample 1"

# Custom test cases
assert run("0000\n") == "0", "all zeros"
assert run("-00012\n") == "-21", "negative with leading zeros"
assert run("1200\n") == "21", "trailing zeros reversed"
assert run("-1000\n") == "-1", "negative, trailing zeros"
assert run("1\n") == "1", "single digit"
assert run("1000000000000000000000\n") == "1", "large input with zeros"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0000` | `0` | All zeros input |
| `-00012` | `-21` | Negative number with leading zeros |
| `1200` | `21` | Trailing zeros removed after reversal |
| `-1000` | `-1` | Negative number, reversed correctly |
| `1` | `1` | Single digit |
| `1000000000000000000000` | `1` | Large number with zeros |

## Edge Cases

An input like `-0000` is handled by first stripping the negative sign and leading zeros, which produces an empty string, then replaced with `0`. After reversal, the output remains `0`, correctly ignoring the negative sign. An input like `0001234000` first becomes `1234000`, then reversed to `0004321`, and stripping leading zeros after reversal yields `4321`, as expected. Negative numbers and single-digit inputs behave correctly because the code treats the negative sign separately and ensures at least one digit remains.
