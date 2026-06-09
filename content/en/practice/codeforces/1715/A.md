---
title: "CF 1715A - Crossmarket"
description: "The store is an n × m grid. Stanley starts in the upper-left corner and wants to reach the lower-right corner. Megan starts in the lower-left corner and wants to reach the upper-right corner. Moving to a neighboring cell costs one unit of energy."
date: "2026-06-09T19:54:10+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1715
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 816 (Div. 2)"
rating: 800
weight: 1715
solve_time_s: 58
verified: false
draft: false
---

[CF 1715A - Crossmarket](https://codeforces.com/problemset/problem/1715/A)

**Rating:** 800  
**Tags:** constructive algorithms, greedy, math  
**Solve time:** 58s  
**Verified:** no  

## Solution
## Problem Understanding

The store is an `n × m` grid. Stanley starts in the upper-left corner and wants to reach the lower-right corner. Megan starts in the lower-left corner and wants to reach the upper-right corner.

Moving to a neighboring cell costs one unit of energy. Megan leaves a portal in every cell she visits. From any cell containing a portal, either person may spend one unit of energy to jump to any other portal cell. The two people are free to move in any order, since time itself has no cost. We must find the minimum total energy consumed by both of them together.

Each test case contains only the dimensions of the grid. The answer is a single number representing the minimum combined energy.

The dimensions can be as large as `10^5`, and there may be up to `1000` test cases. A solution that explores the grid or runs graph algorithms would be far too expensive. Even a single breadth-first search on a `100000 × 100000` grid would involve around `10^10` cells, which is completely infeasible. Since the input size is tiny, the answer must come from a direct mathematical observation and run in constant time per test case.

Several edge cases are easy to mishandle.

When the grid contains only one cell,

```
1 1
```

both people already stand at their destinations, so the answer is

```
0
```

A formula that blindly subtracts one would produce a negative value.

Single-row grids require special care. For example,

```
1 5
```

The two people simply walk along the row. Portals provide no advantage because there is only one path. The answer is

```
5
```

Using the general formula without considering this case gives

```
4
```

which is incorrect.

The same issue appears for single-column grids.

```
5 1
```

The answer is again

```
5
```

because each person must traverse the column.

## Approaches

The most direct interpretation is to view the grid as a graph and search for an optimal schedule of movements and teleports. Since portals appear dynamically and both people can move in arbitrary order, the state space becomes enormous. A state would need to describe the positions of both people and which cells already contain portals. Even for moderate grid sizes, the number of possibilities explodes.

The brute-force approach is correct because it explicitly considers every possible sequence of actions, but its complexity grows exponentially. With grids containing up to `10^10` cells, such an approach is hopeless.

The key observation is that only the shape of the grid matters. Without portals, each person needs

```
(n - 1) + (m - 1)
```

steps, giving a total of

```
2(n + m - 2).
```

Portals allow one person to reuse part of the route already explored by Megan. Every time we change direction while traversing the rectangle, we effectively lose one unit compared with moving in a straight line. A rectangle requires two direction changes, so portals save exactly one unit relative to the naive total.

Thus, for grids having at least two rows and two columns, the answer becomes

```
2(n + m - 2) - max(n, m) + 1
```

which simplifies to

```
2(min(n, m) - 1) + max(n, m).
```

An even cleaner form is

```
2(n + m - 2) - (min(n, m) - 1).
```

After simplification,

```
answer = 2(n + m - 2) - (min(n, m) - 1)
       = n + m + max(n, m) - 2.
```

For a single row or single column, portals do not help and the answer is simply

```

```
