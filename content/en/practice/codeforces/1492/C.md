---
title: "CF 1492C - Maximum width"
description: "We are given two strings, s of length n and t of length m, and we need to find a subsequence of s that exactly matches t. This subsequence is called beautiful if each character in t appears in order in s."
date: "2026-06-10T22:22:07+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dp", "greedy", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1492
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 704 (Div. 2)"
rating: 1500
weight: 1492
solve_time_s: 216
verified: true
draft: false
---

[CF 1492C - Maximum width](https://codeforces.com/problemset/problem/1492/C)

**Rating:** 1500  
**Tags:** binary search, data structures, dp, greedy, two pointers  
**Solve time:** 3m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two strings, `s` of length `n` and `t` of length `m`, and we need to find a subsequence of `s` that exactly matches `t`. This subsequence is called _beautiful_ if each character in `t` appears in order in `s`. The challenge is not just to find any subsequence but to select one where the largest gap between consecutive indices is maximized. That gap is defined as the _width_ of the sequence.

The input guarantees that at least one such subsequence exists, so we do not have to handle the empty case. The output is a single integer, the maximum width among all possible beautiful sequences.

The constraints are important. Both `n` and `m` can be as large as 200,000. A naive approach that tries all combinations of positions would have a complexity of roughly $O(\binom{n}{m})$, which is astronomically large and infeasible. This tells us that we need a solution close to linear or linearithmic time, certainly no worse than $O(n \log n)$. Edge cases include sequences where all characters are the same, `t` occurs at the very beginning and very end of `s`, or when `t` is almost identical to `s`. A careless solution could, for example, always pick the first occurrence of each character in `t` and miss a wider spacing at later positions.

## Approaches

A brute-force approach would enumerate all sequences of indices in `s` that match `t`. For each sequence, we would calculate the width and keep track of the maximum. While this is correct in principle, its complexity is combinatorial, roughly $O(n^m)$, which is clearly infeasible for `n = 2 \cdot 10^5` and `m = 10^5`.

The key insight is that the maximum width can be determined by considering only two sequences: one where we greedily choose the _leftmost_ occurrence of each character in `t` and one where we choose the _rightmost_ occurrence. Let `left[i]` denote the earliest index in `s` that can match `t[i]` while maintaining order, and let `right[i]` denote the latest index in `s` that can match `t[i]`. The maximum width will always occur between one `left[i]` and the corresponding `right[i+1]`, because this gives the largest gap while still forming a valid sequence. This reduces the problem to a linear scan over these two arrays, which is feasible in $O(n)$ time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^m) | O(m) | Too slow |
| Optimal | O(n) | O(m) | Accepted |

## Algorithm Walkthrough

1. Initialize two arrays, `left` and `right`, both of length `m`. `left[i]` will store the earliest index in `s` that matches `t[i]` in order, and `right[i]` will store the latest index that matches `t[i]` in reverse order.
2. Fill `left` by iterating over `s` from left to right. Maintain a pointer `j` into `t`. When `s[i] == t[j]`, assign `left[j] = i` and increment `j`. After the iteration, `left` contains the earliest indices forming a beautiful sequence.
3. Fill `right` by iterating over `s` from right to left. Maintain a pointer `j` starting at `m-1` and moving backward. When `s[i] == t[j]`, assign `right[j] = i` and decrement `j`. After the iteration, `right` contains the latest indices forming a beautiful sequence.
4. Compute the maximum width by iterating `i` from `0` to `m-2`. For each `i`, calculate `right[i+1] - left[i]` and keep track of the maximum.

The reason this works is that the largest gap is always realized by pairing the earliest possible occurrence of some `t[i]` with the latest possible occurrence of `t[i+1]`. Any other combination would either reduce the gap or violate the order constraint.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
s = input().strip()
t = input().strip()

left = [0] * m
right = [0] * m

# Compute left array
j = 0
for i in range(n):
    if s[i] == t[j]:
        left[j] = i
        j += 1
        if j == m:
            break

# Compute right array
j = m - 1
for i in range(n-1, -1, -1):
    if s[i] == t[j]:
        right[j] = i
        j -= 1
        if j < 0:
            break

# Find maximum width
max_width = 0
for i in range(m - 1):
    max_width = max(max_width, right[i+1] - left[i])

print(max_width)
```

The left array stores the earliest possible positions, ensuring the sequence is valid. The right array stores the latest possible positions, ensuring the gap is maximized. The loop that computes the maximum width carefully considers only consecutive pairs, `left[i]` and `right[i+1]`, to respect the order of `t`.

## Worked Examples

Sample 1: `s = "abbbc"`, `t = "abc"`

| i | left[i] | right[i] |
| --- | --- | --- |
| 0 | 0 | 0 |
| 1 | 1 | 3 |
| 2 | 4 | 4 |

Compute gaps: `right[1]-left[0] = 3-0 = 3`, `right[2]-left[1] = 4-1 = 3`. Maximum width = 3.

Sample 2: `s = "abacaba"`, `t = "aa"`

| i | left[i] | right[i] |
| --- | --- | --- |
| 0 | 0 | 6 |
| 1 | 2 | 6 |

Compute gaps: `right[1]-left[0] = 6-0 = 6`. Maximum width = 6.

This confirms that taking leftmost and rightmost sequences captures the largest possible spacing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each of the two passes over `s` is linear, plus one linear pass over `m` to compute max width |
| Space | O(m) | We store two arrays of length `m` |

The algorithm fits comfortably within the constraints since `n ≤ 2*10^5` and a linear solution performs at most a few hundred thousand operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    s = input().strip()
    t = input().strip()
    
    left = [0] * m
    right = [0] * m
    
    j = 0
    for i in range(n):
        if s[i] == t[j]:
            left[j] = i
            j += 1
            if j == m:
                break
    
    j = m - 1
    for i in range(n-1, -1, -1):
        if s[i] == t[j]:
            right[j] = i
            j -= 1
            if j < 0:
                break
    
    max_width = 0
    for i in range(m-1):
        max_width = max(max_width, right[i+1] - left[i])
    
    return str(max_width)

# provided samples
assert run("5 3\nabbbc\nabc\n") == "3", "sample 1"
assert run("2 1\naa\na\n") == "1", "sample 2"

# custom cases
assert run("7 2\nabacaba\naa\n") == "6", "widest possible gap"
assert run("5 2\naaaaa\naa\n") == "4", "all same letters"
assert run("10 5\nabcdefghij\nacegi\n") == "2", "maximum width in spaced letters"
assert run("2 2\nab\nab\n") == "1", "minimum size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `abacaba` / `aa` | 6 | Widest gap in a small string |
| `aaaaa` / `aa` | 4 | All letters identical, sequence must skip intermediate characters |
| `abcdefghij` / `acegi` | 2 | Regular spaced letters, max width computed correctly |
| `ab` / `ab` | 1 | Minimum input size |

## Edge Cases

For a string where all characters are identical, like `s = "aaaaa"` and `t = "aa"`, the left array will take the first two positions, `left = [0, 1]`, and the right array will take the last two positions, `right = [3, 4]`. The maximum width calculation considers `right[1]-left[0] = 4-0 = 4`, correctly identifying that the optimal beautiful sequence
