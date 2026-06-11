---
title: "CF 1154A - Restoring Three Numbers"
description: "We are given four numbers that represent three pairwise sums of unknown positive integers $a$, $b$, $c$ and the sum of all three numbers. These four numbers are in no particular order. Our task is to reconstruct the original three integers $a$, $b$, $c$ from these sums."
date: "2026-06-12T02:47:34+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1154
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 552 (Div. 3)"
rating: 800
weight: 1154
solve_time_s: 91
verified: false
draft: false
---

[CF 1154A - Restoring Three Numbers](https://codeforces.com/problemset/problem/1154/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 1m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given four numbers that represent three pairwise sums of unknown positive integers $a$, $b$, $c$ and the sum of all three numbers. These four numbers are in no particular order. Our task is to reconstruct the original three integers $a$, $b$, $c$ from these sums.

The input guarantees that a solution exists, which simplifies our task because we do not need to validate feasibility. Each number on the board is at least 2 and at most $10^9$, meaning we are dealing with small input size (only four numbers) but potentially very large integers. Because there are only four numbers, any algorithm with constant or linear time complexity is acceptable.

Edge cases to consider include situations where some or all of $a$, $b$, and $c$ are equal. For example, if $a = b = c = 1$, the four numbers on the board would be $2, 2, 2, 3$. A naive approach that assumes all sums are distinct could fail here. Another case is when two numbers are equal, such as $a = b = 2, c = 3$, producing sums $4, 5, 5, 7$. Recognizing the sum of all three numbers and separating it from the pairwise sums is critical.

## Approaches

A brute-force approach would attempt to check all possible assignments of the four numbers to the roles of $a+b$, $a+c$, $b+c$, and $a+b+c$. There are only $4! = 24$ permutations, which is small, so a pure brute-force would work. For each permutation, we could solve a small linear system of equations and check if all results are positive integers. This approach works because there are only four numbers, but it is unnecessarily complicated and not intuitive.

The key observation is that the sum of all three numbers $a+b+c$ is always the largest number among the four because it includes all three positive integers. Once we identify the largest number as $a+b+c$, the remaining three numbers must be the pairwise sums. Denote the largest number as $S = a+b+c$ and the other numbers as $x, y, z$. Then we can solve directly for the original numbers:

- $a = S - (b+c) = S - x$
- $b = S - (a+c) = S - y$
- $c = S - (a+b) = S - z$

This works regardless of order because $x, y, z$ represent all pairwise sums. The algorithm reduces to sorting, identifying the largest number, and simple subtraction. It is simple, direct, and avoids unnecessary enumeration.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(24) = O(1) | O(1) | Works but unnecessary |
| Optimal | O(4 log 4) = O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the four integers into a list. This captures the sums as provided in arbitrary order.
2. Sort the list in ascending order. Sorting makes it easy to identify the largest number, which is guaranteed to be $a+b+c$ because all three integers are positive.
3. Let the last number in the sorted list be $S = a+b+c$. Let the first three numbers in the sorted list be $x, y, z$. These correspond to the pairwise sums but we do not need to know which is which.
4. Compute the original numbers by subtracting each pairwise sum from $S$:

- $a = S - x$
- $b = S - y$
- $c = S - z$

These calculations work because $S - x$ removes the sum that includes all integers except one, leaving the remaining integer.
5. Print $a$, $b$, and $c$ in any order.

Why it works: Sorting guarantees we identify $a+b+c$ as the largest number. Subtracting each remaining number from the sum of all three isolates the individual integers. Because we are guaranteed a solution with positive integers, there is no ambiguity, and the operations correctly reconstruct the original numbers.

## Python Solution

```python
import sys
input = sys.stdin.readline

nums = list(map(int, input().split()))
nums.sort()
S = nums[3]
a = S - nums[0]
b = S - nums[1]
c = S - nums[2]
print(a, b, c)
```

The solution reads input efficiently, sorts the four numbers, identifies the largest as the total sum, and reconstructs each individual number using subtraction. Sorting ensures we consistently identify $a+b+c$ without manually checking which sum contains all three numbers. Subtraction order is flexible because the problem allows any order in output.

## Worked Examples

**Sample 1:**

Input: `3 6 5 4`

Sorted list: `3 4 5 6`

Largest sum $S = 6$

Remaining sums: `3, 4, 5`

| Step | Variable | Value |
| --- | --- | --- |
| 1 | nums | [3,4,5,6] |
| 2 | S | 6 |
| 3 | a = S - nums[0] | 6 - 3 = 3 |
| 4 | b = S - nums[1] | 6 - 4 = 2 |
| 5 | c = S - nums[2] | 6 - 5 = 1 |

Output: `3 2 1` (any order valid)

This confirms that subtracting each pairwise sum from the total sum isolates the correct integers.

**Sample 2:**

Input: `2 2 2 3`

Sorted list: `2 2 2 3`

Largest sum $S = 3$

Remaining sums: `2, 2, 2`

| Step | Variable | Value |
| --- | --- | --- |
| 1 | nums | [2,2,2,3] |
| 2 | S | 3 |
| 3 | a = 3 - 2 | 1 |
| 4 | b = 3 - 2 | 1 |
| 5 | c = 3 - 2 | 1 |

Output: `1 1 1`

Algorithm correctly handles the all-equal numbers case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(4 log 4) = O(1) | Sorting four numbers takes constant time. |
| Space | O(1) | Only four numbers are stored plus three variables for output. |

Given the small input size, this algorithm is extremely efficient and comfortably fits within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    nums = list(map(int, input().split()))
    nums.sort()
    S = nums[3]
    a = S - nums[0]
    b = S - nums[1]
    c = S - nums[2]
    return f"{a} {b} {c}"

# Provided sample
assert run("3 6 5 4\n") in ["3 2 1", "2 3 1", "1 2 3"], "sample 1"

# Custom cases
assert run("2 2 2 3\n") == "1 1 1", "all equal case"
assert run("4 5 5 7\n") in ["3 2 2", "2 3 2", "2 2 3"], "two equal numbers"
assert run("10 11 15 21\n") in ["11 6 10", "10 11 6", "6 10 11"], "general case"
assert run("1000000000 1000000000 1000000000 3000000000\n") == "1000000000 1000000000 1000000000", "max values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 6 5 4 | 3 2 1 | general case |
| 2 2 2 3 | 1 1 1 | all equal numbers |
| 4 5 5 7 | 3 2 2 | two equal numbers |
| 10 11 15 21 | 6 10 11 | arbitrary order of sums |
| 10^9 10^9 10^9 3*10^9 | 10^9 10^9 10^9 | maximum input size |

## Edge Cases

If all numbers are equal, for example `2 2 2 3`, sorting identifies `3` as the sum of all three numbers. Subtracting `2` from `3` produces `1` for each individual number, correctly reconstructing `a = b = c = 1`.

If two numbers are equal, for instance `4 5 5 7`, sorting gives `4,5,5,7`. The largest `7` is $a+b+c$. Subtracting `4,5,5` produces `3,2,2`, which correctly identifies the original integers
