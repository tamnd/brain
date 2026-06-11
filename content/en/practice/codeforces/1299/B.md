---
title: "CF 1299B - Aerodynamic"
description: "We are given a strictly convex polygon $P$ in the plane as a list of its vertices in counterclockwise order. Each vertex has integer coordinates, and no three vertices are collinear."
date: "2026-06-11T18:23:56+07:00"
tags: ["codeforces", "competitive-programming", "geometry"]
categories: ["algorithms"]
codeforces_contest: 1299
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 618 (Div. 1)"
rating: 1800
weight: 1299
solve_time_s: 118
verified: true
draft: false
---

[CF 1299B - Aerodynamic](https://codeforces.com/problemset/problem/1299/B)

**Rating:** 1800  
**Tags:** geometry  
**Solve time:** 1m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a strictly convex polygon $P$ in the plane as a list of its vertices in counterclockwise order. Each vertex has integer coordinates, and no three vertices are collinear. From $P$, we define a new polygon $T$ as the set of all vectors $\overrightarrow{AB}$ where $A$ and $B$ are points in $P$. Geometrically, $T$ is the polygon formed by all translations of $P$ that contain the origin. The task is to determine whether $P$ and $T$ are similar in the geometric sense - they have the same shape up to scaling and rotation.

Input gives $n$, the number of vertices, followed by $n$ coordinate pairs. Output should be "YES" if $P$ and $T$ are similar and "NO" otherwise.

Given $n$ can reach $10^5$ and coordinates can go up to $10^9$, the algorithm must run in roughly $O(n)$ or $O(n \log n)$ time. Any approach with nested loops over all pairs of points ($O(n^2)$) is immediately ruled out.

A subtle edge case arises with very small polygons or highly asymmetric shapes. For example, a triangle with vertices $(0,0),(2,0),(1,3)$ generates a $T$ that is a hexagon with different side ratios. A naive approach that only looks at edges or bounding boxes could incorrectly claim similarity. The correct check must account for the relative vectors between points, not just side lengths.

## Approaches

The brute-force way to build $T$ is to iterate over all pairs of vertices $(A,B)$ in $P$ and store the vector $\overrightarrow{AB}$ as a vertex of $T$. We would then sort the resulting vectors counterclockwise and compare with $P$ for similarity. This is $O(n^2)$ and immediately impractical for $n=10^5$, since it would perform around $10^{10}$ operations.

The key insight is that $T$ is actually the Minkowski sum of $P$ and $-P$ (the polygon obtained by reflecting $P$ through the origin). Minkowski sums of convex polygons preserve edge directions and create a polygon with twice as many vertices. For strictly convex polygons, a known result is that $P$ and $T$ can only be similar if $P$ is centrally symmetric. More concretely, $T$ has vertices at the midpoints between opposite edges in $P$, so the condition reduces to checking that for every edge vector in the first half of $P$, there exists a parallel and equal-length edge vector in the opposite half.

This means we can solve the problem by comparing the sequence of edge vectors in $P$ with the sequence formed by summing opposite edges, all in $O(n)$ time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n²) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the edge vectors of $P$ in order. For vertices $v_0, v_1, ..., v_{n-1}$, the edge vector $e_i = v_{i+1} - v_i$ modulo $n$. Each vector encodes both direction and length of the edge.
2. Check whether $n$ is even. If $n$ is odd, $P$ cannot be centrally symmetric, so $P$ and $T$ cannot be similar. Output "NO".
3. For even $n$, split the edges into two halves. Pair each edge $e_i$ with $e_{i + n/2}$. The sum of each pair must be zero vector if $P$ is centrally symmetric. This directly encodes the Minkowski sum symmetry condition.
4. Iterate over $i$ from 0 to $n/2 - 1$. If $e_i + e_{i+n/2} \neq (0,0)$ for any $i$, output "NO". Otherwise, output "YES".

**Why it works:** For a convex polygon, $T = P + (-P)$. Two polygons are similar if one is a scaled and rotated copy of the other. For convex $P$, this occurs if and only if $P$ is centrally symmetric, because $T$ effectively doubles the shape by reflection. By checking edge vector pairs as above, we verify central symmetry without explicitly building $T$.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
vertices = [tuple(map(int, input().split())) for _ in range(n)]

if n % 2 == 1:
    print("NO")
    sys.exit(0)

edges = []
for i in range(n):
    x1, y1 = vertices[i]
    x2, y2 = vertices[(i+1)%n]
    edges.append((x2-x1, y2-y1))

half = n // 2
for i in range(half):
    ex, ey = edges[i]
    ex_op, ey_op = edges[i+half]
    if ex + ex_op != 0 or ey + ey_op != 0:
        print("NO")
        sys.exit(0)

print("YES")
```

The solution reads the polygon vertices and immediately rejects odd-sized polygons. Edge vectors are computed in order modulo $n$ to handle wrap-around. Each edge is paired with its opposite; failing any pair check returns "NO". The final "YES" occurs only if all pairs satisfy central symmetry.

## Worked Examples

**Sample 1:**

Input:

```
4
1 0
4 1
3 4
0 3
```

Compute edges:

| Edge | Vector |
| --- | --- |
| 0->1 | (3,1) |
| 1->2 | (-1,3) |
| 2->3 | (-3,-1) |
| 3->0 | (0,-3) |

Check pairs: (3,1)+(-3,-1)=(0,0), (-1,3)+(0,-3)=( -1+0,3-3)=(-1,0) → fails? Wait check carefully.

Edge computation must wrap carefully:

0->1: (4-1,1-0) = (3,1)

1->2: (3-4,4-1) = (-1,3)

2->3: (0-3,3-4) = (-3,-1)

3->0: (1-0,0-3) = (1,-3)

Now pairs:

(0,1) sum: (3,1)+(-3,-1)=(0,0) 

(1,2) sum: (-1,3)+(1,-3)=(0,0) 

Output: YES

**Sample 2 (triangle, n=3):**

```
3
0 0
1 0
0 1
```

n is odd → output NO

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to compute edge vectors, one pass to check symmetry pairs |
| Space | O(n) | Store edge vectors and vertices |

This fits comfortably within 1 second for $n=10^5$ with Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    captured = io.StringIO()
    sys.stdout = captured
    n = int(input())
    vertices = [tuple(map(int, input().split())) for _ in range(n)]

    if n % 2 == 1:
        print("NO")
        return captured.getvalue().strip()

    edges = []
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i+1)%n]
        edges.append((x2-x1, y2-y1))

    half = n // 2
    for i in range(half):
        ex, ey = edges[i]
        ex_op, ey_op = edges[i+half]
        if ex + ex_op != 0 or ey + ey_op != 0:
            print("NO")
            return captured.getvalue().strip()

    print("YES")
    return captured.getvalue().strip()

# provided samples
assert run("4\n1 0\n4 1\n3 4\n0 3\n") == "YES", "sample 1"
assert run("3\n0 0\n1 0\n0 1\n") == "NO", "sample 2"

# custom cases
assert run("4\n0 0\n2 0\n2 2\n0 2\n") == "YES", "square"
assert run("6\n0 0\n2 0\n3 1\n2 2\n0 2\n-1 1\n") == "YES", "hexagon symmetric"
assert run("4\n0 0\n1 0\n
```
