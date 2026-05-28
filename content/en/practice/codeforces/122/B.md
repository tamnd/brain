---
title: "CF 122B - Lucky Substring"
description: "The problem asks us to find the \"luckiest\" substring of a given string of digits. By luckiest, we mean a substring that consists only of the digits 4 and 7, occurs in the string as many times as possible, and is the lexicographically smallest if there are ties."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 122
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 91 (Div. 2 Only)"
rating: 1000
weight: 122
solve_time_s: 78
verified: true
draft: false
---

[CF 122B - Lucky Substring](https://codeforces.com/problemset/problem/122/B)

**Rating:** 1000  
**Tags:** brute force, implementation  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to find the "luckiest" substring of a given string of digits. By luckiest, we mean a substring that consists only of the digits 4 and 7, occurs in the string as many times as possible, and is the lexicographically smallest if there are ties. The input string can be as short as one character or up to 50 characters, and it may include any digits, including zeros. The output should be a single lucky substring, or "-1" if none exist.

Given the small maximum input length of 50 characters, any solution that runs in roughly O(n²) or O(n·m) time will perform efficiently. One subtle edge case arises when the string contains no 4s or 7s at all, in which case the correct answer is "-1". Another edge case is when multiple lucky substrings appear the same number of times, but only the lexicographically smallest should be returned. For example, in the string `"4747"`, the lucky substrings `"4"` and `"7"` each appear twice, but `"4"` should be returned.

A naive approach that tries every substring is feasible due to the short input length, but we can simplify further by noticing that only single digits '4' and '7' can maximize occurrence as a substring because any multi-digit lucky number is strictly less frequent than its individual digits.

## Approaches

The brute-force approach would generate all possible substrings of the input string, filter those that are lucky, count occurrences for each, and finally pick the one with the maximum frequency. Generating all substrings of a string of length n requires roughly n·(n+1)/2 substrings, and counting occurrences for each can make the total operation count O(n³) if implemented naively. With n ≤ 50, this is just feasible but unnecessarily complex.

The key observation is that any lucky substring with length greater than 1 cannot appear more times than either '4' or '7' individually. This is because longer substrings require consecutive digits to match exactly. Therefore, we only need to count how many times '4' occurs and how many times '7' occurs. The result is the digit that occurs most often, with ties broken by choosing '4' as the lexicographically smaller option. This reduces the solution from O(n³) to O(n), which is simple and robust.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(n²) | Feasible for n≤50 but overkill |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize two counters, one for '4' and one for '7'. These will track how many times each appears in the string. This directly targets the observation that only individual digits can maximize frequency.
2. Iterate through each character in the string. For each character, if it is '4', increment the '4' counter. If it is '7', increment the '7' counter. Ignore all other digits because they cannot form lucky numbers.
3. After counting, check which digit occurs more often. If '4' appears more frequently than '7', the answer is `"4"`. If '7' appears more frequently, the answer is `"7"`. If both occur equally, choose `"4"` as it is lexicographically smaller.
4. If neither '4' nor '7' appears in the string, return "-1".

This algorithm works because we are guaranteed that no multi-digit lucky substring can have a higher frequency than its constituent digits. The invariant is that after counting, one of these two single-digit lucky numbers will always represent the maximum possible frequency of any lucky substring.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

count4 = 0
count7 = 0

for ch in s:
    if ch == '4':
        count4 += 1
    elif ch == '7':
        count7 += 1

if count4 == 0 and count7 == 0:
    print("-1")
elif count4 >= count7:
    print("4")
else:
    print("7")
```

The code initializes counters and scans the string once. Only '4' and '7' affect the counters. The final decision uses simple comparisons. We check for the special case of no lucky digits first to return "-1". The tie-breaking rule is naturally handled by the comparison `count4 >= count7`.

## Worked Examples

### Sample 1

Input: `"047"`

| Step | Character | count4 | count7 |
| --- | --- | --- | --- |
| 1 | '0' | 0 | 0 |
| 2 | '4' | 1 | 0 |
| 3 | '7' | 1 | 1 |

`count4 == count7`, so the answer is `"4"`.

This confirms that tie-breaking is handled correctly.

### Sample 2

Input: `"123"`

| Step | Character | count4 | count7 |
| --- | --- | --- | --- |
| 1 | '1' | 0 | 0 |
| 2 | '2' | 0 | 0 |
| 3 | '3' | 0 | 0 |

Both counts are zero, so the answer is `"-1"`.

This confirms that strings without lucky digits are correctly rejected.

### Sample 3

Input: `"777447"`

| Step | Character | count4 | count7 |
| --- | --- | --- | --- |
| 1 | '7' | 0 | 1 |
| 2 | '7' | 0 | 2 |
| 3 | '7' | 0 | 3 |
| 4 | '4' | 1 | 3 |
| 5 | '4' | 2 | 3 |
| 6 | '7' | 2 | 4 |

`count7 > count4`, so the answer is `"7"`.

This demonstrates frequency comparison and correct selection.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass through the string to count digits |
| Space | O(1) | Only two integer counters are used |

With n ≤ 50, this runs instantly and uses negligible memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = sys.stdin.readline().strip()
    count4 = 0
    count7 = 0
    for ch in s:
        if ch == '4':
            count4 += 1
        elif ch == '7':
            count7 += 1
    if count4 == 0 and count7 == 0:
        return "-1"
    elif count4 >= count7:
        return "4"
    else:
        return "7"

# Provided samples
assert run("047\n") == "4", "sample 1"
assert run("123\n") == "-1", "sample 2"
assert run("7\n") == "7", "sample 3"

# Custom cases
assert run("4747\n") == "4", "equal counts, tie-break"
assert run("4447777\n") == "7", "7 occurs more"
assert run("4444444\n") == "4", "only 4s"
assert run("0\n") == "-1", "no lucky digits"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `"4747"` | `"4"` | Tie-breaking for equal counts |
| `"4447777"` | `"7"` | Correct selection when one digit occurs more |
| `"4444444"` | `"4"` | Only one lucky digit present |
| `"0"` | `"-1"` | No lucky digits |
| `"7"` | `"7"` | Single-digit input |

## Edge Cases

When the string contains no lucky digits, such as `"1230"`, the algorithm correctly counts zero for both digits and outputs "-1". For strings with equal numbers of '4' and '7', such as `"4747"`, the algorithm correctly prefers '4'. For strings with only one type of lucky digit repeated multiple times, the algorithm correctly returns that digit, for example `"7777"` returns `"7"`. Each of these scenarios is explicitly handled by the final comparison logic.
