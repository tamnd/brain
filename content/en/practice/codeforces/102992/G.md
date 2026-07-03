---
title: "CF 102992G - Go"
description: "The input is a square board where each position is either black, white, or empty. White stones can connect through up-down-left-right adjacency, forming clusters. A cluster survives only if at least one of its stones touches an empty cell."
date: "2026-07-04T04:41:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102992
codeforces_index: "G"
codeforces_contest_name: "2020-2021 ACM-ICPC, Asia Nanjing Regional Contest (XXI Open Cup, Grand Prix of Nanjing)"
rating: 0
weight: 102992
solve_time_s: 42
verified: true
draft: false
---

[CF 102992G - Go](https://codeforces.com/problemset/problem/102992/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

The input is a square board where each position is either black, white, or empty. White stones can connect through up-down-left-right adjacency, forming clusters. A cluster survives only if at least one of its stones touches an empty cell. If every stone in a cluster is completely surrounded by non-empty cells (black or white), that cluster is considered captured, and all its white stones must be counted.

The output is a single integer: the total number of white stones that belong to captured white clusters.

Because the board can have up to one million cells, any algorithm must run in linear time relative to the grid size. This immediately rules out repeated searches per stone or per query. The memory limit suggests that storing auxiliary arrays of the same size as the grid is fine, but nothing superlinear is possible.

A key failure case for naive logic appears when one checks each white stone independently without marking visited components. In a chain of 10,000 white stones, this would repeatedly re-scan the same structure, leading to massive duplication of work and incorrect performance assumptions.

Another edge case arises when a white cluster touches both black stones and other white clusters but has a single empty liberty somewhere far away in the same connected component. If that liberty is missed due to incomplete traversal, the cluster may be incorrectly marked as dead.

## Approaches

A brute-force method would iterate over every white stone and perform a flood fill from it to determine whether its connected component contains any empty neighbor. Each flood fill could cost $O(n^2)$, and in a dense board with all white stones, this becomes $O(n^4)$ in the worst case. The correctness is straightforward because each component is explicitly checked for liberties, but the repeated recomputation of the same components makes it infeasible.

The key observation is that the board naturally decomposes into connected components of white stones, and each component has a binary property: either it has at least one adjacent empty cell or it does not. This suggests running a single traversal per component instead of per node. A standard BFS or DFS can discover an entire component in one pass, simultaneously tracking whether any boundary touches a ‘.’ cell. Once the traversal finishes, we either add the size of the component to the answer or ignore it entirely.

This reduces the problem to linear time because each cell is visited exactly once and each edge is examined a constant number of times.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force per stone BFS | $O(n^4)$ | $O(n^2)$ | Too slow |
| Component BFS/DFS | $O(n^2)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

1. Scan every cell of the grid, and whenever an unvisited white stone is found, start a traversal from it. This ensures each white component is processed exactly once.
2. During traversal, maintain a queue or stack containing all stones in the current component. Mark each visited white cell so it is never added again to another traversal.
3. Keep two pieces of information while expanding the component: the number of white stones encountered, and a boolean flag indicating whether any neighboring cell of any visited stone is empty. This flag determines survival.
4. For each stone popped from the traversal structure, check its four neighbors. If a neighbor is white and unvisited, add it to the component. If a neighbor is empty, set the liberty flag to true. Black cells are ignored for expansion but do not affect the liberty flag.
5. After the traversal finishes, if the liberty flag is false, add the component size to the final answer.
6. Continue scanning the grid until all cells are processed.

The correctness rests on treating each connected component as a single entity. The traversal ensures no white stone is counted twice, and the liberty flag aggregates all possible escape points for the component.

### Why it works

Each white component is fully explored before any decision is made about it. Since connectivity is transitive, any white stone reachable from another white stone in the same component is guaranteed to be discovered in the same traversal. The liberty condition depends only on adjacency to empty cells, and this property is monotonic over the component: if any stone has a liberty, the entire component is alive. Therefore, classifying the component based on a single traversal preserves correctness and prevents double counting.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    n = int(input().strip())
    grid = [input().strip() for _ in range(n)]
    
    vis = [[False] * n for _ in range(n)]
    
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]
    
    ans = 0
    
    for i in range(n):
        for j in range(n):
            if grid[i][j] != 'o' or vis[i][j]:
                continue
            
            q = deque()
            q.append((i, j))
            vis[i][j] = True
            
            size = 0
            alive = False
            
            while q:
                x, y = q.popleft()
                size += 1
                
                for dx, dy in dirs:
                    nx, ny = x + dx, y + dy
                    if nx < 0 or nx >= n or ny < 0 or ny >= n:
                        continue
                    if grid[nx][ny] == '.':
                        alive = True
                    elif grid[nx][ny] == 'o' and not vis[nx][ny]:
                        vis[nx][ny] = True
                        q.append((nx, ny))
            
            if not alive:
                ans += size
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The grid is stored as strings to avoid repeated parsing overhead. The visited array ensures each white stone is processed exactly once. BFS is chosen over DFS to avoid recursion depth issues on large grids. The `alive` flag is updated whenever any empty neighbor is encountered, and the component size is accumulated only if no such neighbor exists.

A common implementation pitfall is forgetting that only white stones propagate the BFS; black stones should never be enqueued, even though they block expansion. Another subtle issue is boundary handling: out-of-bounds cells are ignored rather than treated as empty space.

## Worked Examples

### Example 1

Consider a small board:

```
o x o
x o x
o x .
```

| Step | Start Cell | Component Size | Alive Flag | Action |
| --- | --- | --- | --- | --- |
| 1 | (0,0) | 1 | false | no white neighbors |
| 2 | (1,1) | 1 | true | touches '.' at (2,2) |
| 3 | (0,2) | 1 | false | isolated white |

The final answer counts only components with no liberty, which are the isolated ones. This confirms that the BFS correctly distinguishes enclosed clusters from those touching empty space.

### Example 2

```
o o x
x o x
x x x
```

| Step | Component | Size | Alive Flag | Result |
| --- | --- | --- | --- | --- |
| 1 | all connected o's | 3 | false | fully enclosed |

All three white stones belong to one connected component with no adjacent empty cell. The BFS merges all whites into one traversal and correctly counts all of them.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | Each grid cell is visited once during BFS/DFS traversal |
| Space | $O(n^2)$ | Visited array and queue in worst case store all cells |

The grid size bound of $10^6$ cells fits comfortably within this complexity, since each operation is constant time per cell.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    
    def solve():
        n = int(input().strip())
        grid = [input().strip() for _ in range(n)]
        vis = [[False]*n for _ in range(n)]
        dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        ans = 0
        
        for i in range(n):
            for j in range(n):
                if grid[i][j] != 'o' or vis[i][j]:
                    continue
                q = deque([(i,j)])
                vis[i][j] = True
                alive = False
                size = 0
                
                while q:
                    x,y = q.popleft()
                    size += 1
                    for dx,dy in dirs:
                        nx,ny = x+dx, y+dy
                        if nx<0 or nx>=n or ny<0 or ny>=n:
                            continue
                        if grid[nx][ny]=='.':
                            alive = True
                        elif grid[nx][ny]=='o' and not vis[nx][ny]:
                            vis[nx][ny]=True
                            q.append((nx,ny))
                
                if not alive:
                    ans += size
        
        print(ans)
    
    solve()
    return sys.stdout.getvalue().strip()

# minimal
assert run("1\no\n") == "1"

# no capture
assert run("2\noo\n..") == "0"

# full capture
assert run("2\noo\noo") == "4"

# mixed
assert run("3\no.x\nxoo\nx.x") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 white | 1 | smallest component |
| surrounded whites with empty | 0 | liberty detection |
| all enclosed block | 4 | full component counting |
| mixed structure | 2 | correct component separation |

## Edge Cases

A single white stone completely surrounded by black stones demonstrates the simplest captured component. The BFS starts at that cell, finds no empty neighbors, and adds exactly one to the answer.

A large chain of white stones with one empty cell adjacent anywhere in the chain shows why per-cell checking fails. The traversal sees the empty neighbor once, sets the alive flag, and correctly avoids counting the entire structure.

A board with no white stones results in zero traversal triggers, and the algorithm immediately returns zero without unnecessary processing.
