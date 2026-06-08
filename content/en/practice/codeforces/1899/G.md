---
title: "CF 1899G - Unusual Entertainment"
description: "We have a rooted tree with root at vertex 1. A permutation p contains every vertex exactly once. Each query gives three values (l, r, x). We look at the vertices appearing in the permutation segment p[l..."
date: "2026-06-08T21:26:49+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "dsu", "shortest-paths", "sortings", "trees", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1899
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 909 (Div. 3)"
rating: 1900
weight: 1899
solve_time_s: 46
verified: false
draft: false
---

[CF 1899G - Unusual Entertainment](https://codeforces.com/problemset/problem/1899/G)

**Rating:** 1900  
**Tags:** data structures, dfs and similar, dsu, shortest paths, sortings, trees, two pointers  
**Solve time:** 46s  
**Verified:** no  

## Solution
## Problem Understanding

We have a rooted tree with root at vertex `1`. A permutation `p` contains every vertex exactly once.

Each query gives three values `(l, r, x)`. We look at the vertices appearing in the permutation segment `p[l...r]` and ask whether at least one of those vertices belongs to the subtree of `x`.

Since the tree is rooted, "descendant of `x`" is exactly the same as "vertex inside the subtree of `x`", including `x` itself.

Rephrased, every query asks:

> Among the vertices whose positions in the permutation lie between `l` and `r`, does there exist a vertex inside the subtree of `x`?

The total number of vertices across all test cases is at most `10^5`, and the total number of queries is also at most `10^5`. Any solution that scans an entire subtree or an entire permutation interval for every query would be far too slow. A quadratic approach could easily require around `10^10` operations in the worst case.

The challenge is that the query mixes two different structures.

The subtree condition lives in the tree.

The interval condition lives in the permutation positions.

The solution must efficiently combine both.

Consider a chain `1-2-3`.

```
p = [1,2,3]
query = (1,2,3)
```

The interval contains vertices `{1,2}`.

The subtree of `3` contains only `{3}`.

The answer is `NO`.

A careless implementation that checks whether `x` itself appears in the interval would incorrectly answer `YES` for many similar cases.

Consider:

```
1
3 1
1 2
1 3
2 1 3
1 1 1
```

The interval contains only vertex `2`.

The subtree of `1` contains every vertex.

The answer is `YES`.

Any approach that only checks direct children of `1` would fail because descendants are not restricted to depth one.

Another subtle case occurs when the matching vertex is exactly `x`.

```
1
1 1
1
1 1 1
```

The subtree of `1` contains `1` itself, so the answer is `YES`.

An implementation that treats descendants as strict descendants would produce the wrong result.

## Approaches

A direct approach is easy to describe. For a query `(l,r,x)`, inspect every vertex in `p[l...r]` and test whether it belongs to the subtree of `x`.

Using Euler tour timestamps, subtree membership can be checked in `O(1)`, but the interval length can be `O(n)`. A single query may require scanning nearly the entire permutation. With `10^5` queries, this becomes `O(nq)`, which is much too large.

The key observation is that a subtree becomes a contiguous interval in Euler tour order.

Suppose we run DFS and assign entry times `tin[v]`.

Every vertex in the subtree of `x` receives a timestamp inside:

```
[tin[x], tout[x]]
```

Now look at the permutation. For every position `i`, instead of storing vertex `p[i]`, store its Euler entry time:

```
a[i] = tin[p[i]]
```

A query asks whether some vertex of the subtree of `x` appears between positions `l` and `r`.

After the transformation, the query becomes:

> Does the array segment `a[l...r]` contain a value inside the interval `[tin[x], tout[x]]`?

This is now a purely geometric problem involving array positions and value ranges.

A very useful offline technique for such existence queries is to process the array positions from left to right while maintaining, for every Euler value, the latest position where it appeared.

For a query `(l,r,x)`, we want to know whether some Euler value belonging to the subtree interval of `x` appears in positions `[l,r]`.

We process queries grouped by their right endpoint `r`.

When position `r` is processed, all values up to that point have been inse
