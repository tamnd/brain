---
title: "CF 102420A - \u0417\u0430 \u0433\u0440\u043e\u0431\u043e\u0446\u0432\u0435\u0442\u0430\u043c\u0438"
description: "We have (n) hunters, and each hunter occupies a distinct point ((xi,yi)) on the plane. We need to choose three different hunters whose positions do not lie on one straight line. If such a triple exists, we print Yes and their indices."
date: "2026-08-10T11:33:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102420
codeforces_index: "A"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0422\u0440\u0435\u0442\u044c\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430, \u0443\u0441\u043b\u043e\u0436\u043d\u0435\u043d\u043d\u0430\u044f \u043d\u043e\u043c\u0438\u043d\u0430\u0446\u0438\u044f"
rating: 0
weight: 102420
solve_time_s: 1141
verified: true
draft: false
---

[CF 102420A - \u0417\u0430 \u0433\u0440\u043e\u0431\u043e\u0446\u0432\u0435\u0442\u0430\u043c\u0438](https://codeforces.com/problemset/problem/102420/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 19m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We have (n) hunters, and each hunter occupies a distinct point ((x_i,y_i)) on the plane. We need to choose three different hunters whose positions do not lie on one straight line. If such a triple exists, we print `Yes` and their indices. If every hunter lies on the same line, we print `No`.

The distinction between these two cases is geometric but can be checked with integer arithmetic. For three points (A), (B), and (C), they are collinear exactly when the vectors (B-A) and (C-A) have zero cross product:

[
(x_B-x_A)(y_C-y_A) - (y_B-y_A)(x_C-x_A)=0.
]

The bound (n\le 100000) rules out checking every triple. There are

[
\binom{100000}{3}\approx 1.67\cdot 10^{14}
]

triples, which is far beyond what a competitive programming time limit can handle. We need a linear or near-linear solution. The coordinate bound reaches (10^9), so products in the cross product can reach about (4\cdot 10^{18}), and the difference can approach (8\cdot 10^{18}). Python integers handle these values exactly, while a fixed-width 32-bit integer would overflow badly.

The first non-obvious case is when the first three hunters are collinear even though a valid answer exists. For example,

```
4
0 0
1 1
2 2
0 1
```

The correct output is `Yes`, for example with indices `1 2 4`. A method that only tests the first three points would incorrectly print `No`.

The opposite case is when all points really are on one line:

```
4
1 1
2 2
3 3
4 4
```

The correct output is `No`. Any method must be able to inspect points beyond the initial three before declaring impossibility.

A third case concerns a vertical line:

```
3
5 0
5 2
5 7
```

The correct output is `No`. Computing a slope such as ((y_2-y_1)/(x_2-x_1)) can accidentally introduce division by zero. The cross product has no such special case, so vertical and horizontal lines are handled identically.

## Approaches

The direct brute-force solution considers every triple of hunters and checks whether its three points are collinear. This is correct because every possible answer is explicitly examined. The problem is the number of triples. For (n=100000), there are approximately (1.67\cdot10^{14}) of them, so even a very small constant amount of work per triple is too much.

The useful observation is that the first two hunters are distinct, so they determine one unique line. If there is any valid answer at all, there must be a third hunter outside this line. Conversely, if every hunter lies on this line, then every possible triple is collinear and the answer is impossible.

That means we do not need to search over triples. Fix hunters (1) and (2), then scan every remaining hunter and test whether it lies on their line. The first point that does not lie on the line immediately gives a valid answer. If the scan reaches the end without finding one, all hunters are on the same line and the answer is `No`.

The brute-force method works because testing a triple directly answers the question for that triple, but it fails because there are too many triples. The fixed-line observation reduces the problem to one collinearity test per remaining point.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^3)) | (O(1)) | Too slow |
| Optimal | (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read all (n) points together with their original 1-based indices. We need the indices in the output, not just the coordinates.
2. Take the first two points as (A=(x_1,y_1)) and (B=(x_2,y_2)). Because the statement guarantees that no two hunters occupy the same point, these two points define a unique line.
3. For every point (C=(x_i,y_i)) starting from the third point, calculate

[
cross=(x_2-x_1)(y_i-y_1)-(y_2-y_1)(x_i-x_1).
]

If `cross != 0`, the three points (A,B,C) are not collinear, so immediately print `Yes` and their indices.

1. If every remaining point has `cross == 0`, every hunter lies on the line through the first two hunters. In that case no three hunters can form a non-degenerate triangle, so print `No`.

The scan works because the line through the first two points is fixed for the entire algorithm. A nonzero cross product proves that the current point is outside that line, while a zero cross product proves that it is on the line.

### Why it works

The invariant is that the first two points always define the reference line. During the scan, if a point has a nonzero cross product with these two points, it is outside that line, so the three selected points cannot be collinear and the algorithm has found a valid answer.

If the algorithm never finds such a point, every input point has zero cross product with the first two points. Hence every point lies on their unique line. Since all hunters are on one line, every possible choice of three hunters is collinear, so `No` is the only correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    points = []

    for i in range(1, n + 1):
        x, y = map(int, input().split())
        points.append((x, y, i))

    x1, y1, i1 = points[0]
    x2, y2, i2 = points[1]

    dx = x2 - x1
    dy = y2 - y1

    for x, y, i in points[2:]:
        cross = dx * (y - y1) - dy * (x - x1)

        if cross != 0:
            print("Yes")
            print(i1, i2, i)
            return

    print("No")

if __name__ == "__main__":
    solve()
```

The input loop stores each coordinate together with its original index. This avoids having to reconstruct indices later and keeps the geometric computation separate from the output numbering.

The two differences `dx` and `dy` are computed once because the reference line never changes. For every later point, only the vector from the first point to the current point changes.

The expression

```
dx * (y - y1) - dy * (x - x1)
```

is the two-dimensional cross product. Its sign tells which side of the reference line the point is on, but for this problem only zero versus nonzero matters.

There is no division, so vertical lines cause no special case. Python integers also avoid overflow even for the largest permitted coordinates. The indices stored in `points` are already 1-based, matching the required output format.

The loop starts at `points[2:]` because the first two hunters are already being used as the fixed pair. There is no off-by-one issue in the output because the stored index is exactly the input position.

## Worked Examples

### Sample 1

The input is:

```
3
1 1
2 2
2 3
```

The first two points define the line (y=x). The third point is above that line.

| Step | Reference A | Reference B | Current C | Cross product | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | ((1,1)) | ((2,2)) | ((2,3)) | (1\cdot2-1\cdot1=1) | Print `Yes 1 2 3` |

The cross product is nonzero, so the three points are not collinear. The algorithm terminates immediately with a valid triple.

### Sample 2

The input is:

```
5
1 2
0 0
3 6
4 8
4 4
```

The first two points define the line (y=2x). Points 3 and 4 are also on that line, while point 5 is not.

| Step | Reference A | Reference B | Current C | Cross product | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | ((1,2)) | ((0,0)) | ((3,6)) | ((-1)\cdot4-(-2)\cdot2=0) | Continue |
| 2 | ((1,2)) | ((0,0)) | ((4,8)) | ((-1)\cdot6-(-2)\cdot3=0) | Continue |
| 3 | ((1,2)) | ((0,0)) | ((4,4)) | ((-1)\cdot2-(-2)\cdot3=4) | Print `Yes 1 2 5` |

The sample output uses a different valid triple, `3 2 5`. The problem accepts any three non-collinear hunters, so `1 2 5` is equally correct.

The first two candidate points after the reference pair demonstrate why checking only the first three hunters would not be sufficient. Several points can lie on the reference line before the scan reaches a valid third point.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Each hunter is read once and each point after the first two receives one cross-product test. |
| Space | (O(n)) | The coordinates and indices of all hunters are stored. |

With (n\le100000), a linear scan performs only around (100000) geometric tests, which is easily practical. The memory usage is also linear and comfortably within normal competitive programming limits.

## Test Cases

The statement guarantees that no two hunters occupy the same point, so a literal input where all coordinate pairs are identical is outside the valid input domain. The test suite below includes such an input as a robustness check anyway. A valid solution is not required to support it, but the implementation naturally returns `No`.

The assert helper captures standard output, while the checker validates the actual geometric property rather than requiring one particular valid triple. This is necessary because the problem allows any correct set of three indices.

```python
import sys
import io
import contextlib

def solve():
    input = sys.stdin.readline

    n = int(input())
    points = []

    for i in range(1, n + 1):
        x, y = map(int, input().split())
        points.append((x, y, i))

    x1, y1, i1 = points[0]
    x2, y2, i2 = points[1]

    dx = x2 - x1
    dy = y2 - y1

    for x, y, i in points[2:]:
        cross = dx * (y - y1) - dy * (x - x1)

        if cross != 0:
            print("Yes")
            print(i1, i2, i)
            return

    print("No")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            solve()
    finally:
        sys.stdin = old_stdin

    return output.getvalue().strip()

def valid_answer(inp: str, out: str) -> bool:
    data = inp.strip().splitlines()
    n = int(data[0])
    points = [tuple(map(int, line.split())) for line in data[1:]]

    tokens = out.split()

    if tokens[0] == "No":
        x1, y1 = points[0]
        x2, y2 = points[1]

        for x, y in points[2:]:
            cross = (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)
            if cross != 0:
                return False

        return True

    assert tokens[0] == "Yes"
    a, b, c = map(int, tokens[1:4])
    assert 1 <= a <= n
    assert 1 <= b <= n
    assert 1 <= c <= n
    assert len({a, b, c}) == 3

    x1, y1 = points[a - 1]
    x2, y2 = points[b - 1]
    x3, y3 = points[c - 1]

    cross = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
    return cross != 0

# Sample 1
sample1 = """\
3
1 1
2 2
2 3
"""
assert run(sample1).startswith("Yes")
assert valid_answer(sample1, run(sample1)), "sample 1"

# Sample 2
sample2 = """\
5
1 2
0 0
3 6
4 8
4 4
"""
assert run(sample2).startswith("Yes")
assert valid_answer(sample2, run(sample2)), "sample 2"

# Sample 3
sample3 = """\
4
1 1
2 2
3 3
4 4
"""
assert run(sample3) == "No"
assert valid_answer(sample3, run(sample3)), "sample 3"

# Minimum-size input, non-collinear
case4 = """\
3
0 0
1 1
1 0
"""
assert valid_answer(case4, run(case4)), "minimum non-collinear case"

# Minimum-size input, all points collinear
case5 = """\
3
-5 7
0 7
10 7
"""
assert run(case5) == "No"
assert valid_answer(case5, run(case5)), "minimum collinear case"

# Boundary coordinates and large cross product
case6 = """\
4
-1000000000 -1000000000
1000000000 1000000000
1000000000 -1000000000
0 0
"""
assert valid_answer(case6, run(case6)), "coordinate boundary case"

# First three points are collinear, fourth is not
case7 = """\
4
0 0
1 1
2 2
0 1
"""
assert valid_answer(case7, run(case7)), "late non-collinear point"

# Robustness only: duplicate coordinates are forbidden by the statement.
case8 = """\
3
5 5
5 5
5 5
"""
assert run(case8) == "No"
assert valid_answer(case8, run(case8)), "duplicate-coordinate robustness"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 / 0 0 / 1 1 / 1 0` | `Yes` | Minimum valid input with a non-collinear triple |
| `3 / -5 7 / 0 7 / 10 7` | `No` | Minimum input where every point is on one horizontal line |
| `4 / -10^9 -10^9 / 10^9 10^9 / 10^9 -10^9 / 0 0` | `Yes` | Coordinate boundaries and large integer cross products |
| `4 / 0 0 / 1 1 / 2 2 / 0 1` | `Yes` | Prevents the incorrect strategy of checking only the first three points |
| `3 / 5 5 / 5 5 / 5 5` | `No` | Robustness against duplicate coordinates, although this violates the input guarantee |

## Edge Cases

When the first three points are collinear, the algorithm does not conclude that the answer is impossible. For

```
4
0 0
1 1
2 2
0 1
```

the reference line is (y=x). The third point gives cross product (0), so the scan continues. The fourth point gives

[
1\cdot1-1\cdot0=1,
]

so the algorithm prints `Yes` with indices `1 2 4`. This is exactly the case that breaks a naive first-three-points solution.

When all points are collinear, such as

```
4
1 1
2 2
3 3
4 4
```

the first two points define (y=x). Every subsequent cross product is zero. The loop finishes without finding an outside point, so the algorithm prints `No`. Since every point belongs to the same line, no alternative triple can possibly work.

For a vertical line,

```
3
5 0
5 2
5 7
```

the differences between the first two (x)-coordinates are zero. The cross product still works directly:

[
0\cdot(y-0)-2\cdot(5-5)=0.
]

The algorithm prints `No` without any division or special handling. This is safer than a slope-based implementation, where the expression ((y_2-y_1)/(x_2-x_1)) would divide by zero.

Finally, consider the maximum coordinate range:

```
4
-1000000000 -1000000000
1000000000 1000000000
1000000000 -1000000000
0 0
```

The difference between the first two (x)-coordinates is (2\cdot10^9), and the corresponding (y)-difference has the same magnitude. For the third point, the cross product is on the order of (10^{18}), but Python's arbitrary-precision integers evaluate it exactly. The algorithm therefore makes the correct geometric decision without overflow.
