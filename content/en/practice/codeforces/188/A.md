---
title: "CF 188A - Hexagonal Numbers"
description: "We are asked to calculate the n-th hexagonal number. Hexagonal numbers represent a figurate number pattern where each number counts the total tiles forming a hexagon with successive layers. The formula for the n-th hexagonal number is given by $Hn = 2n^2 - n$."
date: "2026-06-05T00:32:29+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 188
codeforces_index: "A"
codeforces_contest_name: "Surprise Language Round 6"
rating: 1100
weight: 188
solve_time_s: 75
verified: true
draft: false
---

[CF 188A - Hexagonal Numbers](https://codeforces.com/problemset/problem/188/A)

**Rating:** 1100  
**Tags:** *special  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to calculate the _n_-th hexagonal number. Hexagonal numbers represent a figurate number pattern where each number counts the total tiles forming a hexagon with successive layers. The formula for the _n_-th hexagonal number is given by $H_n = 2n^2 - n$. Conceptually, the first hexagonal number is a single tile, the second adds a surrounding layer to form a larger hexagon, and so on.

The input is a single integer $n$ representing which hexagonal number to compute, constrained to 1 ≤ n ≤ 100. The output is a single integer, the value of the corresponding hexagonal number.

Given the constraint $n \le 100$, the computation remains small. Even the largest value, $H_{100} = 2 \cdot 100^2 - 100 = 19900$, easily fits in standard 32-bit or 64-bit integers. This means no special handling of large integers or optimization is necessary for performance. A naive approach is already efficient, but reasoning carefully about the formula ensures correctness.

Potential edge cases include the smallest input $n = 1$ which should output 1, and confirming the formula scales correctly for $n = 100$. A careless implementation might misapply the formula, forget the subtraction of $n$, or use a floating-point calculation that introduces rounding errors.

## Approaches

A brute-force approach would attempt to construct the hexagonal number iteratively by summing the tiles in each layer up to the $n$-th layer. For example, one could sum $1 + 6 + 12 + 18 + \dots$ where each term corresponds to tiles added per new layer. While correct, this approach is unnecessary because the formula $H_n = 2n^2 - n$ directly gives the answer. Iteratively adding layers is redundant and increases complexity, though for $n \le 100$ it would still execute instantly.

The key observation is that the problem provides a closed-form formula. Recognizing this allows a direct calculation in constant time. There are no dependencies on previous numbers other than computing $n^2$ and performing simple arithmetic. The problem reduces to evaluating the quadratic expression for the input $n$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (sum layers iteratively) | O(n) | O(1) | Accepted but unnecessary |
| Formula (direct calculation) | O(1) | O(1) | Accepted and optimal |

## Algorithm Walkthrough

1. Read the integer $n$ from input. This represents which hexagonal number we need to compute.
2. Compute $n^2$. This captures the quadratic growth of hexagonal numbers as the number of layers increases.
3. Multiply $n^2$ by 2. The pattern of hexagonal numbers doubles the square term to account for the tiles extending outward in six directions.
4. Subtract $n$ from the result. This corrects for the overcounting of the central tile in the doubling step, aligning with the formula $H_n = 2n^2 - n$.
5. Print the result. This is the value of the $n$-th hexagonal number.

Why it works: The invariant is that the formula exactly counts the number of tiles in a hexagonal arrangement up to the $n$-th layer. Each layer adds a predictable number of tiles, and the quadratic term captures the growth, while the linear subtraction corrects for the single central tile counted multiple times. Since we apply the formula directly, no iterative steps can introduce error.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
hex_num = 2 * n * n - n
print(hex_num)
```

The code reads a single integer, computes the hexagonal number using the closed-form formula, and prints it. Multiplying before subtracting ensures integer arithmetic throughout. Using `sys.stdin.readline` guarantees fast input, though here the difference is negligible due to a single line. The multiplication order prevents operator precedence errors.

## Worked Examples

### Example 1

Input:

```
3
```

| Step | n | 2*n^2 | 2*n^2 - n | hex_num |
| --- | --- | --- | --- | --- |
| Compute | 3 | 18 | 18 - 3 = 15 | 15 |

The calculation matches the expected output. Each step aligns with the algorithm, confirming the formula works for small n.

### Example 2

Input:

```
1
```

| Step | n | 2*n^2 | 2*n^2 - n | hex_num |
| --- | --- | --- | --- | --- |
| Compute | 1 | 2 | 2 - 1 = 1 | 1 |

This traces the smallest input. The output confirms the algorithm correctly handles boundary cases.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations are performed regardless of n. |
| Space | O(1) | Only a single integer variable is used. |

Given the maximum $n = 100$, the operations are trivial. The solution easily executes within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(sys.stdin.readline())
    return str(2 * n * n - n)

# Provided sample
assert run("3\n") == "15", "sample 1"

# Custom cases
assert run("1\n") == "1", "minimum n"
assert run("100\n") == "19900", "maximum n"
assert run("50\n") == "4950", "mid-range n"
assert run("2\n") == "6", "small n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | Minimum input boundary |
| 100 | 19900 | Maximum input boundary |
| 50 | 4950 | Mid-range correctness |
| 2 | 6 | Small input correctness |

## Edge Cases

For $n = 1$, the algorithm computes $2*1^2 - 1 = 1$, which is exactly the first hexagonal number. For $n = 100$, the computation $2*100^2 - 100 = 19900$ confirms the formula scales correctly. Both cases demonstrate the algorithm handles extreme bounds without off-by-one errors or integer overflow. The algorithm consistently applies the formula for any $n$ within the constraints.
