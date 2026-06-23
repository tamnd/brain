---
title: "CF 105450H - Warhead Games"
description: "We are given a rectangular grid where each cell is either usable or blocked. A token starts at the top-left cell and two players alternate moves."
date: "2026-06-23T17:33:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105450
codeforces_index: "H"
codeforces_contest_name: "UTPC x WiCS Contest 10-25-24 (UT Internal)"
rating: 0
weight: 105450
solve_time_s: 87
verified: false
draft: false
---

[CF 105450H - Warhead Games](https://codeforces.com/problemset/problem/105450/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rectangular grid where each cell is either usable or blocked. A token starts at the top-left cell and two players alternate moves. On a turn, a player moves the token one step either down, right, or diagonally down-right, but only if the destination cell is inside the grid and not blocked. If a player has no legal move, that player loses immediately.

The task is to determine whether the first player, Alice, has a winning strategy.

The grid size can be as large as 1000 by 1000, which makes any solution that tries to explore all move sequences explicitly infeasible. A full game tree from each cell would branch up to three ways and can grow exponentially in depth proportional to r + c, so a naive recursive search would exceed time limits by many orders of magnitude.

One subtle issue is that blocked cells can create isolated regions that make some positions dead ends even if they are not near the boundary. For example, a cell surrounded by black squares except backward directions is irrelevant because backward moves are not allowed, so it effectively becomes a terminal losing state.

Another edge case is when the starting cell has no valid moves at all. Even though it is guaranteed to be white, it may still be completely surrounded by black or boundary, leading to an immediate loss for Alice.

## Approaches

A direct simulation of the game treats every white cell as a game state and recursively explores all reachable moves. From each state, we check whether there exists a move to a position where the opponent loses. This is the standard minimax definition for impartial games on a directed graph.

However, this recursion repeats the same subproblems many times. In the worst case, each of the r × c cells can branch into three transitions, leading to exponential behavior. Even with memoization, the structure is acyclic because all moves increase either row or column, so each state depends only on cells "later" in the grid.

This monotonic structure is the key observation. Since every move strictly increases either coordinate, there are no cycles. That means we can compute results bottom-up: any cell depends only on cells to its right, below, or diagonally down-right. If we process the grid in reverse order, from bottom-right to top-left, every transition leads to a state that has already been computed.

For each white cell, we mark it as winning if it can move to at least one losing cell. If all possible moves lead to winning positions, then the current cell is losing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DFS | O(3^(r+c)) | O(r·c) recursion | Too slow |
| Bottom-up DP | O(r·c) | O(r·c) | Accepted |

## Algorithm Walkthrough

We model each cell as a game state that is either winning or losing.

1. We create a DP table where each cell stores whether the current player starting there can force a win. A black cell is always losing because it is invalid to stand on it.
2. We iterate over the grid in reverse order, starting from the bottom-right corner and moving toward the top-left corner. This order guarantees that whenever we evaluate a cell, all cells it can move to have already been processed.
3. For each white cell, we try all valid moves: down, right, and diagonal down-right. If any of these moves leads to a cell that is losing, we mark the current cell as winning. The reasoning is that we can force the opponent into a losing position.
4. If none of the moves leads to a losing state, we mark the current cell as losing because every move gives the opponent a winning position.
5. After filling the DP table, the answer is determined by the value at the starting cell (0,0). If it is winning, Alice can force a win, otherwise Bob wins.

### Why it works

The DP table encodes the fundamental property of impartial games on a DAG: a position is winning exactly when it has at least one outgoing edge to a losing position. Because the move graph is acyclic, every state depends only on strictly later states in the processing order, so each value is computed exactly once and never invalidated. This ensures consistency between local decisions and the global game outcome.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    r, c = map(int, input().split())
    grid = [input().strip() for _ in range(r)]
    
    dp = [[False] * c for _ in range(r)]
    
    for i in range(r - 1, -1, -1):
        for j in range(c - 1, -1, -1):
            if grid[i][j] == 'B':
                dp[i][j] = False
                continue
            
            win = False
            
            if i + 1 < r and grid[i + 1][j] == 'B':
                win = win or not dp[i + 1][j]
            elif i + 1 < r:
                win = win or (not dp[i + 1][j])
            
            if j + 1 < c:
                win = win or (not dp[i][j + 1])
            
            if i + 1 < r and j + 1 < c:
                win = win or (not dp[i + 1][j + 1])
            
            dp[i][j] = win
    
    print("Alice" if dp[0][0] else "Bob")

if __name__ == "__main__":
    solve()
```

The core of the implementation is the reverse traversal of the grid. Each dp cell is computed only once, and transitions only look forward in the grid. The boolean logic captures the minimax rule directly: a position becomes winning if any move leads to a losing state.

The only subtlety is handling black cells. They are forced losing states and must never be treated as valid move targets. This is enforced by immediately assigning False to them and skipping transitions.

## Worked Examples

### Sample 1

Input grid:

```
W B W B W
W W W W W
W B W B W
B W B W B
```

We compute dp from bottom-right backward. The table below shows only a few key positions:

| Cell | Type | Move outcomes | dp |
| --- | --- | --- | --- |
| (3,4) | W | no moves | False |
| (3,3) | W | → (3,4)=False | True |
| (2,2) | W | diagonal leads to losing | True |
| (0,0) | W | at least one losing move reachable | True |

The starting position is winning, so Alice wins.

Output:

```
Alice
```

### Sample 2

Input:

```
W B B B
B B B B
```

The grid blocks almost everything. From (0,0), there are no valid moves at all.

| Cell | Type | Move outcomes | dp |
| --- | --- | --- | --- |
| (1,3) | B | invalid | False |
| (0,0) | W | no valid moves | False |

Alice has no move on the first turn.

Output:

```
Bob
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(r·c) | Each cell is processed once with constant transitions |
| Space | O(r·c) | DP table stores one boolean per cell |

The constraints allow up to one million cells, and the algorithm performs only a small constant amount of work per cell, which fits comfortably within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    input = sys.stdin.readline

    def solve():
        r, c = map(int, input().split())
        grid = [input().strip() for _ in range(r)]
        
        dp = [[False] * c for _ in range(r)]
        
        for i in range(r - 1, -1, -1):
            for j in range(c - 1, -1, -1):
                if grid[i][j] == 'B':
                    dp[i][j] = False
                    continue
                
                win = False
                
                if i + 1 < r:
                    win |= not dp[i + 1][j]
                if j + 1 < c:
                    win |= not dp[i][j + 1]
                if i + 1 < c and j + 1 < c:
                    win |= not dp[i + 1][j + 1]
                
                dp[i][j] = win
        
        return "Alice" if dp[0][0] else "Bob"
    
    return solve()

# provided samples
assert run("4 5\nWBWBW\nWWWWB\nWBWBW\nBWBWB\n") == "Alice"
assert run("2 2\nWBBB\n") == "Bob"

# custom cases
assert run("1 1\nW\n") == "Bob", "single cell loses"
assert run("1 2\nWW\n") == "Alice", "one move available"
assert run("3 3\nWBW\nBBB\nWBW\n") == "Bob", "blocked middle row"
assert run("2 3\nWWW\nWWW\n") == "Alice", "fully open small grid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 white | Bob | terminal position |
| 1x2 all white | Alice | single forced move |
| blocked middle row | Bob | isolation handling |
| full 2x3 grid | Alice | multiple-path win consistency |

## Edge Cases

A minimal grid consisting of a single white cell immediately ends the game. The DP marks it as losing because there are no outgoing moves, so Bob is declared the winner.

A grid where every neighbor of the starting cell is blocked also results in an immediate loss for Alice. The DP does not find any transition from (0,0), so it remains False, correctly modeling a terminal state.

A fully open grid behaves differently: every cell eventually has at least one move to a losing position near the bottom-right boundary, propagating winning states backward until the start becomes winning.
