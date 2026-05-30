---
title: "CF 470B - Hexakosioihexekontahexaphobia"
description: "We are given a string consisting solely of digits, and the task is to determine if the number \"666\" appears anywhere as a contiguous sequence inside that string. The output should be \"YES\" if it does, and \"NO\" otherwise."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 470
codeforces_index: "B"
codeforces_contest_name: "Surprise Language Round 7"
rating: 1800
weight: 470
solve_time_s: 66
verified: true
draft: false
---

[CF 470B - Hexakosioihexekontahexaphobia](https://codeforces.com/problemset/problem/470/B)

**Rating:** 1800  
**Tags:** *special  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string consisting solely of digits, and the task is to determine if the number "666" appears anywhere as a contiguous sequence inside that string. The output should be "YES" if it does, and "NO" otherwise. This is a pattern-detection problem rather than a numerical computation problem, so the actual size of the numbers is irrelevant; we treat the input purely as a sequence of characters.

The string can be as short as one digit or as long as 100 digits. Since 100 is a very small number for modern computational limits, we do not need highly sophisticated algorithms. Even an approach that examines every possible substring of length 3 will run efficiently because the maximum number of such substrings is roughly 98.

The non-obvious edge cases involve strings shorter than three digits, where it is impossible to have "666" as a substring. For example, an input of "66" must output "NO". Another edge case is when "666" appears at the very start or end of the string, such as "666123" or "123666". Careless implementations that scan only the middle of the string might miss these occurrences. Strings containing repeated digits longer than three, like "6666", should still yield "YES" because a contiguous substring of length three exists within the repeated sequence.

## Approaches

A naive brute-force approach would involve iterating over every substring of length three in the string and checking if it matches "666". This approach is correct because it explicitly examines every candidate, but it becomes inefficient if the string were much longer than our constraints allow. The number of checks in the worst case is approximately `n-2` comparisons, where `n` is the string length. For a maximum length of 100, this is just 98 checks, which is trivial.

The optimal approach relies on Python's built-in substring search. The `in` operator can check if "666" is contained within the string in linear time relative to the string length. This avoids manual indexing, reduces boilerplate code, and handles all edge cases correctly. The key insight is that this problem reduces to a simple pattern membership check, and Python provides a highly optimized mechanism for that.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal (substring search) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input string and strip any trailing newline or whitespace characters. This ensures we are only working with the digits themselves.
2. Check if the string "666" is contained anywhere in the input string using the `in` operator. This efficiently scans the string in a single pass.
3. If "666" is found, print "YES". Otherwise, print "NO".

Why it works: The algorithm maintains the invariant that we have scanned the string for the specific pattern "666". Since we check the entire string in a linear scan, there is no possibility of missing a valid substring. The correctness stems from the fact that substring membership in Python is exact and respects contiguity, which matches the problem requirement.

## Python Solution

```python
import sys
input = sys.stdin.readline

p = input().strip()

if "666" in p:
    print("YES")
else:
    print("NO")
```

The first line imports `sys` and rebinds `input` to `sys.stdin.readline` for fast input reading. We immediately strip any trailing whitespace to avoid false negatives. The `in` operator performs a linear scan over the string to check for the contiguous sequence "666". Finally, we print the correct response based on whether the substring was found.

## Worked Examples

### Example 1

Input: `123098`

| Step | p | "666" in p | Output |
| --- | --- | --- | --- |
| 1 | "123098" | False | "NO" |

Explanation: The string contains no sequence of three consecutive sixes. The scan confirms that the substring does not exist.

### Example 2

Input: `456666789`

| Step | p | "666" in p | Output |
| --- | --- | --- | --- |
| 1 | "456666789" | True | "YES" |

Explanation: The sequence "666" appears starting at the fourth character. The algorithm correctly identifies it and outputs "YES".

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | The `in` operator checks each position of the string at most once for the substring of length three. |
| Space | O(1) | Only the input string is stored; no extra memory proportional to n is allocated. |

Given the maximum n of 100, this linear scan is extremely fast and fits well within the 2-second limit and 256 MB memory constraint.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    p = input().strip()
    if "666" in p:
        print("YES")
    else:
        print("NO")
    return output.getvalue().strip()

# Provided samples
assert run("123098\n") == "NO", "sample 1"

# Custom cases
assert run("666\n") == "YES", "exact match"
assert run("66\n") == "NO", "too short"
assert run("6666\n") == "YES", "longer repeated sixes"
assert run("123666789\n") == "YES", "in the middle"
assert run("0000000\n") == "NO", "no sixes at all"
assert run("6\n") == "NO", "single character"
assert run("123456789012345678901234567890666\n") == "YES", "end of long string"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "666" | YES | Exact match of substring |
| "66" | NO | String too short to contain 666 |
| "6666" | YES | Overlapping occurrences are handled |
| "123666789" | YES | Substring in the middle |
| "0000000" | NO | No sixes at all |
| "6" | NO | Single-character input |
| "123456789012345678901234567890666" | YES | Substring at end of long string |

## Edge Cases

A string shorter than three characters cannot contain "666", such as "66". The algorithm returns "NO" because the `in` operator checks all contiguous substrings of length three and finds none. For repeated sixes longer than three, like "6666", the algorithm still returns "YES" because the substring "666" exists starting at multiple positions. Substrings at the very beginning or end, such as "666123" or "123666", are correctly detected because the search scans the entire string without skipping any positions.
