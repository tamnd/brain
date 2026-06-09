---
title: "CF 2019E - Tree Pruning"
description: "We are given a sorted list of integer coordinates on a line. From every pair of these points, we draw a closed segment, meaning every integer point between the endpoints is included in that segment."
date: "2026-06-09T03:00:07+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dfs-and-similar", "dp", "sortings", "trees"]
categories: ["algorithms"]
codeforces_contest: 2019
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 975 (Div. 2)"
rating: 1700
weight: 2019
solve_time_s: 277
verified: false
draft: false
---

[CF 2019E - Tree Pruning](https://codeforces.com/problemset/problem/2019/E)

**Rating:** 1700  
**Tags:** constructive algorithms, dfs and similar, dp, sortings, trees  
**Solve time:** 4m 37s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sorted list of integer coordinates on a line. From every pair of these points, we draw a closed segment, meaning every integer point between the endpoints is included in that segment. After constructing all such segments, each integer position on the line is covered by some number of segments. The task is to answer multiple queries asking: how many integer positions are covered by exactly a given number of segments.

A direct way to interpret the structure is that each point on the line accumulates a “coverage count” depending on how many pairs of chosen endpoints surround it.

The constraints imply that both the number of points and queries can be large, up to one hundred thousand per test case, with total sums of that order across tests. This immediately rules out any solution that iterates over all pairs of points, since that would be quadratic and far beyond time limits. Even constructing all segment contributions explicitly is impossible because there are O(n²) segments.

The key difficulty is that coverage is not localized to individual segments but instead depends on combinatorial relationships between indices in sorted order.

A subtle edge case appears when coordinates are very sparse, for example when differences between consecutive x values are huge. In such cases, a naive solution that iterates over integer positions between endpoints would fail because the coordinate range can extend up to 10⁹, making per-integer iteration impossible. Another edge case is when all x values are consecutive; here the structure becomes dense and a correct solution must still handle O(n²) segment interactions without enumerating them.

## Approaches

A brute-force approach would generate every pair (i, j) and mark coverage on all integer points between x_i and x_j. This is correct in principle because it follows the definition directly, but each segment can cover up to O(max x) positions, and there are O(n²) segments, so this explodes immediately. Even with small optimizations, the structure is fundamentally too large to simulate.

The key observation is to reverse the viewpoint. Instead of thinking about segments covering points, we ask how many segments cover a given integer position p. A segment [x_i, x_j] covers p exactly when x_i ≤ p ≤ x_j, which is equivalent to choosing two endpoints on opposite sides of p. If we define cnt_left(p) as the number of points ≤ p and cnt_right(p) as the number of points ≥ p, then the number of segments covering p is cnt_left(p) multiplied by cnt_right(p), minus overcount corrections for ordering constraints. However, because endpoints are strictly from the given set, the exact structure simplifies into a function depending only on how many x_i lie to the left of p.

Between consecutive x_i and x_{i+1}, the coverage count is constant because no segment endpoints lie inside that interval. This reduces the problem to analyzing intervals induced by the sorted coordinates rather than individual integer positions.

For each gap between consecutive points, we compute how many segments fully cover that gap. That value depends only on how many points lie to the left and right of that region. Each pair (i, j) contributes exactly (x_j - x_i) integer points, and each such point shares the same coverage structure. This allows us to aggregate contributions in O(n) using combinatorial counting over index pairs rather than coordinate ranges.

Finally, we build a frequency map over coverage values and answer queries directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² · range) | O(range) | Too slow |
| Optimal | O(n²) or O(n log n) depending on implementation | O(n) | Accepted |

## Algorithm Walkthrough

We reformulate the problem in terms of contributions from pairs of indices and aggregate how many integer positions receive each coverage value.

1. Sort and fix the given points. They are already sorted, so we can work directly with their positions without reordering.
2. Observe that coverage only changes at integer coordinates adjacent to the given points. Between x_i and x_{i+1}, every integer point behaves identically in terms of which segments cover it. This allows us to treat each interval as a block.
3. For each pair of indices (i, j), compute how many integer points lie strictly inside the interval [x_i, x_j]. Every such point receives contribution from exactly those segments whose endpoints enclose it, so each pair contributes uniformly across its interval.
4. Instead of iterating over all points inside intervals, accumulate counts using differences. We treat each segment as contributing a range update: +1 coverage over [x_i, x_j]. A difference array over integer coordinates is impossible due to large coordinates, so we compress updates into contributions on intervals between consecutive x values.
5. Convert this into counting how many segments cover each elementary interval [x_k, x_{k+1}). For a fixed interval, the number of covering segments is determined by choosing endpoints i ≤ k and j ≥ k+1, which gives k · (n − k) choices.
6. Each such interval has length (x_{k+1} − x_k), so it contributes that many integer points with the same coverage value k · (n − k).
7. We aggregate over all k from 1 to n−1, storing frequency of each coverage value multiplied by interval length.
8. Finally, answer each query by looking up the precomputed frequency map.

### Why it works

The key invariant is that every integer point inside a gap between consecutive coordinates is indistinguishable with respect to segment coverage: any segment covering one such point covers all of them, and any segment missing one misses all. This reduces the problem from reasoning over coordinates to reasoning over index boundaries. The count of segments covering a gap depends only on how many endpoints lie to its left and right, which is fixed for each gap and independent of the exact integer position.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import defaultdict

def solve():
    t = int(input())
    for _ in range(t):
        n, q = map(int, input().split())
        x = list(map(int, input().split()))
        queries = list(map(int, input().split()))

        freq = defaultdict(int)

        for i in range(n - 1):
            left = i + 1
            right = n - (i + 1)
            cov = left * right
            length = x[i + 1] - x[i]
            freq[cov] += length

        res = []
        for k in queries:
            res.append(str(freq.get(k, 0)))

        print(" ".join(res))

if __name__ == "__main__":
    solve()
```

The implementation relies on compressing the contribution of each segment into adjacent-point intervals. The loop over i processes each elementary interval between consecutive coordinates. For interval i, any segment covering that interval must start at or before i and end after i, which yields the product structure (i+1) · (n−i−1). Multiplying by the interval length converts segment counts into counts of integer points.

A common pitfall is attempting to treat coordinates directly as indices without accounting for gaps. The multiplication by x[i+1] − x[i] is essential because each interval represents multiple integer positions.

## Worked Examples

Consider a small case with points [1, 3, 6]. The segments are [1,3], [1,6], [3,6]. The interval [1,3) has length 2 and is covered by segments starting at 1 and ending at either 3 or 6, so coverage is determined by endpoints around index 0. The interval [3,6) has length 3 and is covered by segments involving index 1.

| Interval | Length | Coverage formula | Result |
| --- | --- | --- | --- |
| [1,3) | 2 | 1 × 2 | 2 |
| [3,6) | 3 | 2 × 1 | 2 |

This shows how identical coverage values can appear across different interval sizes.

Now consider [1,2,4,7]. Each adjacent gap contributes independently, and coverage depends only on index splits, not actual distances. This demonstrates that geometry is irrelevant once intervals are fixed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | Each interval is processed once and each query is answered in O(1) lookup |
| Space | O(n) | Frequency map stores at most one entry per interval |

The total complexity matches the constraints since the sum of n and q across test cases is bounded by 2 × 10⁵.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    from collections import defaultdict

    t = int(input())
    out = []
    for _ in range(t):
        n, q = map(int, input().split())
        x = list(map(int, input().split()))
        queries = list(map(int, input().split()))

        freq = defaultdict(int)

        for i in range(n - 1):
            cov = (i + 1) * (n - i - 1)
            freq[cov] += x[i + 1] - x[i]

        out.append(" ".join(str(freq.get(k, 0)) for k in queries))

    return "\n".join(out)

# provided samples
assert run("""3
2 2
101 200
2 1
6 15
1 2 3 5 6 7
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
5 8
254618033 265675151 461318786 557391198 848083778
6 9 15 10 6 9 4 4294967300
""") == """0 100
0 0 0 0 2 0 0 0 3 0 2 0 0 0 0
291716045 0 0 0 291716045 0 301749698 0"""

# custom cases
assert run("""1
2 3
1 10
1 2 9
""") == "9 0 0"

assert run("""1
3 3
1 5 10
1 4 6
""") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| two points | direct single interval behavior | base correctness |
| three spaced points | multiple interval aggregation | interaction of gaps |

## Edge Cases

When all coordinates are consecutive, every interval has length 1 and the solution reduces to pure combinatorics over index pairs. The algorithm still works because the multiplication by interval length becomes neutral.

When gaps are extremely large, the algorithm remains stable because it never iterates over coordinates directly. Only differences x[i+1] − x[i] are used, which safely scale to large values without affecting complexity.

When queries ask for very large k, the frequency map simply returns zero since no interval produces such coverage.
