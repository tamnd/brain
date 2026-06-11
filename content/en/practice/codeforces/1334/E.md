---
title: "CF 1334E - Divisor Paths"
description: "We are given a number $D$ and need to reason about all of its divisors. The problem defines a graph whose vertices are all divisors of $D$. An edge exists from a divisor $y$ to a larger divisor $x$ if $x$ is divisible by $y$ and the quotient $x / y$ is prime."
date: "2026-06-11T15:59:29+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "graphs", "greedy", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1334
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 85 (Rated for Div. 2)"
rating: 2200
weight: 1334
solve_time_s: 49
verified: false
draft: false
---

[CF 1334E - Divisor Paths](https://codeforces.com/problemset/problem/1334/E)

**Rating:** 2200  
**Tags:** combinatorics, graphs, greedy, math, number theory  
**Solve time:** 49s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a number $D$ and need to reason about all of its divisors. The problem defines a graph whose vertices are all divisors of $D$. An edge exists from a divisor $y$ to a larger divisor $x$ if $x$ is divisible by $y$ and the quotient $x / y$ is prime. The weight of such an edge is the number of divisors of $x$ that are not divisors of $y$. The task is, for multiple queries each asking for a pair of divisors $v$ and $u$, to count the number of shortest paths between them in this graph.

The constraints are significant: $D$ can be as large as $10^{15}$ and there are up to $3 \cdot 10^5$ queries. Enumerating all divisors of $D$ or constructing the full graph explicitly is infeasible for large numbe
