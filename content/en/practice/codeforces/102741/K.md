---
title: "CF 102741K - Crafty Explosions"
description: "The problem asks for the least volatility of one newly placed TNT piece so that every existing TNT piece is guaranteed to explode immediately. The new TNT can be placed at any real-valued position in three-dimensional space."
date: "2026-07-29T00:50:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102741
codeforces_index: "K"
codeforces_contest_name: "UTPC Contest 9-25-20 Div. 1"
rating: 0
weight: 102741
solve_time_s: 44
verified: true
draft: false
---

[CF 102741K - Crafty Explosions](https://codeforces.com/problemset/problem/102741/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
# Problem Understanding

The problem asks for the least volatility of one newly placed TNT piece so that every existing TNT piece is guaranteed to explode immediately. The new TNT can be placed at any real-valued position in three-dimensional space. For an existing TNT at `(xi, yi, zi)` with volatility constant `vi`, the required volatility of the new TNT is its Manhattan distance from that point divided by `vi`. The task is to choose the placement position that minimizes the maximum required volatility among all TNT pieces.

The input contains up to 20000 TNT pieces. Each piece contributes a constraint on the possible location of the new TNT. A quadratic search over pairs of TNT pieces or a grid search over coordinates is far too expensive because coordinates can reach one million and the answer can be a real number. With this input size, the algorithm needs to be close to linear or linear times a small logarithmic factor.

A few edge cases are easy to miss. If there is only one TNT piece, the new TNT can be placed exactly at the same position and the answer is zero.

For example:

```
1
5 5 5 10
```

The correct output is:

```
0.00000000
```

A careless implementation that assumes the answer must be positive would fail here.

Another subtle case is when the best location is not an existing TNT coordinate. Consider:

```
4
0 0 0 1
1 2 0 1
3 4 0 1
2 1 0 1
```

The correct output is:

```
3.50000000
```

The optimal point lies between existing coordinates. Checking only integer positions or only existing TNT locations would miss the answer.

The volatility constants also change the influence of each point. For example:

```
3
1 0 0 1
2 1 1 4
3 2 3 2
```

The correct output is:

```
2.33333333
```

Treating every TNT as having the same weight would incorrectly solve an ordinary geometric center problem instead of the weighted version.

## Approaches

A direct approach is to try candidate positions and calculate the required volatility at each one. The difficulty is that the position is continuous, not restricted to integer coordinates. Even if we somehow generated all interesting coordinates, comparing all possible candidates would become impractical. The search space has no natural small bound.

The key observation is to reverse the problem. Instead of asking where the TNT should be placed for a given volatility, ask whether a chosen volatility `T` is enough.

For a fixed `T`, every TNT piece defines a region of allowed locations. The new TNT must be within Manhattan distance `T * vi` from every existing TNT. The question becomes whether all these regions share at least one common point.

Manhattan distance in three dimensions has a useful transformation. For any point `(x, y, z)`, define four values:

```
s1 = x + y + z
s2 = x + y - z
s3 = x - y + z
s4 = -x + y + z
```

For any two points, their Manhattan distance equals the maximum absolute difference among these four transformed coordinates. This converts the original three-dimensional diamond-shaped regions into four independent interval constraints.

For a TNT with transformed values `s1, s2, s3, s4`, a candidate volatility `T` requires:

```
|S1 - s1| <= T * vi
|S2 - s2| <= T * vi
|S3 - s3| <= T * vi
|S4 - s4| <= T * vi
```

Each of the four transformed coordinates now only needs its intervals to overlap. If the intersection of all intervals is non-empty for every transformed coordinate, then the chosen volatility works.

The answer can be found with binary search on `T`. Each feasibility check scans all TNT pieces once, so the complete algorithm is fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(search space × N) | O(1) | Too slow |
| Optimal | O(N log C) | O(N) | Accepted |

Here `C` is the numeric range covered by the binary search. Using a fixed number of iterations makes this effectively constant, around 70 checks for double precision.

## Algorithm Walkthrough

1. Transform every TNT position `(x, y, z)` into four values:

```
x + y + z
x + y - z
x - y + z
-x + y + z
```

The transformation works because Manhattan distance becomes the maximum difference among these four coordinates.

1. Binary search the answer `T`, the volatility of the newly placed TNT. Start with a lower bound of zero and a sufficiently large upper bound.
2. For each binary search midpoint `T`, check whether this volatility is possible. For every transformed coordinate, maintain the intersection interval of all possible values.
3. For a TNT with volatility `v`, its transformed coordinate `a` allows the new transformed coordinate to be anywhere inside:

```
[a - T*v, a + T*v]
```

Intersect this interval with the current global interval.

1. If any of the four transformed coordinate intervals becomes empty, `T` cannot work. Otherwise, `T` is feasible.
2. After enough binary search iterations, output the lower bound as the minimum required volatility.

Why it works:

For a fixed volatility `T`, every TNT piece independently restricts the possible transformed coordinates of the answer. The transformation preserves Manhattan distance exactly, so satisfying the four interval constraints is equivalent to satisfying the original three-dimensional distance constraints. The algorithm declares a value feasible exactly when all four transformed dimensions have a common valid value, which means a real point exists that satisfies every TNT requirement. Binary search then finds the smallest feasible value because feasibility is monotonic: increasing the volatility can only expand the allowed regions.

## Python Solution

```python
import sys

input = sys.stdin.readline

def solve():
    n = int(input())
    points = []

    for _ in range(n):
        x, y, z, v = map(int, input().split())
        points.append((
            x + y + z,
            x + y - z,
            x - y + z,
            -x + y + z,
            v
        ))

    def possible(t):
        low = [-10**30] * 4
        high = [10**30] * 4

        for a, b, c, d, v in points:
            vals = (a, b, c, d)
            radius = t * v

            for i in range(4):
                low[i] = max(low[i], vals[i] - radius)
                high[i] = min(high[i], vals[i] + radius)
                if low[i] > high[i]:
                    return False

        return True

    left = 0.0
    right = 3 * 10**6

    for _ in range(80):
        mid = (left + right) / 2
        if possible(mid):
            right = mid
        else:
            left = mid

    print("{:.10f}".format(right))

if __name__ == "__main__":
    solve()
```

The input is read once and every TNT is stored after applying the coordinate transformation. Keeping transformed values avoids recomputing the same expressions during every binary search iteration.

The `possible` function represents the feasibility test. The arrays `low` and `high` store the current intersection of allowed intervals for each transformed dimension. When processing a TNT, the allowed interval is narrowed using `max` and `min`. If the lower endpoint ever exceeds the upper endpoint, no placement can satisfy the current volatility.

The binary search uses floating point values because the answer is not necessarily an integer. Eighty iterations are more than enough for the required `1e-6` precision. The upper bound of `3 * 10^6` is safe because coordinates differ by at most three million in Manhattan distance and every volatility constant is at least one.

## Worked Examples

For the first sample:

```
4
0 0 0 1
1 2 0 1
3 4 0 1
2 1 0 1
```

The binary search tests different volatility values. At a value below `3.5`, the transformed intervals leave at least one dimension with no common overlap. At `3.5`, all four transformed dimensions have an intersection.

| Iteration | Tested volatility | Result |
| --- | --- | --- |
| Early search | 1500000.0 | Possible |
| Middle search | 3.0 | Impossible |
| Middle search | 4.0 | Possible |
| Final search | 3.5 | Possible |

The trace demonstrates the monotonic property. Once a volatility is large enough, every larger value remains valid.

For the second sample:

```
1
1 1 1 1
```

| Step | TNT count processed | Interval status |
| --- | --- | --- |
| Initial | 0 | All intervals unlimited |
| After TNT | 1 | All four intervals contain the same point |

The answer is zero because the chosen point can exactly match the only TNT location. This checks the zero-distance case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log C) | Each binary search step scans all TNT pieces, and the number of iterations is fixed for floating point precision. |
| Space | O(N) | The transformed coordinates of all TNT pieces are stored. |

The algorithm performs about 80 linear passes over at most 20000 TNT pieces, which is easily within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

# sample 1
assert abs(float(run("""4
0 0 0 1
1 2 0 1
3 4 0 1
2 1 0 1
""")) - 3.5) < 1e-6

# sample 2
assert abs(float(run("""1
1 1 1 1
"""))) < 1e-6

# sample 3
assert abs(float(run("""3
1 0 0 1
2 1 1 4
3 2 3 2
""")) - 2.33333333) < 1e-6

# same position, different volatility values
assert abs(float(run("""3
5 5 5 1
5 5 5 100
5 5 5 2
"""))) < 1e-6

# boundary case with far apart points
assert abs(float(run("""2
0 0 0 1
1000000 1000000 1000000 1
""")) - 1500000.0) < 1e-6
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single TNT | 0 | Zero-distance handling |
| Sample 1 | 3.5 | Non-integer optimal position |
| Sample 3 | 2.33333333 | Weighted volatility handling |
| Multiple TNT at same coordinate | 0 | Duplicate coordinates |
| Extreme coordinates | 1500000 | Large values and precision |

## Edge Cases

For the single TNT case:

```
1
5 5 5 10
```

The binary search checks whether zero works. The transformed intervals for the only TNT all collapse to one point, and their intersection is valid. The algorithm keeps reducing the answer until it reaches zero.

For a case where the answer is not an existing coordinate:

```
4
0 0 0 1
1 2 0 1
3 4 0 1
2 1 0 1
```

The feasibility check does not try to guess the actual location. Instead, it verifies whether the transformed intervals overlap. At volatility `3.5`, every transformed interval shares a common value, proving that some real point exists even though it is not one of the original TNT positions.

For different volatility constants:

```
3
1 0 0 1
2 1 1 4
3 2 3 2
```

The TNT with volatility `4` allows a much larger distance for the same required volatility. The interval intersection naturally accounts for this by multiplying each radius by its own volatility constant during every check. The algorithm never assumes equal weights, so the resulting value matches the weighted geometry of the problem.
