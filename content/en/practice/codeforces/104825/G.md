---
title: "CF 104825G - War"
description: "We are given a grid where each cell is either empty or contains a single enemy unit. Empty cells and the area outside the grid are already controlled by us. The grid starts with all enemy cells still alive, and the goal is to eliminate every enemy cell."
date: "2026-06-28T12:32:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104825
codeforces_index: "G"
codeforces_contest_name: "The 17-th BIT Campus Programming Contest - Onsite Round"
rating: 0
weight: 104825
solve_time_s: 48
verified: true
draft: false
---

[CF 104825G - War](https://codeforces.com/problemset/problem/104825/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a grid where each cell is either empty or contains a single enemy unit. Empty cells and the area outside the grid are already controlled by us. The grid starts with all enemy cells still alive, and the goal is to eliminate every enemy cell.

At any moment, we are only allowed to attack an enemy cell that is adjacent to at least one friendly cell, where friendliness comes from either a zero cell in the grid or the outside border. When we attack such a cell, we pay a cost that depends on the structure of the remaining enemy configuration at that moment: the cost is one unit for the cell itself plus an additional unit for each of its four-directional neighbors that still contains an enemy at the time of removal. After paying the cost, that cell becomes friendly.

The task is to choose an order of removing all enemy cells so that the total cost is minimized.

The constraints allow grids up to size 1000 by 1000, so up to one million cells. Any solution that tries to simulate the process step by step while recomputing neighbor counts dynamically for each removal would be too slow. Even a linear-time per removal approach would lead to roughly $10^{12}$ operations in the worst case, which is not feasible.

A subtle point is that the cost depends on the current state of the grid, not the initial one. This makes it tempting to think that a greedy ordering or simulation is required. Another pitfall is assuming that removing cells in BFS or perimeter order changes the contribution of edges in a complicated way, when in fact the cost has a hidden additivity.

Edge cases are mostly about structure:

If all enemy cells are isolated, for example a checkerboard-like pattern of single ones, then every removal costs exactly one, since no cell ever has an enemy neighbor. The answer equals the number of ones.

If all cells are enemies in a fully filled $n \times m$ grid, naive intuition might suggest the cost depends heavily on removal order, but in reality the structure forces every adjacent pair to contribute exactly once regardless of the sequence.

## Approaches

A brute-force approach would explicitly simulate all valid removal orders. At each step we would identify all currently removable enemy cells, try removing each one, and track the resulting cost recursively or via backtracking. This correctly models the problem because it follows the exact rule definition, but the branching factor is large and the number of permutations of removals is $(nm)!$, which is astronomically large even for tiny grids. Even if we prune by only considering valid frontier cells, the state space remains exponential.

The key observation is that the cost function is local and decomposes over cells and adjacency relationships. Each cell always contributes a base cost of one when it is removed. The additional cost comes from counting how many of its neighbors are still enemies at that time. Instead of tracking time evolution, we can reinterpret each adjacency between two enemy cells as being charged exactly once, when the later of the two cells in the removal order is processed.

This transforms the problem from a dynamic process into a static counting problem: each enemy cell contributes one, and each adjacent pair of enemy cells contributes one more.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | O(nm) | Too slow |
| Counting Cells and Adjacencies | O(nm) | O(nm) | Accepted |

## Algorithm Walkthrough

We avoid simulating removals entirely and instead compute contributions directly from the initial grid.

1. First, scan the entire grid and count how many cells contain an enemy. This gives the base cost contribution because every enemy cell is removed exactly once and always pays at least one unit.
2. Next, inspect each enemy cell and check its right and down neighbors only. For every pair of adjacent enemy cells, we count one additional cost. We only check right and down to avoid double counting, since each adjacency is undirected.
3. Sum the base count and the adjacency count to obtain the final answer.

The reason we only consider right and down directions is that every adjacency between two enemy cells has exactly two endpoints, and checking both sides would count the same pair twice.

### Why it works

Think of the removal order as arbitrary but fixed. Every cell contributes its base cost exactly once. Now consider any pair of adjacent enemy cells u and v. One of them is removed first. When that happens, the other cell is still an enemy, so it contributes exactly one extra cost to the removal of the first. When the second cell is removed, the first is already gone and contributes nothing. So every adjacent pair contributes exactly one unit total, independent of ordering. This makes the total cost equal to the number of enemy cells plus the number of adjacent enemy pairs.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
g = [list(map(int, input().split())) for _ in range(n)]

ones = 0
edges = 0

for i in range(n):
    for j in range(m):
        if g[i][j] == 1:
            ones += 1
            if i + 1 < n and g[i + 1][j] == 1:
                edges += 1
            if j + 1 < m and g[i][j + 1] == 1:
                edges += 1

print(ones + edges)
```

The code directly implements the decomposition of the answer into node contributions and edge contributions. The nested loops ensure every cell is visited once. The checks `(i + 1, j)` and `(i, j + 1)` enforce unique counting of adjacency pairs. Boundary conditions are naturally handled by index checks, so no extra padding or sentinel grid is required.

## Worked Examples

Consider the sample grid:

```
0 0 0 0 0
0 0 0 1 0
0 1 1 1 0
0 0 1 0 0
0 0 0 0 0
```

We track only enemy cells and their right/down adjacencies.

| Step | Cell | Is enemy | New ones | New edges |
| --- | --- | --- | --- | --- |
| scan | (2,3) | yes | +1 | +1 (to (2,4)) |
| scan | (3,2) | yes | +1 | +1 (to (3,3)) |
| scan | (3,3) | yes | +1 | +1 (to (3,4)) +1 (to (4,3)) |
| scan | (3,4) | yes | +1 | 0 |
| scan | (4,3) | yes | +1 | 0 |

This gives a total of 5 enemy cells and 4 adjacency pairs, resulting in 9.

This trace shows that the answer is entirely determined by static structure. The dynamic “attack order” never appears, yet the result already matches any valid optimal sequence.

Now consider a fully isolated configuration:

```
1 0
0 1
```

| Cell | Ones | Edges |
| --- | --- | --- |
| (1,1) | +1 | 0 |
| (2,2) | +1 | 0 |

Total cost is 2, confirming that isolated cells contribute only their base cost.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Each cell is visited once and checked in constant time |
| Space | O(1) | Only counters are used beyond input storage |

The solution comfortably fits within limits because a single pass over a $10^6$ grid performs only constant work per cell, which is well within typical 1-second constraints in Python when implemented with fast I/O.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    g = [list(map(int, input().split())) for _ in range(n)]

    ones = 0
    edges = 0

    for i in range(n):
        for j in range(m):
            if g[i][j] == 1:
                ones += 1
                if i + 1 < n and g[i + 1][j] == 1:
                    edges += 1
                if j + 1 < m and g[i][j + 1] == 1:
                    edges += 1

    return str(ones + edges)

def run(inp: str) -> str:
    return solve(inp)

# provided sample
assert run("""5 5
0 0 0 0 0
0 0 0 1 0
0 1 1 1 0
0 0 1 0 0
0 0 0 0 0
""") == "9"

# single cell
assert run("""1 1
1
""") == "1"

# no enemies
assert run("""2 3
0 0 0
0 0 0
""") == "0"

# all enemies 2x2
assert run("""2 2
1 1
1 1
""") == "8"

# checkerboard
assert run("""3 3
1 0 1
0 1 0
1 0 1
""") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 single | 1 | minimal base case |
| empty grid | 0 | no contribution handling |
| full 2x2 | 8 | dense adjacency counting |
| checkerboard | 5 | isolated components and no double counting |

## Edge Cases

A completely empty grid is handled naturally because the scan never increments either counter, producing zero without special logic.

A single enemy cell also behaves correctly since it contributes one to the base count and has no neighbors to generate adjacency contributions. The algorithm does not attempt to access invalid indices because all neighbor checks are guarded.

A fully filled grid is where correctness is most non-obvious. For a $n \times m$ block, every internal adjacency is counted exactly once via right and down scanning, matching the idea that each edge contributes a single unit of cost regardless of removal order.
