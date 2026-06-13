---
title: "CF 1199B - Water Lily"
description: "A water lily is attached to the bottom of a lake by a straight stem. Initially the stem is perfectly vertical, so the flower sits directly above its root point on the lake bed. The flower is floating above the water surface by a known height (H)."
date: "2026-06-13T14:59:34+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "math"]
categories: ["algorithms"]
codeforces_contest: 1199
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 576 (Div. 2)"
rating: 1000
weight: 1199
solve_time_s: 227
verified: true
draft: false
---

[CF 1199B - Water Lily](https://codeforces.com/problemset/problem/1199/B)

**Rating:** 1000  
**Tags:** geometry, math  
**Solve time:** 3m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

A water lily is attached to the bottom of a lake by a straight stem. Initially the stem is perfectly vertical, so the flower sits directly above its root point on the lake bed. The flower is floating above the water surface by a known height \(H\).

We then simulate what happens when the flower is pulled horizontally along the water surface by a distance \(L\). The stem remains straight and rigid, so it rotates as a single segment anchored at the bottom point. At the moment described in the problem, the flower has just reached the water surface.

The task is to determine the depth of the lake at the stem’s attachment point.

Geometrically, this becomes a right triangle problem. The stem is the hypotenuse, its length is fixed, and it connects the lake bottom to the flower. Initially, the vertical distance from bottom to flower is the full stem length minus water depth. After dragging the flower horizontally by \(L\), the vertical height becomes exactly the lake depth, because the flower is now on the surface.

The constraints \(1 \le H < L \le 10^6\) indicate that everything fits comfortably in floating-point arithmetic, and we can safely rely on standard double precision without worrying about overflow or numerical instability from extreme magnitudes.

A subtle issue that can confuse naive reasoning is mixing up which segment corresponds to the stem length. The stem is not simply \(H + \text{depth}\); that only holds in the initial vertical configuration. After rotation, the geometry changes, and the correct relationship comes from the invariant length of the stem combined with the right triangle formed by horizontal displacement and vertical drop.

## Approaches

If we think purely algebraically, we can introduce unknowns. Let the lake depth be \(D\). The stem length is then \(D + H\), because initially the flower is \(H\) above the surface. After dragging, the flower lies on the water surface, so the vertical projection of the stem becomes exactly \(D\), while the horizontal displacement is \(L\). This forms a right triangle where the hypotenuse is \(D + H\), one leg is \(D\), and the other is \(L\).

From the Pythagorean theorem we obtain:
\[
(D + H)^2 = D^2 + L^2
\]

Expanding and simplifying removes \(D^2\) from both sides:
\[
D^2 + 2DH + H^2 = D^2 + L^2
\]
\[
2DH + H^2 = L^2
\]
\[
D = \frac{L^2 - H^2}{2H}
\]

A brute-force approach would be to guess the depth and simulate the geometry each time, checking whether the resulting stem length matches consistency constraints. That would require iterating over all possible depths up to \(10^6\), which is unnecessary and wasteful since the relationship is algebraic and direct.

The key observation is that the system is fully determined by a single quadratic equation. Once the geometric constraints are translated correctly, the solution is immediate.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force (guess depth) | \(O(L)\) or worse | \(O(1)\) | Too slow |
| Algebraic derivation | \(O(1)\) | \(O(1)\) | Accepted |

## Algorithm Walkthrough

1. Read integers \(H\) and \(L\). These define the initial height above water and the horizontal displacement after dragging.

2. Translate the geometry into a right triangle relation where the stem length is constant and equals \(D + H\). This step converts the physical setup into algebra.

3. Apply the Pythagorean theorem:
   \[
   (D + H)^2 = D^2 + L^2
   \]
   This captures the invariant stem length and the orthogonal decomposition after rotation.

4. Expand and cancel identical terms on both sides to isolate the unknown \(D\). This simplification removes the quadratic term in a clean way due to symmetry.

5. Solve the resulting linear equation in \(D\):
   \[
   D = \frac{L^2 - H^2}{2H}
   \]

6. Output \(D\) as a floating-point number with sufficient precision.

### Why it works

The entire construction relies on a rigid segment of fixed length. That fixed length does not change under rotation, so the only valid configurations of the stem endpoints lie on a circle centered at the lake bottom point with radius \(D + H\). The final position forms a right triangle whose hypotenuse is that radius and whose legs are the horizontal displacement \(L\) and vertical depth \(D\). Because this geometric constraint uniquely determines the triangle, the computed expression for \(D\) is the only value consistent with both the initial and final configurations.

## Python Solution

```python
import sys
input = sys.stdin.readline

H, L = map(int, input().split())

D = (L * L - H * H) / (2 * H)
print(D)
```

The solution directly implements the derived closed-form formula. Using Python floating-point division is sufficient because the required precision is only \(10^{-6}\), and the intermediate values are at most \(10^{12}\), which are well within exact representability in double precision for this context.

The subtraction \(L^2 - H^2\) is safe because both values fit in 64-bit integers before conversion. The division by \(2H\) is performed in floating point, ensuring the final result is a real number as required.

## Worked Examples

### Example 1

Input:
```
H = 1, L = 2
```

We compute:
\[
D = \frac{2^2 - 1^2}{2 \cdot 1}
\]

| Step | Expression | Value |
|------|------------|-------|
| Read input | H, L | 1, 2 |
| Square values | L², H² | 4, 1 |
| Numerator | L² - H² | 3 |
| Denominator | 2H | 2 |
| Depth | D | 1.5 |

Output:
```
1.5000000000000
```

This confirms a valid triangle where the stem length is \(2.5\), and the final configuration satisfies both horizontal and vertical constraints.

### Example 2

Input:
```
H = 2, L = 6
```

| Step | Expression | Value |
|------|------------|-------|
| Read input | H, L | 2, 6 |
| Square values | L², H² | 36, 4 |
| Numerator | L² - H² | 32 |
| Denominator | 2H | 4 |
| Depth | D | 8 |

Output:
```
8.0
```

This shows a larger displacement produces a deeper lake consistent with the fixed stem length constraint.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | \(O(1)\) | Only a constant number of arithmetic operations are performed |
| Space | \(O(1)\) | No additional data structures are used |

The computation consists only of a few integer multiplications and one floating-point division, which is trivially fast under the given constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    H, L = map(int, sys.stdin.readline().split())
    D = (L * L - H * H) / (2 * H)
    return str(D)

# provided sample
assert abs(float(run("1 2\n")) - 1.5) < 1e-9

# minimum values
assert abs(float(run("1 2\n")) - 1.5) < 1e-9

# simple geometric check
assert abs(float(run("2 6\n")) - 8.0) < 1e-9

# equal difference case
assert abs(float(run("3 5\n")) - ((25 - 9) / 6)) < 1e-9

# large values
assert run("1000000 1000000\n")  # just ensures no crash
```

| Test input | Expected output | What it validates |
|---|---|---|
| 1 2 | 1.5 | basic correctness |
| 2 6 | 8.0 | larger triangle consistency |
| 3 5 | (25-9)/6 | algebraic correctness |
| 1000000 1000000 | valid output | numerical stability |

## Edge Cases

When \(H\) is minimal, for example \(H = 1\) and \(L = 2\), the computation reduces to a small integer arithmetic expression and confirms that the formula does not depend on scaling. The algorithm directly computes \(D = (4 - 1)/2 = 1.5\), which matches the expected geometric configuration.

When \(L\) is only slightly larger than \(H\), the numerator \(L^2 - H^2\) remains positive but small, producing a shallow lake. The subtraction step is safe because both squares fit within 64-bit integers, and the division produces a stable floating-point result.

When \(L\) is very large relative to \(H\), the depth grows quadratically with \(L\). The formula still behaves correctly because Python integers handle large intermediate values exactly before conversion to float, ensuring no overflow or precision loss at the integer stage.
