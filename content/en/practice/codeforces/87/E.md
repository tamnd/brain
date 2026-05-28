---
title: "CF 87E - Mogohu-Rea Idol"
description: "We have three convex polygons on the plane. From each polygon we must choose one point, and the average of these three chosen points must equal the position of the idol."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "geometry"]
categories: ["algorithms"]
codeforces_contest: 87
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 73 (Div. 1 Only)"
rating: 2600
weight: 87
solve_time_s: 196
verified: true
draft: false
---

[CF 87E - Mogohu-Rea Idol](https://codeforces.com/problemset/problem/87/E)

**Rating:** 2600  
**Tags:** geometry  
**Solve time:** 3m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We have three convex polygons on the plane. From each polygon we must choose one point, and the average of these three chosen points must equal the position of the idol.

If the chosen altar points are $A, B, C$, and the idol is at point $P$, the condition is

$$\frac{A+B+C}{3}=P$$

which can be rewritten as

$$A+B+C=3P$$

For every hill independently, we must determine whether such a triple of points exists.

The polygons are convex and can have up to $5 \cdot 10^4$ vertices each. The number of hills is up to $10^5$. These limits immediately rule out anything that processes each query against every polygon edge in linear time. Even $O(nm)$ would already be around $10^{10}$ operations in the worst case.

The geometry structure matters more than the raw size. Convex polygons behave very nicely under Minkowski sums, and the condition

$$A+B+C=3P$$

strongly suggests transforming the problem into a point-in-convex-polygon query.

The first subtle point is that the altar positions are not restricted to polygon vertices. They may lie anywhere inside the polygon, including on the boundary. A solution that only checks vertices is incorrect.

Consider:

```
Triangle 1: (0,0) (2,0) (0,2)
Triangle 2: (0,0) (2,0) (0,2)
Triangle 3: (0,0) (2,0) (0,2)
Hill: (1,1)
```

The point $(1,1)$ is achievable because we can choose all three altar points to be $(1,1)$, which lies inside the triangle. Restricting ourselves to vertices would incorrectly answer NO.

The second subtle point is that polygons may intersect or even contain one another. No separation assumptions exist. Any approach relying on disjointness fails immediately.

Another easy mistake is forgetting that boundary points are allowed. Suppose one polygon degenerately contributes through an edge endpoint.

```
Triangle 1: (0,0) (2,0) (0,2)
Triangle 2: (0,0) (2,0) (0,2)
Triangle 3: (0,0) (2,0) (0,2)
Hill: (0,0)
```

Choosing all three altars at $(0,0)$ is valid, so the correct answer is YES. A strict interior test would incorrectly reject it.

The last dangerous area is precision. Coordinates are as large as $5 \cdot 10^8$, and Minkowski sums can temporarily produce values around $1.5 \cdot 10^9$. Floating point geometry is unnecessary here and risks boundary errors. Integer cross products fit safely inside 64-bit signed integers, so the entire solution should stay integer-only.

## Approaches

The brute-force interpretation follows the definition directly. For each hill point $P$, we would try to determine whether there exist points $A \in S_1$, $B \in S_2$, and $C \in S_3$ such that

$$A+B+C=3P$$

If we restricted ourselves to polygon vertices, we could enumerate all triples of vertices, but that is already impossible. Each polygon may have $5 \cdot 10^4$ vertices, so the number of triples becomes roughly

$$(5 \cdot 10^4)^3 \approx 10^{14}$$

and this still would not even solve the real problem because valid altar points are not limited to vertices.

The key observation is that the equation already describes a Minkowski sum.

Define

$$S = S_1 + S_2 + S_3$$

where the Minkowski sum contains every point representable as

$$A+B+C$$

with $A \in S_1$, $B \in S_2$, $C \in S_3$.

Then the query becomes extremely simple:

$$3P \in S$$

So instead of solving a fresh geometric existence problem for every hill, we can precompute the combined region once, and each query reduces to a point-in-convex-polygon test.

This works beautifully because convex polygons are closed under Minkowski sum. The sum of convex polygons is again a convex polygon. Even better, Minkowski sums of convex polygons can be computed in linear time using the edge-angle merge technique.

Suppose the three polygons contain $n_1, n_2, n_3$ vertices. Their Minkowski sum has at most

$$n_1+n_2+n_3$$

vertices after removing collinear redundancies. That means we can build the final polygon once in linear time and then answer each query in logarithmic time using binary-search point inclusion.

The brute-force approach fails because it repeatedly reconstructs geometric relationships independently for every query. The Minkowski-sum viewpoint compresses the entire feasible region into one convex polygon.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(m \cdot n_1 n_2 n_3)$ | $O(1)$ | Too slow |
| Optimal | $O(n_1+n_2+n_3+m\log N)$ | $O(N)$ | Accepted |

Here $N$ is the number of vertices of the final Minkowski sum polygon.

## Algorithm Walkthrough

1. Read the three convex polygons.

The vertices are already given in counterclockwise order, which is exactly what the Minkowski-sum algorithm needs.
2. Rotate each polygon so that its lexicographically smallest vertex comes first.

This gives every polygon a canonical starting position. After this rotation, the edge vectors appear in sorted angular order around the polygon.
3. Convert each polygon into a cyclic edge sequence.

If the vertices are $p_0, p_1, \dots, p_{n-1}$, then the edges are

$$p_{i+1}-p_i$$

with wraparound at the end.
4. Compute the Minkowski sum of two polygons using edge merging.

Start from the sum of the two smallest vertices. Then walk simultaneously through the edge sequences.

At every step, compare the cross product of the current edge vectors.

If the cross product is positive, advance the first polygon.

If negative, advance the second polygon.

If zero, advance both.

This is identical in spirit to merging two sorted arrays, except the ordering is by edge angle.
5. Sum the three polygons.

First compute

$$T=S_1+S_2$$

then compute

$$S=T+S_3$$
6. Remove redundant collinear vertices from the resulting polygon.

Consecutive collinear edges do not affect the shape but complicate point queries.
7. For each hill point $P$, scale it by 3.

The feasibility condition is

$$3P \in S$$

so we query the point

$$Q=(3x,3y)$$
8. Perform point-in-convex-polygon testing in logarithmic time.

Fix the first vertex as the origin of a fan triangulation.

First reject points outside the angular range formed by the first and last edges.

Then binary search for the triangle sector containing the query point.

Finally check whether the point lies inside that triangle using cross products.
9. Print YES if the point lies inside or on the boundary of the Minkowski sum polygon, otherwise print NO.

### Why it works

The Minkowski sum

$$S_1+S_2+S_3$$

contains exactly all points representable as

$$A+B+C$$

with one point chosen from each polygon.

The idol condition requires

$$A+B+C=3P$$

which means the hill is feasible exactly when $3P$ belongs to the Minkowski sum polygon.

Because every polygon is convex, their Minkowski sum is also convex. The edge-angle merge algorithm constructs its boundary correctly by traversing the supporting edges in increasing angular order. Point-in-convex-polygon queries are correct because every convex polygon can be partitioned into non-overlapping triangles sharing a common anchor vertex.

## Python Solution

```python
import sys
input = sys.stdin.readline

def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]

def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def rotate_smallest(poly):
    idx = min(range(len(poly)), key=lambda i: (poly[i][0], poly[i][1]))
    return poly[idx:] + poly[:idx]

def compress(poly):
    res = []
    n = len(poly)

    for p in poly:
        while len(res) >= 2:
            a = res[-2]
            b = res[-1]
            if cross(sub(b, a), sub(p, b)) == 0:
                res.pop()
            else:
                break
        res.append(p)

    while len(res) >= 3:
        a = res[-2]
        b = res[-1]
        c = res[0]
        if cross(sub(b, a), sub(c, b)) == 0:
            res.pop()
        else:
            break

    return res

def minkowski(A, B):
    A = rotate_smallest(A)
    B = rotate_smallest(B)

    n = len(A)
    m = len(B)

    ea = [sub(A[(i + 1) % n], A[i]) for i in range(n)]
    eb = [sub(B[(i + 1) % m], B[i]) for i in range(m)]

    i = j = 0

    cur = add(A[0], B[0])
    res = [cur]

    while i < n or j < m:
        va = ea[i % n] if i < n else None
        vb = eb[j % m] if j < m else None

        if i == n:
            take_a = False
        elif j == m:
            take_a = True
        else:
            cr = cross(va, vb)
            if cr > 0:
                take_a = True
            elif cr < 0:
                take_a = False
            else:
                cur = add(cur, add(va, vb))
                res.append(cur)
                i += 1
                j += 1
                continue

        if take_a:
            cur = add(cur, va)
            i += 1
        else:
            cur = add(cur, vb)
            j += 1

        res.append(cur)

    res.pop()
    return compress(res)

def point_in_convex(poly, p):
    n = len(poly)

    if n == 1:
        return p == poly[0]

    if cross(sub(poly[1], poly[0]), sub(p, poly[0])) < 0:
        return False

    if cross(sub(poly[-1], poly[0]), sub(p, poly[0])) > 0:
        return False

    l = 1
    r = n - 1

    while r - l > 1:
        mid = (l + r) // 2

        if cross(sub(poly[mid], poly[0]), sub(p, poly[0])) >= 0:
            l = mid
        else:
            r = mid

    a = poly[0]
    b = poly[l]
    c = poly[(l + 1) % n]

    return cross(sub(b, a), sub(p, a)) >= 0 and \
           cross(sub(c, b), sub(p, b)) >= 0 and \
           cross(sub(a, c), sub(p, c)) >= 0

def read_poly():
    n = int(input())
    return [tuple(map(int, input().split())) for _ in range(n)]

p1 = read_poly()
input()

p2 = read_poly()
input()

p3 = read_poly()
input()

sum12 = minkowski(p1, p2)
total = minkowski(sum12, p3)

m = int(input())

out = []

for _ in range(m):
    x, y = map(int, input().split())
    q = (3 * x, 3 * y)

    if point_in_convex(total, q):
        out.append("YES")
    else:
        out.append("NO")

print("\n".join(out))
```

The implementation follows the mathematical structure directly.

The `rotate_smallest` function normalizes the polygon representation. Minkowski edge merging only works cleanly when both polygons start from their lexicographically smallest vertex.

The `minkowski` function performs the linear merge. Each polygon contributes a cyclic sequence of edge vectors sorted by angle. The merge logic advances whichever edge has smaller polar angle, detected using the cross product. When two edges are parallel and point in the same direction, both are consumed together.

The result may contain unnecessary collinear vertices. The `compress` function removes them using orientation checks. This matters because the point query assumes a strictly convex fan structure.

The point inclusion test uses only integer arithmetic. The polygon is treated as a fan rooted at `poly[0]`. Binary search identifies the unique triangle sector containing the query point, then three orientation tests determine whether the point lies inside or on the boundary.

One subtle detail is the use of non-strict inequalities. Boundary points are valid according to the statement, so every containment test must accept zero cross products.

Another subtle point is overflow safety. Python integers are arbitrary precision, but even in C++ all computations fit in signed 64-bit integers because coordinate magnitudes stay below roughly $10^{18}$ after multiplication inside cross products.

## Worked Examples

### Sample 1

Input:

```
3
0 0
1 0
1 1

4
8 8
5 5
6 4
8 4

3
-1 -1
-3 -1
-2 -2

5
0 0
2 1
7 1
1 1
5 3
```

The algorithm first builds the Minkowski sum polygon.

One successful query is the hill $(2,1)$.

We test the point:

$$Q=(6,3)$$

The chosen altar points from the statement are:

$$(1,0), (7,5), (-2,-2)$$

Their sum is:

$$(1,0)+(7,5)+(-2,-2)=(6,3)$$

which equals $3(2,1)$.

| Query Hill | Scaled Query | Inside Minkowski Sum | Answer |
| --- | --- | --- | --- |
| (0,0) | (0,0) | No | NO |
| (2,1) | (6,3) | Yes | YES |
| (7,1) | (21,3) | No | NO |
| (1,1) | (3,3) | Yes | YES |
| (5,3) | (15,9) | No | NO |

This demonstrates the central reduction of the problem. We never search for altar triples explicitly. The entire feasible region is encoded into one convex polygon.

### Custom Example

Consider three identical unit squares:

```
4
0 0
1 0
1 1
0 1
```

Their Minkowski sum becomes the square:

```
0 ≤ x ≤ 3
0 ≤ y ≤ 3
```

Now query the hill $(1,1)$.

| Step | Value |
| --- | --- |
| Hill | (1,1) |
| Scaled point | (3,3) |
| Minkowski bounds | 0 ≤ x ≤ 3, 0 ≤ y ≤ 3 |
| Inclusion result | Boundary point |
| Answer | YES |

This trace confirms that boundary points are accepted correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n_1+n_2+n_3+m\log N)$ | Linear Minkowski construction and logarithmic point queries |
| Space | $O(N)$ | Stores the final convex polygon |

The total number of polygon vertices is at most $1.5 \cdot 10^5$, so the linear Minkowski construction is easily fast enough. Each of the $10^5$ hill queries costs only logarithmic time, which comfortably fits within the time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def cross(a, b):
        return a[0] * b[1] - a[1] * b[0]

    def sub(a, b):
        return (a[0] - b[0], a[1] - b[1])

    def add(a, b):
        return (a[0] + b[0], a[1] + b[1])

    def rotate_smallest(poly):
        idx = min(range(len(poly)), key=lambda i: (poly[i][0], poly[i][1]))
        return poly[idx:] + poly[:idx]

    def compress(poly):
        res = []

        for p in poly:
            while len(res) >= 2:
                a = res[-2]
                b = res[-1]

                if cross(sub(b, a), sub(p, b)) == 0:
                    res.pop()
                else:
                    break

            res.append(p)

        return res

    def minkowski(A, B):
        A = rotate_smallest(A)
        B = rotate_smallest(B)

        n = len(A)
        m = len(B)

        ea = [sub(A[(i + 1) % n], A[i]) for i in range(n)]
        eb = [sub(B[(i + 1) % m], B[i]) for i in range(m)]

        i = j = 0

        cur = add(A[0], B[0])
        res = [cur]

        while i < n or j < m:
            va = ea[i % n] if i < n else None
            vb = eb[j % m] if j < m else None

            if i == n:
                take_a = False
            elif j == m:
                take_a = True
            else:
                cr = cross(va, vb)

                if cr > 0:
                    take_a = True
                elif cr < 0:
                    take_a = False
                else:
                    cur = add(cur, add(va, vb))
                    res.append(cur)
                    i += 1
                    j += 1
                    continue

            if take_a:
                cur = add(cur, va)
                i += 1
            else:
                cur = add(cur, vb)
                j += 1

            res.append(cur)

        res.pop()
        return compress(res)

    def point_in_convex(poly, p):
        n = len(poly)

        if cross(sub(poly[1], poly[0]), sub(p, poly[0])) < 0:
            return False

        if cross(sub(poly[-1], poly[0]), sub(p, poly[0])) > 0:
            return False

        l, r = 1, n - 1

        while r - l > 1:
            mid = (l + r) // 2

            if cross(sub(poly[mid], poly[0]), sub(p, poly[0])) >= 0:
                l = mid
            else:
                r = mid

        a = poly[0]
        b = poly[l]
        c = poly[(l + 1) % n]

        return cross(sub(b, a), sub(p, a)) >= 0 and \
               cross(sub(c, b), sub(p, b)) >= 0 and \
               cross(sub(a, c), sub(p, c)) >= 0

    def read_poly():
        n = int(input())
        return [tuple(map(int, input().split())) for _ in range(n)]

    p1 = read_poly()
    input()

    p2 = read_poly()
    input()

    p3 = read_poly()
    input()

    total = minkowski(minkowski(p1, p2), p3)

    m = int(input())

    ans = []

    for _ in range(m):
        x, y = map(int, input().split())

        if point_in_convex(total, (3 * x, 3 * y)):
            ans.append("YES")
        else:
            ans.append("NO")

    return "\n".join(ans)

# sample 1
assert run("""3
0 0
1 0
1 1

4
8 8
5 5
6 4
8 4

3
-1 -1
-3 -1
-2 -2

5
0 0
2 1
7 1
1 1
5 3
""") == """NO
YES
NO
YES
NO"""

# minimum triangles
assert run("""3
0 0
1 0
0 1

3
0 0
1 0
0 1

3
0 0
1 0
0 1

1
0 0
""") == "YES"

# boundary point
assert run("""4
0 0
1 0
1 1
0 1

4
0 0
1 0
1 1
0 1

4
0 0
1 0
1 1
0 1

1
1 1
""") == "YES"

# outside point
assert run("""4
0 0
1 0
1 1
0 1

4
0 0
1 0
1 1
0 1

4
0 0
1 0
1 1
0 1

1
2 2
""") == "NO"

# negative coordinates
assert run("""3
-1 -1
0 -1
-1 0

3
-1 -1
0 -1
-1 0

3
-1 -1
0 -1
-1 0

1
-1 -1
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Three identical minimal triangles | YES | Smallest valid polygons |
| Boundary query on summed square | YES | Boundary inclusion |
| Query outside summed square | NO | Correct rejection |
| Negative-coordinate triangles | YES | Signed arithmetic correctness |

## Edge Cases

Consider the boundary inclusion case:

```
3
0 0
1 0
0 1

3
0 0
1 0
0 1

3
0 0
1 0
0 1

1
0 0
```

The scaled query point is still $(0,0)$. This point lies exactly at a vertex of the Minkowski sum polygon. The point-in-polygon test accepts it because every orientation check uses `>= 0` instead of `> 0`. The algorithm correctly prints YES.

Now consider an example where only interior points work:

```
3
0 0
2 0
0 2

3
0 0
2 0
0 2

3
0 0
2 0
0 2

1
1 1
```

The scaled query becomes $(3,3)$. No triple of vertices sums to $(3,3)$, so any vertex-only approach fails. But the Minkowski sum contains all convex combinations, not just vertex sums. Since $(1,1)$ lies inside each triangle, choosing all three altar points there gives

$$(1,1)+(1,1)+(1,1)=(3,3)$$

and the algorithm correctly outputs YES.

Finally, consider intersecting polygons:

```
3
0 0
2 0
0 2

3
1 0
3 0
1 2

3
0 1
2 1
0 3

1
1 1
```

The polygons overlap heavily. The algorithm does not rely on disjointness anywhere. Minkowski sums remain valid for arbitrary convex sets, so the same construction and query logic works unchanged.
