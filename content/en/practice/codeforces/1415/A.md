---
title: "CF 1415A - Prison Break"
description: "We are given a rectangular prison with $n$ rows and $m$ columns. Each cell contains exactly one prisoner, and there is a single exit tunnel in a cell located at row $r$ and column $c$."
date: "2026-06-11T07:11:13+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math"]
categories: ["algorithms"]
codeforces_contest: 1415
codeforces_index: "A"
codeforces_contest_name: "Technocup 2021 - Elimination Round 2"
rating: 800
weight: 1415
solve_time_s: 83
verified: true
draft: false
---

[CF 1415A - Prison Break](https://codeforces.com/problemset/problem/1415/A)

**Rating:** 800  
**Tags:** brute force, math  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular prison with $n$ rows and $m$ columns. Each cell contains exactly one prisoner, and there is a single exit tunnel in a cell located at row $r$ and column $c$. Every prisoner can move to any adjacent cell (up, down, left, right) in one second, or stay in place. The goal is to determine how long it takes for the last prisoner to reach the escape tunnel if all prisoners move optimally. The result is the minimum number of seconds after which all prisoners can gather at the exit.

The input provides multiple test cases, each giving the prison size and the location of the tunnel. The output for each test case is a single integer representing the minimum time required for all prisoners to reach the tunnel.

The constraints are very large: $n$ and $m$ can be up to $10^9$, and the number of test cases $t$ can reach $10^4$. This immediately rules out any simulation or iteration over all cells. We cannot compute distances for each prisoner individually, nor can we store a full $n \times m$ matrix in memory. The solution must be a formula that computes the maximum distance directly.

The non-obvious edge cases involve tunnels located at corners or edges. For example, if the tunnel is in the top-left corner of a $1 \times 1$ prison, the answer is 0. If the tunnel is at $(1, 1)$ in a $10 \times 10$ prison, the farthest prisoner is in the opposite corner at $(10, 10)$, and the time is $18$. A careless approach that assumes the tunnel is near the center or that averages distances would produce wrong answers here.

## Approaches

The brute-force approach is to imagine each prisoner as a point in a grid and calculate its Manhattan distance to the tunnel. For each prisoner at $(i, j)$, the distance is $|i - r| + |j - c|$. The minimum number of seconds for all prisoners to reach the tunnel is then the maximum distance over all cells. This works conceptually, but iterating over every cell in an $n \times m$ grid is impossible for large $n$ and $m$. For the worst case, with $n = m = 10^9$, this would require $10^{18}$ operations, which is completely infeasible.

The key insight is that we only need the prisoner who is farthest from the tunnel. In a rectangular grid, the farthest cell from a given cell is always one of the four corners. Therefore, we can compute the distance from the tunnel to each corner and take the maximum. This reduces the problem from iterating over billions of cells to simply evaluating four expressions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*m) | O(1) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases, $t$.
2. For each test case, read the dimensions $n$ and $m$ and the tunnel position $(r, c)$.
3. Identify the four corners of the grid: $(1, 1)$, $(1, m)$, $(n, 1)$, and $(n, m)$.
4. Compute the Manhattan distance from the tunnel to each corner: $|r - 1| + |c - 1|$, $|r - 1| + |c - m|$, $|r - n| + |c - 1|$, and $|r - n| + |c - m|$.
5. Take the maximum of these four distances. This represents the minimum number of seconds needed for the farthest prisoner to reach the tunnel.
6. Print the maximum distance for each test case.

Why it works: Manhattan distance accurately represents the minimum number of moves required in a grid when movement is restricted to cardinal directions. The farthest prisoner from the tunnel must be in one of the corners, because any point inside the grid is closer to the tunnel than at least one corner. Taking the maximum distance ensures that all prisoners, including the farthest, can reach the tunnel.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m, r, c = map(int, input().split())
    dist1 = abs(r - 1) + abs(c - 1)
    dist2 = abs(r - 1) + abs(c - m)
    dist3 = abs(r - n) + abs(c - 1)
    dist4 = abs(r - n) + abs(c - m)
    print(max(dist1, dist2, dist3, dist4))
```

The solution first reads the number of test cases. For each test case, it reads the four integers representing the prison size and tunnel coordinates. The distances to the four corners are computed using absolute differences, which directly implement the Manhattan distance. The maximum of these four values is printed. Using `abs` guarantees that negative differences do not cause errors, and computing each distance independently avoids off-by-one mistakes.

## Worked Examples

### Sample 1

Input: `10 10 1 1`

| Corner | Distance |
| --- | --- |
| (1,1) | 0 |
| (1,10) | 9 |
| (10,1) | 9 |
| (10,10) | 18 |

Maximum distance: 18. This shows the farthest prisoner is in the bottom-right corner.

### Sample 2

Input: `3 5 2 4`

| Corner | Distance |
| --- | --- |
| (1,1) | 4 |
| (1,5) | 3 |
| (3,1) | 4 |
| (3,5) | 2 |

Maximum distance: 4. The farthest prisoners are in the top-left or bottom-left corners.

These examples demonstrate that the maximum distance always comes from one of the corners and that the algorithm correctly identifies it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only four distance computations are performed |
| Space | O(1) | No arrays or grids are stored |

Given $t \le 10^4$, the total operations are $4 \cdot t \le 4 \cdot 10^4$, which easily fits in the 1-second limit. Memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n, m, r, c = map(int, input().split())
        dist1 = abs(r - 1) + abs(c - 1)
        dist2 = abs(r - 1) + abs(c - m)
        dist3 = abs(r - n) + abs(c - 1)
        dist4 = abs(r - n) + abs(c - m)
        print(max(dist1, dist2, dist3, dist4))
    return output.getvalue().strip()

assert run("3\n10 10 1 1\n3 5 2 4\n10 2 5 1\n") == "18\n4\n6", "Sample 1"
assert run("1\n1 1 1 1\n") == "0", "Single cell"
assert run("1\n5 5 3 3\n") == "4", "Tunnel in center"
assert run("1\n1000000000 1000000000 1 1\n") == "1999999998", "Maximum size corner"
assert run("1\n1000000000 1000000000 500000000 500000000\n") == "1000000000", "Maximum size center"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1 1 1 1\n` | `0` | Single-cell prison |
| `1\n5 5 3 3\n` | `4` | Tunnel in the center |
| `1\n1000000000 1000000000 1 1\n` | `1999999998` | Maximum-size grid, corner tunnel |
| `1\n1000000000 1000000000 500000000 500000000\n` | `1000000000` | Maximum-size grid, center tunnel |

## Edge Cases

For a $1 \times 1$ prison, the tunnel is the only cell. The algorithm computes distances to the single corner $(1,1)$, which is 0. The output is correctly 0.

For the maximum-size grid with the tunnel at a corner, $(1,1)$ in a $10^9 \times 10^9$ prison, the farthest prisoner is at $(10^9,10^9)$. The algorithm computes `abs(1-10^9) + abs(1-10^9) = 1999999998`, which matches expectations.

When the tunnel is in the center, distances to corners vary. The algorithm correctly selects the maximum, ensuring the farthest prisoner is accounted for without iteration over all cells
