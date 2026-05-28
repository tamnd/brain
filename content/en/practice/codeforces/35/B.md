---
title: "CF 35B - Warehouse"
description: "We are asked to simulate a warehouse with a grid-like shelving system. Each shelf has m sections, and there are n shelve"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 35
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 35 (Div. 2)"
rating: 1700
weight: 35
solve_time_s: 81
verified: true
draft: false
---

[CF 35B - Warehouse](https://codeforces.com/problemset/problem/35/B)

**Rating:** 1700  
**Tags:** implementation  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to simulate a warehouse with a grid-like shelving system. Each shelf has `m` sections, and there are `n` shelves stacked from top to bottom. Every section can hold at most one box. We receive a sequence of operations: some add boxes to a given shelf and section, and others remove boxes by identifier. Boxes cannot overlap. If the intended section is full, the box is placed in the next available section to the right on the same shelf. If no sections remain, we continue to the next shelf below, starting from the leftmost section. If no sections are free across all shelves, the box is discarded.

For each removal operation, we must output the exact shelf and section the box occupied or `-1 -1` if it was not in the warehouse.

The constraints are small: `n` and `m` are at most 30, and the number of operations `k` is up to 2000. This allows a direct simulation. Each placement may, in the worst case, require scanning all `n * m` positions. That yields `2000 * 900 = 1.8 * 10^6` operations, which is acceptable under the 2-second limit. Non-obvious edge cases involve attempts to place boxes in full shelves or removing a box that was never inserted.

For example, if we try to place a box in section `(1, 2)` but it is full and the entire shelf 1 is full, the box should go to section `(2, 1)`. If all shelves are full, the box is ignored. A naive approach that forgets to continue on the next shelf would produce incorrect placement.

## Approaches

The brute-force approach is straightforward: maintain a 2D grid representing the warehouse. Each cell either stores the box identifier or is empty. For an insertion `+1 x y id`, attempt to place the box at `(x, y)`. If occupied, scan the remainder of the current row and then subsequent rows in order until a free cell is found or all shelves are exhausted. For a removal `-1 id`, search the entire grid to locate the box and clear its cell.

This is correct but inefficient for `-1` queries because each search could take `O(n*m)` time, resulting in `O(k * n * m)` overall. Given the constraints, this naive search would still work but is avoidable.

The key insight for an efficient solution is that every box has a unique identifier and we only need to answer removals efficiently. By maintaining a dictionary mapping box identifiers to their positions, we can retrieve positions in constant time. The placement logic still uses the grid but the removal operation no longer requires scanning. This reduces time spent on removals from `O(n*m)` to `O(1)` per query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k * n * m) | O(n*m) | Works but slow on upper bound |
| Optimal | O(k * n * m) | O(n*m + k) | Accepted |

## Algorithm Walkthrough

1. Initialize a 2D array `warehouse` of size `n x m` to store box identifiers or `None` for empty sections. Create a dictionary `positions` mapping box identifiers to their current `(shelf, section)` coordinates.
2. For each query, parse the operation. If it is `+1 x y id`, attempt to place the box starting at shelf `x-1` and section `y-1`. Check if the cell is empty. If so, place the box, store its coordinates in `positions`, and continue to the next query. If occupied, move right along the same shelf. If the end of the shelf is reached, move to the next shelf below, scanning from the leftmost section. Repeat until an empty section is found or all shelves are exhausted. If no space is found, ignore the box.
3. For `-1 id`, check if `id` exists in `positions`. If so, retrieve `(shelf, section)`, output 1-based indices, remove the entry from `positions`, and mark the cell in `warehouse` as empty. If not present, output `-1 -1`.
4. Repeat for all queries.

The reason this works is that the warehouse grid correctly represents the real-time occupancy, and the dictionary ensures constant-time retrieval for removals. The scanning order strictly follows the problem’s placement rules, guaranteeing correct positions.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m, k = map(int, input().split())
warehouse = [[None for _ in range(m)] for _ in range(n)]
positions = {}

for _ in range(k):
    parts = input().split()
    if parts[0] == '+1':
        x, y, box_id = int(parts[1]) - 1, int(parts[2]) - 1, parts[3]
        placed = False
        for i in range(x, n):
            start_j = y if i == x else 0
            for j in range(start_j, m):
                if warehouse[i][j] is None:
                    warehouse[i][j] = box_id
                    positions[box_id] = (i, j)
                    placed = True
                    break
            if placed:
                break
    else:
        box_id = parts[1]
        if box_id in positions:
            i, j = positions.pop(box_id)
            print(i + 1, j + 1)
            warehouse[i][j] = None
        else:
            print(-1, -1)
```

We maintain the grid for placement because scanning is simple and safe. The dictionary ensures removals are O(1). We carefully handle 0-based vs 1-based indices to match output expectations. We also reset the column scan when moving to a new shelf.

## Worked Examples

Sample 1 input:

```
2 2 9
+1 1 1 cola
+1 1 1 fanta
+1 1 1 sevenup
+1 1 1 whitekey
-1 cola
-1 fanta
-1 sevenup
-1 whitekey
-1 cola
```

| Step | Operation | Warehouse State | Positions | Output |
| --- | --- | --- | --- | --- |
| 1 | +1 1 1 cola | [[cola, None],[None,None]] | {'cola':(0,0)} |  |
| 2 | +1 1 1 fanta | [[cola, fanta],[None,None]] | {'cola':(0,0),'fanta':(0,1)} |  |
| 3 | +1 1 1 sevenup | [[cola,fanta],[sevenup,None]] | ... |  |
| 4 | +1 1 1 whitekey | [[cola,fanta],[sevenup,whitekey]] | ... |  |
| 5 | -1 cola | [[None,fanta],[sevenup,whitekey]] | {'fanta':(0,1),...} | 1 1 |
| 6 | -1 fanta | [[None,None],[sevenup,whitekey]] | {'sevenup':(1,0),'whitekey':(1,1)} | 1 2 |
| 7 | -1 sevenup | [[None,None],[None,whitekey]] | {'whitekey':(1,1)} | 2 1 |
| 8 | -1 whitekey | [[None,None],[None,None]] | {} | 2 2 |
| 9 | -1 cola | [[None,None],[None,None]] | {} | -1 -1 |

This trace confirms the placement order and dictionary lookups.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k * n * m) | Each placement may scan all sections in the worst case, removals are O(1). |
| Space | O(n*m + k) | Grid for warehouse + dictionary for up to k box identifiers. |

With `n, m <= 30` and `k <= 2000`, this is comfortably within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # call solution
    n, m, k = map(int, input().split())
    warehouse = [[None]*m for _ in range(n)]
    positions = {}
    for _ in range(k):
        parts = input().split()
        if parts[0] == '+1':
            x, y, box_id = int(parts[1]) - 1, int(parts[2]) - 1, parts[3]
            placed = False
            for i in range(x, n):
                start_j = y if i == x else 0
                for j in range(start_j, m):
                    if warehouse[i][j] is None:
                        warehouse[i][j] = box_id
                        positions[box_id] = (i,j)
                        placed = True
                        break
                if placed:
                    break
        else:
            box_id = parts[1]
            if box_id in positions:
                i,j = positions.pop(box_id)
                print(i+1,j+1)
                warehouse[i][j] = None
            else:
                print(-1,-1)
    return output.getvalue().strip()
```
