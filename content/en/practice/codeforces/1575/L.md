---
title: "CF 1575L - Longest Array Deconstruction"
description: "We start with an array. We may repeatedly delete arbitrary elements, and after each deletion the remaining elements close up together. For any resulting array, define its score as the number of positions where the value equals its current 1-based index."
date: "2026-06-10T11:00:04+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "divide-and-conquer", "dp", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1575
codeforces_index: "L"
codeforces_contest_name: "COMPFEST 13 - Finals Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 2100
weight: 1575
solve_time_s: 154
verified: false
draft: false
---

[CF 1575L - Longest Array Deconstruction](https://codeforces.com/problemset/problem/1575/L)

**Rating:** 2100  
**Tags:** data structures, divide and conquer, dp, sortings  
**Solve time:** 2m 34s  
**Verified:** no  

## Solution
## Problem Understanding

We start with an array. We may repeatedly delete arbitrary elements, and after each deletion the remaining elements close up together.

For any resulting array, define its score as the number of positions where the value equals its current 1-based index. We want to choose a subsequence of the original array, preserving relative order, so that in the resulting array as many positions as possible satisfy

$$b_i=i.$$

The task is to compute the maximum achievable score.

The key observation is that deleting elements only changes indices. The relative order of the kept elements never changes. Any final array is simply a subsequence of the original array.

The constraints are large. The array length can reach $2 \cdot 10^5$, which immediately rules out any solution that explicitly considers subsets, intervals, or dynamic programming over pairs of positions. Even $O(n^2)$ would require roughly $4 \cdot 10^{10}$ operations in the worst case, which is far beyond the time limit. We need something close to $O(n \log n)$.

Several situations are easy to misinterpret.

Consider:

```
3
1 1 1
```

The answer is 1. We can keep a single element and obtain `[1]`, whose first position matches. A careless solution might count all occurrences of value 1 and incorrectly return 3.

Consider:

```
4
4 4 4 4
```

The answer is 1. Keeping all elements gives only one match at position 4. We can also keep a single element, but then it sits at position 1 and no longer matches. The index after deletions matters.

Consider:

```
5
2 3 4 5 6
```

The answer is 5. No element initially matches its position, yet keeping the entire array yields positions

```
1 2 3 4 5
```

against values

```
2 3 4 5 6
```

which still do not match. However, if we think in terms of the final subsequence positions, every element can become a match because the first kept element becomes position 1, the second becomes position 2, and so on. A solution that only looks at original indices would miss this.

## Approaches

A brute-force view is straightforward. Every final array is a subsequence of the original one, so we could enumerate all subsequences, compute their scores, and ta
