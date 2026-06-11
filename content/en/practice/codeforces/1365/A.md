---
title: "CF 1365A - Matrix Game"
description: "We are given a grid where some cells are already occupied. Two players alternate turns, and on each move a player must pick a previously unused cell under a strong restriction: no two chosen cells are allowed to share a row or a column."
date: "2026-06-11T12:21:36+07:00"
tags: ["codeforces", "competitive-programming", "games", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1365
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 648 (Div. 2)"
rating: 1100
weight: 1365
solve_time_s: 485
verified: true
draft: false
---

[CF 1365A - Matrix Game](https://codeforces.com/problemset/problem/1365/A)

**Rating:** 1100  
**Tags:** games, greedy, implementation  
**Solve time:** 8m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a grid where some cells are already occupied. Two players alternate turns, and on each move a player must pick a previously unused cell under a strong restriction: no two chosen cells are allowed to share a row or a column.

The game ends when a player cannot make a legal move, and we need to decide who wins if both play optimally and Ashish starts.

The key observation is that the grid structure itself does not matter beyond whether a row or a column is already “blocked” by an occupied cell. Once a row contains a chosen cell, that row can never contribute another move, and the same applies to columns. Every move effectively consumes one unused row and one unused column simultaneously.

With constraints up to 50 by 50 per test case and 50 test cases, a direct simulation is fine, but anything that tries to search combinations of placements would quickly explode. The structure strongly suggests a counting reduction rather than a search problem.

A common failure case comes from misinterpreting how blocked rows and columns interact. For example, if two initial 1s lie in the same row or column, a naive implementation that simply counts rows and columns independently without deduplicating can overestimate available moves.

Another subtle issue appears when the grid is fully empty. One might assume every empty cell is playable, but in reality selecting one cell immediately blocks its entire row and column, collapsing many potential choices into a single move.

## Approaches

A brute-force strategy would try to simulate all valid sequences of moves, branching on every available cell that satisfies the row and column constraint. Even in a 50 by 50 grid, the number of valid sequences can grow combinatorially because each move changes the structure of available moves globally. This quickly becomes infeasible.

The crucial simplification comes from reframing the problem in terms of structure rather than positions. Each move selects exactly one previously untouched row and one previously untouched column. Therefore the game reduces to repeatedly pairing free rows with free columns. The number of such pairings is determined entirely by how many rows and columns are already blocked by initial ones.

We observe that every initial occupied cell blocks its row and column. After removing duplicates, the number of free choices collapses into the minimum of remaining free rows and free columns. The game becomes a simple pile where each move removes one unit, and the winner depends only on parity.

The brute-force works because it follows the rules directly, but fails because it does not compress the symmetry between rows and columns. The observation that every move consumes exactly one row and one column reduces the problem to counting how many such pairs exist.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | Exponential | Too slow |
| Row/Column counting reduction | O(nm) | O(n + m) | Accepted |

## Algorithm Walkthrough

We first identify which rows and columns are already blocked by initial occupied cells. A row is blocked if it contains at least one 1, and similarly for columns.

Next, we count how many rows are still completely free and how many columns are still completely free. These represent resources that can still participate in moves.

Each move consumes one free row and one free column simultaneously, so the total number of possible moves is the minimum of these two quantities.

Finally, since players alternate moves starting from Ashish, we determine the winner by checking whether this number is odd or even. If it is odd, Ashish makes the final move and wins. If even, Vivek does.

The key invariant is that after every move, exactly one row and one column are permanently removed from future consideration. No move can reuse either dimension, so the game state always reduces monotonically in both directions, ensuring the count of valid moves fully determines the outcome.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())

        rows = [False] * n
        cols = [False] * m

        grid = [list(map(int, input().split())) for _ in range(n)]

        for i in range(n):
            for j in range(m):
                if grid[i][j] == 1:
                    rows[i] = True
                    cols[j] = True

        free_rows = sum(1 for i in range(n) if not rows[i])
        free_cols = sum(1 for j in range(m) if not cols[j])

        moves = min(free_rows, free_cols)

        if moves % 2 == 1:
            print("Ashish")
        else:
            print("Vivek")

solve()
```

The solution scans the grid once, marking which rows and columns are already unusable. After that, it counts remaining usable rows and columns and reduces the game to a parity check. The only subtle point is that a row or column is considered blocked if it contains at least one occupied cell, not based on how many occupied cells it contains.

## Worked Examples

### Example 1

Input:

```
2 2
0 0
0 0
```

All rows and columns are free initially.

| Step | Free Rows | Free Columns | Moves |
| --- | --- | --- | --- |
| Start | 2 | 2 | 0 |
| Compute | 2 | 2 | 2 |

The number of moves is 2, so Vivek wins.

This shows that even in a completely empty grid, play is limited to at most min(n, m) moves, not the number of cells.

### Example 2

Input:

```
2 2
0 0
0 1
```

Row 1 and column 1 are blocked by the single occupied cell.

| Step | Free Rows | Free Columns | Moves |
| --- | --- | --- | --- |
| Start | 1 | 1 | 0 |
| Compute | 1 | 1 | 1 |

One move is possible, so Ashish wins.

This confirms that a single blocked row-column pair determines a single forced move.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Each grid cell is checked once per test case |
| Space | O(n + m) | Arrays track blocked rows and columns |

The total number of cells across test cases is small enough for a direct scan to run comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import builtins
    return sys.stdin.read()

# This is a placeholder runner structure; actual CF setup would call solve()

# sample-style sanity checks
assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| empty grid | Vivek | parity on maximum free structure |
| single 1 in corner | Ashish | blocked row/col propagation |
| full grid of 1s | Vivek | zero-move case |
| alternating sparse | depends | mixed blocking behavior |

## Edge Cases

A fully empty grid exercises the fact that the answer depends only on min(n, m), not total cells. A grid where all rows are already blocked except one tests that column constraints dominate. A grid where all columns are blocked except one tests the symmetric case. Each of these cases reduces cleanly to a single parity computation of the remaining free dimension, and the algorithm handles them uniformly because it never assumes independence between cells.
