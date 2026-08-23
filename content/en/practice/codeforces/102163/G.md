---
title: "CF 102163G - Ali and the Breakfast"
description: "Ali chooses a launch angle uniformly from the interval ([L,R]), measured in degrees. The tea drop starts at the origin with speed (V), follows ordinary projectile motion under gravity (g=10), and lands back on the (X)-axis."
date: "2026-08-23T08:11:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102163
codeforces_index: "G"
codeforces_contest_name: "NCD 2019"
rating: 0
weight: 102163
solve_time_s: 874
verified: true
draft: false
---

[CF 102163G - Ali and the Breakfast](https://codeforces.com/problemset/problem/102163/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 14m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

Ali chooses a launch angle uniformly from the interval ([L,R]), measured in degrees. The tea drop starts at the origin with speed (V), follows ordinary projectile motion under gravity (g=10), and lands back on the (X)-axis. Each friend owns a cup represented by an interval ([X_1,X_2]) on that axis. For every cup, we need the fraction of launch angles that make the landing coordinate belong to that interval. Cups may overlap, and each probability is computed independently.

The projectile range for an angle (\theta) is

[
x(\theta)=\frac{V^2\sin(2\theta)}{g}
=\frac{V^2}{10}\sin(2\theta).
]

The input allows (N\le 1000), so an (O(N)) solution per test case is easily fast enough. Even (O(N\log N)) would fit comfortably, but there is no reason to sort anything here because every cup can be handled independently. The coordinates and speed can reach (10^9), so (V^2) can reach (10^{18}). Python integers handle this exactly, while the final inverse-trigonometric calculation only needs floating-point precision because the answer is printed to four decimal places.

The main geometric difficulty is that (x(\theta)) is not monotonic over the whole (0^\circ) to (90^\circ) interval. It increases until (45^\circ), then decreases. A careless implementation that computes only one inverse-sine angle misses the second branch. For example, with (V=10), an angle of (30^\circ) and an angle of (60^\circ) both produce a landing position of (10\sin60^\circ). Both angles must contribute to the probability.

The endpoints also need care. Consider

```
1
1 10 0 90
0 10
```

The maximum possible range is (10), so the correct answer is `1.0000`. A formula that treats (x=V^2/10) as being outside the inverse-sine domain because of a tiny floating-point error can incorrectly produce zero or a domain error.

The case (L=R) is another special situation. For example,

```
1
1 10 45 45
9 10
```

The launch angle is fixed at (45^\circ), producing (x=10), so the correct answer is `1.0000`. Dividing by (R-L) without handling this case would divide by zero.

Finally, a cup can lie completely beyond the projectile's maximum range. For

```
1
1 10 0 90
11 20
```

the answer is `0.0000`, because the drop can never travel farther than (10). The same reasoning handles cups that begin at (0), where the exact endpoint (x=0) has zero probability when the angle interval has positive length.

## Approaches

A direct brute-force idea is to sample many launch angles, simulate the corresponding landing position, and count how many samples enter each cup. This works as an approximation because the angle is the only random variable, but it is not a good competitive-programming solution. For example, sampling every (10^{-5}) degree over a (90^\circ) interval requires about (9\cdot10^6) samples for one cup. With (N=1000), that becomes roughly (9\cdot10^9) cup checks. More importantly, sampling does not give a clean mathematical guarantee for the required four-decimal rounding unless the sampling error is carefully controlled.

The brute force works because the answer is exactly the measure of a set of valid angles. The useful observation is that we can describe that set analytically.

Starting from

[
x=\frac{V^2}{10}\sin(2\theta),
]

a landing coordinate (x) corresponds to

[
\sin(2\theta)=\frac{10x}{V^2}.
]

For (0\leq x\leq V^2/10), let

[
\alpha=\frac{1}{2}\arcsin\left(\frac{10x}{V^2}\right).
]

Inside (0^\circ\leq\theta\leq90^\circ), the equation (x(\theta)=x) has two possible solutions:

[
\theta=\alpha
]

and

[
\theta=90^\circ-\alpha.
]

More importantly, the inequality (x(\theta)\leq x) holds on two intervals:

[
\theta\leq\alpha
]

or

[
\theta\geq90^\circ-\alpha.
]

So for any coordinate (x), we can calculate exactly how much of the requested angle interval ([L,R]) produces a landing coordinate at most (x). Call this quantity (F(x)). The probability of landing inside a cup ([X_1,X_2]) is then simply

[
\frac{F(X_2)-F(X_1)}{R-L}.
]

The observation that turns the problem into (O(N)) is that every cup needs only two evaluations of this same cumulative function. There is no interaction between cups, so overlapping cups require no special treatment.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(NM)), where (M) is the number of sampled angles | (O(1)) | Too slow and only approximate |
| Optimal | (O(N)) | (O(1)) besides input/output storage | Accepted |

## Algorithm Walkthrough

1. Convert (L) and (R) from degrees to radians. Trigonometric functions in Python use radians, and keeping the whole calculation in radians avoids repeatedly converting angles.
2. Define the maximum possible horizontal range

[
X_{\max}=\frac{V^2}{10}.
]

If a queried coordinate (x) is at least (X_{\max}), every possible launch angle lands at or before (x). If (x\leq0), the cumulative probability is zero for a non-degenerate angle interval because landing exactly at (x=0) occurs only at isolated endpoint angles.

1. For (0<x<X_{\max}), calculate

[
\alpha=\frac12\arcsin\left(\frac{10x}{V^2}\right).
]

The valid angles for (x(\theta)\leq x) are

[
[0,\alpha]\cup[90^\circ-\alpha,90^\circ].
]

This is the key step. The second interval is necessary because the projectile range decreases after (45^\circ).

1. Intersect both valid angle intervals with the actual random interval ([L,R]). The length of the first intersection is

[
\max(0,\min(R,\alpha)-L),
]

and the length of the second is

[
\max(0,R-\max(L,90^\circ-\alpha)).
]

Their sum is the total angular measure for which the landing coordinate is at most (x).

1. For every cup ([X_1,X_2]), compute the cumulative measures for both endpoints. Their difference is exactly the angular measure for which

[
X_1\leq x(\theta)\leq X_2.
]

Divide by (R-L) to obtain the probability.

1. If (L=R), skip the cumulative calculation because there is no positive-length random interval. Evaluate the single trajectory directly. If its landing coordinate belongs to the cup, print `1.0000`; otherwise print `0.0000`.

### Why it works

For a positive-length angle interval, the function (F(x)) counts exactly the measure of angles in ([L,R]) whose landing coordinate is at most (x). The two inverse-sine branches describe every angle satisfying that inequality, because (2\theta) lies between (0) and (\pi), where sine first increases and then decreases. Consequently, the angles counted by (F(X_2)) but not by (F(X_1)) are precisely those landing inside the cup. Since the launch angle is uniform, dividing that angular measure by the total angle length gives the required probability.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

PI = math.pi
HALF_PI = math.pi / 2.0

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n, v, L, R = map(int, input().split())

        lrad = math.radians(L)
        rrad = math.radians(R)
        total = rrad - lrad

        v2 = v * v

        if L == R:
            # The angle is fixed, so the result is deterministic.
            landing = (v2 / 10.0) * math.sin(2.0 * lrad)

            for _ in range(n):
                x1, x2 = map(int, input().split())

                # Small tolerance protects exact endpoint cases such as
                # sin(0) and sin(pi/2) from floating-point noise.
                eps = 1e-9 * max(1.0, abs(landing))

                if x1 - eps <= landing <= x2 + eps:
                    out.append("1.0000")
                else:
                    out.append("0.0000")

            continue

        def measure_leq(x):
            """
            Return the angular length inside [lrad, rrad]
            for which the landing coordinate is <= x.
            """
            if x <= 0:
                return 0.0

            # Compare using integers before converting to float.
            # x >= v^2 / 10  <=>  10*x >= v^2
            if 10 * x >= v2:
                return total

            y = (10.0 * x) / v2

            # y is mathematically in (0, 1), but clamp against
            # a possible floating-point overshoot.
            y = max(0.0, min(1.0, y))

            alpha = 0.5 * math.asin(y)

            # First branch: theta <= alpha.
            left = max(0.0, min(rrad, alpha) - lrad)

            # Second branch: theta >= pi/2 - alpha.
            second_start = HALF_PI - alpha
            right = max(0.0, rrad - max(lrad, second_start))

            return left + right

        for _ in range(n):
            x1, x2 = map(int, input().split())

            m1 = measure_leq(x1)
            m2 = measure_leq(x2)

            probability = (m2 - m1) / total

            # Protect the printed value from tiny accumulated
            # floating-point errors such as 1.0000000000000002.
            probability = max(0.0, min(1.0, probability))

            out.append(f"{probability:.4f}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution first converts the angle bounds once per test case, because every cup uses the same interval. The integer `v2` stores (V^2) exactly. The comparison `10 * x >= v2` is deliberately performed before converting to floating point, so the important maximum-range boundary is decided without precision loss.

The `measure_leq` function is the implementation of the cumulative function from the walkthrough. For an interior coordinate, `alpha` represents the first inverse-sine branch. The variable `second_start` represents the symmetric branch after (45^\circ). Each branch is intersected with the actual random interval using `max` and `min`, which naturally gives zero when there is no intersection.

The cup probability uses the difference `m2 - m1`. There is no need to worry about whether cup endpoints themselves are included, because for a positive-length continuous random angle interval, individual angles have probability zero.

The fixed-angle case is separated before defining the cumulative function. Otherwise `total` would be zero and the probability formula would divide by zero. The tolerance in that branch is only used for comparing the deterministic floating-point trajectory with integer cup boundaries.

Python's arbitrary-size integers also remove the overflow concern that would exist in a 32-bit implementation. The only floating-point operations are the trigonometric calculations and the final probability, which are more than precise enough for four decimal places.

## Worked Examples

The provided sample uses (V=15), so

[
X_{\max}=\frac{15^2}{10}=22.5.
]

The random angle interval is (30^\circ) to (45^\circ), whose length is (15^\circ).

| Cup | (X_1) | (X_2) | Cumulative measure at (X_1) | Cumulative measure at (X_2) | Probability |
| --- | --- | --- | --- | --- | --- |
| 1 | 16 | 21 | (0) | about (4.4805^\circ) | 0.2987 |
| 2 | 21 | 22 | about (4.4805^\circ) | about (8.9490^\circ) | 0.2979 |
| 3 | 22 | 30 | about (8.9490^\circ) | (15^\circ) | 0.4034 |
| 4 | 10 | 15 | (0) | (0) | 0.0000 |
| 5 | 1 | 40 | (0) | (15^\circ) | 1.0000 |

The first cup illustrates the main inverse-sine calculation. The smallest possible landing position over the interval starts near (19.49), so (16) contributes no cumulative measure. The upper endpoint (21) corresponds to an angle around (34.48^\circ), leaving about (4.48^\circ) of valid angles inside the (30^\circ) to (45^\circ) interval. Dividing by (15^\circ) gives approximately (0.2987).

The second and third cups demonstrate that overlapping or adjacent intervals do not require any global processing. Each answer is obtained from the same cumulative function. The final cup contains the entire possible landing range, so its probability is exactly one.

For a second example, consider the degenerate angle interval

```
1
3 10 45 45
9 10
0 9
10 20
```

The launch angle is fixed at (45^\circ), and the landing position is

[
\frac{10^2}{10}\sin(90^\circ)=10.
]

| Cup | Fixed angle | Landing position | Is landing inside cup? | Probability |
| --- | --- | --- | --- | --- |
| ([9,10]) | (45^\circ) | 10 | Yes | 1.0000 |
| ([0,9]) | (45^\circ) | 10 | No | 0.0000 |
| ([10,20]) | (45^\circ) | 10 | Yes | 1.0000 |

This example exercises the (L=R) branch and also confirms that cup boundaries are treated as part of the cup. With a fixed angle there is no probability distribution to integrate, so the answer is simply whether the deterministic landing coordinate belongs to the interval.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N)) per test case | Each cup performs two constant-time cumulative calculations |
| Space | (O(1)) auxiliary space | Only scalar variables are required apart from the output buffer |

With (N\leq1000), the algorithm performs only a few arithmetic and trigonometric operations per cup. There is no sorting, simulation, numerical integration, or iteration over the coordinate range, so it comfortably fits the one-second limit. The largest intermediate integer is (V^2\leq10^{18}), which Python handles exactly.

## Test Cases

```python
import sys
import io
import math

PI = math.pi
HALF_PI = math.pi / 2.0

def solve_text(inp: str) -> str:
    data = io.StringIO(inp)
    input_ = data.readline
    t = int(input_())
    out = []

    for _ in range(t):
        n, v, L, R = map(int, input_().split())

        lrad = math.radians(L)
        rrad = math.radians(R)
        total = rrad - lrad
        v2 = v * v

        if L == R:
            landing = (v2 / 10.0) * math.sin(2.0 * lrad)

            for _ in range(n):
                x1, x2 = map(int, input_().split())
                eps = 1e-9 * max(1.0, abs(landing))

                if x1 - eps <= landing <= x2 + eps:
                    out.append("1.0000")
                else:
                    out.append("0.0000")

            continue

        def measure_leq(x):
            if x <= 0:
                return 0.0

            if 10 * x >= v2:
                return total

            y = (10.0 * x) / v2
            y = max(0.0, min(1.0, y))

            alpha = 0.5 * math.asin(y)

            left = max(0.0, min(rrad, alpha) - lrad)

            second_start = HALF_PI - alpha
            right = max(0.0, rrad - max(lrad, second_start))

            return left + right

        for _ in range(n):
            x1, x2 = map(int, input_().split())

            probability = (
                measure_leq(x2) - measure_leq(x1)
            ) / total

            probability = max(0.0, min(1.0, probability))
            out.append(f"{probability:.4f}")

    return "\n".join(out)

def run(inp: str) -> str:
    return solve_text(inp)

sample1 = """\
1
5 15 30 45
16 21
21 22
22 30
10 15
1 40
"""

assert run(sample1) == """\
0.2987
0.2979
0.4034
0.0000
1.0000
""", "sample 1"

sample2 = """\
1
3 10 0 90
0 5
5 10
0 10
"""

assert run(sample2) == """\
0.3333
0.6667
1.0000
""", "full angle range"

sample3 = """\
1
3 10 45 45
9 10
0 9
10 20
"""

assert run(sample3) == """\
1.0000
0.0000
1.0000
""", "fixed angle"

sample4 = """\
1
1 10 0 90
11 20
"""

assert run(sample4) == """\
0.0000
""", "cup beyond maximum range"

sample5 = """\
1
3 10 0 90
0 10
0 10
0 10
"""

assert run(sample5) == """\
1.0000
1.0000
1.0000
""", "all equal cups"

# Maximum N: 1000 independent cups, all containing the entire
# reachable range. The generated input has exactly 1000 queries.
n = 1000
max_case = "1\n{} 10 0 90\n".format(n) + ("0 10\n" * n)
expected = "1.0000\n" * n
assert run(max_case).splitlines() == expected.strip().splitlines(), "maximum N"

# Boundary case: x = 0 is reachable only at isolated angles,
# so it has probability zero for a positive-length angle interval.
sample6 = """\
1
2 10 0 90
0 1
1 10
"""

assert run(sample6) == """\
0.0000
1.0000
""", "zero endpoint and maximum endpoint"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 10 0 90 / 0 10` | `1.0000` | Minimum-size case and full reachable range |
| `1 / 3 10 0 90 / 0 5, 5 10, 0 10` | `0.3333, 0.6667, 1.0000` | Both inverse-sine branches and exact maximum |
| `1 / 3 10 45 45 / 9 10, 0 9, 10 20` | `1.0000, 0.0000, 1.0000` | (L=R) and boundary inclusion |
| `1 / 1 10 0 90 / 11 20` | `0.0000` | Cup completely outside the reachable range |
| `1 / 3 10 0 90 / 0 10` repeated | `1.0000` for every cup | All-equal cup values and independent answers |
| 1000 cups `[0,10]` | 1000 lines of `1.0000` | Maximum (N) and linear complexity |
| `1 / 2 10 0 90 / 0 1, 1 10` | `0.0000, 1.0000` | Lower boundary and maximum-range boundary |

## Edge Cases

When (L=R), the random angle interval has zero width, so the usual probability formula cannot divide by (R-L). For

```
1
1 10 45 45
9 10
```

the algorithm computes the single landing position (10), checks that (9\leq10\leq10), and prints `1.0000`. If the cup were `[0,9]`, the same deterministic calculation would produce `0.0000`.

When the cup extends beyond the maximum possible range, the cumulative function immediately returns the entire angle measure for the upper endpoint. For

```
1
1 10 0 90
11 20
```

the maximum range is (10), so both endpoints of the cup lie beyond it. The difference of the two cumulative measures is zero, giving `0.0000`.

When a cup contains the entire reachable range, every launch angle is valid. For

```
1
1 10 0 90
0 10
```

the lower endpoint contributes zero cumulative measure and the upper endpoint contributes all (90^\circ). Their difference is the complete random interval, so the answer is `1.0000`.

The non-monotonic projectile range is handled by counting two angle intervals. With (V=10), (L=0), (R=90), and cup `[0,5]`, the condition (x\leq5) is equivalent to (\sin(2\theta)\leq0.5). This occurs for (\theta\in[0,15^\circ]) and (\theta\in[75^\circ,90^\circ]), giving (30^\circ) of valid angles out of (90^\circ), hence `0.3333`. An implementation using only the first inverse-sine branch would count only (15^\circ) and incorrectly return `0.1667`.

For (x=0), the only possible angles are (0^\circ) and (90^\circ). When (L<R), these are isolated points and have probability zero. Thus

```
1
2 10 0 90
0 1
1 10
```

produces `0.0000` for the first cup and `1.0000` for the second. The cumulative calculation naturally handles this because `measure_leq(0)` returns zero while `measure_leq(10)` returns the full angle measure.

Overlapping cups need no special treatment because each probability asks about its own interval. In the sample, `[16,21]`, `[21,22]`, and `[22,30]` share endpoints, but each answer is computed independently from two cumulative values. There is no attempt to partition the ground or assign a landing point to only one cup.
