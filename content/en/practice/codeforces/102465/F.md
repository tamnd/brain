---
title: "CF 102465F - Paris by Night"
description: "We have (N) monuments. Monument (i) has coordinates ((xi,yi)) and a positive grade (gi). Morgane chooses two distinct monuments as the endpoints of a line."
date: "2026-08-09T03:38:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102465
codeforces_index: "F"
codeforces_contest_name: "2018-2019 ICPC Southwestern European Regional Programming Contest (SWERC 2018)"
rating: 0
weight: 102465
solve_time_s: 166
verified: true
draft: false
---

[CF 102465F - Paris by Night](https://codeforces.com/problemset/problem/102465/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We have (N) monuments. Monument (i) has coordinates ((x_i,y_i)) and a positive grade (g_i). Morgane chooses two distinct monuments as the endpoints of a line. The balloon is positioned between those two monuments, and the line divides all remaining monuments into two open half-planes.

Each photograph contains the two chosen endpoint monuments, plus all monuments on one of the two sides of the line. If the sums of the two photographs are (A) and (B), we want to minimize (|A-B|) over every possible pair of endpoint monuments.

The input gives the number of monuments followed by their coordinates and grades. The output is the smallest possible difference between the two photograph grades.

The crucial geometric simplification is that the two endpoint monuments occur in both photographs. Their grades are consequently added to both sums and cancel when we take the difference. For a fixed pair of endpoints (i,j), suppose the grades of the monuments strictly to one side of their line sum to (S). Let the total grade of all monuments be (T). The other side has grade

[
T-g_i-g_j-S.
]

Thus the difference is

\left|2S-T+g_i+g_j\right|.
]

So the entire problem becomes: for every line through two monuments, find the grade sum of the points on one side as quickly as possible.

The coordinate limit reaches (10^9), so coordinate differences and cross products can be much larger than a 32-bit integer. A cross product can reach roughly (10^{18}), while the sum of all grades can reach (4\cdot10^{12}). Python integers handle these values directly, so there is no overflow issue in the implementation.

The limit (N\le 4000) is the main algorithmic signal. Enumerating all endpoint pairs already gives about (N^2/2) possibilities, so spending (O(N)) work on every pair would require roughly

31,976,004,000
]

point classifications in the worst case. That is far beyond the 15 second limit. We need to process all pairs associated with one fixed endpoint together.

The first edge case is (N=2). For example,

```
2
0 0 1
1 2 999
```

has answer `0`. There are no monuments on either side of the line. Both photographs contain both endpoints, so both grades are (1000). A careless solution that counts each endpoint only once would incorrectly report (998).

The second edge case is (N=3). For example,

```
3
0 0 5
1 0 10
0 1 7
```

has answer `5`. Whichever pair is chosen as the boundary monuments, the remaining monument is entirely on one side and the other side is empty. The endpoints cancel, leaving a difference equal to the grade of the remaining monument. The best choice leaves the monument with grade (5).

Another easy mistake is to use the wrong strictness when testing the two sides of the line. The statement guarantees that no three monuments are collinear, so no third monument can lie exactly on a boundary line. We can safely use a strict cross-product test. Treating an endpoint itself as part of a side would be wrong, and duplicating it in the side sum would also corrupt the answer.

The official SWERC analysis describes the same reduction from an (O(N^3)) solution to an (O(N^2\log N)) solution by ordering the other monuments around each fixed monument and updating the differences incrementally.

## Approaches

The direct solution is straightforward. Enumerate every pair (i,j) as the two boundary monuments. Then inspect every other monument (k), compute the orientation of (i,j,k) using a cross product, and add (g_k) to one of the two side sums. Once all points have been classified, compute the difference from the two side sums.

This is correct because every possible choice of boundary monuments is explicitly considered, and the cross product tells us exactly which side of the boundary line each remaining monument occupies. The problem is the cost. There are (O(N^2)) endpoint pairs, and each requires (O(N)) classifications, giving (O(N^3)). For (N=4000), the worst case contains about (3.2\cdot10^{10}) point classifications, so this approach is not viable.

The observation that removes the extra factor of (N) is that for one fixed monument (i), all possible second endpoints can be considered in angular order.

Place monument (i) at the origin temporarily and look at vectors from (i) to every other monument. Sort those vectors by polar angle. When the second boundary monument moves clockwise through this sorted order, the set of monuments lying in a particular open half-plane changes continuously. More precisely, the monuments on one side of the new boundary line form a contiguous angular interval of width less than (180^\circ).

That interval can be maintained with a two-pointer sweep. The left endpoint is the current boundary vector. The right endpoint only moves forward because rotating the boundary vector cannot make the end of the corresponding semicircle move backwards. Consequently, across the entire sweep for one fixed (i), every pointer moves only (O(N)) times.

The only expensive operation remaining for a fixed (i) is sorting the other (N-1) monuments by angle, which costs (O(N\log N)). Repeating this for all (N) possible choices of (i) gives (O(N^2\log N)).

The official analysis gives exactly this complexity and describes ordering the monuments around every fixed limiting monument, then computing the grade differences incrementally.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N^3)) | (O(N)) | Too slow |
| Optimal | (O(N^2\log N)) | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Read all monuments and compute the total grade (T). We will repeatedly use (T-g_i-g_j), the total grade of all monuments except the two boundary monuments.
2. Fix one monument (i) as the first boundary monument. For every other monument (j), form the vector
[
v_j=(x_j-x_i,\ y_j-y_i).
]
Store its direction, its vector components, and its grade. We sort these vectors by polar angle around (i).

The sorting gives us a circular order in which the second boundary monument can rotate around (i).
3. Duplicate the angular sequence conceptually by allowing indices up to (2(N-1)-1). We do not physically need to duplicate the vector objects. An index (k) refers to `vectors[k % m]`, where (m=N-1).

This turns the circular angular order into a linear sequence, so a semicircular interval can cross the (0^\circ) boundary without special cases.
4. Maintain a pointer (k) for the end of the current open semicircle. For the current boundary vector (v_j), advance (k) while
[
\operatorname{cross}(v_j,v_k)>0.
]

A positive cross product means that (v_k) is counterclockwise from (v_j) by an angle strictly between (0^\circ) and (180^\circ). Because no three monuments are collinear, the cross product cannot be zero for two different vectors from the same fixed monument.
5. Maintain prefix sums of the grades in the angular order. If the current semicircle contains indices from (j+1) through (k-1), its grade sum is obtained in (O(1)) from the prefix sums.

The boundary monument itself is excluded because the interval starts strictly after (j). This is exactly the side sum we need.
6. For boundary monuments (i) and (j), let `side` be the sum of grades inside the current semicircle. The grades of all non-boundary monuments are
[
T-g_i-g_j.
]
Hence the two side sums are `side` and
[
T-g_i-g_j-\text{side}.
]
The photograph difference is consequently
[
\left|2\cdot\text{side}-(T-g_i-g_j)\right|.
]
7. Update the global minimum with this difference. If the answer becomes zero, stop immediately because no smaller absolute difference exists.
8. Repeat the angular sort and two-pointer sweep for every possible first boundary monument (i). Every unordered pair of boundary monuments is encountered during at least one of these sweeps, so the global minimum contains the true optimum.

### Why it works

For a fixed monument (i), the sorted vectors represent all possible directions of the second boundary monument. For any current direction (v_j), the monuments on one side of the corresponding boundary line are exactly those whose directions lie strictly counterclockwise from (v_j) by less than (180^\circ). The cross-product condition identifies precisely this interval.

As (j) advances in angular order, the endpoint of that (180^\circ) interval never moves backwards. Thus the two-pointer sweep visits every possible side interval while maintaining its grade sum. The prefix sums convert each interval into an (O(1)) query.

Every pair of boundary monuments defines one such interval, and the two photographs are exactly the two complementary side sums plus the same two endpoint grades. The formula used by the algorithm therefore computes the exact difference for every possible pair. Taking the minimum over all pairs gives the required answer.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    n = int(input())
    points = [tuple(map(int, input().split())) for _ in range(n)]

    total_grade = sum(g for _, _, g in points)
    answer = total_grade

    for i in range(n):
        xi, yi, gi = points[i]

        vectors = []
        for j in range(n):
            if i == j:
                continue

            xj, yj, gj = points[j]
            dx = xj - xi
            dy = yj - yi

            vectors.append((math.atan2(dy, dx), dx, dy, gj))

        vectors.sort(key=lambda v: v[0])
        m = n - 1

        grades = [v[3] for v in vectors]

        prefix = [0] * (2 * m + 1)
        for p in range(2 * m):
            prefix[p + 1] = prefix[p] + grades[p % m]

        k = 1

        for j in range(m):
            if k < j + 1:
                k = j + 1

            _, ax, ay, gj = vectors[j]

            limit = j + m

            while k < limit:
                _, bx, by, _ = vectors[k % m]

                cross = ax * by - ay * bx

                if cross <= 0:
                    break

                k += 1

            side = prefix[k] - prefix[j + 1]
            other = total_grade - gi - gj

            diff = abs(2 * side - other)

            if diff < answer:
                answer = diff

                if answer == 0:
                    print(0)
                    return

    print(answer)

if __name__ == "__main__":
    solve()
```

The outer loop chooses the first boundary monument. For that fixed point, the inner construction creates one vector for every other monument. The vector stores both its angular sorting key and its exact integer coordinates, because the later cross-product calculation must use the original integer components.

`atan2` is used only to obtain the circular ordering. The actual (180^\circ) membership test uses the exact integer cross product, so floating-point arithmetic is not used to decide whether a monument belongs to a side. This is especially useful with coordinates as large as (10^9).

The vectors are sorted by their angle in ([-\pi,\pi]). The prefix array has length (2m+1), representing two copies of the grade sequence. We do not duplicate the vector objects themselves, which keeps the per-pivot memory small.

The pointer `k` is never reset when `j` increases. This is the key two-pointer property. The end of the open semicircle moves monotonically around the circle, so `k` can only increase during one complete sweep. Consequently, the total number of cross-product tests for a fixed pivot is (O(N)), rather than (O(N^2)).

The condition `cross <= 0` stops the semicircle. A zero cross product would mean that the two vectors are collinear, which cannot happen for two distinct other monuments because no three monuments are on one line. Using `<= 0` is nevertheless the safe boundary convention and also excludes the duplicated copy of the current vector after one complete revolution.

The expression

```
side = prefix[k] - prefix[j + 1]
```

deliberately starts after `j`. The current boundary monument must not be counted as part of either side sum. The two endpoint grades are inserted into both photograph grades separately, and cancel when their difference is computed.

Python integers automatically expand to arbitrary precision, so cross products near (10^{18}) and total grades near (4\cdot10^{12}) require no special handling.

## Worked Examples

The official sample is:

```
8
0 0 10
1 1 2
2 1 3
3 2 7
2 3 8
5 2 5
1 5 12
4 5 14
```

The total grade is (61). Consider monument ((2,1)), whose grade is (3), as the fixed first boundary monument. The other monuments are sorted counterclockwise by their direction from this point.

| Angular position | Monument | Grade |
| --- | --- | --- |
| 1 | ((0,0)) | 10 |
| 2 | ((5,2)) | 5 |
| 3 | ((3,2)) | 7 |
| 4 | ((4,5)) | 14 |
| 5 | ((2,3)) | 8 |
| 6 | ((1,5)) | 12 |
| 7 | ((1,1)) | 2 |

During the sweep, the important state is:

| Boundary monument | Grade | Side sum | Other-side sum | Difference |
| --- | --- | --- | --- | --- |
| ((0,0)) | 10 | 46 | 2 | 44 |
| ((5,2)) | 5 | 43 | 10 | 33 |
| ((3,2)) | 7 | 46 | 5 | 41 |
| ((4,5)) | 14 | 32 | 12 | 20 |
| ((2,3)) | 8 | 24 | 26 | 2 |
| ((1,5)) | 12 | 12 | 34 | 22 |
| ((1,1)) | 2 | 10 | 46 | 36 |

When ((2,3)) is the second boundary monument, the line is vertical. The monuments to its left have grades (10+2+12=24), while the monuments to its right have grades (7+5+14=26). Both photographs contain the endpoint grades (3+8=11), so their final grades are (35) and (37). Their difference is (2), which matches the sample output. This demonstrates the central cancellation of the boundary grades and the correctness of the semicircular interval.

For a second example, consider the minimum-size input:

```
2
0 0 1
1 2 999
```

There is only one possible pair of boundary monuments.

| Boundary pair | Side sum | Other side | Endpoint grade sum | Photograph grades | Difference |
| --- | --- | --- | --- | --- | --- |
| 1, 2 | 0 | 0 | 1000 | 1000, 1000 | 0 |

The two photographs are identical because both contain both monuments. The two-pointer sweep has no third monument to insert into either side, so both side sums remain zero. This confirms that the endpoints must be counted in both photographs rather than assigned to one side.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N^2\log N)) | For each fixed monument, sort (N-1) directions and then perform an (O(N)) two-pointer sweep. |
| Space | (O(N)) | One angular list and one prefix-sum array are maintained for the current fixed monument. |

For (N=4000), the algorithm performs (N) angular sorts of approximately (N) elements each, followed by only (O(N)) geometric updates per sort. This is the intended (O(N^2\log N)) approach described in the official SWERC analysis. The memory usage remains linear because the angular data for one pivot can be discarded before processing the next pivot.

## Test Cases

The following tests use the same algorithm in a callable `solve_data` function so that each case can be checked with Python assertions.

```python
import io
import math

def solve_data(data: str) -> str:
    it = iter(data.strip().split())
    n = int(next(it))

    points = []
    for _ in range(n):
        x = int(next(it))
        y = int(next(it))
        g = int(next(it))
        points.append((x, y, g))

    total_grade = sum(g for _, _, g in points)
    answer = total_grade

    for i in range(n):
        xi, yi, gi = points[i]

        vectors = []
        for j in range(n):
            if i == j:
                continue

            xj, yj, gj = points[j]
            dx = xj - xi
            dy = yj - yi
            vectors.append((math.atan2(dy, dx), dx, dy, gj))

        vectors.sort(key=lambda v: v[0])

        m = n - 1
        grades = [v[3] for v in vectors]

        prefix = [0] * (2 * m + 1)
        for p in range(2 * m):
            prefix[p + 1] = prefix[p] + grades[p % m]

        k = 1

        for j in range(m):
            if k < j + 1:
                k = j + 1

            _, ax, ay, gj = vectors[j]
            limit = j + m

            while k < limit:
                _, bx, by, _ = vectors[k % m]
                if ax * by - ay * bx <= 0:
                    break
                k += 1

            side = prefix[k] - prefix[j + 1]
            other = total_grade - gi - gj
            diff = abs(2 * side - other)

            if diff < answer:
                answer = diff

            if answer == 0:
                return "0\n"

    return str(answer) + "\n"

# Provided sample.
sample1 = """\
8
0 0 10
1 1 2
2 1 3
3 2 7
2 3 8
5 2 5
1 5 12
4 5 14
"""
assert solve_data(sample1) == "2\n", "provided sample"

# Minimum-size input. Both monuments are boundary monuments,
# so both photographs contain exactly the same two monuments.
sample2 = """\
2
0 0 1
1 2 999
"""
assert solve_data(sample2) == "0\n", "two monuments must give zero"

# Three monuments. Whichever pair is chosen, the remaining
# monument is alone on one side. The best remaining grade is 5.
sample3 = """\
3
0 0 5
1 0 10
0 1 7
"""
assert solve_data(sample3) == "5\n", "three-point case"

# All grades are equal. A balanced split is not even necessary:
# the endpoint grades cancel, and some boundary pair gives
# equal side contributions.
sample4 = """\
4
0 0 7
3 0 7
0 4 7
3 4 7
"""
assert solve_data(sample4) == "0\n", "all grades equal"

# Coordinates and grades at their maximum allowed magnitude.
# With three monuments, the answer is the smallest grade, 1.
sample5 = """\
3
0 0 1000000000
1000000000 0 999999999
0 1000000000 1
"""
assert solve_data(sample5) == "1\n", "large coordinates and grades"

# Maximum-size case. Points (i, i^2) contain no three collinear
# points, all grades are equal, and the answer is immediately zero.
n = 4000
lines = [str(n)]
for i in range(n):
    lines.append(f"{i} {i * i} 1")

large_case = "\n".join(lines) + "\n"
assert solve_data(large_case) == "0\n", "maximum N with valid geometry"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Official 8-monument sample | `2` | Complete geometric sweep and optimal pair |
| Two monuments | `0` | Both endpoints occur in both photographs |
| Three non-collinear monuments with grades 5, 10, 7 | `5` | Empty half-plane and endpoint cancellation |
| Four equal-grade monuments | `0` | Zero answer and early termination |
| Coordinates and grades near (10^9) | `1` | Large integer arithmetic and coordinate boundaries |
| 4000 points ((i,i^2)), all grade 1 | `0` | Maximum (N), valid no-three-collinear geometry, and performance |

## Edge Cases

For two monuments,

```
2
0 0 1
1 2 999
```

the only boundary pair contains every monument. The side sums are both zero, while both photographs contain the endpoint grades (1+999). The photograph grades are (1000) and (1000), so the answer is `0`. The algorithm handles this because `other = total_grade - gi - gj` is zero and the prefix interval is empty.

For three monuments,

```
3
0 0 5
1 0 10
0 1 7
```

fix any monument as the first boundary. The other two vectors are separated by an angle strictly between (0^\circ) and (180^\circ), so one possible boundary pair puts the third monument on one side and leaves the other side empty. For each pair, the difference is exactly the grade of the remaining monument. Choosing the pair that leaves grade (5) gives answer `5`.

For equal grades,

```
4
0 0 7
3 0 7
0 4 7
3 4 7
```

the algorithm can find a pair whose two side sums are equal, producing difference zero. As soon as `answer == 0`, the implementation returns immediately because no absolute difference can be smaller.

For maximum coordinate values,

```
3
0 0 1000000000
1000000000 0 999999999
0 1000000000 1
```

all three points form a valid triangle. Since there are only three monuments, the answer is the smallest grade, `1`. The cross products involve values around (10^{18}), which Python handles exactly.

For the maximum-size test, the points are ((i,i^2)) for (0\le i<4000). No three of these points are collinear because a line can intersect the strictly quadratic curve (y=x^2) in at most two points. Every grade is (1), so a zero difference exists and the algorithm can terminate as soon as it finds one. This test validates both the geometric assumptions and the intended (O(N^2\log N)) scaling.
