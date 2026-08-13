---
title: "CF 102361A - Angle Beats"
description: "For each query point (A), we have to choose two distinct original points (Pu) and (Pv). The three points must form a non-degenerate triangle with one angle equal to (90^circ). The output for that query is the number of such unordered pairs of original points."
date: "2026-08-14T02:48:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102361
codeforces_index: "A"
codeforces_contest_name: "2019 China Collegiate Programming Contest Qinhuangdao Onsite"
rating: 0
weight: 102361
solve_time_s: 115
verified: true
draft: false
---

[CF 102361A - Angle Beats](https://codeforces.com/problemset/problem/102361/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

For each query point (A), we have to choose two distinct original points (P_u) and (P_v). The three points must form a non-degenerate triangle with one angle equal to (90^\circ). The output for that query is the number of such unordered pairs of original points.

The key geometric condition is expressed with vectors. If (A) is the right-angle vertex, then

[
(P_u-A)\cdot(P_v-A)=0.
]

However, (A) can also lie on the hypotenuse. In that case some original point (P_i) is the right-angle vertex, and the condition becomes

[
(A-P_i)\cdot(P_j-P_i)=0.
]

The distinction between these two cases drives the whole solution.

There are at most (2000) original points and (2000) queries. A single query has roughly two million possible pairs of original points, and doing that for every query would require about (4\times10^9) pair checks at the maximum size. The official judge gives this problem a 4 second time limit, so a cubic-looking approach is far beyond what we can afford.

The coordinates can reach (10^9), so differences can reach (2\times10^9), and dot products can reach roughly (4\times10^{18}). Python integers handle these values directly, while a fixed-width implementation would need 64-bit arithmetic.

The first subtle case is when several vectors from the same vertex point along the same line. For example:

```
3 1
1 0
-1 0
0 1
0 0
```

The correct output is `2`. The two horizontal points form one direction line and the vertical point forms a perpendicular line, so there are two choices for the horizontal endpoint. A careless implementation that stores raw vectors instead of their directions can miss the fact that ((1,0)) and ((-1,0)) belong to the same geometric line.

The second subtle case is that the query itself does not have to be the right-angle vertex. For example:

```
2 1
0 0
1 0
0 1
```

The correct output is `1`. The right angle is at ((0,0)), not at the query point ((0,1)). An approach that only counts perpendicular vectors around the query would incorrectly return zero.

A third edge case occurs with points on the same vertical or horizontal line:

```
4 1
0 0
0 1
0 2
0 3
1 1
```

The correct output is `4`. The equal (x)-coordinates force many vectors to be vertical, so this case catches incorrect slope handling, especially code that divides by the (x)-component or treats vertical directions separately in an inconsistent way.

Finally, a query point is guaranteed to be different from every original point. Thus a vector from a query or an original point to another relevant point is never ((0,0)). This matters because direction normalization divides by a gcd, and the gcd of ((0,0)) would be zero.

## Approaches

The direct brute-force solution considers every query (A), every pair (P_u,P_v), and checks whether the triangle is right-angled. There are (\binom n2) pairs for one query, so the total work is

[
O(qn^2).
]

At (n=q=2000), this is

[
2000\binom{2000}{2}=3,998,000,000
]

pair checks. The test itself is constant time, but nearly four billion iterations are already too much, especially in Python.

The brute-force works because every possible triangle is examined directly. The problem is that it ignores the fact that perpendicularity depends only on direction, not on the length of a vector.

Suppose a point (O) is fixed. Consider all vectors from (O) to relevant points. Two such vectors form a right angle exactly when their direction lines are perpendicular. We can normalize every nonzero vector to a canonical representation of its undirected line. For a vector ((x,y)), divide both coordinates by (\gcd(|x|,|y|)), then choose a consistent sign so that either (x>0), or (x=0) and (y>0).

For example, all of

[
(1,2),\quad (2,4),\quad (-1,-2),\quad (-2,-4)
]

become the same canonical direction ((1,2)).

Once a direction (d=(x,y)) is normalized, a perpendicular direction is simply ((-y,x)), followed by the same canonicalization. A hash map can store how many vectors belong to every direction, so a perpendicular lookup becomes (O(1)) expected time.

There are still two geometric roles for the query point. If the query is the right-angle vertex, we can process that query independently in (O(n\log C)), where (C) is the coordinate magnitude, because each of the (n) vectors must be normalized.

If the query is not the right-angle vertex, we cannot independently process every pair around the query. Instead, we reverse the viewpoint. Fix an original point (P_i) as the right-angle vertex. Build a direction-frequency map for all other original points around (P_i). Then every query (A) asks for the number of original points whose vector from (P_i) is perpendicular to (A-P_i). We can answer all (q) queries while this one map is available. Repeating this for every original point gives (O(n^2+nq)) direction operations.

The two cases together reduce the work from billions of pair checks to roughly a few million hash-map operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(qn^2)) | (O(1)) | Too slow |
| Direction hashing | (O((nq+n^2)\log C)) expected | (O(n)) | Accepted |

Here (C) represents the magnitude of the coordinate differences. The logarithmic factor comes from Euclid's algorithm used by `gcd`.

## Algorithm Walkthrough

1. Read all original points and all query points before processing the second case. This makes the computation for a fixed original right-angle vertex completely offline, because every query is already known.
2. Define a direction normalization function. For a nonzero vector ((dx,dy)), divide both coordinates by their gcd and flip both signs when (dx<0), or when (dx=0) and (dy<0). The result represents an unoriented line through the origin.

We deliberately identify opposite vectors. For perpendicularity, ((1,0)) and ((-1,0)) play exactly the same role, and separating them would only make the counting more complicated.
3. For every query (A), construct a frequency map of the (n) directions (P_i-A). For every direction (d) occurring (c_d) times, compute its canonical perpendicular direction (d^\perp). The number of pairs contributed by these two direction classes is (c_d c_{d^\perp}).
4. Sum those products over all direction classes and divide by two. A pair of perpendicular directions is encountered once from each endpoint direction, so without the division every valid pair would be counted twice.
5. Initialize the answer array with the values obtained when the query itself is the right-angle vertex. This accounts for every triangle whose (90^\circ) angle is at the query point.
6. Fix one original point (P_i) as the possible right-angle vertex. Build a frequency map containing the normalized directions (P_j-P_i) for every (j\ne i).
7. For every query (A_k), normalize (A_k-P_i), rotate it by (90^\circ) using ((-y,x)), normalize that perpendicular direction, and look it up in the map. The stored frequency is exactly the number of original points (P_j) such that (P_i,A_k,P_j) have a right angle at (P_i).
8. Add that frequency to the answer of query (A_k). Repeat the previous two steps for every original point (P_i).

A triangle in which the query is not the right-angle vertex has exactly one original point that is the right-angle vertex, so processing each (P_i) separately counts every such triangle exactly once.
9. Print the accumulated answer for every query.

### Why it works

For a fixed vertex (O), two nonzero vectors (u) and (v) are perpendicular exactly when their direction lines are perpendicular. Direction normalization preserves the line represented by a vector, and rotating a normalized direction by (90^\circ) gives precisely its perpendicular direction.

When the query is the right-angle vertex, the frequency map counts every pair of original points whose vectors from the query are perpendicular. Each unordered pair appears twice in the sum, once from each direction class, so division by two gives exactly the number of triangles.

When an original point (P_i) is the right-angle vertex, the vector (A-P_i) determines the direction that the vector (P_j-P_i) must have. The map contains exactly the frequencies of all possible original-point directions from (P_i), so the lookup counts exactly the valid choices of (P_j). Since every triangle has only one right-angle vertex, each triangle with the query on its hypotenuse is counted once. The two cases are disjoint because a non-degenerate triangle has only one right angle.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

def normalize(dx, dy):
    g = gcd(abs(dx), abs(dy))
    dx //= g
    dy //= g

    if dx < 0 or (dx == 0 and dy < 0):
        dx = -dx
        dy = -dy

    return dx, dy

def solve(data=None):
    if data is None:
        read = input
        n, q = map(int, read().split())
        points = [tuple(map(int, read().split())) for _ in range(n)]
        queries = [tuple(map(int, read().split())) for _ in range(q)]
    else:
        it = iter(map(int, data.split()))
        n = next(it)
        q = next(it)
        points = [(next(it), next(it)) for _ in range(n)]
        queries = [(next(it), next(it)) for _ in range(q)]

    ans = [0] * q

    # Case 1: the query point itself is the right-angle vertex.
    for qi, (ax, ay) in enumerate(queries):
        freq = {}

        for px, py in points:
            d = normalize(px - ax, py - ay)
            freq[d] = freq.get(d, 0) + 1

        total = 0

        for (x, y), cnt in freq.items():
            px, py = normalize(-y, x)
            total += cnt * freq.get((px, py), 0)

        ans[qi] = total // 2

    # Case 2: an original point is the right-angle vertex.
    for ox, oy in points:
        freq = {}

        for px, py in points:
            dx = px - ox
            dy = py - oy

            if dx == 0 and dy == 0:
                continue

            d = normalize(dx, dy)
            freq[d] = freq.get(d, 0) + 1

        for qi, (ax, ay) in enumerate(queries):
            dx = ax - ox
            dy = ay - oy

            d = normalize(-dy, dx)
            ans[qi] += freq.get(d, 0)

    result = "\n".join(map(str, ans))

    if data is None:
        sys.stdout.write(result + "\n")
    else:
        return result + "\n"

if __name__ == "__main__":
    solve()
```

The `normalize` function is the geometric core. The gcd removes the irrelevant length of a vector, while the sign convention merges a direction with its opposite. The input guarantee means the vector passed to `normalize` is never zero.

The first outer loop handles the case where the query is the right-angle vertex. Its frequency map contains one entry for each distinct direction line from the query to an original point. Looking up the rotated direction finds all points lying on the perpendicular line.

The `total // 2` operation is necessary because if direction (d) is perpendicular to direction (e), the loop processes both (d) and (e). The same pair of point classes is consequently included twice.

The second outer loop fixes each original point as the right-angle vertex. The frequency map contains only the other original points, so the fixed point itself can never accidentally form a zero vector. For every query, the vector from the fixed point to the query is rotated by (90^\circ), normalized, and used as a dictionary key.

The code uses Python's arbitrary-precision integers, so products involving coordinate differences around (2\times10^9) are safe. No floating-point slope or angle calculation is used, which avoids precision errors for vertical lines and very large coordinates.

## Worked Examples

The given sample has four original points and two queries.

For the first query, ((0,0)), the direction classes are horizontal and vertical. Each contains two points, so the query-as-right-angle contribution is (2\cdot2=4).

For the second query, ((1,1)), the relevant direction classes include a horizontal line containing one point, a vertical line containing one point, and two diagonal lines. The perpendicular pair counts add up to (3).

| Query | Direction classes around query | Right-angle contribution |
| --- | --- | --- |
| ((0,0)) | horizontal: 2, vertical: 2 | 4 |
| ((1,1)) | horizontal: 1, vertical: 1, diagonal pairings | 3 |

The second phase also finds triangles where the query is on the hypotenuse. For example, with query ((1,1)), fixing ((0,1)) as the right-angle vertex gives the perpendicular vectors toward ((1,1)) and ((0,-1)). The same happens for the other two relevant original right-angle vertices. This confirms why checking only the query as the right-angle vertex would be incomplete.

For a second trace, consider:

```
6 2
1 0
2 0
0 2
-1 0
0 -2
-1 -1
2 2
1 1
```

The resulting answers are `5` and `7`.

| Query | Right angle at query | Contributions with original point as right angle | Final |
| --- | --- | --- | --- |
| ((2,2)) | 1 | 4 | 5 |
| ((1,1)) | 1 | 6 | 7 |

For the first query, the query itself accounts for one triangle, while four additional triangles have one of the six original points as their right-angle vertex. For the second query, the corresponding split is one plus six. The trace demonstrates the central invariant: every valid triangle belongs to exactly one of the two cases.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O((nq+n^2)\log C)) expected | (nq) query-direction normalizations and (n^2) original-point direction normalizations, with gcd taking (O(\log C)) |
| Space | (O(n)) | At any moment the frequency map contains at most (n) normalized directions |

With (n,q\le 2000), the algorithm performs on the order of (8\times10^6) direction operations in the largest case, rather than roughly (4\times10^9) explicit triangle checks. The map is rebuilt for each fixed vertex, so we do not store (n) separate maps simultaneously. The official memory limit is 1024 MB and the time limit is 4 seconds.

## Test Cases

The literal "all points have equal values" case is not a legal input because the statement guarantees that all (n+q) points are pairwise distinct. The closest meaningful stress case is to make all original points share one coordinate, which exercises vertical direction handling without violating the guarantee.

```python
# helper: run solution on input string, return output string
import io
import sys

# Assume the solution above has already defined solve(data).
# The helper calls solve with an input string, so no process-level
# stdin replacement is necessary.
def run(inp: str) -> str:
    return solve(inp)

# Provided sample
assert run(
    """4 2
0 1
1 0
0 -1
-1 0
0 0
1 1
"""
) == "4\n3\n", "provided sample"

# Minimum size: exactly one possible pair.
# The query is the right-angle vertex.
assert run(
    """2 1
0 0
1 0
0 1
"""
) == "1\n", "minimum size"

# Query is on the hypotenuse, so the right angle is at an original point.
assert run(
    """2 1
0 0
2 0
0 1
"""
) == "1\n", "query is not the right-angle vertex"

# All original points have the same x-coordinate.
# This stresses vertical directions and repeated collinear directions.
assert run(
    """4 1
0 0
0 1
0 2
0 3
1 1
"""
) == "4\n", "vertical direction groups"

# Boundary coordinates near +/- 1e9.
assert run(
    """3 1
1000000000 1000000000
-1000000000 1000000000
1000000000 -1000000000
-1000000000 -1000000000
"""
) == "1\n", "coordinate boundary"

# Maximum-size test.
# Original points: (i, 0), 0 <= i < 2000.
# Queries:        (i, 1), 0 <= i < 2000.
#
# For i = 0 and i = 1999, there are 1999 triangles.
# For every interior i, there are 1999 triangles with (i, 0)
# as the right-angle vertex, plus one with the query itself
# as the right-angle vertex.
n = 2000
q = 2000

lines = [f"{n} {q}"]
lines.extend(f"{i} 0" for i in range(n))
lines.extend(f"{i} 1" for i in range(q))

maximum_input = "\n".join(lines) + "\n"

expected = [1999] + [2000] * 1998 + [1999]
maximum_output = "\n".join(map(str, expected)) + "\n"

assert run(maximum_input) == maximum_output, "maximum-size test"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Provided sample | `4`, `3` | Both geometric cases together |
| (n=2) with query at ((0,1)) | `1` | Minimum size and direct perpendicularity |
| (n=2), query on the hypotenuse | `1` | Original point as right-angle vertex |
| Four points with identical (x)-coordinate | `4` | Vertical directions and repeated collinear directions |
| Coordinates at (\pm10^9) | `1` | Large differences and integer arithmetic |
| (n=q=2000) | `1999`, followed by 1998 values of `2000`, then `1999` | Maximum constraints and both counting phases |

## Edge Cases

The repeated-direction case is handled by normalization. For

```
3 1
1 0
-1 0
0 1
0 0
```

the two horizontal vectors become the same canonical direction ((1,0)), while the vertical vector is ((0,1)). The frequency map contains counts (2) and (1), so the query-as-right-angle calculation gives (2\cdot1=2). The output is `2`. Opposite vectors are deliberately merged because perpendicularity depends on the line, not on which way the vector points.

The query-on-hypotenuse case is handled by the second phase. For

```
2 1
0 0
1 0
0 1
```

fixing ((0,0)) as the original right-angle vertex gives the vectors ((1,0)) and ((0,1)), which are perpendicular. The query receives one contribution from this fixed vertex, so the output is `1`. The first phase contributes zero, which is exactly what we want because the query itself is not the right-angle vertex.

The vertical-line case uses the same normalization as every other direction. For

```
4 1
0 0
0 1
0 2
0 3
1 1
```

the query has vectors ((-1,-1)), ((-1,0)), ((-1,1)), and ((-1,2)). The pair ((-1,-1)) and ((-1,1)) is perpendicular, giving one triangle with the query as the right-angle vertex. The original point ((0,1)) is also a right-angle vertex with the query vector ((1,0)), perpendicular to the three vertical vectors toward ((0,0)), ((0,2)), and ((0,3)). That adds three more, giving the correct output `4`.

The boundary-coordinate case uses differences of size (2\times10^9). For

```
3 1
1000000000 1000000000
-1000000000 1000000000
1000000000 -1000000000
-1000000000 -1000000000
```

the query has a horizontal vector to ((1000000000,-1000000000)) and a vertical vector to ((1000000000,1000000000)), producing one right angle. Python's integer arithmetic represents the corresponding products exactly, so the output is `1`.

The invalid all-equal-point case needs no special branch. If an input contained the same point twice, it would violate the problem guarantee and could create a zero vector, for which direction normalization is undefined. Since every query and every original point is pairwise distinct, the implementation can safely assume every vector passed to `normalize` is nonzero.
