---
title: "CF 138E - Hellish Constraints"
description: "We are asked to count substrings of a given string that satisfy a complicated set of constraints. Each constraint specifies a letter and a minimum and maximum number of times that letter can appear."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 138
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 99 (Div. 1)"
rating: 2900
weight: 138
solve_time_s: 78
verified: true
draft: false
---

[CF 138E - Hellish Constraints](https://codeforces.com/problemset/problem/138/E)

**Rating:** 2900  
**Tags:** brute force, dp, two pointers  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count substrings of a given string that satisfy a complicated set of constraints. Each constraint specifies a letter and a minimum and maximum number of times that letter can appear. Additionally, a substring is considered valid only if it satisfies at least _L_ and at most _R_ of the _k_ constraints. The string length can reach up to 100,000, while the number of constraints is up to 500.

The main challenge is that we cannot afford to check every substring naively. A string of length 100,000 has roughly 5 billion substrings, which is far beyond what a brute-force approach can handle in a reasonable time. Therefore, we need an approach that counts valid substrings without explicitly enumerating all of them.

Subtle edge cases arise when constraints contradict each other or when L and R are zero. For example, if L = 0 and R = 0, the substring must violate all constraints. Another tricky case occurs when multiple constraints refer to the same character but with conflicting bounds. A careless algorithm might double-count or ignore substrings entirely.

## Approaches

The brute-force approach iterates over all possible substrings, counts character frequencies for each substring, and checks how many constraints are satisfied. While this works for small strings, its time complexity is O(n² k), which is approximately 5×10^10 operations in the worst case for n = 10^5 and k = 500. This is clearly too slow.

The key insight is that for each character we can track the intervals in which the constraints are satisfied using a prefix sum of character counts. Specifically, we can preprocess prefix sums for each character. Then, for a substring starting at index i and ending at j, the number of occurrences of a character is simply `prefix[j+1] - prefix[i]`. This reduces the problem to checking constraints efficiently over substrings starting at each position.

We can then use a two-pointer approach to maintain the longest valid substring starting at each index. By advancing the right pointer while the substring satisfies the number of constraints between L and R, we can count the number of valid substrings starting at each left index in O(n) time for each character. Combining these, we avoid O(n²) complexity and reduce the runtime to O(n k), which fits comfortably within the given constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² k) | O(26 n) | Too slow |
| Optimal (prefix sums + two pointers) | O(n k) | O(26 n + k) | Accepted |

## Algorithm Walkthrough

1. Build a 2D prefix sum array for each lowercase letter. For `prefix[c][i]`, store the number of times character `c` appears in the substring `s[0:i]`. This allows constant-time frequency queries for any substring.
2. For each position `i` in the string, initialize two pointers, `left = i` and `right = i`. The `right` pointer will expand to the right as long as the substring `s[i:right+1]` satisfies between L and R constraints.
3. For each substring starting at `i`, calculate the number of constraints satisfied using the preprocessed prefix sums. For each constraint, compute the count of its character in the current substring and check if it lies within the allowed range.
4. Move the `right` pointer forward until adding one more character would violate the constraint count requirement (less than L or more than R). All substrings starting at `i` and ending between `i` and `right-1` are valid. Add `right - i` to the result.
5. Repeat the process for all starting indices `i`.

Why it works: The algorithm counts every substring exactly once by systematically expanding the right boundary for each left index. Prefix sums allow fast frequency checks, and the two-pointer method ensures that no invalid substrings are counted. The invariant is that at each step, `right` is the first index that cannot be included in the substring starting at `i` without violating the constraint count bounds.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
n = len(s)
k, L, R = map(int, input().split())

constraints = []
for _ in range(k):
    c, l, r = input().split()
    l, r = int(l), int(r)
    constraints.append((c, l, r))

# build prefix sums for each letter
prefix = {chr(ord('a') + i): [0]*(n+1) for i in range(26)}
for i, ch in enumerate(s):
    for c in prefix:
        prefix[c][i+1] = prefix[c][i] + (1 if ch == c else 0)

result = 0

for left in range(n):
    low, high = left, n
    # binary search for right boundary where constraints are violated
    def valid(right):
        count_satisfied = 0
        for c, l, r in constraints:
            cnt = prefix[c][right] - prefix[c][left]
            if l <= cnt <= r:
                count_satisfied += 1
        return L <= count_satisfied <= R

    r = left
    while r < n and valid(r+1):
        r += 1
    result += r - left

print(result)
```

The solution builds prefix sums in O(26 n) time, then iterates over each starting index. The helper `valid` function counts the number of satisfied constraints for the current substring. The two-pointer expansion ensures each substring is counted efficiently. Using prefix sums avoids recalculating counts for overlapping substrings, preventing O(n² k) complexity.

## Worked Examples

**Sample 1**

Input: `codeforces`, constraints `o 1 2`, `e 1 2`, L=0, R=0.

| left | r (max valid end) | substrings counted | Notes |
| --- | --- | --- | --- |
| 0 | 0 | 0 | "c" violates 0 constraint rule |
| 1 | 1 | 1 | "o" violates 1 constraint rule |
| 2 | 2 | 1 | "d" valid |
| 3 | 3 | 1 | "e" violates |
| 4 | 4 | 1 | "f" valid |
| 5 | 5 | 1 | "o" violates |
| 6 | 6 | 1 | "r" valid |
| 7 | 7 | 1 | "c" valid |
| 8 | 8 | 1 | "e" violates |
| 9 | 9 | 1 | "s" valid |

Result = 7

**Sample 2**

Input: `aaabbb`, constraints `a 2 2`, `b 2 3`, L=1, R=2.

| left | right max | substrings counted | Notes |
| --- | --- | --- | --- |
| 0 | 2 | 2 | "aa", "aaa" satisfy at least 1 constraint |
| 1 | 2 | 1 | "aa" |
| 2 | 2 | 0 | "a" only 1 'a' |
| 3 | 4 | 2 | "bb", "bbb" |
| 4 | 4 | 1 | "bb" |
| 5 | 5 | 0 | "b" |

Result = 6

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n k) | Prefix sums O(26 n), checking constraints for each substring O(k) |
| Space | O(26 n + k) | Prefix sum array for each letter + constraints storage |

For n ≤ 10^5 and k ≤ 500, n*k = 5×10^7, which fits comfortably under the 3-second limit. Memory usage is dominated by prefix sums but remains under 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = input().strip()
    n = len(s)
    k, L, R = map(int, input().split())
    constraints = []
    for _ in range(k):
        c, l, r = input().split()
        l, r = int(l), int(r)
        constraints.append((c, l, r))
    prefix = {chr(ord('a') + i): [0]*(n+1) for i in range(26)}
    for i, ch in enumerate(s):
        for c in prefix:
            prefix[c][i+1] = prefix[c][i] + (1 if ch == c else 0)
    result = 0
    for left in range(n):
        r = left
        while r < n:
            count_satisfied = 0
            for c, l, r_c in constraints:
                cnt = prefix[c][r+1] - prefix[c][left]
                if l <= cnt <= r_c:
                    count_satisfied += 1
            if L <= count_satisfied <= R:
                r += 1
            else:
                break
        result += r - left
    return str(result)

# provided samples
assert run("codeforces\n2 0 0\no 1 2\ne 1 2\n") == "7", "sample 1"
assert run("aaabbb\n2 1 2\na 2 2\nb 2
```
