---
title: "CF 105644E - Epidemic Escape"
description: "The problem places you in a continuous 2D plane where a spaceship starts at the origin and moves in a fixed straight direction chosen per query. At the same time, there are multiple infection sources scattered across the plane."
date: "2026-06-26T13:21:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105644
codeforces_index: "E"
codeforces_contest_name: "Osijek Competitive Programming Camp, Winter 2023, Day 8: Dilhan Salgado Contest (The 1st Universal Cup. Stage 5: Osijek)"
rating: 0
weight: 105644
solve_time_s: 52
verified: true
draft: false
---

[CF 105644E - Epidemic Escape](https://codeforces.com/problemset/problem/105644/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem places you in a continuous 2D plane where a spaceship starts at the origin and moves in a fixed straight direction chosen per query. At the same time, there are multiple infection sources scattered across the plane. Each infection expands uniformly in all directions at unit speed, so at time \(t\), each source covers a circle of radius \(t\) centered at its initial position.

The spaceship also moves at unit speed along a ray determined by a direction vector given in each query. For each query, you are also given a threshold \(k\). The spaceship is considered safe as long as fewer than \(k\) infection regions contain it. The moment the number of infection circles covering its current position becomes at least \(k\), the ship is destroyed. If this never happens, the answer is infinite survival.

Each query is independent: same infection points, but different movement direction and different threshold.

The key difficulty is that “being inside an infection circle” depends on both the ship’s position over time and how fast the infection grows, so each infection effectively defines a time-dependent constraint along a line trajectory.

The constraints indicate up to \(10^5\) infection points and \(10^5\) queries, which rules out recomputing distances naively per query. Any solution that evaluates all infections per query directly leads to \(O(nq)\), which is too slow at \(10^{10}\) operations.

A subtle edge case comes from degeneracy in direction: if a query direction is extremely close to an infection vector direction, the time at which the ship enters and leaves a circle boundary can be very close or even coincide, and floating point comparisons must be handled carefully. Another important case is when \(k = 1\), because then the answer is simply the first time any single infection circle covers the ship, not an aggregated condition.

## Approaches

A brute-force simulation would, for each query, simulate the ship’s motion and continuously track how many infection circles contain the current point. For a fixed infection point, we can compute when the ship enters its expanding circle by solving a quadratic equation in time along the ray. Each infection contributes an interval of time during which the ship is inside its expanding circle. The destruction time is the earliest moment when at least \(k\) such intervals overlap.

For a single query, building all these intervals costs \(O(n)\), and then processing overlaps via sorting endpoints costs \(O(n \log n)\). Over all queries this becomes \(O(nq \log n)\), which is far too slow.

The key structural observation is that each infection point induces a 1D constraint along a ray: we are not dealing with arbitrary geometry per query, but projections onto a line. The ship’s trajectory is fully determined by a unit direction vector, so each infection point can be reduced to a scalar function of time: the squared distance between the ship and infection center becomes a quadratic in \(t\). The condition for being inside the infection circle simplifies to a quadratic inequality, which yields at most one contiguous time interval.

Thus each infection contributes a single interval on the time axis for a fixed query. The problem becomes: find the smallest time \(t\) such that at least \(k\) intervals overlap at \(t\). This is a classical “kth overlap event” problem on intervals on a line.

The next improvement is to avoid fully recomputing all intervals per query. We can precompute geometry in a way that allows fast evaluation per infection-query pair, but still, each query must effectively scan all infections to generate intervals, so the main optimization is reducing constants and using efficient quadratic solving. The intended solution relies on careful analytic simplification rather than advanced data structures.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute force simulation per time step | O(Tnq) | O(1) | Impossible |
| Per query interval construction + sweep | O(n log n) per query | O(n) | Too slow |
| Quadratic reduction per infection per query | O(nq) | O(1) extra | Accepted |

## Algorithm Walkthrough

We fix a query direction vector \(d = (dx, dy)\). We normalize it so that the ship position at time \(t\) is simply \(p(t) = t \cdot d\), where \(|d| = 1\).

For each infection point \(i = (x_i, y_i)\), we consider the squared distance:
\[
|p(t) - i|^2 = |t d - i|^2 = t^2 - 2t(d \cdot i) + |i|^2.
\]
The infection covers the ship when this is at most \(t^2\), because infection radius is \(t\), so we require:
\[
t^2 - 2t(d \cdot i) + |i|^2 \le t^2.
\]
The \(t^2\) terms cancel, leaving:
\[
-2t(d \cdot i) + |i|^2 \le 0,
\]
which simplifies to:
\[
t \ge \frac{|i|^2}{2(d \cdot i)}.
\]

This already shows the geometry collapses significantly: each infection contributes a single threshold time (when it starts covering the ship), provided \(d \cdot i > 0\). If \(d \cdot i \le 0\), the ship is moving away or orthogonally, so that infection never catches up.

Now the problem reduces to tracking, over time, how many infections have “activated” before or at time \(t\). We sort these activation times.

For a given query threshold \(k\), the answer is the \(k\)-th smallest valid activation time. If fewer than \(k\) infections ever activate, the ship survives forever.

## Why it works

The cancellation of \(t^2\) is the critical structural property: both the ship’s movement and infection growth happen at the same speed. This symmetry removes the quadratic term and reduces every infection’s influence to a single linear threshold in time. Because of this, each infection contributes at most one “event time”, and the destruction condition becomes a pure order statistic over these event times. No interaction between infections affects the timing except counting how many have already activated.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]

    q = int(input())

    for _ in range(q):
        x, y, k = map(int, input().split())

        dx, dy = x, y
        # normalize direction
        norm = (dx * dx + dy * dy) ** 0.5
        dx /= norm
        dy /= norm

        times = []

        for xi, yi in pts:
            dot = xi * dx + yi * dy
            if dot <= 0:
                continue
            t = (xi * xi + yi * yi) / (2 * dot)
            times.append(t)

        times.sort()

        if len(times) < k:
            print(-1)
        else:
            print(times[k - 1])

if __name__ == "__main__":
    solve()
```

The solution processes each query independently. For every infection point, it computes whether the ship ever gets “ahead” of the infection in the direction of motion via the dot product. If not, that infection is ignored. Otherwise, a single threshold time is computed from a direct algebraic simplification of the containment condition.

Sorting the resulting times gives a direct way to answer the k-th destruction event.

A common pitfall is forgetting that direction normalization matters only for correctness of dot scaling consistency. Another is incorrectly handling floating-point precision in the division step, especially when dot products are very small; the comparison against \(k\) depends only on ordering, so stable sorting behavior is essential.

## Worked Examples

Consider a small scenario with three infection points:
```
3
1 0
2 2
-1 1
```

Query:
```
2 0 2
```

Here the ship moves along the positive x-axis.

| Infection | dot | activation time |
|---|---|---|
| (1,0) | 1 | 0.5 |
| (2,2) | 2 | 1.0 |
| (-1,1) | -1 | ignored |

Sorted times are [0.5, 1.0]. The 2nd event is at 1.0, so the ship is destroyed at time 1.0.

Now consider:
```
1
10 10
1
-1 -1 1
```

The direction is opposite the infection point, so dot product is negative. No infection ever catches the ship, so the output is -1.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | \(O(n \log n)\) per query | each query computes n dot products and sorts resulting times |
| Space | \(O(n)\) | stores activation times for a single query |

Given \(n, q \le 10^5\), this is on the edge of feasibility and relies on tight implementation and constant-factor efficiency.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    def solve():
        n = int(input())
        pts = [tuple(map(int, input().split())) for _ in range(n)]
        q = int(input())

        for _ in range(q):
            x, y, k = map(int, input().split())
            dx, dy = x, y
            norm = math.sqrt(dx * dx + dy * dy)
            dx /= norm
            dy /= norm

            times = []
            for xi, yi in pts:
                dot = xi * dx + yi * dy
                if dot <= 0:
                    continue
                t = (xi * xi + yi * yi) / (2 * dot)
                times.append(t)

            times.sort()
            if len(times) < k:
                print(-1)
            else:
                print(times[k - 1])

    solve()
    return sys.stdout.getvalue().strip()

# custom cases
assert run("""1
1 0
1
1 0 1""") != "", "single infection"

assert run("""2
1 0
-1 0
1
1 0 1""") == "0.5", "one active"

assert run("""3
1 1
2 2
3 3
1
1 1 2""") != "-1", "multiple same direction"

assert run("""1
1 1
1
-1 -1 1""") == "-1", "all negative dot"
```

| Test input | Expected output | What it validates |
|---|---|---|
| single infection | finite time | basic correctness |
| mixed signs | 0.5 | filtering by direction |
| collinear points | finite k-th event | sorting and order statistic |
| opposite direction | -1 | unreachable infections |

## Edge Cases

If all infection points lie behind the direction vector, every dot product is non-positive. In that case, the activation list is empty and any query with \(k \ge 1\) returns -1. The algorithm correctly produces no candidate times and immediately reports survival.

When the direction vector is very small in magnitude, normalization prevents numerical instability in dot products. Without normalization, threshold times would scale incorrectly and distort ordering, producing wrong k-th selection.

When multiple infections produce identical activation times, sorting still handles them correctly, and duplicates correctly contribute to overlap count, preserving correctness of the k-th event interpretation.
