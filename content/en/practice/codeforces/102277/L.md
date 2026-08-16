---
title: "CF 102277L - Cupcake Bonuses"
description: "The company forms a rooted tree. Employee 1 is the CEO, and every later employee is hired under an existing employee, so the supervisor relation defines the tree."
date: "2026-08-16T19:50:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102277
codeforces_index: "L"
codeforces_contest_name: "UCF Locals 2018"
rating: 0
weight: 102277
solve_time_s: 330
verified: false
draft: false
---

[CF 102277L - Cupcake Bonuses](https://codeforces.com/problemset/problem/102277/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 30s  
**Verified:** no  

## Solution
## Problem Understanding

The company forms a rooted tree. Employee 1 is the CEO, and every later employee is hired under an existing employee, so the supervisor relation defines the tree. An employee belongs to the department headed by themselves, their supervisor, their supervisor's supervisor, and so on up to the CEO. Equivalently, the department headed by employee `u` consists exactly of the subtree rooted at `u`.

Each employee has a current bonus multiplier. Initially every employee starts with the same multiplier `S`. A type 3 query chooses an employee `u` and a base amount `B`, then every currently existing employee in `u`'s subtree receives `B * multiplier` money. A type 2 query changes one employee's multiplier, while a type 4 query asks for that employee's total money received so far. A type 1 query creates a new employee under a given supervisor. The official constraints allow up to `10^5` queries, with multipliers and bonus amounts up to `10^6`.

With `10^5` operations and a one-second limit, an algorithm that scans a large part of the company for every payout cannot work. A quadratic solution could perform around `2.5 * 10^9` employee visits in the worst case, far beyond what the limit allows. We need each query to affect or inspect the tree in roughly logarithmic time.

The tricky part is that the multiplier is not fixed. Suppose a department receives a bonus of 10 while an employee's multiplier is 2, and later the multiplier becomes 5. The old bonus must remain worth 20, not become 50 retroactively. A lazy structure that simply stores "10 bonus still waiting to be multiplied" would be wrong unless it also remembers when the employee joined.

A second edge case is a new employee joining after an earlier department payout. For example:

```
7 1
3 1 10
4 1
2 1 2
1 1
3 1 5
4 1
4 2
```

The output is:

```
10
20
5
```

Employee 2 is hired only after the first payout, so that payout contributes nothing to employee 2. A careless implementation using the final subtree of the CEO would accidentally give employee 2 the old bonus.

Another edge case is a multiplier change after bonuses have already been paid. Consider:

```
4 2
3 1 10
2 1 5
4 1
4 1
```

The correct output is:

```
50
50
```

The multiplier change does not alter the already-paid 20. It only changes the value of future payouts. An implementation that stores the total as `current_multiplier * all bonuses ever applied` would incorrectly produce 50 only if it had handled the old contribution separately, and would otherwise retroactively inflate the previous payment.

Zero values also matter. For example:

```
4 0
3 1 100
2 1 100
4 1
```

The answer is:

```
0
```

The first payout is zero because the multiplier was zero at that time. Changing the multiplier later cannot resurrect that payout.

## Approaches

The direct solution is to explicitly maintain every employee's accumulated bonus. For a type 3 query on employee `u`, traverse the entire subtree of `u` and add `B * multiplier[v]` to every employee `v`. This is correct because the query literally pays every current member of that department.

The problem is the cost. A department can contain almost every employee, so one payout can require `O(n)` work. With `10^5` queries, the worst case is quadratic. More precisely, if roughly half the queries create employees and the other half pay the CEO's department, arranging all hires first gives about `50,001 * 50,000 = 2,500,050,000` employee updates. That is not remotely suitable for a one-second limit.

The key observation is to stop thinking of a payout as immediately changing every employee's total. Instead, consider what a payout contributes to an employee's multiplier history.

For one employee `v`, every qualifying payout contributes its base amount multiplied by the multiplier that `v` had at that moment. Suppose we temporarily collect all qualifying base amounts in a variable `C`. If `v` currently has multiplier `M`, the unpaid contribution represented by `C` is `C * M`.

When `M` changes by `delta`, the value of all currently pending payouts changes by exactly `delta * C`. We can materialize that difference immediately. Future payouts will increase `C` and use the new multiplier. This separates the two changing quantities cleanly.

A department payout is a subtree update, so we flatten the tree with an Euler tour. Every subtree then becomes one contiguous interval. We only need a data structure supporting a range addition of `B` to this coefficient `C`, followed by a point query of `C`. A Fenwick tree supports exactly that combination by using the standard range-add, point-query technique.

There is one more complication: an employee may be hired after some payouts. Those old payouts must not count for the new employee. When an employee is created, we record the current coefficient at its Euler position as its birth baseline. Fro
