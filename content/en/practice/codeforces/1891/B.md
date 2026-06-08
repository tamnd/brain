---
title: "CF 1891B - Deja Vu"
description: "We have an array of positive integers and a sequence of queries. A query with value x examines every array element. If an element is divisible by 2^x, we add 2^(x-1) to that element."
date: "2026-06-08T21:59:11+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1891
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 907 (Div. 2)"
rating: 1100
weight: 1891
solve_time_s: 41
verified: false
draft: false
---

[CF 1891B - Deja Vu](https://codeforces.com/problemset/problem/1891/B)

**Rating:** 1100  
**Tags:** brute force, math, sortings  
**Solve time:** 41s  
**Verified:** no  

## Solution
## Problem Understanding

We have an array of positive integers and a sequence of queries.

A query with value `x` examines every array element. If an element is divisible by `2^x`, we add `2^(x-1)` to that element.

The queries are processed in order, and each query sees the array after all previous modifications. After all queries finish, we must output the final array.

At first glance, this looks like a straightforward simulation problem. For each query, scan the whole array and update the elements that satisfy the divisibility condition. The difficulty comes from the constraints. Across all test cases, both the total number of array elements and the total number of queries can reach `2·10^5`. A solution that scans the entire array for every query would perform roughly `n·q` operations, which can be around `10^10` in the worst case. That is far beyond what fits into a 2-second time limit.

The key challenge is understanding how an update changes divisibility by powers of two.

A non-obvious edge case appears when the same query value occurs multiple times.

Consider:

```
a = [4]
queries = [2, 2]
```

The first query applies because `4` is divisible by `4`.

```
4 -> 6
```

Now `6` is no longer divisible by `4`, so the second query does nothing.

Final answer:

```
[6]
```

A careless implementation that treats every query independently from the original array might incorrectly add `2` twice and produce `8`.

Another subtle case is when a smaller query arrives after a larger one.

```
a = [8]
queries = [3, 1]
```

The first query adds `4`:

```
8 -> 12
```

The second query
