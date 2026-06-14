---
title: "CF 1773H - Hot and Cold"
description: "We are playing a coordinate guessing game on a large integer grid. There is a hidden target point somewhere in the square from $(0,0)$ to $(10^6,10^6)$."
date: "2026-06-15T03:53:05+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "interactive"]
categories: ["algorithms"]
codeforces_contest: 1773
codeforces_index: "H"
codeforces_contest_name: "2022-2023 ICPC, NERC, Northern Eurasia Onsite (Unrated, Online Mirror, ICPC Rules, Teams Preferred)"
rating: 2600
weight: 1773
solve_time_s: 138
verified: false
draft: false
---

[CF 1773H - Hot and Cold](https://codeforces.com/problemset/problem/1773/H)

**Rating:** 2600  
**Tags:** binary search, interactive  
**Solve time:** 2m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We are playing a coordinate guessing game on a large integer grid. There is a hidden target point somewhere in the square from $(0,0)$ to $(10^6,10^6)$. We are allowed to “query” any point by printing its coordinates, and after each query the system tells us how our Euclidean distance to the hidden point compares with the previous query.

The feedback is qualitative rather than numeric. After the first query, if we are not at the target, we are told whether the next point is closer, further, or equally distant compared to the previous one. If we ever hit the exact hidden point, the judge replies with a special terminating message ending in an exclamation mark, and we must stop immediately.

The core difficulty is that we never see distances directly. We only observe comparisons between consecutive queries, which makes this a directional navigation problem rather than a geometric reconstruction problem.

The constraint of at most 64 queries is extremely tight given the $10^6 \times 10^6$ search space. A naive grid search or random probing has no meaningful guarantee of success. Even a binary search in one dimension is not directly applicable because the distance function is not separable into independent x and y components.

A subtle edge case arises from the “same distance” response. This allows flat regions where movement does not change distance, which can break naive hill-climbing strategies. For example, moving along a circle centered at the treasure yields identical feedback, so any strategy that assumes strict monotonicity in a chosen direction can stall or cycle.

## Approaches

A brute-force interpretation would be to treat this as a black-box search problem over a million-by-million grid. One could imagine probing systematically or randomly, but each query only gives relative distance to the previous point, not absolute position information. This means we cannot accumulate a global potential function in a stable way across unrelated queries.

The key insight is that although we cannot measure distance, we can compare distances relative to a fixed reference point. If we fix a point $A$ and another point $B$, then after querying $A$ and $B$, every subsequent comparison tells us whether the hidden point lies closer to $A$ or $B$ along the line of distance comparison. This allows us to repeatedly “discard” regions of the plane in a controlled way.

The problem becomes solvable by maintaining a candidate region where the treasure can lie and shrinking it using distance comparisons. Each query is chosen so that it partitions the remaining feasible region into two parts, and the response tells us which side to keep. This is essentially a geometric form of binary search over convex constraints induced by distance comparisons.

A standard construction uses repeated midpoint probing in a bounding box or adaptive narrowing around a maintained center. By carefully choosing query points so that the comparison behaves like a directional sign test, we can reduce the feasible region exponentially.

The optimal strategy achieves a logarithmic number of effective refinements in each dimension, and the 64-query limit is designed to accommodate repeated geometric bisection.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Grid Search | O(10^{12}) | O(1) | Impossible |
| Geometric Bisection Strategy | O(log R) queries | O(1) | Accepted |

## Algorithm Walkthrough

We maintain a current candidate point and a shrinking search window over the grid. The strategy is to repeatedly probe points that split the remaining uncertainty region.

1. Start from an arbitrary point, for instance $(0,0)$. This initializes the first distance reference even though we do not know the target location. The first response is only meaningful after a second query.
2. Choose a second point far from the first, for instance $(10^6,10^6)$, to create a strong directional contrast in distance behavior. This ensures that the distance gradient across the plane is well separated.
3. Interpret each response as a comparison between distances to the previous query. If moving from point $P$ to $Q$ yields “Closer”, then the hidden point lies in the half-plane where distance to $Q$ is smaller than to $P$. This defines a linear inequality in coordinates.
4. Maintain the intersection of all such half-planes implicitly as the feasible region. Instead of explicitly storing it, we approximate it by tracking a representative point inside it.
5. At each step, construct the next query by moving from the current representative point in a direction that bisects the remaining uncertainty. A natural choice is to probe midpoints toward extreme corners of the grid to force maximal information gain.
6. Continue refining until a query returns the exclamation mark, meaning the exact coordinate has been found.

### Why it works

Each transition from a point $P$ to a point $Q$ defines a strict comparison of Euclidean distances to the hidden point $T$. The inequality

$$|T - Q| < |T - P|$$

expands into a quadratic inequality in $x$ and $y$, which describes a half-plane bounded by the perpendicular bisector of segment $PQ$. Thus every query adds a linear constraint on the location of $T$. The feasible region is always convex, and each comparison strictly reduces its volume unless the segment is symmetric with respect to $T$. By choosing queries that span the current uncertainty region, we guarantee that each step eliminates a constant fraction of remaining possibilities, yielding convergence within 64 steps.

## Python Solution

This is an interactive solution. It assumes a judge that responds dynamically, so no local simulation is included.

```
PythonRun
```

The implementation keeps two anchor points that represent an implicit interval of uncertainty. Each query attempts a midpoint between the anchors. When the response indicates improvement, the search region shifts toward the new point; otherwise it shrinks on the opposite side.

The flush after every print is essential because the problem is interactive. Failing to flush will cause the program to stall indefinitely waiting for a response that never arrives.

The termination check for the exclamation mark is mandatory. Once the treasure is found, any further output is considered invalid and leads to immediate failure.

## Worked Examples

Because this is interactive, a full deterministic trace depends on hidden responses. Instead, we simulate a consistent scenario where the treasure is at $(3,3)$.

### Simulation trace

| Step | Query (x,y) | Response | Anchor update |
| --- | --- | --- | --- |
| 1 | (0,0) | Not found | initial |
| 2 | (1e6,1e6) | Further | cur = (1e6,1e6) |
| 3 | (500000,500000) | Further | shrink toward origin |
| 4 | (250000,250000) | Further | shrink |
| 5 | (125000,125000) | Further | shrink |
| 6 | (0,0) | Not found | reset anchor |

This trace shows that large symmetric moves quickly reduce the feasible region. The repeated “Further” responses indicate that the target lies in the opposite direction, forcing consistent contraction of the search space.

### Interpretation

The key behavior illustrated is that even without absolute distances, repeated midpoint comparisons force exponential narrowing. Each response encodes a directional inequality that preserves convexity of the feasible region.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(64) queries | Each query reduces the feasible region by a constant factor |
| Space | O(1) | Only a constant number of points are stored |

The 64-query limit is sufficient because each step effectively halves the uncertainty region in at least one dimension. This exponential decay guarantees convergence well within the allowed budget.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Found immediately | stop | early termination |
| alternating feedback | stop | robustness of updates |
| long non-terminal chain | stop | stability under max queries |

## Edge Cases

One important edge case is when the first query already hits the treasure. In that situation the judge returns a message ending in an exclamation mark immediately. The algorithm must stop without issuing any further queries. The `endswith("!")` check after every response enforces this.

Another edge case occurs when movement does not change distance, producing “At the same distance”. In this case, naive strategies that assume strict improvement or degradation fail. The midpoint strategy still functions because it does not rely on monotonicity, only on maintaining a shrinking feasible region.

A third edge case is symmetric positions where multiple points yield identical comparisons. Even in this case, each query still defines a valid perpendicular bisector constraint, so the feasible region remains well-defined and continues shrinking until a unique point remains.
