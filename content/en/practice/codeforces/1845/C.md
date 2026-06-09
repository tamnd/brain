---
title: "CF 1845C - Strong Password"
description: "We are asked to determine whether Monocarp can construct a password of exactly length m that satisfies three conditions: each digit must lie between the corresponding digits of two strings l and r, the password must only use digits 0 through 9, and it must not appear as a…"
date: "2026-06-09T05:55:02+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dp", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 1845
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 151 (Rated for Div. 2)"
rating: 1400
weight: 1845
solve_time_s: 79
verified: false
draft: false
---

[CF 1845C - Strong Password](https://codeforces.com/problemset/problem/1845/C)

**Rating:** 1400  
**Tags:** binary search, dp, greedy, strings  
**Solve time:** 1m 19s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to determine whether Monocarp can construct a password of exactly length `m` that satisfies three conditions: each digit must lie between the corresponding digits of two strings `l` and `r`, the password must only use digits `0` through `9`, and it must not appear as a subsequence in a given string `s` representing the database of existing passwords. The input consists of multiple test cases, each specifying `s`, `m`, `l`, and `r`. For each case, the output is "YES" if at least one valid password exists and "NO" otherwise.

The main challenge is that `s` can be very long, up to 300,000 characters, and there can be up to 10,000 test cases. This rules out any algorithm that checks all possible passwords individually, since even for the small `m` limit of 10, there could be up to $10^{10}$ candidates in the worst case. The non-obvious difficulty lies in ensuring that the chosen password does not appear as a subsequence in `s`, which requires reasoning about all positions in `s` without explicitly enumerating them.

A naive approach could try generating all sequences in the range `[l_i, r_i]` for each position and checking if each is a subsequence of `s`. For example, if `s = "123412341234"`, `m = 3`, `l = "111"`, and `r = "444"`, the naive approach might iterate through "111", "112", ..., "444". This is infeasible because there are $4^3 = 64$ sequences in this small example, but the approach scales poorly for larger ranges or `m = 10`. Moreover, careless implementations may incorrectly handle subsequence checking, particularly when digits repeat or when `l` and `r` are equal in some positions.

## Approaches

The brute-force solution would generate every password candidate that fits the digit constraints `[l_i, r_i]` for each position and check if it appears as a subsequence in `s`. Checking a password as a subsequence requires scanning `s` linearly, so for a candidate of length `m` and a string `s` of length `n`, this takes $O(n)$ time. Since the number of candidates can be up to $10^{10}$ for `m = 10`, this approach is clearly impractical.

The key observation is that `m` is small, at most 10. This allows us to treat the problem as a bounded search over the password positions. Instead of iterating blindly, we can use dynamic programming to record which positions in `s` can match partial passwords. Specifically, we preprocess `s` to know for every position and every digit `d` where the next occurrence of `d` is. This allows us to advance through `s` quickly when checking subsequences, reducing a naive $O(n)$ scan to $O(1)$ per position once the preprocessing is done. Using a recursive backtracking with memoization or DFS on the password positions, we explore the range `[l_i, r_i]` for each character and stop early when a valid password is found.

The observation that `m <= 10` and digits are only `0-9` is crucial. It allows a recursive search over `m` positions, trying at most 10 digits per position, giving a worst-case branching of $10^{10}$, but practically the preprocessing of `s` eliminates most impossible paths quickly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(10^m \cdot | s | )) |
| Optimal (next-occurrence DP + DFS) | (O( | s | \cdot 10 + 10^m)) amortized |

## Algorithm Walkthrough

1. Preprocess `s` into a next-occurrence table `next_pos[i][d]` where `i` is a position in `s` and `d` is a digit from `0` to `9`. This table stores the earliest index ≥ i where digit `d` occurs in `s`. We build it from the end of `s` backwards, initializing `next_pos[n][d] = n` (out-of-bounds) and updating each `i` with either `i` if `s[i] == d` or the value from `i+1`.
2. Define a recursive function `can_form(pos, s_index)` that checks whether we can complete a password starting from password position `pos` using `s` starting at `s_index`. If `pos == m`, the password is fully built and does not appear in `s`, so return True. Otherwise, iterate over all digits `d` in the range `[l[pos], r[pos]]`.
3. For each digit `d`, use `next_pos[s_index][d]` to determine the earliest place `s_next` where this digit occurs in `s`. If `s_next` is at the end of `s`, then the remaining password cannot appear as a subsequence beyond this point, meaning we can place `d` safely.
4. Recursively call `can_form(pos+1, s_next+1)`. If any branch returns True, the answer is "YES". Otherwise, after exploring all digits for the current position, return False, meaning no valid password exists.
5. Run the above steps for each test case, printing "YES" or "NO".

Why it works: The preprocessing guarantees that for every password position, we know exactly where the corresponding digit can be matched in `s`. By recursively exploring only feasible digits and stopping when a password is completed without matching `s`, we ensure correctness. The invariant is that `s_index` always points to the current prefix of `s` that could potentially match the password, and any successful completion implies a password not appearing as a subsequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        s = input().strip()
        m = int(input())
        l = input().strip()
        r = input().strip()
        n = len(s)
        
        # Preprocess next occurrence
        next_pos = [[n]*10 for _ in range(n+1)]
        for i in range(n-1, -1, -1):
            for d in range(10):
                next_pos[i][d] = next_pos[i+1][d]
            next_pos[i][int(s[i])] = i
        
        memo = {}
        def can_form(pos, s_index):
            if pos == m:
                return True
            key = (pos, s_index)
            if key in memo:
                return memo[key]
            for d in range(int(l[pos]), int(r[pos])+1):
                next_i = next_pos[s_index][d]
                if next_i == n:
                    memo[key] = True
                    return True
                if can_form(pos+1, next_i+1):
                    memo[key] = True
                    return True
            memo[key] = False
            return False
        
        print("YES" if can_form(0, 0) else "NO")
```

The solution is structured to first preprocess `s` efficiently, then explore password possibilities recursively while leveraging memoization to avoid redundant searches. Boundary conditions, such as when a digit does not appear in `s`, are handled correctly by checking `next_i == n`.

## Worked Examples

**Sample 1**

| pos | s_index | digits tried | result |
| --- | --- | --- | --- |
| 0 | 0 | 5,6 | password "50" found |

Explanation: At `pos=0`, digit `5` maps to `s_index=5` (first occurrence of `5`). At `pos=1`, digit `0` maps beyond `s`, so "50" is valid.

**Sample 2**

| pos | s_index | digits tried | result |
| --- | --- | --- | --- |
| 0 | 0 | 1,2,3,4 | all fail |

Explanation: Every digit combination within `[111,444]` appears as a subsequence in `s="123412341234"`, so no valid password exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O( | s |
| Space | O( | s |

The solution handles `|s| ≤ 3*10^5` and `m ≤ 10` efficiently within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided samples
assert run("""5
88005553535123456
2
50
56
123412341234
3
111
444
1234
4
4321
4321
459
2
49
59
00010
2
10
11
""") == "YES\nNO\nYES\nNO\nYES"

# custom cases
assert run("""1
1111
3
```
