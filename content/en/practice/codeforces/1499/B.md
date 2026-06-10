---
title: "CF 1499B - Binary Removals"
description: "We are given a binary string and may delete some characters, with one restriction: no two deleted positions are allowed to be adjacent. After all deletions, the remaining characters keep their original order."
date: "2026-06-10T21:23:05+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1499
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 106 (Rated for Div. 2)"
rating: 1000
weight: 1499
solve_time_s: 55
verified: false
draft: false
---

[CF 1499B - Binary Removals](https://codeforces.com/problemset/problem/1499/B)

**Rating:** 1000  
**Tags:** brute force, dp, greedy, implementation  
**Solve time:** 55s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a binary string and may delete some characters, with one restriction: no two deleted positions are allowed to be adjacent. After all deletions, the remaining characters keep their original order. The goal is to determine whether the resulting string can become sorted, meaning that every `0` appears before every `1`.

A sorted binary string has the form

```
000...00111...11
```

possibly with one of the parts empty. The only forbidden pattern is a `1` appearing somewhere before a later `0`.

The length of each string is at most 100, and there are at most 1000 test cases. Even fairly inefficient algorithms would fit comfortably inside the limits, but the structure of the problem turns out to admit a very simple linear scan.

Several situations are easy to mishandle.

Consider

```
110
```

The answer is `YES`. Removing the last character gives `"11"`, which is sorted. A careless approach might think that the substring `"10"` always causes trouble.

Consider

```
1100
```

The answer is `NO`. There are adjacent ones followed by adjacent zeros. To fix the inversion between them we would need to remove neighboring positions, which is forbidden.

Another interesting case is

```
101010
```

The answer is `YES`. We may remove every other character and obtain `"000"` or `"111"`. Looking only at the number of inversions would not reveal this.

Strings already in sorted order, such as

```

```

should immediately produce `YES`, even though no deletions are required.

## Approaches

A brute-force solution would try every
