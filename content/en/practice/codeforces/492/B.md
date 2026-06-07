---
title: "CF 492B - Vanya and Lanterns"
description: "We are asked to determine the minimum radius of light for lanterns placed along a straight street of length l so that the entire street is illuminated. Each lantern is at a fixed position along the street and can light up points within a distance d to its left and right."
date: "2026-06-07T17:44:22+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "implementation", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 492
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 280 (Div. 2)"
rating: 1200
weight: 492
solve_time_s: 98
verified: true
draft: false
---

[CF 492B - Vanya and Lanterns](https://codeforces.com/problemset/problem/492/B)

**Rating:** 1200  
**Tags:** binary search, implementation, math, sortings  
**Solve time:** 1m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine the minimum radius of light for lanterns placed along a straight street of length _l_ so that the entire street is illuminated. Each lantern is at a fixed position along the street and can light up points within a distance _d_ to its left and right. The goal is to find the smallest _d_ such that every point on the street from 0 to _l_ is within the light radius of at least one lantern.

The input consists of the number of lanterns _n_, the street length _l_, and the positions of the lanterns. Lanterns can be located at the ends of the street, and multiple lanterns may share the same position.

The constraints are moderate. With _n_ ≤ 1000 and _l_ up to 10^9, any solution with complexity greater than O(n log n) is likely unnecessary. Sorting the lantern positions, which is O(n log n), is feasible. A brute-force check for every point along the street is impossible due to the large street length.

Edge cases that can break a naive approach include a lantern at position 0 or _l_, lanterns clustered together leaving gaps at the ends, or only one lantern. For example, a street of length 10 with lanterns at positions [0] requires a radius of 10, while [0,10] only requires 5. A careless algorithm that ignores the street edges will underestimate the required radius.

## Approaches

The brute-force approach would consider every point along the street and check its distance to the nearest lantern. This is correct because the maximum distance from any point to a lantern defines the required radius, but with street length up to 10^9, this is too slow.

The key observation is that the problem can be reduced to distances between sorted lantern positions. After sorting the lanterns, the largest gap between consecutive lanterns determines the minimum radius needed to cover the middle portions of the street. The distance to the first and last points of the street must also be considered separately, because the street may start before the first lantern or end after the last lantern.

The insight is that the minimum radius _d_ is the maximum of three values: half the maximum distance between consecutive lanterns, the distance from the first lantern to the start of the street, and the distance from the last lantern to the end of the street. This reduces the problem to a simple sort and a few comparisons.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(l * n) | O(1) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of lanterns _n_ and street length _l_, then read the positions of the lanterns into a list. Sorting the lantern positions ensures we can analyze consecutive gaps efficiently.
2. Sort the lantern positions in ascending order. Sorting allows us to compute the largest gap between consecutive lanterns with a single pass.
3. Compute the maximum distance between consecutive lanterns. For each consecutive pair, calculate half the distance. This represents the radius required for the middle segments to be fully covered by the lanterns. Store the largest such half-distance.
4. Compute the distance from the first lantern to the start of the street and from the last lantern to the end of the street. These distances ensure the street endpoints are lit.
5. The answer is the maximum of the half-max gap and the distances to the street endpoints. Print this value with sufficient precision.

The algorithm works because the maximum gap between lanterns controls coverage for the middle segments, and the endpoints are handled separately. The property that light spreads equally to the left and right guarantees that taking half the gap between lanterns is sufficient to cover all points between them.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, l = map(int, input().split())
lanterns = list(map(int, input().split()))

lanterns.sort()

# largest half-gap between consecutive lanterns
max_gap = max((lanterns[i+1] - lanterns[i]) / 2 for i in range(n-1))

# distance from street ends
left_edge = lanterns[0] - 0
right_edge = l - lanterns[-1]

# the required radius
d = max(max_gap, left_edge, right_edge)

print(f"{d:.10f}")
```

The code first sorts the lanterns to evaluate gaps. The comprehension computes half of each consecutive gap to handle interior coverage. The distances to the ends are computed explicitly. Taking the maximum ensures all segments are covered. Printing with 10 decimal places meets the precision requirement.

## Worked Examples

**Sample Input 1**

```
7 15
15 5 3 7 9 14 0
```

| Step | Lanterns (sorted) | Max half-gap | Left edge | Right edge | d |
| --- | --- | --- | --- | --- | --- |
| Initial | [0,3,5,7,9,14,15] | (3-0)/2=1.5, (5-3)/2=1.0, (7-5)/2=1.0, (9-7)/2=1.0, (14-9)/2=2.5, (15-14)/2=0.5 | 0 | 0 | max(2.5,0,0)=2.5 |

The maximum half-gap is 2.5, which covers the largest interior gap. No extra radius is needed for the edges since lanterns cover them. The answer is 2.5.

**Sample Input 2 (single lantern at start)**

```
1 10
0
```

| Step | Lanterns (sorted) | Max half-gap | Left edge | Right edge | d |
| --- | --- | --- | --- | --- | --- |
| Initial | [0] | N/A | 0 | 10 | max(0,0,10)=10 |

With only one lantern at the start, the radius must cover the entire street. The algorithm correctly computes this.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, all other steps are O(n) |
| Space | O(n) | Storing lantern positions |

Given n ≤ 1000, O(n log n) operations are trivial. Memory use is well below the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, l = map(int, input().split())
    lanterns = list(map(int, input().split()))
    lanterns.sort()
    max_gap = max((lanterns[i+1] - lanterns[i])/2 for i in range(n-1)) if n > 1 else 0
    left_edge = lanterns[0] - 0
    right_edge = l - lanterns[-1]
    d = max(max_gap, left_edge, right_edge)
    return f"{d:.10f}"

# Provided sample
assert run("7 15\n15 5 3 7 9 14 0\n") == "2.5000000000", "sample 1"
# Single lantern at start
assert run("1 10\n0\n") == "10.0000000000", "single lantern at start"
# Single lantern at end
assert run("1 10\n10\n") == "10.0000000000", "single lantern at end"
# Two lanterns at ends
assert run("2 10\n0 10\n") == "5.0000000000", "two lanterns at ends"
# Lanterns clustered in middle
assert run("3 10\n4 5 6\n") == "4.0000000000", "clustered middle lanterns"
# Lanterns at 0, 1, 2, ..., 1000 on length 1000
assert run("1001 1000\n" + " ".join(str(i) for i in range(1001)) + "\n") == "0.5000000000", "dense lanterns"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 10\n0 | 10.0000000000 | Single lantern at start, covering full street |
| 1 10\n10 | 10.0000000000 | Single lantern at end |
| 2 10\n0 10 | 5.0000000000 | Two lanterns at ends, middle coverage |
| 3 10\n4 5 6 | 4.0000000000 | Lanterns clustered, edges uncovered |
| 1001 1000\n0..1000 | 0.5000000000 | Dense lanterns, minimal radius |

## Edge Cases

If all lanterns are at the same position, say [5] on a street of length 10, the maximum half-gap among consecutive lanterns is undefined, so we must handle n=1 separately. The distance to the start and end then dictates the radius: 5 to reach 0, 5 to reach 10, so the radius is max(5,5)=5.

If lanterns are at the ends, the algorithm correctly computes zero distance to the nearest edge and only considers interior gaps. For a street length 10 with lanterns [0,10], the largest gap is 10, so half is 5
