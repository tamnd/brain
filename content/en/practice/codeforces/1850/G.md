---
title: "CF 1850G - The Morning Star"
description: "We are given a set of distinct points on a 2D integer grid. For every ordered pair of points, we imagine placing a compass at the first point and pointing it toward the second point."
date: "2026-06-09T05:31:19+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "data-structures", "geometry", "implementation", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1850
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 886 (Div. 4)"
rating: 1500
weight: 1850
solve_time_s: 65
verified: true
draft: false
---

[CF 1850G - The Morning Star](https://codeforces.com/problemset/problem/1850/G)

**Rating:** 1500  
**Tags:** combinatorics, data structures, geometry, implementation, math, sortings  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of distinct points on a 2D integer grid. For every ordered pair of points, we imagine placing a compass at the first point and pointing it toward the second point. The compass is considered valid only if the direction from the first point to the second is one of the eight standard compass directions: north, south, east, west, or one of the four diagonals.

The task is to count how many ordered pairs of points produce such an allowed direction.

An equivalent way to phrase the condition is that for a pair of points $(x_1, y_1)$ and $(x_2, y_2)$, the vector between them must either have equal x-coordinates (vertical line), equal y-coordinates (horizontal line), or satisfy $|x_2 - x_1| = |y_2 - y_1|$ (perfect diagonal slope of 1 or -1).

The constraints force us away from quadratic comparison. With up to $2 \cdot 10^5$ points overall, a naive check of all pairs would require roughly $O(n^2)$ operations, which would be on the order of $4 \cdot 10^{10}$ comparisons in the worst case, far beyond what can run in 2 seconds.

The main subtlety is that multiple points may lie on the same horizontal line, vertical line, or diagonal line, and every pair along those lines contributes. A careless approach often double counts or misses pairs if directions are not grouped properly. Another common pitfall is treating diagonals incorrectly by mixing slopes without normalizing by gcd or absolute equality.

Edge cases include:

A configuration where all points share the same x-coordinate. Then every pair is valid vertically, and the answer is simply $n(n-1)$. A naive directional check works but is too slow. Another edge case is a diagonal chain like $(0,0), (1,1), (2,2)$, where every pair is valid and must all be counted, not just adjacent ones. Finally, mixed distributions like random points require separating contributions by line families rather than pairwise inspection.

## Approaches

The brute-force solution is straightforward. For every ordered pair of points, compute the vector between them and check whether it lies on one of the eight allowed directions. This means checking whether either the x difference is zero, the y difference is zero, or their absolute values match. This works because it directly encodes the definition of valid compass movement.

The problem is scale. With $n$ up to $2 \cdot 10^5$, the number of pairs is on the order of $n^2$, which makes this approach infeasible.

The key observation is that validity depends only on three independent geometric classes: same x-coordinate, same y-coordinate, and same diagonal lines of slope $+1$ or $-1$. If we group points by these signatures, every valid pair becomes a pair inside one of these groups. Instead of checking pairs, we count combinations inside groups.

For vertical lines, we group by x-coordinate. If a group has size $k$, it contributes $k(k-1)$ ordered pairs. For horizontal lines, we group by y-coordinate similarly. For diagonals, we use transformed coordinates: $x - y$ for one diagonal family and $x + y$ for the other. Each group again contributes $k(k-1)$. Summing all contributions gives the answer.

This reduces the problem from pair enumeration to frequency counting over four hashable keys.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Group Counting | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. For each test case, read all points and prepare frequency maps for four different line signatures. The goal is to group points that can see each other in valid compass directions.
2. For every point $(x, y)$, increment counters for four keys: $x$, $y$, $x - y$, and $x + y$. Each key corresponds to one family of valid directions. This step builds equivalence classes of points that align along valid compass axes.
3. After processing all points, iterate through each frequency map. For each value $k$, add $k \cdot (k - 1)$ to the answer. This counts all ordered pairs within that group.
4. Sum contributions from all four maps. This includes vertical, horizontal, and both diagonal directions.
5. Output the final sum for the test case.

### Why it works

Each valid ordered pair must satisfy exactly one of the four structural conditions: same x, same y, same x minus y, or same x plus y. These conditions fully characterize all eight compass directions because diagonals split into two slope families and axes split into two directions each. Every valid pair appears inside exactly one corresponding group, and every pair inside a group is valid. This creates a perfect partition of valid pairs, ensuring the count is exact with no overlaps or omissions.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import defaultdict

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        cx = defaultdict(int)
        cy = defaultdict(int)
        cd1 = defaultdict(int)
        cd2 = defaultdict(int)

        pts = []
        for _ in range(n):
            x, y = map(int, input().split())
            cx[x] += 1
            cy[y] += 1
            cd1[x - y] += 1
            cd2[x + y] += 1

        ans = 0

        for d in (cx, cy, cd1, cd2):
            for k in d.values():
                ans += k * (k - 1)

        print(ans)

if __name__ == "__main__":
    solve()
```

The code maintains four independent hash maps. Each map corresponds to one geometric constraint class. The diagonal transformations $x - y$ and $x + y$ ensure that all 45-degree lines are captured without slope arithmetic or floating-point errors. The final loop accumulates ordered pair counts directly, avoiding division by two because direction matters.

A subtle point is that ordered pairs are required, so we use $k(k-1)$ instead of $k(k-1)/2$. Each pair contributes twice when considering compass placement in both directions, which matches the problem’s definition.

## Worked Examples

### Example 1

Points:

$(0,0), (-1,-1), (1,1)$

| Step | cx | cy | cd1 | cd2 | partial ans |
| --- | --- | --- | --- | --- | --- |
| after insert | 3 groups | 3 groups | 3 groups | 3 groups | 0 |
| compute | all k=1 | all k=1 | all k=1 | all k=1 | 0 |

Each structure has no repeated keys, so no group contributes extra pairs. However, this example from the statement includes all ordered pairs as valid because each pair matches one of the four structures, but since each group overlaps across structures, counting per structure ensures all directions are covered cumulatively.

### Example 2

Points:

$(6,9), (10,13), (0,0)$

| Step | cx sizes | cy sizes | cd1 sizes | cd2 sizes | ans |
| --- | --- | --- | --- | --- | --- |
| after insert | {6,10,0} | {9,13,0} | { -3, -3, 0 } | {15,23,0} | 0 |
| compute | all 1s | all 1s | all 1s | all 1s | 0 |

Only pairs aligned diagonally contribute, and only when two points share the same transformed key. The pair (6,9) and (10,13) shares $x-y = -3$, forming one valid group of size 2, contributing 2 ordered pairs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | Each point updates four hash maps and we later iterate over frequencies |
| Space | $O(n)$ | Each point contributes to constant-size key storage in maps |

The total $n$ over all test cases is bounded by $2 \cdot 10^5$, so the solution runs comfortably within limits. Hash map operations remain linear in expectation.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    from collections import defaultdict

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        cx = defaultdict(int)
        cy = defaultdict(int)
        cd1 = defaultdict(int)
        cd2 = defaultdict(int)

        for _ in range(n):
            x, y = map(int, input().split())
            cx[x] += 1
            cy[y] += 1
            cd1[x - y] += 1
            cd2[x + y] += 1

        ans = 0
        for d in (cx, cy, cd1, cd2):
            for k in d.values():
                ans += k * (k - 1)

        out.append(str(ans))

    return "\n".join(out)

# provided samples
assert run("""5
3
0 0
-1 -1
1 1
4
4 5
5 7
6 9
10 13
3
-1000000000 1000000000
0 0
1000000000 -1000000000
5
0 0
2 2
-1 5
-1 10
2 11
3
0 0
-1 2
1 -2
""") == """6
2
6
8
0"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single line vertical chain | n(n-1) | vertical grouping correctness |
| single diagonal chain | n(n-1) | diagonal transforms correctness |
| scattered points | 0 or sparse | no false positives |

## Edge Cases

A vertical alignment such as $(0,0), (0,1), (0,2), (0,3)$ produces a single key in the x-map with size 4. The algorithm adds $4 \cdot 3 = 12$, correctly counting all ordered pairs where the compass points north or south.

A diagonal chain like $(0,0), (1,1), (2,2), (3,3)$ shares the same $x-y$ key, producing another size 4 group. This again contributes 12, covering all diagonal compass directions.

A mixed configuration like $(0,0), (1,2), (2,1)$ splits across different keys, ensuring only valid geometric alignments contribute, and preventing accidental pairing across incompatible directions.
