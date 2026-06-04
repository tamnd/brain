---
title: "CF 217C - Formurosa"
description: "The formula describes a Boolean function built from constants 0 and 1, placeholders ?, and the operators AND, OR, and XOR. Each ? corresponds to a leaf of the plant. During an experiment, we choose which colony is placed on each leaf."
date: "2026-06-05T00:59:41+07:00"
tags: ["codeforces", "competitive-programming", "divide-and-conquer", "dp", "expression-parsing"]
categories: ["algorithms"]
codeforces_contest: 217
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 134 (Div. 1)"
rating: 2600
weight: 217
solve_time_s: 149
verified: false
draft: false
---

[CF 217C - Formurosa](https://codeforces.com/problemset/problem/217/C)

**Rating:** 2600  
**Tags:** divide and conquer, dp, expression parsing  
**Solve time:** 2m 29s  
**Verified:** no  

## Solution
## Problem Understanding

The formula describes a Boolean function built from constants `0` and `1`, placeholders `?`, and the operators AND, OR, and XOR.

Each `?` corresponds to a leaf of the plant. During an experiment, we choose which colony is placed on each leaf. If colony `i` has species value `x_i ∈ {0,1}`, then the formula is evaluated on those values and returns either `0` or `1`.

The scientists may perform as many experiments as they want. The only promise about the unknown colony types is that not all colonies have the same species.

The question is whether the given formula is powerful enough to determine the exact species of every colony for every valid assignment of species.

The input size immediately rules out any approach that constructs truth tables. The formula length can reach one million characters, so even an `O(length × log length)` solution is unnecessarily expensive. We need a linear scan of the expression and only a constant amount of work per symbol.

The subtle part of the problem is that the formula may contain many different `?` leaves, but the scientists are allowed to place the same colony on every leaf. That observation turns out to completely characterize when recovery is possible.

Consider the formula `(?^?)`.

If we put the same colony on both leaves, the result is always `0`. The experiment gives no information about that colony's species. In fact, the two assignments

```
colony A = 0, colony B = 1
```

and

```
colony A = 1, colony B = 0
```

produce exactly the same information, so the species cannot be determined uniquely. The correct answer is `NO`.

Now consider

```
(?|0)
```

Putting colony `i` on every leaf evaluates to exactly the value of that colony. One experiment per colony reveals all species immediately, so the correct answer is `YES`.

Another easy mistake is to analyze the full multi-variable function. The actual question is not whether the formula distinguishes different leaf assignments. The scientists control the leaf assignment pattern themselves. The key experiment is placing the same colony everywhere, which reduces the entire formula to a function of a single variable.

## Approaches

A brute-force viewpoint is to treat the formula as a Boolean function of all its leaves. One could try to characterize every possible experiment and determine whether the resulting family of functions uniquely identifies all colony assignments.

That rapidly becomes impossible. The formula may contain hundreds of thousands of leaves, so even storing the truth table is hopeless. The number of possible leaf assignments is exponential.

The crucial observation is that the scientists may place the same colony on every leaf.

Suppose every `?` in the formula receives the same value `x`. The whole expression collapses into a single-variable Boolean function

```
g(x)
```

Because a Boolean function of one variable has only four possibilities, the reduced formula must be one of

```
0
1
x
!x
```

If `g(x) = x` or `g(x) = !x`, then a single experiment with colony `i` placed on every leaf reveals the species of colony `i`. Repeating this for all colonies recovers the entire assignment.

If `g(x)` is constant, then using the same colony everywhere always gives the same answer regardless of species. The formula never provides an absolute reference that distinguishes sp
