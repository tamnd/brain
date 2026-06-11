---
title: "CF 1154B - Make Them Equal"
description: "We are given an array of integers. We must choose a single non-negative value D and then, independently for each element, either add D, subtract D, or leave it unchanged. The goal is to make every element become the same value after these operations."
date: "2026-06-12T02:46:46+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1154
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 552 (Div. 3)"
rating: 1200
weight: 1154
solve_time_s: 43
verified: false
draft: false
---

[CF 1154B - Make Them Equal](https://codeforces.com/problemset/problem/1154/B)

**Rating:** 1200  
**Tags:** math  
**Solve time:** 43s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers. We must choose a single non-negative value `D` and then, independently for each element, either add `D`, subtract `D`, or leave it unchanged.

The goal is to make every element become the same value after these operations. Among all valid choices, we need the smallest possible `D`. If no such `D` exists, we print `-1`.

The key restriction is that the same `D` must be used for every element. We are free to choose different operations for different elements, but the magnitude of the change is fixed.

The constraints are tiny. The array contains at most 100 elements, and every value is at most 100. Even fairly brute-force approaches would fit comfortably within the time limit. The challenge is not efficiency but recognizing the mathematical structure that determines whether a solution exists.

Several edge cases are easy to mishandle.

Consider an array where all values are already equal:

```
3
5 5 5
```

The correct answer is:

```
0
```

No changes are needed, so the minimum valid `D` is zero. A solution that always computes differences between distinct values may incorrectly return something positive.

Now consider an array with exactly two distinct values:

```
2
2 8
```

The correct answer is:

```
3
```

We can move both numbers to 5 by adding and subtracting 3. A careless approach might return the full difference 6 instead of the required operation size 3.

Another important case is:

```
3
1 4 8
```

The correct answer is:

```
-1
```

There is no single `D` that allows all three numbers to reach one common value. Looking only at pairwise differences is not sufficient.

Finally, consider:

```

```

The answer is:

```

```

The middle value 4 already equals the target. The values 1 and 7 move by exactly 3. This illustrates that some elements may remain unchanged while others are modified.

## Approaches

A brute-force solution can try every possible value of `D` and check whether all numbers can be transformed into a common target.

Since array values are at most 100, any meaningful `D` must also be small. For each candidate `D`, we could generate all reachable values for every element and test whether a common value exists. This works because the search space is tiny.

The drawback is that it completely ignores the mathematical structure of the problem. Even though it would pass these constraints, it does not explain why a solution exists.

The crucial observation is that every element can end up only at one of three positions:

```
a[i] - D
a[i]
a[i] + D
```

Suppose the final common value is `x`.

Then every original number must be one of:

```
x - D
x
x + D
```

That means the entire array can contain at most three distinct values. If there are four or more distinct numbers, a solution is impossible immediately.

Let the distinct values be sorted.

If there is only one distinct value, the answer is obviously `0`.

If there are two distinct values, call them `a < b`.

When `b - a` is even, we can choose

```
D = (b - a) / 2
```

and move both
