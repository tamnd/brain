---
title: "CF 1560E - Polycarp and String Transformation"
description: "We are given a string t which is generated from some original string s through a specific sequence of operations. Starting with an empty string t, Polycarp repeatedly appends the current s to t and then removes all occurrences of one chosen character from s."
date: "2026-06-10T12:19:07+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "implementation", "sortings", "strings"]
categories: ["algorithms"]
codeforces_contest: 1560
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 739 (Div. 3)"
rating: 1800
weight: 1560
solve_time_s: 109
verified: false
draft: false
---

[CF 1560E - Polycarp and String Transformation](https://codeforces.com/problemset/problem/1560/E)

**Rating:** 1800  
**Tags:** binary search, implementation, sortings, strings  
**Solve time:** 1m 49s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string `t` which is generated from some original string `s` through a specific sequence of operations. Starting with an empty string `t`, Polycarp repeatedly appends the current `s` to `t` and then removes all occurrences of one chosen character from `s`. The task is to reverse this process: given `t`, reconstruct a possible original `s` and the order in which characters were removed.

The input consists of multiple test cases, each providing a string `t` of up to 500,000 characters. The sum of all string lengths is limited to 500,000, so the algorithm must be linear in the total string length. This immediately rules out any approach that tries to simulate all possible removal orders, because the number of possible orders grows factorially with the number of distinct characters in `s`.

Edge cases are subtle. For example, if `t` contains repeated patterns that cannot be split consistently according to a single removal order, then no valid `s` exists. An example is `t = "nowyouknowthat"`, which cannot correspond to any valid sequence of operations under the rules, so the output should be `-1`. Careless solutions may misinterpret repeated letters and incorrectly propose a string `s` that is inconsistent with the removal rules.

## Approaches

The brute-force approach is to try every possible order of removing characters from `s`. For each order, simulate Polycarp's process and check if the generated `t` matches the input. This works in principle, but it is exponential in the number of distinct letters, making it infeasible when `t` contains even 26 different letters.

The key insight for an efficient solution is to reverse-engineer the process using the frequency and order of characters in `t`. Observe that the last character removed from `s` must appear exactly once in the last segment of `t`. Similarly, the second-to-last character removed appears exactly twice, once in the second-to-last appended segment and once in the final segment. By working backward and counting occurrences, we can determine the order of removals and the length of the original `s`.

The optimal solution is linear because it computes character frequencies, deduces the removal order, and slices the string in a single pass. We do not need to simulate each removal explicitly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(26!) | O(n) | Too slow |
| Optimal | O(n) | O(26 + n) | Accepted |

## Algorithm Walkthrough

1. Count the total occurrences of each character in `t` and note the order of their first appearances from left to right. This order corresponds to the removal order of characters in `s`.
2. Compute the number of occurrences of each character in the original `s` by dividing its total count by the number of times it appears in `t` after appending. If any count is not divisible evenly, then the process is impossible.
3. Determine the length of the original string `s` as the sum of occurrences calculated in step 2.
4. Extract the initial string `s` from the first segment of `t` of this length.
5. Verify that appending `s` and removing characters according to the deduced order recreates `t`. If verification fails at any point, the answer is `-1`.

Why it works: the invariant is that the total count of each character in `t` is a multiple of the number of segments in which it appears. By dividing properly and reconstructing `s` from the first segment, we guarantee a consistent sequence. No other string of the same length can satisfy the frequency constraints and the required append/remove pattern.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    for _ in range(int(input())):
        t = input().strip()
        total_count = {}
        order = []
        for c in t:
```
