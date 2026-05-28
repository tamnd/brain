---
title: "CF 130B - Gnikool Ssalg"
description: "The problem asks us to reverse a string. Given a sequence of characters, the output should be the same sequence but in the opposite order, so that the first character becomes the last, the second becomes the second-to-last, and so on."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 130
codeforces_index: "B"
codeforces_contest_name: "Unknown Language Round 4"
rating: 1400
weight: 130
solve_time_s: 84
verified: true
draft: false
---

[CF 130B - Gnikool Ssalg](https://codeforces.com/problemset/problem/130/B)

**Rating:** 1400  
**Tags:** *special, implementation, strings  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to reverse a string. Given a sequence of characters, the output should be the same sequence but in the opposite order, so that the first character becomes the last, the second becomes the second-to-last, and so on. The input string is guaranteed to have between 1 and 100 characters, and every character falls within the printable ASCII range from 33 (exclamation mark) to 126 (tilde).

The constraints are mild. With a maximum of 100 characters and a 2-second time limit, any reasonable algorithm that processes each character a constant number of times will run comfortably. We do not need to worry about algorithms with complexities above O(n), since n is small. There are no integer overflow concerns or precision issues because the input is purely textual.

The edge cases here are subtle. A string with a single character should output itself, for example input `A` must return `A`. A string where all characters are identical, like `!!!`, should also return the same sequence. Handling empty strings is unnecessary because the input length is guaranteed to be at least 1. A careful implementation must ensure that no characters are dropped or reordered incorrectly due to off-by-one errors.

## Approaches

The brute-force approach is to manually construct a new string by iterating over the original string from the end to the beginning and appending each character to a new result string. This is correct because it literally reconstructs the reversed sequence character by character. Even though it involves creating a new string, the maximum of 100 iterations ensures the overhead is negligible. In Python, concatenating strings repeatedly is slightly inefficient, but here it is not a concern.

The optimal approach leverages built-in language capabilities. Python strings support slicing with a step argument, which allows us to reverse the string in a single, readable expression: `s[::-1]`. This approach has the same theoretical time complexity as the brute-force method but avoids manual loops, reducing the chance of off-by-one errors and making the code cleaner. The problem’s small input size means we are not constrained by memory or execution time, so this approach is fully acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(n) | Accepted |
| Slicing | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the input string from standard input. This captures the sequence of characters we need to reverse. We strip any trailing newline to avoid it appearing in the output.
2. Reverse the string. Using Python slicing `s[::-1]` traverses the string from the last character to the first, producing a new string with characters in reverse order.
3. Print the reversed string. Output must exactly match the expected sequence, including all characters in their new order.

Why it works: the slicing operation guarantees that each character from the original string appears exactly once in the output, but in the opposite position relative to the start and end. No characters are lost, duplicated, or reordered incorrectly. This preserves the fundamental invariant: the i-th character from the start in the reversed string is the i-th character from the end in the original.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().rstrip()
print(s[::-1])
```

The solution reads the string, removes any trailing newline using `rstrip()`, reverses it with slicing, and prints the result. Stripping the newline is subtle but necessary because otherwise `input()` may include a `\n` at the end, which would appear as an unexpected character in the reversed output.

## Worked Examples

**Sample 1**

Input: `secrofedoc`

| Step | Variable | Value |
| --- | --- | --- |
| Read input | s | 'secrofedoc' |
| Reverse | s[::-1] | 'codeforces' |
| Print | output | 'codeforces' |

This trace confirms that each character is correctly repositioned from last to first.

**Sample 2**

Input: `A`

| Step | Variable | Value |
| --- | --- | --- |
| Read input | s | 'A' |
| Reverse | s[::-1] | 'A' |
| Print | output | 'A' |

This demonstrates handling of the minimal-length input. The single character remains unchanged, confirming edge case handling.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is accessed exactly once during slicing, where n is the string length. |
| Space | O(n) | The reversed string is stored in a new string of the same length as the input. |

Given n ≤ 100, these complexities are trivial to handle within the 2-second time limit and 64 MB memory constraint.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = input().rstrip()
    return s[::-1]

# provided samples
assert run("secrofedoc\n") == "codeforces", "sample 1"

# custom cases
assert run("A\n") == "A", "single character"
assert run("!!!\n") == "!!!", "all identical characters"
assert run("abcdefghijklmnopqrstuvwxyz\n") == "zyxwvutsrqponmlkjihgfedcba", "ordered alphabet"
assert run("1234567890\n") == "0987654321", "numeric characters"
assert run("~!@#$%^&*()\n") == ")(*&^%$#@!~", "special ASCII characters"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| A | A | minimum-length input |
| !!! | !!! | all identical characters |
| abcdefghijklmnopqrstuvwxyz | zyxwvutsrqponmlkjihgfedcba | long sequence of distinct characters |
| 1234567890 | 0987654321 | numeric sequence |
| ~!@#$%^&*() | )(*&^%$#@!~ | special ASCII character handling |

## Edge Cases

For input `A`, the algorithm reads the single character, reverses it (trivially unchanged), and prints it. For input `!!!`, each character is accessed in reverse order, but since all are identical, the output remains `!!!`. Both cases show that the slicing approach handles minimal lengths and repeated characters without error. Tracing step by step confirms that the reversal logic preserves each character's identity and correct position relative to the string's start and end.
