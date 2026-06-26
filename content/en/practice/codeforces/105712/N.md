---
title: "CF 105712N - String Split"
description: "We are given a starting string s and a target string t. The only allowed operation on s is to remove either all characters that currently occupy odd positions or all characters that currently occupy even positions."
date: "2026-06-26T08:53:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105712
codeforces_index: "N"
codeforces_contest_name: "Rutgers University Programming Contest Fall 2024"
rating: 0
weight: 105712
solve_time_s: 28
verified: false
draft: false
---

[CF 105712N - String Split](https://codeforces.com/problemset/problem/105712/N)

**Rating:** -  
**Tags:** -  
**Solve time:** 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a starting string `s` and a target string `t`. The only allowed operation on `s` is to remove either all characters that currently occupy odd positions or all characters that currently occupy even positions. The operation can be repeated any number of times, and the question is whether there exists some sequence of operations that changes `s` into exactly `t`.

The key difficulty is that positions are based on the current string after every deletion. A character that was originally at one position may move to a different position later, so simulating random deletion choices can quickly become misleading. The solution comes from understanding what forms a string can have after repeated splitting.

The total length of all input strings is at most `2 * 10^5`. This means the algorithm must be close to linear. A quadratic approach that compares every possible sequence of deletions or every possible subsequence would perform around `4 * 10^10` operations in the worst case, which is far beyond what a typical one-second limit allows.

The important edge cases come from length changes and from the fact that a single deletion operation does not allow arbitrary subsequences. For example, if the input is:

```
abcdefg
cde
```

the answer is:

```
NO
```

A careless solution might think that any substring or subsequence can be produced, but after one operation the possible strings are only `aceg` or `bdf`. The characters `cde` never appear together.

Another edge case is when the target already equals the original string:

```
baccba
baccba
```

The correct output is:

```
YES
```

because zero operations are allowed. An implementation that always performs at least one deletion would incorrectly reject this case.

A final tricky case is when the target is longer than the source:

```
nick
james
```

The output is:

```
NO
```

Every operation keeps only part of the string, so the length can never increase. Any solution that only checks character relationships but forgets this restriction can fail here.

## Approaches

A straightforward approach is to generate every string reachable from `s`. Since every operation chooses one of two halves of the current positions, a breadth-first search over states would eventually find whether `t` appears. This is correct because it explores exactly the possible transformations.

The problem is that the number of states grows too quickly. A string of length `n` can repeatedly split into smaller strings, and trying both choices at every level creates an exponential search tree. Even though many branches may merge, storing and comparing all generated strings is far too expensive for lengths near `2 * 10^5`.

The observation that removes the need for simulation is to look at the structure of all reachable strings. Each operation keeps either the characters with one parity of indices. If we look at the original indices, after one operation we keep either all indices with the same parity. After another operation, we again take every other character of that already filtered sequence. This means the remaining characters always correspond to positions that follow a regular pattern in the original string.

More precisely, every reachable string is obtained by choosing some starting position and repeatedly taking characters with a fixed step size that is a power of two. However, because each operation halves the current sequence, the only possibilities that survive until the target length are determined by repeatedly choosing one of the two parity groups.

The important consequence is that if the target length is `m`, then the only possible first operation is one that produces a string of length at least `m`, and after continuing the process, the target must appear as the final subsequence created by these parity choices. This can be checked much more directly by observing the binary nature of the splits.

A useful way to view the process is from the target backwards. If a string `x` can become `y` after one operation, then `y` must be either the characters of `x` at positions `0,2,4,...` or the characters at positions `1,3,5,...`. Reversing this relationship means that every valid transformation chain corresponds to repeatedly selecting one parity group until the remaining length becomes exactly the target length.

Since every split reduces the length roughly by half, the number of possible depths is small. The final algorithm only needs to follow the possible parity selections rather than explore all strings.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in ` | s | ` |
| Optimal | O(` | s | + |

## Algorithm Walkthrough

1. If the target string is longer than the original string, immediately answer `NO`. Every operation removes characters, so increasing the length is impossible.
2. Check whether the target can be obtained by repeatedly taking every second character from the current string. Instead of simulating all possible branches, recursively consider the two possible children of the current string: the characters from even indices and the characters from odd indices.
3. Stop the recursion when the current string length equals the target length. At that point, the only valid result is an exact string equality check.
4. Memoize the strings that have already been checked. The same intermediate string can be reached through different sequences of operations, and storing failed states prevents repeated work.
5. Output `YES` if any sequence of parity selections reaches the target, otherwise output `NO`.

The reason this works is that every legal operation has exactly two outcomes: keeping one parity of the current positions. The recursion examines both of those outcomes, so it cannot miss a valid sequence. Memoization only removes repeated checks of identical states and does not change the set of reachable strings being considered.
