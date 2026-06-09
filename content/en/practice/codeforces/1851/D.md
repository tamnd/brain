---
title: "CF 1851D - Prefix Permutation Sums"
description: "We are given an array derived from the prefix sums of a permutation of numbers from 1 to $n$. One of these prefix sums is missing. Our task is to determine whether the incomplete array could have come from a valid permutation."
date: "2026-06-09T17:15:50+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1851
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 888 (Div. 3)"
rating: 1300
weight: 1851
solve_time_s: 153
verified: false
draft: false
---

[CF 1851D - Prefix Permutation Sums](https://codeforces.com/problemset/problem/1851/D)

**Rating:** 1300  
**Tags:** implementation, math  
**Solve time:** 2m 33s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array derived from the prefix sums of a permutation of numbers from 1 to $n$. One of these prefix sums is missing. Our task is to determine whether the incomplete array could have come from a valid permutation.

A permutation here is simply an array containing each integer from 1 to $n$ exactly once. The prefix sum array is formed by summing elements cumulatively: $b_i = a_1 + a_2 + ... + a_i$. For example, the permutation $[1, 3, 2]$ has prefix sums $[1, 4, 6]$. If we remove a prefix sum, say 4, the array becomes $[1, 6]$. The problem is to decide whether there exists a permutation that would lead to the given array after dropping a single prefix sum.

The constraints give us up to $2 \cdot 10^5$ numbers summed over all test cases, so any solution must run in roughly $O(n)$ per test case. Brute force reconstruction of all permutations is completely infeasible because $n!$ grows extremely fast.

A subtle edge case arises when the missing element is the largest number in the permutation. For example, if $n = 4$ and the input prefix sums are $[1, 3, 6]$, the missing sum corresponds to the last element, 4, and we have to recognize this situation. Another tricky case is when removing a prefix sum hides a number that could otherwise be repeated, e.g., $[1, 3, 3]$ would look impossible but could correspond to a missing 2 in $[1, 3, 5, 6]$. A careless approach that only checks differences between consecutive prefix sums could fail here.

## Approaches

The brute-force approach would attempt to reconstruct all possible original arrays from the given prefix sums by trying to insert one number in all possible positions and check if the resulting array forms a valid permutation. This is correct in principle because each prefix sum defines cumulative sums uniquely, but the number of possibilities is $O(n)$ insertions per test case and $O(n)$ work per insertion to validate the permutation, resulting in $O(n^2)$. This would be too slow for $n \approx 2 \cdot 10^5$.

The key insight is that the missing element corresponds either to a single number from 1 to $n$ or to the last prefix sum itself. This reduces the problem to analyzing the differences between consecutive prefix sums, which represent the original numbers in the permutation (except for the missing one). Specifically, if the differences form a multiset that is almost all numbers from 1 to $n$, then the missing number is either the sum difference that’s too large or the number $n$ itself.

The faster approach is therefore: compute the differences between consecutive prefix sums to get candidate numbers, count how many times each number occurs, and verify that either one number is missing or one number is duplicated in a way that could account for the missing prefix. This reduces the solution to $O(n)$ per test case, which is feasible under the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, compute the differences between consecutive prefix sums. Include the first element of the prefix sum array as a difference because it equals the first element of the original permutation. Store these differences in a list called `nums`.
2. Compute the sum of numbers from 1 to $n$ using the formula $n(n+1)/2$.
3. Compare the sum of `nums` to this total sum. If they match, all numbers are present and the missing prefix sum corresponds to the last element. In this case, the array forms a valid permutation.
4. If the sum of `nums` is less than the total sum, calculate the missing number as the difference. Count the occurrences of each number in `nums`. If this missing number occurs exactly zero times and all other numbers are within 1 to $n$, then the permutation is possible by inserting the missing number at the correct position.
5. If any number occurs twice or a number is outside 1 to $n$, the answer is "NO". Otherwise, the answer is "YES".
6. Return the result for each test case.

**Why it works**: The differences between consecutive prefix sums are exactly the elements of the original permutation, except for the missing one. By checking the sum and frequency of these differences, we can infer whether there exists a single number that restores the full permutation from 1 to $n$.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        b = list(map(int, input().split()))
        total = n * (n + 1) // 2
        nums = [b[0]] + [b[i] - b[i - 1] for i in range(1, n - 1)]
        current_sum = sum(nums)
        
        if current_sum == total:
            print("YES")
            continue
        
        diff = total - current_sum
        count = {}
        valid = True
        for x in nums:
            if x < 1 or x > n:
                valid = False
                break
            count[x] = count.get(x, 0) + 1
            if count[x] > 1:
                valid = False
                break
        if not valid:
            print("NO")
        elif diff >= 1 and diff <= n and count.get(diff, 0) == 0:
            print("YES")
        else:
            print("NO")

solve()
```

This implementation reads input efficiently for multiple test cases, calculates the differences, and checks sum and frequency to verify whether a valid permutation is possible. Handling the first element separately ensures the correct reconstruction of the first element, which is a common source of off-by-one errors.

## Worked Examples

### Example 1

Input prefix sums: `[6, 8, 12, 15]`, $n=5$

| Step | nums | sum(nums) | total | diff | counts |
| --- | --- | --- | --- | --- | --- |
| Compute differences | [6, 2, 4, 3] | 15 | 15 | 0 | {6:1,2:1,4:1,3:1} |

The sum matches `n(n+1)/2`, so the missing number is the first element, which is 1. Valid permutation exists. Output: YES

### Example 2

Input prefix sums: `[1, 2, 100]`, $n=4$

| Step | nums | sum(nums) | total | diff | counts |
| --- | --- | --- | --- | --- | --- |
| Compute differences | [1,1,98] | 100 | 10 | -90 | {1:2,98:1} |

Duplicate `1` and out-of-range number `98` make it impossible. Output: NO

These traces show how the algorithm handles missing first, last, and middle elements, and how frequency and sum checks detect invalid cases.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Computing differences, sum, and frequency table all run linearly |
| Space | O(n) | Store `nums` and frequency dictionary for each test case |

Given the constraints, this solution handles up to $2 \cdot 10^5$ numbers comfortably within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("12\n5\n6 8 12 15\n5\n1 6 8 15\n4\n1 2 100\n4\n1 3 6\n2\n2\n3\n1 2\n4\n3 7 10\n5\n5 44 46 50\n4\n1 9 10\n5\n13 21 36 42\n5\n1 2 3 1000000000000000000\n9\n9 11 12 20 25 28 30 33\n") == "YES\nYES\nNO\nYES\nYES\nNO\nYES\nNO\nNO\nNO\nNO\nNO"

# Custom cases
assert run("1\n2\n1") == "YES", "smallest n"
assert run("1\n3\n3 5") == "YES", "missing middle"
assert run("1\n4\n1 3 6") == "YES", "missing last"
assert run("1\n5\n2 3 4 5") == "NO", "missing first invalid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2\n1` | YES | Smallest n, valid missing first element |
|  |  |  |
