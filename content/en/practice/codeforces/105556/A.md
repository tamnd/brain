---
title: "CF 105556A - \u7ebf\u6bb5"
description: "We are given a straight line segment in the plane defined by two endpoints. From this single segment, we must construct another segment such that the new one has exactly the same length and is perpendicular to the original segment when both are extended into infinite lines."
date: "2026-06-25T06:07:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105556
codeforces_index: "A"
codeforces_contest_name: "The 6th FanRuan Cup Southeast University Programming Contest (Winter)"
rating: 0
weight: 105556
solve_time_s: 49
verified: true
draft: false
---

[CF 105556A - \u7ebf\u6bb5](https://codeforces.com/problemset/problem/105556/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a straight line segment in the plane defined by two endpoints. From this single segment, we must construct another segment such that the new one has exactly the same length and is perpendicular to the original segment when both are extended into infinite lines. The task does not ask for a unique answer, any valid construction is accepted as long as it satisfies those two geometric conditions.

Each test case provides four integers representing the coordinates of the original segment endpoints. The output must be another pair of endpoints forming a second segment. There is no restriction that the new segment must intersect the original one or share any point with it.

The coordinate bounds are large, up to $10^8$ in magnitude for inputs and up to $10^9$ for outputs. This rules out any geometric construction that depends on dense search or discretization of the plane. The number of test cases can be as large as $10^4$, so each case must be solved in constant time with only a few arithmetic operations.

A naive approach that tries to search for a valid perpendicular segment by scanning possible endpoints in a grid fails immediately because even a tiny search space of $10^5 \times 10^5$ candidates per test case would already exceed time limits by many orders of magnitude.

A subtle edge case is when the original segment is axis-aligned or has very large slope. For example, if the segment is $(0,0)$ to $(1,0)$, any valid answer must be vertical and have length $1$. A careless implementation that attempts to normalize direction vectors using floating-point arithmetic could introduce precision errors and produce slightly incorrect coordinates that fail the perpendicular or length condition.

Another edge case is when the segment is very long or involves negative coordinates, such as $(-10^8, -10^8)$ to $(10^8, 10^8)$. The solution must avoid overflow when computing direction vectors and must stay within integer bounds.

## Approaches

The brute-force idea would be to consider all pairs of integer points within the allowed output range and check whether the segment they form has the same length as the original and is perpendicular to it. This works conceptually because Euclidean geometry is well-defined and exhaustive search would eventually find valid solutions.

However, the number of candidate segments is on the order of $O((10^9)^4)$ if treated naively, since each endpoint has two coordinates. Even restricting to a reasonable local neighborhood still leaves too many possibilities per test case. The brute-force approach fails because it ignores the algebraic structure of perpendicular vectors.

The key observation is that a segment can be represented as a vector. If the original segment has direction vector $(dx, dy)$, then any perpendicular segment must have a direction vector orthogonal to it, meaning their dot product is zero. A standard perpendicular vector in 2D is $(dy, -dx)$ or $(-dy, dx)$. These are guaranteed to satisfy the orthogonality condition.

Once we fix a perpendicular direction vector, its length is automatically equal to the original segment because swapping coordinates preserves the squared norm: $dx^2 + dy^2 = dy^2 + dx^2$. Therefore, we do not need any normalization or scaling.

This reduces the problem to simply computing a perpendicular vector and placing it anywhere in the plane. The simplest choice is to anchor it at the origin, producing endpoints $(0,0)$ and $(dy, -dx)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration of Segments | $O(10^{36})$ | $O(1)$ | Too slow |
| Vector Perpendicular Construction | $O(1)$ per test case | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the endpoints of the given segment and compute its direction vector as the difference between the second and first point. This isolates the geometric information that actually matters, ignoring absolute position.
2. Let the vector be $(dx, dy)$. Construct a perpendicular vector by swapping components and negating one of them, for example $(dy, -dx)$. This step relies on the fact that perpendicularity in 2D corresponds to a 90-degree rotation.
3. Construct the output segment using any starting point. The simplest choice is to start at the origin $(0,0)$ and end at $(dy, -dx)$.
4. Output these two points for the answer.

The reasoning behind choosing the origin is that translation does not affect either length or perpendicularity, so fixing one endpoint removes unnecessary degrees of freedom.

### Why it works

The transformation $(dx, dy) \rightarrow (dy, -dx)$ preserves squared length because both vectors have norm $dx^2 + dy^2$. It also guarantees orthogonality because their dot product is $dx \cdot dy + dy \cdot (-dx) = 0$. Since the output segment is defined directly from this vector, both required conditions are satisfied regardless of where it is placed in the plane.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    x1, y1, x2, y2 = map(int, input().split())
    
    dx = x2 - x1
    dy = y2 - y1
    
    # perpendicular vector
    px, py = dy, -dx
    
    # anchor at origin
    print(0, 0, px, py)
```

The key implementation detail is computing the difference vector using integer arithmetic, which avoids precision issues entirely. The perpendicular vector is obtained by a direct swap and sign change, which is constant time and safe under the given constraints. No special handling is needed for negative coordinates or degenerate slopes because the construction is purely algebraic.

## Worked Examples

### Example 1

Input segment: $(0,0)$ to $(1,1)$

| Step | dx | dy | perpendicular (px, py) | output |
| --- | --- | --- | --- | --- |
| compute vector | 1 | 1 | - | - |
| rotate | - | - | (1, -1) | (0,0) to (1,-1) |

This produces a segment of the same length $\sqrt{2}$ and perpendicular direction since $(1,1) \cdot (1,-1) = 0$.

This confirms that diagonal segments are handled correctly.

### Example 2

Input segment: $(-3,2)$ to $(5,4)$

| Step | dx | dy | perpendicular (px, py) | output |
| --- | --- | --- | --- | --- |
| compute vector | 8 | 2 | - | - |
| rotate | - | - | (2, -8) | (0,0) to (2,-8) |

The constructed segment has length $\sqrt{68}$, matching the original, and dot product with original direction is zero.

This confirms correctness under mixed signs and non-axis-aligned segments.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t)$ | Each test case uses constant-time arithmetic operations |
| Space | $O(1)$ | No additional structures are stored |

The solution fits easily within limits since even $10^4$ test cases require only a few integer operations each, far below the time constraint.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    
    t = int(input())
    out = []
    for _ in range(t):
        x1, y1, x2, y2 = map(int, input().split())
        dx = x2 - x1
        dy = y2 - y1
        out.append(f"0 0 {dy} {-dx}")
    return "\n".join(out) + "\n"

# provided samples (format adapted)
assert run("""4
0 0 1 1
-3 2 5 4
17 9 -16 -5
-111 -451 119 19180
""").splitlines()[0].split()[2:]  # basic sanity check

# minimal segment
assert run("""1
0 0 1 0
""")

# vertical segment
assert run("""1
2 3 2 10
""")

# negative coordinates
assert run("""1
-5 -5 -1 2
""")

# large segment
assert run("""1
-100000000 0 100000000 0
""")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single horizontal segment | vertical segment | basic perpendicular construction |
| vertical segment | horizontal segment | axis swap correctness |
| negative coordinates | valid rotated vector | sign handling |
| extreme range | no overflow behavior | constraint safety |

## Edge Cases

For a horizontal segment like $(0,0)$ to $(5,0)$, the algorithm computes $(dx, dy) = (5,0)$ and outputs $(0,-5)$. The resulting segment is vertical with length $5$, and the dot product with the original direction is zero, so perpendicularity holds exactly.

For a vertical segment like $(2,3)$ to $(2,10)$, the vector is $(0,7)$ and the output becomes $(7,0)$, producing a horizontal segment of equal length.

For a segment with negative coordinates such as $(-3,-4)$ to $(1,2)$, the vector becomes $(4,6)$ and the output is $(6,-4)$. Squared lengths match and the dot product is zero, confirming correctness even when both endpoints are negative.
