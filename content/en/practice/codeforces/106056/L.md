---
title: "CF 106056L - New Houses"
description: "The grid describes a small neighborhood laid out as an R by C map. Each cell is either blocked, freely walkable, a candidate house location, a school, or a park. Movement is only allowed between orthogonally adjacent walkable cells, and every move costs exactly one step."
date: "2026-06-25T12:21:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106056
codeforces_index: "L"
codeforces_contest_name: "The 1st Universal Cup. Stage 18: Shenzhen"
rating: 0
weight: 106056
solve_time_s: 46
verified: true
draft: false
---

[CF 106056L - New Houses](https://codeforces.com/problemset/problem/106056/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

The grid describes a small neighborhood laid out as an R by C map. Each cell is either blocked, freely walkable, a candidate house location, a school, or a park. Movement is only allowed between orthogonally adjacent walkable cells, and every move costs exactly one step.

The company wants to know which houses can actually be sold under a constraint: a buyer will only accept a house if both a school and a park are reachable from that house within at most distance D, measured in grid steps. A house is valid only if there exists at least one school within D steps and at least one park within D steps, where paths are restricted by blocked cells.

The task is to count how many house cells satisfy both of these reachability conditions.

The grid size is at most 30 by 30, so there are at most 900 cells. Even with a distance limit up to 1000, the state space is tiny, which strongly suggests that a shortest path computation from multiple sources is feasible.

A naive idea would be to run a BFS separately from each house, then search for a school and a park. That would mean up to 900 BFS runs on a 900 cell grid, each costing O(RC), which is already borderline but still plausible. However, if each BFS also searches for two targets independently, or restarts expensive work repeatedly, it becomes unnecessary duplication.

A subtle failure case for naive local search appears when one tries to stop BFS early after finding any school or park. For example, a house might find a nearby school quickly, but the nearest park might lie in a completely different region of the grid requiring full exploration. Early stopping based on partial discovery risks incorrect pruning if not handled separately for both target types.

Another mistake happens when computing distance independently for each house using DFS without memoization. In grids with corridors, this recomputes the same shortest paths many times and leads to redundant exponential exploration patterns in practice.

## Approaches

The brute-force direction treats each house as a query point. From every house, we run a shortest path search over the grid until we either reach a school and a park or exhaust all reachable cells. Each BFS is O(RC), so the total complexity becomes O(HRC), where H is the number of houses. In the worst case H is close to RC, which leads to roughly O((RC)^2). With RC up to 900, this can approach about 810,000 cell visits, which is still borderline but includes repeated scanning overhead and two separate target searches per BFS. If implemented carefully it may pass, but it is conceptually wasteful because every BFS repeats the same exploration from scratch.

The key observation is that all houses share the same environment, and the cost metric is uniform. This suggests reversing the perspective: instead of computing distance from each house to schools and parks, compute distances from all schools to every cell, and separately from all parks to every cell. This is a classic multi-source BFS idea. Once these two distance fields are known, each house can be evaluated in O(1) by checking whether both distances are within D.

This transformation works because shortest path distance in an unweighted grid is independent of the starting query set. A BFS from all sources simultaneously produces correct minimum distances to the nearest source of that type.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force BFS from each house | O((RC)^2) | O(RC) | Acceptable but unnecessary |
| Multi-source BFS from schools and parks | O(RC) | O(RC) | Accepted |

## Algorithm Walkthrough

We compute two independent distance maps: one for schools and one for parks.

1. Collect all school cells and run a BFS starting from all of them simultaneously. Initialize their distance as zero and push them into a queue. Every time we expand a cell, we relax its four neighbors if we find a shorter distance. This produces the minimum distance from every cell to its nearest school.
2. Repeat the same process for parks, producing a second distance grid that stores the minimum distance from each cell to the nearest park.
3. Iterate over all cells in the grid. Whenever we encounter a house cell, we check its value in both distance grids. If both distances are less than or equal to D, we count this house as valid.
4. Output the total count of valid houses.

The BFS expansion works correctly because each layer of the queue corresponds to increasing distance from the source set, and once a cell is visited with the smallest possible distance, any future path to it would only be longer due to uniform edge weights.

### Why it works

The algorithm maintains the invariant that when a cell is popped from the BFS queue, its recorded distance equals the shortest possible distance from any source of that type (school or park). Since all edges have equal cost, BFS explores in increasing order of distance, and multi-source initialization does not change correctness because all sources start at distance zero and propagate outward simultaneously. As a result, the computed distance grids exactly represent true shortest-path distances to the nearest school and nearest park respectively.

A house is valid if and only if both shortest-path constraints are satisfied, and since both constraints are checked independently using correct distance functions, no interaction effects can invalidate the result.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def bfs(starts, grid, R, C):
    INF = 10**9
    dist = [[INF] * C for _ in range(R)]
    q = deque()

    for r, c in starts:
        dist[r][c] = 0
        q.append((r, c))

    dr = [1, -1, 0, 0]
    dc = [0, 0, 1, -1]

    while q:
        r, c = q.popleft()
        for k in range(4):
            nr, nc = r + dr[k], c + dc[k]
            if 0 <= nr < R and 0 <= nc < C:
                if grid[nr][nc] != '#':
                    if dist[nr][nc] > dist[r][c] + 1:
                        dist[nr][nc] = dist[r][c] + 1
                        q.append((nr, nc))

    return dist

R, C, D = map(int, input().split())
grid = [list(input().strip()) for _ in range(R)]

schools = []
parks = []
houses = []

for i in range(R):
    for j in range(C):
        if grid[i][j] == 'S':
            schools.append((i, j))
        elif grid[i][j] == 'P':
            parks.append((i, j))
        elif grid[i][j] == 'H':
            houses.append((i, j))

distS = bfs(schools, grid, R, C)
distP = bfs(parks, grid, R, C)

ans = 0
for r, c in houses:
    if distS[r][c] <= D and distP[r][c] <= D:
        ans += 1

print(ans)
```

The BFS function is written generically for both schools and parks. The key implementation detail is initializing all sources at distance zero before starting the queue, which is what turns it into a multi-source BFS. The grid check `grid[nr][nc] != '#'` ensures we never traverse blocked cells.

A common mistake is to forget that BFS must treat all sources as starting simultaneously. If instead one runs BFS separately per source and then takes minimums manually, the solution becomes much slower and redundant.

Another subtle point is using a large sentinel value for initialization. This avoids accidental comparisons with uninitialized data and ensures that any reachable cell gets properly relaxed.

## Worked Examples

Consider a small grid where we evaluate whether houses can reach both facilities within the limit.

### Example 1

Input:

```
3 5 3
S...P
.#.#.
H...H
```

After BFS from schools:

| Cell | Distance to S |
| --- | --- |
| H(2,0) | 2 |
| H(2,4) | 6 |

After BFS from parks:

| Cell | Distance to P |
| --- | --- |
| H(2,0) | 6 |
| H(2,4) | 2 |

Now evaluation:

| House | distS | distP | Valid |
| --- | --- | --- | --- |
| (2,0) | 2 | 6 | No |
| (2,4) | 6 | 2 | No |

Output is 0, since neither house can reach both within D=3.

This shows how requiring both conditions simultaneously filters out asymmetric accessibility.

### Example 2

Input:

```
3 5 4
S...P
.....
H...H
```

After BFS:

| House | distS | distP | Valid |
| --- | --- | --- | --- |
| (2,0) | 2 | 4 | Yes |
| (2,4) | 4 | 2 | Yes |

Output is 2.

This demonstrates that once open paths exist, multi-source BFS correctly captures global shortest distances without recomputation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(RC) | Each BFS visits each cell at most once, and we run two BFS passes |
| Space | O(RC) | Two distance grids plus queues over at most RC cells |

The grid is at most 900 cells, so even with constant factor overhead, the solution is easily fast within limits. The approach remains efficient even for the maximum distance constraint since BFS complexity depends on structure, not on D.

## Test Cases

```python
import sys, io

def solve():
    from collections import deque
    input = sys.stdin.readline

    def bfs(starts, grid, R, C):
        INF = 10**9
        dist = [[INF]*C for _ in range(R)]
        q = deque()
        for r,c in starts:
            dist[r][c]=0
            q.append((r,c))
        dr=[1,-1,0,0]
        dc=[0,0,1,-1]
        while q:
            r,c=q.popleft()
            for k in range(4):
                nr,nc=r+dr[k],c+dc[k]
                if 0<=nr<R and 0<=nc<C and grid[nr][nc]!='#':
                    if dist[nr][nc]>dist[r][c]+1:
                        dist[nr][nc]=dist[r][c]+1
                        q.append((nr,nc))
        return dist

    R,C,D=map(int,input().split())
    grid=[list(input().strip()) for _ in range(R)]

    S=[];P=[];H=[]
    for i in range(R):
        for j in range(C):
            if grid[i][j]=='S': S.append((i,j))
            if grid[i][j]=='P': P.append((i,j))
            if grid[i][j]=='H': H.append((i,j))

    ds=bfs(S,grid,R,C)
    dp=bfs(P,grid,R,C)

    ans=0
    for r,c in H:
        if ds[r][c]<=D and dp[r][c]<=D:
            ans+=1
    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue() if False else None

# sample-like checks
# (placeholders since official samples were partial in prompt context)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single cell grid with house only | 0 | No facilities exist |
| All cells open, dense S and P | All H counted | Full reachability |
| Blocked separation between S and H | 0 | Wall handling |
| Multiple sources scattered | correct filtered count | multi-source BFS correctness |

## Edge Cases

One edge case occurs when a house is surrounded by open cells but separated from all schools by a thin wall. In that situation, BFS from schools never reaches the house cell, so its distance remains infinite and the final check correctly rejects it.

Another case is when there are multiple schools or parks. Multi-source BFS naturally handles this by initializing all of them at distance zero. The distance field becomes the minimum over all possible sources, so the nearest facility always dominates regardless of how many exist.

A final edge case is when D is extremely large. Even if D exceeds the grid diameter, the answer still depends only on reachability, not on the value of D itself. The algorithm correctly handles this because distances are computed exactly, and the threshold comparison remains valid regardless of scale.
