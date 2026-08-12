---
title: "CF 102318E - Simple Darts"
description: "We have a dartboard centered at the origin. The board is divided radially into w equal wedges, and it has three concentric scoring regions. The innermost circle of radius b is the bullseye and always gives 50 points."
date: "2026-08-13T05:20:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102318
codeforces_index: "E"
codeforces_contest_name: "UCF Locals 2017"
rating: 0
weight: 102318
solve_time_s: 362
verified: true
draft: false
---

[CF 102318E - Simple Darts](https://codeforces.com/problemset/problem/102318/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a dartboard centered at the origin. The board is divided radially into `w` equal wedges, and it has three concentric scoring regions. The innermost circle of radius `b` is the bullseye and always gives 50 points. Between radii `b` and `d` is the double region, where the wedge's value is multiplied by 2. Between radii `d` and `s` is the single region, where the wedge's ordinary value is used. A dart outside radius `s` scores 0.

The wedge immediately counterclockwise from the positive x-axis has value 1. Moving counterclockwise through the wedges increases the value by one, so the wedge immediately clockwise from the positive x-axis has value `w`. For every test case, we are given the board dimensions followed by the coordinates of all darts, and we need the sum of their scores. The original contest statement gives `2 <= w <= 20`, `0 < b < d < s < 100`, and at most 100 darts per test case. The dart coordinates lie between `-100` and `100`, and no dart is within `10^-5` of a wedge boundary or circular boundary.

These bounds make the problem much simpler than many geometry problems. Even an `O(tw)` solution performs at most `100 * 20 = 2000` wedge checks in one test case, so a straightforward solution is already fast enough. Still, we can process each dart in `O(1)` by converting its angle directly into a wedge number, giving `O(t)` time.

The most relevant edge cases are caused by the geometry rather than by large input sizes. A dart at the exact center, for example

```
1
2 1 2 3
1
0.000 0.000
```

scores 50, not 0 or a wedge value. A solution that computes the angle first and treats the center as an ordinary wedge can still happen to produce a value, but that value is meaningless because the bullseye takes precedence over angular scoring.

A dart outside the board must score zero even if its angle points toward a high-value wedge. For example,

```
1
2 1 2 3
1
0.000 4.000
```

scores 0 because its distance from the origin is greater than the outer radius.

A dart in the double ring must use twice the wedge value. With

```
1
2 1 5 8
1
0.000 3.000
```

the dart is in the double ring and lies in the upper wedge, whose value is 1, so the correct output is `2`. Forgetting the multiplier would produce `1`.

The negative-angle case is also easy to mishandle. With

```
1
4 1 5 8
1
1.000 -1.000
```

the angle is `-45` degrees. This belongs to the fourth wedge, not the first wedge, so the dart gets the fourth wedge's value. A careless implementation that simply divides the negative angle by the wedge width gets a negative index.

There is also a historical inconsistency in the archived 2017 statement's first sample. It gives `4 7 13 10`, despite the stated relationship `b < d < s`. The expected answer treats `13` as the outer boundary of the double region, so the implementation below follows the variables exactly as written and reproduces the original sample output. The later samples and the scoring rules are consistent with this interpretation.

## Approaches

The most direct approach is to process every dart independently. First compute its squared distance from the origin. If that value is smaller than `b²`, the dart is worth 50. Otherwise, determine which wedge contains the dart and then multiply that wedge's value by 2, 1, or 0 according to the radial region.

For a brute-force implementation, once the dart's angle is known, we can test that angle against every one of the `w` wedge intervals until we find the matching wedge. This is correct because the wedges partition the full circle. Since there are at most 20 wedges and 100 darts, the worst case is exactly 2000 wedge checks per test case. That is nowhere near enough work to threaten a one-second limit, so this version is already accepted.

The cleaner observation is that the wedges are equal-sized. We do not need to search through them at all. One full revolution has angle `2π`, so each wedge occupies an angle of

`2π / w`.

If the dart has normalized angle `θ` in `[0, 2π)`, its zero-based wedge index is simply

`floor(θ / (2π / w))`.

Adding one converts that index into the dartboard's score from 1 through `w`. This reduces the angular work from `O(w)` to `O(1)`.

The brute-force method works because every dart can be classified independently, but it spends unnecessary work searching for a wedge that can be calculated directly. The equal angular widths are exactly what make the direct formula possible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(tw) | O(1) | Accepted |
| Optimal | O(t) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. Each test case describes one independent dartboard and its throws, so the total score can be reset to zero at the beginning of every case.
2. Read `w`, `b`, `d`, and `s`, then read the number `t` of darts. Store the radii squared as `b²`, `d²`, and `s²`. Comparing squared distances avoids an unnecessary square root and preserves the exact ordering of the radial regions.
3. For every dart at `(x, y)`, compute `r² = x² + y²`. If `r² < b²`, immediately add 50 points. The bullseye has a fixed score, so its angle does not matter.
4. If the dart is not in the bullseye, determine its angular position with `atan2(y, x)`. This function gives the correct angle in all four quadrants, unlike `atan(y / x)`, which loses quadrant information.
5. If the angle is negative, add `2π` so that it lies in `[0, 2π)`. This turns the circular coordinate into a normal nonnegative interval that can be divided into equal wedge widths.
6. Compute `wedge = int(angle / (2π / w)) + 1`. The division determines how many complete wedge intervals occur before the dart's angle, and the `+1` converts the zero-based index into the board's score numbering.
7. Determine the multiplier from the radial position. A dart with `r² < d²` is in the double region and gets multiplier 2. A dart with `r² < s²` is in the single region and gets multiplier 1. A dart beyond `s` gets multiplier 0.
8. Add `wedge * multiplier` to the test case's total and print the total after all darts have been processed.

### Why it works

For every dart, the squared distance uniquely determines which concentric scoring region contains it, while `atan2` uniquely determines its direction. Because all wedges have the same angular width, dividing the normalized angle by `2π/w` gives exactly the index of the wedge containing the dart. The radial multiplier then applies the scoring rule for that region. The only special case is the bullseye, which is checked first because its fixed score overrides the wedge score. Since the problem guarantees that darts do not lie close to boundaries, floating-point rounding cannot make a valid dart switch between adjacent regions.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    tc = int(input())
    out = []

    for _ in range(tc):
        w, b, d, s = map(int, input().split())
        t = int(input())

        b2 = b * b
        d2 = d * d
        s2 = s * s

        wedge_angle = 2.0 * math.pi / w
        total = 0

        for _ in range(t):
            x, y = map(float, input().split())
            r2 = x * x + y * y

            if r2 < b2:
                total += 50
                continue

            angle = math.atan2(y, x)
            if angle < 0:
                angle += 2.0 * math.pi

            wedge = int(angle / wedge_angle) + 1

            if r2 < d2:
                total += 2 * wedge
            elif r2 < s2:
                total += wedge

        out.append(str(total))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first three squared-radius variables are computed once per test case because the board does not change between darts. Comparing `r2` with these values avoids `sqrt`, so every radial classification uses only arithmetic comparisons.

The bullseye check comes before the angle calculation. Besides being slightly cheaper, this directly reflects the scoring hierarchy: a dart in the bullseye always scores 50, regardless of direction.

`atan2(y, x)` is used instead of `atan(y / x)` because `atan` cannot distinguish, for example, `(1, -1)` from `(-1, 1)`. `atan2` handles the full circle correctly. Negative results are shifted by `2π`, producing an angle in the range `[0, 2π)`.

The expression `int(angle / wedge_angle) + 1` is the key geometric calculation. Because the dart is guaranteed not to be close to a wedge boundary, no epsilon adjustment is necessary. The same boundary guarantee lets us use strict `<` comparisons for the radii.

Python integers have arbitrary precision, so there is no integer overflow concern. The floating-point values are only used for coordinates and angles, while all final scores remain integers.

## Worked Examples

### Sample 1

The original contest sample is:

```
3
4 7 13 10
2
4.000 4.000
6.000 -4.000
10 1 6 10
1
20.000 -0.500
8 3 7 50
5
-0.750 1.207
1.180 3.132
27.111 -44.630
-43.912 -22.104
2.000 -6.000
```

The first test case demonstrates both the bullseye and double-ring handling.

| Dart | x | y | r² | Angle | Wedge | Region | Score | Total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 4 | 4 | 32 | not needed | not needed | Bullseye | 50 | 50 |
| 2 | 6 | -4 | 52 | 326.31° | 4 | Double | 8 | 58 |

The first dart has squared distance 32, which is less than `7² = 49`, so it immediately scores 50. The second dart has squared distance 52, which places it below `13² = 169` and outside the bullseye. Its negative angle is normalized to about 326.31 degrees, placing it in wedge 4. The double multiplier changes its score from 4 to 8, giving a total of 58.

### Sample 3

The third test case is more representative because it exercises all scoring regions.

| Dart | x | y | r² | Region | Wedge | Multiplier | Score | Running total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | -0.750 | 1.207 | ≈2.02 | Bullseye | not needed | not needed | 50 | 50 |
| 2 | 1.180 | 3.132 | ≈11.21 | Double | 2 | 2 | 4 | 54 |
| 3 | 27.111 | -44.630 | ≈2730 | Outside | not needed | 0 | 0 | 54 |
| 4 | -43.912 | -22.104 | ≈2415 | Single | 5 | 1 | 5 | 59 |
| 5 | 2.000 | -6.000 | 40 | Double | 7 | 2 | 14 | 73 |

The first dart is inside radius 3 and scores 50. The second is between radii 3 and 7 and lies in wedge 2, so it scores 4. The third is beyond the radius 50 board and scores zero. The fourth lies in the single ring and points into wedge 5, giving 5. The last dart is in the double ring and points into wedge 7, giving 14. The final total is 73.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) per test case | Each of the `t` darts requires a constant number of arithmetic, trigonometric, and comparison operations. |
| Space | O(1) | Only the board parameters, current dart, and running score are stored. |

With at most 100 darts per test case, the algorithm performs only a few hundred constant-time operations per case. The `w <= 20` bound is not even needed by the optimal solution's asymptotic complexity, since the number of wedges only appears in one division.

## Test Cases

```python
import sys
import io
import math

def solve():
    input = sys.stdin.readline
    tc = int(input())
    out = []

    for _ in range(tc):
        w, b, d, s = map(int, input().split())
        t = int(input())

        b2 = b * b
        d2 = d * d
        s2 = s * s
        wedge_angle = 2.0 * math.pi / w

        total = 0

        for _ in range(t):
            x, y = map(float, input().split())
            r2 = x * x + y * y

            if r2 < b2:
                total += 50
                continue

            angle = math.atan2(y, x)
            if angle < 0:
                angle += 2.0 * math.pi

            wedge = int(angle / wedge_angle) + 1

            if r2 < d2:
                total += 2 * wedge
            elif r2 < s2:
                total += wedge

        out.append(str(total))

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

sample = """\
3
4 7 13 10
2
4.000 4.000
6.000 -4.000
10 1 6 10
1
20.000 -0.500
8 3 7 50
5
-0.750 1.207
1.180 3.132
27.111 -44.630
-43.912 -22.104
2.000 -6.000
"""

assert run(sample) == "58\n0\n73", "provided samples"

assert run("""\
1
2 1 2 3
1
0.000 0.000
""") == "50", "minimum-size bullseye"

assert run("""\
1
20 1 10 99
100
100.000 100.000
""" + "\n".join(["100.000 100.000"] * 99) + "\n") == "0", \
    "maximum-size outside-board case"

assert run("""\
1
2 1 10 20
100
0.000 0.000
""" + "\n".join(["0.000 0.000"] * 99) + "\n") == "5000", \
    "all-equal bullseye values"

assert run("""\
1
2 2 5 8
4
0.000 1.000
0.000 3.000
0.000 6.000
0.000 9.000
""") == "53", "radial region boundaries"

assert run("""\
1
4 1 5 8
1
1.000 -1.000
""") == "8", "negative-angle fourth wedge"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 2 1 2 3 / 1 / 0 0` | `50` | Minimum-size board and bullseye precedence |
| `20 1 10 99` with 100 darts at `(100,100)` | `0` | Maximum number of darts and outside-board handling |
| 100 identical darts at `(0,0)` | `5000` | Repeated identical values and accumulation |
| `2 2 5 8` with radii 1, 3, 6, 9 | `53` | Bull, double, single, and outside regions |
| `4 1 5 8` with `(1,-1)` | `8` | Negative angle normalization and fourth wedge |

## Edge Cases

The bullseye must be checked before any angular calculation. For

```
1
2 1 2 3
1
0.000 0.000
```

we get `r² = 0`, which is smaller than `b² = 1`. The algorithm immediately adds 50 and skips `atan2`, producing `50`. This avoids assigning an arbitrary wedge to the center point.

A dart outside the board follows the same angular calculation as an ordinary dart, but its multiplier remains zero. For

```
1
2 1 2 3
1
0.000 4.000
```

the squared distance is 16, larger than `s² = 9`, so no score is added. The result is `0`.

The double ring is handled before the single ring because the radial regions are nested. For

```
1
2 1 5 8
1
0.000 3.000
```

the squared distance is 9, which lies between `1²` and `5²`. The point is in wedge 1, so its base value is 1 and the double multiplier gives `2`.

The single ring works similarly. For

```
1
2 1 5 8
1
0.000 6.000
```

the squared distance is 36, which lies between `5²` and `8²`. The point is still in wedge 1, but the multiplier is now 1, giving `1`.

A negative angle must be normalized before finding the wedge. For

```
1
4 1 5 8
1
1.000 -1.000
```

`atan2(-1, 1)` returns `-π/4`. Adding `2π` produces `7π/4`, which belongs to the fourth of four 90-degree wedges. The base score is 4 and the point is in the double ring, so the result is `8`.

Finally, the contest sample containing `4 7 13 10` deserves special care. The written constraints say `b < d < s`, but that particular historical sample reverses the last two radii. The expected output of 58 is obtained by treating the dart at `(6,-4)` as being inside the double region because its distance is about 7.21, below `d = 13`. The code deliberately does not sort or reinterpret the three radii. It follows the scoring comparisons in their input order, which reproduces the official sample while also behaving normally on valid cases satisfying `b < d < s`.
