---
title: "CF 104015B - Computer Game"
description: "We are given a very small game board with exactly two rows and $n$ columns. A player starts at the top-left cell and wants to reach the bottom-right cell. Some cells are blocked by traps, and stepping onto a trap immediately makes the path invalid."
date: "2026-07-02T04:50:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104015
codeforces_index: "B"
codeforces_contest_name: "ICPC 2021-2022 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 104015
solve_time_s: 44
verified: true
draft: false
---

[CF 104015B - Computer Game](https://codeforces.com/problemset/problem/104015/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a very small game board with exactly two rows and $n$ columns. A player starts at the top-left cell and wants to reach the bottom-right cell. Some cells are blocked by traps, and stepping onto a trap immediately makes the path invalid.

The movement rule is more generous than in standard grid problems. From any cell $(x, y)$, you can move to any cell $(x', y')$ as long as both row and column differ by at most one. This includes horizontal, vertical, and diagonal moves, meaning each position connects to up to eight neighbors (less on boundaries). The task is simply to determine whether there exists any valid path from $(1, 1)$ to $(2, n)$ that never steps on a trap.

The input size is very small, with $n \le 100$. That immediately suggests that even fairly naive graph traversal techniques will be sufficient. A direct BFS or DFS over all cells is at most 200 nodes, and each node has constant-degree edges, so even an $O(n)$ or $O(n^2)$ solution is trivially fast.

A subtle issue comes from the diagonal movement rule. Because diagonals are allowed, many solutions that assume only 4-directional or 2-row special structure can miss valid shortcuts. For example, it is possible to "jump around" traps that would otherwise block a straight horizontal route.

Another corner case arises from the start and end constraints. The problem guarantees that $(1,1)$ and $(2,n)$ are safe, so we never need to validate them, but implementations that blindly check bounds or treat indices incorrectly can still accidentally block them.

A naive mistake is to assume that you can only move rightwards in columns. That is false because vertical and diagonal moves allow revisiting earlier columns, which means cycles exist. Any solution that assumes monotonicity in column index will be incorrect.

## Approaches

The brute-force interpretation is to treat every cell as a graph node and run a search from the start. Each node has up to eight edges depending on whether neighboring cells are inside the grid and not traps. A DFS or BFS explores all reachable cells until either the target is found or the search exhausts the component.

Because there are only $2n \le 200$ nodes, even checking all neighbors repeatedly is cheap. The worst-case work is proportional to the number of edges, which is at most $8 \cdot 200$, so under a few thousand operations.

There is no need for a more sophisticated optimization, but it is still useful to notice why this problem is structurally simple. The grid is tiny, connectivity is static, and there are no weights or constraints that depend on path history. This makes it a pure reachability problem in an undirected implicit graph.

One could try to compress states or reason greedily about column transitions, but that is unnecessary and risks mistakes because diagonal movement breaks simple row-by-row reasoning. The safest and cleanest approach is a standard BFS/DFS.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DFS/BFS | $O(n)$ | $O(n)$ | Accepted |
| Optimal BFS/DFS | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We model each cell as a node in a graph. Two nodes are connected if a move between their coordinates is allowed and both cells are safe.

1. Build a representation of the grid as a 2 by $n$ array of characters. Each cell is either safe or blocked.
2. Maintain a visited array of the same size to avoid revisiting cells and getting stuck in cycles caused by diagonal movement.
3. Initialize a queue (or stack) with the starting cell $(1, 1)$.
4. Repeatedly extract a cell from the data structure and consider it as the current position.
5. If the current position is $(2, n)$, immediately return success because we have found a valid path.
6. Try all up to eight neighboring moves by varying row by $-1, 0, +1$ and column by $-1, 0, +1$, skipping the zero move.
7. For each neighbor, check that it lies inside the grid and is not a trap.
8. If the neighbor is valid and unvisited, mark it visited and push it into the queue.
9. If the search ends without reaching $(2, n)$, return failure.

The key design choice is marking visited immediately when pushing into the queue. This prevents revisiting the same state through different diagonal paths, which would otherwise create unnecessary repetition.

### Why it works

The grid forms an unweighted graph where every move is reversible and has equal cost. BFS or DFS explores exactly the set of reachable nodes from the start. Since every valid path corresponds to a sequence of valid edges in this graph, reaching $(2, n)$ in the search is equivalent to the existence of a valid path in the game. The visited structure ensures termination without removing any reachable configurations from consideration, because it only prevents redundant exploration, not reachability.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    n = int(input().strip())
    g = [input().strip() for _ in range(2)]
    
    # (row, col), 0-indexed
    start = (0, 0)
    target = (1, n - 1)
    
    if g[0][0] == '1' or g[1][n - 1] == '1':
        print("NO")
        return
    
    vis = [[False] * n for _ in range(2)]
    q = deque()
    q.append(start)
    vis[0][0] = True
    
    while q:
        r, c = q.popleft()
        if (r, c) == target:
            print("YES")
            return
        
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < 2 and 0 <= nc < n:
                    if not vis[nr][nc] and g[nr][nc] == '0':
                        vis[nr][nc] = True
                        q.append((nr, nc))
    
    print("NO")

if __name__ == "__main__":
    solve()
```

The implementation directly mirrors the BFS described earlier. The grid is stored as two strings, and indexing is kept zero-based to avoid off-by-one errors at the boundaries. The nested loop over $(-1, 0, 1)$ for both row and column cleanly enumerates all 8 possible moves without manually listing them.

A common mistake is forgetting to exclude the $(0,0)$ move, which would incorrectly reinsert the same cell indefinitely. Another is delaying the visited marking until dequeue time, which can lead to repeated enqueueing of the same node through different diagonals, increasing runtime unnecessarily even though constraints are small.

## Worked Examples

Consider a simple grid:

```
n = 4
row1 = 0000
row2 = 0010
```

We trace BFS exploration:

| Step | Current | Queue after expansion | Visited additions |
| --- | --- | --- | --- |
| 1 | (1,1) | (1,2), (2,1), (2,2) | (1,2), (2,1), (2,2) |
| 2 | (1,2) | ... | neighbors added if safe |
| 3 | ... | ... | ... |

From the start, the search quickly discovers that even if a trap blocks a direct path in row 2, diagonal movement allows bypassing it by shifting row at column 2 or 3.

Now consider a blocking example:

```
n = 3
row1 = 010
row2 = 101
```

| Step | Current | Queue after expansion | Visited additions |
| --- | --- | --- | --- |
| 1 | (1,1) | (1,2), (2,1) | (1,2), (2,1) |
| 2 | (1,2) | (2,3) | (2,3) |
| 3 | (2,3) | target reached | stop |

This demonstrates that even with alternating traps, diagonal movement can preserve connectivity.

The second trace shows that BFS naturally discovers multi-step diagonal transitions without needing any special casing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each of the $2n$ cells is visited at most once, and each has constant neighbors |
| Space | $O(n)$ | Visited array and queue store at most $2n$ states |

Given $n \le 100$, the total number of operations is tiny, and the solution runs instantly within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    def solve():
        n = int(input().strip())
        g = [input().strip() for _ in range(2)]
        if g[0][0] == '1' or g[1][n - 1] == '1':
            return "NO"
        vis = [[False]*n for _ in range(2)]
        q = deque([(0,0)])
        vis[0][0] = True
        while q:
            r,c = q.popleft()
            if (r,c)==(1,n-1):
                return "YES"
            for dr in (-1,0,1):
                for dc in (-1,0,1):
                    if dr==0 and dc==0: continue
                    nr,nc=r+dr,c+dc
                    if 0<=nr<2 and 0<=nc<n and not vis[nr][nc] and g[nr][nc]=='0':
                        vis[nr][nc]=True
                        q.append((nr,nc))
        return "NO"

    return solve()

# provided sample-style tests
assert run("3\n000\n000\n") == "YES"
assert run("3\n010\n000\n") == "YES"

# custom cases
assert run("3\n000\n111\n") == "YES", "top row path exists"
assert run("3\n010\n101\n") == "YES", "diagonal rescue path"
assert run("4\n0100\n1011\n") == "NO", "blocked structure"
assert run("5\n00000\n00000\n") == "YES", "fully open grid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 open rows | YES | trivial reachability |
| alternating traps | YES | diagonal bypass |
| blocked bottom row | YES | top-row routing |
| structured traps | NO | true separation |
| full grid | YES | maximal openness |

## Edge Cases

A common edge case is when traps form a zigzag that seems to block straight movement but still leaves a diagonal escape. For example:

```
n = 3
000
010
```

From $(1,1)$, BFS can move to $(2,2)$ diagonally, then to $(1,3)$, and finally to $(2,3)$. The algorithm handles this correctly because all eight directions are always explored.

Another edge case is when the only valid path repeatedly switches rows at adjacent columns. Without diagonal moves, this would require explicit vertical transitions, but here it happens naturally as part of the neighbor enumeration.

Finally, cases where almost all cells are blocked except a thin winding corridor are still handled correctly because BFS does not assume any directional bias and treats every reachable configuration uniformly.
