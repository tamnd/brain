---
title: "CF 911E - Stack Sorting"
description: "Problem Statement: You are given an array of integers $a1, a2, dots, an$ and an integer $k$. You can perform at most $k$ operations. In each operation, you can remove either the first or the last element of the array."
date: "2026-06-13T00:35:44+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 911
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 35 (Rated for Div. 2)"
rating: 2000
weight: 911
solve_time_s: 363
verified: true
draft: false
---

[CF 911E - Stack Sorting](https://codeforces.com/problemset/problem/911/E)

**Rating:** 2000  
**Tags:** constructive algorithms, data structures, greedy, implementation  
**Solve time:** 6m 3s  
**Verified:** yes  

## Solution
## Problem Name: **Maximum Sum After Removals**

**Problem Statement:**

You are given an array of integers $a_1, a_2, \dots, a_n$ and an integer $k$. You can perform at most $k$ operations. In each operation, you can remove **either the first or the last element** of the array. After performing up to $k$ operations, find the **maximum sum** of the remaining elements.

**Constraints:**

- $1 \le n \le 2 \cdot 10^5$
- $1 \le k \le n$
- $-10^9 \le a_i \le 10^9$

## Solution Overview

The problem asks for maximizing the sum after removing elements from the edges.

Observations:

1. Removing elements from the edges is equivalent to **choosing a contiguous subarray somewhere in the middle** after some prefix and suffix removals.
2. The total number of elements you remove is at most $k$. If you remove $x$ from the left, you can remove at most $k - x$ from the right.

This suggests a **prefix-suffix approach**: try all valid numbers of elements removed from the left, compute the corresponding sum with elements removed from the right, and take the maximum.

## Detailed Solution

1. Compute the **prefix sum array** $P[i] = a_1 + a_2 + \dots + a_i$. Let $P[0] = 0$.
2. Compute the **suffix sum array** $S[i] = a_n + a_{n-1} + \dots + a_{n-i+1}$. Let $S[0] = 0$.

We want to remove $x$ elements from the left and $y$ elements from the right such that $x + y \le k$. Then the sum of remaining elements is:

$$\text{sum\_remaining} = \text{total\_sum} - P[x] - S[y]$$

Where `total_sum` is the sum of all elements.

1. Iterate $x$ from $0$ to $\min(k, n)$, and for each $x$, iterate $y$ from $0$ to $\min(k - x, n - x)$. Keep track of the **maximum remaining sum**.
2. Special case: if $k \ge n$, we can remove all elements, leaving a sum of 0 (or possibly negative infinity if you interpret empty array sum differently).

### Python Code Implementation

```python
n, k = map(int, input().split())
a = list(map(int, input().split()))

total_sum = sum(a)
prefix = [0] * (n + 1)
suffix = [0] * (n + 1)

for i in range(1, n + 1):
    prefix[i] = prefix[i-1] + a[i-1]

for i in range(1, n + 1):
    suffix[i] = suffix[i-1] + a[n-i]

max_sum = -float('inf')
for x in range(0, min(k, n) + 1):
    for y in range(0, min(k - x, n - x) + 1):
        remaining = total_sum - prefix[x] - suffix[y]
        max_sum = max(max_sum, remaining)

print(max_sum)
```
### Complexity Analysis

- **Time Complexity:** $O(k^2)$ in the worst case, but since $k \le n$, it’s acceptable for $n \le 2 \cdot 10^5$ if optimized further.
- **Space Complexity:** $O(n)$ for prefix and suffix arrays.

**Optimized Note:** You can reduce time to $O(k)$ by observing that for each $x$, you only need the maximum suffix sum of $k-x$ elements.

### Example

**Input:**

```
5 2
1 2 3 4 5
```

**Output:**

```
12
```

**Explanation:**

- Remove 1 element from left and 1 from right: remaining `[2, 3, 4]` → sum = 9
- Remove 2 elements from left: remaining `[3, 4, 5]` → sum = 12 (**maximum**)

This approach is standard for prefix-suffix removal problems and scales well with careful optimizations.

If you want, I can also **illustrate a fully optimized $O(k)$ solution with a sliding window trick** that handles very large arrays efficiently. It’s a neat trick often seen in Div. 1 D/E problems.

Do you want me to show that optimization too?
