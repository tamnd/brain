---
title: "CF 912A - Tricky Alchemy"
description: "Grisha has a stash of yellow and blue crystals and wants to craft a specific number of yellow, green, and blue balls. Each type of ball consumes crystals differently."
date: "2026-06-12T10:15:55+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 912
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 456 (Div. 2)"
rating: 800
weight: 912
solve_time_s: 349
verified: false
draft: false
---

[CF 912A - Tricky Alchemy](https://codeforces.com/problemset/problem/912/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 5m 49s  
**Verified:** no  

## Solution
## Problem Understanding

Grisha has a stash of yellow and blue crystals and wants to craft a specific number of yellow, green, and blue balls. Each type of ball consumes crystals differently. A yellow ball requires two yellow crystals, a green ball consumes one yellow and one blue crystal, and a blue ball consumes three blue crystals. The input gives the counts of yellow and blue crystals currently available and the numbers of balls of each type Grisha wants. The task is to compute the minimum number of additional crystals Grisha must obtain to meet the desired counts.

The main constraints are that both crystal counts and ball counts can be as high as $10^9$. This immediately rules out any simulation approach that iterates over individual crystals or balls, as the number of operations would exceed feasible limits. Calculations must be done arithmetically, using sums, differences, and maximum functions.

Non-obvious edge cases arise when Grisha already has more than enough crystals of one type but not the other. For instance, if he has 100 yellow crystals and 0 blue crystals but only wants one green ball, he will still need one blue crystal. Similarly, if he has zero crystals and wants zero balls, the answer should be zero, which can be overlooked if one blindly computes required crystals as differences without maxing against zero.

## Approaches

A naive brute-force approach would try to iteratively "craft" each ball and decrement the corresponding crystal counts. For each yellow ball, subtract two yellow crystals; for each green ball, subtract one yellow and one blue; for each blue ball, subtract three blue. If a crystal count goes negative, track how many additional crystals are needed. This approach is correct in principle but fails for large inputs because iterating over up to $10^9$ balls is impossible.

The key observation is that each ball type has a fixed, small number of crystal requirements and these can be aggregated. We can compute the total yellow crystals needed as twice the number of yellow balls plus the number of green balls. Total blue crystals needed are three times the number of blue balls plus the number of green balls. The difference between required crystals and available crystals, clamped to zero, gives the number of additional crystals needed. This arithmetic approach reduces the problem to a constant number of operations, independent of the actual counts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(x + y + z) | O(1) | Too slow for large x, y, z |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the current number of yellow and blue crystals, $A$ and $B$, and the target numbers of yellow, green, and blue balls, $x$, $y$, $z$.
2. Compute the total number of yellow crystals required as $2 \cdot x + y$. This accounts for two crystals per yellow ball and one per green ball.
3. Compute the total number of blue crystals required as $3 \cdot z + y$. This accounts for three crystals per blue ball and one per green ball.
4. Compute additional yellow crystals needed as the maximum of zero and the difference between total required yellow crystals and available yellow crystals, $\max(0, 2 \cdot x + y - A)$.
5. Compute additional blue crystals needed similarly as $\max(0, 3 \cdot z + y - B)$.
6. The total additional crystals needed is the sum of the additional yellow and blue crystals.
7. Print this sum.

Why it works: each ball has fixed, additive crystal requirements. Aggregating these first ensures that we never undercount crystals, and using $\max(0, \text{needed} - \text{available})$ ensures we only count crystals we actually need to acquire. There are no dependencies between different ball types that could lead to overcounting.

## Python Solution

```python
import sys
input = sys.stdin.readline

A, B = map(int, input().split())
x, y, z = map(int, input().split())

required_yellow = 2 * x + y
required_blue = 3 * z + y

additional_yellow = max(0, required_yellow - A)
additional_blue = max(0, required_blue - B)

print(additional_yellow + additional_blue)
```

The code first reads the available crystals and target balls. It then calculates the total crystal requirements by combining contributions from all relevant balls. Using `max(0, ...)` ensures that we never report negative additional crystals if Grisha already has enough. Finally, summing these gives the minimal number of crystals Grisha must acquire.

## Worked Examples

Sample 1:

| Variable | Value |
| --- | --- |
| A | 4 |
| B | 3 |
| x | 2 |
| y | 1 |
| z | 1 |
| required_yellow | 2*2 + 1 = 5 |
| required_blue | 3*1 + 1 = 4 |
| additional_yellow | max(0, 5 - 4) = 1 |
| additional_blue | max(0, 4 - 3) = 1 |
| total | 1 + 1 = 2 |

This demonstrates that aggregating crystal needs correctly accounts for overlapping requirements, in this case the green ball's contribution to both crystal types.

Custom Example:

Input: `0 0\n1 1 1\n`

| Variable | Value |
| --- | --- |
| A | 0 |
| B | 0 |
| x | 1 |
| y | 1 |
| z | 1 |
| required_yellow | 2*1 + 1 = 3 |
| required_blue | 3*1 + 1 = 4 |
| additional_yellow | max(0, 3 - 0) = 3 |
| additional_blue | max(0, 4 - 0) = 4 |
| total | 3 + 4 = 7 |

This trace confirms that when starting with no crystals, the calculation still produces the correct number.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only arithmetic operations and a few max computations are used, independent of input sizes |
| Space | O(1) | Only a fixed number of variables are allocated, no data structures grow with input |

Given the constraints $0 \le A, B, x, y, z \le 10^9$, the constant-time arithmetic ensures the solution executes well within the 1-second time limit and uses negligible memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    A, B = map(int, input().split())
    x, y, z = map(int, input().split())
    required_yellow = 2 * x + y
    required_blue = 3 * z + y
    additional_yellow = max(0, required_yellow - A)
    additional_blue = max(0, required_blue - B)
    return str(additional_yellow + additional_blue)

# Provided sample
assert run("4 3\n2 1 1\n") == "2", "sample 1"

# Custom cases
assert run("0 0\n1 1 1\n") == "7", "all crystals missing"
assert run("5 5\n0 0 0\n") == "0", "no balls needed"
assert run("10 10\n3 0 2\n") == "0", "enough crystals for all balls"
assert run("1 1\n1 1 1\n") == "5", "small numbers, partial crystals"
assert run("1000000000 1000000000\n1000000000 1000000000 1000000000\n") == "1000000001", "large numbers, edge"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0\n1 1 1 | 7 | All crystals missing |
| 5 5\n0 0 0 | 0 | No balls needed |
| 10 10\n3 0 2 | 0 | Sufficient crystals, no additional needed |
| 1 1\n1 1 1 | 5 | Partial crystals, must compute differences |
| 10^9 10^9\n10^9 10^9 10^9 | 1000000001 | Large inputs near upper limit |

## Edge Cases

If Grisha already has more crystals than required, the algorithm correctly returns zero. For input `5 5\n1 1 1\n`, `required_yellow` is 3 and `required_blue` is 4. Since both are less than available crystals, `max(0, ...)` produces 0 for both
