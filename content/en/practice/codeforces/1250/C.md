---
title: "CF 1250C - Trip to Saint Petersburg"
description: "We are choosing a continuous stay interval on a number line of days, and optionally selecting some projects whose full time ranges must lie inside that stay. Each project gives a fixed profit if taken, but staying itself costs a fixed amount per day."
date: "2026-06-15T22:08:21+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 1250
codeforces_index: "C"
codeforces_contest_name: "2019-2020 ICPC, NERC, Southern and Volga Russian Regional Contest (Online Mirror, ICPC Rules, Teams Preferred)"
rating: 2100
weight: 1250
solve_time_s: 178
verified: false
draft: false
---

[CF 1250C - Trip to Saint Petersburg](https://codeforces.com/problemset/problem/1250/C)

**Rating:** 2100  
**Tags:** data structures  
**Solve time:** 2m 58s  
**Verified:** no  

## Solution
## Problem Understanding

We are choosing a continuous stay interval on a number line of days, and optionally selecting some projects whose full time ranges must lie inside that stay. Each project gives a fixed profit if taken, but staying itself costs a fixed amount per day. The goal is to pick both the stay window and a subset of projects so that total profit from projects minus total accommodation cost is maximized, while staying for at least one day and covering every chosen project completely.

The key structure is that once we fix a set of projects, the best arrival and departure days are forced: we must arrive no later than the earliest selected project start and leave no earlier than the latest selected project end. This makes the cost depend only on the minimum left endpoint and maximum right endpoint among chosen projects.

The constraints push us toward a solution that avoids enumerating subsets or intervals explicitly. With up to 2⋅10^5 projects and large coordinate ranges, any quadratic or subset-based approach is impossible. Even iterating over all pairs of projects as candidate boundaries is too slow because that already leads to O(n^2). The solution must rely on sorting plus a data structure that aggregates contributions efficiently.

A few edge cases are easy to get wrong:

A naive greedy approach that picks all profitable projects individually fails because including one project can expand the interval and increase cost enough to destroy global optimality. For example, if one high-profit project lies far away, it can force a very large interval and dominate cost.

Another subtle case is when the best answer involves choosing only one project. If we incorrectly assume we must merge overlapping intervals or expand greedily, we may end up including unnecessary projects and losing profit.

Finally, the requirement that
