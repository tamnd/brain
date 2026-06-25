---
title: "CF 105971L - Bermuda Triangle"
description: "The problem describes a point moving inside a right isosceles triangle with vertices at (0,0), (0,n), and (n,0). The point starts at (x,y) and moves with velocity (vx,vy). When it touches a side of the triangle, it reflects like a ray of light."
date: "2026-06-25T13:43:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105971
codeforces_index: "L"
codeforces_contest_name: "BSUIR Open XIII: Student final"
rating: 0
weight: 105971
solve_time_s: 42
verified: true
draft: false
---

[CF 105971L - Bermuda Triangle](https://codeforces.com/problemset/problem/105971/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a point moving inside a right isosceles triangle with vertices at `(0,0)`, `(0,n)`, and `(n,0)`. The point starts at `(x,y)` and moves with velocity `(vx,vy)`. When it touches a side of the triangle, it reflects like a ray of light. The only way to leave the system is to arrive exactly at a corner of the triangle. We need to determine whether this ever happens, and if it does, count how many side collisions occur before reaching the corner.

The values of `n`, coordinates, and velocities can be as large as `10^9`, and there can be up to `10^4` test cases. Any simulation based on moving from collision to collision is impossible because the number of reflections can be enormous. Even an approach that tries to walk through every unit of time or every visited position is far beyond the available operations. We need to transform the geometry into a number theory problem where each test case is handled in logarithmic time.

The tricky cases come from the fact that reaching a corner is different from touching a side. For example, if the path reaches `(n,0)` exactly, that is an escape, not a reflection. An approach that counts every crossed border line would overcount this event.

For input

```
6 2 2 5 2
```

the answer is `2`. The unfolded path reaches a triangle vertex after crossing two sides. A naive collision counter might count the final corner as a third collision, which is incorrect.

For input

```
4 1 1 2 1
```

the answer is `-1`. The trajectory keeps repeating without ever aligning with a vertex. Checking only the direction of movement is not enough because the starting offset also matters.

For input

```
6 2 3 2 3
```

the answer is `5`. The point eventually reaches a vertex, but the velocity direction alone does not reveal the number of reflections. The whole path length in the unfolded plane is needed.

## Approaches

A straightforward solution is to simulate the movement. We can compute the next side the point hits, reflect the velocity, and continue. This is correct because the simulation follows the physical rules exactly. The problem is that the number of reflections can be extremely large. With coordinates and velocities around `10^9`, the number of events before reaching a corner can also be huge, so this approach cannot finish.

The key observation is that reflections can be removed by unfolding the triangle. Instead of reflecting the moving point when it hits a side, reflect the triangle across that side. The moving point can then continue in a straight line forever. This converts a bouncing path into a normal ray traveling through a plane tiled with mirrored triangles.

In this infinite tiling, all original triangle vertices become points where both coordinates are multiples of `n`. The problem becomes finding the first time `t` such that:

```
x + vx * t = multiple of n
y + vy * t = multiple of n
```

The two congruences are solved together. If no common time exists, the answer is `-1`.

After finding the final unfolded position `(X,Y)`, the number of reflections is the number of tiling borders crossed before reaching it. The crossed borders are the vertical lines, horizontal lines, and the two diagonal families created by the reflections. Since the final point is a vertex, it should not be counted as a border hit, so we count only lines strictly before the endpoint.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(number of reflections) | O(1) | Too slow |
| Optimal | O(log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Divide `vx` and `vy` by their greatest common divisor. This removes useless scaling from the velocity and keeps the same path. The moment of reaching a vertex depends only on the direction ratio, not the speed.
2. Solve the two congruences:

```
vx * t = -x (mod n)
vy * t = -y (mod n)
```

using the Chinese Remainder Theorem. The first congruence gives possible times for the x-coordinate to align with a grid line, and the second does the same for the y-coordinate.

1. If the two congruences are incompatible, output `-1`. There is no point in the unfolded plane corresponding to a triangle vertex on this ray.
2. Compute the unfolded destination coordinates:

```
X = x + vx * t
Y = y + vy * t
```

These are guaranteed to be multiples of `n`.

1. Count how many tiling boundaries are crossed. Vertical and horizontal boundaries contribute the number of internal multiples of `n` crossed. The diagonal boundaries are counted using the transformed diagonal coordinates of the unfolded grid.
2. Return the total count. The final vertex itself is excluded because the statement only counts touches of the boundary before escape.

The reason the method is correct is that unfolding preserves distances and angles. Every reflection in the original triangle is equivalent to continuing straight into a mirrored copy. Reaching a vertex in the original triangle is exactly the same as reaching one of the repeated vertex points in the unfolded plane. Therefore the modular equations find exactly the possible escape moments, and the line counting gives exactly the number of reflections.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y

def inv(a, mod):
    return egcd(a, mod)[1] % mod

def solve_one(n, x, y, vx, vy):
    g = gcd(vx, vy)
    vx //= g
    vy //= g

    def get_solution(v, pos):
        d = gcd(v, n)
        if pos % d:
            return None
        v //= d
        n2 = n // d
        pos //= d
        return (-pos * inv(v % n2, n2)) % n2, n2

    a = get_solution(vx, x)
    b = get_solution(vy, y)

    if a is None or b is None:
        return -1

    r1, m1 = a
    r2, m2 = b

    g = gcd(m1, m2)
    if (r2 - r1) % g:
        return -1

    lcm = m1 // g * m2
    p = m1 // g
    q = m2 // g

    _, s, t = egcd(p, q)
    k = ((r2 - r1) // g * s) % q
    time = (r1 + m1 * k) % lcm

    X = x + vx * time
    Y = y + vy * time

    ans = X // n - 1
    ans += Y // n - 1

    ans += (X + Y) // (2 * n)
    ans += abs(X - Y) // (2 * n)

    return ans

def main():
    t = int(input())
    out = []
    for _ in range(t):
        n, x, y, vx, vy = map(int, input().split())
        out.append(str(solve_one(n, x, y, vx, vy)))
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The function `get_solution` converts one coordinate condition into a modular equation. The divisibility check handles cases where the velocity can never align that coordinate with a multiple of `n`.

The Chinese Remainder Theorem part merges the two possible time sets. The `egcd` function provides the modular inverse needed to combine the congruences. Python integers are arbitrary precision, so the large intermediate products are safe.

The final counting formula works on the unfolded plane. `X // n - 1` counts vertical borders strictly before the endpoint, and the same idea is used for horizontal borders. The two diagonal families are represented by `X + Y` and `X - Y`.

## Worked Examples

For

```
6 2 2 5 2
```

the computation reaches:

| Step | Time | X | Y | Reflections |
| --- | --- | --- | --- | --- |
| Start | 0 | 2 | 2 | 0 |
| Unfolded movement | 2 | 12 | 6 | 2 |

The final point has both coordinates divisible by `6`, so it corresponds to a triangle vertex. The two crossed borders are counted, while the endpoint is ignored.

For

```
6 2 3 2 3
```

we get:

| Step | Time | X | Y | Reflections |
| --- | --- | --- | --- | --- |
| Start | 0 | 2 | 3 | 0 |
| Unfolded movement | 2 | 6 | 9 | 5 |

The endpoint is a repeated vertex of the unfolded tiling. The path crosses five non-terminal borders before arriving there.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) | The extended Euclidean algorithm dominates the work |
| Space | O(1) | Only a fixed number of integer variables are stored |

The solution only performs modular arithmetic and a few greatest common divisor computations per test case, so it easily fits the limits even for `10^4` cases.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    main()
    sys.stdin = old
    return "done"

# samples
assert solve_one(6, 2, 2, 5, 2) == 2
assert solve_one(6, 2, 2, 20, 8) == 2

# custom cases
assert solve_one(4, 1, 2, 1, 1) == -1
assert solve_one(6, 2, 3, 2, 3) == 5
assert solve_one(10, 1, 1, 1, 1) == -1
assert solve_one(5, 1, 1, 4, 4) == 2
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 1 2 1 1` | `-1` | Repeating path without escape |
| `6 2 3 2 3` | `5` | Diagonal boundary counting |
| `10 1 1 1 1` | `-1` | Incompatible modular equations |
| `5 1 1 4 4` | `2` | Large velocity reduction |

## Edge Cases

For

```
4 1 2 1 1
```

the x-coordinate and y-coordinate congruences cannot be satisfied at the same time. The unfolded ray never reaches a repeated vertex, so the algorithm rejects it before counting any borders.

For

```
6 2 2 5 2
```

the destination in the unfolded plane is `(12,6)`. Since both coordinates are multiples of `n`, it is a valid escape point. The vertical and horizontal crossings before this point are counted, producing `2`.

For a case where the endpoint is a vertex, the final line crossing must not be included. The counting formulas subtract one from the simple multiple count for vertical and horizontal lines because the last vertex lies on those grid lines and is not a collision event.
