---
title: "CF 102443B - Blocking the View"
description: "For each test case, we have two non-intersecting line segments, called (a) and (b), together with a non-zero direction vector (vec v). We need to decide whether some point (A) on (a) can move from (A) in the direction of (vec v) and hit some point (B) on (b)."
date: "2026-08-08T12:46:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102443
codeforces_index: "B"
codeforces_contest_name: "2019-2020 Russia Team Open, High School Programming Contest (VKOSHP 19)"
rating: 0
weight: 102443
solve_time_s: 123
verified: true
draft: false
---

[CF 102443B - Blocking the View](https://codeforces.com/problemset/problem/102443/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

For each test case, we have two non-intersecting line segments, called (a) and (b), together with a non-zero direction vector (\vec v). We need to decide whether some point (A) on (a) can move from (A) in the direction of (\vec v) and hit some point (B) on (b).

Equivalently, we need points (A\in a) and (B\in b) such that

[
B-A=t\vec v
]

for some (t>0). The strict positivity follows from the fact that the two segments do not intersect, so (A) and (B) cannot be the same point.

Each test case contains eight coordinates for the two segment endpoints and two coordinates for the viewing direction. There can be as many as (50,000) independent test cases. All coordinates have absolute value at most (10^6), so an (O(n)) or (O(n\log n)) total solution is easily fast enough, but an algorithm that performs a large search inside every segment is not appropriate.

The main difficulty is that (A) and (B) are arbitrary real points on the segments. Checking only the endpoints is not sufficient. For example,

```
1
0 0 4 4 1 3 3 1 1 1
```

has the direction ((1,1)). The endpoint pairs do not give the desired direction, but the two segments contain points with the same perpendicular coordinate, and one such point on the second segment is ahead of the corresponding point on the first. A solution that checks only the four endpoint pairs can miss this.

A second trap is the direction. Consider

```
1
0 0 1 0 -3 0 -2 0 1 0
```

The segments lie on the same horizontal line, but the second segment is behind the first when looking in direction ((1,0)). The correct answer is `No`. A test that checks only whether the two segments lie on the same line would incorrectly answer `Yes`.

A third edge case occurs when a segment is parallel to the viewing direction. For example,

```
1
0 0 1 0 2 0 2 1 1 0
```

has the first segment parallel to (\vec v). The correct answer is `Yes`, because the point ((1,0)) can move right and reach ((2,0)) on the second segment. Any formula that divides by the perpendicular coordinate difference of the first segment must handle a zero denominator separately.

Finally, the segments may have only one common perpendicular coordinate. For example,

```
1
0 0 1 0 2 0 2 1 1 0
```

has exactly this situation. Treating the overlap of projected intervals as an open interval instead of a closed interval would lose the valid point at the boundary.

## Approaches

A direct brute-force idea is to parameterize both segments and search through possible positions of (A). For a fixed (A), we can test whether the ray (A+t\vec v), (t\geq0), intersects (b). The difficulty is that the parameter of (A) is continuous. Sampling (K) positions gives (O(K)) work per test, or (50,000K) samples in the worst case. Even with (K=10^5), that is (5\cdot10^9) samples. More fundamentally, finite sampling is not an exact algorithm because a valid blocking point can lie between two samples.

The exact formulation initially looks like a system with three continuous variables, the position on (a), the position on (b), and the distance travelled along (\vec v). Solving that system separately for every possible configuration is unnecessarily complicated. The useful observation is that the direction condition has two independent parts. The displacement (B-A) must have no component perpendicular to (\vec v), and its component along (\vec v) must be positive.

Define two coordinates for any point (P=(x,y)):

[
q(P)=\operatorname{cross}(\vec v,P)=v_x y-v_y x
]

and

[
p(P)=\operatorname{dot}(\vec v,P)=v_xx+v_yy.
]

The value (q) measures the position perpendicular to the viewing direction, up to a constant scale. The value (p) measures the position along the viewing direction, also up to a constant scale.

Now suppose (B-A=t\vec v). Then

# \operatorname{cross}(\vec v,B-A)

# \operatorname{cross}(\vec v,t\vec v)

1. 

]

So (A) and (B) must have the same (q)-coordinate.

At the same time,

# \operatorname{dot}(\vec v,B-A)

t|\vec v|^2.
]

Since (t>0), we need (p(B)>p(A)). Because the segments are guaranteed to be non-intersecting, equality cannot occur for a valid pair, so checking (p(B)\geq p(A)) is also safe.

The (q)-values of a segment form an interval because (q) is linear along the segment. Thus the two segments can possibly block each other only if their (q)-intervals overlap.

Inside that overlap, the point of each segment with a given (q)-coordinate is determined by linear interpolation. Consequently, (p_A(q)) and (p_B(q)) are linear functions. Their difference

[
d(q)=p_B(q)-p_A(q)
]

is also linear. A linear function on a closed interval reaches its maximum at one of the two endpoints. Therefore we only have to inspect the two endpoints of the overlapping (q)-interval.

This is the key reduction. A continuous existence problem becomes two exact comparisons of rational numbers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force sampling | (O(K)) per test | (O(1)) | Too slow and not exact |
| Optimal projection method | (O(1)) per test | (O(1)) | Accepted |

## Algorithm Walkthrough

1. For every endpoint of both segments, compute its perpendicular coordinate (q=\operatorname{cross}(\vec v,P)) and its parallel coordinate (p=\operatorname{dot}(\vec v,P)). These two integer values completely describe the point for the purpose of this problem.
2. For each segment, take the minimum and maximum of its two (q)-values. These are exactly the range of perpendicular coordinates covered by that segment.
3. Compute the intersection of the two (q)-ranges. If the left endpoint is greater than the right endpoint, the ranges are disjoint, so no pair of points can have equal (q)-coordinates. The answer is immediately `No`.
4. Let the overlap be ([L,R]). For a particular value (q=t) inside a segment's range, recover its (p)-coordinate by linear interpolation. If the segment endpoints have coordinates ((q_0,p_0)) and ((q_1,p_1)), then

[
p(t)=
\frac{p_0(q_1-t)+p_1(t-q_0)}
{q_1-q_0}.
]

If (q_0=q_1), the segment is parallel to (\vec v), so its (q)-coordinate is constant and its (p)-coordinate at the only relevant (q) is simply its endpoint (p).

1. Evaluate both segments at (q=L). Compare their (p)-coordinates. We need (p_B(L)\geq p_A(L)).
2. Evaluate both segments at (q=R) and perform the same comparison. Since (p_B(q)-p_A(q)) is linear over the overlap, if it is non-negative anywhere, it is non-negative at one of these two endpoints.
3. Compare the interpolated values using cross multiplication instead of floating point. If

[
p_A=\frac{n_A}{d_A},
\qquad
p_B=\frac{n_B}{d_B},
]

with positive denominators, then

[
p_B\geq p_A
]

is equivalent to

[
n_Bd_A\geq n_Ad_B.
]

Python integers have arbitrary precision, so these products are safe.

Why it works: for every perpendicular coordinate (q) in the overlap, there is one corresponding point on each segment, except that a segment parallel to (\vec v) has only one possible (q). The condition that the two points lie on the same viewing ray is exactly (p_B(q)>p_A(q)). The difference of the two (p)-coordinates is linear in (q), so its maximum over the overlap is attained at (L) or (R). The algorithm checks both, hence it finds a valid pair exactly when one exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(data):
    ax1, ay1, ax2, ay2, bx1, by1, bx2, by2, vx, vy = data

    def coords(x, y):
        # q: coordinate perpendicular to v
        # p: coordinate along v
        q = vx * y - vy * x
        p = vx * x + vy * y
        return q, p

    a0 = coords(ax1, ay1)
    a1 = coords(ax2, ay2)
    b0 = coords(bx1, by1)
    b1 = coords(bx2, by2)

    aq0, ap0 = a0
    aq1, ap1 = a1
    bq0, bp0 = b0
    bq1, bp1 = b1

    left = max(min(aq0, aq1), min(bq0, bq1))
    right = min(max(aq0, aq1), max(bq0, bq1))

    if left > right:
        return False

    def value_at(q0, p0, q1, p1, q):
        if q0 == q1:
            return p0, 1

        den = q1 - q0
        num = p0 * (q1 - q) + p1 * (q - q0)

        if den < 0:
            den = -den
            num = -num

        return num, den

    for q in (left, right):
        an, ad = value_at(aq0, ap0, aq1, ap1, q)
        bn, bd = value_at(bq0, bp0, bq1, bp1, q)

        if bn * ad >= an * bd:
            return True

    return False

def main():
    t = int(input())
    out = []

    for _ in range(t):
        data = list(map(int, input().split()))
        out.append("Yes" if solve_case(data) else "No")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The `coords` function performs the central coordinate transformation. The cross product gives the perpendicular coordinate, while the dot product gives the coordinate along the viewing direction. No normalization by (|\vec v|) is needed because multiplying either coordinate system by a common positive scale does not change comparisons.

The next four lines compute the two (q)-intervals and intersect them. The endpoints are included because a blocking point is allowed to be an endpoint of either segment.

The `value_at` function performs exact linear interpolation. The denominator is normalized to be positive so that all later comparisons have the same direction. The special case `q0 == q1` is required because a segment parallel to the viewing direction has a constant perpendicular coordinate.

The final loop checks only `left` and `right`. These are not arbitrary sample points. They are the endpoints of the entire feasible range of perpendicular coordinates, and the difference between the two parallel coordinates is linear on that range.

There is no floating-point arithmetic anywhere in the solution. This matters because two segments can be separated by a very small exact difference after projection, and a floating-point comparison could change the answer. The largest intermediate values are much larger than (10^6), but Python's integers grow automatically, so there is no overflow issue.

## Worked Examples

The first sample uses

```
0 2 1 1 2 2 3 1 1 1
```

Here (\vec v=(1,1)), so (q=y-x) and (p=x+y).

| Quantity | Segment (a) | Segment (b) |
| --- | --- | --- |
| First endpoint ((q,p)) | ((2,2)) | ((0,4)) |
| Second endpoint ((q,p)) | ((0,2)) | ((-2,4)) |
| (q)-range | ([0,2]) | ([-2,0]) |
| Overlap | ([0,0]) | ([0,0]) |
| (p_A(0)) | (2) |  |
| (p_B(0)) |  | (4) |
| (p_B-p_A) |  | (2>0) |
| Answer |  | `Yes` |

The overlap consists of the single perpendicular coordinate (q=0). At that coordinate, segment (a) contributes (p=2), while segment (b) contributes (p=4). Thus the second segment is farther along the viewing direction, and a point on (a) can move along ((1,1)) to reach (b).

The second sample case is

```
0 2 1 1 2 2 3 1 -1 -1
```

Now (\vec v=(-1,-1)), giving (q=x-y) and (p=-x-y).

| Quantity | Segment (a) | Segment (b) |
| --- | --- | --- |
| First endpoint ((q,p)) | ((-2,-2)) | ((0,-4)) |
| Second endpoint ((q,p)) | ((0,-2)) | ((2,-4)) |
| (q)-range | ([-2,0]) | ([0,2]) |
| Overlap | ([0,0]) | ([0,0]) |
| (p_A(0)) | (-2) |  |
| (p_B(0)) |  | (-4) |
| (p_B-p_A) |  | (-2<0) |
| Answer |  | `No` |

The same geometric segments are being viewed in the opposite direction. The perpendicular coordinates still meet, but the second segment is now behind the first in the (p)-coordinate. The direction test is what changes the answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Each test case performs a constant number of cross products, dot products, interpolations, and integer comparisons |
| Space | (O(1)) auxiliary | Only a constant number of integer coordinates are stored for one test case |

With at most (50,000) test cases, the algorithm performs only a constant amount of arithmetic per case, so the total work is linear in the number of test cases. The input itself is the dominant source of data, and the solution comfortably fits the 2 second and 512 MB limits.

## Test Cases

```python
import sys
import io

def blocking(data):
    ax1, ay1, ax2, ay2, bx1, by1, bx2, by2, vx, vy = data

    def coords(x, y):
        return vx * y - vy * x, vx * x + vy * y

    aq0, ap0 = coords(ax1, ay1)
    aq1, ap1 = coords(ax2, ay2)
    bq0, bp0 = coords(bx1, by1)
    bq1, bp1 = coords(bx2, by2)

    left = max(min(aq0, aq1), min(bq0, bq1))
    right = min(max(aq0, aq1), max(bq0, bq1))

    if left > right:
        return False

    def value_at(q0, p0, q1, p1, q):
        if q0 == q1:
            return p0, 1

        den = q1 - q0
        num = p0 * (q1 - q) + p1 * (q - q0)

        if den < 0:
            den = -den
            num = -num

        return num, den

    for q in (left, right):
        an, ad = value_at(aq0, ap0, aq1, ap1, q)
        bn, bd = value_at(bq0, bp0, bq1, bp1, q)

        if bn * ad >= an * bd:
            return True

    return False

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input_fn = sys.stdin.readline

    t = int(input_fn())
    ans = []

    for _ in range(t):
        data = list(map(int, input_fn().split()))
        ans.append("Yes" if blocking(data) else "No")

    return "\n".join(ans)

# Provided sample
sample = """\
2
0 2 1 1 2 2 3 1 1 1
0 2 1 1 2 2 3 1 -1 -1
"""
assert run(sample) == "Yes\nNo", "provided sample"

# Minimum-size case: two horizontal, disjoint segments, second is ahead.
assert run("""\
1
0 0 1 0 2 0 3 0 1 0
""") == "Yes", "minimum-size positive case"

# Same line, but the second segment is behind the first.
assert run("""\
1
0 0 1 0 -3 0 -2 0 1 0
""") == "No", "wrong direction"

# Perpendicular projections do not overlap.
assert run("""\
1
0 0 1 0 0 2 1 2 1 0
""") == "No", "disjoint perpendicular projections"

# First segment is parallel to the viewing direction.
assert run("""\
1
0 0 1 0 2 0 2 1 1 0
""") == "Yes", "parallel segment with a boundary witness"

# Equal direction components, testing a non-axis-aligned direction.
assert run("""\
1
0 0 1 1 2 2 3 3 1 1
""") == "Yes", "equal direction components"

# Maximum number of test cases.
one = "0 0 1 0 2 0 3 0 1 0\n"
large_input = "50000\n" + one * 50000
large_output = run(large_input)
assert large_output.count("Yes") == 50000, "maximum number of tests"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 1 0 2 0 3 0 1 0` | `Yes` | Minimum-size positive case |
| `0 0 1 0 -3 0 -2 0 1 0` | `No` | Correct orientation along the viewing direction |
| `0 0 1 0 0 2 1 2 1 0` | `No` | Disjoint perpendicular-coordinate intervals |
| `0 0 1 0 2 0 2 1 1 0` | `Yes` | Zero interpolation denominator and boundary overlap |
| `0 0 1 1 2 2 3 3 1 1` | `Yes` | Non-axis-aligned direction with equal components |
| 50,000 repeated valid cases | 50,000 `Yes` lines | Maximum number of test cases |

## Edge Cases

The first edge case is a perpendicular-coordinate boundary. Consider

```
1
0 0 1 0 2 0 2 1 1 0
```

For (\vec v=(1,0)), we have (q=y) and (p=x). Segment (a) has (q)-range ([0,0]), while segment (b) has (q)-range ([0,1]). Their overlap is exactly (q=0). At that coordinate, (a) has (p=0) to (1), while (b) has (p=2), so the comparison succeeds and the answer is `Yes`. The closed interval is essential here.

The second edge case is a segment parallel to the viewing direction. In the same input, segment (a) has (q_0=q_1=0). The interpolation routine detects this before dividing. Its (p)-coordinate is taken directly from the endpoint, and the algorithm compares it with the point where segment (b) reaches (q=0). This gives `Yes` without any division by zero.

The third edge case is two collinear segments pointing in the wrong order:

```
1
0 0 1 0 -3 0 -2 0 1 0
```

Both (q)-ranges are ([0,0]), so the perpendicular condition alone says that a possible alignment exists. At (q=0), however, the first segment has (p)-values from (0) to (1), while the second has (p)-values from (-3) to (-2). The second segment is behind the first, so (p_B<p_A) everywhere and the answer is `No`.

The fourth edge case is completely disjoint perpendicular projections:

```
1
0 0 1 0 0 2 1 2 1 0
```

The first segment has (q=0), while the second has (q=2). The intersection of the ranges is empty, so the algorithm stops before interpolation and returns `No`. This avoids accidentally treating segments with nearby but different projection coordinates as aligned.

The fifth edge case is the zero-distance boundary of the direction test. In this problem the segments are guaranteed not to intersect, so if (q_A=q_B) and (p_A=p_B), the points would actually be identical, contradicting the input guarantee. Consequently, the implementation can use `>=` in the final comparison without accidentally accepting a zero-length displacement. For the given input class, every accepted pair has a genuinely positive displacement along (\vec v).

If you want, I can also turn this into a shorter Codeforces-style editorial with the same proof and code but less exposition.
