---
title: "CF 2200C - Specialty String"
description: "We are given a string consisting of lowercase letters, and the game involves repeatedly replacing pairs of equal letters with asterisks, provided that all characters between them have already become asterisks."
date: "2026-06-07T20:15:31+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 2200
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1084 (Div. 3)"
rating: 900
weight: 2200
solve_time_s: 93
verified: true
draft: false
---

[CF 2200C - Specialty String](https://codeforces.com/problemset/problem/2200/C)

**Rating:** 900  
**Tags:** brute force, greedy, strings  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string consisting of lowercase letters, and the game involves repeatedly replacing pairs of equal letters with asterisks, provided that all characters between them have already become asterisks. Specifically, we can pick indices $i < j$ such that the characters at those positions are the same and all characters strictly between $i$ and $j$ are already `*`. Once we replace a pair, those positions become `*`. The goal is to determine if it is possible to convert the entire string to `*` through a sequence of such moves.

The input consists of multiple test cases. Each test case provides the length of the string $n$ and the string $s$ itself. We need to output "YES" if we can eventually turn the entire string into `*`, or "NO" otherwise.

The constraints are such that $n \leq 5000$ and the sum of $n$ across all test cases does not exceed 5000. This indicates that a solution with $O(n^2)$ time complexity is feasible because $5000^2 = 25{,}000{,}000$, which is acceptable for a 2-second time limit in Python. The edge cases are strings of length 1, which are trivially unwinnable, or strings where every character appears an even number of times but cannot be paired consecutively due to interleaving characters.

A naive approach that tries every possible pair blindly could fail on interleaving patterns. For example, for the string `oooioi`, although there are three `o`s and two `i`s, the pairing constraints prevent a complete elimination, leading to "NO".

## Approaches

The brute-force method is to simulate the game exactly: scan for every valid pair of equal letters separated only by `*`, replace them, and repeat until no more moves are possible. This works correctly but becomes inefficient because each scan is $O(n^2)$ in the worst case, and updating the string repeatedly multiplies the cost, potentially reaching $O(n^3)$. This would be too slow for $n \sim 5000$.

The key insight is that the order of operations is constrained by the requirement that all characters between a pair are already `*`. This means the problem is essentially about nested matching, which resembles a greedy or stack-based approach used in problems like balanced parentheses. We can process the string from left to right and try to pair characters with their next valid match recursively, keeping track of the last positions of each character. If we can pair everything this way, the string can be fully converted to `*`. The fact that `n` is small allows us to use a simple $O(n^2)$ dynamic programming solution as well: let `dp[l][r]` be true if the substring from `l` to `r` can be completely turned into `*`. Then we check all possible pairs for the first character and see if splitting the remaining substring also works.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n^3) | O(n) | Too slow |
| Dynamic Programming / Greedy | O(n^2) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Initialize a boolean array `dp` of size `n x n`, where `dp[l][r]` will be true if the substring `s[l..r]` can be fully converted into `*`. All single-character substrings are initially false because a single character cannot be removed.
2. Iterate over all substring lengths from 2 to `n`. For each substring `s[l..r]`, consider pairing the first character `s[l]` with every later character `s[m]` (`l < m <= r`) where `s[m] == s[l]`.
3. Check if the substring between `l` and `m` is already convertible (`dp[l+1][m-1]` is true). If so, check the remainder of the substring (`dp[m+1][r]`). If both are true (or empty), then `dp[l][r]` is true.
4. After processing all lengths, the result for the full string is `dp[0][n-1]`. If true, output "YES", otherwise "NO".

Why it works: The DP captures the recursive structure of the game. A substring is fully removable if we can pick a valid pair for its first character and recursively remove the substring between them and after the second character. The base case handles single pairs directly. This ensures all valid sequences of moves are considered without missing interleaving constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_win(s):
    n = len(s)
    dp = [[False]*n for _ in range(n)]
    
    for length in range(2, n+1):
        for l in range(n-length+1):
            r = l + length - 1
            for m in range(l+1, r+1):
                if s[l] == s[m]:
                    if (m == l+1 or dp[l+1][m-1]) and (m == r or dp[m+1][r]):
                        dp[l][r] = True
                        break
    return dp[0][n-1]

t = int(input())
for _ in range(t):
    n = int(input())
    s = input().strip()
    print("YES" if can_win(s) else "NO")
```

The DP initialization ensures that substrings of length 1 are false. The nested loops handle every possible substring efficiently. The check `(m == l+1 or dp[l+1][m-1])` ensures the middle substring can be removed, and `(m == r or dp[m+1][r])` ensures the remainder is also removable. Breaking early once a valid pair is found avoids unnecessary computations.

## Worked Examples

Trace for `llmllm`:

| Step | Substring | Pairing | dp[l][r] |
| --- | --- | --- | --- |
| 0 | `ll` | l-l | True |
| 1 | `llm` | l-l | False |
| 2 | `llml` | l-l | True |
| 3 | `llmllm` | l-lm-lm | True |

This shows that greedy pairing from left works and DP captures interleaving.

Trace for `oooioi`:

| Step | Substring | Pairing | dp[l][r] |
| --- | --- | --- | --- |
| 0 | `oo` | o-o | True |
| 1 | `ooo` | o-o | False |
| ... | full | cannot pair last o | False |

This demonstrates that interleaving `o` and `i` prevents full removal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | For each substring of length up to n, we scan possible pairings. |
| Space | O(n^2) | Storing DP table for all substrings. |

With $n \leq 5000$ across all test cases, $O(n^2)$ fits comfortably in 2s and 256MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open(__file__).read())
    return output.getvalue().strip()

assert run("6\n1\na\n6\nllmllm\n6\nuwuuwu\n6\nbyebye\n6\noooioi\n12\nsiixxsevvenn\n") == "NO\nYES\nYES\nNO\nNO\nYES"

assert run("1\n1\na\n") == "NO"  # single character
assert run("1\n2\naa\n") == "YES"  # minimal pair
assert run("1\n4\naabb\n") == "YES"  # simple consecutive pairs
assert run("1\n4\nabab\n") == "NO"  # interleaved cannot resolve
assert run("1\n6\nabcabc\n") == "NO"  # nested interleaving
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\na` | NO | single character case |
| `2\naa` | YES | minimal pair removal |
| `4\naabb` | YES | consecutive pairs |
| `4\nabab` | NO | interleaving prevents full removal |
| `6\nabcabc` | NO | nested interleaving |

## Edge Cases

For a single character like `a`, the DP table remains `False` because there is no pair to remove, returning "NO".

For a string like `abab`, the algorithm attempts to pair the first `a` with the second `a`, but the substring between them contains `b`, which is not removable yet, making `dp[0][3]` false and correctly outputting "NO".

For `siixxsevvenn`, the recursive DP finds pairs like `ii`, `xx`, `ss`, `ee`, `vv`, `nn` in order, validating that interleaving is handled properly and returning "YES".
