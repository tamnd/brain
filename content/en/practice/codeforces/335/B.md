---
title: "CF 335B - Palindrome"
description: "We are given a lowercase string and asked to extract a palindromic subsequence from it. A subsequence keeps the original order of characters but may skip positions. The output requirement has a twist."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dp"]
categories: ["algorithms"]
codeforces_contest: 335
codeforces_index: "B"
codeforces_contest_name: "MemSQL start[c]up Round 2 - online version"
rating: 1900
weight: 335
solve_time_s: 144
verified: false
draft: false
---

[CF 335B - Palindrome](https://codeforces.com/problemset/problem/335/B)

**Rating:** 1900  
**Tags:** constructive algorithms, dp  
**Solve time:** 2m 24s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a lowercase string and asked to extract a palindromic subsequence from it. A subsequence keeps the original order of characters but may skip positions. The output requirement has a twist. If the string contains any palindromic subsequence of length at least 100, we only need to print one of length exactly 100. Otherwise, we must print the longest possible palindromic subsequence.

At first glance this looks like the classic longest palindromic subsequence problem. The standard dynamic programming solution computes the best answer for every substring. The trouble is the input size. The string length can reach 50000, so an O(n²) DP would need about 2.5 billion states. Even storing the table would require several gigabytes of memory, far beyond the limit.

The constraint changes the nature of the task. We do not actually need the exact longest palindromic subsequence when the answer is large. Once we can produce any palindrome of length 100, we are already done. That observation is the entire reason the problem is solvable.

There are several edge cases that break naive constructions.

Consider the string:

```
abcdefghijklmnopqrstuvwxyz
```

Every character appears once. The longest palindromic subsequence has length 1, because no pair of equal characters exists. A greedy strategy that always tries to match characters from both ends would fail to produce anything unless it explicitly handles the single-character case.

Consider:

```
abca
```

The correct answer is `"aca"` or `"aba"`. A careless two-pointer strategy might match the outer `'a'` characters and then stop immediately, producing `"aa"` and missing the possible center character.

Consider:

```
aaaaaaaaaa...
```

with more than 100 `'a'` characters. The optimal answer is much longer than 100, but the problem only asks for exactly 100 once such a palindrome exists. An implementation that continues building unnecessarily may waste time or memory.

Another subtle case is when multiple matching pairs exist but choosing the wrong pair blocks future matches. For example:

```
character
```

The longest palindromic subsequence is `"carac"`. A purely local greedy rule can easily get trapped into shorter answers. The accepted solution avoids this issue by exploiting the small alphabet size rather than making irreversible local decisions.

## Approaches

The brute-force direction is the classic longest palindromic subsequence DP. Define `dp[l][r]` as the best answer inside substring `s[l:r+1]`. If the endpoints match, we extend the answer from the inner substring. Otherwise we take the better of skipping the left or right character.

The recurrence is correct because every optimal palindromic subsequence either uses both endpoints or skips one of them. The problem is scale. With `n = 50000`, the DP table has roughly:

```
50000 × 50000 = 2.5 × 10^9
```

states.

Even if each state computation were constant time, this is far too slow for a 2 second limit. Memory usage is equally impossible.

The key observation comes from the alphabet size. We only have 26 lowercase letters. Suppose the longest palindromic subsequence length is at least 100. Then we do not care about the exact optimum anymore. We only need some palindrome of length 100.

That means we can stop searching as soon as we collect 50 matching pairs.

Now think about how to build a palindrome greedily. We maintain two pointers at the ends of the current interval. Somewhere inside this interval, at least one character must appear at least twice. Otherwise every character would be unique, and the interval length could never exceed 26.

So at every stage, we can choose some character that appears on both sides, take one occurrence from the left and one from the right, append that character to both halves of the answer, and shrink the interval.

This process is surprisingly powerful. Each step removes at least two characters, and because there are only 26 character types, finding a usable pair is cheap.
