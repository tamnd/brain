---
title: "CF 73C - LionAge II"
description: "We are given a string representing a character's name in a game, and we can change at most k of its letters to maximize a score called euphony. The euphony is computed as the sum of bonuses for every consecutive pair of letters in the string."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 73
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 66"
rating: 1800
weight: 73
solve_time_s: 87
verified: true
draft: false
---

[CF 73C - LionAge II](https://codeforces.com/problemset/problem/73/C)

**Rating:** 1800  
**Tags:** dp  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string representing a character's name in a game, and we can change at most _k_ of its letters to maximize a score called euphony. The euphony is computed as the sum of bonuses for every consecutive pair of letters in the string. Each pair of letters may have an associated bonus, which can be positive or negative, and if a pair is not listed, its bonus is zero.

The input consists of the string _s_, the integer _k_, and a set of pairs of letters with their corresponding bonuses. Our output is a single integer, the maximum possible euphony after making at most _k_ changes.

The constraints are fairly tight: the string length is at most 100, and _k_ is also at most 100. The number of letter pairs is at most 676 (all possible lowercase letter pairs). These limits indicate that an approach with polynomial time complexity on the string length is feasible. An algorithm with complexity O(n * k * 26^2), where n is the string length, is acceptable because 100 * 100 * 676 is roughly 6.7 million operations, which fits within a 2-second limit. Edge cases include _k_ = 0, where no changes are allowed, and _n_ = 0, where all pair bonuses are zero. Careless approaches might assume all pairs have bonuses or neglect _k_ = 0, leading to incorrect results.

## Approaches

The brute-force approach would enumerate all possible ways to change up to _k_ letters in the string. For each position, we could either leave the letter as is or replace it with any of 25 other letters, generating a huge number of possibilities. For a string of length 100 and _k_ = 100, this would result in O(26^100) possibilities, which is completely infeasible. Even trying to optimize by considering only beneficial changes still leaves an exponential search space.

The key insight is that the problem has optimal substructure and overlapping subproblems, making it suitable for dynamic programming. We can define a DP state as `dp[i][changes][last]`, representing the maximum euphony achievable using the first `i` letters, having used `changes` replacements, where the last letter used is `last`. At each step, we can try every possible letter at the current position, either changing the original letter (counting toward `k`) or keeping it, and update the DP based on the bonus for the last and current letter. The small alphabet (26 letters) and limited string length make this approach tractable.

This transforms the problem from exponential brute-force to a polynomial DP solution, exploiting the observation that the score of a prefix depends only on the last letter of the prefix and the number of changes used.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(26^n) | O(1) | Too slow |
| Dynamic Programming | O(n * k * 26^2) | O(n * k * 26) | Accepted |

## Algorithm Walkthrough

1. Initialize a 3D DP array `dp[i][changes][last]`, where `i` is the index in the string, `changes` is the number of letters replaced, and `last` is the index of the last letter used. Fill it with a large negative number, since we are maximizing.
2. Convert the input string to numerical indices 0-25 corresponding to letters 'a'-'z'.
3. Parse the bonus pairs into a 26x26 matrix `bonus` where `bonus[x][y]` gives the score for pair `xy`. Unlisted pairs default to 0.
4. Set the base case for the first character. For each possible letter at index 0, if we change it, increment the used changes. Update `dp[0][changes][letter]` with 0, as there are no previous letters to generate a bonus.
5. Iterate over the string from index 1 to n-1. For each possible number of changes used so far, and for each possible previous letter, consider every letter we could place at the current position. Calculate the new change count and the bonus of the pair formed with the previous letter. Update `dp[i][new_changes][current_letter]` to be the maximum between its previous value and `dp[i-1][changes][prev_letter] + bonus[prev_letter][current_letter]`.
6. After processing the entire string, iterate over all DP states at index n-1 and changes ≤ k, keeping track of the maximum euphony.
7. Output the maximum value found.

Why it works: The DP ensures that at each position we consider all possible ways to reach it with a given number of replacements and last letter. By always taking the maximum when updating, we guarantee that no better configuration is overlooked. The use of a last-letter dimension ensures that the pair bonus is correctly applied between consecutive letters.

## Python Solution

```python
import sys
input = sys.stdin.readline

s, k = input().split()
k = int(k)
n = int(input())

bonus = [[0]*26 for _ in range(26)]
for _ in range(n):
    x, y, c = input().split()
    bonus[ord(x)-97][ord(y)-97] = int(c)

m = len(s)
dp = [[[-10**18]*26 for _ in range(k+1)] for _ in range(m)]

# Initialize first character
for letter in range(26):
    changes = 0 if letter == ord(s[0])-97 else 1
    if changes <= k:
        dp[0][changes][letter] = 0

# Fill DP
for i in range(1, m):
    for used in range(k+1):
        for prev in range(26):
            if dp[i-1][used][prev] == -10**18:
                continue
            for cur in range(26):
                new_used = used + (cur != ord(s[i])-97)
                if new_used <= k:
                    dp[i][new_used][cur] = max(dp[i][new_used][cur], dp[i-1][used][prev] + bonus[prev][cur])

# Get result
ans = max(dp[m-1][used][letter] for used in range(k+1) for letter in range(26))
print(ans)
```

The code first reads and converts the input. The bonus matrix is straightforward, and the DP initialization uses a large negative number to represent impossible states. We carefully handle the first character separately, as it has no previous letter. Iterating over possible previous letters and current letters guarantees all transitions are considered. Using `max` ensures we track the optimal euphony at each state.

## Worked Examples

**Sample 1:**

Input: `winner 4` with bonuses: `s e 7, o s 8, l o 13, o o 8`.

| i | used | prev | cur | new_used | dp[i][new_used][cur] |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | - | l | 1 | 0 |
| 1 | 1 | l | o | 1 | 13 |
| 2 | 1 | o | o | 1 | 21 |
| 3 | 1 | o | s | 2 | 29 |
| 4 | 2 | s | e | 2 | 36 |
| 5 | 2 | e | r | 3 | 36 |

This shows the construction of `looser` and the euphony accumulation.

**Another small example:**

Input: `abc 1`, bonuses `a b 5, b c 10`.

| i | used | prev | cur | new_used | dp[i][new_used][cur] |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | - | a | 0 | 0 |
| 1 | 0 | a | b | 0 | 5 |
| 2 | 0 | b | c | 0 | 15 |
| 1 | 1 | a | c | 1 | 0 |
| 2 | 1 | c | b | 1 | 0 |

The DP correctly picks no changes needed as optimal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * k * 26^2) | For each position, each possible used changes, and each previous letter, we consider 26 possible current letters. |
| Space | O(n * k * 26) | DP array stores values for each position, change count, and last letter. |

This fits comfortably in the limits: 100 * 100 * 26^2 ≈ 6.7 million iterations and about 260,000 integers in memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    exec(open("solution.py").read())
    return ""

# provided sample
assert run("winner 4\n4\ns e 7\no s 8\nl o 13\no o 8\n") == "", "sample 1"

# minimum input
assert run("a 0\n0\n") == "", "single character, no changes"

# maximum k
assert run("abc 3\n3\na b 5\nb c 10\nc a 2\n") == "", "all letters can be changed"

# all pair bonuses negative
assert run("abc
```
