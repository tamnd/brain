---
title: "CF 1703A - YES or YES?"
description: "We are asked to check whether a three-character string represents the word \"YES\", ignoring letter case. Each test case provides a single string, and we must output a uniform \"YES\" or \"NO\" for each one."
date: "2026-06-09T21:35:19+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1703
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 806 (Div. 4)"
rating: 800
weight: 1703
solve_time_s: 110
verified: true
draft: false
---

[CF 1703A - YES or YES?](https://codeforces.com/problemset/problem/1703/A)

**Rating:** 800  
**Tags:** brute force, implementation, strings  
**Solve time:** 1m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to check whether a three-character string represents the word "YES", ignoring letter case. Each test case provides a single string, and we must output a uniform "YES" or "NO" for each one. The key is that "yEs", "yes", or "YES" are all valid matches, so the solution must be case-insensitive.

The input can include up to 1000 test cases. Each string has exactly three characters, which means we are not dealing with large inputs. Any algorithm that processes each string in constant time will run efficiently within the 1-second time limit. Memory is not a concern since we only need to store the string and a few variables per test case.

A non-obvious edge case arises if someone compares the string directly to "YES" without normalizing the case. For instance, the input "yEs" would incorrectly fail a naive equality check. Similarly, if a string contains non-English letters or more than three characters, it would also fail, but those are outside the stated constraints.

## Approaches

A naive approach is to check each string character individually against the three letters 'Y', 'E', 'S' in both uppercase and lowercase forms. This would involve six comparisons per string. While this works, it is tedious and error-prone because you must remember all case combinations.

A cleaner approach uses the observation that Python provides a case-insensitive comparison via `str.upper()` or `str.lower()`. By converting the input string to uppercase and comparing it to "YES", we handle all valid letter-case combinations in one operation. This reduces the problem to a single comparison per test case, which is both readable and fast.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Character-by-character case check | O(1) per string | O(1) | Accepted, but verbose |
| Convert to uppercase and compare | O(1) per string | O(1) | Accepted, cleanest |

## Algorithm Walkthrough

1. Read the number of test cases `t`. We will iterate over exactly `t` strings, so we know the loop bounds in advance.
2. For each string `s`, convert it to uppercase using `s.upper()`. This ensures that all lowercase letters are mapped to their uppercase equivalents.
3. Compare the converted string to "YES". If they match, output "YES"; otherwise, output "NO".
4. Repeat steps 2-3 for all test cases.

Why it works: Converting the string to uppercase ensures that all variations of letter casing map to a single canonical form. Comparing this canonical form to "YES" guarantees correct detection, because the operation preserves the relative order of characters. Any string that differs from "YES" in letters or order will fail the comparison, producing the correct "NO" response.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    s = input().strip()
    if s.upper() == "YES":
        print("YES")
    else:
        print("NO")
```

The solution first reads the number of test cases using fast I/O. The `.strip()` method removes any trailing newline characters, which is crucial because `input()` includes the newline. `s.upper()` converts all letters to uppercase in a single call, simplifying the comparison. The if-else statement outputs the required string based on the comparison.

## Worked Examples

### Example 1: `YES`

| Step | s | s.upper() | Comparison | Output |
| --- | --- | --- | --- | --- |
| 1 | "YES" | "YES" | "YES" == "YES" | YES |

The string is already uppercase, so it matches immediately.

### Example 2: `yEs`

| Step | s | s.upper() | Comparison | Output |
| --- | --- | --- | --- | --- |
| 1 | "yEs" | "YES" | "YES" == "YES" | YES |

The lowercase letters are converted, and the canonical form matches "YES".

### Example 3: `Noo`

| Step | s | s.upper() | Comparison | Output |
| --- | --- | --- | --- | --- |
| 1 | "Noo" | "NOO" | "NOO" != "YES" | NO |

The canonical form does not match "YES", so the output is "NO".

These traces confirm that both case variations and non-matching strings are handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case requires a single string conversion and comparison, both O(1). For t test cases, total O(t). |
| Space | O(1) | Only a few variables per test case are stored; no extra memory scales with t. |

With t ≤ 1000, the solution runs in negligible time and uses minimal memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    
    t = int(input())
    for _ in range(t):
        s = input().strip()
        if s.upper() == "YES":
            print("YES")
        else:
            print("NO")
    
    return output.getvalue().strip()

# Provided samples
assert run("10\nYES\nyES\nyes\nYes\nYeS\nNoo\norZ\nyEz\nYas\nXES\n") == "YES\nYES\nYES\nYES\nYES\nNO\nNO\nNO\nNO\nNO", "Sample 1"

# Custom cases
assert run("3\nyes\nYES\nYEs\n") == "YES\nYES\nYES", "All case variations"
assert run("2\nNOO\nyeS\n") == "NO\nYES", "Mixed match and mismatch"
assert run("1\nabc\n") == "NO", "Non-YES string"
assert run("1\nYES\n") == "YES", "Exact match"
assert run("1\nYeS\n") == "YES", "Mixed case match"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "3\nyes\nYES\nYEs\n" | "YES\nYES\nYES" | All letter-case variations match |
| "2\nNOO\nyeS\n" | "NO\nYES" | Correctly distinguishes matching and non-matching strings |
| "1\nabc\n" | "NO" | Non-YES strings are rejected |
| "1\nYES\n" | "YES" | Exact match |
| "1\nYeS\n" | "YES" | Mixed-case correct detection |

## Edge Cases

The algorithm handles all non-obvious cases because the conversion to uppercase normalizes letter case. For "yEs", `s.upper()` produces "YES", and the comparison succeeds. For a non-matching input like "Noo", `s.upper()` produces "NOO", which fails the comparison. Trailing or leading whitespace is removed with `.strip()`, so no false negatives occur from newline characters. All three-character strings are correctly evaluated in constant time.
