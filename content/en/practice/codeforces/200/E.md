---
title: "CF 200E - Tractor College"
description: "We are asked to distribute a fixed scholarship budget among students based on their exam grades. Each student receives a mark of 3, 4, or 5, and students with the same mark must receive the same scholarship."
date: "2026-06-03T16:28:15+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math", "number-theory", "ternary-search"]
categories: ["algorithms"]
codeforces_contest: 200
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 126 (Div. 2)"
rating: 2400
weight: 200
solve_time_s: 71
verified: false
draft: false
---

[CF 200E - Tractor College](https://codeforces.com/problemset/problem/200/E)

**Rating:** 2400  
**Tags:** implementation, math, number theory, ternary search  
**Solve time:** 1m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to distribute a fixed scholarship budget among students based on their exam grades. Each student receives a mark of 3, 4, or 5, and students with the same mark must receive the same scholarship. Let _c3_, _c4_, _c5_ be the counts of students with grades 3, 4, and 5, and let _k3_, _k4_, _k5_ be the respective scholarships. The constraints are that the scholarships are integers, non-decreasing (_k3 ≤ k4 ≤ k5_), and the total amount spent equals the budget _s_. Additionally, the "optimal" distribution minimizes a specific function of the scholarships, which boils down to balancing the differences between them.

The input gives the number of students _n_ (3 ≤ n ≤ 300), the total budget _s_ (1 ≤ s ≤ 3·10^5), and the marks for each student. The output should provide any distribution of scholarships that satisfies the constraints, or -1 if no such distribution exists.

The problem is subtle because small integer rounding can prevent exact equality of the total budget. A naive approach that tries to assign proportional shares might silently violate the integer requirement. For example, if _c3 = 2_, _c4 = 1_, _c5 = 2_, and _s = 7_, simply dividing the budget proportionally could yield fractions like 2.8 rubles, which are invalid. Care must be taken to explore integer solutions.

## Approaches

A brute-force approach would iterate over all possible values of _k3_, _k4_, _k5_ that satisfy 0 ≤ k3 ≤ k4 ≤ k5 and check if the total budget matches. Since each scholarship could be up to _s_, this gives roughly O(s^3) possibilities. For s up to 3·10^5, this is far too large.

The key observation is that we can reduce the search space by noting that once we fix _k3_ and _k5_, _k4_ is determined by the total budget:

```
k4 = (s - c3*k3 - c5*k5) / c4
```

This must be an integer, satisfy k3 ≤ k4 ≤ k5, and meet the budget exactly. This reduces the problem to a double loop over possible k3 and k5, which is feasible because n ≤ 300 and s ≤ 3·10^5. The range for k3 and k5 can be further bounded by floor(s / c3) and floor(s / c5), respectively, keeping the loops tight.

Finally, for each candidate (k3, k5), we check if k4 computed this way is valid. The "optimal" function is minimized when the differences between the scholarships are as small as possible, so iterating k3 from 0 upwards and k5 from the smallest feasible value tends to produce a minimal spread.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(s³) | O(1) | Too slow |
| Double Loop (Optimal) | O((s/c3)*(s/c5)) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count the number of students with each grade: _c3_, _c4_, _c5_. These counts are guaranteed to be ≥1.
2. Iterate over all feasible integer values of _k3_ from 0 up to floor(s / c3). This ensures we do not overspend the budget.
3. Iterate over all feasible integer values of _k5_ from k3 up to floor(s / c5). The lower bound ensures non-decreasing order.
4. Compute _k4_ as `(s - c3_k3 - c5_k5
