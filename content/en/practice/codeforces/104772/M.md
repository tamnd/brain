---
title: "CF 104772M - Missing Vowels"
description: "We are given two strings that represent the same place or name written in two different ways. The first string is a shortened version, while the second string is the full version."
date: "2026-06-28T16:15:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104772
codeforces_index: "M"
codeforces_contest_name: "2023-2024 ICPC NERC (NEERC), North-Western Russia Regional Contest (Northern Subregionals)"
rating: 0
weight: 104772
solve_time_s: 82
verified: false
draft: false
---

[CF 104772M - Missing Vowels](https://codeforces.com/problemset/problem/104772/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two strings that represent the same place or name written in two different ways. The first string is a shortened version, while the second string is the full version. The transformation rule is very specific: starting from the full string, we are allowed to delete some vowels, but we are not allowed to delete consonants or hyphens. After deleting any subset of vowels, the resulting string must match the short string exactly.

The task is to decide whether such a deletion process can transform the full string into the short string.

The strings can be up to length 1000, so any solution that tries all subsets of vowels or simulates deletions in an exponential way is immediately too slow. A quadratic or linear scan per test is completely fine, but anything beyond linear matching with simple state tracking would be unnecessary overhead.

A subtle point is case-insensitivity. Uppercase and lowercase letters must be treated as identical, so normalization is required before comparison. Another detail that often breaks naive solutions is forgetting that only vowels may be deleted. Consonants and hyphens must appear in the same relative order in both strings.

Edge cases that commonly break incorrect implementations include situations where:

A vowel exists in the short string but not in the full string. For example, short = "a", full = "b". This must be "Different" because we are not allowed to insert characters, only delete vowels.

Another case is when the short string skips consonants. For example, short = "shrm", full = "sharm". Here the full string contains extra vowels, so we can delete 'a' and match, which is valid.

A third subtle case is when hyphens are involved, since hyphens behave like consonants and cannot be removed or skipped.

## Approaches

A brute-force interpretation would consider all subsets of vowel positions in the full string. For each subset, we delete those vowels and compare the result to the short string. If we think of a full string of length n, there are potentially 2^k subsets where k is the number of vowels, and in the worst case k is proportional to n. Each constructed string costs O(n) to build and compare, giving an overall complexity on the order of O(n · 2^n), which is completely infeasible even for n = 1000.

The key observation is that the operation does not rearrange characters and does not allow deletion of consonants or hyphens. This means we are not choosing a subset arbitrarily; we are matching two sequences under a strict rule: every non-vowel character in the full string must appear in the short string in the same order, while vowels in the full string may be optionally skipped if they are not needed to match the short string.

This immediately suggests a two-pointer scan. We traverse both strings simultaneously. Whenever characters match (after case normalization), we advance both pointers. If they do not match, the only possible explanation is that the character in the full string is a vowel, in which case we are allowed to skip it. If it is not a vowel, matching is impossible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · 2^n) | O(n) | Too slow |
| Two-pointer scan | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Convert both strings to lowercase so comparisons are case-insensitive. This ensures uniform character handling without branching later.
2. Define a helper function that checks whether a character is a vowel. In this problem vowels are a, e, i, o, u, y. Hyphens are not vowels and must never be skipped.
3. Initialize two pointers, one for the short string and one for the full string, both starting at position zero. These pointers represent how much of each string we have successfully matched so far.
4. Iterate through the full string pointer from left to right. At each step, compare the current character in the full string with the current character in the short string if it still exists.
5. If both characters match, advance both pointers. This represents consuming a required character in the short string from the full string.
6. If they do not match, check whether the current full-string character is a vowel. If it is, we can safely skip it by advancing only the full-string pointer. This corresponds to deleting that vowel.
7. If the characters do not match and the full-string character is not a vowel, we immediately conclude that the transformation is impossible, since consonants and hyphens cannot be removed or altered.
8. After processing the full string, check whether we have successfully consumed all characters in the short string. If yes, the transformation is valid; otherwise, some required characters were never matched.

### Why it works

The algorithm maintains the invariant that every character consumed from the short string is matched in order by a corresponding character in the full string. We never reorder characters, and we only skip characters in the full string when they are vowels. This exactly mirrors the allowed operation. If at any point a non-vowel mismatches, there is no legal deletion sequence that can fix it, since non-vowels are mandatory and order-preserving. Therefore, reaching the end of the full string with the short string fully matched is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

VOWELS = set("aeiouy")

def can_transform(s, f):
    s = s.strip().lower()
    f = f.strip().lower()

    i = 0  # pointer for s
    j = 0  # pointer for f

    n, m = len(s), len(f)

    while j < m:
        if i < n and s[i] == f[j]:
            i += 1
            j += 1
        else:
            if f[j] in VOWELS:
                j += 1
            else:
                return False

    return i == n

def main():
    s = input().strip()
    f = input().strip()

    if can_transform(s, f):
        print("Same")
    else:
        print("Different")

if __name__ == "__main__":
    main()
```

The implementation follows the two-pointer strategy directly. Both strings are normalized to lowercase at the start to remove case sensitivity concerns. The main loop always advances the full-string pointer, either consuming a match or skipping a vowel.

A common pitfall is forgetting the final check `i == n`. Without it, cases where the full string ends early but the short string still has unmatched characters would incorrectly pass.

Another subtlety is ensuring that only the full string pointer advances when skipping vowels. Advancing both pointers during mismatch would incorrectly assume deletions in the short string, which is not allowed.

## Worked Examples

### Example 1

Input:

```
Shrm-el-Shikh
Sharm-el-Sheikh
```

| Step | s pointer | f pointer | s[i] | f[j] | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | s | s | match, advance both |
| 2 | 1 | 1 | h | h | match, advance both |
| 3 | 2 | 2 | r | a | skip vowel |
| 4 | 2 | 3 | r | r | match, advance both |
| 5 | 3 | 4 | m | m | match, advance both |
| ... | ... | ... | ... | ... | continue similarly |

At each mismatch, the character in the full string is a vowel, so it is safely skipped. Eventually the short string is fully consumed, confirming that the short form can be derived by deleting vowels only.

### Example 2

Input:

```
Eilot
Eilat
```

| Step | s pointer | f pointer | s[i] | f[j] | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | e | e | match |
| 2 | 1 | 1 | i | i | match |
| 3 | 2 | 2 | l | l | match |
| 4 | 3 | 3 | o | a | mismatch, skip 'a'? |

At step 4, the characters differ and f[j] = 'a' is a vowel, so we skip it. However, later we eventually run out of matching structure and cannot align the remaining characters correctly, leaving the short string unmatched at termination.

This demonstrates a case where local skipping is not enough to guarantee a full match.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each pointer only moves forward through its string once |
| Space | O(1) | Only constant extra memory for pointers and vowel set |

The linear scan is sufficient for strings up to length 1000, and the constant-factor work per character is minimal, so the solution easily fits within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import main
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

# provided samples
assert run("Shrm-el-Shikh\nSharm-el-Sheikh\n") == "Same"
assert run("Eilot\nEilat\n") == "Different"
assert run("Saint-Petersburg\nSaint-Petersburg\n") == "Same"

# custom cases
assert run("a\nb\n") == "Different", "single mismatch non-vowel"
assert run("shrm\nsharm\n") == "Same", "simple vowel deletion"
assert run("Aeiouy\nbcdfg\n") == "Different", "vowels cannot create matches"
assert run("abc\nabc\n") == "Same", "no deletions needed"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| a / b | Different | non-vowel mismatch |
| shrm / sharm | Same | vowel skipping works |
| Aeiouy / bcdfg | Different | case handling and no forced matches |
| abc / abc | Same | identity case |

## Edge Cases

A case like `s = "a"`, `f = "b"` is handled immediately by the algorithm. After lowering, the first comparison is between 'a' and 'b'. Since they differ and 'b' is not a vowel, the function returns false at once. This confirms that vowels cannot be used to compensate for missing consonants.

For `s = "shrm"` and `f = "sharm"`, the scan proceeds until the 'a' in the full string. Since 'a' is a vowel, it is skipped, and the remaining characters align perfectly. The invariant holds because all matched characters in `s` are preserved in order.

For `s = "Saint-Petersburg"` and `f = "Saint-Petersburg"`, every character matches directly, so no skipping occurs. The algorithm consumes both strings synchronously and finishes with both pointers aligned, confirming correctness when no deletions are needed.
