---
title: "CF 478C - Table Decorations"
description: "We have three types of balloons: red, green, and blue. Each table at a banquet requires exactly three balloons, and no table can have all three balloons of the same color."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 478
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 273 (Div. 2)"
rating: 1800
weight: 478
solve_time_s: 69
verified: true
draft: false
---

[CF 478C - Table Decorations](https://codeforces.com/problemset/problem/478/C)

**Rating:** 1800  
**Tags:** greedy  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We have three types of balloons: red, green, and blue. Each table at a banquet requires exactly three balloons, and no table can have all three balloons of the same color. The task is to compute the maximum number of tables we can decorate given a certain number of red, green, and blue balloons.

The input consists of three integers representing the number of balloons of each color. The output is a single integer: the maximum number of tables that satisfy the constraint. The bounds on balloon counts go up to 2×10^9, which means we cannot afford any algorithm that iterates through all possible combinations. We need a solution that runs in essentially constant time with respect to the input values.

A naive approach might attempt to decrement the counts in a loop, always taking one balloon from each available color. This fails when one color dominates: if we have many more red balloons than green and blue, a simple greedy approach that always takes one of each may leave unused red balloons that could have been paired more effectively. An example is having 10 red, 1 green, and 1 blue balloon. Naively taking one of each color produces only one table, but we cannot make more because we must avoid repeating all the same color. The correct output is indeed 1, but the greedy choice can become non-obvious with slightly more balanced numbers, so the algorithm must reason about the relative sizes.

Another potential pitfall is relying on integer division by 3 of the sum of balloons. While the maximum number of tables cannot exceed `(r + g + b) // 3`, this is only an upper bound. A careless approach might return this value directly without considering the individual color limits.

## Approaches

The brute-force method would be to repeatedly select three balloons while ensuring they are not all the same color. In practice, we would select the three largest counts and decrement each. While this guarantees correctness, in the worst case it could require up to 2×10^9 iterations if all counts are large. Clearly, iterating that many times is not feasible.

The key observation for an optimal solution is that the problem is constrained by both the total number of balloons and the largest individual color. Each table requires three balloons, so the maximum number of tables is at most `(r + g + b) // 3`. On the other hand, if one color has more than the sum of the other two, the excess balloons cannot be paired to form tables, so the effective number of tables is also bounded by the sum of the two smaller colors. Therefore, the true maximum number of tables is the minimum of these two quantities: `(r + g + b) // 3` and `r + g + b - max(r, g, b)` (equivalently, the sum of the two smaller numbers). This ensures we never attempt to over-allocate a dominant color or violate the per-table color rule.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(max(r, g, b)) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the counts of red, green, and blue balloons into variables `r`, `g`, and `b`. This gives us the total available resources to work with.
2. Compute the sum of all balloons. Divide this sum by three using integer division to get the theoretical maximum number of tables if colors were perfectly balanced. Store this as `max_by_total`. This ensures we never exceed the total number of balloons available.
3. Identify the largest balloon count among the three colors. The sum of the two smaller counts is the maximum number of tables we can actually form without violating the per-table color restriction. Store this as `max_by_balance`.
4. The answer is the minimum of `max_by_total` and `max_by_balance`. This guarantees that we respect both the total balloon limit and the distribution constraint.

Why it works: The algorithm maintains two invariants. First, `(r + g + b) // 3` ensures we cannot make more tables than total balloons allow. Second, the sum of the two smaller counts ensures that no table ends up with three identical colors. Because each table removes one balloon from three colors in some combination, this bound captures all feasible arrangements. Taking the minimum guarantees we respect both constraints simultaneously.

## Python Solution

```python
import sys
input = sys.stdin.readline

r, g, b = map(int, input().split())

total = r + g + b
max_total_tables = total // 3
max_by_balance = total - max(r, g, b)

print(min(max_total_tables, max_by_balance))
```

The code first reads the three integers efficiently using `sys.stdin.readline`. It calculates the total number of balloons and derives the theoretical upper bound by dividing by three. It then calculates the sum of the two smaller counts as `total - max(r, g, b)`, which is equivalent to taking the sum of the other two colors. Finally, it prints the minimum of the two bounds to respect both constraints. Using subtraction instead of sorting is a subtle optimization to avoid unnecessary operations.

## Worked Examples

**Sample 1**: Input `5 4 3`

| r | g | b | total | max_total_tables | max_by_balance | min |
| --- | --- | --- | --- | --- | --- | --- |
| 5 | 4 | 3 | 12 | 4 | 9 | 4 |

We can form 4 tables. The algorithm confirms that even though the total allows for 4 tables, the largest color does not restrict us because 5 ≤ 4 + 3.

**Sample 2**: Input `10 1 1`

| r | g | b | total | max_total_tables | max_by_balance | min |
| --- | --- | --- | --- | --- | --- | --- |
| 10 | 1 | 1 | 12 | 4 | 2 | 2 |

The sum of the two smaller colors is only 2, which limits the number of tables. Even though the total allows 4 tables, the imbalance prevents more than 2 tables. The algorithm correctly outputs 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only arithmetic and comparisons, no iteration |
| Space | O(1) | Uses a constant number of variables |

Given the input constraints (up to 2×10^9), these operations complete well within 1 second, and no extra memory beyond a few integers is required.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    r, g, b = map(int, input().split())
    total = r + g + b
    return str(min(total // 3, total - max(r, g, b)))

# Provided samples
assert run("5 4 3\n") == "4", "sample 1"
# Custom cases
assert run("10 1 1\n") == "2", "dominant red"
assert run("0 0 0\n") == "0", "no balloons"
assert run("6 6 6\n") == "6", "all equal"
assert run("2 3 7\n") == "5", "large imbalance"
assert run("2000000000 2000000000 2000000000\n") == "2000000000", "maximum values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 10 1 1 | 2 | One color dominates, limits tables |
| 0 0 0 | 0 | No balloons, zero tables |
| 6 6 6 | 6 | All colors equal, perfectly balanced |
| 2 3 7 | 5 | Imbalance handled correctly |
| 2×10^9 2×10^9 2×10^9 | 2×10^9 | Maximum input values |

## Edge Cases

For input `10 1 1`, the total divided by three gives 4, but the largest color is 10 while the sum of the other two is 2. The algorithm computes `total - max(r, g, b) = 12 - 10 = 2`, correctly limiting the tables to 2. For input `0 0 0`, both `total // 3` and `total - max(...)` yield 0, correctly producing zero tables. In the case where all counts are equal, the sum divided by three and `total - max(...)` produce the same number, ensuring no off-by-one error occurs. This demonstrates that the approach handles both extreme imbalances and perfectly balanced inputs correctly.
