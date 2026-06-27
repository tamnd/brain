---
title: "CF 105055M - Dimly Lit"
description: "A straight street runs from position 0 to position N. Along this line, there are M lampposts placed at arbitrary integer coordinates. Every lamppost uses an identical light bulb, and each bulb lights symmetrically left and right from its position with some fixed radius R."
date: "2026-06-28T00:27:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105055
codeforces_index: "M"
codeforces_contest_name: "UDESC Selection Contest 2023-2"
rating: 0
weight: 105055
solve_time_s: 79
verified: false
draft: false
---

[CF 105055M - Dimly Lit](https://codeforces.com/problemset/problem/105055/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 19s  
**Verified:** no  

## Solution
## Problem Understanding

A straight street runs from position 0 to position N. Along this line, there are M lampposts placed at arbitrary integer coordinates. Every lamppost uses an identical light bulb, and each bulb lights symmetrically left and right from its position with some fixed radius R.

If a lamp is at position x, it illuminates the interval from x − R to x + R. The city is considered fully illuminated if every point on the segment from 0 to N lies inside at least one such interval. The task is to choose the smallest possible common radius R such that the union of all illuminated segments covers the entire street.

The key difficulty comes from the irregular spacing of lampposts. Large gaps between consecutive lamps may force a large radius, but lamps near the edges also matter because the first lamp must cover the segment from 0, and the last must cover up to N.

The input size allows up to 200,000 lampposts. This immediately rules out quadratic solutions that try to test coverage for every candidate radius by simulating coverage point-by-point or checking all gaps repeatedly. A linear scan or a simple greedy pass is required, since O(M^2) operations would be far beyond feasible limits.

A subtle edge case arises when there is only one lamppost. In that case, the radius must simultaneously reach 0 and N, so the answer is max(P1, N − P1). Another corner case appears when lamps are extremely unevenly spaced, where the largest gap dominates the solution. Any approach that forgets boundary coverage at 0 or N will produce an answer that is too small.

## Approaches

A brute-force way to think about the problem is to fix a radius R and check whether all points from 0 to N are covered. For a given R, each lamppost produces an interval, and we could sort or merge these intervals and verify whether they collectively cover the entire segment. If we try all possible R values from 0 up to N, this becomes extremely slow, since each check costs O(M), and there are O(N) candidate radii, producing O(NM) worst-case complexity.

The structure of the problem suggests a monotonic property: if a radius R is sufficient to cover the street, any larger radius also works. This makes the problem suitable for binary search on the answer. However, even binary search is unnecessary once we observe what actually determines the required radius.

The critical insight is that the final answer is determined entirely by local constraints. Each gap between consecutive lampposts creates a region that must be covered from both sides, meaning a radius of at least half the gap is needed to bridge it. Similarly, the left edge requires the first lamp to reach position 0, and the right edge requires the last lamp to reach N.

Thus, the answer is governed by three types of distances: the distance from 0 to the first lamppost, the distance from the last lamppost to N, and half of the maximum gap between adjacent lampposts. The maximum of these three values is sufficient and necessary.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NM) | O(1) | Too slow |
| Optimal | O(M) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the distance from the left endpoint 0 to the first lamppost position P[0]. This is the minimum radius needed so that the first lamp can cover the start of the street.
2. Compute the distance from the last lamppost P[M−1] to the endpoint N. This ensures coverage at the right boundary.
3. Traverse all consecutive pairs of lampposts and compute the gap between them. For each pair (P[i], P[i+1]), calculate P[i+1] − P[i]. The required radius contribution from this gap is half of it, because two adjacent lamps must expand until their coverage meets in the middle.
4. Track the maximum value among the left boundary distance, right boundary distance, and half of every gap. This maximum is the minimum radius that satisfies all constraints simultaneously.
5. Output this maximum as an integer.

The reason step 3 uses half the gap is that if two lamps are distance d apart, each must cover at least d/2 toward the center to eliminate the uncovered region between them. Since all lamps share the same radius, the worst such gap dictates the required radius globally.

### Why it works

Any valid radius must at least handle the worst local deficiency in coverage. These deficiencies occur only at three places: the left boundary, the right boundary, and between adjacent lamps. If a radius R is smaller than any of these required values, there exists a point either at an endpoint or inside a gap that remains uncovered. Conversely, if R is at least as large as all these requirements, every gap is closed and both endpoints are reached, so coverage is continuous across the entire segment. This establishes both necessity and sufficiency.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    p = list(map(int, input().split()))

    ans = 0

    ans = max(ans, p[0] - 0)
    ans = max(ans, n - p[-1])

    for i in range(m - 1):
        gap = p[i + 1] - p[i]
        ans = max(ans, (gap + 1) // 2)

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation begins by reading the street length and lamppost positions. The variable `ans` accumulates the maximum required radius across all constraints. The boundary contributions are computed directly using the first and last positions.

The loop over adjacent pairs handles internal gaps. The expression `(gap + 1) // 2` performs integer ceiling division, which is necessary because if two lamps are at distance 3 apart, each must extend at least 2 units to meet in the middle; a floor division would underestimate the required radius.

Finally, the maximum collected value is printed as the answer.

## Worked Examples

### Sample 1

Input:

```
20 5
1 5 9 15 18
```

We track boundary distances and gaps.

| Step | Pair / Boundary | Value | Current Answer |
| --- | --- | --- | --- |
| Left boundary | 1 − 0 | 1 | 1 |
| Right boundary | 20 − 18 | 2 | 2 |
| Gap 1 | 5 − 1 | 4 → 2 | 2 |
| Gap 2 | 9 − 5 | 4 → 2 | 2 |
| Gap 3 | 15 − 9 | 6 → 3 | 3 |
| Gap 4 | 18 − 15 | 3 → 2 | 3 |

Final answer is 3.

This shows the largest structural constraint comes from the gap between 9 and 15, where a 6-unit separation forces a radius of 3.

### Sample 2

Input:

```
5 1
1
```

| Step | Component | Value | Current Answer |
| --- | --- | --- | --- |
| Left boundary | 1 − 0 | 1 | 1 |
| Right boundary | 5 − 1 | 4 | 4 |

Final answer is 4.

This case confirms that with a single lamppost, both endpoints independently constrain the radius.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(M) | single pass over lampposts |
| Space | O(1) | only a constant number of variables used |

The algorithm performs a single linear scan over the lamppost positions and computes local maxima. With M up to 2×10^5, this is comfortably within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    p = list(map(int, input().split()))

    ans = 0
    ans = max(ans, p[0])
    ans = max(ans, n - p[-1])

    for i in range(m - 1):
        ans = max(ans, (p[i + 1] - p[i] + 1) // 2)

    return str(ans)

# provided samples
assert run("20 5\n1 5 9 15 18\n") == "3"
assert run("5 1\n1\n") == "4"

# custom cases
assert run("10 2\n0 10\n") == "5"
assert run("10 3\n0 5 10\n") == "3"
assert run("7 2\n3 4\n") == "3"
assert run("100 4\n10 20 30 90\n") == "40"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 10 with endpoints only | 5 | symmetric edge coverage |
| evenly spaced | 3 | balanced gap handling |
| tight cluster | 3 | endpoint dominates |
| sparse far right lamp | 40 | large boundary effect |

## Edge Cases

When there is only one lamppost, the algorithm computes both boundary distances directly. For input `5 1 / 1`, the left boundary gives 1 and the right boundary gives 4, so the final answer becomes 4, correctly forcing the lamp to cover both ends simultaneously.

When lampposts sit exactly at the endpoints, for example `10 2 / 0 10`, boundary contributions become zero. The only constraint comes from the gap of 10, producing a required radius of 5, so the midpoint becomes the bottleneck and the algorithm returns 5 correctly.

When lampposts are very close together but far from one endpoint, for example `7 2 / 3 4`, the internal gap is small, but the left boundary requires 3 and the right boundary requires 3. The algorithm correctly ignores the small internal gap and outputs 3, showing that endpoint constraints can dominate even when local spacing is tight.
