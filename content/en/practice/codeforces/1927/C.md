---
title: "CF 1927C - Choose the Different Ones!"
description: "We are given two arrays, a and b, and an even integer k. We need to pick exactly k/2 elements from each array such that the multiset of chosen elements contains all integers from 1 to k."
date: "2026-06-08T18:53:24+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1927
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 923 (Div. 3)"
rating: 1000
weight: 1927
solve_time_s: 138
verified: false
draft: false
---

[CF 1927C - Choose the Different Ones!](https://codeforces.com/problemset/problem/1927/C)

**Rating:** 1000  
**Tags:** brute force, greedy, math  
**Solve time:** 2m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two arrays, `a` and `b`, and an even integer `k`. We need to pick exactly `k/2` elements from each array such that the multiset of chosen elements contains **all integers from `1` to `k`**. The order in which we pick elements does not matter; what matters is coverage of the full range `[1, k]`.

The input provides multiple test cases. Each test case specifies the lengths of the arrays `n` and `m`, the arrays themselves, and the value of `k`. The output is a simple "YES" or "NO" depending on whether the selection is possible.

The constraints are moderate but important. `n` and `m` can be up to `2 * 10^5` individually, and the sum across all test cases does not exceed `4 * 10^5`. This rules out any approach that examines **all possible subsets** of size `k/2` in either array, because the number of subsets grows combinatorially. Instead, we need a solution that can scan each array linearly or near-linearly. The value of `k` is always even and satisfies `k <= 2 * min(n, m)`, which guarantees that selecting `k/2` elements from each array is always feasible in terms of count.

Edge cases are subtle. One is when an array contains repeated elements. For instance, if `k=4`, `a=[1,1,1,1]` and `b=[2,3,4]`, we can pick only `1` from `a` (as many as we like, but duplicates don't cover new numbers), and we cannot satisfy the coverage requirement, so the answer is "NO". Another case is when `k/2` is equal to the length of an array, forcing us to pick all elements there. We must still check that the other array can cover the remaining numbers. Ignoring these nuances leads to subtle errors.

## Approaches

The naive approach is brute-force. One could enumerate all subsets of size `k/2` from `a` and all subsets of size `k/2` from `b`, then check whether their union covers all numbers from `1` to `k`. While this would work in theory, the complexity is `O(n choose k/2 * m choose k/2 * k)`, which is infeasible for `n, m` up to `2*10^5`.

The key insight is that we do not care about specific subsets, only about **which numbers are present**. Each array can contribute a number to the coverage only once, even if it has multiple duplicates. So, we can treat each array as a **set of numbers less than or equal to `k`**. The problem then reduces to checking whether it is possible to choose at most `k/2` elements from each set while collectively covering all `1..k`.

In practice, we only need to compute how many numbers from `1..k` are present in each array. Let `count_in_a` be the number of numbers in `1..k` that appear in `a`, and similarly `count_in_b` for `b`. If `count_in_a > k/2`, we can only pick `k/2` numbers from `a`, so effectively the number of covered numbers from `a` is `min(count_in_a, k/2)`. Similarly for `b`. Then, the problem reduces to verifying whether the sum of these contributions is at least `k`. If so, a valid selection exists; otherwise, it does not.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n choose k/2) * (m choose k/2) * k) | O(k) | Too slow |
| Optimal | O(n + m + k) per test case | O(k) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n`, `m`, `k` and the arrays `a` and `b`.
3. Initialize two boolean arrays (or sets) `present_a` and `present_b` of length `k+1` to track which numbers from `1..k` appear in `a` and `b` respectively.
4. For each number in `a`, if it is between `1` and `k`, mark it as present in `present_a`.
5. Repeat for `b`, marking `present_b`.
6. Count the numbers in `1..k` that appear in each array: `count_in_a` is the sum of `present_a[1..k]`, and `count_in_b` is the sum of `present_b[1..k]`.
7. Compute the effective contribution of each array: `contrib_a = min(count_in_a, k/2)`, `contrib_b = min(count_in_b, k/2)`.
8. If `contrib_a + contrib_b >= k`, output "YES". Otherwise, output "NO".

**Why it works:** The invariant is that each array can contribute at most `k/2` numbers to the coverage. By counting the actual numbers present and capping them at `k/2`, we simulate the maximum coverage each array can provide. If their combined coverage reaches `k`, then a valid selection of `k/2` elements from each array exists; otherwise, it is impossible.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m, k = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    present_a = [0] * (k + 1)
    present_b = [0] * (k + 1)
    
    for x in a:
        if 1 <= x <= k:
            present_a[x] = 1
    for x in b:
        if 1 <= x <= k:
            present_b[x] = 1
    
    count_in_a = sum(present_a[1:])
    count_in_b = sum(present_b[1:])
    
    contrib_a = min(count_in_a, k // 2)
    contrib_b = min(count_in_b, k // 2)
    
    print("YES" if contrib_a + contrib_b >= k else "NO")
```

The solution reads input efficiently and uses boolean arrays to track which numbers are available. The use of `min(count, k//2)` ensures we respect the limit of how many elements we can pick from each array. Summing the presence array is safe because we ignore numbers outside `1..k`. This avoids off-by-one errors.

## Worked Examples

**Example 1:** `a=[2,3,8,5,6,5]`, `b=[1,3,4,10,5]`, `k=6`.

| Number | Present in a | Present in b |
| --- | --- | --- |
| 1 | 0 | 1 |
| 2 | 1 | 0 |
| 3 | 1 | 1 |
| 4 | 0 | 1 |
| 5 | 1 | 1 |
| 6 | 1 | 0 |

`count_in_a = 4`, `count_in_b = 4`. `k/2 = 3`. `contrib_a = 3`, `contrib_b = 3`. Sum = 6 ≥ k → YES.

**Example 2:** `a=[2,3,4,5,6,5]`, `b=[1,3,8,10,3]`, `k=6`.

| Number | Present in a | Present in b |
| --- | --- | --- |
| 1 | 0 | 1 |
| 2 | 1 | 0 |
| 3 | 1 | 1 |
| 4 | 1 | 0 |
| 5 | 1 | 0 |
| 6 | 1 | 0 |

`count_in_a = 5`, `count_in_b = 2`. `contrib_a = 3`, `contrib_b = 2`. Sum = 5 < 6 → NO.

These traces show that capping the contributions ensures the solution respects the `k/2` selection limit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m + k) per test case | Scanning each array once, summing presence arrays |
| Space | O(k) | Two arrays of size k+1 to track presence |

Across all test cases, the sum of `n + m` ≤ 4 * 10^5, and `k ≤ 2 * min(n, m)` ≤ 4 * 10^5. Total operations fit comfortably in the 2-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # call the solution code
    t = int(input())
    for _ in range(t):
        n, m, k = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        present_a =
```
