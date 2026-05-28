---
title: "CF 100I - Rotation"
description: "We are given a point $(x, y)$ on the 2D plane and an angle $k$ in degrees. The task is to rotate the point counter-clockwise around the origin by exactly $k$ degrees and print the coordinates of the new point."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "geometry", "math"]
categories: ["algorithms"]
codeforces_contest: 100
codeforces_index: "I"
codeforces_contest_name: "Unknown Language Round 3"
rating: 1500
weight: 100
solve_time_s: 261
verified: true
draft: false
---

[CF 100I - Rotation](https://codeforces.com/problemset/problem/100/I)

**Rating:** 1500  
**Tags:** *special, geometry, math  
**Solve time:** 4m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a point $(x, y)$ on the 2D plane and an angle $k$ in degrees. The task is to rotate the point counter-clockwise around the origin by exactly $k$ degrees and print the coordinates of the new point.

A rotation around the origin preserves the distance from the origin while changing the direction of the vector. Geometrically, this is the standard 2D rotation transformation.

The constraints are extremely small. The coordinates are bounded by only 1390 in absolute value, and there is only one point to process. Time complexity is effectively irrelevant here because even a mathematically heavy solution runs instantly. The real challenge is implementing the geometry formula correctly and handling floating-point precision carefully enough to satisfy the error bound.

The required relative error is less than $10^{-1}$, which is very forgiving. Standard double precision floating-point arithmetic is more than sufficient.

Several edge cases can silently break a careless implementation.

Rotating by 0 degrees should return the original point unchanged.

Input:

```
0
5 -3
```

Correct output:

```
5.00000000 -3.00000000
```

A buggy implementation might accidentally convert degrees incorrectly or apply clockwise rotation instead of counter-clockwise rotation.

Rotating by 90 degrees is another classic trap because the coordinates swap positions and one sign changes.

Input:

```
90
1 1
```

Correct output:

```
-1.00000000 1.00000000
```

If the rotation matrix is written incorrectly, the output may become `(1, -1)` or `(-1, -1)`.

Negative coordinates are also important because sign mistakes become obvious there.

Input:

```
180
-2 7
```

Correct output:

```
2.00000000 -7.00000000
```

A wrong angle conversion or incorrect sine/cosine placement often produces mirrored results instead of true rotation.

## Approaches

The brute-force way to think about this problem is geometric simulation. One could repeatedly apply tiny rotations until the total angle reaches $k$ degrees. Since a rotation is just a transformation of coordinates, repeatedly multiplying by small-angle matrices eventually reaches the target orientation.

This idea is mathematically correct because rotations compose cleanly. Applying a 1-degree rotation ninety times produces the same result as a single 90-degree rotation.

The problem is that repeated floating-point operations accumulate numerical error unnecessarily. Even though the constraints are tiny enough that this would still run quickly, it is inefficient and much less accurate than needed. If we simulated one degree at a time, the worst case would involve 359 matrix multiplications for no real benefit.

The key observation is that rotation in 2D already has a direct closed-form formula. If a point $(x, y)$ is rotated counter-clockwise by angle $\theta$, the new coordinates are:

$\begin{aligned}x' &= x\cos\theta - y\sin\theta \\ y' &= x\sin\theta + y\cos\theta\end{aligned}$

This comes directly from the geometry of the unit circle and the rotation matrix. Since Python's trigonometric functions operate on radians, we first convert degrees to radians.

The optimal solution is simply evaluating these two formulas once. That gives constant time complexity and avoids cumulative floating-point drift.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k) | O(1) | Unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the rotation angle `k` and the point coordinates `x` and `y`.
2. Convert the angle from degrees to radians because Python's `math.sin` and `math.cos` functions expect radians.

The conversion formula is:

$\theta = k \cdot \frac{\pi}{180}$

1. Compute `cos(theta)` and `sin(theta)` once.

Computing them once avoids duplicate work and keeps the code cleaner.

1. Apply the 2D rotation formulas:

$$x' = x \cos\theta - y \sin\theta$$

$$y' = x \sin\theta + y \cos\theta$$

These formulas come from multiplying the point vector by the standard rotation matrix.

1. Print the resulting coordinates using floating-point formatting.

The judge allows small floating-point error, so standard decimal formatting is sufficient.

### Why it works

A counter-clockwise rotation by angle $\theta$ is represented by the matrix:

$\begin{bmatrix}\cos\theta & -\sin\theta \\ \sin\theta & \cos\theta\end{bmatrix}$

Multiplying this matrix by the vector $(x, y)$ produces the exact coordinates of the rotated point. Since matrix rotation preserves distances and angles, the transformed point is precisely the original point rotated around the origin.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

# solution

k = int(input())
x, y = map(int, input().split())

theta = math.radians(k)

c = math.cos(theta)
s = math.sin(theta)

nx = x * c - y * s
ny = x * s + y * c

print(f"{nx:.8f} {ny:.8f}")
```

The program starts by reading the angle and coordinates. The angle is converted into radians using `math.radians`, which avoids manual conversion mistakes.

The variables `c` and `s` store the cosine and sine values of the angle. Computing them once is cleaner and slightly more efficient.

The formulas for `nx` and `ny` directly implement the rotation matrix multiplication. The order matters. A common bug is mixing the signs or swapping sine and cosine terms.

The output uses fixed decimal formatting with 8 digits after the decimal point. The problem only requires a small relative error, so this is comfortably accurate.

## Worked Examples

### Example 1

Input:

```
90
1 1
```

| Step | Value |
| --- | --- |
| k | 90 |
| theta | $\pi / 2$ |
| cos(theta) | 0 |
| sin(theta) | 1 |
| nx | $1 \cdot 0 - 1 \cdot 1 = -1$ |
| ny | $1 \cdot 1 + 1 \cdot 0 = 1$ |

Output:

```
-1.00000000 1.00000000
```

This trace demonstrates the classic 90-degree rotation. The point `(1,1)` moves to `(-1,1)` exactly as expected for counter-clockwise motion.

### Example 2

Input:

```
180
2 -3
```

| Step | Value |
| --- | --- |
| k | 180 |
| theta | $\pi$ |
| cos(theta) | -1 |
| sin(theta) | 0 |
| nx | $2 \cdot (-1) - (-3) \cdot 0 = -2$ |
| ny | $2 \cdot 0 + (-3) \cdot (-1) = 3$ |

Output:

```
-2.00000000 3.00000000
```

A 180-degree rotation flips the point to the opposite side of the origin. This example confirms that the signs are handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic and trigonometric operations are performed |
| Space | O(1) | No extra data structures are used |

The solution easily fits within the limits. Only one point is processed, and all operations are constant time.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
import math

def solve():
    input = sys.stdin.readline

    k = int(input())
    x, y = map(int, input().split())

    theta = math.radians(k)

    c = math.cos(theta)
    s = math.sin(theta)

    nx = x * c - y * s
    ny = x * s + y * c

    print(f"{nx:.8f} {ny:.8f}")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.strip()

# provided sample
assert run("90\n1 1\n") == "-1.00000000 1.00000000", "sample 1"

# zero rotation
assert run("0\n5 -3\n") == "5.00000000 -3.00000000", "zero rotation"

# 180 degree rotation
assert run("180\n2 -3\n") == "-2.00000000 3.00000000", "180 degrees"

# point at origin
assert run("270\n0 0\n") == "0.00000000 -0.00000000", "origin"

# maximum coordinate magnitude
out = run("90\n1390 -1390\n")
assert out.startswith("1390.00000000"), "large coordinates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 / 5 -3` | `5.00000000 -3.00000000` | Identity rotation |
| `180 / 2 -3` | `-2.00000000 3.00000000` | Sign correctness |
| `270 / 0 0` | `0.00000000 -0.00000000` | Origin remains fixed |
| `90 / 1390 -1390` | approximately `1390 1390` | Large coordinate handling |

## Edge Cases

A rotation by 0 degrees should leave the point unchanged.

Input:

```
0
5 -3
```

The algorithm converts 0 degrees into 0 radians. Since:

$$\cos(0)=1$$

and

$$\sin(0)=0$$

the formulas become:

$$x' = 5 \cdot 1 - (-3)\cdot 0 = 5$$

$$y' = 5 \cdot 0 + (-3)\cdot 1 = -3$$

The output remains identical to the input point.

A 90-degree rotation is sensitive to sign errors.

Input:

```
90
1 1
```

The algorithm computes:

$$\cos(90^\circ)=0$$

$$\sin(90^\circ)=1$$

Then:

$$x' = 1\cdot0 - 1\cdot1 = -1$$

$$y' = 1\cdot1 + 1\cdot0 = 1$$

This confirms the rotation is counter-clockwise rather than clockwise.

The origin is another useful boundary case.

Input:

```
270
0 0
```

Regardless of the angle:

$$x' = 0$$

$$y' = 0$$

The algorithm correctly preserves the origin because every term in the formulas becomes zero.
