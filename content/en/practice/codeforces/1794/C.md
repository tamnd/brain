---
title: "CF 1794C - Scoring Subsequences"
description: "We are given a non-decreasing array. For every prefix a[1...k], we must determine a special value called the cost. For any subsequence of length d, its score is the product of its elements divided by d!."
date: "2026-06-09T10:10:25+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "math", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1794
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 856 (Div. 2)"
rating: 1300
weight: 1794
solve_time_s: 53
verified: false
draft: false
---

[CF 1794C - Scoring Subsequences](https://codeforces.com/problemset/problem/1794/C)

**Rating:** 1300  
**Tags:** binary search, greedy, math, two pointers  
**Solve time:** 53s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a non-decreasing array. For every prefix `a[1...k]`, we must determine a special value called the cost.

For any subsequence of length `d`, its score is the product of its elements divided by `d!`. Among all subsequences of the prefix, we first find the maximum possible score. Several subsequences may achieve that maximum score. The cost is the largest length among those optimal subsequences.

The task is to output this cost for every prefix of the array.

The array is already sorted in non-decreasing order, and every value satisfies `1 ≤ a[i] ≤ n`.

The total number of elements across all test cases is at most `5 · 10^5`. With this input size, anything quadratic is far too expensive. An `O(n^2)` solution would require roughly `2.5 · 10^11` operations in the worst case. Even `O(n log^2 n)` would be unnecessarily heavy. We should aim for `O(n log n)` or better per test file.

The tricky part is that the definition involves products of subsequences, which initially suggests exponential search over all subsequences. The key observation is that the score definition has a very strong structure that collapses the problem into a simple counting condition.

One easy mistake is to think that maximizing the score requires examining products directly.

For example:

```
a = [1, 2, 3]
```

The optimal score is achieved both by `[3]` and `[2,3]`.

The score of `[3]` is `3`.

The score of `[2,3]` is `6/2 = 3`.

Since the cost asks for the maximum length among optimal subsequences, the answer is `2`, not `1`.

Another subtle case is when many values are equal.

```
a = [5,5,5,5]
```

The answers are:

```
1 2 3 4
```

A careless greedy that always takes only the largest element would output all ones, which is incorrect because adding another `5` multiplies the numerator by `5` while the denominator only gains a factor equal to the new length.

A third edge case occurs when many small values appear.

```
a = [1,1,1]
```

Answers:

```
1 1 1
```

Even though the prefix length grows, longer subsequences do not improve the maximum score because every added element contributes only `1`.

## Approaches

A brute-force approach would examine every subsequence of every prefix.

For a prefix of length `k`, there are `2^k` subsequences. Computing scores and finding the best one is completely infeasible even for `k = 50`, let alone `10^5`.

The reason brute force works conceptually is simple: it directly follows the definition. The problem is the enormous number of subsequences.

The key observation comes from comparing a subsequence of length `d-1` with the same subsequence after adding one more element `x`.

The score changes by a factor

$$\frac{x}{d}.$$

If `x > d`, the score strictly increases.

If `x = d`, the score stays the same.

If `x < d`, the score decreases.

This completely changes how we think about the problem.

Suppose we want a subsequence of length `d` to achieve the maximum possible score. Since the array is sorted, the best way to obtain length `d` is to take the largest possible elements. For such a subsequence to be extendable up to length `d` without decreasing the score, its elements must satisfy

$$b_i \ge i$$

after sorting inside the subsequence.

Because the original array is already sorted, we only need to find the largest suffix-like selection whose elements can serve as positions `1,2,...,d`.

For a prefix ending at position `i`, the answer becomes the largest length `len` such that among the last `len` elements,

$$a_{i-len+1} \ge 1,\quad a_{i-len+2} \ge 2,\quad \dots,\quad a_i \ge len.$$

Since the array is sorted, this condition reduces to

$$a_j \ge len-(i-j)$$

for every chosen position.

A particularly convenient form is

$$a_j \ge j-L+1,$$

where `L` is the starting position of the chosen segment.

As we process prefixes from left to right, the answer never decreases by more than necessary. This allows maintaining the current valid length and extending it greedily.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(1) extra | Accepted |

## Algorithm Walkthrough

Let `ans` denote the answer for the current prefix.

1. Process the array from left to right.
2. When a new element `a[i]` arrives, try to increase the current answer by one.
3. The candidate new length is `ans + 1`.
4. For this length to be feasible, the smallest element inside the chosen suffix of length `ans + 1` must be at least `1`, the next at least `2`, and so on.
5. Because the array is sorted, checking feasibility reduces to verifying whether the new element can occupy position `ans + 1`.
6. If `a[i] > ans`, increase `ans` by one.
7. Output the current value of `ans`.

The implementation can also be viewed as maintaining the longest suffix satisfying

$$a_{i-len+1} \ge 1,\; a_{i-len+2} \ge 2,\; \dots,\; a_i \ge len.$$

Whenever a new value arrives, only one additional position can become valid, so a single comparison is enough.

### Why it works

Let the optimal subsequence have sorted elements `b1 ≤ b2 ≤ ... ≤ bd`.

Adding the `i`-th selected e
