---
title: "CF 1656A - Good Pairs"
description: "We are asked to find a \"good pair\" of indices in an array of positive integers. A good pair consists of two indices $i$ and $j$ such that, if you consider any element $ak$ in the array, the sum of distances from $ai$ to $ak$ and from $ak$ to $aj$ equals the distance from $ai$ to…"
date: "2026-06-10T03:32:51+07:00"
tags: ["codeforces", "competitive-programming", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1656
codeforces_index: "A"
codeforces_contest_name: "CodeTON Round 1 (Div. 1 + Div. 2, Rated, Prizes!)"
rating: 800
weight: 1656
solve_time_s: 143
verified: true
draft: false
---

[CF 1656A - Good Pairs](https://codeforces.com/problemset/problem/1656/A)

**Rating:** 800  
**Tags:** math, sortings  
**Solve time:** 2m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to find a "good pair" of indices in an array of positive integers. A good pair consists of two indices $i$ and $j$ such that, if you consider any element $a_k$ in the array, the sum of distances from $a_i$ to $a_k$ and from $a_k$ to $a_j$ equals the distance from $a_i$ to $a_j$. In geometric terms, $a_k$ must lie on the straight line segment connecting $a_i$ and $a_j$, when considering the numbers on the real number line.

Input consists of multiple test cases, each with the array size $n$ and the array elements. The output must identify any good pair, and the problem guarantees that a solution always exists. A key detail is that $i$ may equal $j$, which immediately allows a trivial solution for arrays of size one.

The constraints allow up to $10^5$ elements in a single array, and the total sum across all test cases does not exceed $2 \cdot 10^5$. This means any solution performing more than linear work per array is likely too slow. We also must be careful with arrays where all elements are equal, arrays with two elements, or arrays with duplicates in general, since naive selection of the first two indices could fail if we ignore the absolute value property.

## Approaches

The brute-force approach is to try every pair of indices $(i, j)$ and check the defining property for all $k$. This requires $O(n^3)$ operations in the worst case because for each of $O(n^2)$ pairs we examine $n$ elements. This is clearly infeasible with $n$ up to $10^5$.

Observing the equality

$$|a_i - a_k| + |a_k - a_j| = |a_i - a_j|$$

reveals a simplification. The left-hand side equals the distance from $a_i$ to $a_j$ if and only if $a_k$ lies between $a_i$ and $a_j$ inclusive. That is, either $a_i \le a_k \le a_j$ or $a_j \le a_k \le a_i$. This insight reduces the problem to finding two numbers that are the minimum and maximum in the array. Any $k$ will automatically satisfy the property because all other elements lie between the smallest and largest values. Thus, the problem reduces to identifying the minimum and maximum elements in $O(n)$ time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(1) | Too slow |
| Min-Max Selection | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$ and the array $a$.
2. Initialize two variables to store the minimum value and maximum value of the array, and their respective indices.
3. Iterate over the array. If the current element is smaller than the current minimum, update the minimum and its index. If it is larger than the current maximum, update the maximum and its index.
4. After finishing the iteration, we now have indices of the smallest and largest elements. Output these indices as the good pair.
5. If the array contains only one element, output its index twice. This covers the edge case without additional checks.

Why it works: by choosing the smallest and largest numbers, all other array elements lie between them. This guarantees that for any $k$, $|a_i - a_k| + |a_k - a_j| = |a_i - a_j|$, satisfying the good pair property. No element can violate the equality, and linear scanning ensures correctness and efficiency.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        min_val = float('inf')
        max_val = float('-inf')
        min_idx = max_idx = 0

        for idx, val in enumerate(a):
            if val < min_val:
                min_val = val
                min_idx = idx
            if val > max_val:
                max_val = val
                max_idx = idx

        # output 1-based indices
        print(min_idx + 1, max_idx + 1)

if __name__ == "__main__":
    solve()
```

The solution reads each array efficiently using fast I/O. We track indices carefully to return 1-based results. Using `float('inf')` and `float('-inf')` ensures correct initialization even for large integers. Iterating once over the array guarantees $O(n)$ time per test case.

## Worked Examples

**Sample Input 1:** `5 1 4 2 2 3`

| Index | Value | min_val | min_idx | max_val | max_idx |

|---|---|---|---|---
