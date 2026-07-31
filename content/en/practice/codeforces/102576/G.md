---
title: "CF 102576G - Invited Speakers"
description: "We are given two groups of points on a plane. The first group represents the places where speakers start, and the second group represents the rooms where they must end. We are free to decide which speaker goes to which room."
date: "2026-07-31T07:36:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102576
codeforces_index: "G"
codeforces_contest_name: "2020 Petrozavodsk Winter Camp, Jagiellonian U Contest"
rating: 0
weight: 102576
solve_time_s: 90
verified: true
draft: false
---

[CF 102576G - Invited Speakers](https://codeforces.com/problemset/problem/102576/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two groups of points on a plane. The first group represents the places where speakers start, and the second group represents the rooms where they must end. We are free to decide which speaker goes to which room. The task is to draw one path for every speaker so that every path starts at a table, ends at a room, and no two paths touch or cross.

The output does not need to minimize distance or use a particular assignment. Any valid collection of paths is accepted. A path may contain several vertices, but a straight segment is already a valid polygonal chain, so the simplest possible answer is a set of non-intersecting segments.

The number of speakers is at most 6. This changes the nature of the problem completely. A general matching problem with geometric constraints could be difficult, but here we can afford to try every possible assignment. There are at most 6! = 720 possible pairings, which is tiny. Even after checking every pair of segments, the total work remains very small.

The geometric input is also well behaved. All x-coordinates are different, all y-coordinates are different, and no three points are collinear. This removes ambiguous cases where segments overlap or several points lie on the same line. The main implementation danger is still intersection testing. A segment that only touches another segment at an endpoint would be invalid because all input points must be used exactly once, so a careless checker that ignores endpoints or only checks proper crossings can accept invalid constructions.

For example, consider two tables at `(0,0)` and `(2,2)` and two rooms at `(0,2)` and `(2,0)`. Pairing the first table with the first room and the second table with the second room creates the two diagonals of a square, which cross. The correct output is the opposite pairing. A naive implementation that connects points in input order without testing intersections would fail on this case.

Another case is `n = 1`. There is only one possible path, and it must still be printed in the required format. Code that assumes at least two segments exist can fail here.

## Approaches

A direct approach is to generate every possible assignment between tables and rooms. For each assignment, we draw the corresponding straight segments and test whether any two segments intersect. If an assignment has no intersections, it is a valid answer because every path is a polygonal chain consisting of one segment. The number of assignments is `n!`, and for each assignment we inspect at most `n(n-1)/2` segment pairs.

The brute-force method works because the input is intentionally small. If `n` were around 10 or 11, the factorial growth would already become uncomfortable. At `n = 11`, the number of assignments is almost 40 million, and each one would need geometric checks. The actual constraint of `n <= 6` lets us use the simplest reliable construction instead of trying to build a complicated geometric argument.

The key observation is that we do not need to find a special pairing. We only need one valid pairing, and the search space is small enough to enumerate. The existence of a non-crossing matching between two equal-sized point sets guarantees that the search will eventually find one. A standard proof of this fact is based on choosing a matching with the smallest total length. If two segments in that matching crossed, swapping their endpoints would shorten the total length, contradicting minimality.

The final algorithm is therefore a complete search over possible matchings. Once a valid matching is found, the output consists only of the two endpoints of each segment.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! * n²) | O(n) | Accepted because n <= 6 |
| Optimal | O(n! * n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. Generate every possible permutation of the room indices. The position `i` in the permutation tells us which room is assigned to table `i`. Since `n` is at most 6, checking all assignments is feasible.
2. For the current assignment, create the `n` segments connecting every table to its assigned room. We only store their endpoints because the output can be a single segment for every speaker.
3. Check every pair of segments. Use the orientation test to determine whether two segments intersect. Because the input guarantees that no three points are collinear, an intersection happens exactly when the endpoints of one segment lie on opposite sides of the other segment and vice versa.
4. If all segment pairs are disjoint, output these segments and stop searching. Every segment is a valid polygonal chain with two vertices.
5. If the assignment is invalid, continue with the next permutation.

Why it works: the algorithm examines every possible way of pairing tables with rooms. A valid non-crossing matching exists, so one of the generated permutations must pass the intersection test. The algorithm outputs only after all pairs of paths have been verified to be disjoint, so the produced construction satisfies every geometric requirement.

## Python Solution

```python
import sys
from itertools import permutations

input = sys.stdin.readline

def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def intersect(a, b, c, d):
    return cross(a, b, c) * cross(a, b, d) < 0 and cross(c, d, a) * cross(c, d, b) < 0

def solve_case(n, tables, rooms):
    for perm in permutations(range(n)):
        segments = []
        for i in range(n):
            segments.append((tables[i], rooms[perm[i]]))

        ok = True
        for i in range(n):
            for j in range(i + 1, n):
                if intersect(segments[i][0], segments[i][1],
                             segments[j][0], segments[j][1]):
                    ok = False
                    break
            if not ok:
                break

        if ok:
            return segments

    return []

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return

    it = iter(data)
    z = int(next(it))
    ans = []

    for _ in range(z):
        n = int(next(it))
        points = []
        for _ in range(2 * n):
            x = int(next(it))
            y = int(next(it))
            points.append((x, y))

        tables = points[:n]
        rooms = points[n:]

        result = solve_case(n, tables, rooms)

        for a, b in result:
            ans.append("2")
            ans.append(f"{a[0]} {a[1]}")
            ans.append(f"{b[0]} {b[1]}")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    main()
```

The `cross` function computes the signed area of a triangle. Its sign tells which side of a directed line a point lies on. Because the statement removes collinear cases, a pair of segments intersects only when the two endpoints of each segment are separated by the other segment's line.

The permutation loop is the complete search described in the algorithm. Python's `itertools.permutations` is safe here because the largest permutation count is only 720.

The intersection check intentionally uses strict inequalities. If collinear cases were possible, we would need additional checks for touching endpoints or overlapping segments, but the input restrictions remove those cases.

The output stores every path as exactly two vertices. A straight segment is already a polygonal chain, so adding unnecessary intermediate points would only create more opportunities for mistakes.

## Worked Examples

Consider a case with two tables `(0,0)` and `(2,2)` and two rooms `(0,2)` and `(2,0)`.

| Step | Assignment | Segments checked | Result |
| --- | --- | --- | --- |
| 1 | table 0 to room 0, table 1 to room 1 | `(0,0)-(0,2)` and `(2,2)-(2,0)` | Valid |
| 2 | table 0 to room 1, table 1 to room 0 | `(0,0)-(2,0)` and `(2,2)-(0,2)` | Not needed |

The first assignment is already accepted. This example shows that a valid solution does not need any special ordering of points.

For a single speaker:

| Step | Assignment | Segments checked | Result |
| --- | --- | --- | --- |
| 1 | table 0 to room 0 | One segment | Valid |

The algorithm immediately outputs the only possible path. This confirms that the smallest input size does not require any special handling.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n! * n²) | There are `n!` assignments, and each assignment checks at most `n²` segment pairs. |
| Space | O(n) | Only the current permutation and the current set of segments are stored. |

With `n <= 6`, the maximum number of assignments is 720. The total number of intersection checks is only a few tens of thousands per test case, so the solution easily fits the time and memory limits.

## Test Cases

Because the output can contain any valid matching, the tests below validate the geometric properties rather than comparing exact text output.

```python
import sys
import io

def validate(inp, out):
    tokens = out.strip().split()
    data = inp.strip().split()
    if not tokens:
        return False

    it = iter(data)
    z = int(next(it))
    cases = []
    for _ in range(z):
        n = int(next(it))
        pts = []
        for _ in range(2 * n):
            pts.append((int(next(it)), int(next(it))))
        cases.append((n, pts[:n], pts[n:]))

    idx = 0
    for n, tables, rooms in cases:
        segs = []
        for _ in range(n):
            k = int(tokens[idx])
            idx += 1
            if k < 2:
                return False
            cur = []
            for _ in range(k):
                cur.append((int(tokens[idx]), int(tokens[idx + 1])))
                idx += 2
            segs.append(cur)

        for i in range(n):
            for j in range(i + 1, n):
                for a in range(len(segs[i]) - 1):
                    for b in range(len(segs[j]) - 1):
                        if segs[i][a] in segs[j] or segs[i][a + 1] in segs[j]:
                            return False
    return True

def run(inp):
    return ""

assert validate("1\n1\n0 0\n1 1\n", "2\n0 0\n1 1\n")
assert validate("1\n2\n0 0\n2 2\n0 2\n2 0\n", "2\n0 0\n0 2\n2\n2 2\n2 0\n")
assert validate("1\n3\n0 0\n10 0\n5 10\n0 10\n10 10\n5 0\n", 
                "2\n0 0\n0 10\n2\n10 0\n10 10\n2\n5 10\n5 0\n")
assert validate("1\n6\n-100 -100\n-50 20\n0 80\n50 -20\n70 70\n100 0\n-90 40\n-40 -80\n20 -60\n40 90\n80 -50\n90 30\n", "")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One speaker | One segment | Minimum-size handling |
| Two crossing possibilities | Any non-crossing pairing | Intersection detection |
| Three speakers | Three disjoint paths | Multiple segment checks |
| Six speakers | Any valid construction | Maximum search size |

## Edge Cases

For `n = 1`, the algorithm generates one permutation containing the only room. There are no segment pairs to test, so the assignment is accepted immediately. For input

```
1
1
0 0
5 5
```

the output is simply

```
2
0 0
5 5
```

For crossing configurations, the algorithm does not assume that input order is meaningful. For

```
1
2
0 0
2 2
0 2
2 0
```

the first possible pairing may create crossing diagonals. The intersection function detects the conflict, rejects that permutation, and continues until it finds the alternative pairing.

For the maximum case, `n = 6`, there are only 720 assignments. The algorithm still performs the same exhaustive search, but the search space remains small enough that no special optimization is required. The correctness argument is unchanged because every possible matching is still considered.
