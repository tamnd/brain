---
title: "CF 2074A - Draw a Square"
description: "We are given four fixed points in the plane. Their coordinates are always aligned with the axes: one lies on the negative x-axis at $(-l, 0)$, one on the positive x-axis at $(r, 0)$, one on the negative y-axis at $(0, -d)$, and one on the positive y-axis at $(0, u)$."
date: "2026-06-08T06:38:36+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2074
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1009 (Div. 3)"
rating: 800
weight: 2074
solve_time_s: 85
verified: true
draft: false
---

[CF 2074A - Draw a Square](https://codeforces.com/problemset/problem/2074/A)

**Rating:** 800  
**Tags:** geometry, implementation  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given four fixed points in the plane. Their coordinates are always aligned with the axes: one lies on the negative x-axis at $(-l, 0)$, one on the positive x-axis at $(r, 0)$, one on the negative y-axis at $(0, -d)$, and one on the positive y-axis at $(0, u)$. The only freedom in each test case is the four distances $l, r, d, u$.

The task is to decide whether these four points can serve as the vertices of some square when connected in some order. We are not allowed to move the points; we can only decide whether a valid ordering exists that forms a square without self-intersection.

The constraints are extremely small per test case, with each value between 1 and 10, but there can be up to $10^4$ test cases. This pushes us toward a constant time check per case. Any approach that tries permutations of point order is still acceptable in theory because there are only 24 permutations, but doing geometric checks repeatedly across many test cases makes a direct brute-force less clean than necessary.

A subtle edge case comes from the fact that these points are not arbitrary. They are always on axes, so the geometry is heavily constrained. A naive intuition might be that “if all four distances are equal, it is always a square”, but that is not sufficient unless we also ensure the points can actually be connected in square order without crossing edges.

For example, if $l = r = d = u = 2$, we clearly can form a rotated square centered at the origin. However, if one side is larger, say $l = 1, r = 2, d = 3, u = 4$, the points become stretched differently in each direction and no rigid square can connect them.

The key hidden requirement is symmetry: a square centered at the origin with sides parallel to diagonals would require equal extension in all four directions.

## Approaches

A brute-force approach would attempt to consider all permutations of the four given points and check whether any ordering forms a valid square. For each permutation, we would compute the four side lengths and verify equality, and also ensure the diagonals match and the shape is non-self-intersecting. Since there are 24 permutations per test case and up to $10^4$ test cases, this yields about $2.4 \times 10^5$ checks, which is already fine, but the geometric validation per permutation is unnecessary overhead for such a constrained configuration.

The key observation is that the four points are already fixed on the axes, and any square formed from them must be centered at the origin. This is because opposite points lie symmetrically across both axes in any square that uses these axis-aligned extremes.

For a square centered at the origin, the vertices must be at $(\pm a, 0)$ and $(0, \pm a)$ after rotation by 45 degrees or alignment in this specific configuration. In this problem, since the points are strictly axis-aligned, the only possible square is one where all four distances from the origin are equal. That means $l = r = d = u$.

So the entire problem reduces to a single equality check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all permutations + geometry checks) | $O(t)$ | $O(1)$ | Accepted but unnecessary |
| Optimal (direct equality check) | $O(t)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We process each test case independently and directly compare the four values.

1. Read $l, r, d, u$. These represent how far each point lies from the origin along the axes. This fully determines the geometry.
2. Check whether all four values are equal. This condition enforces perfect symmetry in all four directions, which is required for a square centered at the origin.
3. If they are equal, output “Yes”, otherwise output “No”.

### Why it works

A square has all vertices equidistant from its center. In this configuration, the only possible center is the origin because every point lies on one of the axes. For the shape to be a square, all four vertices must lie at equal radius from the center along perpendicular directions. The given structure fixes those directions to the axes themselves, so the only way to maintain equal side lengths and right angles is for all four distances from the origin to match exactly. Any imbalance forces either unequal edges or a distorted quadrilateral that cannot satisfy square constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    l, r, d, u = map(int, input().split())
    if l == r == d == u:
        print("Yes")
    else:
        print("No")
```

The solution is a direct implementation of the symmetry condition. The chained equality check ensures all four directions are identical, which is the only valid configuration.

No additional data structures or geometric computations are required, since the input already encodes the full spatial constraints.

## Worked Examples

### Example 1

Input:

```
2 2 2 2
```

| l | r | d | u | Check | Output |
| --- | --- | --- | --- | --- | --- |
| 2 | 2 | 2 | 2 | all equal | Yes |

All directions are identical, so the points can form a perfectly symmetric square centered at the origin.

This confirms the invariant that equal radii in all four axial directions are sufficient.

### Example 2

Input:

```
1 2 3 4
```

| l | r | d | u | Check | Output |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 3 | 4 | not all equal | No |

The asymmetry means at least one side would be longer or shorter, preventing equal edges. This breaks the square condition immediately.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t)$ | One constant-time comparison per test case |
| Space | $O(1)$ | Only four integers stored per test case |

The solution trivially satisfies the constraints since it performs only a few integer comparisons for each test case, well within limits for $t \le 10^4$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(sys.stdin.readline())
    out = []
    for _ in range(t):
        l, r, d, u = map(int, sys.stdin.readline().split())
        out.append("Yes" if l == r == d == u else "No")
    return "\n".join(out)

# provided samples
assert run("2\n2 2 2 2\n1 2 3 4\n") == "Yes\nNo"

# custom cases
assert run("1\n1 1 1 1\n") == "Yes"
assert run("1\n1 1 1 2\n") == "No"
assert run("1\n10 10 10 9\n") == "No"
assert run("1\n2 3 2 3\n") == "No"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 1 | Yes | minimal valid square |
| 1 1 1 2 | No | single-axis deviation |
| 10 10 10 9 | No | boundary inequality |
| 2 3 2 3 | No | alternating imbalance pattern |

## Edge Cases

One edge case is when three values are equal and one differs slightly, such as $l = r = d = 5, u = 4$. The algorithm correctly outputs “No” because the equality check fails immediately. Geometrically, this would stretch one axis and destroy rotational symmetry.

Another case is when two opposite directions differ but the other pair matches, such as $l = r = 7, d = u = 3$. Even though both axes are symmetric independently, the mismatch between axes prevents a square because side lengths would differ depending on orientation.

Finally, in a fully equal case like $l = r = d = u = 1$, the check passes and the configuration corresponds to a perfectly centered square.
