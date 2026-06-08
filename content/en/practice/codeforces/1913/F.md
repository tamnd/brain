---
title: "CF 1913F - Palindromic Problem"
description: "We are given a string consisting of lowercase letters, and we are allowed to change at most one character to any other lowercase letter. The goal is to produce a string that maximizes the number of palindromic substrings."
date: "2026-06-08T20:09:18+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "hashing", "string-suffix-structures", "strings"]
categories: ["algorithms"]
codeforces_contest: 1913
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 160 (Rated for Div. 2)"
rating: 2800
weight: 1913
solve_time_s: 37
verified: false
draft: false
---

[CF 1913F - Palindromic Problem](https://codeforces.com/problemset/problem/1913/F)

**Rating:** 2800  
**Tags:** binary search, data structures, hashing, string suffix structures, strings  
**Solve time:** 37s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string consisting of lowercase letters, and we are allowed to change at most one character to any other lowercase letter. The goal is to produce a string that maximizes the number of palindromic substrings. A palindromic substring is any contiguous sequence of characters that reads the same forward and backward, and repeated palindromes are counted each time they appear. If multiple strings achieve the maximum number of palindromic substrings, we must choose the lexicographically smallest one.

The input size can be up to 300,000 characters. This rules out any naive approach that examines all possible substrings individually, because the number of substrings grows quadratically. Specifically, for a string of length $n$, there are $n(n+1)/2$ substrings, so a straightforward brute-force solution would require roughly $4.5 \cdot 10^{10}$ operations in the worst case, which is far beyond feasible in 5 seconds.

Non-obvious edge cases include strings that are already palindromes, strings with all identical letters, and strings where changing a single character can make multiple palindromic expansions possible. For example, the string `aabaa` becomes `aaaaa` if we change the third character `b` to `a`, increasing the number of palindromic substrings from 9 to 15. A careless approach that only counts single-letter palindromes o
