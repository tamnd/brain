---
title: "CF 1493C - K-beautiful Strings"
description: "We are asked to transform a given string into a \"beautiful\" string. A beautiful string of length $n$ with respect to a number $k$ is one where the number of occurrences of each letter is divisible by $k$."
date: "2026-06-10T22:14:13+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "constructive-algorithms", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 1493
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 705 (Div. 2)"
rating: 2000
weight: 1493
solve_time_s: 72
verified: false
draft: false
---

[CF 1493C - K-beautiful Strings](https://codeforces.com/problemset/problem/1493/C)

**Rating:** 2000  
**Tags:** binary search, brute force, constructive algorithms, greedy, strings  
**Solve time:** 1m 12s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to transform a given string into a "beautiful" string. A beautiful string of length $n$ with respect to a number $k$ is one where the number of occurrences of each letter is divisible by $k$. The new string must also be lexicographically no smaller than the original string. The input provides multiple test cases, each consisting of a string and the integer $k$. The output should be the lexicographically smallest string satisfying these properties, or $-1$ if it is impossible.

The constraints imply that $n$ can reach $10^5$ in a single test case, and the total sum of $n$ over all test cases does not exceed $10^5$. With a 2-second limit, algorithms with time complexity up to roughly $O(n \log n)$ per test case are safe, whereas naive approaches that attempt to generate all candidate strings or enumerate possibilities are too slow.

Non-obvious edge cases include strings that are already beautiful, strings where a small increment in one character cannot satisfy divisibility constraints, and strings where it is impossible to adjust counts because the remainder after dividing by $k$ exceeds the remaining positions. For instance, for $s = "aaaa"$ and $k = 3$, it is impossible to find a beautiful string of length 4 because the total count must be a multiple of 3, but 4 is not divisible by 3. A naive greedy approach that only increments letters may incorrectly produce a string of incorrect length or non-divisible counts.

## Approaches

A brute-force approach is to iterate over all strings lexicographically greater than or equal to $s$ and check if each string is beautiful. This works in theory because we can count the letters and check divisibility by $k$. However, the number of strings to check grows exponentially with $n$, making this completely infeasible for $n = 10^5$.

The key observation is that we only need to find the first position where we can increment a character to make the remaining string adjustable to meet the divisibility constraints. For each prefix of $s$, we can attempt to increment the rightmost character in the prefix and then greedily fill the remaining positions with the smallest letters possible, ensuring the total letter counts become divisible by $k$. This turns the problem into a constructive greedy algorithm: start from the end, try to increase a character minimally, and then fill the rest optimally.

This reduces the problem to $O(n)$ per test case, since we iterate over the string and compute the adjustments needed for divisibility.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(26^n) | O(n) | Too sl |
