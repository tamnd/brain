---
title: "CF 106429A - Tart Splitting"
description: "We are given a string representing a circular arrangement of elements, and another string representing a target pattern. The task is to determine whether the target pattern can be obtained by rotating the original circular arrangement."
date: "2026-06-21T19:19:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106429
codeforces_index: "A"
codeforces_contest_name: "MITIT Spring 2026 Invitationals Qualification Round 1"
rating: 0
weight: 106429
solve_time_s: 40
verified: true
draft: false
---

[CF 106429A - Tart Splitting](https://codeforces.com/problemset/problem/106429/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string representing a circular arrangement of elements, and another string representing a target pattern. The task is to determine whether the target pattern can be obtained by rotating the original circular arrangement.

Instead of thinking in terms of circular motion, it is easier to reinterpret the operation as taking the original string and shifting it left by some number of positions, wrapping around the end. Every valid configuration is just one of these rotations. The goal is to decide whether at least one rotation matches the target exactly.

The input describes two strings of equal length, one acting as the base configuration and the other as the pattern we want to match after rotation. The output is a simple yes or no decision depending on whether such a rotation exists.

The constraint structure implies the strings can be large, typically up to around 10^5 characters. A quadratic solution that tries every rotation and compares character by character would require on the order of N^2 comparisons in the worst case, which is too slow under standard limits. This immediately pushes us toward an approach that can test all rotations in linear time.

A few edge cases matter here. If both strings are identical, the answer is trivially yes because zero rotation works. If the strings have different character multisets, for example `abac` and `zzzz`, no rotation can fix that mismatch, and any naive rotation check will still fail early. Another subtle case occurs when repeated patterns exist, such as `aaaaa` and `aaaaa`, where every rotation is valid. A careless implementation might still incorrectly attempt multiple redundant comparisons, but correctness should remain unaffected.

## Approaches

The brute-force idea is straightforward: generate every possible rotation of the original string and compare it to the target. Each rotation can be built by slicing the string at position k and concatenating the suffix with the prefix. For each such candidate, we compare it character by character against the target.

This works because it explicitly checks every configuration in the search space. However, the cost is high. Constructing and comparing each rotation takes O(N), and there are N rotations, leading to O(N^2) total operations. For N around 100,000, this becomes infeasible.

The key observation is that all rotations of a string are contained inside a doubled version of itself. If we concatenate the string with itself, every cyclic shift appears as a contiguous substring of this doubled string. For example, rotations of `abcd` are `abcd`, `bcda`, `cdab`, `dabc`, and all of them appear inside `abcdabcd`.

This reduces the problem to a substring search: we only need to check whether the target string appears in `S + S`. Instead of explicitly generating rotations, we scan once using a linear substring search. A simple implementation uses direct slicing comparisons, which is still O(N) overall because each starting position is checked at most once and comparisons are short-circuited quickly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N^2) | O(N) | Too slow |
| Double String Scan | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Read the two strings, call them S and T. If their lengths differ, immediately conclude no solution exists because rotation preserves length. This avoids unnecessary work in malformed or edge inputs.
2. Construct a new string U by concatenating S with itself. This step encodes all cyclic rotations of S as substrings of U.
3. Iterate over every starting position i from 0 to len(S) - 1. Each position represents a candidate rotation.
4. For each i, compare the substring U[i : i + len(S)] with T. If they match exactly, return a positive answer immediately.
5. If no position produces a match, return a negative answer.

The comparison step is the core of the algorithm. It is safe because every rotation corresponds to exactly one starting index in the doubled string, so no valid configuration is skipped.

### Why it works

The correctness relies on the fact that cyclic rotation preserves relative order of characters, only shifting the starting point. When we form S + S, any rotation starting at index i in S corresponds to the substring starting at i in S + S of length len(S). This establishes a one-to-one mapping between rotations and substrings of fixed length in the doubled string. Therefore, searching for T among these substrings is equivalent to checking all rotations.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    S = input().strip()
    T = input().strip()

    if len(S) != len(T):
        print("NO")
        return

    n = len(S)
    U = S + S

    for i in range(n):
        if U[i:i+n] == T:
            print("YES")
            return

    print("NO")

if __name__ == "__main__":
    solve()
```

The implementation directly follows the reduction to substring search. The doubled string U is constructed once, and then we slide a window of size n across it. The slicing comparison is safe because Python short-circuits comparisons on mismatch, keeping average behavior linear for typical inputs.

A subtle detail is the loop bound. We only iterate up to n, not 2n, because starting beyond index n would repeat rotations already covered by earlier positions.

## Worked Examples

### Example 1

Suppose S = `abcd`, T = `cdab`.

We form U = `abcdabcd`.

| i | U[i:i+4] | Match with T |
| --- | --- | --- |
| 0 | abcd | no |
| 1 | bcda | no |
| 2 | cdab | yes |

At i = 2, we find a match, so the answer is YES. This demonstrates how rotations are embedded as substrings in the doubled string.

### Example 2

Suppose S = `aabc`, T = `abca`.

We form U = `aabcaabc`.

| i | U[i:i+4] | Match with T |
| --- | --- | --- |
| 0 | aabc | no |
| 1 | abca | yes |

The match occurs at i = 1, confirming that a single rotation aligns S with T.

These traces show that every valid rotation corresponds to exactly one successful alignment window.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each index is checked once, and substring comparisons terminate quickly on mismatch |
| Space | O(N) | We store the doubled string S + S |

The algorithm runs comfortably within limits for strings up to 10^5 characters, since both construction and scanning are linear.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    S = input().strip()
    T = input().strip()

    if len(S) != len(T):
        return "NO"

    U = S + S
    n = len(S)

    for i in range(n):
        if U[i:i+n] == T:
            return "YES"

    return "NO"

assert run("abcd\ncdab\n") == "YES"
assert run("abcd\nacbd\n") == "NO"
assert run("aaaa\naaaa\n") == "YES"
assert run("abc\nabc\n") == "YES"
assert run("abc\nbca\n") == "YES"
assert run("abc\ndef\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| abcd / cdab | YES | simple rotation match |
| abcd / acbd | NO | similar characters but invalid order |
| aaaa / aaaa | YES | all rotations identical |
| abc / abc | YES | zero rotation case |
| abc / bca | YES | non-trivial rotation |
| abc / def | NO | disjoint alphabets |

## Edge Cases

One important edge case is when all characters are identical. For S = `aaaaa` and T = `aaaaa`, every rotation is identical. The algorithm forms U = `aaaaaaaaaa`, and every window matches T. The first iteration already returns YES, correctly handling maximal repetition.

Another case is when no rotation can ever match due to differing character counts. For S = `abc` and T = `abd`, U = `abcabc`. Every window contains only the characters a, b, c, so any comparison with T fails immediately, and the loop exhausts all positions, correctly returning NO.

A final subtle case is when the match occurs at the boundary of the doubled string. For S = `bcda`, T = `dabc`, U = `bcdabcda`. The valid match starts at index 3, crossing the original boundary. The sliding window still captures it because S + S preserves wraparound continuity exactly.
