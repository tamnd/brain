---
title: "CF 2192E - Swap to Rearrange"
description: "Each position i contains a pair of values (ai, bi). For that position we have exactly two choices. If we do nothing, the value ai stays in array a and bi stays in array b. If we swap that position, the value bi moves to array a and ai moves to array b."
date: "2026-06-07T20:58:56+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dfs-and-similar", "graph-matchings", "graphs", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 2192
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1081 (Div. 2)"
rating: 2100
weight: 2192
solve_time_s: 152
verified: false
draft: false
---

[CF 2192E - Swap to Rearrange](https://codeforces.com/problemset/problem/2192/E)

**Rating:** 2100  
**Tags:** constructive algorithms, dfs and similar, graph matchings, graphs, greedy, strings  
**Solve time:** 2m 32s  
**Verified:** no  

## Solution
## Problem Understanding

Each position `i` contains a pair of values `(a_i, b_i)`. For that position we have exactly two choices.

If we do nothing, the value `a_i` stays in array `a` and `b_i` stays in array `b`.

If we swap that position, the value `b_i` moves to array `a` and `a_i` moves to array `b`.

After making these independent choices, we want the multiset of values in `a` to be exactly the same as the multiset of values in `b`.

The size of a single test can reach one million elements across all test cases. Any solution that compares positions against each other, performs matching between occurrences explicitly, or repeatedly updates frequency tables per operation is far too expensive. The target complexity is essentially linear in the total input size.

The first subtle observation is that every occurrence of a value belongs to exactly one position. For a fixed value `x`, suppose it appears `k` times across both arrays together. In the final configuration, the number of copies of `x` in `a` must equal the number of copies of `x` in `b`. Since together they still contain `k` copies, `k` must be even.

A small example already shows why this condition is necessary:

```
a = [1]
b = [2]
```

Value `1` appears once and value `2` appears once. No sequence of swaps can make the two arrays have identical multisets.

Another easy-to-miss case is a self-pair:

```
a = [5]
b = [5]
```

Swapping does nothing. The pair contributes one copy of `5` to each array regardless of our decision. A graph construction must treat such edges correctly.

A third trap is assuming that even frequencies are sufficient without constructing an actual set of swaps. For example:

```
a = [1,2,3]
b = [2,3,1]
```

Every value appears twice overall, so a solution exists. The challenge is producing a consistent choice for every position.

## Approaches

A brute-force approach would try all subsets of positions. Each position can be swapped or not swapped, so
