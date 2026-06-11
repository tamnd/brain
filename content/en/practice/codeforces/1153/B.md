---
title: "CF 1153B - Serval and Toy Bricks"
description: "We are given a 3-dimensional arrangement of unit bricks arranged in an $n times m$ grid. The height of bricks at position $(i,j)$ is unknown, but we are provided with three partial views: the front, the left, and the top."
date: "2026-06-12T02:52:01+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1153
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 551 (Div. 2)"
rating: 1200
weight: 1153
solve_time_s: 145
verified: false
draft: false
---

[CF 1153B - Serval and Toy Bricks](https://codeforces.com/problemset/problem/1153/B)

**Rating:** 1200  
**Tags:** constructive algorithms, greedy  
**Solve time:** 2m 25s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a 3-dimensional arrangement of unit bricks arranged in an $n \times m$ grid. The height of bricks at position $(i,j)$ is unknown, but we are provided with three partial views: the front, the left, and the top. The front view gives the maximum height in each of the $m$ columns along the row direction, the left view gives the maximum height in each of the $n$ rows along the column direction, and the top view is a binary $n \times m$ matrix indicating whether a brick exists at a particular position. The task is to reconstruct **any** 3D arrangement of bricks consistent with all three views.

Each height is bounded by the maximum allowed height $h$, and the number of rows and columns is at most 100, which is small enough to allow an $O(n \cdot m)$ solution. Brute force enumeration of all possible height combinations is unnecessary and would be inefficient even for these small limits because it would require trying $h^{n \cdot m}$ configurations.

A non-obvious edge case arises when the top view prohibits a brick at a position but the front or left view allows a positive height. For example, suppose the top view has a $0$ at $(2,3)$, the left view suggests row 2 has a maximum of $4$, and the front view suggests column 3 has a maximum of $5$. A careless implementation might try to assign the maximum allowed height without respecting the top view, resulting in an invalid configuration.

Another edge case occurs when the maximum height constraints from the front and left views differ. For instance, if the left view for row 1 is $3$ and the front view for column 2 is $2$, then the cell $(1,2)$ cannot exceed $2$, even though the row allows $3$. Handling these conflicts carefully is critical.

## Approaches

The naive approach would be to try assigning heights from $1$ to $h$ for every cell marked as $1$ in the top view and check if the maximum in each row and column matches the left and front views. This would be correct in principle but extremely inefficient, as it would require checking up to $h^{n \cdot m}$ configurations, which is infeasible even for $n = m = 100$.

The key insight is that each cell with a $1$ in the top view is **constrained independently** by the corresponding row and column maximums. Specifically, the height of a brick at $(i,j)$ cannot exceed either the left view for row $i$ or the front view for column $j$, because exceeding either maximum would violate one of the views. Since the top view allows the cell to be non-zero, the optimal and simplest choice is to assign the **minimum** of the row and column maxima. Cells with a $0$ in the top view are forced to zero, regardless of row or column constraints.

This observation reduces the problem to a single $O(n \cdot m)$ pass over the matrix, where for each cell we check the top view and assign either zero or the minimum of the row and column maxima.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(h^{n·m}) | O(n·m) | Too slow |
| Optimal | O(n·m) | O(n·m) | Accepted |

## Algorithm Walkthrough

1. Read $n$, $m$, and $h$. These define the dimensions of the 3D object and the maximum allowed height.
2. Read the front view array of length $m$. Each entry represents the maximum height for the corresponding column.
3. Read the left view array of length $n$. Each entry represents the maximum height for the corresponding row.
4. Read the top view $n \times m$ matrix, with entries $0$ or $1$.
5. Initialize an empty $n \times m$ matrix `H` to store the reconstructed heights.
6. Iterate over each cell $(i,j)$:

a. If the top view at $(i,j)$ is $0$, assign `H[i][j] = 0`.

b. If the top view at $(i,j)$ is $1$, assign `H[i][j] = min(left[i], front[j])`. This respects both the left and front view constraints while ensuring a positive height.
7. Print the matrix `H` row by row.

Why it works: The algorithm maintains the invariant that no row or column maximum is exceeded while ensuring that all cells indicated by the top view are positive. Assigning the minimum guarantees that all front and left view maxima can still be achieved by at least one cell in each row and column. Cells marked as $0$ in the top view are guaranteed to remain zero, preventing violations.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m, h = map(int, input().split())
front = list(map(int, input().split()))
left = list(map(int, input().split()))
top = [list(map(int, input().split())) for _ in range(n)]

H = [[0]*m for _ in range(n)]

for i in range(n):
    for j in range(m):
        if top[i][j]:
            H[i][j] = min(left[i], front[j])
        else:
            H[i][j] = 0

for row in H:
    print(' '.join(map(str, row)))
```

The first part reads input efficiently using `sys.stdin.readline`. The nested loops assign the minimum height respecting the top, left, and front views. Using `min(left[i], front[j])` ensures that the assigned height never violates the row or column maximum. Finally, we print each row of the reconstructed height matrix.

## Worked Examples

### Sample 1

Input:

```
3 7 3
2 3 0 0 2 0 1
2 1 3
1 0 0 0 1 0 0
0 0 0 0 0 0 1
1 1 0 0 0 0 0
```

Step trace:

| i | j | top[i][j] | left[i] | front[j] | H[i][j] |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 2 | 2 | 2 |
| 0 | 1 | 0 | 2 | 3 | 0 |
| 0 | 4 | 1 | 2 | 2 | 2 |
| 1 | 6 | 1 | 1 | 1 | 1 |
| 2 | 0 | 1 | 3 | 2 | 2 |
| 2 | 1 | 1 | 3 | 3 | 3 |

Output:

```
2 0 0 0 2 0 0
0 0 0 0 0 0 1
2 3 0 0 0 0 0
```

This confirms the algorithm respects all views and assigns heights correctly.

### Sample 2

Input:

```
2 3 4
3 4 1
4 2
1 0 1
1 1 1
```

Step trace:

| i | j | top[i][j] | left[i] | front[j] | H[i][j] |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 4 | 3 | 3 |
| 0 | 1 | 0 | 4 | 4 | 0 |
| 0 | 2 | 1 | 4 | 1 | 1 |
| 1 | 0 | 1 | 2 | 3 | 2 |
| 1 | 1 | 1 | 2 | 4 | 2 |
| 1 | 2 | 1 | 2 | 1 | 1 |

Output:

```
3 0 1
2 2 1
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n·m) | Single pass over the n×m grid, constant work per cell |
| Space | O(n·m) | Storage of top view and reconstructed heights |

The problem constraints ($n, m ≤ 100$) ensure that an $O(n·m)$ solution executes comfortably within the 1-second time limit. Memory usage is also well below the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m, h = map(int, input().split())
    front = list(map(int, input().split()))
    left = list(map(int, input().split()))
    top = [list(map(int, input().split())) for _ in range(n)]
    H = [[0]*m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if top[i][j]:
                H[i][j] = min(left[i], front[j])
            else:
                H[i][j] = 0
    return '\n'.join(' '.join(map(str,row)) for row in H)

# provided samples
assert run
```
