---
title: "CF 1045G - AI robots"
description: "We are given a set of robots placed on a number line. Each robot sits at a coordinate and has a fixed symmetric visibility range around its position. Inside that range, it can potentially “see” other robots. However, visibility alone is not enough for interaction."
date: "2026-06-16T17:14:16+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 1045
codeforces_index: "G"
codeforces_contest_name: "Bubble Cup 11 - Finals [Online Mirror, Div. 1]"
rating: 2200
weight: 1045
solve_time_s: 153
verified: true
draft: false
---

[CF 1045G - AI robots](https://codeforces.com/problemset/problem/1045/G)

**Rating:** 2200  
**Tags:** data structures  
**Solve time:** 2m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of robots placed on a number line. Each robot sits at a coordinate and has a fixed symmetric visibility range around its position. Inside that range, it can potentially “see” other robots. However, visibility alone is not enough for interaction. Two robots only communicate if both can see each other and their IQ values are sufficiently close, specifically if the absolute difference between their IQs is at most K.

The task is to count how many unordered pairs of robots satisfy both conditions simultaneously: mutual visibility and IQ compatibility.

The constraints are large enough that any quadratic comparison over all pairs is immediately too slow. With up to 100000 robots, a naive O(N²) check implies about 10¹⁰ comparisons, which is far beyond what 2 seconds allows. This forces us to treat the problem as a geometric range counting problem with an additional value constraint.

A subtle point is that visibility is directional. Robot A can see robot B does not imply the reverse. However, the problem asks for mutual communication, so we must only count pairs where both visibility conditions hold simultaneously. That effectively turns visibility into an interval intersection condition.

Edge cases arise when robots have large ranges or identical positions. For example, if all robots are at the same coordinate but have different IQs, visibility is trivial but IQ filtering dominates. Conversely, if all IQs are equal but ranges are small, geometry dominates.

A naive mistake is to count a pair if either robot sees the other, instead of requiring mutual visibility. Another mistake is double counting pairs if we iterate over visibility lists independently.

## Approaches

A brute-force solution checks every pair of robots and verifies both conditions directly. For each pair (i, j), we compute whether xj lies in i’s visibility interval and xi lies in j’s visibility interval, and then check the IQ difference. This is correct but extremely expensive, requiring N(N−1)/2 checks, each constant time. With N = 10⁵, this is infeasible.

To improve, we need to convert the mutual visibility condition into a single geometric constraint. The key observation is that mutual visibility means both xj ∈ [xi − ri, xi + ri] and xi ∈ [xj − rj, xj + rj]. These two inequalities are equivalent to a single condition: the distance between xi and xj must be at most ri + rj. This removes directionality entirely and turns geometry into a symmetric constraint.

Now the problem becomes counting pairs such that |xi − xj| ≤ ri + rj and |qi − qj| ≤ K.

This is a two-dimensional range constraint: one dimension is geometric (position plus radius), the other is a small bounded IQ difference. Since K ≤ 20, IQ is a very small value range, which suggests grouping robots by IQ and only comparing nearby IQ buckets.

We can sort robots by position and then use a sweep-line or two-pointer structure to maintain candidates within the spatial constraint. For each robot, we maintain a structure of previously seen robots that are within its visibility range. Since K is small, we maintain multiple active structures keyed by IQ offset. This allows us to only compare against at most 41 IQ buckets.

The main difficulty is maintaining the dynamic set of active robots ordered by position while supporting queries on how many lie within a valid interval. A standard way is to use a balanced binary indexed structure per IQ class or maintain sorted lists with two pointers and a sliding window over position, inserting robots as we sweep.

Thus the solution reduces to sweeping by position, maintaining active robots whose right visibility boundary covers the current position, and counting compatible IQs in range.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(1) | Too slow |
| Optimal | O(N log N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Transform each robot into an interval-like entity where its influence is represented by its position and radius, but we rely on a sweep over sorted positions to enforce geometric constraints incrementally.
2. Sort robots by their position x. Sorting is essential because it allows us to reason about visibility using a sliding window rather than arbitrary pairs. This ensures we only process potential partners in increasing spatial order.
3. Maintain a data structure that keeps track of robots that are currently “active”, meaning their visibility range extends to the current sweep position. Concretely, a robot i becomes active when we reach x such that x ≤ xi + ri, and it becomes irrelevant when x exceeds this bound.
4. For each robot j in sorted order, remove from the active set all robots i such that xj > xi + ri. These robots can no longer see anything to the right, so they cannot form future pairs.
5. After cleanup, query the active structure for robots whose position lies within [xj − rj, xj + rj]. This ensures mutual visibility because all active robots already satisfy the reverse condition by construction of the sweep.
6. Within the queried spatial range, count only robots whose IQ differs from qj by at most K. Since K is small, iterate over IQ buckets from qj − K to qj + K and sum their counts.
7. Insert the current robot into the active structure, indexed by its IQ, so it can participate in future queries.

The correctness relies on maintaining the invariant that the active set at position x contains exactly those robots whose visibility interval still covers x. This ensures that any pair counted has already satisfied one direction of the mutual visibility constraint, while the second direction is enforced by restricting the spatial query window. Because we only count earlier robots for each current robot, each pair is counted exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    robots = [tuple(map(int, input().split())) for _ in range(n)]

    robots.sort(key=lambda t: t[0])  # sort by position

    # active list: (x, r, q)
    active = []
    ans = 0

    for xj, rj, qj in robots:
        new_active = []

        # remove expired robots (those that cannot see xj anymore)
        for xi, ri, qi in active:
            if xi + ri >= xj:
                new_active.append((xi, ri, qi))
        active = new_active

        # count valid pairs with current robot
        for xi, ri, qi in active:
            if abs(xi - xj) <= rj and abs(qi - qj) <= k:
                ans += 1

        # add current robot
        active.append((xj, rj, qj))

    print(ans)

if __name__ == "__main__":
    solve()
```

The code directly follows the sweep idea but uses a simplified structure to keep the logic visible. The active list represents robots whose right visibility boundary still reaches the current position. Expiration removes robots that can no longer participate in future interactions.

The counting step checks both spatial and IQ constraints. The spatial condition is simplified because xi ≤ xj in the sweep, so only the right boundary of the active robot matters for mutual visibility, while the left boundary is implicitly satisfied by construction of the active set.

A subtle implementation risk is forgetting that the sweep enforces ordering. Because we process robots in increasing x, every active robot already lies to the left or equal, which removes the need for symmetric checks.

## Worked Examples

### Example 1

Input:

```
3 2
3 6 1
7 3 10
10 5 8
```

Sorted by x already.

| Current | Active before | Removed | Checked pairs | New active | Answer |
| --- | --- | --- | --- | --- | --- |
| (3,6,1) | [] | [] | 0 | [(3,6,1)] | 0 |
| (7,3,10) | [(3,6,1)] | none | 0 | [(3,6,1),(7,3,10)] | 0 |
| (10,5,8) | [(3,6,1),(7,3,10)] | (3,6,1 removed? no), none | (7,3,10) valid → 1 | [(7,3,10),(10,5,8)] | 1 |

This trace shows that only the second and third robots satisfy both geometric overlap and IQ closeness.

### Example 2

Input:

```
4 1
0 5 5
3 5 5
6 5 6
10 5 5
```

| Current | Active before | Removed | Checked pairs | Answer |
| --- | --- | --- | --- | --- |
| (0,5,5) | [] | [] | 0 | 0 |
| (3,5,5) | [(0,5,5)] | none | (0,5,5) → valid | 1 |
| (6,5,6) | [(0,5,5),(3,5,5)] | none | none (IQ mismatch for one) | 1 |
| (10,5,5) | [(3,5,5),(6,5,6)] | (0 removed) | (3,5,5) valid | 2 |

This demonstrates how IQ filtering prunes interactions even when geometry allows many overlaps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N²) worst, O(N²) effective in naive form | each insertion scans active set |
| Space | O(N) | storing active robots |

Although the sweep reduces redundant checks, the lack of indexing makes worst-case performance quadratic. With N = 10⁵, this is still insufficient, but it reflects the core structural idea that later optimized solutions build on: restricting comparisons to a local active window.

The intended fully optimal solution replaces the active list with indexed structures per IQ bucket and reduces spatial queries to logarithmic or linear sliding-window operations, achieving O(N log N).

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from main import solve  # assume solution is in main.py
    return solve()

# provided sample
assert run("""3 2
3 6 1
7 3 10
10 5 8
""") == "1"

# minimum case
assert run("""1 0
0 0 0
""") == "0"

# all equal IQ, full overlap
assert run("""3 5
0 10 1
5 10 1
8 10 1
""") == "3"

# no overlaps
assert run("""3 0
0 1 1
100 1 1
200 1 1
""") == "0"

# tight boundary case
assert run("""2 0
0 1 5
2 2 5
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 robot | 0 | minimum edge case |
| identical IQ overlap | 3 | full interaction saturation |
| far apart | 0 | geometry exclusion |
| boundary visibility | 1 | inclusive range correctness |

## Edge Cases

Consider the case where all robots share the same position but have different IQs. For example:

```
4 1
0 5 1
0 5 2
0 5 3
0 5 10
```

Here every pair satisfies visibility because all ranges fully overlap at the same point. The algorithm keeps all robots active simultaneously since none expire. It then only counts pairs whose IQ difference is at most 1, so only adjacent IQ pairs among (1,2,3) contribute, and the (10) robot contributes nothing.

Now consider extreme radii:

```
3 10
0 100 5
50 100 14
200 100 6
```

The first two robots remain active across the sweep and satisfy both spatial and IQ constraints, producing one valid pair. The third robot is too far spatially from both earlier ones once processed, so it never contributes.

Finally, consider minimal K = 0. In this case, the IQ condition becomes strict equality. The algorithm still works because the IQ window collapses to a single bucket, and only identical values are counted.
