---
title: "CF 104279D - \u5c0f\u7f8e\u7231\u753b\u9c7c"
description: "We are given several independent test cases. In each test case, we are working on a grid in the first quadrant. Every segment we receive lies on a single 45-degree diagonal line, because each segment’s endpoints satisfy the same value of $x + y$."
date: "2026-07-01T21:11:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104279
codeforces_index: "D"
codeforces_contest_name: "21st UESTC Programming Contest - Preliminary"
rating: 0
weight: 104279
solve_time_s: 65
verified: true
draft: false
---

[CF 104279D - \u5c0f\u7f8e\u7231\u753b\u9c7c](https://codeforces.com/problemset/problem/104279/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. In each test case, we are working on a grid in the first quadrant. Every segment we receive lies on a single 45-degree diagonal line, because each segment’s endpoints satisfy the same value of $x + y$. This means every segment is constrained to move from a point $(x_1, y_1)$ to another point $(x_2, y_2)$ while staying on the same anti-diagonal line, moving strictly to the right and down.

Geometrically, each such segment traces a portion of one fixed diagonal line in the grid. Different segments may lie on different diagonals depending on their $x + y$ value.

Two things are required for each test case. First, we must determine whether any unit grid cell has its diagonal traversed more than once. Since each unit cell contributes exactly one diagonal segment (the same slope direction), this condition is equivalent to ensuring that along every fixed diagonal line, the drawn segments do not overlap in a way that causes any point on the line to be covered multiple times.

Second, we must compute the total length of all drawn segments, but the problem asks for this total length divided by 2. Each segment’s contribution depends only on its horizontal displacement, since vertical displacement is determined by the diagonal constraint.

The constraints allow up to $10^5$ segments per test case and up to 10 test cases. This immediately rules out any quadratic pairwise overlap checking. Even an $O(n \log^2 n)$ approach per test case would be borderline if implemented with heavy constants, so we should aim for $O(n \log n)$ or better per test case.

A subtle failure case arises if we ignore grouping by diagonal. For example, consider segments:

$(0,1)\to(1,0)$ and $(1,2)\to(2,1)$. These are on different diagonals, so they never interact, and overlap checking across them would be meaningless. A naive approach that sorts all segments globally by $x_1$ would incorrectly compare them and might report false overlaps.

Another failure case appears if we check only endpoints. Two segments on the same diagonal might not share endpoints but still partially overlap inside the segment, which would violate the condition.

## Approaches

A brute-force approach would compare every pair of segments that lie on the same diagonal line. For each pair, we would check whether their intervals on that line intersect with positive length. This requires $O(n^2)$ comparisons in the worst case, which is far too slow when $n = 10^5$. Even if restricted per diagonal, a single diagonal could still contain almost all segments.

The key observation is that each segment is simply an interval on a one-dimensional line identified by $c = x + y$. Once we group segments by this value, the problem becomes a classic interval overlap detection problem per group. We only need to sort intervals within each group and verify that they do not intersect beyond endpoints.

The second task, computing half of the total drawn length, simplifies because every segment contributes exactly its horizontal span $(x_2 - x_1)$ to the required answer. Summing these values across all segments yields the final result directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Pairwise Checking | $O(n^2)$ | $O(n)$ | Too slow |
| Sort by diagonal and check intervals | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We process each test case independently.

First, we group segments by the value $c = x + y$. This is the identity of the diagonal line on which the segment lies. Every segment belongs to exactly one such group.

Second, within each group, we treat each segment as a one-dimensional interval $[x_1, x_2]$, since $y$ is determined uniquely by $x + y = c$.

We then sort these intervals by their left endpoint $x_1$. Sorting ensures that if any overlap exists, it must appear between consecutive intervals in this order.

Next, we scan through the sorted intervals and maintain the rightmost point reached so far. If we encounter a new interval whose start is strictly less than the current right boundary, we immediately detect overlap and mark the answer as invalid. If the start equals the boundary, this is allowed since endpoints touching do not imply repeated coverage.

At the same time, we accumulate the contribution of each segment to the final answer by adding $x_2 - x_1$.

Finally, we output whether the overlap condition was violated and the computed sum.

The correctness comes from reducing each diagonal to a one-dimensional line. On such a line, any repeated coverage must appear as an interval intersection in sorted order. Since sorting preserves adjacency of potentially overlapping intervals, a single linear scan is sufficient to detect all violations.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import defaultdict

def solve():
    T = int(input())
    for _ in range(T):
        n = int(input())
        groups = defaultdict(list)
        total = 0
        ok = True

        for _ in range(n):
            x1, y1, x2, y2 = map(int, input().split())
            c = x1 + y1
            groups[c].append((x1, x2))
            total += (x2 - x1)

        for c, segs in groups.items():
            segs.sort()
            r = -1
            for l, rr in segs:
                if l < r:
                    ok = False
                    break
                r = max(r, rr)
            if not ok:
                break

        print("YES" if ok else "NO")
        print(total)

if __name__ == "__main__":
    solve()
```

The solution first builds a dictionary keyed by diagonal identifier $x+y$. Each stored entry is reduced to an interval over $x$, since the diagonal constraint makes $y$ redundant. The overlap check is performed only within each bucket after sorting.

The running sum is accumulated immediately during input parsing, since each segment independently contributes $x_2 - x_1$. This avoids needing to revisit segments later.

A subtle point is that we allow adjacent intervals where $l = r$. This corresponds to segments touching at endpoints without double coverage of any interior point, which is valid under the problem condition.

## Worked Examples

Consider a case with two segments on the same diagonal:

Input:

$$(0,1)\to(2,-1)\ \text{is invalid geometrically so instead use valid: } (0,1)\to(2,-1) \text{ignored}$$

A correct example:

Segments:

$(0,1)\to(1,0)$, $(1,1)\to(2,0)$ are on different diagonals, so they never interact.

| Segment | c = x+y | Interval |
| --- | --- | --- |
| (0,1)-(1,0) | 1 | [0,1] |
| (1,1)-(2,0) | 2 | [1,2] |

Each group is independent, so no overlap occurs and the answer is YES.

Now consider overlapping segments:

Input:

$(0,1)\to(2,-1)$ invalid again, so correct version:

$(0,1)\to(2,-1)$ replaced by valid diagonal examples:

$(0,2)\to(2,0)$ and $(1,1)\to(3,-1)$ invalid again; instead:

Use consistent c=2:

$(0,2)\to(2,0)$

$(1,1)\to(3,-1)$ still invalid due to negative y, so adjust domain:

Better example:

$(0,2)\to(2,0)$

$(1,1)\to(2,0)$

Second is actually $(1,1)\to(2,0)$, same c=3.

Now both on different diagonals, so still no overlap.

To properly illustrate overlap on same diagonal:

All points must satisfy x+y=c and non-negative y:

Take c=4:

$(0,4)\to(2,2)$

$(1,3)\to(3,1)$

| Segment | Interval |
| --- | --- |
| (0,4)-(2,2) | [0,2] |
| (1,3)-(3,1) | [1,3] |

Sorting gives $[0,2]$, $[1,3]$. The second starts before the first ends, so overlap is detected and the answer becomes NO.

This confirms that the scan correctly identifies interior intersection, not just endpoint conflicts.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Each segment is inserted into a group and sorted per diagonal, total sorting across all groups dominates |
| Space | $O(n)$ | All segments are stored once, grouped by diagonal |

The constraints allow up to $10^5$ segments per test case, so an $O(n \log n)$ solution fits comfortably within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import defaultdict

    def solve():
        T = int(input())
        out = []
        for _ in range(T):
            n = int(input())
            g = defaultdict(list)
            total = 0
            ok = True
            for _ in range(n):
                x1,y1,x2,y2 = map(int,input().split())
                c = x1+y1
                g[c].append((x1,x2))
                total += x2-x1

            for segs in g.values():
                segs.sort()
                r = -1
                for l,rr in segs:
                    if l < r:
                        ok = False
                        break
                    r = max(r, rr)
                if not ok:
                    break

            out.append(("YES" if ok else "NO") + "\n" + str(total))
        return "\n".join(out)

    return solve()

# simple non-overlap
assert run("1\n2\n0 1 1 0\n1 2 2 1\n") == "YES\n2", "no overlap"

# overlap on same diagonal
assert run("1\n2\n0 4 2 2\n1 3 3 1\n") == "NO\n4", "overlap case"

# single segment
assert run("1\n1\n0 0 5 5\n") == "YES\n5", "single segment"

# disjoint multiple diagonals
assert run("1\n3\n0 1 1 0\n1 2 2 1\n2 3 3 2\n") == "YES\n3", "separate diagonals"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single segment | YES | base case correctness |
| overlapping intervals | NO | overlap detection on same diagonal |
| multiple diagonals | YES | independence of groups |

## Edge Cases

A tricky case is when segments only touch at endpoints. For example, $[0,2]$ and $[2,5]$ on the same diagonal do not violate the condition because no unit point is covered twice. The algorithm handles this because it allows equality $l = r$ without triggering failure, and only flags strict overlap when $l < r$.

Another case is when all segments lie on different diagonals. Even if their projections overlap in global x-order, they are independent. The grouping by $x+y$ ensures they never interfere, and the scan never compares unrelated intervals.

A final subtle case is large inputs where all segments share the same diagonal. In that situation, the algorithm degenerates into a single sorted interval sweep, which still runs in $O(n \log n)$ due to sorting and remains within limits.
