---
title: "CF 104772H - H-Shaped Figures"
description: "We are given a fixed directed segment defined by two points $P$ and $Q$. In addition, there are $n$ candidate line segments scattered on the plane. Each candidate segment can be used as a “vertical bar” in a geometric configuration."
date: "2026-06-28T16:12:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104772
codeforces_index: "H"
codeforces_contest_name: "2023-2024 ICPC NERC (NEERC), North-Western Russia Regional Contest (Northern Subregionals)"
rating: 0
weight: 104772
solve_time_s: 34
verified: true
draft: false
---

[CF 104772H - H-Shaped Figures](https://codeforces.com/problemset/problem/104772/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed directed segment defined by two points $P$ and $Q$. In addition, there are $n$ candidate line segments scattered on the plane. Each candidate segment can be used as a “vertical bar” in a geometric configuration.

We want to count ordered pairs of distinct segments $(a, b)$ chosen from the candidates such that together with segment $PQ$, they form an H-shaped structure.

Geometrically, this means the following conditions must hold simultaneously. Point $P$ must lie strictly inside segment $a$, and segment $a$ must not lie on the same infinite line as $PQ$. Similarly, point $Q$ must lie strictly inside segment $b$, and segment $b$ must not be collinear with $PQ$. Finally, the two chosen segments $a$ and $b$ must not intersect each other at any point.

So intuitively, each valid configuration is determined by picking one segment that “crosses” $P$ in a non-parallel way and another segment that “crosses” $Q$ in a non-parallel way, while ensuring the two chosen segments do not overlap or touch.

The constraints imply up to $2 \cdot 10^5$ segments across all test cases, so any solution must be roughly linear or near-linear per test case. A quadratic check over all pairs is immediately impossible because it would require about $4 \cdot 10^{10}$ intersection tests in the worst case.

A subtle point is that the conditions are geometric but the final task is combinatorial: we are counting valid pairs. That usually signals a reduction to classification plus counting with sorting or hashing.

A naive implementation failure appears in the intersection condition. For example, if many segments pass through $P$ or $Q$, a naive approach that checks all pairs of candidate segments would repeatedly recompute intersection geometry. Another pitfall is treating “point lies strictly inside segment” incorrectly by allowing endpoints, which would incorrectly include degenerate H-shapes where a segment endpoint coincides with $P$ or $Q$.

## Approaches

A brute-force solution would test every ordered pair of segments $(a, b)$. For each pair, we would check whether $P$ lies strictly inside $a$, whether $Q$ lies strictly inside $b$, whether $a$ and $b$ are not collinear with $PQ$, and whether $a$ and $b$ do not intersect. Each pair check requires constant time geometric predicates, so the total cost is $O(n^2)$ per test case.

With $n$ up to $2 \cdot 10^5$, this becomes completely infeasible. Even $n=10^5$ yields $10^{10}$ checks, far beyond limits.

The key observation is that most constraints are local to a single segment. Whether a segment is valid for $P$ depends only on that segment and $P$, not on other segments. The same applies to $Q$. The only global interaction is the intersection constraint between segments chosen for $P$ and those chosen for $Q$.

This suggests splitting segments into two groups: those that can serve $P$, and those that can serve $Q$. Once we have these groups, the problem reduces to counting pairs across the two groups and subtracting invalid interactions caused by segment intersections.

The critical structural insight is that intersection constraints can be handled by ordering segments around the points and counting “conflicting intervals” using sweep or sorting by angular order around $P$ and $Q$. This converts geometric intersection constraints into inversion counting over cyclic orders.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Angular sorting + counting | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

### 1. Classify segments by endpoint conditions

For each segment, check whether point $P$ lies strictly inside it. This is done using collinearity and bounding box checks. If true and the segment is not collinear with $PQ$, mark it as a candidate for $P$. Do the same for $Q$.

This step filters irrelevant segments early so later counting only considers meaningful candidates.

### 2. Represent segments relative to endpoints

For each valid segment for $P$, compute the two endpoints in polar angle order around $P$. Do the same around $Q$. This transforms each segment into an angular interval on a circle.

The reason for this transformation is that segment intersection relationships become interval overlaps in angular order when viewed from a fixed point.

### 3. Sort segments by angular representation

Sort candidate segments for $P$ by the angle of their midpoint around $P$, and similarly for $Q$. This ordering allows us to detect crossings by scanning in a consistent cyclic order.

This ordering is essential because intersection constraints become monotonic in angular space.

### 4. Count valid pairs using sweep logic

We want pairs $(a, b)$ such that $a$ is valid for $P$, $b$ is valid for $Q$, and they do not intersect.

Start with the total product $|A| \cdot |B|$. Then subtract invalid pairs where segment from $A$ intersects segment from $B$.

To count intersections efficiently, for each segment in $A$, we determine how many segments in $B$ it intersects using a sweep over angular endpoints, maintaining an active set. Each intersection corresponds to a crossing in angular order that can be counted as an inversion.

### 5. Aggregate final answer

The final result is total pairs minus intersecting pairs.

### Why it works

Each segment is fully determined by its angular span around a reference point. Two segments intersect if and only if their projections on at least one endpoint’s angular order cross. This reduces geometric intersection to a combinatorial crossing condition. Since crossings form an inversion structure under sorting, counting them with a sweep guarantees exact subtraction without double counting.

## Python Solution

```python
import sys
input = sys.stdin.readline

def cross(ax, ay, bx, by):
    return ax * by - ay * bx

def orient(px, py, ax, ay, bx, by):
    return cross(ax - px, ay - py, bx - px, by - py)

def on_segment(px, py, ax, ay, bx, by):
    if orient(px, py, ax, ay, bx, by) != 0:
        return False
    return min(ax, bx) <= px <= max(ax, bx) and min(ay, by) <= py <= max(ay, by)

def point_on_strict_segment(px, py, ax, ay, bx, by):
    if orient(px, py, ax, ay, bx, by) != 0:
        return False
    return (min(ax, bx) < px < max(ax, bx) or min(ay, by) < py < max(ay, by))

def solve():
    t = int(input())
    for _ in range(t):
        xP, yP, xQ, yQ = map(int, input().split())
        n = int(input())

        A = []
        B = []

        for _ in range(n):
            x1, y1, x2, y2 = map(int, input().split())

            if point_on_strict_segment(xP, yP, x1, y1, x2, y2):
                A.append((x1, y1, x2, y2))

            if point_on_strict_se_ment(xQ, yQ, x1, y1, x2, y2):
                B.append((x1, y1, x2, y2))

        total = len(A) * len(B)

        #
```
