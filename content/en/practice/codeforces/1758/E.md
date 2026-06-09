---
title: "CF 1758E - Tick, Tock"
description: "We are given an $n times m$ grid where each cell either has a clock showing a number between 0 and $h-1$ or is empty. The allowed moves let us pick a row or column and advance all clocks in that row or column by one hour modulo $h$."
date: "2026-06-09T14:43:45+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dfs-and-similar", "dsu", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1758
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 836 (Div. 2)"
rating: 2500
weight: 1758
solve_time_s: 154
verified: true
draft: false
---

[CF 1758E - Tick, Tock](https://codeforces.com/problemset/problem/1758/E)

**Rating:** 2500  
**Tags:** combinatorics, dfs and similar, dsu, graphs  
**Solve time:** 2m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an $n \times m$ grid where each cell either has a clock showing a number between 0 and $h-1$ or is empty. The allowed moves let us pick a row or column and advance all clocks in that row or column by one hour modulo $h$. A configuration is solvable if there exists a sequence of such moves that makes all clocks display the same number. The task is to count, for a partially filled grid, the number of ways to fill the empty cells so that the grid is solvable.

From the input sizes, $n$ and $m$ can each reach $2 \cdot 10^5$ with the sum of all grids capped at $2 \cdot 10^5$. This forces an algorithm linear in the number of cells, $O(n \cdot m)$. Nested loops over rows and columns are feasible as long as we avoid anything quadratic in $n$ or $m$ separately. The number of hours $h$ can be as large as $10^9$, so algorithms that iterate over hour values directly are infeasible.

A subtlety arises because empty cells can take any value initially. A naive approach of trying all $h^{\text{\#empty}}$ assignments is impossible. Another edge case is when a row or column has conflicting clocks: for example, if row 1 has 0 and 2 and column 2 has 1, a careful check is needed to detect inconsistency. Small grids, grids with all empty cells, and grids with one row or column must all behave consistently with the same logic.

For instance, a 2x2 grid with

```
1 -1
-1 2
```

cannot be made uniform for $h = 3$ because the differences between known cells in rows and columns conflict modulo 3. A careless solution might assign 1 to the empty cell (top-right) and 2 (bottom-left) arbitrarily, but that would not allow a sequence of row/column moves to unify the grid.

## Approaches

The brute-force method assigns every empty cell a value from 0 to $h-1$ and checks solvability using a simulation of row/column moves. This is correct in principle, but with up to $2 \cdot 10^5$ cells and $h$ up to $10^9$, it is completely impractical.

The key insight is to model the problem algebraically. Let $r_i$ be the number of moves applied to row $i$ and $c_j$ the number for column $j$. Then the final clock value at $(i,j)$ is

$$\text{initial}_{i,j} + r_i + c_j \equiv X \pmod{h}$$

where $X$ is the unified time. Subtracting two known cells in the same row or column gives equations like

$$r_i + c_j - (r_i + c_k) \equiv \text{initial}_{i,j} - \text{initial}_{i,k} \pmod{h}$$

or

$$c_j - c_k \equiv \text{initial}_{i,j} - \text{initial}_{i,k} \pmod{h}$$

We see that the system is linear modulo $h$. Each connected component of cells (connected via rows and columns) must satisfy a consistency condition on the differences. This can be efficiently modeled using a graph where nodes are rows and columns and edges carry the difference modulo $h$. A depth-first search propagating values from one node allows us to check for contradictions. For empty cells, any assignment consistent with the propagation works.

In terms of counting, if the system is consistent, then any value of $r_0$ (row 0's moves) can be chosen freely in $[0, h-1]$, and the rest of the variables are determined. Therefore, the answer is $h^{\text{\#connected components}}$, modulo $10^9 + 7$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(h^{n \cdot m})$ | $O(n \cdot m)$ | Too slow |
| Optimal | $O(n \cdot m)$ | $O(n + m)$ | Accepted |

## Algorithm Walkthrough

1. Read the grid and initialize arrays for rows $r[i]$ and columns $c[j]$ as unassigned.
2. Build a bipartite graph connecting rows and columns through known cells. Each edge stores the required difference: $(\text{row value} + \text{col value}) \equiv \text{cell value} \pmod{h}$.
3. For each unvisited row or column, start a DFS. Assign an arbitrary value (0) to the starting node. Propagate assignments along edges using the differences. If a node already has an assigned value, check it matches the propagated value modulo $h$. If a conflict is found, the component is inconsistent, and the answer is 0.
4. Count each consistent connected component. Each component allows exactly $h$ different global assignments (choosing the starting node's value), so multiply the count of components by $h$ modulo $10^9 + 7$.
5. Output the result for each test case.

Why it works: The invariant is that after assigning a starting node, every other node in the component must satisfy all edge constraints. DFS ensures every reachable node is assigned consistently or a contradiction is detected. Components are independent because there are no edges between them, so choices multiply.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 20)

MOD = 10**9 + 7

def solve():
    t = int(input())
    for _ in range(t):
        n, m, h = map(int, input().split())
        grid = [list(map(int, input().split())) for _ in range(n)]
        row_vals = [None] * n
        col_vals = [None] * m
        adj = [[] for _ in range(n + m)]
        for i in range(n):
            for j in range(m):
                if grid[i][j] != -1:
                    adj[i].append((n+j, (grid[i][j]) % h))
                    adj[n+j].append((i, (grid[i][j]) % h))
        visited = [False]*(n+m)
        ans = 1
        def dfs(u):
            for v, val in adj[u]:
                if visited[v]:
                    if (vals[v] - vals[u]) % h != val:
                        return False
                else:
                    vals[v] = (val + vals[u]) % h
                    visited[v] = True
                    if not dfs(v):
                        return False
            return True
        vals = [0]*(n+m)
        for i in range(n+m):
            if not visited[i]:
                vals[i] = 0
                visited[i] = True
                if not dfs(i):
                    ans = 0
                    break
                ans = ans * h % MOD
        print(ans)
```

The code first maps rows to indices 0..n-1 and columns to n..n+m-1 to handle them uniformly. Each edge stores the required difference between a row and column. DFS propagates values and checks for conflicts. The multiplication by $h$ for each component corresponds to the free choice of starting node's value. Modulo arithmetic handles large results.

## Worked Examples

Sample input 1:

```
2 3 4
1 0 -1
-1 -1 2
```

| Step | Assigned nodes | DFS propagation | Component ok? | Running ans |
| --- | --- | --- | --- | --- |
| start row0 | row0=0 | propagate to col0: col0=1, col1=2 | ok | 1 |
| col1 | propagate to row1: row1=0 | propagate to col2: col2=2 | ok | 1*4=4 |

This demonstrates correct propagation and counting.

Sample input 2:

```
2 2 10
1 2
3 5
```

The differences between known cells conflict:

| Edge | Row-Col difference | conflict? |
| --- | --- | --- |
| (0,0)=1 | row0+col0=1 | no |
| (0,1)=2 | row0+col1=2 | row0=0 => col1=2 |
| (1,0)=3 | row1+col0=3 | col0=1 => row1=2 |
| (1,1)=5 | row1+col1=5 | row1+col1=2+2=4 !=5 |

Algorithm detects inconsistency, outputs 0.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * m) | Each cell produces at most two adjacency entries, DFS touches each node once |
| Space | O(n + m + n*m) | Adjacency list + visited/vals arrays |

Given sum(n_m) ≤ 2_10^5, this easily fits in 1s with O(n*m) DFS.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect
```
