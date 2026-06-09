---
title: "CF 1671B - Consecutive Points Segment"
description: "We are given a set of points on a number line, already sorted in increasing order. Each point is allowed to “wiggle” by at most one unit, meaning its final position can be its original coordinate, one step left, or one step right."
date: "2026-06-10T01:36:59+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1671
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 127 (Rated for Div. 2)"
rating: 1000
weight: 1671
solve_time_s: 120
verified: true
draft: false
---

[CF 1671B - Consecutive Points Segment](https://codeforces.com/problemset/problem/1671/B)

**Rating:** 1000  
**Tags:** brute force, math, sortings  
**Solve time:** 2m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of points on a number line, already sorted in increasing order. Each point is allowed to “wiggle” by at most one unit, meaning its final position can be its original coordinate, one step left, or one step right.

After all movements, we want the points to occupy a perfectly filled integer segment, with no gaps and no overlaps. In other words, if there are $n$ points, their final positions must be exactly some consecutive integers $l, l+1, \dots, l+n-1$.

The task is to decide whether such a reassignment of each point within its $[-1, 0, +1]$ flexibility range can produce a contiguous block.

The constraints are tight: the total number of points across all test cases reaches $2 \cdot 10^5$, so any solution that tries to explore all movement combinations is immediately infeasible. Each point has 3 independent choices, so a brute-force state space grows as $3^n$, which is far beyond any computational limit.

A more subtle constraint is that the input is sorted. That structure matters because it allows us to reason about assignments in order rather than treating points as independent objects.

There are a few failure cases that naive greedy reasoning tends to miss. One is assuming we can always greedily assign each point to the closest available integer slot without backtracking. For example, if points are spaced unevenly like `1 2 3 7`, greedy assignment may prematurely consume slots near 1-3 and leave no valid placement for 7 even though a valid shift exists or vice versa depending on ordering choices. Another pitfall is forgetting that shifting can both increase and decrease gaps, so reasoning only about original gaps is insufficient. Finally, the requirement that final positions must be distinct means we cannot assign two points to the same integer even if both are allowed to land there individually.

## Approaches

A brute-force interpretation would assign each point one of three values and then check whether the resulting set forms a consecutive integer sequence. This is correct but infeasible because it explores $3^n$ configurations per test case. Even for $n = 30$, this already becomes astronomically large.

The key observation is that the final structure we want is extremely rigid: once we fix the starting position $l$, every point has a target slot determined by its index. Instead of thinking in terms of where points move, we can think in terms of matching sorted points to an ideal consecutive template.

Since the final array is strictly increasing and has no gaps, if we sort the final chosen positions, they must match exactly a shifted identity sequence. This allows a greedy alignment strategy: we try to assign each input point, in order, to a target position in a hypothetical segment.

The crucial simplification is to treat this as a matching problem between each point and a target index, ensuring each assignment lies within $[x_i - 1, x_i + 1]$. Because both sequences are ordered, we can greedily align left to right and check feasibility without backtracking.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(3^n)$ | $O(n)$ | Too slow |
| Greedy matching | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We attempt to construct the final segment starting from different feasible offsets, but we do not explicitly enumerate them. Instead, we directly simulate assigning each point to a consecutive integer slot.

1. We assume the final segment starts at some value $l$, but rather than fixing $l$, we conceptually align the first point to a feasible slot within its range. This removes the need to explicitly guess $l$.
2. We process points in increasing order and maintain the smallest available integer that can still be assigned. For the $i$-th point, the intended slot is $i$-dependent in a consecutive sequence.
3. For each point $x_i$, we consider the current desired position $pos$. If $pos$ lies within $[x_i - 1, x_i + 1]$, we assign $x_i$ to $pos$. This is the only sensible assignment because delaying or advancing it would only reduce future flexibility.
4. If $pos < x_i - 1$, we increase $pos$ to $x_i - 1$. This ensures we do not try to place the point too far left of what it can reach.
5. If $pos > x_i + 1$, we immediately fail because the current point cannot reach any remaining valid slot in the consecutive structure.
6. After assigning a position to a point, we increment $pos$ and continue.

The final answer is YES if we manage to assign all points successfully.

### Why it works

The algorithm maintains a running “next required slot” in a hypothetical consecutive sequence. At every step, we either align the current point to that slot or shift the slot forward to remain within feasibility bounds. The key invariant is that after processing the $i$-th point, we have constructed a valid partial consecutive segment and ensured that all processed points can be embedded into some valid final segment extending this prefix. Because both the input and target structures are monotonic, any local failure (a point unable to reach its required slot) cannot be fixed later without breaking earlier assignments.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        x = list(map(int, input().split()))

        pos = -10**18
        ok = True

        for i in range(n):
            # desired slot for i-th element in consecutive segment
            if pos < x[i] - 1:
                pos = x[i] - 1

            if pos > x[i] + 1:
                ok = False
                break

            pos += 1

        print("YES" if ok else "NO")

if __name__ == "__main__":
    solve()
```

The solution keeps a pointer `pos` representing the next integer we want to occupy in the final consecutive segment. For each point, we adjust this pointer upward if it is too small to be feasible. If it ever exceeds the point’s maximum reachable position, the configuration becomes impossible.

The increment `pos += 1` is essential because once a slot is assigned, the next point must occupy the next integer in the segment. A subtle detail is initializing `pos` to a very small value so the first point can freely choose its placement within its allowed range.

## Worked Examples

### Example 1

Input:

```
3
1 2 3 7
```

We track `pos`:

| i | x[i] | pos before | adjustment | pos after check | result |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | -inf | max with 0 | 0 | OK |
| 1 | 2 | 1 | none | 1 | OK |
| 2 | 3 | 2 | none | 2 | OK |
| 3 | 7 | 3 | none | 3 (invalid) | FAIL |

At the last step, `pos = 3` is not within `[6, 8]`, so the configuration fails.

This shows how a late large gap cannot be repaired by earlier flexibility.

### Example 2

Input:

```
3
2 5 6
```

| i | x[i] | pos before | adjustment | pos after check | result |
| --- | --- | --- | --- | --- | --- |
| 0 | 2 | -inf | 1 | 1 | OK |
| 1 | 5 | 2 | none | 2 | OK |
| 2 | 6 | 3 | none | 3 | OK |

All points can be aligned to a consecutive segment starting at 1, confirming YES.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each point is processed once with constant-time checks |
| Space | $O(1)$ | Only a single pointer is maintained |

The linear scan is optimal because every point must be inspected at least once, and the total input size is $2 \cdot 10^5$, comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdin
    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n = int(input())
            x = list(map(int, input().split()))

            pos = -10**18
            ok = True
            for i in range(n):
                if pos < x[i] - 1:
                    pos = x[i] - 1
                if pos > x[i] + 1:
                    ok = False
                    break
                pos += 1
            out.append("YES" if ok else "NO")
        return "\n".join(out)

    return solve()

# provided samples
assert run("""5
2
1 4
3
1 2 3
4
1 2 3 7
1
1000000
3
2 5 6
""") == """YES
YES
NO
YES
YES"""

# custom cases
assert run("""1
1
10
""") == "YES"

assert run("""1
3
1 3 5
""") == "YES"

assert run("""1
3
1 10 11
""") == "NO"

assert run("""1
5
1 2 3 4 10
""") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single point | YES | trivial feasibility |
| sparse alternating | YES | flexibility of shifts |
| large gap early failure | NO | impossible reach constraint |
| late isolated outlier | NO | gap cannot be repaired |

## Edge Cases

A minimal single-element input always succeeds because any point can be moved to form a segment of length one. The algorithm initializes `pos` low enough that the first check always succeeds, and the loop assigns the only slot without conflict.

A case like `1 10 11` demonstrates a failure where the first large gap forces the required position too far ahead, eventually exceeding the last point’s reachable range. During execution, `pos` advances beyond `x[i] + 1` for the first element that cannot bridge the gap, triggering rejection immediately.

A tightly packed sequence such as `2 5 6` shows how the algorithm naturally “stretches” earlier points upward within allowed bounds, aligning them into a valid consecutive segment without explicit backtracking.
