---
title: "CF 102899B - KK \u5b66\u51e0\u4f55"
description: "We are given a stream of geometric figures, each described by a type identifier followed by its dimensions. Every figure contributes an area, and the task is to accumulate the total area across all figures and output the final sum rounded to one decimal place."
date: "2026-07-04T08:19:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102899
codeforces_index: "B"
codeforces_contest_name: "The 2nd Hangzhou Normal University Freshman Programming Contest"
rating: 0
weight: 102899
solve_time_s: 47
verified: true
draft: false
---

[CF 102899B - KK \u5b66\u51e0\u4f55](https://codeforces.com/problemset/problem/102899/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a stream of geometric figures, each described by a type identifier followed by its dimensions. Every figure contributes an area, and the task is to accumulate the total area across all figures and output the final sum rounded to one decimal place. The geometry involved is intentionally simple: circles use a fixed value of π equal to 3, triangles use the standard half base times height formula, and rectangles use the product of side lengths.

The input size is small, with at most 1000 shapes and all dimensions bounded by 100. This immediately tells us that any solution running in linear time over the input is sufficient, and even straightforward floating-point arithmetic is safe in terms of performance and precision. There is no need for spatial data structures or optimization tricks, since each shape is independent of the others and contributes additively to the final answer.

A subtle edge case comes from precision and formatting. Even though all inputs are integers, the triangle area involves division by 2, and the final output must be printed with exactly one digit after the decimal point. A careless implementation that uses integer division would silently break half of the cases. For example, a triangle with base 3 and height 1 should contribute 1.5, but integer division would produce 1.

Another edge case is the fixed π value. Many programmers instinctively use math.pi, but here the problem explicitly defines π = 3, so using a real approximation like 3.14159 would produce consistently incorrect answers.

## Approaches

The structure of the problem is additive: each figure contributes independently to a running total. This means the most direct approach is also the correct one. We read each shape, compute its area immediately, and add it to an accumulator.

A brute-force interpretation would still do exactly the same thing, since there is no interaction between shapes. The only difference between a naive and optimal solution would be implementation cleanliness rather than algorithmic efficiency. Even if we recomputed everything multiple times or stored all shapes and processed them later, the cost would remain linear in the number of shapes, which is trivial under the constraints.

The key observation is that the problem is not asking for any transformation, sorting, or geometric relationship between figures. Each line is self-contained, so the computation reduces to a direct mapping from input record to numeric contribution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (store and recompute) | O(n) | O(n) | Accepted |
| Optimal (stream accumulation) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process each figure one by one and maintain a running sum.

1. Read the number of figures n, which determines how many independent computations we will perform. This sets the number of iterations for the main loop.
2. Initialize a variable total to 0. This variable accumulates the sum of all computed areas. It must be floating-point to correctly store triangle halves.
3. For each of the n lines, read the type identifier t and the associated parameters. The parsing step is purely structural and determines which formula to apply.
4. If the type is 1, interpret the parameters as the radius r of a circle. Compute area as 3 * r * r using the problem’s fixed π value. Add this to total.
5. If the type is 2, interpret the parameters as base L and height h of a triangle. Compute area as (L * h) / 2.0 to ensure floating-point division is used. Add this to total.
6. If the type is 3, interpret the parameters as rectangle dimensions L and W. Compute area as L * W and add it to total.
7. After processing all shapes, output total formatted with exactly one digit after the decimal point.

The correctness of this procedure relies on the fact that each shape contributes independently and linearly to the final sum, so no ordering or intermediate structure affects the result.

### Why it works

The algorithm maintains the invariant that after processing i shapes, total equals the sum of areas of exactly those i shapes. Each iteration adds exactly one new independent area value derived solely from the current input line. Since no step modifies previous contributions and no shape depends on another, the invariant holds inductively until the last element, at which point total equals the sum of all areas.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    total = 0.0

    for _ in range(n):
        parts = input().split()
        t = int(parts[0])

        if t == 1:
            r = int(parts[1])
            total += 3 * r * r
        elif t == 2:
            L = int(parts[1])
            h = int(parts[2])
            total += (L * h) / 2.0
        else:
            L = int(parts[1])
            W = int(parts[2])
            total += L * W

    print(f"{total:.1f}")

if __name__ == "__main__":
    solve()
```

The implementation keeps everything in a single pass over the input. The use of floating-point arithmetic is only necessary for triangles, but the accumulator is kept as a float throughout to avoid repeated type conversions. The formatting step at the end ensures correct rounding behavior to one decimal place.

A common mistake is writing `(L * h) // 2`, which forces integer division and discards fractional halves. Another mistake is forgetting to use 3 as π, which is explicitly required by the problem and overrides mathematical constants.

## Worked Examples

Consider a small input with a circle and a rectangle.

Input:

```
2
1 2
3 3 4
```

| Step | Type | Computation | Total |
| --- | --- | --- | --- |
| 1 | Circle r=2 | 3 × 2 × 2 = 12 | 12 |
| 2 | Rectangle 3×4 | 12 | 24 |

The final output is 24.0. This trace shows that accumulation is purely additive and order independent.

Now consider a case involving a triangle.

Input:

```
3
2 3 1
1 1
2 4 2
```

| Step | Type | Computation | Total |
| --- | --- | --- | --- |
| 1 | Triangle 3×1 | 1.5 | 1.5 |
| 2 | Circle r=1 | 3 | 4.5 |
| 3 | Triangle 4×2 | 4 | 8.5 |

This example demonstrates why floating-point division is necessary. The first triangle contributes a fractional value, and preserving it is essential for correctness.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each of the n shapes is processed exactly once with constant work per shape |
| Space | O(1) | Only a running sum and a few temporary variables are used |

The constraints allow up to 1000 shapes, so a single pass with constant-time computation per shape is trivially fast within the limits. Memory usage is minimal since no storage of the full input is required beyond the current line.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    output = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = output

    solve()

    sys.stdout = sys_stdout
    return output.getvalue().strip()

# provided sample-like case
assert run("2\n1 2\n3 3 4\n") == "24.0"

# triangle precision case
assert run("1\n2 3 1\n") == "1.5"

# all circles
assert run("3\n1 1\n1 2\n1 3\n") == "42.0"

# mixed minimal case
assert run("3\n1 1\n2 2 2\n3 1 1\n") == "9.0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 circle | 3.0 | basic circle formula and π = 3 |
| triangle only | 1.5 | correct fractional handling |
| multiple circles | 42.0 | repeated accumulation correctness |
| mixed shapes | 9.0 | integration of all three formulas |

## Edge Cases

A key edge case is the triangle computation where integer division would silently break correctness. For an input like `2 3 1`, the correct result is 1.5. The algorithm explicitly uses floating-point division `(L * h) / 2.0`, ensuring that the fractional component is preserved.

Another edge case is precision formatting. Even when the result is an integer, such as a single rectangle `3 2`, the output must still be printed as `6.0`. The formatted output `f"{total:.1f}"` enforces this consistently.

A final edge case is the misuse of π. If a solver uses a standard library constant like `math.pi`, the circle contributions will be slightly larger than expected, and errors will accumulate across multiple circles. Using the fixed constant 3 avoids this systematic drift entirely.
