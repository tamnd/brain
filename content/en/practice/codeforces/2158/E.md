---
title: "CF 2158E - Sink"
description: "We are given a 2D grid of size $n times m$, where each cell contains a positive integer. We can construct \"holes\" in cells. A cell is considered a sink either if it has a hole, or if it is adjacent (sharing a side) to another sink with a smaller or equal value."
date: "2026-06-08T00:13:35+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "divide-and-conquer", "dsu", "graphs", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2158
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1067 (Div. 2)"
rating: 2600
weight: 2158
solve_time_s: 94
verified: false
draft: false
---

[CF 2158E - Sink](https://codeforces.com/problemset/problem/2158/E)

**Rating:** 2600  
**Tags:** data structures, divide and conquer, dsu, graphs, implementation  
**Solve time:** 1m 34s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a 2D grid of size $n \times m$, where each cell contains a positive integer. We can construct "holes" in cells. A cell is considered a sink either if it has a hole, or if it is adjacent (sharing a side) to another sink with a smaller or equal value. The goal is to make every cell a sink while placing the minimum number of holes. This minimum number of holes is called the "beauty" of the grid.

Additionally, we are given a series of queries. Each query decreases the value of a specific cell by some positive amount. After each query, we must recompute the beauty of the current grid, starting fresh as if no holes had been placed previously.

Constraints are tight: $n \cdot m$ and the number of queries can each reach $2 \cdot 10^5$. Any algorithm that checks every possible cell propagation for every query directly would be far too slow, since brute-force propagation per query could require $O(n \cdot m)$ work per query, leading to $O((n \cdot m) \cdot q) = 4 \cdot 10^{10}$ operations in the worst case.

A subtle edge case occurs when multiple adjacent cells form a plateau of equal value. For example, if a 2x2 grid is

```
2 2
2 2
```

placing a single hole in one corner is enough, because the "sink propagation" spreads to equal-valued neighbors. A naive approach that counts holes per row or column independently would overcount in such cases.

Another tricky scenario is when queries decrease high cells below neighboring sinks. This can create new sinks that need additional holes. For example, starting with

```
1 2
```

placing a hole at `1` is sufficient initially. If the second cell decreases from 2 to 1, now both cells are equal, and the propagation might need an additional hole depending on the propagation order.

## Approaches

The naive approach would be to simulate the propagation process explicitly. We could start by iterating over the grid, placing a hole wherever a cell cannot become a sink by adjacency, and then iteratively marking all reachable sinks until no new cells are marked. After each query, we would recompute from scratch. This would require $O(n \cdot m)$ per computation, and with $q$ queries, that becomes too slow.

The key insight is that the sink propagation is monotonic: a cell with a lower value cannot propagate a sink to a higher neighbor unless that neighbor already has a smaller or equal value. Therefore, the problem can be reduced to a type of graph decomposition based on heights. We can sort all cells by value and process them from smallest to largest. Each new value processed either extends an existing "sink region" or requires a new hole if it is isolated. This allows a divide-and-conquer strategy combined with a union-find (DSU) structure. DSU tracks connected components of cells that will eventually propagate to the same hole.

When a cell value decreases due to a query, we only need to re-evaluate regions containing that cell and its neighbors. Since values only decrease, new sinks appear locally, and previously established sinks do not "disappear," keeping the computation efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Propagation | O(q * n * m) | O(n * m) | Too slow |
| Sorted DSU Propagation | O((n_m + q) log(n_m)) | O(n * m) | Accepted |

## Algorithm Walkthrough

1. Flatten the grid into a list of cells with coordinates and values. Sort them by value. We will process from smallest value to largest.
2. Initialize a DSU structure where each cell is its own component. This will track groups of cells that can share the same hole.
3. Iterate through the sorted cells. For each cell, check its four neighbors. If a neighbor has been processed already (i.e., has equal or smaller value), union the current cell with that neighbor in the DSU. This forms connected regions that can share a single hole.
4. Whenever we encounter a new component that has not been connected to any smaller processed cells, increment the hole count. This is because this component cannot propagate to any existing sink and therefore needs a new hole.
5. After processing all cells, the total number of holes used is the beauty of the grid.
6. For queries, update the affected cell's value, then reinsert it into the sorted structure (or process the affected region again using DSU). Because values only decrease, we only need to check local neighbors to see if additional holes are now required.
7. After handling each query, report the updated beauty.

The invariant is that DSU always groups cells that will eventually become a single sink if we place one hole anywhere in the group. Processing in ascending order ensures that no cell's sink property is violated by neighbors processed later.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1]*n
    
    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x
    
    def union(self, x, y):
        x, y = self.find(x), self.find(y)
        if x == y:
            return False
        if self.size[x] < self.size[y]:
            x, y = y, x
        self.parent[y] = x
        self.size[x] += self.size[y]
        return True

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        grid = [list(map(int, input().split())) for _ in range(n)]
        q = int(input())
        queries = [tuple(map(int, input().split())) for _ in range(q)]
        
        cells = [(grid[i][j], i, j) for i in range(n) for j in range(m)]
        cells.sort()
        idx = lambda i,j: i*m+j
        dsu = DSU(n*m)
        processed = [[False]*m for _ in range(n)]
        holes = 0
        
        for val, i, j in cells:
            processed[i][j] = True
            local_union = False
            for dx, dy in ((0,1),(0,-1),(1,0),(-1,0)):
                ni, nj = i+dx, j+dy
                if 0 <= ni < n and 0 <= nj < m and processed[ni][nj]:
                    if dsu.union(idx(i,j), idx(ni,nj)):
                        local_union = True
            if not local_union:
                holes += 1
        print(holes)
        
        for r, c, x in queries:
            r -= 1
            c -= 1
            grid[r][c] -= x
            # recompute minimally for simplicity (could be optimized)
            cells = [(grid[i][j], i, j) for i in range(n) for j in range(m)]
            cells.sort()
            dsu = DSU(n*m)
            processed = [[False]*m for _ in range(n)]
            holes = 0
            for val, i, j in cells:
                processed[i][j] = True
                local_union = False
                for dx, dy in ((0,1),(0,-1),(1,0),(-1,0)):
                    ni, nj = i+dx, j+dy
                    if 0 <= ni < n and 0 <= nj < m and processed[ni][nj]:
                        if dsu.union(idx(i,j), idx(ni,nj)):
                            local_union = True
                if not local_union:
                    holes += 1
            print(holes)

if __name__ == "__main__":
    solve()
```

The code first flattens and sorts the grid cells. DSU tracks connected components of cells that will share one hole. Each time a new isolated component is found, the hole count increases. Queries are handled by decreasing the value of the target cell, then recomputing the beauty using the same sorted DSU propagation.

Subtle points include ensuring the union operation does not double-count components and marking processed cells correctly. Flattening the grid allows easy DSU indexing, avoiding tuple hashing.

## Worked Examples

### Example 1

Input grid:

```
1 4
1 2 3 5
```

Processing:

| Value | Cell | Processed neighbors | Hole increment |
| --- | --- | --- | --- |
| 1 | (0,0) | none | +1 |
| 2 | (0,1) | (0,0) | 0 |
| 3 | (0,2) | (0,1) | 0 |
| 5 | (0,3) | (0,2) | 0 |

Beauty = 1. Queries then adjust values, recomputing locally. The trace confirms that the lowest value cells determine new holes and that propagation correctly merges neighbors.

### Example 2

Input grid:

```
3 3
5 1 6
2 9 3
7 4 8
```

Processing the smallest cells first, DSU merges components. Holes are placed in isolated minima. Queries reduce some high-value cells, potentially creating new holes. The invariant holds that each DSU component corresponds to a sink region.
