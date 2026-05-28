---
title: "CF 72H - Reverse It!"
description: "The task is to reverse a number given as a string, taking care of signs and leading zeros. The input can be a very large integer, up to 10,000 digits, possibly with leading zeros."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 72
codeforces_index: "H"
codeforces_contest_name: "Unknown Language Round 2"
rating: 1600
weight: 72
solve_time_s: 208
verified: true
draft: false
---

[CF 72H - Reverse It!](https://codeforces.com/problemset/problem/72/H)

**Rating:** 1600  
**Tags:** *special, implementation  
**Solve time:** 3m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to reverse a number given as a string, taking care of signs and leading zeros. The input can be a very large integer, up to 10,000 digits, possibly with leading zeros. We need to remove those leading zeros first, reverse the remaining digits, and output the result as a string representing an integer. If the number is negative, the reversed number must retain the negative sign. Leading zeros in the reversed number must also be omitted.

The constraints imply we cannot rely on standard integer types, because a 10,000-digit number exceeds any built-in numeric type. Instead, we must treat the number as a string, manipulating characters directly. Since the input size is at most 10,000 characters, an O(n) solution is feasible, but anything worse than O(n log n) could be too slow. Non-obvious edge cases include numbers like "0000123", which should reverse to "321", or negative numbers like "-00120", which should become "-21". A careless implementation could leave trailing zeros after reversing or mishandle the negative sign.

## Approaches

A brute-force approach would attempt to convert the string into an integer, then reverse the digits by repeatedly dividing by 10 and collecting remainders. This works for small numbers, but it fails here because Python integers could handle the size, but in other languages it would overflow. Moreover, the input can have leading zeros which are lost when converting to integer, making direct reversal impossible.

The key observation is that the problem is naturally a string manipulation problem. We can trim leading zeros, check for a negative sign, reverse the substring representing the digits, and then remove any leading zeros that appear after reversal. This reduces the problem to a simple linear pass over the input string. The negative sign is handled separately, ensuring the final output has correct sign placement.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (integer conversion) | O(n) | O(n) | Conceptually correct but fails for very large numbers |
| String Manipulation | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the input string representing the number and remove any surrounding whitespace. This ensures we do not misinterpret accidental spaces as digits.
2. Check if the first character is a negative sign. If it is, store this information and work on the substring excluding the minus sign. This allows uniform processing of digits.
3. Remove leading zeros from the numeric substring. Python’s `lstrip('0')` achieves this. If the string becomes empty, the number is zero.
4. Reverse the cleaned numeric string using slicing `[::-1]`. Reversing a string in-place is O(n) and preserves the order of digits properly.
5. Remove any leading zeros that appear after reversal, using the same method as in step 3. This is crucial for numbers like "1000" which reverse to "0001".
6. Prepend the negative sign if the original number was negative and the reversed string is not empty. This ensures the sign is correct and we do not produce "-0".
7. If the final string is empty, output "0" to represent the zero value. Otherwise, print the reversed string.

The invariant is that after each transformation step, the string represents the current numeric value without invalid leading zeros. This guarantees that reversing and trimming produces the correct integer representation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    s = input().strip()
    if not s:
        print(0)
        return

    negative = s[0] == '-'
    if negative:
        s = s[1:]

    s = s.lstrip('0')
    if not s:
        print(0)
        return

    reversed_s = s[::-1].lstrip('0')
    if negative:
        reversed_s = '-' + reversed_s

    print(reversed_s)

if __name__ == "__main__":
    main()
```

The solution begins by stripping whitespace to prevent errors from extraneous characters. Detecting the negative sign early allows us to handle reversal uniformly. Leading zeros are removed before and after reversal to handle both inputs like "000123" and outputs like "1000". The explicit empty string check ensures we correctly return "0" for inputs that are all zeros.

## Worked Examples

For input "23":

| Step | Variable | Value |
| --- | --- | --- |
| Read input | s | "23" |
| Check negative | negative | False |
| Strip leading zeros | s | "23" |
| Reverse | reversed_s | "32" |
| Output | print | "32" |

This confirms a basic two-digit positive number is reversed correctly.

For input "-00120":

| Step | Variable | Value |
| --- | --- | --- |
| Read input | s | "-00120" |
| Check negative | negative | True |
| Remove sign | s | "00120" |
| Strip leading zeros | s | "120" |
| Reverse | reversed_s | "021" |
| Strip leading zeros after reverse | reversed_s | "21" |
| Prepend negative | reversed_s | "-21" |
| Output | print | "-21" |

This trace demonstrates correct handling of negative numbers and both leading and trailing zeros.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is visited a constant number of times for stripping, slicing, and reversing |
| Space | O(n) | Reversal and substring operations create new strings proportional to input length |

Given n ≤ 10,000, these operations are comfortably within the 4-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# provided sample
assert run("23\n") == "32", "sample 1"
# negative number
assert run("-00120\n") == "-21", "negative number with leading zeros"
# only zeros
assert run("0000\n") == "0", "all zeros"
# large number
assert run("100000000000000000000\n") == "1", "large power-of-ten number"
# single digit
assert run("7\n") == "7", "single digit number"
# negative single digit
assert run("-9\n") == "-9", "negative single digit"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "23" | "32" | Basic positive number reversal |
| "-00120" | "-21" | Negative number with leading zeros |
| "0000" | "0" | Input of all zeros |
| "100000000000000000000" | "1" | Very large number with trailing zeros |
| "7" | "7" | Single-digit input |
| "-9" | "-9" | Single-digit negative input |

## Edge Cases

For input "0000", the algorithm first strips leading zeros, leaving an empty string. The empty string check then prints "0". For input "-00120", after stripping leading zeros the string becomes "120", reversing produces "021", and stripping zeros after reversal produces "21", then the negative sign is prepended to yield "-21". The approach correctly handles both zero-only inputs and numbers with complex leading/trailing zero patterns.
