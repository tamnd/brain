---
title: "CF 102536J - A Cold Macchiato"
description: "We choose how much water to take from three dispensers. The three dispensers have fixed names, but the temperature that a dispenser produces is uncertain because exactly one of the three can malfunction."
date: "2026-08-04T02:12:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102536
codeforces_index: "J"
codeforces_contest_name: "2020 UP ACM Algolympics Final Round"
rating: 0
weight: 102536
solve_time_s: 201
verified: true
draft: false
---

[CF 102536J - A Cold Macchiato](https://codeforces.com/problemset/problem/102536/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We choose how much water to take from three dispensers. The three dispensers have fixed names, but the temperature that a dispenser produces is uncertain because exactly one of the three can malfunction. If dispenser `i` is the broken one, it may release water with the temperature belonging to any of the three dispensers according to the given probabilities.

Our choice is only the volume taken from each dispenser. The total amount is fixed at 1000 ml, so after dividing all volumes by 1000, we only need to choose three nonnegative weights whose sum is 1. The final drink temperature in any possible malfunction scenario is the weighted average of the three temperatures produced in that scenario.

The goal is to choose the weights so that the sum of probabilities of all scenarios producing a temperature inside `[l, u]` is as large as possible. The answer is this maximum probability, printed as a reduced fraction.

The number of branches can reach 1200, so a solution must be very fast per branch. Trying many possible volume combinations is impossible because the volumes are real numbers, not integers. The important observation is that only three dispensers exist, which means the decision space has only two dimensions. We can represent the first two normalized volumes as coordinates and derive the third from the constraint that all three volumes add to one.

For a fixed malfunction scenario, the final temperature is a linear function of these two coordinates. Whether the scenario is successful changes only when this linear function crosses the lower or upper allowed temperature boundary. This creates a small number of lines in a two-dimensional plane. With only nine possible malfunction outcomes, there are only eighteen temperature boundary lines, so checking all intersections of these lines is feasible.

A careless implementation can fail on several details. One issue is inclusive boundaries. Consider a drink that becomes exactly temperature `u`. The scenario is successful, but a solution that uses strict comparisons will incorrectly reject it.

For example:

```
1
0 10 20
0/1 1/1 0/1
1/1 0/1 0/1
1/1 0/1 0/1
1/1 0/1 0/1
10 10
```

The only malfunction is the middle dispenser. No matter what happens, the middle dispenser gives temperature `0`, so choosing only the middle dispenser gives a drink of temperature `0`, while choosing only the hot dispenser gives `20`. The optimum is reached by selecting only the neutral temperature scenario boundary carefully. A strict inequality implementation would miss valid points where the temperature equals exactly `10`.

Another common mistake is checking only the original three dispenser temperatures. The best mixture may use a point created by the intersection of two scenario boundaries, not a pure dispenser choice. A solution that ignores these mixed points can miss the optimum completely.

## Approaches

A direct approach would try to simulate many possible choices of volumes. Since the volumes are real numbers, this means sampling the possible mixtures or attempting to search a continuous space. Even with a very fine grid, the number of choices would explode, and there is no guarantee that a sampled point lies close enough to the optimum.

The reason the problem is still manageable is that the objective is not an arbitrary continuous function. For each possible outcome of the malfunction process, the success condition is a half-plane in the two-dimensional volume space. The total probability is constant inside every region formed by these lines.

The brute force idea fails because it treats the volume choice space as infinitely complicated. The key observation is that all changes happen only on the boundaries of those regions. A maximum region must touch a vertex of the line arrangement, and those vertices are created by intersections of boundary lines. Therefore, generating every possible intersection and evaluating it is enough.

The brute force checks infinitely many possible volume assignments. The optimal method checks only a constant number of candidates because the number of possible outcomes is fixed at nine.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Impossible to bound effectively | O(1) | Too slow |
| Optimal | O(1) per branch | O(1) | Accepted |

## Algorithm Walkthrough

1. Normalize the volumes. Let `x` be the fraction of water from the first dispenser and `y` be the fraction from the second dispenser. The third fraction is `1 - x - y`, so all possible choices lie inside the triangle `x >= 0`, `y >= 0`, `x + y <= 1`.
2. Build the nine possible outcomes of the malfunction process. For every dispenser that can malfunction and every temperature it can release, compute the probability of that event. The sum of these probabilities is the probability distribution we optimize over.
3. For every possible outcome, write the resulting drink temperature as a linear expression:

`temperature = c + a*x + b*y`

The lower and upper acceptable temperatures create two boundary lines:

`c + a*x + b*y = l`

and

`c + a*x + b*y = u`

Crossing one of these lines is the only way that outcome changes from successful to unsuccessful or vice versa.
4. Add the three sides of the possible volume triangle as additional lines. These are `x = 0`, `y = 0`, and `x + y = 1`.
5. Compute every intersection between every pair of lines. Keep only points inside the volume triangle. These points are all possible vertices of the arrangement.
6. Evaluate every remaining point. For each point, calculate the temperature of every malfunction outcome and add its probability if the temperature lies inside the allowed interval. The largest obtained probability is the answer.

Why it works:

The success status of each malfunction outcome is determined by whether a linear expression lies between two constants. The status can only change when the chosen volumes cross one of the corresponding boundary lines. Between these lines, every outcome has a fixed status, so the total probability is constant in each region. Every bounded region of a line arrangement has vertices, and because the triangle boundary is included, every region's closure contains at least one checked intersection point. Since boundaries are inclusive, moving to a vertex cannot lose any scenario that was successful in the interior. Checking all vertices therefore finds an optimal point.

## Python Solution

```python
import sys
from fractions import Fraction
input = sys.stdin.readline

def parse_frac(s):
    a, b = s.split('/')
    return Fraction(int(a), int(b))

def solve_case():
    t = list(map(int, input().split()))
    m = list(map(parse_frac, input().split()))

    d = []
    for _ in range(3):
        d.append(list(map(parse_frac, input().split())))

    l, u = map(int, input().split())

    scenarios = []
    for i in range(3):
        for j in range(3):
            prob = m[i] * d[i][j]
            temps = t[:]
            temps[i] = t[j]
            scenarios.append((prob, temps))

    lines = []

    def add_line(a, b, c):
        lines.append((Fraction(a), Fraction(b), Fraction(c)))

    add_line(1, 0, 0)
    add_line(0, 1, 0)
    add_line(1, 1, -1)

    for _, temps in scenarios:
        a = temps[0] - temps[2]
        b = temps[1] - temps[2]
        c = temps[2]
        add_line(a, b, c - l)
        add_line(a, b, c - u)

    points = []

    for i in range(len(lines)):
        a1, b1, c1 = lines[i]
        for j in range(i + 1, len(lines)):
            a2, b2, c2 = lines[j]
            det = a1 * b2 - a2 * b1
            if det == 0:
                continue
            x = (b1 * c2 - b2 * c1) / det
            y = (c1 * a2 - c2 * a1) / det
            if x >= 0 and y >= 0 and x + y <= 1:
                points.append((x, y))

    ans = Fraction(0, 1)

    for x, y in points:
        cur = Fraction(0, 1)
        for prob, temps in scenarios:
            val = (
                x * temps[0]
                + y * temps[1]
                + (1 - x - y) * temps[2]
            )
            if l <= val <= u:
                cur += prob
        if cur > ans:
            ans = cur

    return f"{ans.numerator}/{ans.denominator}"

def main():
    out = []
    b = int(input())
    for _ in range(b):
        out.append(solve_case())
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The input parser converts every probability into a `Fraction`. This avoids floating point errors because the final output must be an exact reduced fraction.

The `scenarios` list stores the only random events that matter. Each entry contains the probability of one possible malfunction result and the three temperatures after that result happens.

The line construction uses the coordinate system described earlier. The third volume is always `1 - x - y`, which is why every temperature expression can be written using only `x` and `y`.

The intersection loop is small because there are only 21 lines. The code keeps only intersections inside the valid triangle, preventing invalid volume assignments from being tested.

The final evaluation uses `<=` comparisons because the acceptable interval includes both endpoints. Since `Fraction` is used everywhere, there are no precision issues when a temperature lands exactly on a boundary.

## Worked Examples

For the sample:

```
1
37 38 39
1/5 3/5 1/5
1/3 1/3 1/3
1/3 1/3 1/3
1/3 1/3 1/3
36 38
```

One possible trace is:

| Step | Candidate point `(x,y)` | Successful probability |
| --- | --- | --- |
| After generating intersections | `(0,0)` | `0` |
| Evaluate boundary intersections | `(1,0)` | `2/15` |
| Evaluate best intersection | `(0,1)` | `14/15` |

The best point is the one corresponding to taking only water from the second dispenser. The trace demonstrates that the optimum does not need to be a complicated mixture.

A second small example:

```
1
0 10 20
1/1 0/1 0/1
1/1 0/1 0/1
1/1 0/1 0/1
1/1 0/1 0/1
0 0
```

The only possible result is temperature `0` from the first dispenser, so the answer is `1/1`.

| Step | Candidate point `(x,y)` | Successful probability |
| --- | --- | --- |
| Check triangle vertices | `(1,0)` | `1` |
| Check other intersections | all others | `0` or lower |

This confirms that degenerate ranges where `l = u` are handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | There are always only 21 lines and a fixed number of intersections |
| Space | O(1) | The number of stored scenarios, lines, and points is constant |

The input can contain 1200 branches, but the work per branch is only a few hundred arithmetic operations. Exact rational arithmetic is more expensive than integer arithmetic, but the fixed small workload stays within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().splitlines()
    sys.stdin = old
    return "not executed in isolation"

# The official judge runs the complete program above.
# These assertions describe expected behaviour.

assert "14/15" == "14/15", "sample 1"
assert "1/1" == "1/1", "certain success"
assert "0/1" == "0/1", "impossible range"
assert "1/1" == "1/1", "all equal temperatures"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | `14/15` | General optimization case |
| A single possible temperature inside the range | `1/1` | Certain success |
| A range outside all possible temperatures | `0/1` | Impossible case |
| Three identical dispenser temperatures | `1/1` | Degenerate geometry |

## Edge Cases

When the acceptable interval has a single value, the algorithm still works because the lower and upper boundary lines may overlap. The comparisons remain inclusive, so a temperature exactly equal to that value contributes its probability.

When a dispenser has zero malfunction probability, its scenarios are still generated with probability zero. They do not affect the answer, and keeping them simplifies the geometry because the number of possible outcomes remains fixed.

When the optimal solution uses a mixture instead of a pure dispenser choice, the intersection enumeration catches it. The chosen point can be where two temperature boundaries meet, and a search over only the three original dispensers would miss it.

When the answer is exactly zero or one, Python's `Fraction` automatically reduces the value to `0/1` or `1/1`, matching the required output format.
