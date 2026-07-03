---
title: "CF 103433C - New Year Presents"
description: "We are given a string made of digits 0, 2, 5, and 6, and we are allowed to change any character into any other allowed digit in a single operation. The goal is to transform the string so that it satisfies a specific “New Year condition” involving the substrings “2025” and “2026”."
date: "2026-07-03T07:55:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103433
codeforces_index: "C"
codeforces_contest_name: "2018-2019 Russia Team Open, High School Programming Contest (VKOSHP 18)"
rating: 0
weight: 103433
solve_time_s: 34
verified: false
draft: false
---

[CF 103433C - New Year Presents](https://codeforces.com/problemset/problem/103433/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string made of digits 0, 2, 5, and 6, and we are allowed to change any character into any other allowed digit in a single operation. The goal is to transform the string so that it satisfies a specific “New Year condition” involving the substrings “2025” and “2026”.

A string is considered valid if it meets at least one of the following conditions: it contains the substring “2026”, or it does not contain the substring “2025”. Since these two conditions overlap in a non-trivial way, the problem is essentially asking for the minimum number of character replacements needed so that either we successfully “force” a 2026 pattern somewhere, or we “break” all occurrences of 2025.

The input gives multiple test cases, each consisting of a single string. For each string, we must compute the minimum number of single-character edits needed to make it valid.

The constraints imply that each string is very small, with length at most 20, while the number of test cases can be large. This combination strongly suggests that any solution exponential in string length is acceptable, but anything that multiplies that by a large factor per test case would still be fine. We can freely consider all substrings and all alignments of patterns without worrying about performance blowups.

A few edge cases are not obvious at first glance.

One is when the string already contains “2026”. In that case the answer is zero even if there are many “2025” substrings elsewhere, since the first condition already holds. For example, in “20252026”, no operations are needed.

Another is when the string contains overlapping or multiple occurrences of “2025”. For example, in “20252025”, fixing one occurrence might still leave another intact, so we cannot greedily fix just one window; we must consider the global effect of edits.

A third case is when both patterns appear as close variants of each other. For instance, “2025” and “2026” differ in only one character, so a single change can flip between satisfying and breaking the condition. A naive approach that only looks locally at one substring at a time may miss that a single edit can simultaneously eliminate all “2025” occurrences while also creating a “2026”.

## Approaches

A brute-force approach would try all possible ways of modifying the string. Since each position has 4 choices and the length is at most 20, this leads to 4^20 possibilities in the worst case, which is far too large. Even if we reduce the branching, exploring all full assignments is unnecessary because the condition depends only on length-4 substrings.

The key observation is that the condition depends only on whether the final string contains a specific 4-character pattern or avoids another 4-character pattern. This reduces the structure significantly. Instead of thinking about arbitrary modifications of the whole string, we can consider where a potential “2026” could appear and how many edits are needed to enforce it, and separately compute how many edits are needed to eliminate all “2025” occurrences.

For the first case, we fix a starting position i and try to transform the substring s[i:i+4] into “2026”. The cost is simply the number of mismatched characters. We take the minimum over all valid starting positions.

For the second case, we want to ensure that no substring equals “2025”. Instead of tracking global constraints, we again slide a window of length 4. For each occurrence of a “2025” pattern, we must change at least one character in that window. A single change can break multiple overlapping occurrences, so we compute the minimal number of positions to modify such that every “2025” window is invalidated. Since n is at most 20, we can try all subsets of positions or use bitmask enumeration over positions to test coverage.

This dual view is what makes the problem tractable: we either pay to create one “2026” or we pay to destroy all “2025” occurrences, and we take the minimum of these two costs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all modifications | O(4^n · n) | O(n) | Too slow |
| Enumerate positions / windows | O(n · 2^n) | O(n) | Accepted |

## Algorithm Walkthrough

### 1. Try to force a “2026” substring

For every index i where i + 3 < n, compare s[i], s[i+1], s[i+2], s[i+3] with “2026”. Count mismatches. Keep the minimum mismatch count over all i.

This directly measures the cheapest way to create a valid substring that satisfies the first condition.

### 2. Collect all “2025” windows

Scan all substrings of length 4. For each i where s[i:i+4] == “2025”, record this window as a constraint that m
