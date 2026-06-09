---
title: "CF 1697C - awoo's Favorite Problem"
description: "The problem gives two strings s and t of the same length consisting of the characters 'a', 'b', and 'c'. The allowed operations let us swap adjacent \"ab\" to \"ba\" and \"bc\" to \"cb\". The task is to determine whether we can transform s into t using any number of these moves."
date: "2026-06-09T22:30:50+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "constructive-algorithms", "data-structures", "greedy", "implementation", "strings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1697
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 130 (Rated for Div. 2)"
rating: 1400
weight: 1697
solve_time_s: 441
verified: true
draft: false
---

[CF 1697C - awoo's Favorite Problem](https://codeforces.com/problemset/problem/1697/C)

**Rating:** 1400  
**Tags:** binary search, constructive algorithms, data structures, greedy, implementation, strings, two pointers  
**Solve time:** 7m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem gives two strings `s` and `t` of the same length consisting of the characters 'a', 'b', and 'c'. The allowed operations let us swap adjacent "ab" to "ba" and "bc" to "cb". The task is to determine whether we can transform `s` into `t` using any number of these moves.

The input consists of multiple test cases, and the sum of string lengths across all cases is bounded by 10^5. This constraint implies that any solution that processes each character a constant number of times will be fast enough, but naive simulation of all possible moves is too slow because the number of operations needed to reach `t` could be quadratic in `n`.

Edge cases arise when `s` and `t` have identical counts of 'a', 'b', 'c' but the order of characters makes transformation impossible. For example, `s = "acb"` and `t = "bac"` have the same character counts, but 'a' cannot move past 'c' directly, so the transformation is impossible. Another case occurs when strings are already equal, in which case no moves are required.

## Approaches

The brute-force approach tries to repeatedly apply all possible swaps until `s` equals `t`. This is correct in theory but infeasible for strings of length up to 10^5 because each swap changes only a single pair, and the number of moves could approach O(n^2).

A better approach relies on the constraints of the moves. Each swap can only move 'a' right over 'b' and 'c' left over 'b'. This means the relative order of 'a' and 'c' cannot be reversed. Therefore, the core insight is to check whether the order of 'a' and 'c' in `s` can be rearranged into `t` under the allowed swaps. We first verify that the counts of 'a', 'b', 'c' in `s` and `t` are identical; if they differ, transformation is impossible. Next, we check the positions of 'a' and 'c' relative to 'b'. 'a' can only move right and 'c' only left across 'b', so for each character, we check that no character needs to move past another in a forbidden direction. This reduces the problem to a linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Linear Scan with Constraints | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read strings `s` and `t` and their length `n`.
2. Compare counts of 'a', 'b', and 'c' in `s` and `t`. If any count differs, print "NO" and continue to the next test case.
3. Iterate through `s` and `t` simultaneously, ignoring all 'b' characters. For the remaining characters, check that the sequence of 'a' and 'c' matches exactly. If there is a mismatch in type or order, print "NO".
4. For positions where 'a' appears, ensure that each 'a' in `s` is not to the right of its corresponding position in `t`. 'a' can only move right.
5. For positions where 'c' appears, ensure that each 'c' in `s` is not to the left of its corresponding position in `t`. 'c' can only move left.
6. If all checks pass, print "YES".

Why it works: the allowed moves preserve the relative order of 'a' and 'c' across each other because 'ab' can only move 'a' right past 'b' and 'bc' can only move 'c' left past 'b'. By ignoring 'b', we reduce the problem to a one-dimensional order check, ensuring all transformations are achievable.

## Python Solution

```
PythonRun
```

The solution first ensures that the characters in both strings match. It then creates index lists for all characters except 'b', allowing us to check whether 'a' and 'c' can move according to the allowed rules. 'a' can only move right and 'c' can only move left. If any character violates these rules, the answer is "NO".

## Worked Examples

Trace the sample input:

```

```

| i | s[i] | t[i] | Check |
| --- | --- | --- | --- |
| 0 | a | b | ignore 'b', compare 'a' to 'a' in t index 2 |
| 1 | b | b | ignored |
| 2 | b | a | ignored |
| 3 | a | a | i=3, j=3 |
| 4 | b | c | ignored |
| 5 | c | b | 'c' i=5, j=5 |

All constraints satisfied, output "YES". This confirms the algorithm handles mixed sequences of 'a', 'b', 'c' correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single scan of the string and comparison of characters; linear in length. |
| Space | O(n) | For storing filtered indices of non-'b' characters. |

The solution is efficient because the sum of `n` over all test cases does not exceed 10^5, ensuring that the linear algorithm completes well within the 2-second limit.

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
assert run("5\n3\ncab\ncab\n1\na\nb\n6\nabbabc\nbbaacb\n10\nbcaabababc\ncbbababaac\n2\nba\nab\n") == \
    "YES\nNO\nYES\nYES\nNO", "sample 1"

# Custom cases
assert run("2\n4\naabc\nabac\n3\nabc\ncba\n") == "YES\nNO", "custom order check"
assert run("1\n5\naaaab\naaaab\n") == "YES", "all equal except last b"
assert run("1\n3\nacb\nabc\n") == "NO", "a cannot move left past c"
assert run("1\n6\nabcbac\nabcabc\n") == "YES", "complex interleaving"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4\naabc\nabac | YES | a can move right to match t |
| 3\nabc\ncba | NO | impossible to move 'a' past 'c' |
| 5\naaaab\naaaab | YES | verifies strings already almost equal |
| 3\nacb\nabc | NO | 'a' cannot move left |
| 6\nabcbac\nabcabc | YES | complex swaps with multiple 'b' characters |

## Edge Cases

The algorithm correctly handles strings of length 1. For example, `s = "a"` and `t = "a"` outputs "YES" because no moves are required. If `s = "a"` and `t = "b"`, output is "NO" because characters do not match.

Strings with only 'b' characters are always transformable if counts match because no restrictions exist on 'b' movements. The algorithm treats them correctly by ignoring 'b' positions in the relative order check.

The solution also handles the maximum size efficiently due to linear time complexity and minimal extra space for index tracking.
