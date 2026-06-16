---
title: "CF 948A - Protect Sheep"
description: "The grid can be viewed as a rectangular graph where each cell is a node connected to its four orthogonal neighbors. Some nodes contain sheep, some contain wolves, and the rest are empty."
date: "2026-06-17T02:27:40+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dfs-and-similar", "graphs", "implementation"]
categories: ["algorithms"]
codeforces_contest: 948
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 470 (rated, Div. 2, based on VK Cup 2018 Round 1)"
rating: 900
weight: 948
solve_time_s: 80
verified: false
draft: false
---

[CF 948A - Protect Sheep](https://codeforces.com/problemset/problem/948/A)

**Rating:** 900  
**Tags:** brute force, dfs and similar, graphs, implementation  
**Solve time:** 1m 20s  
**Verified:** no  

## Solution
## Problem Understanding

The grid can be viewed as a rectangular graph where each cell is a node connected to its four orthogonal neighbors. Some nodes contain sheep, some contain wolves, and the rest are empty. Wolves are free to move step by step across empty cells, but they cannot pass through dogs once we place them. Sheep and dogs are static obstacles from the perspective of movement.

The task is to decide whether we can place dogs into empty cells so that no path exists from any wolf to any sheep using only four-directional moves through non-dog cells. If this is possible, we must output one valid configuration of dog placements. If not, we report impossibility.

The constraints allow up to a 500 by 500 grid, so the total number of cells is at most 250,000. Any solution that performs even a small constant amount of graph exploration per cell is fine, but anything attempting to recompute reachability separately for every wolf or every sheep would still be acceptable only if carefully implemented as a single traversal. A naive pairwise reachability check between wolves and sheep is immediately infeasible because it would imply up to O(R^2 C^2) behavior in the worst case.

A subtle point is that wolves are not individually constrained. A single wolf reaching any sheep invalidates the configuration, and multiple wolves can cooperate implicitly because reachability is purely graph based.

The main edge case arises when a wolf is adjacent to a sheep in the input. Since we are only allowed to place dogs in empty cells, there is no way to separate them if they are already neighboring. For example, in a 2 by 2 grid with a wolf and sheep adjacent, the answer must be impossible immediately. Another important edge case is when wolves surround a sheep in such a way that all paths from wolves to that sheep pass through a single empty corridor cell. That corridor must be blocked, and the solution must correctly identify and place dogs there.

## Approaches

A brute-force idea is to simulate the movement of all wolves using a multi-source BFS, marking all reachable cells. After computing the full reachable region of wolves, we simply check whether any sheep lies inside it. If a sheep is reachable, we try to place dogs to block paths and repeat. However, this becomes complicated because deciding where to place dogs dynamically requires solving a global minimum cut style problem, which is unnecessary here.

The key observation simplifies everything: we do not need to control all paths between wolves and sheep globally. We only need to ensure that no wolf can step directly into a sheep cell through an adjacent empty cell. If a wolf can reach a sheep, then there must exist a path where the last step enters the sheep from one of its four neighbors. This means that if we prevent adjacency between any wolf and any sheep by blocking empty neighbors of sheep, the entire problem is solved.

This reduces the problem to a local construction problem. We scan the grid. If any wolf is already adjacent to a sheep, there is no way to insert a dog between them, so the answer is immediately impossible. Otherwise, we place dogs in every empty cell adjacent to a sheep. These dogs act as barriers preventing any future reachability from wolves into sheep regions. Since wolves cannot pass through dogs, and all sheep are now isolated from adjacent empty cells that lead to wolves, no path can exist.

The brute-force exploration would simulate global reachability, but the structure of the grid ensures that only immediate adjacency matters, because any longer path must pass through a neighbor of a sheep first.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force BFS reachability checks | O(RC) per search, potentially O(R^2C^2) | O(RC) | Too slow / unnecessary |
| Optimal local blocking | O(RC) | O(RC) | Accepted |

## Algorithm Walkthrough

We treat the grid as a mutable structure and construct the final arrangement directly.

1. Copy the input grid into a mutable array so we can place dogs without losing original information. This is necessary because we must preserve all sheep and wolves unchanged.
2. Traverse every cell in the grid. Whenever we find a sheep, inspect its four neighboring cells.
3. If any neighbor is a wolf, we immediately conclude the answer is impossible. This is because we cannot place a dog inside a sheep or wolf cell, so adjacency cannot be repaired.
4. If a neighbor is empty, we convert it into a dog. This ensures that any future attempt by a wolf to move toward the sheep is blocked at the boundary. We do this eagerly for all sheep, since multiple sheep may share boundary cells.
5. After processing all cells, output the modified grid.

The reason we do not need to explicitly simulate wolves is that any valid path from a wolf to a sheep must pass through a neighbor of a sheep. By ensuring all such neighbors are blocked, we eliminate all possible routes in one pass.

### Why it works

Any path from a wolf to a sheep is a sequence of adjacent cells ending in a sheep cell. The second-to-last cell in such a path must be a neighbor of that sheep. If that neighbor is a dog or a wall, the path cannot exist. Therefore, the only way a path exists is if some neighbor of a sheep is either a wolf or an empty cell that remains unblocked. We explicitly forbid wolf adjacency and convert all empty neighbors into dogs, so no valid final step into a sheep remains possible. This invariant holds for all sheep simultaneously because the blocking is done globally.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    R, C = map(int, input().split())
    grid = [list(input().strip()) for _ in range(R)]
    
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]
    
    for i in range(R):
        for j in range(C):
            if grid[i][j] == 'S':
                for di, dj in dirs:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < R and 0 <= nj < C:
                        if grid[ni][nj] == 'W':
                            print("No")
                            return
                        if grid[ni][nj] == '.':
                            grid[ni][nj] = 'D'
    
    print("Yes")
    for row in grid:
        print("".join(row))

if __name__ == "__main__":
    solve()
```

The implementation directly follows the grid scan described earlier. The key detail is that modifications are done in place while scanning, but this is safe because turning empty cells into dogs only strengthens protection and never introduces a new path for wolves.

The boundary checks ensure we do not access invalid indices. The early exit on detecting an adjacent wolf avoids unnecessary processing once impossibility is established.

## Worked Examples

### Example 1

Input:

```
3 3
S.W
...
W.S
```

We scan each sheep and check neighbors.

| Cell (i,j) | Type | Neighbor check result | Action |
| --- | --- | --- | --- |
| (0,0) | S | right is W | impossible detected |

Since a wolf is adjacent to a sheep, we immediately output No. This confirms that adjacency is a fatal configuration.

### Example 2

Input:

```
3 3
S..
...
..W
```

We process the sheep at (0,0).

| Cell (i,j) | Type | Neighbor scan | Grid change |
| --- | --- | --- | --- |
| (0,0) | S | (1,0),(0,1) are '.' | place D at (1,0),(0,1) |

Final grid becomes:

```
SD.
D..
..W
```

No sheep is adjacent to a wolf after blocking, so output is Yes. This demonstrates that local blocking fully separates components.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(RC) | Each cell is visited once, and each neighbor check is constant work |
| Space | O(RC) | Grid storage plus minor overhead |

The grid size is at most 250,000 cells, and each cell contributes at most four neighbor checks. This comfortably fits within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample 1 (conceptual form)
assert run("""3 3
S.W
...
W.S
""") == "No"

# simple valid case
assert run("""2 2
S.
.W
""") == "Yes\nSD\nDW"

# no wolves
assert run("""2 3
S..
...
""") != ""

# fully empty grid
assert run("""2 2
..
..
""") == "Yes\n..\n.."
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| S.W / W.S | No | immediate adjacency failure |
| S. / .W | grid output | basic blocking correctness |
| no wolves | Yes | trivial safe case |
| empty grid | Yes | degenerate case handling |

## Edge Cases

A direct wolf-sheep adjacency is the most critical failure mode. For an input like:

```
2 2
SW
..
```

the algorithm inspects cell (0,0), sees a sheep, and immediately finds a wolf to its right. It returns No before any modification. This ensures we never incorrectly attempt to "repair" an impossible configuration.

A second case is when multiple sheep share a boundary cell. In a grid like:

```
3 3
S.S
...
W.W
```

the middle row empty cells adjacent to both sheep are converted into dogs during processing of each sheep. Even though the same cell may be considered multiple times, reassigning '.' to 'D' is idempotent, so the final grid remains consistent and fully blocked.
