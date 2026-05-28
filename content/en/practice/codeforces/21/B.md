---
title: "CF 21B - Intersection"
description: "Each input line describes a geometric object in the plane. The equation $$Ax + By + C = 0$$ represents a line. The task"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 21
codeforces_index: "B"
codeforces_contest_name: "Codeforces Alpha Round 21 (Codeforces format)"
rating: 2000
weight: 21
solve_time_s: 81
verified: true
draft: false
---

[CF 21B - Intersection](https://codeforces.com/problemset/problem/21/B)

**Rating:** 2000  
**Tags:** implementation, math  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

Each input line describes a geometric object in the plane. The equation

$$Ax + By + C = 0$$

represents a line. The task is to determine how many points belong to both lines at the same time.

Two different non-parallel lines intersect at exactly one point. Two parallel but distinct lines never meet. Two identical lines overlap completely, so they share infinitely many points. The output format follows this directly:

- print `1` if the lines intersect once,
- print `0` if they never intersect,
- print `-1` if they are actually the same line.

The constraints are tiny, coefficients are only between `-100` and `100`. Performance is not the challenge here. The entire problem is about correctly handling all geometric cases and avoiding mistakes with proportional coefficients.

The dangerous part is distinguishing between “parallel” and “identical”. A naive implementation might only compare slopes. That works for detecting parallelism, but it cannot tell whether the equations describe the exact same line.

Consider this input:

```
1 1 0
2 2 0
```

The second equation is just the first multiplied by `2`, so both describe the same line. The correct answer is:

```
-1
```

A careless implementation that only checks whether the determinant is zero would incorrectly print `0`.

Another tricky case is when one pair of coefficients matches proportionally but the constant term does not.

```
1 1 1
2 2 3
```

The direction vectors are proportional, so the lines are parallel. But the constants are not scaled by the same factor, so these are distinct parallel lines. The correct output is:

```
0
```

A buggy equality check might wrongly classify them as identical.

There is also a subtle edge case involving zero coefficients:

```
0 1 0
0 2 0
```

These equations become:

$$y = 0$$

and

$$2y = 0$$

Again they are the same line, even though `A = 0`. Any solution based on division can crash or lose precision here. Integer cross-multiplication avoids that completely.

## Approaches

The brute-force idea would be to explicitly solve the linear system and inspect the result. For two equations:

$$A_1x + B_1y + C_1 = 0$$

$$A_2x + B_2y + C_2 = 0$$

we can compute the determinant:

$$D = A_1B_2 - A_2B_1$$

If `D ≠ 0`, the system has a unique solution, so the answer is `1`.

If `D = 0`, the lines are parallel. At that point we still need to distinguish between “same line” and “different lines”. One way is to solve for ratios using floating point arithmetic. That works in theory, but it is unnecessarily fragile because division by zero and precision issues appear immediately.

The key observation is that identical lines must have all coefficients proportional:

$$\frac{A_1}{A_2} =
\frac{B_1}{B_2} =
\frac{C_1}{C_2}$$

Instead of dividing, we compare products:

$$A_1B_2 = A_2B_1$$

$$A_1C_2 = A_2C_1$$

$$B_1C_2 = B_2C_1$$

This completely avoids floating point errors and handles zeros naturally.

The problem becomes a small case analysis based on determinants and proportionality.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force with floating point ratios | O(1) | O(1) | Risky implementation |
| Optimal integer determinant checks | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the six coefficients describing the two lines.
2. Compute the determinant:

$$D = A_1B_2 - A_2B_1$$

If `D ≠ 0`, the lines are not parallel, so they intersect at exactly one point. Print `1`.

1. If `D = 0`, the lines are parallel or identical. We now check whether all coefficients are proportional.
2. Compare:

$$A_1C_2 = A_2C_1$$

and

$$B_1C_2 = B_2C_1$$

The determinant check already guarantees:

$$A_1B_2 = A_2B_1$$

so these extra comparisons are enough to verify full proportionality.

1. If both proportionality checks hold, the equations describe the same line. Print `-1`.
2. Otherwise the lines are parallel but distinct. Print `0`.

### Why it works

The determinant tells us whether the direction vectors of the two lines are linearly independent. A nonzero determinant means the lines must cross once.

When the determinant is zero, both lines have the same direction, so either they never meet or they coincide entirely. Two linear equations describe the same geometric line exactly when one equation can be obtained by multiplying the other by a constant. Cross-multiplication checks this proportionality without division, so every possible combination of zero and nonzero coefficients is handled safely.

## Python Solution

```python
import sys
input = sys.stdin.readline

a1, b1, c1 = map(int, input().split())
a2, b2, c2 = map(int, input().split())

det = a1 * b2 - a2 * b1

if det != 0:
    print(1)
else:
    same = (
        a1 * c2 == a2 * c1 and
        b1 * c2 == b2 * c1
    )

    if same:
        print(-1)
    else:
        print(0)
```

The first part computes the determinant of the coefficient matrix. This is the standard criterion for whether a `2 × 2` linear system has a unique solution.

If the determinant is nonzero, the answer is immediately `1`, because the lines intersect once.

The second branch handles the parallel case. Instead of dividing coefficients to compare ratios, the implementation uses integer multiplication. This matters because coefficients can be zero. For example, comparing `a1 / a2` becomes invalid when `a2 = 0`.

The proportionality checks are written as exact integer equalities, so there are no floating point precision issues. Since all values are tiny, overflow is not even remotely possible in Python, though the same method is also safe in C++ for these limits.

## Worked Examples

### Example 1

Input:

```
1 1 0
2 2 0
```

| Variable | Value |
| --- | --- |
| `a1, b1, c1` | `1, 1, 0` |
| `a2, b2, c2` | `2, 2, 0` |
| `det` | `1*2 - 2*1 = 0` |
| `a1*c2 == a2*c1` | `1*0 == 2*0` → `True` |
| `b1*c2 == b2*c1` | `1*0 == 2*0` → `True` |

The determinant is zero, so the lines are parallel or identical. Both proportionality checks succeed, meaning the second equation is exactly twice the first. The algorithm prints:

```
-1
```

This example demonstrates why checking only the determinant is insufficient.

### Example 2

Input:

```
1 -1 0
1 1 -4
```

| Variable | Value |
| --- | --- |
| `a1, b1, c1` | `1, -1, 0` |
| `a2, b2, c2` | `1, 1, -4` |
| `det` | `1*1 - 1*(-1) = 2` |

Since the determinant is nonzero, the lines intersect at exactly one point. The algorithm immediately prints:

```
1
```

This trace confirms that non-parallel lines always produce a unique intersection.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations are performed |
| Space | O(1) | No extra memory proportional to input size is used |

The constraints are extremely small, so even inefficient solutions would pass. This implementation still uses the mathematically clean constant-time approach and easily fits within all limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    a1, b1, c1 = map(int, input().split())
    a2, b2, c2 = map(int, input().split())

    det = a1 * b2 - a2 * b1

    if det != 0:
        print(1)
    else:
        same = (
            a1 * c2 == a2 * c1 and
            b1 * c2 == b2 * c1
        )

        if same:
            print(-1)
        else:
            print(0)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("1 1 0\n2 2 0\n") == "-1\n", "sample 1"

# intersecting lines
assert run("1 -1 0\n1 1 -4\n") == "1\n", "unique intersection"

# parallel but distinct
assert run("1 1 1\n2 2 3\n") == "0\n", "parallel lines"

# zero coefficients, same line
assert run("0 1 0\n0 2 0\n") == "-1\n", "horizontal line scaling"

# maximum magnitude coefficients
assert run("100 -100 50\n-100 -100 0\n") == "1\n", "boundary coefficients"

# vertical parallel lines
assert run("1 0 -1\n2 0 -3\n") == "0\n", "distinct vertical lines"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 0 / 2 2 0` | `-1` | Identical lines |
| `1 -1 0 / 1 1 -4` | `1` | Unique intersection |
| `1 1 1 / 2 2 3` | `0` | Parallel but different |
| `0 1 0 / 0 2 0` | `-1` | Zero coefficients handled safely |
| `100 -100 50 / -100 -100 0` | `1` | Boundary coefficient values |
| `1 0 -1 / 2 0 -3` | `0` | Vertical parallel lines |

## Edge Cases

Consider the case where both equations represent the same horizontal line:

```
0 1 0
0 2 0
```

The determinant becomes:

$$0 \cdot 2 - 0 \cdot 1 = 0$$

so the lines are parallel or identical. The proportionality checks give:

$$0 \cdot 0 = 0 \cdot 0$$

and

$$1 \cdot 0 = 2 \cdot 0$$

Both are true, so the algorithm prints `-1`. A division-based approach could easily fail here because `A_1 = A_2 = 0`.

Now examine distinct parallel lines:

```
1 1 1
2 2 3
```

The determinant is again zero:

$$1 \cdot 2 - 2 \cdot 1 = 0$$

but the proportionality check fails:

$$1 \cdot 3 \neq 2 \cdot 1$$

The algorithm correctly prints `0`. This distinguishes “same direction” from “same line”.

Finally, consider intersecting vertical and horizontal lines:

```
1 0 -2
0 1 -3
```

The determinant is:

$$1 \cdot 1 - 0 \cdot 0 = 1$$

Since it is nonzero, the algorithm immediately prints `1`. No special handling for vertical lines is needed because the determinant method works uniformly for every orientation.
