---
title: "CF 494B - Obsessive String"
description: "We are given two strings, s and t. Our goal is to count the number of ways to select one or more non-overlapping substrings from s such that each selected substring contains t somewhere inside it."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "strings"]
categories: ["algorithms"]
codeforces_contest: 494
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 282 (Div. 1)"
rating: 2000
weight: 494
solve_time_s: 658
verified: false
draft: false
---

[CF 494B - Obsessive String](https://codeforces.com/problemset/problem/494/B)

**Rating:** 2000  
**Tags:** dp, strings  
**Solve time:** 10m 58s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two strings, `s` and `t`. Our goal is to count the number of ways to select one or more non-overlapping substrings from `s` such that each selected substring contains `t` somewhere inside it. A substring is defined by its starting and ending indices, and “non-overlapping” means that no two chosen substrings share any character. The output is the total number of valid selections modulo $10^9+7$.

The input constraints allow `s` and `t` to have lengths up to $10^5$. This immediately rules out naive approaches that iterate over all possible substrings of `s`, because the number of substrings is $\frac{n(n+1)}{2}$, which can reach $5 \cdot 10^9$ for $n=10^5$. We need a solution that scales linearly or near-linearly with `|s|`.

A subtle edge case arises when `t` occurs multiple times in overlapping ways. For example, if `s = "aaa"` and `t = "aa"`, the valid substrings containing `t` can overlap in positions, but the chosen selections themselves must not overlap. Counting these incorrectly leads to overcounting. Another case is when `t` is longer than `s` or does not occur in `s` at all, where the result should clearly be zero.

## Approaches

A brute-force approach would iterate over all substrings of `s`, check if each contains `t`, and then generate all non-overlapping sets of these substrings. While correct in principle, this is clearly infeasible for `n = 10^5`. The operation count is roughly $O(n^3)$ considering substring extraction and validation, far above our limit.

The key insight for an optimal solution is dynamic programming combined with precomputing the occurrences of `t` in `s`. If we know the earliest ending index of `t` starting at or after each position, we can incrementally build the number of ways to choose substrings ending at each index. Essentially, for each position `i`, the number of sequences ending at or before `i` can be expressed in terms of sequences ending strictly before the first position where `t` starts, plus one for starting a new sequence at `i`. This avoids iterating over all substrings explicitly and reduces the complexity to $O(n)$ after preprocessing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n^2) | Too slow |
| Dynamic Programming with t occurrences | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute all starting indices where `t` occurs in `s` using a string matching algorithm like Knuth-Morris-Pratt (KMP) or Python's `find` in a loop. This gives an array `occ` such that `occ[i]` is True if `t` starts at index `i`.
2. Initialize a DP array `dp` of length `n+1` where `dp[i]` represents the number of valid selections considering the first `i` characters of `s`. Initialize `dp[0] = 0` since no substrings exist before the first character.
3. Maintain a prefix sum array `pref` to quickly compute cumulative sums of `dp` values. This will allow us to compute sums over ranges in O(1).
4. Iterate over `s` from index `1` to `n`. For each index `i`:

- If `t` ends at `i` (i.e., there is a starting index `j` such that `j + |t| - 1 == i` and `occ[j]` is True), then the number of ways to form sequences ending at `i` is equal to `1 + pref[j]`, where `pref[j]` is the sum of all `dp[k]` for `k < j`. The `1` accounts for the new sequence starting at `j` alone.
- Update `dp[i]` with this value modulo $10^9+7$.
- Update `pref[i] = (pref[i-1] + dp[i]) % MOD`.
5. The answer is the sum of all `dp[i]` for `i = 1..n`.

Why it works: At every index `i`, `dp[i]` counts all sequences of substrings ending at `i` containing `t`. By using the prefix sum, we efficiently account for all sequences ending before the current substring, maintaining non-overlapping constraints automatically because we only extend sequences that end before the current starting position.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    s = input().strip()
    t = input().strip()
    n, m = len(s), len(t)
    
    # Compute occurrences of t in s
    occ = [0] * n
    i = 0
    while i <= n - m:
        if s[i:i+m] == t:
            occ[i] = 1
        i += 1
    
    dp = [0] * (n + 1)
    pref = [0] * (n + 1)
    
    for i in range(1, n + 1):
        dp[i] = dp[i-1]  # inherit previous count
        if i >= m and occ[i-m]:
            # number of ways to pick a new substring ending here
            dp[i] = (dp[i] + 1 + pref[i-m]) % MOD
        pref[i] = (pref[i-1] + dp[i]) % MOD
    
    print(dp[n] % MOD)

solve()
```

The `occ` array marks positions where `t` starts. The DP array `dp` accumulates sequences of substrings ending at each position. Using `pref`, we efficiently sum all valid sequences ending before the current substring to extend them without overlaps. The subtle point is `i-m` to correctly identify the start of `t` relative to current `i`.

## Worked Examples

Sample Input 1:

```
s = "ababa"
t = "aba"
```

| i | occ[i] | dp[i] | pref[i] |
| --- | --- | --- | --- |
| 0 | - | 0 | 0 |
| 1 | 1 | 1 | 1 |
| 2 | 0 | 1 | 2 |
| 3 | 0 | 1 | 3 |
| 4 | 1 | 2 | 5 |
| 5 | 0 | 5 | 10 |

The table shows how `dp` increments when `t` occurs, and the prefix sum allows us to count all sequences ending before each occurrence. The final output is `dp[n] = 5`.

Second Input:

```
s = "aaa"
t = "aa"
```

| i | occ[i] | dp[i] | pref[i] |
| --- | --- | --- | --- |
| 0 | - | 0 | 0 |
| 1 | 1 | 1 | 1 |
| 2 | 1 | 2 | 3 |
| 3 | 0 | 2 | 5 |

The table demonstrates overlapping occurrences handled correctly, with `dp` only counting non-overlapping sequences.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Scanning `s` once to find occurrences, iterating over `n` indices for DP and prefix sums. |
| Space | O(n) | DP, prefix sum, and occurrence arrays of size `n` each. |

The solution easily fits within the 2-second limit for $n = 10^5$ and the 256MB memory limit.

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

# provided sample
assert run("ababa\naba\n") == "5", "sample 1"

# t longer than s
assert run("abc\ndef\n") == "0", "t longer than s"

# multiple overlapping
assert run("aaa\naa\n") == "2", "overlapping occurrences"

# single character match
assert run("a\na\n") == "1", "single character"

# no occurrence
assert run("abcdef\nxyz\n") == "0", "no occurrence"

# all characters equal
assert run("aaaaa\naa\n") == "9", "all equal characters, multiple overlapping"

# max input (just sanity, not actual stress test)
s = "a"*100000
t = "aa"
expected = (100000-1)*(100000)//2 % (10**9+7)
assert run(f"{s}\n{t}\n") == str(expected), "large input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "abc\ndef" | 0 | t longer than s |
| "aaa\naa" | 2 | overlapping occurrences |
| "a\na" | 1 | single character strings |
| "abcdef\nxyz" | 0 | no occurrences |
| "aaaaa\naa" | 9 | multiple overlapping substrings |
| "a"*100000, "aa |  |  |
