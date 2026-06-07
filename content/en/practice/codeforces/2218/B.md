---
title: "CF 2218B - The 67th 6-7 Integer Problem"
description: "We are given exactly seven integers. The task is to negate six of them-multiply them by -1-and leave one unchanged, then compute the sum. We want the maximum sum achievable by choosing which six to negate."
date: "2026-06-07T18:30:01+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 2218
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1090 (Div. 4)"
rating: 800
weight: 2218
solve_time_s: 109
verified: false
draft: false
---

[CF 2218B - The 67th 6-7 Integer Problem](https://codeforces.com/problemset/problem/2218/B)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 1m 49s  
**Verified:** no  

## Solution
## Problem Understanding

We are given exactly seven integers. The task is to negate six of them-multiply them by `-1`-and leave one unchanged, then compute the sum. We want the maximum sum achievable by choosing which six to negate. Conceptually, each number can either contribute positively or negatively depending on whether we flip it. Since there are only seven numbers, there are only seven possible ways to select the number to leave unnegated.

The constraints are very small. Each number is between `-67` and `67`, and there are at most `6767` test cases. This means any algorithm that processes a single test case in constant time will run efficiently, even at the upper limit of inputs. Edge cases include all numbers being positive, all negative, or mixtures where the largest absolute value might be either positive or negative. For example, if all numbers are positive, leaving the largest positive number unnegated will maximize the sum because negating it would subtract the largest amount.

A naive approach that tries all subsets of six numbers to negate is feasible for seven numbers, but understanding the underlying pattern is better. We need to identify which number to leave unnegated to maximize the sum.

An example of a subtle edge case is `a = [1, 2, 3, 4, 5, 6, 7]`. Negating six numbers and leaving `7` unnegated produces a sum of `-1-2-3-4-5-6+7 = -14`. Leaving `1` unnegated produces `1-2-3-4-5-6-7 = -26`. The maximum is obtained by leaving the number with the smallest value negative if most numbers are positive. Another example is `a = [-1, -2, -3, -4, -5, -6, -7]`. Negating six and leaving `-1` gives `1+2+3+4+5+6-7 = 14`. Leaving `-7` gives `1+2+3+4+5+6-7 = 14`. The principle is that the maximum sum is obtained by leaving the number with the smallest absolute value unchanged if all are negative, or leaving the largest number unchanged if all are positive.

## Approaches

The brute-force approach would enumerate all subsets of six numbers to negate and compute the sum each time. There are exactly seven such subsets because choosing six to negate is equivalent to choosing one to leave. Computing the sum of each subset requires summing seven numbers, leading to a total of `7*7 = 49` operations per test case. This is extremely small and feasible, but we can reason more carefully to avoid even this.

The key observation is that negating six numbers out of seven is equivalent to negating all numbers except one. Therefore, for each test case, we only need to consider leaving each number unnegated and summing the transformed array. Since the sum after leaving `a[i]` unnegated is equal to the negative of the sum of all other numbers plus `a[i]`, the problem reduces to computing the sum of all numbers once and then, for each candidate, calculating `sum_except_i = total_sum - a[i]` and the candidate sum `candidate_sum = -sum_except_i + a[i] = -total_sum + 2 * a[i]`. The maximum of these seven values is the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(7^2) = O(49) per test case | O(1) | Accepted but unnecessary |
| Optimal | O(7) per test case | O(1) | Accepted, minimal computation |

## Algorithm Walkthrough

1. For each test case, read the seven integers into a list `a`.
2. Compute the total sum of the list, `total_sum = sum(a)`.
3. Initialize a variable `max_sum` to a very small number, for example `-inf`.
4. For each number `a[i]` in the list, compute the sum obtained by leaving it unnegated. This is `candidate_sum = -total_sum + 2 * a[i]`.
5. If `candidate_sum` is greater than `max_sum`, update `max_sum`.
6. After checking all seven numbers, `max_sum` contains the maximum possible sum after negating six numbers. Output it.

Why it works: Negating six out of seven numbers is equivalent to negating all numbers except one. Computing `-total_sum + 2 * a[i]` efficiently gives the sum without physically creating a new array for each choice. Iterating through all seven possibilities guarantees we consider every valid choice.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a = list(map(int, input().split()))
    total_sum = sum(a)
    max_sum = -float('inf')
    for x in a:
        candidate = -total_sum + 2 * x
        if candidate > max_sum:
            max_sum = candidate
    print(max_sum)
```

The code first reads the number of test cases and then iterates over each one. It converts the input line into integers and computes the total sum. The loop computes the candidate sum for leaving each number unnegated and keeps track of the maximum. Using `-total_sum + 2 * x` avoids creating new arrays and ensures the computation is exact. The initialization of `max_sum` to negative infinity handles all-negative arrays correctly.

## Worked Examples

Sample input: `441 41 41 41 41 41 416`

| Step | total_sum | Candidate sums for leaving each number | max_sum |
| --- | --- | --- | --- |
| Compute total_sum | 1022 | - | - |
| Leave 441 | -1022 + 882 = -140 | -140 | -140 |
| Leave 41 | -1022 + 82 = -940 | -140 | -140 |
| Leave 41 | -940 | -140 | -140 |
| Leave 41 | -940 | -140 | -140 |
| Leave 41 | -940 | -140 | -140 |
| Leave 41 | -940 | -140 | -140 |
| Leave 416 | -1022 + 832 = -190 | -140 | -140 |

The maximum sum is `-140`.

Another input: `6 9 4 20 6 7 67`

| Step | total_sum | Candidate sums | max_sum |
| --- | --- | --- | --- |
| total_sum | 119 | - | - |
| Leave 6 | -119 + 12 = -107 | -107 | -107 |
| Leave 9 | -119 + 18 = -101 | -101 | -101 |
| Leave 4 | -119 + 8 = -111 | -101 | -101 |
| Leave 20 | -119 + 40 = -79 | -79 | -79 |
| Leave 6 | -119 + 12 = -79 | -79 | -79 |
| Leave 7 | -119 + 14 = -79 | -79 | -79 |
| Leave 67 | -119 + 134 = 15 | 15 | 15 |

The maximum sum is `15`, which matches the sample output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * 7) = O(t) | Each test case involves summing 7 numbers and iterating 7 numbers |
| Space | O(7) = O(1) | Only the array of 7 numbers and a few variables are stored |

Given `t <= 6767`, the solution performs at most `6767 * 7 ≈ 47000` operations, far below typical limits. Memory usage is minimal and safe under the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        a = list(map(int, input().split()))
        total_sum = sum(a)
        max_sum = -float('inf')
        for x in a:
            candidate = -total_sum + 2 * x
            if candidate > max_sum:
                max_sum = candidate
        print(max_sum)
    return output.getvalue().replace('\r','')

# provided samples
assert run("2\n441 41 41 41 41 41 416\n6 9 4 20 6 7 67\n") == "-205\n15\n", "sample 1"

# custom cases
assert run("1\n1 1 1 1 1 1 1\n") == "-5\n", "all ones"
assert run("1\n-1 -1 -1 -1 -1 -1 -1\n") == "5\n", "all negative ones"
assert run("1\n-5 -4 0 3 2 1 -1\n") == "13\n", "mixed numbers"
assert run("1\n67 67 67 67 67 67 67\n") == "67\n", "all max values"
assert run("1\n-67 -67 -67 -67 -67 -67 -67\n") == "67\n", "all min values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1 1 |  |  |
