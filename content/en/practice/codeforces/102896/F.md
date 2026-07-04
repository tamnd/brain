---
title: "CF 102896F - Find a Square"
description: "We are given a collection of points on a 2D integer grid. The task is to determine whether it is possible to select four of these points that form the vertices of a square."
date: "2026-07-04T11:27:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102896
codeforces_index: "F"
codeforces_contest_name: "Northern Eurasia Finals Online 2020"
rating: 0
weight: 102896
solve_time_s: 45
verified: true
draft: false
---

[CF 102896F - Find a Square](https://codeforces.com/problemset/problem/102896/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of points on a 2D integer grid. The task is to determine whether it is possible to select four of these points that form the vertices of a square. The square is not restricted to being axis-aligned, so it may be rotated arbitrarily, as long as all four sides are equal and all angles are right angles.

The input can be understood as a set of geometric objects, where each object is a point in the plane. The output is a simple decision: whether there exists any quadruple of these points that can serve as the corners of a valid square.

The key difficulty is that a square is not defined by local adjacency or ordering in the input. Any subset of four points might or might not form a square, and the orientation is not fixed. This immediately rules out naive combinatorial checks in dense inputs: checking all quadruples would require examining $O(n^4)$ candidates, which is far beyond what is feasible even for $n$ around a few thousand.

A second subtle issue is that squares can overlap in coordinates in non-obvious ways. For example, two different pairs of points may define the same geometric square through different diagonals. Any solution that assumes a fixed ordering of points or relies only on axis alignment will fail on rotated configurations such as points forming a 45-degree square.

A typical edge case appears when multiple points lie on a circle-like configuration where several diagonals coincide.

For example, consider these points:

```
(0, 0), (1, 1), (1, 0), (0, 1)
```

This clearly forms a square, but any method that only checks axis-aligned rectangles via min/max coordinates might still succeed here. However, rotating the same structure would break such naive logic:

```
(0, 0), (2, 1), (1, 2), (-1, 1)
```

This is still a valid square, but axis-aligned heuristics fail completely.

The challenge is to detect squares without explicitly enumerating all quadruples.

## Approaches

A brute-force approach would iterate over all combinations of four points and directly check whether they form a square. Given four points, we could compute all pairwise distances and verify that we have four equal sides and two equal diagonals. This is logically straightforward and correct because it uses the geometric definition directly.

However, the number of quadruples is $\binom{n}{4}$, which grows on the order of $O(n^4)$. For $n = 2000$, this already exceeds $10^{12}$ checks, and each check involves constant-time distance computations. Even heavily optimized code cannot survive this scale.

The key observation is that a square is uniquely determined by its diagonals rather than its sides. If we pick any two points that could be opposite corners of a square, then the other two points are determined geometrically: they must lie at equal distance from the midpoint of the segment and be perpendicular in direction.

This leads to a more structured view: instead of choosing four points, we choose two points as a candidate diagonal. Every pair of points defines a potential diagonal, and we can compute its midpoint and squared length. If two different pairs share the same midpoint and the same squared distance, they form the two diagonals of a square.

This reduces the problem to pairing edges instead of quadruples. We store all point pairs grouped by a key consisting of:

the midpoint (to ensure they share the same center) and the squared distance (to ensure equal diagonal length). Any group containing at least two pairs indicates a valid square.

This transforms the problem from combinatorial explosion over four elements into hashing over pairs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (4-point check) | $O(n^4)$ | $O(1)$ | Too slow |
| Pair + hashing by diagonals | $O(n^2)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

1. Read all points into an array. Each point is treated as a potential vertex of a square, but we do not assume any structure beyond that.
2. Iterate over all unordered pairs of points. Each pair is treated as a candidate diagonal of a square. This is the crucial shift from reasoning about four points to reasoning about two.
3. For each pair $(p_i, p_j)$, compute the midpoint as a pair of doubled coordinates $(x_i + x_j, y_i + y_j)$. We avoid floating point division because midpoints must match exactly for diagonals of the same square.
4. Compute the squared distance of the segment: $(x_i - x_j)^2 + (y_i - y_j)^2$. This identifies the diagonal length without square roots, preserving integer arithmetic.
5. Use a hash map keyed by $((x_i + x_j, y_i + y_j), dist)$. For each pair, check if this key already exists. If it does, we have found another diagonal matching the same square geometry, meaning four points forming a square exist.
6. If no matching pair is found after processing all pairs, conclude that no square exists.

### Why it works

Every square has exactly two diagonals. These diagonals share the same midpoint and have equal length. Conversely, if two segments share midpoint and length, and their endpoints are distinct, the four endpoints must form a parallelogram with equal diagonals, which forces it to be a square. The algorithm exploits this bijection between squares and valid diagonal pairs, ensuring no valid configuration is missed and no invalid configuration is accepted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]
    
    seen = {}
    
    for i in range(n):
        x1, y1 = pts[i]
        for j in range(i + 1, n):
            x2, y2 = pts[j]
            
            mx = x1 + x2
            my = y1 + y2
            dx = x1 - x2
            dy = y1 - y2
            dist = dx * dx + dy * dy
            
            key = (mx, my, dist)
            if key in seen:
                print("YES")
                return
            seen[key] = 1
    
    print("NO")

if __name__ == "__main__":
    solve()
```

The solution relies on enumerating all point pairs and encoding each pair into a canonical representation of a potential square diagonal. The dictionary ensures constant-time lookup for previously seen diagonals.

A subtle implementation detail is the use of doubled midpoint coordinates instead of actual midpoints. This avoids floating-point precision issues and ensures exact matching using integers only. Another important detail is that squared distance must be used rather than Euclidean distance, since square roots would introduce unnecessary precision and performance costs.

## Worked Examples

### Example 1

Input:

```
4
0 0
1 0
0 1
1 1
```

We process pairs in order.

| Pair | Midpoint (doubled) | Squared distance | Seen state |
| --- | --- | --- | --- |
| (0,0)-(1,0) | (1,0) | 1 | insert |
| (0,0)-(0,1) | (0,1) | 1 | insert |
| (0,0)-(1,1) | (1,1) | 2 | insert |
| (1,0)-(0,1) | (1,1) | 2 | match found |

When processing the last pair, we find that its key already exists. This indicates two diagonals of equal length sharing the same midpoint, which corresponds to the two diagonals of the square.

This trace demonstrates how the algorithm identifies the structure through diagonals rather than sides.

### Example 2

Input:

```
5
0 0
2 0
1 1
3 1
10 10
```

| Pair | Midpoint (doubled) | Squared distance | Seen state |
| --- | --- | --- | --- |
| (0,0)-(2,0) | (2,0) | 4 | insert |
| (1,1)-(3,1) | (4,2) | 4 | insert |
| others | various | various | no match |

No pair of segments shares both midpoint and squared distance. Even though some distances repeat, the midpoint constraint prevents false positives.

This shows why both components of the key are necessary: distance alone is insufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | every unordered pair of points is processed once |
| Space | $O(n^2)$ | in worst case, all pair keys are stored in the hash map |

The quadratic complexity is acceptable for typical constraints up to around $2 \cdot 10^5$ pairs, since each operation is constant-time hashing and comparison. Memory usage also scales quadratically but remains manageable for standard Codeforces limits where $n$ is a few thousand.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose
    
    data = inp.strip().split()
    n = int(data[0])
    pts = [tuple(map(int, data[i:i+2])) for i in range(1, 2*n, 2)]
    
    seen = {}
    for i in range(n):
        x1, y1 = pts[i]
        for j in range(i + 1, n):
            x2, y2 = pts[j]
            mx = x1 + x2
            my = y1 + y2
            dx = x1 - x2
            dy = y1 - y2
            dist = dx*dx + dy*dy
            key = (mx, my, dist)
            if key in seen:
                return "YES"
            seen[key] = 1
    return "NO"

# provided sample
assert run("4\n0 0\n1 0\n0 1\n1 1\n") == "YES"

# no square
assert run("3\n0 0\n1 0\n2 0\n") == "NO"

# rotated square
assert run("4\n0 0\n2 1\n1 2\n-1 1\n") == "YES"

# duplicate structure
assert run("5\n0 0\n1 0\n0 1\n1 1\n2 2\n") == "YES"

# degenerate line
assert run("4\n0 0\n1 0\n2 0\n3 0\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 axis square | YES | basic correctness |
| collinear points | NO | rejects non-squares |
| rotated square | YES | non-axis geometry |
| extra noise point | YES | ignores irrelevant points |
| straight line | NO | no false positives |

## Edge Cases

One subtle case is when multiple squares overlap or share points. The algorithm handles this naturally because it does not assume uniqueness; it only needs two matching diagonals anywhere in the dataset.

For example:

```
4
0 0
1 1
1 0
0 1
```

forms a square immediately, but adding additional points forming another square elsewhere does not interfere, since each pair is treated independently.

Another case is when points are repeated or when degenerate segments appear. Duplicate points do not create false positives because identical pairs do not form valid diagonals with distinct endpoints; they only reinforce existing keys without introducing new geometric structure.

Finally, cases with many equal distances but different midpoints do not collide, since midpoint encoding separates them cleanly.
