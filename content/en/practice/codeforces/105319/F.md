---
title: "CF 105319F - We Want a Lesson"
description: "We are given a sequence of short text messages, and for each one we must decide how to respond based on a single special phrase."
date: "2026-06-22T12:01:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105319
codeforces_index: "F"
codeforces_contest_name: "Tishreen Collegiate Programming Contest 2024"
rating: 0
weight: 105319
solve_time_s: 48
verified: true
draft: false
---

[CF 105319F - We Want a Lesson](https://codeforces.com/problemset/problem/105319/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of short text messages, and for each one we must decide how to respond based on a single special phrase. Every incoming string is just a line of letters, and the task is to check whether it matches exactly one fixed target word, including case and characters.

If the message is exactly equal to the string `BdnaDars`, the response must be `Enough!`. For every other possible string, the response is `OK`.

The input size is small, with at most 1000 strings and each string length up to 100 characters. This means a direct comparison for each string is more than sufficient. Even a naive per-character scan is bounded by roughly 100,000 character checks overall, which is trivial for a typical time limit.

The only subtle failure mode comes from incorrect string comparison logic. A few examples illustrate what can go wrong. If a solution normalizes case or trims characters, then `bdnadars` or `BdnaDars ` would incorrectly be treated as matches even though they should not be. If a solution compares only prefixes, then `BdnaDarsX` could be mistakenly accepted. The correct behavior requires full exact equality.

## Approaches

The brute-force approach is also the optimal one in this problem. For each incoming string, we compare it character by character against the target string `BdnaDars`. If any mismatch is found, we immediately classify it as `OK`. If we finish the comparison without finding a mismatch and the lengths are identical, we output `Enough!`.

The reason this is sufficient is that the problem defines a single exact pattern to detect. There is no structure to exploit beyond equality checking, and no preprocessing or hashing is needed. The worst-case work is comparing each character of every string once, giving at most 1000 strings times 100 characters, which is only 100,000 comparisons.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (direct comparison) | O(n · L) | O(1) | Accepted |

## Algorithm Walkthrough

We process each input string independently and decide its output based on a direct equality check with the target phrase.

1. Read the number of strings n. This determines how many independent decisions we will make.
2. Fix the target string as `BdnaDars`, since every comparison is against this constant reference.
3. For each input string s, compare it directly with the target string. The comparison must consider both length and character-by-character equality.
4. If s is exactly equal to the target string, output `Enough!`, since it matches the forbidden phrase.
5. Otherwise, output `OK`, since all non-matching strings are treated uniformly.

The key design choice is treating equality as a single atomic condition. This avoids partial matching logic that could accidentally accept prefixes or case variations.

### Why it works

The algorithm is correct because the output depends solely on whether the input string is identical to one fixed reference string. Equality of strings is fully determined by matching lengths and matching characters at every index. Since the algorithm checks exactly that condition, every string is classified correctly, and no two distinct strings can produce the same incorrect match result.

## Python Solution

```python
import sys
input = sys.stdin.readline

TARGET = "BdnaDars"

def solve():
    n = int(input().strip())
    for _ in range(n):
        s = input().strip()
        if s == TARGET:
            print("Enough!")
        else:
            print("OK")

if __name__ == "__main__":
    solve()
```

The solution reads all strings using fast input and compares each one against the fixed constant. The `.strip()` is important because it removes the trailing newline character, which would otherwise interfere with equality checks.

The comparison `s == TARGET` is implemented efficiently in Python and internally short-circuits on the first mismatch, making it optimal for this problem size. There is no need for manual character loops or hashing.

## Worked Examples

### Example 1

Input:

```
3
Hi
BdnaDars
Bye
```

We process each string in order.

| Step | Input String | Comparison Result | Output |
| --- | --- | --- | --- |
| 1 | Hi | not equal | OK |
| 2 | BdnaDars | equal | Enough! |
| 3 | Bye | not equal | OK |

This shows that only the exact match triggers the special response, while all other strings are treated uniformly regardless of similarity.

### Example 2

Input:

```
2
bdnadars
BdnaDarsX
```

| Step | Input String | Comparison Result | Output |
| --- | --- | --- | --- |
| 1 | bdnadars | case mismatch | OK |
| 2 | BdnaDarsX | extra character | OK |

This trace highlights that both case differences and length differences immediately break equality, which is necessary to avoid incorrect matches.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · L) | Each of the n strings is compared character-by-character up to length L |
| Space | O(1) | Only a fixed target string and a single input buffer are used |

The constraints allow up to 1000 strings of length 100, so the total number of character operations is bounded by 100,000. This is comfortably within limits for Python, even with straightforward string comparisons.

## Test Cases

```python
import sys, io

def solve():
    input = sys.stdin.readline
    TARGET = "BdnaDars"
    n = int(input().strip())
    for _ in range(n):
        s = input().strip()
        if s == TARGET:
            print("Enough!")
        else:
            print("OK")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# provided sample
assert run("2\nHi\nBdnaDars\n") == "OK\nEnough!", "sample 1"

# custom cases

# minimum size
assert run("1\nBdnaDars\n") == "Enough!", "exact match single case"

# all different
assert run("3\nA\nB\nC\n") == "OK\nOK\nOK", "no matches"

# case sensitivity check
assert run("2\nbdnaDars\nBdnaDars\n") == "OK\nEnough!", "case sensitivity"

# near match with extra character
assert run("1\nBdnaDarsX\n") == "OK", "extra suffix"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\nBdnaDars | Enough! | exact match single element |
| 3\nA\nB\nC | OK OK OK | uniform rejection |
| bdnaDars / BdnaDars | OK / Enough! | case sensitivity handling |
| BdnaDarsX | OK | prevents prefix acceptance |

## Edge Cases

One important edge case is case sensitivity. The string `bdnadars` should never be accepted, even though it visually resembles the target. The algorithm correctly rejects it because Python string equality requires exact character matches, including uppercase and lowercase differences.

Another edge case is additional trailing characters. For example, `BdnaDarsX` shares a prefix with the target but has a longer length. The equality check fails because string lengths differ, so it is safely classified as `OK`.

A third edge case is the exact boundary match where the input is identical to the target. In that case, the comparison succeeds only after verifying all characters, and the output becomes `Enough!`, which is the only special case the problem defines.
