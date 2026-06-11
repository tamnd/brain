---
title: "CF 1185B - Email from Polycarp"
description: "The task is to verify whether a typed word t could plausibly result from pressing the keys of a word s on a keyboard that occasionally repeats letters. Each letter in s must appear in order in t, but it may appear one or more times consecutively."
date: "2026-06-12T00:53:28+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1185
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 568 (Div. 2)"
rating: 1200
weight: 1185
solve_time_s: 86
verified: true
draft: false
---

[CF 1185B - Email from Polycarp](https://codeforces.com/problemset/problem/1185/B)

**Rating:** 1200  
**Tags:** implementation, strings  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to verify whether a typed word `t` could plausibly result from pressing the keys of a word `s` on a keyboard that occasionally repeats letters. Each letter in `s` must appear in order in `t`, but it may appear one or more times consecutively. For instance, if `s` is "hello", then "helloo" or "hheelloo" are valid outputs, but "helo" or "hlllloo" are not because either letters are missing or the order is violated.

The input consists of multiple word pairs, up to 100,000, with each word having up to 1,000,000 characters. However, the total length of all `s` words combined does not exceed 1,000,000, and similarly for all `t` words. This means our solution cannot have nested loops that iterate over the lengths of `s` and `t` in the worst case, as that could result in up to 10^12 operations. Linear scans of each word pair are acceptable because the total number of characters processed will be at most 2 * 10^6, which is feasible within the time limit.

Non-obvious edge cases include situations where `t` contains additional letters that do not correspond to consecutive repeats of `s`. For example, `s = "abc"` and `t = "aabbccx"` should return NO, because the extra 'x' cannot be generated from `s`. Another subtle case is when `t` is missing a letter entirely, for instance `s = "aaa"` and `t = "aa"`. Here the output should also be NO because each letter in `s` must appear at least once in order.

## Approaches

A naive approach would try to match every character in `s` to every character in `t` using nested loops. For each character in `s`, one would scan forward in `t` until a match is found, then repeat for the next character. This is correct logically, but if `s` has length m and `t` has length n, the worst case complexity is O(m * n). With maximum word lengths, this could be on the order of 10^12 operations, which is far too slow.

The key insight for an optimal approach is to realize that both `s` and `t` can be scanned simultaneously with two pointers. We keep a pointer `i` in `s` and a pointer `j` in `t`. When `s[i] == t[j]`, we move `i` and `j` forward. If `t[j]` equals `t[j-1]`, we only move `j` forward because it could be a repeated key press. Any deviation from this pattern means `t` cannot result from `s`. This reduces the problem to a linear scan through `t` and `s`, with complexity proportional to the sum of their lengths.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m*n) | O(1) | Too slow |
| Two-pointer scan | O(m+n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize two pointers `i` and `j` to zero. `i` will traverse `s` and `j` will traverse `t`.
2. While `j` has not reached the end of `t`:

a. If `i` has reached the end of `s`, check if the remaining characters in `t` are all equal to `t[j-1]`. If not, return NO.

b. If `s[i] == t[j]`, move both `i` and `j` forward.

c. Else if `j > 0` and `t[j] == t[j-1]`, move `j` forward. This accounts for repeated characters caused by the broken keyboard.

d. Otherwise, return NO, because `t[j]` does not match the current character in `s` or any valid repetition.
3. After the loop, check if `i` has reached the end of `s`. If not, return NO because some characters of `s` were not used.
4. If all checks pass, return YES.

Why it works: At each step, `i` and `j` maintain the invariant that all characters before `i` in `s` have been matched in order to characters before `j` in `t`, allowing for repetitions. If any character in `t` violates this pattern, the algorithm immediately returns NO. The scan guarantees that each character in `s` is matched at least once and in order, and `t` may have additional repeated characters.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_be_typed(s: str, t: str) -> str:
    i, j = 0, 0
    while j < len(t):
        if i < len(s) and s[i] == t[j]:
            i += 1
            j += 1
        elif j > 0 and t[j] == t[j-1]:
            j += 1
        else:
            return "NO"
    return "YES" if i == len(s) else "NO"

n = int(input())
results = []
for _ in range(n):
    s = input().strip()
    t = input().strip()
    results.append(can_be_typed(s, t))

print("\n".join(results))
```

The function `can_be_typed` implements the two-pointer scan described above. It carefully handles boundaries: `i` may reach the end of `s` while `j` is still in `t`, and repeated letters at the end of `t` are allowed. The main loop ensures the pointers never go out of bounds, and final check confirms all of `s` was consumed.

## Worked Examples

Trace Sample 1:

| i | j | s[i] | t[j] | Action |
| --- | --- | --- | --- | --- |
| 0 | 0 | h | h | match, i++, j++ |
| 1 | 1 | e | e | match, i++, j++ |
| 2 | 2 | l | l | match, i++, j++ |
| 3 | 3 | l | l | match, i++, j++ |
| 4 | 4 | o | o | match, i++, j++ |
| 5 | 5 | - | - | end, YES |

Trace second pair "hello" -> "helloo":

| i | j | s[i] | t[j] | Action |
| --- | --- | --- | --- | --- |
| 0-4 | 0-4 | h,e,l,l,o | h,e,l,l,o | matches |
| 5 | 5 | - | o | t[j] == t[j-1], j++ |
| 5 | 6 | - | - | end, YES |

These traces show the algorithm correctly handles repeated characters and confirms the invariant.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total length of all s + total length of all t) | Each character in `s` and `t` is visited at most once by the pointers |
| Space | O(1) extra | Only pointers and local variables are used; output list is negligible |

Given the constraints that total lengths are at most 10^6, the algorithm will run efficiently within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    results = []
    for _ in range(n):
        s = input().strip()
        t = input().strip()
        results.append(can_be_typed(s, t))
    return "\n".join(results)

# Provided samples
assert run("4\nhello\nhello\nhello\nhelloo\nhello\nhlllloo\nhello\nhelo\n") == "YES\nYES\nNO\nNO", "sample 1"

# Custom cases
assert run("1\na\naaa\n") == "YES", "repeated single character"
assert run("1\nabc\naabbcc\n") == "YES", "all repeated in order"
assert run("1\nabc\nacb\n") == "NO", "wrong order"
assert run("1\nabc\nab\n") == "NO", "missing last char"
assert run("1\nx\ny\n") == "NO", "different characters"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| a -> aaa | YES | single character repetition |
| abc -> aabbcc | YES | multiple letters repeated |
| abc -> acb | NO | order of letters matters |
| abc -> ab | NO | missing letters |
| x -> y | NO | completely different characters |

## Edge Cases

For the input `s = "aaa"`, `t = "aa"`, the algorithm starts with `i = 0, j = 0`. It matches the first 'a', increments both pointers, then matches the second 'a', increments both, and finds `j` at the end of `t` while `i` is still at 2. Since `i != len(s)`, it returns NO, correctly identifying that `t` does not cover all of `s`.

For `s = "abc"` and `t = "aabbccx"`, the scan successfully matches 'a','b','c' and the
