---
title: "CF 903E - Swapping Characters"
description: "We are given $k$ strings of the same length $n$. Each of them was produced from a single unknown original string by performing exactly one swap of two different positions. The swapped characters are allowed to be equal, so a string may remain unchanged after the operation."
date: "2026-06-12T22:56:31+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "hashing", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 903
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 34 (Rated for Div. 2)"
rating: 2200
weight: 903
solve_time_s: 139
verified: false
draft: false
---

[CF 903E - Swapping Characters](https://codeforces.com/problemset/problem/903/E)

**Rating:** 2200  
**Tags:** brute force, hashing, implementation, strings  
**Solve time:** 2m 19s  
**Verified:** no  

## Solution
## Problem Understanding

We are given $k$ strings of the same length $n$. Each of them was produced from a single unknown original string by performing exactly one swap of two different positions. The swapped characters are allowed to be equal, so a string may remain unchanged after the operation.

We must reconstruct any original string that could have generated every given string in this way. If no such string exists, we print `-1`.

The most interesting constraint is $k \cdot n \le 5000$. This means the total input size is small, but one dimension can still be large. For example, $k=1$ and $n=5000$ is legal. Any algorithm containing an $O(n^2)$ enumeration of all swaps becomes dangerous when $n$ is large.

A useful observation comes from comparing two strings that were both obtained from the same original string by one swap. A swap affects at most two positions, so two resulting strings can differ in at most four positions. If we ever find two input strings whose Hamming distance exceeds four, the answer is immediately impossible.

There are several easy-to-miss corner cases.

If a string already equals the candidate original string, we still need one valid swap. That is only possible when the string contains a repeated character, because we can swap two equal letters and leave the string unchanged.

For example:

```

```

The answer is `-1`. Any original string equal to `abc` has all distinct letters, so no exact swap can leave it unchanged.

Another subtle case is when two strings differ in four positions.

```

```

A naive check that only allows distance two would reject this pair, yet both can come from the same original string after one swap each.

## Approaches

A direct brute force idea is to guess the original string and verify it. Since the original differs from any given string by one swap, we could take the first string and try all $O(n^2)$ swaps inside it. For every candidate we would check all $k$ strings.

The verification itself costs $O(kn)$, giving $O(n^2kn)$ in total. This is far too large when $n=5000$.

The key insight is that we do not need to try every swap.

Take two different input strings $a$ and $b$. Let $p$ be their first differing position. Since both strings were created from the same original by one swap, at least one of those swaps must involve position $p$. Otherwise position $p$ would be unchanged in both strings and could not differ.

That means one of the following must be true:

1. The original can be obtained from $a$ by swapping position $p$ with some other position.
2. The original can be obtained from $b$ by swapping position $p$ with some other position.

Now only $O(n)$ possibilities remain in each case. We enumerate the second endpoint of the swap, build the candidate original string, and verify it against all input strings.

Because $k \cdot n \le 5000$, checking a candidate in $O(kn)$ time is cheap enough. We try only $O(n)$ candidates, leading to $O(nkn)$, which is at most about $25$ million character comparisons and comfortably fits the limit.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Enumerate all swaps in one string | $O(n^2kn)$ | $O(n)$ | Too slow |
| Fix one mismatch position and enumerate its partner | $O(nkn)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read all strings.
2. Verify that all strings are anagrams of the first string.

A swap never changes character frequencies. If some string has different frequencies, the answer is impossible.
3. Find a string different from the first one.

If every string is identical, handle this as a special case. We need a duplicate character somewhere. If none exists, print `-1`. Otherwise swap two equal characters and print the unchanged string.
4. Let $a$ be the first string and $b$ be a different string. Find the first position $p$ where they differ.
5. Generate candidates in two groups.

First, swap $a[p]$ with every position $j$.

Second, swap $b[p]$ with every position $j$.

Each generated string is a possible original.
6. For every candidate, check every input string.

Let the candidate be $t$ and the current input string be $s$.

Compute all positions where $s$ and $t$ differ.

If the number of differing positions is $1$, this string can never be obtained by one swap.

If it is greater than $2$, one swap is insufficient.

If it is exactly $2$, say the positions are $x$ and $y$. We require

$$s[x]=t[y], \quad s[y]=t[x].$$

If it is $0$, then $t$ must contain a repeated character. Otherwise there is no swap that leaves it unchanged.
7. The first candidate passing all checks is a valid answer.
8. If no candidate survives
