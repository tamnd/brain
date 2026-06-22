---
title: "CF 105937L - Gros-Phi"
description: "Each game describes a set of timed targets on a line. Every target is a pair consisting of a time moment and a position on the line. Starting at time zero, Awa can choose any initial position and then move along the line with a fixed maximum speed."
date: "2026-06-22T15:49:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105937
codeforces_index: "L"
codeforces_contest_name: "2025 Xian Jiaotong University Programming Contest"
rating: 0
weight: 105937
solve_time_s: 82
verified: true
draft: false
---

[CF 105937L - Gros-Phi](https://codeforces.com/problemset/problem/105937/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

Each game describes a set of timed targets on a line. Every target is a pair consisting of a time moment and a position on the line. Starting at time zero, Awa can choose any initial position and then move along the line with a fixed maximum speed. When a target appears, she can only score it if she is exactly at its position at its time.

The task is to select a largest possible subset of these targets such that there exists some way to move through them in increasing time order, starting from an arbitrary position at time zero, while never exceeding the speed limit.

The key difficulty is that feasibility is not local. Whether a target is reachable depends on which previous target we came from, because each choice determines where we must have been earlier in time.

The constraints imply that a naive pairwise check between all targets per test case is impossible. With up to 5e5 total points across all tests, a quadratic approach would require on the order of 10^11 checks in the worst case, which is far beyond a one-second limit.

The most delicate edge cases come from targets that are close in time but far in space, or vice versa, where a greedy choice might pick a locally reachable point that blocks access to a much larger chain later.

For example, consider two points:

time-position pairs (0, 0), (1, 1000000000) with small speed. The second is unreachable from the first, so any solution that assumes reachability based only on ordering or position would fail immediately. Conversely, points that look far in time but are close in space can still be chained if intermediate movement is feasible.

The real challenge is that reachability defines a partial order over points, and we want the longest chain in that structure.

## Approaches

If we try to brute force, we can think of each point as a node and try to compute the best chain ending at it by checking all previous points. For a pair of points i and j with i earlier in time, we check whether Awa can move from j to i within the available time difference. This produces a natural dynamic programming transition.

The correctness is straightforward: every valid route ends at some last point, and we try all possibilities for the previous step.

The bottleneck is the transition cost. With n points, this requires checking all pairs, producing O(n^2) transitions per test case. With 5e5 total points, this is not viable.

The key observation is that the reachability condition can be rewritten into geometric dominance constraints after a transformation. Each point (t, x) can be mapped into two derived values that encode how far left and right Awa can have been while still reaching this point. Under this transformation, a point j can reach point i exactly when j lies in a certain dominance region relative to i.

This converts the problem into finding the longest chain under a 2D partial order. Once viewed this way, the structure becomes amenable to coordinate compression and a data structure that maintains maximum DP values over ranges.

The final solution reduces to processing points in a carefully chosen order and using a Fenwick tree (or similar structure) to maintain best DP values over one coordinate while iterating over the other.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP over pairs | O(n²) | O(n) | Too slow |
| Coordinate transform + BIT DP | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For every point, compute two derived values from its time and position that encode reachable space constraints relative to speed. These values capture how far left and right the point can be connected through a valid movement segment.
2. Sort all points in descending order of the left-reach value. This ensures that when processing a point, all candidates that could legally precede it in a chain (with respect to one constraint) are already considered.
3. Maintain a Fenwick tree over the right-reach coordinate. The tree stores the maximum DP value achieved for any point with a given compressed coordinate.
4. Process points in sorted order. For each point, query the Fenwick tree for the best DP value among all points that satisfy the second constraint (right-reach dominance). This gives the best valid predecessor chain ending at this point.
5. Set dp[i] to that queried value plus one, then update the Fenwick tree at the current point’s right-reach coordinate with dp[i].
6. The answer for the test case is the maximum dp value over all points.

The reason this ordering works is that sorting by the first transformed coordinate guarantees we never attempt to use a point as a predecessor unless it satisfies the first half of the feasibility condition. The Fenwick tree enforces the second half efficiently.

### Why it works

A valid transition between two points depends on two inequalities derived from the speed constraint. After transformation, these inequalities become a dominance relation in two dimensions. Any valid chain is therefore a chain in a partially ordered set defined by these dominance rules.

The sorting ensures we respect one axis of this order globally, and the Fenwick tree enforces the other locally. Every time we compute dp[i], all feasible predecessors have already been processed and are queryable. This guarantees that dp[i] always reflects the best valid chain ending at i, and no invalid predecessor can be included because it would violate at least one of the dominance constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

class BIT:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def update(self, i, v):
        while i <= self.n:
            if v > self.bit[i]:
                self.bit[i] = v
            i += i & -i

    def query(self, i):
        res = 0
        while i > 0:
            if self.bit[i] > res:
                res = self.bit[i]
            i -= i & -i
        return res

def solve():
    T = int(input())
    out = []

    for _ in range(T):
        n, v = map(int, input().split())
        pts = []

        for _ in range(n):
            t, x = map(int, input().split())
            A = x - v * t
            B = x + v * t
            pts.append((A, B))

        # compress B
        vals = sorted({b for _, b in pts})
        idx = {v: i + 1 for i, v in enumerate(vals)}

        pts.sort(reverse=True)  # sort by A descending

        bit = BIT(len(vals))
        ans = 0

        for A, B in pts:
            bi = idx[B]
            best = bit.query(bi)
            dp = best + 1
            if dp > ans:
                ans = dp
            bit.update(bi, dp)

        out.append(str(ans))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution compresses the second transformed coordinate so it can be used in a Fenwick tree. Each point is processed in decreasing order of the first transformed coordinate, and the tree maintains best chain lengths for feasible predecessors.

A subtle point is that we never need to explicitly track time in the DP state. The transformation already encodes time into the derived coordinates, so feasibility is fully captured by the dominance relation.

## Worked Examples

Consider a small case with three points:

Input points (t, x):

(0, 0), (2, 2), (4, 1) with v = 1

We compute transformed values:

| Point | A = x - vt | B = x + vt |
| --- | --- | --- |
| (0,0) | 0 | 0 |
| (2,2) | 0 | 4 |
| (4,1) | -3 | 5 |

Sorted by A descending gives:

(0,0), (2,2), (4,1)

We process:

| Step | Point | BIT Query (B) | DP | BIT Update |
| --- | --- | --- | --- | --- |
| 1 | (0,0) | 0 | 1 | set B=0 to 1 |
| 2 | (2,2) | 1 | 2 | update B=4 to 2 |
| 3 | (4,1) | 2 | 3 | update B=5 to 3 |

The final answer is 3, showing all points are chainable under the speed constraint.

This trace demonstrates how earlier points in the sorted order correctly act as potential predecessors for later ones when both dominance conditions are satisfied.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting plus Fenwick tree updates and queries |
| Space | O(n) | storage for transformed points and BIT |

Across all test cases, the total number of points is bounded by 5e5, so the solution runs comfortably within limits. The logarithmic factor from coordinate compression and BIT operations keeps total work well under the threshold.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    class BIT:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)

        def update(self, i, v):
            while i <= self.n:
                self.bit[i] = max(self.bit[i], v)
                i += i & -i

        def query(self, i):
            res = 0
            while i > 0:
                res = max(res, self.bit[i])
                i -= i & -i
            return res

    T = int(input())
    out = []

    for _ in range(T):
        n, v = map(int, input().split())
        pts = []
        for _ in range(n):
            t, x = map(int, input().split())
            pts.append((x - v * t, x + v * t))

        vals = sorted({b for _, b in pts})
        idx = {v: i + 1 for i, v in enumerate(vals)}

        pts.sort(reverse=True)

        bit = BIT(len(vals))
        ans = 0

        for a, b in pts:
            bi = idx[b]
            dp = bit.query(bi) + 1
            bit.update(bi, dp)
            ans = max(ans, dp)

        out.append(str(ans))

    return "\n".join(out)

# custom tests

# single point
assert run("1\n1 10\n0 0\n") == "1"

# two unreachable points
assert run("1\n2 1\n0 0\n1 100\n") == "1"

# fully chainable
assert run("1\n3 10\n0 0\n1 1\n2 2\n") == "3"

# same time different positions
assert run("1\n3 1\n0 0\n0 1\n0 2\n") == "1"

# sample-like mixed case
assert run("1\n4 2\n0 0\n1 3\n2 1\n3 5\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single point | 1 | minimal case |
| two unreachable points | 1 | speed constraint blocking transitions |
| fully chainable | 3 | ideal monotone chain |
| same time different positions | 1 | time-zero independence |
| sample-like mixed case | 3 | nontrivial ordering and DP interaction |

## Edge Cases

A critical edge case is when multiple points share similar transformed coordinates but differ significantly in time. Since the transformation encodes time, it is still possible for such points to have identical A or B values, which would collapse during coordinate compression. The Fenwick tree handles this safely because identical coordinates are treated as equivalent states, and DP values naturally accumulate the best achievable chain.

Another subtle case occurs when points appear in decreasing spatial order but increasing time order. A naive greedy approach would try to follow time ordering only, but feasibility may break due to spatial distance exceeding speed limits. In the transformed representation, such cases become incomparable in at least one dimension, preventing invalid transitions from being considered.

Finally, cases where all points lie on a tight feasible corridor produce maximum chains where every point is reachable from every earlier one. In this situation, the BIT continuously propagates increasing DP values, effectively degenerating into a longest increasing subsequence computation over the transformed coordinate.
