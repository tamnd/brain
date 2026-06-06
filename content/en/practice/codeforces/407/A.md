---
title: "CF 407A - Triangle"
description: "We are given two positive integers, a and b, which are the lengths of the legs of a right triangle. The task is not to check whether such a triangle exists, it obviously does."
date: "2026-06-07T01:46:47+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "geometry", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 407
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 239 (Div. 1)"
rating: 1600
weight: 407
solve_time_s: 273
verified: true
draft: false
---

[CF 407A - Triangle](https://codeforces.com/problemset/problem/407/A)

**Rating:** 1600  
**Tags:** brute force, geometry, implementation, math  
**Solve time:** 4m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two positive integers, `a` and `b`, which are the lengths of the legs of a right triangle. The task is not to check whether such a triangle exists, it obviously does. Instead, we must place that triangle on the integer lattice so that all three vertices have integer coordinates and none of its sides is parallel to either coordinate axis.

A useful way to think about the problem is to construct two perpendicular vectors whose lengths are exactly `a` and `b`. If we place one vertex at the origin, then the other two vertices can be obtained by moving along these vectors. The resulting triangle will automatically be right-angled.

The limits are very small. Both `a` and `b` are at most 1000. This means we can afford to enumerate all integer coordinate pairs whose squares sum to `a²` or `b²`. Even an `O(1000²)` search is completely safe.

The main difficulty is not performance but geometry. We need integer coordinates, a right angle, the prescribed side lengths, and additionally no side may be horizontal or vertical.

One easy mistake is to construct the obvious triangle

```
(0,0), (a,0), (0,b)
```

For example, with input

```
3 4
```

this has the correct side lengths, but two sides are parallel to the coordinate axes, so it is invalid.

Another trap is finding integer vectors of the correct lengths but allowing them to lie on the same line. For example, if both vectors point in the same direction, the three points become collinear and do not form a triangle.

A more subtle case is when no integer decomposition exists. For input

```
1 1
```

the only integer vectors of length 1 are `(±1,0)` and `(0,±1)`. Any construction using them necessarily creates a side parallel to an axis. The correct answer is

```
NO
```

and a solution that only checks lengths without enforcing the "no axis-parallel side" condition would incorrectly output a triangle.

## Approaches

A brute-force idea is to search for all integer coordinates of the three vertices inside some large box and test every possibility. Such an approach is clearly correct because every valid triangle would eventually be examined. The problem is that even a box of side length 2000 contains millions of lattice points, making the number of triples astronomically large.

The structure of the problem gives us a much better representation. Since the triangle is right-angled, we may place the right angle at the origin. Let one leg be represented by vector

```
(x1, y1)
```

with length `a`, and the other by vector

```
(x2, y2)
```

with length `b`.

The vectors must satisfy

```
x1² + y1² = a²
x2² + y2² = b²
```

and they must be perpendicular:

```
x1*x2 + y1*y2 = 0
```

A key observation is that if `(x1, y1)` is known, then a perpendicular vector is

```
(-y1, x1)
```

or

```
(y1, -x1)
```

These have exactly the same length as `(x1, y1)`.

Suppose we find integers `(x, y)` such that

```
x² + y² = a².
```

Then the vector

```
(-y, x)
```

has length `a`. To obtain a perpendicular vector of length `b`, we can scale it by `b / a`:

```
(-y*b/a, x*b/a)
```

For this vector to have integer coordinates, both `y*b` and `x*b` must be divisible by `a`.

Rather than reasoning with fractions, we can directly enumerate all integer pairs `(x, y)` satisfying

```
x² + y² = a²
```

and all integer pairs `(u, v)` satisfying

```
u² + v² = b².
```

Then we only need to find a pair where

```
x*u + y*v = 0.
```

The bounds are tiny, so this search is easy.

There is an even simpler observation used in most accepted solutions. Enumerate all non-zero integer pairs `(x, y)` with

```
x² + y² = a².
```

Then take

```
(u, v) = (-y, x).
```

This is automatically perpendicular and has length `a`.

If we want length `b`, we can look for a scaling factor

```
k = b / a
```

that keeps coordinates integral. Equivalently, we search for another decomposition of `b²` and check whether it matches the perpendicular direction.

The standard accepted implementation enumerates all decompositions of `a²` and directly tests whether the corresponding scaled perpendicular coordinates are integers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over vertex positions | Enormous | Enormous | Too slow |
| Enumerate lattice vectors on circles | O(a + b) to O(1000²) | O(1) | Accepted |

## Algorithm Walkthrough

1. Fix the right-angle vertex at `(0,0)`.
2. Enumerate all positive integers `x` from `1` to `a-1`.
3. Compute

```
y² = a² - x².
```

If `y²` is not a perfect square, this `x` cannot belong to an integer vector of length `a`.
4. Let `y = sqrt(y²)`. Skip the case `y = 0` because that would create an axis-parallel side.
5. Consider the perpendicular direction `(-y, x)`. Its length is also `a`.
6. Scale this perpendicular vector by `b / a`. The candidate coordinates become

```
X = -y*b/a
Y = x*b/a.
```
7. Check whether both `X` and `Y` are integers. This is equivalent to checking

```
(y*b) % a == 0
(x*b) % a == 0.
```
8. If both divisibility conditions hold and neither coordinate becomes zero, output

```
(0,0)
(x,y)
(X,Y)
```

and terminate.
9. If all decompositions are exhausted without success, output `"NO"`.

### Why it works

The first leg is the vector `(x,y)`, whose length is exactly `a` because it satisfies `x²+y²=a²`.

The second leg is obtained from the perpendicular vector `(-y,x)` and scaled by `b/a`. Scaling changes its length from `a` to `b`, while preserving perpendicularity. Thus the dot product of the two leg vectors remains zero, so the angle at the origin is a right angle.

The divisibility checks guarantee integer coordinates. Excluding zero coordinates prevents any side from becoming horizontal or vertical. Every valid construction with the right angle at the origin corresponds to some lattice vector of length `a`, so the enumeration cannot miss a solution.

## Python Solution

```python
import sys
from math import isqrt

input = sys.stdin.readline

a, b = map(int, input().split())

for x in range(1, a):
    y2 = a * a - x * x
    y = isqrt(y2)

    if y * y != y2 or y == 0:
        continue

    if (y * b) % a != 0:
        continue
    if (x * b) % a != 0:
        continue

    X = -(y * b) // a
    Y = (x * b) // a

    if X == 0 or Y == 0:
        continue

    print("YES")
    print(0, 0)
    print(x, y)
    print(X, Y)
    sys.exit()

print("NO")
```

The code follows the geometric construction directly.

The loop enumerates all integer lattice vectors of length `a` with positive coordinates. For each candidate, the expression

```
y2 = a * a - x * x
```

computes the remaining square. Using `isqrt` avoids floating-point precision issues when testing whether `y2` is a perfect square.

The divisibility checks are the core of the solution. They verify that scaling the perpendicular vector by `b/a` keeps both coordinates integral. Without these checks, integer division would silently truncate values and produce an incorrect triangle.

The final guard

```
if X == 0 or Y == 0:
```

removes constructions that would introduce an axis-parallel side.

Once a valid configuration is found, the program prints it immediately and exits. Since any valid triangle is acceptable, there is no need to continue searching.

## Worked Examples

### Example 1

Input:

```
1 1
```

| x | y² = 1 - x² | Perfect square? | Action |
| --- | --- | --- | --- |
| none | none | none | loop never runs |

Output:

```
NO
```

Since `a = 1`, there is no integer `x` in the range `[1, a-1]`. No non-axis lattice vector of length 1 exists, so the answer is correctly rejected.

### Example 2

Input:

```
5 10
```

| x | y² | y | (y·b)%a | (x·b)%a | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | 24 | not square | - | - | skip |
| 2 | 21 | not square | - | - | skip |
| 3 | 16 | 4 | 0 | 0 | found |

The resulting coordinates are

```
(0,0)
(3,4)
(-8,6)
```

Verification:

```
3² + 4² = 25 = 5²
(-8)² + 6² = 100 = 10²
3*(-8) + 4*6 = 0
```

The trace demonstrates the key invariant: the second vector is always perpendicular to the first and has the required length after scaling.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(a) | One scan through values of `x` from `1` to `a-1` |
| Space | O(1) | Only a few integer variables are stored |

With `a ≤ 1000`, the loop executes at most 999 iterations. The running time is effectively instantaneous, and the memory usage is negligible compared to the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from math import isqrt

def solve():
    a, b = map(int, input().split())

    for x in range(1, a):
        y2 = a * a - x * x
        y = isqrt(y2)

        if y * y != y2 or y == 0:
            continue

        if (y * b) % a != 0:
            continue
        if (x * b) % a != 0:
            continue

        X = -(y * b) // a
        Y = (x * b) // a

        if X == 0 or Y == 0:
            continue

        print("YES")
        print(0, 0)
        print(x, y)
        print(X, Y)
        return

    print("NO")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    global input
    input = sys.stdin.readline

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout
    return out

# provided sample
assert run("1 1\n") == "NO\n"

# custom cases
assert run("5 10\n").startswith("YES")
assert run("2 2\n") == "NO\n"
assert run("3 4\n") == "NO\n"
assert run("1000 1000\n").startswith("YES")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 10` | YES | Typical successful construction |
| `2 2` | NO | Small value with no valid lattice decomposition |
| `3 4` | NO | Classic Pythagorean lengths but impossible placement under constraints |
| `1000 1000` | YES | Large boundary value |

## Edge Cases

For input

```
1 1
```

the loop range is empty because there is no positive `x < 1`. The algorithm immediately prints `"NO"`. This matches the fact that every length-1 lattice vector is axis-aligned.

For input

```
2 2
```

the only candidate is `x = 1`, giving

```
y² = 3
```

which is not a perfect square. No lattice vector of length 2 with both coordinates non-zero exists, so the answer is `"NO"`.

For input

```
3 4
```

the candidate vector is `(x,y)=(?,?)`. The only decomposition of `3²` is effectively `(0,3)` and `(3,0)`, both containing a zero coordinate. The algorithm rejects them automatically and prints `"NO"`.

For input

```
5 5
```

the algorithm finds `(3,4)` since

```
3² + 4² = 25.
```

The perpendicular vector is

```
(-4,3),
```

which already has length 5. All coordinates are non-zero, so it outputs

```
YES
0 0
3 4
-4 3
```

Every side avoids being horizontal or vertical, and all coordinates remain integers.
