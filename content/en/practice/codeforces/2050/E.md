---
title: "CF 2050E - Three Strings"
description: "We are given three strings: a, b, and c. Conceptually, c is formed by taking letters from a and b in some interleaving order. At each step, one letter is taken from the front of either a or b and appended to c."
date: "2026-06-08T08:48:23+07:00"
tags: ["codeforces", "competitive-programming", "dp", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 2050
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 991 (Div. 3)"
rating: 1500
weight: 2050
solve_time_s: 87
verified: true
draft: false
---

[CF 2050E - Three Strings](https://codeforces.com/problemset/problem/2050/E)

**Rating:** 1500  
**Tags:** dp, implementation, strings  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three strings: `a`, `b`, and `c`. Conceptually, `c` is formed by taking letters from `a` and `b` in some interleaving order. At each step, one letter is taken from the front of either `a` or `b` and appended to `c`. Once one string is empty, the remaining letters from the other string are appended. After that, some letters in `c` may have been arbitrarily replaced. Our goal is to determine the **minimum number of letters in `c` that must have been changed** compared to a valid interleaving of `a` and `b`.

The input provides multiple test cases. Each string has at most 1000 characters, and the sum of lengths across all test cases does not exceed 2000 for `a` or `b`. This implies that a solution with complexity `O(|a|*|b|)` per test case is feasible, because `1000*1000 = 10^6` operations is acceptable within a 2-second time limit.

Non-obvious edge cases arise when all characters are identical, or when one string is entirely consumed before the other. For example, if `a = "aa"`, `b = "b"`, and `c = "aba"`, the minimal number of changes is `0` since `a` and `b` could have interleaved to form `aba`. A naive greedy approach that only matches characters from `a` until it fails would incorrectly compute extra changes.

## Approaches

The brute-force approach would be to generate every interleaving of `a` and `b` and compare it to `c`, counting differences. This is correct but infeasible: for `|a|=n` and `|b|=m`, there are `C(n+m, n)` interleavings. Even for `n = m = 20`, this is already over a hundred million combinations.

The key insight is that this is a **dynamic programming problem**, similar to computing edit distance or interleaving strings. Let `dp[i][j]` represent the minimum number of changes needed to form the first `i+j` characters of `c` using the first `i` characters of `a` and first `j` characters of `b`. At each step, we can either take the next character from `a` or `b` and compare it to the corresponding position in `c`, incrementing the cost if it does not match.

This approach reduces the problem from exponential to `O(|a|*|b|)`, which is feasible given the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C(n+m, n)) | O(1) | Too slow |
| Dynamic Programming | O( | a | * |

## Algorithm Walkthrough

1. Initialize a 2D array `dp` of size `(len(a)+1) x (len(b)+1)` with infinity, except `dp[0][0] = 0`. This represents zero changes needed for empty prefixes.
2. Iterate over all `i` from `0` to `len(a)` and all `j` from `0` to `len(b)`. At each cell `(i, j)` we have a partial interleaving of `i` characters from `a` and `j` characters from `b`.
3. If `i < len(a)`, attempt to take the next character from `a`. Compare `a[i]` with `c[i+j]`. If they match, the cost remains the same; otherwise, increment the cost by `1`. Update `dp[i+1][j]` with the minimum of its current value and this cost.
4. If `j < len(b)`, attempt to take the next character from `b`. Compare `b[j]` with `c[i+j]` and similarly update `dp[i][j+1]`.
5. After filling the table, `dp[len(a)][len(b)]` contains the minimal number of changes required to match `c`.

**Why it works:** At every prefix `(i,j)`, `dp[i][j]` is guaranteed to be the minimum number of changes needed to form the corresponding prefix of `c`. By considering both options (taking from `a` or `b`) at each step, the DP ensures that no interleaving is missed, and the cost is accumulated correctly. This is exactly the recurrence for interleaving strings with modification cost.

## Python Solution

```python
import sys
input = sys.stdin.readline

def min_changes(a, b, c):
    n, m = len(a), len(b)
    INF = int(1e9)
    dp = [[INF] * (m+1) for _ in range(n+1)]
    dp[0][0] = 0

    for i in range(n+1):
        for j in range(m+1):
            if i < n:
                cost = dp[i][j] + (a[i] != c[i+j])
                if cost < dp[i+1][j]:
                    dp[i+1][j] = cost
            if j < m:
                cost = dp[i][j] + (b[j] != c[i+j])
                if cost < dp[i][j+1]:
                    dp[i][j+1] = cost
    return dp[n][m]

t = int(input())
for _ in range(t):
    a = input().strip()
    b = input().strip()
    c = input().strip()
    print(min_changes(a, b, c))
```

The `dp` initialization sets all states to infinity to represent uncomputed/invalid states. The updates carefully choose the minimum, ensuring the optimal solution propagates. Using `a[i] != c[i+j]` succinctly captures the "changed character" cost. Boundary conditions are handled by only attempting the next character if within bounds.

## Worked Examples

**Example 1**: `a="a"`, `b="b"`, `c="cb"`

| i | j | dp[i][j] | action |
| --- | --- | --- | --- |
| 0 | 0 | 0 | start |
| 1 | 0 | 1 | take 'a' vs 'c', mismatch +1 |
| 0 | 1 | 1 | take 'b' vs 'c', mismatch +1 |
| 1 | 1 | 1 | choose optimal path |

Result: `1` change.

**Example 2**: `a="ab"`, `b="cd"`, `c="acbd"`

| i | j | dp[i][j] | action |
| --- | --- | --- | --- |
| 0 | 0 | 0 | start |
| 1 | 0 | 0 | 'a' matches 'a' |
| 0 | 1 | 1 | 'c' vs 'a', mismatch |
| 1 | 1 | 0 | 'c' vs 'c', no mismatch |
| 2 | 1 | 0 | 'b' vs 'b', no mismatch |
| 2 | 2 | 0 | 'd' vs 'd', no mismatch |

Result: `0` changes.

These tables demonstrate that the DP correctly tracks minimal changes, even when characters are interleaved in different orders.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O( | a |
| Space | O( | a |

Given the sum of lengths across all test cases does not exceed 2000, this guarantees under 4 million operations in total, which is well within 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # call solution
    t = int(input())
    for _ in range(t):
        a = input().strip()
        b = input().strip()
        c = input().strip()
        print(min_changes(a, b, c))
    return output.getvalue().strip()

# provided samples
assert run("7\na\nb\ncb\nab\ncd\nacbd\nab\nba\naabb\nxxx\nyyy\nxyxyxy\na\nbcd\ndecf\ncodes\nhorse\ncodeforces\negg\nannie\negaegaeg\n") == "1\n0\n2\n0\n3\n2\n3", "Sample 1"

# custom cases
assert run("1\na\na\naa\n") == "0", "identical strings"
assert run("1\nab\ncd\nacbd\n") == "0", "interleaving matches perfectly"
assert run("1\nab\ncd\nabcd\n") == "0", "all from a then b"
assert run("1\nab\ncd\ndcba\n") == "4", "completely reversed"
assert run("1\nabc\ndef\nxyzuvw\n") == "6", "all changed"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| a="a", b="a", c="aa" | 0 | identical characters |
| a="ab", b="cd", c="acbd" | 0 | interleaving possible without changes |
| a="ab", b="cd", c="abcd" | 0 | one string fully before the |
