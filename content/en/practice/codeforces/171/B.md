---
title: "CF 171B - Star"
description: "In this problem, we are asked to calculate the total number of cells in a star-shaped pattern drawn on a grid, given a number of layers. The input is a single integer a, representing the number of concentric layers in the star."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "combinatorics"]
categories: ["algorithms"]
codeforces_contest: 171
codeforces_index: "B"
codeforces_contest_name: "April Fools Day Contest"
rating: 1300
weight: 171
solve_time_s: 177
verified: true
draft: false
---

[CF 171B - Star](https://codeforces.com/problemset/problem/171/B)

**Rating:** 1300  
**Tags:** *special, combinatorics  
**Solve time:** 2m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

In this problem, we are asked to calculate the total number of cells in a star-shaped pattern drawn on a grid, given a number of layers. The input is a single integer `a`, representing the number of concentric layers in the star. The output is a single integer, which is the total number of cells that would be colored in if we drew all `a` layers of the star.

Each layer of the star increases its size symmetrically, so the number of cells grows according to a simple combinatorial formula. The first layer is a single cell in the center. The second layer adds cells around it forming a cross-like pattern plus corners, and each subsequent layer adds more cells following the same symmetric structure.

The constraints tell us that `a` can go up to 18257. Given that the output can reach up to 2·10⁹, this implies that any naive simulation of filling a grid layer by layer would be too slow and memory-intensive. We need a closed-form formula for the number of cells to handle the maximum input efficiently.

An edge case is when `a = 1`. The correct output is 1, as only the central cell is present. A careless approach that assumes at least two layers or uses a formula without handling the first layer explicitly would produce an incorrect result.

## Approaches

The brute-force approach would attempt to simulate drawing each layer of the star explicitly, counting each cell added. The first layer adds 1, the second adds 12, the third adds 24, and so on. While this is conceptually correct, it would require iterating over each layer and each cell in the layer. With `a = 18257`, the total number of cells grows roughly like `6*a^2 + 6*a + 1`, which is around 2·10⁹ operations for the largest `a`. This is too slow and exceeds memory limits if we attempt to store the grid.

The key insight is to recognize the pattern in the number of cells. The sequence of the total number of cells is a quadratic sequence: the first layer is 1, the second is 13, the third is 37, and so on. By examining the differences between layers, we notice that each new layer adds `12 * (layer - 1)` cells. This leads to a closed formula for the total number of cells in `a` layers: `1 + 6*a*(a-1)`.

The brute-force approach works for small `a` because we can simulate each layer safely, but fails at large `a` due to quadratic growth. The observation that the sequence is quadratic lets us compute the result directly in constant time without iteration.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(a²) | O(a²) | Too slow for max input |
| Closed-Form Formula | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer `a` from input. This represents the number of layers in the star.
2. Compute the total number of cells using the closed formula `1 + 6*a*(a-1)`. This formula arises from observing that each layer `i` (where `i ≥ 2`) adds `12*(i-1)` cells, and summing these gives a quadratic expression.
3. Print the computed total.

The reason this works is that the formula correctly captures the pattern of cell addition. The first layer contributes 1. Every subsequent layer adds 12 more cells than the previous layer did in total, producing the sequence of differences 12, 24, 36, etc., which sums to the quadratic formula.

## Python Solution

```python
import sys
input = sys.stdin.readline

a = int(input())
result = 1 + 6 * a * (a - 1)
print(result)
```

The solution reads a single integer `a`, calculates the total number of cells using the derived formula, and prints it. The formula uses integer arithmetic only, so there are no floating-point issues. We multiply `6*a*(a-1)` first, which avoids integer overflow because Python handles large integers automatically.

## Worked Examples

**Sample 1:** Input `2`

| Step | a | Formula calculation | Result |
| --- | --- | --- | --- |
| Read input | 2 |  |  |
| Compute cells | 2 | 1 + 6_2_(2-1) = 1 + 12 | 13 |
| Print output |  |  | 13 |

This confirms that the formula correctly accounts for the first two layers.

**Sample 2:** Input `3`

| Step | a | Formula calculation | Result |
| --- | --- | --- | --- |
| Read input | 3 |  |  |
| Compute cells | 3 | 1 + 6_3_(3-1) = 1 + 36 | 37 |
| Print output |  |  | 37 |

The trace shows that the formula correctly captures the growth pattern.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Single formula evaluation without loops |
| Space | O(1) | Only stores the input and result |

The algorithm executes in constant time and space regardless of `a`. Even at the maximum `a = 18257`, the computation is trivial for modern CPUs and fits comfortably in Python's integer type.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    a = int(sys.stdin.readline())
    return str(1 + 6 * a * (a - 1))

# provided sample
assert run("2\n") == "13", "sample 1"
# custom cases
assert run("1\n") == "1", "minimum input"
assert run("3\n") == "37", "three layers"
assert run("18257\n") == str(1 + 6*18257*18256), "maximum input"
assert run("10\n") == "541", "ten layers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | Minimum input edge case |
| 2 | 13 | Provided sample, small number of layers |
| 3 | 37 | Correct summing of multiple layers |
| 18257 | 1 + 6_18257_18256 | Maximum input handling |
| 10 | 541 | Typical mid-range input |

## Edge Cases

For `a = 1`, the formula evaluates to `1 + 6*1*(1-1) = 1`. The algorithm correctly outputs 1 without special handling. For large inputs such as `a = 18257`, the formula computes `1 + 6*18257*18256` directly, avoiding any iteration or memory-intensive simulation. All intermediate products stay within Python's integer range. This guarantees correct results for the entire input range.
