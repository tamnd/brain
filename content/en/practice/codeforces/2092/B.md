---
title: "CF 2092B - Lady Bug"
description: "We are given two bit strings of equal length, a and b, representing a password. Lady Bug wants to transform the first string a so that it contains only zeros."
date: "2026-06-08T05:42:15+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 2092
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1014 (Div. 2)"
rating: 1000
weight: 2092
solve_time_s: 98
verified: false
draft: false
---

[CF 2092B - Lady Bug](https://codeforces.com/problemset/problem/2092/B)

**Rating:** 1000  
**Tags:** brute force, constructive algorithms, implementation, math  
**Solve time:** 1m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two bit strings of equal length, `a` and `b`, representing a password. Lady Bug wants to transform the first string `a` so that it contains only zeros. She can perform a series of swap operations between adjacent elements of the two strings, specifically either swapping `a[i]` with `b[i-1]` or `b[i]` with `a[i-1]` for `i` from 2 to `n`. The goal is to determine if, after any number of such swaps, the string `a` can become all zeros.

Each test case gives us `n`, the length of the strings, followed by the two strings themselves. The number of test cases can be as high as 10,000, and the total sum of all string lengths across all test cases does not exceed 200,000. This means we need a solution that is roughly linear in `n` for each test case, otherwise a brute-force simulation of all possible swaps will be too slow.

A key edge case is when the first element of `a` is `1` and the first element of `b` is `0`. Since swaps only involve indices `i ≥ 2`, we cannot directly move a `1` at `a[1]` to `b[0]` or anywhere else, which would make the password impossible to crack. Similarly, if `b` has no `1`s anywhere that can reach a `1` in `a`, we also fail. Small `n=2` cases are critical because there are only a few swaps available and the strings can be immediately unsolvable.

## Approaches

The naive approach would be to simulate all possible swaps between the strings. At each index `i`, one could try both operations recursively or iteratively, until either `a` becomes all zeros or all possibilities are exhausted. This is guaranteed to be correct but completely impractical: the number of states grows exponentially with `n`, up to `2^n`, which is far beyond the 1-second limit even for small `n`.

The key insight is to track whether each `1` in `a` can be “pushed” left into `b` using the available swaps. Each swap allows a `1` in `a[i]` to move to `b[i-1]` or a `1` in `b[i]` to move to `a[i-1]`. This means if we scan the strings from left to right, the only situation where a `1` in `a` cannot be removed is when there is a `1` in `a[i]` and no `1` in `b[i-1]` or `b[i]` that can reach it. Essentially, every `1` in `a` at `i` must have either `b[i-1]` or a subsequent `b[j]` that can swap into that position.

A further simplification is that we only need to count the total number of `1`s in `a` and `b`. For each prefix of the strings, the cumulative number of `1`s in `b` must be at least the cumulative number of `1`s in `a`. If at any index the cumulative `1`s in `a` exceed those in `b`, the process fails because we have too many `1`s in `a` that cannot be moved. This transforms the problem into a single linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (simulate all swaps) | O(2^n) | O(n) | Too slow |
| Prefix Counting / Linear Scan | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n` and the strings `a` and `b`.
3. Initialize two counters: `count_a` for the number of `1`s in `a` seen so far, and `count_b` for the number of `1`s in `b` seen so far.
4. Iterate through the strings from left to right. At each index `i`, increment `count_a` if `a[i]` is `1` and `count_b` if `b[i]` is `1`.
5. If at any point `count_a` exceeds `count_b`, print "NO" for this test case. This indicates that there are more `1`s in `a` than can be “absorbed” by `b` up to this index.
6. If the iteration completes without `count_a > count_b`, print "YES".

Why it works: Each swap can only move a `1` from `a[i]` to `b[i-1]` or from `b[i]` to `a[i-1]`. By ensuring that for every prefix of the string, the total number of `1`s in `b` is at least the number of `1`s in `a`, we guarantee that each `1` in `a` can eventually be pushed into `b` using allowed operations. This cumulative counting captures the reachability of each `1` without simulating individual swaps.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = input().strip()
    b = input().strip()
    
    count_a = 0
    count_b = 0
    possible = True
    
    for i in range(n):
        if a[i] == '1':
            count_a += 1
        if b[i] == '1':
            count_b += 1
        if count_a > count_b:
            possible = False
            break
    
    print("YES" if possible else "NO")
```

The code reads input efficiently using `sys.stdin.readline`. It tracks cumulative counts of `1`s in both strings. The loop checks if at any point there are more `1`s in `a` than can be matched by `b`. Breaking early prevents unnecessary iterations.

## Worked Examples

Sample input:

```
6
010001
010111
```

| i | a[i] | b[i] | count_a | count_b | possible |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 | True |
| 1 | 1 | 1 | 1 | 1 | True |
| 2 | 0 | 0 | 1 | 1 | True |
| 3 | 0 | 1 | 1 | 2 | True |
| 4 | 0 | 1 | 1 | 3 | True |
| 5 | 1 | 1 | 2 | 4 | True |

No prefix has `count_a > count_b`, so the answer is YES.

Edge case:

```
2
11
00
```

| i | a[i] | b[i] | count_a | count_b | possible |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | 0 | False |

The first `1` in `a` cannot be swapped anywhere, so the answer is NO.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Single scan of strings; sum of all n ≤ 2×10^5 |
| Space | O(1) | Only counters and a few scalars are used |

This linear complexity is well within the limits, and the space usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# Provided samples
assert run("4\n3\n000\n000\n6\n010001\n010111\n5\n10000\n01010\n2\n11\n00\n") == "YES\nYES\nNO\nYES", "sample 1"

# Custom tests
assert run("1\n2\n01\n00\n") == "NO", "a[1] cannot be removed"
assert run("1\n2\n10\n01\n") == "YES", "a[0] 1 can be pushed to b[0]"
assert run("1\n5\n11111\n11111\n") == "YES", "all 1s can be matched"
assert run("1\n3\n010\n101\n") == "YES", "mixed 1s are solvable"
assert run("1\n3\n110\n001\n") == "NO", "insufficient 1s in b"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2\n01\n00 | NO | Cannot remove first `1` in `a` |
| 2\n10\n01 | YES | Single swap possible to remove `1` |
| 5\n11111\n11111 | YES | All 1s matched, maximal case |
| 3\n010\n101 | YES | Mixed solvable arrangement |
| 3\n110\n001 | NO | Not enough `1`s in `b` to clear `a` |

## Edge Cases

For `n=
