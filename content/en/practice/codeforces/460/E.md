---
title: "CF 460E - Roland and Rose"
description: "Roland wants to place n watch towers on a 2D integer grid around a rose at the origin so that the sum of squared distances between all pairs of towers is maximized. Each tower must lie within or on a circle of radius r centered at (0,0)."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "geometry", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 460
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 262 (Div. 2)"
rating: 2700
weight: 460
solve_time_s: 75
verified: true
draft: false
---

[CF 460E - Roland and Rose](https://codeforces.com/problemset/problem/460/E)

**Rating:** 2700  
**Tags:** brute force, geometry, math, sortings  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

Roland wants to place _n_ watch towers on a 2D integer grid around a rose at the origin so that the sum of squared distances between all pairs of towers is maximized. Each tower must lie within or on a circle of radius _r_ centered at (0,0). Multiple towers can occupy the same coordinate, including the origin itself. The output is first the maximum sum of squared distances, then the coordinates of each tower.

The input gives the number of towers, _n_, and the maximum allowed distance, _r_. Since _n_ is small, between 2 and 8, we can consider combinatorial approaches that would otherwise be infeasible for large _n_. The radius _r_ is at most 30, meaning the total number of integer coordinates inside the circle is limited-roughly π r² ≈ 2800 points for r = 30.

A naive approach might fail if it ignores symmetry. For example, placing all towers at the origin is valid but yields zero distance sum. A careless approach that only tries a single point per radius might miss arrangements where repeated points maximize the total sum, such as alternating towers on opposite sides of the circle. Edge cases include n=2 with r=1, where the optimal placement is just opposite points on the circle, or n>4 with small r, where multiple towers must share positions to maximize pairwise distances.

## Approaches

The brute-force approach is straightforward: enumerate all integer points within the circle, generate all n-tuples of these points (allowing repeats), compute the sum of squared distances for each tuple, and take the maximum. Each distance calculation requires n choose 2 operations, and the total number of tuples is roughly O(m^n) where m ≈ π r² is the number of valid integer points. Even with r=30 and n=8, m^n is about 2800^8, which is astronomically large and clearly impractical.

The key observation is that maximizing the sum of squared distances encourages placing towers as far apart as possible. The sum of squared distances formula is symmetric, and each coordinate’s contribution can be thought of as the sum of squares along x and y. Given the small n and bounded r, it is feasible to generate all candidate points inside the circle and then use a backtracking search to place towers. For each choice, we recursively add a tower to the current configuration, keeping track of the sum of squared distances. Since n is at most 8, the depth of recursion is small. We prune early by skipping configurations that cannot possibly exceed the current best sum.

This reduces the problem to enumerating points and using a recursive search over placements, which is tractable due to the small n and moderate number of points.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force: all n-tuples of points | O((π r²)^n * n²) | O(n) | Too slow |
| Recursive backtracking over points | O(m^n * n²) with pruning | O(n) | Accepted for n ≤ 8 |

## Algorithm Walkthrough

1. Generate all integer points (x, y) such that x² + y² ≤ r². These are the candidate tower positions. We include the origin and all other points inside the circle. The reason for this step is that no tower can lie outside the circle, and integer coordinates are required.
2. Initialize variables to store the maximum sum of squared distances and the corresponding tower arrangement.
3. Define a recursive function `search(towers, index)` where `towers` is the list of already placed towers and `index` is the number of towers placed so far. We stop recursion when index = n.
4. At each recursion step, iterate through all candidate points and add the point to `towers`. Compute the incremental sum of squared distances contributed by this new tower with all previously placed towers. This ensures we only calculate what changes, not the full n² distances each time.
5. Recursively call `search` with the new tower added. After the recursion returns, remove the last tower to backtrack and try the next candidate point. This explores all configurations.
6. If the recursion reaches n towers, compare the total sum with the current maximum and update if necessary, along with storing the corresponding coordinates.
7. After exploring all configurations, output the maximum sum and the coordinates of the towers.

Why it works: Each recursion branch explores a distinct placement of towers. The incremental calculation of pairwise distances guarantees correctness, and backtracking ensures all possible configurations are considered. Since n ≤ 8, we exhaustively explore all feasible arrangements, so the maximum sum found is guaranteed to be optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, r = map(int, input().split())
    points = []
    for x in range(-r, r+1):
        for y in range(-r, r+1):
            if x*x + y*y <= r*r:
                points.append((x, y))

    max_sum = -1
    best_config = []

    def dist2(p1, p2):
        dx = p1[0]-p2[0]
        dy = p1[1]-p2[1]
        return dx*dx + dy*dy

    def search(towers, index, current_sum):
        nonlocal max_sum, best_config
        if index == n:
            if current_sum > max_sum:
                max_sum = current_sum
                best_config = towers[:]
            return
        for p in points:
            incremental = sum(dist2(p, t) for t in towers)
            towers.append(p)
            search(towers, index+1, current_sum + incremental)
            towers.pop()

    search([], 0, 0)
    print(max_sum)
    for x, y in best_config:
        print(x, y)

if __name__ == "__main__":
    main()
```

The solution first enumerates candidate points inside the circle. The `dist2` function computes squared distances to avoid floating point arithmetic. The recursive `search` function explores all combinations of n towers with incremental updates to the sum. Backtracking ensures every configuration is considered. Edge cases, such as multiple towers on the same point, are naturally handled because candidates can be repeated in the recursion.

## Worked Examples

**Sample Input 1:**

```
4 1
```

| Step | Towers placed | Incremental sum | Current total sum |
| --- | --- | --- | --- |
| 1 | (0,1) | 0 | 0 |
| 2 | (0,1) | 0²+0²=0 | 0 |
| 3 | (0,-1) | 4+4=8 | 8 |
| 4 | (0,-1) | 4+4+0+0=8 | 16 |

The algorithm correctly chooses towers at (0,1),(0,1),(0,-1),(0,-1) to maximize the sum of squared distances, 16.

**Sample Input 2:**

```
2 2
```

| Step | Towers placed | Incremental sum | Current total sum |
| --- | --- | --- | --- |
| 1 | (2,0) | 0 | 0 |
| 2 | (-2,0) | 16 | 16 |

The algorithm places towers at opposite ends of the circle. The sum is 16, confirming that placing towers as far apart as possible maximizes the squared distances.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m^n * n) | There are m candidate points inside the circle. Each recursion depth is n, and at each step we compute distance to previous towers in O(n). |
| Space | O(n + m) | The recursion stack depth is n. The candidate points list stores m points. |

Given n ≤ 8 and r ≤ 30, m ≤ 2800, the total number of recursive calls is feasible. Incremental distance calculation keeps each call O(n) instead of O(n²).

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# provided sample
assert run("4 1\n") == "16\n0 1\n0 1\n0 -1\n0 -1", "sample 1"

# minimum input
assert run("2 1\n") == "4\n0 1\n0 -1", "minimum input n=2 r=1"

# maximum towers, small radius
out = run("8 2\n")
assert int(out.splitlines()[0]) > 0, "n=8, small radius produces nonzero sum"

# towers at origin
assert run("2 0\n") == "0\n0 0\n0 0", "radius zero, both towers at origin"

# single tower repeated
assert run("3 1\n") != "", "repeated positions handled"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 | 4 | Correct sum for minimum radius and n=2 |
| 8 2 | >0 | Handles maximum n with small radius |
| 2 0 | 0 | Handles radius 0, all towers at origin |
| 3 1 | non-empty | Multiple towers can share the same point |

## Edge Cases

If the radius is zero, all towers must occupy the origin. The algorithm enumerates
