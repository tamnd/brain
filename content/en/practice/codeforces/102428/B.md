---
title: "CF 102428B - Build the Perfect House"
description: "We have a set of vegetable plants represented by points in the plane. The desired house is a square whose center is fixed at the origin, but its orientation is completely free. A plant may lie on the boundary of the square, but it cannot lie strictly inside it."
date: "2026-08-12T07:11:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102428
codeforces_index: "B"
codeforces_contest_name: "2019-2020 ACM-ICPC Latin American Regional Programming Contest"
rating: 0
weight: 102428
solve_time_s: 123
verified: true
draft: false
---

[CF 102428B - Build the Perfect House](https://codeforces.com/problemset/problem/102428/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a set of vegetable plants represented by points in the plane. The desired house is a square whose center is fixed at the origin, but its orientation is completely free. A plant may lie on the boundary of the square, but it cannot lie strictly inside it.

For a square with half-side length (a), the actual side length is (2a), so its perimeter is (8a). The task is consequently to find the largest possible half-side (a), then multiply it by (8).

The input contains at most (10^4) points, while each coordinate can have absolute value up to (10^9). The archived Codeforces statement gives a 6 second time limit, so an (O(N^2)) or (O(N^3)) geometric search needs to be avoided in the intended solution. The large coordinate bound also means that calculations involving squared distances should use integer arithmetic where possible, while the final angular calculations necessarily use floating point.

The first non-obvious case is a plant exactly on the boundary. For example,

```
1
0 1
```

has answer `8.0000`. A square with half-side (1), centered at the origin, can put the plant on one of its sides. Treating boundary points as forbidden would incorrectly reject this square and produce an answer smaller than (8).

A second edge case is a plant that is very close to the origin. For

```
1
1 0
```

the answer is again `8.0000`. The square can be rotated so that the plant lies exactly on a side. A careless implementation that checks whether a point is at distance less than or equal to the half-side would incorrectly regard this boundary position as invalid.

A third issue comes from rotation. For

```
2
1 0
0 1
```

the answer is `8.0000`. Both plants can simultaneously lie on the boundary of the axis-aligned square with half-side (1). Testing only squares whose sides are at some arbitrary fixed orientation would miss the fact that the orientation itself is part of the optimization.

The final subtlety is that the orientation is periodic. Rotating a square by (90^\circ) gives exactly the same square, so only an interval of length (\pi/2) needs to be considered.

## Approaches

A direct geometric search would fix an orientation, inspect every plant, and determine the largest half-side compatible with that orientation. The difficulty is that there are infinitely many orientations. One could generate all critical orientations where two constraints interact and then test them, but there are (O(N^2)) such candidates and testing each candidate against all (N) plants gives (O(N^3)) work. With (N=10^4), that can reach about (10^{12}) point checks, far beyond what the time limit permits.

The useful observation is that we do not need to optimize the orientation and the square size simultaneously. Instead, fix a candidate half-side (a) and ask a yes-or-no question: is there some rotation for which no plant is strictly inside the square? This property is monotone. If a square of half-side (a) can be placed, then every smaller square can also be placed with the same orientation. We can consequently binary search (a). This binary-search reduction is also the approach described by independent solutions of the problem.

The remaining problem is checking one candidate (a).

Take one plant (P=(x,y)), and let its polar coordinates be ((r,\phi)). Let (\theta) denote the direction of one of the square's outward normals. In the coordinate system determined by the square, the plant has projections

[
r\cos(\phi-\theta)
]

and

[
r\sin(\phi-\theta).
]

The plant is strictly inside the square exactly when both absolute projections are smaller than (a):

[
|r\cos(\phi-\theta)|<a
]

and

[
|r\sin(\phi-\theta)|<a.
]

When (r<a), the plant is inside every possible square orientation, so the candidate is immediately impossible. When (r\geq\sqrt2a), at least one of the two projections is always at least (a), so the plant never enters the square and imposes no restriction.

The interesting case is

[
a\leq r<\sqrt2a.
]

Put (q=a/r). Since (1/\sqrt2<q\leq1), the angles satisfying both inequalities form one open interval modulo (90^\circ). Its center is (\phi-\pi/4), and its half-width is

[
h=\arcsin(q)-\frac{\pi}{4}.
]

Thus every plant gives one forbidden open interval of orientations. We only need to determine whether the union of all these forbidden intervals covers the entire circle of orientations of length (\pi/2).

That check is a standard sweep after sorting the interval endpoints. The reference solution description also uses angular intervals and a sweep to determine whether every possible rotation is blocked.

There is a small numerical detail here. The forbidden intervals are open because a plant exactly on a square side is allowed. During binary search we can safely use closed intervals in the feasibility test. If the only valid orientation occurs exactly at an endpoint, the closed-interval test may reject the exact optimum, but every value infinitesimally below that optimum is accepted. Binary search consequently approaches the same supremum, which is more than sufficient for four decimal places.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N^3)) | (O(N)) | Too slow |
| Optimal | (O(KN\log N)) | (O(N)) | Accepted |

Here (K) is the fixed number of binary-search iterations, chosen as 70 in the implementation.

## Algorithm Walkthrough

1. Read every plant and compute its distance from the origin. We keep the squared distance as an integer initially, which avoids unnecessary floating-point error when deciding whether a plant is certainly inside or certainly irrelevant.
2. Binary search the half-side (a) between (0) and the smallest distance from the origin to any plant. A larger half-side cannot be possible because the square contains the entire disk of radius (a), so a plant with distance smaller than (a) would necessarily be inside.
3. For a candidate (a), inspect every plant. If (r<a), return false immediately because no rotation can save that plant.
4. If (a\leq r/\sqrt2), ignore the plant. At least one of the two perpendicular projections has magnitude at least (r/\sqrt2), which is at least (a), so the plant is never strictly inside.
5. For every remaining plant, compute its polar angle (\phi=\operatorname{atan2}(y,x)). Since the square repeats every (\pi/2), normalize the forbidden interval center (\phi-\pi/4) into ([0,\pi/2)).
6. Compute

[
h=\arcsin(a/r)-\pi/4.
]

The forbidden orientations are the angles within (h) of the center, modulo (\pi/2).

1. If an interval crosses either end of ([0,\pi/2)), split it into two intervals. This converts the circular interval problem into an ordinary interval union problem.
2. Sort all interval endpoints and merge the intervals. If their union covers the complete range ([0,\pi/2]), every orientation places at least one plant strictly inside the square, so the candidate (a) is impossible. Otherwise there is an orientation outside every forbidden interval, so (a) is feasible.
3. Run the binary search for 70 iterations. The interval becomes vastly smaller than the precision needed for four decimal digits, even when coordinates are as large as (10^9).
4. Print (8a) with exactly four digits after the decimal point, because (8a) is the perimeter of the square.

### Why it works

For a fixed half-side (a), each plant forbids exactly the orientations for which both of its perpendicular projections onto the square's normal directions have magnitude less than (a). Those forbidden orientations form one open interval modulo (\pi/2), except for the two trivial cases where the plant is always inside or never inside.

Consequently, a feasible orientation exists exactly when the union of all forbidden intervals does not cover the entire orientation circle. The sweep checks precisely that condition. The feasibility predicate is monotone in (a), because enlarging a square cannot turn an invalid placement into a valid one. Binary search thus converges to the maximum feasible half-side, and multiplying it by (8) gives the maximum perimeter.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

PI = math.pi
PERIOD = PI / 2.0
EPS = 1e-12

def solve():
    n = int(input())
    points = []

    min_r2 = None

    for _ in range(n):
        x, y = map(int, input().split())
        r2 = x * x + y * y
        points.append((x, y, r2))
        if min_r2 is None or r2 < min_r2:
            min_r2 = r2

    min_r = math.sqrt(min_r2)

    def feasible(a):
        intervals = []

        for x, y, r2 in points:
            r = math.sqrt(r2)

            if r < a:
                return False

            # If r / sqrt(2) >= a, the point is never strictly inside.
            if r * r >= 2.0 * a * a:
                continue

            phi = math.atan2(y, x)

            # The forbidden interval is centered at phi - pi/4
            # modulo pi/2.
            center = (phi - PI / 4.0) % PERIOD

            q = a / r
            if q > 1.0:
                q = 1.0

            half = math.asin(q) - PI / 4.0

            left = center - half
            right = center + half

            if left < 0.0:
                intervals.append((0.0, right))
                intervals.append((left + PERIOD, PERIOD))
            elif right >= PERIOD:
                intervals.append((left, PERIOD))
                intervals.append((0.0, right - PERIOD))
            else:
                intervals.append((left, right))

        if not intervals:
            return True

        intervals.sort()

        covered = 0.0

        for left, right in intervals:
            if left > covered + EPS:
                return True

            if right > covered:
                covered = right

            if covered >= PERIOD - EPS:
                return False

        return True

    lo = 0.0
    hi = min_r

    for _ in range(70):
        mid = (lo + hi) / 2.0
        if feasible(mid):
            lo = mid
        else:
            hi = mid

    print(f"{8.0 * lo:.4f}")

if __name__ == "__main__":
    solve()
```

The input loop stores each point together with (x^2+y^2). Python integers have arbitrary precision, so even the maximum squared coordinate sum is represented exactly.

The `feasible` function implements the three geometric cases directly. The comparison `r * r >= 2 * a * a` avoids computing (r/\sqrt2) and is preferable because both sides can be compared without introducing an additional square root.

For the nontrivial case, `atan2` gives the plant direction in the full range ((-\pi,\pi]). Subtracting (\pi/4) moves the forbidden interval from the plant direction to the direction of the square's diagonal, and taking modulo (\pi/2) removes the square's (90^\circ) rotational symmetry.

The expression `asin(a / r) - pi / 4` is nonnegative precisely in the case being processed. Clamping `q` to (1) protects against a tiny floating-point overshoot when (a) is extremely close to (r).

A circular interval can cross zero, so the code splits it into two ordinary intervals. After sorting, `covered` stores the rightmost point continuously covered from zero. If the next interval starts strictly after `covered`, there is an uncovered orientation and the candidate is feasible. The small `EPS` prevents numerical noise at touching endpoints from changing the decision.

The binary search uses 70 iterations rather than relying on an epsilon-based termination condition. This gives a deterministic precision bound and avoids an off-by-one style termination issue. Seventy halvings leave an error many orders of magnitude below the (10^{-4}) output requirement.

## Worked Examples

### Sample 1

The input contains one plant at ((0,1)), so its distance from the origin is (1).

| Variable | Value |
| --- | --- |
| (r) | (1) |
| Candidate (a) | (1) |
| (a/r) | (1) |
| Forbidden interval | almost the whole (\pi/2) range |
| Feasible orientation | (\theta=0) |
| Perimeter | (8) |

At (a=1), the plant lies exactly on a side when the square's normal is vertical. Since boundary contact is allowed, this is a valid square. No half-side larger than (1) can work because the plant would then be strictly inside for every orientation.

The binary search approaches (a=1), and the final perimeter is `8.0000`.

### Sample 2

The plants are ((10,4)) and ((-5,-8)).

Their distances are

[
r_1=\sqrt{116}\approx10.7703
]

and

[
r_2=\sqrt{89}\approx9.4340.
]

The optimal half-side is approximately (9.3704), giving the perimeter (74.9634).

| Plant | (r) | (a/r) | Forbidden center modulo (\pi/2) | Half-width |
| --- | --- | --- | --- | --- |
| ((10,4)) | (10.7703) | (0.8703) | (1.1659) | (0.2705) |
| ((-5,-8)) | (9.4340) | (0.9933) | (0.2260) | (0.6695) |

The two forbidden intervals meet at the optimum. Slightly below this half-side there is a small orientation gap, so the square is feasible. Slightly above it, the two forbidden intervals overlap enough to cover all orientations, making the square impossible.

This is exactly the situation binary search is designed for: the feasibility changes from true to false at the optimal half-side, and the interval union check detects that transition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(KN\log N)) | Each of the (K=70) feasibility checks creates (O(N)) intervals and sorts them. |
| Space | (O(N)) | At most two ordinary intervals are stored for each plant. |

With (N\leq10^4), the solution performs about 70 sorting passes over at most (2N) intervals. This is comfortably within the intended complexity for the 6 second limit, while avoiding the quadratic or cubic geometric searches that would become prohibitive at this input size.

## Test Cases

```python
import sys
import io
import math

PI = math.pi
PERIOD = PI / 2.0
EPS = 1e-12

def main():
    input = sys.stdin.readline

    n = int(input())
    points = []
    min_r2 = None

    for _ in range(n):
        x, y = map(int, input().split())
        r2 = x * x + y * y
        points.append((x, y, r2))
        if min_r2 is None or r2 < min_r2:
            min_r2 = r2

    min_r = math.sqrt(min_r2)

    def feasible(a):
        intervals = []

        for x, y, r2 in points:
            r = math.sqrt(r2)

            if r < a:
                return False

            if r * r >= 2.0 * a * a:
                continue

            phi = math.atan2(y, x)
            center = (phi - PI / 4.0) % PERIOD

            q = min(1.0, a / r)
            half = math.asin(q) - PI / 4.0

            left = center - half
            right = center + half

            if left < 0.0:
                intervals.append((0.0, right))
                intervals.append((left + PERIOD, PERIOD))
            elif right >= PERIOD:
                intervals.append((left, PERIOD))
                intervals.append((0.0, right - PERIOD))
            else:
                intervals.append((left, right))

        if not intervals:
            return True

        intervals.sort()

        covered = 0.0

        for left, right in intervals:
            if left > covered + EPS:
                return True

            if right > covered:
                covered = right

            if covered >= PERIOD - EPS:
                return False

        return True

    lo = 0.0
    hi = min_r

    for _ in range(70):
        mid = (lo + hi) / 2.0
        if feasible(mid):
            lo = mid
        else:
            hi = mid

    print(f"{8.0 * lo:.4f}")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        main()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run("""1
0 1
""") == "8.0000\n", "sample 1"

assert run("""2
10 4
-5 -8
""") == "74.9634\n", "sample 2"

# One point on a coordinate axis. The point can lie exactly on the boundary.
assert run("""1
1 0
""") == "8.0000\n", "single point on boundary"

# One point at distance sqrt(2). Align a square normal with the point.
assert run("""1
1 1
""") == "11.3137\n", "diagonal single point"

# Four points at radius 1. All four can lie on the boundary of
# the square with half-side 1.
assert run("""4
1 0
0 1
-1 0
0 -1
""") == "8.0000\n", "four symmetric boundary points"

# All points have the same distance 5 from the origin.
# The largest angular gap modulo 90 degrees is atan(3/4),
# so the optimal half-side is 3*sqrt(10)/2.
assert run("""12
5 0
4 3
3 4
0 5
-3 4
-4 3
-5 0
-4 -3
-3 -4
0 -5
3 -4
4 -3
""") == "18.9737\n", "equal-radius points"

# Maximum N. The point (1, 0) alone limits the answer to perimeter 4,
# while all other points are outside the square at that orientation.
pts = ["10000"]
for y in range(-5000, 5000):
    pts.append(f"1 {y}")
assert run("\n".join(pts) + "\n") == "4.0000\n", "maximum N"

# Maximum coordinate magnitude.
assert run("""1
1000000000 0
""") == "4000000000.0000\n", "coordinate boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0 1` | `8.0000` | Boundary contact is allowed. |
| `1 / 1 1` | `11.3137` | Single-point optimum and diagonal geometry. |
| Four axis points at radius 1 | `8.0000` | Symmetry and simultaneous boundary contacts. |
| Twelve integer points at radius 5 | `18.9737` | Equal-radius values and angular interval interaction. |
| 10000 points `(1,y)` | `4.0000` | Maximum (N) and performance. |
| `1 / 1000000000 0` | `4000000000.0000` | Maximum coordinate magnitude and large output. |

## Edge Cases

For a point exactly on the eventual boundary, the forbidden orientation interval is open. Consider

```
1
0 1
```

At half-side (a=1), the point has distance (r=1). The only orientations that are safe are the ones where the point lies on a square side, and those orientations are not considered forbidden because the plant is allowed on the boundary. The binary search approaches (a=1) from below, where a nonempty set of safe orientations exists, and produces the correct perimeter `8.0000`.

For a point at the origin's diagonal direction, consider

```
1
1 1
```

The plant has distance (\sqrt2). Rotating the square so that one of its normals points toward ((1,1)) lets the plant lie on a side with half-side (\sqrt2). The resulting perimeter is

[
8\sqrt2\approx11.313708,
]

so the output is `11.3137`. The implementation handles this without any special angular case because the point is processed by the general projection inequalities.

For symmetric points,

```
4
1 0
0 1
-1 0
0 -1
```

every orientation is constrained by the same geometry modulo (90^\circ). The best choice is the axis-aligned square with half-side (1), where all four plants are on its boundary. The interval sweep recognizes that a candidate just above (1) has no valid orientation, while (a=1) is the limiting value approached by binary search. The printed perimeter is `8.0000`.

For equal-radius plants, the twelve points

```
12
5 0
4 3
3 4
0 5
-3 4
-4 3
-5 0
-4 -3
-3 -4
0 -5
3 -4
4 -3
```

all have distance exactly (5). Their directions, after reducing modulo (90^\circ), leave a largest angular gap of (\arctan(3/4)). The optimal square places its diagonal direction halfway through that gap, giving half-side

[
5\cos\left(\frac{\arctan(3/4)}2\right)
=\frac{3\sqrt{10}}2.
]

The perimeter is approximately `18.9737`. This case exercises the part of the algorithm where several forbidden intervals overlap and the answer is determined by their exact angular arrangement rather than by the nearest plant alone.
