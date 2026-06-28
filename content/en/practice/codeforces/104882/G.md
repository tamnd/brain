---
title: "CF 104882G - Grandma's Cubes"
description: "We are given a sequence of dice outcomes, one per throw. At each position Masha is allowed to announce any number from 1 to 6, independent of the real roll, and her score is the sum of all announced numbers. The twist is a “surveillance rule” tied to the value 6."
date: "2026-06-28T09:18:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104882
codeforces_index: "G"
codeforces_contest_name: "Voronezh State University - Sitronics contest II"
rating: 0
weight: 104882
solve_time_s: 34
verified: false
draft: false
---

[CF 104882G - Grandma's Cubes](https://codeforces.com/problemset/problem/104882/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of dice outcomes, one per throw. At each position Masha is allowed to announce any number from 1 to 6, independent of the real roll, and her score is the sum of all announced numbers.

The twist is a “surveillance rule” tied to the value 6. If the grandmother hears three consecutive announced sixes, she immediately inspects only the most recent throw. If that inspected value does not match the real dice outcome, Masha is caught. After this inspection, the streak of consecutive sixes is reset.

So the only danger comes from producing a run of three announced sixes. Everything else is unconstrained except that at the moment the third consecutive six happens, that position must be truthful, meaning it must equal the actual roll.

The task is to choose an announced sequence maximizing total sum while never triggering a caught state.

The input is the actual dice sequence. The output is the maximum possible sum of the announced sequence under the rule above.

With n up to 100000, any quadratic strategy over prefixes or states is impossible. A linear or near-linear dynamic program is required, since 10^5 transitions is the natural target under a one second limit.

A naive approach would try to simulate all possible announced sequences. Even if we restrict values to 6 for maximum gain, we still face a constraint that depends on the last two decisions. That already suggests a state-based dependency rather than independent greedy choices.

A subtle failure case appears when greedily outputting 6 everywhere.

For example, if the input is:

```
n = 3
a = [1, 1, 1]
```

A greedy strategy outputs 6, 6, 6, but this creates a triple-six situation at the third position, which forces truthfulness at position 3. Since a3 is 1, this would cause a mismatch and Masha is caught. So even though the greedy sum is high, it violates the rule.

Another edge case is when the actual sequence already contains many 6s:

```

```
