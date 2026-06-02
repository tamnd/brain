---
title: "CF 175C - Geometry Horse"
description: "We have several types of geometric figures. Type i contains ki identical figures, and every figure of that type has base value ci. When a figure is destroyed, the earned score equals: base value × current factor The factor changes over time. Initially it is 1."
date: "2026-06-02T16:56:05+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 175
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 115"
rating: 1600
weight: 175
solve_time_s: 61
verified: false
draft: false
---

[CF 175C - Geometry Horse](https://codeforces.com/problemset/problem/175/C)

**Rating:** 1600  
**Tags:** greedy, implementation, sortings, two pointers  
**Solve time:** 1m 1s  
**Verified:** no  

## Solution
## Problem Understanding

We have several types of geometric figures. Type `i` contains `k_i` identical figures, and every figure of that type has base value `c_i`.

When a figure is destroyed, the earned score equals:

`base value × current factor`

The factor changes over time. Initially it is `1`. After exactly `p1` figures have been destroyed, the factor becomes `2`. After exactly `p2` figures have been destroyed, it becomes `3`, and so on. After `pt` figures have been destroyed, the factor becomes `t + 1`.

All figures must eventually be destroyed, but we are free to choose their destruction order. The task is to maximize the total score.

The key observation is that the factor depends only on how many figures have already been destroyed, not on which figures they were. This means the game creates several consecutive "slots" with different multipliers. We must decide which figures occupy which slots.

The constraints are unusual. There are at most 100 figure types, but each type may contain up to `10^9` figures, and the factor change positions can be as large as `10^12`. Any algorithm that tries to represent individual figures is impossible. The total number of figures may exceed `10^11`, so we must work with counts in bulk.

Another important detail is that costs may be zero. Such figures should naturally be assigned to the worst multipliers whenever possible, because moving them to better multipliers wastes valuable slots.

A common mistake is to think about the process chronologically and greedily choose the next figure one by one. Consider:

```
2
1000000000 1
1 1000
1
1
```

The first destroyed figure uses factor `1`, all others use factor `2`.

The optimal strategy destroys the cheap figure first and saves the expensive figure for factor `2`.

Score:

```
1*1 + 1000*2 = 2001
```

Destroying the expensive figure first gives:

```
1000*1 + 1*2 = 1002
```

Another subtle case occurs when a factor boundary lies beyond the total number of figures.

```
1
5 10
2
100 200
```

Only five figures exist, so every figure is destroyed with factor `1`.

The answer is:

```
50
```

A careless implementation that blindly processes all intervals from `p` may incorrectly assume factors `2` and `3` are ever reached.

One more edge case is when multiple figure types have the same cost.

```
2
3 5
4 5
1
3
```

Since every figure has equal value, any ordering produces the same answer. The algorithm must still work correctly without relying on strict inequalities.

## Approaches

A brute-force view is helpful for understanding the structure.

Imagine expanding every figure into an individual item. We would know exactly how many slots belong to factor `1`, how many belong to factor `2`, and so on. Each slot has a multiplier attached to it.

For example:

```
Factors by destruction position:
1 1 1 2 2 3 3 3 ...
```

Every figure contributes:

```
cost × assigned multiplier
```

If we explicitly listed all figures and all slots, the problem would become an assignment problem. The optimal solution is straightforward: sort figures by cost and assign the largest costs to the largest multipliers.

This follows directly from the rearrangement inequality. Whenever a larger cost is paired with a smaller multiplier while a smaller cost is paired with a larger multiplier, swapping them increases or preserves the score.

The brute-force approach fails because the number of figures can be enormous. A single type may contain `10^9` figures, so expanding all figures is impossible.

The crucial observation is that there are only 100 figure types and at most 101 different multiplier levels. We never need to track individual figures.

Suppose we sort figure types by cost in ascending order. Then, in the optimal assignment, low-cost figures occupy the earliest slots with small multipliers, while high-cost figures occupy the latest slots with large multipliers.

Instead of assigning one figure at a time, we process multiplier intervals in increasing order and consume counts from the sorted figure types. Each interval contains some number of destruction positions having the same factor. We fill those positions using the currently cheapest remaining figures.

This simulates the optimal sorted assignment without ever expanding counts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(F log F) | O(F) | Too slow |
| Optimal | O(n log n + n + t) | O(n) | Accepted |

Here `F = Σ k_i`, which may exceed `10^11`.

## Algorithm Walkthrough

### 1. Sort all figure types by cost in ascending order

Each type is represented by `(cost, count)`.

The optimal arrangement places cheap figures into low-factor slots and expensive figures into high-factor slots.

### 2. Convert factor changes into interval lengths

Let:

```
prev = 0
```

For each boundary `p_i`, create an interval:

```
length = p_i - prev
factor = i
```

Then update:

```
prev = p_i
```

These intervals describe how many destruction positions use each factor.

### 3. Process intervals from smallest factor to largest factor

Maintain a pointer to the current cheapest figure type that still has remaining figures.

For an interval of length `L` and factor `f`, repeatedly take figures from the current type until either:

```
L = 0
```

or that type is exhausted.

If we take `x` figures of cost `c`, we add:

```
x * c * f
```

to the answer.

Then decrease both the interval length and the remaining count of that figure type.

### 4. Handle all remaining figures

After processing every boundary interval, any remaining figures are destroyed with factor:

```
t + 1
```

Consume all remaining counts and add:

```
count * cost * (t + 1)
```

to the answer.

### Why it works

Consider any two figures with costs `a ≤ b` and two multiplier slots `x ≤ y`.

If the
