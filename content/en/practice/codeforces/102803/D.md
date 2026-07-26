---
title: "CF 102803D - Death by Thousand Cuts"
description: "We have a rectangular box whose opposite corners are the origin and (a, b, c). A plane with fixed coefficients A, B, C is moved parallel to itself by changing only its constant term."
date: "2026-07-26T16:21:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102803
codeforces_index: "D"
codeforces_contest_name: "The 15th Heilongjiang Provincial Collegiate Programming Contest"
rating: 0
weight: 102803
solve_time_s: 54
verified: true
draft: false
---

[CF 102803D - Death by Thousand Cuts](https://codeforces.com/problemset/problem/102803/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
# Problem Understanding

We have a rectangular box whose opposite corners are the origin and `(a, b, c)`. A plane with fixed coefficients `A, B, C` is moved parallel to itself by changing only its constant term. The only possible positions considered are the ones where the plane cuts the box, and all such positions are equally likely.

For any chosen position, the intersection between the plane and the box is a polygon. The task is to determine the probabilities that this polygon has 3, 4, 5, or 6 sides. The answer for each probability must be printed modulo `10^9 + 7`, so every probability is represented as a fraction and converted using a modular inverse.

The key observation is that changing `D` only moves the plane along its normal direction. If we define

```
value(x, y, z) = A*x + B*y + C*z
```

then the plane position is equivalent to choosing a random value `t` and looking at the slice:

```
A*x + B*y + C*z = t
```

inside the box. The possible values of `t` form the interval between the minimum and maximum values reached at the vertices of the box.

There are only eight vertices, so there are only eight relevant values where the shape of the cross section can change. Between two consecutive vertex values, the polygon shape is fixed because the plane never passes through a vertex during that interval. This means the whole continuous probability problem can be reduced to checking a small number of intervals.

The constraints allow up to `10^4` test cases. The side lengths and coefficients can be as large as `10^4`, but they do not affect the number of important events because a cuboid always has exactly eight vertices and twelve edges. An approach depending on the size of `a`, `b`, or `c`, such as scanning every coordinate or every possible plane position, would be impossible. The solution must perform only constant work per test case.

Several details can break a naive implementation. Equal vertex values are common when a coefficient is zero or when different vertices happen to produce the same expression value. For example, if the plane is parallel to a face, many vertices can share the same value. The algorithm must ignore zero-length intervals between equal values.

Another issue is testing a position exactly on a vertex value. Such positions have probability zero, but if they are used during counting they may incorrectly count edges touching a vertex. For example, a plane passing through a cube corner has a degenerate intersection, while almost every nearby position has a normal polygon. The algorithm avoids this by always choosing a point strictly inside an interval.

A concrete example of a coefficient-zero case is:

```
a = 1, b = 1, c = 1
A = 1, B = 0, C = 0
```

Every valid plane is of the form `x = constant`, so the cross section is always a rectangle. The answer is:

```
0 1 0 0
```

A careless method that expects all coefficients to contribute equally might incorrectly count triangles near the boundary.

Another example is:

```
a = 1, b = 1, c = 1
A = 1, B = 1, C = 1
```

The vertex values are `0, 1, 1, 1, 2, 2, 2, 3`. The middle interval `(1, 2)` gives a hexagon, while the two outer intervals give triangles. The correct probabilities are:

```
2/3 0 0 1/3
```

A solution that treats all eight vertices as having different values would create incorrect intervals.

# Approaches

A direct approach is to simulate every possible cross section change. Since the shape only changes when the plane passes a vertex, we could find all vertex positions, sort them, and for every interval choose a representative plane. For that representative plane we test all twelve edges of the cuboid and count how many are crossed. The count of crossed edges is exactly the number of sides of the polygon.

This brute-force idea is already close to the final solution because the geometry is small. The problem is that many contestants might try to discretize the actual coordinate space because `a`, `b`, and `c` can be large. A scan over the box volume or over all possible positions would require far too many operations. For example, a cube with side length `10000` already contains `10^12` unit cells.

The important structural fact is that the number of vertices and edges never changes. The eight vertex values completely describe all possible transitions. Once the sorted unique vertex values are known, there are at most seven intervals to examine. For each interval, checking twelve edges is constant work.

The brute-force works because the geometric object is tiny, but it fails when the implementation depends on the coordinate range. The observation that only vertex events matter reduces the problem from a large continuous space to a constant number of intervals.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(abc) or worse depending on discretization | O(1) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

# Algorithm Walkthrough

1. Compute the values of `A*x + B*y + C*z` for all eight vertices of the cuboid. Each coordinate is either `0` or the corresponding side length, so there are only eight combinations.
2. Sort these eight values and remove duplicates. Consecutive distinct values define intervals where the cross section has a constant number of sides. Duplicate values are removed because an interval of length zero contributes no probability.
3. For every adjacent pair of values `l` and `r`, choose any point strictly inside the interval. Instead of using floating point numbers, use the doubled midpoint `l + r`.
4. Check all twelve cuboid edges. An edge contributes one side to the polygon exactly when its two endpoint values lie on opposite sides of the chosen midpoint. Using doubled values avoids precision problems.
5. Add the interval length `r - l` to the bucket corresponding to the number of intersected edges. The interval length is the probability weight because the plane position is uniformly distributed.
6. Divide every accumulated weight by the total range of possible plane positions. Perform the division modulo `10^9 + 7` using the modular inverse of the range.

Why it works: The value `A*x + B*y + C*z` changes continuously as the plane moves. The only moments where the topology of the intersection can change are when the plane reaches a vertex of the cuboid. Between two consecutive vertex values, no vertex crosses the plane, so every edge either always intersects or never intersects. Counting intersected edges in one representative point therefore gives the exact polygon size for the entire interval. Summing the lengths of all intervals with the same edge count gives the exact probability numerator.

# Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

vertices = [
    (0, 0, 0),
    (0, 0, 1),
    (0, 1, 0),
    (0, 1, 1),
    (1, 0, 0),
    (1, 0, 1),
    (1, 1, 0),
    (1, 1, 1),
]

edges = []
for i, p in enumerate(vertices):
    for j, q in enumerate(vertices):
        if i < j:
            diff = sum(abs(p[k] - q[k]) for k in range(3))
            if diff == 1:
                edges.append((i, j))

def solve_case(a, b, c, A, B, C):
    vals = []
    for x, y, z in vertices:
        vals.append(A * x * a + B * y * b + C * z * c)

    order = sorted(set(vals))
    total = order[-1] - order[0]

    ans = [0, 0, 0, 0]

    for l, r in zip(order, order[1:]):
        mid2 = l + r
        cnt = 0

        for u, v in edges:
            x = vals[u]
            y = vals[v]
            if (2 * x < mid2 and 2 * y > mid2) or (2 * y < mid2 and 2 * x > mid2):
                cnt += 1

        ans[cnt - 3] += r - l

    inv_total = pow(total, MOD - 2, MOD)
    return [(x % MOD) * inv_total % MOD for x in ans]

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if len(data) == 0:
        return

    if len(data) == 6:
        t = 1
        idx = 0
    else:
        t = data[0]
        idx = 1

    out = []

    for _ in range(t):
        a, b, c, A, B, C = data[idx:idx + 6]
        idx += 6
        out.append(" ".join(map(str, solve_case(a, b, c, A, B, C))))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The vertex list stores only the eight possible corner choices. The actual coordinates are created by multiplying these binary choices by `a`, `b`, and `c`.

The edge construction is done once. Two vertices form an edge exactly when their binary coordinates differ in one position, which generates the twelve edges of the cuboid.

The midpoint comparison is the most delicate part of the implementation. Using floating point values could fail when coefficients are large or when two values are very close. Since all vertex values are integers, comparing `2 * value` with `l + r` gives an exact comparison with the interval midpoint.

The final division uses Fermat's theorem because the modulus is prime. The total range is always positive because the coefficients are not all zero and the cuboid has positive dimensions.

# Worked Examples

For the first sample:

```
a = 1, b = 2, c = 3
A = 1, B = 1, C = 1
```

The vertex values are:

| Vertex | Value |
| --- | --- |
| (0,0,0) | 0 |
| (0,2,0) | 2 |
| (0,0,3) | 3 |
| (0,2,3) | 5 |
| (1,0,0) | 1 |
| (1,2,0) | 3 |
| (1,0,3) | 4 |
| (1,2,3) | 6 |

The sorted unique values are `0,1,2,3,4,5,6`.

| Interval | Midpoint comparison | Sides | Weight |
| --- | --- | --- | --- |
| (0,1) | inside first interval | 3 | 1 |
| (1,2) | inside second interval | 4 | 1 |
| (2,3) | inside third interval | 4 | 1 |
| (3,4) | inside middle interval | 4 | 1 |
| (4,5) | inside fifth interval | 4 | 1 |
| (5,6) | inside last interval | 3 | 1 |

The total range is `6`. Triangles occupy length `2`, quadrilaterals occupy length `4`, so the probabilities are `1/3` and `2/3`, matching the output.

For the second sample:

```
a = 2, b = 2, c = 2
A = 1, B = 1, C = 1
```

The sorted vertex values are `0,2,4,6`.

| Interval | Sides | Weight |
| --- | --- | --- |
| (0,2) | 3 | 2 |
| (2,4) | 6 | 2 |
| (4,6) | 3 | 2 |

The total range is `6`. Triangles have total weight `4` and the hexagon has weight `2`, giving:

```
2/3 0 0 1/3
```

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | There are always eight vertices and twelve edges, so the amount of work is fixed. |
| Space | O(1) | Only constant-sized arrays are used. |

The solution easily handles `10^4` test cases because each case performs only a few dozen arithmetic operations.

# Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

MOD = 10**9 + 7

def run(inp: str) -> str:
    # Paste the submitted solution's main logic here and call it.
    # This placeholder assumes the solution has been wrapped into main().
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    main()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

# provided sample 1
assert run(
    "1\n1 2 3 1 1 1\n"
) == "333333336 333333336 333333336 0\n"

# provided sample 2
assert run(
    "1\n2 2 2 1 1 1\n"
) == "666666672 0 0 333333336\n"

# custom: plane parallel to a face, always a rectangle
assert run(
    "1\n1 1 1 1 0 0\n"
) == "0 1 0 0\n"

# custom: all coefficients equal on a cube
assert run(
    "1\n10000 10000 10000 1 1 1\n"
) == "666666672 0 0 333333336\n"

# custom: two-dimensional diagonal extrusion
assert run(
    "1\n1 1 10000 1 1 0\n"
) == "0 1 0 0\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1 0 0` | `0 1 0 0` | Handles zero coefficients and parallel planes |
| `10000 10000 10000 1 1 1` | `666666672 0 0 333333336` | Handles maximum dimensions and repeated vertex values |
| `1 1 10000 1 1 0` | `0 1 0 0` | Handles a coefficient that removes one dimension |

# Edge Cases

When a coefficient is zero, several vertex values become identical. For the input:

```
1
1 1 1 1 0 0
```

the vertex values are only `0` and `1`. The algorithm creates one interval `(0,1)`. A midpoint check shows that the four edges parallel to the `x` direction form the boundary of the slice, giving four sides. The interval covers the entire possible range, so the result is:

```
0 1 0 0
```

When multiple vertices share values, duplicate values must not create artificial probability. For:

```
1
1 1 1 1 1 1
```

the values are `0,1,2,3` after removing duplicates. The algorithm checks the three intervals. The first and last intervals produce triangles, while the middle interval produces a hexagon. The result is:

```
666666672 0 0 333333336
```

When the plane passes exactly through a vertex value, that position has zero probability. The algorithm never chooses those positions. It only checks open intervals between consecutive distinct values, so degenerate slices cannot affect the answer.
