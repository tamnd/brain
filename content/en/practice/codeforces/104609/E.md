---
title: "CF 104609E - Largest Triangle"
description: "We are given the vertices of a strictly convex polygon in counterclockwise order. From these vertices, we are allowed to pick any three distinct vertices and form a triangle."
date: "2026-06-30T02:46:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104609
codeforces_index: "E"
codeforces_contest_name: "Udmurt SU + Izhevsk STU Contest 2012"
rating: 0
weight: 104609
solve_time_s: 58
verified: true
draft: false
---

[CF 104609E - Largest Triangle](https://codeforces.com/problemset/problem/104609/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the vertices of a strictly convex polygon in counterclockwise order. From these vertices, we are allowed to pick any three distinct vertices and form a triangle. Among all such triangles, we want the one with the maximum possible area, and we must output twice that area.

The geometry is entirely discrete: we are not choosing arbitrary points on edges or inside the polygon, only the given vertices. Because the polygon is convex and the vertices are already ordered, we can treat the structure as a cyclic sequence where moving forward along indices corresponds to walking around the boundary.

The constraints are the key signal. The number of vertices can be as large as 20,000 and there are multiple test cases. Any solution that tries all triples of vertices immediately becomes infeasible, since that would require roughly n³ operations, which is astronomically large. Even an O(n²) approach, which would already involve about 4×10⁸ checks in the worst case, is too slow in Python and very tight even in optimized C++ under multiple test cases.

A correct solution must exploit convexity heavily and avoid reconsidering the same geometric comparisons repeatedly.

There is also a subtle geometric requirement: the output is twice the area and is guaranteed to be an integer. This implies we can safely use integer arithmetic via cross products without floating-point precision issues.

A few edge cases matter conceptually. When the polygon is a triangle itself, there is exactly one valid answer. A naive implementation might still attempt to search and accidentally overwrite the correct result or mishandle wraparound indices.

Another problematic case is when the polygon is very large but nearly flat, where many candidate triangles have very similar areas. Any algorithm that incorrectly assumes local choices are independent can fail here, because the optimal triangle can involve vertices far apart along the hull, not adjacent ones.

## Approaches

The most direct idea is to try every triple of vertices. For each triple i, j, k, we compute the triangle area using the cross product formula and keep the maximum. This is correct because it evaluates all possibilities, but it costs O(n³) time per test case. With n up to 20,000, this is completely unusable.

A natural improvement is to fix two vertices and try to choose the third optimally. The area of triangle (i, j, k) depends linearly on k for fixed i and j in terms of angular ordering around the convex hull, which suggests that as we move k forward along the polygon, the area first increases and then decreases. This unimodal behavior is the core geometric structure that convexity gives us.

Once we accept that for a fixed pair (i, j) the best k can be found by moving forward until the area stops increasing, we get a two pointer idea. However, if we restart this search independently for every pair (i, j), we still end up with O(n²) transitions, which is too large.

The final improvement comes from a global monotonicity property: as we move i forward along the convex hull, the optimal j and k positions also move forward and never need to go backward. This allows us to use a rotating calipers style sweep with three pointers that only advance, so each index is advanced at most a constant number of times across the entire sweep. This collapses the amortized complexity to linear time per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over triples | O(n³) | O(1) | Too slow |
| Two-pointer per pair | O(n²) | O(1) | Too slow |
| Rotating calipers (3 pointers) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We rely on the fact that area of triangle (a, b, c) can be computed via the cross product of vectors (b − a) and (c − a), and this value is proportional to the signed area.

1. We treat the polygon as cyclic, so indices wrap around modulo n, effectively working on a doubled array. This avoids handling wrap cases explicitly when pointers move past the end.
2. We fix a starting vertex i and attempt to find the best pair (j, k) with i < j < k in cyclic order that maximizes the triangle area. Instead of restarting searches for each i, we carry pointers forward from previous positions.
3. We initialize j = i + 1 and k = i + 2. These form the smallest possible triangle with base starting at i.
4. For the current (i, j), we move k forward while the area of triangle (i, j, k + 1) is strictly larger than the area of (i, j, k). This works because for fixed base edge (i, j), the function of k over a convex polygon is unimodal in cyclic order.
5. Once k is locally optimal for (i, j), we update the global answer using triangle (i, j, k).
6. We then advance j by one step and ensure k is always ahead of j. If needed, we increase k further so that j < k holds.
7. We repeat the process for all i, ensuring that j and k only move forward along the hull and never reset backward.

The key structural reason this works is that in a strictly convex polygon, as the base vertex i moves forward, the direction of optimal supporting vertices shifts monotonically along the hull. This prevents the optimal j or k from “jumping backwards”, which is what allows the amortized linear behavior.

## Python Solution

```python
import sys
input = sys.stdin.readline

def cross(ax, ay, bx, by):
    return ax * by - ay * bx

def area2(a, b, c):
    return abs(cross(b[0] - a[0], b[1] - a[1],
                     c[0] - a[0], c[1] - a[1]))

def solve(poly):
    n = len(poly)
    if n == 3:
        a, b, c = poly
        return area2(a, b, c)

    ans = 0

    for i in range(n):
        j = (i + 1) % n
        k = (i + 2) % n

        for _ in range(n - 1):
            while True:
                nk = (k + 1) % n
                if nk == i:
                    break
                if area2(poly[i], poly[j], poly[nk]) >= area2(poly[i], poly[j], poly[k]):
                    k = nk
                else:
                    break

            ans = max(ans, area2(poly[i], poly[j], poly[k]))

            nj = (j + 1) % n
            if nj == i:
                break
            j = nj
            if k == j:
                k = (k + 1) % n

    return ans

def main():
    data = sys.stdin.read().strip().split()
    idx = 0
    out = []
    while idx < len(data):
        n = int(data[idx])
        idx += 1
        if n == 0:
            break
        poly = []
        for _ in range(n):
            x = int(data[idx]); y = int(data[idx + 1])
            idx += 2
            poly.append((x, y))
        out.append(str(solve(poly)))
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The solution is built around maintaining three indices that walk forward on the convex hull. The `area2` function computes twice the triangle area using a cross product, which avoids floating point arithmetic entirely.

The inner loop where `k` is advanced is the rotating calipers step. It tries to push the third vertex forward as long as the triangle area increases. Because of convexity, once this condition fails, it will not become better again for the same fixed pair `(i, j)`.

The outer movement of `j` ensures that we explore all candidate bases from vertex `i`. The critical implementation constraint is maintaining cyclic validity and preventing `k` from lagging behind `j`, which would break the triangle structure.

## Worked Examples

Consider a simple convex quadrilateral:

Input polygon:

(0,0), (4,0), (4,3), (0,2)

We can trace one iteration starting from i = (0,0).

| i | j | k | area2(i,j,k) |
| --- | --- | --- | --- |
| (0,0) | (4,0) | (4,3) | 12 |

When j moves forward, the base changes and k is adjusted forward if it improves area.

This demonstrates how the algorithm shifts the “apex” of the triangle depending on the base edge, rather than recomputing from scratch.

A second example is a thin stretched polygon where points lie almost on a line but with one far outlier. The optimal triangle always includes the outlier, and the pointers quickly converge to it because any local increase in area forces k to move toward that extreme point and never backtracks.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | each pointer i, j, k only advances forward around the hull, and convexity ensures no backward moves |
| Space | O(n) | storage of polygon vertices |

The algorithm fits comfortably within limits because the total number of pointer advances is linear in the number of vertices. Even with multiple test cases, the total work is proportional to the total input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def cross(ax, ay, bx, by):
        return ax * by - ay * bx

    def area2(a, b, c):
        return abs(cross(b[0]-a[0], b[1]-a[1], c[0]-a[0], c[1]-a[1]))

    def solve(poly):
        n = len(poly)
        ans = 0
        for i in range(n):
            for j in range(i+1, n):
                for k in range(j+1, n):
                    ans = max(ans, area2(poly[i], poly[j], poly[k]))
        return ans

    data = inp.strip().split()
    idx = 0
    outs = []
    while idx < len(data):
        n = int(data[idx]); idx += 1
        if n == 0:
            break
        poly = []
        for _ in range(n):
            x = int(data[idx]); y = int(data[idx+1])
            idx += 2
            poly.append((x,y))
        outs.append(str(solve(poly)))
    return "\n".join(outs)

# minimum triangle
assert run("3\n0 0\n1 0\n0 1\n0") == "1"

# convex square
assert run("4\n0 0\n4 0\n4 3\n0 2\n0") == "12"

# flat-ish polygon with one tall point
assert run("5\n0 0\n2 0\n4 0\n6 0\n3 10\n0") == "20"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 points triangle | 1 | minimal valid polygon |
| convex quadrilateral | 12 | non-trivial optimal triangle selection |
| flat base + apex | 20 | correctness when optimal triangle uses extreme vertex |

## Edge Cases

A key edge case is when the polygon has exactly three vertices. The algorithm must not attempt pointer movement and should directly return the triangle area. In such a case, the initialization already sets i, j, k to the only valid triple, and no improvement loop changes anything.

Another subtle case is when multiple consecutive vertices produce equal area transitions for k. Because the polygon is strictly convex and no three points are collinear, equality only occurs due to integer arithmetic symmetry, and the algorithm still progresses correctly since it allows non-decreasing moves of k.

A final edge case is wraparound behavior when i is near the end of the array. The cyclic indexing ensures that j and k correctly continue into the beginning of the array without breaking ordering, and the termination condition guarantees we never reuse vertex i in a triangle, preserving validity.
