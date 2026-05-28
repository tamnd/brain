---
title: "CF 132B - Piet"
description: "We are asked to simulate a simplified Piet interpreter on a small rectangular grid. Each cell is a pixel with a color between 0 and 9, where 0 is black and other digits are colored blocks."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 132
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 96 (Div. 1)"
rating: 2100
weight: 132
solve_time_s: 116
verified: true
draft: false
---

[CF 132B - Piet](https://codeforces.com/problemset/problem/132/B)

**Rating:** 2100  
**Tags:** implementation  
**Solve time:** 1m 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to simulate a simplified Piet interpreter on a small rectangular grid. Each cell is a pixel with a color between 0 and 9, where 0 is black and other digits are colored blocks. Colored blocks are always rectangular and connected, so every color cluster forms a perfect rectangle. Black pixels can be arbitrary shapes. The program begins with the instruction pointer (IP) at the top-left colored block. The IP is defined by three components: the current block (BP), a direction pointer (DP) which can point up, down, left, or right, and a block chooser (CP) which modifies the movement when the IP encounters edges or black pixels.

At each step, the interpreter moves the BP in the DP direction to the next block if possible, otherwise, it updates CP and possibly rotates DP. The task is to determine the color of the block where BP lands after `n` steps. The grid is at most 50×50 pixels, but `n` can be up to 50 million, which is far too large for naive step-by-step simulation.

The non-obvious edge cases include single-row or single-column blocks, sequences of black pixels that force DP and CP to rotate repeatedly, and loops where the BP revisits the same block multiple times. For example, a grid:

```
12
34
```

with `n = 10` cycles through the blocks in a predictable pattern. A naive simulation would attempt all 10 steps, but in larger `n`, this would be impossible.

## Approaches

The brute-force approach is straightforward: start from the initial block, iterate step by step, applying the rules for DP and CP updates, and track the current block after each move. This works because each step is deterministic and the rules fully specify the new state. However, with `n` up to 50 million, this approach performs too many operations; each step requires O(1) work, so the total complexity is O(n), which is too slow given the time limit of 2 seconds.

The key insight for a faster solution is to treat the IP transitions as a finite deterministic state machine. Each state is defined by the current block, DP, and CP. Because the number of blocks is limited (at most 2500 for a 50×50 grid) and there are 8 possible DP/CP configurations (4 DP directions × 2 CP directions), the total number of states is at most 20,000. By simulating the steps until a state repeats, we detect cycles. Once a cycle is found, we can compute the final block after `n` steps using modular arithmetic rather than iterating each step.

The brute-force works for small `n` or small grids but fails when `n` is large. The observation that there are finitely many states allows us to reduce the simulation to at most one cycle detection followed by a modulo computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Too slow for large n |
| Cycle Detection | O(m × w × 8) | O(m × w × 8) | Accepted |

## Algorithm Walkthrough

1. Preprocess the grid to identify all colored blocks. For each block, store its top-left and bottom-right coordinates. This allows constant-time checks of the block edges when moving in any direction.
2. Define DP and CP directions as vectors: DP can be up `(−1,0)`, down `(1,0)`, left `(0,−1)`, right `(0,1)`, and CP can be left or right relative to DP. This makes computing the next pixel along the edge straightforward.
3. Initialize the IP at the top-left block with DP pointing right and CP pointing left. Encode each state as a tuple `(block_id, dp, cp)`.
4. Simulate the program step by step while recording visited states in a dictionary mapping `(block_id, dp, cp)` to the step number. For each step, determine the next block according to DP and CP rules.
5. If a state repeats, detect the cycle length. Let `start` be the step where the cycle begins and `length` the number of steps in the cycle. Compute the final step modulo the cycle length and return the block at that step.
6. If no cycle is detected within the total number of steps (unlikely due to finite states), continue normal simulation until step `n`.

Why it works: The finite number of blocks and orientations guarantees that the simulation must eventually repeat a state. Because the Piet interpreter is deterministic, entering the same state again always produces the same sequence of blocks. By reducing large `n` to a step inside the detected cycle, we achieve correctness without simulating every step.

## Python Solution

```python
import sys
input = sys.stdin.readline

# direction vectors: 0=right, 1=down, 2=left, 3=up
dp_moves = [(0,1), (1,0), (0,-1), (-1,0)]

# CP left/right: -1 for left, +1 for right relative to DP
cp_changes = {'L': -1, 'R': 1}

def rotate_dp(dp):
    return (dp + 1) % 4

def parse_grid(m):
    grid = []
    for _ in range(m):
        row = list(map(int, list(input().strip())))
        grid.append(row)
    return grid

def find_blocks(grid):
    m, w = len(grid), len(grid[0])
    block_id = 0
    block_map = [[-1]*w for _ in range(m)]
    blocks = []
    for i in range(m):
        for j in range(w):
            color = grid[i][j]
            if color == 0 or block_map[i][j] != -1:
                continue
            # expand rectangle
            x0, y0 = i, j
            x1, y1 = i, j
            while x1+1 < m and all(grid[x1+1][y] == color for y in range(y0, y1+1)):
                x1 += 1
            while y1+1 < w and all(grid[x][y1+1] == color for x in range(x0, x1+1)):
                y1 += 1
            # mark cells
            for x in range(x0, x1+1):
                for y in range(y0, y1+1):
                    block_map[x][y] = block_id
            blocks.append((x0, y0, x1, y1, color))
            block_id += 1
    return block_map, blocks

def next_block(block_map, blocks, block_idx, dp, cp):
    x0, y0, x1, y1, color = blocks[block_idx]
    dx, dy = dp_moves[dp]
    # find furthest edge in DP
    if dp == 0:  # right
        edge_cells = [(i, y1) for i in range(x0, x1+1)]
    elif dp == 1:  # down
        edge_cells = [(x1, j) for j in range(y0, y1+1)]
    elif dp == 2:  # left
        edge_cells = [(i, y0) for i in range(x0, x1+1)]
    else:  # up
        edge_cells = [(x0, j) for j in range(y0, y1+1)]
    # select cell in CP direction
    if cp == 'L':
        if dp % 2 == 0:
            next_cell = min(edge_cells, key=lambda x: x[0] if dp==0 else x[1])
        else:
            next_cell = min(edge_cells, key=lambda x: x[1] if dp==1 else x[0])
    else:
        if dp % 2 == 0:
            next_cell = max(edge_cells, key=lambda x: x[0] if dp==0 else x[1])
        else:
            next_cell = max(edge_cells, key=lambda x: x[1] if dp==1 else x[0])
    nx, ny = next_cell[0]+dx, next_cell[1]+dy
    m, w = len(block_map), len(block_map[0])
    if 0 <= nx < m and 0 <= ny < w and block_map[nx][ny] != -1:
        return block_map[nx][ny], dp, cp
    else:
        if cp == 'L':
            return block_idx, dp, 'R'
        else:
            return block_idx, rotate_dp(dp), 'L'

def main():
    m, n = map(int, input().split())
    grid = parse_grid(m)
    block_map, blocks = find_blocks(grid)
    dp, cp = 0, 'L'
    block_idx = block_map[0][0]

    visited = {}
    states = []
    step = 0
    while step < n:
        key = (block_idx, dp, cp)
        if key in visited:
            cycle_start = visited[key]
            cycle_len = step - cycle_start
            remaining = (n - step) % cycle_len
            block_idx, dp, cp = states[cycle_start + remaining]
            break
        visited[key] = step
        states.append((block_idx, dp, cp))
        block_idx, dp, cp = next_block(block_map, blocks, block_idx, dp, cp)
        step += 1
    print(blocks[block_idx][4])

if __name__ == "__main__":
    main()
``
```
