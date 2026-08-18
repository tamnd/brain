---
title: "CF 102222J - Nested Triangles"
description: "We have two fixed pivots, (P) and (Q), and (n) other points (A1,ldots,An). None of the other points lies on the line (PQ). We want a sequence of indices (v1,v2,ldots,vk) such that every point (A{v{i+1}}) lies strictly inside the triangle formed by (P,Q,A{vi})."
date: "2026-08-19T00:31:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102222
codeforces_index: "J"
codeforces_contest_name: "2018-2019 ACM-ICPC, China Multi-Provincial Collegiate Programming Contest"
rating: 0
weight: 102222
solve_time_s: 227
verified: true
draft: false
---

[CF 102222J - Nested Triangles](https://codeforces.com/problemset/problem/102222/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two fixed pivots, (P) and (Q), and (n) other points (A_1,\ldots,A_n). None of the other points lies on the line (PQ). We want a sequence of indices (v_1,v_2,\ldots,v_k) such that every point (A_{v_{i+1}}) lies strictly inside the triangle formed by (P,Q,A_{v_i}).

The first objective is to maximize (k). Among all sequences of that maximum length, the required answer is the lexicographically smallest sequence of original indices. The official sample contains three cases, with answers of lengths (6), (3), and (1).

The constraint (n\le 10^5) already rules out anything close to quadratic time for a single large case. Checking every pair of points costs about (n(n-1)/2), which is roughly (5\cdot10^9) pair checks when (n=10^5). The total number of points over all test cases is (10^6), so even an (O(n\log^2 n)) solution has to be implemented with fairly small constants. The coordinates can reach (10^9), so geometric comparisons must be exact rather than based on floating-point angles.

There are two particularly easy ways to get a wrong answer. First, points on the same side of (PQ) must be treated independently. For example,

```
1
0 0 10 0
2
5 1
5 -1
```

has answer length (1), not (2). The second point is on the opposite side of (PQ), so it cannot be inside the triangle whose third vertex is the first point.

Second, equality in an angular direction represents a point on a triangle edge and is not allowed. For example,

```
1
0 0 10 0
3
1 1
2 2
3 3
```

has answer

```
Case #1: 1
1
```

All three points lie on the same ray from (P). A careless non-strict LIS would treat them as a chain, even though every later point is on the boundary of the triangle determined by an earlier one.

A third corner case is that the line (PQ) need not be horizontal. For example,

```
1
0 0 0 10
4
1 5
2 5
-1 5
-2 5
```

has maximum length (2). The right-side chain is (2,1), and the left-side chain is (4,3), so the lexicographically smaller maximum solution is

```
Case #1: 2
2
1
```

Any solution based on ordinary slopes such as (y/x) would need special handling for vertical directions. Using cross products avoids that entire class of problems.

## Approaches

A direct dynamic programming approach considers every ordered pair of points on the same side of (PQ). For each possible outer point (A_i), we inspect every possible inner point (A_j), test whether (A_j) lies strictly inside triangle (PQA_i), and use the resulting relation as a DP transition. This is correct because the nesting relation forms a directed acyclic ordering once the geometric coordinates are converted into suitable ranks. The problem is the number of pair checks. With (n=10^5), the (\frac{n(n-1)}2) possible pairs already give approximately (5\cdot10^9) tests, before considering the cost of the geometric predicates.

The useful observation is that triangle containment can be described using only the directions of a point as seen from the two pivots. Suppose (A) is strictly inside triangle (PQB). Then (A) and (B) must be on the same side of (PQ). From (P), the ray (PA) lies strictly between (PQ) and (PB). From (Q), the ray (QA) lies strictly between (QP) and (QB).

That turns the geometry into two strict order relations. For every point we assign one angular rank around (P), measured from the ray (PQ), and another angular rank around (Q), measured from (QP). Within one side of (PQ), a point can be nested inside another exactly when both of its ranks are smaller.

The ranks can be computed without angles or floating point. Given two vectors (u) and (v), the sign of (u\times v) tells which vector comes first in angular order inside a half-plane. Points on the same ray have cross product zero and receive the same rank, correctly representing a boundary case that cannot participate in strict nesting.

After obtaining the two ranks, each side becomes a two-dimensional strict increasing subsequence problem. Sorting by the first rank and using a Fenwick tree over the second rank gives the longest chain in (O(n\log n)).

The lexicographic requirement fits naturally into the same DP result. Let (f[i]) be the length of the longest increasing chain ending at point (i) in rank space. Every point with (f[i]=L) can be the first, outermost point of an optimal answer. Among all such points compatible with the already selected outer point, we simply choose the smallest original index. We process (f=L,L-1,\ldots,1), so every point is examined exactly once during reconstruction.

The two sides of (PQ) are solved independently because no triangle can contain a point from the opposite side. We take the longer result, and if the lengths are equal, the sequence whose first index is smaller is lexicographically smaller.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) pair checks | (O(n)) | Too slow |
| Optimal | (O(n\log n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Compute the orientation of every (A_i) relative to the directed line (PQ). The sign of ((Q-P)\times(A_i-P)) identifies the two open half-planes. Since no point lies on (PQ), there is no zero case.
2. Sort the points around (P), separately ordering the two sides by angular distance from the ray (PQ). For one side the cross-product comparison is clockwise, and for the other it is counterclockwise. Equal rays are grouped together and receive the same first rank.
3. Sort the same points around (Q), this time measuring angular distance from (QP). Again, equal rays receive the same second rank.
4. Work on one side at a time. Sort its points by increasing first rank and, when the first rank is equal, by decreasing second rank. The decreasing tie order prevents two points having the same first rank from forming a subsequence transition. They are on the same ray from (P), so such a transition would represent a boundary point rather than a strict interior point.
5. Scan the points in that order and maintain a Fenwick tree whose position is the second rank. For point (i), query all second ranks strictly smaller than its own. If the maximum value there is (x), set (f[i]=x+1). Then update the Fenwick tree at the point's second rank with (f[i]).
6. The maximum (f[i]) is the maximum nesting depth on this side. Store every point in a bucket according to its DP value. These buckets will be used to reconstruct the lexicographically smallest answer.
7. Starting from the maximum DP value and moving downward, choose the smallest original index whose two ranks are strictly smaller than the ranks of the previously selected point. For the first position there is no previous point, so choose the smallest index among all points with maximum DP value.
8. Repeat the calculation for the other side of (PQ). Compare the two resulting sequences by length first and by their first index when their lengths are equal.

Why it works: for two points on the same side of (PQ), the point (A) lies strictly inside triangle (PQB) exactly when the ray (PA) is strictly between (PQ) and (PB), and the ray (QA) is strictly between (QP) and (QB). Those two strict angular conditions are exactly the two rank inequalities. Thus every valid nesting sequence corresponds to a strictly increasing sequence of rank pairs when read from inner to outer. The Fenwick tree computes the longest such sequence. During reconstruction, a point with DP value (d) always has a chain of (d-1) predecessors, so choosing the smallest valid original index at every level preserves the maximum possible remaining length while minimizing the earliest differing index. That is precisely lexicographic minimization.

## Python Solution

```python
import sys
from functools import cmp_to_key

input = sys.stdin.readline

class FenwickMax:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def update(self, i, value):
        n = self.n
        bit = self.bit
        while i <= n:
            if value > bit[i]:
                bit[i] = value
            i += i & -i

    def query(self, i):
        bit = self.bit
        ans = 0
        while i > 0:
            if bit[i] > ans:
                ans = bit[i]
            i -= i & -i
        return ans

def cross(ax, ay, bx, by):
    return ax * by - ay * bx

def solve_side(points, pivot_p, pivot_q, side):
    if not points:
        return []

    px, py = pivot_p
    qx, qy = pivot_q

    # The points are already assigned to one side.
    # Rank 1: angular order around P, starting from P->Q.
    def cmp_p(a, b):
        ax = a[0] - px
        ay = a[1] - py
        bx = b[0] - px
        by = b[1] - py
        c = ax * by - ay * bx

        if c == 0:
            return 0

        # side == 0 means cross(PQ, PA) < 0.
        # side == 1 means cross(PQ, PA) > 0.
        if side == 0:
            return -1 if c < 0 else 1
        return -1 if c > 0 else 1

    points.sort(key=cmp_to_key(cmp_p))

    rank = 0
    first = None

    for p in points:
        if first is None:
            rank = 1
            first = p
            p[4] = rank
            continue

        ax = first[0] - px
        ay = first[1] - py
        bx = p[0] - px
        by = p[1] - py

        if ax * by - ay * bx != 0:
            rank += 1
            first = p

        p[4] = rank

    # Rank 2: angular order around Q, starting from Q->P.
    def cmp_q(a, b):
        ax = a[0] - qx
        ay = a[1] - qy
        bx = b[0] - qx
        by = b[1] - qy
        c = ax * by - ay * bx

        if c == 0:
            return 0

        if side == 0:
            return -1 if c > 0 else 1
        return -1 if c < 0 else 1

    points.sort(key=cmp_to_key(cmp_q))

    rank = 0
    first = None

    for p in points:
        if first is None:
            rank = 1
            first = p
            p[5] = rank
            continue

        ax = first[0] - qx
        ay = first[1] - qy
        bx = p[0] - qx
        by = p[1] - qy

        if ax * by - ay * bx != 0:
            rank += 1
            first = p

        p[5] = rank

    # Strictly increasing rank pairs.
    # For equal rank1, decreasing rank2 prevents equal-rank1 transitions.
    points.sort(key=lambda p: (p[4], -p[5]))

    max_rank2 = rank
    bit = FenwickMax(max_rank2)

    groups = [[]]
    maximum = 0

    for p in points:
        f = bit.query(p[5] - 1) + 1
        p[6] = f

        if f > maximum:
            maximum = f
            groups.extend([[] for _ in range(f - len(groups) + 1)])

        groups[f].append(p)
        bit.update(p[5], f)

    # Reconstruct the lexicographically smallest chain.
    answer = []
    current = None

    for length in range(maximum, 0, -1):
        best = None

        if current is None:
            for p in groups[length]:
                if best is None or p[2] < best[2]:
                    best = p
        else:
            r1 = current[4]
            r2 = current[5]

            for p in groups[length]:
                if p[4] < r1 and p[5] < r2:
                    if best is None or p[2] < best[2]:
                        best = p

        current = best
        answer.append(current[2])

    return answer

def solve():
    t = int(input())
    output = []

    for case_id in range(1, t + 1):
        xP, yP, xQ, yQ = map(int, input().split())
        n = int(input())

        P = (xP, yP)
        Q = (xQ, yQ)

        dx = xQ - xP
        dy = yQ - yP

        right = []
        left = []

        for idx in range(1, n + 1):
            x, y = map(int, input().split())
            c = dx * (y - yP) - dy * (x - xP)

            # p = [x, y, original_id, side, rank1, rank2, dp]
            point = [x, y, idx, 0, 0, 0, 0]

            if c < 0:
                point[3] = 0
                right.append(point)
            else:
                point[3] = 1
                left.append(point)

        ans_right = solve_side(right, P, Q, 0)
        ans_left = solve_side(left, P, Q, 1)

        if len(ans_right) > len(ans_left):
            answer = ans_right
        elif len(ans_left) > len(ans_right):
            answer = ans_left
        else:
            if ans_right[0] < ans_left[0]:
                answer = ans_right
            else:
                answer = ans_left

        output.append(f"Case #{case_id}: {len(answer)}")
        output.extend(map(str, answer))

    sys.stdout.write("\n".join(output))

if __name__ == "__main__":
    solve()
```

The input loop first computes the orientation of every point relative to (PQ). The sign is enough because the statement guarantees that no point is exactly on the pivot line.

Each point stores its coordinates, original index, side, two angular ranks, and its DP value. Python integers have arbitrary precision, so the cross products remain exact even though the coordinates can reach (10^9).

The first custom comparator orders rays around (P), while the second orders rays around (Q). The comparators deliberately use cross products instead of `atan2`. A floating-point angle can distinguish most directions, but it cannot guarantee correct ordering for rational directions whose difference is smaller than machine precision.

The rank assignment compares every point with the first point of its current equal-ray group. A zero cross product means the two vectors have the same direction inside the relevant open half-plane. They receive the same rank because they cannot form a strict nesting transition.

The Fenwick tree contains only maximum DP values. `query(r2 - 1)` enforces strict inequality in the second rank. The decreasing second-rank order inside equal first-rank groups handles the other strict inequality without needing a separate group-processing pass.

The reconstruction deliberately works from the largest DP value down to one. The point with DP value (L) is the outermost point, while the point with DP value (L-1) is placed inside it. Choosing the smallest original index among all geometrically compatible candidates gives the smallest possible next index while keeping the remaining chain length unchanged.

No subtraction or multiplication is performed using floating point, and Python's arbitrary-precision integers remove the overflow issue that would otherwise require care in a lower-level language.

## Worked Examples

The first sample is especially useful because all six points are on the same side of (PQ), and they form one complete chain. The official output is (6,5,4,3,2,1).

| Point | First rank | Second rank | DP | Reconstruction |
| --- | --- | --- | --- | --- |
| (A_1=(5,1)) | 1 | 1 | 1 | selected last |
| (A_2=(5,2)) | 2 | 2 | 2 | selected fifth |
| (A_3=(5,3)) | 3 | 3 | 3 | selected fourth |
| (A_4=(6,4)) | 4 | 4 | 4 | selected third |
| (A_5=(6,5)) | 5 | 5 | 5 | selected second |
| (A_6=(6,6)) | 6 | 6 | 6 | selected first |

The Fenwick query for each point sees every earlier second rank, so the DP values become (1,2,3,4,5,6). Reconstruction starts at DP (6), chooses point (6), then point (5), and continues down to point (1). The result is exactly the required outer-to-inner order.

For the second sample, the pivots are (P=(6,6)) and (Q=(0,0)), and the maximum chain is (1,3,2). The three selected points lie on the same side of the pivot line. The DP finds a chain of length (3), while the other points either belong to the opposite side or fail one of the two strict rank inequalities.

| Reconstruction stage | Required DP | Chosen index | Reason |
| --- | --- | --- | --- |
| First point | 3 | 1 | Smallest point capable of starting a length-3 chain |
| Second point | 2 | 3 | Smallest compatible point with the remaining length |
| Third point | 1 | 2 | Compatible point completing the chain |

The second example demonstrates why lexicographic minimization cannot simply choose the smallest index globally. Point (1) is the best first choice, but after fixing it, the next choice has to satisfy the geometric nesting relation as well as the remaining DP requirement.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log n)) | Two exact angular sorts, rank processing, Fenwick DP, and linear reconstruction |
| Space | (O(n)) | Point storage, Fenwick tree, and DP buckets |

The largest case contains (10^5) points, and the sum over all cases is (10^6). The algorithm performs a logarithmic number of operations per point for the sorting and Fenwick stages, while all reconstruction and rank assignment passes are linear. The memory usage is linear in the number of points in the current test case.

## Test Cases

```python
# This test block assumes the solve() function from the solution above
# has already been defined.

import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Official samples.
sample = """\
3
0 0 10 0
6
5 1
5 2
5 3
6 4
6 5
6 6
6 6
0 0
9
1 6
2 3
4 7
6 8
8 2
9 3
7 6
2 4
2 7
0 10 10 0
9
0 0
0 2
2 0
0 4
4 0
0 6
6 0
0 8
8 0
"""

expected_sample = """\
Case #1: 6
6
5
4
3
2
1
Case #2: 3
1
3
2
Case #3: 1
1
"""

assert run(sample) == expected_sample, "official samples"

# Minimum-size input.
assert run("""\
1
0 0 10 0
1
5 1
""") == """\
Case #1: 1
1
""", "minimum n"

# Equal ray from P: every point is on a boundary ray, so no pair can nest.
assert run("""\
1
0 0 10 0
3
1 1
2 2
3 3
""") == """\
Case #1: 1
1
""", "equal ray must remain strict"

# Both sides have a chain of length 2.
# The two maximum solutions are [2, 1] and [4, 3],
# so lexicographic order chooses [2, 1].
assert run("""\
1
0 0 10 0
4
5 1
5 2
5 -1
5 -2
""") == """\
Case #1: 2
2
1
""", "tie between the two sides"

# Vertical PQ. This catches implementations that rely on ordinary slopes.
assert run("""\
1
0 0 0 10
4
1 5
2 5
-1 5
-2 5
""") == """\
Case #1: 2
2
1
""", "vertical pivot line"

# Maximum-size case with a deliberately simple answer.
# All 100000 points lie on the same ray from P, so the answer is still 1.
points = "\n".join(f"{i} {i}" for i in range(1, 100001))
max_case = "1\n0 0 1 0\n100000\n" + points + "\n"

assert run(max_case) == """\
Case #1: 1
1
""", "n = 100000"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| (P=(0,0),Q=(10,0),A_1=(5,1)) | `Case #1: 1 / 1` | Minimum input size |
| Three points ((1,1),(2,2),(3,3)) | `Case #1: 1 / 1` | Equal angular ranks and strictness |
| Two chains on opposite sides | `Case #1: 2 / 2 / 1` | Side separation and lexicographic tie-breaking |
| Vertical (PQ) | `Case #1: 2 / 2 / 1` | Direction handling without division |
| (100000) points on one ray | `Case #1: 1 / 1` | Maximum (n) and linear-memory behavior |

## Edge Cases

For points on opposite sides of (PQ), the algorithm places them in different arrays before doing any DP. For

```
1
0 0 10 0
2
5 1
5 -1
```

the first point receives a rank only in the upper-side computation and the second only in the lower-side computation. Each side produces a chain of length (1), so the final answer is

```
Case #1: 1
1
```

The comparison never creates a transition between the two sides, which matches the geometry because an interior point of triangle (PQA) must be on the same side of (PQ) as (A).

For equal rays, consider

```
1
0 0 10 0
3
1 1
2 2
3 3
```

All three points have the same first angular rank around (P). They are consequently processed inside one equal-rank group, and the decreasing second-rank order prevents one from extending another. Every DP value is (1), so reconstruction chooses the smallest original index, producing

```
Case #1: 1
1
```

This is the strict-boundary case that catches an ordinary non-strict LIS.

For a vertical pivot line,

```
1
0 0 0 10
4
1 5
2 5
-1 5
-2 5
```

the algorithm never computes a slope such as (y/x). It compares vectors using cross products, so the vertical direction of (PQ) requires no special branch. On each side, the point farther from (PQ) is the outer point, giving the two possible chains (2,1) and (4,3). Since both have length (2), the first index decides the answer, yielding

```
Case #1: 2
2
1
```

Finally, the (n=100000) test places every point on one ray. The angular ranks collapse into one first-rank group, so the Fenwick DP never creates a chain longer than one. The algorithm still performs only its sorting and linear passes and outputs

```
Case #1: 1
1
```

The example also confirms why storing exact direction groups matters even when the input contains many points with very similar geometric directions.
