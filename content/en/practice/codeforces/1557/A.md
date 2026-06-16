---
title: "CF 1557A - Ezzat and Two Subsequences"
description: "We are given an array of integers, and we must split it into two non-empty groups while preserving every element exactly once. Each group has a score equal to its arithmetic mean, and the goal is to maximize the sum of these two means."
date: "2026-06-16T16:11:44+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1557
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 737 (Div. 2)"
rating: 800
weight: 1557
solve_time_s: 196
verified: true
draft: false
---

[CF 1557A - Ezzat and Two Subsequences](https://codeforces.com/problemset/problem/1557/A)

**Rating:** 800  
**Tags:** brute force, math, sortings  
**Solve time:** 3m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, and we must split it into two non-empty groups while preserving every element exactly once. Each group has a score equal to its arithmetic mean, and the goal is to maximize the sum of these two means.

So if we choose a split into two subsequences $a$ and $b$, the objective is

$$\frac{\sum a}{|a|} + \frac{\sum b}{|b|}.$$

The difficulty is that both the sums and the sizes depend on how we partition the elements, so a naive intuition like “put large numbers together” is not obviously justified.

The constraints are strong: up to $10^5$ elements per test case and up to $3 \cdot 10^5$ total. This immediately rules out anything that considers all partitions, since splitting into two subsets already has $2^n$ possibilities. Even quadratic reasoning per test case is too slow in the worst case.

A subtle point is that the function is not linear in the partition sizes. Moving one element changes both a numerator and a denominator, so greedy reasoning is not obviously safe unless we reduce the structure.

Edge cases that can mislead naive solutions include arrays with all negative values, and arrays where the best split is not “largest half vs smallest half” but something more unbalanced.

For example, if all numbers are negative like $[-7, -6, -6]$, putting the most negative element alone improves the average structure in a non-intuitive way because averaging penalizes group size differently for negative values.

## Approaches

A brute-force approach would try every way to assign each element to one of the two subsequences. For each partition, compute both averages and track the maximum sum. This is correct because it directly evaluates the objective function, but it requires examining $2^n$ assignments per test case, which is impossible even for $n = 30$.

To find structure, rewrite the expression. Suppose we split into sets $a$ and $b$. Let total sum be $S$, and let subset $a$ have sum $S_a$ and size $k$. Then $b$ has sum $S - S_a$ and size $n - k$. The objective becomes

$$\frac{S_a}{k} + \frac{S - S_a}{n-k}.$$

Now the key observation is that for a fixed $k$, the best subset $a$ is simply the set of the $k$ largest elements. This comes from a standard exchange argument: swapping a smaller element in $a$ with a larger element in $b$ always increases or preserves the value.

This reduces the problem to sorting the array. Once sorted, we try every split point $k$ from $1$ to $n-1$, computing prefix sums so that each candidate split is evaluated in constant time.

Thus the problem collapses to a one-dimensional optimization over sorted prefixes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Sort the array in non-decreasing order. This ensures that any prefix corresponds to a set of the smallest elements, and any suffix corresponds to the largest elements.
2. Build prefix sums so that sum of the first $i$ elements can be queried in $O(1)$. This allows fast evaluation of any split.
3. For each split position $k$ from $1$ to $n-1$, treat the first $k$ elements as group $a$ and the remaining as group $b$.
4. Compute the value

$$\frac{\text{sum}(0..k-1)}{k} + \frac{\text{total} - \text{sum}(0..k-1)}{n-k}.$$

This gives the best possible value for that fixed split size because sorted order guarantees optimal grouping.
5. Track the maximum over all valid $k$.
6. Output the result for each test case.

The reason each split only needs to be checked once is that within a fixed split size, any deviation from sorted prefix structure can be improved by swapping elements across the boundary.

### Why it works

Fix a split size $k$. Suppose we have any subset $a$ of size $k$. If $a$ contains an element $x$ and outside $a$ there is a larger element $y$, swapping $x$ out and $y$ in strictly increases the sum of $a$, and correspondingly adjusts the other group in a way that preserves the total sum. The change in the objective simplifies to a linear comparison that always favors concentrating larger values into the same group when the size is fixed. Repeating swaps leads to the subset of the $k$ largest elements, proving optimality for each $k$. Since we evaluate all $k$, global optimality follows.

## Python Solution

```
PythonRun
```

The code starts by sorting the array so that candidate groups become contiguous prefixes and suffixes. The prefix array allows constant-time sum queries for any split. Each split point is evaluated by computing the two averages directly.

A subtle implementation detail is using floating-point division for averages. Since the required precision is $10^{-6}$, standard double precision is sufficient. Another important detail is initializing `best` to a very negative number to handle cases where all values are negative.

## Worked Examples

### Example 1

Input: `[3, 1, 2]`

Sorted array: `[1, 2, 3]`

| k | sum_a | avg_a | sum_b | avg_b | total |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1.0 | 5 | 2.5 | 3 |
| 2 | 3 | 1.5 | 3 | 3.0 | 3 |

Maximum occurs at $k = 2$, giving $1.5 + 3 = 4.5$.

This trace shows why imbalance can help: the larger element prefers to form a singleton group to avoid lowering the average of a larger group.

### Example 2

Input: `[-7, -6, -6]`

Sorted array: `[-7, -6, -6]`

| k | sum_a | avg_a | sum_b | avg_b | total |
| --- | --- | --- | --- | --- | --- |
| 1 | -7 | -7.0 | -12 | -6.0 | -19 |
| 2 | -13 | -6.5 | -6 | -6.0 | -19 |

Best split is $k = 2$, giving $-6.5 + -6 = -12.5$.

This shows that even with negative values, the optimal strategy is still governed by ordering, not sign-based heuristics.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates; prefix scan is linear |
| Space | $O(n)$ | Prefix sums stored alongside input |

The total input size across test cases is bounded by $3 \cdot 10^5$, so sorting per test case comfortably fits within the time limit. The solution performs only linear extra work beyond sorting.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample set | given | correctness on mixed cases |
| all equal | 4.0 | symmetry and neutrality |
| 2 elements | variable | minimal valid split |
| mixed extremes | variable | handling wide ranges |

## Edge Cases

When all elements are identical, every split yields the same value because both averages equal the same constant. The algorithm still sorts and evaluates all splits, and every computed value matches the expected constant sum of two identical averages.

When the array size is exactly two, there is only one valid partition. The loop evaluates only $k = 1$, so the algorithm directly returns $a_1 + a_2$, which matches the definition of two singleton averages.

When values span large negative and positive ranges, sorting ensures that extremes are isolated into different groups as needed. The prefix-suffix evaluation automatically tests splits where large positives are grouped together and large negatives are separated, so no special casing is required.
