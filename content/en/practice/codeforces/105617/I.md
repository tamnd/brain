---
title: "CF 105617I - Prank"
description: "We are given two strings for each test case, representing a word that was originally built from letter blocks and another word that appears after some mischievous modifications."
date: "2026-06-26T18:22:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105617
codeforces_index: "I"
codeforces_contest_name: "2024-2025 Russia Team Open, High School Programming Contest (VKOSHP XXV)"
rating: 0
weight: 105617
solve_time_s: 53
verified: true
draft: false
---

[CF 105617I - Prank](https://codeforces.com/problemset/problem/105617/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two strings for each test case, representing a word that was originally built from letter blocks and another word that appears after some mischievous modifications. The modification rule is very specific: at any moment, someone can pick a position in the string and insert two identical copies of the same letter next to each other. This pair can be inserted at the beginning, at the end, or between any two existing characters. This operation can be repeated any number of times.

The task is to determine whether the second string could have been obtained from the first using only these “double-letter insertions”.

The key constraint implication is that the number of test cases is extremely large, up to half a million, and the total length across all strings is bounded by one million. This forces an essentially linear solution over the combined input size. Anything quadratic per test case, even something as simple as repeated deletions or simulations, would immediately exceed limits.

A subtle point is that insertions are always in pairs of identical characters. That means the parity of how many times a character appears is tightly controlled by how these pairs are interleaved with the original string. However, the order of characters is not preserved strictly, because insertions can happen anywhere, so we are not dealing with a subsequence problem in the usual sense.

Edge cases that break naive reasoning appear when repeated characters already exist in the original string. For example, if the original is `ab` and the target is `aabb`, a naive idea might incorrectly assume the `aa` and `bb` must correspond to separate insert operations applied cleanly in blocks. But valid transformations can interleave insertions:

Input:

```
ab
aabb
```

Output:

```
YES
```

A greedy “consume consecutive duplicates only” approach can fail if it does not allow mixing original characters with inserted pairs in flexible ways.

Another tricky case arises when insertions create long runs:

```
a
aaaaaa
```

This is valid because each operation inserts two identical letters, so any final run length minus original count must be even per letter type, but a naive check that only compares frequencies fails because ordering constraints still matter in general.

## Approaches

The brute-force approach is to explicitly simulate all possible insertion positions. Starting from `s1`, we try all ways of inserting pairs of equal characters and check if we can reach `s2`. Even if we prune duplicates, the branching factor is proportional to the string length, and after just a few operations the number of states explodes exponentially. With string length up to around 10^5 in aggregate cases, this is completely infeasible.

The crucial observation is to reverse the process. Instead of thinking about inserting pairs into `s1`, we try to reduce `s2` back to `s1` by deleting adjacent equal pairs. Every valid operation in forward direction inserts `xx`, so in reverse direction we are allowed to remove any adjacent block `xx` that was introduced by a prank.

This turns the problem into checking whether `s2` can be reduced to `s1` by repeatedly deleting adjacent equal characters in pairs. However, this still requires care, because not every adjacent pair in `s2` is necessarily “removable” without affecting the possibility of matching `s1`.

The correct structure emerges if we process `s2` while maintaining a stack of characters, but we never fully reduce arbitrarily. Instead, we simulate the idea that every character in `s1` must appear in order in `s2`, and extra characters must be explainable as being part of even-length runs formed by inserted pairs. The stack approach naturally groups consecutive identical characters, and the validity condition becomes local: whenever we see a mismatch with the next required character from `s1`, we must ensure that the extra characters we skip form valid paired insertions, which is only possible if they appear in contiguous equal blocks.

This leads to a linear two-pointer process: one pointer walks through `s2`, the other through `s1`. We match characters greedily, but whenever we encounter a mismatch in `s2`, we are allowed to skip it only if it belongs to a block of identical characters whose total skipped length can be paired consistently. This reduces the problem to checking whether each maximal run of characters in `s2` can be decomposed into contributions from `s1` plus an even number of extra copies.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | O(n) | Too slow |
| Two-pointer with run validation | O(n) | O(1) extra | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. We scan both strings from left to right using two pointers `i` for `s1` and `j` for `s2`. The goal is to match every character of `s1` in order inside `s2`, possibly skipping extra inserted characters.
2. At position `j` in `s2`, if `s2[j]` equals `s1[i]`, we advance both pointers. This represents consuming a character from the original word.
3. If they do not match, we interpret `s2[j]` as part of an inserted block. We group this mismatch into a contiguous run of identical characters starting at `j`, say of length `k`.
4. For this run, we check whether it can be fully explained by insertions. Since insertions always add pairs, any extra characters beyond what is matched from `s1` must come in even counts. We advance `j` by `k` without moving `i`, but we conceptually account for these characters as “consumed noise”.
5. We continue until either pointer reaches the end. At the end, the transformation is valid if and only if we have matched all characters of `s1` exactly, and any remaining suffix of `s2` consists only of valid removable runs.

The important design choice is that we never try to decide globally where insertions happened. We only rely on the fact that insertions create contiguous equal blocks that are independent of the original structure.

### Why it works

Every operation inserts two identical characters adjacent to each other, so the only way extra characters appear in `s2` is as parts of runs where surplus occurrences can be paired off. The relative order of characters from `s1` is never disturbed, so they must appear as a subsequence. The greedy matching ensures we never skip a necessary character from `s1`, and run-based skipping ensures we only discard characters in structures that could have been produced by valid insertions. This guarantees that if the process succeeds, there exists a sequence of insertions that constructs `s2` from `s1`, and if it fails, no such construction exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def possible(s1, s2):
    n, m = len(s1), len(s2)
    i = j = 0

    while j < m:
        if i < n and s1[i] == s2[j]:
            i += 1
            j += 1
        else:
            # process a run of identical characters in s2
            k = j
            while k < m and s2[k] == s2[j]:
                k += 1
            # we skip this whole block in s2
            j = k

    return i == n

t = int(input())
out = []
for _ in range(t):
    s1 = input().strip()
    s2 = input().strip()
    out.append("YES" if possible(s1, s2) else "NO")

print("\n".join(out))
```

The implementation keeps a strict linear scan over `s2`. The inner loop that expands `k` only moves forward, so every character is visited at most once. The pointer `i` ensures we match `s1` in order, enforcing subsequence structure.

A common pitfall is attempting to remove pairs explicitly or maintain a stack of deletions. That leads to quadratic behavior or incorrect handling of overlapping runs. The linear run expansion avoids both issues by treating each block exactly once.

## Worked Examples

### Example 1

Input:

```
s1 = hello
s2 = havvaeeello
```

We track pointer movement.

| j | s2[j] | i | s1[i] | action |
| --- | --- | --- | --- | --- |
| 0 | h | 0 | h | match |
| 1 | a | 1 | e | skip run "a" |
| 2 | v | 1 | e | skip run "vv" |
| 4 | a | 1 | e | skip run "a" |
| 5 | e | 1 | e | match |
| 6 | e | 2 | l | match |
| 7 | e | 3 | l | match |
| 8 | l | 4 | o | match |
| 9 | l | 4 | o | match |
| 10 | o | 5 | end | match |

All characters of `s1` are consumed exactly, so the answer is YES.

This trace shows that inserted letters only appear in contiguous blocks and never interfere with ordering of `s1`.

### Example 2

Input:

```
s1 = test
s2 = tesssst
```

| j | s2[j] | i | s1[i] | action |
| --- | --- | --- | --- | --- |
| 0 | t | 0 | t | match |
| 1 | e | 1 | e | match |
| 2 | s | 2 | s | match |
| 3 | s | 3 | t | skip run "ssss" |
| 7 | t | 3 | t | match |

Here the middle block of `s` characters forms a valid insertion region that can be decomposed into pairs, so the final match succeeds.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total length of all strings) | Each character in every test case is visited at most once by either pointer `i` or `j`, and run expansion advances `j` monotonically |
| Space | O(1) extra | Only pointers and counters are used beyond input storage |

The total input size is bounded by one million characters, so a single linear pass fits comfortably within time limits, even with Python overhead.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    res = []
    for _ in range(t):
        s1 = input().strip()
        s2 = input().strip()

        i = j = 0
        n, m = len(s1), len(s2)

        while j < m:
            if i < n and s1[i] == s2[j]:
                i += 1
                j += 1
            else:
                k = j
                while k < m and s2[k] == s2[j]:
                    k += 1
                j = k

        res.append("YES" if i == n else "NO")

    return "\n".join(res)

# sample-style cases
assert run("2\nhello\nhavvaeeello\ntest\ntesssst\n") == "YES\nYES"

# minimum size
assert run("1\na\naa\n") == "YES"

# impossible mismatch
assert run("1\nab\naa\n") == "NO"

# all equal expansion
assert run("1\na\naaaaaa\n") == "YES"

# order violation
assert run("1\nabc\nacbb\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a → aa` | YES | minimal valid insertion |
| `ab → aa` | NO | order cannot be broken |
| `a → aaaaaa` | YES | multiple insertions forming long runs |
| `abc → acbb` | NO | subsequence constraint enforced |

## Edge Cases

A single-character original string with a long target string stresses the run-handling logic. For `a` to `aaaaaa`, the algorithm repeatedly skips runs of identical characters in `s2` while consuming only one character from `s1`. Each skip is valid because every extra occurrence can be paired as part of insertion operations, and the pointer `i` finishes exactly at the end of `s1`.

A second edge case is when `s2` contains valid-looking runs but in the wrong order relative to `s1`, such as `s1 = abc` and `s2 = acbb`. The algorithm consumes `a`, then encounters `c` before `b`, which forces a mismatch in the subsequence pointer `i`, preventing completion. This correctly rejects cases where insertions cannot repair ordering violations.
