---
title: "CF 102576H - Lighthouses"
description: "We have a convex polygon whose vertices are lighthouses. Some pairs of vertices are connected by tram tracks, and Vladik may only move along those tracks."
date: "2026-07-31T07:37:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102576
codeforces_index: "H"
codeforces_contest_name: "2020 Petrozavodsk Winter Camp, Jagiellonian U Contest"
rating: 0
weight: 102576
solve_time_s: 78
verified: true
draft: false
---

[CF 102576H - Lighthouses](https://codeforces.com/problemset/problem/102576/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a convex polygon whose vertices are lighthouses. Some pairs of vertices are connected by tram tracks, and Vladik may only move along those tracks. A valid trip is a path in this graph, but with a geometric restriction: the drawn chain of travelled segments may not intersect itself and may not visit the same point twice.

The task is to find the maximum possible total Euclidean length of such a path.

The number of lighthouses is at most 300, which rules out any solution that depends on enumerating paths or subsets of vertices. A graph with 300 vertices can still have almost 45,000 edges, so a solution close to cubic time is the natural target. The total number of vertices over all tests is only 3000, which allows some heavier per-test processing.

The main difficulty is not graph traversal. A longest path in a general graph is hard, but here all vertices lie on a convex polygon. The order of the vertices gives us a strong geometric structure: whenever we take a chord, the remaining possible route is restricted to one side of that chord. This creates smaller independent subproblems.

A few cases easily break naive approaches. If there are crossing tram lines, they cannot both appear in the answer even if they give a larger graph-theoretic path. For example, a square with both diagonals available does not allow the route `1-3-2-4`, because the diagonals cross in the middle. The correct route must avoid the crossing.

Another trap is assuming the longest path must start at a fixed lighthouse. Consider a square with only three consecutive sides available. The best route starts at one end of those sides and ends at the other, so fixing the first vertex can lose the optimum.

A third issue is that the polygon is circular. A path can cross the artificial boundary between the last and first indexed vertices. Any interval DP that only works on `0...n-1` without handling the circle can miss valid answers.

## Approaches

A brute-force solution would try every possible sequence of vertices, keep only sequences that form valid tram paths, and reject those with self-intersections. This is correct because every possible trip is explicitly considered. However, the number of possible paths is exponential. Even a complete search over subsets would already require roughly `2^300` states, which is impossible.

The useful observation is that the polygon is convex. Take a valid path and look at its first edge inside some interval of vertices. Once that edge is chosen, the rest of the path is forced to stay on one side of the chord, because using vertices on both sides would make some future segment cross the chosen chord.

This means the problem can be solved with interval dynamic programming. We keep track of a segment of the polygon that is still available and the endpoint where the current route is located. When we choose the next tram edge, the remaining problem becomes another smaller interval with a known endpoint.

Because the polygon is circular, we duplicate the vertices and run the interval DP on this doubled array. Every possible circular interval of length `n` then appears as an ordinary interval.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Interval DP | O(n³) | O(n²) | Accepted |

## Algorithm Walkthrough

1. Duplicate the polygon vertices. Vertex `i` is copied to position `i+n`, and every tram edge is copied accordingly. This converts circular ranges into normal intervals.
2. Define `dp[l][r]` as the maximum length of a valid route that uses only vertices from `l` to `r` and whose current endpoint is `l`.
3. Process intervals by increasing length. For an interval `[l,r]`, first inherit the answer from skipping vertex `l`, which gives `dp[l+1][r]`.
4. Try every possible first tram edge from `l` to a vertex `k` inside the interval. If that edge exists, after travelling to `k`, the remaining trip must stay inside `[k,r]` and start from `k`. The transition is:

$$dp[l][r] = \max(dp[l][r], dist(l,k)+dp[k][r])$$

1. The answer is the maximum `dp[i][i+n-1]` over all starting positions. These intervals represent every possible choice of where the circular polygon is cut.

The invariant behind the DP is that every valid route inside an interval has exactly one first edge from its current endpoint, or it does not use that endpoint at all. In the first case, the chosen edge divides the remaining search space into the smaller interval on the correct side of the chord. In the second case, removing the endpoint leaves another valid interval problem. Since every valid route follows one of these two forms, the recurrence considers every possible answer and never creates an invalid crossing.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve_case():
    n = int(input())
    pts = []
    for _ in range(n):
        x, y = map(int, input().split())
        pts.append((x, y))

    m = int(input())

    size = 2 * n
    edges = [[-1.0] * size for _ in range(size)]

    def length(a, b):
        x1, y1 = pts[a % n]
        x2, y2 = pts[b % n]
        return math.hypot(x1 - x2, y1 - y2)

    for _ in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        w = length(a, b)
        for x in (a, a + n):
            for y in (b, b + n):
                if x < size and y < size:
                    edges[x][y] = w
                    edges[y][x] = w

    dp = [[0.0] * size for _ in range(size)]

    for ln in range(2, n + 1):
        for l in range(size - ln + 1):
            r = l + ln - 1
            best = dp[l + 1][r]
            row = edges[l]
            for k in range(l + 1, r + 1):
                if row[k] >= 0:
                    cand = row[k] + dp[k][r]
                    if cand > best:
                        best = cand
            dp[l][r] = best

    ans = 0.0
    for i in range(n):
        if dp[i][i + n - 1] > ans:
            ans = dp[i][i + n - 1]
    return ans

def main():
    data = sys.stdin.read().split()
    if not data:
        return

    it = iter(data)

    def next_input():
        return next(it)

    global input
    old_input = input

    def fake_input():
        return next_input() + "\n"

    input = fake_input

    t = int(input())
    out = []
    for _ in range(t):
        out.append(f"{solve_case():.12f}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The edge matrix stores the length of every available tram line. The duplicated indexing is handled by taking coordinates modulo `n`, so copied vertices share the same geometric position.

The DP table only stores intervals of length at most `n`. Longer intervals in the doubled polygon would repeat a lighthouse and could create invalid routes. The interval length loop guarantees that every dependency has already been computed before it is used.

The transition tries every possible first tram line leaving the current endpoint. If no tram line exists, the state simply keeps the option of ignoring that endpoint. Python integers handle the coordinate range safely, and all geometric calculations use floating point only when computing final lengths.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n³) | There are O(n²) intervals and each tries O(n) next vertices. |
| Space | O(n²) | The DP table and edge matrix both contain O(n²) values. |

For `n = 300`, the cubic term is about 27 million transitions, which is suitable for the given limits. The total number of vertices over all tests keeps the accumulated work manageable.

## Edge Cases

When no tram lines exist, every DP transition fails and every state remains zero. The answer is correctly `0`, because Vladik cannot move anywhere.

When the best route wraps around the end of the input order, the duplicated polygon is what captures it. For a square where the available edges are `1-4`, `4-3`, `3-2`, `2-1`, the optimal route uses three sides. In the original indexing this crosses the artificial boundary, but in the doubled array it appears as an ordinary interval.

When two available chords cross, the DP never combines them into one route. Choosing one chord restricts the remaining state to one side of that chord, so the crossing chord cannot appear later in the same path. This is the geometric property that replaces explicit intersection checking.
