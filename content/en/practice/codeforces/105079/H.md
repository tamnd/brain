---
title: "CF 105079H - Packing Cupcakes"
description: "We are simulating a dynamic process on an $N times M$ grid that starts empty and gradually becomes filled cell by cell. Each incoming operation places a cupcake of one of three flavors into a specific empty cell."
date: "2026-06-27T22:50:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105079
codeforces_index: "H"
codeforces_contest_name: "UTPC x WiCS Contest 04-05-23 (UT Internal)"
rating: 0
weight: 105079
solve_time_s: 88
verified: false
draft: false
---

[CF 105079H - Packing Cupcakes](https://codeforces.com/problemset/problem/105079/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are simulating a dynamic process on an $N \times M$ grid that starts empty and gradually becomes filled cell by cell. Each incoming operation places a cupcake of one of three flavors into a specific empty cell. After every placement, we must report how many connected components exist among all currently placed cupcakes, where connectivity is defined orthogonally: cells are connected if they share a side, and a region is a maximal connected set of identical flavors.

The key point is that regions are flavor-sensitive. Two adjacent cells contribute to the same region only if they contain the same flavor and are connected through a chain of same-flavor adjacencies. This means each color induces its own evolving graph, but we are asked for the total number of connected components across all colors combined.

The constraints $N, M \le 300$ imply at most 90,000 insertions. A solution that recomputes connected components from scratch after each insertion would need a flood fill or DFS over up to 90,000 cells per step, leading to roughly $O((NM)^2)$, which is far beyond feasible limits. Even a single DFS per update is already borderline; doing it $NM$ times makes it impossible.

The operations are online, so we must maintain connectivity dynamically.

A few subtle cases matter.

First, inserting into a cell that has no occupied neighbors creates a new region, so the count increases by one.

Second, inserting next to one or more cells of the same color can merge regions. For example, if a new cell connects two previously separate strawberry regions, the total number of regions decreases by one, not two, because those regions become one.

Third, adjacency to different colors does not interact at all; a blue neighbor does not affect strawberry connectivity.

A small example illustrating merging:

Input grid updates (conceptual):

Step 1: place S at (1,1) → 1 region

Step 2: place S at (1,2) → still 1 region

Step 3: place S at (2,1) → still 1 region

Step 4: place S at (2,2) → still 1 region

Now consider a different order:

Step 1: S at (1,1) → 1

Step 2: S at (1,3) → 2

Step 3: S at (1,2) → merges two regions → 1

A naive method that only checks “does it touch same color” without accounting for whether those neighbors already belong to different components will overcount.

The problem is therefore a classic dynamic connectivity maintenance problem on a grid with insertions only.

## Approaches

A brute-force approach maintains the entire grid and recomputes connected components after every insertion using DFS or BFS. After each of the $NM$ updates, we would scan all cells and flood fill each unvisited occupied cell. Each flood fill visits each cell at most once, so one recomputation costs $O(NM)$. Repeating this for $NM$ operations gives $O((NM)^2)$, which is about $8 \times 10^9$ visits in the worst case when $N=M=300$. This is too slow.

The key observation is that connectivity only changes locally at the inserted cell. Each new cell can only interact with at most four neighbors. If we could quickly determine whether those neighbors belong to the same component or different components, we could update the number of regions in constant or near-constant time per operation.

This is exactly a dynamic connectivity problem on a graph where edges are only added over time. Each cell is a node, and edges exist between adjacent cells of the same flavor. We need to maintain connected components under edge insertions.

Disjoint Set Union (DSU), also called Union-Find, is well-suited for this. Each time we place a cell, we create a new node (initially its own component). Then we attempt to union it with its already-occupied neighbors of the same flavor. If two nodes are already in the same set, no change occurs. If they are in different sets, merging reduces the number of regions by one.

The subtle but crucial point is that multiple neighbors might belong to the same component. We must avoid subtracting more than once for the same region. DSU naturally handles this because repeated unions within the same set are ignored.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (recompute DFS each step) | $O((NM)^2)$ | $O(NM)$ | Too slow |
| DSU incremental merging | $O(NM \cdot \alpha(NM))$ | $O(NM)$ | Accepted |

## Algorithm Walkthrough

We treat each grid cell as a node indexed by a unique integer $id = i \cdot M + j$.

1. Initialize a DSU structure for all $N \times M$ possible nodes. Maintain an occupancy array initially all false. Also maintain a running variable `regions = 0`.
2. For each incoming operation placing flavor $f$ at cell $(i, j)$, mark the cell as occupied and set `regions += 1`. This reflects the fact that a new isolated region is born.
3. For each of the four neighbors of $(i, j)$, check whether the neighbor is inside the grid and already occupied.
4. If a neighbor is occupied and has the same flavor, attempt to union the current cell with the neighbor in DSU. If the union succeeds (meaning they were previously in different components), decrement `regions` by 1. This captures the merging of two previously separate regions.
5. Output `regions` after processing the current operation.

The subtle reasoning behind step 4 is that DSU does not tell us directly whether two cells belong to different regions unless we compare their roots. A successful union implies two components are being merged, reducing the total count by exactly one.

### Why it works

The invariant is that after processing each operation, every connected component of same-colored occupied cells corresponds exactly to one DSU set, and `regions` equals the number of such sets. Initially both are zero. Each insertion adds a singleton set, increasing `regions` by one. Every time we union two distinct sets via a valid adjacency, we merge exactly two previously separate regions into one, decreasing the count by one. No other operation changes connectivity. Since DSU never incorrectly merges already-connected nodes, the count remains consistent with the true number of connected components.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True

def solve():
    N, M = map(int, input().split())
    total = N * M

    dsu = DSU(total)
    occupied = [False] * total
    color = [''] * total

    regions = 0

    def id_of(i, j):
        return i * M + j

    for _ in range(N * M):
        i, j, f = input().split()
        i = int(i) - 1
        j = int(j) - 1
        idx = id_of(i, j)

        occupied[idx] = True
        color[idx] = f

        regions += 1

        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < N and 0 <= nj < M:
                nidx = id_of(ni, nj)
                if occupied[nidx] and color[nidx] == f:
                    if dsu.union(idx, nidx):
                        regions -= 1

        print(regions)

if __name__ == "__main__":
    solve()
```

The DSU maintains connectivity between cells as a forest of parent pointers with path compression. The `union` function returns a boolean indicating whether a merge actually happened, which is essential for correctly updating the region count.

We also store the flavor of each cell in an array so we only union same-colored neighbors. Without this check, different flavors would incorrectly merge into a single region, violating the definition.

The grid-to-index mapping ensures we can treat the 2D grid as a flat DSU structure.

## Worked Examples

### Example 1

Consider a 2 by 2 grid with all placements being strawberry S:

| Step | Cell | Action | Union merges | Regions |
| --- | --- | --- | --- | --- |
| 1 | (1,1) S | new component | 0 | 1 |
| 2 | (1,2) S | merge with left | 1 merge | 1 |
| 3 | (2,1) S | merge with up | 1 merge | 1 |
| 4 | (2,2) S | merges both neighbors but only one new merge matters | 1 merge | 1 |

The key observation is that the last insertion touches two neighbors, but those neighbors already belong to the same DSU set, so only one union succeeds.

This confirms that DSU prevents double counting merges.

### Example 2

A sequence mixing colors:

| Step | Cell | Flavor | Neighbor interaction | Regions |
| --- | --- | --- | --- | --- |
| 1 | (1,1) | S | none | 1 |
| 2 | (1,3) | P | none | 2 |
| 3 | (1,2) | S | merges with (1,1) only | 2 |
| 4 | (2,3) | P | merges with (1,3) only | 2 |
| 5 | (2,2) | B | none | 3 |
| 6 | (2,1) | B | new merge with (2,2) | 3 |

This demonstrates that color separation is strictly enforced and that unions only happen within identical flavors.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(NM \cdot \alpha(NM))$ | Each cell is processed once, and each union/find is nearly constant due to path compression |
| Space | $O(NM)$ | DSU arrays and grid metadata store one entry per cell |

The total number of operations is at most 90,000, and each operation involves up to four DSU checks. This comfortably fits within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import prod

    # inline solution for testing
    class DSU:
        def __init__(self, n):
            self.p = list(range(n))
            self.s = [1]*n
        def f(self,x):
            while self.p[x]!=x:
                self.p[x]=self.p[self.p[x]]
                x=self.p[x]
            return x
        def u(self,a,b):
            a,b=self.f(a),self.f(b)
            if a==b:
                return False
            if self.s[a]<self.s[b]:
                a,b=b,a
            self.p[b]=a
            self.s[a]+=self.s[b]
            return True

    N,M=map(int,input().split())
    dsu=DSU(N*M)
    occ=[False]*(N*M)
    col=['']*(N*M)
    def idd(i,j): return i*M+j

    res=[]
    regions=0
    for _ in range(N*M):
        i,j,f=input().split()
        i=int(i)-1;j=int(j)-1
        idx=idd(i,j)
        occ[idx]=True
        col[idx]=f
        regions+=1
        for di,dj in ((1,0),(-1,0),(0,1),(0,-1)):
            ni,nj=i+di,j+dj
            if 0<=ni<N and 0<=nj<M:
                nidx=idd(ni,nj)
                if occ[nidx] and col[nidx]==f:
                    if dsu.u(idx,nidx):
                        regions-=1
        res.append(str(regions))
    return "\n".join(res)

# provided samples
assert run("""2 2
1 1 P
1 2 P
2 2 P
2 1 P
""") == "1\n1\n1\n1"

# custom cases
assert run("""1 1
1 1 S
""") == "1", "single cell"

assert run("""1 3
1 1 S
1 3 S
1 2 S
""") == "1\n2\n1", "merge two components"

assert run("""2 2
1 1 S
1 2 P
2 1 P
2 2 S
""") == "1\n2\n3\n4", "all different colors"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 single | 1 | base case |
| line merge | 1 2 1 | DSU merge behavior |
| checkerboard | increasing components | color isolation |

## Edge Cases

A critical edge case occurs when a new cell touches multiple neighbors that are already connected through other paths. For example, placing a cell that is adjacent to two neighbors of the same color but those neighbors are already in the same DSU set. The DSU prevents double decrement because only one union succeeds. The input:

```
2 2
1 1 S
1 2 S
2 1 S
2 2 S
```

When processing (2,2), it touches three S neighbors, but only one DSU merge occurs because all neighbors share the same root. The algorithm correctly keeps the region count unchanged.

This confirms that the method handles redundant adjacency safely without overcounting merges.
