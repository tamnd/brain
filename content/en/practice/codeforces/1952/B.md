---
title: "CF 1952B - Is it stated?"
description: "We are given a list of strings, each consisting of lowercase English letters, and for each string, we are asked to answer either \"YES\" or \"NO\" based on a hidden pattern."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "strings"]
categories: ["algorithms"]
codeforces_contest: 1952
codeforces_index: "B"
codeforces_contest_name: "April Fools Day Contest 2024"
rating: 0
weight: 1952
solve_time_s: 41
verified: true
draft: false
---

[CF 1952B - Is it stated?](https://codeforces.com/problemset/problem/1952/B)

**Rating:** -  
**Tags:** *special, strings  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of strings, each consisting of lowercase English letters, and for each string, we are asked to answer either "YES" or "NO" based on a hidden pattern. Observing the sample inputs and outputs, the strings "it", "submit", and "timelimitexceeded" yield "YES", while others like "is", "stated", or "ac" yield "NO". By examining these, the pattern emerges: the string is marked "YES" if it contains the substring "it" anywhere within it. All other strings that lack this substring are marked "NO".

The input constraints are modest: up to 100 strings, each of length up to 100. This means a total of 10,000 characters to check in the worst case, so any solution that scans each string once is fast enough. We can afford a simple linear scan per string.

Non-obvious edge cases include strings that are very short or where "it" appears at the edges. For instance, "it" itself should return "YES", while "ti" should return "NO". Also, strings may contain multiple occurrences of "it", but the presence of at least one is sufficient.

## Approaches

The naive approach is to check each possible substring of length two in every string and see if it equals "it". This works because every two-character substring is a candidate for matching, but it requires scanning nearly the entire string for each check. In the worst case, this is O(n^2) for a string of length n. For our constraints, this is still acceptable, but it is unnecessary.

The optimal approach uses Python's built-in substring search. We can simply check `"it" in s` for each string `s`. This is linear in the length of the string because substring search is implemented efficiently in Python, and it captures the problem's logic directly without constructing unnecessary substrings. The brute-force check is correct but slow for larger strings; using Python's native substring test reduces overhead and is clean and readable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all substrings) | O(n^2) per string | O(1) | Accepted but unnecessary |
| Optimal (`"it" in s`) | O(n) per string | O(1) | Accepted and clean |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each string `s` in the test cases:

1. Check if `"it"` is a substring of `s`.
2. If yes, print "YES".
3. If no, print "NO".

The key insight is that the problem reduces to a simple substring check. Python's `in` operator iterates through the string efficiently and stops as soon as the substring is found, guaranteeing linear time per string.

Why it works: The algorithm relies on the invariant that for each string, if "it" appears anywhere, it will be detected exactly once by the substring check. The presence or absence of other letters does not affect the outcome. There is no ambiguity because the task is solely dependent on this fixed substring.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    s = input().strip()
    if "it" in s:
        print("YES")
    else:
        print("NO")
```

The code first reads the number of test cases. Each string is stripped of trailing newlines to avoid false negatives when checking for the substring. The substring check `"it" in s` captures the core logic efficiently, and the print statement outputs the result immediately.

## Worked Examples

### Example 1

Input string: `"it"`

| Step | s | `"it" in s` | Output |
| --- | --- | --- | --- |
| 1 | "it" | True | YES |

The substring matches exactly, and the output is "YES".

### Example 2

Input string: `"submit"`

| Step | s | `"it" in s` | Output |
| --- | --- | --- | --- |
| 1 | "submit" | True | YES |

The substring appears at the end; the algorithm still detects it correctly.

### Example 3

Input string: `"is"`

| Step | s | `"it" in s` | Output |
| --- | --- | --- | --- |
| 1 | "is" | False | NO |

No match is found, so the output is "NO".

These traces demonstrate that the algorithm correctly handles strings of length 2, strings containing "it" at the start, middle, or end, and strings without the substring.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T * n) | Each of the T strings is scanned once; n is the string length |
| Space | O(1) | Only a few variables are used; no extra data structures proportional to input size |

Given the constraints (T ≤ 100, n ≤ 100), the maximum number of operations is roughly 10,000, which is well within the 2-second time limit.

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
        if "it" in s:
            print("YES")
        else:
            print("NO")
    return output.getvalue().strip()

# Provided sample
assert run("""10
is
it
stated
submit
ac
accepted
wa
wronganswer
tle
timelimitexceeded""") == """NO
YES
NO
YES
NO
NO
NO
NO
NO
YES"""

# Custom: minimum input
assert run("1\ni") == "NO", "single character string"

# Custom: substring at start
assert run("1\nitstart") == "YES", "substring at start"

# Custom: substring at end
assert run("1\nendit") == "YES", "substring at end"

# Custom: substring in middle
assert run("1\nmiddleitmiddle") == "YES", "substring in middle"

# Custom: multiple occurrences
assert run("1\nititisit") == "YES", "multiple occurrences"

# Custom: no occurrence
assert run("1\nxyz") == "NO", "no occurrence"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `"i"` | NO | Single-character string cannot contain "it" |
| `"itstart"` | YES | Substring at start |
| `"endit"` | YES | Substring at end |
| `"middleitmiddle"` | YES | Substring in middle |
| `"ititisit"` | YES | Multiple occurrences still yield YES |
| `"xyz"` | NO | String without substring |

## Edge Cases

For `"i"`, the algorithm checks `"it" in "i"` and returns False because the string is too short, yielding "NO". For `"itstart"`, the substring appears at the beginning, and `"it" in s` detects it immediately, returning "YES". For `"endit"`, the substring is at the end; Python scans until the match is found. For `"middleitmiddle"`, the substring in the middle is detected correctly. For `"ititisit"`, only one match is needed, and the algorithm returns "YES" even if there are multiple occurrences. For `"xyz"`, no match occurs, so the algorithm correctly outputs "NO". All edge cases are handled directly by the substring check without additional logic.
