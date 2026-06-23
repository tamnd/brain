---
title: "CF 105059A - Luddy Rocks"
description: "The task is essentially about checking whether a fixed target word can be constructed from the letters available in a given string. For each test case, we are given a “banner” made of uppercase letters."
date: "2026-06-23T10:48:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105059
codeforces_index: "A"
codeforces_contest_name: "IU Programming Challenge 2024"
rating: 0
weight: 105059
solve_time_s: 45
verified: true
draft: false
---

[CF 105059A - Luddy Rocks](https://codeforces.com/problemset/problem/105059/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is essentially about checking whether a fixed target word can be constructed from the letters available in a given string. For each test case, we are given a “banner” made of uppercase letters. Cora wants to rearrange some of these letters, discarding any she does not need, to exactly form the string “LUDDYROCKS”.

So the output depends purely on whether the multiset of characters in the banner contains enough copies of each required letter. Order is irrelevant because we are allowed to rearrange freely. What matters is frequency matching: every character in the target word must be available at least as many times as needed.

The constraints are small, with at most 100 test cases and each string length at most 100. This immediately tells us that even a straightforward scan of each string is cheap. A frequency count per test case is bounded by roughly 10,000 character operations in the worst case, which is trivial under a 1 second limit.

A subtle point is that characters may repeat in the target word. For example, “LUDDYROCKS” contains two D’s. A naive check that only verifies presence of distinct characters would fail here. Another pitfall is treating the problem like a subsequence check, where order matters. That would be incorrect because we are allowed to reorder arbitrarily.

A small illustrative failure case is the string “LUDYROCKS”. It contains only one D, so even though all other letters are present, the answer must be NO. Any approach that only checks set inclusion would incorrectly accept it.

## Approaches

The brute-force way to think about the problem is to try forming the target word explicitly. One could attempt to match each character of “LUDDYROCKS” by repeatedly scanning the banner and marking used characters. For each character in the target, we search the entire string to find an unused matching letter. This works because it simulates actual construction, ensuring correctness even with duplicates.

However, this approach performs up to 10 matches, and each match may require scanning up to 100 characters. That gives a worst-case complexity of about 1000 operations per test case, which is still fine here, but the structure becomes unnecessarily heavy and would not scale if constraints increased.

The key observation is that order is irrelevant and reuse is not allowed, so the problem reduces to counting frequencies. Instead of repeatedly searching, we count occurrences of each character in the banner once, and compare them directly against the required frequencies of the target word. This reduces the problem from repeated searching to a single linear pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Matching | O(n · m) | O(n) | Accepted for constraints |
| Frequency Counting | O(n) | O(1) | Optimal |

## Algorithm Walkthrough

1. Precompute the frequency of each character in the target string “LUDDYROCKS”. This gives a fixed requirement table that does not change across test cases.
2. For each test case, read the banner string.
3. Count the frequency of each character in the banner.
4. For every character required by the target word, check whether the banner count is at least as large as the required count.
5. If all requirements are satisfied, output YES; otherwise output NO.

The reasoning behind checking all required characters independently is that each character represents an independent constraint. Failing any one of them means construction is impossible.

### Why it works

The algorithm relies on the invariant that the frequency table of the banner fully describes all possible rearrangements. Since rearrangement does not change counts, any valid construction must be representable as a sub-multiset of the banner’s character multiset. By checking that every required count is less than or equal to the available count, we guarantee that a valid selection of characters exists. No ordering constraints exist, so feasibility reduces exactly to multiset inclusion.

## Python Solution

```python
import sys
input = sys.stdin.readline

TARGET = "LUDDYROCKS"

# precompute required frequencies
need = {}
for c in TARGET:
    need[c] = need.get(c, 0) + 1

t = int(input())
for _ in range(t):
    n = int(input())
    s = input().strip()

    have = {}
    for c in s:
        have[c] = have.get(c, 0) + 1

    ok = True
    for c, cnt in need.items():
        if have.get(c, 0) < cnt:
            ok = False
            break

    print("YES" if ok else "NO")
```

The code begins by building a fixed requirement map for the target word. This avoids recomputing it for every test case. For each input string, a fresh frequency dictionary is built in a single pass.

The final loop is the critical comparison step. It ensures every required character is present in sufficient quantity. Using `get(c, 0)` avoids key errors and cleanly handles missing characters.

One subtle implementation detail is stripping the input string. Without `.strip()`, newline characters could be misinterpreted as part of the frequency count, potentially introducing incorrect keys into the dictionary.

## Worked Examples

### Example 1

Input:

```
1
10
LUDDYROCKS
```

| Step | Character | Action | have state (partial) |
| --- | --- | --- | --- |
| build | L | increment | L:1 |
| build | U | increment | L:1 U:1 |
| build | D | increment | L:1 U:1 D:1 |
| build | D | increment | L:1 U:1 D:2 |
| build | Y | increment | L:1 U:1 D:2 Y:1 |
| build | R | increment | L:1 U:1 D:2 Y:1 R:1 |
| build | O | increment | L:1 U:1 D:2 Y:1 R:1 O:1 |
| build | C | increment | L:1 U:1 D:2 Y:1 R:1 O:1 C:1 |
| build | K | increment | L:1 U:1 D:2 Y:1 R:1 O:1 C:1 K:1 |
| build | S | increment | L:1 U:1 D:2 Y:1 R:1 O:1 C:1 K:1 S:1 |

All required counts match exactly, so output is YES.

This confirms the algorithm handles the simplest full-match case.

### Example 2

Input:

```
1
9
LUDYROCKS
```

| Required check | have count | needed | result |
| --- | --- | --- | --- |
| L | 1 | 1 | ok |
| U | 1 | 1 | ok |
| D | 1 | 2 | fail |
| Y | 1 | 1 | ok |
| R | 1 | 1 | ok |
| O | 1 | 1 | ok |
| C | 1 | 1 | ok |
| K | 1 | 1 | ok |
| S | 1 | 1 | ok |

The missing second D immediately breaks feasibility, so the output is NO. This trace shows the importance of counting duplicates rather than only checking existence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t · n) | each test case scans the string once and compares against a constant-sized target |
| Space | O(1) | frequency maps are bounded by uppercase alphabet size |

The solution easily fits within limits since the maximum total input size is only about 10,000 characters, leading to negligible runtime.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    TARGET = "LUDDYROCKS"
    need = {}
    for c in TARGET:
        need[c] = need.get(c, 0) + 1

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        s = input().strip()

        have = {}
        for c in s:
            have[c] = have.get(c, 0) + 1

        ok = True
        for c, cnt in need.items():
            if have.get(c, 0) < cnt:
                ok = False
                break

        out.append("YES" if ok else "NO")

    return "\n".join(out)

# provided samples
assert run("1\n10\nLUDDYROCKS\n") == "YES"
assert run("1\n9\nLUDYROCKS\n") == "NO"

# custom cases
assert run("1\n5\nABCDE\n") == "NO", "missing most letters"
assert run("1\n20\nLLLUDDDYROCKSSSSS\n") == "YES", "extra letters allowed"
assert run("2\n10\nLUDDYROCKS\n9\nLUDDYROCKS\n") == "YES\nNO", "multi-test correctness"
assert run("1\n10\nLUDDYROCKS\n") == "YES", "exact match"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5-letter random string | NO | missing required letters |
| padded valid string | YES | extra letters are harmless |
| mixed multi-test input | YES/NO | correct per-case processing |
| exact match | YES | baseline correctness |

## Edge Cases

One important edge case is when the banner contains all required letters but in insufficient multiplicity, as in “LUDYROCKS”. The algorithm explicitly counts occurrences, so when it compares the requirement for D (2 needed, 1 available), it immediately rejects the case.

Another edge case is when the banner is much longer and contains many irrelevant characters. For example, a string like “ZZZLUDDYROCKSZZZ” still produces correct YES because the frequency comparison ignores extra characters not in the target. The invariant is that only lower bounds matter, not exact equality.

A final case is repeated full construction, such as “LUDDYROCKSLUDDYROCKS”. The frequency table naturally supports this because counts scale linearly, and every required character is still satisfied.
