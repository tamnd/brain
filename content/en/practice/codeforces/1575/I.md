---
title: "CF 1575I - Illusions of the Desert"
description: "The labyrinth is a tree. Every room has a value $ai$, called its illusion rate. Moving through an edge $(x,y)$ costs $$max( Queries either change the value of one room or ask for the minimum energy needed to travel between two rooms."
date: "2026-06-10T10:56:33+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "trees"]
categories: ["algorithms"]
codeforces_contest: 1575
codeforces_index: "I"
codeforces_contest_name: "COMPFEST 13 - Finals Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 2300
weight: 1575
solve_time_s: 43
verified: false
draft: false
---

[CF 1575I - Illusions of the Desert](https://codeforces.com/problemset/problem/1575/I)

**Rating:** 2300  
**Tags:** data structures, trees  
**Solve time:** 43s  
**Verified:** no  

## Solution
## Problem Understanding

The labyrinth is a tree. Every room has a value $a_i$, called its illusion rate.

Moving through an edge $(x,y)$ costs

$$\max(|a_x+a_y|,\ |a_x-a_y|).$$

Queries either change the value of one room or ask for the minimum energy needed to travel between two rooms.

Because the graph is a tree, there is exactly one path between any two rooms. A type 2 query is simply asking for the total edge cost along that unique path.

The first challenge is understanding the edge cost formula. For any two numbers $p$ and $q$,

$$\max(|p+q|,\ |p-q|)=|p|+|q|.$$

One way to see this is to assume $|p|\ge |q|$. Then $p+q$ and $p-q$ have absolute values whose maximum is exactly $|p|+|q|$.

After this simplification, every edge $(x,y)$ has weight

$$|a_x|+|a_y|.$$

The values change during updates, so edge weights are dynamic.

The constraints are large: both $n$ and $q$ can reach $10^5$. A single query may involve a path containing $O(n)$ vertices. Recomputing an entire path for every query would lead to roughly $10^{10}$ operations in the worst case, far beyond what fits in a 3-second limit. We need something close to logarithmic time per query.

A few easy-to-miss cases deserve attention.

Consider a query from a node to itself:

```
1
|
(only one node)

2 1 1
```

No edges are traversed, so the answer is 0. Any formula that blindly sums path weights must handle this correctly.
