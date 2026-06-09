---
title: "CF 1890F - Game of Stacks"
description: "Each stack belongs to a vertex. If we are currently at vertex u, we look at the top element of stack u. If the stack is empty, the process stops and returns u. Otherwise we pop the top element, jump to the vertex written on that element, and repeat."
date: "2026-06-09T01:10:35+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs", "implementation", "trees"]
categories: ["algorithms"]
codeforces_contest: 1890
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 906 (Div. 2)"
rating: 3000
weight: 1890
solve_time_s: 50
verified: false
draft: false
---

[CF 1890F - Game of Stacks](https://codeforces.com/problemset/problem/1890/F)

**Rating:** 3000  
**Tags:** dfs and similar, graphs, implementation, trees  
**Solve time:** 50s  
**Verified:** no  

## Solution
## Problem Understanding

Each stack belongs to a vertex. If we are currently at vertex `u`, we look at the top element of stack `u`.

If the stack is empty, the process stops and returns `u`.

Otherwise we pop the top element, jump to the vertex written on that element, and repeat.

The catch is that every call starts from the original stacks. A pop performed while evaluating `init(i)` does not affect `init(j)`.

A direct simulation from every starting vertex is hopeless. One execution may pop up to all stack elements, and the total number of elements is as large as `10^6`. Running that independently for all `n ≤ 10^5` starting vertices would require around `10^11` operations in the worst case.

The structure hidden in the process is that only the current top element of each stack matters. At any moment every non-empty stack defines exactly one outgoing edge, from the stack's index to its current top value. That gives a functional graph.

A particularly tricky situation is a directed cycle.

Consider:

```
1: [2]
2: [1]
```

Starting from either vertex, we do not loop forever. The first visit to vertex `1` consumes its top. The first visit to vertex `2` consumes its top. After that both stacks are empty, so the process eventually terminates.

A naive DFS on the functional graph would incorrectly treat the cycle as an infinite loop. The cycle must be reduced by popping one element from every stack on the cycle.

Another easy mistake is assuming that a vertex gets only one answer. A vertex's outgoing edge changes after its top element is removed. For example:

```
1: [2, 3]
2: []
3: []
```

The first top of stack `1` points to `3`, but after removing it the next top points to `2`. Any solution that permanently fixes one outgoing edge per vertex loses essential information.

The constraints strongly suggest an almost linear solution. The total number of stack elements is at most `10^6`, so spending `O(1)` or `O(log n)` work per element is fine. Anything cl
