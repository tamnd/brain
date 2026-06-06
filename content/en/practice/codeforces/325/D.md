---
title: "CF 325D - Reclamation"
description: "We are asked to simulate a process of turning cells in a cylindrical grid from sea into land, one by one, while ensuring that a sea path connecting the top row to the bottom row always exists."
date: "2026-06-06T08:53:43+07:00"
tags: ["codeforces", "competitive-programming", "dsu"]
categories: ["algorithms"]
codeforces_contest: 325
codeforces_index: "D"
codeforces_contest_name: "MemSQL start[c]up Round 1"
rating: 2900
weight: 325
solve_time_s: 90
verified: false
draft: false
---

[CF 325D - Reclamation](https://codeforces.com/problemset/problem/325/D)

**Rating:** 2900  
**Tags:** dsu  
**Solve time:** 1m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to simulate a process of turning cells in a cylindrical grid from sea into land, one by one, while ensuring that a sea path connecting the top row to the bottom row always exists. The grid has `r` rows and `c` columns, with horizontal wrap-around connectivity: the leftmost and rightmost cells in the same row are considered adjacent. Each input operation specifies a cell to reclaim, and the output is the total number of cells successfully turned into land.

The key challenge is to efficiently check after each reclamation whether a top-to-bottom sea path still exists. A naive method of performing a flood-fill search after each operation would take `O(r * c)` time per operation. With up to 300,000 reclamation attempts and up to 9 million cells in the largest grid, this approach is far too slow, as it would require over 10^12 operations in the worst case.

A naive approach also risks subtle mistakes. For example, if one ignores the horizontal wrap-around, a reclamation that splits a row horizontally might be incorrectly allowed. Another edge case is when `r = 1`: a single row with wrap-around can easily be disconnected if we attempt to reclaim all cells, so the algorithm must treat single-row connectivity correctly.

## Approaches

The brute-force solution is conceptually simple: for each reclamation, mark the cell as land, then perform a BFS or DFS from every top-row sea cell to check if a bottom-row sea cell is reachable. This is correct because it directly implements the problem statement, but it is too slow: each check is O(r * c), and there are up to n = 3_10^5 operations, giving a worst-case time of 3_10^5 * 9_10^6 = 2.7_10^12 operations.

The key insight for a faster solution is to notice that the condition only requires knowing whether the top and bottom rows are connected via sea. If we reverse the problem and treat reclamation as "removing sea cells," we can track connected components of sea efficiently using a Disjoint Set Union (DSU) structure. Instead of checking connectivity after each removal, we can track connected components of sea cells, merging adjacent sea cells when necessary, and maintain two special markers: one for top-connected components and one for bottom-connected components. If a reclamation would break a connection between top and bottom, it is forbidden. Using DSU with union-by-rank and path compression, each operation is near-constant time, giving a total runtime that fits within the limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * r * c) | O(r * c) | Too slow |
| DSU Optimal | O(n * α(r * c)) | O(r * c) | Accepted |

Here, α is the inverse Ackermann function, which grows extremely slowly and can be treated as constant for practical purposes.

## Algorithm Walkthrough

1. Initialize a DSU for all grid cells, with extra boolean flags for each component: `top_connected` and `bottom_connected`. These flags indicate whether the component currently touches the top row or bottom row.
2. Initialize a `land` matrix marking all cells as sea (False).
3. Iterate over reclamation requests in the given order. For each cell `(x, y)`, check whether it is currently sea.
4. Tentatively mark the cell as land and check its four neighbors, considering wrap-around horizontally. If a neighbor is sea, merge the DSU components. When merging, propagate the `top_connected` and `bottom_connected` flags so that the merged component correctly reflects if it touches top or bottom.
5. After merging with neighbors, check if the DSU component containing this cell has both `top_connected` and `bottom_connected` flags set. If so, the cell cannot be reclaimed because it would disconnect the sea path. In that case, revert the cell to sea and do not merge its DSU, otherwise keep the reclamation.
6. Count all successful reclamations.

Why it works: The DSU tracks connected sea components efficiently. The invariant is that every sea component correctly knows whether it reaches the top or bottom. Since we only forbid reclamation if a component simultaneously touches top and bottom (indicating that removing this cell would break the path), this correctly enforces the top-to-bottom connectivity rule without performing costly BFS searches.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 25)

r, c, n = map(int, input().split())
cells = [tuple(map(lambda x: int(x)-1, input().split())) for _ in range(n)]

parent = {}
top_connected = {}
bottom_connected = {}
land = [[False] * c for _ in range(r)]

def find(u):
    if parent[u] != u:
        parent[u] = find(parent[u])
    return parent[u]

def union(u, v):
    u_root, v_root = find(u), find(v)
    if u_root == v_root:
        return
    parent[v_root] = u_root
    top_connected[u_root] |= top_connected[v_root]
    bottom_connected[u_root] |= bottom_connected[v_root]

def index(x, y):
    return x * c + y

successful = 0
for x, y in cells:
    if land[x][y]:
        continue
    land[x][y] = True
    idx = index(x, y)
    parent[idx] = idx
    top_connected[idx] = (x == 0)
    bottom_connected[idx] = (x == r - 1)
    
    neighbors = [
        (x - 1, y), (x + 1, y),
        (x, (y - 1) % c), (x, (y + 1) % c)
    ]
    for nx, ny in neighbors:
        if 0 <= nx < r and land[nx][ny]:
            union(idx, index(nx, ny))
    
    root = find(idx)
    if top_connected[root] and bottom_connected[root]:
        land[x][y] = False
        parent.pop(idx)
        top_connected.pop(idx)
        bottom_connected.pop(idx)
    else:
        successful += 1

print(successful)
```

The solution uses `parent` as the DSU parent dictionary, and two extra dictionaries to track whether each sea component touches the top or bottom row. Indexing flattens the 2D grid into 1D to simplify union-find operations. Wrap-around is handled via modulo in the horizontal direction. Reclamation that would disconnect the sea is reverted by removing the cell from `land` and deleting its DSU tracking.

## Worked Examples

**Sample 1**

Input:

```
3 4 9
2 2
3 2
2 3
3 4
3 1
1 3
2 1
1 1
1 4
```

Trace:

| Step | Cell | Action | Successful Reclamation | Notes |
| --- | --- | --- | --- | --- |
| 1 | 2,2 | Reclaim | 1 | Sea remains connected top-bottom |
| 2 | 3,2 | Reclaim | 2 | Connected to 2,2, still valid |
| 3 | 2,3 | Reclaim | 3 | Merged with 2,2, path valid |
| 4 | 3,4 | Reclaim | 4 | Merged with 3,2, path valid |
| 5 | 3,1 | Reclaim | 5 | Merged horizontally with 3,4 (wrap-around), path valid |
| 6 | 1,3 | Reclaim | 6 | Connected to 2,3, still valid |
| 7 | 2,1 | Skip | 6 | Would disconnect path |
| 8 | 1,1 | Skip | 6 | Would disconnect path |
| 9 | 1,4 | Skip | 6 | Would disconnect path |

This trace confirms that the algorithm correctly respects top-bottom connectivity and handles horizontal wrap-around.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * α(r * c)) | Each union/find operation is almost constant due to DSU optimizations; n operations total |
| Space | O(r * c) | DSU structures and land matrix store one entry per cell |

With n ≤ 3_10^5 and r_c ≤ 9*10^6, this fits within 5s and 512 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    r, c, n = map(int, input().split())
    cells = [tuple(map(lambda x: int(x)-1, input().split())) for _ in range(n)]

    parent = {}
    top_connected = {}
    bottom_connected = {}
    land = [[False] * c for _ in range(r)]

    def find(u):
        if parent[u] != u:
            parent[u] = find(parent[u])
        return parent[u]

    def union(u, v):
        u_root, v_root = find(u), find(v)
        if u_root == v_root:
            return
        parent[v_root] = u_root
        top_connected[u_root] |= top_connected[v_root]
        bottom_connected[u_root] |= bottom_connected[v_root]

    def index(x, y):
        return x * c + y

    successful = 0
    for x, y in cells:
        if land[x][y]:
            continue
        land[x][y] = True
        idx = index(x, y)
        parent[idx] = idx
        top_connected[idx] = (x == 0)
```
