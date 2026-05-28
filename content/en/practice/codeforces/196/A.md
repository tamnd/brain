---
title: "CF 196A - Lexicographically Maximum Subsequence"
description: "We are given a string composed of lowercase English letters, and our goal is to select a subsequence from it that is lexicographically the largest possible. A subsequence is formed by taking zero or more characters in order without reordering them."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 196
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 124 (Div. 1)"
rating: 1100
weight: 196
solve_time_s: 62
verified: true
draft: false
---

[CF 196A - Lexicographically Maximum Subsequence](https://codeforces.com/problemset/problem/196/A)

**Rating:** 1100  
**Tags:** greedy, strings  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string composed of lowercase English letters, and our goal is to select a subsequence from it that is lexicographically the largest possible. A subsequence is formed by taking zero or more characters in order without reordering them. Lexicographical comparison is just dictionary order, so "bca" is larger than "abc" because the first differing character 'b' is greater than 'a'.

The string can be up to 100,000 characters long. This rules out any solution that explicitly generates all subsequences, because there are 2^n possible subsequences, which is astronomically large. We need an approach that inspects the string in a linear or near-linear fashion.

A naive error would be to try to greedily append the largest remaining character without considering the relative positions. For instance, in the string "ababba", if we just always pick the current maximum character globally and ignore order, we might incorrectly pick the first 'b', then the first 'a', missing that a later 'b' can contribute to a larger subsequence. Correct handling must respect the original order while still selecting characters that maximize lexicographical value.

## Approaches

The brute-force method would consider all subsequences of the string, compare them lexicographically, and choose the maximum. This is correct in principle but infeasible, because with n up to 100,000, generating 2^100000 subsequences is impossible.

The key insight for a faster approach comes from observing the structure of lexicographical order: the maximum subsequence must start with the largest character that appears anywhere, and the rest of the subsequence is obtained by recursively applying the same rule to the suffix that follows that character. This allows us to scan the string from left to right, always appending a character if it is at least as large as any character that occurs later. In practical terms, we can precompute the maximum character for each suffix of the string. This transforms the problem into a linear scan with a simple comparison, giving an O(n) solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the input string and determine its length n. This is needed to create a suffix array of maximum characters.
2. Initialize an array `max_suffix` of length n. This will store, for each position i, the maximum character in the suffix starting at i.
3. Populate `max_suffix` by scanning from right to left. For the last character, `max_suffix[n-1]` is just `s[n-1]`. For each earlier character `i`, set `max_suffix[i]` to the larger of `s[i]` and `max_suffix[i+1]`.
4. Initialize an empty list `result` to build the final subsequence.
5. Scan the string from left to right. At each position i, if `s[i]` is equal to `max_suffix[i]`, append `s[i]` to `result`. This ensures we only include characters that can contribute to the maximum subsequence.
6. Join the list `result` into a string and output it.

Why it works: The invariant maintained is that at every position, we only pick a character if no character to its right is greater. This guarantees that the selected subsequence is lexicographically as large as possible while maintaining order.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
n = len(s)

# Step 1: Compute max_suffix
max_suffix = [''] * n
max_suffix[-1] = s[-1]
for i in range(n - 2, -1, -1):
    max_suffix[i] = max(s[i], max_suffix[i + 1])

# Step 2: Build result subsequence
result = []
for i in range(n):
    if s[i] == max_suffix[i]:
        result.append(s[i])

print(''.join(result))
```

The first loop computes the maximum character for each suffix. This allows the second loop to decide whether to include a character efficiently. Off-by-one errors are avoided by carefully indexing the suffix array from the last character backward. Using a list for `result` and joining at the end prevents inefficient string concatenations.

## Worked Examples

### Sample 1: "ababba"

| i | s[i] | max_suffix[i] | Append? | result |
| --- | --- | --- | --- | --- |
| 0 | a | b | No | "" |
| 1 | b | b | Yes | "b" |
| 2 | a | b | No | "b" |
| 3 | b | b | Yes | "bb" |
| 4 | b | b | Yes | "bbb" |
| 5 | a | a | Yes | "bbba" |

This trace confirms that only characters that are maximal in their suffix are included.

### Sample 2: "abbcabc"

| i | s[i] | max_suffix[i] | Append? | result |
| --- | --- | --- | --- | --- |
| 0 | a | c | No | "" |
| 1 | b | c | No | "" |
| 2 | b | c | No | "" |
| 3 | c | c | Yes | "c" |
| 4 | a | c | No | "c" |
| 5 | b | c | No | "c" |
| 6 | c | c | Yes | "cc" |

The trace shows that characters earlier than a later 'c' are skipped, maintaining order and maximizing lexicographical value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Both loops traverse the string once; comparisons are O(1) |
| Space | O(n) | `max_suffix` stores one character per position; `result` stores up to n characters |

The linear time complexity is well within the limit for n up to 100,000, and memory usage is modest compared to the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = input().strip()
    n = len(s)
    max_suffix = [''] * n
    max_suffix[-1] = s[-1]
    for i in range(n - 2, -1, -1):
        max_suffix[i] = max(s[i], max_suffix[i + 1])
    result = []
    for i in range(n):
        if s[i] == max_suffix[i]:
            result.append(s[i])
    return ''.join(result)

# provided samples
assert run("ababba\n") == "bbba", "sample 1"
# custom cases
assert run("abcde\n") == "e", "strictly increasing"
assert run("edcba\n") == "edcba", "strictly decreasing"
assert run("aaaaa\n") == "aaaaa", "all equal"
assert run("bacbacbac\n") == "ccc", "repeated pattern"
assert run("zxyxz\n") == "zz", "max at start and end"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "abcde" | "e" | picks the last max in increasing order |
| "edcba" | "edcba" | all characters are in descending order, keep all |
| "aaaaa" | "aaaaa" | identical characters, all included |
| "bacbacbac" | "ccc" | repeated pattern, only suffix maxima chosen |
| "zxyxz" | "zz" | max character at multiple positions, only maxima included |

## Edge Cases

In the string "abcde", scanning finds that only 'e' is the suffix maximum, so the subsequence is "e". In "edcba", each character is itself the maximum in its suffix, so the entire string is taken. For repeated characters like "aaaaa", each character is equal to the suffix maximum, so all are included. These examples demonstrate that the algorithm correctly handles increasing, decreasing, and uniform patterns. It also handles maxima occurring at multiple positions, preserving order and correctly skipping lower characters between maxima.
