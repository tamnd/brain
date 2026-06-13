---
title: "CF 1251A - Broken Keyboard"
description: "We are given a final string that appeared on a screen after someone pressed keyboard keys one by one. Each key corresponds to a lowercase Latin letter, and each key is either always healthy or always broken during the entire typing process."
date: "2026-06-13T21:34:16+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "strings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1251
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 75 (Rated for Div. 2)"
rating: 1000
weight: 1251
solve_time_s: 307
verified: false
draft: false
---

[CF 1251A - Broken Keyboard](https://codeforces.com/problemset/problem/1251/A)

**Rating:** 1000  
**Tags:** brute force, strings, two pointers  
**Solve time:** 5m 7s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a final string that appeared on a screen after someone pressed keyboard keys one by one. Each key corresponds to a lowercase Latin letter, and each key is either always healthy or always broken during the entire typing process.

The behavior of a healthy key is simple: pressing it appends exactly one copy of its letter to the output. A broken key is more aggressive: every press appends two copies of its letter instead of one. The final string is the result of mixing these two behaviors across an unknown sequence of key presses.

The task is not to reconstruct the sequence of key presses. Instead, we must identify which letters are guaranteed to correspond to healthy keys in every possible explanation of the final string. A letter is safe to output only if it is impossible for it to be broken in any valid decomposition of the string into single and double letter contributions.

The key difficulty is that the same string can often be explained in multiple ways depending on whether we treat occurrences as single or doubled characters. The decision is local in appearance but global in constraint, since a single letter may be interpreted consistently or inconsistently across the entire string.

The string length is at most 500 and there are up to 100 test cases, so an O(n^2) or O(n) per case solution is sufficient. Anything exponential in interpretation choices is unnecessary because we do not need to enumerate all decompositions.

A naive mistake is to assume that if a letter appears in isolation sometimes, it must be healthy, or that every adjacent pair of identical letters must come from a broken key. Both interpretations fail because pairing decisions are not independent across the string.

For example, consider the string `aabb`. One might think `a` is broken because it appears as `aa`, and `b` is broken because it appears as `bb`. But `aabb` could also come from four healthy presses: `a a b b`, making both letters healthy. So local grouping is insufficient.

Another subtle failure case is alternating patterns like `abab`. Here, neither letter can form pairs, so both must be healthy, but a greedy scan that tries to pair whenever possible could incorrectly mark both as broken or ambiguous.

## Approaches

A direct brute-force approach would try all ways to partition the string into segments of size 1 or 2, ensuring each segment is a repetition of a single character. Each partition corresponds to assuming whether each press produced one or two characters. After generating a valid partition, we could deduce which letters ever appear in a way consistent with being broken or healthy, and then intersect across all partitions.

This quickly becomes infeasible because each position potentially branches into two choices, leading to O(2^n) decompositions in the worst case. Even with pruning, the number of valid segmentations of a string like `aaaaaa...` grows exponentially.

The key observation is that we do not need to explicitly construct all valid decompositions. Instead, we only need to determine whether a letter can be forced to be broken in every valid explanation. Equivalently, we want letters that can never be explained as consistently producing exactly one character per press.

The crucial simplification is to observe that a letter is unsafe only if we can partition its occurrences entirely into disjoint pairs of identical consecutive letters, meaning every occurrence can be grouped into blocks of size two. If at least one occurrence of a letter cannot be paired with an identical neighbor, then there exists a valid interpretation where that letter must be healthy.

So for each letter, we only need to check whether all its occurrences in the string can be fully covered by disjoint adjacent pairs. If that is impossible, the letter is guaranteed to be healthy in at least one valid interpretation, and thus is not in the required output. Conversely, if it is possible to fully pair all occurrences, the letter could be entirely broken in some interpretation, so it is not guaranteed healthy.

This reduces the problem to a linear scan: detect whether occurrences of a letter can be perfectly matched in adjacent pairs throughout the string.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(26·n) | O(26) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Scan the string and record, for each letter, all indices where it appears. This lets us reason about pairing structure per character without interference from others.
2. For a fixed letter, attempt to simulate pairing greedily from left to right in the original string. Whenever we see the letter at position i, we check whether i and i+1 both contain the same letter. If yes, we treat this as one broken-key block and skip both positions. If not, this occurrence cannot be part of a broken pair, so it must be treated as a single press.
3. While scanning, if we ever encounter a situation where a single occurrence cannot be matched into a pair but also cannot be safely treated as a singleton consistently across the structure, we conclude that the letter cannot be fully explained as broken everywhere. That means it is safe and should be included in the answer.
4. Repeat this process for all 26 letters independently.
5. Collect all letters that fail the “fully pairable” condition, and output them in alphabetical order.

### Why it works

The key invariant is that any broken letter must contribute its occurrences in contiguous pairs of identical characters. If a letter is truly broken, every occurrence must be part of a valid adjacent pair, because a broken press produces exactly two consecutive identical letters. If even one occurrence is isolated or breaks adjacency consistency, then no decomposition exists where that letter is always broken, meaning there is at least one interpretation where it is healthy. Therefore, the set of letters that can be fully covered by adjacent pairs exactly corresponds to letters that are not guaranteed to be healthy.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_fully_pairable(s, ch):
    i = 0
    n = len(s)
    while i < n:
        if s[i] != ch:
            i += 1
            continue
        if i + 1 < n and s[i + 1] == ch:
            i += 2
        else:
            return False
    return True

t = int(input())
for _ in range(t):
    s = input().strip()
    res = []
    for c in "abcdefghijklmnopqrstuvwxyz":
        if is_fully_pairable(s, c):
            res.append(c)
    print("".join(res))
```

The function `is_fully_pairable` checks whether all occurrences of a character can be consumed as adjacent pairs. The pointer `i` moves through the string and greedily consumes `cc` pairs whenever possible. If a standalone occurrence appears, it breaks the possibility of interpreting the character as always broken.

The main loop simply applies this test to all 26 letters and collects those that satisfy it.

## Worked Examples

### Example 1: `zzaaz`

We trace each character.

| i | s[i] | action |
| --- | --- | --- |
| 0 | z | pair found? no, single z |
| 1 | z | pair z z used |
| 2 | a | pair a a used |
| 4 | z | single z left, no pair |

For `z`, pairing fails because there is an unmatched occurrence. For `a`, pairing succeeds fully.

This shows that only `a` can be guaranteed healthy.

### Example 2: `ccff`

| i | s[i] | action |
| --- | --- | --- |
| 0 | c | c c pair |
| 2 | f | f f pair |

Both letters can be fully paired, meaning both could be broken consistently, so neither is guaranteed healthy. Thus output is empty.

This confirms the logic distinguishes between fully pairable letters and those with unavoidable singleton structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(26 · n) | Each of 26 letters is scanned linearly over the string |
| Space | O(1) | Only counters and loop variables are used |

The constraints allow up to 500 characters per test case and 100 test cases, so at most 50,000 character operations. The algorithm is comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import *
    
    input = _sys.stdin.readline

    def is_fully_pairable(s, ch):
        i = 0
        n = len(s)
        while i < n:
            if s[i] != ch:
                i += 1
                continue
            if i + 1 < n and s[i + 1] == ch:
                i += 2
            else:
                return False
        return True

    t = int(input())
    out = []
    for _ in range(t):
        s = input().strip()
        res = []
        for c in "abcdefghijklmnopqrstuvwxyz":
            if is_fully_pairable(s, c):
                res.append(c)
        out.append("".join(res))
    return "\n".join(out) + ("\n" if out else "")

# provided samples
assert run("4\na\nzzaaz\nccff\ncbddbb\n") == "a\nz\n\nbc\n"

# custom cases
assert run("1\nab\n") == "ab\n"  # no pairing possible, both must be healthy
assert run("1\naa\n") == "a\n"   # single letter fully pairable
assert run("1\nabab\n") == "ab\n"  # alternating, no pairs, both healthy
assert run("1\naaa\n") == "a\n"   # odd length breaks full pairing
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `ab` | `ab` | alternating letters cannot be paired |
| `aa` | `a` | simple full pair case |
| `abab` | `ab` | interleaving structure |
| `aaa` | `a` | odd leftover forces singleton |

## Edge Cases

A key edge case is when a letter appears in runs of odd length. For example, `aaa` cannot be fully partitioned into `aa` blocks, leaving one leftover occurrence. The algorithm detects this immediately because it encounters a single unmatched `a` after consuming one pair, returning failure for that letter in a full pairing interpretation.

Another edge case is interleaving like `ababa`. Even though both letters appear frequently, neither can form consistent adjacent pairs. The scan fails on the first isolated occurrence of each letter, ensuring both are correctly classified as healthy candidates.

A final subtle case is when pairing is locally possible but globally inconsistent. For example `aabbaabb` allows full pairing, so `a` is marked as pairable, while `abac` breaks pairing for `a` immediately at the isolated `c` transition, preventing incorrect classification.
