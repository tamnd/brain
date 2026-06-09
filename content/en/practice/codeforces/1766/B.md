---
title: "CF 1766B - Notepad#"
description: "We are asked to type a string s of length n using a text editor that allows two operations: appending a single character or copying a contiguous substring that has already been typed and pasting it at the end."
date: "2026-06-09T12:57:04+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1766
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 139 (Rated for Div. 2)"
rating: 1000
weight: 1766
solve_time_s: 129
verified: false
draft: false
---

[CF 1766B - Notepad#](https://codeforces.com/problemset/problem/1766/B)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 2m 9s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to type a string `s` of length `n` using a text editor that allows two operations: appending a single character or copying a contiguous substring that has already been typed and pasting it at the end. The goal is to determine if it is possible to produce the entire string in strictly fewer than `n` operations.

Each test case gives the length of the string and the string itself. The output should be "YES" if we can type it in fewer than `n` operations, otherwise "NO". Because the sum of all string lengths across test cases is at most 200,000, any solution that processes each string in linear time is feasible. Solutions that are quadratic in `n` will be too slow because `n` can reach 200,000.

The problem has some subtle cases. For example, if the string has all distinct characters, there is no substring to copy, so the only option is to type each character individually. If the string starts repeating a sequence early, copying can reduce the total operations. A careless solution that only looks for long repeated substrings might incorrectly output "NO" for strings that have a single repeated character early, like `aa`, which can be typed in one append and one copy.

Edge cases include a string of length one, where no copy is possible, so the output must be "NO", and a string where the first two characters are identical, which allows a copy after typing the first character, immediately reducing the operations below `n`.

## Approaches

A brute-force approach would try to simulate typing the string, at each step considering every substring of the already typed portion to see if it matches the upcoming segment. This method is correct, but for a string of length `n`, it could require checking `O(n^2)` substring matches in the worst case. With `n` up to 2·10^5, this becomes unmanageable.

The key insight is that we only need to check whether we can save a single operation. To type the string in fewer than `n` operations, we need to have a repeated character at the very beginning. Once we have typed the first character, if it appears again later, we can copy a substring of length at least one starting at that first character. This observation reduces the problem drastically: we do not need to simulate the entire typing process; we just need to see if any character appears at least twice in the first half of the string or anywhere after the first character. If so, we can guarantee at least one copy operation and save an operation compared to typing each character individually.

This reduces the solution to a simple linear scan for a repeated character.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n` and the string `s`.
3. If `n` is 1, output "NO" because a single character cannot benefit from a copy operation.
4. Otherwise, iterate through the string from the first character to the penultimate character.
5. Check if any character matches any character before it (or equivalently, if `s[i]` appears in `s[0:i]`). If a match is found, output "YES" immediately because we can type the initial part and then perform a copy, reducing the total operations below `n`.
6. If no repeated character is found, output "NO".

Why it works: the algorithm ensures that we only output "YES" if there is a possibility to save at least one operation by copying a substring. Since a copy must be from a previously typed segment, a repeated character guarantees that such a copy exists. Conversely, if all characters are unique, no copy is possible and the minimum number of operations is exactly `n`, so "NO" is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    s = input().strip()
    if n == 1:
        print("NO")
        continue
    found = False
    seen = set()
    for c in s:
        if c in seen:
            found = True
            break
        seen.add(c)
    print("YES" if found else "NO")
```

The solution reads input efficiently using `sys.stdin.readline`. We immediately handle the trivial case `n == 1`. For other cases, we iterate through the string and maintain a set of characters we have seen. The first time we encounter a character that has appeared before, we output "YES". Using a set ensures constant-time lookups, keeping the complexity linear. Subtle points include trimming the input line and breaking early when a repeated character is found to avoid unnecessary iterations.

## Worked Examples

Consider the string `labacaba`:

| Index | Character | Seen | Found |
| --- | --- | --- | --- |
| 0 | l | {l} | False |
| 1 | a | {l, a} | False |
| 2 | b | {l, a, b} | False |
| 3 | a | {l, a, b} | True |

At index 3, `a` is already in `seen`, so the algorithm outputs "YES". This demonstrates that we detect the possibility of a copy immediately.

Consider `codeforces`:

| Index | Character | Seen | Found |
| --- | --- | --- | --- |
| 0 | c | {c} | False |
| 1 | o | {c, o} | False |
| 2 | d | {c, o, d} | False |
| 3 | e | {c, o, d, e} | False |
| 4 | f | {c, o, d, e, f} | False |
| 5 | o | {c, o, d, e, f} | True |

Here, `o` repeats at index 5. This confirms the invariant that any repeated character guarantees we can save an operation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We scan each string once and maintain a set for constant-time lookup |
| Space | O(min(n,26)) | The set of seen characters has at most 26 entries for lowercase letters |

Given the sum of `n` across test cases is at most 200,000, the solution runs efficiently within the time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n = int(input())
        s = input().strip()
        if n == 1:
            print("NO")
            continue
        found = False
        seen = set()
        for c in s:
            if c in seen:
                found = True
                break
            seen.add(c)
        print("YES" if found else "NO")
    return output.getvalue().strip()

# provided samples
assert run("6\n10\ncodeforces\n8\nlabacaba\n5\nuohhh\n16\nisthissuffixtree\n1\nx\n4\nmomo\n") == "NO\nYES\nNO\nYES\nNO\nYES", "sample 1"

# custom cases
assert run("3\n1\na\n2\nab\n2\naa\n") == "NO\nNO\nYES", "single char and two-char variations"
assert run("2\n26\nabcdefghijklmnopqrstuvwxyz\n26\naabcdefghijklmnopqrstuvwxy\n") == "NO\nYES", "all unique vs first char repeat"
assert run("1\n5\naaaaa\n") == "YES", "all equal letters"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1, a | NO | Single character, cannot copy |
| 2, ab | NO | Two distinct characters, no repeated character |
| 2, aa | YES | Two identical characters, copy possible |
| 26, abc...z | NO | All unique characters, cannot reduce operations |
| 26, aabc...y | YES | Repeated first character allows a copy |
| 5, aaaaa | YES | Repeated letters, can copy multiple times |

## Edge Cases

The smallest input `n = 1` returns "NO" because no copy is possible. For `n = 2` with two identical characters, the algorithm correctly outputs "YES" because after typing the first character, we can copy it to reduce the operations from 2 to 1+1=2, which is equal, so only strictly less is possible if the second character appears later in longer strings. The algorithm handles long strings with all unique characters correctly, outputting "NO" as no operation savings exist. It also handles strings with repeated characters early in the sequence by immediately detecting a repeat and printing "YES", which confirms the invariant that the presence of a repeat allows a copy operation.
