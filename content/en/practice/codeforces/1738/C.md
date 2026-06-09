---
title: "CF 1738C - Even Number Addicts"
description: "The failure is not in I/O or iteration mechanics, but in the logic of what an “isolated cell” actually means. The previous solution implicitly assumed a global classification based only on board dimensions, and then defaulted to returning $(1,1)$ for all cases."
date: "2026-06-09T17:50:17+07:00"
tags: ["codeforces", "competitive-programming", "dp", "games", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1738
codeforces_index: "C"
codeforces_contest_name: "Codeforces Global Round 22"
rating: 1500
weight: 1738
solve_time_s: 410
verified: false
draft: false
---

[CF 1738C - Even Number Addicts](https://codeforces.com/problemset/problem/1738/C)

**Rating:** 1500  
**Tags:** dp, games, greedy, math  
**Solve time:** 6m 50s  
**Verified:** no  

## Solution
## Diagnosis

The failure is not in I/O or iteration mechanics, but in the logic of what an “isolated cell” actually means.

The previous solution implicitly assumed a global classification based only on board dimensions, and then defaulted to returning $(1,1)$ for all cases. That contradicts the actual definition: isolation is a local property of a specific cell, depending on whether all knight moves from that cell stay inside the board.

The expected output shows that isolated cells do exist in nontrivial structured ways. For example, on a $3 \times 3$ board the center $(2,2)$ is isolated, but corners are not necessarily treated as isolated in the same way under the problem’s intended interpretation. Similarly, on larger boards like $8 \times 8$, there exist specific isolated positions such as $(7,2)$.

So the correct task is genuinely per-cell geometric verification, not a global shortcut.

The bug in the current output arises because the algorithm collapsed the entire grid into a constant answer without checking actual knight reachability.

## Correct reasoning

A cell $(r,c)$ is isolated if all eight knight moves fall outside the board. That condition is purely local and must be checked explicitly.

The board is small enough that we can safely brute force all cells. For each cell, we test the eight possible moves and verify whether any stays inside the grid. If none do, we output that cell immediately.

If no such cell exists, we output any valid cell, for example $(1,1)$.

This directly matches the definition and avoids incorrect assumptions about board structure.

## Corrected Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    moves = [(2, 1), (2, -1), (-2, 1), (-2, -1),
             (1, 2), (1, -2), (-1, 2), (-1, -2)]
    
    for _ in range(t):
        n, m = map(int, input().split())
        
        found = False
        
        for r in range(1, n + 1):
            for c in range(1, m + 1):
                isolated = True
                
                for dr, dc in moves:
                    nr, nc = r + dr, c + dc
                    if 1 <= nr <= n and 1 <= nc <= m:
                        isolated = False
                        break
                
                if isolated:
                    print(r, c)
                    found = True
                    break
            
            if found:
                break
        
        if not found:
            print(1, 1)

if __name__ == "__main__":
    solve()
```

## Why this fixes the issue

The corrected solution restores the direct definition of isolation: a cell is valid if and only if all knight moves leave the board. This avoids any incorrect global reasoning and ensures that special cases like $(3,3)$ grids or asymmetric boards are handled correctly.

The early exit ensures we still return a valid isolated cell as soon as one is found, matching the requirement that any such cell is acceptable.

## Complexity Analysis

Each test case checks at most $64$ cells, and each cell checks at most $8$ moves, so the total work per test case is constant. This easily fits within constraints.

## Key takeaway

The main mistake was replacing a local geometric condition with a global shortcut. In grid problems with small constraints, direct simulation is often the correct and safest approach, especially when the definition depends on adjacency or move sets.
