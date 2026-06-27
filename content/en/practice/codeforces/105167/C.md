---
title: "CF 105167C - Counting Rectangles"
description: "We are given a grid drawn using horizontal and vertical lines. The grid is fully defined by having $n$ horizontal lines and $m$ vertical lines, evenly spaced in the plane."
date: "2026-06-27T10:02:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105167
codeforces_index: "C"
codeforces_contest_name: "ETH Zurich Competitive Programming Contest Spring 2024"
rating: 0
weight: 105167
solve_time_s: 56
verified: true
draft: false
---

[CF 105167C - Counting Rectangles](https://codeforces.com/problemset/problem/105167/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a grid drawn using horizontal and vertical lines. The grid is fully defined by having $n$ horizontal lines and $m$ vertical lines, evenly spaced in the plane. Any rectangle we form must use these lines as boundaries, meaning each side of the rectangle lies exactly on one of the grid lines.

A valid rectangle is determined by choosing two distinct horizontal lines as its top and bottom boundaries, and two distinct vertical lines as its left and right boundaries. Every such choice uniquely defines one rectangle. Two rectangles are considered the same only if their four corner points coincide, which again corresponds exactly to selecting the same pair of horizontal lines and the same pair of vertical lines.

The task is to count how many such non-degenerate rectangles exist.

The constraints are small, with $n, m \le 100$, so even cubic or quadratic approaches are feasible. However, the structure of the problem suggests we should expect a combinational counting identity rather than any simulation. Any approach that explicitly iterates over all rectangles by checking geometry is already effectively $O(n^2 m^2)$, which is still fine here but unnecessary.

A common mistake is to think in terms of “grid cells” instead of “grid lines”. If someone interprets $n$ and $m$ as cells rather than lines, they might incorrectly use $n \cdot m$ or similar expressions. Another subtle mistake is forgetting that a rectangle needs two distinct horizontal and two distinct vertical lines, so cases where $n < 2$ or $m < 2$ must produce zero.

For example, if $n = 1, m = 4$, there is only one horizontal line, so no rectangle can be formed at all. The correct answer is 0. Any approach that assumes “choose any pair” without checking feasibility would silently produce invalid combinations.

## Approaches

A brute-force interpretation starts by explicitly selecting a top and bottom horizontal line, then a left and right vertical line, and counting every valid combination. This is already a direct model of the problem: every rectangle corresponds to exactly one quadruple of distinct boundary lines.

The brute-force method works by iterating over all pairs of horizontal lines and all pairs of vertical lines. The number of horizontal pairs is $\binom{n}{2}$, and the number of vertical pairs is $\binom{m}{2}$. For each combination, we count one rectangle. This is correct because the rectangle is uniquely determined by its boundary lines.

The inefficiency only appears if we think in geometric enumeration terms, such as scanning all rectangles cell-by-cell or validating geometry explicitly. Even then, the problem size is small enough that $O(n^2 m^2)$ would pass, since $n, m \le 100$, giving at most $10^8$ operations, borderline but still acceptable in optimized Python.

The key observation is that the horizontal and vertical choices are independent. Once we choose two horizontal lines, they can pair with any valid pair of vertical lines. This decouples the problem into two combinatorial counts.

So the total number of rectangles is:

$$\binom{n}{2} \cdot \binom{m}{2}$$

This removes all need for iteration and reduces the solution to constant-time arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2 m^2)$ | $O(1)$ | Accepted but unnecessary |
| Optimal | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the integers $n$ and $m$. These represent counts of available horizontal and vertical grid lines.
2. Compute how many ways we can choose two distinct horizontal lines. This is $\frac{n(n-1)}{2}$. The reasoning is that a rectangle needs a top and bottom boundary, and order does not matter.
3. Compute how many ways we can choose two distinct vertical lines. This is $\frac{m(m-1)}{2}$, for the same reason.
4. Multiply these two values. Each horizontal pair can be combined with any vertical pair, and each combination forms exactly one rectangle.
5. Output the product.

### Why it works

Every rectangle is uniquely identified by a choice of two horizontal and two vertical lines. There is no overlap between different selections, and no selection produces more than one rectangle. This creates a bijection between the set of valid rectangles and the Cartesian product of the two combinations sets. Because of this one-to-one mapping, counting rectangles reduces exactly to multiplying independent combinatorial choices.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())

# choose any 2 horizontal lines
h = n * (n - 1) // 2

# choose any 2 vertical lines
v = m * (m - 1) // 2

print(h * v)
```

The solution relies entirely on the combinatorial identity rather than iteration. The most common implementation mistake is off-by-one indexing when people try to simulate grid cells instead of working with line counts. Another issue is forgetting integer division, but here we explicitly use `//` to ensure integer results.

The multiplication step is safe in Python due to arbitrary precision integers, so no overflow concerns exist.

## Worked Examples

### Example 1

Input:

```
3 4
```

We compute combinations step by step.

| Step | Horizontal lines | Vertical lines | Horizontal pairs | Vertical pairs | Result |
| --- | --- | --- | --- | --- | --- |
| Initial | 3 | 4 | - | - | - |
| Compute pairs | 3 | 4 | 3 | 6 | - |
| Final | 3 | 4 | 3 | 6 | 18 |

Here, $\binom{3}{2} = 3$ and $\binom{4}{2} = 6$, giving 18 rectangles.

This confirms that even a small grid produces multiple rectangles due to combinatorial pairing of boundaries.

### Example 2

Input:

```
2 5
```

| Step | Horizontal lines | Vertical lines | Horizontal pairs | Vertical pairs | Result |
| --- | --- | --- | --- | --- | --- |
| Initial | 2 | 5 | - | - | - |
| Compute pairs | 2 | 5 | 1 | 10 | - |
| Final | 2 | 5 | 1 | 10 | 10 |

This shows a degenerate case where only one horizontal pair exists. The result is entirely determined by vertical choices.

The trace demonstrates that the formula naturally handles small edge structures without special casing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a constant number of arithmetic operations |
| Space | $O(1)$ | No auxiliary data structures are used |

The computation consists of a few integer multiplications and divisions, independent of input size. Given $n, m \le 100$, the solution is far below any time limit constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline
    n, m = map(int, input().split())
    h = n * (n - 1) // 2
    v = m * (m - 1) // 2
    return str(h * v)

# provided sample
assert run("3 4") == "18"

# minimum case: no rectangle possible
assert run("1 1") == "0"

# only vertical flexibility
assert run("2 5") == "10"

# only horizontal flexibility
assert run("5 2") == "10"

# larger balanced case
assert run("10 10") == str((10*9//2)**2)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 0 | no valid pairs exist |
| 2 5 | 10 | single horizontal pair case |
| 5 2 | 10 | symmetric edge case |
| 10 10 | 2025 | larger combinatorial correctness |

## Edge Cases

When $n = 1$ or $m = 1$, the formula correctly yields zero because one of the binomial terms becomes zero. For input `1 4`, the computation becomes $\binom{1}{2} = 0$, so the result is 0. The algorithm handles this naturally without branching.

For `2 2`, both dimensions have exactly one possible pair of lines. The computation yields $1 \cdot 1 = 1$, which corresponds to the single rectangle formed by the outer boundary.

For larger but still small inputs like `3 3`, the algorithm produces $3 \cdot 3 = 9$, matching the full enumeration of all possible rectangles in a 2D grid of intersections.
