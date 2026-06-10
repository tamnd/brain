---
title: "CF 1418G - Three Occurrences"
description: "We are given an array of length $n$, and we want to count how many contiguous segments have the following property: every distinct value appearing inside that segment appears exactly three times. The condition is surprisingly restrictive."
date: "2026-06-11T06:51:45+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "divide-and-conquer", "hashing", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1418
codeforces_index: "G"
codeforces_contest_name: "Educational Codeforces Round 95 (Rated for Div. 2)"
rating: 2500
weight: 1418
solve_time_s: 28
verified: false
draft: false
---

[CF 1418G - Three Occurrences](https://codeforces.com/problemset/problem/1418/G)

**Rating:** 2500  
**Tags:** data structures, divide and conquer, hashing, two pointers  
**Solve time:** 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of length $n$, and we want to count how many contiguous segments have the following property: every distinct value appearing inside that segment appears exactly three times.

The condition is surprisingly restrictive. If a number appears once or twice inside the segment, the segment is invalid. If it appears four times, the segment is also invalid. A valid segment consists only of values whose frequencies are all equal to three.

The array length can reach $5 \cdot 10^5$. A quadratic algorithm would examine roughly $2.5 \times 10^{11}$ subarrays, which is completely infeasible under a five second time limit. Even $O(n\sqrt n)$ would be uncomfortable in Python. We need something very close to linear time.

Several edge cases are easy to mishandle.

Consider

```
3
1 1 1
```

The answer is

```
1
```

The whole array is valid because the only value appears exactly three times.

Now consider

```
4
1 1 1 1
```

The answer is

```
1
```

Only the first three positions and the last three positions form valid subarrays. The whole array is invalid because the frequency becomes four. Any approach that merely checks divisibility of the length by three will fail.

Another subtle example is

```

```

The answer is

```

```

The entire array works because both values occur three times. Small
