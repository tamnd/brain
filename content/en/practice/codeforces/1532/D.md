---
title: "CF 1532D - Teams Forming"
description: "We are given an even number of students, each with a programming skill level. The goal is to form exactly $n/2$ teams, each containing two students. A team is valid only if both students have the same skill level."
date: "2026-06-10T16:37:19+07:00"
tags: ["codeforces", "competitive-programming", "*special", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1532
codeforces_index: "D"
codeforces_contest_name: "Kotlin Heroes: Practice 7"
rating: 0
weight: 1532
solve_time_s: 81
verified: true
draft: false
---

[CF 1532D - Teams Forming](https://codeforces.com/problemset/problem/1532/D)

**Rating:** -  
**Tags:** *special, sortings  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an even number of students, each with a programming skill level. The goal is to form exactly $n/2$ teams, each containing two students. A team is valid only if both students have the same skill level. To achieve this, students can solve problems, each of which increases their skill by one.

The input consists of $n$ (the number of students) and an array of integers representing the skills. The output is a single integer: the minimum total number of problems students need to solve so that every student is paired into a team of equal skills.

The constraints are small: $2 \le n \le 100$ and $1 \le a_i \le 100$. With $n$ capped at 100, any algorithm up to $O(n^2 \log n)$ or $O(n^2)$ will run comfortably within the time limit. This suggests that even a pairwise comparison approach is feasible, but we should aim for something simpler and more direct. Edge cases that can trip up a naive solution include having multiple duplicates or all unique values, where the minimal number of problems may require non-obvious pairings.

A careless approach would be to simply pair students in input order. For example, with input `4\n1 3 2 2`, pairing `(1,3)` and `(2,2)` would cost `2` for the first pair, but a better solution is `(1,2)` and `(2,3)` which costs only `1`. This shows the order of pairing matters.

## Approaches

A brute-force approach would consider every possible pairing of the $n$ students. There are $(n-1)!!$ ways to form pairs (double factorial), which is factorial in growth and impractical even for $n=20$. At each pairing, we would compute the cost to equalize the skills. This approach is correct in principle but computationally infeasible.

The key observation is that the cost to equalize two students depends only on the absolute difference of their skills. This suggests that if we sort the students by skill, pairing adjacent students minimizes the cost. Sorting ensures that the difference between paired students is the smallest possible, and any other pairing would only increase the sum of differences. Once sorted, the optimal strategy is to pair the first student with the second, the third with the fourth, and so on. This reduces the problem to $O(n \log n)$ for sorting plus $O(n)$ for summing differences.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n-1)!!) | O(n) | Too slow |
| Optimal (sort + adjacent pairs) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read $n$ and the array of skills $a$. Sorting requires a data structure that allows ordering; a list is sufficient.
2. Sort the array $a$ in non-decreasing order. This ensures that the difference between consecutive elements is minimized.
3. Initialize a variable `total_cost` to zero. This will accumulate the number of problems to be solved.
4. Iterate over the array in steps of two, pairing $a[i]$ with $a[i+1]$. For each pair, compute the cost as $a[i+1] - a[i]$ and add it to `total_cost`. Pairing in sorted order guarantees minimal total cost.
5. After processing all pairs, output `total_cost`.

Why it works: After sorting, each student is paired with the closest possible skill level. Any attempt to cross-pair students would replace small differences with larger differences, increasing the total number of problems required. The invariant is that after sorting, consecutive elements form the globally optimal minimal difference pairs.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))
a.sort()

total_cost = 0
for i in range(0, n, 2):
    total_cost += a[i+1] - a[i]

print(total_cost)
```

The solution starts with reading input efficiently. Sorting ensures minimal pairwise differences. The loop iterates in steps of two to form pairs correctly. Computing `a[i+1] - a[i]` directly gives the number of problems needed for each team. Edge cases such as duplicates or identical skills require zero problems, which the subtraction automatically handles.

## Worked Examples

**Sample 1:**

Input: `6\n5 10 2 3 14 5`

Sorted array: `[2, 3, 5, 5, 10, 14]`

| i | Pair | Cost | total_cost |
| --- | --- | --- | --- |
| 0 | (2,3) | 1 | 1 |
| 2 | (5,5) | 0 | 1 |
| 4 | (10,14) | 4 | 5 |
