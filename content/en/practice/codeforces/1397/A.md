---
title: "CF 1397A - Juggling Letters"
description: "We are given a set of strings, and we can move characters freely between any strings, including moving a character from a string back into itself. The goal is to determine if it is possible to rearrange all the characters so that every string ends up identical."
date: "2026-06-11T09:19:22+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 1397
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 666 (Div. 2)"
rating: 800
weight: 1397
solve_time_s: 105
verified: true
draft: false
---

[CF 1397A - Juggling Letters](https://codeforces.com/problemset/problem/1397/A)

**Rating:** 800  
**Tags:** greedy, strings  
**Solve time:** 1m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of strings, and we can move characters freely between any strings, including moving a character from a string back into itself. The goal is to determine if it is possible to rearrange all the characters so that every string ends up identical.

Input consists of multiple test cases. Each test case specifies the number of strings and the strings themselves. The output is a simple "YES" or "NO" depending on whether the rearrangement is possible.

The constraints are moderate. Each test case can have up to 1000 strings, and each string can be up to 1000 characters long, but the sum of all characters across all test cases is capped at 1000. This means we can afford algorithms that are linear in the total number of characters rather than per string or per test case.

An important subtlety arises when characters are unevenly distributed. For example, if we have three strings "a", "a", and "b", the total count of 'a' is 2 and 'b' is 1. There is no way to make three identical strings because each string must ultimately have the same count of each letter. A careless implementation might only check that all strings contain the same set of characters without accounting for frequency, producing a wrong "YES" in this case.

## Approaches

The brute-force approach would be to simulate moving characters between strings until they all match. One could, for example, try to transform every string to match the first string by repeatedly moving characters. This is theoretically correct but infeasible: moving each character individually could take up to 1000 moves per character per string, leading to a worst-case operation count on the order of a million or more, which is unnecessary given the problem constraints.

The key insight is to recognize that the order of characters does not matter. Any character can be inserted anywhere in any string. This reduces the problem to checking the total count of each character across all strings. For a valid solution, each character’s total count must be divisible by the number of strings. If it is not, it is impossible to evenly distribute that character to all strings, and thus impossible to make all strings identical.

This transforms a potentially complex simulation problem into a simple counting problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(total_chars * n) | O(total_chars) | Too slow |
| Optimal | O(total_chars) | O(26) | Accepted |

## Algorithm Walkthrough

1. Initialize a counter for each letter of the alphabet, representing the total count of that letter across all strings in the current test case. This is done using an array of size 26 indexed by the letters 'a' through 'z'.
2. Iterate through each string. For each character in the string, increment the corresponding counter. At the end of this iteration, the counter holds the total occurrences of each character across all strings.
3. Check each counter value. If every counter is divisible by the number of strings `n`, it is possible to redistribute the characters evenly, so print "YES". If any counter is not divisible by `n`, print "NO" immediately. This works because divisibility ensures that every string can receive the exact same number of each character.

Why it works: the invariant is that redistributing characters is unconstrained; therefore, the only requirement for equality is that each string receives an equal share of each letter. If the total count is divisible by the number of strings, a valid redistribution exists; otherwise, it does not.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    counts = [0] * 26  # total counts of 'a' to 'z'
    
    for _ in range(n):
        s = input().strip()
        for ch in s:
            counts[ord(ch) - ord('a')] += 1
    
    possible = all(count % n == 0 for count in counts)
    print("YES" if possible else "NO")
```

The solution reads the number of test cases and processes each independently. For each test case, it counts occurrences of each letter. Using the modulo operator ensures that each character can be evenly distributed. The choice of an array of size 26 is safe and efficient, avoiding the overhead of dictionaries. Stripping input is necessary to remove trailing newlines.

## Worked Examples

### Example 1

Input strings: "caa", "cbb"

| Letter | Total count | Divisible by 2? |
| --- | --- | --- |
| a | 2 | Yes |
| b | 2 | Yes |
| c | 2 | Yes |

All counts divisible by 2, output: YES. Characters can be rearranged to form "cab" in both strings.

### Example 2

Input strings: "cba", "cba", "cbb"

| Letter | Total count | Divisible by 3? |
| --- | --- | --- |
| a | 2 | No |
| b | 4 | No |
| c | 3 | Yes |

Some counts not divisible by 3, output: NO.

This confirms the algorithm correctly identifies when redistribution is impossible due to indivisible character counts.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total_chars) | We iterate over all characters exactly once per test case |
| Space | O(26) | Fixed-size array for counting letters |

Given the sum of all string lengths ≤ 1000, this runs well under the time limit. Space is trivial.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # call solution
    t = int(input())
    for _ in range(t):
        n = int(input())
        counts = [0] * 26
        for _ in range(n):
            s = input().strip()
            for ch in s:
                counts[ord(ch) - ord('a')] += 1
        possible = all(count % n == 0 for count in counts)
        print("YES" if possible else "NO")
    return output.getvalue().strip()

# Provided samples
assert run("4\n2\ncaa\ncbb\n3\ncba\ncba\ncbb\n4\nccab\ncbac\nbca\nacbcc\n4\nacb\ncaf\nc\ncbafc\n") == "YES\nNO\nYES\nNO"

# Custom test cases
assert run("1\n1\na") == "YES", "single string, always YES"
assert run("1\n2\na\na") == "YES", "already equal strings"
assert run("1\n3\na\nb\nc") == "NO", "distinct single characters cannot be equal"
assert run("1\n3\naaa\naaa\naaa") == "YES", "all equal large strings"
assert run("1\n2\nabc\ndef") == "NO", "cannot redistribute to make equal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 string "a" | YES | Minimal input case |
| 2 strings "a", "a" | YES | Already equal strings |
| 3 strings "a", "b", "c" | NO | Single characters not redistributable |
| 3 strings "aaa", "aaa", "aaa" | YES | All equal strings with multiple letters |
| 2 strings "abc", "def" | NO | No common letters, impossible |

## Edge Cases

A case with one string always outputs YES. If the total character counts of a letter are divisible by the number of strings, the algorithm correctly handles strings of differing lengths. For example, "abc", "a" gives counts a=2, b=1, c=1. With n=2, b and c are not divisible by 2, output: NO. This confirms the algorithm properly accounts for both character distribution and the number of strings.
