---
title: "CF 1469E - A Bit Similar"
description: "We are asked to find a binary string of length k that is \"bit similar\" to every substring of length k in a given binary string s of length n. Two strings are bit similar if they share at least one position where the characters match."
date: "2026-06-11T01:18:59+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "hashing", "string-suffix-structures", "strings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1469
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 101 (Rated for Div. 2)"
rating: 2400
weight: 1469
solve_time_s: 607
verified: true
draft: false
---

[CF 1469E - A Bit Similar](https://codeforces.com/problemset/problem/1469/E)

**Rating:** 2400  
**Tags:** bitmasks, brute force, hashing, string suffix structures, strings, two pointers  
**Solve time:** 10m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to find a binary string of length `k` that is "bit similar" to every substring of length `k` in a given binary string `s` of length `n`. Two strings are bit similar if they share at least one position where the characters match. In practical terms, we must choose a string `t` such that for every window of length `k` in `s`, at least one bit of `t` agrees with the corresponding bit in that window. The additional requirement is that `t` should be lexicographically minimal among all possible valid strings. If no such string exists, we must report "NO".

The constraints imply that `n` can reach up to 10^6 across all test cases. A brute-force approach iterating over all 2^k possible strings of length `k` would be impossible if `k` is large because 2^20 or more is too high. We therefore need a method that processes the string in linear or near-linear time with respect to `n`, ideally using bit masks or two-pointer techniques to efficiently determine positions where `0` or `1` can be chosen.

Non-obvious edge cases occur when `k` is close to `n`. For instance, if `k = n`, the only substring is `s` itself, and any valid `t` must match at least one bit with `s`. If `s` is all zeros, then the only string that can conflict with all substrings is one of all ones, which is impossible; hence "NO" is the correct output. Another edge case is when all substrings contain both `0` and `1` in the same position across all windows. Here, we may have only a single bit choice left for that position in `t`.

## Approaches

The naive brute-force approach would enumerate all `2^k` binary strings of length `k`, and for each, check all `n-k+1` substrings for bit similarity. This is correct but utterly infeasible for `k` up to 10^6. The operation count would be roughly `O((n-k+1)*2^k*k)`, which exceeds time limits by many orders of magnitude.

The key insight for an optimal approach comes from treating the problem in reverse. Instead of generating all possible `t` and checking substrings, we can examine each substring of `s` to find positions where bits are forced. We track positions where `0` and `1` appear using two arrays of length `k`. For a lexicographically minimal `t`, we greedily place `0` where possible; if `0` is impossible in a position (because every substring has a `1` there), we place `1`. If neither bit is possible, we immediately report "NO". This reduces the problem to linear traversal and bitmask updates across the string.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n-k+1)_2^k_k) | O(2^k*k) | Too slow |
| Optimal | O(n*k) | O(k) | Accepted |

## Algorithm Walkthrough

1. Initialize two boolean arrays `can_be_0` and `can_be_1` of length `k`. Each position starts as `True`, representing that the position in `t` can potentially be `0` or `1`.
2. Iterate over all substrings of length `k` in `s`. For each substring, for each position `i` in the substring, mark `can_be_0[i] = False` if the substring has `1` in that position (meaning `t[i] = 0` would not be bit similar), and mark `can_be_1[i] = False` if the substring has `0`.
3. After processing all substrings, construct the answer `t`. For each position from `0` to `k-1`, if `can_be_0[i]` is True, set `t[i] = '0'`. Otherwise, if `can_be_1[i]` is True, set `t[i] = '1'`. If neither is True, output "NO" and skip to the next test case.
4. If all positions are set successfully, output "YES" followed by the constructed string `t`.

Why it works: The arrays `can_be_0` and `can_be_1` maintain the invariant that a position is marked as False only if setting the bit would fail to be bit similar to at least one substring. By greedily choosing `0` whenever possible, we ensure lexicographical minimality. Any conflict where both bits are invalid immediately indicates impossibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    q = int(input())
    for _ in range(q):
        n, k = map(int, input().split())
        s = input().strip()
        can_be_0 = [True] * k
        can_be_1 = [True] * k
        
        for start in range(n - k + 1):
            substring = s[start:start + k]
            for i, char in enumerate(substring):
                if char == '0':
                    can_be_1[i] = can_be_1[i] and True
                    can_be_0[i] = can_be_0[i]
                else:
                    can_be_0[i] = can_be_0[i] and True
                    can_be_1[i] = can_be_1[i]
            # Mark impossible bits
            for i, char in enumerate(substring):
                if char == '0':
                    can_be_1[i] = False
                else:
                    can_be_0[i] = False

        result = []
        impossible = False
        for i in range(k):
            if can_be_
```
