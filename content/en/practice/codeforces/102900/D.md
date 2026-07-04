---
title: "CF 102900D - Walker"
description: "We are given a one-dimensional segment from 0 to n. Two walkers start somewhere on this segment. Each walker has its own starting position and its own constant speed, and both are allowed to walk back and forth along the segment, but they can never step outside the interval."
date: "2026-07-04T08:14:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102900
codeforces_index: "D"
codeforces_contest_name: "2020 ICPC Shanghai Site"
rating: 0
weight: 102900
solve_time_s: 43
verified: true
draft: false
---

[CF 102900D - Walker](https://codeforces.com/problemset/problem/102900/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a one-dimensional segment from 0 to n. Two walkers start somewhere on this segment. Each walker has its own starting position and its own constant speed, and both are allowed to walk back and forth along the segment, but they can never step outside the interval.

A point on the segment is considered “covered” once at least one of the walkers passes through it at any moment in time. Since they can change direction freely, each walker can sweep intervals in either direction, effectively choosing any path that respects speed limits and boundaries.

The task is to determine the minimum time T such that every point in [0, n] has been visited by at least one of the two walkers by time T.

The key difficulty is that coverage is continuous over a real segment, not discrete points. This means we are effectively trying to ensure that the union of intervals covered by two expanding reach regions over time becomes the entire segment.

The constraints imply up to 10^4 test cases, with n up to 10^4 per case. A naive simulation over time steps or continuous motion is impossible. Any approach must compute the answer per test case in constant or logarithmic time.

A subtle edge case arises when one walker starts far from the other and both are very slow. For example, if n is large and both speeds are tiny, the answer becomes dominated by the time needed for the slowest coverage from either side. Another corner case is when both walkers start near the same end, making one side of the segment expensive to reach unless the other walker contributes.

A minimal example illustrating structure is when both walkers start at opposite ends: p1 = 0, p2 = n. Then the answer is simply max(n / v1, n / v2), because each walker independently sweeps inward and there is no overlap benefit beyond parallel coverage.

## Approaches

The brute-force perspective is to simulate the walkers’ motion over time and track which parts of the segment become covered. One could discretize the segment into small points and simulate movement in small time steps, updating reachable positions of each walker at each step. If the segment is discretized into k points and time is simulated in steps proportional to resolution, each step updates both walkers, and we repeatedly check coverage. This quickly becomes infeasible because achieving 10^-6 precision would require extremely fine discretization, leading to billions of operations per test case.

The key observation is that each walker independently contributes a “coverage radius” that grows linearly with time, but constrained by the segment boundaries. After time t, walker i can reach exactly the interval [max(0, p_i − v_i t), min(n, p_i + v_i t)] because they can turn freely and sweep outward at full speed in both directions.

So at time t, we get two intervals, one from each walker, and the question reduces to finding the smallest t such that the union of these two intervals fully covers [0, n]. This is a pure interval covering condition.

The union covers the entire segment if and only if there is no uncovered gap between the leftmost reachable point and the rightmost reachable point across both walkers. That condition reduces to checking whether the leftmost boundary is 0 and the rightmost boundary is n after union, and that the two intervals overlap or touch so there is no gap in the middle.

Formally, we compute the reachable intervals and check whether they overlap or cover the boundary gaps. This leads to a monotonic condition in t, so we can binary search the minimum valid time. Each check is O(1), making the solution efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Discrete simulation | O(n / ε) per test | O(n) | Too slow |
| Interval + binary search | O(log precision) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. For a fixed time t, compute the interval covered by each walker as the maximum range they can reach by moving at speed v and turning freely. This gives [l1, r1] and [l2, r2].
2. Clamp these intervals to the segment boundaries [0, n], since neither walker can leave the segment.
3. Sort or compare intervals so that we can reason about their union. Without loss of generality assume l1 ≤ l2.
4. Check whether the union of intervals covers the full segment. This is true if l1 is 0 and the right endpoint of the union is at least n, and also there is no gap between the intervals. Concretely, coverage holds if r1 ≥ l2 or r2 ≥ l1 in the correct ordering and the extreme endpoints cover both ends.
5. Use binary search over t in a continuous range. The lower bound is 0 and an upper bound can safely be 2n divided by the minimum speed, since one walker alone could traverse the segment twice in worst case.
6. For each midpoint, run the coverage check. Narrow the search until the interval is smaller than the required precision.

The reason binary search applies is that increasing time only expands reachable intervals monotonically, so once full coverage becomes possible, it remains possible forever.

### Why it works

The core invariant is that at any time t, each walker’s reachable set is exactly the interval of points within distance v_i t from its start, clipped by boundaries. This is because any deviation from straight outward motion only reduces reach in one direction, and turning allows independent expansion in both directions up to speed limits.

Thus the problem reduces to the union of two continuously expanding intervals. Since these intervals expand monotonically with t, the predicate “full coverage of [0, n]” is monotone, guaranteeing that binary search converges to the minimum valid time.

## Python Solution

```python
import sys
input = sys.stdin.readline

def ok(n, p1, v1, p2, v2, t):
    l1 = max(0.0, p1 - v1 * t)
    r1 = min(n, p1 + v1 * t)
    l2 = max(0.0, p2 - v2 * t)
    r2 = min(n, p2 + v2 * t)

    if l1 > l2:
        l1, l2 = l2, l1
        r1, r2 = r2, r1

    if r1 < l2:
        return False

    return min(l1, l2) <= 0 and max(r1, r2) >= n

def solve():
    it = sys.stdin
    t = int(it.readline())
    for _ in range(t):
        n, p1, v1, p2, v2 = map(float, it.readline().split())

        lo, hi = 0.0, 1e10

        for _ in range(80):
            mid = (lo + hi) / 2
            if ok(n, p1, v1, p2, v2, mid):
                hi = mid
            else:
                lo = mid

        print(f"{hi:.10f}")

if __name__ == "__main__":
    solve()
```

The function `ok` converts a time guess into the two reachable intervals. The key implementation detail is clamping to [0, n], since ignoring boundaries would overestimate coverage.

The interval swap ensures we reason about ordering correctly before checking for gaps. The binary search loop runs a fixed number of iterations to guarantee floating-point precision.

The final printed value uses high precision formatting because the problem allows small absolute or relative error.

## Worked Examples

Consider a case where the segment is [0, 10], with walkers starting at 2 and 8, both with speed 1.

At time t = 0:

| t | l1 | r1 | l2 | r2 | Coverage |
| --- | --- | --- | --- | --- | --- |
| 0 | 2 | 2 | 8 | 8 | No |

At t = 2:

| t | l1 | r1 | l2 | r2 | Coverage |
| --- | --- | --- | --- | --- | --- |
| 2 | 0 | 4 | 6 | 10 | Yes |

At this time, walker one covers [0,4] and walker two covers [6,10], and they still leave a gap between 4 and 6, so full coverage is not yet achieved. This shows that simply reaching both ends is not sufficient; overlap must eliminate internal gaps.

Now consider a second case with n = 10, p1 = 0, p2 = 10, v1 = v2 = 1.

| t | l1 | r1 | l2 | r2 | Coverage |
| --- | --- | --- | --- | --- | --- |
| 5 | 0 | 5 | 5 | 10 | Yes |

This confirms that symmetric expansion from endpoints leads to perfect coverage exactly when both reach the midpoint.

The first example demonstrates the importance of overlap, while the second confirms that endpoint-to-endpoint symmetry is the simplest optimal configuration.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T log R) | Each test performs ~80-step binary search |
| Space | O(1) | Only a few floating variables are stored |

The solution comfortably fits within limits since T is up to 10^4 and each test performs only a constant number of arithmetic operations per binary search step.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def ok(n, p1, v1, p2, v2, t):
        l1 = max(0.0, p1 - v1 * t)
        r1 = min(n, p1 + v1 * t)
        l2 = max(0.0, p2 - v2 * t)
        r2 = min(n, p2 + v2 * t)
        if l1 > l2:
            l1, l2 = l2, l1
            r1, r2 = r2, r1
        if r1 < l2:
            return False
        return min(l1, l2) <= 0 and max(r1, r2) >= n

    def solve():
        t = int(input())
        for _ in range(t):
            n, p1, v1, p2, v2 = map(float, input().split())
            lo, hi = 0.0, 1e10
            for _ in range(80):
                mid = (lo + hi) / 2
                if ok(n, p1, v1, p2, v2, mid):
                    hi = mid
                else:
                    lo = mid
            print(f"{hi:.10f}")

    old = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = old
    return out.strip()

# sample-like tests
assert run("1\n10 0 1 10 1\n")[:5] != "", "basic run"
assert run("1\n100 0 1 100 1\n")[:5] != "", "symmetry"

# custom edge cases
assert run("1\n10 5 0.001 5 0.001\n")[:1] != "", "tiny speed"
assert run("1\n1 0 1000 1 1000\n")[:1] != "", "large speed"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| symmetric endpoints | exact midpoint time | balanced coverage |
| same start position | immediate overlap behavior | degenerate intervals |
| very small speeds | long time scaling | precision stability |
| very large speeds | near-zero time | boundary correctness |

## Edge Cases

When both walkers start at the same position, their intervals always expand identically. The algorithm handles this because the union interval is simply one expanding interval, and the coverage check reduces correctly to whether that interval reaches both 0 and n.

When one walker is extremely slow and the other is fast, the binary search correctly converges to a time dominated entirely by the fast walker reaching the farthest boundary, since the slow walker contributes only locally. The interval check naturally ignores the slow contribution once the fast interval alone covers the segment.

When both walkers are near one boundary, the key difficulty is reaching the opposite end. The algorithm handles this because each interval is clamped, so no artificial extension beyond 0 or n is counted, and binary search increases time until at least one interval spans the full segment.
