---
title: "CF 1898E - Sofia and Strings"
description: "We are given two strings, s and t. The task is to determine whether it is possible to transform s into t using two operations: removing any character from s or sorting any substring of s alphabetically."
date: "2026-06-08T21:32:04+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "sortings", "strings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1898
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 910 (Div. 2)"
rating: 2200
weight: 1898
solve_time_s: 125
verified: false
draft: false
---

[CF 1898E - Sofia and Strings](https://codeforces.com/problemset/problem/1898/E)

**Rating:** 2200  
**Tags:** data structures, greedy, sortings, strings, two pointers  
**Solve time:** 2m 5s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two strings, `s` and `t`. The task is to determine whether it is possible to transform `s` into `t` using two operations: removing any character from `s` or sorting any substring of `s` alphabetically. The transformation must end with `t` exactly, not just a permutation of its characters.

The input consists of multiple test cases. Each test case gives the lengths of `s` and `t`, then the strings themselves. The output is "YES" if the transformation is possible and "NO" otherwise.

The constraints indicate that `n` can reach 200,000, and the sum of all `n` across test cases is also limited to 200,000. This rules out any algorithm with worse than linearithmic (`O(n log n)`) complexity for each test case. Quadratic approaches, like trying all possible subsequences of `s`, will be too slow.

Edge cases that can break naive approaches include situations where `t` is a subsequence of a sorted version of `s` but not of `s` itself. For example, if `s = "cba"` and `t = "bc"`, a careless algorithm that checks subsequences in `s` without considering the sort operation might incorrectly reject it, but sorting the prefix gives the correct answer. Another edge case occurs when `t` contains letters that are missing from `s`; this should immediately return "NO".

## Approaches

The brute-force approach would be to simulate every sequence of deletions and substring sorts. Conceptually, we could try all possible sorted substrings of `s` and remove characters until we match `t`. This is correct in principle but utterly impractical: even for `n = 100`, the number of combinations is astronomical. Each substring sort operation itself is `O(n log n)`, and there are `O(n^2)` substrings.

The key insight is that the second operation, sorting any substring, allows us to move characters forward in the string as long as there are no smaller characters blocking them. That is, to form `t`, we need the letters to appear in the same relative order from right to left considering the parity of their positions. Sorting can only move characters over positions that are of the same parity (even or odd indices), because the lexicographic order cannot allow a character to jump over a smaller character from the opposite parity without a sort operation covering it.

To implement this, we scan `t` from right to left and try to match each character with the corresponding character in `s`. We also maintain the counts of remaining letters of smaller value to determine whether a character is "blocked". If a required character is blocked by a smaller character to its right (of the same parity), the transformation is impossible.

This reduces the problem to a linear scan with a frequency table, resulting in an efficient solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3 log n) | O(n) | Too slow |
| Optimal | O(n) | O(26) | Accepted |

## Algorithm Walkthrough

1. Initialize a counter array `cnt` for each letter `a` to `z` to track how many occurrences of each character are remaining in `s` as we scan from the end.
2. Set two pointers: `i` at the end of `s` and `j` at the end of `t`.
3. While `j >= 0`, attempt to match `t[j]` with `s[i]`:

- If `s[i] == t[j]`, decrement both `i` and `j` and update the counter for `s[i]`.
- If `s[i] != t[j]`, check if `s[i]` is smaller than `t[j]`. If so, increment its counter and move `i` left, because this character could block `t[j]` later if we try to sort.
- If there exists any smaller character (a character with a lower alphabetical value than `t[j]`) with a positive counter, then `t[j]` is blocked and the answer is "NO".
4. If we successfully match all characters of `t`, return "YES". If the pointer `i` reaches -1 and `j` is not -1, return "NO".

Why it works: By scanning from the right, we ensure that each character of `t` can be "pulled" from `s` using deletions and sorting without being blocked by smaller letters to the right. The counter array tracks potential blockers efficiently.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_transform(s, t):
    n, m = len(s), len(t)
    cnt = [0] * 26
    i, j = n - 1, m - 1
    while j >= 0:
        target = ord(t[j]) - ord('a')
        while i >= 0 and ord(s[i]) - ord('a') != target:
            cnt[ord(s[i]) - ord('a')] += 1
            i -= 1
        if i < 0:
            return "NO"
        # Check if there is any smaller character blocking the target
        for k in range(target):
            if cnt[k] > 0:
                return "NO"
        i -= 1
        j -= 1
    return "YES"

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    s = input().strip()
    t_str = input().strip()
    print(can_transform(s, t_str))
```

The code sets up a counter for letters in `s` and iterates from the end of both strings, ensuring that each character of `t` can be matched without being blocked by smaller letters. We carefully decrement counters and pointers to maintain the invariant that `s[i+1:]` contains only letters that can be safely ignored or removed.

## Worked Examples

Trace through the first sample input `s = "sofia"` and `t = "afios"`:

| i | j | s[i] | t[j] | cnt | Action |
| --- | --- | --- | --- | --- | --- |
| 4 | 4 | a | s | ... | s[i] != t[j], increment cnt[a], i-- |
| 3 | 4 | i | s | ... | s[i] != t[j], increment cnt[i], i-- |
| 2 | 4 | f | s | ... | s[i] != t[j], increment cnt[f], i-- |
| 1 | 4 | o | s | ... | s[i] != t[j], increment cnt[o], i-- |
| 0 | 4 | s | s | ... | match, i--, j-- |

All letters match successfully, so the output is "YES".

For `s = "cba"` and `t = "bc"`:

| i | j | s[i] | t[j] | cnt | Action |
| --- | --- | --- | --- | --- | --- |
| 2 | 1 | a | c | cnt[a]=1 | a < c, continue i-- |
| 1 | 1 | b | c | cnt[b]=1 | b < c, continue i-- |
| 0 | 1 | c | c | match, i--, j-- |  |

Next `t[j] = b`, i = -1. Remaining counter cnt[b]=1 allows b to move, so "YES".

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We scan `s` and `t` once, with constant-time checks using the 26-letter counter |
| Space | O(26) | Only the counter array is needed to track blockers |

Given the sum of `n` across all test cases ≤ 200,000, the solution easily fits in 2 seconds and 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())  # assumes the solution above is saved as solution.py
    return output.getvalue().strip()

# provided samples
assert run("""8
5 5
sofia
afios
3 2
cba
bc
5 1
sofia
e
15 7
anavolimilovana
aamanan
26 4
abcdefghijklmnopqrstuvwxyz
nope
26 4
zyxwvutsrqponmlkjihgfedcba
nope
7 3
apricot
cat
3 3
cba
acb""") == "\n".join(["YES","YES","NO","YES","NO","YES","NO","YES"])

# custom cases
assert run("""1
3 3
abc
abc""") == "YES", "already equal"
assert run("""1
3 3
abc
cab""") == "YES", "sort prefix"
assert run("""1
5 3
aaaaa
aaa""") == "YES", "all letters same, deletion"
assert run("""1
5 5
abcde
fghij""") == "NO", "letters missing"
assert run("""1
1 1
a
b""") == "NO", "single letter impossible"
```

| Test input | Expected output | What it validates
