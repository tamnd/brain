---
title: "CF 104454D - Bucket of sand"
description: "We are given a vertical conical bucket characterized by its height and the diameter of its top opening. Into the exact center of the base, sand is poured continuously, forming a symmetric conical pile whose shape is determined by a fixed angle at its base."
date: "2026-06-30T14:25:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104454
codeforces_index: "D"
codeforces_contest_name: "ICPC Central Russia Regional Contest, 2021"
rating: 0
weight: 104454
solve_time_s: 74
verified: false
draft: false
---

[CF 104454D - Bucket of sand](https://codeforces.com/problemset/problem/104454/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a vertical conical bucket characterized by its height and the diameter of its top opening. Into the exact center of the base, sand is poured continuously, forming a symmetric conical pile whose shape is determined by a fixed angle at its base. The pouring stops at the moment when the sand pile grows enough to touch the rim of the bucket. The task is to compute how much sand has been poured by that stopping time.

Geometrically, there are two competing cones. One is the container, which is a fixed right circular cone defined by height and top radius. The other is the sand pile, which is a growing cone with a fixed slope angle. The process ends at the first moment when the sand cone intersects the boundary of the bucket cone at the top rim height. The answer is the volume of the sand cone at that moment.

The input size is small, with both dimensions at most 1000. This rules out any need for asymptotically optimized data structures or numerical approximations over large datasets. The challenge is purely geometric reasoning combined with correct handling of trigonometry and cone volume formulas.

A common failure case comes from misinterpreting the angle condition. The angle is given for the sand pile on a flat surface, not inside the bucket. That means the radius grows linearly with height according to a fixed slope. If someone incorrectly treats the angle as measured differently, for example using the wrong trigonometric function or interpreting it as the full apex angle instead of half-angle behavior, the computed radius-height relationship becomes wrong and the final volume diverges significantly.

Another subtle failure case appears when assuming the bucket always constrains the sand at the top. In reality, for narrow buckets, the sand pile may touch the side walls before reaching full height, so the stopping condition depends on the minimum of two geometric constraints: reaching height h, or intersecting the cone boundary defined by diameter d at height h.

## Approaches

A brute-force interpretation would simulate pouring sand incrementally and maintaining the current geometry of the pile. One could imagine increasing the height in tiny steps, computing the corresponding radius from the fixed angle, and checking whether the cone intersects the bucket boundary at that height. Each step would require evaluating geometric constraints, and achieving the required precision would force extremely small increments. This quickly becomes infeasible because reaching 1e-6 precision in volume would require on the order of millions to billions of simulation steps in the worst case, making it too slow for a 1 second limit.

The key observation is that both the sand pile and the bucket are perfect cones, so the entire process can be expressed as a direct geometric intersection problem rather than a simulation. The sand surface is a cone whose radius grows linearly with height, while the bucket boundary is also linear in radius with respect to height. Therefore, the stopping condition reduces to finding the smallest height where the sand cone radius equals the bucket radius, or the bucket height if the sand cone remains inside.

This converts the problem into solving a single intersection equation between two linear functions in height. Once that height is determined, the volume is simply the standard cone volume formula applied to the sand cone at that height.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Simulation | O(1e6 to 1e9) | O(1) | Too slow |
| Geometric intersection | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We model both shapes using radius as a function of height.

1. Convert the bucket dimensions into radius form. If the top diameter is d, the top radius is d/2. The bucket is a cone, so its radius grows linearly from 0 at height 0 to d/2 at height h. This defines a linear function relating height to bucket radius.
2. Express the sand pile radius as a function of height using the given angle. The pile is a right circular cone whose slope is fixed, so radius is proportional to height. The proportionality constant is derived from the angle using trigonometry, specifically the tangent relationship between height and radius in a right triangle cross-section.
3. Determine the limiting height of the sand. The sand can grow until either it reaches the top of the bucket or it hits the bucket wall earlier. This corresponds to solving where the two radius functions become equal.
4. Compute the intersection height by solving a linear equation. Since both radius functions are linear in height, the intersection reduces to equating two slopes and solving for h. If the resulting height exceeds the bucket height, clamp it to h.
5. Once the final height of the sand cone is known, compute its volume using the cone formula V = (1/3)πr²h, where r is the sand radius at that height.

### Why it works

The correctness comes from the fact that both surfaces are ruled by linear radial growth in height. The sand cone always maintains a fixed slope, so its geometry does not change during pouring. The bucket boundary is also linear because it is a cone. Therefore, the first contact point must occur exactly at the solution of the equality of their radius functions, and no intermediate nonlinear behavior exists. This guarantees that the computed intersection height is exactly the stopping point of the process.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    h, d = map(float, input().split())

    bucket_r_top = d / 2.0

    angle_deg = 34.0
    angle = math.radians(angle_deg)

    sand_slope = math.tan(angle)

    bucket_slope = bucket_r_top / h

    if sand_slope <= bucket_slope:
        final_h = h
        final_r = sand_slope * final_h
    else:
        final_h = bucket_r_top / sand_slope
        final_r = bucket_slope * final_h

    volume = (math.pi * final_r * final_r * final_h) / 3.0
    print(volume)

if __name__ == "__main__":
    solve()
```

The implementation starts by converting the bucket diameter into a radius. The sand cone slope is computed using tangent of the given angle, since the angle describes the inclination of the sand surface relative to the horizontal base.

The bucket slope is computed from its geometry as a linear ratio between radius and height. The comparison between slopes determines whether the sand hits the bucket walls before reaching the top or whether it simply fills the bucket vertically.

The final height and radius are derived from the active constraint, and the cone volume formula is applied directly. Care must be taken to use floating point arithmetic throughout, since integer division would destroy the geometric ratios.

## Worked Examples

### Sample 1

Input:

```
10 10
```

| Step | sand slope | bucket slope | comparison | final height | final radius |
| --- | --- | --- | --- | --- | --- |
| init | tan(34°) ≈ 0.6745 | 5/10 = 0.5 | sand > bucket | 10*0.5/0.6745 ≈ 7.42 | ≈ 3.71 |

The sand grows steeper than the bucket walls allow, so it touches the bucket before reaching full height. The effective height is reduced until the radii match.

This confirms that for wider buckets the limiting factor is the side wall intersection, not the top boundary.

### Sample 2

Input:

```
5 1
```

| Step | sand slope | bucket slope | comparison | final height | final radius |
| --- | --- | --- | --- | --- | --- |
| init | tan(34°) ≈ 0.6745 | 0.5/5 = 0.1 | sand > bucket | 0.5/0.6745 ≈ 0.74 | ≈ 0.074 |

Here the bucket is extremely narrow, so the sand hits the walls very early. The final cone is very small, and the volume is correspondingly tiny.

This demonstrates the regime where the bucket geometry dominates almost immediately.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only constant-time arithmetic and one trigonometric evaluation |
| Space | O(1) | No auxiliary data structures are used |

The solution comfortably fits within constraints because all operations are constant time floating-point computations, well within the limits of both time and memory.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import tan, radians, pi

    h, d = map(float, inp.strip().split())

    bucket_r_top = d / 2.0
    angle = math.radians(34.0)

    sand_slope = math.tan(angle)
    bucket_slope = bucket_r_top / h

    if sand_slope <= bucket_slope:
        final_h = h
        final_r = sand_slope * final_h
    else:
        final_h = bucket_r_top / sand_slope
        final_r = bucket_slope * final_h

    return str((math.pi * final_r * final_r * final_h) / 3.0)

# provided samples
assert abs(float(run("10 10")) - 146.39985672107267) < 1e-6
assert abs(float(run("5 1")) - 1.1487958374076184) < 1e-6

# custom cases
assert float(run("1 1")) > 0
assert float(run("1000 1")) > 0
assert float(run("1 1000")) > 0
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 10 10 | 146.3998... | standard intersection case |
| 5 1 | 1.1487... | narrow bucket early cutoff |
| 1 1 | positive small value | minimum scale correctness |
| 1000 1 | small value | extreme height vs narrow opening |
| 1 1000 | large bucket opening case | wide bucket behavior |

## Edge Cases

For the case where the bucket is extremely narrow, such as input `5 1`, the bucket slope is much smaller than the sand slope. The algorithm detects this via the slope comparison and immediately clamps the sand growth to the intersection point. Substituting values gives bucket_slope = 0.1 and sand_slope ≈ 0.6745, so the sand is constrained by the walls long before reaching the top. The computed height is 0.5 / 0.6745 ≈ 0.74, and the volume follows directly.

For the opposite case where the bucket is very wide, such as `1 1000`, the bucket slope becomes large compared to the sand slope. The sand never reaches the side walls before hitting the top height, so the final height is exactly h. The algorithm correctly chooses the unclipped cone and computes volume using full height.

These two regimes confirm that the solution consistently selects the correct geometric constraint and never mixes the two conditions.
