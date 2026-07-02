---
title: "CF 103965J - \u0423\u0431\u043e\u0440\u043a\u0430 \u043b\u0438\u0441\u0442\u044c\u0435\u0432"
description: "We are given a sequence of leaf pile sizes, but these piles are positioned on a long line of positions numbered from 1 to c."
date: "2026-07-02T06:36:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103965
codeforces_index: "J"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2022-2023, \u041f\u0435\u0440\u0432\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 103965
solve_time_s: 28
verified: false
draft: false
---

[CF 103965J - \u0423\u0431\u043e\u0440\u043a\u0430 \u043b\u0438\u0441\u0442\u044c\u0435\u0432](https://codeforces.com/problemset/problem/103965/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of leaf pile sizes, but these piles are positioned on a long line of positions numbered from 1 to c. Only n of these positions actually contain non-zero piles, specifically positions 1 through n store values a1 through an, while all positions after n up to c are effectively empty.

We are allowed to choose any contiguous segment of positions of fixed length k, anywhere inside the range [1, c]. For each such segment, we compute the sum of values of all piles that fall inside it. Positions outside 1..n contribute nothing because they are empty.

The task is to find the segment of length k that minimizes this sum.

The key constraint is that c can be as large as 10^9, which makes it impossible to treat this as a normal sliding window over a full array. The number of actual non-zero elements is only n up to 10^5, so any correct solution must avoid iterating over the full coordinate range and instead reason about how windows interact with the small active region.

A naive idea would be to build an array of size c and slide a window of length k. This fails immediately because even iterating over c is impossible.

A second naive idea would be to consider only windows entirely within 1..n. This misses valid optimal answers when the window extends into the empty region beyond n, which can reduce the sum significantly.

One subtle case appears when k is large enough that a window can sit completely in the empty region. For example, if n = 5, c = 10, k = 4, then choosing [6, 9] yields sum 0, which is optimal, even though it does not touch any a values. Any approach that ignores the empty region will fail here.

Another tricky case appears when k is larger than n. Then every valid window that touches any non-empty element must include a suffix of the array, and reasoning purely in terms of fixed-length subarrays of a becomes incorrect.

## Approaches

The brute-force approach would explicitly construct an array b of size c where b[i] = a[i] for i ≤ n and b[i] = 0 otherwise, then evaluate every segment of length k. Each window sum would be computed in O(k), giving an overall complexity of O(c · k), which is far beyond any feasible limit since c can be 10^9.

The structure of the problem allows a much stronger simplification. The only non-zero contributions are confined to positions 1 through n, and ever
