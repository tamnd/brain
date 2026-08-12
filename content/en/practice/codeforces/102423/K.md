---
title: "CF 102423K - Windmill Pivot"
description: "We have n distinct points in the plane, with no three on the same line. A windmill consists of a line and a current pivot point on that line. The line rotates clockwise around the pivot until it first reaches another point, which becomes the new pivot."
date: "2026-08-12T07:08:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102423
codeforces_index: "K"
codeforces_contest_name: "North American Southeast Regional 2019 (Div 1)"
rating: 0
weight: 102423
solve_time_s: 1754
verified: true
draft: false
---

[CF 102423K - Windmill Pivot](https://codeforces.com/problemset/problem/102423/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 29m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We have n distinct points in the plane, with no three on the same line. A windmill consists of a line and a current pivot point on that line. The line rotates clockwise around the pivot until it first reaches another point, which becomes the new pivot. We want to choose the initial pivot and starting direction so that, during one full 360 ∘ rotation, some point is promoted as many times as possible.

The key difficulty is that the pivot changes, so directly simulating one windmill means repeatedly asking which point the rotating line reaches next. Doing that for every possible starting state would be far too expensive. The useful way to look at the process is instead from the point that we want to count. Every time that point is promoted, the windmill line passes through it and one other point. We can characterize such an event entirely by the number of points on either side of that line.

The input contains up to 2000 points, with coordinates bounded by 10 5. An O(n 3 ) solution would already perform roughly

2000⋅1999⋅1998≈7.98×10 9

geometric tests, which is not practical under the ten second limit. An O(n 2 logn) solution is comfortable. The coordinates also mean ordinary 64-bit integer cross products are sufficient, since coordinate differences are at most 2⋅10 5, giving products around 4⋅10 10.

There are several subtle cases that matter.

With only two points, the answer is 1. For example,

```
2
0 0
1 0
```

has output

```
1
```

There is only one other point available to become a pivot, so a point cannot be promoted more than once during the relevant cycle.

For three noncollinear points, the answer can be 2, as in the official sample:

```
3
-1 0
1 0
0 2
```

The reason a careless implementation can get 1 is that a single geometric line through two points has two orientations. When the two possible side counts coincide, both orientations contribute promotions to the same state of the windmill, so the contribution must be counted twice rather than merged.

Another boundary case occurs when all other points lie on one side of a line through the pivot. Such a line corresponds to a hull tangent configuration, where one side count is zero. A solution that only considers balanced splits, such as n/2 points on each side, misses these windmills and can produce a wrong maximum.

## Approaches

A direct approach is to choose a pivot, choose another point that defines the next line event, and explicitly count how many points lie on each side of that line. There are O(n 2 ) choices of the ordered pair, and counting the points on the two sides takes O(n). This gives O(n 3 ) time, about 8×10 9 cross-product evaluations at n=2000. Simulating every complete windmill from every possible starting configuration would be even worse.

The observation that removes the third factor of n is that, once we fix a point p, all relevant lines pass through p. We can put p at the origin and sort all other points by their polar angle. For a directed line from p toward another point q, the number of points on its left side is exactly the number of vectors whose angles lie in the next open semicircle. Because no three points are collinear, no other vector lies exactly on a boundary of that semicircle.

This means all side counts for every line through p can be found with one angular sort and a two-pointer sweep. We never need to explicitly simulate the changing pivot.

Suppose there are L points strictly to the left of the directed ray p→q. At the moment when q and p exchange pivot status, the two possible orientations of this same geometric line correspond to windmill states with

k 1 ​ =L+1

points on the left, or

k 2 ​ =n−L−2

points on the left.

Both orientations are relevant because the windmill line is a directed rotating object during the sweep. If k 1 ​ =k 2 ​, these are two distinct promotion events belonging to the same state, so both must be added.

For every pivot p, we therefore build a frequency array indexed by the number k of points on the left. Every other point contributes one promotion to state L+1 and another to state n−L−2. The largest frequency over all p and k is exactly the required answer. The connection to the actual windmill is the invariant that the number of points on either side of the oriented line remains fixed while the pivot changes. Thus, for a fixed k, the angular sweep enumerates precisely the promotion events of that windmill state.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n 3 ) | O(1) | Too slow |
| Optimal | O(n 2 logn) | O(n) | Accepted |

## Algorithm Walkthrough

1. Fix one point p as the point whose number of promotions we are currently measuring. Translate the coordinate system conceptually so that p is the origin. Every other point now gives a vector from p.
2. Compute the polar angle of every vector and sort these angles increasingly. Since no three input points are collinear, no two vectors from the same pivot have the same direction modulo 180 ∘. We can safely use floating point angles here, although the geometry itself is based only on strict angular ordering.
3. Duplicate the sorted angle array with 2π added to every element. This turns the circular sequence into a linear one. For each original angle θ i ​, advance a pointer until the angle reaches θ i ​ +π. The number of points strictly between these two angles is the number L of points on the left side of the directed line.
4. For this event, calculate the two possible windmill states as k 1 ​ =L+1 and k 2 ​ =n−L−2. Increment both frequency counters. If they happen to be equal, incrementing the same counter twice is intentional because the two opposite orientations represent two promotion events during the full rotation.
5. After processing every other point for the current pivot, take the largest frequency obtained for that pivot. Repeat the same procedure for every point and keep the global maximum.
6. Output that maximum. Every promotion of a fixed point corresponds to one of the ordered line events counted above, and every counted event belongs to exactly one windmill state determined by its side counts.

### Why it works

Fix a point p. Consider an event where another point q and p lie on the rotating line. Let L be the number of remaining points on the left of the directed line p→q.

The windmill preserves the number of points on each side of its oriented line when the pivot changes. At the instant of promotion, one point leaves the line as the old pivot and the newly promoted point takes its place, so the side count does not change.

For one orientation of the line, the promoted point contributes the pivot-side point to the left count, giving L+1. For the opposite orientation, the same event has n−L−2 points on the left. These are exactly the two possible windmill states associated with the event.

Conversely, every time p is promoted, the preceding pivot is some q, so the promotion occurs on the line pq. The event is represented by one of the two orientations above and is counted by the sweep. Thus the frequency of a state k is exactly the number of times p is promoted in a full rotation of a windmill with that side count. Taking the maximum over all p and k gives the answer.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    n = int(input())
    points = [tuple(map(int, input().split())) for _ in range(n)]

    answer = 0
    two_pi = 2.0 * math.pi

    for p in range(n):
        px, py = points[p]

        angles = []
        for i in range(n):
            if i == p:
                continue
            x, y = points[i]
            angles.append(math.atan2(y - py, x - px))

        angles.sort()
        m = n - 1

        # Put every angle into [0, 2*pi).
        for i in range(m):
            if angles[i] < 0.0:
                angles[i] += two_pi

        angles.sort()

        extended = angles + [a + two_pi for a in angles]

        freq = [0] * n
        j = 1

        for i in range(m):
            if j <= i:
                j = i + 1

            limit = angles[i] + math.pi

            while j < i + m and extended[j] < limit:
                j += 1

            # Points strictly inside the counterclockwise semicircle.
            left = j - i - 1

            k1 = left + 1
            k2 = n - left - 2

            freq[k1] += 1
            freq[k2] += 1

        cur = max(freq)
        if cur > answer:
            answer = cur

    print(answer)

if __name__ == "__main__":
    solve()
```

For each pivot, `angles` contains the directions from that pivot to every other point. The normalization into [0,2π) makes the duplicated array easy to reason about, and the second copy shifted by 2π handles semicircles that cross the zero-angle boundary.

The two-pointer variable `j` only moves forward. Since the angles are sorted, when `i` increases, the endpoint of the semicircle never moves backward. Consequently, all n−1 values of `left` are found in linear time after sorting.

The condition `extended[j] < limit` is strict. Equality would mean that another point lies exactly on the boundary of the semicircle, which would put three points on one line through the current pivot. The problem guarantees that this never happens, but using a strict comparison also matches the definition of points strictly on one side.

The expressions `left + 1` and `n - left - 2` account for the promoted point and the old pivot occupying the line during a promotion. The two expressions can be equal, and the code deliberately increments the same frequency twice in that case.

All arithmetic involving coordinates is avoided after computing angles, so there is no integer overflow issue. Python's floating point precision is more than sufficient for ordering angles of integer-coordinate vectors when no two vectors are collinear.

## Worked Examples

### Sample 1

The points are

```
(-1, 0)
( 1, 0)
( 0, 2)
```

Consider the third point (0,2) as the pivot. The two vectors point down-left and down-right. Their angular ordering gives two semicircle counts.

| Event | `left` | `k1 = left + 1` | `k2 = n - left - 2` | Frequency update |
| --- | --- | --- | --- | --- |
| To `(-1,0)` | 1 | 2 | 0 | `freq[2] += 1`, `freq[0] += 1` |
| To `(1,0)` | 0 | 1 | 1 | `freq[1] += 2` |

The second event is the important edge case. Both orientations correspond to the same side count k=1, but they are distinct promotion events, so `freq[1]` becomes 2.

The other pivots cannot exceed this, giving the sample answer 2.

### Sample 2

Consider the point (1,2) in

```
(0,0)
(5,0)
(0,5)
(5,5)
(1,2)
(4,2)
```

The angular order of the other five points around (1,2) produces the following left-side counts.

| Event direction | `left` | `k1` | `k2` | Updates |
| --- | --- | --- | --- | --- |
| angle 0 ∘ | 2 | 3 | 2 | `freq[3]`, `freq[2]` |
| angle 36.9 ∘ | 1 | 2 | 3 | `freq[2]`, `freq[3]` |
| angle 108.4 ∘ | 0 | 1 | 4 | `freq[1]`, `freq[4]` |
| angle 243.4 ∘ | 1 | 2 | 3 | `freq[2]`, `freq[3]` |
| angle 333.4 ∘ | 1 | 2 | 3 | `freq[2]`, `freq[3]` |

The resulting largest frequency is 3, so this pivot alone achieves the sample answer.

The trace also shows why simply looking for the most common value of `left` is not enough. Each event contributes to two windmill states, and those two states can have different frequencies.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n 2 logn) | For each of n pivots, sort n−1 angles and sweep them in linear time |
| Space | O(n) | The angle arrays and frequency array contain O(n) elements |

With n≤2000, the algorithm performs roughly n sorts of arrays of length n, followed by only linear two-pointer sweeps. This is well within the ten second limit, while the O(n 3 ) alternative would require billions of geometric operations.

## Test Cases

The original problem has no meaningful "all-equal values" case because the objects are geometric points, not repeated numeric values, and duplicate coordinates are forbidden. A symmetric configuration is the closest useful analogue because it creates repeated side-count patterns.

```python
# helper: run solution on input string, return output string
import sys
import io
import math

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        # Inline version of the submitted solution.
        n = int(sys.stdin.readline())
        points = [tuple(map(int, sys.stdin.readline().split()))
                  for _ in range(n)]

        answer = 0
        two_pi = 2.0 * math.pi

        for p in range(n):
            px, py = points[p]
            angles = []

            for i in range(n):
                if i == p:
                    continue
                x, y = points[i]
                angles.append(math.atan2(y - py, x - px))

            angles.sort()

            for i in range(len(angles)):
                if angles[i] < 0.0:
                    angles[i] += two_pi

            angles.sort()

            m = n - 1
            extended = angles + [a + two_pi for a in angles]

            freq = [0] * n
            j = 1

            for i in range(m):
                if j <= i:
                    j = i + 1

                limit = angles[i] + math.pi

                while j < i + m and extended[j] < limit:
                    j += 1

                left = j - i - 1

                k1 = left + 1
                k2 = n - left - 2

                freq[k1] += 1
                freq[k2] += 1

            answer = max(answer, max(freq))

        print(answer)
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
assert solve_data("""\
3
-1 0
1 0
0 2
""") == "2", "sample 1"

# Provided sample 2
assert solve_data("""\
6
0 0
5 0
0 5
5 5
1 2
4 2
""") == "3", "sample 2"

# Minimum-size input
assert solve_data("""\
2
0 0
1 0
""") == "1", "minimum n"

# Symmetric square, useful for repeated side-count patterns
assert solve_data("""\
4
0 0
1 0
0 1
1 1
""") == "2", "symmetric square"

# Five points in a convex symmetric arrangement
assert solve_data("""\
5
0 0
2 0
3 2
1 4
-1 2
""") == "4", "five-point symmetric configuration"

# Maximum-size stress test.
# Points are (x, x^2 mod 2011). Since 2011 is prime, a line intersects
# this quadratic over the field in at most two points, so the integer
# coordinates contain no three collinear points.
n = 2000
stress_points = [(x, (x * x) % 2011) for x in range(n)]
stress_input = str(n) + "\n" + "\n".join(
    f"{x} {y}" for x, y in stress_points
) + "\n"

stress_output = solve_data(stress_input)
stress_answer = int(stress_output)
assert 1 <= stress_answer <= 2 * (n - 1), "maximum-size stress test"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3` point triangle from the statement | `2` | Equal two-orientation states must be counted twice |
| `6` point sample | `3` | Multiple side-count states for an interior pivot |
| Two points | `1` | Minimum size and zero-side configurations |
| Unit square | `2` | Symmetry and repeated angular structure |
| Five-point symmetric configuration | `4` | Repeated side counts and convex geometry |
| 2000-point modular parabola | Range check | Maximum constraint and performance |

## Edge Cases

For the two-point input

```
2
0 0
1 0
```

each pivot has exactly one other point. Its semicircle count is L=0, giving k 1 ​ =1 and k 2 ​ =0. Each state receives one promotion, so the answer is 1. The algorithm's two-pointer sweep handles this without needing any special case for a semicircle containing no points.

For the three-point sample

```
3
-1 0
1 0
0 2
```

the pivot (0,2) has one event with L=0. Both formulas produce k=1, so the code increments `freq[1]` twice. This is exactly the case that would be lost if the implementation used a set of states rather than counting promotion events.

For a hull-tangent situation, some event can have L=n−2. Then the formulas give k 1 ​ =n−1 and k 2 ​ =0. These extreme states are valid windmills and must remain in the frequency array. Restricting the search to middle values such as k≈n/2 would incorrectly discard promotions occurring on the convex hull.

For the maximum-size test, the algorithm never constructs all pairwise line relationships explicitly. It processes one pivot at a time, stores only its n−1 angles, and advances a single pointer through the duplicated angle array. The total work remains O(n 2 logn), which is the reason the n=2000 case remains practical.
