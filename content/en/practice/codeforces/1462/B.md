---
title: "CF 1462B - Last Year's Substring"
description: "The problem presents a string of digits and asks whether it can be transformed into the string \"2020\" using at most one contiguous deletion. Polycarp may remove zero or more consecutive characters anywhere in the string."
date: "2026-06-11T02:09:17+07:00"
tags: ["codeforces", "competitive-programming", "dp", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1462
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 690 (Div. 3)"
rating: 800
weight: 1462
solve_time_s: 211
verified: true
draft: false
---

[CF 1462B - Last Year's Substring](https://codeforces.com/problemset/problem/1462/B)

**Rating:** 800  
**Tags:** dp, implementation, strings  
**Solve time:** 3m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem presents a string of digits and asks whether it can be transformed into the string "2020" using at most one contiguous deletion. Polycarp may remove zero or more consecutive characters anywhere in the string. The input consists of multiple test cases, each providing the length of the string and the string itself. The output for each test case is "YES" if such a transformation is possible and "NO" otherwise.

The constraints are moderate: strings have lengths between 4 and 200, and there can be up to 1000 test cases. Because each string is relatively short, a solution can afford to check multiple possible deletions without exceeding time limits. Edge cases include strings that are exactly "2020", strings with "2020" at the start or end, and strings where "2020" could be formed by removing an internal block. For instance, "22020" can become "2020" by deleting the first character, while "20202" can become "2020" by deleting the last character. A naive approach might miss these positions if it only checks for "2020" as a contiguous substring.

## Approaches

A brute-force approach would attempt all possible substrings to delete, reconstruct the remaining string, and compare it to "2020". For a string of length `n`, there are `n*(n+1)/2` substrings, giving a complexity of `O(n^3)` for checking each deletion. This is unnecessary given the small target string "2020" and the structure of the problem.

The key insight is that "2020" has length 4, so at most 4 characters of the original string are relevant to forming it. We only need to check whether the first `k` characters of the string and the last `4-k` characters form "2020" for some `k` from 0 to 4. This covers all scenarios where a single contiguous deletion could leave "2020" intact. The observation reduces the problem from considering all deletions to checking exactly five cases per string: the prefix alone, the suffix alone, and combinations of prefix and suffix totaling four characters.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow |
| Prefix-Suffix Check | O(1) per string | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, read the string `s` and its length `n`.
3. Check if `s` itself is "2020"; if so, print "YES".
4. Otherwise, iterate `k` from 0 to 4, representing the number of characters taken from the start of `s`. Take the first `k` characters and the last `4-k` characters, concatenate them, and compare with "2020".
5. If any combination matches, print "YES"; if none match, print "NO".

The reason this works is that any valid single-deletion transformation of `s` into "2020" must leave some prefix and some suffix of the original string untouched. Since the length of "2020" is fixed at 4, the untouched characters can only be distributed between the start and end. This guarantees that checking all `k` from 0 to 4 covers all possible valid deletions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        s = input().strip()
        target = "2020"
        found = False
        for k in range(5):
            if s[:k] + s[n-(4-k):] == target:
                found = True
                break
        print("YES" if found else "NO")

if __name__ == "__main__":
    solve()
```

The code reads input efficiently using `sys.stdin.readline`. For each string, it checks exactly five potential prefix-suffix combinations against "2020". The slicing operations are safe because `n >= 4` is guaranteed. The loop breaks immediately when a match is found to avoid unnecessary checks.

## Worked Examples

### Example 1

Input string: `"20192020"`

| k | s[:k] | s[n-(4-k):] | Combined | Match? |
| --- | --- | --- | --- | --- |
| 0 | "" | "2020" | "2020" | Yes |

The match occurs immediately with `k=0`. Output is "YES".

### Example 2

Input string: `"22019020"`

| k | s[:k] | s[n-(4-k):] | Combined | Match? |
| --- | --- | --- | --- | --- |
| 0 | "" | "9020" | "9020" |  |
