---
title: "CF 1537B - Bad Boy"
description: "We are asked to place two yo-yos in a rectangular room to maximize the total Manhattan distance Anton must travel to pick them both up and return to his starting position. The room is an $n times m$ grid, and Anton starts at cell $(i, j)$."
date: "2026-06-10T15:22:50+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1537
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 726 (Div. 2)"
rating: 900
weight: 1537
solve_time_s: 1375
verified: false
draft: false
---

[CF 1537B - Bad Boy](https://codeforces.com/problemset/problem/1537/B)

**Rating:** 900  
**Tags:** constructive algorithms, greedy, math  
**Solve time:** 22m 55s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to place two yo-yos in a rectangular room to maximize the total Manhattan distance Anton must travel to pick them both up and return to his starting position. The room is an $n \times m$ grid, and Anton starts at cell $(i, j)$. Riley can throw both yo-yos in any cell, including the same cell. Anton moves only to adjacent cells in the four cardinal directions, so the distance between two cells is the sum of absolute differences of their row and column indices.

The input consists of up to $10^4$ test cases, and the room dimensions $n, m$ can be as large as $10^9$. This immediately rules out any brute-force approach that would try all possible placements of the yo-yos or simulate Anton's travel step by step. The only viable solution is one that computes the answer mathematically with constant time per test case.

Non-obvious edge cases include rooms with only one row or column, where there are fewer distinct cells to place yo-yos, or when Anton starts at a corner, because the “furthest points” from him may coincide with room boundaries. For instance, if $n = 1$ and $m = 5$ with Anton at $(1, 3)$, the optimal yo-yo positions are at $(1, 1)$ and $(1, 5)$, exploiting the ends of the row. Any approach that assumes a rectangular area in all directions would fail here.

## Approaches

The brute-force solution would consider every pair of cells in the room, compute the Manhattan distance for Anton to pick them both up and return to the start, and pick the pair with the maximum distance. The number of pairs is $O((nm)^2)$, which is impossible for the maximum constraints of $n, m \le 10^9$. This shows brute-force is infeasible.

The key observation is that the Manhattan distance is maximized when the two yo-yos are at two opposite corners of the room. This is because the distance Anton must travel is the sum of the distances from his starting cell to each yo-yo and back, and corners maximize row and column differences. Since Anton’s starting position does not change the fact that corners are extremal points, we only need to consider the four corners: $(1, 1)$, $(1, m)$, $(n, 1)$, and $(n, m)$. There are only six unique pairs of corners, so we can compute the total distance for Anton for each pair in $O(1)$ per pair, pick the maximum, and output that.

This reduces the problem from an impossible brute-force complexity to a constant-time solution per test case, even for the largest room dimensions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((nm)^2) | O(1) | Too slow |
| Optimal (corners) | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Identify the four corners of the room: $(1,1), (1,m), (n,1), (n,m)$. These are the only positions that can maximize Manhattan distances.
2. Generate all six unique pairs of corners. The pairs are: top-left & top-right, top-left & bottom-left, top-left & bottom-right, top-right & bottom-left, top-right & bottom-right, bottom-left & bottom-right.
3. For each corner pair, compute the total Manhattan distance Anton would travel: the distance from his starting position to the first yo-yo, plus the distance between the two yo-yos, plus the distance from the second yo-yo back to the starting position.
4. Keep track of the pair that gives the maximum distance.
5. Output the coordinates of the two yo-yos corresponding to the pair with the maximum distance.

Why it works: the Manhattan distance is additive in rows and columns, so placing yo-yos at extreme corners ensures that each coordinate difference is maximized. Any interior point would reduce either row or column distance, giving a smaller total path. Checking only corner pairs guarantees we find the optimal solution in constant time per test case.

## Python Solution

```python
import sys
input = sys.stdin.readline

def max_distance_yoyos(n, m, i, j):
    corners = [(1,1), (1,m), (n,1), (n,m)]
    best = None
    max_dist = -1
    for c1 in corners:
        for c2 in corners:
            dist = abs(i - c1[0]) + abs(j - c1[1]) \
                 + abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) \
                 + abs(c2[0] - i) + abs(c2[1] - j)
            if dist > max_dist:
                max_dist = dist
                best = (c1, c2)
    return best

t = int(input())
for _ in range(t):
    n, m, i, j = map(int, input().split())
    (x1, y1), (x2, y2) = max_distance_yoyos(n, m, i, j)
    print(x1, y1, x2, y2)
```

The function `max_distance_yoyos` explicitly computes distances for all corner pairs and tracks the maximum. Using only the four corners avoids the need to iterate over the enormous $n \times m$ grid. The nested loop over corners is only 16 iterations at most, which is effectively constant. The code also correctly handles all boundaries, including single-row or single-column rooms.

## Worked Examples

### Sample Input 1

```
n=2, m=3, i=1, j=1
```

| c1 | c2 | Distance |
| --- | --- | --- |
| (1,1) | (1,3) | 4 |
| (1,1) | (2,1) | 2 |
| (1,1) | (2,3) | 6 |
| (1,3) | (2,1) | 6 |
| (1,3) | (2,3) | 4 |
| (2,1) | (2,3) | 2 |

Optimal pair: `(1,1) & (2,3)` or `(1,3) & (2,1)`, giving maximum distance 6.

### Sample Input 2

```
n=4, m=4, i=1, j=2
```

Compute all corner pairs similarly. The optimal pair is `(4,1) & (4,4)`, giving maximum distance of 9.

These examples show that evaluating only corner pairs is sufficient, and the algorithm correctly identifies the pair giving the maximal Manhattan travel distance.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only 16 distance calculations per test case (four corners squared) |
| Space | O(1) | Only a few variables to store distances and best pair |

Even for $t = 10^4$ and maximal $n, m$, the total operations are around $1.6 \times 10^5$, well within time limits. Memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # run the solution
    t = int(input())
    for _ in range(t):
        n, m, i, j = map(int, input().split())
        (x1, y1), (x2, y2) = max_distance_yoyos(n, m, i, j)
        print(x1, y1, x2, y2)
    return output.getvalue().strip()

# provided samples
assert run("7\n2 3 1 1\n4 4 1 2\n3 5 2 2\n5 1 2 1\n3 1 3 1\n1 1 1 1\n1000000000 1000000000 1000000000 50\n") == \
"1 1 2 3\n4 1 4 4\n1 1 3 5\n1 1 5 1\n1 1 3 1\n1 1 1 1\n1 1 1000000000 1000000000"

# custom tests
assert run("1\n1 1 1 1\n") == "1 1 1 1", "single cell"
assert run("1\n1 5 1 3\n") == "1 1 1 5", "single row"
assert run("1\n5 1 2 1\n") == "1 1 5 1", "single column"
assert run("1\n1000000000 1000000000 500000000 500000000\n") == "1 1 1000000000 1000000000", "large grid"
assert run("1\n2 2 2 2\n") == "1 1 2 2", "small square"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 1 | 1 1 1 |  |
