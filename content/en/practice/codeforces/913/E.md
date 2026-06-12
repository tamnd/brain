---
title: "CF 913E - Logical Expression"
description: "We are working with Boolean functions of exactly three variables, x, y, and z. A Boolean function on three variables has only eight possible input assignments. The input gives the value of the function on each of those eight assignments as a binary string of length eight."
date: "2026-06-13T01:08:12+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "dp", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 913
codeforces_index: "E"
codeforces_contest_name: "Hello 2018"
rating: 2400
weight: 913
solve_time_s: 205
verified: false
draft: false
---

[CF 913E - Logical Expression](https://codeforces.com/problemset/problem/913/E)

**Rating:** 2400  
**Tags:** bitmasks, dp, shortest paths  
**Solve time:** 3m 25s  
**Verified:** no  

## Solution
## Problem Understanding

We are working with Boolean functions of exactly three variables, `x`, `y`, and `z`.

A Boolean function on three variables has only eight possible input assignments. The input gives the value of the function on each of those eight assignments as a binary string of length eight. Our task is to reconstruct a logical expression using variables, negation, conjunction, disjunction, and parentheses.

The expression must evaluate to exactly the given truth table. Among all valid expressions, we want the one with the smallest number of characters. If several expressions have the same minimum length, we must output the lexicographically smallest one.

The most important observation is that there are only `2^8 = 256` different Boolean functions of three variables. Even though the number of syntactically valid expressions is infinite, the number of distinct semantics is tiny. This completely changes the problem. Instead of searching among expressions, we can search among the 256 truth tables.

The number of queries is as large as 10,000, but every query asks about one of only 256 possible functions. This strongly suggests a preprocessing solution. If we can compute the optimal expression for all 256 functions once, answering each query becomes a simple table lookup.

Several edge cases make a naive implementation fail.

Consider the function represented by:

```
11110000
```

The optimal answer is:

```
!x
```

A careless implementation might generate:

```
!(x)
```

Both are correct logically, but the second expression is longer and therefore invalid as an answer.

Another subtle case is operator precedence. Suppose we want the function:

```
x&(y|z)
```

The expression

```
x&y|z
```

represents a different function because `&` binds more strongly than `|`. Parentheses must be added exactly when required by the grammar and omitted otherwise.

Lexicographic tie breaking is another trap. Two expressions may have equal length and represent the same function. For example,
