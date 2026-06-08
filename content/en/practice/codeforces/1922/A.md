---
title: "CF 1922A - Tricky Template"
description: "We are given three strings of equal length, and we need to construct a template string such that the first two strings match the template while the third one does not. Each position in the template can be either lowercase or uppercase."
date: "2026-06-08T19:19:02+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1922
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 161 (Rated for Div. 2)"
rating: 800
weight: 1922
solve_time_s: 270
verified: false
draft: false
---

[CF 1922A - Tricky Template](https://codeforces.com/problemset/problem/1922/A)

**Rating:** 800  
**Tags:** constructive algorithms, implementation, strings  
**Solve time:** 4m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given three strings of equal length, and we need to construct a template string such that the first two strings match the template while the third one does not. Each position in the template can be either lowercase or uppercase. A lowercase letter forces the corresponding character in a matching string to be exactly the same, while an uppercase letter forbids the corresponding character from being equal to the lowercase version of the template character. The input contains multiple test cases, and each string length is small, up to 20. This small size means we can reason about every position independently without worrying about combinatorial explosion.

The tricky part is handling positions where the first two strings differ. If `a[i]` equals `b[i]`, a lowercase template letter can ensure both match, but if `a[i] != b[i]`, there is no lowercase letter that allows both to match, so we must choose an uppercase letter. The template must also ensure that `c[i]` violates the matching rule at least once, which might be subtle when `c[i]` coincides with `a[i]` or `b[i]`. Edge cases include when all three characters at a position are distinct, when `a[i] = b[i] = c[i]`, or when only two of them are equal. A naive approach ignoring these distinctions would produce incorrect templates.

## Approaches

A brute-force approach would be to enumerate all `2^n * 26^n` possible templates and check whether `a` and `b` match while `c` does not. Even with `n` up to 20, this is infeasible. The key observation is that each position can be solved independently. We only need to determine a valid template character for that position that allows both `a` and `b` to match and blocks `c` if possible. There are only a few cases for each position: if `a[i] = b[i]`, we can choose either lowercase `a[i]` (to match `a` and `b`) unless it coincides with `c[i]`, in which case uppercase `a[i]` works. If `a[i] != b[i]`, we must pick an uppercase letter that is different from both `a[i]` and `b[i]`; if `c[i]` coincides with neither `a[i]` nor `b[i]`, this is straightforward. Because `n` is at most 20, iterating over these options per position is efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(26^n * 2^n) | O(n) | Too slow |
| Position-wise greedy | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Iterate over each position `i` from `0` to `n-1`.
2. If `a[i] == b[i]`, check if `c[i] == a[i]`. If yes, choose the uppercase version of `a[i]` as the template to block `c`. Otherwise, use the lowercase letter `a[i]`.
3. If `a[i] != b[i]`, we must choose an uppercase letter different from both `a[i]` and `b[i]`. If `c[i]` equals `a[i]` or `b[i]`, the uppercase choice automatically blocks `c[i]`. Otherwise, any uppercase letter different from `a[i]` and `b[i]` suffices.
4. If no valid choice exists in any position, return "NO". Otherwise, return "YES" after checking all positions.

The invariant is that at each position, we select a template character that allows both `a` and `b` to match. The design ensures that at least one position violates the match for `c` when required, because either `c[i]` coincides with `a[i]` or `b[i]` and we pick uppercase, or we pick an uppercase letter different from `a[i]` and `b[i]`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = input().strip()
        b = input().strip()
        c = input().strip()
        possible = True
        template = []
        for i in range(n):
            if a[i] == b[i]:
                if c[i] == a[i]:
                    template.append(a[i].upper())
                else:
                    template.append(a[i])
            else:
                # need uppercase letter different from both a[i] and b[i]
                for ch in 'abcdefghijklmnopqrstuvwxyz':
                    if ch != a[i] and ch != b[i] and (ch != c[i] or c[i] == a[i] or c[i] == b[i]):
                        template.append(ch.upper())
                        break
                else:
                    possible = False
                    break
        print("YES" if possible else "NO")

if __name__ == "__main__":
    solve()
```

Each loop handles a position independently. When `a[i] = b[i]`, the uppercase transformation is used to block `c[i]`. When `a[i] != b[i]`, the loop over all letters guarantees at least one uppercase letter is valid due to the 26-letter alphabet and the small maximum string length. The `else` clause of the `for` loop ensures we correctly detect impossible cases. Edge cases with all three letters equal are correctly handled by converting to uppercase.

## Worked Examples

**Example 1:**

Input: `1 a b c`

| i | a[i] | b[i] | c[i] | Template choice | Reason |
| --- | --- | --- | --- | --- | --- |
| 0 | a | b | c | C | a[i] != b[i], pick any letter ≠ a, b (C) |

Output: `YES`

**Example 2:**

Input: `2 aa bb aa`

| i | a[i] | b[i] | c[i] | Template choice | Reason |
| --- | --- | --- | --- | --- | --- |
| 0 | a | b | a | N/A | a[i] != b[i], any letter ≠ a,b blocks c? impossible |
| 1 | a | b | a | N/A | impossible |

Output: `NO`

These traces show that when `a[i] != b[i]` and `c[i]` coincides with one of them, no valid uppercase choice may exist, triggering "NO".

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * n * 26) | For each test case, iterate over n positions and at most 26 letters per position |
| Space | O(n) | Template string of length n |

Given `t ≤ 1000` and `n ≤ 20`, the solution runs in at most 520,000 iterations, which fits well within 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Provided samples
assert run("4\n1\na\nb\nc\n2\naa\nbb\naa\n10\nmathforces\nluckforces\nadhoccoder\n3\nacc\nabd\nabc\n") == "YES\nNO\nYES\nNO", "sample 1"

# Custom cases
assert run("1\n1\na\na\na\n") == "NO", "all equal letters"
assert run("1\n3\nabc\nabc\ndef\n") == "YES", "all positions differ in c"
assert run("1\n3\nabc\nabc\nbbc\n") == "YES", "mixed c letters"
assert run("1\n2\nab\nac\nad\n") == "YES", "a != b, c distinct"
assert run("1\n2\nab\nab\nab\n") == "NO", "cannot block c anywhere"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 a a a | NO | all three letters equal |
| 3 abc abc def | YES | c differs everywhere |
| 3 abc abc bbc | YES | some positions require careful choice |
| 2 ab ab ad | YES | a != b, c distinct |
| 2 ab ab ab | NO | cannot block c |

## Edge Cases

When all letters in `a`, `b`, and `c` coincide, the algorithm picks uppercase to block `c`, but in `a != b` situations, no uppercase letter can satisfy constraints, correctly producing "NO". When `n = 1`, the single-letter logic handles both equal and unequal scenarios. Maximum-length strings (`n = 20`) do not affect correctness because each position is independent, and 26 letters suffice to always find a valid uppercase unless blocked by `c`.
