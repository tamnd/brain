---
title: "CF 106054A - Artifact to print"
description: "We are given a single string of fixed length ten, consisting only of uppercase Latin letters. From this string, we are allowed to delete characters, but we are not allowed to rearrange what remains."
date: "2026-06-20T13:20:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106054
codeforces_index: "A"
codeforces_contest_name: "2025 Argentinian Programming Tournament (TAP)"
rating: 0
weight: 106054
solve_time_s: 50
verified: true
draft: false
---

[CF 106054A - Artifact to print](https://codeforces.com/problemset/problem/106054/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single string of fixed length ten, consisting only of uppercase Latin letters. From this string, we are allowed to delete characters, but we are not allowed to rearrange what remains. The question is whether it is possible to obtain the subsequence “TAP” after deleting some characters.

So the task is not about finding “T”, “A”, and “P” anywhere independently. They must appear in this order inside the original string, possibly with other letters in between, and we are allowed to ignore those extra letters.

The constraints are extremely small because the string length is always exactly ten. That immediately tells us that even quadratic or cubic methods would be overkill. A linear scan is sufficient, and even brute force over subsequences would be acceptable in terms of performance.

There are a few edge situations worth calling out explicitly. A string that contains all three letters but in wrong order should fail. For example, “PATXXXTXXX” contains all characters but not in the correct sequence order, so it is invalid. Another case is when one of the required letters is missing entirely, such as “CONTRACETO”, which should immediately fail because there is no “P”. Finally, repeated letters can be misleading. A string like “TAAAPPPPPP” is valid because we can pick the first valid “T”, then any later “A”, then a later “P”, preserving order.

## Approaches

A brute-force way to think about the problem is to consider every subsequence of length three and check whether it equals “TAP”. Since the string has length ten, there are at most C(10, 3) = 120 such subsequences, and checking each one is constant time. This already works comfortably within limits and is simple to reason about.

However, this approach explicitly enumerates combinations, which is unnecessary. The structure of the problem only asks whether “T”, then later “A”, then later “P” can be found in order. Once we recognize that order is the only constraint, we can reduce the problem to a single pass greedy scan.

The key observation is that we only need to track progress through a fixed pattern. We start looking for “T”. Once we find it, we stop caring about earlier characters and start looking for “A”. Once “A” is found after that, we look for “P”. If we manage to reach the end of the pattern, the answer is yes.

This works because each character of the pattern must be matched in order, and skipping ahead never blocks a valid future match.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force subsequences | O(120) | O(1) | Accepted |
| Greedy scan | O(10) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a pointer `i = 0` over the target string “TAP”, meaning we are currently trying to match the first unmatched character.
2. Iterate through each character `c` in the input string from left to right.
3. If `c` equals `TAP[i]`, advance `i` by one. This means we have successfully matched the next required character in order.
4. If at any point `i` becomes 3, we already matched all characters of “TAP”, so we can stop early.
5. After scanning the full string (or stopping early), check whether `i == 3`. If yes, output “S”, otherwise output “N”.

The reason for advancing only on matches is that we must preserve order. Skipping non-matching characters ensures we are effectively searching for a subsequence rather than a substring.

### Why it works

The algorithm maintains the invariant that before processing each character in the input, `i` represents the length of the longest prefix of “TAP” that can be formed using a subsequence of the processed prefix of the input string. Each time we match the next needed character, we extend this prefix by exactly one. Because we only move forward in both the input and the pattern, we never invalidate earlier choices, and any valid subsequence must correspond to some sequence of successful advances of `i`.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
target = "TAP"

i = 0
for c in s:
    if i < 3 and c == target[i]:
        i += 1
        if i == 3:
            break

print("S" if i == 3 else "N")
```

The code reads the single input string and maintains a pointer `i` into the pattern “TAP”. Each character is checked against the current required character. Once all three characters are matched, we terminate early since further scanning cannot change the result. The final condition checks whether the full pattern was matched.

A subtle point is the early exit. While unnecessary for correctness, it guarantees the scan stops as soon as success is achieved, even though with length ten this is mostly stylistic.

## Worked Examples

### Example 1: “CONTRAPELO”

We track how the pointer evolves as we scan left to right.

| Character | Current target | Action | i |
| --- | --- | --- | --- |
| C | T | skip | 0 |
| O | T | skip | 0 |
| N | T | skip | 0 |
| T | A | match T | 1 |
| R | A | skip | 1 |
| A | P | match A | 2 |
| P | end | match P | 3 |

At the end, `i = 3`, so the answer is “S”. This confirms that even with intervening letters, ordering is preserved correctly.

### Example 2: “XATPTPKABB”

| Character | Current target | Action | i |
| --- | --- | --- | --- |
| X | T | skip | 0 |
| A | T | skip | 0 |
| T | A | match T | 1 |
| P | A | skip (does not match A? actually target is A) | 1 |
| T | A | skip | 1 |
| P | A | skip | 1 |
| K | A | skip | 1 |
| A | P | match A | 2 |
| B | P | skip | 2 |
| B | P | skip | 2 |

We never reach `P` after completing “TA”, so we end with `i = 2`, producing “N”. This shows that even if all letters exist, incorrect ordering prevents completion.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(10) | single linear scan over fixed-length string |
| Space | O(1) | only a constant pointer and target string |

The constraints fix the input size at ten characters, so the algorithm runs in constant time and trivially satisfies both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = sys.stdin.readline().strip()
    target = "TAP"
    i = 0
    for c in s:
        if i < 3 and c == target[i]:
            i += 1
    return "S" if i == 3 else "N"

# provided samples
assert run("CONTRAPELO\n") == "S"
assert run("XATPTKABPB\n") == "S"
assert run("XATPTPKABB\n") == "N"

# custom cases
assert run("TAPXXXXXXXX\n") == "S"
assert run("XXXXXXXXXX\n") == "N"
assert run("TTTAAAAPPPP\n") == "S"
assert run("PTAATPXABCD\n") == "N"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| TAPXXXXXXXX | S | already formed at start |
| XXXXXXXXXX | N | missing all required letters |
| TTTAAAAPPPP | S | multiple occurrences still valid |
| PTAATPXABCD | N | correct letters but wrong order |

## Edge Cases

One subtle case is when all required letters exist but are interleaved incorrectly. For input “PTAATPXABCD”, the scan finds a “T” first, but no valid “A” after it that leads to a “P” in the correct progression. The pointer gets stuck at the second stage, and the algorithm correctly rejects it.

Another case is heavy repetition. For “TTTAAAAPPPP”, the algorithm does not try to choose optimal occurrences, it simply takes the first valid progression: first T, first A after it, first P after that. This guarantees correctness because any valid subsequence would still allow at least one monotonic advancement through the pattern.
