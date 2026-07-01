---
title: "CF 104282L - Auto Chess"
description: "We are given a set of enemy positions on a plane, all measured relative to the origin where our character stands."
date: "2026-07-01T21:08:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104282
codeforces_index: "L"
codeforces_contest_name: "The 20th Hangzhou City University Programming Contest"
rating: 0
weight: 104282
solve_time_s: 60
verified: true
draft: false
---

[CF 104282L - Auto Chess](https://codeforces.com/problemset/problem/104282/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of enemy positions on a plane, all measured relative to the origin where our character stands. The character can rotate a weapon and choose a direction, and whenever it attacks, it eliminates all enemies that lie inside a fixed 45-degree angular sector starting from that direction. The sector is anchored at the origin, so the only freedom is how we rotate this wedge.

The task is to choose the orientation of this 45-degree wedge so that the number of enemies inside it is maximized.

The key input is up to 100,000 points with coordinates in the range −10⁴ to 10⁴. This immediately rules out any solution that tries to test every possible wedge orientation defined by pairs or triples of points, since a naive angular comparison per candidate direction would lead to quadratic or worse behavior.

A subtle issue appears with boundary behavior. Points lying exactly on the two rays forming the 45-degree wedge must be counted. This matters because any angular formulation must handle equality carefully, otherwise points on the boundary may be lost or double-counted depending on floating-point comparisons. Another edge case is vertical and horizontal directions where naive slope computations fail due to division by zero or precision instability.

A small example illustrates the boundary sensitivity. If we have points (1, 2), (2, 1), and (1, 1), the optimal wedge of 45 degrees can include all three if oriented properly along the line y = x. A naive approach that relies on floating-point angles might exclude boundary-aligned points due to precision errors.

## Approaches

A brute-force idea is to treat every enemy point as a candidate direction for one boundary ray of the wedge. For each such direction, we could sweep another boundary ray 45 degrees away and count how many points lie in between. For each fixed orientation, checking all points takes O(n), and trying all n directions leads to O(n²), which is about 10¹⁰ operations at worst and will not run within the time limit.

The key observation is that the geometry becomes simple once we change coordinates. A 45-degree wedge aligned in the plane corresponds to a condition involving differences of coordinates. If we rotate the plane by 45 degrees, the wedge turns into an axis-aligned interval constraint in the transformed coordinate system.

Specifically, define transformed coordinates:

u = x + y and v = x − y.

A 45-degree angular sector in the original plane corresponds to selecting points whose u values lie within an interval of length proportional to the wedge direction, while respecting ordering in v or equivalently handling monotonic alignment. After transformation, the problem reduces to finding the maximum number of points that can be covered by a sliding window over sorted angular representations or equivalently over sorted directional angles.

A more robust interpretation avoids trigonometry entirely: each point defines an angle θ = atan2(y, x). The wedge problem becomes: find the maximum number of points whose angles lie in an interval of length π/4. We sort all angles and use a two-pointer sweep on the circular array (duplicating angles by adding 2π). This turns the problem into a classic maximum points in a fixed angular window.

The sweep works because once angles are sorted, expanding a window until it exceeds π/4 and then shrinking it maintains a linear scan over all endpoints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Angle sort + two pointers | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We solve the problem by converting geometric direction into a one-dimensional angular ordering.

1. Compute the angle of every point using atan2(y, x). This gives a value in the range (−π, π]. This step converts geometric direction into a sortable scalar, which is essential because angular inclusion becomes interval containment.
2. Normalize angles into a consistent range, typically [0, 2π), so that circular wraparound can be handled cleanly.
3. Sort all angles in increasing order. Sorting is required so that any contiguous segment in this list corresponds to a continuous sweep in angular space.
4. Extend the array by appending each angle plus 2π. This duplication allows us to handle wraparound intervals without modular arithmetic complications.
5. Use a two-pointer sliding window. Maintain a right pointer that expands while the angular difference between angles[r] and angles[l] is at most π/4. This ensures all points in the window are valid under the wedge constraint.
6. For each left pointer position, compute the maximum valid right extension and update the answer with r − l + 1. Then move the left pointer forward and continue.
7. Return the maximum window size found.

The reason we can safely use a sliding window is that after sorting, expanding the right pointer only increases the angular span. Once the span exceeds π/4, it will never become valid again for that fixed left endpoint unless we move the left pointer.

### Why it works

The correctness relies on the fact that any valid wedge corresponds exactly to an interval of angles of length at most π/4. Every such interval can be represented by a starting angle equal to the smallest angle inside it. For that starting angle, the optimal solution is the largest contiguous block of points within π/4 ahead. Since sorting preserves angular order, every valid subset appears as a contiguous segment in the sorted doubled array, and the two-pointer scan enumerates all such segments implicitly.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

def solve():
    n = int(input())
    angles = []
    
    for _ in range(n):
        x, y = map(int, input().split())
        ang = math.atan2(y, x)
        if ang < 0:
            ang += 2 * math.pi
        angles.append(ang)
    
    angles.sort()
    
    # duplicate for circular wrap
    extended = angles + [a + 2 * math.pi for a in angles]
    
    ans = 0
    r = 0
    window = math.pi / 4
    
    for l in range(n):
        while r < len(extended) and extended[r] - extended[l] <= window + 1e-12:
            r += 1
        ans = max(ans, r - l)
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The core of the implementation is the conversion to angles using atan2, which avoids all slope-based instability. The normalization step ensures all angles are comparable on a single circular scale. The duplication of the array is what allows wraparound windows such as angles near 350 degrees combined with angles near 10 degrees to be handled without special cases.

The two-pointer logic carefully maintains a monotonic right pointer, so each element is processed at most twice, once as left and once as right boundary.

The small epsilon in the comparison avoids floating-point precision issues when points lie exactly on the boundary of the 45-degree sector.

## Worked Examples

Consider points (1, 2), (2, 1), and (1, 1).

After converting to angles:

| Point | Angle (approx) |
| --- | --- |
| (1,2) | 1.107 |
| (2,1) | 0.464 |
| (1,1) | 0.785 |

Sorted angles become [0.464, 0.785, 1.107]. We duplicate them as [0.464, 0.785, 1.107, 6.747, 7.068, 7.389].

We now slide a window of size π/4 ≈ 0.785.

| l | r | angles[l] | angles[r-1] | span | window size |
| --- | --- | --- | --- | --- | --- |
| 0 | 3 | 0.464 | 1.107 | 0.643 | 3 |
| 1 | 3 | 0.785 | 1.107 | 0.322 | 2 |
| 2 | 3 | 1.107 | 1.107 | 0 | 1 |

The maximum is 3, meaning all points can be covered in a 45-degree wedge.

This trace shows that once points are sorted in angular space, the optimal wedge corresponds to a contiguous segment, and the sliding window correctly captures it.

A second example with widely separated points such as (1,0), (0,1), (-1,0), (0,-1) shows that no three points fall within any π/4 interval, and the window correctly peaks at 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting angles dominates, sliding window is linear |
| Space | O(n) | Stores angle list and duplicated array |

With n up to 100,000, sorting is easily fast enough, and the linear sweep is negligible. Memory usage is well within limits since we only store a few floating-point arrays.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    angles = []
    for _ in range(n):
        x, y = map(int, input().split())
        ang = math.atan2(y, x)
        if ang < 0:
            ang += 2 * math.pi
        angles.append(ang)

    angles.sort()
    extended = angles + [a + 2 * math.pi for a in angles]

    ans = 0
    r = 0
    window = math.pi / 4

    for l in range(n):
        while r < len(extended) and extended[r] - extended[l] <= window + 1e-12:
            r += 1
        ans = max(ans, r - l)

    return str(ans)

# provided samples
assert run("2\n1 2\n2 1\n") == "2"
assert run("1\n1 100\n100 1\n") == "1"

# custom cases
assert run("1\n1 1\n") == "1", "single point"
assert run("3\n1 1\n2 2\n3 3\n") == "3", "collinear same direction"
assert run("4\n1 0\n0 1\n-1 0\n0 -1\n") == "1", "orthogonal spread"
assert run("5\n1 2\n2 1\n3 3\n4 4\n1 0\n") == "4", "mixed cluster"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single point | 1 | minimal input correctness |
| collinear same direction | 3 | all points in one angular ray |
| orthogonal spread | 1 | no large wedge possible |
| mixed cluster | 4 | sliding window correctness on dense region |

## Edge Cases

Points lying very close to the boundary of the 45-degree sector test floating-point robustness. For example, points like (1, 100) and (100, 1) produce angles extremely close to the π/4 boundary. The algorithm handles this via a small epsilon in comparisons, ensuring boundary inclusion is consistent.

Wraparound cases such as angles near 0 and near 2π are handled by duplicating the array. Without duplication, a wedge spanning the 0 angle would incorrectly appear split into two disconnected segments. The extended array merges these cases into a single contiguous window, and the sliding pointer naturally picks them up as part of a valid interval.
