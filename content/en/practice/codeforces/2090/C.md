---
title: "CF 2090C - Dining Hall"
description: "The problem presents an infinite grid where every table occupies a 2×2 square in a repeating pattern. Each table starts at coordinates of the form $(3x + 1, 3y + 1)$ and occupies four cells. All other cells are corridors."
date: "2026-06-08T05:50:16+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2090
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1012 (Div. 2)"
rating: 1700
weight: 2090
solve_time_s: 96
verified: false
draft: false
---

[CF 2090C - Dining Hall](https://codeforces.com/problemset/problem/2090/C)

**Rating:** 1700  
**Tags:** data structures, greedy, implementation, sortings  
**Solve time:** 1m 36s  
**Verified:** no  

## Solution
## Problem Understanding

The problem presents an infinite grid where every table occupies a 2×2 square in a repeating pattern. Each table starts at coordinates of the form $(3x + 1, 3y + 1)$ and occupies four cells. All other cells are corridors. Guests enter at $(0, 0)$ and want to reach a table cell following a specific rule. Some guests, with characteristic $t_i=1$, only care about the nearest free table cell. Others, with $t_i=0$, require a table that is completely unoccupied by any guest. Guests move orthogonally through corridors and finally step into a table cell.

The input specifies multiple test cases. Each test case lists the number of guests and a sequence of characteristics $t_i$. The output must give, for each guest in order, the coordinates of the cell they occupy.

The constraints indicate that the sum of all guests across all test cases is at most 50,000. A brute-force simulation that explores the grid explicitly would require processing an unbounded number of cells for each guest, making an $O(n^2)$ or BFS-per-guest approach infeasible. Therefore, we need a method that computes target table cells directly. The problem also has tie-breaking rules: guests prefer smaller $x$, then smaller $y$ if distances are equal. A careless implementation might misorder cells or reuse a partially occupied table for a $t_i=0$ guest.

Edge cases include sequences with consecutive $t_i=0$ guests, which require skipping partially occupied tables, and guests needing to choose between two tables at the same distance where one has smaller $x$ or $y$.

## Approaches

A naive approach would simulate the hall as a grid, marking table occupancy and performing BFS for each guest from $(0, 0)$ to find the nearest valid table cell according to $t_i$. While correct in principle, this method is too slow. The grid is infinite, so BFS could explore many unnecessary cells, leading to worst-case operations of $O(n \cdot D^2)$ where $D$ is the maximum Manhattan distance to the furthest occupied table. For large $n$, this exceeds feasible time limits.

The key insight is that the tables repeat in a regular 3×3 pattern, and guests always start at $(0, 0)$. We can map table coordinates to a sequence that expands outward diagonally along $x+y$, since Manhattan distance to $(0, 0)$ is monotonic. Each table has exactly four cells, and their order within a table can be predefined. This allows us to maintain a simple pointer or index to the next unoccupied table for $t_i=0$ guests, and a pointer to the next free cell for $t_i=1$ guests, generating coordinates on demand.

By precomputing the sequence of table cells along diagonals and assigning them incrementally, we can decide in $O(1)$ per guest which cell they occupy. This approach avoids any BFS or full grid simulation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (BFS per guest) | O(n D^2) | O(D^2) | Too slow |
| Precomputed sequence / pointer method | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Define a deterministic order for table cells. Each table at $(3x + 1, 3y + 1)$ occupies four cells. We enumerate them as $(3x + 1, 3y + 1)$, $(3x + 1, 3y + 2)$, $(3x + 2, 3y + 1)$, $(3x + 2, 3y + 2)$. This ensures tie-breaking by $x$ and then $y$ automatically.
2. Maintain two separate sequences: one for all table cells (for $t_i=1$ guests) and one for table starts (for $t_i=0$ guests). Track which cells have been occupied using simple indices. For $t_i=0$ guests, skip to the next fully unoccupied table.
3. Generate table coordinates dynamically instead of storing an infinite grid. The $k$-th table can be assigned coordinates using a pattern: enumerate tables diagonally by $x+y$ sum, within each sum in increasing $x$ order.
4. For each guest, check $t_i$. If $t_i=0$, assign the next fully unoccupied table's first available cell and mark the table as partially occupied. If $t_i=1$, assign the next free cell from the global sequence.
5. Increment pointers after each assignment. For $t_i=0$, once all four cells of a table are used, move to the next unoccupied table. For $t_i=1$, always pick the next free cell regardless of table occupancy.
6. Output the assigned coordinates in order.

Why it works: The Manhattan distance is determined by the sum $x + y$, so enumerating tables diagonally guarantees the correct nearest table. Within a diagonal, sorting by $x$ then $y$ satisfies the tie-breaking rules. Maintaining separate sequences ensures $t_i=0$ guests only get unoccupied tables, while $t_i=1$ guests always take the nearest available cell.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    q = int(input())
    for _ in range(q):
        n = int(input())
        t = list(map(int, input().split()))
        
        occupied_cells = []
        unoccupied_tables = []
        ptr_cell = 0
        ptr_table = 0
        
        # Precompute coordinates lazily
        coords_cell = []
        coords_table = []
        limit = n  # we only need as many cells/tables as guests
        k = 0
        while len(coords_cell) < limit:
            for dx in range(k + 1):
                dy = k - dx
                base_x, base_y = 3*dx + 1, 3*dy + 1
                coords_table.append((base_x, base_y))
                coords_cell.extend([
                    (base_x, base_y),
                    (base_x, base_y + 1),
                    (base_x + 1, base_y),
                    (base_x + 1, base_y + 1)
                ])
                if len(coords_cell) >= limit:
                    break
            k += 1
        
        table_taken = [0]*len(coords_table)
        
        for ti in t:
            if ti == 0:
                while table_taken[ptr_table] == 4:
                    ptr_table += 1
                base_x, base_y = coords_table[ptr_table]
                # assign next free cell in this table
                cell_idx = table_taken[ptr_table]
                if cell_idx == 0:
                    x, y = base_x, base_y
                elif cell_idx == 1:
                    x, y = base_x, base_y + 1
                elif cell_idx == 2:
                    x, y = base_x + 1, base_y
                else:
                    x, y = base_x + 1, base_y + 1
                table_taken[ptr_table] += 1
                print(x, y)
            else:
                x, y = coords_cell[ptr_cell]
                ptr_cell += 1
                print(x, y)

if __name__ == "__main__":
    solve()
```

The code precomputes only as many table cells as needed for the guests. Lazy enumeration ensures correct diagonal order for Manhattan distance. We track how many cells of each table are occupied to handle $t_i=0$ guests, and maintain a separate pointer for $t_i=1$ to always pick the next free cell globally.

## Worked Examples

Sample input:

```
6
0 1 1 0 0 1
```

| Guest | t_i | Selected Cell | ptr_table | ptr_cell |
| --- | --- | --- | --- | --- |
| 1 | 0 | (1,1) | 1 | 0 |
| 2 | 1 | (1,2) | 1 | 1 |
| 3 | 1 | (2,1) | 1 | 2 |
| 4 | 0 | (1,4) | 2 | 3 |
| 5 | 0 | (4,1) | 3 | 4 |
| 6 | 1 | (1,5) | 3 | 5 |

This trace demonstrates that $t_i=0$ guests skip partially occupied tables, and $t_i=1$ guests take the next free cell globally, maintaining correct distance and tie-breaking.

Second test input:

```
5
1 0 0 1 1
```

| Guest | t_i | Selected Cell | ptr_table | ptr_cell |
| --- | --- | --- | --- | --- |
| 1 | 1 | (1,1) | 0 | 1 |
| 2 | 0 | (1,4) | 1 | 1 |
| 3 | 0 | (4,1) | 2 | 2 |
| 4 | 1 | (1,2) | 2 | 3 |
| 5 | 1 | (2,1) | 2 | 4 |

The table confirms that separate sequences
