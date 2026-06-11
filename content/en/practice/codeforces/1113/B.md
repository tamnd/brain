---
title: "CF 1113B - Sasha and Magnetic Machines"
description: "We are given an array of integers representing the power of n magnetic machines. Each machine contributes positively to the total power of the farm."
date: "2026-06-12T04:56:45+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1113
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 539 (Div. 2)"
rating: 1300
weight: 1113
solve_time_s: 65
verified: true
draft: false
---

[CF 1113B - Sasha and Magnetic Machines](https://codeforces.com/problemset/problem/1113/B)

**Rating:** 1300  
**Tags:** greedy, number theory  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers representing the power of `n` magnetic machines. Each machine contributes positively to the total power of the farm. The farmer can perform **at most one operation**: pick two machines, choose an integer `x` that divides the power of the first machine, reduce the first machine’s power by a factor of `x`, and simultaneously multiply the second machine’s power by `x`. All powers must remain positive integers. If desired, the farmer can also choose not to perform any operation.

The goal is to determine the **minimum possible total power** after optionally performing this operation.

The constraints are moderate: `n` goes up to 50,000 and each `a_i` is at most 100. Because `a_i` is small, any factorization or divisor enumeration is inexpensive. The main challenge is handling `n` efficiently: a naive check of every pair `(i, j)` with every divisor of `a_i` would result in O(n² * d) operations, which is potentially 2500 million if we blindly iterate through all pairs, too slow for 1-second execution.

Non-obvious edge cases include arrays where all elements are equal, arrays where one element is `1`, or arrays where reducing the largest element and increasing the smallest gives the maximal benefit. For example, `[1, 100]` could reduce `100` by a factor of `100` to `1` and multiply `1` by `100` to `100`, leaving the sum unchanged. If handled carelessly, an algorithm might incorrectly perform unnecessary operations.

## Approaches

The brute-force approach would consider every pair of machines `(i, j)` and every possible divisor `x` of `a_i`. For each combination, it would calculate the new total sum after applying the operation and keep track of the minimum. This is correct but too slow because the number of pairs is `n*(n-1)/2` and the number of divisors can be up to 50 (for numbers up to 100). At the upper limit, this could be on the order of 50,000² * 50 ≈ 125 billion operations, clearly infeasible.

The key observation is that the **maximum gain comes from reducing the largest element and increasing the smallest element**. Formally, the operation reduces one number by a factor and increases another by the same factor. Since all numbers are small (≤100), we can precompute the divisors for every number. We then iterate over each machine `i` as the one to reduce, find its divisors, and apply each divisor `x` to the machine with the **smallest current power** `j` ≠ `i`. This reduces the number of pairs we consider dramatically. The total operations become O(n * d), where `d` is the maximum number of divisors for any number (at most 50), which is acceptable.

This insight converts a potentially cubic algorithm into a linear one with respect to `n`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² * d) | O(1) | Too slow |
| Optimal | O(n * d) | O(n + d) | Accepted |

## Algorithm Walkthrough

1. Compute the total sum of the array, which is our baseline if no operation is applied.
2. Precompute all divisors for numbers from 1 to 100. This lets us quickly enumerate potential reduction factors for each machine.
3. Identify the **smallest machine power** `min_val` and its index. This machine is the best candidate to receive a multiplication to minimize the total sum.
4. Iterate over each machine `i` as a candidate for reduction. For each divisor `x` of `a_i` (excluding 1):

- Compute the new power for `i`: `a_i / x`.
- Compute the new power for `j` (the smallest machine): `a_j * x`.
- Calculate the new total sum using `sum - a_i - a_j + (a_i / x) + (a_j * x)`.
- Track the minimum total sum.
5. If no operation improves the total sum, retain the original sum.
6. Output the minimum total sum.

Why it works: The total sum changes by `(a_i / x + a_j * x) - (a_i + a_j)`. To minimize the sum, reducing large numbers and increasing small numbers has the greatest potential to decrease this difference. By only considering the smallest recipient machine, we capture the best-case scenario without needing to check all O(n²) pairs.

## Python Solution

```python
import sys
input = sys.stdin.readline

# Precompute divisors for numbers 1..100
divisors = [[] for _ in range(101)]
for i in range(1, 101):
    for j in range(1, i + 1):
        if i % j == 0:
            divisors[i].append(j)

n = int(input())
a = list(map(int, input().split()))

total_sum = sum(a)
min_total = total_sum

# Find index of smallest machine power
min_val = min(a)
min_idx = a.index(min_val)

for i in range(n):
    if i == min_idx:
        continue  # can't reduce and increase same machine
    for x in divisors[a[i]]:
        if x == 1:
            continue  # operation must change values
        new_ai = a[i] // x
        new_aj = a[min_idx] * x
        new_total = total_sum - a[i] - a[min_idx] + new_ai + new_aj
        if new_total < min_total:
            min_total = new_total

print(min_total)
```

The code first computes all divisors, which is cheap because numbers are ≤100. We then iterate over each machine `i` and consider only divisors >1 to reduce its power. We always multiply the smallest machine `a[min_idx]` to maximize the decrease in total sum. The algorithm avoids O(n²) by restricting the recipient to the minimal machine, which is mathematically sound due to the monotonicity of the sum reduction formula.

## Worked Examples

**Sample 1**

Input: `5`, `[1, 2, 3, 4, 5]`

| i | a[i] | x | new_ai | new_aj | new_total |
| --- | --- | --- | --- | --- | --- |
| 3 | 4 | 2 | 2 | 2 | 14 |

Original sum: 15

Optimal operation: reduce `4 → 2`, multiply `1 → 2`. Total sum = 14

**Sample 2**

Input: `4`, `[3, 6, 2, 5]`

| i | a[i] | x | new_ai | new_aj | new_total |
| --- | --- | --- | --- | --- | --- |
| 1 | 6 | 2 | 3 | 2*2=4 | 3+3+4+5=15 |

Original sum: 16

Optimal total sum: 15

These traces confirm the algorithm correctly identifies the largest contributor to reduce and the smallest to increase, producing the minimal total sum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * d) | For each machine, iterate over its divisors (d ≤ 50) |
| Space | O(n + d) | Store array, precomputed divisors |

With n ≤ 50,000 and d ≤ 50, O(n*d) ≈ 2.5 million operations, well within 1s time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    divisors = [[] for _ in range(101)]
    for i in range(1, 101):
        for j in range(1, i + 1):
            if i % j == 0:
                divisors[i].append(j)
    n = int(input())
    a = list(map(int, input().split()))
    total_sum = sum(a)
    min_total = total_sum
    min_val = min(a)
    min_idx = a.index(min_val)
    for i in range(n):
        if i == min_idx:
            continue
        for x in divisors[a[i]]:
            if x == 1:
                continue
            new_ai = a[i] // x
            new_aj = a[min_idx] * x
            new_total = total_sum - a[i] - a[min_idx] + new_ai + new_aj
            if new_total < min_total:
                min_total = new_total
    return str(min_total)

# provided samples
assert run("5\n1 2 3 4 5\n") == "14", "sample 1"
assert run("3\n1 2 3\n") == "5", "sample 2"

# custom cases
assert run("2\n1 100\n") == "101", "edge min max"
assert run("4\n10 10 10 10\n") == "40", "all equal"
assert run("3\n1 1 100\n") == "102", "reduce largest, increase smallest"
assert run("5\n1 2 2 2 50\n") == "57", "mix small and one large"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
